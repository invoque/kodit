# Skill Authoring Guide

Writing patterns adapted from Anthropic's `skill-creator`, adjusted for Hermes Agent.
Load this when writing or revising a skill's body.

## Contents

- [Anatomy](#anatomy)
- [Progressive disclosure](#progressive-disclosure)
- [Writing the description](#writing-the-description)
- [Writing the body](#writing-the-body)
- [Section order (Hermes house style)](#section-order-hermes-house-style)
- [Output format templates](#output-format-templates)
- [Examples](#examples)
- [Domain organization](#domain-organization)
- [Common mistakes](#common-mistakes)

## Anatomy

```
skill-name/
├── SKILL.md (required)
│   ├── YAML frontmatter (name, description required)
│   └── Markdown instructions
└── Bundled resources (optional)
    ├── scripts/    - Executable code for deterministic/repetitive tasks
    ├── references/ - Docs loaded into context as needed
    └── assets/     - Files used in output (templates, icons, fonts)
```

Put logic that must run identically every time in `scripts/`; knowledge the agent reads
selectively in `references/`; files the skill produces or fills in `assets/`.

## Progressive disclosure

Hermes loads a skill in three levels:

1. **Metadata** (~100 tokens): `name` + `description`, present for all skills.
2. **Instructions** (target < 5000 tokens): the full `SKILL.md` body, loaded on trigger.
3. **Resources** (as needed): `scripts/`, `references/`, `assets/`, loaded only when used.

Keep `SKILL.md` under 500 lines; when approaching the limit, split detail into `references/`
and leave a pointer. Reference files cost nothing until read, so prefer several focused files
over one large one. For reference files over ~300 lines, add a table of contents.

## Writing the description

The description does both jobs: **what** the skill does and **when** to use it.

- Put all "when to use" information here, not in the body.
- Include concrete keywords the user would actually type.
- Be slightly pushy to counter under-triggering: instead of "How to build a dashboard",
  write "…whenever the user mentions dashboards, data visualization, internal metrics, or
  wants to display company data, even if they don't explicitly ask for a 'dashboard.'"
- Stay within 1024 characters. Dense and specific beats long and vague.
- The compact index uses a ≤60-char form; lead with the essential noun phrase so it reads
  well truncated.

## Writing the body

- Use the **imperative form** ("Extract the table", not "The agent should extract…").
- Address the agent directly; do not narrate.
- Be concrete: name exact tools, commands, endpoints, and file paths.
- Explain *why* for non-obvious steps so the agent can adapt when conditions differ.
- Do not pad with restatements of the frontmatter.

## Section order (Hermes house style)

```markdown
# Skill Title

Brief intro.

## When to Use

Trigger conditions — when should the agent load this skill?

## <Workflow / Steps>

Tables of common commands or API calls; step-by-step instructions.

## Pitfalls

Known failure modes and how to handle them.

## Verification

How the agent confirms it worked.
```

Adapt the middle sections to the skill; keep the `When to Use`, `Pitfalls`, and
`Verification` sections, which Hermes uses as its authoring standard.

## Output format templates

When the skill must produce a fixed structure, state it explicitly:

```markdown
## Report structure

ALWAYS use this exact template:

# [Title]

## Executive summary

## Key findings

## Recommendations
```

## Examples

Include worked examples when the task benefits from them, ideally pairing input with
output:

```markdown
### Example

Input: "summarize this PDF"
Output: a 3-bullet summary followed by the extracted tables as Markdown.
```

Keep examples minimal — enough to pin the format, not a tutorial.

## Domain organization

When a skill covers several variants (clouds, frameworks, languages), organize by variant
and let the agent read only the relevant file:

```
cloud-deploy/
├── SKILL.md (workflow + selection)
└── references/
    ├── aws.md
    ├── gcp.md
    └── azure.md
```

## Common mistakes

- **Vague description** ("Helps with PDFs") — will not trigger reliably.
- **Everything in SKILL.md** — split detail into `references/`.
- **Invented tools or commands** — Hermes fails at runtime; verify every name.
- **Deep reference chains** — keep references one level deep from `SKILL.md`.
- **Mixed runtimes** — no Claude Code, Codex, or other agents' tools.
- **Over-broad `requires_*`** — hides the skill when needed; keep requirements minimal.
- **Secrets in the body** — use `required_environment_variables` instead.
