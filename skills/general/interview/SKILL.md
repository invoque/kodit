---
name: interview
description: >-
  Use when a request is not yet fully settled and the user wants it thought
  through by being asked questions — "interview me", "ask me whatever you need
  to know" — is torn between options, or is about to have a spec, plan, PRD, or
  design written. Runs numbered rounds of questions, each with a strong
  recommendation, until every decision is settled and confirmed. Not for
  how-to, debugging, well-specified tasks, or "skip the questions". When in
  doubt, interview rather than guess.
---

# Interview

Interview the user relentlessly until you share an understanding of what is
being designed, one round of questions at a time.

## Usage

Invoke before acting on any request whose shape is not fully settled,
typically before writing a spec or plan; the user can also invoke it directly
("interview me").

Inputs: the **topic** being designed, and all known **context** (the message,
conversation, repository, any specs) — decisions settled there seed the design
tree. Outputs: rounds of numbered questions with recommendations; a scratch
design-tree artifact in `.kodit/tmp/`; and a final summary the user confirms.
**Nothing is acted on before that confirmation.** Formats: `references/formats.md`.

## What You Must Do When Invoked

### 1. Seed the design tree

The topic is the root; each decision hanging off it is a node, and each decision
branches into the decisions that only make sense once it is settled. Read the
conversation and context first: any decision the user already made is **settled**
and must never be asked again, and anything readable from the repository is
already known.

Only what the user stated, plus what you established from the environment, is
settled. Inferences about preferences, priorities, or budget are **not** facts —
"it's a side project" does not mean "they want the cheapest option". If a
recommendation depends on an inferred preference, either ask it or state it as a
labeled assumption in the round body ("assuming you'd rather avoid a new paid
service — correct me if not"). Never seed an inference silently.

### 2. Keep the scratch artifact current

Create and maintain `.kodit/tmp/design-tree-<topic>.md` (format in
`references/formats.md`). Give each node a stable ID on creation and never change
it: statuses change, IDs do not, so "node D7" means one decision from first round
to last. Update it every round — it is how you recover the thread if the
interview outlives the context window. It is scratch, never load-bearing: the
invoking phase promotes it or discards it.

### 3. Compute the knowledge

The **knowledge** is every open decision whose prerequisites are already
settled — every question you can ask *now* without guessing at answers you have
not heard. A question that depends on another still open this round belongs to a
**later** round; asking it now forces you to invent options.

### 4. Find facts yourself; put decisions to the user

Facts are your job. When a question needs a fact from the environment —
filesystem, tools, repository, docs — find it: delegate to a subagent when one
is available, otherwise research inline. Never ask the user for something you
could look up. Do not block on a fact-finding task: a running exploration is an
unsettled prerequisite, so only questions downstream of it wait.

Decisions are the user's job. Put each one to them and wait. When an answer
opens new decisions, add them to the tree as children of the one that created
them.

### 5. Ask one round

Ask the whole knowledge in one round — not one question at a time, and not a
second round smuggled into the first. Order most-consequential-first, where
consequence is how much the answer reshapes the tree or unblocks. If more than
roughly six are open, ask the top of that order and let the rest wait; a wall of
questions gets skimmed, and skimmed answers are guesses again.

Number questions continuously across the interview: round 2 continues after
round 1's last number, so "Q7" means one thing for the session. Use the question
format in `references/formats.md`: up to three short options and exactly one
strong recommendation, with reasoning, per question. Depth over volume.

### 6. Wait, then reshape

Wait for the answers before the next round; do not proceed on assumed answers or
start work in parallel. When they arrive, mark those nodes settled, add the
child decisions they reveal, and recompute the knowledge — settled decisions
push it outward and unblock what depended on them.

If an answer is ambiguous, keep its node open and ask a sharper version next
round. If it contradicts an earlier settled decision, surface the conflict and
reopen that branch rather than silently picking one. If the user cannot decide,
recommend a default and ask them to confirm or override it explicitly — an
explicit default is a decision; a silent assumption is not.

### 7. Stop when the knowledge is empty

Done means the knowledge is empty: every branch visited and nothing silently
assumed. Present the settled design tree — decisions, answers, and established
facts — as a summary, and ask the user to confirm it matches their understanding.

### 8. Do not act until confirmed

Do not write the spec, generate the plan, or make any change until the user
confirms. If they correct the summary, reopen the affected branches; if they
confirm, the interview ends and the invoking phase takes over with the tree.
