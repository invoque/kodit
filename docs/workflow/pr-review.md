# pr-review

Review a milestone pull request and close the loop with the tracker.

## When to Use

- After `pr-request` creates or identifies a milestone PR.
- When you ask to review the PR for the active milestone.

## Prerequisites

- `kodit.json` must exist (checked via `kodit-config` in check mode).
- Exactly one milestone must be `active`.
- **Hard gate:** exactly one open PR must exist with confirmed read access. Steps 4–9 are **forbidden** unless this gate passes. When any precondition fails, stop immediately — no review record, no tracker changes.

The hard gate refuses when:
- No eligible PR exists.
- GitHub read access is missing or unauthenticated.
- Multiple candidate PRs exist and need user disambiguation.

## How It Works

### 1. Verify entry

Follow `kodit-config` in check mode. Stop and direct to `setup-kodit` when setup is incomplete.

### 2. Identify the active milestone

Follow `issue-tracker` in operate mode. Exactly one milestone must be `active`.

### 3. Locate and validate the PR (hard gate)

Follow `github-pr-state` to select exactly one open PR for the active milestone branch. **Steps 4–9 are forbidden unless this step produces a single confirmed PR with read access.** When any precondition fails, stop immediately.

### 4. Present the review context

Show the user: milestone ID and goal, branch pair, PR URL, check status, mergeability, current task states, and whether a GitHub review can be published.

### 5. Coordinate the technical review

Follow `code-review`. Supply the active milestone, relevant specs/plans, task list, and PR facts. Receive findings, severity counts, and recommended status moves.

### 6. Write the local review record

Follow `issue-tracker` in operate mode to write `.kodit/tmp/specs/review-M-NNN-<slug>.md` with milestone, PR, verdict, findings, evidence, fix recommendations, and task transitions.

### 7. Publish findings to GitHub

Follow `github-pr-state` to publish the review. When any blocker exists, request changes. Otherwise publish a comment when permitted. **Never approve, never merge.**

### 8. Update the tracker

Follow `issue-tracker` in operate mode to move each reviewed task:
- Pass: `review → done`
- Blocked: `review → implement`

Append a `## Review` note to each affected user story with the PR URL, review file, verdict, finding summary, and fix expectations.

### 9. Stop and hand off

Summarize milestone, PR, verdict, blocker count, changed tasks, and review file path.
- **Blockers remain:** tell the user to run `implement`.
- **No blockers:** tell the user to run `pr-approve`.

## User Decisions

None explicitly. The user receives the review context (step 4) before the technical review is coordinated.

## Key Rules

- **Hard gate is absolute.** If the PR cannot be located with read access, nothing downstream runs. No fallback to local-only review.
- **No approve, no merge.** This skill publishes `REQUEST_CHANGES` or `COMMENT` only. Approval belongs to `pr-approve`.
- **Review record persists.** The local review file lives until the milestone closes.
- **Loop back on blockers.** When issues are found, the workflow returns to `implement` before `pr-approve`.

## Artifacts Created

- `.kodit/tmp/specs/review-M-NNN-<slug>.md` — local review record

## Artifacts Modified

- Story records — review notes appended via issue-tracker operate mode
- Task statuses — `review → done` or `review → implement`

## Handoff

- **Blockers:** `implement`
- **Clean:** `pr-approve`

## Source

- Canonical definition: `skills/workflow/pr-review/SKILL.md`
- Local review record format: `skills/workflow/pr-review/references/review-report.md`
