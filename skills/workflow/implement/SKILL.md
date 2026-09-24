---
name: implement
description: >-
  Use when the user wants to build agreed milestone work — "start implementing",
  "work on the milestone", "do the next task", "implement T-003", or when
  milestone-planning hands off. Works exactly one user story per run: settles
  an automated-vs-step-by-step mode gate, delegates spec, plan, tests, and code
  to subagents with test-first commits, presents a story summary, and stops
  with the next step named. Refuses when the project is not set up or no
  milestone is open. Never opens a PR.
---

# implement

The implement phase: one user story per run, test-first, via delegation.

## Usage

Invoke after `milestone-planning` records a milestone, to resume an interrupted
run, or to work the next story. Pure orchestrator: it sequences, asks, and
reports — it never authors specs, plans, tests, or code itself. When a
general-purpose subagent capability is available, delegate each concern to it;
otherwise perform that work inline yourself (briefs in
`references/delegation.md`). Read `references/spec-format.md` before step 5
and `references/summary-format.md` before step 8.

## What You Must Do When Invoked

### 1. Verify entry

Follow `kodit-config` in **check mode**. Missing `kodit.json`: the project is
not set up — say so and stop, directing the user to `setup-kodit`.

### 2. Select the milestone and branch

Follow `issue-tracker` in **operate mode**. If no milestone is non-`closed`,
refuse: name the state and direct the user to `milestone-planning`. Work
exactly one milestone: move the single non-`closed` one to `active`, and
create its branch `<feature_prefix>m-NNN-<slug>` from `git.dev_branch`
(default `dev`), resuming if it already exists.

### 3. Compute the next story

List the milestone's stories in ID order; the **next story** is the first
with any task not `review`/`done`/`wontfix`. Skip — but flag — tasks that are
`blocked` or labelled `ready-for-human`, `needs-info`, `needs-triage`,
`wontfix`. Never ask which story to work. If every remaining task in the
milestone is blocked or labelled, stop and report that state. If no story is
eligible, go to step 8.

### 4. Settle the mode, once

After the refusals and before any delegation: if the invocation contains an
auto-accept phrase — "auto", "you decide", "go on with your recommendation",
or an equivalent — run in **automated** mode. Otherwise ask the user to choose
**automated** or **step-by-step** and hold that answer for the whole run.
Automated: a freshly generated spec and plans are treated as approved.
Step-by-step: exactly two approval STOPs — the spec (step 5) and all plans
together (step 6).

### 5. Spec the story

Delegate spec authoring per `references/delegation.md`, in the format from
`references/spec-format.md`. Reuse an existing `spec-US-NNN-*.md` — never
rewrite it. The delegate moves the story's tasks `open → spec`; you move the
story to `in-progress`. In step-by-step mode, present the spec and wait for
approval; route change requests back to the delegate and present again.

### 6. Plan every task of the story

Delegate plan authoring for **all** of the story's tasks — the delegate
follows the `plan-writing` skill, saves each `plan-T-NNN-*.md` under
`.kodit/tmp/specs/`, records plan links per `references/spec-format.md`, and
moves tasks `spec → plan`. In step-by-step mode, present **all plans** in one
STOP and wait for approval before implementing anything.

### 7. Work each task: tests first, then code

Per task, in ID order:

1. **Test delegate (RED).** Writes the plan's failing checks, runs them,
   observes the failure, **commits the failing tests** with a `test:`
   message, and moves `plan → implement`.
2. **Code delegate (GREEN).** Implements the plan's change, verifies the
   checks now pass, commits with `feat:` or `fix:`, and moves
   `implement → review`.

Never commit or continue past a failing check. After each commit, report what
landed and what remains in the story — a report, never a question, in both
modes. Work only tasks of the current story; a second story waits for the
next invocation.

### 8. Story summary and stop

Present the summary from `references/summary-format.md` — the story summary,
or the milestone-exhausted note when step 3 found no eligible story. Then
stop: tell the user to re-invoke `implement` for the next story, or to run
`pr-request` when the milestone is exhausted. Never open, create, or merge a
pull request.
