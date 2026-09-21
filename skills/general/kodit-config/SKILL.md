---
name: kodit-config
description: >-
  Use when a workflow skill needs to inspect, validate, or write a project's
  kodit files -- kodit.json, AGENTS.md, README.md, CONTEXT.md, and .kodit/.
  Provides the kodit.json schema, checks adoption state and resumes an
  interrupted setup, runs the project-metadata interview, writes the final
  artifacts from the setup drafts, migrates legacy document sections to
  marker-delimited blocks, and appends entries to the CONTEXT.md decisions log.
  Invoked by the setup-kodit and milestone-planning workflow skills; the schema
  is the single source of truth for every other kodit skill.
---

# kodit-config

Owns `kodit`'s file surface: what exists, what is valid, and how the final
artifacts are written.

## Usage

Invoked as six modes. Follow the `interview` skill for the metadata
interview. Read `references/kodit-json-schema.md` for the config contract,
`references/rendering-contract.md` for document normalization, and
`references/templates.md` for output templates.

- **Check mode** -- inspect adoption state and report where to resume.
- **Metadata mode** -- interview for project metadata; write
  `.kodit/tmp/setup-project-metadata.md`.
- **Provision mode** -- after checkpoint approval, create or verify tracker
  resources (file seed files or Linear project/states/labels) and write
  `kodit.json`.
- **Write mode** -- turn the setup drafts into final artifacts; remove the
  drafts.
- **Migrate mode** -- detect legacy document sections and replace them with
  marker-delimited managed blocks after approval.
- **Decisions mode** -- append settled decisions to the managed
  `CONTEXT.md` decisions log.

## What You Must Do When Invoked

### Check mode

1. Ensure `.kodit/tmp/` exists (create it if missing).
2. Report, for each of `kodit.json`, `AGENTS.md`, `README.md`, `CONTEXT.md`:
   present or missing. Report whether the directory is a git repository.
3. List any `.kodit/tmp/setup-*.md` drafts. The first setup step with no draft
   is the resume point; a draft is that step's completed output to re-confirm.
4. If `kodit.json` exists, report the project as already set up and stop --
   do not reconfigure without the user asking. Return the report to the caller.

### Metadata mode

1. Read the project for facts first: name, description, language, build and
   test commands -- from `README.md`, manifests, and the conversation. Never ask
   for what you can look up.
2. Follow the `interview` skill with topic "project metadata" and
   the field list from `references/templates.md` as context. Use that
   reference's template as the record shape.
3. Write `.kodit/tmp/setup-project-metadata.md` once the interview confirms.

### Write mode

1. Read the three drafts: `setup-project-metadata.md`,
   `setup-issue-tracker.md`, `setup-git-branching.md`. If any is missing, stop
   and name it -- the caller must finish that step first.
2. Assemble the normalized setup model from all three drafts per
   `references/rendering-contract.md`. Never read values piecemeal per document.
3. Write `kodit.json` at the project root per
   `references/kodit-json-schema.md`.
4. For `AGENTS.md`, `README.md`, and `CONTEXT.md`: classify each file per the
   document-state matrix in `rendering-contract.md`. For missing files, create
   the shell plus managed block. For existing files with a managed block, no-op
   if current, or migrate if older. For existing files without a managed block,
   detect legacy or append. Never overwrite content outside managed markers.
5. Write `.kodit/.gitignore` containing `tmp`. Never ignore `.kodit/issues/`
   when the backend is file-based.
6. Remove all `.kodit/tmp/setup-*.md` drafts.
7. Report every file written with its action: created, appended, no-op, migrated,
   or legacy-retained.

### Provision mode

1. Read the setup draft `setup-issue-tracker.md` and the written `kodit.json`.
   If either is missing, stop and name it.
2. Follow the `issue-tracker` skill in **provision mode** to create or verify
   tracker resources. For file-based: seed `.kodit/issues/`. For Linear: create
   or find the project, ensure states and labels exist.
3. If provisioning succeeds and the backend is Linear, update `kodit.json` with
   any discovered IDs (e.g. the resolved Linear project ID).
4. Report what was created or verified.

### Migrate mode

1. For each of `AGENTS.md`, `README.md`, `CONTEXT.md`: search for legacy
   fingerprints per `rendering-contract.md` (heading without markers).
2. If no legacy found, report `no legacy found` and stop.
3. If legacy found and unmodified from the original template: show a bounded
   before/after diff. Ask for approval to replace.
4. If legacy found but user-modified: preserve it; append a new managed block.
   Report `legacy retained, new block added`.
5. On approval, replace the legacy block with the current managed block. Preserve
   all content outside the legacy boundaries.

### Decisions mode

1. Take the settled decisions -- each a decision plus its rationale. Do not
   invent decisions; record only what was agreed.
2. Read `CONTEXT.md`. If it is missing, create it from the template in
   `references/templates.md`.
3. Find the managed `<!-- kodit:context:v1:start/end -->` block. Locate the
   `### Decisions Log` table inside it. Append one dated row per decision.
   Most recent last; never rewrite existing rows.
4. If no managed block exists, create one with the full Context structure and
   append the decision rows.
5. Confirm the entries with the caller before writing when the caller did not
   already present them for approval.
6. Report the rows appended.
