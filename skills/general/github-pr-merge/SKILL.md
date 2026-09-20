---
name: github-pr-merge
description: >-
  Use when a Kodit caller needs a GitHub pull request approved, merged, or
  cleaned up after an explicit confirmation object is presented — approve and
  merge the milestone PR only after final user confirmation and only when the
  repository allows it. Never create a PR, never use an admin bypass, and never
  approve when the authenticated identity is ineligible. For state reads or
  constrained review publishing, use github-pr-state.
---

# github-pr-merge

Approve and merge a confirmed pull request, or report why it cannot be merged.

## Usage

Invoked by workflow skills that already have review evidence and a user-approved
merge confirmation. Inputs are a confirmation object plus the repository path,
remote, PR, and any optional branch-cleanup preference; outputs are approval,
merge, and cleanup outcomes. All GitHub-specific approve/merge mechanics stay
here.

## What You Must Do When Invoked

### 1. Validate access

Confirm a GitHub capability exists: authenticated `gh` CLI or GitHub MCP tools
with merge/approve permissions. Stop with the missing piece named when access,
permissions, or the remote is absent.

### 2. Read the current PR state

Locate the PR by number, URL, or recorded charter reference and re-read its
current state. Return when any precondition blocks action:

- PR not found or unreadable.
- Repository rules prohibit approval or merge.
- The current head SHA differs from the reviewed SHA.
- Checks are failing, pending in a blocking queue, or unknown.
- The PR is a draft or not in a mergeable repository state.

Name the blocker clearly; never guess a merge capability.

### 3. Resolve approval

- When approval is required, use the confirmation object to determine whether a
  separate eligible reviewer identity is available.
- Publish `APPROVE` only when permitted and only after explicit workflow
  confirmation.
- When the authenticated identity is ineligible, stop and return the manual
  approval requirement; do not approve and do not merge.
- When approval is already satisfied by repository rules, skip publishing it
  again.

### 4. Merge only after confirmation

- Require the workflow confirmation object to contain the PR URL, the reviewed
  head SHA, the intended merge method, and whether branch deletion is requested.
- Perform the final pre-merge check on current state: required checks pass, the
  PR is not blocked by rules, and the merge method is allowed by repository
  policy.
- Never use `--admin`, never bypass branch protection, and never bypass merge
  queues.
- Use repository policy as the authoritative merge method; request the allowed
  method even if the caller prefers another.
- When the PR is queued or waiting on checks, return `queued` with the expected
  next step instead of forcing a direct merge.

### 5. Clean up the branch

- Handle deletion only when the confirmation explicitly requests it and the merge
  succeeds.
- Prefer deleting both local and remote references when the workflow can confirm
  them.
- When deletion fails, report the failure but keep the merge result visible.

### 6. Return the result

Report at least:

- `approval_result`: `approved`, `not_required`, `ineligible`, or `failed`.
- `merge_result`: `merged`, `queued`, or `blocked`.
- `merge_sha`: the merge commit or SHA when merged.
- `branch_deleted`: `true` / `false` when cleanup was attempted.

Keep tooling details internal and keep failure messages actionable.
