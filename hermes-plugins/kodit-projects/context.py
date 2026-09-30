"""Size-capped ``[project-context]`` block builder.

The block is what ``pre_llm_call`` returns as ``{"context": ...}`` — Hermes joins
it into the user message, so every byte is per-turn LLM context. Target cap is
2000 chars; the builder sheds optional rows before it ever hard-cuts.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

MAX_BLOCK = 2000

# shed order: nice-to-have rows first, summary last (it carries the most signal)
_SHED = ("key paths:", "github:", "linear:", "indexed files:")

_NEXT = ("next: find files with kodit_projects_search; read or edit metadata with "
         "/projects or skill kodit-projects:projects.")


def build_block(project: Dict[str, Any], *, first_turn: bool = False,
                top_paths: Optional[List[str]] = None, file_total: int = 0) -> str:
    """Render one project's context block, guaranteed <= MAX_BLOCK characters."""
    lines = [f'[project-context] active project "{project.get("name") or project.get("slug")}" '
             f'(slug: {project.get("slug")}).',
             f'working dir: {project.get("working_dir")}']
    summary = str(project.get("summary") or "").strip()
    if summary:
        lines.append(f"summary: {summary}")
    if project.get("linear_url"):
        lines.append(f"linear: {project['linear_url']}")
    if project.get("github_repo"):
        lines.append(f"github: {project['github_repo']}")
    if file_total:
        lines.append(f"indexed files: {file_total}")
    if first_turn and top_paths:
        lines.append("key paths: " + ", ".join(str(p) for p in top_paths[:6]))
    lines.append(_NEXT)

    block = "\n".join(lines)
    if len(block) <= MAX_BLOCK:
        return block

    # 1. shed optional rows (never working dir or the tail)
    for prefix in _SHED:
        if len(block) <= MAX_BLOCK:
            break
        lines = [l for l in lines if not l.startswith(prefix)]
        block = "\n".join(lines)

    # 2. truncate the summary row to fit
    if len(block) > MAX_BLOCK:
        for i, line in enumerate(lines):
            if line.startswith("summary: "):
                budget = MAX_BLOCK - (len(block) - len(line)) - 1  # -1 for the ellipsis
                if budget > 16:
                    lines[i] = line[:budget] + "…"
                else:
                    lines = lines[:i] + lines[i + 1:]
                block = "\n".join(lines)
                break

    # 3. last resort: hard cut
    if len(block) > MAX_BLOCK:
        block = block[:MAX_BLOCK - 1] + "…"
    return block


# -- selftest -----------------------------------------------------------------------------

def _selftest() -> None:
    checks: List[str] = []

    def ok(label: str, cond: bool) -> None:
        if not cond:
            raise AssertionError(label)
        checks.append(label)

    p = {"slug": "kodit", "name": "Kodit", "working_dir": "/w/kodit",
         "summary": "workflow skills", "linear_url": "https://linear.app/x/y",
         "github_repo": "https://github.com/me/kodit"}

    block = build_block(p, first_turn=True, top_paths=["a.py", "b.py"], file_total=12)
    ok("name present", 'active project "Kodit"' in block)
    ok("summary present", "summary: workflow skills" in block)
    ok("key paths first turn", "key paths: a.py, b.py" in block)
    ok("file count present", "indexed files: 12" in block)
    ok("skill named", "kodit-projects:projects" in block)

    block2 = build_block(p)
    ok("no key paths on later turns", "key paths" not in block2)

    small = {"slug": "s", "name": "S", "working_dir": "/s"}
    ok("missing fields tolerated", "summary:" not in build_block(small))

    fat = dict(p, summary="x" * 10000)
    big = build_block(fat, first_turn=True, top_paths=["f%d" % i for i in range(50)])
    ok("cap enforced", len(big) <= MAX_BLOCK)
    ok("tail survives truncation", "kodit_projects_search" in big)

    ok("no fields at all", "active project" in build_block({}))

    print(f"context selftest: PASS ({len(checks)} checks)")


if __name__ == "__main__":
    import sys
    if "--selftest" in sys.argv:
        _selftest()
    else:
        print("usage: context.py --selftest")
        sys.exit(2)
