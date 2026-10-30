# Erratum — BPO re-pin approval record (PR #17): when the extract-rebuild job runs

**This corrects a record of work. It is not a decision, and it changes no decision.** The
architect approved it in the closure decision of 2026-10-30
(`docs/decisions/2026-10-30-closure-decided.md`). The original record is preserved
unchanged.

## What was wrong

`docs/decisions/2026-10-28-bpo-repin-approved.md` was merged by PR #17 (`6c62a9b`). At
`a8fb873` its SHA-256 is
`c183aa23df7f2d481051e6dc85b16fd2acc348ac199c085498bc3b417c258979`. The row "Checks at the
reviewed head" (line 18) says two jobs were skipped at the PR head:

- `Deploy to Pages`;
- `Extracts still rebuild from the pinned sources`.

It gives the reason "because they run only on `main` and on the weekly schedule". That is
true of neither job as stated, and false for the extract-rebuild job.

## What is true

- **`Extracts still rebuild from the pinned sources`** is the `vendored` job in
  `.github/workflows/checks.yml`. Its condition is
  `if: github.event_name == 'schedule' || github.event_name == 'workflow_dispatch'`.
  - It runs on the weekly schedule and when the workflow is dispatched by hand.
  - It does not run on a push to `main`, or on a pull request.
  - The condition is the same at #15's head `f0fd009`, at its merge `6731f59` and at
    #17's merge `6c62a9b`. So the job did not run when #15 or #17 merged.
- **`Deploy to Pages`** is the `deploy` job in `.github/workflows/pages.yml`. It runs on a
  push to `main` and on a manual dispatch, never for a pull request. The record's reason
  is right for this job: it was skipped at the PR head because the PR head is not `main`.
- **What the record relied on still holds.** The approval did not depend on the job
  running on `main`. Its verification condition was a `vendor_upstream.py --confirm` run
  against `f0fd009`, recorded in the same table and attached to PR #15.

## The same sentence elsewhere

`docs/decisions/2026-10-27-inventory-i1-approved.md` (SHA-256
`0daa3d5cd3f95f369e3af191f74e8ff1dbf7978f573a9f57ee55d08ce04540f4`) gives the same reason
for the same two skipped jobs at PR #12's head. The facts above apply to it equally. That
record is also preserved unchanged.
