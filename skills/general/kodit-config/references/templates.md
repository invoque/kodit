# Output templates

Templates for `kodit-config` in metadata and write modes. Fill placeholders from
the normalized setup model (see `rendering-contract.md`). All managed blocks use
versioned markers for idempotency.

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

## `AGENTS.md` managed block

Bounded by `<!-- kodit:agents:v1:start -->` and `<!-- kodit:agents:v1:end -->`.
Written for the adopting project's coding agent, not for `kodit`'s own
repository.

```markdown
<!-- kodit:agents:v1:start -->

## kodit Workflow

This project uses `kodit`. Read `CONTEXT.md` first -- it is the source of truth.
Configuration is in `kodit.json`.

Phases, in order: setup -> milestone-planning -> implement -> review-loop ->
milestone-review -> done. Never implement an item without an approved spec and
plan. Inside `implement` and `review-loop`, each user story runs
spec -> plan -> implement -> review; each task runs the full status machine
below.

**Artifacts:** specs (`spec-US-NNN-*.md`) attach to user stories and plans
(`plan-T-NNN-*.md`) attach to tasks, both in `.kodit/tmp/specs/`. They are
local working artifacts, never committed.

**Issues:** [render backend line]. Taxonomy is
PROJECT -> MILESTONE -> USER STORY -> TASK, numbered `M-001`, `US-001`, `T-001`
globally. Tasks run
`open -> spec -> plan -> implement -> review -> done`, stories run
`open -> in-progress -> done`, milestones run `planned -> active -> closed`.
Labels are handoff signals: [render from configured labels]. [render
conventions pointer].

**Branches:** [render from git model, or "Version control is not configured for
this project."]

Record significant decisions in `CONTEXT.md` in the same change. Use
conventional commit messages.

<!-- kodit:agents:v1:end -->
```

### Backend line rendering (AGENTS.md)

When `tracker.type` is `file`, render:

```
file-based under `.kodit/issues/`
```

When `tracker.type` is `linear`, render:

```
Linear at project `{{tracker.linear_project.name}}` (team `{{tracker.team.key}}`)
```

### Conventions pointer rendering (AGENTS.md)

When `tracker.type` is `file`, render:

```
The full conventions live in `.kodit/issues/README.md`.
```

When `tracker.type` is `linear`, render:

```
The full conventions live in the issue-tracker skill's `references/linear.md`.
```

### Branch rendering (AGENTS.md)

When `git` is configured, render:

```
`{{git.main_branch}}` (stable), `{{git.dev_branch}}` (integration),
`{{git.feature_prefix}}*`, `{{git.bugfix_prefix}}*`. Work on a feature branch,
merge to `{{git.dev_branch}}` after review; never commit directly to a protected
branch.
```

When `git` is `null`, render:

```
Version control is not configured for this project.
```

### Label rendering

Render labels from the configured `tracker.labels` list. The default set is:
`ready-for-agent`, `ready-for-human`, `needs-info`, `needs-triage`, `wontfix`.
Projects may extend this list; always render the actual configured values.

## `README.md` managed block

Bounded by `<!-- kodit:readme:v1:start -->` and `<!-- kodit:readme:v1:end -->`.

```markdown
<!-- kodit:readme:v1:start -->

## kodit Development Workflow

{{project.description}}

This project follows the kodit milestone workflow:
setup -> milestone-planning -> implement -> review-loop -> milestone-review ->
done. Project context and decisions live in `CONTEXT.md`; agent instructions in
`AGENTS.md`; configuration in `kodit.json`.

Track work as milestones -> user stories -> tasks [render tracker location].
[Branch sentence when Git is configured; omitted when `git` is `null`.]

<!-- kodit:readme:v1:end -->
```

### Tracker location rendering (README.md)

When `tracker.type` is `file`, render:

```
under `.kodit/issues/` (conventions in `.kodit/issues/README.md`)
```

When `tracker.type` is `linear`, render:

```
in Linear at project `{{tracker.linear_project.name}}` (team `{{tracker.team.key}}`)
```

### Branch rendering (README.md)

When `git` is configured, append after the tracker sentence:

```
Work happens on `{{git.feature_prefix}}*` branches merged into
`{{git.dev_branch}}`.
```

When `git` is `null`, omit the branch sentence entirely.

## `CONTEXT.md` managed block

Bounded by `<!-- kodit:context:v1:start -->` and `<!-- kodit:context:v1:end -->`.
When creating a new `CONTEXT.md`, write the file header plus the managed block.
When appending to an existing file, add only the managed block.

```markdown
<!-- kodit:context:v1:start -->

## kodit Context

### Project

- **Name:** {{project.name}}
- **Description:** {{project.description}}
- **Language:** {{project.language}}

### Environment

- **Build:** {{project.build}}
- **Test:** {{project.test}}
- **Branches:** [render from git model, or "Not configured"]
- **Issue tracking:** [render tracking line]

### Decisions Log

| Date | Decision | Rationale |
|---|---|---|
| {{date}} | Adopt `kodit` with [backend] issue tracking | [rationale]. |
[Second row only when Git is configured:]

| {{date}} | Branch model {{git.main_branch}} / {{git.dev_branch}} / {{git.feature_prefix}} / {{git.bugfix_prefix}} | Adapted to existing repository branches. |

<!-- kodit:context:v1:end -->
```

### Tracking line rendering (CONTEXT.md)

When `tracker.type` is `file`, render:

```
file at `.kodit/issues`
```

When `tracker.type` is `linear`, render:

```
Linear at project `{{tracker.linear_project.name}}` (team `{{tracker.team.key}}`)
```

### Adoption decision rendering (CONTEXT.md)

When `tracker.type` is `file`, the first decision row renders as:

```
| {{date}} | Adopt `kodit` with file-based issue tracking | Track milestones, stories, and tasks as committed markdown. |
```

When `tracker.type` is `linear`, render:

```
| {{date}} | Adopt `kodit` with Linear issue tracking | Track milestones, stories, and tasks in Linear. |
```

### Date format

All dates use `YYYY-MM-DD` (ISO 8601).

### Branch rendering (CONTEXT.md)

When `git` is configured, render the Branches line as:

```
{{git.main_branch}} / {{git.dev_branch}} / {{git.feature_prefix}} / {{git.bugfix_prefix}}
```

When `git` is `null`, render:

```
Not configured
```

And omit the second decision row (branch model).

## Decisions log entry (decisions mode)

Append rows to the `### Decisions Log` table inside the managed
`<!-- kodit:context:v1:start/end -->` block. One row per settled decision, most
recent last; never rewrite existing rows. If the managed block or table is
missing, create them per the Context template above.

```markdown
| {{date}} | {{decision}} | {{rationale}} |
```

## `.kodit/.gitignore`

```text
tmp
```
