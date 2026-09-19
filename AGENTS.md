# AGENTS.md

Instructions for coding agents working in `kodit`. This file wins over any
other instruction for work in this repository.

## Project Overview

`kodit` is an opinionated, milestone-driven development workflow for solo
developers, delivered as agent-agnostic skills. This repository is
markdown-first: no build step, no runtime code, no package manifest.

The layout below applies to `kodit` itself and to any project that adopts it.
Items marked *(setup)* are created by the `setup` phase in the adopting project.

```
kodit/
├── AGENTS.md            # this file — agent instructions
├── README.md            # human-facing overview
├── CONTEXT.md           # project context, decisions, environment
├── kodit.json           # project configuration (setup)
├── .kodit/
│   └── tmp/             # temporary working artifacts (setup, gitignored)
│       └── workspaces/  # throwaway workspaces for testing (created on demand)
├── specs/               # per-item workflow artifacts (created on first use)
│   ├── spec-NNN-*.md    # specifications
│   └── plan-NNN-*.md    # implementation plans (tasks embedded)
└── skills/
    ├── workflow/        # one skill per workflow phase (orchestrators)
    │   └── <skill-name>/
    │       ├── SKILL.md
    │       ├── references/
    │       └── scripts/
    └── general/         # single-purpose capability skills
        └── <skill-name>/
            ├── SKILL.md
            ├── references/
            └── scripts/
```

## Working Contract

1. Read `CONTEXT.md` first — it is the source of truth.
2. Read `kodit.json` when it exists — it holds project configuration.
3. Follow the workflow phases below, in order. Do not skip phases.
4. Never implement a milestone item without an approved spec and plan.
5. Record significant decisions in the `CONTEXT.md` decisions log in the same
   change.

### Workflow Phases

Each phase is one workflow skill in `skills/workflow/`. The skill owns that
phase's detailed steps, artifacts, and exit conditions; this table is the
overview only.

| Phase | Purpose | Entry criteria | Exit criteria |
|---|---|---|---|
| **setup** | Initialize a project for `kodit` | Project has not adopted `kodit` | `kodit.json` and `.kodit/tmp/` exist and configuration is validated |
| **milestone-planning** | Agree the scope of the next milestone | Setup complete; a milestone worth of work exists | Milestone scope agreed and recorded |
| **implement-loop** | Work each milestone item to completion | Approved milestone scope | Every milestone item implemented |
| **review-loop** | Verify each implemented item | Completed `implement-loop` | Every milestone item reviewed; deltas recorded |
| **milestone-review** | Confirm the milestone achieved its goal | Completed `review-loop` | Milestone goal verified and retrospective captured |
| **done** | Finalize the milestone | Passing `milestone-review` | Milestone artifacts, docs, and changelog agree; work committed |

The six phases form an outer milestone loop —
`setup → milestone-planning → implement-loop → review-loop → milestone-review → done`.
Inside `implement-loop` and `review-loop`, each milestone item runs an inner loop:

| Inner step | Purpose | Artifact |
|---|---|---|
| **spec** | Capture the item's requirements | `specs/spec-NNN-<name>.md` |
| **plan** | Turn the spec into an ordered approach | `specs/plan-NNN-<name>.md` (tasks embedded) |
| **implement** | Execute the plan exactly | Code / skill files |
| **review** | Verify against the spec | Review notes in the plan |

Artifact naming: `spec-NNN-short-name.md` and `plan-NNN-short-name.md`, where
`NNN` is a zero-padded sequential number (e.g. `spec-001-skill-format.md`).

## Runtime Layout

Two paths are created by `setup` in every adopting project.

### `kodit.json`

Project configuration at the repository root, alongside any other project
manifest. It is committed and written by the `setup` phase. Its exact schema is
owned by the `setup` workflow skill and its general skills.

### `.kodit/tmp/`

Temporary working artifacts, always markdown:

- One file per task, named in lowercase kebab-case (e.g.
  `milestone-003-interview-notes.md`).
- Never load-bearing. Anything still needed after its phase ends must be
  promoted into a permanent artifact (typically under `specs/`); the rest is
  discarded.
