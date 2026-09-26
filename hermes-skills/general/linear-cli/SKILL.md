---
name: linear-cli
description: Manage Linear issues, projects, teams, and documents from the command
  line with the `linear` CLI (@schpet/linear-cli). Query and update issues, create
  issues and comments with file-based markdown, use templates, labels, cycles, and
  initiatives, with a raw GraphQL fallback. Use when the user mentions Linear,
  issues/tickets, ENG-123-style identifiers, or wants Linear data queried, created,
  or updated — even if they just say "add this to my backlog".
version: 1.0.0
author: invoque
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [linear, issues, project-management, cli, tracking]
    requires_toolsets: [terminal]
required_environment_variables:
  - name: LINEAR_API_KEY
    prompt: Linear API key (create at https://linear.app/settings/account/security)
    help: Takes precedence over stored credentials; leave empty if you use `linear auth login` keyring auth
    required_for: Linear API access
---

# Linear CLI

Manage Linear from the command line with the `linear` CLI
(`@schpet/linear-cli`), which is git and jj aware. Run every `linear` command
through the `terminal` tool.

## When to Use

- The user mentions Linear, `linear.app`, Linear issues, tickets, projects, cycles,
  milestones, initiatives, or identifiers such as `ENG-123`.
- The user wants Linear issues queried, created, updated, commented on, or closed.
- The user wants Linear state reflected in or read from the command line — listing
  their work, triaging a backlog, or filing a bug.
- Not for GitHub issues (use `gh`) or other trackers.

## Prerequisites

Verify the CLI is installed:

```bash
linear --version
```

If `linear` is not on PATH, run it without installing:

```bash
npx @schpet/linear-cli --version
```

Prefix every command with `npx @schpet/linear-cli` in place of `linear`, or install
it via Homebrew (`brew install schpet/tap/linear`), npm
(`npm install -D @schpet/linear-cli`), Deno
(`deno install -A --reload -f -g -n linear jsr:@schpet/linear-cli`), or a release
binary. See https://github.com/schpet/linear-cli for install details.

### Authentication

Hermes injects `LINEAR_API_KEY` into `terminal` sandboxes when it is configured,
and the CLI reads it automatically. It has the highest precedence after the
`--api-key` flag, so it also works in remote backends where the system keyring is
unavailable (Docker, Modal, SSH).

Alternatively, authenticate the CLI interactively, which stores the key in the
system keyring:

```bash
linear auth login
```

On Linux the keyring requires `secret-tool` from `libsecret`. When neither method
is available, pass `--api-key <key>` for a single command, or set `api_key` in the
project's `.linear.toml` (less secure — never commit it).

Confirm the active identity and workspace:

```bash
linear auth whoami
```

Multi-workspace users switch per command with `--workspace <slug>`, or
`linear auth default <slug>` to change the default.

## Common Tasks

Copy-pasteable recipes for the most frequent flows. Prefer these dedicated commands
over `linear api` — reach for the GraphQL fallback only when no dedicated command or
flag covers the operation.

### Query issues with filters

`issue query` searches across all assignees and supports structured filters that can
be combined:

```bash
linear issue query --team ENG --state started --json
linear issue query --project "Mobile App" --state backlog --state triage --unassigned
linear issue query --assignee sam --label bug --updated-after 2026-01-01
```

`linear issue list` is an alias of `issue mine` and only shows *your* issues — use
`issue query` for anything scoped to other people or a whole team/project.

### List my issues

```bash
linear issue mine --state started --sort priority
```

### Create an issue

```bash
linear issue create --team ENG --title "Fix login redirect" \
  --description-file ./description.md --no-interactive
```

Write multi-line markdown to a file and pass `--description-file` (see
[Markdown Content](#markdown-content)); `--no-interactive` avoids prompts in
scripted use.

### Update an issue's state, assignee, or labels

```bash
linear issue update ENG-123 --state "In Review" --assignee sam
linear issue update ENG-123 --unassign
linear issue update ENG-123 --add-label security             # add, keep existing labels
linear issue update ENG-123 --remove-label sprint-42         # detach; does not delete the label
linear issue update ENG-123 --remove-label sprint-42 --add-label sprint-43  # atomic swap
linear issue update ENG-123 --label infra --label security   # replaces the label set
```

### Create an issue or project from a template

```bash
linear template list --type issue --team ENG              # find the template a team expects
linear template view "Bug report"                         # see what it pre-fills (title, fields, body, sub-issues)
linear issue create --team ENG --template "Bug report" --title "Login fails on Safari"
linear project create --name "Q3 launch" --team ENG --template "Kickoff"
```

Explicit flags override the template's values, `--label` merges with its labels, and
`--description` replaces its body (omit it to keep the body). Document templates
cannot be applied through the API.

### Add a comment

```bash
linear issue comment add ENG-123 --body-file ./comment.md
```

### Attach an image or screenshot so it is visible inline

```bash
linear issue comment add ENG-123 --attach ./screenshot.png
```

This uploads the image and embeds it in a comment, where Linear renders it inline. Do
not use `linear issue attach` when the image must be visible: that command creates a
sidebar link attachment and does not render images inline.

### View an issue / get its URL

```bash
linear issue view ENG-123          # details incl. comments
linear issue view ENG-123 --json   # structured output
linear issue url ENG-123           # print just the URL
```

### Close, delete, or archive an issue

```bash
linear issue update ENG-123 --state Done       # or Canceled; Linear auto-archives closed issues later
linear issue delete ENG-123                    # trash; restorable in Linear for 30 days
linear issue archive ENG-123 --confirm         # rarely appropriate, see Pitfalls
```

## Markdown Content

When issue descriptions or comment bodies contain markdown, always use file-based
flags instead of passing content as command-line arguments:

- `--description-file` for `issue create` and `issue update`
- `--body-file` for `comment add` and `comment update`

Write the markdown with `write_file` to a path the CLI can read, then pass that path.
File-based flags ensure correct rendering in the Linear web UI, avoid shell escaping
problems with newlines, prevent literal `\n` sequences, and keep multi-line content
manageable. Use inline flags (`--description`, `--body`) only for simple
single-line content.

```bash
# 1. write_file -> ./description.md
# 2. create the issue with the file
linear issue create --title "My Issue" --description-file ./description.md
```

### Mention people and resources with plain URLs

Linear turns a resource's **plain Linear URL** in Markdown into a linked mention. A
literal `@name`, `@[Name](id)`, or a Markdown link such as `[Name](url)` does not
create the same mention. Put the plain URL directly in the comment or description:

```markdown
https://linear.app/yourworkspace/profiles/someuser could you review this? https://linear.app/yourworkspace/issue/ENG-123 is related.
```

Resolve people within the relevant team first — the team can usually be inferred
from the issue identifier or the current directory:

```bash
linear team members ENG --json
```

Use the selected member's `url` field verbatim. If the intended person is not a
member of that team, stop and confirm before searching the whole workspace with
`linear user list --json`; mentioning someone outside the team is likely accidental.
For issues, use `linear issue url ENG-123` and include that plain URL.

### Add collapsible sections

Open a collapsible section with `+++ [title]` and close it with `+++`; the square
brackets around the title and the closing `+++` are required:

```markdown
+++ [Server log]

Markdown content that is initially hidden.

+++
```

## GraphQL Fallback

Prefer the CLI for all supported operations. Use `linear api` only for queries not
covered by the CLI. See `references/api.md` for details.

Write the schema to a temp file, then search it:

```bash
linear schema -o "${TMPDIR:-/tmp}/linear-schema.graphql"
grep -i "cycle" "${TMPDIR:-/tmp}/linear-schema.graphql"
grep -A 30 "^type Issue " "${TMPDIR:-/tmp}/linear-schema.graphql"
```

`linear api` takes the GraphQL document as its only positional argument and has no
subcommands. Put a leading `query` or `mutation` keyword inside that quoted document:
use `linear api 'query { ... }'`, never `linear api query '...'`.

GraphQL queries containing non-null type markers (for example `String` followed by
an exclamation mark) must be passed via heredoc stdin to avoid escaping issues;
simple queries without those markers can be passed inline.

```bash
# Simple query (no type markers, so inline is fine)
linear api '{ viewer { id name email } }'

# Query with variables — use heredoc to avoid escaping issues
linear api --variable teamId=abc123 <<'GRAPHQL'
query($teamId: String!) { team(id: $teamId) { name } }
GRAPHQL

# Search issues by text
linear api --variable term=onboarding <<'GRAPHQL'
query($term: String!) { searchIssues(term: $term, first: 20) { nodes { identifier title state { name } } } }
GRAPHQL

# Numeric and boolean variables
linear api --variable first=5 <<'GRAPHQL'
query($first: Int!) { issues(first: $first) { nodes { title } } }
GRAPHQL

# Complex variables via JSON
linear api --variables-json '{"filter": {"state": {"name": {"eq": "In Progress"}}}}' <<'GRAPHQL'
query($filter: IssueFilter!) { issues(filter: $filter) { nodes { title } } }
GRAPHQL

# Pipe to jq for filtering
linear api '{ issues(first: 5) { nodes { identifier title } } }' | jq '.data.issues.nodes[].title'
```

For full HTTP control, use `linear auth token` with `curl`:

```bash
curl -s -X POST https://api.linear.app/graphql \
  -H "Content-Type: application/json" \
  -H "Authorization: $(linear auth token)" \
  -d '{"query": "{ viewer { id } }"}'
```

## Pitfalls

- **Never archive by default.** Prefer closing or deleting. Linear auto-archives
  closed issues after the team's configured period and removed manual archiving from
  its app; `issue archive` calls the `issueArchive` mutation directly, bypassing
  auto-archive's checks for open parents, sub-issues, cycles, and projects. Archived
  issues vanish from `issue list`, `issue query`, and search unless
  `--include-archived` is passed. Only archive when the user explicitly asks.
- **`issue list` is not a general search.** It is an alias of `issue mine`; use
  `issue query` for other assignees, teams, or projects.
- **`--no-pager` only works on `issue list`** — passing it to commands like
  `project list` errors.
- **Hidden required flags.** `issue list` sorts by priority by default — override
  with `--sort` (`manual` or `priority`), the `issue_sort` config option, or
  `LINEAR_ISSUE_SORT`. It also requires `--team <key>` unless the team can be
  inferred from the directory; run `linear team list --json` to map names to keys.
- **`linear api` quoting.** The GraphQL document is a single quoted argument with the
  `query`/`mutation` keyword inside it; non-null markers (`String!`) need a heredoc.
- **Mentions.** Only plain Linear URLs create mentions; resolve team members before
  using their URL, and confirm before mentioning non-members.
- **Remote terminal backends.** The system keyring (and stored credentials) may be
  absent; rely on `LINEAR_API_KEY`. A file written with `write_file` may also be
  invisible to a remote backend — if the CLI reports a missing file, create it with a
  terminal command (for example a heredoc) instead.
- **`LINEAR_API_KEY` precedence.** It overrides stored credentials, so it can
  override a multi-workspace default selection.

## Verification

- `linear auth whoami` exits successfully and prints the expected user/workspace.
- A created or updated issue returns its identifier, and
  `linear issue view <ID> --json` reflects the fields that were set.
- A comment added with `--body-file` renders as formatted markdown (not literal
  `\n`) when viewed in Linear.
- A GraphQL call returns data under `.data` when piped to `jq` (no `.errors`).

## Reference files

Read the matching file on demand; do not rely on this body for command details.

| Topic | Read |
| --- | --- |
| API | `references/api.md` |
| Auth | `references/auth.md` |
| Full command tree and index | `references/commands.md` |
| Config | `references/config.md` |
| Cycles | `references/cycle.md` |
| Documents | `references/document.md` |
| Initiatives | `references/initiative.md` |
| Initiative updates | `references/initiative-update.md` |
| Issues | `references/issue.md` |
| Labels | `references/label.md` |
| Markdown: mentions and collapsibles | `references/markdown.md` |
| Milestones | `references/milestone.md` |
| Organization features (initiatives, labels, projects, bulk ops) | `references/organization-features.md` |
| Projects | `references/project.md` |
| Project updates | `references/project-update.md` |
| GraphQL schema | `references/schema.md` |
| Teams | `references/team.md` |
| Templates | `references/template.md` |
| Users | `references/user.md` |
