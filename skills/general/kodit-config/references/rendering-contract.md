# Rendering contract

Defines how `kodit-config` normalizes setup data and renders managed document
blocks. Read this before writing or appending to `AGENTS.md`, `README.md`, or
`CONTEXT.md`.

## Normalized setup model

Before rendering any file, assemble one model from all three setup drafts.
Never read values piecemeal per document; render from the same snapshot.

```yaml
project:
  name: string          # required
  description: string   # required, one line
  language: string|null # null = not configured
  build: string|null    # null = not configured
  test: string|null     # null = not configured

tracker:
  type: string          # "file" or "linear"
  path: string|null     # ".kodit/issues" for file; null for linear
  labels: [string]      # configured label list
  workspace: string|null  # Linear workspace slug; null for file
  team: object|null     # {key: string, id: string}; null for file
  linear_project: object|null  # {id: string, name: string}; null for file
  status_map: map|null  # Kodit→Linear state map; null for file

git:                    # null when no version control
  main_branch: string
  dev_branch: string
  feature_prefix: string
  bugfix_prefix: string
```

### Draft field mappings

| Draft field | Model field | Source |
|---|---|---|
| `Name` | `project.name` | metadata draft |
| `Description` | `project.description` | metadata draft |
| `Language` | `project.language` | metadata draft |
| `Build` | `project.build` | metadata draft |
| `Test` | `project.test` | metadata draft |
| `Backend` | `tracker.type` | issue-tracker draft (`file-based` → `file`, `linear` → `linear`) |
| `Path` | `tracker.path` | issue-tracker draft (file only) |
| `Labels` | `tracker.labels` | issue-tracker draft |
| `Workspace` | `tracker.workspace` | issue-tracker draft (Linear only) |
| `Team key` | `tracker.team.key` | issue-tracker draft (Linear only) |
| `Team ID` | `tracker.team.id` | issue-tracker draft (Linear only, resolved during provision) |
| `Project name` | `tracker.linear_project.name` | issue-tracker draft (Linear only) |
| `Project ID` | `tracker.linear_project.id` | issue-tracker draft (Linear only, resolved during provision) |
| `Status Map` | `tracker.status_map` | issue-tracker draft (Linear only) |
| `Main branch` | `git.main_branch` | branching draft |
| `Dev branch` | `git.dev_branch` | branching draft |
| `Feature prefix` | `git.feature_prefix` | branching draft |
| `Bugfix prefix` | `git.bugfix_prefix` | branching draft |
| `Repository: no` | `git = null` | branching draft |

## Canonical conversions

| Input | Output | Rule |
|---|---|---|
| `file-based` | `file` | Backend name normalization |
| `linear` | `linear` | Backend name passthrough |
| `none`, `null`, empty | `Not configured` | Display value for absent fields |
| Date | `YYYY-MM-DD` | ISO 8601 date only, no time |
| Labels | escaped strings | Escape `\|` in table cells |
| `tracker.team` (Linear) | rendered as `Team \| <key>` | Linear setup table row |
| `tracker.linear_project` (Linear) | rendered as `Project \| <name>` | Linear setup table row |

## Shared workflow fragments

Templates reference these strings. Never duplicate or vary them.

**Six-phase sequence:**
```
setup -> milestone-planning -> implement -> review-loop -> milestone-review -> done
```

**Inner loop (inside implement and review-loop):**
```
spec -> plan -> implement -> review
```

## Marker specification

Managed blocks are bounded by visible HTML comments. The prefix identifies the
document; the version allows future evolution.

| Document | Marker prefix | Start marker |
|---|---|---|
| `AGENTS.md` | `kodit:agents` | `<!-- kodit:agents:v1:start -->` |
| `README.md` | `kodit:readme` | `<!-- kodit:readme:v1:start -->` |
| `CONTEXT.md` | `kodit:context` | `<!-- kodit:context:v1:start -->` |

End markers replace `start` with `end`.

### Marker rules

- Markers are the sole idempotency mechanism. Heading-only matching is retired.
- Managed content is replace-only: never manually edit inside markers.
- A document may contain only one managed block per marker prefix.
- Markers must not appear inside code blocks or other markup.

