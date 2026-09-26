# Pull request title and body

Reusable shape for PRs opened by the `github-pr` skill. The caller supplies the
values; this reference defines the order and headings only.

## Title

`M-NNN — <milestone goal>`

## Body

```markdown
# M-NNN — <milestone goal>

**Head:** `<head>` into **Base:** `<base>`

## Stories and tasks

| Story | Task | Status |
|---|---|---|
| US-001 <title> | T-001 <task> | review |
| US-001 <title> | T-002 <task> | done |

## Verification

- <Per task, one line: the check that now passes and where it ran.>

## Review notes

- <Skipped or blocked items, known limits, or "none".>

## Tracker

- Milestone charter records `**PR:** <url>` after creation; statuses unchanged.
```

A caller outside the kodit workflow supplies its own title and headings; only
the `write_file` → `--body-file` mechanism is fixed.
