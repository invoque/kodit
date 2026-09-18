# kodit

> Opinionated spec-driven development for solo developers — works with any
> coding agent.

`kodit` is a small, explicit workflow that keeps a coding agent honest. You
capture what you want in a spec, agree on a plan, let the agent implement it,
then verify the result against the spec. No team-sized ceremony, no vendor
lock-in, nothing to install. Everything is markdown, and every phase produces an
artifact you can read, diff, and commit.

## How It Works

Five phases, always in order. Each has a defined input, output, and exit
condition.

| Phase | What happens | Artifact |
|---|---|---|
| **spec** | The need is written down as explicit, testable requirements, free of implementation detail. | `specs/spec-NNN-<name>.md` |
| **plan** | The spec becomes a technical approach with ordered, independently verifiable tasks. | `specs/plan-NNN-<name>.md` |
| **implement** | The tasks are executed exactly as planned — no added scope, no skipped tasks. | Code / skill files |
| **review** | Each task is verified against the spec; deltas are recorded. | Review notes in the plan |
| **done** | Docs and changelog are updated and the work is committed. | Final commit |

If a phase reveals a problem in an earlier one, loop back and amend the spec or
plan — never improvise during implementation. The agent does not start a phase
until you approve the previous phase's artifact.

## Goals & Non-Goals

**Goals**

- A complete, minimal skill set covering the full workflow: spec → plan →
  implement → review → done.
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

The workflow is delivered as skills, one per phase.

| Phase | Skill |
|---|---|
| spec | `spec` |
| plan | `plan` |
| implement | `implement` |
| review | `review` |
| done | `done` |

None exist yet — this repository currently holds only project documentation.
Skill scaffolding is first on the [roadmap](#roadmap).

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
cp -R kodit/skills/<skill-name> ~/.claude/skills/

# Symlink (stays in sync with this repo — recommended during development)
ln -s "$(pwd)/kodit/skills/<skill-name>" ~/.claude/skills/<skill-name>
```

## Usage

Invoke skills through your agent in plain language. A typical session:

```text
You:  Let's spec out an offline mode for the notes app.
Agent: → writes specs/spec-003-offline-mode.md
You:  Plan that spec.
Agent: → writes specs/plan-003-offline-mode.md with ordered tasks
You:  Implement the plan.
Agent: → works the tasks in order
You:  Review the implementation against the spec.
Agent: → records findings in the plan
You:  Wrap it up.
Agent: → runs the done skill: docs, changelog, commit
```

You review and approve each artifact before the agent moves on.

## Contributing

Contributions follow the same workflow this project prescribes.

- **Spec first.** Describe the need and requirements before any implementation
  PR.
- **Stay agent-agnostic.** No vendor-specific instructions or agent-specific
  tool names inside a skill.
- **Follow the canonical format** defined in `AGENTS.md`.
- **Validate frontmatter** before committing:

  ```bash
  python3 -c "import sys, yaml; yaml.safe_load(open(sys.argv[1]).read().split('---')[1])" \
    skills/<skill-name>/SKILL.md
  ```

- **Use conventional commits** (`feat:`, `fix:`, `docs:`, `chore:`) and record
  decisions in the `CONTEXT.md` decisions log.
- **Work on `feature/*` branches.** `master` and `dev` are protected; see
  `AGENTS.md` for the full working contract.

## Roadmap

- [ ] Scaffold the five workflow skills with `SKILL.md` files.
- [ ] Add `references/` material and a review checklist for each skill.
- [ ] Evaluate a CLI installer (e.g. `uv`- or `bun`-based).
- [ ] Add a worked end-to-end spec → done example.

## License

No license chosen yet. All rights reserved by the author until one is added.
