# Decision record — G1-T tranche 2 batch decided, 2026-11-14

Recorded verbatim by Claude Code (`claude-opus-5-5`) on 2026-11-14, from the decision the
architect, Aaron Damiano, gave in session. The act is the architect's. It signs nothing:
the signature it calls for is the named reviewer's own, recorded against the finalized
records.

## What it is about

PR #49, as pushed at `c5b97f2`:

| Record | SHA-256 at `c5b97f2` |
| --- | --- |
| `docs/catalog/admission/G1T-T2-recommendation.md` | `8ceb274865308a33a6685aae84a91815d8bea964514b72fc30f1622fcb06100b` |
| `docs/catalog/admission/G1T-T2-batch.md` (revision 2) | `86eb55fddf46b430b7f003e7579f1f9c82959b71014dcc50c94396473056ecf5` |
| `docs/catalog/admission/G1T-T2-review-2026-11-07.md` (the independent review, as received) | `7c7efb831cf6a5276fe6e173cea34f4a3f40af7f4d5adae3e8e881c175671e08` |

It follows `docs/decisions/2026-11-07-stage-03-ratified-g1t-review-authorized.md`, B.

## The decision

````text
Subject: Architect Decision — PR #49, Tranche 2 G1-T Batch Admission
I have reviewed the consolidated G1-T recommendation for the 43 Tranche 2 candidate classes.
Decision: APPROVE BATCH A AND BATCH B, WITHDRAW THE THREE CAPABILITY AREAS, AND AUTHORIZE SPECIFIC CORRECTIONS TO THE SEVEN REMAINING CANDIDATES.
I am resolving all five requested decisions and the two embedded policy choices in one act.
1. Batch A — 17 Classes APPROVED
I approve all 17 Batch A candidates for G1-T admission upon completion of the required reviewer signature.
Use the corrected revision-2 records. No further conceptual or definition revisions are required for these 17 unless verification reveals a substantive defect.
2. Batch B — 16 Classes APPROVED WITH DEFINITION CORRECTIONS
I approve all 16 MD-7 definition corrections as proposed in their individual admission records.
Apply the corrections to the controlled vocabulary and G1-T records, preserving revision history, provenance and accepted conceptual distinctions.
The corrections must remove unsupported clauses, eliminate unjustified success conditions, and align each definition with the realization evidence.
Once the corrected definitions are verified against the applicable admission criteria, the 16 candidates are approved for G1-T admission upon signature.
Policy-formulation decision: APPROVED.
For Accounting Policy Management (T2-07) and Treasury Policy Management (T2-42), formulating, drafting, reviewing and communicating policies may be treated as non-deontic activities where the actual indexed acts support that interpretation.
Adopting, authorizing or conferring standing through a policy is distinct and remains outside those indexes.
Use "formulate" rather than "set" where this distinction is necessary. Do not equate policy formulation with authoritative adoption.
3. Withdraw Three Capability Areas — APPROVED
Withdraw the following from the G1-T admission batch:

* T2-06 — Financial Accounting.
* T2-27 — Revenue and Receivables Management.
* T2-37 — Financial Risk Management.

