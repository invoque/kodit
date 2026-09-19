# kodit.json schema

The project configuration. Lives at the project root next to `package.json` or
any other manifest. Committed. `kodit-config` is the write authority; every
other skill reads it.

## Shape

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

## Fields

| Field | Required | Notes |
|---|---|---|
| `version` | yes | Schema version. `1` today. |
| `project.name` | yes | Project name. |
| `project.description` | yes | One line; also seeded into `README.md` and `CONTEXT.md`. |
| `project.language` | no | Primary language, else `null`. |
| `project.build` | no | Build command, else `null`. |
| `project.test` | no | Test command, else `null`. |
| `issue_tracker.type` | yes | `file` today. `github` and `linear` are reserved. |
| `issue_tracker.path` | yes | `.kodit/issues` for file-based. |
| `issue_tracker.labels` | yes | Workflow/handoff labels. May be extended per project. |
| `git` | no | `null` when the project declined a repository. |
| `git.main_branch` | yes when `git` is set | Stable branch. |
| `git.dev_branch` | yes when `git` is set | Integration branch. |
| `git.feature_prefix` | yes when `git` is set | e.g. `feature/`. |
| `git.bugfix_prefix` | yes when `git` is set | e.g. `bugfix/`. |
| `git.staging_branch` | no | `null`, or a release-hardening branch between `dev` and `main`. |
| `git.remote` | no | Remote name, else `null`. |

## Rules

- State machines, label semantics, and the issue tree are **not** here; they
  live in the issue tracker's conventions doc (`.kodit/issues/README.md`).
- `issue_tracker` is backend-swappable: changing `type` and its fields later is
  the migration path once other backends are supported.
- Never invent extra top-level keys. Add a field only with a schema version
  bump and a decision recorded in `CONTEXT.md`.

## Example — file-based, non-git project

```json
{
  "version": 1,
  "project": { "name": "sketch", "description": "Notes and prototypes.", "language": null, "build": null, "test": null },
  "issue_tracker": { "type": "file", "path": ".kodit/issues",
    "labels": ["ready-for-agent", "ready-for-human", "needs-info", "needs-triage", "wontfix"] },
  "git": null
}
```
