---
name: issue-tracker
description: >-
  Use when setting up or interacting with a project's issue tracker under kodit
  — choosing a backend, seeding a file-based tracker, or creating, updating, and
  querying milestones, user stories, and tasks. Invoked by the setup-kodit
  workflow skill to configure tracking. File-based and Linear backends are
  supported. Owns the conventions, state machines, and backend dispatch for both.
---

# issue-tracker

Configures and operates the project's issue tracker.

## Usage

Invoked in three modes. Read the conventions for the active backend before any
write: `references/file-based.md` for file, `references/linear.md` for Linear.

- **Setup mode** — choose a backend, check requirements, write
  `.kodit/tmp/setup-issue-tracker.md`. Does not seed or provision.
- **Provision mode** — after checkpoint approval, create or verify tracker
  resources (file seed or Linear project/milestones/labels/states).
- **Operate mode** — create, update, move, or query issues using the active
  backend's conventions.

## What You Must Do When Invoked

### Setup mode

1. Offer the backend choice with a recommendation: **file-based** (default,
   fully supported) or **Linear** (requires MCP or CLI).
2. For file-based: confirm labels from `kodit.json`. For Linear:
   a. Ask the user for the **workspace** slug and **team** key.
   b. Run the access preflight:
      - Check for a write-capable Linear MCP integration.
      - Else check for an authenticated `linear-cli` (`linear auth whoami`).
      - If neither works, report the two remediation paths (connect MCP or
        install/authenticate CLI) and offer file-based as the alternative.
   c. Verify the workspace exists: `linear workspace list` or MCP equivalent.
      If not found, stop and ask the user to confirm the workspace slug.
   d. Verify the team exists within the workspace: `linear team list --workspace <ws>`
      or MCP equivalent. If the team is not found and cannot be created (plan
      limit), stop and ask the user to pick an existing team.
   e. Record the resolved team ID in the draft.
3. Write `.kodit/tmp/setup-issue-tracker.md` with backend, workspace, team key
   and ID, labels, and any Linear-specific fields (linear_project, status_map).
   **Do not create tracker resources yet.**

### Provision mode

1. Read the setup draft and `kodit.json`.
2. For file-based: create `.kodit/issues/` with `README.md` and `INDEX.md`
   from `references/file-based.md`. Do not create milestones or stories.
3. For Linear:
   a. Verify `workspace` and `team.id` are present in `kodit.json`. If not,
      stop — do not guess or substitute defaults.
   b. Create or find the project **within the specified workspace**:
      `linear project list --workspace <workspace> --team <team-key>`.
      If not found, create it: `linear project create --workspace <workspace>
      --team <team-key> --name "<project-name>"`.
   c. Record the resolved project ID in `kodit.json`.
   d. Ensure required workflow states exist **for the specified team**.
   e. Create labels if missing **for the specified workspace/team**.
   f. Report what was created or verified.
4. **Never** create a team, workflow state, or label in a workspace/team
   other than the one recorded in `kodit.json`.

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

- Query by reading `.kodit/issues/`, filtering on frontmatter fields.
- Write story and charter files directly. See `references/file-based.md`.

#### Linear-specific operations

- Query via MCP/CLI: `linear issue query`, `linear milestone list`, etc.
- Write via MCP/CLI: `linear issue create`, `linear issue update`, etc.
- Maintain the Kodit ID metadata block in issue descriptions.
- Maintain the tasks table in story issue descriptions as a convenience
  index; canonical status lives on each sub-issue.
- Record PR/merge metadata in milestone descriptions, review notes as
  comments on story issues. See `references/linear.md`.
