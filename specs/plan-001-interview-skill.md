# plan-001 — `interview` general skill

**Spec:** `specs/spec-001-interview-skill.md`
**Status:** approved
**Date:** 2026-09-19

## Approach

Write the skill as a single self-contained `SKILL.md` (no `references/` or
`scripts/`: the capability is purely conversational and fits comfortably under
the 500-line guidance). Validate it with the skill-creator qualitative eval
loop before committing. Commits happen on `feature/interview-skill`; merge to
`dev` only after the user approves the eval results.

## Tasks

- [ ] **T1 — Branch.** `git switch -c feature/interview-skill` from `dev`.
- [ ] **T2 — Spec and plan.** Author `specs/spec-001-interview-skill.md` and
      this plan. Commit `docs: add spec and plan for interview skill`.
- [ ] **T3 — Draft skill.** Author `skills/general/interview/SKILL.md`:
  - frontmatter: `name: interview` plus a description that states what the
    skill does and when to use it, with trigger guidance (planning a feature,
    spec, or design; user asks to be interviewed; requirements unclear).
  - `# Interview`, one-line purpose, `## Usage`.
  - `## What You Must Do When Invoked` with ordered steps:
    1. Seed the design tree from the topic and from decisions already settled
       in the conversation (never re-ask what is already settled).
    2. Create/refresh the scratch artifact `.kodit/tmp/design-tree-<topic>.md`
       marking nodes settled / open / blocked.
    3. Compute the knowledge (open nodes whose parents are all settled).
    4. Dispatch fact-finding for unresolved facts (subagent if available,
       otherwise inline); do not block — ask the rest of the knowledge now and
       defer only the downstream questions.
    5. Emit one round in the fixed format; number questions; up to three
       options; exactly one strong recommendation after `➡️`.
    6. Wait for answers; fold them in; recompute the knowledge; repeat.
    7. When the knowledge is empty, present the settled design tree as a
       summary and ask the user to confirm shared understanding.
    8. Do not act on the design until the user confirms.
  - A short "facts vs. decisions" section explaining why guessing user
    decisions poisons the tree and why asking for look-up-able facts wastes the
    user's time.
- [ ] **T4 — Evals JSON.** Write the three prompts from spec Appendix A to
      `.kodit/tmp/workspaces/interview-workspace/evals/evals.json`.
- [ ] **T5 — Run iteration-1.** Spawn six subagents in one turn: three
      with-skill, three baseline (`without_skill`). Save transcripts to
      `.kodit/tmp/workspaces/interview-workspace/iteration-1/eval-N/`.
      Write `eval_metadata.json` per eval. Capture `timing.json` from each
      task notification as it arrives.
- [ ] **T6 — Eval viewer.** Run
      `python .agents/skills/skill-creator/eval-viewer/generate_review.py`
      with `--static` to produce a standalone HTML file for the user. No
      benchmark/assertions — the skill is qualitative.
- [ ] **T7 — Review and iterate.** Read the user's feedback, improve the
      skill (generalize; do not overfit the three prompts), rerun as
      `iteration-2/` with `--previous-workspace` if needed. Repeat until the
      user is satisfied.
- [ ] **T8 — Finalize.** Validate frontmatter with the README command. Update
      `CONTEXT.md` (status line and decisions log entry for the design-tree
      interview method and scratch-file convention). Commit
      `feat: add interview general skill` and any follow-up `docs:` commit.

## Verification

- Frontmatter validation command from `README.md` Contributing passes.
- Acceptance criteria 1–7 from the spec are checked off, with criterion 7
  evidenced by the iteration-1 review.

## Risks

- **Overfitting to three prompts.** Mitigate by generalizing feedback rather
  than adding prompt-specific language.
- **Skill length.** Keep the procedure tight; the round format template is the
  only large literal block.
- **Agent-agnostic wording for subagents.** Use "delegate to a subagent when
  one is available, otherwise research inline"; never name a tool.

## Review notes

### 2026-09-19 — iteration-1 review

Qualitative review of three with-skill runs against three no-skill baselines
(workspace: `.kodit/tmp/workspaces/interview-workspace/iteration-1`).

**Confirmed working.** Settled decisions were seeded and never re-asked (eval
2); dependent questions correctly waited for later rounds (eval 1); the round
format was followed exactly; every with-skill run ended at the confirmation
gate, while every baseline front-loaded a full design or schema before any
answer.

**Findings and resolutions.**

1. *Over-seeded inference.* In eval 0 the agent inferred "low budget tolerance,
   prefers operational simplicity" from "side project" and seeded it as a fact,
   then used it to justify a recommendation. Resolved by spec changelog
   amendment 1: inferred preferences are never settled facts.
2. *Round-size inflation.* Rounds reached 5–6 questions (17 in one session).
   Resolved by amendment 2: order most-consequential-first, soft ~6 guideline.
3. *Inconsistent numbering.* Evals 1–2 restarted at Q1 each round; eval 0
   numbered continuously. Resolved by amendment 3: continuous numbering.
4. *Shifting node IDs.* A node renumbered on settling, making references
   unstable. Resolved by amendment 4: stable IDs.

Iteration-2 reruns all six cells with the revised skill.

### 2026-09-19 — iteration-2 review

Same three prompts, revised skill, six fresh runs
(`.kodit/tmp/workspaces/interview-workspace/iteration-2`).

**All four fixes verified.** The greenfield run no longer seeds "side project →
low budget" as a fact; it lists those inferences explicitly as not settled and
carries a labeled assumption instead. Rounds are ordered most-consequential-first
and stay within the soft cap (4/6/6 and 6/4/2). Question numbering is continuous
(Q1–Q14, Q1–Q12, Q1–Q17). Tree nodes carry stable IDs that survive status
changes. Regressions checked: exactly one recommendation per question in all
runs, and no settled decision is re-asked (eval 2 references settled nodes
rather than questioning them).

**User review outcome.** All three with-skill runs marked "looks great"; the
baselines were rejected, one explicitly because its questions were not
numbered — the failure the skill exists to prevent. Skill approved for
finalization; merge to `dev` deferred pending the user's final review.

**Description optimization.** Deferred to a follow-up step using an
`opencode`-based harness (the machine uses `opencode`, not `claude`; the
skill-creator optimizer scripts are hardwired to the latter).
