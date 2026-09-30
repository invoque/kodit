# AGENTS.md

Instructions for coding agents working in `hermes-plugins/`. This file governs
the `hermes-plugins/` subtree and wins over any other instruction for work in it.

## Project Overview

`hermes-plugins` holds **native Hermes Agent plugins** — Python runtime code
that runs inside the Hermes process. This is the one subtree in `kodit` where
runtime code lives; everything else in this repository is markdown.

## Directory Layout

```
hermes-plugins/
├── AGENTS.md                 # this file
└── <plugin-name>/
    ├── plugin.yaml           # manifest: name, version, description, provides_hooks/tools
    ├── __init__.py           # register(ctx) + hook/tool/command handlers + selftest
    ├── *.py                  # focused modules (store, detect, indexer, ...), each with a selftest
    ├── skills/<name>/SKILL.md  # optional bundled companion skill
    └── README.md             # what the plugin does, install and usage
```

- `plugin.yaml` `name` must equal the directory name.
- `register(ctx)` is the only entry point Hermes calls; everything else is
  module internals.

## Authoritative References

Plugin API details (hooks, `ctx.*` registrars, manifest schema, tool schemas)
belong to Hermes, not to this file. Check the local Hermes checkout when in
doubt — `hermes_cli/plugins.py`, `hermes_cli/plugins_manifest.py`, and
`website/docs/user-guide/features/plugins.md` are the source of truth.

## Non-Negotiable Rules

- **Fail open.** Every hook and prompt-section callback wraps its body in
  `try/except`, logs a warning, and returns `None`/fallback text. A plugin bug
  must never break a turn or a session start.
- **Bounded work on the hot path.** `pre_llm_call` runs per turn: keep it to
  lookups, cap any scanning (file counts, message scans), and never block on
  network or subprocess with long timeouts.
- **Storage goes in the plugin data dir.** Use
  `<HERMES_HOME>/plugin-data/<plugin-name>/` (see `plugins/plugin_storage.py`).
  Never write into `~/.hermes/plugins/<name>/` (the install dir) or into a
  registered project.
- **No secrets.** Credentials are read through Hermes secret plumbing, never
  stored in plugin files or the plugin DB.
- **Every module ships a selftest.** `python3 <file>.py --selftest` must exit 0
  with no Hermes install, no network, and no writes outside a temp dir.
  `python3 __init__.py --selftest` must exercise `register(ctx)` end to end
  against a fake context and a temp `HERMES_HOME`.

## Do

- Keep modules small and single-purpose; one concern per file.
- Validate the manifest and run every selftest before committing:
  `for f in <plugin>/*.py; do python3 "$f" --selftest || exit 1; done`
- Use conventional commit messages (`feat:`, `fix:`, `docs:`, `chore:`).
- Work on a `feature/*` branch; never commit to a protected branch.

## Don't

- Do not vendor or pin Hermes internals; import them lazily and tolerate their
  absence (a module must still import and selftest outside a Hermes process).
- Do not register the same tool/command name twice or override built-ins.
- Do not keep the plugin DB inside a project's working directory (it bumps the
  directory mtime and defeats staleness detection).
- Do not commit to `master` or `dev`.

## Distribution

Plugins are consumed from this repository's default branch (`master`): symlink
the plugin directory into the user's Hermes plugins dir and enable it — never
copy source files.

```bash
ln -s "$(pwd)/hermes-plugins/<name>" ~/.hermes/plugins/<name>
hermes plugins enable <name>
```

Install dirs are deleted by `hermes plugins remove` and rewritten by
`hermes plugins update`; state belongs in the plugin data dir only. CI runs the
selftests on every push to `master` via `.github/scripts/validate-hermes-plugins.py`.
