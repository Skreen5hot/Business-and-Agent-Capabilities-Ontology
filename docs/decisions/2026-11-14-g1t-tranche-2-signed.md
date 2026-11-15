# Decision record — G1-T tranche 2 signed: 40 classes PASS, 2026-11-14

Recorded verbatim by Claude Code (`claude-opus-5-5`) on 2026-11-14, from the signature the
named signing reviewer, Aaron Damiano, Product Owner and Ontology Architect, gave in session.
The finding and the signature are his. It names the record it signs, the version by SHA-256
and the finding for every class, as the provenance correction of 2026-11-05
(`docs/decisions/2026-11-05-g1t-approval-provenance-corrected.md`) requires of an approval.

## What it is about

The signed baseline, on `main` at `a929749` (PR #50 merged):

| Record | SHA-256 at `a929749` |
| --- | --- |
| `docs/catalog/admission/G1T-T2-batch.md` (revision 5; the digest the signature names) | `b44ec9ea2af76a9cbf48fcb125a94b93c88076475603532bf23fc32106bd90ef` |
| `docs/catalog/admission/G1T-T2-signature.md` (the consolidated record, as prepared, signature block empty) | `6cfca8eeef7b49d10d4bf8b640fdaefbc6305c19869c472e69229e712695403d` |

It follows `docs/decisions/2026-11-14-g1t-tranche-2-batch-decided.md`,
`docs/decisions/2026-11-14-g1t-tranche-2-t2-25-and-the-six.md` and
`docs/decisions/2026-11-14-g1t-tranche-2-t2-25-final.md`.

## The signature

````text
Subject: Architect Signature — G1-T Tranche 2, 40 Business Capability Types
Decision: G1-T PASS — ALL 40 CLASSES APPROVED AND SIGNED.
Acting in my capacity as Product Owner and Ontology Architect, I approve and sign the consolidated G1-T Tranche 2 admission record:
`docs/catalog/admission/G1T-T2-signature.md`
This approval applies to the 40 candidate classes and their finalized definitions, grounding rationales, realization indexes, exclusions and admission findings, as identified in `G1T-T2-batch.md`, revision 5, SHA-256:
`b44ec9ea2af76a9cbf48fcb125a94b93c88076475603532bf23fc32106bd90ef`
Confirmation 1 — T2-17
APPROVED — PASS.
I explicitly extend the previously approved Formulation reading of G1-T question 4 to T2-17, Control Environment and Risk Objective Formulation.
Formulating and communicating codes, objectives, risk descriptions and tolerances is distinguishable from authoritatively adopting them or assigning standing.
Retain the three approved realization-index members. No change to the approved definition is required.
Confirmation 2 — T2-25
APPROVED — PASS.
Retain `bpo:P10787` in the Financial Performance Analysis realization index.
I accept the source-supported interpretation that the act evaluates performance using activity-based measures, rather than establishing the authoritative measures governing that evaluation.
Retain the four-member index established in revision 5. The exclusions of `P10786`, `P10785` and summary act `P10741` remain binding.
Consolidated G1-T Signature
I confirm PASS for all 40 capability types enumerated in the consolidated signature record, including:

* 17 Batch A types.
* 16 Batch B types with approved definition corrections.
* Six types accepted following supplementary review.
* T2-25, Financial Performance Analysis, as finally corrected.

This is my explicit architectural G1-T admission signature for those 40 types. It does not extend to withdrawn capability areas, unresolved concepts or Q-12-blocked candidates.
Recording and Implementation
Please record this signature verbatim in the consolidated signature record and the corresponding decision record, citing the exact SHA-256 digest of the signed baseline.
Verify that no definitions, concept identifiers or realization indexes have changed from the reviewed baseline.
You may commit and integrate the signature and resulting administrative status updates after the required repository checks.
G1-T admission is not G1-I attribution. This signature establishes admissibility of the 40 capability types, not that any particular organization possesses them.
No OWL generation or Stage 05 formalization is authorized by this signature.
Final decision: All 40 Tranche 2 capability types are admitted under G1-T. Proceed with recording the signature and preparation for the next authorized ontology-development stage.
````

## Verification before recording

As the signature directs, before anything was recorded:

- `G1T-T2-batch.md` on `main` has the SHA-256 the signature names. It is kept byte for byte
  as the signed baseline: its own status lines ("Decided; not signed") and empty
  confirmation rows are not edited, and this record and the signature record carry the
  signature.
- For each of the 40 classes in the signature record, the candidate, the concept IRI, the
  definition, the realization index and the vocabulary record digest (`tools/vocab/build.py`)
  were checked against the batch record and the vocabulary as built: none differs. T2-17
  keeps its three members; T2-25 keeps `P10782`, `P10783`, `P10784` and `P10787`, with
  `P10786`, `P10785` and `P10741` excluded.

## Acts it contains

1. **G1-T PASS for the 40 classes** of the signature record: 17 of Batch A, 16 of Batch B,
   the six accepted after the supplementary review, and T2-25. They are admitted under G1-T.
2. **T2-17:** the Formulation reading of question 4 is extended to it; its three members and
   its definition stand.
3. **T2-25:** `P10787` stays in the index, on the reading that it evaluates performance by
   activity-based measures and does not establish them; the four-member index and the three
   exclusions are binding.

## How it was carried out

- `G1T-T2-signature.md` holds the signature verbatim (section 3), its status reads signed,
  and its signature table holds the finding, the classes, the reviewer and the date. Nothing
  else in it changed.
- The 40 rows of `docs/catalog/tranche-2-review.yaml` read admitted; `docs/catalog/tranche-2.md`,
  HANDOFF and ROADMAP state the figures.

## What it does not do

- It does not extend to the three withdrawn capability areas, the unresolved concepts, the
  functional groupings or the Q-12-blocked candidates.
- It is not G1-I: it licenses no organization's claim to bear any of these capabilities.
- It authorizes no OWL generation and no Stage 05 formalization. A PASS licenses asserting
  each class under `obo:BFO_0000016`, and so under `bco:BusinessCapability` (CAP-04), once
  that is authorized; nothing is asserted now.
- It changes no definition, IRI, index or link, and does not ratify any vocabulary concept:
  the vocabulary's concepts stay Draft.
