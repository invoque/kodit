---
name: github-pr
description: >-
  Use when any caller needs a GitHub pull request opened — given a repository,
  remote, head branch, base branch, title, and body. Validates authentication
  and branches, reuses an existing open PR instead of duplicating it, pushes the
  head branch when needed, and creates a ready-for-review PR via GitHub MCP or
  the gh CLI. Fails clearly when no GitHub capability is available.
---

# github-pr

Open a GitHub pull request for a head branch into a base branch.

## Usage

Invoked with a repository path, remote name, head branch, base branch, title,
and rendered body. Read `references/pr-template.md` for the title/body shape
before creating. Returns created or existing status, the PR URL, and the
head/base pair. Never merges.

## What You Must Do When Invoked

### 1. Validate prerequisites

Confirm the path is a git repository with the remote configured and the head
branch present locally or on the remote. Confirm a GitHub capability exists: a
GitHub MCP pull-request-create tool or an authenticated `gh` CLI. Plain `git`
can push but cannot open a GitHub PR. Stop with the missing piece named when
authentication, the remote, the head branch, or both GitHub capabilities are
absent; never invent a URL.

### 2. Reuse an existing PR

Before creating, check for an open PR from head into base (MCP equivalent or
`gh pr list --head <head> --base <base> --state open`). When one exists, return
it as `existing` with its URL and stop; never open a duplicate.

### 3. Push the head branch

When the head's commits are not on the remote, push only the head branch
(`git push <remote> <head>`). Never push the base branch or force-push a
protected branch.

### 4. Create the PR

Build the title and body per `references/pr-template.md`, writing the body to a
temporary file when the CLI needs `--body-file`. Prefer the GitHub MCP create
tool when available; otherwise run non-interactively, e.g.
`gh pr create --base <base> --head <head> --title <title> --body-file <file>`.
Create a ready-for-review PR by default (no draft flag unless the caller asked
for a draft).

### 5. Return the result

Report exactly: `created` or `existing`, the PR URL, head, base, and title. On
failure report which step failed and the next fix (authenticate, add a remote,
push the branch, or retry).
