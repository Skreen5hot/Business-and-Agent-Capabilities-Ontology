# Stage-completion record — Stage 05, first tranche (draft for the architect)

| Field | Value |
|---|---|
| Status | **Prepared for the architect's final acceptance** (decision of 2026-11-15, H and I6: `docs/decisions/2026-11-15-d6-class-increment-accepted.md`). It completes nothing: completion is the architect's decision. Its recommendation is that the tranche is **not yet complete** (section 8) |
| Date | 2026-11-15 |
| Prepared by | Claude Code (`claude-opus-5-5`), for the BCO team |
| Form | roadmap §10, "Stage-completion record". It cites artifacts by digest and does not copy them |
| Scope | The first Stage 05 tranche: `bco:BusinessCapability` and the 39 types of D5-3 |

## 1. Approved deliverables

The class-only increment was accepted for integration and merged as PR #54 at
`69f0948`. The evidence for CP-1 and CP-2 is on branch `d6/cp1-cp2`, which is not yet
merged. SHA-256 of each artifact as this record cites it:

| Artifact | SHA-256 |
|---|---|
| `src/05_ontology/apqc-cap.ttl` (the module) | `3b2f8a50e204a2a2ce45039e3ef69966a873f999c4036ac2d0b54f619baa979b` |
| `src/05_ontology/tranche-1.yaml` (the tranche record) | `a433ded84078b638b033d6651c31306347d0db035fe9c0877d5715c6b31ea0b6` |
| `src/05_ontology/fidelity-trace-tranche-1.md` (the conceptual-fidelity trace) | `085058a8f8c99be02fcd312d51d70594ab5d7d632ff3a8ac1c54ae1100a5c825` |
| `shapes/stage05_shapes.ttl` | `3aeeda48faa49961743300a112ba4b94996721408e24f97eca25c550bbf63e72` |
| `shapes/stage05_bad_examples.ttl` | `8ca54b37a574d5489b2ed65119fd02d8a601fb643316d33fa716cc74fb8782a9` |
| `shapes/instance_shapes.ttl` | `c7ca715907be47446e471174f0a27bc224c5015fb163d1cd0f071c6fe5fd646b` |
| `shapes/instance_bad_examples.ttl` (test-only individuals) | `b4837b0a6118cb6ecd5994ba22bb9a9a2f48faffe4f840cf13e5a7b68f78cba5` |
| `tests/fixtures/cq_organizations.ttl` (test-only fixture organizations) | `883f348ef82413ff660a3af49c33070fb645e8d1fe194424e911be26d9dcc5e7` |
| `tools/ontology/formalize.py` | `8353966c7878aaf31e918b6d6924217cd3245300150a470b76f3ef1d0e467f6d` |
| `tools/ontology/reason.py` | `cdd3cac85861e91ab71e38c58377cbf740fdbe493dd671f5c78615dfc428737e` |
| `config/reasoner-pins.yaml` | `930ce2cf0e8d23ab6c71e4de834c5bdc73855bf9e4cde0b05619989de09f6b84` |
| `config/validation-baseline.json` | `316d93050b0cd6c5982b2f3c950ccc6ef415e62ffbd04019d63a5851b2d54503` |
| `config/corpus-digest.json` | `838f98d4ca9dabd6867f633527725bbcc76384cb0fc01568d9d9a35d44fc8293` |

## 2. Applicable standard and baselines

| Baseline | Reference | SHA-256 |
|---|---|---|
| Stage 05 standard | `docs/standards/stage-05-ontology.md`, approved 2026-11-15 (D5-1, D5-2) | `7faf9e2fc3ee60d868e11a626999475c0a5caf80286524a74386c9bbb6d98f1f` |
| Specification in force | v0.5.0-draft.3, ratified under CP-0, ADR-002 | `2224f869b0ec7a1e31b0afc1c2b403ad222ea290c334bff48a93ebbb6516c574` |
| Conceptual model | CM-01, approved 2026-10-26 | `292c8f36d64075b9663e159985a15b448aa933c3b5ed4baff3b2a556ca861ccc` |
| Admission | G1-T T1-02 and T1-03 at `7515f44`; the T2 batch at `1fdb2c5` | `f41e29cc…`, `b49935b7…`, `b44ec9ea…90ef` |

## 3. Reviewers and their capacities

| Role | Who | What |
|---|---|---|
| Proxy Domain Expert, approving authority | Aaron Damiano, Product Owner and Ontology Architect | D5, the D6 authorization, the increment's acceptance; final acceptance of this record |
| Ontologist (drafting) | Claude Code (`claude-opus-5-5`) | the module, the tranche record, the shapes, the fixtures, the trace and this record |
| Independent reviewer | none for this tranche | — |

