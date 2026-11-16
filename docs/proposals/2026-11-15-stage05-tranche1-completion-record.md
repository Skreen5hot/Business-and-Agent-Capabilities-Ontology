# Stage-completion record — Stage 05, first tranche and description tranche (accepted)

| Field | Value |
|---|---|
| Status | **Accepted** by the architect on 2026-11-16 (`docs/decisions/2026-11-16-stage05-completion-accepted.md`). The reviewed version is this file at `2a9c6b1`, SHA-256 `95c65a47b67e3b6911d269cf9b77d2fd6cc358e56da8e8b36a4d81eaef0719c5`. Only the title, this row, CAP-13's and the encodings' rows in section 5, N-6 and N-9 in section 6, and section 9 differ from it. The first capability tranche and the description tranche of Stage 05 are complete under the standard's section 7, validated against test fixtures. Not a release |
| Date | 2026-11-15 |
| Prepared by | Claude Code (`claude-opus-5-5`), for the BCO team |
| Form | roadmap §10, "Stage-completion record". It cites artifacts by digest and does not copy them |
| Scope | The first Stage 05 tranche (`bco:BusinessCapability` and the 39 types of D5-3) and the description tranche (B-1). Earlier version: this file at `2b49eb5`, SHA-256 `05838920bf30…` |

## 1. Approved deliverables

Merged so far:

- the class-only increment, PR #54 at `69f0948`;
- the CP-1 and CP-2 evidence for existing terms, PR #55 at `2b49eb5`.

The description tranche, Gate M, the remaining competency questions and this update are
on branch `d6/tranche-2`. SHA-256 of each artifact as this record cites it:

