#!/usr/bin/env python3
"""Stage issue-tracker eval workspaces with deterministic fixtures.

Reads evals.json and creates isolated workspace directories for each eval.
Stages fixtures (mock Linear data, staged files) so that eval runs do not
depend on the machine's Linear CLI configuration.

Usage:
    python stage_evals.py <workspace-root> [--evals-json evals.json]

After staging, the main agent spawns subagents to execute each eval, then
calls this script with --grade to grade the outputs.
"""

import argparse
import json
import shutil
from pathlib import Path

# Deterministic fixtures for the Linear sandbox
FIXTURES = {
    "workspace": "invoque",
    "team_key_requested": "TEST",
    "team_key_canonical": "TES",
    "team_id": "4019459a-b8a4-4523-94e8-120465984fee",
    "team_name": "TEST",
    "project_name": "taskflow",
    "project_id": None,  # resolved during provision
    "labels": [
        "ready-for-agent",
        "ready-for-human",
        "needs-info",
        "needs-triage",
        "wontfix",
    ],
    "workflow_states": [
        {"name": "Backlog", "type": "backlog"},
        {"name": "Todo", "type": "unstarted"},
        {"name": "In Progress", "type": "started"},
        {"name": "Done", "type": "completed"},
        {"name": "Canceled", "type": "canceled"},
        {"name": "Duplicate", "type": "duplicate"},
        {"name": "In Review", "type": "started"},
    ],
}


def stage_eval_workspace(
    workspace_root: Path,
    eval_def: dict,
    skill_path: str,
) -> Path:
    """Stage a single eval workspace with fixtures.

    Returns the path to the staged workspace directory.
    """
    eval_id = eval_def["id"]
    prompt = eval_def["prompt"]

    # Determine eval directory name from the prompt scenario
    if "file-based backend" in prompt:
        eval_name = "eval-0-file-backend-setup"
    elif "Linear" in prompt and "MCP connected" in prompt:
        eval_name = "eval-1-linear-setup-with-mcp"
    elif "Linear" in prompt and "don't have any Linear integration" in prompt:
        eval_name = "eval-2-linear-setup-no-integration"
    elif "Linear" in prompt and "Provision" in prompt:
        eval_name = "eval-3-linear-provision"
    elif "file-based setup draft" in prompt:
        eval_name = "eval-4-file-provision"
    else:
        eval_name = f"eval-{eval_id}-unknown"

    eval_dir = workspace_root / eval_name / "with_skill"
    eval_dir.mkdir(parents=True, exist_ok=True)

    _write_metadata_and_fixtures(eval_dir, eval_id, prompt, eval_def, skill_path, "with_skill")

    # Stage the matching baseline so the benchmark has a comparison.
    baseline_dir = workspace_root / eval_name / "without_skill"
    baseline_dir.mkdir(parents=True, exist_ok=True)
    _write_metadata_and_fixtures(baseline_dir, eval_id, prompt, eval_def, None, "without_skill")

    return eval_dir


def _write_metadata_and_fixtures(
    eval_dir: Path,
    eval_id: int,
    prompt: str,
    eval_def: dict,
    skill_path: str | None,
    run_type: str,
) -> None:
    """Write eval metadata and stage the fixtures for a run directory."""
    metadata = {
        "eval_id": eval_id,
        "run_type": run_type,
        "skill_path": skill_path,
        "prompt": prompt,
        "allow_remote_writes": eval_def.get("allow_remote_writes", False),
        "resource_prefix": eval_def.get("resource_prefix"),
        "assertions": [{"text": e} for e in eval_def.get("expectations", [])],
        "fixtures": FIXTURES,
    }
    (eval_dir / "eval_metadata.json").write_text(
        json.dumps(metadata, indent=2) + "\n"
    )

    # Stage fixtures based on eval type
    if "file-based backend" in prompt:
        _stage_file_setup(eval_dir)
    elif "Linear" in prompt and "don't have" in prompt:
        _stage_no_integration(eval_dir)
    elif "Linear" in prompt and "MCP connected" in prompt:
        _stage_linear_setup(eval_dir, FIXTURES)
    elif "Linear" in prompt and "Provision" in prompt:
        _stage_linear_provision(eval_dir, FIXTURES)
    elif "file-based setup draft" in prompt:
        _stage_file_provision(eval_dir)


