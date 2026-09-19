# Sizing and output examples

Sizing guidance for step 3 (settle scope) and the presentation formats for step
4 (checkpoint) and step 7 (final summary) of `milestone-planning`.

## Sizing: soft caps

A milestone is a batch of related work a solo developer can finish and review
before the next one starts. These caps keep it that size — they are **soft**:
a strong recommendation surfaced in the interview and restated as a verdict at
the checkpoint, never a rejection.

| Measure | Target | Why |
|---|---|---|
| User stories per milestone | 2–5 | Few enough to hold in one context, review as a unit, and close. |
| Tasks per story | 2–6 | A story needing more is usually two stories. |
| Tasks per milestone | ≤ ~20 | Above this, the milestone stops being reviewable in one pass. |

Treat the counts as a sanity check, not arithmetic to hit. One large, coherent
story can beat three thin ones; six stories can be fine if each is small.

## When the scope is too big

Don't argue the user out of their ambition — reshape it. Name the split
concretely and let them choose:

- **Split by outcome.** The first slice is the smallest thing that ships and
  teaches something; the rest becomes a later milestone.
- **Split by depth.** Ship the thin end-to-end version now, harden it later.
- **Drop a story.** Move it to the backlog; it is not lost.

If the user still wants to exceed a cap, accept it, then record the override as
a decision in step 6 so the reason is not lost. Never silently drop or shrink
the user's scope.

## Worked example

Scope: "let admins invite teammates." Two stories, five tasks:

```markdown
# M-001 — Admin invites teammates to a project

**Status:** planned
**Created:** 2026-09-19

## Goal
An admin can invite a teammate by email; the invitee joins the project with the
role the admin chose.

## Stories

| ID | Title | Status |
|----|-------|--------|
| US-001 | Send and accept an email invitation | open |
| US-002 | Assign a role on acceptance | open |
```

```markdown
---
id: US-001
title: Send and accept an email invitation
type: feature
labels: [ready-for-agent]
status: open
parent: M-001
created: 2026-09-19
---

## Story
As an admin I want to invite a teammate by email so that they can join the
project without manual setup.

## Acceptance Criteria
- [ ] An invite email is sent to the address the admin enters.
- [ ] The invite link signs the invitee in and adds them to the project.
- [ ] A stale or reused link is rejected with a clear message.

## Tasks
| ID | Description | Status |
|----|-------------|--------|
| T-001 | Invitation model and token expiry | open |
| T-002 | Invite form and email send | open |
| T-003 | Accept-invite route and project join | open |
```

Sizing verdict for this scope: 2 stories, 5 tasks — within caps.

## Checkpoint format (step 4)

Present exactly these sections, then stop for approval.

```markdown
## Milestone proposal

**Goal:** <what done looks like>
**Numbers:** M-00N; stories US-00a–US-00c; tasks T-00x–T-00y
**Sizing:** <n> stories, <m> tasks — within caps / over cap (<reason>)

### Stories

| US | Title | Type | Tasks |
|----|-------|------|-------|
| US-00a | <title> | feature | T-00x, T-00y |

<One line of acceptance criteria per story.>

### Files
- create `.kodit/issues/M-00N-<name>/INDEX.md`
- create `.kodit/issues/M-00N-<name>/US-00a-<name>.md`, ...
- update `.kodit/issues/INDEX.md` (add M-00N row)
- append decisions to `CONTEXT.md`

Approve, or tell me what to change.
```

## Final summary format (step 7)

```markdown
## Milestone recorded

**M-00N — <goal>** at `.kodit/issues/M-00N-<name>/`

| US | Title | Tasks |
|----|-------|-------|
| US-00a | <title> | T-00x, T-00y |

**Decisions recorded:** <n> appended to `CONTEXT.md`.
**Next:** run the `implement` skill to start implementation.
```