| Artifact | SHA-256 |
|---|---|
| `src/05_ontology/apqc-cap.ttl` (the capability module (unchanged)) | `3b2f8a50e204a2a2ce45039e3ef69966a873f999c4036ac2d0b54f619baa979b` |
| `src/05_ontology/tranche-1.yaml` (its tranche record (unchanged)) | `a433ded84078b638b033d6651c31306347d0db035fe9c0877d5715c6b31ea0b6` |
| `src/05_ontology/apqc-cap-desc.ttl` (the description module) | `be9fea20dece2f41a5637ae19352eea05d15606e36602652c9435e74759e7048` |
| `src/05_ontology/tranche-2-description.yaml` (its tranche record) | `23ea554c4f4b6e99732a9858f4608ec9e7b099203688119cefd5cf842cab644e` |
| `docs/proposals/2026-11-15-stage05-description-tranche-readiness.md` (the description tranche's readiness record) | `675793811e50b5fc176dcc3c87ef2b65456c1cf44462da217249a129321bc75f` |
| `src/05_ontology/fidelity-trace-tranche-1.md` (the conceptual-fidelity trace, with its description addendum) | `b7bb4ae1080d2e37839911c7b1cdcad9155ca06b96d99c76a4702d7eb0424295` |
| `shapes/stage05_shapes.ttl` | `3aeeda48faa49961743300a112ba4b94996721408e24f97eca25c550bbf63e72` |
| `shapes/instance_shapes.ttl` | `c7ca715907be47446e471174f0a27bc224c5015fb163d1cd0f071c6fe5fd646b` |
| `shapes/description_shapes.ttl` (42 constraints) | `b71aaff40e3ebec66faa277239370c8598d6376d249f1a45bb9f941f73c11f82` |
| `shapes/instance_bad_examples.ttl` (test-only individuals) | `b4837b0a6118cb6ecd5994ba22bb9a9a2f48faffe4f840cf13e5a7b68f78cba5` |
| `shapes/description_bad_examples.ttl` (test-only individuals) | `dd5ba3689796506fb411326305cb1768839662ca0dd8f90b7ad959e021cf7755` |
| `config/completeness-manifest.schema.json` (the CD15 manifest schema (Gate M)) | `02ea3fc8b215dbc1ad8664e81f34abcd97fed50ea94d1db791fc9be968e502e2` |
| `tools/ontology/manifests.py` (Gate M and CD15's bounded answers) | `e4795e4fbeef54976135e3b395d1b3c41a0d5fde3e440320d34cf583a8b99d3c` |
| `tools/ontology/review_records.py` (CQ-11's review-record extraction) | `59a2fb218b365b2b0e3d6655e60cf7674df63a93fe4d72bd4a412df1b26a8475` |
| `tools/ontology/formalize.py` | `18be9c26b3d92b8c2b8d9ad89f04a52116c1dd7201c5c6ba6374e34e16e21713` |
| `tools/ontology/reason.py` | `cdd3cac85861e91ab71e38c58377cbf740fdbe493dd671f5c78615dfc428737e` |
| `tests/fixtures/cq_organizations.ttl` (test-only fixture organizations) | `883f348ef82413ff660a3af49c33070fb645e8d1fe194424e911be26d9dcc5e7` |
| `tests/fixtures/cq_description.ttl` (their test-only description layer) | `6cc49a6268c8aad30443ffb09b18ee42c3fbf17a131aa5185040ccdcda76f895` |
| `tests/fixtures/coverage_register.yaml` (the test-only coverage register (B-3)) | `ed562be51a53bf0d1a289eb9ec93151f61efe2dc2adf44f2fcd178bed64bc19e` |
| `tests/fixtures/cd15/manifests.json` (test-only manifests) | `29a22d1a3cca846e85e8d04103a6f63ca838d6fdd8998a9f5a773e730f4e6928` |
| `tests/fixtures/cd15/evidence.trig` (test-only evidence graphs) | `0c52ca63e198c44e23cb59ca6eec41926ad9a3cd555ae2a362fc373160f3ceb1` |
| `config/reasoner-pins.yaml` | `930ce2cf0e8d23ab6c71e4de834c5bdc73855bf9e4cde0b05619989de09f6b84` |
| `config/validation-baseline.json` | `d04831b541e48979e96ab453582e11922a0bb20b2d5a85e41c5382df7698cf87` |
| `config/corpus-digest.json` | `f5c3e77fd14b81fe3bea1217986d5c1775d8d95e896fd4feee702ade7a2567b3` |

## 2. Applicable standard and baselines

| Baseline | Reference | SHA-256 |
|---|---|---|
| Stage 05 standard | `docs/standards/stage-05-ontology.md`, approved 2026-11-15 (D5-1, D5-2), with its §9 amendment history (B-1 to B-4, N-4) | `d3eef7428a97fd05345c9710773cdad38f74962ff5958faf05b9a228e779b15f` |
| Specification in force | v0.5.0-draft.3, ratified under CP-0, ADR-002; preserved unchanged | `2224f869b0ec7a1e31b0afc1c2b403ad222ea290c334bff48a93ebbb6516c574` |
| Conceptual model | CM-01, approved 2026-10-26 | `292c8f36d64075b9663e159985a15b448aa933c3b5ed4baff3b2a556ca861ccc` |
| Admission | G1-T T1-02 and T1-03 at `7515f44`; the T2 batch at `1fdb2c5`. Not reopened | `f41e29cc…`, `b49935b7…`, `b44ec9ea…90ef` |

## 3. Reviewers and their capacities

| Role | Who | What |
|---|---|---|
| Proxy Domain Expert, approving authority | Aaron Damiano, Product Owner and Ontology Architect | D5, the D6 authorization, the increment's acceptance, B-1 to B-4 and N-4; final acceptance of this record |
| Ontologist (drafting) | Claude Code (`claude-opus-5-5`) | the modules, the tranche records, the shapes, the fixtures, the tools, the trace and this record |
| Independent reviewer | none for these tranches | — |

## 4. Decisions and dispositions

| Decision | Record |
|---|---|
| D5-1 to D5-7, the first tranche's readiness | `docs/decisions/2026-11-15-bpo-inquiry-and-d5-approved.md` |
| v0.5.0-draft.3 in force | `docs/decisions/2026-11-15-spec-v0.5-in-force.md` |
| D6 authorized | `docs/decisions/2026-11-15-v05-transition-approved-d6-authorized.md` |
| Class-only increment accepted; test fixtures authorized | `docs/decisions/2026-11-15-d6-class-increment-accepted.md` |
| APQC-derived act labels omitted from the BPO extract (the pin predates BPO's `NOTICE.md`) | the same record, "Verification under F" |
| B-1: the description tranche, including `bco:FunctionalAdequacyAssessment` under `cco:ont00000853` | `docs/decisions/2026-11-15-b1-b4-approved-cap34-confirmed.md`; readiness record `docs/proposals/2026-11-15-stage05-description-tranche-readiness.md` |
| B-2: the CD15 JSON manifest and Gate M | the same record |
| B-3: a test-only coverage register for CQ-9 and CQ-12 | the same record |
| B-4: CQ-11 by the review-record method; OI-4 open | the same record; standard §9 |
| N-4: CAP-34 is `cco:ont00001833` has agent / `cco:ont00001787` agent in; OI-8 resolved for CAP-34 | the same record |

## 5. Validation results

### Class level

| Check | Result |
|---|---|
| S05-T1, capability module | **PASS**: 40 classes, 160 members verified against the signed bytes; drift falsifications refused. `apqc-cap.ttl` is byte-identical to the merged one |
| S05-T1, description module | **PASS**: 9 classes and 2 annotation properties verified against the vocabulary build, §4 (by SHA-256), §5 and the decision; 5 drift falsifications refused (`tests/test_description.py`) |
| S05-C1 to C9; S3 | **PASS**, each with a falsification (unchanged) |
| S05-B, Gate B | **PASS**: every `obo:`, `cco:` and `ex:` IRI the modules and shapes name is described in an extract, after a rebuild for the description shapes' terms and BPO's `designatesProcessType` declaration |
| S05-D, ELK 0.6.0 | **PASS** over 5 files (the two modules, three extracts); the unsatisfiable and CAP-16 cases are rejected |
| S05-D2, HermiT 1.4.5.456, at the checkpoint | **PASS**: consistent, nothing unsatisfiable, 0 CAP-10 candidates. The unsatisfiable, CAP-16 and inconsistent cases are rejected and the CAP-10 case detected. Run locally on Java 23; CI runs it on Java 17 |
| SHACL ladder | **PASS**: 0 findings against authored terms over 5 shape sets; each fixture rejected (description 66 violations, instances 17, Stage 05 12, vocabulary 119, wellformedness 10) |

### CP-1 (specification §10)

> the first tranche's classes are formalized with their index. Every fixture checked by
> Gates B, C, C-A, G and M fails as stated, including CAP-21 and CAP-25 to CAP-35. Gates A to
> D are green. Requirements marked *encoding at Stage 05* have their encoding chosen.

| Requirement | Evidence | Result |
|---|---|---|
| Classes formalized with their index | `apqc-cap.ttl`; S05-T1 | **PASS** |
| Gates A to D green | parse; Gate B; the ladder; ELK | **PASS** |
| CAP-01, K3 part | `tests/test_description.py`: the description module holds exactly the 9 authorized information classes, each under one CCO information class | **PASS** |
| CAP-02 to CAP-10, CAP-12, CAP-14, CAP-16, CAP-30, CAP-32 | as recorded at `2b49eb5`: Stage 05 shapes, `test_formalization.py`, `reason.py`, instance shapes | **PASS** |
| CAP-05 (K2 unions) | no union exists; S05-C7 holds that no `only` restriction exists | **PASS, vacuously**. Stated so it is not mistaken for coverage |
| CAP-13 (`capability_scope.json`) | not exercised. The indexes are the signed G1-T indexes (D5-3); no scope file is an input to the module, so there is nothing to resolve | **NOT APPLICABLE TO THIS TRANCHE** (the decision of 2026-11-16): no fixture, not counted as a pass |
| CAP-11, CAP-19 | instance shapes, now also on a written `bco:CapabilityMap` that has a capability (the specification's case) | **PASS** |
| CAP-17 | 6 description constraints, each failing on its case: a map with a type annotation; an assessment with two; an Authorization Record naming a capability class; a map with an adequacy assessment as an entry; a map with no entry; a target naming an act class | **PASS** |
| CAP-18 | Gate M and `manifests.py`: a date outside the manifest returns *unknown*, never an empty set; an in-scope question returns *none recorded*; each CD15 rule has a positive and a negative case (`tests/test_manifests.py`, 24 tests) | **PASS** |
| CAP-20 | 6 constraints; the ordinal value encoded as `schema:ratingValue` (Stage 05 choice, for confirmation) | **PASS** |
| CAP-21 (Gate C-A) | instance shapes, asserted graph | **PASS** |
| CAP-22 | the test-only register's CAP-22 cases, a key that is a K1 class, an unresolved component, a designated class listed as a component, each fail; no subclass link is generated (`test_competency_questions.py`) | **PASS over fixture data**. The production register is Stage 06's |
| CAP-23, CAP-24, CAP-28, CAP-31 | description constraints, each failing on the specification's case (three organizations, two `describes`; a plain-string date, no authority; a prospective license typed Action Permission; a plan with no target) | **PASS** |
| CAP-25, CAP-34, CAP-35 | instance shapes: the vendor case, the organization-only performer, the single-member basis and joint performance preserved, as N-4 directs | **PASS** |
| CAP-26 | 3 constraints: no assessment; bearing asserted only as capability of with no assessment; an assessment citing only an Authorization Record; one citing only a past realization; two bearers | **PASS** at Gate C. Gate F's part (an organization chart as the only evidence) is review work |
| CAP-27 | 6 constraints and the CD14 absent-finding rule: no finding; two findings; no criteria; criteria with no identifier; an absent finding with no source; no date or two | **PASS** at Gate C. Gate F's part (evidence that establishes a negative finding; sufficiency against the threshold) is review work |
| CAP-29 (Gate G) | the index generator's tests; CQ-12 adds no triple when run | **PASS** |
| CAP-33 | 9 constraints: two findings; a finding without criteria, date or source; an unknown value; a presence finding on the adequacy assessment; an individual typed as both; a Capability Assessment stating an integration finding | **PASS** at Gate C. Gate F's part is review work |
| Gate M | `tools/ontology/manifests.py`: the schema is valid JSON Schema 2020-12; 4 fixture manifests built to pass pass, and 9 built to fail fail, one reason each | **PASS**, over fixture manifests only (no evidence graph exists before Stage 06) |
| Encodings marked *at Stage 05* | CAP-20: `schema:ratingValue`. CAP-33: findings as continuant parts with `schema:reviewAspect` and `schema:ratingValue`. CAP-34: has agent (confirmed). R5-02 and CD17's open representation are now chosen | **CONFIRMED** on 2026-11-16 (section 9): encoding conventions only, not Schema.org Ratings or Reviews |

**CP-1: MET**, over test-only fixtures. Two qualifications:

- The Gate F judgments in CAP-26, CAP-27 and CAP-33 need real evidence and a reviewer.
- CAP-13 is not exercised, because no scope file is an input.

### CP-2 (specification §10)

> Gate D2 has run, with an absent reasoner counted as FAIL. The CAP-10 and CAP-16 fixtures
> fail as stated. CQ-1 to CQ-14 are answered over a fixture organization, with CAP-18's
> positive and negative cases.

| Question | Method | Result |
|---|---|---|
| D2, absent reasoner as FAIL | `reason.py --checkpoint` (tested) | **PASS** |
| CAP-10, CAP-16 fixtures | HermiT | **PASS** |
| CQ-1, CQ-2, CQ-3, CQ-10 | SPARQL (as at `2b49eb5`; CQ-1 now also counts payroll tax) | **PASS** |
| CQ-4 ‡ | the realization log's manifest. The October answer is recorded for payroll and none recorded for cash management and payroll tax; November is unknown, outside the manifest | **PASS** |
| CQ-5 ‡ | the authorization manifest, per date over a period. Every index act under Act of Reporting is recorded; the remuneration act has none recorded, because the organization's record does not apply to its member; every uncovered act class is unknown | **PASS** |
| CQ-6 | SPARQL over the map | **PASS**: cash management and accounts payable; the incomplete evaluation is no entry |
| CQ-7 | SPARQL | **PASS**: one hybrid arrangement and one sourced-only arrangement |
| CQ-8 | SPARQL | **PASS** |
| CQ-9 | SPARQL over the test-only register's catalog nodes, with `ex:designatesProcessType` verified at the pin | **PASS over fixture data only**. One function designates a whole-function class, and one designates none and is answered by its register entry. A process node is not counted |
| CQ-11 | the CAP-06 review records, i.e. the signed G1-T records at their signed commits (`tools/ontology/review_records.py`): 14 acts over 12 of the 39 classes, with an expected-answer test, positive and negative examples, and none recorded for the rest | **PASS by the approved review-record method**. Not an OWL or SPARQL answer (B-4 exception); OI-4 open |
| CQ-12 | the test-only register joined to CQ-1 | **PASS over fixture data only**. Component possession is distinct from whole-function possession; it establishes no integration, availability or adequacy (the adequacy assessment of the same function finds adequacy not met); a function need not designate; no subclass axiom is generated |
| CQ-13 | SPARQL | **PASS**: the cash claim (only an incomplete evaluation) and the staged claim |
| CQ-14 | SPARQL | **PASS** |
| CAP-18, positive and negative | as under CP-1 | **PASS** |

**CP-2: MET**, with three qualifications:

- CQ-9 and CQ-12 are demonstrated over fixture data. No production coverage register is
  implemented.
- CQ-11 is answered by the approved review-record method.
- CQ-4 and CQ-5 answer within fixture manifests. No real evidence graph exists.

### Conceptual fidelity

**PASS** (unchanged for the 40 classes). The trace's new section 4 maps CM-01's RL-16 to
RL-23 to the description layer's encoding. No subclass link, object property or individual
was added.

### Suite

Full suite on `d6/tranche-2`: **834 passed, 2 skipped (the 2 skips predate this work)**. No competency question and no CAP rule is
skipped.

## 6. Outstanding issues

**Blocking:** none for CP-1 or CP-2, within the qualifications above. B-1 to B-4 are
resolved by the decision of 2026-11-15.

**Non-blocking:**

| # | Issue | Owner | Latest gate |
|---|---|---|---|
| N-1 | **Full upstream conformance.** The reasoners see the partial extracts, which drop anonymous class expressions. No consistency with the complete BFO, CCO or BPO is claimed | architect | before any conformance claim or release |
| N-2 | **The act labels** stay out of the BPO extract until BPO is re-pinned to a commit that carries its `NOTICE.md` | architect | a reviewed repin |
| N-3 | **T2-02, T2-24 and T2-31** wait for source checks SC-1 to SC-3 | Ontologist, then architect | the next tranche |
| N-5 | **The Q-12 inquiry** to BPO is unanswered | BPO, then architect | the Q-12 concepts' tranche |
| N-6 | **Confirm the two encodings chosen at Stage 05:** CAP-20's `schema:ratingValue`, and CAP-33's findings as continuant parts with `schema:reviewAspect` and `schema:ratingValue` (readiness record, section 4). A change edits shapes and fixtures, not the module | architect | **Resolved** 2026-11-16: both confirmed (section 9) |
| N-7 | **Evidence graphs, the production coverage register and Gate F on real evidence** are Stage 06's. Today Gate M checks fixture manifests only, and the Gate F judgments of CAP-26, CAP-27 and CAP-33 have no real evidence to judge | architect | Stage 06 authorization |
| N-8 | **What v0.5 leaves unrepresented:** revocation and supersession of Authorization Records (OI-21), supersession of assessments (OI-24), recorded content beyond the finding (OI-25), incomplete evaluations (OI-23) and the development relation (OI-4). Each answer states the limit that applies | architect | their own decisions |
| N-9 | **CAP-13** is not exercised, since no scope file is an input (the indexes are the signed ones). If a later tranche generates its index from `capability_scope.json`, CAP-13 needs its fixture then. Recorded as not applicable to this tranche (2026-11-16) | Ontologist | that tranche |

## 7. Upstream dependencies and pins

| Dependency | Pin |
|---|---|
| BFO 2020 | `044490fc`, `bfo-core.ttl` `6944e2c9…3b3b` |
| CCO v2.0 | `510dad76`, merged `e609db27…fe5b` |
| BPO v0.4.1 | `bc64e91`: `apqc-ext.ttl` in full; act classes (type and parents only) from `apqc_9_0.ttl` and `apqc_12_0.ttl`; the `enablesProcess` declaration from `capabilities_roles.ttl`; the `designatesProcessType` declaration from `apqc-catalog.ttl` (B-3) (`config/upstream-sources.yaml`, `b9f04b62…`) |
| Extracts | BFO `3249b5c5…`, CCO `7249b027…`, BPO `a44e6763…`; manifest `c7c41d0a…` |
| ROBOT | v1.9.11, commit `37d514d2`, `robot.jar` `53cd275c…ab26`; ELK 0.6.0, HermiT 1.4.5.456 |
| jsonschema | 4.26.0 (`requirements-dev.txt`), ARO's pin, for Gate M |
| schema.org | `https://schema.org/ratingValue` and `reviewAspect`, read at schema.org (no pinned file; the specification already reuses schema.org) |

## 8. Approval authority and recommendation

The approving authority is the architect.

**Recommendation: CP-1 and CP-2 are met for these tranches, within the qualifications in
section 5, and the record is ready for the architect's acceptance.** The classes and the
description layer are:

- implemented, written from records that are verified against their sources;
- validated, with every constraint falsified;
- reasoned at the checkpoint;
- traced.

Every CAP rule the specification names for CP-1 is exercised, except CAP-13. That rule has
no input to check, and is not counted. Every competency question is answered by its
authorized method.

What acceptance would and would not mean:

- **It would mean** that Stage 05 is complete for the first tranche and the description
  tranche.
- **It would not mean:**
  - a release;
  - conformance with the complete BFO, CCO or BPO (N-1);
  - a production coverage register or evidence graph (N-7);
  - any Stage 06 work, which is not authorized.

Before or with acceptance, the architect may wish to confirm or change the two encodings in
N-6.

## 9. Acceptance

The architect accepted this record on 2026-11-16 (`docs/decisions/2026-11-16-stage05-completion-accepted.md`): CP-1 and CP-2 are satisfied for
the approved first capability tranche and description tranche, with the recorded
qualifications. Those qualifications stay binding, here and in any future release
documentation:

- CAP-13 is not applicable to this tranche: the index-generation workflow does not consume
  `capability_scope.json`. It is not a passing test.
- CAP-05's union restriction check is vacuous: the tranche has no K2 union.
- CQ-9 and CQ-12 use the test-only coverage register.
- CQ-11 uses the CAP-06 review-record method; OI-4 stays unresolved.
- CQ-4, CQ-5 and Gate M operate on fixture evidence and manifests.
- Gate F has not established that any real-world evidence is sufficient.
- ELK and HermiT results apply to the pinned partial BFO, CCO and BPO extracts, not to the
  complete published ontologies.
- The upstream extract-refetch check was not exercised in CI. The local pin evidence
  (section 7) is kept, and the reproducibility check is required before any release or
  claim of full upstream conformance.

**Confirmed encodings.**

- **CAP-20.** A Capability Maturity Rating carries its ordinal value as
  `schema:ratingValue`: exactly one value, an identified ordinal scale, and the Capability
  Assessment as its source. The rating stays a CCO Ordinal Measurement Information Content
  Entity. It is not typed `schema:Rating`, and no OWL equivalence is asserted.
- **CAP-33.** A Functional Adequacy Assessment's three findings are continuant parts of it
  (`obo:BFO_0000178`). Each stays a Descriptive Information Content Entity, with
  `schema:reviewAspect` for its dimension (integration and coordination, operational
  availability, adequacy for the function), `schema:ratingValue` for "met", "partly met" or
  "not met", and its criteria, evidence and date. This is an RDF/SHACL encoding convention,
  not an assertion that the findings are Schema.org Reviews or Ratings.

No new property or class, assessment subclass relationship or capability-bearing inference
is authorized by either. N-1 to N-9 stay open with their scopes, except N-6, now resolved.
CP-3 and the source-coverage, migration and production-register obligations stay open
where applicable. The acceptance does not authorize a release, production G1-I assertions
or Stage 06 implementation, and does not mean every possible BCO capability is formalized.
