# Provision mode

Create or verify tracker resources after checkpoint approval, before
`kodit.json` is written. The setup phase's `setup-kodit` skill invokes this;
`issue-tracker` performs the backend-specific work.

## Steps

1. Read the setup draft `setup-issue-tracker.md`. If missing, stop and name it.
   The draft is the source of truth during provisioning — `kodit.json` does
   not exist yet at this point.
2. Follow the `issue-tracker` skill in **provision mode** to create or verify
   tracker resources. For file-based: seed `.kodit/issues/`. For Linear: create
   or find the project, ensure states and labels exist.
3. If provisioning succeeds and the backend is Linear, append the resolved
   project ID to the draft. Do not write `kodit.json` — that happens in
   write mode.
4. Report what was created or verified.

## Failure handling

- Never create resources in a workspace/team other than the one in the draft.
- If a required resource cannot be created, stop and report which one; do not
  partially configure the tracker.
- If provisioning fails, leave the draft in place so the step can be retried —
  write mode must not remove drafts for an unprovisioned tracker.
