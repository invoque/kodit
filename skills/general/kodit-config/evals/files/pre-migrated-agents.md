# AGENTS.md

Instructions for coding agents working in this project.

<!-- kodit:agents:v1:start -->

## kodit Workflow

This project uses `kodit`. Read `CONTEXT.md` first -- it is the source of truth.
Configuration is in `kodit.json`.

Phases, in order: setup -> milestone-planning -> implement -> review-loop ->
milestone-review -> done. Never implement an item without an approved spec and
plan. Inside `implement` and `review-loop`, each user story runs
spec -> plan -> implement -> review; each task runs the full status machine
below.

**Artifacts:** specs (`spec-US-NNN-*.md`) attach to user stories and plans
(`plan-T-NNN-*.md`) attach to tasks, both in `.kodit/tmp/specs/`. They are
local working artifacts, never committed.

**Issues:** file-based under `.kodit/issues/`. Taxonomy is
PROJECT -> MILESTONE -> USER STORY -> TASK, numbered `M-001`, `US-001`, `T-001`
globally. Tasks are rows inside the story file: tasks run
`open -> spec -> plan -> implement -> review -> done`, stories run
`open -> in-progress -> done`, milestones run `planned -> active -> closed`.
Labels are handoff signals: `ready-for-agent`, `ready-for-human`, `needs-info`,
`needs-triage`, `wontfix`, `blocked`. The full conventions live in
`.kodit/issues/README.md`.

**Branches:** `main` (stable), `develop` (integration), `feat/*`, `fix/*`. Work
on a feature branch, merge to `develop` after review; never commit directly to a
protected branch.

Record significant decisions in `CONTEXT.md` in the same change. Use
conventional commit messages.

<!-- kodit:agents:v1:end -->
