# Output templates

Templates for `kodit-config` in metadata and write modes. Fill placeholders from
the setup drafts; keep section headings verbatim so appends are idempotent.

## Project metadata fields (metadata mode)

Settle these with `interview`; write the result to
`.kodit/tmp/setup-project-metadata.md` in this shape:

```markdown
# setup — project metadata

- **Name:** <project name>
- **Description:** <one line>
- **Language:** <primary language, or none>
- **Build:** <build command, or none>
- **Test:** <test command, or none>
```

## `AGENTS.md` append section

Append verbatim, substituting the configured values. Written for the adopting
project's coding agent, not for `kodit`'s own repository.

```markdown
## kodit Workflow

This project uses `kodit`. Read `CONTEXT.md` first — it is the source of truth.
Configuration is in `kodit.json`.

Phases, in order: setup → milestone-planning → implement-loop → review-loop →
milestone-review → done. Never implement an item without an approved spec and
plan. Inside `implement-loop` and `review-loop`, each user story runs
spec → plan → implement → review; each task runs the full status machine below.

**Artifacts:** specs (`spec-US-NNN-*.md`) attach to user stories and plans
(`plan-T-NNN-*.md`) attach to tasks, both in `.kodit/tmp/specs/`. They are local
working artifacts, never committed.

**Issues:** file-based under `.kodit/issues/`. Taxonomy is
PROJECT → MILESTONE → USER STORY → TASK, numbered `M-001`, `US-001`, `T-001`
globally. Tasks are rows inside the story file: tasks run
`open → spec → plan → implement → review → done`, stories run
`open → in-progress → done`, milestones run `planned → active → closed`.
Labels are handoff signals: `ready-for-agent`, `ready-for-human`, `needs-info`,
`needs-triage`, `wontfix`. The full conventions live in
`.kodit/issues/README.md`.

**Branches:** `{{git.main_branch}}` (stable), `{{git.dev_branch}}`
(integration), `{{git.feature_prefix}}*`, `{{git.bugfix_prefix}}*`. Work on a
feature branch, merge to `{{git.dev_branch}}` after review; never commit
directly to a protected branch.

Record significant decisions in `CONTEXT.md` in the same change. Use
conventional commit messages.
```

If `git` is `null`, replace the Branches paragraph with: "Version control is not
configured for this project."

## `README.md` append section

```markdown
## Development Workflow

This project follows the [`kodit`](https://github.com/) milestone workflow:
`setup → milestone-planning → implement-loop → review-loop → milestone-review →
done`. Project context and decisions live in `CONTEXT.md`; agent instructions in
`AGENTS.md`; configuration in `kodit.json`.

Track work as milestones → user stories → tasks under `.kodit/issues/`
(conventions in `.kodit/issues/README.md`). Work happens on
`{{git.feature_prefix}}*` branches merged into `{{git.dev_branch}}`.
```

## `CONTEXT.md` create / append section

When creating, write the header plus the section. When appending, add only the
section (headings are the idempotency key).

```markdown
# CONTEXT

Source of truth for this project: purpose, environment, and decisions.

## Project

- **Name:** {{project.name}}
- **Description:** {{project.description}}
- **Language:** {{project.language}}

## Environment

- **Build:** {{project.build}}
- **Test:** {{project.test}}
- **Branches:** {{git.main_branch}} / {{git.dev_branch}} / {{git.feature_prefix}} / {{git.bugfix_prefix}}
- **Issue tracking:** {{issue_tracker.type}} at `{{issue_tracker.path}}`

## Decisions Log

| Date | Decision | Rationale |
|---|---|---|
| {{date}} | Adopt `kodit` with file-based issue tracking | Track milestones, stories, and tasks as committed markdown. |
| {{date}} | Branch model {{git.main_branch}} / {{git.dev_branch}} / {{git.feature_prefix}} / {{git.bugfix_prefix}} | {{branch_rationale}} |
```

## Decisions log entry (decisions mode)

Append rows to the `## Decisions Log` table in `CONTEXT.md`. One row per
settled decision, most recent last; never rewrite existing rows. If the section
or table is missing, create it using the header from the create/append section
above.

```markdown
| {{date}} | {{decision}} | {{rationale}} |
```

## `.kodit/.gitignore`

```text
tmp
```
