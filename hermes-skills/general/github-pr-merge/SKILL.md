---
name: github-pr-merge
description: >-
  Approve and merge a confirmed GitHub pull request after an explicit
  confirmation object is presented — "merge the PR", "approve and merge", or a
  kodit pr-approve handoff. Validates GitHub access, re-reads current PR state,
  resolves approval eligibility, merges with the repository-allowed method, and
  optionally cleans up the branch. Never creates a PR, never uses an admin
  bypass, and never approves when the authenticated identity is ineligible. For
  state reads or review publishing, use gh directly.
version: 1.0.0
author: invoque
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [github, pull-request, merge, approval]
    related_skills: [github-pr, gh-cli, code-review]
    requires_toolsets: [terminal]
---

# github-pr-merge

Approve and merge a confirmed pull request, or report why it cannot be merged.

## When to Use

- A caller has review evidence and a user-approved merge confirmation and needs
  the PR approved, merged, or cleaned up.
- The user says "merge the PR", "approve and merge", or a kodit `pr-approve`
  flow hands off.
- Not for creating a PR — use `github-pr`.
- Not for reviewing code or publishing review findings — use `code-review`.
- Not for reading PR state or a first-pass review comment — read it with `gh`
  directly.

## Usage

Inputs: a confirmation object containing the PR URL, the reviewed head SHA, the
intended merge method, and whether branch deletion is requested — plus the
repository path and remote. Outputs: approval, merge, and cleanup outcomes. All
GitHub approve/merge mechanics stay here.

Run every `gh` and `git` command through `terminal`. For install,
authentication (`GH_TOKEN` or `gh auth login`), and `gh` behavior details,
follow the `gh-cli` skill; load it with `skill_view` when available, otherwise
run the commands below directly. When the git remote is ambiguous or another
repository is meant, pass `-R OWNER/REPO` or set `GH_REPO`.

## Steps

### 1. Validate access

Confirm a GitHub capability exists: an authenticated `gh` CLI with merge and
approve permission:

```
terminal(command="gh auth status")
```

Stop with the missing piece named when access, permissions, or the remote is
absent. Never guess a merge capability.

### 2. Read the current PR state

Locate the PR by number or URL and re-read its current state:

```
terminal(command="gh pr view <N> --json state,headRefName,baseRefName,headRefOid,mergeable,mergeStateStatus,reviewDecision")
```

Return with the blocker named when any precondition blocks action:

- PR not found or unreadable.
- Repository rules prohibit approval or merge.
- The current head SHA differs from the reviewed SHA.
- Checks are failing, pending in a blocking queue, or unknown.
- The PR is a draft or not in a mergeable repository state.

### 3. Resolve approval

- When approval is required, use the confirmation object to determine whether a
  separate eligible reviewer identity is available.
- Publish approval only when permitted and only after explicit confirmation:

  ```
  terminal(command="gh pr review <N> --approve")
  ```

- When the authenticated identity is ineligible (for example, it authored the
  PR), stop and return the manual approval requirement; do not approve and do
  not merge.
- When approval is already satisfied by repository rules, skip publishing it
  again.

### 4. Merge only after confirmation

- Require the confirmation object to contain the PR URL, the reviewed head SHA,
  the intended merge method, and whether branch deletion is requested.
- Perform the final pre-merge check on current state: required checks pass, the
  PR is not blocked by rules, and the merge method is allowed by repository
  policy.
- Merge with the repository-allowed method:

  ```
  terminal(command="gh pr merge <N> --squash")   # or --merge / --rebase per policy
  ```

- Never use `--admin`, never bypass branch protection, and never bypass merge
  queues.
- Use repository policy as the authoritative merge method; request the allowed
  method even if the caller prefers another.
- When the PR is queued or waiting on checks, return `queued` with the expected
  next step instead of forcing a direct merge.

### 5. Clean up the branch

- Handle deletion only when the confirmation explicitly requests it and the
  merge succeeds.
- Prefer deleting both local and remote references when the workflow can confirm
  them:

  ```
  terminal(command="git branch -d <branch>")
  terminal(command="git push <remote> --delete <branch>")
  ```

- When deletion fails, report the failure but keep the merge result visible.

### 6. Return the result

Report at least:

- `approval_result`: `approved`, `not_required`, `ineligible`, or `failed`.
- `merge_result`: `merged`, `queued`, or `blocked`.
- `merge_sha`: the merge commit or SHA when merged.
- `branch_deleted`: `true` / `false` when cleanup was attempted.

Keep tooling details internal and keep failure messages actionable.

## Pitfalls

- **Stale review evidence.** Never merge when the current head SHA differs from
  the reviewed SHA; request a fresh review or explicit reconfirmation against
  the current head.
- **Self-approval.** When the authenticated identity authored the PR, approval
  is ineligible — stop and require a separate eligible reviewer before rerunning.
- **Admin bypass temptation.** `gh pr merge --admin` is never allowed, even when
  offered; do not bypass branch protection or merge queues.
- **Merge-method override.** Repository policy wins over caller preference;
  read the allowed method before requesting a merge.
- **Forcing a queued merge.** A PR waiting on checks or queued returns `queued`;
  report the expected next step rather than retrying a forced merge.
- **Repo ambiguity.** `gh` reports from the git remote; pass `-R OWNER/REPO` or
  set `GH_REPO` in a directory without a `github.com` remote or for another
  repository.
- **Deleting the wrong branch.** Clean up only after a successful merge and only
  when the confirmation requested it; never force-delete.

## Verification

- `terminal(command="gh pr view <N> --json state,mergedAt,mergeCommit")` shows
  the PR merged (or the returned `queued`/`blocked` state).
- Approval was published only after explicit confirmation or reported as
  `ineligible` without merging.
- No `--admin` flag, branch-protection bypass, or merge-queue bypass was used.
- The merge method matched repository policy.
- The result reports `approval_result`, `merge_result`, `merge_sha`, and
  `branch_deleted`; `branch_deleted` is present only when cleanup was requested.