def _stage_file_setup(eval_dir: Path) -> None:
    """Stage file-based setup eval: no pre-existing files needed."""
    pass


def _stage_no_integration(eval_dir: Path) -> None:
    """Stage no-integration eval: provide a fixture that simulates no CLI.

    The fixture is a shell script that replaces `linear` with a deterministic
    failure response. This prevents the eval from using the real CLI.
    """
    fixture_dir = eval_dir / "fixtures"
    fixture_dir.mkdir(exist_ok=True)

    # Write a fake linear CLI that always fails
    fake_linear = fixture_dir / "linear"
    fake_linear.write_text(
        '#!/bin/bash\n'
        '# Fixture: simulates no Linear integration\n'
        'echo "Error: linear-cli is not installed or not authenticated."\n'
        'echo "Install: npm install -g @linear/cli"\n'
        'echo "Auth: linear auth login"\n'
        'exit 1\n'
    )
    fake_linear.chmod(0o755)


def _stage_linear_setup(eval_dir: Path, fixtures: dict) -> None:
    """Stage Linear setup eval: provide fixture data for workspace/team verification."""
    fixture_dir = eval_dir / "fixtures"
    fixture_dir.mkdir(exist_ok=True)

    # Write fixture data that the eval can read
    fixture_data = {
        "workspace": fixtures["workspace"],
        "team_key_requested": fixtures["team_key_requested"],
        "team_key_canonical": fixtures["team_key_canonical"],
        "team_id": fixtures["team_id"],
        "team_name": fixtures["team_name"],
        "project_name": fixtures["project_name"],
        "labels": fixtures["labels"],
        "workflow_states": fixtures["workflow_states"],
    }
    (fixture_dir / "linear_fixtures.json").write_text(
        json.dumps(fixture_data, indent=2) + "\n"
    )


def _stage_linear_provision(eval_dir: Path, fixtures: dict) -> None:
    """Stage Linear provision eval: provide kodit.json and setup draft."""
    # Write kodit.json
    kodit_json = {
        "version": 2,
        "project": {
            "name": fixtures["project_name"],
            "description": "Personal task tracking with weekly reviews.",
            "language": "typescript",
            "build": "npm run build",
            "test": "npm test",
        },
        "issue_tracker": {
            "type": "linear",
            "workspace": fixtures["workspace"],
            "team": {
                "key": fixtures["team_key_canonical"],
                "id": fixtures["team_id"],
            },
            "linear_project": {"name": fixtures["project_name"]},
            "status_map": {
                "spec": "In Progress",
                "plan": "In Progress",
                "implement": "In Progress",
                "review": "In Review",
                "done": "Done",
                "story_open": "Todo",
                "story_in_progress": "In Progress",
                "story_done": "Done",
                "milestone_planned": "In Progress",
                "milestone_active": "In Progress",
                "milestone_closed": "Done",
            },
            "labels": fixtures["labels"],
        },
        "git": {
            "main_branch": "main",
            "dev_branch": "develop",
            "feature_prefix": "feat/",
            "bugfix_prefix": "fix/",
            "staging_branch": None,
            "remote": "origin",
        },
    }
    (eval_dir / "kodit.json").write_text(json.dumps(kodit_json, indent=2) + "\n")

    # Write setup draft
    draft_dir = eval_dir / ".kodit" / "tmp"
    draft_dir.mkdir(parents=True, exist_ok=True)
    draft = (
        "# Issue Tracker Setup Draft\n\n"
        "## Backend\nLinear\n\n"
        f"## Workspace\n{fixtures['workspace']}\n\n"
        "## Team\n"
        f"- Key: {fixtures['team_key_canonical']}\n"
        f"- ID: {fixtures['team_id']}\n\n"
        "## Project\n"
        f"- Name: {fixtures['project_name']}\n\n"
        "## Labels\n"
        + "\n".join(f"- {l}" for l in fixtures["labels"])
        + "\n\n"
        "## Status Map\n"
        "- spec: In Progress\n"
        "- plan: In Progress\n"
        "- implement: In Progress\n"
        "- review: In Review\n"
        "- done: Done\n"
        "- story_open: Todo\n"
        "- story_in_progress: In Progress\n"
        "- story_done: Done\n"
        "- milestone_planned: In Progress\n"
        "- milestone_active: In Progress\n"
        "- milestone_closed: Done\n"
    )
    (draft_dir / "setup-issue-tracker.md").write_text(draft)


