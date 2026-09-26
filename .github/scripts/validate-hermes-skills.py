#!/usr/bin/env python3
"""Validate Hermes skills under hermes-skills/.

Checks each immediate skill directory in every category directory
(`hermes-skills/<category>/<name>/SKILL.md`):

  - SKILL.md exists
  - frontmatter is a YAML mapping delimited by `---`
  - `name` is present, lowercase kebab-case, and equals the directory name
  - `description` is present and at most 1024 characters

`gh skill publish --dry-run` cannot see this tree because its discovery
conventions only match paths containing a `skills/` segment. This script is the
equivalent gate for Hermes skills.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

ROOT = Path("hermes-skills")
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
MAX_DESCRIPTION = 1024


def fail(path: Path, message: str) -> str:
    return f"{path}: {message}"


def parse_frontmatter(path: Path) -> dict:
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError("missing opening frontmatter delimiter")
    try:
        end = next(i for i, line in enumerate(lines[1:], start=1) if line.strip() == "---")
    except StopIteration:
        raise ValueError("missing closing frontmatter delimiter") from None
    data = yaml.safe_load("\n".join(lines[1:end]))
    if not isinstance(data, dict):
        raise ValueError("frontmatter is not a YAML mapping")
    return data


def validate_skill(skill_dir: Path) -> list[str]:
    skill_file = skill_dir / "SKILL.md"
    errors: list[str] = []
    if not skill_file.is_file():
        return [fail(skill_file, "SKILL.md is missing")]

    try:
        frontmatter = parse_frontmatter(skill_file)
    except (ValueError, yaml.YAMLError) as exc:
        return [fail(skill_file, f"invalid frontmatter: {exc}")]

    name = frontmatter.get("name")
    if not isinstance(name, str) or not name:
        errors.append(fail(skill_file, "`name` must be a non-empty string"))
    else:
        if name != skill_dir.name:
            errors.append(fail(skill_file, f"`name: {name}` does not match directory `{skill_dir.name}`"))
        if not NAME_RE.match(name):
            errors.append(fail(skill_file, f"`name: {name}` is not lowercase kebab-case"))

    description = frontmatter.get("description")
    if not isinstance(description, str) or not description.strip():
        errors.append(fail(skill_file, "`description` must be a non-empty string"))
    elif len(description) > MAX_DESCRIPTION:
        errors.append(fail(skill_file, f"`description` is {len(description)} characters (max {MAX_DESCRIPTION})"))

    return errors


def main() -> int:
    if not ROOT.is_dir():
        print(f"{ROOT}: missing", file=sys.stderr)
        return 1

    skill_dirs = sorted(
        child
        for category in ROOT.iterdir()
        if category.is_dir()
        for child in category.iterdir()
        if child.is_dir()
    )
    if not skill_dirs:
        print(f"{ROOT}: no skill directories found", file=sys.stderr)
        return 1

    errors = [error for skill_dir in skill_dirs for error in validate_skill(skill_dir)]
    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        print(f"hermes skill validation failed with {len(errors)} error(s)", file=sys.stderr)
        return 1

    print(f"validated {len(skill_dirs)} hermes skill(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
