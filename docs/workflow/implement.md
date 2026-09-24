# implement

Work exactly one user story per invocation — test-first, via delegation — and end in a story summary. The skill never opens a pull request.

## When to Use

- After `milestone-planning` records a milestone.
- Resuming an interrupted implementation run.
- To work the next story ("start implementing", "work on the milestone", "do the next task", "implement T-003").

## Prerequisites

- `kodit.json` must exist (checked via `kodit-config` in check mode).
- Exactly one non-`closed` milestone must exist.

If no milestone is open, the skill stops and directs you to `milestone-planning`.

## Mode

Settled once per run — after the entry refusals and next-story computation (steps 1–3), before any delegation (step 5).

- If the invocation contains an auto-accept phrase — "auto", "you decide", "go on with your recommendation", or an equivalent — the run is **automated** and no mode question is asked.
- Otherwise the user chooses **automated** or **step-by-step**; the answer holds for the whole run.
- **Automated:** a freshly generated spec and plans are treated as approved.
- **Step-by-step:** exactly two approval stops — the spec (step 5), then all plans together (step 6).

## How It Works

### 1. Verify entry

Follow `kodit-config` in check mode. If `kodit.json` is missing, the project is not set up — stop and direct the user to `setup-kodit`.

### 2. Select the milestone and its branch

Follow `issue-tracker` in operate mode. If no milestone is non-`closed`, refuse: name the state and direct the user to `milestone-planning`. Move the single non-`closed` milestone to `active` and create its branch `<feature_prefix>m-NNN-<slug>` from `git.dev_branch` (default `dev`), resuming if it already exists. All task commits land here.

### 3. Compute the next story

List the milestone's stories in ID order. The **next story** is the first with any task not `review`/`done`/`wontfix`. Skip — but flag — tasks that are `blocked` or labelled `ready-for-human`, `needs-info`, `needs-triage`, `wontfix`. **Never ask which story to work — compute it.** If every remaining task in the milestone is blocked or labelled, stop and report that state. If no story is eligible, go to step 8.

### 4. Settle the mode, once

Apply the Mode section above: an auto-accept phrase in the invocation means automated mode with no question asked; otherwise ask the user to choose automated or step-by-step and hold that answer for the whole run.

### 5. Spec the story

Delegate spec authoring per `references/delegation.md`, in the format from `references/spec-format.md`. Reuse an existing `spec-US-NNN-*.md` under `.kodit/tmp/specs/` — never rewrite it. The delegate moves the story's tasks `open → spec`; you move the story to `in-progress`. In step-by-step mode, present the spec and wait for approval; route change requests back to the delegate and present again.

### 6. Plan every task of the story

Delegate plan authoring for **all** of the story's tasks. The delegate follows `plan-writing`, saves each `plan-T-NNN-*.md` under `.kodit/tmp/specs/`, records plan links in the story per `references/spec-format.md`, and moves tasks `spec → plan`. In step-by-step mode, present **all plans in one stop** and wait for approval before implementing anything.

### 7. Work each task: tests first, then code

Per task, in ID order:

1. **Test delegate (RED).** Writes the plan's failing checks, runs them, observes the failure, **commits the failing tests** with a `test:` message, and moves `plan → implement`.
2. **Code delegate (GREEN).** Implements the plan's change, verifies the checks now pass, commits with `feat:` or `fix:`, and moves `implement → review`.

Never commit or continue past a failing check. After each commit, report what landed and what remains in the story — a report, never a question, in both modes. Work only tasks of the current story; a second story waits for the next invocation.

### 8. Story summary and stop

Present the summary from `references/summary-format.md` — the story summary, or the milestone-exhausted note when step 3 found no eligible story. Then stop: tell the user to re-invoke `implement` for the next story, or to run `pr-request` when the milestone is exhausted. Never open, create, or merge a pull request.

## Delegation Ladder

| Concern | Delegate | Commit | Status transition |
|---|---|---|---|
| Spec authoring | spec delegate | none | `open → spec` |
| Plan authoring | plan delegate | none | `spec → plan` |
| Test authoring (RED) | test delegate | `test:` | `plan → implement` |
| Implementation (GREEN) | code delegate | `feat:` or `fix:` | `implement → review` |

Status writes go through `issue-tracker` in operate mode; artifacts under `.kodit/tmp/specs/` are untracked, so the spec and plan delegates commit nothing. Full briefs live in `references/delegation.md`.

## Two-Commit Policy

Each task lands in two commits: the RED `test:` commit carrying the observed failure must be durable before the GREEN `feat:`/`fix:` commit begins. For this markdown repository the checks are verification greps and YAML/JSON parse checks against skill, docs, and eval files; the two-commit discipline applies unchanged.

## User Decisions

| Step | Decision |
|---|---|
| 4 | Mode: automated or step-by-step (every run; asked once unless the invocation already accepted automation) |
| 5 | Story spec approval (step-by-step mode only) |
| 6 | All of the story's plans, approved together (step-by-step mode only) |

## Key Rules

- **One story per run.** Exactly one user story per invocation; never start a second story, even when tasks remain.
- **Compute the story, never ask.** The next story comes from the tracker in ID order; there is no scope question.
- **Delegate-owned transitions.** Spec, plan, test, and code delegates move tasks `open → spec → plan → implement → review`. The orchestrator owns only milestone → active plus branch creation, and story → in-progress.
- **Spec reuse.** An existing `spec-US-NNN-*.md` is never rewritten.
- **Checkpoint is a report.** After each commit, report what landed and what remains — never a question, in both modes.

## Artifacts Created

- `.kodit/tmp/specs/spec-US-NNN-<slug>.md` — story spec (reused when present)
- `.kodit/tmp/specs/plan-T-NNN-<slug>.md` — task plans
- Code and skill files (per plan)
- Conventional commits on the milestone branch: `test:` then `feat:`/`fix:` per task

## Handoff

The story stop ends the run. Next step: re-invoke `implement` for the next story, or run `pr-request` when the milestone is exhausted. The skill never creates a pull request. Do not merge or push protected branches — the pull-request flow and the review that follows own those steps.

## Source

- Canonical definition: `skills/workflow/implement/SKILL.md`
- Delegation briefs: `skills/workflow/implement/references/delegation.md`
- Spec template and plan-recording format: `skills/workflow/implement/references/spec-format.md`
- Story summary and handoff format: `skills/workflow/implement/references/summary-format.md`
