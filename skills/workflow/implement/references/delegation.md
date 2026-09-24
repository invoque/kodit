# Delegation briefs

Per `SKILL.md`, when a general-purpose subagent capability is available,
delegate each concern — **spec authoring**, **plan authoring**,
**test authoring (RED)**, **implementation (GREEN)** — to it with the brief
below; otherwise perform the work inline yourself under the same contract.
Status writes always go through the `issue-tracker` skill in **operate mode**;
artifacts under `.kodit/tmp/specs/` are untracked, so the spec and plan
delegates commit nothing.

## Spec authoring

- **Inputs:** the story file (acceptance criteria, tasks), `kodit.json`,
  `references/spec-format.md`.
- **Outputs:** `.kodit/tmp/specs/spec-US-NNN-<name>.md`, or nothing when one
  already exists — reuse it, never rewrite it.
- **Invoked skills:** `issue-tracker` (operate mode).
- **Commit:** none.
- **Transition:** moves the story's tasks `open → spec`.

## Plan authoring

- **Inputs:** the approved story spec, one task's scope, `kodit.json`.
- **Outputs:** `.kodit/tmp/specs/plan-T-NNN-<name>.md`, plans table embedded,
  RED → GREEN ordering.
- **Invoked skills:** `plan-writing` (owns the plan format and test-first
  rule), then `issue-tracker` (operate mode) to record plan links in the
  story file.
- **Commit:** none.
- **Transition:** moves the task `spec → plan`.

## Test authoring (RED)

- **Inputs:** the task's plan, its RED steps, the files under test.
- **Outputs:** the failing checks written and run, with the observed failure
  recorded; in this repository the tests are verification greps and YAML/JSON
  parse checks against skill, docs, and eval files (precedent:
  `plan-T-007-implement-checkpoint-loop.md`).
- **Invoked skills:** `issue-tracker` (operate mode).
- **Commit:** **commit the failing tests** immediately with a `test:`
  conventional message — the failure evidence must be durable before any
  implementation starts.
- **Transition:** moves the task `plan → implement`.

## Implementation (GREEN)

- **Inputs:** the task's plan (GREEN steps), the committed failing checks.
- **Outputs:** the minimal change that makes the checks pass, verified by
  re-running them.
- **Invoked skills:** `issue-tracker` (operate mode).
- **Commit:** commits the passing implementation with `feat:` (new behavior)
  or `fix:` (correction) — never past a failing check.
- **Transition:** moves the task `implement → review`.
