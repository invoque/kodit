"""kodit-projects store — registry + FTS5 file index for Hermes plugin.

Persistence lives in the official per-plugin location
``<HERMES_HOME>/plugin-data/kodit-projects/projects.db`` (WAL, foreign keys on).
Run ``python3 store.py --selftest`` to exercise every public routine.
"""

from __future__ import annotations

import os
import re
import secrets
import sqlite3
import sys
import tempfile
import time
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

PLUGIN_NAME = "kodit-projects"
DEFAULT_MAX_AGE = 86400  # index older than 24h counts as stale

_SLUG_RE = re.compile(r"^[a-z0-9][a-z0-9\-_]{0,63}$")
_FIELD_RE = re.compile(r"[^a-z0-9]+")
_SETTABLE = ("name", "summary", "description", "linear_url", "github_repo")

_SCHEMA = """
CREATE TABLE IF NOT EXISTS projects (
    id              TEXT PRIMARY KEY,
    slug            TEXT NOT NULL UNIQUE,
    name            TEXT NOT NULL,
    description     TEXT NOT NULL DEFAULT '',
    working_dir     TEXT NOT NULL UNIQUE,
    summary         TEXT NOT NULL DEFAULT '',
    linear_url      TEXT NOT NULL DEFAULT '',
    github_repo     TEXT NOT NULL DEFAULT '',
    created_at      INTEGER NOT NULL,
    last_session_at INTEGER,
    last_indexed_at INTEGER
);
CREATE TABLE IF NOT EXISTS aliases (
    project_id TEXT NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    alias      TEXT NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS files (
    project_id TEXT NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    path       TEXT NOT NULL,
    mtime      INTEGER NOT NULL DEFAULT 0,
    PRIMARY KEY (project_id, path)
);
CREATE VIRTUAL TABLE IF NOT EXISTS files_fts
    USING fts5(proj, path, title, body, tokenize='unicode61');
CREATE VIRTUAL TABLE IF NOT EXISTS registry_fts
    USING fts5(proj, text, tokenize='unicode61');
"""


# -- paths / connection -------------------------------------------------------------------

def default_db_path() -> Path:
    """Prefer the official ``plugin_data_dir`` helper; fall back to the same location built manually."""
    try:
        from plugins.plugin_storage import plugin_data_dir  # type: ignore
        return plugin_data_dir(PLUGIN_NAME) / "projects.db"
    except Exception:
        home = Path(os.environ.get("HERMES_HOME") or Path.home() / ".hermes")
        path = home / "plugin-data" / PLUGIN_NAME / "projects.db"
        path.parent.mkdir(parents=True, exist_ok=True)
        return path


def connect(db_path: Optional[Path] = None) -> sqlite3.Connection:
    path = Path(db_path) if db_path is not None else default_db_path()
    if str(path) != ":memory:":
        path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(path), check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    conn.executescript(_SCHEMA)
    return conn


@contextmanager
def db(db_path: Optional[Path] = None):
    conn = connect(db_path)
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


# -- helpers ------------------------------------------------------------------------------

def _now() -> int:
    return int(time.time())


def _now_f() -> float:
    """Sub-second index timestamps: getmtime() has sub-second precision, so
    comparing it against a whole-second index time is flaky."""
    return time.time()


def _norm_dir(path: str) -> str:
    return os.path.abspath(os.path.expanduser(str(path).strip())).rstrip("/\\") or "/"


def _slugify(name: str) -> str:
    s = _FIELD_RE.sub("-", str(name).strip().lower()).strip("-_")
    return s[:64].strip("-_") or "project"


def _fts_query(query: str) -> Optional[str]:
    """Quote user input as FTS5 literal terms; None when nothing searchable remains."""
    terms = re.findall(r"[A-Za-z0-9_./-]+", str(query or ""))
    return " ".join(f'"{t}"' for t in terms if t) or None


def _row(conn: sqlite3.Connection, sql: str, args: tuple) -> Optional[Dict[str, Any]]:
    r = conn.execute(sql, args).fetchone()
    return dict(r) if r else None


