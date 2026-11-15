# Decision record — BPO inquiry approved; D5-1 to D5-7 approved; locator updates deferred, 2026-11-15

Recorded verbatim by Claude Code (`claude-opus-5-5`) on 2026-11-15, from the decision the
architect, Aaron Damiano, Product Owner and Ontology Architect, gave in session on PR #52
at commit `cd81767`. The acts are the architect's. This record makes none.

## What it is about

These records are on branch `catalog/tranche-2-followup-d5`, at
`cd817676e805d263aa2022e5630bc35a5570b59a` (PR #52):

| Record | SHA-256 at `cd81767` |
| --- | --- |
| `communications/bpo/outgoing/2026-11-15-q12-capability-typing-inquiry.md` (approved in A) | `02efa0050690d61a26bb98806405452722aa7aa08b1465849b9bb00dd3a02d37` |
| `docs/proposals/2026-11-15-stage-05-ontology-standard.md` (approved in D5-1) | `128a81493f904a4211ebf170dede317a9d227a784a1608b58c37871a5afac77c` |
| `docs/proposals/2026-11-15-d5-readiness-package.md` (D5-1 to D5-7) | `2743c27b21c13809000f26acdb209834cbb5d1b995f2b087f2a5a79e8c4f112f` |
| `docs/catalog/tranche-2-followup.md` (the held locator updates, C) | `e55e6f09f5638ce585a0c5d08eeda6d4935fc85a1701659848bb76a10ccb16a7` |
| `docs/decisions/2026-11-15-tranche-2-remaining-issues-and-d5-preparation.md` | `a25c6f4738b5ba0fe2aae30511c9657822c2cfebdc93e41646991aac1e1f6354` |

## The decision

````text
Subject: Architect Decision — PR #52, BPO Inquiry, D5 Readiness and Locator Updates
I have reviewed PR #52 at commit `cd81767` and its supporting documents.
Decision: APPROVE THE BPO INQUIRY AND D5-1 THROUGH D5-7, WITH THE INTERPRETATIONS AND CONDITIONS BELOW.
A. BPO Inquiry — APPROVED
I approve the text of:
`communications/bpo/outgoing/2026-11-15-q12-capability-typing-inquiry.md`
The inquiry correctly recognizes that BPO's classification of the 39 classes appears deliberate under ADR-001 R5/R6. We are requesting confirmation and clarification, not alleging an upstream modeling error.
You are authorized to send the inquiry through the established communications procedure. Post the board alert after the governing commit is on `main`, as repository rules require.
Do not change BPO classes or re-pin BPO in response to this decision. Any subsequent upstream changes require their own review.
The inquiry does not block formalization of independently admitted BCO types.
B. D5 Decisions — APPROVED
D5-1 — Stage 05 Standard: APPROVED
Approve the proposed Ontology Development Standard for Stage 05.
Publish it in the designated standards directory and preserve its approved version and digest.
D5-2 — Validation Architecture: APPROVED
Approve S05-T1, S05-C1 through S05-C9, S05-B, ELK and HermiT.
ELK must execute successfully once substantive OWL capability classes are submitted for acceptance. HermiT must execute at the required checkpoint. A skipped or unavailable reasoner is not a passing checkpoint result.
Each applicable validation rule must have appropriate positive and negative test evidence.
D5-3 — First Formalization Tranche: APPROVED
Approve the initial scope:

* `bco:BusinessCapability`.
* The 39 admitted capability types identified as ready in the D5 package.

The following remain excluded until their focused source checks are complete:

* T2-02 — Corporate Card Management.
* T2-24 — Cost Driver and Critical Activity Analysis.
* T2-31 — Customer Credit Management.

A source check finding no substantive defect permits the affected type to join a later authorized implementation tranche without reopening its G1-T admission.
Preserve all signed G1-T records and indexes.
D5-4 — Terminology Dependencies: APPROVED AS A FIRST-TRANCHE EXCEPTION
I explicitly approve a limited exception to the roadmap's T1/T2/T3 sequencing for this first formalization tranche.
Accept the 39 reviewed vocabulary concepts and the approved Business Capability parent definition as the terminology baseline for this tranche only.
This approval rests on their existing terminology review, semantic curation, taxonomy review, signed G1-T evidence and ratified CM-01/specification commitments.
It does not ratify the entire controlled vocabulary or declare T1, T2 and T3 globally complete.
Before implementation, verify that the `BusinessCapability` metamodel concept, its controlled-vocabulary definition, CM-01 and the ratified specification are semantically aligned. Record that verification as the parent-specific portion of terminology reconciliation.
The remaining Stage 01 standard, vocabulary acceptance and full terminology reconciliation remain outstanding for their applicable future gates. Do not use this exception as blanket authorization for other concepts.
Record the exception explicitly in the D5 decision and roadmap.
D5-5 — BPO Extract Expansion: APPROVED
Approve narrowly scoped expansion of the pinned BPO extract to include the 156 distinct indexed act classes, necessary genera and superclass chains, and the declaration of `bpo:enablesProcess`.
Reuse the existing vendoring mechanism wherever possible.
Include only the permitted declarations. Do not import excluded `requiresCapability` assertions, BPO capability classes or unrelated source modules.
Preserve source pins, provenance, licensing notices and reproducible extract validation.
D5-6 — CD12 Interpretation: APPROVED
For BCO-minted capability classes, the signed G1-T admission record is the authoritative source of the realization index.
The BPO `capability_scope.json` generator continues to govern its own BPO output; it is not authoritative for BCO-minted classes.
BCO may write the existing `bpo:enablesProcess` annotations from its signed admission records.
S05-T1 must enforce exact agreement with those records.
The annotation remains non-causal, non-modal and non-exhaustive. No `requiresCapability` assertions are authorized.
This is a scoped implementation clarification of ratified CD12, not a new object property or a revision to approved capability meaning.
D5-7 — Reasoning Dependencies: APPROVED
Approve introducing ELK and HermiT through a version-pinned ROBOT dependency.
Record and verify the dependency versions, checksums, source provenance and applicable licensing requirements.
Make reasoner execution part of the established validation workflow, with mandatory execution at the applicable acceptance checkpoints.
C. Held Source-Locator Updates — DECIDED
Defer the T2-02 and T2-31 locator updates until the corresponding types are prepared for formalization, after their focused source checks.
At that point, apply each locator correction as a separately traceable, nonsemantic vocabulary revision.
Preserve the signed admission baseline and record both old and new digests. The corrections must not silently change approved definitions, realization indexes or G1-T findings.
No additional architectural decision is needed for a provenance-only correction. Escalate if a source check reveals a substantive mismatch.
D. Repository Integration
You may record this decision, update the approved Stage 05 standard and D5 readiness status, and merge PR #52 after required CI passes on the final reviewed changes.
You may also perform the approved dependency and validation preparation using the existing tooling.
Before implementation, reconcile any inconsistency between the reported total of 42 signed types and the readiness document's reference to T1-01 as independently admitted. Do not modify an admission record merely to force the totals to agree.
E. Authorization Boundary
D5 is approved and its readiness gate is satisfied for the defined first tranche, subject to the explicit conditions above.
This decision does not, by itself, authorize writing OWL capability classes.
Stage 05 implementation under D6 requires a separate implementation authorization, using this approved tranche and standard. Do not create another broad readiness proposal; the D5 decision is complete.
No additional ontology object property, unsupported class, automatic taxonomy axiom or BPO reclassification is authorized.
Immediate Next Actions

1. Record the approvals and the tranche-specific sequencing exception.
2. Complete CI and integrate PR #52.
3. Send the approved BPO inquiry and post its alert under repository rules.
4. Publish the approved Stage 05 standard.
5. Prepare the narrowly scoped vendoring and reasoner configuration work.
6. Report any genuine D6 implementation blockers, without reopening D5.

Final disposition: BPO inquiry approved; D5-1 through D5-7 approved; T2-02/T2-31 locator updates deferred; D5 completed for the approved first tranche.
````

## Acts it contains

1. **The BPO inquiry is approved** (A), to be sent through the protocol. Its alert is
   posted once the commit that holds it is on `main`.
2. **D5-1 to D5-7 are approved** (B):
   - D5-1: the Stage 05 standard.
   - D5-2: the validation architecture. A skipped reasoner is not a passing checkpoint
     result.
   - D5-3: the first tranche, `bco:BusinessCapability` and 39 types, with T2-02, T2-24
     and T2-31 excluded until their source checks.
   - D5-4: a **first-tranche-only exception** to the roadmap's T1, T2 and T3 sequencing.
   - D5-5: the narrow BPO extract widening.
   - D5-6: CD12, read for BCO-minted classes.
   - D5-7: ELK and HermiT, through a version-pinned ROBOT.
3. **The T2-02 and T2-31 locator updates are deferred** (C) until each type is prepared
   for formalization. Each is then applied as a traceable, non-semantic revision.
4. **D5 is complete** for the first tranche (E). Writing OWL needs a separate D6
   implementation authorization.

## The terminology exception (D5-4)

It covers only `bcom:BusinessCapability` and the 39 concepts of D5-3 (listed in the
package, section 2). It ratifies no vocabulary concept, and it does not complete T1, T2
or T3. Those stay open for their later gates. The roadmap's D5 row records it.

## Verification required by D5-4: the parent's alignment

This is the parent-specific portion of terminology reconciliation, done before
implementation as the decision requires. It compares four sources:

- the metamodel concept `bcom:BusinessCapability` and its generated definition
  (`src/01_controlled_vocabulary/generated/bco-metamodel.ttl`);
- CM-01's entry "Business Capability" (`src/02_conceptual_models/CM-01-business-capability.md`,
  SHA-256 `292c8f36…1ccc`);
