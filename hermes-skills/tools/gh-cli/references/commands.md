# gh Command Reference

Full command surface of the GitHub CLI. Generated from `gh --help` against gh
v2.99.0; confirm details with `gh <command> <subcommand> --help`, which is always
authoritative for the installed version.

## Commands

| Command | Purpose | Reference |
| --- | --- | --- |
| `gh auth` | Authenticate gh and git with GitHub | [`auth.md`](./auth.md) |
| `gh api` | Make an authenticated GitHub API request | [`api.md`](./api.md) |
| `gh pr` | Manage pull requests | [`pr.md`](./pr.md) |
| `gh issue` | Manage issues | [`issue.md`](./issue.md) |
| `gh release` | Manage releases | [`release.md`](./release.md) |
| `gh run`, `gh workflow` | View GitHub Actions runs and workflows | [`run.md`](./run.md) |
| `gh repo`, `gh search`, `gh gist`, `gh label` | Repositories, search, gists, labels | [`repo.md`](./repo.md) |
| `gh browse` | Open repositories, issues, PRs in the browser | — |
| `gh status` | Summary of assigned issues, PRs, and review requests | — |
| `gh alias`, `gh config` | Command shortcuts and gh configuration | — |
| `gh cache`, `gh secret`, `gh variable` | Actions caches, secrets, and variables | — |
| `gh project`, `gh discussion`, `gh org` | Projects, discussions, organizations | — |
| `gh ruleset`, `gh attestation`, `gh ssh-key`, `gh gpg-key` | Security and key management | — |
| `gh codespace`, `gh extension`, `gh copilot`, `gh skill` | Codespaces, extensions, preview features | — |

Prefer a dedicated command over `gh api`; reach for `gh api` only when no
command or flag covers the operation.

## Full Command Tree

Top level:

```bash
gh auth          gh gist         gh project      gh ssh-key
gh agent-task    gh gpg-key      gh release      gh status
gh alias         gh issue        gh repo         gh variable
gh api           gh label        gh ruleset      gh workflow
gh attestation   gh licenses     gh run
gh browse        gh org          gh search
gh cache         gh pr           gh secret
gh codespace     gh preview      gh skill
gh completion    gh config       gh copilot
gh discussion    gh extension
```

Subcommands:

```bash
gh auth
gh auth login
gh auth logout
gh auth refresh
gh auth setup-git
gh auth status
gh auth switch
gh auth token

gh api

gh pr
gh pr checkout        (alias: gh co)
gh pr checks
gh pr close
gh pr comment
gh pr create          (alias: gh pr new)
gh pr diff
gh pr edit
gh pr list            (alias: gh pr ls)
gh pr lock
gh pr merge
gh pr ready
gh pr reopen
gh pr revert
gh pr review
gh pr status
gh pr unlock
gh pr update-branch
gh pr view

gh issue
gh issue close
gh issue comment
gh issue create       (alias: gh issue new)
gh issue delete
gh issue develop
gh issue edit
gh issue list         (alias: gh issue ls)
gh issue lock
gh issue pin
gh issue reopen
gh issue status
gh issue transfer
gh issue unlock
gh issue unpin
gh issue view

gh release
gh release create     (alias: gh release new)
gh release delete
gh release delete-asset
gh release download
gh release edit
gh release list       (alias: gh release ls)
gh release upload
gh release verify
gh release verify-asset
gh release view

gh run
gh run cancel
gh run delete
gh run download
gh run list           (alias: gh run ls)
gh run rerun
gh run view
gh run watch

gh workflow
gh workflow disable
gh workflow enable
gh workflow list      (alias: gh workflow ls)
gh workflow run
gh workflow view

gh repo
gh repo archive
gh repo autolink
gh repo clone
gh repo create        (alias: gh repo new)
gh repo delete
gh repo deploy-key
gh repo edit
gh repo fork
gh repo gitignore
gh repo license
gh repo list          (alias: gh repo ls)
gh repo read-dir      (preview)
gh repo read-file     (preview)
gh repo rename
gh repo set-default
gh repo sync
gh repo unarchive
gh repo view

gh search
gh search code
gh search commits
gh search issues
gh search prs
gh search repos

gh gist
gh gist clone
gh gist create        (alias: gh gist new)
gh gist delete
gh gist edit
gh gist list          (alias: gh gist ls)
gh gist rename
gh gist view

gh label
gh label clone
gh label create
gh label delete
gh label edit
gh label list         (alias: gh label ls)

gh cache
gh cache delete
gh cache list

gh secret
gh secret delete
gh secret list
gh secret set

gh variable
gh variable delete
gh variable get
gh variable list
gh variable set

gh config
gh config get
gh config list        (alias: gh config ls)
gh config set

gh alias
gh alias delete
gh alias list         (alias: gh alias ls)
gh alias set

gh browse
gh status
gh api
```

## Help Topics

```bash
gh help accessibility   # accessibility experiences
gh help actions         # working with GitHub Actions
gh help environment     # environment variables gh reads
gh help exit-codes      # exit codes used by gh
gh help formatting      # --json, --jq, and --template
gh help mintty          # using gh with MinTTY on Windows
gh help reference       # comprehensive command reference
gh help telemetry       # telemetry in gh
```

## Exit Codes

- `0` — success.
- `1` — any command failure.
- `2` — command running when cancelled.
- `4` — command requires authentication.

A specific command can define more (for example `gh pr checks` returns `8` when
checks are pending), so check command help before branching on exit codes.

## Global Notes

- `gh <command> --help` and `gh help <topic>` are authoritative for the installed
  version; run them before relying on a flag.
- `-R, --repo [HOST/]OWNER/REPO` selects another repository on every repository
  command.
- `--json <fields>` plus `--jq <expr>` or `--template <go-template>` gives
  structured output; omit the field list (`--json`) to print available fields.
