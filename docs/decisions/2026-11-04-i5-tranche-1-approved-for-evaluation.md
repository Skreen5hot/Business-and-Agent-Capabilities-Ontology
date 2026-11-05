# Decision record — I-5 tranche 1 approved for evaluation, with conditions, 2026-11-04

Recorded verbatim by Claude Code (`claude-opus-5-5`) on 2026-11-04, from the decision the
architect, Aaron Damiano, gave in session. The acts are the architect's.

**What it is about:** the tranche 1 readiness record, `docs/catalog/tranche-1.md` at
`f320a67` (SHA-256 `c6b1185c514a6a7be47ff523590963cb1bdec97470feacc2e74ef9e4d10bf454`),
pull request #36, which reviewed `docs/catalog/candidates.yaml` at `9854052` (SHA-256
`4242de571a4b14309634bbab7c9513ae625d9214b82dcdf6c15e1fda3c6297d9`), and the three
questions that record put to the architect.

## The decision

````text
Decision: Approve the first I-5 review tranche, with conditions. Do not admit any candidates yet.

### 1. First tranche — APPROVED for evaluation

Proceed with all three candidates under the proposed conditions.

| Candidate                     | Decision             | Required action                                                                                           |
| ----------------------------- | -------------------- | --------------------------------------------------------------------------------------------------------- |
| Customer Complaint Management | Proceed              | Exclude the complaint-handling analysis act unless its role in exercising the capability is demonstrated. |
| Payroll Processing            | Proceed              | Resolve duplicate, validate component-derived realization evidence, exclude policy-setting acts.          |
| Accounts Payable Processing   | Hold for remediation | Remove invalid realization evidence and rebuild the index before admission evaluation.                    |

This authorizes the review tranche, not an ontology change or successful admission-test result.

### 2. Payroll realization index — APPROVED CONDITIONALLY

Use the three component candidates as the source of realization evidence, subject to these constraints:

- Every cited act must genuinely exercise Payroll Processing.
- Preserve traceability to its originating component.
- Do not assume an act realizes the parent capability merely because it realizes a component.
- Exclude policy-setting and summary acts unless their inclusion can be justified against the admission criteria.

Treat BRM Payroll (BCC-b7c46718) as a proposed synonym of Payroll Processing. Retire the duplicate only after confirming semantic equivalence.

### 3. Accounts Payable payment-approval act — REMOVE

Remove “Approve payments” from the ability realization index.

Approval and authorization acts establish or exercise standing; they do not, by themselves, demonstrate the operational ability under evaluation.

Also remove “Maintain e-commerce” from the Accounts Payable realization index.

Rebuild the index using appropriate operational acts already present in the source inventories. Do not relabel authorization acts to manufacture qualifying evidence.

Payments Approval (BCC-9ecf360b) should be rejected as an ability candidate, while preserving its source evidence for possible standing-related modeling.

### Execution authorization

Proceed with PR #36 under these decisions, stacked on PR #35.

The acceptance boundary remains:

- Admission test must be ratified before any candidate can pass.
- Every realization link must be justified and traceable.
- No new BFO/CCO object properties.
- No OWL admission before all required conditions are satisfied.
- Preserve the distinction between ready for evaluation and approved for ontology inclusion.

Next milestone: complete the three candidate readiness records, resolve the remaining evidence issues, and obtain admission-test ratification.

No additional candidate harvesting. No expansion of scope.
````

## The acts it contains

1. **Tranche 1 is approved for evaluation**, not for admission: T1-01 Customer Complaint
   Management and T1-02 Payroll Processing proceed; T1-03 Accounts Payable Processing is
   held for remediation. No candidate is admitted, and no G1-T result is given.
2. **T1-01:** the complaint-handling analysis act (`bpo:P19072`) is excluded unless its
   role in exercising the capability is demonstrated.
3. **T1-02:** the realization index is drawn from the three component candidates
   (BCC-85fbcb90, BCC-d105ff07, BCC-394909c1), act by act: each cited act must exercise
   Payroll Processing itself, keeps its originating component, and policy-setting and
   summary acts are excluded unless justified. BRM Payroll (BCC-b7c46718) is a proposed
   synonym, retired only after semantic equivalence is confirmed.
4. **T1-03:** "Approve payments" (`bpo:P10872`) and "Maintain/Manage electronic commerce"
   (`bpo:P10870`) are removed; the index is rebuilt from operational acts already in the
   inventories, without relabelling authorization acts.
5. **Payments Approval (BCC-9ecf360b) is rejected as an ability candidate.** Its source
   evidence is kept for possible standing-related modeling.
6. **PR #36 proceeds**, stacked on PR #35, inside the stated acceptance boundary.
7. **Excluded:** further candidate harvesting and any expansion of scope.

## How it was carried out

`docs/catalog/tranche-1.md`, revision 2, applies acts 2 to 5 and records each index
member's disposition and reason. The generated catalog is not edited: its review statuses
are the generator's, and the dispositions above are recorded in the tranche record, which
pins the catalog digest it reviewed.

## What it does not do

It admits, ratifies or mints nothing. G1-T is not ratified (D4), so no G1-T record can be
a PASS. It does not merge PR #35. CM-01, DP-1, DP-2 and the specification are unchanged.
