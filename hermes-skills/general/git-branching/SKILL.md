---
name: git-branching
description: >-
  Use when defining or checking a project's git branch model under kodit —
  which branches are stable and integrating, how feature and bugfix branches
  are named, whether a staging branch exists, and whether a remote is
  configured. Invoked by the setup-kodit workflow skill to settle branching,
  and directly for "set up our branch model", "what branches do we use",
  "define the branching strategy", or "is dev protected?". Detects git state,
  interviews for the model with recommendations, validates the names against
  the repository, offers to create a missing dev branch or add a remote, and
  writes the branching draft to `.kodit/tmp/setup-git-branching.md`. Never
  forces repository changes.
version: 1.0.0
author: invoque
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [kodit, git, branching, setup, workflow]
    related_skills: [interview, kodit-config]
---

# git-branching

Settles the branch model and records it for `kodit.json` and the generated
docs.

## When to Use

- Invoked by the setup-kodit workflow skill during the setup phase.
- The user asks directly: "set up our branch model", "what branches do we
  use", "define the branching strategy", "is dev protected?".
- Not for day-to-day branch work — creating a `feature/*` branch, merging, or
  resolving conflicts. This skill only settles and records the model.

## Usage

Inputs: access to the repository (and the user, for the model decisions).
Output: `.kodit/tmp/setup-git-branching.md`, plus any branch or remote changes
the user approves. Read `references/strategies.md` for the model options,
defaults, and the draft format before starting.

## Steps

### 1. Detect the current state

Report facts, not questions. Run read-only commands through `terminal`:
`git rev-parse --is-inside-work-tree`, `git branch`, `git remote -v`, and
`git status --porcelain`. Establish whether this is a git repository, the
existing branches and which is default, configured remotes, and whether the
working tree is clean. Never ask for what `git` can tell you.

### 2. If there is no repository

Ask whether to run `git init` or continue without version control. If the user
declines, record `git: null` in the draft, skip the remaining steps, and note
the skip. Do not run `git init` without approval.

### 3. Settle the model with interview

Follow the `interview` skill with topic "git branching model" and the field
list from `references/strategies.md` as context: main branch, dev branch,
feature prefix, bugfix prefix, optional staging branch, optional remote.
Recommend the defaults and adapt them to the branches already present. Use
`clarify` only for the single blocking question of whether to initialize a
repository (step 2); put the model decisions to the user through `interview`.

### 4. Validate before offering changes

Check the chosen names against the detected state: a chosen main branch that
does not exist, a feature prefix that collides with an existing branch, or a
missing dev branch. Surface every conflict and let the user resolve it — do
not silently rename.

### 5. Offer, never force

If the dev branch is missing, offer to create it. If no remote is configured
and the user wants one, ask for the name and URL and offer to add it. Run only
what the user approves through `terminal`, and report the exact commands you
ran.

### 6. Write the draft

Write `.kodit/tmp/setup-git-branching.md` with `write_file` in the shape given
in `references/strategies.md`, recording the final model and any actions
taken. Create the directory first with `terminal` (`mkdir -p .kodit/tmp`) if
it does not exist.

## Pitfalls

- **Asking for facts.** Branch names, the default branch, and remotes are
  readable with `git`; asking wastes the user's time.
- **Silent renames.** Renaming or deleting an existing branch to fit the model
  is never allowed; surface the conflict instead.
- **Forcing changes.** Creating a branch or adding a remote without explicit
  approval mutates the user's repository.
- **Skipping validation.** Offering changes before checking the chosen names
  against the detected state produces a model that cannot be applied.

## Verification

- `.kodit/tmp/setup-git-branching.md` exists and records the final model and
  every action taken.
- Every created branch or added remote was explicitly approved, and the exact
  commands run were reported.
- No existing branch was renamed or deleted; every name conflict was surfaced
  and resolved by the user.

## Reference files

| Topic | Read |
| --- | --- |
| Branching model fields, defaults, and the draft format | `references/strategies.md` |
