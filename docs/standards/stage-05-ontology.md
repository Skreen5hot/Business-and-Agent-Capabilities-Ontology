# Ontology Development Standard
## Stage 05 — Ontology

| Field | Value |
|---|---|
| Status | **Approved** on 2026-11-15 as D5-1, with the validation architecture as D5-2 (`docs/decisions/2026-11-15-bpo-inquiry-and-d5-approved.md`). The approved text is `docs/proposals/2026-11-15-stage-05-ontology-standard.md` at `cd81767`, SHA-256 `128a81493f904a4211ebf170dede317a9d227a784a1608b58c37871a5afac77c`; only this status row and §9, the amendment history, differ from it. Under D5-2, a skipped or unavailable reasoner is not a passing checkpoint result. It authorizes no OWL: writing the first tranche needs a D6 implementation authorization. A substantive change is a new, reviewed version |
| Date | 2026-11-15 |
| Drafted by | Claude Code (`claude-opus-5-5`), for the BCO team |
| Applies to | The modules under `src/05_ontology/`, the shapes and fixtures that validate them, the vendored upstream extracts they rest on, and the tranche records that admit terms into them |
| Rests on | Specification v0.5.0-draft.3 (§2, §3.1, §4, §5, §6 CAP-01 to CAP-35, §8), accepted as ADR-002; CM-01 (approved); the Stage 03 standard (ratified 2026-11-07); ADR-003 D1 and RP-5 (namespaces); RP-3 (the BPO import boundary); roadmap §7 (tranche readiness) and §10 (stage completion) |

## 1. Purpose

Stage 05 turns reviewed, admitted terms into OWL 2 classes. It does that only for terms
that already carry the evidence that justifies them. It does not decide meaning. Meaning
is settled upstream:

- the definition, in the controlled vocabulary;
- the conceptual distinctions, in CM-01;
- the taxonomy, under Stage 03;
- admission, by G1-T.

Stage 05 records that meaning in a form a reasoner and SHACL can check, and keeps the OWL
traceable to each source.

## 2. What a tranche needs before any term is written

A tranche is written only after the architect approves its readiness record. D5 approves
the first tranche; D6 approves each later one. The record holds roadmap §7's eight items
and names, for every class:

1. its vocabulary concept, with the concept's record digest (`tools/vocab/build.py --digest`);
2. its G1-T record, signed PASS, with the SHA-256 of the signed baseline;
3. its realization index, member by member, exactly as signed;
4. its taxonomy links under the Stage 03 standard, with each one's kind and disposition;
5. any open source check or erratum that affects it.

A class whose source check is open is not written (§8).

## 3. Authoring rules

**S1 — IRIs.** A capability class is minted in `https://fandaws.com/ontology/bco#`, the
first of `AUTHORED_NAMESPACES`. Its local name is its vocabulary concept's local name, so
`bcoc:PaymentProcessing` becomes `bco:PaymentProcessing`. No IRI is minted for a concept
outside an approved tranche. Vocabulary IRIs stay with `tools/vocab/build.py`.

**S2 — The parent.** `bco:BusinessCapability` has two parents: `rdfs:subClassOf
cco:ont00000568` and `rdfs:subClassOf obo:BFO_0000016`. Its label and definition are those
of `bcom:BusinessCapability`, which follow specification §4. It was admitted by
ratification (`docs/decisions/2026-11-04-d4-rp1-rp10-ratified-option-b.md`), not by G1-T
(CD3).

**S3 — A specific capability class.** Each class has, and has only:

- `a owl:Class`;
- `rdfs:subClassOf bco:BusinessCapability`, its only named parent unless S6 allows another;
- `rdfs:label`, the concept's preferred label (`@en`);
- `skos:definition`, the concept's definition verbatim (`@en`), which is the signed
  definition;
- one `ex:enablesProcess` per member of its signed realization index, and no others.

It has no `owl:equivalentClass`, no `owl:disjointWith`, no restriction on
`obo:BFO_0000054` (CAP-02; an `only` needs a CAP-30 record), and no class-level
`obo:BFO_0000218`.

**S4 — Staging is not used for an admitted class.** CD3 lets a class sit under
`cco:ont00000568` alone until G1-T passes. A class in an approved tranche has passed, so it
goes straight under `bco:BusinessCapability`. A class that has not passed is not written
at all.

**S5 — Traceability lives in the tranche record, not in new annotations.** The tranche
record maps each class to its concept, its G1-T record and their digests. A test holds the
module to that record (§5, S05-T1). No annotation property is minted for it: the
specification allows two, `bco:concernsType` and `bco:assessedPresence` (§5), and neither
is for this.

