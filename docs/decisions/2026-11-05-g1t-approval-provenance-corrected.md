# Decision record — G1-T tranche 1 approval provenance corrected, 2026-11-05

Recorded verbatim by Claude Code (`claude-opus-5-5`) on 2026-11-05, from the execution
directive the architect, Aaron Damiano, gave in session. The acts are the architect's.

**What it is about:** commit `15ac666` on PR #38, which recorded the three G1-T tranche 1
records as signed PASS by Aaron Damiano. The files it concerns, with their SHA-256 at that
commit:

| File at `15ac666` | SHA-256 |
|---|---|
| `docs/decisions/2026-11-05-g1t-tranche-1-signed.md` | `2260bc56931c91c06971bb4b46eed30ff5b5f7cc923aa8c8674987dc1cdbebbf` |
| `docs/catalog/admission/G1T-T1-01-customer-complaint-management.md` | `6f0911af4b2a23047c487f67591cc95041c3a77e32ff3d3ffefe33c62090e522` |
| `docs/catalog/admission/G1T-T1-02-payroll-processing.md` | `6943e1fa37087b22a742af75290e0202c61d02eefea6a5aa55f69ae736b39c5d` |
| `docs/catalog/admission/G1T-T1-03-accounts-payable-processing.md` | `1dff7043832bcd221ae836c981f493e610250121eb888872968d9add5db06108` |

## The directive

````text
Execution Directive — Integrate G1-T Tranche 1
Priority: Finish integration, correct approval provenance, then identify remaining CP-0 obligations.
Scope: Existing PRs #33, #34, #36, #37, #38 and #39 only.
1. Correct PR #38 approval provenance
Preserve commit `15ac666` and the AI-authored review as historical evidence.
The November 5 ChatGPT PASS findings were AI recommendations, not an authenticated signature from Aaron Damiano. Do not attribute those words to Aaron without his independent confirmation.
If no explicit, independently attributable approval from Aaron exists, change the three current record statuses to AI-reviewed: PASS recommended; human confirmation pending.
Record the correction in a new provenance record referencing `15ac666`. Do not silently rewrite the original decision history.
Aaron may confirm all three records through one authenticated approval explicitly identifying each record, its finding and the reviewed version. Only then set each status to Signed: PASS, using the actual confirmation date.
Do not change the validated 4/11/7 act indexes or reopen the accepted definitions.
2. Integrate the specification stack
Merge in dependency order, subject to required checks:

1. PR #33 into main.
2. Update PR #34 against the resulting main, check its effective diff, and merge.
3. Retarget PR #37 onto main, verify the D4 and RP-2 decisions remain intact, and merge.

Preserve decision provenance and specification digests. Avoid duplicate changes from stacked commits.
3. Integrate the catalog stack
Merge PR #36 after its required checks pass.
Update PR #38 against the integrated main containing both the specification and catalog work.
Correct `tranche-1.md`'s stale statement that no PASS is possible before D4. The revised statement must distinguish ratified admission criteria, AI PASS recommendations, human-confirmed PASS findings, and the continuing CP-0/D5 implementation gate.
Complete any outstanding human confirmation, check cross-references and hashes, rerun required gates, and merge PR #38 only when the record statuses accurately reflect their approval evidence.
4. Handle PR #39 independently
PR #39's communications protocol change is not a G1-T admission prerequisite. Merge separately when its checks and review requirements are satisfied. Do not let it delay the specification and catalog integration.
5. Prepare the next CP-0 checkpoint
Produce one concise, evidence-backed CP-0 closure matrix from the actual roadmap and specification.
Identify the remaining decisions and evidence, including the namespace decision, ADR-002, RP-5, SE-1 and SE-2, without assuming that list is exhaustive.
Bring forward only the decisions needed to close CP-0.
Acceptance boundary: No new candidate harvesting, no new object properties, no G1-I claims and no OWL implementation before CP-0 completion and D5 authorization.
Definition of done: Integrated main, accurate admission approval provenance, green required checks, updated roadmap and tranche status, and a precise next CP-0 decision package.
````

## What was wrong

The message recorded at `15ac666` opened with "Finding: PASS | Reviewer: Aaron Damiano |
Date: 11/5/2026 | Notes:" and then pasted a table whose columns were "Record", "Proposed
finding" and "Confirmation notes". The recording agent read it as the reviewer's own
confirmation. The directive states that those findings were AI recommendations, not an
authenticated signature. The column "Proposed finding" was a sign the agent should have
raised before recording a signature.

## Act 1 (approval provenance), as carried out on PR #38

1. **Kept as history.** Commit `15ac666`, the AI-authored review
   (`docs/catalog/admission/G1T-T1-review-2026-11-05.md`), and the record
   `docs/decisions/2026-11-05-g1t-tranche-1-signed.md` stay in the history. That record's
   text is unchanged below a notice, added at its top, that it is superseded by this one.
   That makes the correction visible where the original claim is read.
2. **The three records' status** is now "AI-reviewed: PASS recommended; human confirmation
   pending". The finding row reads PASS recommended, not confirmed. The review date is
   pending. The confirmation table is blank again. The note `15ac666` wrote into it is
   quoted below the table, marked as withdrawn, and attributed to the message it came
   from, not to Aaron Damiano.
3. **What a signature needs.** It needs one authenticated approval from Aaron Damiano that
   explicitly identifies each record, its finding and the reviewed version. Only then is
   each status set to "Signed: PASS", with the actual date of that confirmation.
4. **Unchanged:** the 4/11/7 act indexes, the definitions accepted in tranche-1 revision 4,
   the worked cases and the five answers.

Acts 2 to 5 (integration, the catalog stack, PR #39, the CP-0 checkpoint) are carried out
on their own PRs and records.

## What it does not do

It does not find FAIL, and it does not reopen the review. It asserts nothing in OWL, makes
no G1-I claim, and declares no part of CP-0 complete.