- Swept clean at phase boundaries.
- Always gitignored. `.kodit/tmp` is never committed.
- The one exception to "always markdown": when an agent needs a workspace
  directory for testing (e.g. to exercise skill setup or workflow phases),
  always use `.kodit/tmp/workspaces/`. Never create test workspaces elsewhere
  in the repository.

## Canonical Skill Format

Every skill lives in `skills/<category>/<skill-name>/SKILL.md`, where
`<category>` is `workflow` or `general`. The format is agent-agnostic and must
not encode assumptions about a specific agent.

### Skill Categories

| Category | Role | Depends on |
|---|---|---|
| `workflow` | One skill per workflow phase. Sequences the phase, enforces its entry and exit criteria, and invokes general skills as needed. | `general` |
| `general` | A single, reusable capability with no phase knowledge — for example interviewing the user, setting up `kodit`, or interacting with an issue tracker. | Nothing |

Rules:

- Dependency direction is one-way: workflow skills may reference general
  skills, never the reverse.
- Workflow skills invoke a general skill by relative path, e.g. "follow
  `skills/general/<skill-name>/SKILL.md`".
- One responsibility per skill. If two skills overlap, merge or resplit them so
  their responsibilities are disjoint.
- Skill names are globally unique across both categories, because agents may
  flatten the directory tree when installing.
- New categories require a decision recorded in `CONTEXT.md`.

Use exactly two frontmatter fields — no more:

```yaml
---
name: <skill-name>
description: <one paragraph; state what the skill does and when to use it>
---
```

- `name` must match the immediate containing directory name, in lowercase
  kebab-case.
- `description` must include trigger guidance (e.g. "Use when ...") because
  agents select skills by description alone.

Body structure:

```markdown
# <Skill Title>

<One-line purpose.>

## Usage

<How the skill is invoked and what inputs it expects.>

## What You Must Do When Invoked

1. <Step>
2. <Step>
```

- Keep `SKILL.md` focused; move long reference material into `references/`.
- Move executable helpers into `scripts/` and reference them by relative path.
- Write procedures as discrete, ordered steps; prefer explicit commands over
  vague instruction.

## Do

- Keep every skill agent-agnostic, self-contained, and deterministic.
- State trigger conditions in each skill `description`.
- Validate that skill frontmatter parses as YAML before committing (see README,
  Contributing).
- Match the naming and layout conventions in this file and `CONTEXT.md`.
- Record significant decisions in the `CONTEXT.md` decisions log.
- Use conventional commit messages (`feat:`, `fix:`, `docs:`, `chore:`).
- Commit every completed task on its `feature/*` branch before moving on;
  never leave finished work uncommitted.

## Don't

- Do not put vendor-specific instructions inside a skill (no "only for Claude",
  no "only for pi", no agent-specific tool names).
- Do not add runtime code, dependencies, or a package manifest without a prior
  decision recorded in `CONTEXT.md`.
- Do not let two skills overlap in responsibility.
- Do not let a general skill depend on a workflow skill or a workflow phase.
- Do not make `.kodit/tmp/` load-bearing, and do not commit `.kodit/`.
- Do not modify an approved spec or plan during implementation; amend it in a
  new spec or append a dated changelog entry.
- Do not create files outside the documented layout.
- Do not create test workspaces outside `.kodit/tmp/workspaces/`.
- Do not commit secrets, tokens, or machine-specific absolute paths.
- Do not commit unless the change is complete and verified for its phase.
- Do not commit directly to `master` or `dev`, and do not force-push either.

### Branching

`master` and `dev` are **protected branches**. Never commit to them directly.

| Branch | Role |
|---|---|
| `master` | Stable, released state. Only updated by merging `dev`. |
| `dev` | Integration branch. Only updated by merging `feature/*`. |
| `feature/*` | All work happens here. Branch from `dev`, merge back into `dev`. |

Workflow for every change:

1. Branch from the latest `dev`: `git switch dev && git pull && git switch -c feature/<short-name>`.
2. Do all work — specs, plans, skills, docs — on the `feature/*` branch.
3. Merge the feature branch into `dev` once review passes.
4. Merge `dev` into `master` only for a release.

Name branches `feature/<short-name>` in lowercase kebab-case, e.g.
`feature/spec-skill`. Never force-push a protected branch.
