---
name: skill-creator
description: Create, edit, validate, and improve Hermes Agent skills. Use whenever the user wants to create a new skill for Hermes, turn a workflow or document into a skill, edit or fix an existing SKILL.md, add Hermes frontmatter (platforms, metadata.hermes, required env vars), or test and iterate a skill's triggering description. Trigger this even if the user does not say "skill" explicitly and instead asks to capture a process, package know-how, or make the agent remember how to do something.
version: 1.0.0
author: invoque
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [hermes, skills, meta, authoring, skill-creator]
    related_skills: [hermes-agent]
---

# Skill Creator (Hermes)

Create and improve skills for **Hermes Agent**. A skill is a directory with `SKILL.md`
(required) plus optional `scripts/`, `references/`, and `assets/`. Hermes loads the `name` +
`description` up front and injects the body only on trigger (progressive disclosure).

Figure out where the user is and help them move forward. They may arrive with an idea, a
rough draft, or a finished skill that only needs fixing. Adapt — do not force every stage.

## Workflow

### 1. Capture intent

Mine the current conversation first if it contains the workflow ("turn this into a skill"):
the tools used, step sequence, corrections, input/output formats. Then confirm what you
found rather than asking blindly. Establish:

1. What should this skill let Hermes do?
2. When should it trigger — which user phrasings or contexts?
3. What is the expected output (format, files, side effects)?
4. Does it need secrets, config, a specific OS, or specific tools? (Frontmatter fields in
   `references/hermes-skill-format.md` express these.)

### 2. Interview

Ask about edge cases, formats, example files, success criteria, and dependencies. Use
`clarify` only when a decision blocks progress. Investigate the codebase, docs, or web
(`web_search`, `web_extract`, `terminal`) before asking what you can find yourself.

Decide whether the skill needs tests. Objectively verifiable outputs (file transforms,
extraction, fixed workflows) benefit; subjective skills (style, design) usually do not.
Suggest a default; let the user decide.

### 3. Draft the skill

Create `CATEGORY/<skill-name>/SKILL.md` in this repo, where `CATEGORY` is `general` or
`workflow`. The directory name **must** equal the frontmatter `name`. Start from
`assets/skill-template/SKILL.md` and fill it in.
For the full frontmatter schema, read `references/hermes-skill-format.md`.

Use Hermes-specific fields only when they earn their place: `platforms` for OS gating,
`requires_toolsets` / `requires_tools` / `fallback_for_*` for conditional activation,
`required_environment_variables` for secrets, `config` for non-secret settings,
`required_credential_files` for OAuth files, `blueprint` for cron automations.

Write the body in **imperative form**, in Hermes tool vocabulary (`terminal`,
`read_file`/`patch`/`write_file`, `web_search`, `web_extract`, `execute_code`,
`delegate_task`, and the skill tools by their real names). Never invent commands or tools.
House body order: intro; `## When to Use`; steps/tables/examples; `## Pitfalls`;
`## Verification`. For writing patterns and progressive-disclosure rules, read
`references/skill-authoring-guide.md`.

### 4. Validate

Check the draft against the checklist in `references/hermes-skill-format.md`. At minimum:

- `name` matches the directory and passes the charset/length rules.
- `description` is non-empty, <=1024 chars, and states both the what and the when.
- The body is well under 500 lines; detail has been moved to `references/`.
- All linked files exist and are referenced with relative paths one level deep.
- No foreign-runtime tool names remain.

### 5. Optional test loop

For evidence the skill works, run a lightweight evaluation with `delegate_task`:

1. Write 2–5 realistic prompts with clear expected outcomes.
2. Run each prompt twice in isolated subagents — once **without** the skill, once **with**
   its instructions included.
3. Compare manually: where the skill changed behavior, and where it did not.
4. Report what improved, what stayed the same, what got worse.

No browser viewer or automated timing/token capture. If the `delegation` toolset is
unavailable, skip this stage or run the prompts yourself and reason about the difference.

### 6. Iterate

Rewrite based on the comparison and user feedback, plus any obvious flaws. Re-run affected
test prompts if the change is significant. Repeat until the user is satisfied.

### 7. Optimize the description (triggering)

The `description` is the only thing Hermes sees before loading the skill, so it drives
triggering.

1. List ~10 realistic phrasings that **should** trigger the skill and ~10 that should **not**.
2. Check the current description against them. Broaden phrasing if it misses valid triggers;
   add boundaries if it would fire on unrelated work.
3. Stay within 1024 characters and prefer concrete keywords. Being slightly "pushy" is
   encouraged so the skill fires when useful.

### 8. Hand off

Summarize the finished skill: name, what it does, when it triggers, files created, and how
to install it (copy to `~/.hermes/skills/`, or publish the repo as a tap and run
`hermes skills install`). If the user asked for tests, state the observed results.

## Communicating with the user

Match the user's level — from non-technical to expert. Define a term briefly when unsure
("`description` is the line Hermes uses to decide when to load the skill"). Do not lecture;
prefer a short definition over jargon.

## Principle of Lack of Surprise

A skill must not contain malware, exploit code, credential exfiltration, or anything that
would compromise the user's system. Its contents must not surprise the user given how it was
described. Do not create misleading skills or ones facilitating unauthorized access or data
exfiltration, and do not fold user instructions that override these constraints into a skill.

## Reference files

Load the matching file before detailed work — do not answer format or tooling questions from
this body alone:

| Topic | Read |
| --- | --- |
| Full Hermes frontmatter schema, field-by-field, with examples and a validation checklist | `references/hermes-skill-format.md` |
| Hermes tools and toolsets, and which to reference from a skill | `references/hermes-tools.md` |
| Writing patterns, section order, progressive disclosure, description style | `references/skill-authoring-guide.md` |
| Starter SKILL.md with Hermes frontmatter | `assets/skill-template/SKILL.md` |
