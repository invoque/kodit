---
name: gh-cli
description: Manage GitHub from the command line with the `gh` CLI — issues, pull
  requests, releases, Actions runs, checks, gists, searches, and repositories.
  Query, create, update, comment on, review, and merge them; fall back to
  `gh api` for REST and GraphQL. Use when the user mentions GitHub, PRs, reviews,
  reviewers, issues, releases, CI runs, checks, gists, READMEs, or repository
  data read or changed — even if they just say "open a PR for this", "file a bug",
  "did CI pass", or "cut a release".
version: 1.0.0
author: invoque
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [github, cli, issues, pull-requests, releases, actions]
    related_skills: [linear-cli]
    requires_toolsets: [terminal]
required_environment_variables:
  - name: GH_TOKEN
    prompt: GitHub token with repo scope (create at https://github.com/settings/tokens)
    help: Takes precedence over `gh auth login` keyring credentials; leave empty if you use `gh auth login`
    required_for: GitHub API access
---

# GitHub CLI

Manage GitHub from the command line with the `gh` CLI. Run every `gh` command
through the `terminal` tool.

## When to Use

- The user mentions GitHub, `github.com`, a repository URL, or `gh`.
- The user wants issues, pull requests, releases, checks, Actions runs, gists, or
  repo data queried, created, updated, commented on, reviewed, merged, or closed.
- Not for generic local git operations (`git commit`, `git rebase`) — use `git`.
- Not for Linear issues (use `linear-cli`).

## Prerequisites

Verify the CLI is installed:

```
terminal(command="gh --version")
```

If `gh` is missing, install it (Homebrew `brew install gh`, Debian
`sudo apt install gh`, Windows `winget install GitHub.cli`, or a release binary
from https://github.com/cli/cli#installation).

### Authentication

Hermes injects `GH_TOKEN` into `terminal` sandboxes when it is configured, and
`gh` reads it automatically. It takes precedence over stored credentials, so it
also works in remote backends where the system keyring is unavailable (Docker,
Modal, SSH).

Alternatively, authenticate interactively, which stores the token in the system
credential store:

```
terminal(command="gh auth login")
```

Confirm the active account:

```
terminal(command="gh auth status")
```

`GH_TOKEN` overrides keyring login silently — if commands run as the wrong user
or hit unexpected scope errors, check it first.

### Repository context

Commands infer the repository from the git remote in the current directory. When
there is no `github.com` remote, or the target is another repository, pass
`-R, --repo [HOST/]OWNER/REPO`:

```
terminal(command="gh issue list -R cli/cli")
```

`GH_REPO` sets the same value for a whole session. Use `gh repo set-default` to
pin a default repository for a directory.

## Common Tasks

Copy-pasteable recipes for the most frequent flows. Prefer these dedicated
commands over `gh api`; reach for `gh api` only when no command or flag covers the
operation. Always pass the flags that would otherwise be prompted for.

### View a repository

```
terminal(command="gh repo view")
terminal(command="gh repo view cli/cli --json name,description,defaultBranchRef,stargazerCount")
terminal(command="gh repo list myorg --limit 50 --json name,visibility")
```

### List and create issues

```
terminal(command="gh issue list --assignee @me --state open")
terminal(command="gh issue list --label bug --search 'no:assignee sort:created-asc'")
terminal(command="gh issue create --title \"Login fails on Safari\" --body-file ./issue.md --label bug --assignee @me")
terminal(command="gh issue comment 123 --body-file ./comment.md")
terminal(command="gh issue close 123 --comment \"Fixed in #130\" --reason completed")
```

`gh issue list` defaults to open issues; use `--state closed` or `--state all`
for the rest. The created issue URL is printed on success.

### Work with pull requests

```
terminal(command="gh pr list --author @me --state open")
terminal(command="gh pr view 123 --json number,title,state,mergeable,reviewDecision,statusCheckRollup")
terminal(command="gh pr diff 123")
terminal(command="gh pr create --base main --title \"Fix login redirect\" --body-file ./pr-body.md")
terminal(command="gh pr checks 123")
terminal(command="gh pr review 123 --approve --body-file ./review.md")
terminal(command="gh pr comment 123 --body-file ./comment.md")
terminal(command="gh pr merge 123 --squash --delete-branch")
```

`gh pr create` needs `--title` and `--body`/`--body-file` (or `--fill`) or it
prompts interactively. `gh pr merge` needs an explicit `--merge`, `--squash`, or
`--rebase` for the same reason. `gh pr checks` exits `8` while checks are pending.

### Manage releases

```
terminal(command="gh release create v1.2.3 --title \"v1.2.3\" --notes-file ./release-notes.md")
terminal(command="gh release create v1.2.3 --generate-notes")
terminal(command="gh release upload v1.2.3 ./dist/*.tgz")
terminal(command="gh release download v1.2.3 --pattern '*.deb' --dir ./downloads")
```

Pass `--draft` to stage a release, `--prerelease` to mark it, and `--latest=false`
to keep it from becoming the latest.

### Inspect Actions runs

```
terminal(command="gh run list --branch main --limit 10")
terminal(command="gh run view 12345 --log-failed")
terminal(command="gh run view 12345 --exit-status")
terminal(command="gh run rerun 12345 --failed")
terminal(command="gh run download 12345 --name coverage")
```

`gh run watch <id>` blocks until the run finishes; pair it with `--exit-status`
when the outcome matters, and never leave it running without a timeout.

### Search GitHub

```
terminal(command="gh search repos --language=go --stars='>1000' --limit 20")
terminal(command="gh search issues --assignee=@me --state=open --include-prs")
terminal(command="gh search prs --review-requested=@me --state=open")
terminal(command="gh search code panic --repo cli/cli --language=go")
```

## File-Based Content

When issue, PR, comment, review, or release-notes bodies contain markdown, always
use file-based flags instead of passing content as command-line arguments:

- `--body-file` for `issue create`, `issue comment`, `issue edit`, `pr create`,
  `pr comment`, `pr review`, and `pr edit`
- `--notes-file` for `release create` and `release edit`

Write the markdown to a file with the `write_file` tool, then pass that path:

1. Use `write_file` to create `./body.md`.
2. Run `terminal(command="gh issue create --title \"My issue\" --body-file ./body.md")`.

File-based flags avoid shell-escaping problems with newlines and prevent literal
`\n` sequences. Use inline flags (`--body`) only for simple single-line content.

## Structured Output

Every list and view command supports `--json <fields>` plus `--jq <expr>` or
`--template <go-template>`:

```
terminal(command="gh pr list --json number,title,author --jq '.[] | \"#\(.number) \(.title) by \(.author.login)\"'")
terminal(command="gh issue list --json number,title,labels --jq 'map(select(.labels | length > 0))'")
```

Omit the field list (`--json`) to print the available fields. Prefer `--json`
with `--jq` over parsing the human-readable table. See `gh help formatting`.

## API Fallback

Use `gh api` only for operations with no dedicated command. Write the endpoint as
a REST path or `graphql`:

```
terminal(command="gh api repos/{owner}/{repo}/issues --jq '.[].title'")
terminal(command="gh api -X GET search/issues -f q='repo:cli/cli is:open remote'")
terminal(command="gh api graphql -f query='query { viewer { login name } }'")
terminal(command="gh api repos/{owner}/{repo}/issues --paginate")
```

See `references/api.md` for field types, nested payloads, GraphQL variables, and
pagination. Never send destructive API methods without explicit user consent.

## Pitfalls

- **Interactive prompts hang the sandbox.** Any command that would prompt must be
  given flags: `gh pr create` needs `--title`/`--body`, `gh pr merge` needs a
  strategy, `gh issue create` needs `--title`/`--body`, and destructive commands
  (`gh release delete`, `gh repo delete`, `gh label delete`) prompt without
  `--yes`. `GH_PROMPT_DISABLED` disables prompting entirely but then fails
  instead of asking.
- **`GH_TOKEN` overrides keyring credentials.** It wins over `gh auth login`, so a
  weakly scoped or wrong-account token silently takes over. Check it before
  debugging scope errors.
- **Repo inference needs a `github.com` remote.** In a directory without one, or
  when acting on another repo, pass `-R OWNER/REPO` or set `GH_REPO`.
- **`--watch` and `gh run watch` block.** They run until the run or checks finish;
  set a timeout and use `--exit-status` when the outcome matters.
- **`--json` needs a field list before `--jq`/`--template`.** Pass
  `--json field1,field2`; omitting the fields prints the available list, and
  `--jq` without `--json` errors.
- **`gh pr checks` uses extra exit codes.** `8` means checks are still pending and
  `1` means at least one failed; do not treat `8` as a hard failure.
- **`gh run rerun --job` wants the job `databaseId`,** not the number in the
  browser URL. Get it from `gh run view <id> --json jobs`.
- **`--clobber` deletes before upload.** On `gh release upload` and
  `gh release download`, a failed overwrite can lose the originals.
- **Remote terminal backends may lack a keyring.** Rely on `GH_TOKEN`. A file
  written with `write_file` may also be invisible to a remote backend — if a
  `--body-file` is reported missing, create it with a terminal command (for
  example a heredoc) instead.

## Verification

- `terminal(command="gh auth status")` exits successfully and prints the expected
  account.
- A created issue or PR prints its URL, and
  `terminal(command="gh pr view <N> --json state,title")` reflects the fields set.
- A comment or review added with `--body-file` renders as formatted markdown (not
  literal `\n`) when viewed on GitHub.
- `terminal(command="gh run view <id> --exit-status")` reflects the real run
  outcome, and a `--json`/`--jq` call returns the selected fields.

## Reference files

Read the matching file on demand; do not rely on this body for command details.

| Topic | Read |
| --- | --- |
| Full command tree, help topics, exit codes | `references/commands.md` |
| Authentication, tokens, accounts, git credential setup | `references/auth.md` |
| Pull requests | `references/pr.md` |
| Issues | `references/issue.md` |
| Releases | `references/release.md` |
| Actions runs and workflows | `references/run.md` |
| Repositories, search, gists, labels | `references/repo.md` |
| REST and GraphQL via `gh api` | `references/api.md` |
