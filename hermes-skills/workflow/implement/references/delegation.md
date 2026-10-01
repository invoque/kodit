# Delegation briefs

Per `SKILL.md`, when `delegate_task` is available, delegate each authoring
concern — **spec authoring**, **plan authoring**, **test authoring (RED)**,
**implementation (GREEN)** — to a subagent with the brief below; otherwise
perform the authoring inline yourself under the same contract.

Whatever the mode, the orchestrator owns the `terminal` work and every tracker
transition: it creates and switches the branch, runs the checks, makes both
commits per task, and moves statuses through the `issue-tracker` skill in
**operate mode**. Delegates only produce content. Artifacts under
`.kodit/tmp/specs/` are untracked, so spec and plan authoring commits nothing.

## Spec authoring

- **Inputs:** the story file (acceptance criteria, tasks), `kodit.json`,
  `references/spec-format.md`.
- **Outputs:** `.kodit/tmp/specs/spec-US-NNN-<name>.md`, written with
  `write_file`, or nothing when one already exists — reuse it, never rewrite
  it.
- **Files touched:** the spec file only.
- **Transition (orchestrator applies):** moves the story's tasks `open → spec`
  and the story to `in-progress` via the `issue-tracker` skill.

## Plan authoring

- **Inputs:** the approved story spec, one task's scope, `kodit.json`.
- **Outputs:** `.kodit/tmp/specs/plan-T-NNN-<name>.md`, written with
  `write_file`, with the plans table embedded and a RED → GREEN ordering.
- **Invoked skills:** `plan-writing` (owns the plan format and test-first
  rule).
- **Transition (orchestrator applies):** records plan links in the story file
  and moves the task `spec → plan` via the `issue-tracker` skill.

## Test authoring (RED)

- **Inputs:** the task's plan, its RED steps, the files under test.
- **Outputs:** the failing checks, written to disk with `write_file`.
- **Checks are whatever the plan's RED steps specify** — for markdown-first
  projects that is commonly parse checks or verification greps; for code it is
  the plan's test command.
- **Verification (orchestrator applies):** runs the checks with `terminal`,
  observes the failure, **commits the failing tests** with a `test:`
  conventional message — the failure evidence must be durable before any
  implementation starts — and moves the task `plan → implement`.
- **Never** commit or continue when the checks do not fail as expected.

## Implementation (GREEN)

- **Inputs:** the task's plan (GREEN steps), the committed failing checks.
- **Outputs:** the minimal change that makes the checks pass, written with
  `write_file`/`patch`.
- **Verification (orchestrator applies):** re-runs the checks with `terminal`
  to confirm they pass, commits the passing implementation with `feat:` (new
  behavior) or `fix:` (correction) — never past a failing check — and moves the
  task `implement → review`.
