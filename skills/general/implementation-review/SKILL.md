---
name: implementation-review
description: >-
  Use when a Kodit caller needs a technical review of implemented work against
  approved specs, plans, acceptance criteria, and evidence — compare the PR or
  branch diff to requirements, identify blockers and non-blockers, and produce
  findings with severity and fix recommendations. Never change GitHub state,
  issue status, or milestone records.
---

# implementation-review

Review implementation facts against requirements and produce structured findings.

## Usage

Invoked by workflow skills that need technical judgment. Inputs are the active
milestone ID, selected tasks and stories, the relevant specs/plans, and the
implementation facts from `github-pr-state`. Outputs are structured findings
grouped by story/task, each with severity, evidence, and a fix recommendation.
This skill never writes GitHub reviews, tracker files, or temporary reports.

## What You Must Do When Invoked

### 1. Scope the review

Use the caller’s milestone, PR, and task state to decide what needs review.
Include only items that are implemented or claimed ready for review.

### 2. Gather requirements

Read the relevant story files, acceptance criteria, approved specs, and approved
plans. Record the requirements each task must satisfy.

### 3. Examine implementation evidence

Use the implementation facts supplied by the caller: changed files, diffs,
checks results, verification evidence, and any locally readable tests or
commands. When facts are missing, stop and name what the caller must provide
rather than guessing.

### 4. Map findings to requirements

For every finding, record the affected milestone/story/task, severity,
requirement reference, evidence source, and a concrete fix recommendation.
Severity must be one of: `blocker`, `major`, `minor`, `nit`.

### 5. Classify the verdict

Derive one story-level outcome: `pass`, `change_request`, or `comment_only`.
Blockers in a story produce `change_request`.

### 6. Return structured output

Return at least:

- `milestone_id`
- `verdict`
- `findings[]`: story/task, severity, requirement, evidence, fix
- `summary_counts`: blockers, majors, minors, nits
- `status_moves`: recommended task transitions only.

Never update statuses or publish a review.
