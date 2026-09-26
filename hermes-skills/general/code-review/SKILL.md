---
name: code-review
description: >-
  Use when implemented kodit work needs a technical review against approved
  specs, plans, and acceptance criteria — "review this PR", "review the
  milestone work", "check T-003 against the spec", or when a kodit review flow
  needs findings. Gathers story requirements from the issue tracker and PR facts
  itself (via gh), maps each finding to a requirement with severity
  (blocker/major/minor/nit), evidence, and a fix, and returns a story-level
  verdict (pass, change_request, comment_only). Read-only: never publishes
  GitHub reviews and never changes issue, task, or milestone status.
version: 1.0.0
author: invoque
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [kodit, review, pr, findings, severity]
    related_skills: [issue-tracker, gh-cli, plan-writing]
---

# code-review

Reviews implementation facts against requirements and returns structured findings.

## When to Use

- A user asks directly: "review this PR", "review the milestone work", "check
  T-003 against the spec", "review this implementation".
- A kodit review flow needs technical judgment on completed work.
- Not for opening, approving, or merging a pull request, and not for fixing the
  findings — this skill only reads and reports.

## Usage

Inputs: the active milestone ID, the tasks and stories to review, their approved
specs and plans, and the implementation facts (changed files, diffs, checks,
verification evidence). If the caller does not supply the facts, gather them
yourself in step 3. Output: structured findings grouped by story/task, each with
severity, evidence, and a fix recommendation, plus a story-level verdict. This
skill never writes GitHub reviews, tracker files, or temporary reports.

## Steps

### 1. Scope the review

Use the milestone, PR, and task state to decide what needs review. Include only
items that are implemented or claimed ready for review.

### 2. Gather requirements

Follow the `issue-tracker` skill in operate mode (load it with `skill_view` when
available) to read the relevant story data, acceptance criteria, approved specs,
and approved plans. If it is not installed, read the file-based tracker directly
with `read_file` (`.kodit/issues/M-NNN-*/US-NNN-*.md`); for a Linear backend,
use the `linear-cli` skill or stop and report that `issue-tracker` is required.
Record the requirements each task must satisfy.

### 3. Examine implementation evidence

Use the facts the caller supplied when present: changed files, diffs, checks
results, verification evidence, and any locally readable tests or commands. When
they are absent, gather them yourself with `terminal`:

- Locate the PR from the milestone charter's `**PR:**` record, or with
  `gh pr list --head <head> --base <base> --state open`.
- Read the diff and checks with the `gh-cli` skill (load it with `skill_view`
  when available): `gh pr view`, `gh pr diff`, `gh pr checks`.
- Read locally available tests and verification output with `read_file`.

When facts cannot be obtained (no GitHub access, no PR, missing checks), stop
and name exactly what is missing rather than guessing.

### 4. Map findings to requirements

For every finding, record the affected milestone/story/task, severity,
requirement reference, evidence source, and a concrete fix recommendation.
Severity must be one of `blocker`, `major`, `minor`, or `nit`. Read
`references/review-criteria.md` for the severity and evidence rules.

### 5. Classify the verdict

Derive one story-level outcome: `pass`, `change_request`, or `comment_only`.
Blockers in a story produce `change_request`. The exact rules are in
`references/review-criteria.md`.

### 6. Return structured output

Return at least:

- `milestone_id`
- `verdict`
- `findings[]`: story/task, severity, requirement, evidence, fix
- `summary_counts`: blockers, majors, minors, nits
- `status_moves`: recommended task transitions only.

Never update statuses or publish a review.

## Pitfalls

- **Guessing when evidence is missing.** If facts cannot be gathered, stop and
  name what the caller or environment must provide.
- **Publishing or mutating state.** This skill never publishes a GitHub review
  and never changes issue, task, or milestone status; `status_moves` are
  recommendations only.
- **Findings without evidence.** Every finding must cite a requirement and an
  evidence source from `references/review-criteria.md`.
- **Severity drift.** Use only `blocker`, `major`, `minor`, `nit`.
- **Reviewing without requirements.** Skipping step 2 makes the verdict
  meaningless; read the story data first.

## Verification

- Requirements were read before any judgment; every finding cites a requirement
  and an evidence source.
- Every severity is one of `blocker`, `major`, `minor`, `nit`.
- The verdict follows the blocker rule in `references/review-criteria.md`.
- The output carries `milestone_id`, `verdict`, `findings[]`, `summary_counts`,
  and `status_moves`.
- No GitHub review was published and no tracker or milestone record was changed.

## Reference files

| Topic | Read |
| --- | --- |
| Severity levels, evidence requirements, verdict rules, task mapping | `references/review-criteria.md` |
