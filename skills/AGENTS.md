# AGENTS.md

Instructions for coding agents working in `skills/`. This file governs the
`skills/` subtree. The root `AGENTS.md` remains the source of truth for the
canonical skill format; this file adds what that format means for the coding
agents this collection targets.

## Target Agents

These skills are authored for four coding agents:

- **opencode**
- **Claude Code**
- **Codex**
- **pi**

Every skill must work in all four. Keep skills agent-agnostic: no agent-specific
tool names, no per-agent instructions, no vendor-only frontmatter. Category and
dependency rules are in the root `AGENTS.md`.

## Cross-Agent Frontmatter Rules

Keep to the intersection the four agents share:

- `name` — lowercase kebab-case, 64 characters or fewer, and equal to the skill
  directory name. opencode requires the match; Claude Code derives its
  `/command` from the directory; pi is the only target that relaxes the rule.
- `description` — **500 characters or fewer**, the strictest limit across the
  four targets. State what the skill does and when to use it; front-load the
  concrete trigger keywords. This is tighter than the 1024-character limit some
  agents allow, so treat 500 as the ceiling.
- Optional shared fields only: `license`, `compatibility`, `metadata` (a
  string-to-string map). Do not add agent-specific fields.

Body rules — under 100 lines, the required section order, and conciseness — are
unchanged and live in the root `AGENTS.md`.

## Discovery Paths

A bare repo-root `skills/` is scanned by **none** of the four agents. Each reads
its own convention:

| Agent | Project scope | Global scope |
|---|---|---|
| opencode | `.opencode/skills/`, `.claude/skills/`, `.agents/skills/` | `~/.config/opencode/skills/`, `~/.claude/skills/`, `~/.agents/skills/` |
| Claude Code | `.claude/skills/` | `~/.claude/skills/` |
| Codex | `.agents/skills/` | `~/.agents/skills/` |
| pi | `.pi/skills/`, `.agents/skills/` | `~/.pi/agent/skills/`, `~/.agents/skills/` |

opencode and pi walk from the working directory up to the repo root; Codex does
the same for `.agents/skills/`. `.agents/skills/` is the only path three of the
four share — Claude Code does not read it.

## Testing a Skill

Symlink the skill directory into the agent's skills directory:

```bash
ln -s "$(pwd)/skills/general/NAME" ~/.agents/skills/NAME   # opencode, Codex, pi
ln -s "$(pwd)/skills/general/NAME" ~/.claude/skills/NAME   # Claude Code
```

Repo-scoped alternatives: list extra directories in opencode's `skills.paths`
config array or pi's settings `skills` array. Users install the published
collection with `npx skills add invoque/kodit` (see the root `README.md`).

## evals/

`evals/` directories are development-only: they hold test prompts and scripts and
are not part of a skill's runtime surface. Exclude `evals/` when copying,
symlinking, or publishing a skill for use.
