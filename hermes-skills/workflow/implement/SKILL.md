---
name: implement
description: >-
  Use when the user wants to build agreed milestone work — "start implementing",
  "work on the milestone", "do the next task", "implement T-003", or when
  milestone-planning hands off. Works exactly one user story per run: settles an
  automated-vs-step-by-step mode gate, delegates spec, plan, tests, and code
  authoring (or does it inline), commits tests first, presents a story summary,
  and stops with the next step named. Refuses when the project is not set up or
  no milestone is open. Never opens a PR.
version: 1.0.0
author: invoque
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [kodit, implement, milestone, test-first, workflow, delegation]
    related_skills: [kodit-config, issue-tracker, plan-writing, milestone-planning, pr-request]
---

# implement

The implement phase: one user story per run, test-first, via delegation.

## When to Use

- Building agreed milestone work: "start implementing", "work on the milestone",
  "do the next task", "implement T-003".
- Handing off after `milestone-planning` records a milestone — it directs here.
- Resuming an interrupted implement run.
- Not for planning a milestone — use the `milestone-planning` skill. Not for
  opening a PR — that is the `pr-request` skill.

## Usage

A pure orchestrator: it sequences, asks, and reports — it never authors specs,
plans, tests, or code itself. When `delegate_task` is available, delegate each
authoring concern to a subagent with the briefs in `references/delegation.md`;
otherwise perform that authoring inline under the same contract. The
orchestrator always performs the `terminal` work itself — branch creation,
running checks, the commits, and every tracker transition. Load each delegate
skill with `skill_view` when available. Read `references/spec-format.md` before
step 5 and `references/summary-format.md` before step 8.

The delegates and their modes:

- **kodit-config** — check mode.
- **issue-tracker** — operate mode.
- **plan-writing** — its plan format and test-first rule.

## Steps

### 1. Verify entry

Load the `kodit-config` skill with `skill_view` and follow it in **check mode**.
If `kodit.json` is missing, the project is not set up: say so and stop,
directing the user to the `setup-kodit` skill. If the `kodit-config` skill is
not installed, stop and report that it is required.

### 2. Select the milestone and branch

Load the `issue-tracker` skill with `skill_view` and follow it in **operate
mode**. If no milestone is non-`closed`, refuse: name the state and direct the
user to the `milestone-planning` skill. Work exactly one milestone: move the
single non-`closed` one to `active`. Read `git.dev_branch` (default `dev`) and
`git.feature_prefix` from `kodit.json`, compute the branch
`<feature_prefix>m-NNN-<slug>`, and create it with `terminal`, resuming if it
already exists:

```
terminal(command="git rev-parse --verify <branch>")            # exists?
terminal(command="git switch -c <branch> <dev_branch>")       # create
terminal(command="git switch <branch>")                        # resume
```

### 3. Compute the next story

List the milestone's stories in ID order; the **next story** is the first with
any task not `review`/`done`/`wontfix`. Skip — but flag — tasks that are
`blocked` or labelled `ready-for-human`, `needs-info`, `needs-triage`,
`wontfix`. Never ask which story to work. If every remaining task in the
milestone is blocked or labelled, stop and report that state. If no story is
eligible, go to step 8.

### 4. Settle the mode, once

After the refusals and before any delegation: if the invocation contains an
auto-accept phrase — "auto", "you decide", "go on with your recommendation", or
an equivalent — run in **automated** mode. Otherwise ask the user to choose
**automated** or **step-by-step** and hold that answer for the whole run.
Automated: a freshly generated spec and plans are treated as approved.
Step-by-step: exactly two approval STOPs — the spec (step 5) and all plans
together (step 6).

### 5. Spec the story

Delegate spec authoring per `references/delegation.md`, in the format from
`references/spec-format.md`; when `delegate_task` is unavailable, author it
inline. Reuse an existing `spec-US-NNN-*.md` — never rewrite it. Move the
story's tasks `open → spec` and the story to `in-progress` via the
`issue-tracker` skill. In step-by-step mode, present the spec and wait for
approval; route change requests back to the author and present again.

### 6. Plan every task of the story

Author a plan for **all** of the story's tasks — follow the `plan-writing`
skill, save each `plan-T-NNN-*.md` with `write_file` under `.kodit/tmp/specs/`,
record plan links per `references/spec-format.md`, and move tasks `spec → plan`
via the `issue-tracker` skill. In step-by-step mode, present **all plans** in
one STOP and wait for approval before implementing anything.

### 7. Work each task: tests first, then code

Per task, in ID order:

1. **Test authoring (RED).** Write the plan's failing checks, run them with
   `terminal`, and observe the failure. **Commit the failing tests** with a
   `test:` message (never past a failing check), then move the task
   `plan → implement` via the `issue-tracker` skill.
2. **Implementation (GREEN).** Make the minimal change the plan calls for,
   re-run the checks with `terminal` to confirm they pass, commit with `feat:`
   or `fix:`, then move the task `implement → review` via the `issue-tracker`
   skill.

Never commit or continue past a failing check. After each commit, report what
landed and what remains in the story — a report, never a question, in both
modes. Work only tasks of the current story; a second story waits for the next
invocation.

### 8. Story summary and stop

Present the summary from `references/summary-format.md` — the story summary, or
the milestone-exhausted note when step 3 found no eligible story. Then stop:
tell the user to re-invoke `implement` for the next story, or to run the
`pr-request` skill when the milestone is exhausted. Never open, create, or merge
a pull request.

## Pitfalls

- **Committing past a failing check.** The `test:` commit must capture an
  observed failure, and nothing is committed between RED and a passing GREEN.
  Re-run the checks and stop if they do not pass.
- **Rewriting an existing spec.** A present `spec-US-NNN-*.md` is reused as-is.
  Never overwrite it.
- **Starting a second story.** One story per run; a second waits for the next
  invocation, even when its tasks look trivial.
- **Working skipped tasks.** Tasks that are `blocked` or labelled
  `ready-for-human`, `needs-info`, `needs-triage`, or `wontfix` are reported,
  never worked.
- **Re-asking settled scope.** Never ask which story to work, and never re-ask
  the mode mid-run; hold the step-4 answer for the whole run.
- **Changing status outside the tracker.** Every transition goes through the
  `issue-tracker` skill in operate mode — never hand-edit a status.
- **Opening a PR.** This skill stops at the handoff; `pr-request` owns the PR.
- **Improvising a missing dependency.** If `kodit-config`, `issue-tracker`, or
  `plan-writing` is not installed, stop and report it; do not hand-roll its
  work.

## Verification

- `kodit.json` was verified before any branch or tracker action.
- Exactly one non-`closed` milestone was moved to `active`, and its branch was
  created from `git.dev_branch` (default `dev`) or resumed.
- The next story was computed from task states, never asked for.
- The mode was settled once; a step-by-step run had exactly two approval stops
  (the spec, then all plans together).
- Each worked task has a `test:` commit of observed-failing checks followed by
  a `feat:`/`fix:` commit, with no check committed past.
- Task statuses advanced only through `issue-tracker`: `open → spec → plan →
  implement → review` (or `→ done`), and the story is `in-progress`.
- The story summary (or milestone-exhausted note) was presented, and the
  handoff names re-invoking `implement` or running `pr-request`; no PR was
  opened.

## Reference files

| Topic | Read |
| --- | --- |
| Delegation briefs for spec authoring, plan authoring, tests (RED), and code (GREEN) | `references/delegation.md` |
| Spec template, generation steps, and plan-link recording | `references/spec-format.md` |
| Story summary, milestone-exhausted note, and handoff rules | `references/summary-format.md` |
