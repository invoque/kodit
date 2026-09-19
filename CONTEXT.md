# CONTEXT.md

Living context for the `kodit` project. This is the source of truth for project
identity, environment, terminology, and decisions.

**Agents: read this file before making changes, and keep it current. When you
make a significant decision, add an entry to the decisions log at the bottom in
the same change.**

## Identity

| Field | Value |
|---|---|
| **Name** | `kodit` |
| **Tagline** | Opinionated milestone-driven development for solo developers |
| **Audience** | Individual developers working with coding agents |
| **Form** | A collection of agent-agnostic skills, delivered as markdown |
| **Status** | First general skill implemented (`interview`); workflow skills pending |

### Philosophy

`kodit` is **opinionated** by design. It picks one workflow — setup,
milestone-planning, implement-loop, review-loop, milestone-review, done — and does not
try to support every process. It is built for the **solo developer**: enough
structure to keep an agent accountable, without the roles, approvals, and
handoffs of a team process. It is **agent-agnostic**: skills are plain markdown,
so any coding agent that can read instructions can use them.

## Background & Environment

`kodit` lives in the `agent-harness` workspace alongside sibling projects such
as `pi-extensions`. The skill format is deliberately inherited from conventions
already proven on this machine (see the `graphify` and `linear-cli` skills),
rather than invented from scratch.

Environment facts relevant to working here:

| Item | Value |
|---|---|
| **Repository** | `kodit` (markdown-first, no build step) |
| **Skill sources of truth** | Defined in this repo under `skills/`, installed into an agent's skills directory |
| **Skill directories in use on this machine** | `~/.claude/skills/` (Claude Code), `~/.agents/skills/` (agent-agnostic / pi) |
| **Documented tooling** | `python3` (3.14) and `uv` for frontmatter validation; `bun` available |
| **Agent CLI in use** | `opencode`, exclusively — `claude` is not used on this machine |
| **Not on PATH** | `node` / `npm` — do not assume they exist |

## Workflow Definition

Every project that uses `kodit` moves through six phases, always in order,
forming a milestone loop. Phases are not skipped.

| # | Phase | Purpose | Exit criteria |
|---|---|---|---|
| 1 | **setup** | Initialize `kodit` in the project | `kodit.json` and `.kodit/tmp/` exist and configuration is validated |
| 2 | **milestone-planning** | Agree the scope of the next milestone | Milestone scope agreed and recorded |
| 3 | **implement-loop** | Work each milestone item to completion | Every milestone item implemented |
| 4 | **review-loop** | Verify each implemented item | Every milestone item reviewed; deltas recorded |
| 5 | **milestone-review** | Confirm the milestone achieved its goal | Milestone goal verified and retrospective captured |
| 6 | **done** | Finalize the milestone | Milestone artifacts, docs, and changelog agree; work committed |

### Inner item loop

Inside `implement-loop` and `review-loop`, each milestone item runs the same inner
loop. This is where the spec-driven discipline lives.

| # | Step | Purpose | Artifact |
|---|---|---|---|
| 1 | **spec** | Capture the item's requirements | `specs/spec-NNN-<name>.md` |
| 2 | **plan** | Turn the spec into an ordered approach | `specs/plan-NNN-<name>.md` (tasks embedded) |
| 3 | **implement** | Execute the plan exactly | Code / skill files |
| 4 | **review** | Verify against the spec | Review notes in the plan |

Rules that govern the workflow:

- No milestone item is implemented without an approved spec and plan.
- An approved spec or plan is not edited during implementation. Amend it via a
  new spec, or append a dated changelog entry to the existing one.
- Artifacts use zero-padded sequential numbers: `spec-001-...`, `plan-001-...`.
- Each phase's detailed steps, artifacts, and exit conditions are owned by that
  phase's workflow skill, not by this document.

## Runtime Layout

Paths that `setup` creates in every adopting project.

| Path | Committed | Purpose |
|---|---|---|
| `kodit.json` | Yes | Project configuration at the repository root. Schema owned by the `setup` skill. |
| `.kodit/tmp/` | No (gitignored) | Temporary working artifacts, always markdown. Never load-bearing; promoted into a permanent artifact or discarded, and swept at phase boundaries. |
| `.kodit/tmp/workspaces/` | No (gitignored) | Throwaway workspaces agents create for testing. Always used for test workspaces; ephemeral and swept with `.kodit/tmp/`. |

The `kodit` repository itself stays markdown-first; `kodit.json` is the
configuration that `kodit` writes into the projects that adopt it.

## Canonical Skill Format

The normative format for every skill in this repository.

