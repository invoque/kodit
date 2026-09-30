"""Filesystem walk → FTS5 index rows for one registered project.

Walk policy: skip generated/vendor trees and binaries, cap file size and total
count, index only a bounded text prefix. The whole walk is bounded so it can run
inside the 30s ``on_session_start`` hook timeout.
"""

from __future__ import annotations

import os
import stat
from typing import Any, Dict, List, Optional

try:
    from . import store
except ImportError:  # running as a script: python3 indexer.py --selftest
    import store  # type: ignore

SKIP_DIRS = frozenset({
    ".git", "node_modules", "__pycache__", ".venv", "venv", "dist", "build",
    ".cache", ".tox", ".mypy_cache", ".pytest_cache", ".ruff_cache", ".eggs",
    ".next", ".nuxt", ".gradle", "target", "vendor", ".idea", ".vscode",
})
MAX_FILES = 5000
MAX_BYTES = 512 * 1024
READ_BYTES = 16384
HEAD_BYTES = 8192


def _title(filename: str, text: str) -> str:
    """Markdown heading if the file opens with one, else the file name."""
    for line in text.splitlines()[:12]:
        s = line.strip()
        if s.startswith("#"):
            return s.lstrip("#").strip()[:120] or filename
        if s:
            break  # a heading, when present, comes first — don't scan past real content
    return filename


def iter_rows(root: str) -> List[Dict[str, Any]]:
    """Walk ``root`` into ``{path, title, body, mtime}`` rows (path is repo-relative, ``/``-separated)."""
    rows: List[Dict[str, Any]] = []
    root = os.path.abspath(str(root))
    if not os.path.isdir(root):
        return rows
    for dirpath, dirnames, filenames in os.walk(root):
        rel_dir = os.path.relpath(dirpath, root)
        dirnames[:] = [
            d for d in sorted(dirnames)
            if d not in SKIP_DIRS and not (rel_dir == ".kodit" and d == "tmp")
        ]
        for name in sorted(filenames):
            if len(rows) >= MAX_FILES:
                return rows
            path = os.path.join(dirpath, name)
            try:
                if os.path.islink(path):
                    continue  # never index outside the project root
                st = os.stat(path)
                if not stat.S_ISREG(st.st_mode) or st.st_size > MAX_BYTES:
                    continue
                with open(path, "rb") as fh:
                    data = fh.read(READ_BYTES)
            except OSError:
                continue
            if b"\x00" in data[:HEAD_BYTES]:
                continue  # binary
            text = data.decode("utf-8", errors="replace")
            rel = os.path.relpath(path, root).replace(os.sep, "/")
            rows.append({
                "path": rel,
                "title": _title(name, text),
                "body": text[:8000],
                "mtime": int(st.st_mtime),
            })
    return rows


def index_project(project: Dict[str, Any], db_path: Optional[str] = None) -> int:
    """(Re)build the project's whole file index; returns indexed file count."""
    return store.replace_file_index(project["id"], iter_rows(project["working_dir"]),
                                    db_path=db_path)


def maybe_refresh(project: Dict[str, Any], db_path: Optional[str] = None,
                  max_age: int = store.DEFAULT_MAX_AGE) -> bool:
    """Reindex when stale (>max_age old or working_dir newer than the index)."""
    if store.is_index_stale(project["id"], max_age=max_age, db_path=db_path):
        index_project(project, db_path=db_path)
        return True
    return False


# -- selftest -----------------------------------------------------------------------------

def _selftest() -> None:
    global MAX_FILES, MAX_BYTES
    import tempfile
    from pathlib import Path as P

    checks: List[str] = []

    def ok(label: str, cond: bool) -> None:
        if not cond:
            raise AssertionError(label)
        checks.append(label)

    with tempfile.TemporaryDirectory() as tmp:
        base = P(tmp)
        proj = base / "proj"
        (proj / "src").mkdir(parents=True)
        (proj / "src" / "app.py").write_text("def run():\n    return 1\n")
        (proj / "README.md").write_text("# My Project\n\nBody text here.\n")
        (proj / "node_modules").mkdir()
        (proj / "node_modules" / "junk.js").write_text("skip me")
        (proj / ".git").mkdir()
        (proj / ".git" / "config").write_text("skip me")
        (proj / ".kodit" / "tmp").mkdir(parents=True)
        (proj / ".kodit" / "tmp" / "spec.md").write_text("skip me")
        (proj / "logo.png").write_bytes(b"\x89PNG\x00\x00binary")
        (proj / "big.txt").write_text("y" * (512 * 1024 + 1))

        rows = iter_rows(str(proj))
        paths = [r["path"] for r in rows]
        ok("walks nested files", "src/app.py" in paths and "README.md" in paths)
        ok("skips vendor", not any("node_modules" in p for p in paths))
        ok("skips .git", not any(p.startswith(".git") for p in paths))
        ok("skips .kodit/tmp", not any(".kodit/tmp" in p for p in paths))
        ok("skips binary", "logo.png" not in paths)
        ok("skips oversized", "big.txt" not in paths)
        ok("markdown title", next(r for r in rows if r["path"] == "README.md")["title"] == "My Project")
        ok("filename fallback title",
           next(r for r in rows if r["path"] == "src/app.py")["title"] == "app.py")
        ok("mtime recorded", next(r for r in rows if r["path"] == "README.md")["mtime"] > 0)

        old = MAX_FILES
        MAX_FILES = 1
        try:
            ok("file cap enforced", len(iter_rows(str(proj))) == 1)
        finally:
            MAX_FILES = old

        # db outside the project root: a db inside working_dir would bump dir mtime
        # on every index write and report permanent staleness
        db_path = base / "db" / "projects.db"
        p = store.register_project(str(proj), name="Idx Test", db_path=db_path)
        n = index_project(p, db_path=db_path)
        ok("index_project count", n == len(rows) and n > 0)
        ok("search after index",
           store.search_files(p["id"], "return", db_path=db_path)[0]["path"] == "src/app.py")
        ok("fresh not stale", not maybe_refresh(p, db_path=db_path))

        (proj / "extra.md").write_text("brand new file content")
        ok("dir mtime change triggers reindex", maybe_refresh(p, db_path=db_path))
        ok("reindexed", store.search_files(p["id"], "brand", db_path=db_path)[0]["path"] == "extra.md")

    print(f"indexer selftest: PASS ({len(checks)} checks)")


if __name__ == "__main__":
    import sys
    if "--selftest" in sys.argv:
        _selftest()
    else:
        print("usage: indexer.py --selftest")
        sys.exit(2)
