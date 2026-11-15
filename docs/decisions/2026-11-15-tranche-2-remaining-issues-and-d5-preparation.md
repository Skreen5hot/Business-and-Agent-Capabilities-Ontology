# Decision record — PR #51 accepted; Q-12 dispositions, the BPO inquiry, the wording notes, `P14057` and D5 preparation, 2026-11-15

Recorded verbatim by Claude Code (`claude-opus-5-5`) on 2026-11-15, from the direction the
architect, Aaron Damiano, Product Owner and Ontology Architect, gave in session after
reviewing merged PR #51. The acts are the architect's. This record makes none.

## What it is about

The records on `main` at `e41eb072b32f8ce726ded8d71d16c17f400f4764` (PR #51 merged):

| Record | SHA-256 at `e41eb07` |
| --- | --- |
| `docs/catalog/admission/G1T-T2-signature.md` (the signed consolidated record) | `18b0e1569beb18c5b88643b54be3d8b431506da8d44566426d3962384b4d9f1e` |
| `docs/catalog/admission/G1T-T2-batch.md` (revision 5, the signed baseline) | `b44ec9ea2af76a9cbf48fcb125a94b93c88076475603532bf23fc32106bd90ef` |
| `docs/decisions/2026-11-14-g1t-tranche-2-signed.md` | `ebc549d5fe8a94bd611bdd5e9bbcbd5da960b96315102503b7bda06c5b9e6369` |
| `docs/catalog/tranche-2-q12.md` (the 13 blocked concepts, section B) | `42ec348384e0a46521e3e85b86aac712ef1f3b00903808d3e2af096dfa0f3600` |
| `docs/proposals/2026-11-07-bpo-q12-issue-recommendation.md` (the proposed BPO issue, section C) | `c235b4381e6fc4db731c0e3e7c3e7631cd56f9a1eaf00977c570969e27a96a14` |
| `docs/catalog/admission/G1T-T2-supplementary-review.md` (the wording notes, section D) | `1430f89ba10d29044ba10e5d21388798959bb21852c50391b9dc6f4d9a42b648` |
| `docs/catalog/tranche-2-review.yaml` (the ledger) | `0fe81c123c78fce23d7aba453a5158eba8f9a45a7ca4d85065970c35b076b4cc` |

## The direction

````text
Subject: Architect Direction — PR #51 Accepted and Remaining Tranche 2 Issues
I have reviewed merged PR #51 and the remaining Tranche 2 issues.
Decision: ACCEPT PR #51 AS COMPLETE. PRESERVE ALL 42 SIGNED G1-T ADMISSIONS. RESOLVE THE REMAINING ISSUES AS DIRECTED BELOW.
A. PR #51 — CLOSED
The 40 Tranche 2 G1-T admissions have been signed and recorded. Together with the two previously admitted Tranche 1 types, this establishes 42 admitted capability types.
No additional G1-T approval is required for these 42 unless a subsequent substantive change affects an approved type's meaning or admission evidence.
Do not reopen the signed batch to resolve unrelated source-mapping issues.
B. Q-12 — Decisions on the 13 Blocked Candidates
1. Treat the following as capability areas for now:

* Financial Planning and Management Accounting.
* Internal Control.
* Tax Management.

Retain their terminology, provenance and component relationships.
They are not G1-T failures. A distinct whole-function capability type may be proposed later only with its own justification and admission record.
2. Keep the eight remaining leaf-process-dependent concepts blocked.
Do not use BPO classes typed under CCO Organization Capability as realization-index act types.
Do not automatically retype BPO classes or invent replacement act genera.
3. Treasury Management
Preserve its current definition and outstanding R26 review.
Do not substitute the union of its components' acts for a justified realization index of its own.
4. Default Account Management
Do not admit this broad type based solely on `bpo:P14007`, Perform recovery workout.
Retain that act as relevant evidence, but require a defensible match to the claimed capability's meaning before reconsidering G1-T admission.
C. Upstream BPO Communication — AUTHORIZED
Prepare and send one consolidated technical inquiry to BPO through the established communications protocol.
Ask:

1. Whether the 39 `bpo:P...` classes currently classified under Organization Capability are intentionally modeled as capabilities or are intended to be process/act types.
2. Where they are intended as act types, which existing BPO act genus applies to each, according to BPO's maintainers.
3. Whether act-type declarations are intended for PCF elements 10735, 10736 and 14008.

Provide the exact pinned BPO identifiers, source modules and evidence.
Do not demand blanket retyping, propose invented replacements or modify BPO without a separately reviewed upstream decision.
This communication must not block development of the 42 already admitted BCO capability types.
D. Supplementary Review Wording Notes — DISPOSITIONED
Accept the remaining nonblocking wording notes as implementation and evidence-quality follow-up.
Correct editorial explanations, inaccurate exclusion descriptions and outdated references where the changes do not alter signed definitions, realization indexes or admission findings.
For notes exposing a possible mismatch between a BPO act's source meaning and an admitted capability's definition, require a focused source check before formalizing that affected type.
Do not initiate a new broad G1-T review.
If an actual substantive defect is found, isolate the affected type and return only that change for architectural review.
Preserve every signed admission baseline.
E. `bpo:P14057` — PROFIT CENTRE ACCOUNTING
Retain the existing exclusion of `bpo:P14057` from T2-23 Cost Accounting.
Do not insert it into T2-25 Financial Performance Analysis merely to eliminate an unmapped act.
Record `P14057` as source evidence for a potential distinct Profit Centre Accounting capability concept.
During the next relevant semantic-curation batch, compare its meaning and specialization with Cost Accounting and Financial Performance Analysis.
Apply the normal terminology, taxonomy and G1-T processes if a distinct capability type is justified.
No new OWL class or object property is authorized by this decision.
F. Stage 05 — D5 Readiness Preparation AUTHORIZED
I authorize preparation of the D5 formalization-readiness package for the already admitted and eligible Business Capability types.
The package must establish:

* The proposed Stage 05 standard.
* The validation architecture and required executable checks.
* The reviewed terminology, definitions and taxonomy for the proposed first formalization tranche.
* The signed G1-T records and exact source baselines.
* Verified BFO/CCO parent and relation reuse.
* The permitted BPO import boundary and handling of Q-12, Q-13 and Q-14.
* A clear list of genuinely blocking versus deferred dependencies.

The unresolved Q-12 candidates must be isolated from the proposed first tranche unless subsequently admitted. Explain how the remaining BPO integration concerns are addressed for the actual classes proposed for formalization.
Do not turn the 13 blocked candidates into a blanket obstacle to unrelated admitted types.
D5 preparation does not authorize Stage 05 implementation. Return the readiness package for my approval before generating OWL capability classes.
G. Immediate Priorities
Proceed with these actions:

1. Close PR #51 administratively, without reopening the signed G1-T batch.
2. Record the Q-12 dispositions and send the consolidated BPO technical inquiry.
3. Preserve and triage the supplementary wording notes without another general review cycle.
4. Queue `P14057` for subsequent semantic curation.
5. Prepare the D5 readiness package for architectural approval.

Do not build additional generator infrastructure or create another broad governance workstream.
Final direction: The 42 G1-T admissions stand. Resolve the remaining dependencies selectively and move directly toward D5 authorization and formal ontology construction.
````

## Acts it contains

1. **PR #51 is accepted as complete** (A). The 42 G1-T admissions stand: tranche 1's
   Payroll Processing and Accounts Payable Processing, and tranche 2's 40. They need no
   further G1-T approval unless a later substantive change affects a type's meaning or its
   admission evidence. The signed batch is not reopened for source-mapping issues.
2. **Q-12 dispositions** (B):
   - Financial Planning and Management Accounting, Internal Control and Tax Management
     are capability areas for now. This is not a G1-T failure. Their terminology,
     provenance and component links are kept.
   - The eight leaf-process-dependent concepts stay blocked.
   - Treasury Management keeps its definition and its R26 review.
   - Default Account Management is not admitted on `bpo:P14007` alone.
3. **The BPO inquiry is authorized** (C): one consolidated message, through the protocol,
   asking the three questions named. It demands no retyping and proposes no replacement.
4. **The supplementary review's wording notes are dispositioned** (D). Editorial
   corrections may be made where they alter no signed definition, index or finding. A
   possible mismatch between a source and an admitted definition needs a focused source
   check before that type is formalized.
5. **`P14057` is queued** (E) for the next relevant semantic-curation batch, as evidence
   for a possible Profit Centre Accounting concept. It stays excluded from Cost Accounting
   and is not added to Financial Performance Analysis.
6. **D5 preparation is authorized** (F): a readiness package for the architect's approval.
   It does not authorize Stage 05 implementation or OWL capability classes.

## How it was carried out

- **A.** Nothing in the signed batch, the signature record or the vocabulary changes. Both
  signed records keep the SHA-256 above.
- **B.** `docs/catalog/tranche-2-q12.md` records the dispositions (section 5).
  `docs/catalog/tranche-2-review.yaml` changes for five rows:
  - the three capability areas read `not proposed: a capability area`;
  - Treasury Management's and Default Account Management's rows cite this record.
  
  The vocabulary concepts are unchanged.
- **C.** The inquiry is drafted at `communications/bpo/outgoing/2026-11-15-q12-capability-typing-inquiry.md`.
  Under `communications/README.md`, local rule 4, it is sent when the architect approves its
  text, and its alert is posted only after the commit that holds it reaches `main`.
  Drafting it showed that each of the 39 classes carries an `rdfs:comment` applying BPO's
  ADR-001 rule R5, and that five were re-modeled from acts to capabilities at BPO's Gate F.
  So the inquiry asks BPO to confirm their intent. It does not
  assume that the classes are misclassified, which the proposal of 2026-11-07 had assumed.
- **D and E.** `docs/catalog/tranche-2-followup.md` triages each note and records `P14057`.
  Each correction is entered there, as an erratum against the signed batch, which keeps
  its bytes.
- **F.** The package is `docs/proposals/2026-11-15-d5-readiness-package.md`, with the
  proposed standard `docs/proposals/2026-11-15-stage-05-ontology-standard.md`.

## What it does not do

- It admits nothing, and fails nothing.
- It writes no OWL, mints no IRI, and authorizes no OWL class or object property.
- It does not ratify any vocabulary concept, and changes no definition, IRI, index or link.
