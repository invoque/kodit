# Hermes Tools & Toolsets Reference

On-demand reference for the tools a Hermes skill can name. Load this when authoring a skill
body or deciding which tools a skill should require.

Source: https://hermes-agent.nousresearch.com/docs/user-guide/features/tools

## Contents

- [Tools by category](#tools-by-category)
- [Toolsets](#toolsets)
- [Terminal backends](#terminal-backends)
- [How a skill should reference tools](#how-a-skill-should-reference-tools)
- [Choosing conditional activation](#choosing-conditional-activation)

## Tools by category

| Category | Tools | What they do |
| --- | --- | --- |
| Web | `web_search`, `web_extract` | Search the web; extract the content of a page. |
| X Search | `x_search` | Search X/Twitter posts and threads. Opt-in; needs xAI credentials. |
| Terminal & Files | `terminal`, `process`, `read_file`, `patch`, `write_file` | Run commands; manage background processes; read, edit, and write files. |
| Browser | `browser_navigate`, `browser_snapshot`, `browser_vision` | Interactive browser automation with text and vision. |
| Media | `vision_analyze`, `image_generate`, `text_to_speech` | Analyze images; generate images; synthesize speech. |
| Agent orchestration | `todo`, `clarify`, `execute_code`, `delegate_task` | Track tasks; ask the user a question; run sandboxed Python with RPC tool access; spawn isolated subagents. |
| Memory & recall | `memory`, `session_search` | Persistent memory; search past conversations (FTS5 + summarization). |
| Automation | `cronjob` | Create/list/update/pause/resume/run/remove scheduled tasks. |
| Skill tools | `skills_list`, `skill_view`, `skill_manage` | List skills; load a skill or reference; create/edit/delete skills. |
| Integrations | `ha_*`, MCP server tools | Home Assistant; any connected MCP server. |

Note: cross-session memory via Honcho is a memory-provider plugin, not a built-in toolset.

## Toolsets

Toolsets group tools and can be enabled/disabled per platform:

- `hermes tools` — list and configure available tools interactively.
- `hermes chat --toolsets "web,terminal"` — enable a specific set for a session.

Common toolsets: `web`, `search`, `terminal`, `file`, `browser`, `vision`, `image_gen`,
`skills`, `tts`, `todo`, `memory`, `session_search`, `cronjob`, `code_execution`,
`delegation`, `clarify`, `homeassistant`, `messaging`, `spotify`, `discord`,
`discord_admin`, `debugging`, `safe`.

Platform presets: `hermes-cli`, `hermes-telegram` (and other messaging presets).

Dynamic MCP toolsets use the `mcp-<server>` form.

## Terminal backends

The `terminal` tool can execute in different environments, configured under `terminal.backend`
in `~/.hermes/config.yaml`:

| Backend | Use case |
| --- | --- |
| `local` | Default; development, trusted tasks. |
| `docker` | Isolated, persistent container; security and reproducibility. |
| `ssh` | Remote server; keeps the agent away from its own code. |
| `singularity` | HPC containers; rootless cluster computing. |
| `modal` | Serverless cloud execution. |
| `daytona` | Persistent cloud sandbox workspace. |
| `vercel_sandbox` | Vercel Sandbox cloud microVM with snapshot persistence. |

A skill that shells out should not assume a specific backend; use `terminal` and let the
user's configuration decide where it runs.

## How a skill should reference tools

- Name tools exactly as they appear above (`web_search`, not `search_web`).
- Never invent tools or commands. If the capability does not exist, express the skill as
  shell commands run through `terminal`, or suggest a new tool instead of a skill.
- Prefer the simplest existing tool: `web_extract` over scripting a fetch,
  `read_file`/`patch` over raw `sed`/`awk`, `execute_code` for multi-step Python.
- For skills that ship helper scripts, put them in `scripts/` and invoke them with
  `terminal`. Prefer stdlib Python or `curl`; avoid heavy dependencies.
- Reference files in `references/` by relative path and tell the agent when to read them,
  e.g. "See `references/api.md` for the endpoint list."

## Choosing conditional activation

Match the skill's frontmatter to the tools it actually needs (see
`hermes-skill-format.md` for the field semantics):

- Needs the web → `requires_toolsets: [web]` or `requires_tools: [web_search]`.
- Needs to run commands → `requires_toolsets: [terminal]`.
- Needs subagents for its workflow → `requires_toolsets: [delegation]`.
- Is a workaround for a missing tool → `fallback_for_tools: [<primary_tool>]`.

Keep requirements minimal. A skill hidden too aggressively will not surface when the user
needs it; a skill that names a tool it cannot use will fail at runtime.
