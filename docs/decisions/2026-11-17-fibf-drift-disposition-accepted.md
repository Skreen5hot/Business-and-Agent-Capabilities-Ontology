# Decision record — FIBF source drift disposition accepted; original pins retained; bounded presentation-drift check approved, 2026-11-17

Recorded verbatim by Claude Code (`claude-opus-5-5`) on 2026-11-17, from the decision the
architect, Aaron Damiano, Product Owner and Ontology Architect, gave in session on the
disposition committed as `e748de8` on `sources/fibf-drift-disposition`. The acts are the
architect's. This record makes none.

## What it is about

`sources/fibf-drift-disposition` at `e748de8` (on `main` at `b0003bd`):

| Record | SHA-256 at `e748de8` |
| --- | --- |
| `docs/proposals/2026-11-17-fibf-source-drift-disposition.md` (the disposition accepted) | `0b81d62f0fcf3a3a30d9835fdcc5ac26eabe730832860dce360752bcd90bf559` |
| `docs/sources/inventory/rights.yaml` (the rights record whose pins are retained) | `dfea0b3606903d71fac94516513e010acc3c81d2d2e52cf7d1890cb8bef0e262` |
| `tools/inventory/rights.py` (the check to be corrected) | `73cf203d85672805a741bc56f7d0f123cff3b86b0bfdfff308ba624ae3a8eec1` |

## The decision

> Subject: Architect Decision — FIBF Source Drift Disposition and Rights-Check Correction
> I have reviewed `2026-11-17-fibf-source-drift-disposition.md`, committed as `e748de8`.
> DECISION: ACCEPT THE DISPOSITION. RETAIN THE ORIGINAL PINS. APPROVE BOTH PROPOSED FOLLOW-UPS WITH THE SAFEGUARDS BELOW.
> 1. Source Disposition — APPROVED
> I accept the documented finding that:
>
> * The 26 FIBF HTML pages differ from their pinned versions only in the identified asset build-number tokens.
> * Restoring the original tokens reproduces all 26 pinned SHA-256 digests.
> * The GSA website policies page has presentation and navigation changes, while its substantive policy and rights language remains unchanged.
> * All 39 FIBF workbooks and the other identified federal and APQC source items remain byte-identical to their pins.
>
> Retain every original approved SHA-256 pin.
> Do not update source identity, licensing disposition, redistribution permissions or the 2026-10-28 rights decision.
> No new rights review is required for the documented presentation-only changes.
> 2. `rights.yaml` Evidence Addendum — APPROVED
> Add the documented findings beside the existing `fibf-2026-10-28` evidence.
> Record:
>
> * The original pinned SHA-256 values.
> * The November 17 observed digests, explicitly labeled as observations rather than approved replacement pins.
> * The identified FIBF asset build-number substitution.
> * The Internet Archive snapshots preserving the originally approved evidence.
> * The unchanged GSA rights language.
> * The determination that no source-content or licensing change occurred.
>
> Preserve all existing source locators and rights decisions.
> 3. Weekly Rights Check — BOUNDED CHANGE APPROVED
> I authorize updating `rights.py --confirm` to distinguish verified presentation-only HTML drift from substantive source changes.
> Retain strict byte verification as the first check.
> When the original bytes match, report PASS as before.
> When they differ, the checker may classify the difference as tolerated presentation drift only under these conditions:
> For the 26 identified FIBF pages:
>
> * Permit changes to the specifically identified asset build-number tokens.
> * Normalize those tokens against the approved pinned baseline.
> * Require the resulting bytes to reproduce the original pinned SHA-256 exactly.
> * Reject any additional unexplained difference.
>
> For the GSA website policies page:
>
> * Compare against the independently preserved approved baseline.
> * Permit only verified changes to navigation, Drupal settings, asset-version tokens and immaterial whitespace.
> * Require the substantive page content, relevant links and the complete rights-and-redistribution language to remain unchanged.
> * Do not broadly disregard arbitrary changes outside `<main>` or rely on text equality alone when meaningful links or attributes may change.
>
> For all other evidence documents:
> Retain the current strict byte-matching rules. No general relaxation is authorized.
> 4. Required Failure Behavior
> The revised checker must fail when:
>
> * Substantive source text changes.
> * Rights or redistribution language changes.
> * A relevant source link changes unexpectedly.
> * An unexplained HTML difference remains.
> * The approved baseline cannot be verified.
> * The parser or comparison encounters an ambiguous or unsupported condition.
>
> Every byte mismatch must remain visible in the report, even when the classified result is acceptable presentation drift.
> Distinguish these statuses clearly:
>
> * Exact pinned-byte match.
> * Verified presentation-only drift.
> * Substantive or unexplained drift — failure.
>
> A tolerated presentation change must never silently replace the approved evidence or become a new source pin.
> 5. Regression Tests — REQUIRED
> Add focused positive and negative tests demonstrating:
>
> 1. Exact pinned bytes pass.
> 2. A FIBF asset build-number-only change passes with a visible drift report.
> 3. A FIBF substantive text change fails, even when its build numbers are recognizable.
> 4. The verified GSA navigation and asset changes pass.
> 5. A GSA rights-language, substantive-content or relevant-link change fails.
> 6. Unavailable or unverifiable approved baselines fail closed.
> 7. Non-HTML evidence remains subject to strict byte matching.
>
> Do not build a general-purpose website-diff framework. Implement only the bounded normalization and comparisons needed for this documented issue.
> 6. Repository Integration — AUTHORIZED
> You may push `sources/fibf-drift-disposition`, complete the evidence addendum and checker correction, and submit them for repository review.
> After the required tests and CI pass, merge the approved changes.
> Run the networked rights-documents check to verify that it correctly recognizes the documented drift. Confirm that the previously blocked weekly federal harvest check can execute normally again.
> If the check discovers any additional unexplained differences, report those separately instead of expanding the tolerance rules automatically.
> 7. Closure
> Once the corrected check passes against the documented evidence, close this FIBF source-drift issue.
> Do not reopen CP-3, the accepted coverage-register batch, or the existing licensing decisions.
> This decision does not authorize additional source redistribution, new source pins or changes to ontology terms.
> FINAL DECISION: ORIGINAL PINS RETAINED. EVIDENCE ADDENDUM APPROVED. BOUNDED PRESENTATION-DRIFT CHECK APPROVED. IMPLEMENT, TEST AND CLOSE THE ISSUE WITHOUT ANOTHER ARCHITECTURAL REVIEW.

