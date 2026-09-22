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
    "workspace": "<workspace-slug>",
    "team": { "key": "ENG", "id": "<team-uuid>" },
    "linear_project": { "id": "<project-uuid>", "name": "my-project" },
    "status_map": {
      "open": "Todo",
      "spec": "In Progress",
      "plan": "In Progress",
      "implement": "In Progress",
      "review": "In Review",
      "done": "Done",
      "blocked": "Blocked",
      "wontfix": "Canceled",
      "story_open": "Todo",
      "story_in_progress": "In Progress",
      "story_done": "Done",
      "milestone_planned": "Todo",
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
| `issue_tracker.workspace` | yes | Linear workspace slug (e.g. `"acme"`). All operations target this workspace. |
| `issue_tracker.team.key` | yes | Linear team key (e.g. `"ENG"`). Issues belong to this team. |
| `issue_tracker.team.id` | yes | Resolved UUID of the team. Setup resolves and records this in the draft; every operation uses it. |
| `issue_tracker.linear_project.id` | yes | Resolved UUID of the project containing milestones. Provision creates or finds the project and appends the ID to the draft. |
| `issue_tracker.linear_project.name` | yes | Human-readable project name for display. |
| `issue_tracker.status_map` | yes | Kodit status → Linear workflow state name. Must cover every key listed under "Required `status_map` keys" in `linear.md`. |

### Notes on Linear fields

- `path` is **not** used for Linear. There is no local issue tree.
- `workspace` is mandatory and authoritative. Setup mode verifies the workspace
  exists and is accessible; every subsequent CLI/MCP call includes
  `--workspace <workspace>`. No silent fallback to another workspace.
- `team` is an object with both `key` and `id`. Setup mode resolves the team by
  key within the workspace and records both. If the team does not exist and
  cannot be created, setup stops.
- `linear_project` is an object with both `id` and `name`. Provision mode
  creates or finds the project and records both. The `id` is used for all
  subsequent operations.
- `issue_tracker.labels` is the handoff-label vocabulary. In Linear these
  labels are also provisioned on the team (created if missing) and applied to
  story issues; the list itself is config, the labels are remote resources.
- `issue_tracker.status_map` maps each Kodit internal state to a Linear
  workflow state name for that team. It must cover every required key listed in
  `references/linear.md`; provisioning ensures each named state exists.
- Credentials are never stored in `kodit.json`. Authentication is handled by
  the Linear MCP integration or the `linear-cli` tool.

## Rules

- State machines, label semantics, and the issue tree are **not** here; they
  live in the issue tracker's conventions doc (`.kodit/issues/README.md` for
  file backend, or `references/linear.md` for Linear).
- `issue_tracker` is backend-swappable: changing `type` and its fields later is
  the migration path.
- For Linear: setup resolves `workspace` and `team.id`; provision resolves
  `linear_project.id` and ensures states and labels exist. Write mode then
  produces `kodit.json` from the draft. Every subsequent operation uses these
  resolved IDs, not human-readable names.
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
    "workspace": "acme",
    "team": { "key": "ENG", "id": "<team-uuid>" },
    "linear_project": { "id": "<project-uuid>", "name": "taskflow" },
    "status_map": {
      "open": "Todo",
      "spec": "In Progress",
      "plan": "In Progress",
      "implement": "In Progress",
      "review": "In Review",
      "done": "Done",
      "blocked": "Blocked",
      "wontfix": "Canceled",
      "story_open": "Todo",
      "story_in_progress": "In Progress",
      "story_done": "Done",
      "milestone_planned": "Todo",
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
