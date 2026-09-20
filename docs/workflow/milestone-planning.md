# milestone-planning

Agree the next milestone's scope and record it in the issue tracker.

## When to Use

- After `setup-kodit` completes setup.
- When you have a new batch of work to plan.
- Resuming an interrupted planning run (`.kodit/tmp/design-tree-milestone-scope.md` exists).

## Prerequisites

- `kodit.json` must exist (checked via `kodit-config` in check mode).
- **Exactly one milestone** must be `closed` or there must be **no milestones** yet.
- No closed milestone may have an unmerged or open PR with a merge record.

If any of these fail, the skill refuses and names the blocker.

## How It Works

### 1. Verify entry

Follow `kodit-config` in check mode. If `kodit.json` is missing, stop and direct to `setup-kodit`.

### 2. Check the milestone state

Follow `issue-tracker` in operate mode. Read every milestone and derive its status. Refuse when:
- Any milestone is not `closed` (direct to `implement`, close it, or re-scope).
- Any closed milestone has a PR without a merge record, or has an open/queued PR (direct to `pr-approve`).

### 3. Settle the scope

Gather context: project charter, closed milestones, next global numbers, and sizing guidance. Follow `interview` with topic "milestone scope". Steer toward 2–5 stories, 2–6 tasks per story, ≤ ~20 tasks total (soft caps — a strong recommendation, never a rejection). If a design-tree draft exists, resume from it.

### 4. Checkpoint — STOP

Present: milestone goal, stories with acceptance criteria, task tables, allocated numbers, files to create/update, and a sizing verdict. **Nothing is written until you approve.** Change requests route back to step 3.

### 5. Record the milestone

Follow `issue-tracker` in operate mode to create:
- `.kodit/issues/M-NNN-goal-name/INDEX.md` (charter, status: `planned`)
- `.kodit/issues/M-NNN-goal-name/US-NNN-name.md` (stories with embedded task tables)
- Updated row in `.kodit/issues/INDEX.md`

Re-reads the tracker first; never duplicates an existing milestone or story.

### 6. Record decisions

Follow `kodit-config` in **decisions mode** to append milestone-shaping decisions to the `CONTEXT.md` decisions log.

### 7. Hand off

Present the final summary: milestone, stories, numbers allocated, decisions recorded, and the next action — run `implement`.

## User Decisions

| Step | Decision |
|---|---|
| 3 | Milestone goal, story scope, acceptance criteria, task breakdown |
| 4 | Approval of the full milestone proposal before anything is recorded |

## Key Rules

- **Single milestone at a time.** Only one non-closed milestone is permitted.
- **Soft sizing caps.** 2–5 stories, 2–6 tasks per story, ≤ ~20 tasks total. Overages are accepted and recorded, never silently dropped.
- **No implementation detail.** Plans, task sequencing, and assignment belong to the implement phase.

## Artifacts Created

- `.kodit/issues/M-NNN-<name>/INDEX.md` — milestone charter
- `.kodit/issues/M-NNN-<name>/US-NNN-<name>.md` — user stories
- Updated `.kodit/issues/INDEX.md` — project charter index
- Appended decisions in `CONTEXT.md`

## Handoff

**Next skill:** `implement`

## Source

- Canonical definition: `skills/workflow/milestone-planning/SKILL.md`
- Sizing guidance, checkpoint/summary formats, worked example, reviewer's checklist: `skills/workflow/milestone-planning/references/sizing-and-examples.md`
