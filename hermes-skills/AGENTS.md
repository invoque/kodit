# AGENTS.md

Instructions for coding agents working in `hermes-skills/`. This file governs
the `hermes-skills/` subtree and wins over any other instruction for work in it.

## Project Overview

`hermes-skills` is a curated collection of skills for **Hermes Agent**
(Nous Research). Each skill is an on-demand instruction document that teaches
Hermes a task. This subtree is markdown-first: no build step, no runtime code,
no package manifest.

## Mandatory First Step

Before writing, editing, reviewing, or validating **any** skill under this
subtree, load these in order:

1. `general/skill-creator/SKILL.md` — the authoring workflow.
2. `general/skill-creator/references/hermes-skill-format.md` — the full
   frontmatter schema and validation checklist.
3. `general/skill-creator/references/hermes-tools.md` — the Hermes tool and
   toolset vocabulary.

Do not answer format or tooling questions from this file alone. The references
above are the single source of truth for both.

## Directory Layout

```
hermes-skills/
├── AGENTS.md                  # this file
├── general/                   # single-purpose capability skills
│   └── NAME/
│       ├── SKILL.md           # required
│       ├── scripts/           # optional: executable helpers
│       ├── references/        # optional: docs loaded on demand
│       └── assets/            # optional: templates, images, data
└── workflow/                  # phase-orchestrator skills (created on demand)
    └── NAME/
        └── SKILL.md
```

- Categories: `general` (a reusable capability with no phase knowledge) and
  `workflow` (sequences a phase and invokes general skills).
- A skill's directory name **must equal** its frontmatter `name`.
- Names are lowercase kebab-case and globally unique across categories.

## Skill Format (summary)

The full schema is in `references/hermes-skill-format.md`; the essentials:

- `name` and `description` are required. `description` is at most 1024 chars
  and states **what** the skill does and **when** to use it.
- Keep `SKILL.md` well under 500 lines; move detail into `references/`.
- Body order: intro, `## When to Use`, steps/tables, `## Pitfalls`,
  `## Verification`.
- Declare secrets with `required_environment_variables`, non-secret settings
  with `metadata.hermes.config`, and tool gating with `requires_*` /
  `fallback_for_*`. Keep requirements minimal.

## Tool Rules

- Name Hermes tools exactly: `terminal`, `read_file`, `patch`, `write_file`,
  `web_search`, `web_extract`, `execute_code`, `delegate_task`, and the skill
  tools (`skills_list`, `skill_view`, `skill_manage`).
- Never invent a tool or command. If a capability does not exist, express the
  skill as shell commands run through `terminal`.
- Prefer the simplest tool that works. Ship helper scripts in `scripts/` and
  invoke them with `terminal`.

## Do

- Keep each skill self-contained and deterministic.
- Validate against the checklist in `references/hermes-skill-format.md` before
  committing.
- Use conventional commit messages (`feat:`, `fix:`, `docs:`, `chore:`).
- Work on a `feature/*` branch; never commit to a protected branch.

## Don't

- Do not put agent-specific instructions in a skill.
- Do not put secrets in a skill body — use `required_environment_variables`.
- Do not chain references more than one level deep from `SKILL.md`.
- Do not name tools from another runtime (Claude Code, Codex, and the like).
- Do not exceed the 500-line body cap or pad a skill with preamble.

## Distribution

This collection is consumed by Hermes via GitHub.

- Install one skill directly (no tap needed):
  `hermes skills install OWNER/REPO/hermes-skills/general/NAME`
- Tap-style: add an entry with a non-default path (`hermes-skills/`) in
  `~/.hermes/skills/.hub/taps.json`, then `hermes skills tap add OWNER/REPO`.
  Whether discovery recurses through the category directory is **unverified**;
  confirm with a live `hermes skills search` before relying on it.
- Publish changes with
  `hermes skills publish DIR --to github --repo OWNER/REPO`.
- Installed skills land in `~/.hermes/skills/` on the user's machine.
