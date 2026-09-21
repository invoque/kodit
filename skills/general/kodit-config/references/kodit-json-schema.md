# kodit.json schema

The project configuration. Lives at the project root next to `package.json` or
any other manifest. Committed. `kodit-config` is the write authority; every
other skill reads it.

## Shape — file backend (v1, still valid)

```json
{
  "version": 1,
  "project": {
    "name": "my-project",
    "description": "One line on what this project is.",
    "language": "python",
    "build": "python -m build",
    "test": "pytest"
  },
  "issue_tracker": {
    "type": "file",
    "path": ".kodit/issues",
    "labels": [
      "ready-for-agent",
      "ready-for-human",
      "needs-info",
      "needs-triage",
      "wontfix"
    ]
  },
  "git": {
    "main_branch": "master",
    "dev_branch": "dev",
    "feature_prefix": "feature/",
    "bugfix_prefix": "bugfix/",
    "staging_branch": null,
    "remote": null
  }
}
```

## Shape — Linear backend (v2)

```json
{
  "version": 2,
  "project": {
    "name": "my-project",
    "description": "One line on what this project is.",
    "language": "python",
    "build": "python -m build",
    "test": "pytest"
  },
  "issue_tracker": {
    "type": "linear",
    "team": "ENG",
    "linear_project": "my-project",
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
      "milestone_closed": "Done"
    },
    "labels": [
      "ready-for-agent",
      "ready-for-human",
      "needs-info",
      "needs-triage",
      "wontfix"
    ]
  },
  "git": {
    "main_branch": "master",
    "dev_branch": "dev",
    "feature_prefix": "feature/",
    "bugfix_prefix": "bugfix/",
    "staging_branch": null,
    "remote": null
  }
}
```

## Fields

### Common fields (all versions)

| Field | Required | Notes |
|---|---|---|
| `version` | yes | `1` for file backend; `2` for Linear. |
| `project.name` | yes | Project name. |
| `project.description` | yes | One line; seeded into managed docs. |
| `project.language` | no | Primary language, else `null`. |
| `project.build` | no | Build command, else `null`. |
| `project.test` | no | Test command, else `null`. |
| `issue_tracker.labels` | yes | Workflow/handoff labels. May be extended per project. |
| `git` | no | `null` when the project declined a repository. |
| `git.main_branch` | yes when `git` set | Stable branch. |
| `git.dev_branch` | yes when `git` set | Integration branch. |
| `git.feature_prefix` | yes when `git` set | e.g. `feature/`. |
| `git.bugfix_prefix` | yes when `git` set | e.g. `bugfix/`. |
| `git.staging_branch` | no | `null`, or a release-hardening branch. |
| `git.remote` | no | Remote name, else `null`. |

### File backend fields (v1)

| Field | Required | Notes |
|---|---|---|
| `issue_tracker.type` | yes | Must be `"file"`. |
| `issue_tracker.path` | yes | Typically `.kodit/issues`. |

### Linear backend fields (v2)

| Field | Required | Notes |
|---|---|---|
| `issue_tracker.type` | yes | Must be `"linear"`. |
| `issue_tracker.team` | yes | Linear team key (e.g. `"ENG"`). Issues belong to this team. |
| `issue_tracker.linear_project` | yes | Linear Project name or ID containing milestones. Created or selected during setup. |
| `issue_tracker.status_map` | yes | Kodit status → Linear workflow state name. See `linear.md` for required keys. |

### Notes on Linear fields

- `path` is **not** used for Linear. There is no local issue tree.
- `issue_tracker.labels` is used for Kodit handoff labels stored in issue
  descriptions, not for Linear label creation.
- `issue_tracker.status_map` maps each Kodit internal state to a Linear
  workflow state name for that team. See `references/linear.md` for the full
  mapping and provisioning requirements.
- Credentials are never stored in `kodit.json`. Authentication is handled by
  the Linear MCP integration or the `linear-cli` tool.

## Rules

- State machines, label semantics, and the issue tree are **not** here; they
  live in the issue tracker's conventions doc (`.kodit/issues/README.md` for
  file backend, or `references/linear.md` for Linear).
- `issue_tracker` is backend-swappable: changing `type` and its fields later is
  the migration path.
- Never invent extra top-level keys. Add a field only with a schema version
  bump and a decision recorded in `CONTEXT.md`.
- File-backed projects may stay on v1; v2 is only required when adding Linear.

## Examples

### File backend, non-git project (v1)

```json
{
  "version": 1,
  "project": { "name": "sketch", "description": "Notes and prototypes.", "language": null, "build": null, "test": null },
  "issue_tracker": { "type": "file", "path": ".kodit/issues",
    "labels": ["ready-for-agent", "ready-for-human", "needs-info", "needs-triage", "wontfix"] },
  "git": null
}
```

### Linear backend, git project (v2)

```json
{
  "version": 2,
  "project": { "name": "taskflow", "description": "Personal task tracking with weekly reviews.", "language": "typescript", "build": "npm run build", "test": "npm test" },
  "issue_tracker": {
    "type": "linear",
    "team": "ENG",
    "linear_project": "taskflow",
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
      "milestone_closed": "Done"
    },
    "labels": ["ready-for-agent", "ready-for-human", "needs-info", "needs-triage", "wontfix"]
  },
  "git": {
    "main_branch": "main",
    "dev_branch": "develop",
    "feature_prefix": "feat/",
    "bugfix_prefix": "fix/",
    "staging_branch": null,
    "remote": "origin"
  }
}
```
