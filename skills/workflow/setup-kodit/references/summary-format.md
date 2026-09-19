# Summary format

Two presentations: the step-5 checkpoint (for review before writing) and the
step-7 final summary (for handoff). Use these exact structures.

## Checkpoint (step 5)

Present in this order: the three tables, the configuration preview, and the
file plan. Then one line asking for approval, and note that any change request
returns to its owning step.

```markdown
## Setup review — nothing written yet

### Project metadata
| Field | Value |
|---|---|
| Name | TaskFolio |
| Description | Personal task tracking with weekly reviews. |
| Language | python |
| Build | python -m build |
| Test | pytest |

### Issue tracking
| Field | Value |
|---|---|
| Backend | file-based |
| Path | .kodit/issues |
| Labels | ready-for-agent, ready-for-human, needs-info, needs-triage, wontfix |

### Git branching
| Field | Value |
|---|---|
| Repository | yes |
| Main / Dev | master / dev |
| Feature / Bugfix | feature/ / bugfix/ |
| Staging | none |
| Remote | none |

### kodit.json preview
```json
<the exact JSON that will be written>
```

### Files
| File | Action |
|---|---|
| kodit.json | create |
| CONTEXT.md | create |
| AGENTS.md | create |
| README.md | append "## Development Workflow" |
| .kodit/.gitignore | create |
| .kodit/issues/README.md | create |
| .kodit/issues/INDEX.md | create |

Approve this, or tell me what to change — changes go back to the step that owns
them and come back here for another look.
```

The file plan must mark each file create or append, naming the section for an
append. If a step was skipped (non-git project), show it as skipped with the
reason rather than omitting it.

## Final summary (step 7)

```markdown
## setup complete

- **kodit.json** written at the project root.
- **Docs:** CONTEXT.md created, AGENTS.md created, README.md appended
  "## Development Workflow".
- **Issues:** file-based tracker seeded at .kodit/issues/ — see
  .kodit/issues/README.md for the conventions.
- **Git:** main `master`, dev `dev`, work on `feature/*` and `bugfix/*`.
- **Skipped:** <any step skipped, with its reason — omit this line if none>

Next: invoke the **milestone-planning** skill to agree the first milestone.
```
