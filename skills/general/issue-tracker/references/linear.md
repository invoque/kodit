# Linear issue tracker conventions

Canonical reference for the Linear backend. Read this before any operate-mode
write when `issue_tracker.type` is `"linear"`.

## Taxonomy mapping

| Kodit | Linear | Notes |
|---|---|---|
| **Project** | Linear Project | One project per kodit project. Contains milestones. |
| **Milestone** | Project Milestone | `[M-001] <goal>` — a checkpoint within the project. |
| **User Story** | Issue (parent) | `[US-001] <title>` — parent issue with labels from story frontmatter. |
| **Task** | Sub-issue | `[T-001] <title>` — child issue via `parentId`. |

Sub-issues inherit the parent's team, project, and priority. Labels do **not**
inherit; they are set explicitly on each issue.

## Kodit ID encoding

Kodit's global IDs (`M-001`, `US-001`, `T-001`) are not native Linear fields.
Encode them in a structured metadata block at the top of each issue
description:

```markdown
<!-- kodit:M-001:type=milestone -->
<!-- kodit:US-001:type=story;parent=M-001 -->
<!-- kodit:T-001:type=task;parent=US-001 -->
```

The operate mode reads these markers to locate Kodit items. Never strip or
overwrite them. Append all other content after the markers.

## Story issue format

```markdown
<!-- kodit:US-001:type=story;parent=M-001 -->
## Story
As a returning user I want to reset my password by email so that I can regain
access without support.

## Acceptance Criteria
- [ ] A reset link is emailed within one minute.
- [ ] The link expires after 24 hours.
- [ ] An unknown email does not reveal whether an account exists.

## Tasks
| ID | Description | Status |
|----|-------------|--------|
| T-001 | Add reset-token model and expiry | open |
| T-002 | Send reset email | open |
| T-003 | Reset form and confirmation page | open |
```

The Tasks table is maintained in the story issue description. Tasks are
sub-issues, not rows — the table is a convenience index for humans. The
canonical status lives on each sub-issue.

## Status machines

### Task (sub-issue)

```text
open → spec → plan → implement → review → done
                 ↑                   |
                 └───────────────────┘   (rework: review → implement)
blocked  ⇄  any non-done state
wontfix  →  closes from any state
```

Map each state to a Linear workflow state name via `issue_tracker.status_map`
in `kodit.json`. Linear uses the `state` field on each issue.

### User story (parent issue)

```text
open → in-progress → done
blocked ⇄ any non-done state
```

Derived from sub-issue states: `in-progress` when any sub-issue leaves `open`,
`done` when all are `done` or `wontfix`.

### Milestone (project milestone)

```text
planned → active → closed
```

Derived from issue states: `active` when any story is in progress, `closed`
when all stories are done/wontfix.

## Labels

Kodit labels are stored on story issues via the `labels` frontmatter field.
They are handoff signals, not types. The default set:

| Label | Meaning |
|---|---|
| `ready-for-agent` | Fully specified; an agent can pick it up. |
| `ready-for-human` | Needs a human action or decision. |
| `needs-info` | Missing information blocks progress. |
| `needs-triage` | Not yet classified or scoped. |
| `wontfix` | Deliberately not doing this. Terminal. |

Use `--add-label` and `--remove-label` on the CLI for incremental label
changes; use `--label` to replace the full set.

## Milestone charter storage

The milestone's goal, status, PR URL, and merge record are stored in the
project milestone description:

```markdown
## Goal
<what done looks like>

**Status:** planned
**PR:** <url, when open>
**Merged:** <timestamp | sha, after successful merge>
**Created:** YYYY-MM-DD

## Stories
| ID | Title | Status |
|----|-------|--------|
| US-001 | <title> | open |
```

Update the milestone description when adding stories, recording PR/merge
metadata, or deriving status changes.

## Project charter storage

The project-level charter (milestone index) is stored in the Linear Project
description:

```markdown
# Project — <name>

<description>

## Milestones
| ID | Goal | Status |
|----|------|--------|
| M-001 | <goal> | planned |
```

## PR and merge metadata

- **PR URL:** stored in the milestone's description as `**PR:** <url>`.
  Idempotent write; no status change.
- **Merge record:** stored as `**Merged:** <timestamp> | <sha>` in the
  milestone description. Written only after confirmed merge.
- **Review notes:** appended as a comment on the affected story issue.

## Provisioning

After checkpoint approval, the setup-provision mode creates or verifies:

1. The Linear Project (if not found by name).
2. Required workflow states (if missing from the team's workflow).
3. Labels (if missing from the workspace).

GraphQL mutations needed for provisioning:

```graphql
# Create project
mutation { projectCreate(input: { name: "...", teamIds: ["..."] }) { success project { id } } }

# Create workflow state
mutation { workflowStateCreate(input: { teamId: "...", name: "...", type: "unstarted" }) { success workflowState { id } } }

# Create label
mutation { issueLabelCreate(input: { name: "...", teamId: "..." }) { success issueLabel { id } } }
```

## Setup failure modes

When no Linear MCP or CLI is available, or authentication fails:

1. Report exactly which integration is missing.
2. Name the two remediation paths:
   - Connect the official Linear MCP server (`https://mcp.linear.app/mcp`)
     with write-capable OAuth; or
   - Install and authenticate `linear-cli` (`linear auth login`).
3. Offer the user the file-based backend as the alternative.
4. Stop — never partially configure Linear without confirmed access.

## Issue operations

All issue reads/writes go through the active Linear integration (MCP, CLI,
or GraphQL). The operate mode never touches local `.kodit/issues/` when the
backend is Linear.

### Read operations

- List milestones: `linear milestone list --project <id>` or MCP equivalent.
- List stories/tasks: `linear issue query --project <id> --milestone <name> --json`.
- Read story body: `linear issue view <id> --json`.
- Read task status: `linear issue view <id> --json`.

### Write operations

- Create milestone: `linear milestone create --project <id> --name "M-001 — ..."`.
- Create story: `linear issue create --team <key> --title "[US-001] ..." --project <id> --milestone "M-001 — ..." --description-file <path>`.
- Create task: `linear issue create --team <key> --title "[T-001] ..." --parent <story-id> --description-file <path>`.
- Update task status: `linear issue update <id> --state "<state>"`.
- Record PR: `linear issue comment add <milestone-id> --body-file <path>`.
- Append review: `linear issue comment add <story-id> --body-file <path>`.
