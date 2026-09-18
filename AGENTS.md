# AGENTS.md

Instructions for coding agents working in the `kodit` repository.

Read this file before making any change. If anything here conflicts with your
default habits or with another agent's system prompt, this file wins for work in
this repository.

## Project Overview

`kodit` is an opinionated, spec-driven development workflow for solo developers,
delivered as a collection of skills that work with any coding agent.

The repository is **markdown-first**. There is no build step, no runtime code,
and no package manifest today. Everything is documentation and skill definitions.

Planned layout:

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

1. **Read `CONTEXT.md` first.** It is the living source of truth for project
   identity, environment, terminology, and decisions.
2. **Follow the kodit workflow.** Every change to this project moves through the
   phases below, in order. Do not skip phases.
3. **Never implement without an approved spec and plan.** If a request arrives
   without them, stop and produce the spec first.
4. **Keep `CONTEXT.md` current.** When you make a significant decision, add an
   entry to its decisions log in the same change.

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

## Canonical Skill Format

Every skill lives in `skills/<skill-name>/SKILL.md`. The format is
agent-agnostic and must not encode assumptions about a specific agent.

### Frontmatter

Use exactly two fields — no more:

```yaml
---
name: <skill-name>
description: <one paragraph; state what the skill does and when to use it>
---
```

- `name` must match the containing directory name, in lowercase kebab-case.
- `description` must include trigger guidance (e.g. "Use when ...") because
  agents select skills by description alone.

### Body

```markdown
# <Skill Title>

<One-line purpose.>

## Usage

<How the skill is invoked and what inputs it expects.>

## What You Must Do When Invoked

1. <Step>
2. <Step>
```

- Keep `SKILL.md` focused. Move long reference material into `references/`.
- Move executable helpers into `scripts/` and reference them by relative path.
- Write procedures as discrete, ordered steps. Prefer explicit commands over
  vague instruction.

## Do

- Keep every skill agent-agnostic, self-contained, and deterministic.
- State the trigger conditions in each skill `description`.
- Validate that frontmatter parses as YAML before committing a skill.
- Match the naming and layout conventions documented here and in `CONTEXT.md`.
- Record significant decisions in the `CONTEXT.md` decisions log.
- Use conventional commit messages (`feat:`, `fix:`, `docs:`, `chore:`).

## Don't

- Do not put vendor-specific instructions inside a skill (no "only for Claude",
  no "only for pi", no agent-specific tool names).
- Do not add runtime code, dependencies, or a package manifest without prior
  agreement recorded in `CONTEXT.md`.
- Do not modify an approved spec or plan during implementation. Amend it in a
  new spec, or append a dated changelog entry to the existing one.
- Do not create files outside the documented layout.
- Do not commit secrets, tokens, or machine-specific absolute paths.
- Do not commit unless the change is complete and verified for its phase.

## Setup & Verification

```bash
git clone <repo-url> kodit
cd kodit

# Verify a skill's frontmatter parses as YAML (requires yq or python):
python3 -c "import sys, yaml; yaml.safe_load(open(sys.argv[1]).read().split('---')[1])" \
  skills/<skill-name>/SKILL.md
```

There is no build or test step. Verification is structural: files exist in the
documented locations, frontmatter is valid, and prose matches the conventions
above.
