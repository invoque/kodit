# CONTEXT.md

Living context for the `kodit` project. This is the source of truth for project
identity, environment, terminology, and decisions.

**Agents: read this file before making changes, and keep it current. When you
make a significant decision, add an entry to the decisions log at the bottom in
the same change.**

## Identity

| Field | Value |
|---|---|
| **Name** | `kodit` |
| **Tagline** | Opinionated milestone-driven development for solo developers |
| **Audience** | Individual developers working with coding agents |
| **Form** | A collection of agent-agnostic skills, delivered as markdown |
| **Status** | Six workflow helpers implemented (`setup-kodit`, `milestone-planning`, `implement`, `pr-request`, `pr-review`, `pr-approve`) with their general companions; remaining formal phase workflow skills pending |

### Philosophy

`kodit` is **opinionated** by design. It picks one workflow — setup,
milestone-planning, implement, review-loop, milestone-review, done — and does not
try to support every process. It is built for the **solo developer**: enough
structure to keep an agent accountable, without the roles, approvals, and
handoffs of a team process. It is **agent-agnostic**: skills are plain markdown,
so any coding agent that can read instructions can use them.

## Background & Environment

`kodit` lives in the `agent-harness` workspace alongside sibling projects such
as `pi-extensions`. The skill format is deliberately inherited from conventions
already proven on this machine (see the `graphify` and `linear-cli` skills),
rather than invented from scratch.

Environment facts relevant to working here:

| Item | Value |
|---|---|
| **Repository** | `kodit` (markdown-first, no build step) |
| **Skill sources of truth** | Defined in this repo under `skills/`, installed into an agent's skills directory |
| **Skill directories in use on this machine** | `~/.claude/skills/` (Claude Code), `~/.agents/skills/` (agent-agnostic / pi) |
| **Documented tooling** | `python3` (3.14) and `uv` for frontmatter validation; `bun` available |
| **Agent CLI in use** | `opencode`, exclusively — `claude` is not used on this machine |
| **Not on PATH** | `node` / `npm` — do not assume they exist |

## Workflow Definition

Every project that uses `kodit` moves through six phases, always in order,
forming a milestone loop. Phases are not skipped.

| # | Phase | Purpose | Exit criteria |
|---|---|---|---|
| 1 | **setup** | Initialize `kodit` in the project | `kodit.json` and `.kodit/tmp/` exist, the issue tracker is provisioned, and configuration is validated |
| 2 | **milestone-planning** | Agree the scope of the next milestone | Milestone scope agreed and recorded |
| 3 | **implement** | Work each milestone item to completion | Every milestone item implemented |
| 4 | **review-loop** | Verify each implemented item | Every milestone item reviewed; deltas recorded |
| 5 | **milestone-review** | Confirm the milestone achieved its goal | Milestone goal verified and retrospective captured |
| 6 | **done** | Finalize the milestone | Milestone artifacts, docs, and changelog agree; work committed |

### Inner item loop

Inside `implement` and `review-loop`, each milestone item runs the same inner
loop. This is where the spec-driven discipline lives.

| # | Step | Purpose | Artifact |
|---|---|---|---|
| 1 | **spec** | Capture the item's requirements | `.kodit/tmp/specs/spec-US-NNN-<name>.md` |
| 2 | **plan** | Turn the spec into an ordered approach | `.kodit/tmp/specs/plan-T-NNN-<name>.md` (tasks embedded) |
| 3 | **implement** | Execute the plan exactly | Code / skill files |
| 4 | **review** | Verify against the spec | Review notes in the plan |

Rules that govern the workflow:

- No milestone item is implemented without an approved spec and plan.
- An approved spec or plan is not edited during implementation. Amend it via a
  new spec, or append a dated changelog entry to the existing one.
- Artifacts use globally unique zero-padded numbers under `.kodit/tmp/specs/`:
  specs attach to user stories (`spec-US-NNN-...`), plans to tasks
  (`plan-T-NNN-...`).
- Each phase's detailed steps, artifacts, and exit conditions are owned by that
  phase's workflow skill, not by this document.

### Issue taxonomy

