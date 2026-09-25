# implement — story-unit verification checks

Derived from `spec-US-008-implement-story-unit.md` acceptance criteria 1–18
plus four format caps. Every command is copy-pasteable from the repository
root. Record each run's observations in a dated `## RED baseline` /
`## GREEN` section below.

**Self-match rule:** absence checks AC 3, 7, 10, and 13 scan this file's own
directory, so forbidden phrases are written as split shell literals that
concatenate at runtime but never appear as file text (for example
`'rest of the mile''stone'`). After writing this file, grep it for each
forbidden phrase to prove it does not self-match.

## Checks

### AC 1 — one-story unit

- Command: `grep -q 'one user story' skills/workflow/implement/SKILL.md && echo AC1-grep-ok`
- Expected: `AC1-grep-ok`, plus a read confirming no step continues to a second story in the same run.

### AC 2 — mode gate present

- Command: `grep -q 'automated' skills/workflow/implement/SKILL.md && grep -q 'step-by-step' skills/workflow/implement/SKILL.md && grep -qi 'you decide' skills/workflow/implement/SKILL.md && echo AC2-ok`
- Expected: `AC2-ok` — all three literals present (auto-accept phrases listed).

### AC 3 — manual-mode STOPs

- Command: `grep -qi 'all plans' skills/workflow/implement/SKILL.md && ! grep -rn 'Approve ''when the scope' skills/workflow/implement/ docs/workflow/implement.md && echo AC3-ok`
- Expected: `AC3-ok` — one all-plans STOP literal present; old per-task approval phrase absent.

### AC 4 — delegation wording

- Command: `grep -q 'general-purpose subagent capability is available' skills/workflow/implement/SKILL.md && echo AC4-ok`
- Expected: `AC4-ok` — the literal delegation fragment appears.

### AC 5 — delegation briefs

- Command: `test -f skills/workflow/implement/references/delegation.md && grep -q 'spec authoring' skills/workflow/implement/references/delegation.md && grep -q 'plan authoring' skills/workflow/implement/references/delegation.md && grep -q 'test authoring' skills/workflow/implement/references/delegation.md && grep -Eq 'feat:|fix:' skills/workflow/implement/references/delegation.md && grep -qi 'commit the failing tests' skills/workflow/implement/references/delegation.md && echo AC5-ok`
- Expected: `AC5-ok` — `references/delegation.md` exists with all four brief markers.

### AC 6 — delegate-owned transitions

- Command: `grep -q 'open → spec' skills/workflow/implement/references/delegation.md && grep -q 'spec → plan' skills/workflow/implement/references/delegation.md && grep -q 'plan → implement' skills/workflow/implement/references/delegation.md && grep -q 'implement → review' skills/workflow/implement/references/delegation.md && echo AC6-ok`
- Expected: `AC6-ok` — all four transition arrows present.

### AC 7 — old scope ask removed

- Command: `! grep -rn 'rest of the mile''stone' skills/workflow/implement/ docs/workflow/implement.md docs/README.md README.md && echo AC7-ok`
- Expected: `AC7-ok` — no matches in any scanned path.

### AC 8 — two-commit TDD

- Command: `grep -q 'test:' skills/workflow/implement/SKILL.md && grep -Eq 'feat:|fix:' skills/workflow/implement/SKILL.md && echo AC8-ok`
- Expected: `AC8-ok`, plus a read confirming the failing-test commit precedes implementation.

### AC 9 — greps-as-tests

- Command: `grep -qi 'grep' skills/workflow/implement/references/delegation.md && echo AC9-ok`
- Expected: `AC9-ok` — delegation briefs state tests are verification greps.

### AC 10 — handoff, no PR question

- Command: `grep -q 'pr-request' skills/workflow/implement/SKILL.md && grep -q 'pr-request' skills/workflow/implement/references/summary-format.md && ! grep -rn 'open the pull request'' now' skills/workflow/implement/ docs/workflow/implement.md && echo AC10-ok`
- Expected: `AC10-ok` — both `pr-request` references present; old ask absent.

### AC 11 — refusals and blocked-only edge

