# kodit

> Opinionated spec-driven development for solo developers — works with any
> coding agent.

`kodit` is a small, explicit workflow that keeps a coding agent honest. You
capture what you want in a spec, agree on a plan, let the agent implement it,
then verify the result against the spec. No ceremony designed for teams, no
lock-in to a single vendor, no framework to install.

Everything is markdown. Every phase produces an artifact you can read, diff, and
commit.

## Why kodit

Coding agents are fast and confident, which is exactly what makes them risky on
an unbounded task. `kodit` constrains the work:

- **Spec before code.** Requirements are written down and agreed before any
  implementation starts.
- **Plan before execution.** The spec becomes an ordered list of verifiable
  tasks.
- **Review before done.** The implementation is checked against the spec, not
  against the agent's own summary of it.

The result is a paper trail you can trust: what you asked for, what was planned,
what changed, and what was verified.

## Objectives

- Give a solo developer a disciplined workflow without a team-sized process.
- Make every change traceable from requirement to implementation.
- Stay agent-agnostic: the same skills work with Claude Code, pi, opencode, or
  any agent that can read markdown instructions.
- Keep the whole system inspectable — plain files, no hidden state.

## Goals

- A complete, minimal set of skills covering the full workflow: spec → plan →
  implement → review → done.
- Agent-agnostic skill format that any coding agent can consume.
- Artifacts (specs, plans, review notes) stored as plain markdown in the repo.
- Zero runtime dependencies for the core workflow.
- Documentation that a solo developer can read in one sitting.

## Non-Goals

- Team and enterprise features (roles, approvals, multi-person handoff).
- Multi-agent orchestration or autonomous long-running agents.
- A hosted service, database, or proprietary format.
- Replacing your agent's own tools — `kodit` structures the work, it does not
  execute it.
- Runtime tooling (CLI, installer) in the first iteration. See [Roadmap](#roadmap).

## How It Works

Five phases, always in order. Each phase has a defined input, output, and exit
condition.

| Phase | What happens | Artifact |
|---|---|---|
| **spec** | The need is written down as explicit, testable requirements, free of implementation detail. | `specs/spec-NNN-<name>.md` |
| **plan** | The spec is turned into a technical approach with an ordered list of independently verifiable tasks. | `specs/plan-NNN-<name>.md` |
| **implement** | The tasks are executed exactly as planned — no added scope, no skipped tasks. | Code / skill files |
| **review** | Each task is verified against the spec; deltas and deviations are recorded. | Review notes in the plan |
| **done** | Docs and changelog are updated and the work is committed. | Final commit |

If a phase reveals a problem in an earlier one, you loop back and amend the
spec or plan — you do not quietly improvise during implementation.

## Skills

The workflow is delivered as skills. Skill names are planned to map one-to-one
onto workflow phases.

| Phase | Skill | Status |
|---|---|---|
| spec | `spec` | Planned |
| plan | `plan` | Planned |
| implement | `implement` | Planned |
| review | `review` | Planned |
| done | `done` | Planned |

> Status as of this bootstrap: **none of the skills exist yet.** This repository
> currently contains only the project documentation. Skill scaffolding is the
> first item on the [roadmap](#roadmap).

## Requirements

- A coding agent that can discover and follow skills in markdown form.
- `git` for version control.
- Optional: `python3` (with `pyyaml`) or `yq` to validate skill frontmatter.

There is no build step and nothing to install for the workflow itself.

## Installation

Until a CLI installer exists, install skills by copying or symlinking each
skill directory into your agent's skills directory.

Choose the skills directory your agent reads from:

| Agent | Typical skills directory |
|---|---|
| Claude Code | `~/.claude/skills/` |
| Agent-agnostic / pi | `~/.agents/skills/` |
| Project-local (any agent) | `<your-project>/.skills/` (follow your agent's convention) |

### Copy (simple, per-project snapshot)

```bash
git clone <repo-url> kodit
cp -R kodit/skills/<skill-name> ~/.claude/skills/
```

### Symlink (stays in sync with this repo)

```bash
git clone <repo-url> kodit
ln -s "$(pwd)/kodit/skills/<skill-name>" ~/.claude/skills/<skill-name>
```

Symlinks are recommended while `kodit` is under active development: a single
`git pull` updates every linked skill. Use copies when you want a pinned, stable
snapshot.

## Usage

Once a skill is installed, invoke it through your agent in plain language, or by
whatever trigger the skill's description declares. A typical solo session:

1. "Let's spec out an offline mode for the notes app." → the agent runs the
   **spec** skill and writes `specs/spec-003-offline-mode.md`.
2. "Plan that spec." → the agent runs the **plan** skill and writes
   `specs/plan-003-offline-mode.md` with ordered tasks.
3. "Implement the plan." → the agent works the tasks in order.
4. "Review the implementation against the spec." → the agent records findings
   in the plan.
5. "Wrap it up." → the agent runs the **done** skill: docs, changelog, commit.

Between phases you review the artifact and approve it. The agent does not start
the next phase until you do.

## Contributing

Contributions are welcome, and they follow the same workflow this project
prescribes.

1. **Open a spec first.** Describe the need and the requirements. Do not open an
   implementation PR without an agreed spec and plan.
2. **Keep skills agent-agnostic.** No vendor-specific instructions inside a
   skill — no "only for Claude", no agent-specific tool names.
3. **Follow the canonical skill format.** See `AGENTS.md` for the frontmatter
   and body structure.
4. **Validate frontmatter** before committing:

   ```bash
   python3 -c "import sys, yaml; yaml.safe_load(open(sys.argv[1]).read().split('---')[1])" \
     skills/<skill-name>/SKILL.md
   ```

5. **Use conventional commits** (`feat:`, `fix:`, `docs:`, `chore:`).
6. **Record decisions** in the `CONTEXT.md` decisions log.

See `AGENTS.md` for the full working contract that applies to human and agent
contributors alike.

## Roadmap

- [ ] Scaffold the five workflow skills (`spec`, `plan`, `implement`, `review`,
      `done`) with `SKILL.md` files.
- [ ] Add `references/` material for each skill where needed.
- [ ] Define the review checklist used by the `review` skill.
- [ ] Evaluate a CLI installer (e.g. `uv`- or `bun`-based) for skill
      installation.
- [ ] Add worked examples of a full spec → done cycle.

## License

No license has been chosen yet. Until one is added, all rights are reserved by
the author.
