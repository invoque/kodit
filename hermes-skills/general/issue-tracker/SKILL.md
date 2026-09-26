---
name: issue-tracker
description: >-
  Owns a kodit project's issue tracker — choosing the backend, seeding a
  file-based tracker under `.kodit/issues/`, provisioning Linear projects, and
  creating, updating, moving, and querying milestones, user stories, and tasks.
  File-based and Linear backends are supported; owns the conventions, state
  machines, and backend dispatch for both. Use when adopting kodit, setting up
  issue tracking, or working tracker items — even if the user just says "set up
  issues", "where do issues live", "move T-003 to review", or "what's open in
  this milestone". Invoked by kodit-config and the workflow skills, and by the
  user directly.
version: 1.0.0
author: invoque
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [kodit, issues, tracker, milestones, linear, workflow]
    related_skills: [kodit-config, linear-cli]
---

# issue-tracker

Configures and operates the project's issue tracker.

## When to Use

- Adopting kodit and choosing how issues will be tracked (file-based vs Linear).
- Seeding or provisioning the tracker during kodit setup.
- Creating, updating, moving, or querying milestones, user stories, and tasks.
- Recording a PR URL, review outcome, or merge record against a milestone.
- Not for working a milestone item — the milestone workflow drives implement,
  review, and planning; this skill only reads and writes tracker records.

## Usage

Invoked in three modes. Read the conventions for the active backend before any
write: `references/file-based.md` for file, `references/linear.md` for Linear.

- **Setup mode** — choose a backend, check requirements, write
  `.kodit/tmp/setup-issue-tracker.md`. Does not seed or provision.
- **Provision mode** — after checkpoint approval, create or verify tracker
  resources (file seed or Linear project/milestones/labels/states).
- **Operate mode** — create, update, move, or query issues using the active
  backend's conventions.

## Modes

### Setup mode

1. Offer the backend choice with a recommendation: **file-based** (default,
   fully supported) or **Linear** (requires MCP or CLI). Ask with `clarify`, or
   directly in the conversation.
2. For file-based: confirm labels from `kodit.json`. For Linear:
   a. Ask the user for the **workspace** slug and **team** key.
   b. Run the access preflight with `terminal`:
      - Check for a write-capable Linear MCP integration.
      - Else check for an authenticated `linear-cli` (`linear auth whoami`).
      - If neither works, report the two remediation paths (connect MCP or
        install/authenticate CLI) and offer file-based as the alternative. The
        `linear-cli` skill covers installation and authentication; load it with
        `skill_view` when available, or ask the user directly.
   c. Verify the workspace is reachable: `linear team list --workspace <ws>`
      errors or returns nothing for an unknown workspace. (The global
      `--workspace` flag selects among configured credentials; it does not
      list workspaces — there is no `linear workspace` command.)
   d. Verify the team exists within the workspace:
      `linear team list --workspace <ws>` or MCP equivalent. If the team is not
      found and cannot be created (plan limit), stop and ask the user to pick
      an existing team.
   e. Record the resolved team ID in the draft.
3. Write `.kodit/tmp/setup-issue-tracker.md` with `write_file`: backend,
   workspace, team key and ID, labels, and any Linear-specific fields
   (linear_project, status_map). **Do not create tracker resources yet.**

### Provision mode

1. Read the setup draft `.kodit/tmp/setup-issue-tracker.md` with `read_file`.
   The draft is the source of truth during provisioning — `kodit.json` does not
   exist yet.
2. For file-based: create `.kodit/issues/` with `README.md` and `INDEX.md`
   using `write_file`, from the templates in `references/file-based.md`. Do not
   create milestones or stories.
