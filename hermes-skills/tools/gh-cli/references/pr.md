# gh PR Reference

Manage GitHub pull requests: list, view, create, review, comment, check, and
merge. A pull request can be given as a number (`123`), a URL, or a head branch
name (`patch-1` or `OWNER:patch-1`); omitted, it defaults to the PR for the
current branch.

## Commands

| Command | Purpose |
| --- | --- |
| `gh pr create` | Create a pull request (alias `gh pr new`) |
| `gh pr list` | List pull requests (alias `gh pr ls`) |
| `gh pr view` | Display a PR's title, body, and details |
| `gh pr status` | Show status of PRs relevant to you |
| `gh pr diff` | View changes in a PR |
| `gh pr checkout` | Check out a PR in git (alias `gh co`) |
| `gh pr checks` | Show CI status for a PR |
| `gh pr comment` | Add a comment |
| `gh pr review` | Approve, comment, or request changes |
| `gh pr merge` | Merge a PR |
| `gh pr edit` | Edit title, body, labels, reviewers, assignees |
| `gh pr ready` | Mark ready for review (or `--undo` back to draft) |
| `gh pr close` / `gh pr reopen` | Close or reopen |
| `gh pr lock` / `gh pr unlock` | Lock or unlock the conversation |
| `gh pr update-branch` / `gh pr revert` | Update the branch, or revert the merge |

## View and List

```
terminal(command="gh pr view")
terminal(command="gh pr view 123")
terminal(command="gh pr view 123 --comments")
terminal(command="gh pr view 123 --json number,title,state,mergeable,reviewDecision,statusCheckRollup")
terminal(command="gh pr diff 123")
terminal(command="gh pr diff 123 --name-only")
terminal(command="gh pr list --author @me --state open")
terminal(command="gh pr list --search 'status:success review:required'")
terminal(command="gh pr list --label bug --limit 50 --json number,title,url")
terminal(command="gh pr status")
```

## Create

Always pass `--title` and `--body`/`--body-file` (or `--fill`) so the command
does not prompt interactively:

```
terminal(command="gh pr create --base main --head feature/login --title \"Fix login redirect\" --body-file ./pr-body.md")
terminal(command="gh pr create --fill")
terminal(command="gh pr create --draft --title \"WIP: parser\" --body-file ./pr-body.md")
terminal(command="gh pr create --reviewer monalisa,hubot --label bug --label \"help wanted\"")
```

- `--base` selects the target branch; without it gh uses the `gh-merge-base` git
  config or the repository default branch.
- `--head` skips any fork/push prompting; it accepts `owner:branch`.
- Mentioning `Fixes #123` or `Closes #123` in the body auto-closes that issue on
  merge.
- `--dry-run` prints what would be created without creating it.
- `--attach './login.png#The login error state'` uploads an image or video and
  rewrites a matching `![alt](./login.png)` reference in the body.

The created PR URL is printed on success.

## CI Checks

```
terminal(command="gh pr checks")
terminal(command="gh pr checks 123 --json name,state,bucket")
terminal(command="gh pr checks 123 --required")
```

`--json` adds a `bucket` field (`pass`, `fail`, `pending`, `skipping`,
`cancel`) that is easier to branch on than `state`. Exit codes: `8` when checks
are pending; `1` when a check failed. `--watch` blocks until checks finish (see
[run.md](./run.md) for watching Actions runs).

## Review and Comment

```
terminal(command="gh pr review --approve")
terminal(command="gh pr review 123 --request-changes --body-file ./review.md")
terminal(command="gh pr review 123 --comment -b \"Looks good, one nit inline\"")
terminal(command="gh pr comment 123 --body-file ./comment.md")
terminal(command="gh pr comment 123 --edit-last --body-file ./comment.md")
```

Exactly one of `--approve`, `--request-changes`, or `--comment` is required.
Use `--edit-last` to update your previous comment instead of posting a new one
(combine with `--delete-last --yes` when replacing).

## Merge

Choose a strategy explicitly (`--merge`, `--squash`, or `--rebase`); otherwise
gh prompts interactively:

```
terminal(command="gh pr merge 123 --squash --delete-branch")
terminal(command="gh pr merge 123 --merge --subject \"Merge feature/login\" --body ''")
terminal(command="gh pr merge 123 --auto --squash")
```

- `--auto` enables auto-merge and waits for requirements.
- On branches requiring a merge queue, omit the strategy: gh enqueues when checks
  pass or enables auto-merge when they have not.
- `--admin` bypasses requirements; use only when the user explicitly asks.
- `--delete-branch` deletes both local and remote head branches.

## Checkout

```
terminal(command="gh pr checkout 123")
terminal(command="gh pr checkout 123 --branch local-name --recurse-submodules")
```

## Edit

```
terminal(command="gh pr edit 123 --title \"New title\" --body-file ./body.md")
terminal(command="gh pr edit 123 --add-label bug --remove-label wip")
terminal(command="gh pr edit 123 --add-reviewer monalisa --remove-reviewer hubot")
terminal(command="gh pr edit 123 --add-assignee @me")
```
