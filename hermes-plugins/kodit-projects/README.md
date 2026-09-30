# kodit-projects

Native Hermes plugin: a project registry with an SQLite/FTS5 file index. It
works out of an instant message — when you talk about a project, the plugin
figures out *which* registered project you mean, injects a small
`[project-context]` block into the turn, and gives the agent tools to search
that project's files and maintain its metadata.

## What it does

- **Registry** — per project: working directory, name, summary, Linear URL,
  GitHub repo, aliases, session/index timestamps.
- **File index** — every text file under a project's root (bounded: skips
  `.git`, `node_modules`, generated trees and binaries; 512 KB per file; 5000
  files), full-text searchable via SQLite FTS5 over path, title, and body.
- **Detection** — resolves the message's project by cascade:
  GitHub URL → path token → name/alias/slug → session CWD → ≥2 message words
  matching one project's file index → the session's sticky project.
- **Context injection** — a ≤2000-char `[project-context]` block appended to
  the user message each turn (name, slug, working dir, summary, Linear/GitHub,
  first-turn key paths).
- **Bundled skill** — `kodit-projects:projects`, registered automatically;
  the injected context tells the agent when to read it.

## Install

```bash
ln -s "$(pwd)/hermes-plugins/kodit-projects" ~/.hermes/plugins/kodit-projects
hermes plugins enable kodit-projects
hermes plugins doctor   # sanity check
```

State lives in `<HERMES_HOME>/plugin-data/kodit-projects/projects.db` (WAL,
profile-scoped). The install dir holds only source — deleting it never touches data.

## Usage

Slash command (CLI and gateway/IM sessions):

```
/projects register <path> [name]      # derives summary from README/CONTEXT/kodit.json,
                                            # origin from `git remote`, then indexes files
/projects list
/projects show [key]                  # active project when key omitted
/projects set <key> <field> <value>   # name|summary|description|linear_url|github_repo
/projects alias <key> add|remove <alias>
/projects index <key>                 # force reindex
/projects forget <key>
```

Agent tools (toolset `kodit_projects`):

| Tool | Purpose |
|---|---|
| `kodit_projects_search` | FTS5 search — scoped by `project`, or global with per-hit slugs |
| `kodit_projects_show` | read one project's metadata (or the active one) |
| `kodit_projects_set` | update metadata fields / add or remove aliases |

Hooks: `pre_llm_call` (per-turn resolution + context block), `on_session_start`
(refreshes a stale index when the session CWD is a registered project), plus a
system-prompt section that records the session CWD and carries durable guidance.

## Layout

| File | Role |
|---|---|
| `plugin.yaml` | manifest (name, version, hooks, tools) |
| `__init__.py` | `register(ctx)`: hooks, tools, command, prompt section, skill |
| `store.py` | SQLite/FTS5 schema, registry CRUD, lookups, file index |
| `detect.py` | message → project resolution cascade |
| `context.py` | size-capped `[project-context]` block builder |
| `indexer.py` | bounded filesystem walk → index rows |
| `derive.py` | summary/name/origin auto-derivation at register time |
| `skills/projects/SKILL.md` | bundled companion skill |

## Tests

Every module is self-contained and selftests without a Hermes install:

```bash
for f in hermes-plugins/kodit-projects/*.py; do
  python3 "$f" --selftest || exit 1
done
```

`__init__.py --selftest` drives `register(ctx)` end to end against a fake
context and a temp `HERMES_HOME` (register → index → search → set → detect →
inject → sticky → forget).
