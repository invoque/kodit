"""kodit-projects — project registry, FTS5 file index, per-turn context injection.

Data lives in ``store.py`` (SQLite at ``<HERMES_HOME>/plugin-data/kodit-projects/projects.db``).

Turn flow:
  * ``pre_llm_call`` resolves the active project from the message (explicit path /
    name / alias, then session CWD, then file-content match, then the session's
    sticky project) and returns a capped ``[project-context]`` block that Hermes
    appends to the user message.
  * a system-prompt section carries durable guidance, renders the session's
    working-dir project once, and records the session CWD.
  * ``on_session_start`` reindexes a stale project in the background.

Everything fails open: any exception logs a warning and injects nothing.
"""

from __future__ import annotations

import json
import logging
import os
import shlex
from collections import OrderedDict
from pathlib import Path
from typing import Any, Dict, Optional

try:
    from . import context as context_block, derive, detect, indexer, store
except ImportError:  # running as a script: python3 __init__.py --selftest
    import context as context_block  # type: ignore
    import derive, detect, indexer, store  # type: ignore

logger = logging.getLogger(__name__)

_SESSION_CAP = 64
_session_cwd: "OrderedDict[str, str]" = OrderedDict()       # session_id -> launch CWD
_session_project: "OrderedDict[str, str]" = OrderedDict()   # session_id -> sticky project id

_GUIDANCE = (
    'kodit-projects: the "[project-context] ..." block in the user message names the active '
    "project; its working dir and metadata are authoritative for this turn. Find files with the "
    "kodit_projects_search tool, read metadata with kodit_projects_show, and update fields with "
    'kodit_projects_set or /projects. Full workflow: skill "kodit-projects:projects".'
)

_USAGE = """usage:
  /projects register <path> [name]      register a project (derives summary/origin, indexes files)
  /projects list                        all registered projects
  /projects show [key]                  metadata (active project when key omitted)
  /projects set <key> <field> <value>   field: name|summary|description|linear_url|github_repo
  /projects alias <key> add|remove <alias>
  /projects index <key>                 reindex the project's files
  /projects forget <key>                remove the project and its index"""


def _remember(cache: "OrderedDict[str, str]", key: str, value: str) -> None:
    if not key:
        return
    cache[key] = value
    cache.move_to_end(key)
    while len(cache) > _SESSION_CAP:
        cache.popitem(last=False)


def _session_cwd_for(session_id: str, task_id: str = "") -> Optional[str]:
    """Best available CWD: recorded prompt-section cwd → terminal session cwd →
    task override → process CWD (CLI launch dir; harmless for gateways because a
    registered project only matches when CWD is inside it)."""
    cached = _session_cwd.get(session_id)
    if cached:
        return cached
    try:
        from tools.terminal_tool import get_session_cwd, resolve_task_overrides
    except Exception:
        return os.getcwd() or None
    for key in (session_id, task_id):
        if key:
            recorded = get_session_cwd(key)
            if recorded:
                return str(recorded)
    if task_id:
        cwd = (resolve_task_overrides(task_id) or {}).get("cwd")
        if cwd:
            return str(cwd)
    return os.getcwd() or None


# -- hooks ---------------------------------------------------------------------------------

def _on_pre_llm_call(**kw: Any) -> Optional[Dict[str, str]]:
    try:
        message = kw.get("user_message")
        message = message if isinstance(message, str) else ""
        sid = str(kw.get("session_id") or "")
        project = detect.resolve(message, cwd=_session_cwd_for(sid, str(kw.get("task_id") or "")))
        if project is None and sid and sid in _session_project:
            project = store.get_project(_session_project[sid])  # sticky standing context
        if project is None:
            return None
        if sid:
            _remember(_session_project, sid, project["id"])
        store.touch_session(project["id"])
        first = bool(kw.get("is_first_turn"))
        return {"context": context_block.build_block(
            project, first_turn=first,
            top_paths=store.top_paths(project["id"]) if first else None,
            file_total=store.file_count(project["id"]))}
    except Exception as exc:
        logger.warning("kodit-projects: pre_llm_call failed: %s", exc)
        return None