- Command: `grep -q 'setup-kodit' skills/workflow/implement/SKILL.md && grep -q 'milestone-planning' skills/workflow/implement/SKILL.md && grep -qi 'every remaining task' skills/workflow/implement/SKILL.md && echo AC11-ok`
- Expected: `AC11-ok` — both refusals and the blocked-only stop present.

### AC 12 — format caps (SKILL.md)

- Command: `python3 -c "import sys,yaml,re; t=open('skills/workflow/implement/SKILL.md').read(); fm=t.split('---')[1]; d=yaml.safe_load(fm); assert list(d.keys())==['name','description'], d.keys(); body=t.split('---',2)[2].strip('\n'); n=len(body.splitlines()); assert n<100, n; w=len(d['description'].split()); assert w<=80, w; print('AC12-ok body=%d desc_words=%d'%(n,w))"`
- Expected: `AC12-ok` with body < 100 lines and description ≤ 80 words; frontmatter keys exactly `name`,`description`.

### AC 13 — agent-agnostic

- Command: `! grep -riE 'cla''ude|open''code|anthro''pic' skills/workflow/implement/ && ! grep -ri 'named'' general' skills/workflow/implement/ && echo AC13-ok`
- Expected: `AC13-ok` — no vendor strings or agent-specific subagent naming.

### AC 14 — evals rewrite

- Command: `python3 -c "import json; d=json.load(open('skills/workflow/implement/evals/evals.json')); ids=[e['id'] for e in d['evals']]; names=[str(e['name']) for e in d['evals']]; assert len(ids)>=5, ids; assert any('automated' in n for n in names), names; assert any('manual' in n for n in names), names; assert any(n.startswith('resume') for n in names), names; assert 'no-open-milestone-refusal' in names, names; assert 'not-set-up-refusal' in names, names; print('AC14-ok', names)"`
- Expected: `AC14-ok` with ≥ 5 cases (ids numeric, `name`-carried) including automated, manual, `resume*`, `no-open-milestone-refusal`, `not-set-up-refusal`.

### AC 15 — approval model mode-based

- Command: `grep -q 'automated' skills/workflow/implement/references/spec-format.md && ! grep -q 'single-task scope' skills/workflow/implement/references/spec-format.md && echo AC15-ok`
- Expected: `AC15-ok` — mode wording present; old scope phrase absent.

### AC 16 — story summary

- Command: `grep -qi 'story summary' skills/workflow/implement/references/summary-format.md && grep -q 'implement' skills/workflow/implement/references/summary-format.md && grep -q 'pr-request' skills/workflow/implement/references/summary-format.md && echo AC16-ok`
- Expected: `AC16-ok` — story summary template with handoff naming re-invoke and `pr-request`.

### AC 17 — docs agree

- Command: `grep -q 'story' docs/workflow/implement.md && grep -q 'automated' docs/workflow/implement.md && grep -q 'automated' docs/README.md && echo AC17-ok`
- Expected: `AC17-ok` — workflow guide and index use the new vocabulary.

### AC 18 — CONTEXT decisions

- Command: `grep -q '| 2026-09-25 |' CONTEXT.md && grep -q 'Supersede the 2026-09-22' CONTEXT.md && ! grep -q 'one task or the rest of the mile''stone' CONTEXT.md && echo AC18-ok`
- Expected: `AC18-ok` — new superseding decisions row; Current State no longer uses the old phrasing.

## RED baseline — 2026-09-25

Run against the pre-revision skill. Result: **17 of 18 checks FAIL** (only
AC 13 passes); AC 12 fails on the description cap. Expected RED set per plan
T-008 S2 was AC 1–11 and 14–18 — confirmed, plus AC 12 recorded truthfully.