def _refresh_registry_fts(conn: sqlite3.Connection, project_id: str) -> None:
    row = conn.execute(
        "SELECT p.id, p.slug, p.name, p.summary, p.description, "
        "GROUP_CONCAT(a.alias, ' ') AS aliases "
        "FROM projects p LEFT JOIN aliases a ON a.project_id = p.id "
        "WHERE p.id = ? GROUP BY p.id", (project_id,)).fetchone()
    conn.execute("DELETE FROM registry_fts WHERE proj = ?", (project_id,))
    if row:
        text = " ".join(str(x) for x in dict(row).values() if x)
        conn.execute("INSERT INTO registry_fts(proj, text) VALUES (?, ?)", (project_id, text))


def _unique_slug(conn: sqlite3.Connection, base: str) -> str:
    slug, n = base, 1
    while conn.execute("SELECT 1 FROM projects WHERE slug = ?", (slug,)).fetchone():
        n += 1
        slug = f"{base[:60]}-{n}"
    return slug


def _get(conn: sqlite3.Connection, key: str) -> Optional[Dict[str, Any]]:
    """Resolve id, slug, name, alias, or working_dir (case-insensitive where textual)."""
    key = str(key or "").strip()
    if not key:
        return None
    hit = _row(conn, "SELECT * FROM projects WHERE id = ? OR slug = ?", (key, key.lower()))
    if hit:
        return hit
    hit = _row(conn, "SELECT p.* FROM projects p JOIN aliases a ON a.project_id = p.id "
                     "WHERE lower(a.alias) = ?", (key.lower(),))
    if hit:
        return hit
    hit = _row(conn, "SELECT * FROM projects WHERE lower(name) = ?", (key.lower(),))
    return hit or None


# -- registry CRUD ------------------------------------------------------------------------

def register_project(path: str, name: Optional[str] = None, summary: str = "",
                     description: str = "", linear_url: str = "",
                     github_repo: str = "", aliases: Iterable[str] = (),
                     db_path: Optional[Path] = None) -> Dict[str, Any]:
    working_dir = _norm_dir(path)
    with db(db_path) as conn:
        if conn.execute("SELECT 1 FROM projects WHERE working_dir = ?", (working_dir,)).fetchone():
            raise ValueError(f"working_dir already registered: {working_dir}")
        display = (name or "").strip() or Path(working_dir).name
        slug = _unique_slug(conn, _slugify(display))
        project = {
            "id": f"{slug}-{secrets.token_hex(3)}", "slug": slug, "name": display,
            "description": description or "", "working_dir": working_dir,
            "summary": summary or "", "linear_url": linear_url or "",
            "github_repo": github_repo or "", "created_at": _now(),
            "last_session_at": None, "last_indexed_at": None,
        }
        conn.execute(
            "INSERT INTO projects(id, slug, name, description, working_dir, summary, "
            "linear_url, github_repo, created_at) VALUES "
            "(:id, :slug, :name, :description, :working_dir, :summary, "
            ":linear_url, :github_repo, :created_at)", project)
        for alias in sorted({slug, display.lower(), *(str(a).strip().lower() for a in aliases)}):
            alias = alias.strip()
            if alias and not conn.execute("SELECT 1 FROM aliases WHERE alias = ?", (alias,)).fetchone():
                conn.execute("INSERT INTO aliases(project_id, alias) VALUES (?, ?)",
                             (project["id"], alias))
        _refresh_registry_fts(conn, project["id"])
        return project


def get_project(key: str, db_path: Optional[Path] = None) -> Optional[Dict[str, Any]]:
    with db(db_path) as conn:
        return _get(conn, key)


def list_projects(db_path: Optional[Path] = None) -> List[Dict[str, Any]]:
    with db(db_path) as conn:
        return [dict(r) for r in conn.execute("SELECT * FROM projects ORDER BY name")]


def aliases_for(key: str, db_path: Optional[Path] = None) -> List[str]:
    with db(db_path) as conn:
        project = _get(conn, key)
        if not project:
            return []
        return [r["alias"] for r in conn.execute(
            "SELECT alias FROM aliases WHERE project_id = ? ORDER BY alias",
            (project["id"],))]


def set_field(key: str, field: str, value: str, db_path: Optional[Path] = None) -> Dict[str, Any]:
    if field not in _SETTABLE:
        raise ValueError(f"field must be one of {_SETTABLE}, got {field!r}")
    with db(db_path) as conn:
        project = _get(conn, key)
        if not project:
            raise ValueError(f"unknown project: {key!r}")
        conn.execute(f"UPDATE projects SET {field} = ? WHERE id = ?", (str(value), project["id"]))
        _refresh_registry_fts(conn, project["id"])
        return dict(conn.execute("SELECT * FROM projects WHERE id = ?",
                                 (project["id"],)).fetchone())