def _prompt_section(info: Any) -> str:
    try:
        data = dict(info or {})
        sid = str(data.get("session_id") or "")
        cwd = str(data.get("cwd") or "")
        if sid and cwd:
            _remember(_session_cwd, sid, cwd)
        if cwd:
            project = store.project_for_cwd(cwd)
            if project:
                return (f'Active project for this session working dir: "{project["name"]}" '
                        f"({project['working_dir']}).\n{_GUIDANCE}")
    except Exception as exc:
        logger.warning("kodit-projects: prompt section failed: %s", exc)
    return _GUIDANCE


def _on_session_start(**kw: Any) -> None:
    try:
        cwd = _session_cwd_for(str(kw.get("session_id") or ""), str(kw.get("task_id") or ""))
        if not cwd:
            return
        project = store.project_for_cwd(cwd)
        if project:
            indexer.maybe_refresh(project)
    except Exception as exc:
        logger.debug("kodit-projects: index refresh skipped: %s", exc)


# -- slash command -------------------------------------------------------------------------

def _fmt_project(p: Dict[str, Any]) -> str:
    lines = [f'{p["name"]} ({p["slug"]})',
             f'  dir: {p["working_dir"]}',
             f'  summary: {p["summary"] or "-"}']
    if p.get("linear_url"):
        lines.append(f'  linear: {p["linear_url"]}')
    if p.get("github_repo"):
        lines.append(f'  origin: {p["github_repo"]}')
    aliases = store.aliases_for(p["slug"])
    if aliases:
        lines.append("  aliases: " + ", ".join(aliases))
    indexed = "yes" if p.get("last_indexed_at") else "never"
    lines.append(f"  files: {store.file_count(p['id'])} (indexed: {indexed})")
    return "\n".join(lines)


def _cmd_register(args: list) -> str:
    if not args:
        return "usage: /projects register <path> [name ...]"
    root = os.path.abspath(os.path.expanduser(args[0]))
    if not os.path.isdir(root):
        return f"not a directory: {root}"
    project = store.register_project(
        root, name=" ".join(args[1:]) or derive.derive_name(root),
        summary=derive.derive_summary(root), github_repo=derive.derive_origin(root))
    n = indexer.index_project(project)
    return (f'registered "{project["name"]}" as {project["slug"]}\n'
            f'  dir: {project["working_dir"]}\n'
            f'  summary: {project["summary"] or "(none)"}\n'
            f'  origin: {project["github_repo"] or "(none)"}\n'
            f"  files indexed: {n}")


def _cmd_list() -> str:
    projects = store.list_projects()
    if not projects:
        return "no projects registered — /projects register <path>"
    return "\n".join(
        f'{p["slug"]:20} {p["name"]:24} {p["working_dir"]}' for p in projects)


def _cmd_show(args: list) -> str:
    if args:
        project = store.get_project(args[0])
        if project is None:
            return f"unknown project: {args[0]}"
        return _fmt_project(project)
    project = store.project_for_cwd(os.getcwd())
    if project is None:
        projects = store.list_projects()
        if not projects:
            return "no projects registered — /projects register <path>"
        project = max(projects, key=lambda p: p.get("last_session_at") or 0)
    return _fmt_project(project)


def _cmd_set(args: list) -> str:
    if len(args) < 3:
        return "usage: /projects set <key> <field> <value ...>"
    project = store.set_field(args[0], args[1].lower(), " ".join(args[2:]))
    return f'{project["slug"]}.{args[1].lower()} updated'


def _cmd_alias(args: list) -> str:
    if len(args) < 3 or args[1].lower() not in ("add", "remove"):
        return "usage: /projects alias <key> add|remove <alias>"
    if args[1].lower() == "add":
        store.add_alias(args[0], " ".join(args[2:]))
        return f'alias added to {args[0]}'
    removed = store.remove_alias(args[0], " ".join(args[2:]))
    return f"alias removed" if removed else f"alias not found for {args[0]}"


def _cmd_index(args: list) -> str:
    if not args:
        return "usage: /projects index <key>"
    project = store.get_project(args[0])
    if project is None:
        return f"unknown project: {args[0]}"
    n = indexer.index_project(project)
    return f'indexed {n} files for {project["slug"]}'


def _cmd_forget(args: list) -> str:
    if not args:
        return "usage: /projects forget <key>"
    if store.forget(args[0]):
        return f"forgot {args[0]} (registry and file index removed)"
    return f"unknown project: {args[0]}"


