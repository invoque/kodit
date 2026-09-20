# kodit

> Opinionated milestone-driven development for solo developers — works with any
> coding agent.

`kodit` is a small, explicit workflow that keeps a coding agent honest. You
agree a milestone's scope, then work it item by item: capture what you want in a
spec, agree on a plan, let the agent implement it, and verify the result against
the spec. No team-sized ceremony, no vendor lock-in, nothing to install. Every
artifact is markdown you can read, diff, and commit.

## How It Works

Six phases, always in order, forming a milestone loop:

| Phase | What happens |
|---|---|
| **setup** | `kodit` is initialized in the project: configuration is written and the temporary workspace is created. |
| **milestone-planning** | The scope of the next milestone is agreed and recorded. |
| **implement** | Each milestone item is worked to completion. |
| **review-loop** | Each implemented item is verified against its spec; deltas are recorded. |
| **milestone-review** | The milestone's goal is confirmed and a retrospective is captured. |
| **done** | Docs and changelog are updated and the milestone is committed. |

Inside `implement` and `review-loop`, every milestone item runs the same inner
loop: **spec → plan → implement → review**. An item is never implemented without
an approved spec and plan, and an approved spec or plan is never edited mid-flight
— amend it with a new spec or a dated changelog entry.

The detailed steps and artifacts for each phase are defined by that phase's
skill, not by this overview.

## Goals & Non-Goals

**Goals**

- A complete, minimal skill set covering the full milestone workflow:
  setup → milestone-planning → implement → review-loop → milestone-review → done.
- An agent-agnostic skill format any coding agent can consume.
- Artifacts stored as plain markdown in the repo.
- Zero runtime dependencies for the core workflow.
- Documentation a solo developer can read in one sitting.

**Non-Goals**

- Team and enterprise features (roles, approvals, multi-person handoff).
- Multi-agent orchestration or autonomous long-running agents.
- A hosted service, database, or proprietary format.
- Replacing your agent's own tools — `kodit` structures the work, it does not
  execute it.

## Skills

Skills come in two categories:

```
skills/
├── workflow/    # one skill per workflow phase — sequences the phase and
│                # invokes general skills as needed
└── general/     # single-purpose capabilities with no phase knowledge, e.g.
                 # interviewing the user, setting up kodit, or talking to your
                 # issue tracker
```

- **Workflow skills** own one phase each: they sequence it, enforce its entry
  and exit criteria, and call general skills by relative path.
- **General skills** are reusable capabilities with a single responsibility.
  They never depend on a workflow skill or a phase.
- The two categories never overlap: every skill does exactly one thing, and
  names are unique across both.

The specific skills are defined as they are built — see the
[roadmap](#roadmap). The `setup`, `milestone-planning`, and `implement` phases'
skills (`setup-kodit`, `milestone-planning`, `implement`) exist along with their
general companions (`kodit-config`, `issue-tracker`, `git-branching`,
`plan-writing`, `github-pr`, `github-pr-state`, `github-pr-merge`,
`code-review`) and `interview`; the `pr-request` workflow exists and hands off
to the new `pr-review` workflow, and the new `pr-approve` workflow finalizes a
reviewed milestone PR, while the remaining phase skills are still to come.

## Getting Started

Requirements:

- A coding agent that discovers and follows skills in markdown form.
- `git` for version control.
- Optional: `python3` (with `pyyaml`) or `yq` to validate skill frontmatter.

Until a CLI installer exists, install a skill by copying or symlinking its
directory into your agent's skills directory:

| Agent | Skills directory |
|---|---|
| Claude Code | `~/.claude/skills/` |
| Agent-agnostic / pi | `~/.agents/skills/` |
| Project-local | follow your agent's convention |

```bash
# Copy (simple, pinned snapshot)
git clone <repo-url> kodit
cp -R kodit/skills/general/<skill-name> ~/.claude/skills/

# Symlink (stays in sync with this repo — recommended during development)
ln -s "$(pwd)/kodit/skills/general/<skill-name>" ~/.claude/skills/<skill-name>
```

Adopting `kodit` in a project is done by its `setup-kodit` skill. It writes
`kodit.json` at the project root, appends `kodit` sections to `AGENTS.md`,
`README.md`, and `CONTEXT.md` (creating them if absent), and creates `.kodit/`
with a committed file-based issue tracker and a gitignored `tmp/` area. Add
`.kodit/tmp/` to your `.gitignore` — temporary artifacts are never committed —
but keep `.kodit/issues/` under version control.

## Usage

Invoke skills through your agent in plain language. A typical milestone:

```text
You:  Set up kodit in this project.
Agent: → runs setup: writes kodit.json, creates .kodit/tmp/
You:  Let's plan the next milestone.
Agent: → runs milestone-planning and agrees the milestone scope with you
You:  Start implementing.
Agent: → runs implement: a spec and plan per item, then implements each
You:  Reset the milestone for review.
Agent: → runs review-loop, then milestone-review
You:  Wrap it up.
Agent: → runs done: docs, changelog, commit
```

You approve each spec and plan before the agent implements it.

## Contributing

Contributions follow the same workflow this project prescribes.

- **Spec first.** Describe the need and requirements before any implementation
  PR.
- **Stay agent-agnostic.** No vendor-specific instructions or agent-specific
  tool names inside a skill.
- **Follow the canonical format** defined in `AGENTS.md`, including the
  conciseness standard: a `SKILL.md` body under 100 lines and a `description` of
  at most ~80 words.
- **Validate frontmatter** before committing:

  ```bash
  python3 -c "import sys, yaml; yaml.safe_load(open(sys.argv[1]).read().split('---')[1])" \
    skills/<category>/<skill-name>/SKILL.md
  ```

- **Use conventional commits** (`feat:`, `fix:`, `docs:`, `chore:`) and record
  decisions in the `CONTEXT.md` decisions log.
- **Work on `feature/*` branches.** `master` and `dev` are protected; see
  `AGENTS.md` for the full working contract.

## Roadmap

- [ ] Scaffold the six workflow skills with `SKILL.md` files (`setup-kodit`,
      `milestone-planning`, and `implement` done; `review-loop`,
      `milestone-review`, `done` to come).
- [x] Define the first general skills as the workflow skills need them
      (`interview`, `kodit-config`, `issue-tracker`, `git-branching`,
      `plan-writing`).
- [ ] Add `references/` material and a review checklist for each skill.
- [ ] Evaluate a CLI installer (e.g. `uv`- or `bun`-based).
- [ ] Add a worked end-to-end milestone example.

## License

No license chosen yet. All rights reserved by the author until one is added.
