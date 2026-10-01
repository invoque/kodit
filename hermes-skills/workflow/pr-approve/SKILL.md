---
name: pr-approve
description: >-
  Use after pr-review returns a clean milestone pull request — "approve and
  merge the PR", "finalize the milestone PR", or when the user asks to close out
  the reviewed milestone. Verifies project state, locates the reviewed PR,
  validates approval and merge readiness behind an explicit confirmation gate,
  publishes the approval, delegates the merge to github-pr-merge, records the
  merge in the tracker, and optionally cleans up the milestone branch. Never
  approves an ineligible identity and never merges without explicit
  confirmation.
version: 1.0.0
author: invoque
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [kodit, pull-request, pr, approve, merge, workflow, github]
    related_skills: [kodit-config, issue-tracker, github-pr-merge, gh-cli, pr-review]
---

# pr-approve

The pr-approve phase: finalize a reviewed milestone pull request through
approval, merge, and tracker reconciliation.

## When to Use

- Finalizing a reviewed milestone pull request: "approve and merge the PR",
  "merge the milestone branch", "close out the reviewed milestone".
- Handing off after `pr-review` returns a clean PR — it directs here when no
  blockers remain.
- Not for reviewing a PR — use the `pr-review` skill. Not for opening a PR — use
  the `pr-request` skill.

## Usage

A sequencer: it validates project state, reads PR state, publishes approval, and
sequences tracker writes, but delegates the merge itself. It runs the GitHub
reads and the single approval publish directly with `gh`, following the `gh-cli`
skill; the merge goes to `github-pr-merge`. Load each delegate with `skill_view`
when available. The delegates and their modes:

- **kodit-config** — check mode.
- **issue-tracker** — operate mode.
- **github-pr-merge** — its approval, merge, and cleanup steps.
- **gh-cli** — `gh` authentication and command behavior.

## Steps

### 1. Verify entry

Load the `kodit-config` skill with `skill_view` and follow it in **check mode**.
If `kodit.json` is missing, the project is not set up: say so and stop,
directing the user to the `setup-kodit` skill. If the `kodit-config` skill is
not installed, stop and report that it is required.

### 2. Select the target milestone

Load the `issue-tracker` skill with `skill_view` and follow it in **operate
mode** to read the project charter and every milestone. Identify the reviewed
milestone with a recorded `**PR:**`. Prefer the single non-`closed` milestone;
when all milestones are `closed`, select the most recent one with `**PR:**` but
no `**Merged:**` line. Refuse and stop when no eligible milestone exists. If the
`issue-tracker` skill is not installed, stop and report that it is required.

### 3. Validate approval and merge readiness (hard gate)

Steps 5–7 are forbidden unless this step confirms a single mergeable PR. Run
every command through `terminal`, following the `gh-cli` skill:

```
terminal(command="gh auth status")
terminal(command="gh pr view <N> --json number,url,headRefName,baseRefName,headRefOid,isDraft,mergeable,mergeStateStatus,reviewDecision,statusCheckRollup")
```

Confirm all of the following. Stop and report the specific blocker whenever any
one fails — do not publish approval, merge, or write the tracker:

- exactly one eligible PR is found (disambiguate with the user when several
  candidates exist),
- the PR is not a draft,
- required checks pass,
- review evidence exists for the current head SHA, and
- merge rules do not block the merge.

### 4. Present the confirmation gate

Show the user: milestone ID and goal, PR URL, current head SHA, review verdict,
check status, mergeability, and whether the current GitHub identity can publish
an `APPROVE` review. Ask the user to confirm approval and merge actions before
any remote write.

### 5. Publish approval

Publish an `APPROVE` review only after explicit confirmation:

```
terminal(command="gh pr review <N> --approve --body-file ./approval.md")
```

When the authenticated identity is ineligible (for example, it authored the PR)
or publishing fails, stop with the manual approval requirement and ask the user
to approve outside the workflow, then rerun. Do not merge while approval is
required but missing.

### 6. Delegate the merge

Load the `github-pr-merge` skill with `skill_view` and follow it with the
confirmation object containing the PR URL, the reviewed head SHA, the allowed
merge method, and the branch-cleanup preference. Ask about branch cleanup on
every successful-merge run. If the `github-pr-merge` skill is not installed,
stop and report that it is required and that no merge was performed.

### 7. Record the merge in the tracker

Follow the `issue-tracker` skill in **operate mode** to write `**Merged:**
<timestamp> | <sha>` in the milestone charter after GitHub confirms the merge.
Reconcile the milestone and project index tables so they reflect the final
repository state. Never write the merge line for a queued or failed result.

### 8. Stop and summarize

Present the merged PR, merge SHA, whether approval was published or required
manual action, the tracker line recorded, and whether the branch was deleted.
Do not prescribe the next workflow skill here.

## Pitfalls

- **Merging without explicit confirmation.** The confirmation gate in step 4 is
  mandatory; never publish an approval or trigger a merge before the user
  confirms.
- **Self-approval.** When the authenticated identity authored the PR, approval
  is ineligible: stop and require a separate reviewer; do not merge while
  approval is required but missing.
- **Proceeding past the hard gate.** Without one confirmed, non-draft, passing,
  mergeable PR with review evidence for the current head SHA, stop and name the
  blocker; never fall back to a local-only finalize.
- **Stale review evidence.** Re-read the head SHA in step 3; never merge when it
  differs from the reviewed SHA — request a fresh review first.
- **Writing the merge line early.** `**Merged:**` is written only after GitHub
  confirms the merge; a queued or failed result records nothing.
- **Interactive prompts hang the run.** `gh pr review` prompts without a body;
  write the body file first, and recreate it with a terminal heredoc if a remote
  backend cannot see a `write_file` artifact.
- **Improvising a missing dependency.** If `kodit-config`, `issue-tracker`, or
  `github-pr-merge` is not installed, stop and report it; do not hand-roll its
  work.

## Verification

- `kodit.json` was verified before any PR action.
- Exactly one reviewed milestone with a `**PR:**` was selected.
- A single, non-draft, passing, mergeable PR with review evidence for the
  current head SHA was confirmed before steps 5–7 ran.
- The user explicitly confirmed approval and merge before any remote write.
- Approval was published only when eligible, or the manual approval requirement
  was reported without merging.
- The merge was delegated to `github-pr-merge` and `gh pr view <N> --json
  state,mergedAt,mergeCommit` reflects the result.
- `**Merged:** <timestamp> | <sha>` was written only for a confirmed merge, and
  the milestone and project indexes agree.
- The summary reports PR, merge SHA, approval outcome, tracker line, and branch
  deletion, and names no next workflow skill.
