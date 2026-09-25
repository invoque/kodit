# Story summary and handoff

The format for the story summary `implement` presents when a story's tasks are
all `review`/`done`/`wontfix`, the note used when the milestone has no
eligible story left, and the handoff rules that follow. The summary ends the
run.

## Story summary format

```markdown
# US-NNN — <story title>: implementation complete

**Branch:** `<feature_prefix>m-NNN-<slug>` (from `<dev_branch>`)
**Tasks:** M (P review, Q done, S skipped or blocked)

## Tasks and commits

| Task | Status | RED commit (`test:`) | GREEN commit (`feat:`/`fix:`) |
|---|---|---|---|
| T-001 <task title> | review | `abc1234` | `def5678` |
| T-002 <task title> | review | `90abcde` | `1234567` |

## RED failure evidence

- <Per task, one line: the failing check and its observed failure, then the
  command that now passes.>

## Artifacts

- Spec: `spec-US-NNN-<slug>.md`
- Plans: `plan-T-001-<slug>.md`, `plan-T-002-<slug>.md`

## Skipped or blocked

- <Task and why (blocked, ready-for-human, needs-info, needs-triage,
  wontfix), or "none".>

## Decisions surfaced

- <Anything the run decided that should be recorded, or "none".>

## Next

- If stories remain in the milestone: re-invoke `implement` to work the next
  story.
- If the milestone is exhausted: run the **`pr-request`** skill for
  `<feature_prefix>m-NNN-<slug>` into `<dev_branch>`.
```

Keep the table truthful to the tracker: read the story files after the last
commit and report what they say, not what was intended. Rows for skipped items
stay visible with their real status.

## Milestone-exhausted note

When no story is eligible, present a short completion note instead of a story
summary: the branch, story and task counts (`review`/`done`/`wontfix`), the
artifacts, the skipped or blocked items, and the `Next` block above naming
`pr-request`.

## Handoff rules

- Stop after presenting the summary. State the next step — re-invoke
  `implement` when stories remain, run `pr-request` when the milestone is
  exhausted. Never ask whether to continue the run, and never create a pull
  request yourself.
- Name the `pr-request` skill by name; do not use slash commands, and do not
  imply the skill already exists — it is a later stage.
- Do not merge, tag, or push a protected branch. The pull-request flow and the
  review that follows own those steps.
- Write nothing to the issue tracker here beyond what the `issue-tracker` skill
  already applied during the implementation steps.
- If any task is unfinished because it was skipped or blocked, say so plainly
  and do not claim the milestone is complete; report what remains.