def _cmd(raw_args: Any) -> str:
    try:
        raw = str(raw_args or "")
        try:
            parts = shlex.split(raw)
        except ValueError:
            parts = raw.split()
        if not parts:
            return _USAGE
        sub, args = parts[0].lower().lstrip("/"), parts[1:]
        if sub in ("register", "add"):
            return _cmd_register(args)
        if sub == "list":
            return _cmd_list()
        if sub == "show":
            return _cmd_show(args)
        if sub == "set":
            return _cmd_set(args)
        if sub == "alias":
            return _cmd_alias(args)
        if sub == "index":
            return _cmd_index(args)
        if sub == "forget":
            return _cmd_forget(args)
        return _USAGE
    except Exception as exc:
        return f"kodit-projects error: {exc}"


# -- tools ---------------------------------------------------------------------------------

def _json(payload: Any) -> str:
    return json.dumps(payload, ensure_ascii=False, default=str)


def _tool_project(project: str, session_id: str = "") -> Optional[Dict[str, Any]]:
    """Explicit key → session's sticky project → project containing the process CWD."""
    if project:
        return store.get_project(project)
    pid = _session_project.get(str(session_id or ""))
    if pid:
        hit = store.get_project(pid)
        if hit:
            return hit
    return store.project_for_cwd(os.getcwd())


def _tool_search(args: Dict[str, Any], session_id: str = "", **_: Any) -> str:
    query = str(args.get("query") or "").strip()
    if not query:
        return _json({"error": "query is required"})
    limit = max(1, min(int(args.get("limit") or 10), 50))
    project = _tool_project(str(args.get("project") or ""), str(session_id or ""))
    if project is not None:
        return _json({"project": project["slug"],
                      "results": store.search_files(project["id"], query, limit)})
    names = {p["id"]: p["slug"] for p in store.list_projects()}
    hits = [{**r, "project": names.get(r["proj"], r["proj"])}
            for r in store.search_files_global(query, limit)]
    return _json({"results": hits})


def _tool_show(args: Dict[str, Any], session_id: str = "", **_: Any) -> str:
    project = _tool_project(str(args.get("project") or ""), str(session_id or ""))
    if project is None:
        projects = store.list_projects()
        if not projects:
            return _json({"error": "no projects registered; run /projects register <path>"})
        project = max(projects, key=lambda p: p.get("last_session_at") or 0)
    out = {k: project.get(k) for k in (
        "slug", "name", "description", "working_dir", "summary", "linear_url",
        "github_repo", "last_session_at", "last_indexed_at")}
    out["aliases"] = store.aliases_for(project["slug"])
    out["file_count"] = store.file_count(project["id"])
    return _json(out)


_SETTABLE = ("name", "summary", "description", "linear_url", "github_repo")


def _tool_set(args: Dict[str, Any], session_id: str = "", **_: Any) -> str:
    field = str(args.get("field") or "").lower()
    value = str(args.get("value") or "")
    project = _tool_project(str(args.get("project") or ""), str(session_id or ""))
    if project is None:
        return _json({"error": "project is required (no active project in this session)"})
    key = project["slug"]
    try:
        if field in _SETTABLE:
            updated = store.set_field(key, field, value)
            return _json({"ok": True, "slug": updated["slug"], field: updated[field]})
        if field == "alias_add":
            store.add_alias(key, value)
            return _json({"ok": True, "aliases": store.aliases_for(key)})
        if field == "alias_remove":
            store.remove_alias(key, value)
            return _json({"ok": True, "aliases": store.aliases_for(key)})
        return _json({"error": f"field must be one of {', '.join(_SETTABLE)}, "
                               f"alias_add, alias_remove"})
    except Exception as exc:
        return _json({"error": str(exc)})


_SEARCH_SCHEMA = {
    "name": "kodit_projects_search",
    "description": ("Full-text search over registered projects' file paths, titles, and "
                    "contents (SQLite FTS5). Without a project, searches all projects and "
                    "labels hits with their project slug."),
    "parameters": {
        "type": "object",
        "properties": {
            "query": {"type": "string", "description": "search terms"},
            "project": {"type": "string",
                        "description": "scope to one project (slug, name, or alias); "
                                       "defaults to the session's active project, else all"},
            "limit": {"type": "integer", "description": "max results (default 10, max 50)"},
        },
        "required": ["query"],
        "additionalProperties": False,
    },
}

