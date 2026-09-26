---
name: plan-writing
description: >-
  Use when a task needs an implementation plan derived from a story spec —
  "write a plan for T-003", "turn this spec into a plan", or when a kodit
  implement run needs the per-task plan before coding. Requires the task's
  story spec; drafts .kodit/tmp/specs/plan-T-NNN-<slug>.md with an ordered
  technical approach and RED→GREEN test-first step ordering where tests apply,
  with a verifiable-check escape hatch when the project has no test command.
  Refuses to plan a task whose story has no spec. Owns the plan template and
  the test-first rules; contains no kodit phase knowledge.
version: 1.0.0
author: invoque
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [kodit, planning, plan, spec, test-first]
    related_skills: [issue-tracker]
---

# plan-writing

Authors the per-task plan artifact that drives implementation.

## When to Use

- A user asks directly: "write a plan for T-003", "turn this spec into a
  plan", "draft the implementation plan for this task".
- An implement flow needs the per-task plan before it codes.
- Not for writing the spec itself, and not for implementing the task — this
  skill only authors `.kodit/tmp/specs/plan-T-NNN-<slug>.md`.

## Usage

Inputs: the task ID, its story, the story's spec, and `kodit.json` (for the
test command). Output: `.kodit/tmp/specs/plan-T-NNN-<slug>.md`. Read
`references/plan-format.md` before drafting; it owns the template, the worked
example, and the test-first rules.

## Steps

### 1. Gather the inputs

Read the story data and the task row from the issue tracker: follow the
`issue-tracker` skill in operate mode (load it with `skill_view` when
available). If it is not installed, read the file-based tracker directly with
`read_file` (`.kodit/issues/M-NNN-*/US-NNN-*.md`); for a Linear backend, use
the `linear-cli` skill or stop and report that `issue-tracker` is required.

Confirm the story's spec exists at `.kodit/tmp/specs/spec-US-NNN-*.md` with a
`terminal(command="ls .kodit/tmp/specs/")`, then read it with `read_file`. If
the spec is missing, refuse: say the task cannot be planned without one, and
stop.

Read the project's `kodit.json` with `read_file` to learn the test command
(`project.test`) and language.

### 2. Draft the plan

Write the plan in the format from `references/plan-format.md`: header (linked
spec, status, date), Approach, an ordered step checklist, Verification, Risks,
and a Review notes section left for later. Keep the steps a technical approach
derived from the spec — what to change and in what order, not the spec
restated.

### 3. Order every step test-first (RED → GREEN)

Where the task's behavior is testable, order the work so the test comes first:
name the failing test or assertion, run it with `terminal` and record the
failure (RED), then make the smallest change that passes it (GREEN). One
behavior per step. If a step cannot be tested (pure docs, config, formatting),
say so in that step rather than inventing a fake test.

If `project.test` is absent or empty, use the escape hatch in
`references/plan-format.md`: name a verifiable check (a command, a rendered
output, a lint or build result) that fails first and passes after, and record
the substitution. Fail-first-then-pass still applies; only the mechanism
changes.

### 4. Make it verifiable

For each step, state how the reader will know it is done — the command to run
or the artifact to inspect, and the expected observation. The Verification
section collects these into the final check for the whole task.

### 5. Save and return

Write the plan to `.kodit/tmp/specs/plan-T-NNN-<slug>.md`, where `NNN` is the
task's number and `<slug>` is a short kebab-case name from its description.
Never overwrite an existing plan — if one exists
(`terminal(command="test -e .kodit/tmp/specs/plan-T-NNN-<slug>.md")`), read it
and stop, reporting its path.

Record the plan path in the story's task record via the `issue-tracker` skill
in operate mode. If that skill is unavailable, report the plan path and note
that the task record was not updated. Return the path.

## Pitfalls

- **Planning without a spec.** A missing `spec-US-NNN-*.md` is a hard stop, not
  a cue to invent requirements.
- **Overwriting an existing plan.** Read it and report its path instead.
- **Restating the spec as steps.** The plan is the technical approach — what to
  change and in what order.
- **Fake tests.** For a step that genuinely cannot be tested, say so and give
  its verification; never invent a test that cannot fail.
- **Bundling behaviors.** One behavior per RED/GREEN pair; repeat for each.

## Verification

- `.kodit/tmp/specs/plan-T-NNN-<slug>.md` exists, `Status: draft`, and links the
  story's spec.
- Every testable step names a failing test (RED) followed by its smallest green
  change; untestable steps state why and how they are verified.
- Escape-hatch steps record the verifiable-check substitution.
- No existing plan was overwritten, and the plan path was recorded in the task
  record or the omission reported.

## Reference files

| Topic | Read |
| --- | --- |
| Plan template, status flow, RED → GREEN rules, escape hatch, worked example | `references/plan-format.md` |
