# Linear CLI Command Reference

## Commands

- [api](./api.md) - Make a raw GraphQL API request
- [auth](./auth.md) - Manage Linear authentication
- [config](./config.md) - Interactively generate .linear.toml configuration
- [cycle](./cycle.md) - Manage Linear team cycles
- [document](./document.md) - Manage Linear documents
- [initiative](./initiative.md) - Manage Linear initiatives
- [initiative-update](./initiative-update.md) - Manage initiative status updates (timeline posts)
- [issue](./issue.md) - Manage Linear issues
- [label](./label.md) - Manage Linear issue labels
- [markdown](./markdown.md) - Linear-flavored Markdown: mentions and collapsible sections
- [milestone](./milestone.md) - Manage Linear project milestones
- [project](./project.md) - Manage Linear projects
- [project-update](./project-update.md) - Manage project status updates
- [schema](./schema.md) - Print the GraphQL schema to stdout
- [team](./team.md) - Manage Linear teams
- [template](./template.md) - Browse Linear issue, project, and document templates. Apply one with `issue create --template` or `project create --template`.
- [user](./user.md) - Manage Linear users

## Quick Reference

```bash
# Get help for any command
linear <command> --help
linear <command> <subcommand> --help
```

## Full Command Tree

Generated from `linear --help` against CLI v2.2.0:

```bash
linear api

linear auth
linear auth default
linear auth list
linear auth login
linear auth logout
linear auth migrate
linear auth token
linear auth whoami

linear config

linear cycle
linear cycle list
linear cycle view

linear document
linear document comment
linear document comment add
linear document comment list
linear document create
linear document delete
linear document list
linear document update
linear document view

linear initiative
linear initiative add-project
linear initiative archive
linear initiative comment
linear initiative comment add
linear initiative comment list
linear initiative create
linear initiative delete
linear initiative list
linear initiative remove-project
linear initiative unarchive
linear initiative update
linear initiative view

linear initiative-update
linear initiative-update create
linear initiative-update list

linear issue
linear issue agent-session
linear issue agent-session list
linear issue agent-session view
linear issue archive
linear issue attach
linear issue comment
linear issue comment add
linear issue comment delete
linear issue comment list
linear issue comment update
linear issue commits
linear issue create
linear issue delete
linear issue describe
linear issue id
linear issue link
linear issue mine
linear issue pull-request
linear issue query
linear issue relation
linear issue relation add
linear issue relation delete
linear issue relation list
linear issue start
linear issue title
linear issue update
linear issue url
linear issue view

linear label
linear label create
linear label delete
linear label list

linear markdown

linear milestone
linear milestone create
linear milestone delete
linear milestone list
linear milestone update
linear milestone view

linear project
linear project comment
linear project comment add
linear project comment list
linear project create
linear project delete
linear project list
linear project update
linear project view

linear project-update
linear project-update create
linear project-update list

linear schema

linear team
linear team autolinks
linear team create
linear team delete
linear team id
linear team list
linear team members
linear team states

linear template
linear template list
linear template view

linear user
linear user list
```
