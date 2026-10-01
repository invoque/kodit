---
name: pr-review
description: >-
  Use after pr-request creates or identifies a milestone PR — "review the PR",
  "check the pull request", or run review for the active milestone. Verifies
  project state, locates exactly one active milestone and its open PR,
  coordinates a technical review with code-review, records the result, publishes
  findings to GitHub, updates story/task notes and statuses, and stops by
  telling the user to run implement for blockers or pr-approve when clean.
  Never approves and never merges.
version: 1.0.0
author: invoque
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [kodit, pull-request, pr, review, workflow, github]
    related_skills: [kodit-config, issue-tracker, code-review, gh-cli, pr-request]
---

# pr-review

The pr-review phase: review a milestone pull request and close the loop with the
tracker.

## When to Use

- Reviewing a milestone pull request: "review the PR", "check the pull request",
  "run the review for this milestone".
- Handing off after `pr-request` — it directs here once the PR exists.
- Not for opening a PR — use the `pr-request` skill. Not for approving or
  merging — that is `pr-approve`.

## Usage

A pure orchestrator: it sequences checks and delegates, running no `git` and no
tracker edits itself. It does run the GitHub reads and the single review
publish directly with `gh`, following the `gh-cli` skill. Load each delegate
with `skill_view` when available. The delegates and their modes:

- **kodit-config** — check mode.
- **issue-tracker** — operate mode.
- **code-review** — its review procedure.
- **gh-cli** — `gh` authentication and command behavior.

## Steps

### 1. Verify entry

Load the `kodit-config` skill with `skill_view` and follow it in **check mode**.
If `kodit.json` is missing, the project is not set up: say so and stop,
directing the user to the `setup-kodit` skill. If the `kodit-config` skill is
not installed, stop and report that it is required.

### 2. Identify the active milestone

Load the `issue-tracker` skill with `skill_view` and follow it in **operate
mode**. Exactly one milestone must be `active`. Refuse when none is active or
more than one is open, naming what the user should do (implement, close, or
re-scope it). If the `issue-tracker` skill is not installed, stop and report
that it is required.

### 3. Locate and validate the PR (hard gate)

Steps 4–9 are forbidden unless this step produces a single confirmed PR with
read access. Stop immediately when any of these is true — do not write a review
record, change tracker state, or fall back to a local-only review:

- No eligible PR exists.
- GitHub read access is missing or unauthenticated.
- Multiple candidate PRs exist and need user disambiguation.

Run every command through `terminal`, following the `gh-cli` skill:

```
terminal(command="gh auth status")
terminal(command="gh pr list --head <head> --base <base> --state open --json number,title,url,author")
```

Check the milestone charter's `**PR:**` record first (issue-tracker operate
mode); only if it is absent, search by head/base. With exactly one PR,
read its state:

```
terminal(command="gh pr view <N> --json number,url,headRefName,baseRefName,mergeable,mergeStateStatus,reviewDecision,statusCheckRollup")
```

Report which precondition failed and direct the user to `pr-request` or to
disambiguate the PRs.

### 4. Present the review context

Show the user: milestone ID and goal, branch pair, PR URL, check status,
mergeability, current task states, and whether a GitHub review can be published
(permissions and review eligibility from `gh`).

### 5. Coordinate the technical review

Load the `code-review` skill with `skill_view` and follow it, supplying the
active milestone, relevant specs/plans, the task list, and the PR facts from
step 3. Receive findings, severity counts, and recommended status moves. If the
`code-review` skill is not installed, stop and report that it is required.

### 6. Write the local review record

Follow the `issue-tracker` skill in **operate mode** to write
`.kodit/tmp/specs/review-M-NNN-<slug>.md`, using the shape in
`references/review-report.md`: milestone, PR, verdict, findings, evidence, fix
recommendations, and task transitions. Write it with `write_file`. Keep this
file until the milestone closes.

### 7. Publish findings to GitHub

Write the review body with `write_file`, then publish it with `terminal`:

- Any blocker exists:

  ```
  terminal(command="gh pr review <N> --request-changes --body-file ./review-body.md")
  ```

- No blocker, and publishing is permitted:

  ```
  terminal(command="gh pr review <N> --comment --body-file ./review-body.md")
  ```

Never use `--approve` and never merge. When publishing is not permitted or
fails, report it and continue to step 8; the local record still stands.

### 8. Update the tracker

Follow the `issue-tracker` skill in **operate mode** to move each reviewed task:
pass → `review → done`, blocked → `review → implement`. Append a `## Review`
note to each affected user story with the PR URL, review file, verdict, finding
summary, and fix expectations. Update milestone/story indexes only as the
issue-tracker requires to stay consistent.

### 9. Stop and hand off

Summarize milestone, PR, verdict, blocker count, changed tasks, and review file
path. When blockers remain, tell the user to run the **`implement`** skill to
fix them. When there are none, tell the user to run the **`pr-approve`** skill
to finalize merge handling. If a handoff skill is not installed, name it as the
next skill to install.

## Pitfalls

- **Proceeding past the hard gate.** Without one confirmed PR and read access,
  there is no review record, no publish, and no tracker change — and no
  local-only fallback. Report the failed precondition and stop.
- **Approving or merging.** This skill publishes request-changes or a comment
  only; approval and merge belong to `pr-approve`.
- **Interactive prompts hang the run.** `gh pr review` needs `--body-file` or it
  prompts; write the body file first, and recreate it with a terminal heredoc
  if a remote backend cannot see it.
- **Silent disambiguation.** Multiple candidate PRs are a stop: name them and
  ask the user which one is the milestone PR; never pick one silently.
- **Improvising a missing dependency.** If `kodit-config`, `issue-tracker`, or
  `code-review` is not installed, stop and report it; do not hand-roll its work.
- **Changing unreviewed state.** Transition only tasks the review covered, and
  only to the states step 8 names.

## Verification

- `kodit.json` was verified before any PR action.
- Exactly one `active` milestone was identified.
- A single open PR with read access was confirmed before steps 4–9 ran.
- The review record exists at `.kodit/tmp/specs/review-M-NNN-<slug>.md` with
  milestone, PR, verdict, findings, evidence, fix recommendations, and
  transitions.
- Findings were published as `request-changes` when blockers exist, otherwise as
  a comment, never as an approval; a publishing limitation was reported without
  aborting the local record.
- Task transitions are exactly `review → done` (pass) and `review → implement`
  (blocked), and affected stories carry a `## Review` note.
- The handoff names `implement` for blockers or `pr-approve` when clean, and no
  merge was performed.

## Reference files

| Topic | Read |
| --- | --- |
| Local review record shape for `.kodit/tmp/specs/review-M-NNN-<slug>.md` | `references/review-report.md` |
