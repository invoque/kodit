# pr-approve

Finalize a reviewed milestone pull request through approval, merge, and tracker reconciliation.

## When to Use

- After a clean `pr-review` (no blockers remain).
- When you want to merge the active milestone PR.

## Prerequisites

- `kodit.json` must exist (checked via `kodit-config` in check mode).
- A reviewed milestone with a recorded PR must exist.
- PR must be: not a draft, checks pass, review evidence exists for the current head SHA, merge rules do not block.

## How It Works

### 1. Verify entry

Follow `kodit-config` in check mode. Stop and direct to `setup-kodit` when setup is incomplete.

### 2. Select the target milestone

Follow `issue-tracker` in operate mode. Prefer the single non-`closed` milestone. When all milestones are `closed`, select the most recent with `**PR:**` but no `**Merged:**` line. Refuse when no eligible milestone exists.

### 3. Validate approval readiness

Follow `github-pr-state` to read current PR state. Confirm: exactly one eligible PR, not a draft, checks pass, review evidence exists for the current head SHA, merge rules do not block. Stop and report the specific blocker whenever any precondition fails.

### 4. Present the confirmation gate

Show the user: milestone ID and goal, PR URL, current head SHA, review verdict, check status, mergeability, and whether the current GitHub identity can publish an `APPROVE` review. **Ask the user to confirm before any remote write.**

### 5. Publish approval when required

Follow `github-pr-state` to publish an `APPROVE` review only after explicit confirmation. When the identity is ineligible or publishing fails, stop with the manual approval requirement. **Do not merge while approval is required but missing.**

### 6. Delegate the merge

Follow `github-pr-merge` with the PR URL, reviewed head SHA, allowed merge method, and branch-cleanup preference. Ask about branch cleanup on **every** successful merge.

### 7. Record the merge in the tracker

Follow `issue-tracker` in operate mode to write `**Merged:** <timestamp> | <sha>` in the milestone charter after GitHub confirms the merge. Reconcile milestone and project index tables. **Never write the merge line for a queued or failed result.**

### 8. Stop and summarize

Present the merged PR, merge SHA, whether approval was published or required manual action, the tracker line recorded, and whether the branch was deleted. **Do not prescribe the next workflow skill.**

## User Decisions

| Step | Decision |
|---|---|
| 4 | Confirmation of approval and merge actions (before any remote write) |
| 6 | Branch cleanup (asked on every successful merge) |

## Key Rules

- **Explicit confirmation required.** No remote write happens without user approval.
- **Ineligible identity.** When the authenticated identity cannot publish `APPROVE`, the skill stops and requires manual approval outside the workflow.
- **Merge line integrity.** The `**Merged:**` line is written only after GitHub confirms an actual merge — never for queued or failed results.
- **Terminal skill.** This is the last skill in the workflow loop. It does not prescribe a next skill.

## Artifacts Modified

- Milestone charter (`**Merged:**` line appended after confirmed merge) via issue-tracker operate mode

## Handoff

**None.** This is the terminal workflow skill. The milestone is closed.

## Source

- Canonical definition: `skills/workflow/pr-approve/SKILL.md`
