---
name: milestone-planning
description: >-
  Use when the user wants to plan the next milestone — "let's plan a milestone",
  "scope the next chunk of work", "define the next set of stories" — or when
  setup-kodit hands off after setup. Interviews the user to a shared scope, then
  records the milestone, its stories, acceptance criteria, and tasks in the
  issue tracker. Refuses when a milestone is still open, setup is incomplete, or
  a reviewed milestone PR remains unmerged.
  Defines only the sequence and the review gate.
version: 1.0.0
author: invoque
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [kodit, milestone, planning, scope, workflow, stories]
    related_skills: [kodit-config, issue-tracker, interview]
---

# milestone-planning

The milestone-planning phase: agree the next milestone's scope and record it.

## When to Use

- Planning the next milestone: "let's plan a milestone", "scope the next chunk
  of work", "define the next set of stories".
- Handing off after setup — the `setup-kodit` skill directs here once setup is
  complete.
- Resuming a milestone-planning run that was interrupted and left a design-tree
  scratch file behind.
- Not for working milestone items — that is the milestone workflow's implement
  phase.

## Usage

Invoke when setup is complete and a new milestone's worth of work exists, or
when a milestone-planning run was interrupted. Delegates all work to general
skills and never writes tracker or documentation files itself. Load each
delegate with `skill_view` when available. Read
`references/sizing-and-examples.md` before settling scope or presenting the
checkpoint. The delegates and their modes:

- **kodit-config** — check mode, decisions mode.
- **issue-tracker** — operate mode.
- **interview** — its interview procedure, topic "milestone scope".

## Steps

### 1. Verify entry

Load the `kodit-config` skill with `skill_view` and follow it in **check mode**.
If `kodit.json` is missing, the project is not set up: say so and stop,
directing the user to the `setup-kodit` skill. If the `kodit-config` skill is
not installed, stop and report that it is required.

### 2. Check the milestone state

Load the `issue-tracker` skill with `skill_view` and follow it in **operate
mode** to read the project charter and every milestone, deriving each
milestone's status. If any milestone is not `closed` (`planned` or `active`),
refuse: name it, and direct the user to implement it (the `implement` skill),
close it, or explicitly re-scope it first. If any milestone is `closed` but
records a PR without a merge record, or records an open/queued PR, refuse and
direct the user to reconcile the merge with the `pr-approve` skill first; if
`pr-approve` is not installed, reconcile the merge through the `issue-tracker`
skill's operate mode, which owns PR and merge records. Do not plan a second
milestone. Stop. If the `issue-tracker` skill is not installed, stop and report
that it is required.

### 3. Settle the scope

Gather context: the project charter, any closed milestones, the next global
`M`/`US`/`T` numbers from the tracker, and the sizing guidance in
`references/sizing-and-examples.md`. Then follow the `interview` skill with
topic "milestone scope" and that context. Steer toward milestone-sized chunks
using the soft caps. If `.kodit/tmp/design-tree-milestone-scope.md` exists,
resume from it instead of re-asking settled decisions. If the `interview` skill
is not installed, ask the scope questions directly and steer with the same
sizing caps.

### 4. Checkpoint — STOP

Present the expected result for review, in the format from
`references/sizing-and-examples.md`: the milestone goal, each story with its
acceptance criteria and task table, the allocated `M`/`US`/`T` numbers, the
list of files to be created or updated, and a sizing verdict. Route each change
request back to step 3 and present again.

This is a pause for approval within the same run, not the end: once the user
approves, continue to step 5. Write nothing until then.

### 5. Record the milestone

Follow the `issue-tracker` skill in **operate mode** to create the milestone
with its charter (`status: planned`), the story files (frontmatter, Story,
Acceptance Criteria, and embedded Tasks table at `status: open`), and update the
project charter. Re-read the tracker first; never duplicate an existing milestone
or story.

### 6. Record decisions

Follow the `kodit-config` skill in **decisions mode** to append the
milestone-shaping decisions settled in step 3 to the `CONTEXT.md` decisions
log. Record only what was agreed.

### 7. Hand off

Present the final summary from `references/sizing-and-examples.md`: the
milestone and its stories, the numbers allocated, the decisions recorded, and
the next action — invoke the `implement` skill to start implementation. If the
`implement` skill is not installed, name it as the next skill to install. Offer
to commit the new tracker files if the project's conventions expect it.

## Pitfalls

- **Planning a second milestone.** Any milestone that is not `closed`
  (`planned` or `active`), or a closed one with an unreconciled PR, blocks
  planning. Refuse, name it, and give the remedy — never plan over an open
  milestone.
- **Writing before approval.** Nothing is written until step 4 is approved.
  Route each change request back to step 3 and present the checkpoint again; the
  design-tree scratch file is the only state until then.
- **Duplicating IDs.** Re-read the tracker before recording; `M`/`US`/`T`
  numbers are global and never reused. Never duplicate an existing milestone or
  story.
- **Re-asking settled scope.** A present
  `.kodit/tmp/design-tree-milestone-scope.md` is the interview's state — resume
  from it, do not re-open decisions it already settled.
- **Recording decisions nobody agreed to.** Step 6 records only the decisions
  settled in step 3; never invent rationale or add unagreed decisions.
- **Improvising a missing dependency.** If a required delegate skill is not
  installed, stop and report it; do not hand-roll its work, except for the
  interview (step 3) and the `pr-approve` merge reconciliation (step 2), which
  name explicit fallbacks.

## Verification

- No tracker or documentation file was written before the step-4 checkpoint was
  approved.
- Every milestone was checked before planning: none is `planned`/`active`, and
  no closed milestone carries an unreconciled PR.
- The recorded milestone matches the approved checkpoint: the same goal,
  stories, acceptance criteria, tasks, and `M`/`US`/`T` numbers, with no
  duplicates of existing items.
- The decisions appended to `CONTEXT.md` match what was settled in step 3 —
  nothing more.
- The final summary names the next action — invoke the `implement` skill.

## Reference files

| Topic | Read |
| --- | --- |
| Sizing soft caps, worked example, checkpoint and final-summary formats, reviewer's checklist | `references/sizing-and-examples.md` |
