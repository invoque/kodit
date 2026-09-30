---
name: projects
description: >-
  Use when working with the kodit-projects plugin: an [project-context] block
  is in the user's message, or the user wants to search registered projects'
  files, register a project, or change project metadata (summary, Linear URL,
  GitHub repo, aliases).
---

# kodit-projects

Manage and use the project registry: working directory, summary, Linear URL,
GitHub repo, aliases, and an FTS5 full-text index of each project's files.

## Usage

Namespaced as `kodit-projects:projects`; read via `skill_view` when an
`[project-context]` block appears in a turn or the user asks about projects.

## What You Must Do When Invoked

1. Treat an `[project-context]` block in the user message as authoritative for
   this turn: its slug, working dir, and summary are the active project.
2. Search files with `kodit_projects_search` — pass `project` to scope one
   project, omit it to search across all registered projects.
3. Read metadata with `kodit_projects_show`; change fields or aliases with
   `kodit_projects_set` (fields: name, summary, description, linear_url,
   github_repo, alias_add, alias_remove).
4. For registry operations the user runs directly, use `/kodit-projects`:
   `register <path> [name]`, `list`, `show [key]`,
   `set <key> <field> <value>`, `alias <key> add|remove <alias>`,
   `index <key>`, `forget <key>`.
5. When the user supplies a better summary or a new Linear/GitHub URL for the
   active project, persist it with `kodit_projects_set` instead of only
   replying.
6. If there is no `[project-context]` block but the topic may be a registered
   project, call `kodit_projects_show` first to see what exists.
