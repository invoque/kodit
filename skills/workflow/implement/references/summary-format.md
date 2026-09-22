# Milestone summary and handoff

The format for the final summary `implement` presents when every task in the
milestone is `review`/`done`/`wontfix`, and the handoff to the next phase.

## Summary format

```markdown
# M-NNN — <milestone goal>: implementation complete

**Branch:** `<feature_prefix>m-NNN-<slug>` (from `<dev_branch>`)
**Stories:** N (X done, Y in progress)  ·  **Tasks:** M (P review, Q done)

## Stories and tasks

| Story | Task | Status | Commit |
|---|---|---|---|
| US-001 <title> | T-001 <task title> | review | `abc1234` |
| US-001 <title> | T-002 <task title> | review | `def5678` |
| US-002 <title> | T-003 <task title> | done | `90abcde` |

## Artifacts

- Specs: `spec-US-001-<slug>.md`, `spec-US-002-<slug>.md`
- Plans: `plan-T-001-<slug>.md`, `plan-T-002-<slug>.md`, `plan-T-003-<slug>.md`

## Test-first evidence

- <Per task, one line: the failing test/check that was seen to fail, and the
  command that now passes. For the no-test escape hatch, name the substitute.>

## Skipped or blocked

- <Story/task and why (blocked, ready-for-human, needs-info, needs-triage,
  wontfix), or "none".>

## Decisions surfaced

- <Anything the run decided that should be recorded, or "none".>

## Next

All milestone work is implemented and committed on the branch. Ask whether to
open the pull request now; on yes, tell the user to run the **`pr-request`**
skill to open a pull request for `<feature_prefix>m-NNN-<slug>` into
`<dev_branch>`. Do not merge until the pull request is reviewed.
```

Keep the table truthful to the tracker: read the story files after the last
commit and report what they say, not what was intended. Rows for skipped items
stay visible in the table with their real status.

## Handoff rules

- Name the `pr-request` skill by name; do not use slash commands, and do not
  imply the skill already exists — it is a later stage.
- Ask before handing off. The summary is a checkpoint, not a stop: ask whether to
  open the pull request now, and only then name `pr-request`.
- Do not merge, tag, or push a protected branch. The pull-request flow and the
  review that follows own those steps.
- Write nothing to the issue tracker here beyond what the `issue-tracker` skill
  already applied during the implementation steps.
- If any task is unfinished because it was skipped or blocked, say so plainly and
  do not claim the milestone is complete; report what remains.
