# gh Auth Reference

Authenticate gh and git with GitHub, inspect the active account, and obtain
tokens for scripting.

## Commands

| Command | Purpose |
| --- | --- |
| `gh auth login` | Log in to a GitHub account |
| `gh auth logout` | Log out of a GitHub account (local only; does not revoke) |
| `gh auth refresh` | Expand or fix the permission scopes of stored credentials |
| `gh auth setup-git` | Configure `git` to use gh as a credential helper |
| `gh auth status` | Display active account and authentication state per host |
| `gh auth switch` | Switch the active account for a host |
| `gh auth token` | Print the token gh uses for a hostname and account |

## Check Authentication

```
terminal(command="gh auth status")
terminal(command="gh auth status --active --hostname github.com")
terminal(command="gh auth status --json hosts")
```

Each host section names the active account. `gh auth status` exits `1` when any
account has authentication issues — so a non-zero exit here is the auth check,
not a command failure to retry blindly. With `--json`, it always exits `0`
unless there is a fatal error.

## Log In

Interactive browser flow stores the token in the system credential store (and
falls back to a plain-text file when no store is available):

```
terminal(command="gh auth login")
```

Non-interactive, from a token on stdin:

```
terminal(command="gh auth login --with-token < token.txt")
```

Minimum scopes for a classic PAT: `repo`, `read:org`, `gist`. Prefer setting
`GH_TOKEN` for fine-grained PATs instead of `--with-token`.

## Token and Environment Precedence

`GH_TOKEN`, then `GITHUB_TOKEN`, are used when a command targets `github.com` or
a `ghe.com` subdomain, and take precedence over stored credentials:

- Hermes injects `GH_TOKEN` into `terminal` sandboxes when it is configured, so
  remote backends (Docker, Modal, SSH) work without a system keyring.
- **A configured `GH_TOKEN` silently overrides keyring login.** If commands run
  as the wrong user or fail with scopes that do not match `gh auth status`, check
  `GH_TOKEN` first.
- Enterprise Server uses `GH_ENTERPRISE_TOKEN` then `GITHUB_ENTERPRISE_TOKEN`.

`GH_HOST` selects a host when it cannot be inferred from the local git remote.
`GH_REPO` sets `[HOST/]OWNER/REPO` for commands that otherwise use the local
repository. See `gh help environment` for the full list.

## Multiple Accounts

```
terminal(command="gh auth switch --hostname github.com --user monalisa")
terminal(command="gh auth status")
```

`gh auth refresh` changes scopes for the **active** account; switch to an
inactive account first, then switch back. Minimum scopes (`repo`, `read:org`,
`gist`) cannot be removed. Add project scope with:

```
terminal(command="gh auth refresh -s project")
```

## Set Up Git Credential Helper

```
terminal(command="gh auth setup-git")
terminal(command="gh auth setup-git --hostname enterprise.internal")
```

Fails when no account on the host is authenticated; pass `--force` with
`--hostname` to configure anyway.

## Use the Token in Scripts

```
terminal(command="gh auth token")
terminal(command="curl -s -H \"Authorization: Bearer $(gh auth token)\" https://api.github.com/user")
```

Never echo, log, or commit the token. Use `gh auth status --show-token` only when
the user explicitly asks to reveal it.
