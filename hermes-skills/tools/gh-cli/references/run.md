# gh Actions Reference

View GitHub Actions workflow runs and workflows: status, logs, artifacts, and
re-runs. Every command accepts `-R, --repo [HOST/]OWNER/REPO`.

## Commands

| Command | Purpose |
| --- | --- |
| `gh run list` | List recent workflow runs (alias `gh run ls`) |
| `gh run view` | View a run summary, jobs, or logs |
| `gh run watch` | Watch a run until it completes |
| `gh run rerun` | Re-run a whole run, failed jobs, or one job |
| `gh run cancel` / `gh run delete` | Cancel or delete a run |
| `gh run download` | Download run artifacts |
| `gh workflow list` | List workflows (alias `gh workflow ls`) |
| `gh workflow view` | View a workflow summary or YAML |
| `gh workflow run` | Trigger a `workflow_dispatch` workflow |
| `gh workflow enable` / `gh workflow disable` | Toggle a workflow |

## List and View Runs

```
terminal(command="gh run list --limit 10")
terminal(command="gh run list --workflow ci.yml --branch main")
terminal(command="gh run list --status failure --limit 5")
terminal(command="gh run list --json databaseId,status,conclusion,headBranch,displayTitle")
terminal(command="gh run view 12345")
terminal(command="gh run view 12345 --verbose")
terminal(command="gh run view 12345 --log")
terminal(command="gh run view 12345 --log-failed")
terminal(command="gh run view 12345 --json jobs --jq '.jobs[] | {name, databaseId, conclusion}'")
terminal(command="gh run view 12345 --exit-status")
```

`--exit-status` makes `gh run view` exit non-zero if the run failed, which is the
clean way to gate on CI. To see runs associated with a pull request, prefer
`gh pr checks` over parsing `gh run list`.

## Watch a Run

```
terminal(command="gh run watch 12345")
terminal(command="gh run watch 12345 --compact --exit-status")
```

`gh run watch` blocks until the run completes. Do not run it without a timeout
on an agent turn; pair it with `--exit-status` when the outcome matters.

## Re-run and Cancel

```
terminal(command="gh run rerun 12345")
terminal(command="gh run rerun 12345 --failed")
terminal(command="gh run rerun 12345 --job 456789 --debug")
terminal(command="gh run cancel 12345")
terminal(command="gh run cancel 12345 --force")
```

`--job` takes the job **databaseId**, not the number in the browser URL:

```
terminal(command="gh run view 12345 --json jobs --jq '.jobs[] | select(.name==\"build\") | .databaseId'")
```

## Artifacts

```
terminal(command="gh run download 12345")
terminal(command="gh run download 12345 --name coverage")
terminal(command="gh run download 12345 --pattern '*.zip' --dir ./artifacts")
terminal(command="gh run download --name coverage")
```

Each artifact is extracted into a directory named after the artifact; a single
named artifact extracts into the current directory. Without a run ID, gh
downloads the latest matching artifact across runs.

## Workflows

```
terminal(command="gh workflow list")
terminal(command="gh workflow list --all")
terminal(command="gh workflow view ci.yml")
terminal(command="gh workflow view ci.yml --yaml")
terminal(command="gh workflow run ci.yml")
terminal(command="gh workflow run release.yml --ref my-branch -f version=1.2.3")
terminal(command="gh workflow disable ci.yml")
```

`gh workflow run` requires the workflow to declare an `on.workflow_dispatch`
trigger. Inputs are passed with `-f key=value`, `-F` (typed, `@file` supported),
or `--json` on stdin. The created run URL is returned when available.
