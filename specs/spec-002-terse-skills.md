# spec-002 — mandatory skill conciseness

**Status:** approved
**Date:** 2026-09-19
**Milestone item:** terse skills, enforced for all future skills

## Summary

Make every skill clean, concise, and terse, and make that standard mandatory
for all future skills. Define the standard in the governing documents
(`AGENTS.md`, `README.md`, `CONTEXT.md`), then bring the repository's one
existing skill (`skills/general/interview/SKILL.md`) into compliance without
changing its behaviour.

## Problem

Skills are loaded into an agent's context under token pressure: every line of a
`SKILL.md` spends context the agent needs to do the actual work. The repository's
canonical skill format (`AGENTS.md`) says to keep `SKILL.md` focused and move
reference material to `references/`, but it sets no measurable limit, so nothing
stops a skill from growing verbose. The single existing skill illustrates the
drift: a ~130-word description, a "Notes on approach" section that restates
three of its eight steps, and templates embedded in the body that belong in
`references/`.

Without a hard, mandatory standard, the six planned `workflow/` skills will
inherit that verbosity and the problem compounds.

## Requirements

### R1 — A mandatory conciseness standard in `AGENTS.md`

Add a *Conciseness (mandatory)* subsection to the "Canonical Skill Format"
section of `AGENTS.md`, stating at minimum:

- `SKILL.md` body stays under **100 lines** (frontmatter excluded). When a skill
  needs more, move formats, templates, and long examples into `references/`
  rather than cutting required detail.
- `description` is one paragraph of **at most ~80 words** that states what the
  skill does and when to trigger it.
- State each idea exactly once: no preamble, no philosophy sections, no closing
  summaries, no principles that restate steps.
- Write imperative steps; cut any sentence that does not change what the agent
  does.
- Never restate a rule `AGENTS.md` already states.

The subsection itself must follow these rules (it must not be verbose about
being terse).

### R2 — Matching `Do` / `Don't` entries

Add one bullet to the `Do` list ("keep every skill terse: under the line cap,
one idea stated once") and one to the `Don't` list ("do not exceed the body line
cap, and do not pad a skill with preamble, rationale, summaries, or
restatements of steps or of this file").

### R3 — A pointer in `README.md` Contributing

Add one line to the Contributing section noting that skills must meet the
conciseness standard (`SKILL.md` body under 100 lines, `description` at most
~80 words) alongside the existing frontmatter-validation step. One line only —
the standard's home is `AGENTS.md`; repeating it at length would violate R1.

### R4 — A decisions-log row in `CONTEXT.md`

Append a row to the `## Decisions Log` table (format
`| Date | Decision | Rationale |`) recording the mandatory conciseness standard
and its limits.

### R5 — Bring the `interview` skill into compliance

Rewrite `skills/general/interview/SKILL.md` to satisfy the standard while
preserving every behaviour required by `spec-001`:

- Delete the `## Notes on approach` section. Three of its four points restate
  steps 1, 4, and 5; fold any unique point into the relevant step.
- Move the design-tree artifact format and the question template out of the body
  into `skills/general/interview/references/` (sanctioned by `AGENTS.md`), and
  point to them from the body.
- Tighten the prose of the eight steps by roughly 30–40% without dropping any
  instruction that changes behaviour.
- Compress the `description` to at most ~80 words while retaining its trigger
  phrases ("interview me", "ask me whatever you need to know", a half-formed
  idea, torn between options, before writing any spec/plan/PRD/design) and its
  exclusions (how-to questions, debugging, well-specified tasks, job-interview
  practice, "just use sensible defaults").
- The frontmatter keeps exactly `name` and `description`; `name` stays
  `interview`.

## Non-requirements

- No scripts, CI, pre-commit hooks, or other validation tooling. The standard is
  enforced by the governing documents and checked during spec/plan review.
- No `workflow/` skills are created or modified by this spec.
- No change to `.agents/skills/` or any externally installed skill.
- No change to `spec-001`, `plan-001`, or their acceptance criteria.
- No change to the `interview` skill's behaviour, only its wording and layout.

## Acceptance criteria

1. `AGENTS.md` contains the *Conciseness (mandatory)* subsection with the
   100-line body cap and the ~80-word description cap.
2. `AGENTS.md` `Do` and `Don't` each contain the conciseness entry from R2.
3. `README.md` Contributing contains the single-line pointer from R3.
4. `CONTEXT.md` decisions log contains the new row from R4.
5. `skills/general/interview/SKILL.md` body (everything after the closing
   frontmatter delimiter) is **at most 100 lines**.
6. The `interview` description is **at most 80 words** and still contains the
   trigger phrases and exclusions listed in R5.
7. `skills/general/interview/SKILL.md` contains no `## Notes on approach`
   section and no embedded question-template or design-tree-format literal; both
   live under `references/` and are referenced from the body.
8. The frontmatter parses as YAML with exactly `name` (`interview`) and
   `description`.
9. Read-through against `spec-001` acceptance criteria 1–7: every behaviour is
   still specified by the rewritten skill. No behaviour is lost.
10. No file outside the documented layout is created.

## Changelog

(none yet)
