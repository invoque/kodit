# Interview reference formats

Read this when seeding the tree (design-tree artifact format) or emitting a
round (question format).

## Design-tree artifact format

`.kodit/tmp/design-tree-<topic>.md`, lowercase kebab-case topic. One entry per
node, with a stable ID, the decision, its parent, and status:

```markdown
# Design tree — <topic>

| ID | Decision | Parent | Status |
|---|---|---|---|
| D1 | <the decision> | — | settled: <answer> |
| D2 | <the decision> | D1 | open |
| D3 | <the decision> | D2 | blocked: waiting on <fact / parent> |
```

Status is `settled` (user answered it or you found it as a fact), `open`, or
`blocked`. Update the file at the end of every round.

## Question format

Each question shows up to three options and exactly one strong recommendation
after `➡️`. The template shows the shape of a question, not a per-round reset —
numbering runs continuously across the whole interview.

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
