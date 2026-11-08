# Decision record — Stage 03 standard ratified with clarifications, G1-T review authorized, 2026-11-07

Recorded verbatim by Claude Code (`claude-opus-5-5`) on 2026-11-07, from the decision the
architect, Aaron Damiano, gave in session. The act is the architect's.

## What it is about

| Field | Value |
| --- | --- |
| Ratifies | `docs/proposals/2026-11-07-stage-03-taxonomy-standard.md` at `72401ef`, SHA-256 `11669836523a992c0b6cdc651c07b3352fe17887e7a5a12cc0ba34e591a84f64`, with the two clarifications below |
| Accepts | Tranche 2's reconciled taxonomy (`docs/catalog/tranche-2-review.yaml` at `72401ef`, SHA-256 `cf9d1409791d2bfda01c09fe0af816962fa1bc682bede1ef40e966426ff6a71c`), and `docs/catalog/admission/G1T-T2-batch.md` at `72401ef`, SHA-256 `e4a54ebff21e837120b9a335c6ed468b4571191b1b45d5418ff50e6d7bb2f9f2`, as prepared for G1-T review, not as passing it |
| Follows | `docs/decisions/2026-11-07-tranche-2-accepted-g1t-preparation-authorized.md`, whose truncated section C this direction supersedes; the missing text is not reconstructed |

## The decision

````text
Subject: Architectural Decision — Stage 03 Standard, Tranche 2, and G1-T Review
I have reviewed the Tranche 2 results at commit `72401ef`.
Decision: APPROVE THE STAGE 03 STANDARD WITH TWO CLARIFICATIONS; ACCEPT G1-T PREPARATION; AUTHORIZE THE NEXT REVIEW STEP.
A. Approved Now
1. Stage 03 Taxonomy Standard — RATIFIED WITH CLARIFICATIONS
I approve `2026-11-07-stage-03-taxonomy-standard.md`, subject to incorporating these two binding clarifications:

* A `kind-of` relationship requires genuine specialization of the capability disposition: every instance of the narrower capability type must also be an instance of the broader type. Shared terminology, bearer similarities and realization-index overlap alone do not establish subclasshood.
* A source hierarchy is supporting evidence for a proposed functional-component (`part-of`) relationship, not sufficient proof by itself. The relationship must also satisfy the conceptual coverage test.

These clarifications preserve the previously approved rules and introduce no new relationship kinds.
Record the ratification, publish the standard in its designated location, and apply its existing validation gate.
2. Tranche 2 Taxonomy — ACCEPT
Accept the reconciled link classifications and terminology baseline.
The 66 emitted SKOS broader relationships and 18 retained conceptual `kind-of` proposals remain distinct.
Do not generate OWL subclass axioms from either.
Keep the unresolved Internal Control and Global Trade Management root relationships held. Do not force a broader classification by changing their definitions.
3. Repository Integration — AUTHORIZED
Complete the approved standard clarifications and required checks.
Once CI passes on the final reviewed commit, PR #48 may be merged.
Merging does not admit the 43 candidate classes or authorize Stage 05 formalization.
B. G1-T — Independent Review Authorized, Admission Pending
The 43 dossiers are accepted as prepared for G1-T review, not as passing G1-T.
Use a separately instantiated synthetic ontology reviewer, operating in an ontologist capacity, independent of the drafting run. Record its actual identity, model, capacity and review date. This reviewer is distinct in function from the finance-domain practitioner who reviewed terminology.
The reviewer must assess every candidate against the five approved G1-T questions, using its definition, organizational grounding, realization evidence and taxonomy.
The eight explicitly open questions require individual dispositions.
For each candidate, record PASS, FAIL or PENDING REVIEW, with justification. PENDING REVIEW is not an admitted type and must not be confused with a completed G1-T failure.
A concept must not receive PASS merely because all cited BPO act IRIs exist or because the drafting script recommended PASS.
Consolidate the independent review into one batch admission recommendation for my architectural decision. Do not request 43 separate approvals.
Preserve the existing signed T1-02 and T1-03 records.
C. Q-12 — Separate Dependency Resolution
I accept the corrected Q-12 analysis.
The nine concepts with only capability-typed evidence remain blocked.
The four concepts whose available act types belong to their components also remain unready, unless a conceptually appropriate realization index is established.
Do not automatically retype BPO classes as Planned Acts. First determine whether the source class is actually misclassified or whether the BCO concept needs a different existing realization mapping.
Prepare one consolidated upstream BPO issue recommendation if necessary. Do not change BPO or invent replacement act classes without authorization.
The eight affected but unblocked concepts may proceed through G1-T review.
D. Development Priority and Boundaries
Continue applying the approved semantic-curation approach to the remaining candidate catalog. Avoid creating additional framework functionality or repeating a new architecture proposal for every domain.
The immediate objective is to turn reviewed concepts into properly admitted types and then, after the applicable Stage 05 authorization, executable ontology classes.
No OWL class generation, new object property or new formalization stage is authorized by this decision.
E. Next Deliverable
Return a consolidated G1-T review showing:

