---
name: issue-tracker
description: >-
  Use when setting up or interacting with a project's issue tracker under kodit
  — choosing a backend, seeding a file-based tracker, or creating, updating, and
  querying milestones, user stories, and tasks. Invoked by the setup-kodit
  workflow skill to configure tracking. File-based is fully supported; GitHub
  Issues and Linear are selectable but deferred. Owns the file-based
  conventions: the issues tree, story and task formats, labels, and the status
  machines.
---

# issue-tracker

Configures and operates the project's issue tracker.

## Usage

Invoked in two modes. Read `references/file-based.md` for the full conventions
before writing any issue artifact. Follow
the `interview` skill for the backend choice.

- **Setup mode** — choose a backend, check its requirements, seed the tracker,
  and write `.kodit/tmp/setup-issue-tracker.md`.
- **Operate mode** — create, update, move, or query issues using the tree,
  labels, and state machines.

## What You Must Do When Invoked

### Setup mode

1. Offer the backend choice with a recommendation: **file-based** (supported
   today), GitHub Issues, or Linear. If the user picks GitHub or Linear, explain
   that the backend is not yet supported, recommend file-based for now, and note
   that `issue_tracker.type` makes switching later a config change. Do not
   pretend to configure an unsupported backend.
2. For file-based, confirm the labels from `kodit.json` — the five workflow
   labels are the default; ask whether to add any project-specific ones.
3. Create `.kodit/issues/` and write its two seed files from
   `references/file-based.md`: `README.md` (the conventions) and `INDEX.md` (the
   project charter, goal from the metadata draft).
4. Do **not** create milestones or stories — `milestone-planning` does that.
5. Write `.kodit/tmp/setup-issue-tracker.md` recording the backend, path,
   labels, and the seed files written.

### Operate mode

1. Read the story or charter file before changing it; never rewrite unrelated
   content.
2. Move a task only along an allowed transition, or a story/milestone as its
   children require; the machines are in `references/file-based.md`.
3. Keep IDs stable and unique: never renumber, never reuse a retired ID.
4. Query by reading `.kodit/issues/`, filtering on frontmatter `status`,
   `labels`, `type`, or `parent` as asked.
