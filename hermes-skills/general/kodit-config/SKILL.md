---
name: kodit-config
description: >-
  Owns a kodit project's file surface — inspect, validate, and write
  `kodit.json`, `AGENTS.md`, `README.md`, `CONTEXT.md`, and `.kodit/`. Runs six
  modes: check adoption state and resume an interrupted setup, run the
  project-metadata interview, provision tracker resources, write the final
  artifacts from setup drafts, migrate legacy document sections to
  marker-delimited managed blocks, and append the `CONTEXT.md` decisions log.
  Use when adopting or setting up kodit in a project, resuming an interrupted
  kodit setup, checking whether kodit is configured, writing or validating
  `kodit.json`, migrating legacy kodit sections, or recording a decision in
  `CONTEXT.md` — even if the user just says "set up kodit", "is kodit
  initialized?", or "add this decision to the log". Invoked by workflow skills
  and by the user directly.
version: 1.0.0
author: invoque
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [kodit, config, setup, context, decisions, workflow]
    related_skills: [interview, issue-tracker]
---

# kodit-config

Owns `kodit`'s file surface: what exists, what is valid, and how the final
artifacts are written.

## When to Use

- Adopting kodit in a project, or resuming a setup that was interrupted.
- Checking whether a project is already set up (`kodit.json` present) and
  where setup should resume.
- Writing or validating `kodit.json`, `AGENTS.md`, `README.md`, `CONTEXT.md`,
  or `.kodit/`.
- Migrating legacy kodit document sections to marker-delimited managed blocks.
- Appending settled decisions to the `CONTEXT.md` decisions log.
- Not for working a milestone item — use the milestone workflow for that.

## Usage

Invoked in six modes. Follow the `interview` skill for the metadata interview
(load it with `skill_view` when available). Read
`references/kodit-json-schema.md` for the config contract,
`references/rendering-contract.md` for document normalization, and
`references/templates.md` for output templates.

- **Check mode** — inspect adoption state and report where to resume.
- **Metadata mode** — interview for project metadata; write
  `.kodit/tmp/setup-project-metadata.md`.
- **Provision mode** — create or verify tracker resources from the setup
  draft; does not write `kodit.json`.
- **Write mode** — turn the setup drafts into final artifacts; remove the
  drafts.
- **Migrate mode** — detect legacy document sections and replace them with
  marker-delimited managed blocks after approval.
- **Decisions mode** — append settled decisions to the managed `CONTEXT.md`
  decisions log.

## Modes

### Check mode

1. Ensure `.kodit/tmp/` exists: run `mkdir -p .kodit/tmp` with `terminal`.
2. Report, for each of `kodit.json`, `AGENTS.md`, `README.md`, `CONTEXT.md`:
   present or missing, using `read_file` or `terminal`. Report whether the
   directory is a git repository (`git rev-parse --is-inside-work-tree`).
3. List any `.kodit/tmp/setup-*.md` drafts with `terminal`. The first setup
   step with no draft is the resume point; a draft is that step's completed
   output to re-confirm.
4. If `kodit.json` exists, report the project as already set up and stop — do
   not reconfigure without the user asking.

### Metadata mode

1. Read the project for facts first: name, description, language, build and
   test commands — from `README.md`, manifests, and the conversation. Never ask
   for what you can look up.
2. Follow the `interview` skill with topic "project metadata" and the field
   list from `references/templates.md` as context. Use that reference's
   template as the record shape. If the `interview` skill is not installed,
   ask the same questions directly.
3. Write `.kodit/tmp/setup-project-metadata.md` with `write_file` once the
   interview confirms.

### Write mode

1. Read the three drafts with `read_file`: `setup-project-metadata.md`,
   `setup-issue-tracker.md`, `setup-git-branching.md`. If any is missing, stop
   and name it — the caller must finish that step first.
2. Assemble the normalized setup model from all three drafts per
   `references/rendering-contract.md`. Never read values piecemeal per
   document.
3. Write `kodit.json` at the project root with `write_file`, per
   `references/kodit-json-schema.md`.
