# implement

Work every task in an open milestone to completion.

## When to Use

- After `milestone-planning` records a milestone.
- Resuming an interrupted implementation run.

## Prerequisites

- `kodit.json` must exist (checked via `kodit-config` in check mode).
- Exactly one non-`closed` milestone must exist.

If no milestone is open, the skill stops and directs you to `milestone-planning`.

## How It Works

### 1. Verify entry

Follow `kodit-config` in check mode. If `kodit.json` is missing, stop and direct to `setup-kodit`.

### 2. Select the milestone

Follow `issue-tracker` in operate mode. Find the single non-`closed` milestone and move it to `active`.

### 3. Create the milestone branch

Create one branch per milestone from the latest `dev` (or `git.dev_branch`), named `<feature_prefix>m-NNN-<slug>`. All task commits land here. If the branch already exists, switch to it and resume.

### 4. Ask how plans are approved

A one-time choice for the entire run:
- **Interactive:** pauses before each story's implementation for spec+plan approval.
- **Non-interactive:** accepts recommendations, runs through the milestone, presents the summary at the end.

### 5. Survey the worklist

Read all stories and tasks. Build the ordered worklist: stories in ID order, tasks in ID order, skipping tasks already `review`/`done`. Flag blocked items or items with special labels for the summary.

### 6. Ensure a spec per story

For each story, look for `spec-US-NNN-*.md` under `.kodit/tmp/specs/`. Reuse it if present — never rewrite. If missing, generate one from the story's acceptance criteria in the format from `references/spec-format.md`. Move tasks `open → spec`.

### 7. Plan per task

Follow `plan-writing` for each task. Save `plan-T-NNN-*.md` under `.kodit/tmp/specs/`. Link the plan in the story file and move the task `spec → plan`. The plan carries the test-first RED → GREEN ordering.

### 8. Gate on mode

- **Interactive:** present the story's spec and plans, wait for approval, route change requests back to steps 6–7.
- **Non-interactive:** continue without pausing.

### 9. Implement each task

Follow the plan exactly. Move the task `plan → implement`. Enforce the test-first gate: before accepting the passing change, confirm the failing check was produced and run first. Move `implement → review` when code is ready. Commit each completed task with a conventional message. **Never commit or continue past a failing check.**

### 10. Present the summary and hand off

When every task is `review`/`done`, present the summary: branch, stories/tasks completed, artifacts, skipped/blocked items, decisions, and commits. Tell the user to run `pr-request`. Do not merge.

## User Decisions

| Step | Decision |
|---|---|
| 4 | Interactive or non-interactive mode (one-time, holds for the run) |
| 8 | Approval of each story's spec and plans (interactive mode only) |

## Key Rules

- **One branch per milestone.** All commits for the milestone land on `<feature_prefix>m-NNN-<slug>`.
- **Test-first RED → GREEN.** The failing check must be observed before the passing change. A test written after the code proves nothing.
- **No test runner?** When `kodit.json` has no `project.test`, use a verifiable substitute — a command or observation that fails first and passes after.
- **Spec reuse.** An existing `spec-US-NNN-*.md` is never rewritten.
- **Immediate commits.** Every completed task is committed on its feature branch before moving on.

## Artifacts Created

- `.kodit/tmp/specs/spec-US-NNN-<slug>.md` — story specs (if missing)
- `.kodit/tmp/specs/plan-T-NNN-<slug>.md` — task plans
- Code and skill files (per plan)
- Conventional commits on the milestone branch

## Handoff

**Next skill:** `pr-request`

## Source

- Canonical definition: `skills/workflow/implement/SKILL.md`
- Spec template and plan-recording format: `skills/workflow/implement/references/spec-format.md`
- Milestone summary and handoff format: `skills/workflow/implement/references/summary-format.md`
