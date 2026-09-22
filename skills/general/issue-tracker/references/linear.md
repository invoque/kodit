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

Required `status_map` keys — every state in every machine above must have an
entry:

| Machine | Keys |
|---|---|
| Task | `open`, `spec`, `plan`, `implement`, `review`, `done`, `blocked`, `wontfix` |
| User story | `story_open`, `story_in_progress`, `story_done` |
| Milestone | `milestone_planned`, `milestone_active`, `milestone_closed` |

`open` is the state of every newly created task, so it must be mapped. Typical
values: `open` → `Todo`, `blocked` → a `Blocked` workflow state (created
during provisioning), `wontfix` → `Canceled`. Provisioning must ensure every
state named by `status_map` exists for the team (see "Provisioning").

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

- **PR URL:** stored in the milestone's **description** as `**PR:** <url>`,
  written with `linear milestone update --description-file` (or a
  `milestoneUpdate` GraphQL mutation where the CLI flag is unavailable).
  Idempotent write; no status change.
- **Merge record:** stored in the milestone **description** as
  `**Merged:** <timestamp> | <sha>`, using the same write mechanism. Written
  only after confirmed merge.
- **Review notes:** appended as a comment on the affected story issue
  (`linear issue comment add <story-id> --body-file <path>`). Comments target
  issues; never pass a milestone ID to `issue comment`.

## Provisioning

After checkpoint approval, the provision mode creates or verifies resources
**within the workspace and team recorded in the setup draft**
(`.kodit/tmp/setup-issue-tracker.md`). `kodit.json` does not exist yet at this
point — write mode produces it after provisioning succeeds. Treat the draft as
the source of truth; never require `kodit.json`.

1. Verify `workspace` and `team.id` are present in the draft. Stop if not.
2. The Linear Project (if not found by name **in the specified workspace**).
3. Required workflow states (if missing from **the specified team's** workflow).
4. Labels (if missing from **the specified workspace/team**).
5. Append the resolved project ID to the draft. Do not write `kodit.json`.

All CLI commands must include `--workspace <workspace>` explicitly. Never
assume a default workspace.

Prefer dedicated CLI commands over raw GraphQL. Use GraphQL only where the CLI
has no equivalent (workflow-state creation):

```bash
# Project and labels have dedicated commands
linear project create --workspace <workspace> --team <team-key> --name "<project-name>" --no-interactive
linear label create --workspace <workspace> --name "<label>" --team <team-key> --no-interactive
```

```graphql
# Create workflow state: no CLI command exists, so use the API
mutation { workflowStateCreate(input: { teamId: "...", name: "...", type: "unstarted" }) { success workflowState { id } } }
```

**Never** create resources in a workspace/team other than the one in the draft.
If the specified team does not exist, stop and report the failure — do not fall
back to another team.

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

- List milestones: `linear milestone list --workspace <ws> --project <id>` or MCP equivalent.
- List stories/tasks: `linear issue query --workspace <ws> --project <id> --milestone <name> --json`.
- Read story body: `linear issue view <id> --json`.
- Read task status: `linear issue view <id> --json`.

### Write operations

- Create milestone: `linear milestone create --workspace <ws> --project <id> --name "M-001 — ..."`.
- Create story: `linear issue create --workspace <ws> --team <key> --title "[US-001] ..." --project <id> --milestone "M-001 — ..." --description-file <path>`.
- Create task: `linear issue create --workspace <ws> --team <key> --title "[T-001] ..." --parent <story-id> --description-file <path>`.
- Update task status: `linear issue update <id> --state "<state>"`.
- Record PR / merge metadata: update the milestone **description**
  (`linear milestone update ... --description-file <path>`), per the format in
  "PR and merge metadata" above. Never record it as a comment on the milestone.
- Append review: `linear issue comment add <story-id> --body-file <path>`.