## 4. Decisions and dispositions

| Decision | Record |
|---|---|
| D5-1 to D5-7, the first tranche's readiness | `docs/decisions/2026-11-15-bpo-inquiry-and-d5-approved.md` |
| v0.5.0-draft.3 in force | `docs/decisions/2026-11-15-spec-v0.5-in-force.md` |
| D6 authorized | `docs/decisions/2026-11-15-v05-transition-approved-d6-authorized.md` |
| Class-only increment accepted; CP-1 and CP-2 kept open; test fixtures authorized | `docs/decisions/2026-11-15-d6-class-increment-accepted.md` |
| APQC-derived act labels omitted from the BPO extract (the pin predates BPO's `NOTICE.md`) | the same record, "Verification under F" |
| Encoding chosen at Stage 05: the performance relation for CM-01 RL-14 and CAP-34 is `cco:ont00001833` has agent, inverse `cco:ont00001787`, because the Extended Relation Ontology has none | `shapes/instance_shapes.ttl`, header; for the architect's confirmation |

## 5. Validation results

### Class level: the merged increment

| Check | Result |
|---|---|
| S05-T1: the tranche record against its sources | **PASS**: 40 classes, 160 members verified against the signed bytes; 9 drift falsifications refused |
| S05-C1, C2, C3, C5, C6, C7 (SHACL, 11 constraints) | **PASS**: the module conforms; each constraint fires on its own case |
| S05-C1 (module), C3 (declaration), C4, C8, C9; S3 | **PASS**, each with a falsification |
| S05-B, Gate B | **PASS**: every IRI the module and the shapes name is described in an extract. A gap was found and fixed: the scan missed `prefix:local` names inside shape SPARQL |
| S05-D (ELK 0.6.0) | **PASS**; the unsatisfiable and CAP-16 cases rejected |
| S05-D2 (HermiT 1.4.5.456) | **PASS**: consistent, nothing unsatisfiable, 0 CAP-10 candidates. The unsatisfiable, CAP-16 and inconsistent cases are rejected and the CAP-10 case detected. Run in CI on Java 17 and locally on Java 23 |

### CP-1

| Requirement | Result |
|---|---|
| The tranche's classes formalized with their index | **PASS** |
| Gates A to D green | **PASS** (A: parse; B; C; D) |
| Gate C-A (CAP-21, asserted graph) | **PASS**: fires on the misfiled act; the real-class cross-check agrees |
| Gate G (generator tests; CAP-29) | **PASS**: the index generator's tests. CAP-29 holds because no generator writes assessments |
| Gate M (manifest schema) | **NOT DEMONSTRATED**: no CD15 manifest encoding or schema exists |
| CAP-21, CAP-25, CAP-34, CAP-35, and CAP-08, CAP-11, CAP-12, CAP-19 | **PASS**: 11 instance constraints, each failing as stated on its test-only case, with 6 positive controls. CAP-11 is stated over information content entities, because the K3 classes are not minted |
| CAP-26, CAP-27, CAP-28, CAP-31, CAP-33 (and CAP-17, CAP-20, CAP-23, CAP-24) | **NOT DEMONSTRATED**: they need description-layer terms that are not minted |
| CAP-30, CAP-32 | **PASS** as far as they reach: no `only` restriction exists (S05-C7), and no class has a failing record (S05-C9) |
| Encodings marked "at Stage 05" | CAP-34 chosen (above). CAP-20 and CAP-33 are not chosen: they belong to the description layer |

**CP-1: NOT MET.** Everything that existing terms can carry passes. The rest is blocked
(section 6).

### CP-2

| Requirement | Result |
|---|---|
| D2 run, with an absent reasoner counted as FAIL | **PASS**: `--checkpoint` fails when the reasoner is absent (tested) |
| CAP-10 and CAP-16 fixtures fail as stated | **PASS** |
| CQ-1, CQ-2, CQ-3, CQ-10 | **PASS**: SPARQL over two fixture organizations, the real module and the extracts. CQ-3 excludes the vendor case and the misfiled act |
| CQ-4 to CQ-9, CQ-11 to CQ-14 | **NOT DEMONSTRATED** (each a skipped test with its reason): see section 6 |
| CAP-18, positive and negative | **NOT DEMONSTRATED**: no manifest, no Authorization Record |

**CP-2: NOT MET.** 4 of 14 questions are demonstrated.

### Conceptual fidelity

**PASS.** The trace connects all 40 classes to CM-01, to their signed G1-T records and to
their concept digests, and a test holds it to the module. Every definition and index is
the signed one. Nothing CM-01 reserves for review is asserted. The one difference is in
wording, not meaning: the parent sits under disposition by ratification, which CM-01
predates.

### Suite

Full suite on `d6/cp1-cp2`: **781 passed, 13 skipped**. The skips are 2 that predate this work and the 11 items not demonstrated (CQ-4 to CQ-9, CQ-11 to CQ-14, CAP-18), each skipped with its reason and none counted as a pass.

## 6. Outstanding issues

**Blocking** (they stop CP-1 and CP-2; each is the architect's decision):

| # | Issue | Blocks | Owner | Latest gate |
|---|---|---|---|---|
| B-1 | The description layer is not minted: Capability Assessment, Capability Map, Capability Target, Capability Maturity Rating, Capability Sourcing Statement, Capability Sourcing Assessment, Capability Target-State Specification, Authorization Record and Functional Adequacy Assessment (whose representation §4 leaves open), and the annotations `bco:concernsType` and `bco:assessedPresence`. All are specified in the ratified §4. No tranche covers them, and T3 has not reconciled their terms | CAP-17, 20, 23, 24, 26, 27, 28, 31, 33; CQ-5, 6, 7, 8, 13, 14 | architect | CP-1 |
| B-2 | No CD15 completeness-manifest encoding or schema | Gate M; CQ-4, CQ-5; CAP-18 | architect | CP-1, CP-2 |
| B-3 | The coverage register (CD16) is Stage 06's. CQ-9 also needs `ex:designatesProcessType` from APQC catalog nodes, which the BPO import boundary excludes | CQ-9, CQ-12 | architect | CP-2, or a CP-2 scope decision |
| B-4 | No relation for development (OI-4). The specification answers CQ-11 by review records, and SPARQL cannot | CQ-11 | architect | CP-2, or a CP-2 scope decision |

**Non-blocking:**

| # | Issue | Owner | Latest gate |
|---|---|---|---|
| N-1 | Full upstream conformance. The reasoners see the partial extracts, which drop anonymous class expressions. No claim of consistency with the complete BFO, CCO or BPO is made (G) | architect | before any conformance claim or release |
| N-2 | The act labels are omitted from the BPO extract until BPO is re-pinned to a commit that carries its `NOTICE.md` | architect | a reviewed repin |
| N-3 | T2-02, T2-24 and T2-31 wait for source checks SC-1 to SC-3 | Ontologist, then architect | the next tranche |
| N-4 | Confirm the CAP-34 encoding (has agent) | architect | CP-1 acceptance |
| N-5 | The Q-12 inquiry to BPO is unanswered | BPO, then architect | the Q-12 concepts' tranche |

## 7. Upstream dependencies and pins

| Dependency | Pin |
|---|---|
| BFO 2020 | `044490fc`, `bfo-core.ttl` `6944e2c9…3b3b` |
| CCO v2.0 | `510dad76`, merged `e609db27…fe5b` |
| BPO v0.4.1 | `bc64e91`. `apqc-ext.ttl` in full; act classes (type and parents only) from `apqc_9_0.ttl` and `apqc_12_0.ttl`; the `enablesProcess` declaration from `capabilities_roles.ttl` (`config/upstream-sources.yaml`, `0934748c…`) |
| Extracts | BFO `3249b5c5…`, CCO `ceb15871…`, BPO `0471b10c…`; manifest `aaac9507…` |
| ROBOT | v1.9.11, commit `37d514d2`, `robot.jar` `53cd275c…ab26`; ELK 0.6.0, HermiT 1.4.5.456 |

## 8. Approval authority and recommendation

The approving authority is the architect.

**Recommendation: do not accept Stage 05's first tranche as complete yet.** The classes
are implemented, validated at class level, falsified, reasoned and traced. CP-1 and CP-2
are each partly met, and the rest of each waits on B-1 to B-4. Those are decisions,
not work this tranche can do without minting terms.

The decision asked of the architect:

- Authorize a description-layer tranche, or define its scope (B-1). Most of the rest
  follows from it.
- Choose a CD15 manifest encoding, or defer CQ-4, CQ-5 and CAP-18 explicitly (B-2).
- State whether CQ-9, CQ-11 and CQ-12 are in CP-2 for this tranche, given that they rest
  on Stage 06 and OI-4 (B-3, B-4).
- Confirm the CAP-34 encoding (N-4).
