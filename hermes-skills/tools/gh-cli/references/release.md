# gh Release Reference

Manage GitHub Releases: create, view, upload and download assets.

## Commands

| Command | Purpose |
| --- | --- |
| `gh release create` | Create a release (alias `gh release new`) |
| `gh release list` | List releases (alias `gh release ls`) |
| `gh release view` | View a release; latest when no tag is given |
| `gh release edit` | Edit notes, title, draft/prerelease state |
| `gh release upload` | Upload assets to a release |
| `gh release download` | Download assets or source archives |
| `gh release delete` | Delete a release |
| `gh release delete-asset` | Delete one asset |
| `gh release verify` / `gh release verify-asset` | Verify attestations |

## Create

Always pass notes via `--notes` or `--notes-file`, or use `--generate-notes`, so
the command does not prompt:

```
terminal(command="gh release create v1.2.3 --title \"v1.2.3\" --notes-file ./release-notes.md")
terminal(command="gh release create v1.2.3 --generate-notes")
terminal(command="gh release create v1.2.3 --notes-from-tag")
terminal(command="gh release create v1.2.3 --draft --prerelease --notes-file ./notes.md")
terminal(command="gh release create v1.2.3 ./dist/*.tgz")
terminal(command="gh release create v1.2.3 '/path/to/asset.zip#My display label'")
```

- If the tag does not exist, gh creates it from the default branch (or `--target`).
  `--verify-tag` aborts unless the tag already exists.
- `--generate-notes` uses the GitHub Release Notes API; `--notes-start-tag`
  controls the range. Additional `--notes` are prepended.
- `--latest=false` explicitly avoids marking the release latest.
- `--fail-on-no-commits` fails when there are no new commits since the last release.
- Asset labels use `file#display label`. Immutable releases lock tags and assets
  only after publish; draft releases remain editable.

## View and List

```
terminal(command="gh release view")
terminal(command="gh release view v1.2.3")
terminal(command="gh release view v1.2.3 --json tagName,isDraft,isPrerelease,assets")
terminal(command="gh release list --limit 10")
terminal(command="gh release list --exclude-drafts --exclude-pre-releases")
```

## Upload and Download

```
terminal(command="gh release upload v1.2.3 ./dist/*.tgz")
terminal(command="gh release upload v1.2.3 ./asset.zip --clobber")
terminal(command="gh release download v1.2.3")
terminal(command="gh release download v1.2.3 --pattern '*.deb' --dir ./downloads")
terminal(command="gh release download --pattern '*.tar.gz'")
terminal(command="gh release download v1.2.3 --archive=zip")
```

`--clobber` deletes existing same-named assets before uploading; if the upload
then fails, the originals are lost. Without a tag, `gh release download` requires
`--pattern` or `--archive`.

## Edit and Delete

```
terminal(command="gh release edit v1.2.3 --notes-file ./updated-notes.md")
terminal(command="gh release edit v1.2.3 --draft=false")
terminal(command="gh release delete v1.2.3")
terminal(command="gh release delete v1.2.3 --yes --cleanup-tag")
```

`gh release delete` prompts for confirmation unless `--yes` is passed. Prefer
editing over delete-and-recreate for a published release.