_SHOW_SCHEMA = {
    "name": "kodit_projects_show",
    "description": ("Read one registered project's metadata (working dir, summary, Linear URL, "
                    "origin repo, aliases, file count). Omit project for the active one."),
    "parameters": {
        "type": "object",
        "properties": {
            "project": {"type": "string", "description": "slug, name, or alias; optional"},
        },
        "additionalProperties": False,
    },
}

_SET_SCHEMA = {
    "name": "kodit_projects_set",
    "description": ("Update a registered project's metadata or aliases. Use when the user "
                    "provides/corrects a project's summary, Linear URL, GitHub repo, or alias."),
    "parameters": {
        "type": "object",
        "properties": {
            "project": {"type": "string", "description": "slug, name, or alias; optional when "
                                                          "the session has an active project"},
            "field": {"type": "string",
                      "enum": [*_SETTABLE, "alias_add", "alias_remove"]},
            "value": {"type": "string", "description": "new value (or the alias for alias_*)"},
        },
        "required": ["field", "value"],
        "additionalProperties": False,
    },
}


# -- registration --------------------------------------------------------------------------

def register(ctx: Any) -> None:
    ctx.register_hook("pre_llm_call", _on_pre_llm_call)
    ctx.register_hook("on_session_start", _on_session_start)
    ctx.register_system_prompt_section("kodit-projects.context", _prompt_section)
    ctx.register_command("projects", _cmd,
                         description="Manage the project registry and file index",
                         args_hint="[register|list|show|set|alias|index|forget] [args]")
    ctx.register_tool(name="kodit_projects_search", toolset="kodit_projects",
                      schema=_SEARCH_SCHEMA, handler=_tool_search)
    ctx.register_tool(name="kodit_projects_show", toolset="kodit_projects",
                      schema=_SHOW_SCHEMA, handler=_tool_show)
    ctx.register_tool(name="kodit_projects_set", toolset="kodit_projects",
                      schema=_SET_SCHEMA, handler=_tool_set)
    skill = Path(__file__).parent / "skills" / "projects" / "SKILL.md"
    if skill.is_file():
        ctx.register_skill("projects", skill,
                           description="Using kodit-projects: register projects, search files, "
                                       "interpret [project-context] blocks, update metadata.")
    logger.info("kodit-projects: registered 2 hooks, 1 prompt section, 1 command, 3 tools")


# -- selftest ------------------------------------------------------------------------------

class _FakeCtx:
    def __init__(self) -> None:
        self.hooks: Dict[str, Any] = {}
        self.tools: Dict[str, Any] = {}
        self.commands: Dict[str, Any] = {}
        self.sections: Dict[str, Any] = {}
        self.skills: Dict[str, Any] = {}

    def register_hook(self, name, cb):
        self.hooks[name] = cb

    def register_tool(self, *, name, toolset, schema, handler, **_):
        self.tools[name] = (toolset, schema, handler)

    def register_command(self, name, handler, description="", args_hint=""):
        self.commands[name] = handler

    def register_system_prompt_section(self, id, content, **_):
        self.sections[id] = content

    def register_skill(self, name, path, description=""):
        self.skills[name] = str(path)