- the ratified specification's §4 row (`specifications/Business-Capability-Ontology-v0.5.0-draft.3.md`,
  `2224f869…c574`, accepted as ADR-002);
- ADR-002's parent-admission row.

| Point | Vocabulary (generated) | Ratified specification §4, v0.5.0-draft.3 | CM-01 | Aligned? |
|---|---|---|---|---|
| Label | Business Capability | Business Capability | Business Capability | yes |
| Genus and parents | Organization Capability that is a Disposition | `cco:ont00000568`, `obo:BFO_0000016`; admitted by ratification (CD3, R10-04; ADR-002) | under `cco:ont00000568`; disposition "only for a type that has passed type admission", the assertion "a Stage 05 matter" | yes, in effect. CM-01 predates the ratification of CD3, which admits the parent and leaves each specific type to G1-T |
| Bearer | inhering in an Organization | inhering in an Organization | borne by an Organization | yes |
| Basis | "constituent member agents of that organization in their organizational arrangement" | "the relevant member agent or agents of that organization as organized" | "the organization's own members as organized" | **no.** The vocabulary's plural "constituent member agents" does not carry CD2's one-member-suffices reading (CAP-35), which the specification and CM-01 state |
| Realization | "when realized, is realized in Planned Acts of the types in its realization index" | "realizable in Planned Acts the organization's members perform on its behalf" | "realized only by acts that are exercises of it", performed by its members (RL-14) | **no.** The vocabulary ties realization to the index and omits the performance condition. The ratified text states the performance condition (RL-14, CAP-34) |
| Does not imply | "enabling artifacts may be missing"; "artifacts it owns are its basis" | "enabling conditions may be missing"; "any artifact is its basis" | possession distinct from availability; never an artifact | **no**, in wording. The ratified text is broader |

