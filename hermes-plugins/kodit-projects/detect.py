"""Turn-time project detection for kodit-projects.

Cascade, strongest signal first:

1. GitHub URL in the message  → matches a project's ``github_repo``
2. Path tokens in the message  → equals/contains a registered ``working_dir``
3. Name/alias/slug words       → exact registry lookup (longest word first)
4. Session CWD                 → equals/contains a registered ``working_dir``
5. Content phrase              → >=2 message words all in ONE project's file index

Stages 1-3 are explicit user intent and beat ambient CWD (stage 4); stage 5 is
deliberately conservative so a stray sentence cannot hijack the wrong project.
Every stage returns the full project row or ``None``; failures never raise.
"""

from __future__ import annotations

import re
from typing import Any, Dict, List, Optional

try:
    from . import store
except ImportError:  # running as a script: python3 detect.py --selftest
    import store  # type: ignore

# words: >=2 chars, allow dotted/hyphenated identifiers (e.g. ``kodit-projects``)
_WORD_RE = re.compile(r"[A-Za-z0-9_][A-Za-z0-9_.-]{1,63}")
# path fragments: absolute (``/a/b``), home (``~/a``), relative (``a/b``), dot (``./a``)
_PATH_RE = re.compile(r"(?:~|\.{1,2})?/[\w.+/~-]+|[\w.+-]+(?:/[\w.+-]+)+")
_GH_RE = re.compile(r"github\.com[:/]([\w.-]+)/([\w.-]+?)(?:\.git)?(?:\s|/|$)", re.I)

# common message filler — excluded from word stages; exact FTS/alias lookups still work
_STOP = frozenset("""
the and for you your with that this have has was were are but not can all out
get got let its use using about into from who what when where why how please
just some any now then them they their there would could should will shall
been being does did doing done make made want need like also more most work
work's file files test tests code read see look here now ok yes no im i'm dont
don't didnt didn't does doesn't wont won't cant cant cant's its let's lets go
on in of to is it he she we us at by as if or so up down my me be been
""".split())


def _words(message: str) -> List[str]:
    """Message words, stop-filtered, deduped (original order kept)."""
    seen = set()
    out: List[str] = []
    for w in _WORD_RE.findall(message or ""):
        lw = w.lower()
        if len(w) >= 3 and lw not in _STOP and lw not in seen:
            seen.add(lw)
            out.append(w)
    return out


def _paths(message: str) -> List[str]:
    return [t for t in _PATH_RE.findall(message or "") if len(t) >= 2 and ":" not in t]


def _by_github(message: str, db_path=None) -> Optional[Dict[str, Any]]:
    m = _GH_RE.search(message or "")
    if not m:
        return None
    url = f"github.com/{m.group(1)}/{m.group(2)}".lower().rstrip("/")
    for project in store.list_projects(db_path=db_path):
        repo = str(project.get("github_repo") or "").lower().rstrip("/")
        if repo and (repo.endswith(url) or url.endswith(repo)):
            return project
    return None


def _by_content(words: List[str], db_path=None) -> Optional[Dict[str, Any]]:
    """Conservative: >=2 words, all hits confined to exactly one project."""
    if len(words) < 2:
        return None
    phrase = " ".join(words[:4])
    hits = store.search_files_global(phrase, limit=10, db_path=db_path)
    projs = {h["proj"] for h in hits}
    if len(projs) == 1:
        return store.get_project(projs.pop(), db_path=db_path)
    return None


def resolve(message: str, cwd: Optional[str] = None,
            db_path=None) -> Optional[Dict[str, Any]]:
    """Return the project this message is about, or ``None``."""
    try:
        hit = _by_github(message, db_path=db_path)
        if hit:
            return hit

        for token in _paths(message):
            hit = store.find_by_token(token, fuzzy=True, db_path=db_path)
            if hit:
                return hit

        # longest first so ``kodit-projects`` wins over its own short aliases
        for word in sorted(_words(message), key=len, reverse=True):
            hit = store.find_by_token(word, fuzzy=False, db_path=db_path)
            if hit:
                return hit

        if cwd:
            hit = store.project_for_cwd(cwd, db_path=db_path)
            if hit:
                return hit

        return _by_content(_words(message), db_path=db_path)
    except Exception:
        # detection must never break a turn
        return None


# -- selftest -----------------------------------------------------------------------------

def _selftest() -> None:
    import tempfile
    from pathlib import Path as P

    checks: List[str] = []

    def ok(label: str, cond: bool) -> None:
        if not cond:
            raise AssertionError(label)
        checks.append(label)

    with tempfile.TemporaryDirectory() as tmp:
        base = P(tmp)
        db_path = base / "projects.db"
        p1 = store.register_project(str(base / "alpha"), name="Alpha",
                                    summary="search indexer plugin",
                                    github_repo="https://github.com/me/alpha",
                                    db_path=db_path)
        p2 = store.register_project(str(base / "beta"), name="Beta", db_path=db_path)
        store.replace_file_index(p1["id"], [
            {"path": "docs/usage.md", "title": "usage", "body": "tokenize unicode61 body", "mtime": 1},
            {"path": "README.md", "title": "readme", "body": "alpha readme entry point", "mtime": 2},
        ], db_path=db_path)
        store.replace_file_index(p2["id"], [
            {"path": "main.py", "title": "main", "body": "entry point", "mtime": 1},
        ], db_path=db_path)

        ok("github url", resolve("see https://github.com/me/alpha", db_path=db_path)["id"] == p1["id"])
        ok("path token", resolve(f"open {base}/alpha/store.py", db_path=db_path)["id"] == p1["id"])
        ok("alias word", resolve("fix beta please", db_path=db_path)["id"] == p2["id"])
        ok("name word longest-first",
           resolve("work on alpha", db_path=db_path)["id"] == p1["id"])
        ok("explicit beats cwd",
           resolve("do this in beta", cwd=str(base / "alpha"), db_path=db_path)["id"] == p2["id"])
        ok("cwd fallback",
           resolve("fix the bug", cwd=str(base / "alpha" / "src"), db_path=db_path)["id"] == p1["id"])
        ok("cwd miss", resolve("fix the bug", cwd="/nope/elsewhere", db_path=db_path) is None)
        ok("content phrase single project",
           resolve("the unicode61 tokenize docs", db_path=db_path)["id"] == p1["id"])
        ok("content ambiguous -> none",
           resolve("entry point", db_path=db_path) is None)
        ok("no signal -> none", resolve("hello there", db_path=db_path) is None)
        ok("stopword-only -> none", resolve("the and for", db_path=db_path) is None)

    print(f"detect selftest: PASS ({len(checks)} checks)")


if __name__ == "__main__":
    import sys
    if "--selftest" in sys.argv:
        _selftest()
    else:
        print("usage: detect.py --selftest")
        sys.exit(2)
