"""Auto-derive register() metadata from a project's own files.

Summary priority (most trustworthy first): README first paragraph →
CONTEXT.md Identity "Tagline" row → ``kodit.json`` description.
Also derives the display name from ``kodit.json`` and the origin repository
URL from ``git remote get-url origin`` (normalized to ``https://host/owner/repo``).
Everything is best-effort: missing files, no git, or parse errors yield ``""``.
"""

from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path
from typing import Optional

_TAGLINE_RE = re.compile(r"\|\s*\*{0,2}tagline\*{0,2}\s*\|\s*([^|]+?)\s*\|", re.I)

_SKIP = ("#", "!", "[", "|", "-", "*", "<", "```")


def _cap(s: str, max_len: int = 300) -> str:
    s = " ".join(s.split())
    return s if len(s) <= max_len else s[:max_len].rsplit(" ", 1)[0] + "…"


def _read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def _first_paragraph(text: str, max_len: int = 300) -> str:
    """First content of a README: an early blockquote (the tagline slot) or the
    first prose block. Headings, badges, lists, tables, HTML, and fences are skipped."""
    lines = [ln.strip() for ln in text.splitlines()[:40]]
    i = 0
    while i < len(lines):
        s = lines[i]
        if s.startswith(">"):
            parts = []
            while i < len(lines) and lines[i].startswith(">"):
                parts.append(lines[i].lstrip(">").strip())
                i += 1
            quote = _cap(" ".join(p for p in parts if p), max_len)
            if quote and not quote.startswith(("!", "[")):  # skip badge/alert runs
                return quote
            continue
        i += 1
        if not s or s.startswith(_SKIP):
            continue
        block = [s]
        while i < len(lines):
            nxt = lines[i]
            if not nxt or nxt.startswith(">") or nxt.startswith(_SKIP):
                break
            block.append(nxt)
            i += 1
        return _cap(" ".join(block), max_len)
    return ""


def _kodit_json(root: Path) -> dict:
    try:
        data = json.loads(_read(Path(root) / "kodit.json"))
        return data if isinstance(data, dict) else {}
    except ValueError:
        return {}


def derive_summary(root: str) -> str:
    root = Path(root)
    for source in ("README.md", "readme.md", "README", "README.txt"):
        summary = _first_paragraph(_read(root / source))
        if summary:
            return summary
    m = _TAGLINE_RE.search(_read(root / "CONTEXT.md"))
    if m:
        return m.group(1).strip().strip("`")[:300]
    data = _kodit_json(root)
    proj = data.get("project") if isinstance(data.get("project"), dict) else {}
    return str(proj.get("description") or data.get("description") or "").strip()[:300]


def derive_name(root: str) -> Optional[str]:
    data = _kodit_json(Path(root))
    proj = data.get("project") if isinstance(data.get("project"), dict) else {}
    name = proj.get("name") or data.get("name")
    return str(name).strip() if isinstance(name, str) and name.strip() else None


def origin_url(raw: str) -> str:
    """Normalize a git remote URL to ``https://host/owner/repo`` ('' when unparseable)."""
    url = str(raw or "").strip()
    if not url:
        return ""
    m = re.match(r"git@([^:]+):(.+?)(?:\.git)?$", url)
    if m:
        return f"https://{m.group(1)}/{m.group(2).strip('/')}"
    m = re.match(r"ssh://(?:git@)?([^/]+)/(.+?)(?:\.git)?$", url)
    if m:
        return f"https://{m.group(1)}/{m.group(2).strip('/')}"
    m = re.match(r"https?://(.+?)(?:\.git)?$", url)
    if m:
        return f"https://{m.group(1).rstrip('/')}"
    return ""


def derive_origin(root: str) -> str:
    """``git remote get-url origin`` → normalized https URL (no origin / no git → "")."""
    try:
        out = subprocess.run(
            ["git", "-C", str(root), "remote", "get-url", "origin"],
            capture_output=True, text=True, timeout=3)
        if out.returncode != 0:
            return ""
        return origin_url(out.stdout)
    except (OSError, subprocess.SubprocessError):
        return ""


# -- selftest -----------------------------------------------------------------------------

def _selftest() -> None:
    import tempfile

    checks = []

    def ok(label: str, cond: bool) -> None:
        if not cond:
            raise AssertionError(label)
        checks.append(label)

    ok("ssh scp form", origin_url("git@github.com:me/repo.git") == "https://github.com/me/repo")
    ok("ssh url form", origin_url("ssh://git@github.com/me/repo.git") == "https://github.com/me/repo")
    ok("https form", origin_url("https://github.com/me/repo.git") == "https://github.com/me/repo")
    ok("https no .git", origin_url("https://github.com/me/repo") == "https://github.com/me/repo")
    ok("garbage -> ''", origin_url("not a url") == "")

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "README.md").write_text(
            "# Title\n[![badge](https://x/y.svg)](https://x)\n\nReal summary line here.\n")
        ok("readme paragraph wins",
           derive_summary(str(root)) == "Real summary line here.")

        (root / "README.md").write_text(
            "# Title\n\n> Wrapped tagline line one\n> line two.\n\nBody after.\n")
        ok("joined blockquote tagline wins over body",
           derive_summary(str(root)) == "Wrapped tagline line one line two.")

        (root / "README.md").write_text("# Title\n\n- list only\n")
        (root / "CONTEXT.md").write_text(
            "## Identity\n\n| Field | Value |\n|---|---|\n| **Tagline** | `Ctx tagline here` |\n")
        ok("context tagline fallback", derive_summary(str(root)) == "Ctx tagline here")

        (root / "CONTEXT.md").write_text("nothing\n")
        (root / "kodit.json").write_text(
            '{"project": {"name": "Kodit", "description": "from kodit.json"}}')
        ok("kodit.json description fallback",
           derive_summary(str(root)) == "from kodit.json")
        ok("kodit.json name", derive_name(str(root)) == "Kodit")
        ok("no git -> ''", derive_origin(str(root)) == "")
        ok("missing everything -> ''", derive_summary(str(root / "nope")) == "")

    print(f"derive selftest: PASS ({len(checks)} checks)")


if __name__ == "__main__":
    import sys
    if "--selftest" in sys.argv:
        _selftest()
    else:
        print("usage: derive.py --selftest")
        sys.exit(2)
