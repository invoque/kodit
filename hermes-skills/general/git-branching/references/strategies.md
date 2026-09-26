# Branching models

Field list for the branching interview and the draft format. Read this before
asking the branching questions.

## Fields and defaults

| Field | Default | Notes |
|---|---|---|
| `main_branch` | `master` | Stable, released state. Only updated by merging `dev`. |
| `dev_branch` | `dev` | Integration branch. Only updated by merging feature branches. |
| `feature_prefix` | `feature/` | All work branches. Branch from `dev`, merge back to `dev`. |
| `bugfix_prefix` | `bugfix/` | Fixes that are not features. Same flow as features. |
| `staging_branch` | `null` | Optional release-hardening lane between `dev` and `main`. |
| `remote` | `null` | Remote name, e.g. `origin`. |

Name branches in lowercase kebab-case after the prefix, e.g.
`feature/setup-kodit`.

## The default model

```text
feature/*  ─┐
bugfix/*   ─┴─→  dev  ──→  master
```

`master` and `dev` are protected: no direct commits, no force-pushes. Every
change is a `feature/*` or `bugfix/*` branch off `dev`, merged back into `dev`
after review. `dev` is merged into `master` only for a release.

## Staging branch (optional)

When present, `staging` is a release-candidate lane:

```text
feature/* ─→ dev ─→ staging ─→ master
```

`dev` merges into `staging` to harden a release; `staging` merges into `master`
when it is ready. Use it only when a soak period between integration and release
is genuinely wanted; otherwise leave it `null` — an unused branch is ceremony.

## Adapting to an existing repository

- Prefer the repository's actual default branch as `main_branch` even if it is
  not `master` (e.g. `main`).
- If a `dev` branch already exists, keep its name.
- If other long-lived branches exist (`develop`, `release/*`), ask whether they
  map onto `dev` / `staging` before inventing new names.
- Never rename or delete an existing branch during setup.

## Draft format

Write `.kodit/tmp/setup-git-branching.md`:

```markdown
# setup — git branching

- **Repository:** yes | no (git init offered/accepted/skipped)
- **Main branch:** master
- **Dev branch:** dev
- **Feature prefix:** feature/
- **Bugfix prefix:** bugfix/
- **Staging branch:** none
- **Remote:** none

## Actions taken

- (none) | Created branch `dev` from `master` | Added remote `origin` <url>

## Notes

<any conflicts surfaced and how they were resolved>
```