| Check | Observed | Result |
|---|---|---|
| AC 1 | no match — `one user story` absent from SKILL.md | FAIL |
| AC 2 | no output — `automated`, `step-by-step`, `you decide` all absent | FAIL |
| AC 3 | no output — `all plans` absent (presence condition fails; absence condition passes) | FAIL |
| AC 4 | no match — delegation literal absent | FAIL |
| AC 5 | `references/delegation.md` does not exist | FAIL |
| AC 6 | `references/delegation.md` does not exist (No such file or directory) | FAIL |
| AC 7 | matches at SKILL.md:7,58,94; evals/evals.json:8,20; docs/workflow/implement.md:37,53,63; docs/README.md:50; root README.md: none | FAIL |
| AC 8 | no output — `test:` absent (AC8a FAIL) and `feat:`/`fix:` absent (AC8b FAIL) | FAIL |
| AC 9 | `references/delegation.md` does not exist | FAIL |
| AC 10 | presence passes (pr-request in SKILL.md and summary-format.md); absence fails — matches at summary-format.md:44,58; docs/workflow/implement.md:57 | FAIL |
| AC 11 | `setup-kodit` PASS, `milestone-planning` PASS, `every remaining task` FAIL (absent — blocked-only edge unhandled) | FAIL |
| AC 12 | keys exactly name+description PASS; body 92 lines PASS; description 91 words FAIL (> 80) → AssertionError: 91 | FAIL |
| AC 13 | `AC13-ok` — no vendor strings, no agent-specific subagent naming | **PASS** |
| AC 14 | parses, 5 cases, but names lack automated/manual cases: single-task-scope, resume-mid-milestone, whole-milestone-scope, no-open-milestone-refusal, not-set-up-refusal → AssertionError | FAIL |
| AC 15 | `automated` absent in spec-format.md; `single-task scope` present → AssertionError | FAIL |
| AC 16 | `story summary` absent from summary-format.md (handoff still asks the open-the-PR question) | FAIL |
| AC 17 | `story` PASS in docs/workflow/implement.md; `automated` FAIL in both docs | FAIL |
| AC 18 | `\| 2026-09-25 \|` absent from CONTEXT.md; superseding row absent | FAIL |

Self-match proof: grepping this file for each forbidden phrase
(`rest of the mile''stone`, `Approve ''when the scope`,
`open the pull request'' now`, vendor strings, `named'' general`)
returns 0 matches — split literals are working.

## GREEN — 2026-09-25

Run after implementation (T-018). Result: **18 of 18 PASS**. Format caps:
frontmatter keys exactly `name`,`description`; body 87 lines (< 100);
description 79 words (≤ 80); `evals.json` valid JSON, 5 cases.

| Check | Observed | Result |
|---|---|---|
| AC 1 | `one user story` present; step 7 forbids starting a second story | PASS |
| AC 2 | `automated`, `step-by-step`, `you decide` all present (description + step 4) | PASS |
| AC 3 | `all plans` present (step 6); old approval phrase absent from skill and docs | PASS |
| AC 4 | `general-purpose subagent capability is available` present (Usage) | PASS |
| AC 5 | `references/delegation.md` exists; spec/plan/test authoring literals, `feat:`/`fix:`, `commit the failing tests` all present | PASS |
| AC 6 | all four transition arrows present in delegation.md | PASS |
| AC 7 | no matches in skill dir, docs/workflow/implement.md, docs/README.md, README.md | PASS |
| AC 8 | `test:` and `feat:`/`fix:` present; step 7 orders RED commit before GREEN | PASS |
| AC 9 | `grep` present in delegation.md (tests are verification greps) | PASS |
| AC 10 | `pr-request` in SKILL.md and summary-format.md; old ask phrase absent | PASS |
| AC 11 | `setup-kodit`, `milestone-planning`, `every remaining task` all present | PASS |
| AC 12 | keys exact; body 87 < 100; description 79 ≤ 80 | PASS |
| AC 13 | no vendor strings or agent-specific subagent naming in the skill dir | PASS |
| AC 14 | evals.json valid; 5 cases: automated-mode-full-story, manual-mode-stops, resume-mid-story, no-open-milestone-refusal, not-set-up-refusal | PASS |
| AC 15 | `automated` present in spec-format.md; `single-task scope` gone | PASS |
| AC 16 | `story summary` present; handoff names re-invoking `implement` and `pr-request` | PASS |
| AC 17 | `story` and `automated` present in docs/workflow/implement.md; `automated` in docs/README.md | PASS |
| AC 18 | `2026-09-25` row with `Supersede the 2026-09-22` appended; old contiguous phrase gone from CONTEXT.md | PASS |

Self-match proof re-verified: grepping this file for each forbidden phrase
returns 0 matches.
