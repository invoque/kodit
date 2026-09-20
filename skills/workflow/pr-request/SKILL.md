---
name: pr-request
description: >-
  Use when milestone implementation is committed and ready for review — "open a
  PR", "request review", or after implement hands off. Verifies project setup
  and milestone readiness, delegates GitHub PR creation, records the PR URL
  without changing issue states, and hands off to pr-review. Refuses when no
  milestone is eligible. Defines only the sequence and the handoff.
---

# pr-request

Open a pull request for the active milestone branch.

## Usage

Invoke after `implement` completes a milestone, or when the user asks to open a
PR for implemented work. It is a pure orchestrator: it sequences checks and
delegates, never running `git`, `gh`, or tracker writes itself. Inputs are the
current project files; outputs are a created or reused PR plus a recorded URL.

## What You Must Do When Invoked

### 1. Verify entry

Follow the `kodit-config` skill in **check mode**. If `kodit.json` is missing,
the project is not set up: say so and stop, directing the user to `setup-kodit`.

### 2. Select and present the milestone

Follow the `issue-tracker` skill in **operate mode** to read the project charter
and every milestone. If no milestone is non-`closed`, refuse and direct the user
to `milestone-planning`. Work exactly one milestone: the single non-`closed`
one. Present its ID, goal, branch, and story/task counts.

### 3. Refuse when not ready

List every story and task. Stop without creating a PR when any task is still
`open`, `spec`, `plan`, or `implement`, is `blocked`, or carries
`ready-for-human`, `needs-info`, or `needs-triage`. Name what remains; never
mark tasks `done` here.

### 4. Derive the branches

Read `git.dev_branch`, `git.feature_prefix`, and `git.remote` from `kodit.json`.
The head is the milestone branch `<feature_prefix>m-NNN-<slug>`; the base is
`git.dev_branch` (default `dev`). If `git` is null or no remote is configured,
stop and explain that a PR needs a remote.

### 5. Delegate PR creation

Follow the `github-pr` skill with the head, base, remote, and a title and body
built from the milestone ID, goal, completed stories and tasks, verification
evidence, and review notes. Create immediately; on success keep the returned URL
and whether the PR was created or already existed.

### 6. Record the URL

Follow the `issue-tracker` skill in **operate mode** to write the URL as
`**PR:** <url>` in the milestone charter. This write is idempotent and changes
no task, story, or milestone status.

### 7. Summarize and hand off

Present the milestone, head into base, the PR URL, and what was recorded. Then
tell the user to run the **`pr-review`** skill. Do not merge.