4. For `AGENTS.md`, `README.md`, and `CONTEXT.md`: classify each per the
   document-state matrix in `rendering-contract.md` (create shell, no-op if
   current, migrate if older, or detect legacy and append). Write or edit with
   `write_file` and `patch`. Never overwrite content outside managed markers.
5. Write `.kodit/.gitignore` containing `tmp`; never ignore `.kodit/issues/`
   for the file backend.
6. Verify `kodit.json` parses (for example
   `python3 -m json.tool kodit.json` with `terminal`) and carries the resolved
   tracker IDs, and that every write succeeded. Only then remove all
   `.kodit/tmp/setup-*.md` drafts; if anything failed, keep them and stop.
7. Report every file written with its action: created, appended, no-op,
   migrated, or legacy-retained.

### Provision mode

Follow `references/provision-mode.md`: read the setup draft, provision tracker
resources via the `issue-tracker` skill (load it with `skill_view`), append
resolved IDs to the draft, and report. If the `issue-tracker` skill is not
installed, stop and report that it is required. Never write `kodit.json` here.

### Migrate mode

1. For each of `AGENTS.md`, `README.md`, `CONTEXT.md`: search with `read_file`
   for legacy fingerprints per `rendering-contract.md` (heading without
   markers).
2. If no legacy found, report `no legacy found` and stop.
3. If legacy found and unmodified from the original template: show a bounded
   before/after diff (for example `diff -u` with `terminal`). Ask for approval
   to replace.
4. If legacy found but user-modified: preserve it; append a new managed block.
   Report `legacy retained, new block added`.
5. On approval, replace the legacy block with the current managed block using
   `patch`. Preserve all content outside the legacy boundaries.

### Decisions mode

1. Take the settled decisions — each a decision plus its rationale. Do not
   invent decisions; record only what was agreed.
2. Read `CONTEXT.md` with `read_file`. If it is missing, create it from the
   template in `references/templates.md`.
3. Find the managed `<!-- kodit:context:v1:start/end -->` block. Locate the
   `### Decisions Log` table inside it. Append one dated row per decision with
   `patch`. Most recent last; never rewrite existing rows.
4. If no managed block exists, create one with the full Context structure,
   then append the decision rows.
5. Confirm the entries with the caller unless they already approved them, then
   report the rows appended.

## Pitfalls

- **Partial writes.** Removing `.kodit/tmp/setup-*.md` drafts before every
  write is verified loses the only copy of the settings. Remove them last, and
  only when all writes succeeded.
- **Piecemeal rendering.** Reading one draft per document produces
  inconsistent artifacts. Always render from the single normalized model.
- **Editing inside markers.** Managed blocks are replace-only; never hand-edit
  content between `<!-- kodit:*:start -->` and `<!-- kodit:*:end -->`.
- **Reconfiguring an adopted project.** `kodit.json` present means setup is
  done — do not rewrite it unless the user asks.
- **Writing `kodit.json` in provision mode.** Provisioning happens before the
  config exists; the draft is the source of truth until write mode.
- **Rewriting user content.** Preserve content outside managed blocks,
  including user-modified legacy sections.

## Verification

- `kodit.json` parses and contains the resolved tracker IDs.
- Each managed document contains exactly one
  `<!-- kodit:<doc>:v1:start -->` / `end` pair, with no unresolved `{{...}}`
  placeholders.
- The file plan reports an action per file: created, appended, no-op, migrated,
  or legacy-retained.
- `.kodit/tmp/setup-*.md` drafts are removed only after every write succeeded;
  on any failure they remain and the run stops.
- `.kodit/.gitignore` ignores `tmp` and does not ignore `.kodit/issues/` on the
  file backend.

## Reference files

| Topic | Read |
| --- | --- |
| `kodit.json` schema, both backends | `references/kodit-json-schema.md` |
| Normalized setup model, markers, document-state matrix, legacy detection | `references/rendering-contract.md` |
| Output templates for metadata and write modes | `references/templates.md` |
| Tracker provisioning steps | `references/provision-mode.md` |
