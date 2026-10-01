# Review report format

Shape for the local review record written by `pr-review` at
`.kodit/tmp/specs/review-M-NNN-<slug>.md`.

## Required sections

- Milestone
- PR
- Verdict
- Findings
- Recommended task transitions
- Next action

## Example skeleton

```markdown
# Review M-NNN — <milestone goal>

**PR:** <url>
**Verdict:** <change_request | pass>
**Blockers:** <n>
**Majors:** <n>

## Findings

| Story | Task | Severity | Requirement | Evidence | Fix |
|---|---|---|---|---|---|
| US-001 | T-001 | blocker | AC-1 | path/to/file | how to resolve |

## Recommended transitions

- T-001: review → implement

## Next action

Run **implement** to resolve the blockers above.
```