* PASS, FAIL and pending counts across all 43 candidates.
* Explicit resolutions of the eight open questions.
* Any material defects in definitions, grounding or realization indexes.
* A recommendation for a batch admission decision.
* Remaining Q-12 dependencies, without blocking unrelated candidates.

The next architectural review should concern actual type-admission decisions, not another general curation proposal.
The earlier decision record correctly noted that part of my previous message was truncated. Treat this complete direction as the controlling follow-up; do not reconstruct the missing text.
Final disposition: Stage 03 standard ratified with two clarifications; Tranche 2 taxonomy accepted subject to its validation gate; G1-T independent review authorized; formal admission and OWL implementation remain pending.
````

## The acts it contains

1. **The Stage 03 standard is ratified**, with two binding clarifications:
   - `kind-of` requires genuine specialization of the capability disposition: every
     instance of the narrower type is an instance of the broader. Shared terminology, bearer
     similarity and realization-index overlap alone do not establish it.
   - A source hierarchy supports a `part-of` relationship but does not prove it. The
     relationship must also meet the coverage test.

   No relationship kind is added. The ratification is recorded, the standard published in
   its designated place, and its validation gate applied.
2. **Tranche 2's taxonomy is accepted**: the 66 `skos:broader` links and the 18 retained
   `kind-of` proposals stay distinct; no subclass axiom is generated from either; the
   Internal Control and Global Trade Management root links stay unresolved, with no
   definition changed to place them.
3. **PR #48 may be merged** once CI passes on the final reviewed commit. Merging admits none
   of the 43 classes and authorizes no Stage 05 work.
4. **Independent G1-T review**, by a separately instantiated synthetic ontology reviewer in
   an ontologist capacity, independent of the drafting run, with its identity, model,
   capacity and date recorded:
   - every candidate assessed against the five G1-T questions, from its definition,
     grounding, realization evidence and taxonomy;
   - an individual disposition for each of the eight open questions;
   - PASS, FAIL or PENDING REVIEW for each, with justification. PENDING REVIEW is neither an
     admission nor a failure;
   - no PASS only because the cited IRIs exist or the draft recommended it;
   - one consolidated batch admission recommendation for the architect, not 43 approvals;
   - T1-02 and T1-03 preserved.
5. **Q-12.** The corrected analysis is accepted. The nine stay blocked; the four stay unready
   unless a conceptually appropriate index is established. No BPO class is retyped as a
   matter of course: first, whether the source class is misclassified, or whether the BCO
   concept needs a different existing mapping. One consolidated upstream issue
   recommendation, if needed. BPO is not changed, and no act class invented, without
   authorization. The eight affected but unblocked concepts proceed through G1-T review.
6. **Priority.** Semantic curation continues across the catalog without new framework or a
   new proposal per domain. No OWL class, object property or formalization stage is
   authorized.
7. **Next deliverable:** the consolidated G1-T review, with counts, the eight resolutions,
   material defects, a batch admission recommendation, and the remaining Q-12 dependencies.

## What it does not do

It admits no class, generates no OWL, and authorizes no Stage 05 work.