def _selftest() -> None:
    import tempfile

    checks = []

    def ok(label: str, cond: bool) -> None:
        if not cond:
            raise AssertionError(label)
        checks.append(label)

    _hermes_home = os.environ.get("HERMES_HOME")
    with tempfile.TemporaryDirectory() as tmp:
        os.environ["HERMES_HOME"] = tmp  # store falls back to $HERMES_HOME when Hermes isn't importable
        root = Path(tmp)
        proj = root / "regtest"
        proj.mkdir()
        (proj / "README.md").write_text("# Regtest\n\n> Regtest tagline summary line.\n")
        (proj / "notes.md").write_text("unique probe token lives here\n")

        ctx = _FakeCtx()
        register(ctx)
        ok("hooks wired", set(ctx.hooks) == {"pre_llm_call", "on_session_start"})
        ok("3 tools wired", set(ctx.tools) == {
            "kodit_projects_search", "kodit_projects_show", "kodit_projects_set"})
        ok("toolset", all(v[0] == "kodit_projects" for v in ctx.tools.values()))
        ok("schemas valid", all(
            v[1].get("name") == k and "description" in v[1]
            and v[1]["parameters"]["type"] == "object"
            and v[1]["parameters"].get("additionalProperties") is False
            for k, v in ctx.tools.items()))
        ok("command wired", "projects" in ctx.commands)
        ok("section wired", "kodit-projects.context" in ctx.sections)
        ok("skill wired", ctx.skills.get("projects", "").endswith("SKILL.md"))

        # command roundtrip
        cmd = ctx.commands["projects"]
        ok("usage on empty", "usage:" in cmd(""))
        out = cmd(f"register {proj}")
        ok("register", "registered" in out and "files indexed: 2" in out)
        ok("register derives tagline", "Regtest tagline summary line." in out)
        ok("list shows project", "regtest" in cmd("list"))
        ok("set field", "updated" in cmd("set regtest linear_url https://linear.app/x/y"))
        ok("show reflects set", "linear: https://linear.app/x/y" in cmd("show regtest"))
        ok("alias add", "alias added" in cmd("alias regtest add rt2"))
        ok("alias visible", "rt2" in cmd("show regtest"))
        ok("index cmd", "indexed 2 files" in cmd("index regtest"))
        ok("usage on bad set", "usage:" in cmd("set"))
        ok("bad field is error, not raise", "error:" in cmd("set regtest nofield value"))
        ok("unknown project handled", "unknown project" in cmd("show nope"))

        # tools
        search = json.loads(ctx.tools["kodit_projects_search"][2]({"query": "probe"}))
        ok("tool search global", search["results"][0]["path"] == "notes.md"
           and search["results"][0]["project"] == "regtest")
        scoped = json.loads(ctx.tools["kodit_projects_search"][2](
            {"query": "probe", "project": "rt2"}))
        ok("tool search scoped", scoped["project"] == "regtest")
        shown = json.loads(ctx.tools["kodit_projects_show"][2]({}))
        ok("tool show active", shown["slug"] == "regtest" and shown["file_count"] == 2
           and "rt2" in shown["aliases"])
        set_out = json.loads(ctx.tools["kodit_projects_set"][2](
            {"project": "regtest", "field": "summary", "value": "summary via tool"}))
        ok("tool set", set_out.get("ok") and set_out["summary"] == "summary via tool")
        bad = json.loads(ctx.tools["kodit_projects_set"][2]({"field": "nope", "value": "x"}))
        ok("tool set bad field", "error" in bad)

        # prompt section records cwd and names the project
        section = ctx.sections["kodit-projects.context"]
        text = section({"session_id": "t1", "cwd": str(proj)})
        ok("section names project", 'Active project for this session working dir: "regtest"' in text)
        ok("section carries guidance", "kodit_projects_search" in text)
        ok("section generic fallback", "kodit-projects:projects" in section({"session_id": "t2"}))

        # pre_llm_call: explicit name → block
        pre = ctx.hooks["pre_llm_call"]
        block = pre(user_message="tell me about regtest", is_first_turn=True,
                    session_id="t1", task_id="")["context"]
        ok("block marks project", '[project-context] active project "regtest"' in block)
        ok("block first-turn paths", "key paths: README.md, notes.md" in block)
        ok("block has tool hint", "kodit_projects_search" in block)

        # sticky: a session that matched once keeps its project with no new signal
        # (t4 has no cached cwd and the process CWD is not registered in this temp DB,
        # so only the sticky lookup can supply the project)
        _session_project["t4"] = store.get_project("regtest")["id"]
        block3 = pre(user_message="and also please check the other thing",
                     is_first_turn=False, session_id="t4", task_id="")
        ok("sticky keeps project", 'active project "regtest"' in block3["context"])
        ok("sticky on later turn omits paths", "key paths" not in block3["context"])

        # fresh session, no signal → no injection
        ok("no signal no injection",
           pre(user_message="hello there", is_first_turn=True,
               session_id="t-fresh", task_id="") is None)

        # forgetting clears the data the sticky lookup uses
        cmd("forget regtest")
        ok("sticky cleared after forget",
           pre(user_message="tell me about regtest", is_first_turn=False,
               session_id="t4", task_id="") is None)

    if _hermes_home is None:
        os.environ.pop("HERMES_HOME", None)
    else:
        os.environ["HERMES_HOME"] = _hermes_home
    print(f"plugin selftest: PASS ({len(checks)} checks)")


if __name__ == "__main__":
    import sys
    if "--selftest" in sys.argv:
        _selftest()
    else:
        print("usage: __init__.py --selftest")
        sys.exit(2)