**Finding.** The vocabulary's parent definition is the wording of specification
v0.4.0-draft.1, not of the ratified v0.5.0-draft.3. The cause is mechanical: the
vocabulary build takes a metamodel definition from the §4 row of the layout's
"specification in force" (`config/repository-layout.yaml`, component `spec.current`,
role `specification`), and that component is still `v0.4.0-draft.1`
(`c55fb36c…768f9f`). CM-01 and the ratified specification agree with each other. The
vocabulary differs from both, in the basis and realization clauses.

**Consequence.** Standard S2 takes the parent's label and definition from
`bcom:BusinessCapability`. Until that concept carries the ratified definition, the parent
cannot be written as standard S2 requires. This is a D6 implementation blocker, for the
parent only. The 39 specific concepts are not affected: each has its own signed
definition.

**Not done here.** The fix is the architect's choice. There are two options:

1. **Make v0.5.0-draft.3 the specification in force.** This regenerates all nine
   metamodel definitions from its rows, each as a `revises` record. It also changes the
   specification names the vendoring tool reads for seeds.
2. **Revise `bcom:BusinessCapability` alone.** The build ties a metamodel definition to
   the row of the specification in force, so this needs a change to that rule.

D5 is not reopened.

## Reconciling 42 with T1-01

G1-T has signed **43** types PASS:

- T1-01, T1-02 and T1-03 on 2026-11-05 (`docs/decisions/2026-11-05-g1t-tranche-1-signed.md`);
- the 40 of tranche 2 on 2026-11-14.

The "42" in the 2026-11-15 directions counts those that have a vocabulary concept. T1-01,
Customer Complaint Management, is signed PASS but has no catalog concept yet, so it has
nothing to formalize and is not in D5-3. Both figures are true, and they count different
things. No admission record is changed. Wherever a record says "42 admitted", it means
42 catalog concepts with a signed G1-T PASS.

## How it was carried out

- The standard is published, as approved, at `docs/standards/stage-05-ontology.md`. Only
  its status row is changed, and that row cites the approved text by its SHA-256 at
  `cd81767`. The proposal is kept as it was.
- The roadmap's D5 row, standards matrix and terminology lane record approval and the
  exception. HANDOFF says the same.
- The BPO inquiry's alert is posted after PR #52 merges, naming the commit that added the
  message.
- The vendoring and reasoner work is a separate change.

## What it does not do

- It writes no OWL and authorizes none. That needs D6.
- It ratifies no vocabulary concept, and changes no definition, index, link or G1-T
  record.
- It sends nothing to BPO's repository, and does not re-pin BPO.
