---
name: setup-kodit
description: >-
  Use when the user wants to adopt or initialize kodit in a project — "set up
  kodit", "initialize this project for kodit", "get started with the kodit
  workflow" — or when a setup was interrupted and needs resuming. Checks
  adoption state, interviews for project metadata, issue tracking, and git
  branching, checkpoints for review, then writes kodit.json, AGENTS.md,
  README.md, CONTEXT.md, and .kodit/. This is the setup phase; it defines only
  the sequence and delegates the work. Not for milestone work.
---

# setup-kodit

The setup phase: initialize `kodit` in a project, one reviewable step at a time.

## Usage

Invoke when a project is adopting `kodit` or when a setup left
`.kodit/tmp/setup-*.md` drafts behind. It delegates all work to general skills
and never writes configuration itself. Read `references/summary-format.md`
before presenting the checkpoint or the final summary.

## What You Must Do When Invoked

### 1. Check the project

Follow the `kodit-config` skill in **check mode**: adoption state,
`.kodit/tmp/`, git, and existing `setup-*.md` drafts. If `kodit.json` exists,
present the completed state and stop — do not reconfigure unless the user asks.
Otherwise, keep the reported resume point: the first step below with no draft.
Drafts already present are re-confirmed, not re-asked.

### 2. Settle project metadata

If `.kodit/tmp/setup-project-metadata.md` is missing, follow
the `kodit-config` skill in **metadata mode** (it runs the
`interview`). Otherwise re-confirm the draft with the user.

### 3. Settle issue tracking

If `.kodit/tmp/setup-issue-tracker.md` is missing, follow
the `issue-tracker` skill in **setup mode**. Otherwise re-confirm
the draft.

### 4. Settle git branching

If `.kodit/tmp/setup-git-branching.md` is missing, follow
the `git-branching` skill. Otherwise re-confirm the draft.

### 5. Checkpoint — STOP

Present the review summary in the format from `references/summary-format.md`:
per-section tables from the three drafts, the exact `kodit.json` that will be
written, rendered previews of each document's managed block, and a file plan
with per-file actions (create, append, no-op, migrate, or legacy-retained).
If legacy sections are detected, show their bounded diff. Ask the user to
review. Route each change request back to the step that owns it, rewrite that
draft, and present the checkpoint again. Do not continue without approval.

### 6. Write the configuration

Follow the `kodit-config` skill in **write mode** to write
`kodit.json`, render managed blocks into `AGENTS.md`, `README.md`, and
`CONTEXT.md` (creating shells, appending, or migrating per the document-state
matrix), write `.kodit/.gitignore`, and delete all `.kodit/tmp/setup-*.md`
drafts. Report each file and its action: created, appended, no-op, migrated,
or legacy-retained.

### 7. Hand off

Present the final summary from `references/summary-format.md` — what was
written, the branch and issue configuration, and the next action: invoke the
`milestone-planning` skill to agree the first milestone. Offer to commit the
setup if the project's conventions expect it.
