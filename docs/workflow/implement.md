# implement

Work an open milestone one checkpoint at a time.

## When to Use

- After `milestone-planning` records a milestone.
- Resuming an interrupted implementation run.
- To work a single next task ("do the next task", "implement T-003").

## Prerequisites

- `kodit.json` must exist (checked via `kodit-config` in check mode).
- Exactly one non-`closed` milestone must exist.

If no milestone is open, the skill stops and directs you to `milestone-planning`.

## How It Works

### 1. Verify entry

Follow `kodit-config` in check mode. If `kodit.json` is missing, stop and direct to `setup-kodit`.

### 2. Select the milestone and its branch

Follow `issue-tracker` in operate mode. Find the single non-`closed` milestone and move it to `active`. Create its branch from the latest `dev` (or `git.dev_branch`), named `<feature_prefix>m-NNN-<slug>`. All task commits land here. If the branch already exists, switch to it and resume.

### 3. Compute the next unit

Read all stories and tasks and build the ordered worklist: stories in ID order, tasks in ID order, skipping tasks already `review`/`done`. The next unit is the first task not already `review`/`done`/`wontfix`. Flag blocked items or items with special labels and skip them. **You never ask the user which task to work — you compute it.** If every task is `review`/`done`/`wontfix`, the milestone is complete; go to step 7.

### 4. Ask the scope

Present the computed unit — task ID and title, its story, and how many tasks remain — and ask the user to choose:

- **just this task** — work only the next unit, then checkpoint.
- **the rest of the milestone** — keep working tasks until the milestone is done, still checkpointing after each commit.
- **stop** — end the run without working anything.

Ask before any work begins. The answer holds only for that segment; you re-ask at every checkpoint.

### 5. Prepare and implement that unit

Per task in the chosen scope:

1. **Ensure a spec for its story.** Look for `spec-US-NNN-*.md` under `.kodit/tmp/specs/`. Reuse it if present — never rewrite. If missing, generate one from the story's acceptance criteria in the format from `references/spec-format.md`. Move tasks `open → spec`.
2. **Plan the task.** Follow `plan-writing`. Save `plan-T-NNN-*.md` under `.kodit/tmp/specs/`. Link the plan in the story file and move the task `spec → plan`. The plan carries the test-first RED → GREEN ordering.
3. **Approve on single-task scope.** Present the spec and plan and wait for approval before implementing; route change requests back to steps 1–2. In a milestone segment, continue without pre-approval.
4. **Implement.** Follow the plan exactly. Move the task `plan → implement`. Enforce the test-first gate: before accepting the passing change, confirm the failing check was produced and run first. Move `implement → review` when code is ready, and the story to `in-progress` if it is not already.

### 6. Commit and checkpoint after every task

Commit the completed task on the milestone branch with a conventional message. **Never commit or continue past a failing check.** Then recompute the next unit and report what was committed and what remains, asking again: **next task, the rest of the milestone, or stop**. This ask is mandatory after every commit, in both scopes.

### 7. Present the summary and hand off

When every task is `review`/`done`/`wontfix`, present the summary: branch, stories/tasks completed, artifacts, skipped/blocked items, decisions, and commits. Ask whether to open the pull request now; on yes, tell the user to run `pr-request`. Do not merge.

## User Decisions

| Step | Decision |
|---|---|
| 4 | Scope of the segment: one task, the rest of the milestone, or stop (re-asked at every checkpoint) |
| 5 | Approval of the spec and plan (single-task scope only) |
| 7 | Whether to hand off to `pr-request` now |

## Key Rules

- **One branch per milestone.** All commits for the milestone land on `<feature_prefix>m-NNN-<slug>`.
- **Compute, don't ask.** The skill determines the next task from the tracker; the user chooses only the scope.
- **Test-first RED → GREEN.** The failing check must be observed before the passing change. A test written after the code proves nothing.
- **No test runner?** When `kodit.json` has no `project.test`, use a verifiable substitute — a command or observation that fails first and passes after.
- **Spec reuse.** An existing `spec-US-NNN-*.md` is never rewritten.
- **Immediate commits.** Every completed task is committed on its feature branch before the checkpoint.

## Artifacts Created

- `.kodit/tmp/specs/spec-US-NNN-<slug>.md` — story specs (if missing)
- `.kodit/tmp/specs/plan-T-NNN-<slug>.md` — task plans
- Code and skill files (per plan)
- Conventional commits on the milestone branch

## Handoff

**Next skill:** `pr-request` (offered at the milestone-completion checkpoint)

## Source

- Canonical definition: `skills/workflow/implement/SKILL.md`
- Spec template and plan-recording format: `skills/workflow/implement/references/spec-format.md`
- Milestone summary and handoff format: `skills/workflow/implement/references/summary-format.md`