**S6 — Subclass links between capability classes.** A retained `kind-of` link becomes
`rdfs:subClassOf` only when both ends are admitted and written, CD9's review is recorded
(CAP-10), and the tranche record lists it. A `part-of` link never becomes a subclass axiom
(Stage 03 §3). It gets no formal reading in this standard.

**S7 — BPO terms are referenced, never redeclared.** An index member is a BPO act class,
written through the temporary `ex:` binding to `https://fandaws.com/ontology/bpo#`
(decision of 2026-10-28, R3). The BCO's modules have no `owl:imports` of BPO. What
validation needs from BPO comes from the vendored extract, under the boundary in §4.

**S8 — No object property is minted.** Relations come from specification §5, chosen in
§3.1's reuse order: CCO's Extended Relation Ontology first, then the CCO domain ontology.
Every upstream IRI used is checked against the vendored extract. One that is not there yet
is added with `tools/ontology/vendor_upstream.py --rebuild`, never asserted from memory.

**S9 — Change control.** A substantive change to a written class is a new, reviewed
version of its tranche record. If the change affects the class's meaning or its admission
evidence, its G1-T record is reopened (direction of 2026-11-15, A). An editorial change to
a label is still checked against the vocabulary. The vocabulary changes first, and the
class follows.

## 4. The BPO import boundary

| Enters the BCO's validation graph, through the vendored extract | Never enters it |
|---|---|
| The declaration of each act class that a written index names (`rdfs:subClassOf` to its genus, and its label), from the slice that declares it | `ontology/capabilities_wiring.ttl` and `ontology/delivery_processes.ttl`, which assert `bpo:requiresCapability` (RP-3) |
| Each such genus, and its named ancestors up to CCO | Any class under `cco:ont00000568`: BPO's 39 capability-typed `bpo:P…` classes and its `…Capability` classes |
| The declaration of `bpo:enablesProcess` as an `owl:AnnotationProperty` | The PCF catalog nodes (`bpo:PCF_…`) and their text |

Everything enters at the BPO pin in `config/upstream-sources.yaml`. A class drawn from a
module that declares it more than once is taken from one named module (Q-13). A repin is
its own reviewed change.

## 5. Validation architecture

The ladder `tools/ontology/validate.py` runs today: conformance plus falsification, per
shape set. Stage 05 adds the checks below. **A new shape set arrives with its negative
fixture and positive controls in the same commit, and its messages are listed in
`tests/test_ontology_checks.py`.**

| Id | Check | Gate | When it runs | Fails on |
|---|---|---|---|---|
| S05-T1 | The module matches its tranche record: one class per listed concept, the label and definition match the vocabulary, the `ex:enablesProcess` set equals the signed index | pytest | every commit | an extra or missing class; any drift in label, definition or index |
| S05-C1 | CAP-01, K1 part: every class in `apqc-cap.ttl` is `bco:BusinessCapability` or is under it | SHACL | every commit | a class with no K1 parent |
| S05-C2 | CAP-02: no `some` restriction on `obo:BFO_0000054` from a K1 class | SHACL | every commit | the spec's `bco:BadCap` example |
| S05-C3 | CAP-03: every K1 class except the parent has at least one `ex:enablesProcess`; each target is declared in the extract, reaches `cco:ont00000228`, and is not under `cco:ont00000568` | SHACL, Gate B | every commit | a class with no index; a capability-typed member; an undeclared member |
| S05-C4 | CAP-06: a member under a CD5 development genus (Development, Improvement, Organizational Establishment, Acquisition) is listed in the tranche record with its review reason | pytest | every commit | an unreviewed development-genus member |
| S05-C5 | CAP-07: no deontic stem in a K1 definition | SHACL (WARN) | every commit | the spec's "regulatory mandate" example |
| S05-C6 | CAP-09: no K1 class under `obo:BFO_0000034` without a record; none declared disjoint from it | SHACL | every commit | an unrecorded Function subclass |
| S05-C7 | CAP-30: no `only` restriction without a record | SHACL | every commit | an `only` with no record |
| S05-C8 | RP-3: no excluded BPO module, and no `bpo:requiresCapability`, in the data graph | pytest | every commit | the excluded module loaded; the predicate present |
| S05-C9 | CAP-04 and CAP-32: every class has a G1-T PASS in its tranche record, and no failed class is in the module | pytest | every commit | a class with no PASS row |
| S05-D | Gate D, ELK: the module classifies | reasoner | every commit, SKIP where absent | an unsatisfiable class |
| S05-D2 | Gate D2, HermiT: CAP-16 satisfiability and consistency; CAP-10 candidates | reasoner | release and acceptance; SKIP on an ordinary commit, FAIL at a checkpoint | an index member or class unsatisfiable, the module inconsistent |
| S05-B | Gate B: every `obo:`, `cco:` and `ex:` IRI the module names is described in an extract | existing | every commit | an IRI asserted from memory |

