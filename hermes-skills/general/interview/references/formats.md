# Interview Reference Formats

Read this when seeding the design tree (artifact format) or emitting a round
(question format).

## Design-tree artifact format

Maintain one file per interview at `<scratch-dir>/design-tree-<topic>.md`, where
`<scratch-dir>` is the skill config `interview.scratch_dir` (default
`.kodit/tmp`) and `<topic>` is lowercase kebab-case. Create the directory with
`terminal` (`mkdir -p`) if it does not exist.

One row per node, with a stable ID, the decision, its parent, and status:

```markdown
# Design tree — <topic>

| ID | Decision | Parent | Status |
|---|---|---|---|
| D1 | <the decision> | — | settled: <answer> |
| D2 | <the decision> | D1 | open |
| D3 | <the decision> | D2 | blocked: waiting on <fact / parent> |
```

Status is `settled` (the user answered it or you established it as a fact),
`open`, or `blocked`. Update the file at the end of every round. IDs are stable
from creation: statuses change, IDs never do, so "node D7" means one decision
from first round to last.

## Question format

Each question shows up to three options and exactly one strong recommendation
after `➡️`. Numbering runs continuously across the whole interview: round 2
continues after round 1's last number, so "Q7" means one thing for the session.

```
❓ **Q1** - **<question title>**: <question body, might be multiple paragraphs, including multiple choices>

➡️ <your recommended answer>

---

❓ **Q2** - **<question title>**: <question body, might be multiple paragraphs, including multiple choices>

➡️ <your recommended answer>
```

Say why you recommend the answer: the reasoning is what lets the user correct
you when their constraints differ from your assumptions. Keep options short; if
a question has only two sensible choices, offer two.