Work is organized PROJECT → MILESTONE → USER STORY → TASK, numbered globally and
never reused: `M-001`, `US-001`, `T-001`. A user story is a requirement with
acceptance criteria; its tasks are rows in an embedded table. Statuses run
`open → spec → plan → implement → review → done` (plus `blocked` and the
`wontfix` label) on tasks, with coarser derived status on stories and
milestones. Full conventions live in `.kodit/issues/README.md`.

## Runtime Layout

Paths that `setup` creates in every adopting project.

| Path | Committed | Purpose |
|---|---|---|
| `kodit.json` | Yes | Project configuration at the repository root. Schema owned by the `kodit-config` general skill. |
| `.kodit/issues/` | Yes | File-based issue tracker: `README.md` conventions, `INDEX.md` project charter, `M-001-*/` milestone dirs with story files. Load-bearing. Only present for file-backed projects. |
| `.kodit/tmp/` | No (gitignored) | Temporary working artifacts, always markdown. Never load-bearing; promoted into a permanent artifact or discarded, and swept at phase boundaries. |
| `.kodit/tmp/workspaces/` | No (gitignored) | Throwaway workspaces agents create for testing. Always used for test workspaces; ephemeral and swept with `.kodit/tmp/`. |

The `kodit` repository itself stays markdown-first; `kodit.json` is the
configuration that `kodit` writes into the projects that adopt it.

## Canonical Skill Format

The normative format for every skill in this repository.

**Location:** `skills/<category>/<skill-name>/SKILL.md`, with optional
`references/` and `scripts/` subdirectories. `<category>` is `workflow` or
`general`.

### Skill Categories

| Category | Role | Depends on |
|---|---|---|
| `workflow` | One skill per workflow phase. Sequences the phase, enforces its entry and exit criteria, and invokes general skills as needed. | `general` |
| `general` | A single, reusable capability with no phase knowledge — for example interviewing the user, setting up `kodit`, or interacting with an issue tracker. | Nothing |

Rules:

- Dependency direction is one-way: workflow skills may reference general
  skills, never the reverse.
- Workflow skills invoke a general skill by its skill name; paths do not always
  resolve once agents flatten the tree at install time.
- One responsibility per skill; overlapping skills are merged or resplit.
- Skill names are globally unique across both categories.
- New categories require a decision recorded in the decisions log.

**Frontmatter — exactly two fields:**

```yaml
---
name: <skill-name>
description: <what the skill does and when to use it>
---
```

**Body structure:**

```markdown
# <Skill Title>

<One-line purpose.>

## Usage

<Invocation and expected inputs.>

## What You Must Do When Invoked

1. <Step>
2. <Step>
```

Requirements:

- `name` is lowercase kebab-case and matches the immediate containing directory
  name.
- `description` states trigger guidance, because agents select skills by
  description alone.
- Instructions are discrete, ordered, and deterministic.
- No vendor-specific instructions anywhere in a skill.

## Directory Conventions

Current layout:

```
kodit/
├── AGENTS.md
├── README.md
├── CONTEXT.md
├── .github/workflows/validate-skills.yml
├── .github/workflows/release-skills.yml
└── skills/
    ├── workflow/setup-kodit/, workflow/milestone-planning/, workflow/implement/, workflow/pr-request/, workflow/pr-review/, workflow/pr-approve/
    └── general/{interview, kodit-config, issue-tracker, git-branching, plan-writing, github-pr, github-pr-state, github-pr-merge, code-review}/
```

Planned layout (created as work proceeds; *(setup)* marks what the `setup` phase
creates in an adopting project):

