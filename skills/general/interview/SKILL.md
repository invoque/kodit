---
name: interview
description: >-
  Use when the user wants to think something through with you before you build
  it — by being asked questions. Trigger when they say things like "interview
  me", "ask me whatever you need to know", or "question me until we've settled
  it"; when they bring a half-formed idea and need help pinning down
  requirements, scope, or what to actually build; when they're torn between
  design options or stuck on a decision; and before you write any spec, plan,
  PRD, or design for a feature, schema, or system that still has open decisions.
  Runs a structured Q&A, with rounds of pointed questions each carrying a
  recommendation, until every decision is settled and confirmed — nothing gets
  designed or implemented on guesses. Not for how-to questions, debugging,
  well-specified tasks, job-interview practice, or when the user says to skip
  questions and just use sensible defaults. When in doubt, interview rather
  than guess.
---

# Interview

Interview the user relentlessly until you share an understanding of what is
being designed, one round of questions at a time.

## Usage

Invoke this skill before acting on any request whose shape is not yet fully
settled — typically before writing a spec or plan, or at the start of a design
task. The user can also invoke it directly ("interview me", "ask me questions
first").

Inputs:

- **Topic** — what is being designed (a feature, a system, a change).
- **Context** — everything already known: the user's message, the conversation
  so far, the repository, any specs or docs. Decisions already settled here are
  part of the design tree from the start.

Outputs:

- One or more rounds of numbered questions, each with a strong recommendation.
- A scratch design-tree artifact in `.kodit/tmp/`.
- A final summary of the settled design and a request for the user to confirm
  shared understanding. **Nothing is implemented or acted on before that
  confirmation.**

## What You Must Do When Invoked

### 1. Seed the design tree

The topic is the root. Every decision that hangs off it is a node, and each
decision branches into the decisions that only make sense once it is settled.

Read the conversation and any available context first. Any decision the user
has already made is **settled** and must never be asked again — asking it
back is the surest way to make the interview feel like a form. Seed those
nodes as settled before your first round. Likewise, treat anything you can read
from the repository or files as already known; do not ask the user to recite
their own project back to you.

Only what the user actually stated, plus what you established from the
environment, is settled. Inferences about the user's preferences, priorities,
or budget are **not** facts. "It's a side project" does not mean "they want the
cheapest option"; if a recommendation depends on an inferred preference,
either ask about it as a question, or state it explicitly as a labeled
assumption in the round body ("assuming you'd rather avoid a new paid service
— correct me if not") and let the user confirm it. Never seed an inference
silently, and never let one do hidden work inside your reasoning.

### 2. Keep the scratch artifact current

Create and maintain `.kodit/tmp/design-tree-<topic>.md`, using lowercase
kebab-case for the topic. Record, for every node: a stable ID, the decision,
its parent, and whether it is **settled**, **open**, or **blocked** (waiting on
an in-flight fact or on a parent that is still open). Update it at the end of
every round.

Give each node its ID when you create it and never change it. A node's status
changes as the interview progresses; its ID does not. Stable IDs mean that
"node D7" refers to the same decision from the first round to the last, so you
and the user can both follow the thread.

This artifact exists because a real interview outlives a context window. If
you lose the thread, the tree is how you recover it. It is scratch: never
load-bearing. The invoking phase either promotes it into a permanent artifact
or lets it be discarded.

### 3. Compute the knowledge

The **knowledge** is every open decision whose prerequisites are already
settled — every question you can ask *now* without guessing at answers you
have not heard yet.

A question whose answer depends on another question still open in this round
belongs to a **later** round, not this one. Asking it now would force you to
guess, and guessed options are how interviews go wrong: the user picks from a
list you invented rather than the one their real constraints imply.

### 4. Find facts yourself; put decisions to the user

Facts are your job, not the user's. When a question needs a fact from the
environment — filesystem, tools, repository, docs — find it. Delegate the
lookup to a subagent when one is available; otherwise research it inline
yourself. Never ask the user for something you could look up.

Do not block on a fact-finding task. A running exploration is an unsettled
prerequisite, so only the questions downstream of it wait for it to report.
Ask the rest of the knowledge now.

Decisions are the user's job. Put each one to them and wait for the answer.
When an answer opens new decisions, add them to the tree as children of the
decision that created them.

### 5. Ask one round

Ask the whole knowledge in one round — not one question at a time, and not a
second round smuggled into the first. Order the questions
most-consequential-first, where consequence is how much the answer reshapes
the tree or unblocks. If more than roughly six questions are open at once,
ask the top of that order and let the rest wait for the next round; a wall of
questions makes the user skim, and skimmed answers are guesses again.

Number the questions continuously across the whole interview: round 2 starts
after round 1's last number, so a reference like "Q7" means one thing for the
entire session. Give each question up to three options with exactly one strong
recommendation. The template below shows the shape of a question, not a
per-round reset:

```
❓ **Q1** - **<question title>**: <question body, might be multiple paragraphs, including multiple choices>

➡️ <your recommended answer>

---

❓ **Q2** - **<question title>**: <question body, might be multiple paragraphs, including multiple choices>

➡️ <your recommended answer>
```

The recommendation exists so the user can move fast: a well-formed option plus
your reasoning is often enough for them to say "yes" or redirect in one word.
Say why you recommend it — the reasoning is what lets the user correct you
when their constraints differ from your assumptions.

Keep each question's options short. If a question genuinely has only two
sensible choices, offer two; never pad the list to reach three.

### 6. Wait, then reshape

Wait for the user's answers before the next round. Do not proceed on assumed
answers and do not start work in parallel.

When the answers arrive, mark those nodes settled, add the child decisions they
reveal, and recompute the knowledge. Settled decisions push the knowledge
outward and unblock what depended on them. Then ask the next round.

If an answer is ambiguous, keep its node open and ask a sharper version of the
question next round. If an answer contradicts an earlier settled decision,
surface the conflict and reopen the affected branch rather than silently
picking one. If the user genuinely cannot decide, recommend a default and ask
them to confirm or override it explicitly — an explicit default is a decision;
a silent assumption is not.

### 7. Stop when the knowledge is empty

The interview is done when the knowledge is empty: every branch of the tree has
been visited and nothing is left silently assumed. Present the full settled
design tree as a summary — the decisions, their answers, and any facts you
established — and ask the user to confirm that this matches their
understanding.

### 8. Do not act until confirmed

Do not write the spec, generate the plan, or make any change until the user
confirms shared understanding. If they correct the summary, reopen the affected
branches and run another round. If they confirm, the interview ends and the
invoking phase takes over with the settled tree.

## Notes on approach

- **One round at a time** is what keeps the interview honest. Batching the
  frontier forces every current question to be answerable from what the user
  has already said, which is exactly the bar for asking it.
- **Never guess a user decision.** A guessed decision is invisible: it looks
  like agreement until the work is built on it. The tree exists to make every
  decision visible and owned. An inferred preference is a guess wearing a
  fact's clothing — surface it as a question or a labeled assumption.
- **Never make the user do your research.** Asking the user for a fact you
  could have looked up spends their attention on the one thing they delegated
  to you.
- **Depth over volume.** A question that merely checks a box wastes a round.
  Ask what genuinely branches the design.
