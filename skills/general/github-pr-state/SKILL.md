---
name: github-pr-state
description: >-
  Use when any Kodit caller needs GitHub pull request state read or published
  without opening the PR — locate the milestone PR, inspect metadata, checks,
  reviews, comments, diff, and merge capability, or publish a REQUEST_CHANGES /
  COMMENT review. Never approve, merge, or create the PR; for creation use
  github-pr.
---

# github-pr-state

Read GitHub pull request state and publish constrained review feedback.

## Usage

Invoked by workflow skills that need to inspect an already-open PR or publish a
review. Inputs are the repository path, remote, head/base branches, and
optionally milestone/task identifiers; outputs are a structured PR state report
and, when requested, a published GitHub review. All GitHub-specific mechanics
stay here.

## What You Must Do When Invoked

### 1. Validate access

Confirm the repository has a GitHub capability: GitHub MCP tools or an
authenticated `gh` CLI. Stop with the missing piece named when access,
authentication, or the remote is absent.

### 2. Locate the candidate PR

Check the milestone charter for a recorded PR URL first. When absent, search by
head/base (`gh pr list --head <head> --base <base> --state open` or MCP
equivalent). Return one of:

- `none`,
- a single selected PR with the selection reason,
- multiple candidates with required user disambiguation.

### 3. Read PR state

Return only facts the caller needs: number, URL, author, head SHA, base,
created/updated time, draft status, mergeable state, branch protection or
permission constraints, whether a review can be published, per-check status, and
existing reviews/comments. Keep tooling details internal.

### 4. Read reviewable scope

When asked, return changed files, patch text, and any locally readable commits
from head since base. Do not perform judgment here; the goal is to give the
reviewing skill precise facts.

### 5. Publish constrained review

When asked, publish only `REQUEST_CHANGES` or `COMMENT`. Never approve. Always
publish when the caller passes `blocker=True` and the GitHub capability allows
it. For non-blockers, publish only when permitted.

### 6. Handle fallbacks cleanly

When GitHub access is missing or publishing fails, return enough structured data
for the caller to complete a local review and stop with the specific failure.

### 7. Return a structured result

Report at least:

- `status`: `selected`, `none`, `multiple`, `missing_access`, `publish_failed`
- `can_publish`: `true` / `false`
- `pr`: URL, number, head/base, checks summary, mergeability, review state
- `facts`: files, diffs, existing comments
- `publish_result`: review ID, state, and success/failure when used.
