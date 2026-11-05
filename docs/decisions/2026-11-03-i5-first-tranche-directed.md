# Decision record — I-5 directed: the first tranche, three candidates for review, 2026-11-03

Recorded verbatim by Claude Code (`claude-opus-5-5`) on 2026-11-03, from the direction the
product owner and architect, Aaron Damiano, gave in session. The acts are the architect's.

**What it is about:** the Candidate Capability Catalog of Phase I-4 (pull request #35),
`docs/catalog/candidates.yaml` at `4625d0c` (the catalog the direction read), and Phase I-5
of the Capability Term Inventory: a recommendation of a first catalog tranche for the
architect's separate approval (roadmap T7; scope approval of 2026-10-27). The catalog
after the correction this direction asks for is `docs/catalog/candidates.yaml` at
`9854052` (SHA-256 `4242de571a4b14309634bbab7c9513ae625d9214b82dcdf6c15e1fda3c6297d9`).

## The direction

````text
Agreed. Execution over exploration. No side quests.

The Candidate Capability Catalog is already built. We have 1,046 candidates, including 526 classified as likely BFO/CCO-compatible. Those classifications remain provisional.

The immediate priority is I-5: identify the first tranche of capabilities for approval, not build another interface or repeat the synthesis.

We'll preserve the existing work, focus on evidence-backed candidates, enforce BFO/CCO compliance, and keep candidate approval separate from ontology implementation.
First three candidates for I-5 review
Candidate	Evidence	Preliminary assessment
BCC-373b146e Customer Complaint Management	BPO + APQC; 5 supporting act types	Strong candidate; no automated flags  GitHub
BCC-d95f68fd Payroll Processing	2 APQC records; financial transaction and administration acts	Strong candidate; review overlap with the separate Payroll candidate  GitHub
BCC-62e789bf Accounts Payable Processing	APQC; multiple supporting act types	Strong candidate; no automated flags  GitHub

These are recommendations for formal review, not approvals. Each still needs a checked definition, disposition interpretation, and realization evidence before admission.

I also identified one concrete quality problem: Procurement Capability (BCC-cc2de1a5) has a circular draft differentia, describing procurement as the ability to obtain procurement, despite having no automated flags. It should not be included without correction. 

GitHub

Immediate execution path: close PR #35 after required checks and review, then process the I-5 approval tranche against the existing catalog. No additional harvesting, UI development, or unrelated governance work.
````

## The acts it contains

1. **I-5 is authorized** and is the immediate priority: identify the first tranche for
   approval, against the existing catalog.
2. **Three candidates are put forward for formal review**: BCC-373b146e, BCC-d95f68fd,
   BCC-62e789bf. They are recommendations, not approvals; each needs a checked definition,
   a disposition interpretation and realization evidence before admission.
3. **Procurement Capability (BCC-cc2de1a5) is excluded** until its differentia is
   corrected.
4. **PR #35 is to be closed** after its required checks and review.
5. **Excluded work:** further harvesting, user-interface development, unrelated governance.

## How it was carried out

- The Procurement defect was a generator defect, not a single record: 25 candidates had a
  circular differentia. Commit `9854052` (on PR #35) flags them and keeps them out of
  generated-draft status. The same commit flags deontic index members (G1-T question 4),
  which the review of the three candidates found in Accounts Payable Processing.
- The tranche readiness record is `docs/catalog/tranche-1.md`.

## What it does not do

It admits, ratifies or mints nothing, and approves no candidate. G1-T is not ratified
(D4), so no G1-T record can be a PASS yet. CM-01, DP-1, DP-2 and the specification are
unchanged.
