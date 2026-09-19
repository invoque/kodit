# spec-001 — `interview` general skill

**Status:** approved
**Date:** 2026-09-19
**Milestone item:** the first skill in the repository

## Summary

Create the `interview` general skill: a reusable capability an agent invokes to
relentlessly interview a user until the two share an understanding of what is
being designed. The skill maps the conversation as a **design tree**, advances
it one **round** at a time, and refuses to act until the user confirms the
understanding.

## Problem

Agents routinely start building from an underspecified request, silently
assuming answers to decisions the user never made. The failure is invisible at
the time and expensive later: the agent guesses a storage engine, an auth
strategy, or a scope boundary, and the user discovers the guess only when it is
built.

`kodit` is spec-driven, so every milestone item should begin from a shared
understanding. Nothing in the repository yet produces that understanding. The
governing documents (`CONTEXT.md`, `README.md`, `AGENTS.md`) all name
"interviewing the user" as the prototypical `general` skill, so this is the
natural first skill.

## Requirements

### R1 — Relentless until shared understanding

The interview does not stop at the first set of questions. It continues until
every branch of the design tree has been visited and nothing is left silently
assumed. It must not begin acting on the resulting design until the user
explicitly confirms shared understanding.

### R2 — The design tree

The interview is modeled as a tree of decisions:

- The root is the topic being designed.
- Every decision is a node. A decision branches into the decisions that hang
  off it (the ones that only make sense once it is settled).
- A node is **settled** when the user has answered it, or the agent has
  discovered it as a fact.

### R3 — The knowledge (frontier)

The **knowledge** is the set of decisions whose prerequisites are already
settled: every open node whose parent decisions are all settled. These are the
questions that can be asked *now* without guessing at answers that have not
been heard yet. A question whose answer depends on another question still open
in the current round belongs to a **later** round.

### R4 — Rounds

- Ask the whole knowledge in one round. Number each question (`Q1`, `Q2`, …).
- Each question shows up to three options and exactly one strong
  recommendation, marked with `➡️`.
- Then **wait** for the user's answers before the next round.
- Each round of answers reshapes the tree: settled decisions push the knowledge
  outward and unblock questions that depended on them. Recompute the knowledge
  and ask the next round.

The round format is fixed:

```
❓ **Q1** - **<question title>**: <question body, might be multiple paragraphs, including multiple choices>

➡️ <your recommended answer>

---

❓ **Q2** - **<question title>**: <question body, might be multiple paragraphs, including multiple choices>

➡️ <your recommended answer>
```

### R5 — Facts vs. decisions

- **Facts are the agent's job.** When a question needs a fact from the
  environment (filesystem, tools, repository, documentation), find it — by
  delegating to a subagent when one is available, otherwise by researching
  inline. Never ask the user for something that can be looked up.
- **Decisions are the user's job.** Every decision is put to the user and the
  interview waits for the answer.
- The agent must not block on facts. A running exploration is an unsettled
  prerequisite, so only the questions downstream of it wait for the subagent to
  report; the rest of the knowledge is asked now.

### R6 — Scratch artifact

While the interview runs, the design tree is maintained in a temporary markdown
artifact in `.kodit/tmp/`, named in lowercase kebab-case
(e.g. `design-tree-<topic>.md`). It records the tree, which nodes are settled,
which are open, and which are blocked by in-flight research. It is never
load-bearing: at the end the tree is either promoted into a permanent artifact
by the invoking phase or discarded.

### R7 — Terminal summary and confirmation gate

The session is done when the knowledge is empty: every branch of the design
tree has been visited and nothing is left silently assumed. At that point the
skill presents the full settled design tree as a summary and asks the user to
confirm shared understanding. It does not act on the design until the user
confirms.

### R8 — Canonical format (constraints from the repository)

- Location: `skills/general/interview/SKILL.md`.
- Frontmatter: exactly `name` and `description`; `name` matches the directory.
- Body: `# <Title>`, one-line purpose, `## Usage`, `## What You Must Do When
  Invoked` with discrete numbered steps.
- Agent-agnostic: no vendor-specific instructions or agent-specific tool names.

## Non-requirements

- No runtime code, scripts, or dependencies.
- No phase knowledge: the skill must not mention any workflow phase.
- No persistence of the design beyond the scratch artifact and the terminal
  summary; promotion is the invoking phase's job.
- No quantitative benchmark: the output is conversational and judged
  qualitatively by the user.

## Acceptance criteria

1. `skills/general/interview/SKILL.md` exists and its frontmatter parses as
   YAML with exactly `name` and `description`; `name` is `interview`.
2. Reading the skill, an agent can execute the interview end to end: seed the
   tree, compute the knowledge, ask one round in the fixed format with one
   strong recommendation per question, wait, reshape, repeat.
3. The skill instructs the agent to find facts itself (subagent if available,
   otherwise inline) and never ask the user for them.
4. The skill contains the confirmation gate and forbids acting before the user
   confirms shared understanding.
5. The skill maintains the design tree in `.kodit/tmp/design-tree-<topic>.md`.
6. The skill contains no workflow-phase references and no vendor-specific
   tool names.
7. Qualitative eval: on the test prompts in Appendix A, the with-skill output
   visibly runs rounds in the fixed format and does not re-ask settled
   decisions, while the baseline does not.

## Appendix A — Test prompts (qualitative eval)

1. **Greenfield feature.** "I want to add API rate limiting to my side project.
   It's a FastAPI service with Postgres, deployed on Fly.io. Help me work out
   what to build."
2. **Hidden prerequisites.** "I'm building a CLI for tracking my reading habits
   in Go. Figure out the design with me before I start."
3. **Partially settled.** "I'm sketching a small expense-splitting app for my
   flatmates. We already decided: SQLite, no accounts/multi-user sync, and a
   simple web UI — not a mobile app. Help me nail down the rest."