def _stage_file_provision(eval_dir: Path) -> None:
    """Stage file provision eval: provide kodit.json and setup draft."""
    kodit_json = {
        "version": 1,
        "project": {
            "name": "myapp",
            "description": "A Python web service.",
            "language": "python",
            "build": None,
            "test": None,
        },
        "issue_tracker": {
            "type": "file",
            "path": ".kodit/issues",
            "labels": [
                "ready-for-agent",
                "ready-for-human",
                "needs-info",
                "needs-triage",
                "wontfix",
            ],
        },
        "git": None,
    }
    (eval_dir / "kodit.json").write_text(json.dumps(kodit_json, indent=2) + "\n")

    draft_dir = eval_dir / ".kodit" / "tmp"
    draft_dir.mkdir(parents=True, exist_ok=True)
    draft = (
        "# Issue Tracker Setup Draft\n\n"
        "## Backend\nfile\n\n"
        "## Path\n.kodit/issues\n\n"
        "## Labels\n"
        "- ready-for-agent\n"
        "- ready-for-human\n"
        "- needs-info\n"
        "- needs-triage\n"
        "- wontfix\n"
    )
    (draft_dir / "setup-issue-tracker.md").write_text(draft)


def stage_all(
    workspace_root: Path,
    evals_json_path: Path,
    skill_path: str,
) -> list[Path]:
    """Stage all eval workspaces. Returns list of staged workspace paths."""
    evals_data = json.loads(evals_json_path.read_text())
    evals = evals_data.get("evals", [])

    staged = []
    for eval_def in evals:
        path = stage_eval_workspace(workspace_root, eval_def, skill_path)
        staged.append(path)
        print(f"  Staged eval {eval_def['id']}: {path}")

    return staged


def main() -> None:
    parser = argparse.ArgumentParser(description="Stage issue-tracker eval workspaces")
    parser.add_argument("workspace_root", type=Path, help="Root workspace directory")
    parser.add_argument(
        "--evals-json",
        type=Path,
        default=None,
        help="Path to evals.json (default: <skill>/evals/evals.json)",
    )
    parser.add_argument(
        "--skill-path",
        type=str,
        default="skills/general/issue-tracker",
        help="Path to the skill (default: skills/general/issue-tracker)",
    )
    args = parser.parse_args()

    workspace_root = args.workspace_root.resolve()
    workspace_root.mkdir(parents=True, exist_ok=True)

    evals_json = args.evals_json
    if evals_json is None:
        # Find evals.json relative to this script
        script_dir = Path(__file__).resolve().parent
        evals_json = script_dir.parent / "evals" / "evals.json"

    if not evals_json.exists():
        print(f"Error: evals.json not found at {evals_json}", file=__import__("sys").stderr)
        __import__("sys").exit(1)

    print(f"Staging evals from {evals_json} into {workspace_root}")
    staged = stage_all(workspace_root, evals_json, args.skill_path)
    print(f"\nStaged {len(staged)} eval workspaces.")
    print("\nNext steps:")
    print("  1. Main agent spawns subagents for each with_skill/ directory")
    print("  2. Subagents execute the eval prompt and write outputs/")
    print("  3. Run grading against each run")


if __name__ == "__main__":
    main()
