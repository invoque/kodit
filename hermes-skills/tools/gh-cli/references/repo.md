# gh Repository, Search, Gist, Label Reference

Work with repositories, search across GitHub, publish gists, and manage labels.

## Repository Commands

| Command | Purpose |
| --- | --- |
| `gh repo view` | Show a repository's description and README |
| `gh repo list` | List repositories owned by a user or org |
| `gh repo create` | Create a repository (alias `gh repo new`) |
| `gh repo clone` | Clone a repository |
| `gh repo fork` | Fork a repository |
| `gh repo sync` | Sync a fork from its parent |
| `gh repo edit` | Edit description, homepage, visibility, features |
| `gh repo archive` / `gh repo unarchive` | Archive or unarchive |
| `gh repo rename` / `gh repo delete` | Rename or delete |
| `gh repo set-default` | Configure the default repo for a directory |
| `gh repo deploy-key` / `gh repo autolink` | Deploy keys and autolinks |

```
terminal(command="gh repo view")
terminal(command="gh repo view owner/repo")
terminal(command="gh repo view owner/repo --json name,description,defaultBranchRef,stargazerCount,isPrivate")
terminal(command="gh repo list myorg --limit 50")
terminal(command="gh repo list myorg --language go --topic cli --visibility public")
terminal(command="gh repo create my-project --public --clone")
terminal(command="gh repo create my-project --private --source=. --remote=upstream")
terminal(command="gh repo clone owner/repo")
terminal(command="gh repo clone owner/repo ./workspace/repo -- --depth=1")
terminal(command="gh repo fork owner/repo --clone")
terminal(command="gh repo fork owner/repo --clone=false")
terminal(command="gh repo sync owner/fork --branch main")
```

- Repository arguments accept `OWNER/REPO` or a URL; `OWNER/` defaults to the
  authenticating user.
- `gh repo clone` forwards flags after `--` to `git clone`; forking adds the
  parent as an `upstream` remote unless `--no-upstream` is passed.
- `gh repo sync` fast-forwards the destination default branch; `--force` hard
  resets it.
- Destructive commands (`gh repo delete`) require confirmation; pass `--yes` only
  when the user has explicitly authorized deletion.

## Search

| Command | Purpose |
| --- | --- |
| `gh search repos` | Search repositories |
| `gh search issues` | Search issues (and PRs with `--include-prs`) |
| `gh search prs` | Search pull requests |
| `gh search code` | Search code |
| `gh search commits` | Search commits |

Search accepts raw GitHub qualifiers as separate arguments, parameter flags, or
both. Use `--` before a query that starts with a hyphen:

```
terminal(command="gh search repos cli shell")
terminal(command="gh search repos --language=go --stars='>1000' --limit 20")
terminal(command="gh search repos --owner=microsoft --visibility=public")
terminal(command="gh search issues readme typo")
terminal(command="gh search issues --assignee=@me --state=open --include-prs")
terminal(command="gh search issues label:bug author:monalisa state:open")
terminal(command="gh search issues -- -label:bug")
terminal(command="gh search prs fix bug --repo cli/cli")
terminal(command="gh search prs --review-requested=@me --state=open")
terminal(command="gh search code panic --repo cli/cli --language=go")
terminal(command="gh search repos --json fullName,stargazersCount,description --jq '.[] | \"\(.fullName) ★\(.stargazersCount)\"'")
```

`gh search issues` supports `--search-type semantic|hybrid` for relevance-ranked
search (these return a single page and ignore `--sort`/`--order`). Code search
uses the legacy engine and may not match github.com results.

## Gists

| Command | Purpose |
| --- | --- |
| `gh gist create` | Create a gist (alias `gh gist new`) |
| `gh gist list` | List your gists (alias `gh gist ls`) |
| `gh gist view` | View a gist and its files |
| `gh gist edit` / `gh gist delete` | Edit or delete |
| `gh gist clone` / `gh gist rename` | Clone or rename |

```
terminal(command="gh gist create ./notes.md --desc \"Meeting notes\"")
terminal(command="gh gist create ./log.txt --public")
terminal(command="cat build.log | gh gist create -f build.log")
terminal(command="gh gist list --limit 20 --secret")
terminal(command="gh gist list --filter octo --include-content")
terminal(command="gh gist view <id> --files")
terminal(command="gh gist view <id> --filename notes.md --raw")
```

Gists are secret by default; `--public` lists them publicly.

## Labels

```
terminal(command="gh label list")
terminal(command="gh label list --search bug --sort name")
terminal(command="gh label create needs-triage --color FBCA04 --description 'Needs triage'")
terminal(command="gh label edit bug --color d73a4a --description 'Something is broken'")
terminal(command="gh label delete stale --yes")
terminal(command="gh label clone owner/source-repo")
```

`--color` is a six-digit hex value without `#`.
