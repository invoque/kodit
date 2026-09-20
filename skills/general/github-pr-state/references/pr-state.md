# Pull request state return shape

Defines the structured facts `github-pr-state` should return to callers so
workflow skills do not embed GitHub mechanics.

## Minimum returned fields

- `status`: `selected` | `none` | `multiple` | `missing_access` | `publish_failed`
- `can_publish`: `true` | `false`
- `pr`: number, URL, author, head SHA, base, draft status, created/updated time
- `checks`: per-check name/state/result and aggregate summary
- `mergeability`: mergeable/not/unknown, conflicting files when available
- `reviews`: reviewer, state, body, and timestamps
- `changed_files`: path, status, additions, deletions, patch when available

## Publishing shape

When asked to publish, return:

- `publish_result`: review ID or URL when available, state published, success/failure, and fallback note if GitHub publishing failed.
