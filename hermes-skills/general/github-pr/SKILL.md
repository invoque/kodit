---
name: github-pr
description: >-
  Open a GitHub pull request for one head branch into a base branch — "open a
  PR", "create the PR for this branch", or a kodit pr-request handoff. Validates
  the repo, remote, branches, and `gh` authentication, reuses an existing open
  PR instead of duplicating it, pushes the head branch when needed, and creates
  a ready-for-review PR. Returns `created` or `existing` with the PR URL,
  head/base pair, and title. Never reviews, approves, or merges.
version: 1.0.0
author: invoque
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [github, pull-request, pr, review-request]
    related_skills: [gh-cli, code-review]
    requires_toolsets: [terminal]
---

# github-pr

Open a GitHub pull request for a head branch into a base branch.

## When to Use

- A caller needs a PR opened from a repository, remote, head branch, base
  branch, title, and rendered body.
- The user says "open a PR", "create the pull request for this branch", or a
  kodit `pr-request` flow hands off.
- Not for reviewing, approving, or merging a PR — use `code-review` to review,
  and read or publish PR state (approve, merge, comment) with `gh` directly.
- Not for generic local git work (`git commit`, `git rebase`) — use `git`.

## Usage

Inputs: repository path, remote name, head branch, base branch, title, and
rendered body. Read `references/pr-template.md` for the title and body shape
before creating. Output: `created` or `existing`, the PR URL, head, base, and
title. This skill never merges and never opens a draft unless asked.

Run every `gh` and `git` command through `terminal`. For install, authentication
(`GH_TOKEN` or `gh auth login`), and `gh` behavior details, follow the `gh-cli`
skill; load it with `skill_view` when available, otherwise run the commands
below directly.

## Steps

### 1. Validate prerequisites

Confirm the path is a git repository with the remote configured and the head
branch present locally or on the remote:

```
terminal(command="git remote -v")
terminal(command="git rev-parse --verify <head>")
terminal(command="gh auth status")
```

Plain `git` can push but cannot open a GitHub PR, so `gh` must be installed and
authenticated. Stop with the missing piece named when authentication, the
remote, the head branch, or `gh` itself is absent; never invent a PR URL.

### 2. Reuse an existing PR

Before creating, check for an open PR from head into base:

```
terminal(command="gh pr list --head <head> --base <base> --state open")
```

When one exists, return it as `existing` with its URL and stop; never open a
duplicate.

### 3. Push the head branch

When the head's commits are not on the remote, push only the head branch:

```
terminal(command="git push <remote> <head>")
```

Never push the base branch and never force-push a protected branch.

### 4. Create the PR

Read `references/pr-template.md` and build the title and body from the caller's
values. Write the body to a file with `write_file`, then use `--body-file`:

1. `write_file` a body file (for example `./pr-body.md`).
2. `terminal(command="gh pr create --base <base> --head <head> --title \"<title>\" --body-file ./pr-body.md")`

Pass `--title` and `--body-file` together so `gh` never prompts. Create a
ready-for-review PR by default; add `--draft` only when the caller asked for a
draft. If a remote backend cannot see the written file, recreate it with a
terminal heredoc.

### 5. Return the result

Report exactly: `created` or `existing`, the PR URL, head, base, and title. On
failure, report which step failed and the next fix (install or authenticate
`gh`, add a remote, push the branch, or retry).

## Pitfalls

- **Duplicate PRs.** Always run the step 2 check first; return the existing PR
  rather than opening a second one.
- **Pushing the wrong branch.** Push only the head branch, never the base, and
  never force-push a protected branch.
- **Interactive prompts hang the sandbox.** `gh pr create` needs `--title` plus
  `--body`/`--body-file`/`--fill` or it prompts and blocks.
- **Inline `--body` vs `--body-file`.** Markdown bodies passed inline suffer
  shell-escaping and literal `\n`; always write a file and pass `--body-file`.
- **Invisible file on remote backends.** A file written with `write_file` may
  not reach a remote sandbox; recreate it with a terminal heredoc if
  `--body-file` reports it missing.
- **`gh` reports the repo from the git remote.** In a directory without a
  `github.com` remote, or for another repository, pass `-R OWNER/REPO` or set
  `GH_REPO`.

## Verification

- `terminal(command="gh pr view <N> --json state,headRefName,baseRefName,title")`
  reflects the created PR's head, base, and title.
- A reused PR is returned as `existing` with its URL and no second PR is opened.
- The created PR is ready for review (not a draft) unless a draft was requested.
- No merge, approval, or review was performed.

## Reference files

| Topic | Read |
| --- | --- |
| PR title and body shape | `references/pr-template.md` |
