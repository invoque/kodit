---
name: milestone-planning
description: >-
  Use when the user wants to plan the next milestone — "let's plan a milestone",
  "scope the next chunk of work", "define the next set of stories" — or when
  setup-kodit hands off after setup. Interviews the user to a shared scope, then
  records the milestone, its stories, acceptance criteria, and tasks in the
  issue tracker. Refuses when a milestone is still open or setup is incomplete.
  Defines only the sequence and the review gate.
---

# milestone-planning

The milestone-planning phase: agree the next milestone's scope and record it.

## Usage

Invoke when setup is complete and a new milestone's worth of work exists, or
when a milestone-planning run was interrupted. It delegates all work to general
skills and never writes tracker or documentation files itself. Read
`references/sizing-and-examples.md` before settling scope or presenting the
checkpoint.

## What You Must Do When Invoked

### 1. Verify entry

Follow the `kodit-config` skill in **check mode**. If `kodit.json` is missing,
the project is not set up: say so and stop, directing the user to the
`setup-kodit` skill.

### 2. Check the milestone state

Follow the `issue-tracker` skill in **operate mode** to read the project charter
and every milestone, deriving each milestone's status. If any milestone is not
`closed` (`planned` or `active`), refuse: name it, and direct the user to
implement it (the `implement` skill), close it, or explicitly re-scope it
first. Do not plan a second milestone. Stop.

### 3. Settle the scope

Gather context: the project charter from `.kodit/issues/INDEX.md`, any closed
milestones, the next global `M`/`US`/`T` numbers from the tracker, and the
sizing guidance in `references/sizing-and-examples.md`. Then follow the
`interview` skill with topic "milestone scope" and that context. Steer toward
milestone-sized chunks using the soft caps. If
`.kodit/tmp/design-tree-milestone-scope.md` exists, resume from it instead of
re-asking settled decisions.

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
directory `M-NNN-goal-name/` with its `INDEX.md` charter (`status: planned`),
the story files `US-NNN-name.md` (frontmatter, Story, Acceptance Criteria, and
embedded Tasks table at `status: open`), and the new row in the project
`INDEX.md`. Re-read the tracker first; never duplicate an existing milestone or
story.

### 6. Record decisions

Follow the `kodit-config` skill in **decisions mode** to append the
milestone-shaping decisions settled in step 3 to the `CONTEXT.md` decisions
log. Record only what was agreed.

### 7. Hand off

Present the final summary: the milestone and its stories, the numbers allocated,
the decisions recorded, and the next action — run the `implement` skill to
start implementation. Offer to commit the new tracker files if the project's
conventions expect it.
