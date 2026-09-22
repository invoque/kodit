# setup-kodit

Initialize `kodit` in a project, one reviewable step at a time.

## When to Use

- Adopting `kodit` in a new project.
- Resuming an interrupted setup (`.kodit/tmp/setup-*.md` drafts exist).

## Prerequisites

- `kodit.json` must **not** exist in the project root. If it does, the skill stops and shows the completed state.

## How It Works

### 1. Check the project

Follow `kodit-config` in **check mode**. If `kodit.json` exists, present the completed state and stop. Otherwise, find the first step with no draft and resume from there. Drafts already present are re-confirmed, not re-asked.

### 2. Settle project metadata

If `.kodit/tmp/setup-project-metadata.md` is missing, follow `kodit-config` in **metadata mode** (runs the `interview`). Otherwise re-confirm the draft.

### 3. Settle issue tracking

If `.kodit/tmp/setup-issue-tracker.md` is missing, follow `issue-tracker` in **setup mode**. Otherwise re-confirm the draft. Supports file-based and Linear backends.

### 4. Settle git branching

If `.kodit/tmp/setup-git-branching.md` is missing, follow `git-branching`. Otherwise re-confirm the draft.

### 5. Checkpoint — STOP

Present the review summary: per-section tables from the three drafts, the exact `kodit.json` that will be written, rendered previews of each document's managed block, and a file plan with per-file actions (create, append, no-op, migrate, or legacy-retained). For Linear, show planned remote resources in the issue tracking section. If legacy sections are detected, show their bounded diff. **Nothing is written until you approve.** Change requests route back to the step that owns them; the checkpoint re-presents after each fix.

### 6. Provision and write the configuration

Follow `kodit-config` in **provision mode** to create or verify tracker resources (file seed or Linear project/states/labels). Then follow **write mode** to:
- Write `kodit.json` at the project root.
- Render managed blocks into `AGENTS.md`, `README.md`, and `CONTEXT.md` (creating shells, appending, or migrating per the document-state matrix).
- Create `.kodit/.gitignore`.
- Delete all `.kodit/tmp/setup-*.md` drafts.

Each file is reported with its action: created, appended, no-op, migrated, or legacy-retained.

### 7. Hand off

Present the final summary — what was written, the branch/issue configuration, and the next action: invoke `milestone-planning` to agree the first milestone.

## User Decisions

| Step | Decision |
|---|---|
| 2 | Project name, description, language, build/test commands |
| 3 | Issue tracker backend (file-based or Linear) |
| 4 | Main/dev/feature/bugfix branch names, staging branch, remote |
| 5 | Approval of the full checkpoint before any write |

## Artifacts Created

- `kodit.json` -- project configuration
- Marker-delimited managed blocks in `AGENTS.md`, `README.md`, `CONTEXT.md`
- `.kodit/.gitignore` -- excludes `tmp/` from version control
- File backend: `.kodit/issues/README.md` and `.kodit/issues/INDEX.md` (issue tracker seed)
- Linear backend: project, workflow states, and labels in Linear

## Handoff

**Next skill:** `milestone-planning`

## Source

- Canonical definition: `skills/workflow/setup-kodit/SKILL.md`
- Checkpoint and summary templates: `skills/workflow/setup-kodit/references/summary-format.md`
