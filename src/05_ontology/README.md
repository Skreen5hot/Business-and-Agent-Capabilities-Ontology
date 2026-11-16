# Stage 05 — Ontology

**Status:** first tranche implemented under D6
(`docs/decisions/2026-11-15-v05-transition-approved-d6-authorized.md`, E), and the
description tranche under B-1 (`docs/decisions/2026-11-15-b1-b4-approved-cap34-confirmed.md`),
against the
Stage 05 standard (`docs/standards/stage-05-ontology.md`) and specification
v0.5.0-draft.3. Not released, and not a claim of conformance with BFO, CCO or BPO as
published: the reasoners see the vendored extracts, which drop every anonymous class
expression. The tranche is not complete until CP-1 and CP-2, the conceptual-fidelity trace
and a stage-completion record are met (standard, section 7).

| Path | Holds |
|---|---|
| `apqc-cap.ttl` | `bco:BusinessCapability` and the first tranche's 39 specific capability classes, each with its signed realization index. Written by `tools/ontology/formalize.py --write`; never edit it |
| `tranche-1.yaml` | The tranche record the module is written from: each class's signed G1-T record (path, commit, SHA-256), concept digest and index, and the three types held back |
| `apqc-cap-desc.ttl` | The description layer (B-1): seven description-layer classes, `bco:AuthorizationRecord`, `bco:FunctionalAdequacyAssessment`, and the annotation properties `bco:concernsType` and `bco:assessedPresence`. Written by `formalize.py --write` from `tranche-2-description.yaml`; never edit it |
| `tranche-2-description.yaml` | The description tranche's record: each information class with its concept, digest and one CCO parent, and the two annotation properties. Readiness record: `docs/proposals/2026-11-15-stage05-description-tranche-readiness.md` |
| `fidelity-trace-tranche-1.md` | The first tranche's conceptual-fidelity trace |

## What the first tranche is

- **The parent:** `bco:BusinessCapability`, under `cco:ont00000568` and `obo:BFO_0000016`,
  with the ratified definition of `bcom:BusinessCapability`. It was admitted by
  ratification (CD3), not by G1-T.
- **39 specific classes**, each:
  - directly and only under the parent;
  - labelled and defined as its vocabulary concept;
  - carrying one `ex:enablesProcess` per member of its signed G1-T index.
- **Index:** 160 members, over 147 distinct BPO act classes.
- **Held back:** T2-02, T2-24 and T2-31, until their source checks
  (`docs/catalog/tranche-2-followup.md`, section 3). T1-01 has no catalog concept.
- **Nothing else is written:** no object property, no restriction, no equivalence, no
  disjointness, no individual, and no subclass link between capability classes.

## Checks

| Id | Where | Result at this commit |
|---|---|---|
| S05-T1 | `formalize.py`; `tests/test_formalization.py` | 40 classes, 160 members verified against the signed bytes |
| S05-C1, C2, C3, C5, C6, C7 | `shapes/stage05_shapes.ttl` (11 constraints, each with its fixture case) | the module conforms; every constraint fires on its own case |
| S05-C1 (module), C3 (declaration), C4, C8, C9 | `tests/test_formalization.py` | pass, each with a falsification |
| S05-B | `vendor_upstream.py` | every IRI the module names is described in an extract |
| S05-D (ELK), S05-D2 (HermiT) | `tools/ontology/reason.py` | see below |

**S05-D and S05-D2.** ELK 0.6.0 and HermiT 1.4.5.456, through ROBOT 1.9.11
(`config/reasoner-pins.yaml`), run over the two modules and the three extracts.
- Both reasoners classify the input, with no unsatisfiable class.
- HermiT finds it consistent and reports 0 CAP-10 candidates.
- Every run is falsified, as follows:
  - an unsatisfiable class, rejected;
  - CAP-16's fixture (an index member declared disjoint from its own parent), rejected;
  - an inconsistent case, rejected (HermiT);
  - CAP-10's fixture (an intersection of two capability classes), detected (HermiT).

## CP-1 and CP-2: where they stand

Test-only individuals exercise every CP-1 rule and every competency question, under the
decisions of 2026-11-15 (`docs/decisions/2026-11-15-d6-class-increment-accepted.md`, C and
D; `docs/decisions/2026-11-15-b1-b4-approved-cap34-confirmed.md`, B-1 to B-4). The full
account is the stage-completion record
(`docs/proposals/2026-11-15-stage05-tranche1-completion-record.md`), which waits on the
architect's acceptance. Stage 05 is not complete until then.

| Evidence | Where | Covers |
|---|---|---|
| Instance shapes, 11 constraints | `shapes/instance_shapes.ttl`; `tests/test_instances.py` | CAP-08, CAP-11, CAP-12, CAP-19, CAP-21 (Gate C-A), CAP-25, CAP-34 (has agent, confirmed N-4), CAP-35 |
| Description shapes, 42 constraints | `shapes/description_shapes.ttl`; `tests/test_description.py` | CAP-17, CAP-20, CAP-23, CAP-24, CAP-26, CAP-27, CAP-28, CAP-31, CAP-33, and the CD14 and CD17 rules |
| Gate M and CD15's answers | `tools/ontology/manifests.py`; `config/completeness-manifest.schema.json`; `tests/test_manifests.py` | CAP-18 and each CD15 applicability rule, positive and negative; CQ-4, CQ-5 |
| Competency questions | `tests/test_competency_questions.py` | CQ-1 to CQ-14, each by its authorized method (below) |
| Gate G | `tests/test_formalization.py`; CQ-12's no-write test | CAP-29 |
| CAP-10, CAP-16 | `tools/ontology/reason.py` | HermiT fixtures |

How each question is answered:

- **SPARQL over fixture organizations:** CQ-1, CQ-2, CQ-3, CQ-6, CQ-7, CQ-8, CQ-10, CQ-13
  and CQ-14.
- **CQ-9 and CQ-12, over a test-only coverage register**
  (`tests/fixtures/coverage_register.yaml`). They are demonstrated over fixture data only;
  the production register is Stage 06's and is not implemented.
- **CQ-4 and CQ-5, within CD15 manifests.** The answer is recorded, none recorded or
  unknown, never "not authorized".
- **CQ-11 from the signed review records** (`tools/ontology/review_records.py`). This is
  the B-4 exception: a review-record answer, not an OWL or SPARQL one. OI-4 stays open.

Not covered by any shape: the Gate F judgments (whether evidence establishes a negative
finding or is sufficient against its threshold), which are review work.

These files were under `ontology/` until 2026-10-25. Their git history is under that
path; `git log --follow` reaches it.
