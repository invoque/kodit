---
name: plan-writing
description: >-
  Use when a task needs a plan turning a spec into an ordered approach — invoked
  by the implement workflow skill before it codes a task, or directly ("write a
  plan for T-003"). Requires the task's story spec, drafts a plan with a
  RED→GREEN test-first ordering where tests apply, and saves it to
  .kodit/tmp/specs/. Refuses to plan a task whose story has no spec. Owns the
  plan template and the test-first rule; contains no phase knowledge.
---

# plan-writing

Authors the per-task plan artifact that drives implementation.

## Usage

Invoked by `implement` before each task, or directly by a user. Inputs: the task
ID, its story, the story's spec, and `kodit.json` (for the test command). Output:
`.kodit/tmp/specs/plan-T-NNN-<slug>.md`. Read `references/plan-format.md` before
drafting; it owns the template, the worked example, and the test-first rules.

## What You Must Do When Invoked

### 1. Gather the inputs

Read the story data from the issue tracker (file or Linear) and the task row.
Confirm the story's spec exists at `.kodit/tmp/specs/spec-US-NNN-*.md` and read
it. If the spec is missing, refuse: say the task cannot be planned without one,
and stop. Read the project's `kodit.json` to learn the test command
(`project.test`) and language.

### 2. Draft the plan

Write the plan in the format from `references/plan-format.md`: header (linked
spec, status, date), Approach, an ordered step checklist, Verification, Risks,
and a Review notes section left for later. Keep the steps a technical approach
derived from the spec — what to change and in what order, not the spec restated.

### 3. Order every step test-first (RED → GREEN)

Where the task's behavior is testable, order the work so the test comes first:
name the failing test or assertion, run it and record the failure (RED), then
make the smallest change that passes it (GREEN). One behavior per step. If a
step cannot be tested (pure docs, config, formatting), say so in that step
rather than inventing a fake test.

If `project.test` is absent or empty, use the escape hatch in
`references/plan-format.md`: name a verifiable check (a command, a rendered
output, a lint or build result) that fails first and passes after, and record
the substitution. Fail-first-then-pass still applies; only the mechanism
changes.

### 4. Make it verifiable

For each step, state how the reader will know it is done — the command to run or
the artifact to inspect, and the expected observation. The Verification section
collects these into the final check for the whole task.

### 5. Save and return

Write the plan to `.kodit/tmp/specs/plan-T-NNN-<slug>.md`, where `NNN` is the
task's number and `<slug>` is a short kebab-case name from its description.
Never overwrite an existing plan — if one exists, read it and stop, reporting
its path. Record the plan path in the story's task record (via issue-tracker
operate mode) and return the path.