**Location:** `skills/<category>/<skill-name>/SKILL.md`, with optional
`references/` and `scripts/` subdirectories. `<category>` is `workflow` or
`general`.

### Skill Categories

| Category | Role | Depends on |
|---|---|---|
| `workflow` | One skill per workflow phase. Sequences the phase, enforces its entry and exit criteria, and invokes general skills as needed. | `general` |
| `general` | A single, reusable capability with no phase knowledge — for example interviewing the user, setting up `kodit`, or interacting with an issue tracker. | Nothing |

Rules:

- Dependency direction is one-way: workflow skills may reference general
  skills, never the reverse.
- Workflow skills invoke a general skill by relative path.
- One responsibility per skill; overlapping skills are merged or resplit.
- Skill names are globally unique across both categories.
- New categories require a decision recorded in the decisions log.

**Frontmatter — exactly two fields:**

```yaml
---
name: <skill-name>
description: <what the skill does and when to use it>
---
```

**Body structure:**

```markdown
# <Skill Title>

<One-line purpose.>

## Usage

<Invocation and expected inputs.>

## What You Must Do When Invoked

1. <Step>
2. <Step>
```

Requirements:

- `name` is lowercase kebab-case and matches the immediate containing directory
  name.
- `description` states trigger guidance, because agents select skills by
  description alone.
- Instructions are discrete, ordered, and deterministic.
- No vendor-specific instructions anywhere in a skill.

## Directory Conventions

Current layout:

```
kodit/
├── AGENTS.md
├── README.md
└── CONTEXT.md
```

Planned layout (created as work proceeds; *(setup)* marks what the `setup` phase
creates in an adopting project):

```
kodit/
├── AGENTS.md
├── README.md
├── CONTEXT.md
├── kodit.json            # project configuration (setup)
├── .kodit/
│   └── tmp/              # temporary working artifacts (setup, gitignored)
├── specs/               # per-item workflow artifacts
│   ├── spec-NNN-*.md
│   └── plan-NNN-*.md
└── skills/
    ├── workflow/
    │   └── <skill-name>/
    │       ├── SKILL.md
    │       ├── references/
    │       └── scripts/
    └── general/
        └── <skill-name>/
            ├── SKILL.md
            ├── references/
            └── scripts/
```

## Terminology

| Term | Meaning |
|---|---|
| **Skill** | A self-contained markdown instruction set an agent can discover and follow. The unit of delivery in `kodit`. |
| **Workflow skill** | A skill in `skills/workflow/` that owns exactly one workflow phase. Orchestrates, and invokes general skills. |
| **General skill** | A reusable, single-purpose capability in `skills/general/` with no phase knowledge. |
| **Phase** | One of the six milestone workflow stages: setup, milestone-planning, implement-loop, review-loop, milestone-review, done. |
| **Milestone** | A batch of work planned, implemented, and reviewed as one unit before finalization. |
| **Spec** | A written statement of requirements for a milestone item. Contains no implementation detail. |
| **Plan** | A technical approach derived from a spec, expressed as ordered, verifiable tasks. |
| **Task** | A single, independently verifiable unit of work inside a plan. |
| **Artifact** | Any file produced by a phase. Permanent artifacts live under `specs/` and are committed; temporary artifacts live in `.kodit/tmp/` and are not. |
| **Temporary artifact** | A markdown scratch file in `.kodit/tmp/`. Never load-bearing; promoted or discarded. |
| **Configuration** | `kodit.json`, at the repository root, written by `setup`. |
| **Agent** | Any coding agent that consumes `kodit` skills. Never a specific vendor in normative text. |

## Current State

- Repository initialized with `git`; `master` is stable, `dev` is integration.
- The three governing documents exist: `AGENTS.md`, `README.md`, `CONTEXT.md`.
- The first skill exists: `skills/general/interview/SKILL.md`, specified and
  planned by `specs/spec-001-interview-skill.md` and
  `specs/plan-001-interview-skill.md`; merged to `dev`.
- Skills carry a mandatory conciseness standard (`AGENTS.md`), established by
  `specs/spec-002-terse-skills.md` and `specs/plan-002-terse-skills.md`.
- `.kodit/tmp/` is in use for temporary artifacts (gitignored). No `kodit.json`
  exists yet, and there is still no runtime code, dependencies, or package
  manifest.

Next up: scaffold the six workflow skills.

## Decisions Log