## How it is applied

- **Evidence addendum (section 2).** `docs/sources/inventory/rights.yaml`, source
  `fibf-2026-10-28`, gains `presentation_drift`. Every original pin is unchanged. The
  block records the finding, the build-number substitution (`1790778396531677562` to
  `1794604162961183849`, with `1617716038051754794` unchanged) for the 26 pages, the
  Internet Archive captures (`20261028084510` and `20261023063449` for the policies page,
  `20261107030843` for the index), and the 27 digests observed on 2026-11-17, as
  observations. `rights.py` refuses an observation equal to its pin.
- **Bounded check (sections 3 and 4).** `tools/inventory/rights.py --confirm` checks bytes
  first. On a mismatch it classifies only evidence the block names, and prints one of
  three statuses: exact pinned-byte match, verified presentation-only drift, or
  substantive or unexplained drift (a failure). The two rules:
  - FIBF pages: restore one new build number to the baseline, and require the pinned
    sha256 exactly.
  - GSA policies page: fetch the archived baseline from `web.archive.org` only, and require
    its sha256 to be the pin. Then compare every tag, attribute and text run, except the
    header navigation subtree, the Drupal settings script's body and the version part of
    stylesheet and script URLs. Separately, require the quoted rights language to be
    present.

  A retrieval failure, an unverifiable baseline, an ambiguous build number, or a page
  without exactly one navigation region and one settings script fails closed. Every other
  document stays byte-strict. A classified mismatch never becomes a pin: only bytes whose
  digest is the pin are cached or used. `tools/inventory/harvest_federal.py --confirm`
  uses the same rule, and only the recovered pinned bytes.
- **Tests (section 5).** `tests/test_rights_drift.py` covers each required behaviour,
  positive and negative, on synthetic pages, plus the addendum's own checks and the
  harvest's use of the rule.
- **The networked run (section 6).** See the PR. Run locally on 2026-11-17, the check
  classified all 26 FIBF pages as verified presentation-only drift, and verified the GSA
  baseline from the archive. It **failed** the GSA website policies page on one difference
  the disposition did not identify: a script element added to the page
  (`/core/assets/vendor/ckeditor5/ckeditor5-dll/ckeditor5-dll.js`). As section 6
  directs, the tolerance was not widened. The difference is reported to the architect
  separately, and the issue is not closed while it fails.