def add_alias(key: str, alias: str, db_path: Optional[Path] = None) -> None:
    alias = str(alias).strip().lower()
    if not alias:
        raise ValueError("alias must be non-empty")
    with db(db_path) as conn:
        project = _get(conn, key)
        if not project:
            raise ValueError(f"unknown project: {key!r}")
        owner = conn.execute("SELECT project_id FROM aliases WHERE alias = ?", (alias,)).fetchone()
        if owner:
            if owner["project_id"] == project["id"]:
                return
            raise ValueError(f"alias {alias!r} already used by another project")
        conn.execute("INSERT INTO aliases(project_id, alias) VALUES (?, ?)",
                     (project["id"], alias))
        _refresh_registry_fts(conn, project["id"])


def remove_alias(key: str, alias: str, db_path: Optional[Path] = None) -> bool:
    with db(db_path) as conn:
        project = _get(conn, key)
        if not project:
            raise ValueError(f"unknown project: {key!r}")
        cur = conn.execute("DELETE FROM aliases WHERE project_id = ? AND alias = ?",
                           (project["id"], str(alias).strip().lower()))
        if cur.rowcount:
            _refresh_registry_fts(conn, project["id"])
        return bool(cur.rowcount)


def forget(key: str, db_path: Optional[Path] = None) -> bool:
    with db(db_path) as conn:
        project = _get(conn, key)
        if not project:
            return False
        conn.execute("DELETE FROM registry_fts WHERE proj = ?", (project["id"],))
        conn.execute("DELETE FROM files_fts WHERE proj = ?", (project["id"],))
        conn.execute("DELETE FROM projects WHERE id = ?", (project["id"],))
        return True


def touch_session(key: str, db_path: Optional[Path] = None) -> None:
    with db(db_path) as conn:
        project = _get(conn, key)
        if project:
            conn.execute("UPDATE projects SET last_session_at = ? WHERE id = ?",
                         (_now(), project["id"]))


# -- lookup -------------------------------------------------------------------------------

def project_for_cwd(cwd: str, db_path: Optional[Path] = None) -> Optional[Dict[str, Any]]:
    """Registered project whose working_dir equals or contains cwd; longest match wins."""
    try:
        target = _norm_dir(cwd)
    except Exception:
        return None
    with db(db_path) as conn:
        best: Optional[Dict[str, Any]] = None
        for row in conn.execute("SELECT * FROM projects"):
            root = row["working_dir"]
            if target == root or target.startswith(root + os.sep):
                if best is None or len(root) > len(best["working_dir"]):
                    best = dict(row)
        return best


def find_by_token(token: str, db_path: Optional[Path] = None,
                  fuzzy: bool = True) -> Optional[Dict[str, Any]]:
    """Cascade: path token → exact slug/alias/name → registry FTS → LIKE.

    ``fuzzy=False`` stops after the exact/FTS steps; turn-time detection uses it so
    common words cannot substring-match an unrelated project name.
    """
    token = str(token or "").strip()
    if not token:
        return None
    with db(db_path) as conn:
        if token.startswith(("/", "~")) or "/" in token:
            hit = project_for_cwd(token, db_path=db_path)
            if hit:
                return hit
        hit = _get(conn, token)
        if hit:
            return hit
        fts = _fts_query(token)
        if fts:
            row = conn.execute(
                "SELECT proj FROM registry_fts WHERE registry_fts MATCH ? LIMIT 1",
                (fts,)).fetchone()
            if row:
                hit = _get(conn, row["proj"])
                if hit:
                    return hit
        if not fuzzy:
            return None
        row = conn.execute(
            "SELECT id FROM projects WHERE lower(name) LIKE ? OR lower(slug) LIKE ? "
            "LIMIT 1", (f"%{token.lower()}%", f"%{token.lower()}%")).fetchone()
        if row:
            return _get(conn, row["id"])
        row = conn.execute(
            "SELECT project_id FROM aliases WHERE alias LIKE ? LIMIT 1",
            (f"%{token.lower()}%",)).fetchone()
        if row:
            return _get(conn, row["project_id"])
    return None


# -- file index ---------------------------------------------------------------------------

