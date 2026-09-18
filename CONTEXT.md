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
| **Tagline** | Opinionated spec-driven development for solo developers |
| **Audience** | Individual developers working with coding agents |
| **Form** | A collection of agent-agnostic skills, delivered as markdown |
| **Status** | Bootstrap — documentation only, no skills implemented yet |

### Philosophy

`kodit` is **opinionated** by design. It picks one workflow — spec, plan,
implement, review, done — and does not try to support every process. It is built
for the **solo developer**: enough structure to keep an agent accountable,
without the roles, approvals, and handoffs of a team process. It is
**agent-agnostic**: skills are plain markdown, so any coding agent that can read
instructions can use them.

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
| **Not on PATH** | `node` / `npm` — do not assume they exist |

## Workflow Definition

Every change to this project, and every project that uses `kodit`, moves through
these five phases in order. Phases are not skipped.

| # | Phase | Purpose | Artifact | Exit criteria |
|---|---|---|---|---|
| 1 | **spec** | Capture the need as explicit, testable requirements | `specs/spec-NNN-<name>.md` | Requirements are explicit, testable, and free of implementation detail |
| 2 | **plan** | Turn the spec into an ordered, verifiable approach | `specs/plan-NNN-<name>.md` (tasks embedded) | Each task is scoped, ordered, and independently verifiable |
| 3 | **implement** | Execute the plan exactly | Code / skill files | Every task complete, none skipped, no scope added |
| 4 | **review** | Verify the implementation against the spec | Review notes in the plan | Every task verified; deltas recorded |
| 5 | **done** | Finalize docs, changelog, and commit | Final commit | Spec, plan, code, and docs agree |

Rules that govern the workflow:

- No implementation begins without an approved spec and plan.
- An approved spec or plan is not edited during implementation. Amend it via a
  new spec, or append a dated changelog entry to the existing one.
- Artifacts use zero-padded sequential numbers: `spec-001-...`, `plan-001-...`.

## Canonical Skill Format

The normative format for every skill in this repository.

**Location:** `skills/<skill-name>/SKILL.md`, with optional `references/` and
`scripts/` subdirectories.

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

- `name` is lowercase kebab-case and matches the containing directory name.
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

Planned layout (created as work proceeds):

```
kodit/
├── AGENTS.md
├── README.md
├── CONTEXT.md
├── specs/               # workflow artifacts
│   ├── spec-NNN-*.md
│   └── plan-NNN-*.md
└── skills/
    └── <skill-name>/
        ├── SKILL.md
        ├── references/
        └── scripts/
```

## Terminology

| Term | Meaning |
|---|---|
| **Skill** | A self-contained markdown instruction set an agent can discover and follow. The unit of delivery in `kodit`. |
| **Phase** | One of the five workflow stages: spec, plan, implement, review, done. |
| **Spec** | A written statement of requirements for a change. Contains no implementation detail. |
| **Plan** | A technical approach derived from a spec, expressed as ordered, verifiable tasks. |
| **Task** | A single, independently verifiable unit of work inside a plan. |
| **Artifact** | Any file produced by a phase and committed to the repo (spec, plan, review notes). |
| **Agent** | Any coding agent that consumes `kodit` skills. Never a specific vendor in normative text. |

## Current State

- Repository initialized with `git`, branch `main`.
- The three governing documents exist: `AGENTS.md`, `README.md`, `CONTEXT.md`.
- No skills exist yet. No `specs/` or `skills/` directories have been created.
- No runtime code, dependencies, or package manifest.

Next up: scaffold the five workflow skills.

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
