---
name: pr-review
description: >-
  Use after pr-request creates or identifies a milestone PR — "review the PR",
  "check the pull request", or run review for the active milestone. Verifies
  project state, locates exactly one active milestone and its PR, coordinates a
  technical review, records the result, publishes findings, updates story/task
  notes/statuses, and stops by telling the user to run implement for blockers.
---

# pr-review

Review a milestone pull request and close the loop with the tracker.

## Usage

Invoke after `pr-request` completes or when the user asks for PR review on the
active milestone. It is a pure orchestrator: it validates state, delegates reads
and technical review, and sequences writes, but never runs `git`, `gh`, tracker
edits, or GitHub review publishing itself.

## What You Must Do When Invoked

### 1. Verify entry

Follow the `kodit-config` skill in **check mode**. Stop and direct the user to
`setup-kodit` when setup is incomplete.

### 2. Identify the active milestone

Follow the `issue-tracker` skill in **operate mode**. Exactly one milestone must
be `active`. Refuse when none is active or more than one is open.

### 3. Locate and validate the PR (hard gate)

Follow the `github-pr-state` skill to select exactly one open PR for the active
milestone branch. **Steps 4–9 are forbidden unless this step produces a single
confirmed PR with read access.** When any of the following is true, stop
immediately — do not write a review record, change tracker state, or fall back
to local-only review:

- No eligible PR exists.
- GitHub read access is missing or unauthenticated.
- Multiple candidate PRs exist and need user disambiguation.

Report which precondition failed and direct the user to `pr-request` or to
disambiguate the PRs. Do not proceed further.

### 4. Present the review context

Show the user: milestone ID and goal, branch pair, PR URL, check status,
mergeability, current task states, and whether a GitHub review can be published.

### 5. Coordinate the technical review

Follow the `code-review` skill. Supply the active milestone, relevant
specs/plans, task list, and the PR facts from `github-pr-state`. Receive
findings, severity counts, and recommended status moves.

### 6. Write the local review record

Follow the `issue-tracker` skill in **operate mode** to write
`.kodit/tmp/specs/review-M-NNN-<slug>.md` with milestone, PR, verdict,
findings, evidence, fix recommendations, and task transitions. Keep this file
until the milestone closes.

### 7. Publish findings to GitHub

Follow the `github-pr-state` skill to publish the review. When any blocker
exists, request changes. Otherwise publish a comment when publishing is
permitted. Never approve, never merge.

### 8. Update the tracker

Follow the `issue-tracker` skill in **operate mode** to move each reviewed task:
- pass: `review → done`
- blocked: `review → implement`

Append a `## Review` note to each affected user story with the PR URL, review
file, verdict, finding summary, and fix expectations. Update milestone/story
indexes only as the issue-tracker requires to stay consistent.

### 9. Stop and hand off

Summarize milestone, PR, verdict, blocker count, changed tasks, and review file
path. When blockers remain, tell the user to run **`implement`** to fix them.
When there are none, do not merge; present the result and stop.
