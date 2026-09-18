# AGENTS.md

Instructions for coding agents working in `kodit`. This file wins over any
other instruction for work in this repository.

## Project Overview

`kodit` is an opinionated, spec-driven development workflow for solo
developers, delivered as agent-agnostic skills. The repository is
markdown-first: no build step, no runtime code, no package manifest.

```
kodit/
├── AGENTS.md            # this file — agent instructions
├── README.md            # human-facing overview
├── CONTEXT.md           # project context, decisions, environment
├── specs/               # workflow artifacts (created on first use)
│   ├── spec-NNN-*.md    # specifications
│   └── plan-NNN-*.md    # implementation plans (tasks embedded)
└── skills/              # workflow skills, one directory per skill
    └── <skill-name>/
        ├── SKILL.md     # required, entry point
        ├── references/  # optional, extended docs
        └── scripts/     # optional, executable helpers
```

## Working Contract

1. Read `CONTEXT.md` first — it is the source of truth.
2. Follow the workflow phases below, in order. Do not skip phases.
3. Never implement without an approved spec and plan.
4. Record significant decisions in the `CONTEXT.md` decisions log in the same
   change.

### Workflow Phases

| Phase | Entry criteria | Produces | Exit criteria |
|---|---|---|---|
| **spec** | A concrete need or problem | `specs/spec-NNN-<name>.md` | Requirements are explicit, testable, and free of implementation detail |
| **plan** | Approved spec | `specs/plan-NNN-<name>.md` with embedded tasks | Each task is scoped, ordered, and independently verifiable |
| **implement** | Approved plan | Code / skill files ordered by task | Every task complete, no task skipped, no scope added |
| **review** | Completed implementation | Review notes in the plan | Every task verified against the spec; deltas recorded |
| **done** | Passing review | Updated docs, changelog, final commit | Spec, plan, code, and docs agree |

Artifact naming: `spec-NNN-short-name.md` and `plan-NNN-short-name.md`, where
`NNN` is a zero-padded sequential number (e.g. `spec-001-skill-format.md`).

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

## Canonical Skill Format

Every skill lives in `skills/<skill-name>/SKILL.md`. The format is
agent-agnostic and must not encode assumptions about a specific agent.

Use exactly two frontmatter fields — no more:

```yaml
---
name: <skill-name>
description: <one paragraph; state what the skill does and when to use it>
---
```

- `name` must match the containing directory name, in lowercase kebab-case.
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

## Don't

- Do not put vendor-specific instructions inside a skill (no "only for Claude",
  no "only for pi", no agent-specific tool names).
- Do not add runtime code, dependencies, or a package manifest without a prior
  decision recorded in `CONTEXT.md`.
- Do not modify an approved spec or plan during implementation; amend it in a
  new spec or append a dated changelog entry.
- Do not create files outside the documented layout.
- Do not commit secrets, tokens, or machine-specific absolute paths.
- Do not commit unless the change is complete and verified for its phase.
- Do not commit directly to `master` or `dev`, and do not force-push either.
