---
name: git-branching
description: >-
  Use when defining or checking a project's git branch model under kodit — which
  branches are stable and integrating, how feature and bugfix branches are
  named, whether a staging branch exists, and whether a remote is configured.
  Invoked by the setup-kodit workflow skill to settle branching. Detects git
  state, interviews for the model with recommendations, offers to create a
  missing dev branch or add a remote, and writes the branching draft. Never
  forces repository changes.
---

# git-branching

Settles the branch model and records it for `kodit.json` and the generated docs.

## Usage

Invoked by `setup-kodit` during the setup phase. Read
`references/strategies.md` for the model options and defaults. Follow
the `interview` skill for the branching decisions. Output:
`.kodit/tmp/setup-git-branching.md`, plus any branch or remote changes the user
approves.

## What You Must Do When Invoked

### 1. Detect the current state

Report facts, not questions: whether this is a git repository; the existing
branches and which is default; configured remotes; and whether the working tree
is clean. Never ask for what `git` can tell you.

### 2. If there is no repository

Ask whether to run `git init` or continue without version control. If the user
declines, record `git: null`, skip the rest, and write the draft noting the
skip. Do not run `git init` without approval.

### 3. Settle the model with interview

Follow the `interview` skill with topic "git branching model" and
the field list from `references/strategies.md` as context: main branch, dev
branch, feature prefix, bugfix prefix, optional staging branch, optional remote.
Recommend the defaults and adapt them to the branches already present.

### 4. Validate before offering changes

Check the chosen names against the detected state: a chosen main branch that
does not exist, a feature prefix that collides with an existing branch, or a dev
branch missing. Surface every conflict and let the user resolve it — do not
silently rename.

### 5. Offer, never force

If the dev branch is missing, offer to create it. If no remote is configured and
the user wants one, ask for the name and URL and offer to add it. Perform only
what the user approves; report the exact commands you ran.

### 6. Write the draft

Write `.kodit/tmp/setup-git-branching.md` in the shape given in
`references/strategies.md`, recording the final model and any actions taken.
