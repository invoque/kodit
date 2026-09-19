---
name: kodit-config
description: >-
  Use when a workflow skill needs to inspect, validate, or write a project's
  kodit files — kodit.json, AGENTS.md, README.md, CONTEXT.md, and .kodit/.
  Provides the kodit.json schema, checks adoption state and resumes an
  interrupted setup, runs the project-metadata interview, and writes the final
  artifacts from the setup drafts. Invoked by the setup-kodit workflow skill;
  the schema is the single source of truth for every other kodit skill.
---

# kodit-config

Owns `kodit`'s file surface: what exists, what is valid, and how the final
artifacts are written.

## Usage

Invoked as three modes. Follow `skills/general/interview/SKILL.md` for the
metadata interview. Read `references/kodit-json-schema.md` for the config
contract and `references/templates.md` for output templates.

- **Check mode** — inspect adoption state and report where to resume.
- **Metadata mode** — interview for project metadata; write
  `.kodit/tmp/setup-project-metadata.md`.
- **Write mode** — turn the setup drafts into final artifacts; remove the
  drafts.

## What You Must Do When Invoked

### Check mode

1. Ensure `.kodit/tmp/` exists (create it if missing).
2. Report, for each of `kodit.json`, `AGENTS.md`, `README.md`, `CONTEXT.md`:
   present or missing. Report whether the directory is a git repository.
3. List any `.kodit/tmp/setup-*.md` drafts. The first setup step with no draft
   is the resume point; a draft is that step's completed output to re-confirm.
4. If `kodit.json` exists, report the project as already set up and stop —
   do not reconfigure without the user asking. Return the report to the caller.

### Metadata mode

1. Read the project for facts first: name, description, language, build and
   test commands — from `README.md`, manifests, and the conversation. Never ask
   for what you can look up.
2. Follow `skills/general/interview/SKILL.md` with topic "project metadata" and
   the field list from `references/templates.md` as context. Use that
   reference's template as the record shape.
3. Write `.kodit/tmp/setup-project-metadata.md` once the interview confirms.

### Write mode

1. Read the three drafts: `setup-project-metadata.md`,
   `setup-issue-tracker.md`, `setup-git-branching.md`. If any is missing, stop
   and name it — the caller must finish that step first.
2. Write `kodit.json` at the project root per
   `references/kodit-json-schema.md`.
3. For `AGENTS.md`, `README.md`, and `CONTEXT.md`: if missing, write from
   `references/templates.md`; if present, **append** a kodit section — never
   overwrite or remove existing content. Use the templates' section headings so
   the append is idempotent.
4. Write `.kodit/.gitignore` containing `tmp`. Never ignore `.kodit/issues/`.
5. Remove the three `setup-*.md` drafts.
6. Report every file written and whether it was created or appended.