3. For Linear:
   a. Verify `workspace` and `team.id` are present in the draft. If not,
      stop — do not guess or substitute defaults.
   b. Create or find the project **within the specified workspace**, running
      every command with `terminal`:
      `linear project list --workspace <workspace> --team <team-key>`.
      If not found, create it: `linear project create --workspace <workspace>
      --team <team-key> --name "<project-name>"`.
   c. Append the resolved project ID to the draft with `write_file` (do not
      write `kodit.json`).
   d. Ensure required workflow states exist **for the specified team**.
   e. Create labels if missing **for the specified workspace/team**.
   f. Report what was created or verified.
4. **Never** create a team, workflow state, or label in a workspace/team
   other than the one recorded in the draft.

### Operate mode

Dispatch by `issue_tracker.type` in `kodit.json`.

#### Common operations (all backends)

1. Read the item before changing it; never rewrite unrelated content.
2. Move a task only along allowed transitions. The machines are in the
   active backend's reference file.
3. Keep IDs stable and unique: never renumber, never reuse a retired ID.
4. When the caller reports a pull request URL for a milestone, record it
   as `**PR:** <url>` in the milestone charter without changing any status.
5. When a review reports outcomes, append a review record to each affected
   story and move task rows only along allowed transitions: pass moves
   `review → done`; blockers move `review → implement`.
6. When a merge is confirmed, verify milestone tasks are done or wontfix,
   reconcile derived status, and record `**Merged:** <timestamp> | <sha>`
   in the milestone charter.

#### File-specific operations

- Query by reading `.kodit/issues/` with `read_file`, or listing and filtering
  with `terminal`, on frontmatter fields.
- Write story and charter files directly with `write_file` and `patch`. See
  `references/file-based.md`.

#### Linear-specific operations

- Query via MCP or the CLI: `linear issue query`, `linear milestone list`, etc.
- Write via MCP or the CLI: `linear issue create`, `linear issue update`, etc.
- Run every `linear` command with `terminal`. Maintain the Kodit ID metadata
  block in issue descriptions.
- Maintain the tasks table in story issue descriptions as a convenience
  index; canonical status lives on each sub-issue.
- Record PR/merge metadata in milestone descriptions and review notes as
  comments on story issues. See `references/linear.md`.

## Pitfalls

- **Provisioning against the wrong scope.** Never create a team, workflow
  state, or label outside the workspace/team recorded in the setup draft. If
  the named team is missing, stop and report.
- **Requiring `kodit.json` during provisioning.** It does not exist yet; the
  setup draft is the source of truth until write mode. Never write `kodit.json`
  from this skill.
- **Partially configuring Linear.** If no MCP or CLI access is confirmed, stop
  and report exactly what is missing — do not configure half the tracker.
- **Renumbering or reusing IDs.** `M-`, `US-`, and `T-` numbers are global and
  never reused; a name identifies one artifact forever.
- **Stripping Kodit markers.** The `<!-- kodit:... -->` metadata blocks in
  Linear issue descriptions locate items. Never strip or overwrite them; append
  new content after them.
- **Commenting on a milestone.** Review notes are comments on story issues.
  Never pass a milestone ID to `issue comment`.
- **Moving on an invalid transition.** Only the transitions in the backend's
  state machine are legal; a story or milestone status is derived, not set by
  hand.

## Verification

- Setup mode: `.kodit/tmp/setup-issue-tracker.md` exists and carries the
  backend plus the resolved workspace and team ID.
- Provision mode: `.kodit/issues/README.md` and `INDEX.md` exist and match
  `references/file-based.md`, with no milestone directories; for Linear, the
  resolved project ID is appended to the draft and `kodit.json` is untouched.
- Every state named by `status_map` exists for the specified team.
- Operate mode: statuses moved only along the backend's state machine, Kodit
  markers intact, and the milestone/project tables agree with the item files.

## Reference files

Read the active backend's reference before any write:

| Topic | Read |
| --- | --- |
| File-based tree, labels, state machines, story and charter formats | `references/file-based.md` |
| Linear mapping, ID markers, status map, provisioning, issue operations | `references/linear.md` |
