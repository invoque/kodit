---
name: pr-request
description: >-
  Use when milestone implementation is committed and ready for review — "open a
  PR", "request review", or after implement hands off. Verifies project setup
  and milestone readiness, delegates GitHub PR creation, records the PR URL
  without changing issue states, and hands off to pr-review. Refuses when no
  milestone is eligible. Defines only the sequence and the handoff.
version: 1.0.0
author: invoque
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [kodit, pull-request, pr, review, workflow, github]
    related_skills: [kodit-config, issue-tracker, github-pr, milestone-planning]
---

# pr-request

The pr-request phase: open a pull request for the active milestone branch.

## When to Use

- Opening a pull request for implemented milestone work: "open a PR", "request
  review", "create the PR for this milestone".
- Handing off after implementation — the `implement` skill completes a milestone
  and directs here.
- Not for reviewing a PR — use the `pr-review` skill. Not for approving or
  merging — that is `pr-approve`.

## Usage

A pure orchestrator: it sequences checks and delegates, never running `git`,
`gh`, or tracker writes itself. Load each delegate with `skill_view` when
available. The delegates and their modes:

- **kodit-config** — check mode.
- **issue-tracker** — operate mode.
- **github-pr** — its PR creation steps.

## Steps

### 1. Verify entry

Load the `kodit-config` skill with `skill_view` and follow it in **check mode**.
If `kodit.json` is missing, the project is not set up: say so and stop,
directing the user to the `setup-kodit` skill. If the `kodit-config` skill is
not installed, stop and report that it is required.

### 2. Select and present the milestone

Load the `issue-tracker` skill with `skill_view` and follow it in **operate
mode** to read the project charter and every milestone. If no milestone is
non-`closed`, refuse and direct the user to the `milestone-planning` skill. Work
exactly one milestone: the single non-`closed` one. Present its ID, goal,
branch, and story/task counts. If the `issue-tracker` skill is not installed,
stop and report that it is required.

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

Load the `github-pr` skill with `skill_view` and follow it with the head, base,
remote, and a title and body built from the milestone ID, goal, completed
stories and tasks, verification evidence, and review notes. Create immediately;
on success keep the returned URL and whether the PR was created or already
existed. If the `github-pr` skill is not installed, stop and report that it is
required.

### 6. Record the URL

Follow the `issue-tracker` skill in **operate mode** to write the URL as
`**PR:** <url>` in the milestone charter. This write is idempotent and changes
no task, story, or milestone status.

### 7. Summarize and hand off

Present the milestone, head into base, the PR URL, and what was recorded. Then
tell the user to run the **`pr-review`** skill. If the `pr-review` skill is not
installed, name it as the next skill to install. Do not merge.

## Pitfalls

- **Opening a PR with unfinished work.** Any task still `open`, `spec`, `plan`,
  or `implement`, `blocked`, or carrying `ready-for-human`, `needs-info`, or
  `needs-triage` is a stop. Name what remains; never open the PR anyway.
- **Changing issue state here.** The step 6 write records only the PR URL. Never
  mark tasks `done`, and never change a task, story, or milestone status.
- **Creating a duplicate PR.** Delegate to `github-pr`, which reuses an existing
  open PR for the same head and base. Never open a second one.
- **A milestone branch with no remote.** A PR needs a configured remote; if
  `git` is null or the remote is missing, stop and explain rather than
  improvising one.
- **Merging.** This skill stops at the handoff. Approval and merge belong to
  `pr-approve`.
- **Improvising a missing dependency.** If a required delegate skill (`kodit-config`,
  `issue-tracker`, or `github-pr`) is not installed, stop and report it; do not
  hand-roll its work.

## Verification

- `kodit.json` was verified before any PR action was attempted.
- Exactly one non-`closed` milestone was selected and presented.
- No task was still `open`, `spec`, `plan`, `implement`, `blocked`, or carrying
  `ready-for-human`, `needs-info`, or `needs-triage` before the PR was created.
- The milestone charter records the PR URL, and no task, story, or milestone
  status changed.
- An existing open PR for the head and base was reused, not duplicated.
- The handoff names the `pr-review` skill, and no merge was performed.