| Date | Decision | Rationale |
|---|---|---|
| 2026-09-19 | Adopt a five-phase workflow: spec → plan → implement → review → done. | Balanced structure for a solo developer: enough accountability for agent work without team-sized ceremony. Leaner 3-phase and heavier 7-phase variants were rejected. |
| 2026-09-19 | Install skills manually via copy or symlink; no installer yet. | The project is markdown-only and file-based; a script or CLI would add runtime surface before the workflow itself exists. Symlinks are recommended during early development. |
| 2026-09-19 | Bootstrap as a git repository with an initial commit of the three docs. | Establishes history and a clean starting point; every later change follows the spec-driven workflow on top of it. |
| 2026-09-19 | Canonical skill frontmatter is exactly `name` and `description`. | Matches the proven conventions of `graphify` and `linear-cli` and keeps skills portable across agents. Extra metadata fields were rejected to avoid coupling skills to tooling. |
| 2026-09-19 | Keep the repository markdown-first with no runtime code. | Any code (e.g. a future installer) requires a prior decision recorded here. |
| 2026-09-19 | Protect `master` and `dev`; all work happens on `feature/*` branches. | `master` holds released state, `dev` is the integration branch, and feature branches keep unreviewed work off both. Prevents direct commits and force-pushes to protected branches. |
| 2026-09-19 | Compress `AGENTS.md` and `README.md` for conciseness. | `AGENTS.md` is now terse and rule-focused; `README.md` is human-readable. The YAML frontmatter validation command is canonical in `README.md` Contributing, and `AGENTS.md`'s Setup & Verification section was removed as redundant with README Getting Started. |
| 2026-09-19 | Supersede the five-phase workflow with a six-phase milestone workflow: setup → milestone-planning → implement-loop → review-loop → milestone-review → done. | Milestone framing matches how a solo developer batches work, and maps cleanly onto an issue tracker. The per-item spec → plan → implement → review discipline is retained as the inner loop inside `implement-loop` and `review-loop`, so `kodit` stays spec-driven. |
| 2026-09-19 | Project configuration is `kodit.json` at the repository root. | A root-level JSON file is a familiar convention (alongside `package.json` and friends) and is machine-readable for agents. It lives outside `.kodit/`, which holds only temporary state. |
| 2026-09-19 | Temporary working artifacts are markdown files in `.kodit/tmp/`, and `.kodit/` is gitignored. | Gives the workflow scratch space for interviews and drafts without polluting the committed tree. Nothing in `tmp/` is load-bearing: it is promoted into a permanent artifact or discarded. |
| 2026-09-19 | Split skills into two categories: `skills/workflow/` (one orchestrator per phase) and `skills/general/` (single-purpose capabilities). | A one-way dependency (workflow → general) with one responsibility per skill keeps skills composable and non-overlapping, and makes them installable independently. New categories require a recorded decision. |
| 2026-09-19 | Defer defining the specific skills and each phase's artifacts to the skills themselves. | The overview documents describe structure and rules; inventing an inventory before the skills exist would be speculative design. Each phase's artifacts are owned by its workflow skill. |
| 2026-09-19 | Agents needing a workspace directory for testing always use `.kodit/tmp/workspaces/`. | Keeps test workspaces inside the gitignored temporary area so they can never pollute the committed tree, and gives every agent one predictable, collocated location. Test workspaces are ephemeral and swept with `.kodit/tmp/`. |
| 2026-09-19 | Commit every completed task immediately; never leave finished work uncommitted. | Keeps the working tree reflecting real progress and prevents losing completed work. Complements the existing rule that incomplete or unverified changes must not be committed. |
| 2026-09-19 | The first skill is `interview`, a general skill implementing the design-tree interview method, with its working artifact at `.kodit/tmp/design-tree-<topic>.md`. | All three governing documents name interviewing as the prototypical general skill, and it is the prerequisite for spec-driven work: it produces the shared understanding every milestone item starts from. The method — a tree of decisions advanced one round of frontier questions at a time, with facts found by the agent and decisions owned by the user — was chosen over free-form questioning because it is deterministic, terminates when the frontier is empty, and leaves nothing silently assumed. |
| 2026-09-19 | `opencode` is the agent CLI used on this machine; skills and tooling must not assume `claude`. | The machine's harness is `opencode`. Vendor-specific instructions are already forbidden in skills, and this extends to the development tooling: the skill-creator description-optimization scripts, which shell out to `claude`, are adapted to `opencode` when used. |
| 2026-09-19 | Every skill must be clean, concise, and terse: `SKILL.md` body under 100 lines, `description` at most ~80 words, each idea stated once. | Skills are read under token pressure, so every line spends context the agent needs for the work. The measurable caps force detail into `references/` and prevent the six planned workflow skills from inheriting the first skill's verbosity. Enforced by `AGENTS.md` and checked at spec/plan review; no tooling was added, keeping the repository markdown-first. |