def replace_file_index(project_id: str, rows: Iterable[Dict[str, Any]],
                       db_path: Optional[Path] = None) -> int:
    """Replace the project's whole index. rows: {path, title, body, mtime}."""
    rows = list(rows)
    with db(db_path) as conn:
        if not conn.execute("SELECT 1 FROM projects WHERE id = ?", (project_id,)).fetchone():
            raise ValueError(f"unknown project id: {project_id!r}")
        conn.execute("DELETE FROM files WHERE project_id = ?", (project_id,))
        conn.execute("DELETE FROM files_fts WHERE proj = ?", (project_id,))
        for r in rows:
            conn.execute("INSERT INTO files(project_id, path, mtime) VALUES (?, ?, ?)",
                         (project_id, r["path"], int(r.get("mtime") or 0)))
            conn.execute("INSERT INTO files_fts(proj, path, title, body) VALUES (?, ?, ?, ?)",
                         (project_id, r["path"], r.get("title") or "",
                          (r.get("body") or "")[:8000]))
        conn.execute("UPDATE projects SET last_indexed_at = ? WHERE id = ?",
                     (_now_f(), project_id))
    return len(rows)


def search_files(project_id: str, query: str, limit: int = 20,
                 db_path: Optional[Path] = None) -> List[Dict[str, Any]]:
    fts = _fts_query(query)
    if not fts:
        return []
    with db(db_path) as conn:
        rows = conn.execute(
            "SELECT path, title, snippet(files_fts, 3, '[', ']', '...', 12) AS snip "
            "FROM files_fts WHERE files_fts MATCH ? AND proj = ? LIMIT ?",
            (fts, project_id, max(1, min(int(limit), 100)))).fetchall()
        return [dict(r) for r in rows]


def file_count(project_id: str, db_path: Optional[Path] = None) -> int:
    with db(db_path) as conn:
        row = conn.execute("SELECT COUNT(*) AS n FROM files WHERE project_id = ?",
                           (project_id,)).fetchone()
        return int(row["n"]) if row else 0


def top_paths(project_id: str, limit: int = 6,
              db_path: Optional[Path] = None) -> List[str]:
    """Shallowest-path sample for the first-turn context block (README.md before
    deep/nested/file.md — depth first, alphabetical within a depth)."""
    with db(db_path) as conn:
        return [r["path"] for r in conn.execute(
            "SELECT path FROM files WHERE project_id = ? "
            "ORDER BY (LENGTH(path) - LENGTH(REPLACE(path, '/', ''))), path LIMIT ?",
            (project_id, max(1, int(limit))))]


def search_files_global(query: str, limit: int = 10,
                        db_path: Optional[Path] = None) -> List[Dict[str, Any]]:
    """FTS across every project's index: [{proj, path, title, snip}].

    Used by detection (>=2 message words matching one project's files) and by the
    search tool when no project scope was given.
    """
    fts = _fts_query(query)
    if not fts:
        return []
    with db(db_path) as conn:
        rows = conn.execute(
            "SELECT proj, path, title, snippet(files_fts, 3, '[', ']', '...', 12) AS snip "
            "FROM files_fts WHERE files_fts MATCH ? LIMIT ?",
            (fts, max(1, min(int(limit), 100)))).fetchall()
        return [dict(r) for r in rows]


def is_index_stale(project_id: str, max_age: int = DEFAULT_MAX_AGE,
                   db_path: Optional[Path] = None) -> bool:
    with db(db_path) as conn:
        row = conn.execute(
            "SELECT p.last_indexed_at, p.working_dir, "
            "(SELECT MAX(mtime) FROM files f WHERE f.project_id = p.id) AS newest "
            "FROM projects p WHERE p.id = ?", (project_id,)).fetchone()
        if not row:
            return False
        if row["last_indexed_at"] is None:
            return True
        indexed = float(row["last_indexed_at"])
        if time.time() - indexed > max_age:
            return True
        try:
            return os.path.getmtime(row["working_dir"]) > indexed
        except OSError:
            return False


# -- selftest -----------------------------------------------------------------------------

