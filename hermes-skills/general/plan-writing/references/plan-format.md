# Plan format

Read this before drafting any plan. The template, a worked example, and the
test-first (RED → GREEN) rules for `plan-T-NNN-*.md`. Plans are untracked
working artifacts under `.kodit/tmp/specs/`; they attach to a task and live
only for its work.

## Template

```markdown
# plan-T-NNN — <task title>

**Story:** US-NNN — <story title>
**Spec:** `.kodit/tmp/specs/spec-US-NNN-<slug>.md`
**Status:** draft
**Date:** YYYY-MM-DD

## Approach

<One short paragraph: the shape of the solution and the order it is built in.>

## Steps

- [ ] **S1 — <test name>: RED.** <The failing test/assertion to write and why it
      fails now. Run it and record the failure.>
- [ ] **S2 — <behavior>: GREEN.** <The smallest change that makes S1 pass.>
- [ ] **S3 — <next test>: RED.** <...>
- [ ] **S4 — <next behavior>: GREEN.** <...>
- [ ] **S5 — <non-test step>.** <Why it cannot be tested; how to verify it.>

## Verification

- `<command>` — expect `<observation>`.
- Final: the full test command passes (`<project.test>`).

## Risks

- <What could make this approach wrong, and the fallback.>

## Review notes

(pending)
```

Status runs `draft → in progress → approved → done`. `implement` may append
dated Review notes entries; never rewrite the Approach or Steps of an approved
plan — amend with a new plan or a dated entry.

## Test-first rules (RED → GREEN)

Mandatory for every plan. The point is that implementation is driven by a test
that was seen to fail: a test written after the code proves nothing.

1. **Test first.** A step that introduces behavior starts by naming the failing
   test or assertion.
2. **See it fail.** Run it and record the failure before moving on. A RED step
   with no recorded failure is not done.
3. **Smallest green.** The next step is the minimal change that passes the
   failing test — no extra behavior, no speculative generality.
4. **One behavior at a time.** Do not bundle several behaviors into one
   RED/GREEN pair; repeat for each.
5. **Refactor only on green.** Restructure after the test passes, with the suite
   still green.

### Escape hatch: no test runner

When `kodit.json`'s `project.test` is absent or empty, replace each test with a
**verifiable check**: a command or observation that fails before the change and
passes after — a build, a lint, a grep, a rendered output, a manual step. State
the check and its before/after observation in the step, and note that the
substitution is because the project has no test command. Fail-first-then-pass is
still required; only the mechanism changes.

A step that genuinely cannot be tested (pure documentation, formatting, a
rename) says so and gives its verification instead. Prefer a test where one is
possible.

## Worked example

Task `T-001 — Add reset-token model and expiry` for story `US-001` (reset
password by email), spec `spec-US-001-reset-password.md`, `project.test:
pytest`.

```markdown
# plan-T-001 — Add reset-token model and expiry

**Story:** US-001 — Reset password by email
**Spec:** `.kodit/tmp/specs/spec-US-001-reset-password.md`
**Status:** draft
**Date:** 2026-09-20

## Approach

Model the token as a dataclass with an `expires_at` field and a pure
`is_expired(now)` predicate, so expiry is testable without I/O. Build the
predicate first, then the model that carries it.

## Steps

- [ ] **S1 — expiry predicate: RED.** Write `test_token_is_expired_when_past`
      asserting `is_expired(now)` is true for a token whose `expires_at` is
      before `now`; it fails because the model does not exist.
- [ ] **S2 — expiry predicate: GREEN.** Add `ResetToken` with `expires_at` and
      the smallest `is_expired(now)` returning `now >= expires_at`.
- [ ] **S3 — not yet expired: RED.** Write
      `test_token_is_live_when_before_expiry`; it fails only if the predicate is
      wrong (guards against an always-true implementation).
- [ ] **S4 — 24-hour default: GREEN.** Give the model its default 24-hour
      expiry and assert it in `test_default_expiry_is_24h`.
- [ ] **S5 — migration.** Add the table migration; verify with
      `python -m app.migrate --check`.

## Verification

- `pytest tests/test_reset_token.py` — all four tests pass.
- `python -m app.migrate --check` — reports the schema is current.
- Final: `pytest` passes the full suite.

## Risks

- Clock handling: tests pass `now` explicitly to avoid wall-clock flakiness.
- If expiry is later enforced in SQL rather than Python, S1/S3 move behind an
  integration test.

## Review notes

(pending)
```

Note how each behavior is a RED step with a named, initially failing test, and
its GREEN step is the smallest change that passes it; the migration has no test
and says so.
