# gh api Reference

Make authenticated GitHub API requests when no dedicated gh command covers the
operation. `gh api <endpoint>` targets REST (API v3); `gh api graphql` targets
GraphQL (API v4).

Prefer `gh pr`, `gh issue`, `gh release`, and friends first — they handle
pagination, formatting, and edge cases. Reach for `gh api` for endpoints with no
command, or to build custom shapes with GraphQL.

## Endpoint and Placeholders

```
terminal(command="gh api repos/{owner}/{repo}")
terminal(command="gh api repos/{owner}/{repo}/releases")
terminal(command="gh api /orgs/myorg/repos")
```

`{owner}`, `{repo}`, and `{branch}` are replaced from the current repository (or
`GH_REPO`). Quote values containing braces in shells that interpret them.

## Request Method and Fields

```
terminal(command="gh api -X GET search/issues -f q='repo:cli/cli is:open remote'")
terminal(command="gh api repos/{owner}/{repo}/issues/123/comments -f body='Hi from the CLI'")
terminal(command="gh api -X PATCH repos/{owner}/{repo} -f description='New description'")
terminal(command="gh api repos/{owner}/{repo}/rulesets --input ruleset.json")
```

- `-f/--raw-field key=value` sends a string parameter.
- `-F/--field key=value` converts `true`/`false`/`null`/integers, expands
  `{owner}`/`{repo}`/`{branch}`, and reads `@file` or `@-` (stdin) values.
- Adding any field switches the method to `POST`; force `GET` with `-X GET`.
- `--input file` sends a prebuilt body (`-` for stdin); field flags then become
  query parameters.
- Nested payloads use `key[subkey]=value`; arrays use `key[]=value` repeated.

## GraphQL

Pass the document as the `query` field. Non-null type markers (`String!`) are
safe inside single quotes here, unlike some other CLIs:

```
terminal(command="gh api graphql -f query='query { viewer { login name } }'")
terminal(command="gh api graphql -F owner='{owner}' -F name='{repo}' -f query='
query($name: String!, $owner: String!) {
  repository(owner: $owner, name: $name) { releases(last: 3) { nodes { tagName } } }
}'")
```

All fields other than `query` and `operationName` become GraphQL variables.

## Pagination

```
terminal(command="gh api repos/{owner}/{repo}/issues --paginate")
terminal(command="gh api graphql --paginate -f query='query($endCursor: String) {
  viewer { repositories(first: 100, after: $endCursor) {
    nodes { nameWithOwner }
    pageInfo { hasNextPage endCursor }
  } }
}'")
terminal(command="gh api graphql --paginate --slurp -f query='...'")
```

REST pagination is automatic. GraphQL pagination requires the query to accept
`$endCursor: String` and fetch `pageInfo { hasNextPage endCursor }`; each page is
a separate JSON document unless `--slurp` wraps them in one array.

## Filter Output

```
terminal(command="gh api repos/{owner}/{repo}/issues --jq '.[].title'")
terminal(command="gh api repos/{owner}/{repo}/issues/1 --jq '.labels[].name'")
terminal(command="gh api repos/{owner}/{repo}/issues --template '{{range .}}{{.number}} {{.title}}{{\"\\n\"}}{{end}}'")
terminal(command="gh api user --silent")
```

`-q/--jq` filters with jq syntax without needing `jq` installed; `-t/--template`
uses Go templates (see `gh help formatting`).

## Headers and Previews

```
terminal(command="gh api -H 'Accept: application/vnd.github.v3+json' repos/{owner}/{repo}")
terminal(command="gh api --preview corsair repos/{owner}/{repo}/whatever")
terminal(command="gh api -i repos/{owner}/{repo} | head -20")
```

`-i/--include` adds the status line and headers; `--verbose` logs the full HTTP
exchange; `--cache 1h` caches a response.

## Environment

`GH_TOKEN` then `GITHUB_TOKEN` authenticate `github.com` requests;
`GH_ENTERPRISE_TOKEN` then `GITHUB_ENTERPRISE_TOKEN` cover Enterprise Server;
`GH_HOST` selects another host. These are the same tokens `gh auth` manages —
see [auth.md](./auth.md).

## Safety

- Read before write: fetch the current object (`gh api ...`) before mutating it.
- Never send `-X DELETE` or destructive mutations without explicit user consent.
- Do not paste tokens into commands; rely on gh's stored or injected credentials.