def _selftest() -> None:
    from pathlib import Path as P
    checks: List[str] = []

    def ok(label: str, cond: bool) -> None:
        if not cond:
            raise AssertionError(label)
        checks.append(label)

    with tempfile.TemporaryDirectory() as tmp:
        base = P(tmp)
        db_path = base / "projects.db"
        conn = connect(db_path)
        ok("fts5 available", conn.execute(
            "SELECT 1 FROM files_fts WHERE files_fts MATCH 'x'").fetchall() is not None)
        conn.close()

        p1 = register_project(str(base / "proj-one"), name="Kodit One",
                              summary="A test project", db_path=db_path)
        ok("slug derived", p1["slug"] == "kodit-one")
        ok("alias auto (slug+name)",
           get_project("Kodit One", db_path=db_path)["id"] == p1["id"]
           and get_project("kodit-one", db_path=db_path)["id"] == p1["id"])
        try:
            register_project(str(base / "proj-one"), db_path=db_path)
            ok("duplicate working_dir rejected", False)
        except ValueError:
            ok("duplicate working_dir rejected", True)

        nested = str(base / "proj-one" / "src" / "deep")
        ok("project_for_cwd nested", project_for_cwd(nested, db_path=db_path)["id"] == p1["id"])
        ok("project_for_cwd miss", project_for_cwd("/tmp/elsewhere", db_path=db_path) is None)
        ok("find_by_token path", find_by_token(str(base / "proj-one"), db_path=db_path)["id"] == p1["id"])
        ok("find_by_token alias", find_by_token("kodit", db_path=db_path)["id"] == p1["id"])
        ok("find_by_token miss", find_by_token("no-such-project-zzz", db_path=db_path) is None)

        n = replace_file_index(p1["id"], [
            {"path": "src/main.py", "title": "main.py", "body": "def main(): run()", "mtime": 1},
            {"path": "README.md", "title": "Readme",
             "body": "# Kodit One\nThe project summary lives here.", "mtime": 2},
            {"path": "a/b/c.md", "title": "c", "body": "deep nested doc", "mtime": 3},
        ], db_path=db_path)
        ok("index replaced (3)", n == 3)
        ok("search file path", search_files(p1["id"], "main", db_path=db_path)[0]["path"] == "src/main.py")
        ok("search file body", search_files(p1["id"], "summary", db_path=db_path)[0]["path"] == "README.md")
        ok("search miss", search_files(p1["id"], "quantum-tunnel", db_path=db_path) == [])
        ok("file_count", file_count(p1["id"], db_path=db_path) == 3)
        ok("index fresh", not is_index_stale(p1["id"], max_age=10**9, db_path=db_path))

        updated = set_field("kodit-one", "summary", "brand-new phrase for match", db_path=db_path)
        ok("set_field", updated["summary"] == "brand-new phrase for match")
        ok("registry fts refreshed",
           find_by_token("brand-new", db_path=db_path)["id"] == p1["id"])
        add_alias("kodit-one", "k1", db_path=db_path)
        ok("add_alias", find_by_token("k1", db_path=db_path)["id"] == p1["id"])
        ok("aliases_for", aliases_for("kodit-one", db_path=db_path) == ["k1", "kodit one", "kodit-one"])
        ok("remove_alias", remove_alias("kodit-one", "k1", db_path=db_path)
           and find_by_token("k1", db_path=db_path) is None)

        touch_session("kodit-one", db_path=db_path)
        ok("touch_session", get_project("kodit-one", db_path=db_path)["last_session_at"] is not None)

        with db(db_path) as conn:
            conn.execute("UPDATE projects SET last_indexed_at = 1 WHERE id = ?", (p1["id"],))
        ok("stale detected", is_index_stale(p1["id"], max_age=10**9, db_path=db_path))

        ok("top_paths shallowest first",
           top_paths(p1["id"], db_path=db_path) ==
           ["README.md", "src/main.py", "a/b/c.md"])
        ok("search_files_global hit",
           search_files_global("summary lives", db_path=db_path)[0]["proj"] == p1["id"])
        ok("search_files_global miss",
           search_files_global("quantum-tunnel", db_path=db_path) == [])
        ok("find_by_token strict skips LIKE",
           find_by_token("odit", fuzzy=False, db_path=db_path) is None
           and find_by_token("odit", fuzzy=True, db_path=db_path)["id"] == p1["id"])

        ok("forget", forget("kodit-one", db_path=db_path)
           and get_project("kodit-one", db_path=db_path) is None)
        ok("cascade files", file_count(p1["id"], db_path=db_path) == 0)
        ok("forget unknown is False", not forget("ghost", db_path=db_path))

    print(f"selftest: PASS ({len(checks)} checks)")


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        _selftest()
    else:
        print("usage: store.py --selftest")
        sys.exit(2)
