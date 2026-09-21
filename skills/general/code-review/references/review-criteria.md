# Review criteria

Defines how `code-review` classifies findings and derives a story-level
verdict.

## Severity levels

| Level | Meaning |
|---|---|
| `blocker` | Fails acceptance criteria, breaks required behavior, or prevents safe merge. |
| `major` | Correctness or scope gap that should be fixed before release but does not block review. |
| `minor` | Functional but imperfect alignment with intent or best practice. |
| `nit` | Cosmetic, low-risk, optional-for-this-release. |

## Evidence requirements

Every finding must reference at least one of:

- acceptance criteria or requirement line,
- spec or plan section,
- PR diff / changed file path,
- check / test output or command,
- observed behavior.

## Story-level verdicts

| Verdict | Rule |
|---|---|
| `pass` | No blockers and no unresolved majors for that story. |
| `change_request` | At least one blocker exists for that story. |
| `comment_only` | No blockers, but majors/minors/nits exist. |

## Task mapping

Findings map to a task when the evidence points to a specific implemented row in
the story's task list. When a finding spans multiple tasks, attach it to the
broadest owning task and note the shared impact.
