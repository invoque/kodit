---
name: pr-approve
description: >-
  Use after pr-review returns a clean milestone pull request — "approve and
  merge the PR", "finalize the milestone PR", or when the user asks to close out
  the reviewed milestone. Locates the reviewed PR, verifies approval and merge
  eligibility, requires final confirmation, delegates approval and merge to
  github-pr-merge, records the merge in the tracker, and optionally cleans up
  the milestone branch. Never approves an ineligible identity and never merges
  without explicit confirmation.
---

# pr-approve

Finalize a reviewed milestone pull request through approval, merge, and tracker reconciliation.

## Usage

Invoke after a clean `pr-review` or when the user wants to merge the active
milestone PR. It is a pure orchestrator: it validates project state, confirms
approval and merge readiness, delegates GitHub actions, and sequences tracker
writes, but never runs `git`, `gh`, or tracker edits itself.

## What You Must Do When Invoked

### 1. Verify entry

Follow the `kodit-config` skill in **check mode**. Stop and direct the user to
`setup-kodit` when setup is incomplete.

### 2. Select the target milestone

Follow the `issue-tracker` skill in **operate mode**. Identify the reviewed
milestone with a recorded PR. Prefer the single non-`closed` milestone when one
exists; when all milestones are `closed`, select the most recent milestone with
`**PR:**` but no `**Merged:**` line. Refuse when no eligible milestone exists.

### 3. Validate approval readiness

Follow the `github-pr-state` skill to read current PR state. Confirm:

- exactly one eligible PR is found,
- the PR is not a draft,
- required checks pass,
- review evidence exists for the current head SHA, and
- merge rules do not block the merge.

Stop and report the specific blocker whenever any precondition fails.

### 4. Present the confirmation gate

Show the user: milestone ID and goal, PR URL, current head SHA, review verdict,
check status, mergeability, and whether the current GitHub identity can publish
an `APPROVE` review. Ask the user to confirm approval and merge actions before
any remote write.

### 5. Publish approval when required

Follow the `github-pr-state` skill to publish an `APPROVE` review only after
explicit confirmation. When the authenticated identity is ineligible or
publishing fails, stop with the manual approval requirement and ask the user to
approve outside the workflow, then rerun. Do not merge while approval is
required but missing.

### 6. Delegate the merge

Follow the `github-pr-merge` skill with the confirmation object containing the
PR URL, reviewed head SHA, allowed merge method, and branch-cleanup preference.
Ask about branch cleanup on every successful-merge run.

### 7. Record the merge in the tracker

Follow the `issue-tracker` skill in **operate mode** to write `**Merged:**
<timestamp> | <sha>` in the milestone charter after GitHub confirms the merge.
Reconcile the milestone and project index tables so they reflect the final
repository state. Never write the merge line for a queued or failed result.

### 8. Stop and summarize

Present the merged PR, merge SHA, whether approval was published or required
manual action, the tracker line recorded, and whether the branch was deleted.
Do not prescribe the next workflow skill here.
