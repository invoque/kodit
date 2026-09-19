# plan-002 — mandatory skill conciseness

**Spec:** `specs/spec-002-terse-skills.md`
**Status:** approved
**Date:** 2026-09-19

## Approach

First write the standard into the governing documents (`AGENTS.md` is its home;
`README.md` gets a single pointer; `CONTEXT.md` records the decision). Then
rewrite the `interview` skill to comply: delete the repetition, move the two
literal blocks into `references/`, and tighten the prose. The rewrite is
word-and-layout only — `spec-001`'s acceptance criteria are the behaviour
contract and must all still hold. Work on `feature/terse-skills`; merge to `dev`
only after user review.

## Tasks

- [ ] **T1 — Branch.** `git switch dev && git pull && git switch -c
      feature/terse-skills` (fall back to a plain switch-from-`dev` if no remote).
- [ ] **T2 — Spec and plan.** Author this spec and plan. Commit `docs: add spec
      and plan for terse skills standard`.
- [ ] **T3 — `AGENTS.md`.** Add the *Conciseness (mandatory)* subsection after
      the body-structure bullets in "Canonical Skill Format" (R1), and the
      `Do`/`Don't` bullets (R2). Keep the subsection itself under the standard.
      Commit `docs: make skill conciseness mandatory`.
- [ ] **T4 — `README.md`.** One line in Contributing (R3). Commit `docs: note
      skill conciseness standard in contributing`.
- [ ] **T5 — `CONTEXT.md`.** Append the decisions-log row (R4) and update the
      "Next up"/status line if it references the standard. Commit `docs: record
      skill conciseness decision`.
- [ ] **T6 — References.** Create `skills/general/interview/references/` and move
      the design-tree artifact format and the question template there (R5).
      Commit `feat: extract interview skill references`.
- [ ] **T7 — Rewrite the skill.** Edit `skills/general/interview/SKILL.md`:
      delete `## Notes on approach`, replace the inline template/format with
      pointers to `references/`, tighten the eight steps ~30–40%, and compress
      the description to ≤ 80 words keeping its trigger phrases and exclusions.
      Commit `feat: rewrite interview skill to conciseness standard`.
- [ ] **T8 — Verify.** Run the checks below; fix anything that fails. Commit any
      fix as `fix: ...`.
- [ ] **T9 — Merge.** Merge `feature/terse-skills` into `dev` only after the user
      reviews and approves.

## Verification

- Body line count: lines after the closing `---` of the frontmatter ≤ 100.
- Description word count ≤ 80 and still contains the trigger phrases and
  exclusions listed in R5.
- Frontmatter validation command from `README.md` Contributing passes.
- `## Notes on approach` absent; no embedded question template or design-tree
  format literal in the body; both `references/` files exist and are referenced.
- Read-through against `spec-001` acceptance criteria 1–7: seed, knowledge,
  rounds, facts-vs-decisions, scratch artifact, stop/confirm gate, agent-agnostic
  — all still specified.
- No file outside the documented layout created.

## Risks

- **Line cap not reached by prose tightening alone.** If the body is still over
  100 lines after T7, tighten the Usage inputs/outputs or fold step prose
  further — do not move behaviour into `references/`, and do not cut an
  instruction that changes behaviour.
- **Triggering regression from the shorter description.** Mitigate by keeping
  every trigger phrase and exclusion verbatim where possible; only compress the
  connective wording. If the user later sees under-triggering, the description
  may be re-expanded without touching the body cap.
- **Silent behaviour loss.** The read-through against `spec-001` is the guard;
  do it before merging, not after.
