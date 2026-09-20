---
name: implement
description: >-
  Use when the user wants to start building an agreed milestone — "start
  implementing", "work on the milestone", "let's build it" — or when
  milestone-planning hands off. Selects the open milestone, prepares a spec per
  story and a test-first plan per task, implements each task, keeps the issue
  tracker current, and commits every completed task. Refuses when the project
  is not set up or no milestone is open. Defines only the sequence, the
  approval gate, and the handoff.
---

# implement

The implement phase: work every task in an open milestone to completion.

## Usage

Invoke after `milestone-planning` records a milestone, or when an implementation
run was interrupted. It is a pure orchestrator: it sequences the work and
delegates to general skills, never authoring plans, tracker files, or code
itself. Read `references/spec-format.md` before step 6 and
`references/summary-format.md` before step 10.

## What You Must Do When Invoked

### 1. Verify entry

Follow the `kodit-config` skill in **check mode**. If `kodit.json` is missing,
the project is not set up: say so and stop, directing the user to `setup-kodit`.

### 2. Check and select the milestone

Follow the `issue-tracker` skill in **operate mode** to read the project charter
and every milestone. If no milestone is non-`closed`, refuse: name the state and
direct the user to `milestone-planning`. Work exactly one milestone: select the
single non-`closed` one and move it to `active`.

### 3. Create the milestone branch

Create one branch per milestone from the latest integration branch
(`git.dev_branch` in `kodit.json`, default `dev`), named with the project's
feature prefix and the milestone ID — `<feature_prefix>m-NNN-<slug>`. All task
commits for the milestone land here. If the branch already exists, switch to it
and resume rather than recreating it.

### 4. Ask how plans are approved

Ask once: **interactive** or **non-interactive**. Interactive pauses before each
story's implementation for the user to approve the spec and plans;
non-interactive accepts the skill's recommendations, runs through the milestone,
and presents the summary at the end. Hold the answer for the whole run.

### 5. Survey the worklist

Follow the `issue-tracker` skill in **operate mode**: list the milestone's
stories and each story's tasks, and build the ordered worklist — stories in ID
order, tasks in ID order, skipping tasks already `review`/`done`. Flag any story
or task that is `blocked`, or labelled `ready-for-human`, `needs-info`,
`needs-triage`, or `wontfix`, for the summary instead of working it.

### 6. Ensure a spec per story

For each story in the worklist, look for `spec-US-NNN-*.md` under
`.kodit/tmp/specs/`. Reuse it if present — never rewrite it. If it is missing,
generate one from the story's acceptance criteria and body in the format from
`references/spec-format.md`, moving its tasks `open → spec`. Dispatch spec
authoring to a subagent when one is available, otherwise do it inline.

### 7. Plan per task

For each task in the story, follow the `plan-writing` skill (dispatch to a
subagent when available, otherwise inline) and save `plan-T-NNN-*.md` under
`.kodit/tmp/specs/`. Link the plan in the story file per
`references/spec-format.md` and move the task `spec → plan`. The plan carries
the test-first RED → GREEN ordering.

### 8. Gate on the chosen mode

In **interactive** mode, present the story's spec and its tasks' plans, and wait
for approval before implementing anything; route change requests back to steps
6–7 and present again. In **non-interactive** mode, continue without pausing.
This is a pause within the same run, not the end: once approved (or skipped),
continue to step 9.

### 9. Implement each task

Follow the plan exactly. Move the task `plan → implement`, dispatch the work to
a subagent when available (otherwise inline), and enforce the test-first gate:
before accepting the passing change, confirm the failing test or check was
produced and run first. Move the task `implement → review` when its code is
ready, and move the story to `in-progress` if it is not already. Commit each
completed task on the milestone branch with a conventional commit message.
Never commit or continue past a task whose checks fail.

### 10. Present the milestone summary and hand off

When every task in the milestone is `review`/`done`, present the summary in the
format from `references/summary-format.md`: the branch, the stories and tasks
completed, the artifacts written, the items skipped or blocked, the decisions
surfaced, and the commits. Then tell the user to run the **`pr-request`** skill
to open a pull request for the milestone branch. Do not merge; the pull-request
flow owns that.
