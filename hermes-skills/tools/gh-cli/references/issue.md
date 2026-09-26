# gh Issue Reference

Manage GitHub issues: list, view, create, edit, comment, develop, and close. An
issue can be given as a number (`123`) or a URL.

## Commands

| Command | Purpose |
| --- | --- |
| `gh issue create` | Create a new issue (alias `gh issue new`) |
| `gh issue list` | List issues (alias `gh issue ls`) |
| `gh issue view` | Display an issue's title, body, and comments |
| `gh issue status` | Show status of issues relevant to you |
| `gh issue comment` | Add or edit a comment |
| `gh issue edit` | Edit title, body, labels, assignees, milestone, type |
| `gh issue close` / `gh issue reopen` | Close or reopen |
| `gh issue develop` | Create or list linked branches for an issue |
| `gh issue pin` / `gh issue unpin` | Pin or unpin |
| `gh issue lock` / `gh issue unlock` | Lock or unlock the conversation |
| `gh issue transfer` / `gh issue delete` | Move to another repo; delete |

## List and View

```
terminal(command="gh issue list")
terminal(command="gh issue list --assignee @me --state open")
terminal(command="gh issue list --label bug --label \"help wanted\" --limit 50")
terminal(command="gh issue list --author monalisa --state all")
terminal(command="gh issue list --search 'error no:assignee sort:created-asc'")
terminal(command="gh issue list --json number,title,state,labels --jq '.[] | \"#\(.number) \(.title)\"'")
terminal(command="gh issue view 123")
terminal(command="gh issue view 123 --comments")
terminal(command="gh issue status")
```

`gh issue list` defaults to open issues; pass `--state closed` or `--state all`
for the rest. `--search` accepts GitHub search qualifiers.

## Create

Always pass `--title` and `--body`/`--body-file` so the command does not prompt:

```
terminal(command="gh issue create --title \"Login fails on Safari\" --body-file ./issue.md")
terminal(command="gh issue create --title \"Crash on startup\" --label bug --assignee @me")
terminal(command="gh issue create --title \"Docs typo\" --label docs --milestone \"v1.0\"")
terminal(command="gh issue create --title \"Sub-task\" --parent 100")
```

- `--label` accepts commas or repeated flags.
- `--assignee @me` self-assigns; `--assignee @copilot` assigns Copilot.
- `--parent 100` creates a sub-issue; `--blocked-by` / `--blocking` set
  relationships by number or URL.
- `--template` starts from a repository issue template.

The created issue URL is printed on success.

## Comment

```
terminal(command="gh issue comment 123 --body-file ./comment.md")
terminal(command="gh issue comment 123 --edit-last --body-file ./comment.md")
terminal(command="gh issue comment 123 --delete-last --yes")
```

## Edit

```
terminal(command="gh issue edit 123 --title \"New title\" --body-file ./body.md")
terminal(command="gh issue edit 123 --add-label bug --remove-label triage")
terminal(command="gh issue edit 123 --add-assignee @me --remove-assignee monalisa")
terminal(command="gh issue edit 123 --milestone \"Version 1\"")
terminal(command="gh issue edit 123 --add-blocked-by 200 --add-blocking 300")
terminal(command="gh issue edit 123 124 --add-label \"help wanted\"")
```

Multiple issue numbers may be edited at once when they share a repository.

## Close and Reopen

```
terminal(command="gh issue close 123")
terminal(command="gh issue close 123 --comment \"Fixed in #130\"")
terminal(command="gh issue close 123 --reason \"not planned\"")
terminal(command="gh issue close 123 --duplicate-of 456")
terminal(command="gh issue reopen 123 --comment \"Still reproducible\"")
```

`--reason` accepts `completed`, `not planned`, or `duplicate`.

## Linked Branches

```
terminal(command="gh issue develop 123 --list")
terminal(command="gh issue develop 123 --base main --checkout")
terminal(command="gh issue develop 123 --name fix-login --checkout --worktree /path/to/wt")
```

The created branch is configured as the base branch for a later `gh pr create`.
