# Stage 05 — Ontology

**Status:** first tranche implemented under D6
(`docs/decisions/2026-11-15-v05-transition-approved-d6-authorized.md`, E), against the
Stage 05 standard (`docs/standards/stage-05-ontology.md`) and specification
v0.5.0-draft.3. Not released, and not a claim of conformance with BFO, CCO or BPO as
published: the reasoners see the vendored extracts, which drop every anonymous class
expression. The tranche is not complete until CP-1 and CP-2, the conceptual-fidelity trace
and a stage-completion record are met (standard, section 7).

| Path | Holds |
|---|---|
| `apqc-cap.ttl` | `bco:BusinessCapability` and the first tranche's 39 specific capability classes, each with its signed realization index. Written by `tools/ontology/formalize.py --write`; never edit it |
| `tranche-1.yaml` | The tranche record the module is written from: each class's signed G1-T record (path, commit, SHA-256), concept digest and index, and the three types held back |
| `apqc-cap-desc.ttl` | The description layer. Still an `owl:Ontology` header: T3 has not reconciled its terms, and no tranche covers it |

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

Under the decision of 2026-11-15, C and D
(`docs/decisions/2026-11-15-d6-class-increment-accepted.md`), test-only individuals
exercise what can be encoded with existing terms. The full account, with every result, is
the stage-completion record (`docs/proposals/2026-11-15-stage05-tranche1-completion-record.md`).

**Demonstrated:**

- **Instance shapes** (`shapes/instance_shapes.ttl`, 11 constraints, each firing on its
  own test-only case, with 6 positive controls). They check CAP-08, CAP-11, CAP-12,
  CAP-19, CAP-21 (Gate C-A), CAP-25, CAP-34 and CAP-35.
- **The performance relation** (CAP-34, an encoding chosen at Stage 05): CCO's
  `has agent` / `agent in` (`cco:ont00001833` / `cco:ont00001787`). The Extended
  Relation Ontology has none.
- **Competency questions** CQ-1, CQ-2, CQ-3 and CQ-10, as SPARQL over two fixture
  organizations, the real module and the extracts
  (`tests/test_competency_questions.py`).
- **Gate G:** the index generator's tests (`tests/test_formalization.py`); CAP-29 holds
  because nothing generates assessments.
- **CAP-10 and CAP-16 fixtures** under HermiT (`tools/ontology/reason.py`).
- **The conceptual-fidelity trace:** `fidelity-trace-tranche-1.md`.

**Not demonstrated**, for the architect's decision, because each needs a term that is not
minted or an encoding that does not exist:

- **The description layer:** Capability Assessment, Map, Target, Maturity Rating, Sourcing
  Statement and Assessment, Target-State Specification, Authorization Record, Functional
  Adequacy Assessment, and the annotations `bco:concernsType` and `bco:assessedPresence`.
  These block CAP-17, CAP-20, CAP-23, CAP-24, CAP-26, CAP-27, CAP-28, CAP-31 and CAP-33,
  and CQ-5 to CQ-8, CQ-13 and CQ-14.
- **The CD15 completeness manifest and its schema (Gate M):** blocks CQ-4, CQ-5 and CAP-18.
- **The coverage register (CD16, Stage 06's) and the BPO import boundary:** block CQ-9
  and CQ-12.
- **A development relation (OI-4):** blocks CQ-11.

These files were under `ontology/` until 2026-10-25. Their git history is under that
path; `git log --follow` reaches it.