```
kodit/
├── AGENTS.md
├── README.md
├── CONTEXT.md
├── .github/workflows/validate-skills.yml  # CI: validates all skills on master push
├── .github/workflows/release-skills.yml   # CI: creates GitHub Release on v* tag push
├── kodit.json            # project configuration (setup)
├── .kodit/
│   ├── issues/           # issue tracker (setup, committed)
│   │   ├── README.md     # conventions: taxonomy, labels, state machines
│   │   ├── INDEX.md      # project charter
│   │   └── M-001-*/      # milestone dirs (later phases)
│   │       ├── INDEX.md
│   │       └── US-001-*.md
│   └── tmp/              # temporary working artifacts (setup, gitignored)
│       └── specs/        # per-item spec/plan artifacts (untracked)
│           ├── spec-US-NNN-*.md
│           └── plan-T-NNN-*.md
└── skills/
    ├── workflow/
    │   └── <skill-name>/
    │       ├── SKILL.md
    │       ├── references/
    │       └── scripts/
    └── general/
        └── <skill-name>/
            ├── SKILL.md
            ├── references/
            └── scripts/
```

## Terminology

| Term | Meaning |
|---|---|
| **Skill** | A self-contained markdown instruction set an agent can discover and follow. The unit of delivery in `kodit`. |
| **Workflow skill** | A skill in `skills/workflow/` that owns exactly one workflow phase. Orchestrates, and invokes general skills. |
| **General skill** | A reusable, single-purpose capability in `skills/general/` with no phase knowledge. |
| **Phase** | One of the six milestone workflow stages: setup, milestone-planning, implement, review-loop, milestone-review, done. |
| **Milestone** | A batch of work planned, implemented, and reviewed as one unit before finalization. |
| **Issue tracker** | The project's issue record, either file-based at `.kodit/issues/` or external (Linear). Taxonomy is PROJECT → MILESTONE → USER STORY → TASK, numbered `M-001`, `US-001`, `T-001`. |
| **User story** | A requirement with acceptance criteria. In file backend, stored as `.kodit/issues/M-001-*/US-001-*.md`. In Linear, a parent issue with a `[US-001]` prefix. Carries its tasks in an embedded table. The unit a spec attaches to. |
| **Task** | A row inside a user story's task table; the unit a plan attaches to and the only level with the full status machine. |
| **Spec** | A written statement of requirements for a milestone item. Contains no implementation detail. |
| **Plan** | A technical approach derived from a spec, expressed as ordered, verifiable tasks. |
| **Artifact** | Any file produced by a phase. Spec and plan artifacts live under `.kodit/tmp/specs/`; they are local working artifacts, never committed, and exempt from the phase-boundary sweep. All other committed artifacts are skill files, docs, and code. |
| **Temporary artifact** | A markdown scratch file in `.kodit/tmp/`, other than spec/plan artifacts. Never load-bearing; promoted or discarded. |
| **Configuration** | `kodit.json`, at the repository root, written by `setup`. |
| **Agent** | Any coding agent that consumes `kodit` skills. Never a specific vendor in normative text. |

## Current State

- Repository initialized with `git`; `master` is stable, `dev` is integration.
- The three governing documents exist: `AGENTS.md`, `README.md`, `CONTEXT.md`.
- General skills: `interview` (spec-001), plus `kodit-config`, `issue-tracker`,
  `git-branching`, `plan-writing`, `github-pr`, `github-pr-state`,
  `github-pr-merge`, and `code-review`.
- The first workflow skill exists: `skills/workflow/setup-kodit/`, specified and
  planned by `.kodit/tmp/specs/spec-003-setup-kodit.md` and
  `.kodit/tmp/specs/plan-003-setup-kodit.md`; it was evaluated with with-skill
  and baseline runs (100% vs 47% assertion pass rate) and approved on review.
- The second workflow skill exists: `skills/workflow/milestone-planning/`,
  specified and planned by `.kodit/tmp/specs/spec-004-milestone-planning.md` and
  `.kodit/tmp/specs/plan-004-milestone-planning.md`; evaluated over two
  iterations and approved on review.
- The third workflow skill exists: `skills/workflow/implement/`, with the
  `plan-writing` general skill, specified and planned by
  `.kodit/tmp/specs/spec-005-implement-skill.md` and
  `.kodit/tmp/specs/plan-005-implement-skill.md`. It establishes the test-first
  (RED → GREEN) convention.
- The fourth workflow skill exists: `skills/workflow/pr-review/`, using the new
  `github-pr-state` and `code-review` companions; `pr-request` hands
  off to it, and the issue tracker now supports a durable `## Review` note on
  reviewed user stories.
