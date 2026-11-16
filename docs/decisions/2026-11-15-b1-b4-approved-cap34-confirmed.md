# Decision record — Stage 05 B-1 to B-4 approved as bounded work; CAP-34 encoding confirmed; completion kept open, 2026-11-15

Recorded verbatim by Claude Code (`claude-opus-5-5`) on 2026-11-15, from the decision the
architect, Aaron Damiano, Product Owner and Ontology Architect, gave in session after PR
#55 merged into `main` as `2b49eb5`. The acts are the architect's. This record makes none.

## What it is about

`main` at `2b49eb5259bb2d980ecf328b7a1231a80dd91a6f` (PR #55 merged):

| Record | SHA-256 at `2b49eb5` |
| --- | --- |
| `docs/proposals/2026-11-15-stage05-tranche1-completion-record.md` (the completion record, B-1 to B-4, N-4) | `05838920bf305d7f870a2654e49e954f0259da85e143c59209b17d01536b511e` |
| `src/05_ontology/fidelity-trace-tranche-1.md` | `085058a8f8c99be02fcd312d51d70594ab5d7d632ff3a8ac1c54ae1100a5c825` |
| `shapes/instance_shapes.ttl` (the CAP-34 encoding, N-4) | `c7ca715907be47446e471174f0a27bc224c5015fb163d1cd0f071c6fe5fd646b` |
| `src/05_ontology/apqc-cap.ttl` (the completed class formalization, not reopened) | `3b2f8a50e204a2a2ce45039e3ef69966a873f999c4036ac2d0b54f619baa979b` |
| `specifications/Business-Capability-Ontology-v0.5.0-draft.3.md` (the ratified baseline, preserved) | `2224f869b0ec7a1e31b0afc1c2b403ad222ea290c334bff48a93ebbb6516c574` |

## The decision

> Subject: Architectural Decision — PR #55, Stage 05 B-1 to B-4 and CAP-34
> I have reviewed merged PR #55 and the Stage 05 first-tranche completion record.
> Decision: APPROVE THE BOUNDED WORK TO RESOLVE B-1 THROUGH B-4. CONFIRM THE CAP-34 ENCODING. KEEP CP-1, CP-2 AND FINAL STAGE 05 COMPLETION OPEN UNTIL THE REQUIRED EVIDENCE PASSES.
> Do not reopen the 42 signed G1-T admissions, D5, or the completed class-formalization work.
> B-1 — Description Layer: APPROVED
> Authorize a second, narrowly scoped Stage 05 formalization tranche implementing the seven description-layer classes already specified in v0.5:
>
> * Capability Map
> * Capability Assessment
> * Capability Maturity Rating
> * Capability Sourcing Statement
> * Capability Sourcing Assessment
> * Capability Target
> * Capability Target-State Specification
>
> Also authorize:
>
> * `bco:AuthorizationRecord`, as specified by CD15.
> * The two existing specification-defined annotation properties, `bco:concernsType` and `bco:assessedPresence`.
>
> Functional Adequacy Assessment — DECIDED:
> I approve representing Functional Adequacy Assessment as a distinct eighth description-layer OWL class, `bco:FunctionalAdequacyAssessment`, under CCO Descriptive Information Content Entity (`cco:ont00000853`).
> The justification is its distinct semantic target and finding structure: it evaluates a Standing Function through integration, availability and adequacy findings, rather than assessing possession of a particular capability type.
> Before declaring the class, document the reuse check against the pinned Extended Relation Ontology and relevant CCO domain ontology. If an existing class fully expresses this distinction, reuse that class rather than introducing a duplicate.
> It must not be a subclass of `bco:CapabilityAssessment`, a Capability Map entry, or evidence that a whole-function capability is possessed.
> Implement the three findings, required criteria, evidence and dates using verified existing properties and SHACL constraints. Do not invent object properties to represent them.
> Use the specification's approved definitions and CCO parents. Check their controlled-vocabulary records and source digests before writing the module.
> These are information-layer terms, not new Business Capability disposition types. G1-T is not applicable to them.
> Prepare the concise required tranche-readiness record and implement this bounded scope under this authorization. Escalate only a genuine conflict with approved meaning or the need for an otherwise unauthorized ontology term.
> B-2 — CD15 Completeness Manifest: APPROVED
> Adopt the ratified specification's external JSON completeness-manifest pattern.
> The manifest is not an OWL class and does not change OWL's open-world semantics.
> Implement a JSON Schema and Gate M checking the specified scope:
>
> * Evidence graph IRI.
> * Organization.
> * Covered acting agents.
> * Covered act classes.
> * Start and end dates.
> * Authority sources.
>
> Implement the existing CD15 applicability rules, including act-class hierarchy, agent identity, inclusive date ranges, overlapping records and multiple authority sources.
> Enforce the following distinction:
>
> * Applicable authorization evidence exists: report the recorded evidence.
> * No applicable record exists within a verified complete scope: report none recorded.
> * The question is outside the manifest's scope or completeness is not established: report unknown.
>
> Never infer legal non-authorization merely from absent records.
> Include CAP-18's required positive and negative fixtures, as well as cases involving incomplete scope, revoked-record limitations and missing authority evidence.
> Do not create a new ontology object property or authorization logic framework.
> B-3 — CQ-9 and CQ-12: TEST-ONLY REGISTER APPROVED
> The production coverage register remains Stage 06 work.
> For Stage 05 CP-2, authorize a minimal, test-only coverage register containing sufficient fixture data to demonstrate CQ-9 and CQ-12.
> For CQ-9, use the existing BPO `designatesProcessType` annotation only after verifying its declaration at the approved pin. Any necessary catalog-node assertions belong exclusively to the isolated fixture graph, not to the distributed BCO module or prohibited BPO import set.
> For CQ-12, join the test register's required component types with the fixture organization's independently asserted capability instances.
> The tests must demonstrate that:
>
> * Component possession is distinct from whole-function capability possession.
> * Component possession does not establish integration, availability or adequacy.
> * A Standing Function need not designate a whole-function capability type.
> * No component relationship automatically generates an OWL subclass axiom.
>
> Report CQ-9 and CQ-12 as demonstrated over fixture data, if the tests pass. Do not claim that a production coverage register has been implemented.
> B-4 — CQ-11 and OI-4: REVIEW-RECORD METHOD APPROVED
> Do not introduce a development object property.
> The ratified specification explicitly identifies CAP-06 review records as the interim source for answering which acts develop a capability, as distinguished from realizing it.
> Approve an explicit, CQ-11-specific exception to the general SPARQL-only competency-question requirement:
> Use a reproducible query or extraction over the authoritative CAP-06 review records, with an executable expected-answer test.
> Record this as a review-record answer, not an OWL inference or SPARQL answer from the capability module.
> Provide positive and negative examples that distinguish development evidence from realization indexes. Absence of a review record must not be represented as proof that no act can develop the capability.
> Document the limited method exception in the Stage 05 completion evidence and governing standard's amendment history. Preserve the ratified specification baseline.
> OI-4 remains open for a future justified formalization decision, but does not block the current Stage 05 increment.
> No new property is authorized.
> N-4 — CAP-34 Encoding: CONFIRMED
> I confirm:
>
> * `cco:ont00001833` — has agent
> * `cco:ont00001787` — agent in, its inverse.
>
> This is the approved existing CCO relation pair for the CAP-34 performance witness.
> The intended interpretation must remain strict: a member agent of the bearer organization actually performs the realizing Planned Act.
> Mere participation, supplying inputs, receiving outputs, authorizing another organization's work, or naming only the bearer organization is insufficient.
> Preserve the vendor counterexample, organization-only performer failure, single-member performer success and joint-performance success tests.
> Record OI-8's relation-selection issue as resolved for CAP-34.
> Validation and Completion
> Implement these decisions using the existing validation architecture.
> For every newly implemented class and property, verify its definition, parent or property type, IRI, provenance and compatibility with the pinned upstream ontologies.
> Extend the positive and negative fixtures to cover the applicable CAP requirements, and complete the competency-question evidence using the methods authorized above.
> Run the full required checks, including SHACL, Gate M, ELK, HermiT and the repository test suite.
> Do not count an absent implementation, skipped test, unavailable reasoner or fixture-only result beyond its stated scope as a pass.
> The current partial-extract reasoning results remain limited. No assertion of complete upstream BFO/CCO/BPO conformance or ontology release is authorized.
> After these checks, update the existing completion record with:
>
> 1. CP-1 and CP-2 outcomes, with explicit evidence for each remaining requirement.
> 2. The description-layer and CD15 implementation digests.
> 3. The CQ-9/CQ-12 fixture-only qualification.
> 4. The CQ-11 review-record-method exception.
> 5. The confirmed CAP-34 encoding.
> 6. Any genuinely unresolved defects or obligations.
>
> You may commit, push and open the necessary implementation PRs, and merge faithful implementations after required CI passes. Do not require another broad architectural proposal.
> Final Stage 05 completion remains reserved for my acceptance of the updated completion record. Stage 06 production knowledge-graph work is not authorized.
> Final direction: Implement the description layer and CD15 schema, demonstrate the outstanding competency questions with the approved bounded methods, and return the completed validation evidence—not another planning package.

## What it authorizes, and what it does not

- **Authorizes:** the description tranche (`src/05_ontology/tranche-2-description.yaml`,
  written into `src/05_ontology/apqc-cap-desc.ttl` by `tools/ontology/formalize.py`): seven
  description-layer classes, `bco:AuthorizationRecord`, `bco:FunctionalAdequacyAssessment`
  under `cco:ont00000853`, and the annotation properties `bco:concernsType` and
  `bco:assessedPresence`. Also the CD15 manifest schema and Gate M, a test-only coverage
  register, the CQ-11 review-record method, and implementation PRs merged after CI.
- **Does not authorize:** any object property; any change to the 42 signed G1-T admissions,
  D5 or `apqc-cap.ttl`; a production coverage register or any Stage 06 work; a claim of full
  upstream conformance or of a release; Stage 05 completion, which waits on the architect's
  acceptance of the updated completion record.
- **Resolves:** OI-8's relation-selection question for CAP-34 (`cco:ont00001833` /
  `cco:ont00001787`). OI-4 stays open.
