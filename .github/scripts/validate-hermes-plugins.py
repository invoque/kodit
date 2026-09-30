#!/usr/bin/env python3
"""Validate Hermes plugins under hermes-plugins/.

For each immediate plugin directory:

  - plugin.yaml exists, parses, and its ``name`` equals the directory name
  - version and description are present
  - __init__.py exists and defines ``register(``
  - bundled skills/<name>/SKILL.md: frontmatter parses, ``name`` equals the
    directory, ``description`` <= 1024 chars
  - every ``*.py`` module selftests: exit 0 = pass, exit 2 = no selftest
    declared (allowed for leaf modules), anything else fails
  - __init__.py MUST ship a passing selftest (exit 0)

The gate is pure Python + stdlib sqlite3 (FTS5): no Hermes install, no network.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path("hermes-plugins")
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
MAX_DESCRIPTION = 1024
errors: list[str] = []


def fail(path: Path, message: str) -> None:
    errors.append(f"{path}: {message}")


def validate_manifest(plugin_dir: Path) -> None:
    manifest = plugin_dir / "plugin.yaml"
    if not manifest.is_file():
        fail(manifest, "plugin.yaml is missing")
        return
    try:
        data = yaml.safe_load(manifest.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        fail(manifest, f"invalid YAML: {exc}")
        return
    if not isinstance(data, dict):
        fail(manifest, "manifest is not a YAML mapping")
        return
    if data.get("name") != plugin_dir.name:
        fail(manifest, f"name {data.get('name')!r} != directory {plugin_dir.name!r}")
    for field in ("version", "description"):
        if not isinstance(data.get(field), str) or not data[field].strip():
            fail(manifest, f"{field} must be a non-empty string")


def validate_entry(plugin_dir: Path) -> None:
    init = plugin_dir / "__init__.py"
    if not init.is_file():
        fail(init, "__init__.py is missing")
        return
    if "def register(" not in init.read_text(encoding="utf-8"):
        fail(init, "does not define register(")


def validate_skill(skill_dir: Path) -> None:
    skill_file = skill_dir / "SKILL.md"
    if not skill_file.is_file():
        fail(skill_file, "SKILL.md is missing")
        return
    lines = skill_file.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        fail(skill_file, "missing frontmatter")
        return
    try:
        end = next(i for i, ln in enumerate(lines[1:], 1) if ln.strip() == "---")
        front = yaml.safe_load("\n".join(lines[1:end]))
    except (StopIteration, yaml.YAMLError) as exc:
        fail(skill_file, f"invalid frontmatter: {exc}")
        return
    if not isinstance(front, dict):
        fail(skill_file, "frontmatter is not a mapping")
        return
    if front.get("name") != skill_dir.name:
        fail(skill_file, f"name {front.get('name')!r} != directory {skill_dir.name!r}")
    desc = front.get("description")
    if not isinstance(desc, str) or not desc.strip():
        fail(skill_file, "description must be a non-empty string")
    elif len(desc) > MAX_DESCRIPTION:
        fail(skill_file, f"description is {len(desc)} chars (max {MAX_DESCRIPTION})")


def run_selftest(module: Path, *, required: bool) -> bool:
    proc = subprocess.run(
        [sys.executable, str(module), "--selftest"],
        capture_output=True, text=True, timeout=120)
    if proc.returncode == 0:
        last = (proc.stdout.strip().splitlines() or [""])[-1]
        print(f"  ok  {module.name}: {last}")
        return True
    if proc.returncode == 2 and not required:
        print(f"  --  {module.name}: no selftest declared")
        return True
    tail = (proc.stderr.strip().splitlines() or ["no output"])[-1]
    fail(module, f"selftest failed (exit {proc.returncode}): {tail}")
    return False


def main() -> int:
    if not ROOT.is_dir():
        print(f"{ROOT}: directory not found", file=sys.stderr)
        return 1
    plugins = sorted(p for p in ROOT.iterdir() if p.is_dir())
    if not plugins:
        print("no plugins found", file=sys.stderr)
        return 1
    for plugin_dir in plugins:
        print(f"{plugin_dir.name}:")
        validate_manifest(plugin_dir)
        validate_entry(plugin_dir)
        for skill_dir in sorted((plugin_dir / "skills").glob("*")):
            if skill_dir.is_dir():
                validate_skill(skill_dir)
        for module in sorted(plugin_dir.glob("*.py")):
            run_selftest(module, required=module.name == "__init__.py")
    if errors:
        print("\n".join(errors), file=sys.stderr)
        print(f"validate-hermes-plugins: FAIL ({len(errors)} error(s))", file=sys.stderr)
        return 1
    print(f"validate-hermes-plugins: OK ({len(plugins)} plugin(s))")
    return 0


if __name__ == "__main__":
    sys.exit(main())
