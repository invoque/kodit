# Hermes Skill Format Reference

The authoritative on-demand reference for `SKILL.md` frontmatter in Hermes Agent. Load this
when drafting or validating a skill's frontmatter.

Source: https://hermes-agent.nousresearch.com/docs/developer-guide/creating-skills and
https://agentskills.io/specification

## Contents

- [Directory layout](#directory-layout)
- [Core frontmatter](#core-frontmatter)
- [Hermes-specific frontmatter](#hermes-specific-frontmatter)
- [Platforms](#platforms)
- [Conditional activation](#conditional-activation)
- [Secrets: required environment variables](#secrets-required-environment-variables)
- [Non-secret config](#non-secret-config)
- [Credential files](#credential-files)
- [Blueprint (scheduled automations)](#blueprint-scheduled-automations)
- [Full example](#full-example)
- [Validation checklist](#validation-checklist)

## Directory layout

```
skill-name/
├── SKILL.md          # Required: frontmatter + Markdown instructions
├── scripts/          # Optional: executable code (Python, Bash, JS)
├── references/       # Optional: docs loaded on demand
├── assets/           # Optional: templates, images, data files
└── ...               # Any additional files or directories
```

The skill directory name **must equal** the frontmatter `name`. In this repository skills
live under a category directory: `general/<skill-name>/SKILL.md`,
`tools/<skill-name>/SKILL.md`, or `workflow/<skill-name>/SKILL.md`.

## Core frontmatter

| Field | Required | Constraints |
| --- | --- | --- |
| `name` | Yes | Max 64 chars. Lowercase `a-z`, digits `0-9`, hyphens `-` only. Must not start or end with `-`. Must not contain `--`. Must match the parent directory name. |
| `description` | Yes | Max 1024 chars, non-empty. State **what** it does and **when** to use it. This is the primary trigger. |
| `license` | No | License name or reference to a bundled license file. |
| `compatibility` | No | Max 500 chars. Environment requirements. Prefer Hermes-native fields below where possible. |
| `metadata` | No | Map of string keys to string values. Hermes nests under `metadata.hermes`. |
| `allowed-tools` | No | Space-separated pre-approved tools. **Experimental**; support varies. |

Valid `name` examples: `pdf-processing`, `data-analysis`, `skill-creator`.
Invalid: `PDF-Processing` (uppercase), `-pdf` (leading hyphen), `pdf--processing`
(consecutive hyphens), `my_skill` (underscore).

## Hermes-specific frontmatter

```yaml
---
name: my-skill
description: What it does and when to use it.
version: 1.0.0
author: Your Name
license: MIT
platforms: [macos, linux]
metadata:
  hermes:
    tags: [Category, Subcategory, Keywords]
    related_skills: [other-skill-name]
    requires_toolsets: [web]
    requires_tools: [web_search]
    fallback_for_toolsets: [browser]
    fallback_for_tools: [browser_navigate]
    config:
      - key: my.setting
        description: What this setting controls
        default: sensible-default
        prompt: Display prompt for setup
    blueprint:
      schedule: "0 9 * * *"
      deliver: origin
      prompt: Task instruction for each run
      no_agent: false
required_environment_variables:
  - name: MY_API_KEY
    prompt: Enter your API key
    help: Get one at https://example.com
    required_for: API access
required_credential_files:
  - path: google_token.json
    description: Google OAuth2 token (created by setup script)
---
```

Hermes also supports the legacy alias `prerequisites.env_vars` for required env vars.

## Platforms

`platforms` restricts the skill to specific operating systems. When set, the skill is hidden
from the system prompt, `skills_list()`, and slash commands on incompatible platforms.
Omitted or empty means it loads on all platforms.

```yaml
platforms: [macos]              # macOS only (e.g. iMessage, Apple Reminders)
platforms: [macos, linux]       # macOS and Linux
platforms: [windows]            # Windows only
```

Valid values: `macos`, `linux`, `windows`.

## Conditional activation

Four fields under `metadata.hermes` control whether the skill appears in the system prompt,
based on the tools/toolsets available in the session:

| Field | Behavior |
| --- | --- |
| `requires_toolsets` | Hidden when ANY listed toolset is **not** available |
| `requires_tools` | Hidden when ANY listed tool is **not** available |
| `fallback_for_toolsets` | Hidden when ANY listed toolset **is** available |
| `fallback_for_tools` | Hidden when ANY listed tool **is** available |

- `fallback_for_*` marks the skill a backup, shown only when a primary tool is missing.
  Example: `duckduckgo-search` with `fallback_for_tools: [web_search]`.
- `requires_*` marks a skill that needs specific capabilities.
  Example: a scraping workflow with `requires_toolsets: [web]`.
- If both are specified, both must be satisfied. If neither, the skill is always shown.

Example:

```yaml
metadata:
  hermes:
    fallback_for_tools: [web_search]   # show only when web_search is unavailable
```

## Secrets: required environment variables

Use `required_environment_variables` for API keys and tokens.

```yaml
required_environment_variables:
  - name: TENOR_API_KEY
    prompt: Tenor API key
    help: Get your key at https://tenor.com
    required_for: GIF search functionality
```

- Missing values do **not** hide the skill; they trigger a secure CLI-only prompt on load.
- Set values are automatically passed through to `execute_code` and `terminal` sandboxes
  (including remote backends), so scripts can read `$TENOR_API_KEY` /
  `os.environ["TENOR_API_KEY"]`.
- Secrets are stored in `~/.hermes/.env` and are never exposed to the model.
- In gateway/messaging sessions, users get local setup guidance instead of in-band prompts.

Each entry: `name` (required), `prompt` (optional), `help` (optional), `required_for`
(optional).

## Non-secret config

Use `metadata.hermes.config` for paths, preferences, and other non-sensitive values.

```yaml
metadata:
  hermes:
    config:
      - key: myplugin.path
        description: Path to the plugin data directory
        default: "~/myplugin-data"
        prompt: Plugin data directory path
      - key: myplugin.domain
        description: Domain the plugin operates on
        prompt: Plugin domain (e.g., AI/ML research)
```

Each entry: `key` (required dotpath), `description` (required), `default` (optional),
`prompt` (optional).

Behavior:

- Stored in `config.yaml` under `skills.config.<key>`.
- `hermes config migrate` prompts for unconfigured settings; they appear in
  `hermes config show`.
- At load, resolved values are appended to the skill message, e.g.
  `[Skill config (from ~/.hermes/config.yaml): myplugin.path = /home/user/my-data]`.
- Manual: `hermes config set skills.config.myplugin.path ~/my-data`.

Rule of thumb: secrets → `required_environment_variables`; everything else → `config`.

## Credential files

Use `required_credential_files` for file-based credentials (typically OAuth token files
produced by a setup script).

```yaml
required_credential_files:
  - path: google_token.json
    description: Google OAuth2 token (created by setup script)
```

- `path` is relative to `~/.hermes/`.
- Missing files trigger `setup_needed`.
- Existing files are mounted read-only into Docker containers, synced into Modal sandboxes
  (at creation and before each command), and used directly on the local backend.

## Blueprint (scheduled automations)

`metadata.hermes.blueprint` marks a skill as a runnable automation.

```yaml
metadata:
  hermes:
    blueprint:
      schedule: "0 9 * * *"     # cron expr / "every 2h" / ISO timestamp
      deliver: origin           # optional, default origin
      prompt: Task instruction for each run   # optional
      no_agent: false           # optional
```

## Full example

```yaml
---
name: arxiv-search
description: Search arXiv for papers by topic, author, or category, and summarize results. Use when the user asks about academic papers, preprints, or arXiv.
version: 1.0.0
author: invoque
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [research, papers, arxiv]
    related_skills: [literature-review]
    requires_toolsets: [terminal]
required_environment_variables:
  - name: SEMANTIC_SCHOLAR_API_KEY
    prompt: Semantic Scholar API key
    help: https://www.semanticscholar.org/product/api
    required_for: citation data
---

# arXiv Search

Search and summarize arXiv papers via the public API.

## When to Use

Use when the user mentions arXiv, preprints, papers, or academic literature search.

## Steps

1. Build the query string and call the API with `terminal` (`curl`).
2. Parse the Atom response.
3. Summarize the top results with title, authors, date, and abstract.

## Pitfalls

- The API rate-limits bursts; add a short delay between calls.
- Category identifiers are case-sensitive.

## Verification

Confirm at least one result parses into title + authors + date before summarizing.
```

## Validation checklist

Before considering the frontmatter done:

- [ ] `name` equals the parent directory name.
- [ ] `name` is 1–64 chars, lowercase/digits/hyphens only, no leading/trailing hyphen, no `--`.
- [ ] `description` is 1–1024 chars and states both the what and the when.
- [ ] `platforms` (if present) uses only `macos`, `linux`, `windows`.
- [ ] Conditional fields (`requires_*`, `fallback_for_*`) reference real Hermes tools or
      toolsets.
- [ ] Secrets use `required_environment_variables`; non-secrets use `config`.
- [ ] OAuth files use `required_credential_files`.
- [ ] `metadata.hermes.tags` present and meaningful.

Optional: run `skills-ref validate <skill-dir>` if the reference validator is available.