- The fifth workflow helper exists: `skills/workflow/pr-approve/`, which
  finalizes a reviewed milestone PR by delegating approval and merge to
  `github-pr-merge` and recording the merge result in the tracker.
- Skills carry a mandatory conciseness standard (`AGENTS.md`), established by
  `spec-002` / `plan-002`.
- `.kodit/tmp/` is in use for temporary artifacts (gitignored). No `kodit.json`
  exists in this repository, and there is still no runtime code, dependencies, or
  package manifest.

Next up: scaffold the remaining three phase workflow skills and complete review-loop tooling.

## Decisions Log

| Date | Decision | Rationale |
|---|---|---|
| 2026-09-19 | Adopt a five-phase workflow: spec → plan → implement → review → done. | Balanced structure for a solo developer: enough accountability for agent work without team-sized ceremony. Leaner 3-phase and heavier 7-phase variants were rejected. |
| 2026-09-19 | Install skills manually via copy or symlink; no installer yet. | The project is markdown-only and file-based; a script or CLI would add runtime surface before the workflow itself exists. Symlinks are recommended during early development. |
| 2026-09-19 | Bootstrap as a git repository with an initial commit of the three docs. | Establishes history and a clean starting point; every later change follows the spec-driven workflow on top of it. |
| 2026-09-19 | Canonical skill frontmatter is exactly `name` and `description`. | Matches the proven conventions of `graphify` and `linear-cli` and keeps skills portable across agents. Extra metadata fields were rejected to avoid coupling skills to tooling. |
| 2026-09-19 | Keep the repository markdown-first with no runtime code. | Any code (e.g. a future installer) requires a prior decision recorded here. |
| 2026-09-19 | Protect `master` and `dev`; all work happens on `feature/*` branches. | `master` holds released state, `dev` is the integration branch, and feature branches keep unreviewed work off both. Prevents direct commits and force-pushes to protected branches. |
| 2026-09-19 | Compress `AGENTS.md` and `README.md` for conciseness. | `AGENTS.md` is now terse and rule-focused; `README.md` is human-readable. The YAML frontmatter validation command is canonical in `README.md` Contributing, and `AGENTS.md`'s Setup & Verification section was removed as redundant with README Getting Started. |
| 2026-09-19 | Supersede the five-phase workflow with a six-phase milestone workflow: setup → milestone-planning → implement-loop → review-loop → milestone-review → done. | Milestone framing matches how a solo developer batches work, and maps cleanly onto an issue tracker. The per-item spec → plan → implement → review discipline is retained as the inner loop inside `implement-loop` and `review-loop`, so `kodit` stays spec-driven. |
| 2026-09-19 | Project configuration is `kodit.json` at the repository root. | A root-level JSON file is a familiar convention (alongside `package.json` and friends) and is machine-readable for agents. It lives outside `.kodit/`, which holds only temporary state. |
| 2026-09-19 | Temporary working artifacts are markdown files in `.kodit/tmp/`, and `.kodit/` is gitignored. | Gives the workflow scratch space for interviews and drafts without polluting the committed tree. Nothing in `tmp/` is load-bearing: it is promoted into a permanent artifact or discarded. |
| 2026-09-19 | Split skills into two categories: `skills/workflow/` (one orchestrator per phase) and `skills/general/` (single-purpose capabilities). | A one-way dependency (workflow → general) with one responsibility per skill keeps skills composable and non-overlapping, and makes them installable independently. New categories require a recorded decision. |
| 2026-09-19 | Defer defining the specific skills and each phase's artifacts to the skills themselves. | The overview documents describe structure and rules; inventing an inventory before the skills exist would be speculative design. Each phase's artifacts are owned by its workflow skill. |
| 2026-09-19 | Agents needing a workspace directory for testing always use `.kodit/tmp/workspaces/`. | Keeps test workspaces inside the gitignored temporary area so they can never pollute the committed tree, and gives every agent one predictable, collocated location. Test workspaces are ephemeral and swept with `.kodit/tmp/`. |
| 2026-09-19 | Commit every completed task immediately; never leave finished work uncommitted. | Keeps the working tree reflecting real progress and prevents losing completed work. Complements the existing rule that incomplete or unverified changes must not be committed. |
| 2026-09-19 | The first skill is `interview`, a general skill implementing the design-tree interview method, with its working artifact at `.kodit/tmp/design-tree-<topic>.md`. | All three governing documents name interviewing as the prototypical general skill, and it is the prerequisite for spec-driven work: it produces the shared understanding every milestone item starts from. The method — a tree of decisions advanced one round of frontier questions at a time, with facts found by the agent and decisions owned by the user — was chosen over free-form questioning because it is deterministic, terminates when the frontier is empty, and leaves nothing silently assumed. |
| 2026-09-19 | `opencode` is the agent CLI used on this machine; skills and tooling must not assume `claude`. | The machine's harness is `opencode`. Vendor-specific instructions are already forbidden in skills, and this extends to the development tooling: the skill-creator description-optimization scripts, which shell out to `claude`, are adapted to `opencode` when used. |
| 2026-09-19 | Every skill must be clean, concise, and terse: `SKILL.md` body under 100 lines, `description` at most ~80 words, each idea stated once. | Skills are read under token pressure, so every line spends context the agent needs for the work. The measurable caps force detail into `references/` and prevent the six planned workflow skills from inheriting the first skill's verbosity. Enforced by `AGENTS.md` and checked at spec/plan review; no tooling was added, keeping the repository markdown-first. |
| 2026-09-19 | Move spec and plan artifacts from `specs/` to `.kodit/tmp/specs/`; they are untracked and exempt from the tmp sweep. | Specs and plans are local working artifacts whose value is realized in the code and skills they produce, so committing their per-item churn adds noise without durable benefit. The sweep exemption prevents accidental loss and keeps the numbered spec history locally across phases and milestones. |
| 2026-09-19 | Name the setup workflow skill `setup-kodit`, and split its work into three general companions: `kodit-config`, `issue-tracker`, `git-branching`. | `setup` alone is collision-prone once skills are flattened into an agent's directory, so the phase name is suffixed in the skill name. The workflow skill is a pure orchestrator (sequence, gates, summary) because bundling schema, tracker, and branching rules into it would make one unmaintainable skill; the companions own domain knowledge and never depend on the workflow skill. |
| 2026-09-19 | Adopt the issue taxonomy PROJECT → MILESTONE → USER STORY → TASK, numbered globally `M-001`, `US-001`, `T-001`. | The flat milestone-item model was too coarse: stories express requirements, tasks express work. Global numbering (never reset per milestone) keeps every ID a unique reference across the project and makes `spec-US-NNN` / `plan-T-NNN` filenames unambiguous. |
| 2026-09-19 | Store the file-based tracker under `.kodit/issues/` (committed), with the project charter in `INDEX.md`, milestone directories `M-001-*/` each holding an `INDEX.md` charter and `US-001-*.md` story files whose tasks are an embedded table. | Issues are load-bearing, so they cannot live in the gitignored `.kodit/tmp/`. A committed `.kodit/issues/` keeps all project machinery in one place, directories give the tree structure, and embedded task tables keep a story and its work in one file. |
| 2026-09-19 | Attach specs to user stories (`spec-US-NNN-*.md`) and plans to tasks (`plan-T-NNN-*.md`); both stay untracked in `.kodit/tmp/specs/`. | "Spec = what, plan = how" maps to story vs task, avoiding a duplicated spec per task. Keeping them untracked follows the existing decision that per-item spec/plan churn is local, while the story's acceptance criteria live committed in its issue file. |
| 2026-09-19 | Run the full status machine on tasks only; stories derive `open → in-progress → done` and milestones `planned → active → closed`. | A story should not snap back to `spec` when its next task starts; deriving coarse status from children keeps the high-level view truthful without per-level ceremony. |
| 2026-09-19 | Issue labels are handoff signals only: `ready-for-agent`, `ready-for-human`, `needs-info`, `needs-triage`, `wontfix`. Item type is a frontmatter field (`feature`, `bug`, `chore`, `docs`, `refactor`). | Labels answer "who acts next, or is it closed?", which is what a solo developer scanning a board needs; type is orthogonal metadata, so it lives in frontmatter rather than competing for the label namespace. |
| 2026-09-19 | `kodit.json` v1 schema: `version`, `project{name,description,language,build,test}`, `issue_tracker{type,path,labels}`, `git{main_branch,dev_branch,feature_prefix,bugfix_prefix,staging_branch,remote}`; `git` may be null. Owned by `kodit-config`. | A lean, backend-swappable config: state machines and the issue tree live in the tracker's conventions doc, keeping `kodit.json` to machine-readable settings. `git: null` lets non-git projects adopt the workflow without blocking on version control. |
| 2026-09-19 | `setup-kodit` appends to existing `AGENTS.md`, `README.md`, and `CONTEXT.md`; it never overwrites them. | Adopting projects own their docs; appending a kodit section preserves human content and is reversible, whereas overwriting risks destroying information the user cannot recover. |
| 2026-09-19 | GitHub Issues and Linear are selectable but deferred; choosing one explains it is unsupported and guides the user to the file-based backend. | Shipping one backend thoroughly beats three partially. `issue_tracker.type` makes a later migration a config change, and a graceful fallback avoids dead ends during setup. |
| 2026-09-19 | `setup-kodit` checkpoints for review before writing, showing per-section tables, the exact `kodit.json` preview, and a create-vs-append file plan. | Writing config is the one irreversible step of setup; previewing the exact JSON and file actions at a gate catches mistakes before they land, and the file plan makes the append/overwrite behaviour explicit. |
| 2026-09-19 | `git-branching` offers repository changes (create `dev`, add a remote) rather than performing them unilaterally; staging is an optional release-hardening lane between `dev` and `main`. | Branch and remote changes touch shared state and protected branches, so the user approves each action. Defining staging's purpose (or leaving it null) avoids an undefined option that later skills would have to guess at. |
| 2026-09-20 | `milestone-planning` refuses to start when any milestone is not `closed` — `planned` or `active` both block. | One milestone in flight at a time. A freshly planned milestone is not yet being worked on, but planning a second would leave two open scopes and no clear next action; refusing keeps the project on a single, finishable slice. |
| 2026-09-20 | `milestone-planning` sizes a milestone with soft caps: 2–5 stories, 2–6 tasks per story, ≤ ~20 tasks total. | Soft means a strong recommendation surfaced in the interview and restated as a sizing verdict at the checkpoint, never a rejection. The caps are a proxy for "finishable and reviewable before the next milestone"; a deliberate overage is accepted and recorded as a decision, so scope is reshaped rather than silently dropped. |
| 2026-09-20 | `kodit-config` gains a fourth mode, **decisions**, which appends dated rows to the `CONTEXT.md` decisions log; `milestone-planning` uses it rather than writing the log itself. | Every phase must record significant decisions per `AGENTS.md`, but no general skill owned that write outside setup. Keeping it in `kodit-config` (which already owns `CONTEXT.md`) makes the capability phase-blind and reusable, and keeps workflow skills pure orchestrators. Append-only: existing rows are never rewritten. |
| 2026-09-20 | `milestone-planning` hands off to a skill named `implement` (to be created), not `implement-loop`. | The user named the next phase skill `implement`; the phase table's `implement-loop` label will be reconciled when that skill is built. The handoff names the skill by name — no slash commands — because skills are agent-agnostic and installed flat. |
| 2026-09-20 | TDD is mandatory in plans, enforced as a test-first RED → GREEN ordering; `implement` verifies the failing test/check ran before accepting the passing change. | The user requires TDD as a strict rule, but the repository had no such convention. Making the plan own the ordering and the orchestrator verify it keeps the discipline in the artifact that drives the work (so it is reviewable) rather than in prose. A test written after the code proves nothing, so the RED step must be observed. |
| 2026-09-20 | When a project has no test command (`kodit.json` `project.test` absent), the RED → GREEN rule uses a verifiable substitute check — a command or observation that fails first and passes after. | `kodit` is markdown-first and adopting projects may lack a test runner; blocking them would break the workflow, while skipping the rule would hollow it out. Fail-first-then-pass is preserved; only the mechanism changes, and the substitution is recorded in the plan. |
| 2026-09-20 | `implement` asks once per run whether plan approval is interactive or non-interactive: interactive pauses before each story's implementation; non-interactive accepts recommendations and presents the summary at the end. | A single upfront choice keeps a solo developer in control when they want it without forcing a per-task gate that would make large milestones tedious. The mode is a run-level decision, so it is asked once rather than re-litigated per task. |
| 2026-09-20 | When a story has no spec, `implement` auto-generates `spec-US-NNN-*.md` from the story's acceptance criteria and body; an existing spec is reused, never rewritten. | The inner loop requires an approved spec before a plan, but milestone-planning records only stories and criteria. Deriving the spec from criteria the user already approved keeps the loop intact without a second interview per story, and never rewrites an approved artifact. |
| 2026-09-20 | `implement` works one feature branch per milestone, `<feature_prefix>m-NNN-<slug>` from `dev`, commits each completed task on it, and hands off to a not-yet-built `pr-request` skill; the post-`pr-request` chain (review ordering, `review → done`) is deferred. | One branch per milestone gives the pull request a single reviewable unit and matches the one-milestone-in-flight rule; committing per task follows the existing immediate-commit decision. The pull-request flow was named before it exists, as `milestone-planning` named `implement`, and the review ordering will be reconciled when `pr-request` is built. |
| 2026-09-20 | `pr-request` stays a user-invoked workflow helper between `implement` and the future `pr-review`; it is not a new outer milestone phase. | The six-phase loop is unchanged. `implement` already hands off by name to `pr-request`, and review ordering stays deferred, so no phase-table edits in `AGENTS.md`, `README.md`, or `CONTEXT.md` are needed. |
| 2026-09-20 | `pr-request` is a pure orchestrator; all git/GitHub work lives in a new general skill, `github-pr`, with a bundled PR title/body template. | The mandatory rule requires workflow skills to delegate: `pr-request` sequences checks and handoffs only, while `github-pr` owns remote/branch validation, idempotent PR creation via GitHub MCP or `gh`, and the reusable template. Plain `git` alone cannot open a GitHub PR. |
| 2026-09-20 | An open PR is recorded as optional `**PR:** <url>` in the milestone charter; task, story, and milestone statuses do not change. | No `pending`/`pr-open` state exists, tasks already sit at `review` after `implement`, and only review can move them to `done`. A metadata line keeps the tracker truthful without inventing a state transition. |
| 2026-09-20 | Skill eval definitions live with the skill (`evals/evals.json`); transient iteration results live under `.kodit/tmp/workspaces/`. | Follows the skill-creator layout for definitions while respecting the kodit rule that test workspaces stay gitignored under `.kodit/tmp/workspaces/` and are swept at phase boundaries. |
| 2026-09-20 | `pr-review` is a user-invoked workflow helper after `pr-request`, not a formal milestone phase. | Keeps the six-phase loop intact while filling the missing review-handoff step; workflow skills stay orchestrators and delegate GitHub/implementation work. |
| 2026-09-20 | GitHub PR inspection and constrained review publishing live in a new general skill, `github-pr-state`. | Separates PR creation (`github-pr`) from PR state reads and REQUEST_CHANGES/COMMENT publishing, preserving one-responsibility skills without duplicating mechanics. |
| 2026-09-20 | Technical implementation review lives in a new general skill, `implementation-review`. | Keeps judgment reusable and independent of GitHub mechanics and tracker writes, so `pr-review` can stay a pure orchestrator. |
| 2026-09-20 | User stories gain an append-only `## Review` note for PR-linked review outcomes. | Gives reviewed work durable context directly on the story without inventing a new tracker state; task status moves remain the only state machine writes. |
| 2026-09-20 | Rename general skill `implementation-review` to `code-review`. | The shorter name better describes the skill's purpose (technical code judgment against specs) and avoids confusion with the `pr-review` workflow orchestrator. |
| 2026-09-21 | GitHub approve and merge capability lives in a new general skill, `github-pr-merge`, respecting repository merge policy without admin bypass. | Keeps creation, state inspection, and merge mechanics in three disjoint general skills while preventing unsafe merge shortcuts. |
| 2026-09-21 | `pr-approve` is a user-invoked workflow helper after a clean `pr-review`; it requires explicit confirmation before approval and merge. | Fills the missing finalize step without inventing a new formal milestone phase. |
| 2026-09-21 | `github-pr-state` may publish `APPROVE`, `REQUEST_CHANGES`, or `COMMENT` when explicitly requested by the caller after confirmation. | Allows constrained approval publishing without breaking the existing review workflow responsibilities. |
| 2026-09-21 | Milestone merge evidence is recorded as `**Merged:** <timestamp> | <sha>` in the milestone charter after GitHub confirms an actual merge. | Makes merge status durable without writing premature or queue-only markers. |
| 2026-09-21 | `milestone-planning` refuses when any closed milestone still has an open or unmerged PR without a merge record. | Prevents starting the next milestone before the previous reviewed PR is actually merged or reconciled. |
| 2026-09-21 | User-facing workflow skill documentation lives in `docs/workflow/`, with `docs/README.md` as the index. | Separates user guides (navigable, detailed, aimed at skill users) from agent-facing `AGENTS.md` and human-facing `README.md`. The canonical skill definitions remain in `skills/workflow/*/SKILL.md`; `docs/` is a navigable summary. |
| 2026-09-21 | Document templates use versioned marker-delimited managed blocks (`<!-- kodit:<doc>:v1:start/end -->`) instead of heading-based idempotency. | Markers give a single, unambiguous idempotency mechanism: reruns replace the block in-place without touching surrounding content. Heading-only matching was fragile (variant spellings caused duplicates) and could not safely migrate legacy sections. |
| 2026-09-21 | Add `.github/workflows/validate-skills.yml` to validate all canonical skills on every push to `master`. | skills.sh indexes public GitHub repos passively; there is no publish API. The workflow runs `gh skill publish --dry-run` to enforce frontmatter and naming conventions in CI, making the public repo a valid skills.sh source. `GITHUB_TOKEN` with `contents: read` suffices because `--dry-run` swallows advisory remote-check errors. |
| 2026-09-21 | Add `.github/workflows/release-skills.yml` to create GitHub Releases on `v*` tag push, with `workflow_dispatch` for backfills. | GitHub Releases make tagged versions browsable and downloadable. `gh release create --verify-tag --generate-notes` is idempotent and never overwrites an existing release. skills.sh listing is independent — it depends on user installs, not GitHub Releases. Separate from validation to avoid releasing on every merge. |
| 2026-09-22 | Linear backend requires `workspace`, object-valued `team` with `key` and `id`, and object-valued `linear_project` with `id` and `name` in `kodit.json` (v2 schema). | Setup resolves all IDs during preflight and records them authoritatively; every subsequent operation uses resolved UUIDs. Prevents silent workspace/team drift. |
| 2026-09-22 | Provision mode reads the setup draft, not `kodit.json`, as the source of truth. `kodit.json` is written only by write mode after provisioning succeeds. | The setup → provision → write ordering requires provision to consume the draft (which contains all config) and append resolved IDs; write mode then produces the final `kodit.json`. This prevents provision from requiring a file that does not yet exist. |
| 2026-09-22 | Eval viewer recursively collects output files from nested directories under `outputs/`, preserving relative paths. | Subagents may mirror project structure (e.g. `.kodit/issues/`) into outputs. A flat scan misses these files, causing blank output panels. Recursive collection with relative path display handles any nesting. |
| 2026-09-22 | Eval definitions include `allow_remote_writes` and `resource_prefix` fields to enforce sandbox policy. Setup and baseline evals never make remote writes; only explicitly authorized provisioning evals may. | Prevents eval runs from accidentally mutating real Linear workspaces. The `resource_prefix` ensures any live-created resources are uniquely identifiable for cleanup. |