Retain them as capability areas or conceptual groupings in the terminology and taxonomy where justified.
They are not G1-T failures. Their constituent capability types remain independently eligible for admission.
Do not generate OWL capability classes from these three area records.
4. Seven Pending Candidates — Decisions
I authorize the following corrections and one consolidated supplementary G1-T review.
T2-02 — Corporate Card Management
Remove "set their terms" and other claims of granting cardholder standing. Exclude summary act `bpo:P20929`.
Retain only the organizational ability supported by the remaining non-deontic card-administration, reconciliation and settlement activities.
T2-31 — Customer Credit Management
Revise the definition to focus on evaluating credit requests, analyzing relevant credit evidence, reviewing accounts and monitoring credit activity.
Exclude summary act `bpo:P10742` and move `bpo:P14188` out of the index under Q5. Do not include granting, changing or withdrawing customer credit standing.
T2-04 — Capital Planning
Rename the proposed capability type Capital Investment Appraisal.
Narrow its definition to the organizational ability to prepare and evaluate the financial justification for proposed capital investments.
Retain `bpo:P10847` as its realization-index evidence. A single justified act type is sufficient; no invented act type is necessary.
Preserve the broader Capital Planning concept as a functional grouping or future candidate if justified. Do not treat the narrowed appraisal type as equivalent to the original broad concept.
T2-17 — Internal Control Design
Narrow and rename the candidate Control Environment and Risk Objective Formulation.
The revised definition must reflect the retained acts concerning codes of ethics, business process objectives, risks and risk tolerances.
Exclude `bpo:P10762`. Do not imply that these acts establish the organization's entire internal control design.
T2-43 — Internal Control Operation and Monitoring
Narrow and rename the candidate Internal Control Effectiveness Monitoring.
Limit its definition to monitoring whether organizational controls operate as intended and satisfy applicable assessment criteria.
Exclude `bpo:P21574`. Do not claim that the remaining monitoring act also establishes the broader ability to operate every control.
T2-24 — Cost Management
Narrow and rename the candidate Cost Driver and Critical Activity Analysis.
Use the three retained acts concerning identification and measurement of cost drivers and identification of critical activities.
Retain Cost Management as a broader functional grouping. Do not infer the ability to plan, control or reduce spending from analysis alone.
T2-25 — Financial Performance Management
Narrow and rename the candidate Financial Performance Analysis.
Remove "and act on the results" from its definition.
Exclude `bpo:P10785` from its realization index under CD5, because product-mix optimization is not itself the exercise of financial performance analysis.
Review the remaining acts against the narrower definition, retaining only those that genuinely concern financial appraisal, analysis or monitoring.
For all seven: Preserve source provenance, prior definitions, stable candidate identifiers and revision history. Reconcile the grounding statements, taxonomy links and realization indexes with the revised meanings.
These seven remain PENDING REVIEW until their corrected records pass one targeted supplementary G1-T review. Do not automatically admit them.
5. Summary-Act Rule — DECIDED
Retain the strict summary-act exclusion applied in revision 2.
All 25 identified designating summary acts remain excluded from the current indexes, consistent with Tranche 1's signed precedent.
Do not restore summary acts merely because all their child acts are retained. Any future exception requires a specific semantic justification, not a general change to this batch.
6. Signing Reviewer — DESIGNATED
Designate Aaron Damiano, Product Owner and Ontology Architect, as the G1-T signing reviewer, consistent with Tranche 1.
The separate Claude ontology review remains independent analytical evidence, not the admission signature.
Prepare a single consolidated signature record referencing each approved candidate and its final reviewed definition, realization index, G1-T findings and artifact digest.
The developer must not sign or record a completed signature on my behalf.
The 17 Batch A candidates and 16 corrected Batch B candidates become formally admitted only when the required signature is recorded against their finalized records.
7. Implementation and Integration
You are authorized to:

1. Record this architectural decision.
2. Apply the 16 approved vocabulary corrections.
3. Withdraw the three capability areas from G1-T consideration.
4. Apply the seven specified candidate corrections.
5. Run one targeted supplementary review of the seven.
6. Prepare the consolidated signature record for the eligible 33 candidates.
7. Update the affected evidence, terminology, taxonomy and status records.
8. Update PR #49 and merge the faithful, validated review and correction artifacts after required CI passes.

Do not mark unsigned candidate records as admitted merely because the PR has merged.
Do not begin another broad G1-T review of the same 43 candidates. Escalate only substantive defects or unresolved conflicts discovered during the targeted checks.
8. Work Remaining Separate
The 13 Q-12-dependent candidates remain outside this batch.
Do not retype upstream BPO classes or invent substitute act types. Their dependency resolution remains a separate matter.
No new BFO/CCO object properties, OWL classes, subclass axioms or other formal ontology assertions are authorized by this decision.
Stage 05 formalization still requires the applicable D5 authorization.
Final Direction
Proceed immediately with the approved definition corrections, the three withdrawals and the seven targeted revisions.
Prepare the eligible 33 candidates for one consolidated G1-T signature and complete one supplementary review of the remaining seven.
Do not return with the same architectural choices. They have been answered.
Our priority is to move the corrected and genuinely admissible capability types toward formal ontology implementation while continuing semantic curation across the remaining source material.
````

## The acts it contains

1. **Batch A (17)** is approved for G1-T admission on the named reviewer's signature of the
   revision-2 records, with no further revision unless verification finds a substantive
   defect.
2. **Batch B (16)**: the MD-7 definition corrections are approved as proposed, to be applied
   to the vocabulary and the records with their history and provenance kept; once checked
   against the admission criteria, the 16 are approved for admission on signature.
3. **The Formulation reading** of G1-T question 4 is approved for T2-07 and T2-42:
   formulating, drafting, reviewing and communicating a policy is non-deontic where the
   indexed acts support it; adopting, authorizing or conferring standing through one is
   distinct and stays outside the index.
4. **T2-06, T2-27 and T2-37 are withdrawn** from G1-T as capability areas. They are not
   failures; no OWL class is generated from them.
5. **The seven** are corrected as specified, five of them narrowed and renamed, and stay
   PENDING REVIEW until one targeted supplementary G1-T review of the corrected records.
6. **The strict summary-act rule** of revision 2 stands; an exception needs a specific
   semantic justification.
7. **Aaron Damiano is the signing reviewer.** A single consolidated signature record is
   prepared for the 33. Nobody else signs or records a signature for him.
8. **PR #49** may be updated and merged once required CI passes. Merging admits nothing.

## What it does not do

It admits no class: admission is the signature recorded against the finalized records. It
does not touch the 13 Q-12-dependent candidates, retype any BPO class or invent an act type,
and authorizes no OWL class, object property, subclass axiom or Stage 05 work (D5).
