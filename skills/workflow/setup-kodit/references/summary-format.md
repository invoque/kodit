# Summary format

Two presentations: the step-5 checkpoint (for review before writing) and the
step-7 final summary (for handoff). Use these structures as guides; adapt the
example values to the actual project data.

## Checkpoint (step 5)

Present in this order: the three tables, the configuration preview, rendered
document previews, the file plan with per-file actions, and any migration diffs.
Then one line asking for approval, and note that any change request returns to
its owning step.

```markdown
## Setup review -- nothing written yet

### Project metadata
| Field | Value |
|---|---|
| Name | TaskFolio |
| Description | Personal task tracking with weekly reviews. |
| Language | python |
| Build | python -m build |
| Test | pytest |

### Issue tracking

The table adapts to the selected backend.

**File backend:**

| Field | Value |
|---|---|
| Backend | file-based |
| Path | .kodit/issues |
| Labels | ready-for-agent, ready-for-human, needs-info, needs-triage, wontfix |

**Linear backend:**

| Field | Value |
|---|---|
| Backend | linear |
| Team | ENG |
| Project | taskflow |
| Labels | ready-for-agent, ready-for-human, needs-info, needs-triage, wontfix |
| States required | In Progress, In Review, Done, Todo |

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

### Document previews

**AGENTS.md** (action: create)
```markdown
<!-- kodit:agents:v1:start -->
## kodit Workflow
...the rendered managed block...
<!-- kodit:agents:v1:end -->
```

**README.md** (action: append)
```markdown
<!-- kodit:readme:v1:start -->
## kodit Development Workflow
...the rendered managed block...
<!-- kodit:readme:v1:end -->
```

**CONTEXT.md** (action: create)
```markdown
<!-- kodit:context:v1:start -->
## kodit Context
...the rendered managed block...
<!-- kodit:context:v1:end -->
```

### Files
| File | Action |
|---|---|
| kodit.json | create |
| AGENTS.md | create (managed block) |
| README.md | append (managed block) |
| CONTEXT.md | create (managed block) |
| .kodit/.gitignore | create |
| .kodit/issues/README.md | create *(file backend only)* |
| .kodit/issues/INDEX.md | create *(file backend only)* |
| Linear project | create/verify *(Linear backend only)* |
| Linear workflow states | create/verify *(Linear backend only)* |
| Linear labels | create/verify *(Linear backend only)* |

Approve this, or tell me what to change -- changes go back to the step that owns
them and come back here for another look.
```

### Action labels

Use exactly these labels in the file plan:

| Label | Meaning |
|---|---|
| **create** | File does not exist; write shell plus managed block. |
| **append** | File exists without a managed block; add managed block at end. |
| **no-op** | File exists with current managed block; nothing to do. |
| **migrate** | Legacy section detected; replace with managed block after approval. |
| **legacy-retained** | User-modified legacy preserved; new managed block appended. |

### Migration diffs

If any file has a legacy section, show a bounded before/after diff in the
checkpoint:

```markdown
### Migration: AGENTS.md

**Legacy section found** (lines 45-72):
```diff
- ## kodit Workflow
- This project uses `kodit`...
+ <!-- kodit:agents:v1:start -->
+ ## kodit Workflow
+ ...current managed block...
+ <!-- kodit:agents:v1:end -->
```

Replace legacy section? (y/n)
```

If a step was skipped (non-git project), show it as skipped with the reason
rather than omitting it.

## Final summary (step 7)

```markdown
## setup complete

- **kodit.json** written at the project root.
- **Docs:** AGENTS.md created (managed block), README.md appended (managed
  block), CONTEXT.md created (managed block).
- **Issues:** [backend-specific line].
- **Git:** main `master`, dev `dev`, work on `feature/*` and `bugfix/*`.
  [Or: "No version control configured." if git is null]
- **Skipped:** <any step skipped, with its reason -- omit this line if none>

Next: invoke the **milestone-planning** skill to agree the first milestone.
```

### Backend-specific summary lines

When `tracker.type` is `file`:

```
- **Issues:** file-based tracker seeded at .kodit/issues/ -- see
  .kodit/issues/README.md for the conventions.
```

When `tracker.type` is `linear`:

```
- **Issues:** Linear at project `<linear_project>` (team `<team>`) -- see
  issue-tracker `references/linear.md` for the conventions.
```