## Document-state matrix

| File exists? | Managed block found? | Action |
|---|---|---|
| No | N/A | Create minimal document shell plus managed block. |
| Yes | Yes, current version | **No-op.** Report "already up to date." |
| Yes | Yes, older version | **Migrate.** Preview diff; replace after approval. |
| Yes | No, legacy fingerprint match | **Migrate.** Show legacy block; replace after approval; preserve non-legacy content. |
| Yes | No, no fingerprint match | **Append.** Add new managed block at end; preserve all existing content. |

## Legacy detection

A legacy block is detected when the file contains the old-template fingerprint
without markers:

| Document | Legacy fingerprint |
|---|---|
| `AGENTS.md` | Heading `## kodit Workflow` not inside kodit:agents markers |
| `README.md` | Heading `## Development Workflow` not inside kodit:readme markers |
| `CONTEXT.md` | Heading `# CONTEXT` or `# CONTEXT.md` followed by `## Decisions Log` not inside kodit:context markers |

### Legacy handling

- Unmodified legacy block: offer one-click migration (preview diff, approve,
  replace).
- User-modified legacy block: treat as user-owned. Preserve it and append a new
  managed block. Report `legacy retained, new block added`.
- Never silently delete or rewrite user-modified content.

## Rendering rules

### AGENTS.md

Create or replace the block inside `<!-- kodit:agents:v1:start/end -->`.

Content order:
1. `## kodit Workflow`
2. One-line: read `CONTEXT.md` first; configuration in `kodit.json`.
3. Six-phase sequence from shared fragments.
4. Inner loop from shared fragments.
5. Artifact naming: `spec-US-NNN-*.md`, `plan-T-NNN-*.md` in `.kodit/tmp/specs/`.
6. Issue taxonomy, statuses, and labels from configured list.
7. Tracker location: when `file`, state `.kodit/issues/` and conventions pointer.
   When `linear`, state "Linear at project `<tracker.linear_project.name>` (team
   `<tracker.team.key>`)" and point to `references/linear.md` in the tracker skill.
8. Branch rules when Git is configured; "Version control is not configured" when
   `git` is `null`.
9. Decision recording rule.

When `git` is `null`, omit the branch paragraph entirely and substitute the
no-version-control line.

### README.md

Create or replace the block inside `<!-- kodit:readme:v1:start/end -->`.

Content order:
1. `## kodit Development Workflow`
2. Project description from `project.description`.
3. Concise workflow overview: the six-phase sequence.
4. Pointer to `CONTEXT.md`, `AGENTS.md`, `kodit.json`.
5. Tracker location and conventions pointer: when `file`, reference
   `.kodit/issues/`; when `linear`, reference the Linear project and
   `references/linear.md`.
6. Branch rules when Git is configured; omit branch paragraph when `git` is
   `null`.

### CONTEXT.md

Create or replace the block inside `<!-- kodit:context:v1:start/end -->`.

Content order:
1. `## kodit Context`
2. `### Project`: name, description, language (or "Not configured").
3. `### Environment`: build (or "Not configured"), test (or "Not configured"),
   branches when Git is configured (or "Not configured"), issue tracking type
   and location (file path or Linear project/team).
4. `### Decisions Log`: `| Date | Decision | Rationale |` table seeded with:
   - Row 1: adoption decision with today's date.
   - Row 2 (Git only): branch model with today's date.

### Decisions mode (append to existing)

When Decisions mode appends to an existing `CONTEXT.md`:

1. Find the managed `<!-- kodit:context:v1:start -->` block.
2. Locate the `### Decisions Log` table inside it.
3. Append new rows before the `<!-- kodit:context:v1:end -->` marker.
4. If no managed block exists, create one with the full Context structure and
   append the decision rows.
5. Never touch content outside the managed block.

## Validation rules

Before writing any managed block:

1. All placeholders must resolve. If any `{{...}}` remains, stop and name the
   missing field.
2. Table cells with `|`, `[`, or `]` must be escaped.
3. The date must be `YYYY-MM-DD`.
4. Labels must come from the configured list, not a hard-coded subset.
5. The shared workflow fragments must match exactly (no trailing spaces, no
   variant arrows).