The instance-level checks (CAP-08, CAP-11, CAP-12, CAP-17 to CAP-28, CAP-31, CAP-33 to
CAP-35) come with the first tranche that writes individuals or description-layer classes
(`apqc-cap-desc.ttl`). Until then they have nothing to select. Writing them early would
make a falsification rung pass on fixtures alone.

The conceptual-fidelity gate (roadmap D6) traces each written class to CM-01 elements
RL-01 and RL-02 and to the tranche record. The Ontology Template's P6 (incoming message
`EXAMPLE-BCO-2026-11-14-p6-stage05-request`) offers to measure it read-only. Using it is
optional.

## 6. Review

| Role | What it reviews |
|---|---|
| Ontologist (drafting) | The tranche record and the module, against §2 to §4 |
| Proxy Domain Expert (the architect) | The tranche record's readiness. The architect alone approves it |
| Independent reviewer (optional, synthetic) | The module against the tranche record, for drift only. It reopens no G1-T finding |

## 7. Stage completion

A tranche is complete when:

- its module passes every check in §5 that runs per commit, and D2 at the checkpoint;
- CP-1 and CP-2 are met (specification §10);
- the conceptual-fidelity trace is recorded;
- a stage-completion record in roadmap §10's form is approved.

## 8. Boundary

This standard:

- admits nothing, and decides no meaning;
- does not reopen a G1-T record;
- does not move BPO's capability classes into the BCO;
- does not write the description layer, a K2 union, an `only` restriction, a coverage
  register or a material-basis axiom.

Each of those is a later tranche, with its own record. A class whose source check is open
(`docs/catalog/tranche-2-followup.md`, §3) waits for the check, and if a defect is found,
it goes back to the architect alone.

## 9. Amendment history

Amendments the architect has decided, recorded here so the approved text above keeps
its meaning. None changes the specification baseline (v0.5.0-draft.3), which is
preserved.

| Date | Decision | What it changes |
|---|---|---|
| 2026-11-15 | B-1 (`docs/decisions/2026-11-15-b1-b4-approved-cap34-confirmed.md`) | **The description tranche is authorized**, notwithstanding §8's "does not write the description layer". It covers the seven description-layer classes, `bco:AuthorizationRecord`, `bco:FunctionalAdequacyAssessment` (under `cco:ont00000853`) and the annotation properties `bco:concernsType` and `bco:assessedPresence`, written into `apqc-cap-desc.ttl` from `src/05_ontology/tranche-2-description.yaml` (readiness record `docs/proposals/2026-11-15-stage05-description-tranche-readiness.md`). §2's per-class items apply as far as they can: a vocabulary concept and digest, and the parent. G1-T, the realization index and CAP-06 do not apply to information terms. The instance-level checks §5 deferred to this tranche are `shapes/description_shapes.ttl` |
| 2026-11-15 | B-3 | **§4's import boundary admits one more declaration:** BPO's `bpo:designatesProcessType` as an `owl:AnnotationProperty`, from `ontology/apqc-catalog.ttl` at the pin, for CQ-9's test-only coverage register. Catalog nodes and their text still never enter |
| 2026-11-15 | B-4 | **CQ-11 method exception.** The competency questions are answered by SPARQL over fixture data (specification §7), except CQ-11. CQ-11 is answered by a reproducible extraction over the CAP-06 review records, the signed G1-T records (`tools/ontology/review_records.py`), with an executable expected-answer test. It is a review-record answer, not an OWL inference or a SPARQL answer from the module. A class with no recorded development act has none recorded, never none that exists. OI-4 stays open, and no development property is authorized |
| 2026-11-15 | B-2 | **Gate M** (`tools/ontology/manifests.py`, `config/completeness-manifest.schema.json`) joins §5's checks, run on every commit. It applies to fixture manifests only until evidence graphs exist (Stage 06) |
| 2026-11-15 | N-4 | **CAP-34's performance relation** is confirmed as `cco:ont00001833` has agent / `cco:ont00001787` agent in. OI-8's relation selection is resolved for CAP-34 |
