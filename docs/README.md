# Kodit Workflow Skills — User Guide

This guide covers the six implemented workflow skills that drive `kodit`'s milestone-driven development loop. Each skill is a pure orchestrator: it sequences work and delegates to general skills but never writes code, tracker files, or git commands itself.

The canonical definitions live in `skills/workflow/*/SKILL.md`; this guide is a navigable summary for users.

## The Workflow Loop

```
setup-kodit
  │
  ▼
milestone-planning
  │
  ▼
implement ─────────────► pr-request
                              │
                              ▼
                          pr-review ──(blockers)──► implement
                              │
                              ▼ (clean PR)
                          pr-approve
```

Each skill hands off by name to the next. There is no central dispatcher; you invoke the next skill when told to.

## Skill Reference

| Skill | Purpose | User decisions | Handoff to |
|---|---|---|---|
| [setup-kodit](workflow/setup-kodit.md) | Initialize `kodit` in a project | Metadata, issue tracking, git branching, checkpoint approval | `milestone-planning` |
| [milestone-planning](workflow/milestone-planning.md) | Agree the next milestone's scope | Interview, checkpoint approval | `implement` |
| [implement](workflow/implement.md) | Work an open milestone one checkpoint at a time | Scope per segment (one task / rest of milestone / stop), re-asked after every commit; spec+plan approval on single-task scope | `pr-request` |
| [pr-request](workflow/pr-request.md) | Open a PR for the milestone branch | None | `pr-review` |
| [pr-review](workflow/pr-review.md) | Review a milestone PR and close the loop | None (receives review context) | `implement` or `pr-approve` |
| [pr-approve](workflow/pr-approve.md) | Finalize a reviewed PR via approval and merge | Confirmation gate, branch cleanup | — (terminal) |

## Shared Entry Gate

Every workflow skill starts with the same check: follow `kodit-config` in **check mode**. If `kodit.json` is missing, the skill stops and directs you to `setup-kodit`. This prevents any phase from running on an unconfigured project.

## Approval Points

The workflow requires explicit approval at these points:

| Where | What is approved |
|---|---|
| `setup-kodit` step 5 | Project metadata, issue config, git config, and the exact `kodit.json` before anything is written |
| `milestone-planning` step 4 | Milestone goal, stories, tasks, and file plan |
| `implement` step 4 | Scope of the segment: one task, the rest of the milestone, or stop (re-asked at every post-commit checkpoint) |
| `implement` step 5 | The spec and plan of the task (single-task scope only) |
| `implement` step 7 | Whether to hand off to `pr-request` at milestone completion |
| `pr-approve` step 4 | Approval and merge actions before any remote write |

## Safety Invariants

- **Single milestone in flight.** Only one non-closed milestone is allowed at any time.
- **Spec-first implementation.** No task is implemented without an approved spec and plan.
- **Test-first delivery.** Every plan requires a failing check before the passing change (RED → GREEN). No commits past a failing check.
- **Review before merge.** No PR is approved or merged without a review. No workflow skill approves or merges directly; delegation goes to `github-pr-state` and `github-pr-merge`.
- **Protected branches.** `master` and `dev` are never committed to directly. All work happens on `feature/*` branches.

## What This Guide Does Not Cover

The formal milestone phases — `review-loop`, `milestone-review`, and `done` — are defined in [AGENTS.md](../AGENTS.md#workflow-phases) but do not yet have implemented skills. Their behavior is documented there. This guide covers only the six workflow skills that currently exist.

## General Skills Dependency Map

The workflow skills invoke these general skills by name:

| General skill | Invoked by |
|---|---|
| `kodit-config` | All six workflow skills (check mode) |
| `issue-tracker` | All except `setup-kodit` write step |
| `interview` | `setup-kodit`, `milestone-planning` |
| `git-branching` | `setup-kodit` |
| `plan-writing` | `implement` |
| `github-pr` | `pr-request` |
| `github-pr-state` | `pr-review`, `pr-approve` |
| `github-pr-merge` | `pr-approve` |
| `code-review` | `pr-review` |

General skills are single-purpose capabilities with no phase knowledge. Workflow skills call them; they never call workflow skills.
