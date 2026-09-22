---
name: implement
description: >-
  Use when the user wants to build agreed milestone work — "start implementing",
  "work on the milestone", "do the next task", "implement T-003", or when
  milestone-planning hands off. Computes the next task from the tracker, asks
  whether to run one task or the rest of the milestone, prepares a spec per
  story and a test-first plan per task, implements and commits each task, and
  asks again after every commit. Refuses when the project is not set up or no
  milestone is open. Defines only the sequence, the ask, and the handoff.
---

# implement

The implement phase: work an open milestone one checkpoint at a time.

## Usage

Invoke after `milestone-planning` records a milestone, when an implementation
run was interrupted, or to work a single task. It is a pure orchestrator: it
sequences the work and delegates to general skills, never authoring plans,
tracker files, or code itself. Read `references/spec-format.md` before step 5
and `references/summary-format.md` before the milestone handoff.

## What You Must Do When Invoked

### 1. Verify entry

Follow the `kodit-config` skill in **check mode**. If `kodit.json` is missing,
the project is not set up: say so and stop, directing the user to `setup-kodit`.

### 2. Select the milestone and its branch

Follow the `issue-tracker` skill in **operate mode** to read the project charter
and every milestone. If no milestone is non-`closed`, refuse: name the state and
direct the user to `milestone-planning`. Work exactly one milestone: select the
single non-`closed` one and move it to `active`. Create its branch from the
latest integration branch (`git.dev_branch` in `kodit.json`, default `dev`),
named `<feature_prefix>m-NNN-<slug>`; if it already exists, switch to it and
resume.

### 3. Compute the next unit

Follow the `issue-tracker` skill in **operate mode**: list the milestone's
stories and each story's tasks, and build the ordered worklist — stories in ID
order, tasks in ID order. The **next unit** is the first task not already
`review`/`done`/`wontfix`; flag any item that is `blocked` or labelled
`ready-for-human`, `needs-info`, `needs-triage`, or `wontfix` and skip it. Never
ask the user which task or milestone to work — compute it. If every task is
`review`/`done`/`wontfix`, the milestone is complete: go to step 7.

### 4. Ask the scope

Present the computed unit (task ID and title, its story, and how many tasks
remain) and ask the user to choose:

- **just this task** — work only the next unit, then checkpoint;
- **the rest of the milestone** — keep working tasks until the milestone is
  done (still checkpointing after each commit);
- **stop** — end the run without working anything.

Hold the answer only for the segment it was given for; re-ask at every
checkpoint in step 6.

### 5. Prepare and implement that unit

Repeat per task in the chosen scope:

1. **Ensure a spec for its story.** Look for `spec-US-NNN-*.md` under
   `.kodit/tmp/specs/`; reuse it if present — never rewrite it. If missing,
   generate one from the story's acceptance criteria and body in the format from
   `references/spec-format.md`, moving its tasks `open → spec`.
2. **Plan the task.** Follow the `plan-writing` skill and save `plan-T-NNN-*.md`
   under `.kodit/tmp/specs/`. Link the plan in the story file per
   `references/spec-format.md` and move the task `spec → plan`. The plan carries
   the test-first RED → GREEN ordering.
3. **Approve when the scope is a single task.** For a single-task segment,
   present the spec and plan and wait for approval before implementing; route
   change requests back to steps 1–2 and present again. In a milestone segment,
   continue without pre-approval — the step 6 checkpoint is the correction
   point.
4. **Implement.** Follow the plan exactly. Move the task `plan → implement`,
   dispatch the work to a subagent when available (otherwise inline), and
   enforce the test-first gate: before accepting the passing change, confirm the
   failing test or check was produced and run first. Move the task
   `implement → review` when its code is ready, and move the story to
   `in-progress` if it is not already.

### 6. Commit and checkpoint after every task

Commit the completed task on the milestone branch with a conventional commit
message. Never commit or continue past a task whose checks fail. Then recompute
the next unit (step 3) and report what was committed and what remains, asking
again: **next task, the rest of the milestone, or stop**. Continue on the
answer; this ask is mandatory after every commit, in both scopes.

### 7. Present the milestone summary and hand off

When every task in the milestone is `review`/`done`/`wontfix`, present the
summary in the format from `references/summary-format.md`: the branch, the
stories and tasks completed, the artifacts written, the items skipped or
blocked, the decisions surfaced, and the commits. Then ask whether to open the
pull request now; on yes, tell the user to run the **`pr-request`** skill for
the milestone branch. Do not merge; the pull-request flow owns that.
