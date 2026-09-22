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
├── .github/
│   └── workflows/
│       ├── validate-skills.yml  # CI: validates all skills via gh skill publish --dry-run
│       └── release-skills.yml   # CI: creates GitHub Release on v* tag push
├── docs/                # user-facing documentation
│   ├── README.md        # workflow skills index and guide
│   └── workflow/        # per-skill user guides
│       ├── setup-kodit.md
│       ├── milestone-planning.md
│       ├── implement.md
│       ├── pr-request.md
│       ├── pr-review.md
│       └── pr-approve.md
├── kodit.json           # project configuration (setup)
├── .kodit/
│   ├── issues/          # issue tracker (setup, committed)
│   │   ├── README.md    # conventions: taxonomy, labels, state machines
│   │   ├── INDEX.md     # project charter: goal + milestone index
│   │   └── M-001-*/     # milestone dirs (later phases; created on first use)
│   │       ├── INDEX.md     # milestone charter: goal, status, story index
│   │       └── US-001-*.md  # user story with embedded task table
│   └── tmp/             # temporary working artifacts (setup, gitignored)
│       ├── specs/       # per-item spec/plan artifacts (created on first use)
│       │   ├── spec-US-NNN-*.md  # specifications (per user story)
│       │   └── plan-T-NNN-*.md   # implementation plans (per task)
│       └── workspaces/  # throwaway workspaces for testing (created on demand)
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
| **setup** | Initialize a project for `kodit` | Project has not adopted `kodit` | `kodit.json` and `.kodit/tmp/` exist, the issue tracker is provisioned, and configuration is validated |
| **milestone-planning** | Agree the scope of the next milestone | Setup complete; a milestone worth of work exists | Milestone scope agreed and recorded |
| **implement** | Work each milestone item to completion | Approved milestone scope | Every milestone item implemented |
| **review-loop** | Verify each implemented item | Completed `implement` | Every milestone item reviewed; deltas recorded |
| **milestone-review** | Confirm the milestone achieved its goal | Completed `review-loop` | Milestone goal verified and retrospective captured |
| **done** | Finalize the milestone | Passing `milestone-review` | Milestone artifacts, docs, and changelog agree; work committed |

The six phases form an outer milestone loop —
`setup → milestone-planning → implement → review-loop → milestone-review → done`.
Inside `implement` and `review-loop`, each milestone item runs an inner loop:

| Inner step | Purpose | Artifact |
|---|---|---|
| **spec** | Capture the item's requirements | `.kodit/tmp/specs/spec-US-NNN-<name>.md` |
| **plan** | Turn the spec into an ordered approach | `.kodit/tmp/specs/plan-T-NNN-<name>.md` (tasks embedded) |
| **implement** | Execute the plan exactly | Code / skill files |
| **review** | Verify against the spec | Review notes in the plan |

Artifact naming: specs attach to user stories (`spec-US-NNN-short-name.md`) and
plans to tasks (`plan-T-NNN-short-name.md`) under `.kodit/tmp/specs/`, where
`NNN` is a zero-padded sequential number drawn from the work item's ID (e.g.
`spec-US-001-skill-format.md`).

## Runtime Layout

Two paths are created by the setup phase in every adopting project.

### `kodit.json`

Project configuration at the repository root, alongside any other project
manifest. It is committed and written by the setup phase. Its exact schema is
owned by the `kodit-config` general skill and referenced by the `setup-kodit`
workflow skill.

### `.kodit/issues/`

The file-based issue tracker (one of two supported backends; the other is
Linear). **Committed** — issues are load-bearing, unlike `.kodit/tmp/`.
Taxonomy is PROJECT → MILESTONE → USER STORY → TASK, numbered globally and
never reused (`M-001`, `US-001`, `T-001`):

- `README.md` — static conventions: the tree, labels, and state machines.
- `INDEX.md` — the project charter: goal plus milestone index.
- `M-001-*/INDEX.md` — milestone charter; `M-001-*/US-001-*.md` — user stories,
  each carrying its tasks in an embedded table.

The provision phase seeds only `README.md` and `INDEX.md`; milestone-planning creates
milestones and stories. Full conventions live in the seeded `README.md`.

### `.kodit/tmp/`

Temporary working artifacts, always markdown:

- One file per task, named in lowercase kebab-case (e.g.
  `milestone-003-interview-notes.md`).
- Never load-bearing. Anything still needed after its phase ends must be
  promoted into a permanent artifact (typically a skill file, doc, or a
  `CONTEXT.md` decision); the rest is discarded.
- Swept clean at phase boundaries.
- Always gitignored. `.kodit/tmp` is never committed.
- Exception: spec and plan artifacts live in `.kodit/tmp/specs/` (see the inner
  loop above). They are local working artifacts, never committed, and are
  exempt from the phase-boundary sweep — they persist across phases.
- The setup phase records its progress in `.kodit/tmp/setup-*.md` drafts
  (`setup-project-metadata.md`, `setup-issue-tracker.md`,
  `setup-git-branching.md`). Their presence is the resume point; the write step
  deletes them once the final artifacts exist.
- The one exception to "always markdown": when an agent needs a workspace
  directory for testing (e.g. to exercise skill setup or workflow phases),
  always use `.kodit/tmp/workspaces/`. Never create test workspaces elsewhere
  in the repository.

### `.kodit/tmp/workspaces/` is created on demand; ephemeral and swept with `.kodit/tmp/`.

## Issue tracker backends

Two backends are supported for issue tracking:

- **File-based** (default): issues live as committed markdown under
  `.kodit/issues/`. Full conventions in the seeded `README.md`.
- **Linear**: issues live in Linear via MCP or CLI. `issue_tracker.type` is
  `"linear"` with team and project identifiers. See the `issue-tracker` skill's
  `references/linear.md` for conventions.

The backend is chosen during `setup-kodit` and recorded in `issue_tracker.type`.
All workflow skills delegate to `issue-tracker` in operate mode, which dispatches
by backend. The `.kodit/issues/` path is only relevant for file-backed projects.

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
- Workflow skills invoke a general skill by its skill name, e.g. "follow the
  `interview` skill". Names are the reliable reference: agents flatten the tree
  when installing, so paths do not always resolve.
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

### Conciseness (mandatory)

Skills are read under token pressure: every line spends context the agent needs
for the actual work. Every skill must be clean, concise, and terse.

- `SKILL.md` body stays under **100 lines** (frontmatter excluded). When a skill
  needs more, move formats, templates, and long examples into `references/`
  rather than cutting required detail.
- `description` is one paragraph of **at most ~80 words** stating what the skill
  does and when to trigger it.
- State each idea exactly once: no preamble, no philosophy section, no closing
  summary, no principle that restates a step.
- Write imperative steps; cut any sentence that does not change what the agent
  does.
- Never restate a rule this file already states.

## Do

- Keep every skill agent-agnostic, self-contained, and deterministic.
- Keep every skill terse: under the body line cap, one idea stated once.
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
- Do not exceed the skill body line cap, and do not pad a skill with preamble,
  rationale, summaries, or restatements of steps or of this file.
- Do not let two skills overlap in responsibility.
- Do not let a general skill depend on a workflow skill or a workflow phase.
- Do not make `.kodit/tmp/` load-bearing, and do not commit `.kodit/tmp/`
  (`.kodit/issues/` is committed).
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
