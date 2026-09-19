# File-based issue tracker conventions

This is the canonical reference for the file-based backend. `setup` seeds
`.kodit/issues/` with the tree and the two files below; `milestone-planning` and
later phases add milestones, stories, and tasks.

## Tree

```text
.kodit/issues/                      # committed, load-bearing
├── README.md                       # static conventions (a copy of this reference)
├── INDEX.md                        # project charter: goal + milestone index
└── M-001-goal-name/                # milestone directory
    ├── INDEX.md                    # milestone charter: goal, status, story index
    └── US-001-name.md              # user story with embedded tasks
```

Taxonomy: **PROJECT → MILESTONE → USER STORY → TASK**. Numbering is global and
never reused: `M-001`, `US-001`, `T-001` continue across the whole project, so a
name identifies exactly one artifact forever.

## Labels

Labels are handoff signals, not types. The default set:

| Label | Meaning |
|---|---|
| `ready-for-agent` | Fully specified; an agent can pick it up without further decisions. |
| `ready-for-human` | Needs a human action or decision before work continues. |
| `needs-info` | Missing information blocks progress; a specific question is outstanding. |
| `needs-triage` | Not yet classified or scoped. |
| `wontfix` | Deliberately not doing this. Terminal — closes the item from any status. |

Type (`feature`, `bug`, `chore`, `docs`, `refactor`) is a frontmatter field on
the story, not a label. Projects may add labels; keep the five defaults.

## Status machines

### Task (rows inside a story)

```text
open → spec → plan → implement → review → done
                 ↑                   |
                 └───────────────────┘   (rework: review → implement)
blocked  ⇄  any non-done state
wontfix  →  closes from any state
```

Full machine. Moves when its spec is approved (`spec`), its plan is approved
(`plan`), implementation starts (`implement`), the code is ready (`review`), and
verification passes (`done`). `blocked` records why in the row.

### User story

```text
open → in-progress → done
blocked ⇄ any non-done state
```

Coarse and derived: `in-progress` when any task leaves `open`, `done` when all
tasks are `done` or `wontfix`. A story does not return to `spec` when its third
task starts.

### Milestone

```text
planned → active → closed
```

Derived from its stories: `active` when any story is in progress, `closed` when
every story is `done` or `wontfix`.

## Story file format

Frontmatter plus body. Tasks are a table — tasks are **not** separate files.

```markdown
---
id: US-001
title: Reset password by email
type: feature
labels: [ready-for-agent]
status: open
parent: M-001
created: 2026-09-19
---

## Story
As a returning user I want to reset my password by email so that I can regain
access without support.

## Acceptance Criteria
- [ ] A reset link is emailed within one minute.
- [ ] The link expires after 24 hours.
- [ ] An unknown email does not reveal whether an account exists.

## Tasks
| ID | Description | Status |
|----|-------------|--------|
| T-001 | Add reset-token model and expiry | open |
| T-002 | Send reset email | open |
| T-003 | Reset form and confirmation page | open |
```

Frontmatter rules: `id`, `title`, `type`, `status`, `parent`, `created` are
required; `labels` is a list (may be empty). `type` is inherited by its tasks.

## Charters

`INDEX.md` exists at two levels.

**Project charter** (`.kodit/issues/INDEX.md`), seeded by `setup`:

```markdown
# Project — {{project.name}}

{{project.description}}

## Milestones

| ID | Goal | Status |
|----|------|--------|
| M-001 | <goal> | planned |
```

**Milestone charter** (`.kodit/issues/M-001-goal-name/INDEX.md`):

```markdown
# M-001 — <goal>

**Status:** planned
**Created:** 2026-09-19

## Goal
<what done looks like>

## Stories

| ID | Title | Status |
|----|-------|--------|
| US-001 | <title> | open |
```

When a story is added or changes status, update the milestone table; when a
milestone is added or changes status, update the project table. The tables are
the roadmap view — keep them in sync with the files.

## Conventions produced by `setup`

`setup` writes the project charter (`INDEX.md`) and this reference (as
`.kodit/issues/README.md`). It does not create milestone directories or stories.
`milestone-planning` creates `M-XXX-*` directories, their `INDEX.md`, and their
story files, allocating the next global `M`/`US` numbers.
