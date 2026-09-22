# pr-request

Open a pull request for the active milestone branch.

## When to Use

- After `implement` completes a milestone.
- When you ask to open a PR for implemented work.

## Prerequisites

- `kodit.json` must exist (checked via `kodit-config` in check mode).
- Exactly one non-`closed` milestone must exist.
- **Every task** must be `review` or `done`. The skill refuses when any task is `open`, `spec`, `plan`, `implement`, `blocked`, or carries `ready-for-human`, `needs-info`, or `needs-triage`.

## How It Works

### 1. Verify entry

Follow `kodit-config` in check mode. If `kodit.json` is missing, stop and direct to `setup-kodit`.

### 2. Select and present the milestone

Follow `issue-tracker` in operate mode. If no milestone is non-`closed`, refuse and direct to `milestone-planning`. Present the single non-`closed` milestone's ID, goal, branch, and story/task counts.

### 3. Refuse when not ready

List every story and task. Stop without creating a PR when any task is still `open`, `spec`, `plan`, or `implement`, is `blocked`, or carries a special label. **Never mark tasks `done` here.**

### 4. Derive the branches

Read `git.dev_branch`, `git.feature_prefix`, and `git.remote` from `kodit.json`. The head is the milestone branch; the base is `dev`. If `git` is null or no remote is configured, stop and explain.

### 5. Delegate PR creation

Follow `github-pr` with the head, base, remote, and a title/body built from the milestone. On success, keep the returned URL and whether the PR was created or already existed.

### 6. Record the URL

Follow `issue-tracker` in operate mode to write `**PR:** <url>` in the milestone charter. This write is idempotent and changes **no task, story, or milestone status**.

### 7. Summarize and hand off

Present the milestone, head into base, the PR URL, and what was recorded. Tell the user to run `pr-review`. **Do not merge.**

## User Decisions

None. This skill is entirely automated after the readiness check passes.

## Key Rules

- **No approval gates.** After the readiness gate passes, the skill runs without user intervention.
- **No status changes.** The PR URL is recorded as metadata only; task, story, and milestone statuses do not change.
- **No merge.** PR creation and merge are separate concerns.

## Artifacts Modified

- Milestone charter (PR URL line appended) via issue-tracker operate mode

## Handoff

**Next skill:** `pr-review`

## Source

- Canonical definition: `skills/workflow/pr-request/SKILL.md`
