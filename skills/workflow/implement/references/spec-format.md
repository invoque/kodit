# Spec format and story plan links

How `implement` generates a story spec when one is missing, and how plans are
recorded back into the story's task record. Specs are untracked working
artifacts under `.kodit/tmp/specs/`; they attach to a user story.

## Spec template

Mirror the shape the repository already uses, trimmed to a milestone item:

```markdown
# spec-US-NNN — <story title>

**Story:** US-NNN — <story title>
**Status:** draft
**Date:** YYYY-MM-DD
**Milestone item:** M-NNN — <milestone goal>

## Summary

<One paragraph: what this story delivers and why.>

## Problem

<The need the story addresses, from the story body.>

## Requirements

### R1 — <requirement name>

<The requirement, derived from an acceptance criterion.>

### R2 — <requirement name>

<...>

## Non-requirements

- <What the story explicitly does not cover, if the criteria imply a boundary.>

## Acceptance criteria

1. <Each criterion from the story file, copied faithfully.>

## Changelog

(none yet)
```

Status runs `draft → approved → done`. In **automated** mode `implement`
treats a freshly generated spec as approved as the run proceeds. In
**step-by-step** mode it presents the story spec and waits for approval before
implementing; change requests route back to the spec delegate and the spec is
re-presented. One `R<n>` per acceptance criterion, in the same order — the
spec is a faithful restatement of *what*, never *how*.

## Generating a spec

1. Read the story data from the issue tracker: frontmatter (`id`, `title`,
   `type`, `labels`, `parent`), the `## Story` body, and every
   `## Acceptance Criteria` item.
2. Fill the template from those, one requirement per criterion. Invent nothing;
   if a criterion is ambiguous, state the ambiguity under Non-requirements
   rather than guessing.
3. Save as `.kodit/tmp/specs/spec-US-NNN-<slug>.md`, `NNN` from the story ID and
   `<slug>` a short kebab-case name from its title.
4. Move the story's tasks `open → spec` via the `issue-tracker` skill.

An existing `spec-US-NNN-*.md` is reused as-is and never rewritten.

## Recording plans in the story

`AGENTS.md`'s inner loop attaches plans to tasks as separate artifacts. Record
each plan's path next to its task so the story remains the index of its work.
After the plan delegate's `plan-writing` run returns, that delegate records
the plan path via the `issue-tracker` skill in operate mode.

For the file backend, add or update the story file's plan links under
the task table:

```markdown
## Tasks
| ID | Description | Status |
|----|-------------|--------|
| T-001 | Add reset-token model and expiry | plan |
| T-002 | Send reset email | open |

## Plans
| Task | Plan |
|------|------|
| T-001 | `.kodit/tmp/specs/plan-T-001-add-reset-token.md` |
```

Create the `## Plans` section the first time a plan is recorded; add one row per
plan and never remove a row.

For the Linear backend, record the plan path in the task issue's description
metadata block or as a comment. The canonical status lives on each sub-issue.
