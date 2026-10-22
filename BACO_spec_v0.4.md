# Business Capability Ontology — Specification & Requirements

Oct 22, 2026 · @Aaron Damiano

| Field | Value |
| --- | --- |
| Title | Business Capability Ontology — Specification & Requirements |
| Type | Ontology specification and requirements; companion module to the Business Process Ontology |
| Version | 0.4.0-draft.1 (supersedes 0.3.0-draft.1) |
| Date | 2026-10-22 |
| Author | Aaron |
| Status | DRAFT — response to review R4 and the v0.1 term mapping; ADR-002 ratification pending RP-1, RP-2 and RP-7 to RP-10 |
| Domain | Enterprise architecture: organizational capabilities and their realization in business processes (BFO 2020 / CCO 2.0) |

## 0. Document control

This is a DRAFT for ratification. Nothing in it is normative until the architect ratifies it, and every requirement stays DRAFT until its falsifying fixture exists.

| Field | Value |
| --- | --- |
| Document ID | BPO-SPEC-CAP |
| Ratifying architect | Aaron |
| Decision record | Lands as ADR-002 "Organizational Capabilities and Their Realization"; folds into Methodology at next bump |
| Repository | [Skreen5hot/BusinessProcessOntology](https://github.com/Skreen5hot/BusinessProcessOntology) |
| Version history | 0.1.0-draft.1 → R2 → 0.2.0-draft.1 → R3 → 0.3.0-draft.1 → R4 and v0.1 term mapping → 0.4.0-draft.1 |
| Prior vocabulary | The reviewer's separate v0.1 Turtle package (`bc:` namespace) is reconciled in §9.1; it is not this document's v0.1 |

**Dependencies (to be pinned by content hash before any executable release — see OI-1):**

| Dependency | Version | Role |
| --- | --- | --- |
| BFO 2020 | ISO/IEC 21838-2 | Upper ontology |
| CCO | 2.0. The repo describes its `vendor/cco/` closure as 2024-11-06; the supplied Agent Ontology declares a 2024-11-05 version IRI. Hash pinning (OI-1) settles which files are meant | Mid-level; supplies Agent Capability, Organization Capability, Skill, Action Permission, measurement ICEs |
| [ADR-001](https://github.com/Skreen5hot/BusinessProcessOntology/blob/main/docs/adr/ADR-001-category-and-upper-level-modeling.md) | Accepted | Two-layer architecture, R1–R7, bridge annotation |
| BPO methodology | `apqc_to_bfo_cco_methodology.md`, current | Act-type vocabulary (D9 shared genera), validation gates |

## 0.1 Review disposition (R2 → v0.2)

Review R2 recommended revising before ratification. v0.2 accepts 14 of its 18 findings as written, accepts 4 with amendment, and rejects none outright. The four amendments are pushbacks on the proposed fix, not on the finding; each gives its reason below.

| ID | Finding (R2 ref) | Disposition | v0.2 change |
| --- | --- | --- | --- |
| R2-01 | `allValuesFrom` is necessary, not a definition (CD4, CD9) | Accepted | Classes declared primitive; identity carried by bearer, grounding and realization type (CD4, CD9) |
| R2-02 | A realization union does not show the bearer can do every member act (§3.2) | Accepted with amendment | Coverage is not axiomatized; it is expressed by component capabilities and queried (CD4, CQ-12) |
| R2-03 | CAP-01 catches realization-union classes | Accepted | CAP-01 and CAP-03 scoped to the capability class register |
| R2-04 | External dependency test too strict (CD2, G1) | Accepted with amendment | G1 now tests grounding, not participation. The basis boundary itself is kept (CD2) |
| R2-05 | Single-member replacement test too strong (G1) | Accepted | Replaced by an organizational-arrangement test; key-person fragility recorded as assessment |
| R2-06 | Type vs instance references in the description layer (CD11, CQ-6–8) | Accepted | New CD14: annotation `ex:concernsCapabilityType`; punning rejected |
| R2-07 | CQ-4, CQ-5 read absence as falsity | Accepted | New CD15: closed-world declarations over named evidence graphs |
| R2-08 | Act subclassing does not justify disposition subclassing (CD9, CAP-10) | Accepted | Mirroring yields candidates for review, not assertions |
| R2-09 | CD5 prohibition too strong | Accepted with amendment | Rewritten as a justification rule; one act may both realize and develop |
| R2-10 | CAP-16 fixture can leave the capability satisfiable | Accepted | CAP-16 checks realization classes and union members |
| R2-11 | Software as ICE vs the material system running it (CD13) | Accepted | Functions borne by the deployed computing artifact |
| R2-12 | CAP-11 ignores subproperties of is about | Accepted | Describes, ordinal measurement of and prescribes admitted |
| R2-13 | CCO relations already available (§4) | Accepted | OI-8 largely closed; IRIs re-checked at Gate B against the pin |
| R2-14 | Revised definitions (§5) | Accepted with amendment | Maturity Rating and Sourcing Statement adopted as proposed; Business Capability adopted but keeps the owns-or-controls boundary |
| R2-15 | CAP-15 treats hybrid sourcing as an exception | Accepted | CAP-15 retired |
| R2-16 | D2 SKIP must not pass a release | Accepted | D2 absent blocks a release |
| R2-17 | `some` → `only` on Competitive Analysis is its own decision | Accepted | Split into two migration items |
| R2-18 | Editorial: CD12–13 after Sources; "one reality-layer class"; unlabelled authorization example; CCO date | Accepted | All corrected |

**Where v0.2 pushes back**

- **R2-04 — the boundary stays.** The reviewer's revised definition grounds the capability in "the organized material capacities of its members and artifacts" with no ownership or control qualifier. That would let a vendor's staff and systems count toward the consumer's basis, which is exactly the case CD2 exists to exclude. v0.2 adopts the reviewer's distinction between grounding and realization conditions, and keeps the qualifier.
- **R2-02 — no "can do all six" axiom.** OWL cannot state of one disposition that its bearer can perform every member of a set of act types. Expressing it honestly needs one capability per act type. v0.2 does that and makes coverage a query, rather than adding an axiom that would look like coverage and assert none.
- **R2-09 — v0.1 was per-capability, not per-genus.** CD5 forbade counting the development of C as a realization of C; it never barred development genera generally, and CAP-06 was already WARN. The reviewer is right that one act can exercise and strengthen the same capability, so the rule is restated as a justification requirement.
- **R2-06 — an annotation, not a new relation.** The reviewer asked for a queryable type reference without a new object property. v0.2 uses an annotation property, which is DL-safe for class IRIs and mirrors the existing ADR-001 R4 bridge.

## 0.2 Review disposition (R3 → v0.3)

Review R3 recommended keeping the v0.2 architecture and deferring ADR-002 until RP-2, RP-6 and RP-7 have consistent, executable requirements. v0.3 accepts 6 of its 10 findings as written and 4 with an amended fix; none is rejected. Its central point is adopted: specialization, functional coverage and recorded performance are now three separate structures.

| ID | Finding (R3 ref) | Disposition | v0.3 change |
| --- | --- | --- | --- |
| R3-01 | Component coverage is not subclassing (CD4, CD9, CQ-12) | Accepted with amendment | Parent capability means any ability within its function (CD9). Coverage moves to a coverage register (new CD16). The scope file gains a `components` field to hold it |
| R3-02 | CAP-17 single-type cardinality breaks on maps (CD14) | Accepted with amendment | Maps carry no type; their entries are assessments and targets, as continuant parts, each with exactly one type (CD14, CAP-17) |
| R3-03 | CQ-5 has no defined evidentiary target (CD15) | Accepted with amendment | Permission records name an act type and an acting agent; completeness declarations state their coverage (CD15, CQ-5, CAP-24) |
| R3-04 | CAP-03 contradicts CD4 on direct act-class fillers | Accepted | K2 narrowed to named unions; a filler may be a reality-layer act class directly |
| R3-05 | CAP-16 cannot catch an unsupported realization | Accepted | New CAP-21 checks realizations against asserted act types, before reasoning |
| R3-06 | G1 accepts arrangements as evidence of ability (CD2) | Accepted | G1 gains an ability-evidence question; responsibility and authorization documents do not count |
| R3-07 | Sourcing statements cannot separate consumer, provider and act type (CQ-7) | Accepted with amendment | Structural convention on `describes` and `is about`, with roles where they exist (CD11, CAP-23) |
| R3-08 | A maturity rating can pass without a value or scale (CAP-20) | Accepted | Rating must carry an ordinal value, a scale and provenance |
| R3-09 | CP-1 and CP-2 disagree on when CAP-16 must pass | Accepted | CAP-16 moves to CP-2 |
| R3-10 | Historical capability bearing underspecified (CQ-4) | Accepted | CQ-4 restated for capabilities borne at query time; listed as a known limit |

**Where v0.3 amends R3's fix**

- **R3-01 — the register needs a new field.** R3 suggests `capability_scope.json` already serves as the coverage register. It does not: it maps capabilities to processes, not functions to component capabilities. v0.3 adds a `components` field rather than overloading the existing lists.
- **R3-02 — entries, not several annotations on the map.** R3 left both open. A bare type annotation cannot say whether a type is present, absent or needed, and CQ-6 depends on that distinction. Entries that are assessments or targets carry it.
- **R3-03 — `permits` cannot reach an unexercised capability.** `cco:ont00001910` relates a regulation to process *instances*. A permission for acts not yet performed must point at an act *type*, which is the problem CD14 already solves. v0.3 therefore generalizes `ex:concernsCapabilityType` into one annotation, `ex:concernsType`, for capability and act classes alike, instead of adding a second.
- **R3-07 — roles alone do not separate the parties.** An organization can be a customer in one arrangement and a contractor in another, so role assertions on the organizations cannot say which side each plays in a given statement. v0.3 identifies the consumer structurally: it is the single target of `describes`. The provider is the other `is about` target. Contractor and customer roles are asserted where they exist, as corroboration.

## 0.3 Review disposition (R4 and term mapping → v0.4)

R4 found that CD2 conflicted with BFO's own material-basis relation, and that was the decisive finding: v0.4 withdraws the owns-or-controls qualifier from grounding, which v0.2 had defended against R2. Of R4's 15 findings, v0.4 accepts 11 as written and 4 with an amended fix. Of the term mapping's 5 recommendations, it accepts 4 and declines 1.

**Review R4**

| ID | Finding (R4 ref) | Disposition | v0.4 change |
| --- | --- | --- | --- |
| R4-01 | Owned or controlled artifacts are not parts of a CCO Organization (§2) | Accepted | The organization alone bears the disposition; its basis is its constituent members. Artifacts are enabling conditions (CD2, RP-1) |
| R4-02 | G1 mixes type admission with instance attribution (§2) | Accepted | G1 split into G1-T and G1-I (§8, CAP-25, CAP-26) |
| R4-03 | `only` is not an index of capability types (§3) | Accepted with amendment | The mandatory index is the existing `ex:enablesProcess`; `only` becomes optional and reviewed (CD4, CAP-30) |
| R4-04 | CAP-21 misses union membership (§3) | Accepted | CAP-21 checks against the index members directly |
| R4-05 | Action Permission entails a permitted process (§4) | Accepted with amendment | Register holds Authorization Records; `cco:ont00000751` only for an authorization of an act that occurred (CD15, CAP-28) |
| R4-06 | Component possession is not integrated ability (§5) | Accepted | CQ-12 asks about component possession only; integration is an assessment (CD16, CAP-29) |
| R4-07 | The coverage register needs a function key (§5) | Accepted with amendment | Keyed by APQC catalog concepts, in a separate `coverage_register.json` (CD16) |
| R4-08 | Sourcing relies on relation placement (§6) | Accepted | Narrowed to a two-party record under a stated application convention (CD11, CAP-23) |
| R4-09 | Present findings missing; `partial` undefined (§7) | Accepted | Every assessment states a finding; `partial` cites its criteria (CD14, CAP-27) |
| R4-10 | Specialization review must cover grounding and realization (§7) | Accepted | CAP-10 review criteria stated (CD9) |
| R4-11 | CAP-09 stricter than CD6 (§7) | Accepted | Function classification allowed with a justification record |
| R4-12 | CAP-11 overbroad (§7) | Accepted | Scoped to capability-bearing and realization assertions |
| R4-13 | `cco:ont00001739` annotates the measured entity, not the rating (§8) | Accepted with amendment | The value is a data value on the rating ICE, not the annotation (CAP-20) |
| R4-14 | Completeness and validity lack a machine-validated form (§9) | Accepted | Completeness manifest as a schema'd JSON artifact; record validity as typed dates (CD15) |
| R4-15 | Reconcile the v0.1 vocabulary (§10) | Accepted | Term mapping below and §9.1 |

**Term mapping (v0.1 `bc:` → v0.4)**

| ID | Recommendation | Disposition | v0.4 change |
| --- | --- | --- | --- |
| TM-1 | Retain a Capability Description class | Declined | Type-level meaning stays in the class's own definition and its catalog node |
| TM-2 | Keep Sourcing Assessment distinct from Sourcing Statement | Accepted | `ex:CapabilitySourcingAssessment` minted as a sibling, not a subclass, of Capability Assessment |
| TM-3 | Keep Target-State Specification distinct from Capability Target | Accepted | `ex:CapabilityTargetStateSpecification` minted under CCO Plan |
| TM-4 | Keep maturity rating; carry the wider maturity evaluation elsewhere | Accepted | The evaluation is a Capability Assessment; the rating cites it as source |
| TM-5 | No equivalence axioms between v0.1 and v0.4 IRIs | Accepted | Controlled rename through a migration manifest (§9.1) |

**Where v0.4 amends the fix**

- **R4-03 — the index already exists.** R4 asks for a new annotation-based index. `ex:enablesProcess` is already that index, generated from `capability_scope.json` and declared an annotation in CD12. Making it mandatory adds no term.
- **R4-05 — a commitment, not a contradiction.** OWL is atemporal and no competency question counts permitted processes, so the entailed process yields no inconsistency and no wrong answer. It is still a false commitment for a never-used license, so it is fixed. The same entailment already exists in the BPO: slice 1.0 declares `ex:BusinessAuthorization ⊑ cco:ont00000751` (OI-16).
- **R4-07 — a separate file.** v0.3 proposed a `components` field inside `capability_scope.json`. Coverage is keyed by function and scope by capability, so they are now separate files.
- **R4-13 — value on the rating, not the capability.** Moving the value to the capability instance, where `cco:ont00001739` belongs, would collapse two ratings of one capability into one value. A data value on the rating ICE keeps value, scale and source together.
- **TM-1 — declined.** The mapping's question, "what does Strategic Planning Capability mean?", is answered by the class definition and, for standing functions, the catalog node that designates it. An ICE that restates it is a third place to define the same thing, and the three would drift. If capability dictionaries must travel as information artifacts, OI-17 tracks that need.

## 1. Purpose, scope and non-goals

The Business Capability Ontology (BCO) says what an organization can do. The Business Process Ontology (BPO) says what it does. The BCO is a module of the BPO repository, not a separate ontology: it takes its act types from the BPO reality layer and adds the dispositions those acts realize.

It operationalizes ADR-001 R5 and R6. R5 already sends standing-function nodes ("Manage X") to capabilities; R6 says to model them under CCO Organization Capability. Neither rule says when a capability is a BFO Disposition, what bears it, or what realizes it. This spec does.

**In scope**

- Organization capability classes, their bearer, grounding basis, and realization by BPO act types.
- The boundary between capability and role, permission, skill, artifact function and plan.
- A description and assessment layer: capability maps, assessments, maturity, sourcing and target state as ICEs about capabilities.
- Validation rules extending BPO Gates A–D.

**Non-goals**

- Individual competency modeling beyond reusing CCO Skill.
- A new act-type hierarchy. Act types come from the BPO reality layer and `apqc-ext.ttl` only.
- A maturity scoring method. The BCO represents assessments; it does not prescribe how to score.
- Deontic logic. Permissions and requirements are reused from CCO, not reasoned over.
- Industry capability frameworks (BIZBOK, BIAN). These may enter later as further catalog schemes.

## 2. Architecture

The BCO adds two layers to the BPO's two. Capabilities point down to the acts that realize them; descriptions point down to the capabilities they are about; nothing in the capability layer points up.

&#91;embedded content: BCO within the BPO · four layers over BFO/CCO\]

The catalog bridge is ADR-001 R4, unchanged: a catalog node that passes R5 designates a process class, and a standing-function node designates a capability class under R6.

**Module layout (proposed)**

| File | Content |
| --- | --- |
| `ontology/apqc-cap.ttl` | `ex:BusinessCapability`, all capability classes with their `ex:enablesProcess` index, and any reviewed K2 unions, moved out of the slices |
| `ontology/apqc-cap-desc.ttl` | The seven description-layer classes and the Authorization Record |
| `ontology/apqc_shapes.ttl` | CAP shapes beside the existing ones; CAP-21 runs on the asserted graph only |
| `capabilities/capability_scope.json` | Kept; generates the mandatory realization index (CD4, CD12) |
| `capabilities/coverage_register.json` *(new)* | Standing function (APQC catalog concept) → required capability classes (CD16) |
| `qa/evidence/*.manifest.json` *(new)* | Completeness manifests for evidence graphs, checked by Gate M (CD15) |
| `docs/migration/bc-v0.1-to-v0.4.json` *(new)* | Term-by-term rename record for the `bc:` vocabulary (§9.1) |
| `docs/adr/ADR-002-organizational-capabilities.md` | This spec's decisions, once ratified |

Moving capability classes out of the slices follows D9's single-source rule for shared terms. Slices that need them inline the declarations, as they already do for act genera.

## 3. Design decisions (CD1–CD17)

These seventeen commitments carry the design. Each is proposed, not ratified. A tag such as *(v0.4, R4-01)* marks a decision changed in that version under the review finding named. They are numbered CD to avoid collision with methodology D1–D9 and ADR-001 R1–R7.

Three questions run through them, and v0.4 keeps them apart: **admissibility** (can capabilities of this type be genuine dispositions?), **possession** (does this organization bear one?), and **adequacy** (is what it bears sufficient, available, sourced, authorized and integrated for its purpose?). The first is settled in the ontology, the second by evidence, the third by assessments.

**CD1 — Bearer** *(v0.4, R4-01)*. A Business Capability inheres in a `cco:ont00001180` Organization, and in nothing else. Capabilities borne by a person are CCO Skill or Agent Capability and are out of scope, except as part of an organization's basis (CD2).

**CD2 — Grounding basis** *(v0.2, R2-04; v0.4, R4-01)*. The material basis (`obo:BFO_0000218`) of a Business Capability is a set of the organization's own constituents: its member agents, in the organizational arrangement among them. BFO requires a material basis to be a continuant part of the bearer, and a CCO Organization is a group of agents.

- **Artifacts are enabling conditions.** Systems, equipment and facilities, even ones the organization owns or controls, are not parts of a group of agents and so are not the basis. They take part in realizations. Losing one makes the capability *unavailable*, which is recorded in an assessment; it does not make the capability cease.
- **Ownership and control sort dependencies only.** v0.2 kept "owns or controls" in the grounding definition; that is withdrawn. The qualifier now only decides whether an enabling condition is internal, or an external dependency recorded by a sourcing statement.
- **Basis is not the conditions of realization.** A retailer that coordinates deliveries through carriers can bear a logistics-coordination capability grounded in its own staff; the carrier bears its own delivery capability.
- **The provider's work is the provider's.** When another organization's staff perform the acts, the consumer bears no capability for them. Internal capability and sourcing may coexist for the same acts.
- **Fragility is not reclassification.** A capability may depend on one indispensable member and still be organizational, provided its realization runs through organizational arrangements. Losing that member can end the disposition.
- **Ability, not assignment.** An organization chart, an assigned responsibility, a charter or an authorization shows that the organization is responsible or permitted, not that it is able (G1-I).
- **The cost, stated.** When a bank decommissions a core platform without changing its staff, its capability persists latently and is assessed as unavailable. The alternative, a socio-technical system bearer whose parts include artifacts, is tracked as OI-14.
- **Ratification item RP-1** (revised in v0.4).

**CD3 — Admission and attribution** *(v0.4, R4-02)*. A capability class may be asserted `rdfs:subClassOf obo:BFO_0000016` only after it passes the type-admission test G1-T (§8). Asserting that a particular organization bears an instance requires separate instance-level evidence, G1-I. Admitting a class licenses no organization's claim to bear one.

- A class not yet admitted stays under `cco:ont00000568` alone. That is a staging state, not a final category: BFO 2020 divides realizables into dispositions and roles, so a class that fails G1-T must be reclassified or deleted.

**CD4 — Realization index** *(v0.2, R2-01; v0.3, R3-04; v0.4, R4-03)*. Every capability class carries a mandatory realization index: one or more `ex:enablesProcess` annotations, each naming a BPO reality-layer act class or a D9 genus. The index lists admissible realization types. It makes no modal claim and no claim of exhaustiveness.

- **`only` is optional and reviewed.** A class may also carry `obo:BFO_0000054 only <Filler>`, but only with a review record defending the index as exhaustive (CAP-30). Its filler is the single index member, or a K2 union of the members. An unreviewed `only` would turn a provisional process catalog into a claim about every possible realization.
- **Classes are primitive.** A capability's identity is its bearer kind (CD1), its grounding (CD2) and its realization index together. The textual definition states all three. No equivalence axiom is claimed.
- **Observed realizations are checked on asserted data.** An act that `realizes` a capability must have an asserted type under one of the capability's index members (CAP-21), never a type the reasoner supplied.
- **Coverage is not here.** Whether an organization can carry out a whole function is CD16.
- **Non-deontic indexing.** Index members must be describable without deontic success conditions. Where a BPO act is institutional, the capability indexes to the non-deontic act it contains; standing is a role or a permission.

**CD5 — Development and realization** *(v0.2, R2-09)*. Developing capability C and realizing C are different relations an act can stand in. An act counts as a realization of C only when it is justified as an exercise of C; that it brings C about or improves it is not that justification.

- One act may do both: practice that exercises a capability can also strengthen it.
- An act may develop C while realizing a different capability, as when change management builds a new governance capability.
- Example: "Maintain business models" realizes business model governance capability. "Establish business model governance" develops it, and realizes it only if separately justified as an exercise.

**CD6 — Overlap with Function** *(v0.4, R4-11)*. Business Capability is not declared disjoint from BFO Function. A capability class may be classified under Function only with a justification record showing that its instances exist because the organization was designed to have them (CAP-09).

**CD7 — Capability is not role or permission.** No capability definition may mention assignment, responsibility, authorization, license or mandate. "Able but not authorized" and "authorized but not able" must both be representable without contradiction.

**CD8 — No latency exclusion.** No capability class carries an existential realization axiom. A capability that has never been exercised is admissible.

**CD9 — Primitive classes, reviewed specialization** *(v0.3, R3-01; v0.4, R4-10)*. `rdfs:subClassOf` between capability classes means specialization only.

- **A parent means any ability within its function.** Every accounting capability is a financial-management capability of some kind. A parent does not mean complete ability to carry out the function.
- **Review establishes membership, not similarity.** A subclass link is asserted only when review establishes that every instance of the narrower disposition is an instance of the broader one, in bearer, grounding and realization. Overlapping or nested realization types alone are insufficient.
- **Candidates come from the index.** A pair is a candidate (CAP-10) when every index member of the narrower class falls under some index member of the broader one.
- **Nothing is induced.** Neither the coverage register (CD16) nor APQC partonomy generates subclass links.

**CD10 — Member-wise bearing is not organizational bearing** *(v0.2, R2-13)*. Organization-to-capability uses `cco:ont00001954` (has capability), with inverse `cco:ont00001889` (capability of). `cco:ont00001898` (aggregate has capability) says each member bears its own capability instance of the type, not that the aggregate bears one. It never stands in for a Business Capability.

**CD11 — Descriptions are about, not of** *(v0.4, R4-08, R4-12)*. Description-layer ICEs refer to organizations and capability instances by `cco:ont00001808` (is about) or its subproperties: `cco:ont00001982` (describes) and `cco:ont00001811` (is a ordinal measurement of). Directive ICEs may use `cco:ont00001942` (prescribes). A capability listed in a map is not thereby asserted to exist.

- **What is forbidden is narrow.** No ICE may bear a capability or realize one. Provenance, authorship, carrier and parthood relations on ICEs are unaffected (CAP-11).
- **Sourcing is a two-party record, by convention.** A Capability Sourcing Statement concerns exactly two organizations: it `describes` the consumer and is about the provider, and carries one `ex:concernsType` naming the act class sourced. This is an application convention validated by SHACL (CAP-23). It is not a meaning `describes` or `is about` has in CCO. Brokers, intermediaries and provider networks are out of scope for v0.4 (OI-18). Contractor and customer roles corroborate where they exist.

**CD12 — Enablement is the realization index** *(v0.4, R4-03)*. `capabilities/capability_scope.json` generates `ex:enablesProcess`, which is now the mandatory realization index of CD4. It remains an annotation with no causal or modal entailment.

- `requiresCapability` stays withdrawn. Read as stated, it would say every act of a type needs an organization bearing the capability, which is false whenever a contractor or a single person performs it.
- Each scope entry is checked against CD5 before it enters the index.

**CD13 — Agent manifests describe; they do not bear** *(v0.2, R2-11)*. `capabilities/agents.json` lists software agents against Organization Capability classes. No software agent bears an Organization Capability (CD1).

- Software is information content, not a material entity, so it bears no BFO realizable. Any artifact function belongs to the deployed computing artifact that executes it.
- The manifest is an ICE that designates the capability types an agent serves (CD14). It keeps its routing use.
- Under CD2, that computing artifact is an enabling condition of the organization's capabilities, not part of their basis.

**CD14 — Type references and findings** *(v0.3, R3-02; v0.4, R4-09)*. An ICE that concerns a class rather than an instance carries the annotation `ex:concernsType`, valued with a capability class or act class IRI.

- **Maps carry entries, not types.** A Capability Map has its entries as continuant parts (`obo:BFO_0000178`). Each entry is a Capability Assessment or a Capability Target with exactly one `ex:concernsType`.
- **Every assessment states its finding.** Each Capability Assessment carries one `ex:assessedPresence` (`present`, `absent` or `partial`), whether or not it links a capability instance. A `present` finding is an evidential claim, not proof that the disposition exists.
- **`partial` is relative.** A partial finding cites the criteria it is relative to (a component set, a declared scope or an evaluation criterion) through `dct:conformsTo`. It never means a fraction of a disposition.
- Rejected: punning, and per-type designator individuals. The pattern mirrors `ex:designatesProcessType` and stays in OWL 2 DL.

**CD15 — Closed-world evidence** *(v0.3, R3-03; v0.4, R4-05, R4-14)*. OWL reasoning stays open-world. Absence questions are evaluated over named evidence graphs whose completeness is declared in a manifest.

- **Authorization Records, not Action Permissions.** CCO defines `cco:ont00000751` as a regulation that permits some process, so typing a prospective license as one asserts that a permitted process exists. The register therefore holds `ex:AuthorizationRecord`s. Each is about the acting agent, names the permitted act class with `ex:concernsType`, carries `schema:validFrom` and `schema:validThrough` as `xsd:date`, and cites its authority with `dct:source`.
- **Action Permission once an act occurs.** A `cco:ont00000751` individual is asserted only for an authorization of an act that actually occurred, and it `permits` that act (`cco:ont00001910`).
- **The completeness manifest lives outside OWL.** It is a JSON artifact with a fixed schema: graph IRI, organization, acting agents, covered act classes, start and end dates, and authority sources. A graph is complete only within that scope.
- **Answers are bounded.** "No applicable authorization recorded within the declared scope", never "not authorized". Outside any manifest, an absence question returns *unknown*.

**CD16 — Functional coverage** *(v0.3, R3-01; v0.4, R4-06, R4-07)*. Coverage of a standing business function is separate from specialization (CD9) and from recorded performance (CD15).

- **The coverage register** is `capabilities/coverage_register.json`. It is keyed by the APQC catalog concept of each standing function (`ex:PCF_<id>`), which keeps ADR-001's catalog–reality separation, and lists the capability classes the function requires.
- **Coverage is component possession.** CQ-12 asks whether O bears an instance of every listed component. That is not the same as being able to perform the function as an integrated whole.
- **Integration is assessed, never derived.** Whether the components are coordinated, available and sufficient is a Capability Assessment, and is never generated from a CQ-12 result (CAP-29).
- **No generated axioms.** Listing a component creates no subclass link, and a function need not have a capability class of its own.

**CD17 — Information-layer scope** *(new, TM-1 to TM-5)*. The description layer has seven classes. Three distinctions from the v0.1 vocabulary are kept: a sourcing statement (the arrangement) is distinct from a sourcing assessment (the dependence on it); a capability target (the end state) is distinct from a target-state specification (the plan to reach it); and a maturity rating (the ordinal result) is distinct from the assessment that produced it. What a capability type means is stated once, in the class definition and its catalog node; no separate description ICE restates it.

## 4. Terms

The module mints: the generic parent `ex:BusinessCapability`; the specific capability classes; a K2 union only where a reviewed `only` restriction needs one; seven description-layer classes; one evidence-register class; and two annotation properties. Everything else is reused. Each term lists what it does not imply, because that is where misuse starts.

**Reality layer**

| Term | Definition | Parents | Does not imply |
| --- | --- | --- | --- |
| Business Capability `ex:BusinessCapability` *(rev. v0.4)* | An Organization Capability that is a Disposition inhering in an Organization, whose material basis is constituent member agents of that organization in their organizational arrangement, and that, when realized, is realized in Planned Acts of the types in its realization index. | `cco:ont00000568`, `obo:BFO_0000016` | That it has ever been realized. That it is available now (enabling artifacts may be missing). That the organization is authorized. That any one member bears it. That artifacts it owns are its basis. That it was designed (Function). |
| Specific capability classes (`ex:StrategicPlanningCapability` and the rest) | Each states its bearer kind, grounding and realization index in its definition, and carries one or more `ex:enablesProcess` (CD4). | `ex:BusinessCapability` after G1-T; `cco:ont00000568` alone before (CD3) | That any organization bears one. That the class is OWL-defined. That a parent means complete ability to carry out its function (CD9). |
| Realization union `ex:<Name>Realization` | A Planned Act class defined as the union of a capability's index members, used only as the filler of a reviewed `only` restriction. | `cco:ont00000228` | That every instance realizes this organization's capability. That the bearer can perform every member type. |

**Description layer** (CD17)

| Term | Definition | Parent | Does not imply |
| --- | --- | --- | --- |
| Capability Map `ex:CapabilityMap` | A Descriptive ICE that describes an organization and has, as continuant parts, the Capability Assessments and Capability Targets that are its entries. | `cco:ont00000853` | That any listed capability exists. That the arrangement of entries is parthood among capabilities. |
| Capability Assessment `ex:CapabilityAssessment` *(rev. v0.4)* | A Descriptive ICE that describes an organization with respect to the presence, absence or partial presence of a capability of one given type, states that finding, and cites its evidence and criteria. | `cco:ont00000853` | That the finding is true. That an instance exists. That `partial` is a fraction of a disposition. |
| Capability Maturity Rating `ex:CapabilityMaturityRating` *(rev. v0.4)* | An Ordinal Measurement ICE that ranks an existing Organization Capability instance on a specified ordinal scale, carrying its ordinal value as a data value and citing the assessment that produced it. | `cco:ont00001010` | Graded capability subclasses. Any particular scale or scoring method. Use for an absent capability. |
| Capability Sourcing Statement `ex:CapabilitySourcingStatement` | A Descriptive ICE that describes an Organization's arrangement for obtaining performances of one specified Planned Act class from one other Organization. | `cco:ont00000853` | That the consumer lacks an internal capability for the same acts. That the consumer bears the provider's capability. A multi-party arrangement. |
| Capability Sourcing Assessment `ex:CapabilitySourcingAssessment` *(new, TM-2)* | A Descriptive ICE that is about a Capability Sourcing Statement and describes the consumer's dependence on that arrangement (operational risk, possibility of substitution, and whether the consumer bears an internal capability for the sourced acts) on stated criteria and evidence. | `cco:ont00000853` | That the dependence is a defect. That the consumer lacks an internal capability. |
| Capability Target `ex:CapabilityTarget` | An Objective that prescribes that an organization come to bear a capability of one given type. | `cco:ont00000476` | That the capability is absent now. How it is to be reached. |
| Capability Target-State Specification `ex:CapabilityTargetStateSpecification` *(new, TM-3)* | A Plan that prescribes the acts through which an organization is to reach one or more Capability Targets, such as recruitment, training, technology deployment or a sourcing arrangement, and has those targets as continuant parts. | `cco:ont00000974` | That the plan has been adopted or carried out. That the targets will be met. |

**Evidence register** (CD15)

| Term | Definition | Parent | Does not imply |
| --- | --- | --- | --- |
| Authorization Record `ex:AuthorizationRecord` *(new, R4-05)* | A Descriptive ICE that is about an agent and records an authorization for that agent to perform acts of one act class during a stated period, citing the authority that issued it. | `cco:ont00000853` | That any permitted act occurred. That the authorization is valid in fact. That it is a `cco:ont00000751` Action Permission. |

**Annotation properties**

| Term | Use | Value |
| --- | --- | --- |
| `ex:concernsType` | Identifies the capability class or act class an ICE concerns (CD14) | A capability class IRI or an act class IRI |
| `ex:assessedPresence` | Records the finding of every Capability Assessment (CD14) | `present`, `absent` or `partial` |

**Reused without change:** `cco:ont00001180` Organization · `cco:ont00000568` Organization Capability · `cco:ont00001379` Agent Capability · `cco:ont00000089` Skill · `cco:ont00000751` Action Permission · `cco:ont00001010` Ordinal Measurement ICE · `cco:ont00000974` Plan · `cco:ont00000476` Objective · `obo:BFO_0000218` has material basis · Dublin Core `dct:source`, `dct:conformsTo` · schema.org `schema:validFrom`, `schema:validThrough` · BPO `ex:InternalCapabilityData`, `ex:CoreCompetencyAnalysis`, `ex:RequiredCapabilityList`.

## 5. Relations and core pattern

The module mints no object property. It uses existing BFO, CCO, Dublin Core and schema.org terms plus four annotation properties. CCO IRIs taken from reviews are re-checked against the pinned closure at Gate B (OI-8).

| Relation | IRI | Use in BCO | Constraint |
| --- | --- | --- | --- |
| has capability / capability of | `cco:ont00001954` / `cco:ont00001889` | Organization ↔ its Business Capability | Supported by G1-I evidence (CAP-26) |
| has material basis | `obo:BFO_0000218` | Capability → constituent member agents | Never an artifact (CD2, CAP-25) |
| aggregate has capability | `cco:ont00001898` | Member-wise claims only | Never for a Business Capability (CD10) |
| has realization / realizes | `obo:BFO_0000054` / `obo:BFO_0000055` | Capability ↔ act instance | Asserted act type under an index member (CAP-21); `only` optional and reviewed (CAP-30) |
| has continuant part | `obo:BFO_0000178` | Map → its entries; Target-State Specification → its targets | CD14, CD17 |
| is about / describes | `cco:ont00001808` / `cco:ont00001982` | ICE → organization, agent, capability instance or other ICE | Sourcing: two-party convention (CD11) |
| is a ordinal measurement of | `cco:ont00001811` | Maturity rating → capability instance | Instance must exist |
| prescribes | `cco:ont00001942` | Directive ICE → entity it prescribes | — |
| permits | `cco:ont00001910` | Action Permission → an act that occurred | Never on a prospective authorization (CAP-28) |
| ordinal measurement annotation | `cco:ont00001739` | Not used on ratings | Reserved for the measured entity (R4-13) |
| source / conforms to | `dct:source` / `dct:conformsTo` | Evidence and authority; scale or criteria | CD14, CD15, CAP-20 |
| valid from / valid through | `schema:validFrom` / `schema:validThrough` | Authorization Record validity, `xsd:date` | CD15 |
| enables process | `ex:enablesProcess` (annotation) | Capability class → act class | Mandatory realization index (CD4, CD12) |
| designates process type | `ex:designatesProcessType` (annotation) | Catalog node → capability class | ADR-001 R4, unchanged |
| concerns type | `ex:concernsType` (annotation) | ICE → capability class or act class | CD14 |
| assessed presence | `ex:assessedPresence` (annotation) | Assessment → its finding | Mandatory (CD14) |

**Class pattern.** The index is mandatory; the `only` restriction is shown commented out because it needs a CAP-30 review record.

```turtle
ex:StrategicPlanningCapability a owl:Class ;
    rdfs:subClassOf cco:ont00000568 ;               # ex:BusinessCapability once G1-T passes
    ex:enablesProcess ex:P10037 , ex:P10045 , ex:P10039 ,
                      ex:P10043 , ex:P10020 , ex:P19949 .   # realization index

# Only with an exhaustiveness review record (CAP-30):
# ex:StrategicPlanningCapability rdfs:subClassOf
#     [ a owl:Restriction ; owl:onProperty obo:BFO_0000054 ;
#       owl:allValuesFrom ex:StrategicPlanningRealization ] .
```

**Instance pattern 1 — possession, a realization and a rating.** The assessment is the G1-I evidence for the bearing claim; the rating cites the assessment.

```turtle
ex:acme a cco:ont00001180 ;                          # Organization
    cco:ont00001954 ex:acme_spc .                    # has capability
ex:acme_spc a ex:StrategicPlanningCapability .
ex:acme_2027_mission a ex:P10037 ;                   # asserted type, an index member
    obo:BFO_0000055 ex:acme_spc .                    # realizes
ex:acme_spc_assessment a ex:CapabilityAssessment ;   # G1-I evidence
    cco:ont00001982 ex:acme_spc ;
    ex:concernsType ex:StrategicPlanningCapability ;
    ex:assessedPresence "present" ;
    dct:source ex:acme_strategy_staffing_record , ex:acme_2027_mission .
ex:acme_spc_rating a ex:CapabilityMaturityRating ;
    cco:ont00001811 ex:acme_spc ;                    # is a ordinal measurement of
    dct:conformsTo ex:house_maturity_scale ;
    dct:source ex:acme_spc_assessment .
    # ordinal value: a CCO value data property, e.g. "3"^^xsd:integer (IRI per OI-8)
```

**Instance pattern 2 — a map with entries (CD14).**

```turtle
ex:acme_map a ex:CapabilityMap ;
    cco:ont00001982 ex:acme ;
    obo:BFO_0000178 ex:acme_map_e1 , ex:acme_map_e2 , ex:acme_map_e3 .
ex:acme_map_e1 a ex:CapabilityAssessment ;
    cco:ont00001982 ex:acme_spc ;
    ex:concernsType ex:StrategicPlanningCapability ;
    ex:assessedPresence "present" .
ex:acme_map_e2 a ex:CapabilityAssessment ;
    cco:ont00001982 ex:acme ;
    ex:concernsType ex:TreasuryManagementCapability ;
    ex:assessedPresence "absent" .
ex:acme_map_e3 a ex:CapabilityTarget ;
    cco:ont00001808 ex:acme ;
    ex:concernsType ex:TreasuryManagementCapability .
```

**Instance pattern 3 — a two-party sourcing statement and its assessment (CD11, CD17).**

```turtle
ex:acme_payroll_sourcing a ex:CapabilitySourcingStatement ;
    cco:ont00001982 ex:acme ;                        # consumer
    cco:ont00001808 ex:payco ;                       # provider
    ex:concernsType ex:ActOfRemuneration .           # act class sourced
ex:acme_payroll_dependence a ex:CapabilitySourcingAssessment ;
    cco:ont00001808 ex:acme_payroll_sourcing ;
    dct:conformsTo ex:vendor_dependence_criteria ;
    dct:source ex:acme_vendor_review_2026 .
```

**Instance pattern 4 — a prospective authorization, and the manifest that bounds the register (CD15).**

```turtle
ex:acme_filing_auth a ex:AuthorizationRecord ;       # not cco:ont00000751
    cco:ont00001808 ex:acme ;                        # acting agent
    ex:concernsType ex:ActOfReporting ;              # act class authorized
    schema:validFrom "2026-01-01"^^xsd:date ;
    schema:validThrough "2026-12-31"^^xsd:date ;
    dct:source ex:state_regulator_portal .
```

```json
{
  "graph": "ex:graph_acme_authorizations",
  "organization": "ex:acme",
  "acting_agents": ["ex:acme"],
  "act_classes": ["ex:ActOfReporting"],
  "start": "2026-01-01",
  "end": "2026-12-31",
  "authority_sources": ["ex:internal_register", "ex:state_regulator_portal"]
}
```

**Instance pattern 5 — a target and the plan to reach it (CD17).**

```turtle
ex:acme_treasury_target a ex:CapabilityTarget ;
    cco:ont00001808 ex:acme ;
    ex:concernsType ex:TreasuryManagementCapability .
ex:acme_treasury_plan a ex:CapabilityTargetStateSpecification ;
    obo:BFO_0000178 ex:acme_treasury_target .        # has continuant part
```

**Reasoner profile.** `owl:allValuesFrom` and `owl:unionOf` appear only on reviewed classes. They are outside OWL 2 EL, so Gate D (ELK) ignores them and Gate D2 checks them; D2 blocks a release if it cannot run (§8).

## 6. Requirements

Thirty live requirements and one retired, all DRAFT. IDs are stable across versions; CAP-25 to CAP-31 are new in v0.4, and R4's proposed CAP-25 to CAP-30 are adopted under those numbers with the amendments in §0.3. Each names the fixture that must make it fail; where a positive case matters, the fixture also names what must pass. FAIL blocks a build; WARN goes to `qa/queries/warn` for review.

**Class kinds.** Each class in the capability module is exactly one of:

- **K1 capability class:** under `cco:ont00000568`. `ex:BusinessCapability` is the K1 parent and is exempt from CAP-03.
- **K2 realization union:** a union class declared in the module, used only as the filler of a reviewed `only` restriction.
- **K3 information class:** an ICE class declared in `apqc-cap-desc.ttl`, covering the description layer and the evidence register.

| ID | Requirement | Fixture (fails unless noted) | Level · Gate | Traces |
| --- | --- | --- | --- | --- |
| CAP-01 | Every class in the capability module is exactly one of K1, K2 or K3. | A class under none; a K2 union no `only` restriction uses | FAIL · C | CD1 |
| CAP-02 | No K1 class has a `some` restriction on `obo:BFO_0000054`. | `ex:BadCap ⊑ BFO_0000054 some ex:P10037` | FAIL · C | CD8 |
| CAP-03 *(rev. v0.4)* | Every K1 class except the parent carries one or more `ex:enablesProcess`, each a reality-layer act class or a D9 genus, and at most one `only` restriction on `obo:BFO_0000054`, whose filler is its single index member or a K2 union of exactly its index members. | A K1 class with no index; an index value that is a catalog node; an `only` filler that adds a class not in the index | FAIL · C | CD4, R4-03 |
| CAP-04 *(rev. v0.4)* | A K1 class asserted under `obo:BFO_0000016` or `ex:BusinessCapability` carries a G1-T record (PASS, reviewer, date). No organization-specific evidence is required. | A Disposition subclass with no G1-T record | FAIL · C, F | CD3, R4-02 |
| CAP-05 | Every member of a K2 union is a member of the capability's index and never a catalog node. | Union containing `ex:PCF_17040` | FAIL · B, C | CD4, R7 |
| CAP-06 | An index member that is or falls under `ex:ActOfDevelopment`, `ex:ActOfImprovement`, `ex:ActOfOrganizationalEstablishment` or `ex:ActOfAcquisition` needs a review record saying why it exercises the capability. | Governance capability indexing an improvement act with no record | WARN · C, F | CD5 |
| CAP-07 | A K1 definition contains no deontic terms (authoriz-, licen-, mandat-, responsib-, assign-, permit-). | Definition "capacity to fulfill its regulatory mandate" | WARN · C | CD7 |
| CAP-08 | The subject of `cco:ont00001954` with a K1 object is a `cco:ont00001180` Organization. | `agent.strategy_lead.v1` has capability `ex:acme_spc` | FAIL · C | CD1, CD13 |
| CAP-09 *(rev. v0.4)* | A K1 class is placed under `obo:BFO_0000034` Function only with a design-justification record, and is never declared disjoint from it. | A Function subclass with no record; a disjointness axiom | FAIL · C, F | CD6, R4-11 |
| CAP-10 *(rev. v0.4)* | Every candidate pair under CD9's index rule is reviewed, and the review records why every instance of the narrower is an instance of the broader. | A subclass link resting only on realization overlap | WARN · D2, F | CD9, R4-10 |
| CAP-11 *(rev. v0.4)* | No K3 individual is the subject of has capability, bearer of, realizes or has realization. Other relations on ICEs are unaffected. | A map that has capability fails; a map with `dct:creator` passes | FAIL · C | CD11, R4-12 |
| CAP-12 | `cco:ont00001898` never has a K1 object. | Aggregate-has-capability to `ex:acme_spc` | FAIL · C | CD10 |
| CAP-13 | Every `capability_scope.json` key and listed process resolves to a declared class. | Key `ex:NoSuchCapability` | FAIL · B | CD12 |
| CAP-14 | No `ex:requiresCapability` triple is generated. | Any such triple in the build | FAIL · C | CD12 |
| CAP-15 | *Retired in v0.2.* Hybrid sourcing is normal, not an exception. | — | — | R2-15 |
| CAP-16 | Every K1 class, every K2 union and every index member is satisfiable under a DL reasoner, and the module is consistent. Accepted at CP-2. | An index member declared disjoint from its own parent | FAIL · D2 | CD4 |
| CAP-17 *(rev. v0.4)* | Assessments, targets, sourcing statements and Authorization Records each carry exactly one `ex:concernsType` (a K1 class for the first two, an act class for the last two). Maps and sourcing assessments carry none; a map has at least one assessment or target entry via `obo:BFO_0000178`. | A map with a type annotation; an assessment with two; an Authorization Record naming a capability class | FAIL · C | CD14, CD15 |
| CAP-18 *(rev. v0.4)* | An absence query returns *unknown* unless a manifest covers the graph, organization, agent, act class and dates asked. | Fails: a query for a date outside the manifest returns an empty set. Passes: an in-scope query returns "none recorded" | FAIL · query | CD15, R4-14 |
| CAP-19 | No ICE is the bearer of any realizable entity. | A software ICE bearing an artifact function | FAIL · C | CD13 |
| CAP-20 *(rev. v0.4)* | Every Capability Maturity Rating has `cco:ont00001811` to an existing K1 instance, exactly one ordinal data value on the rating, one `dct:conformsTo` scale, and a `dct:source` that is a Capability Assessment. `cco:ont00001739` is never asserted on a rating. | A rating with no value; a rating whose value is given by `cco:ont00001739` | FAIL · C | CD17, R4-13 |
| CAP-21 *(rev. v0.4)* | For every act that `realizes` a K1 instance, the act's asserted type falls under one of the capability's index members in the asserted class hierarchy, checked before any reasoning. | An act asserted only as `ex:P10729` (scoped to Accounting) realizing `ex:acme_spc` | FAIL · C-A | CD4, R4-04 |
| CAP-22 *(rev. v0.4)* | Every `coverage_register.json` key resolves to an APQC catalog concept, every component to a K1 class, and no `rdfs:subClassOf` is generated from the register. | A key that is a K1 class; an unresolved component | FAIL · B, C | CD16, R4-07 |
| CAP-23 *(rev. v0.4)* | A Capability Sourcing Statement `describes` exactly one Organization and is about exactly one other Organization. | Three organizations; two `describes` targets | FAIL · C | CD11, R4-08 |
| CAP-24 *(rev. v0.4)* | Every Authorization Record is about exactly one agent and has exactly one `schema:validFrom` and one `schema:validThrough` typed `xsd:date`, and at least one `dct:source`. | A plain-string date; no authority source | FAIL · C | CD15, R4-14 |
| CAP-25 *(new)* | `obo:BFO_0000218` from a Business Capability has only member agents of its bearer as objects, and G1-I evidence names candidate basis members or positions, never an artifact as basis. | Has material basis `ex:acme_core_platform` | FAIL · C, F | CD2, R4-01 |
| CAP-26 *(new)* | Every has capability triple with a K1 object is supported by a Capability Assessment that describes that instance, matches its type, finds it `present`, and cites at least one source that is not an organization chart, charter, responsibility assignment or Authorization Record. | Has capability with no assessment; an assessment citing only an Authorization Record | FAIL · C | CD3, R4-02 |
| CAP-27 *(new)* | Every Capability Assessment has exactly one `ex:assessedPresence`, and a `partial` finding has a `dct:conformsTo`. | The v0.3 present-capability example with no finding; a `partial` with no criteria | FAIL · C | CD14, R4-09 |
| CAP-28 *(new)* | No individual is typed `cco:ont00000751` unless it `permits` an asserted act instance, and no Authorization Record is typed `cco:ont00000751`. | A prospective license typed Action Permission | FAIL · C | CD15, R4-05 |
| CAP-29 *(new)* | No assessment, finding or has capability triple is generated from a CQ-12 result. | A pipeline step writing an "integrated" finding from CQ-12 | FAIL · C | CD16, R4-06 |
| CAP-30 *(new)* | Every `only` restriction on a K1 class has an exhaustiveness review record. | An `only` restriction with no record | FAIL · C, F | CD4, R4-03 |
| CAP-31 *(new)* | Every Capability Target-State Specification has at least one Capability Target as continuant part. | A target-state plan with none | FAIL · C | CD17, TM-3 |

## 7. Competency questions

The module is done when each question has a SPARQL query in `qa/` that returns the expected answer over a fixture organization. Questions marked ‡ ask about absence; they are answered only within a manifest's declared scope and return *unknown* otherwise (CD15, CAP-18).

| ID | Question | Answered by |
| --- | --- | --- |
| CQ-1 | Which capabilities does organization O bear? | `cco:ont00001954` from O |
| CQ-2 *(rev. v0.4)* | Which BPO act types are admissible realizations of capability type C? | C's `ex:enablesProcess` index |
| CQ-3 | Which capabilities did this act instance realize? | `obo:BFO_0000055` from the act, filtered by CAP-21 |
| CQ-4 ‡ | Which capabilities that O bears at query time have no recorded realization in period P? | Realization log within its manifest's scope |
| CQ-5 ‡ *(rev. v0.4)* | Which index act types of O's capabilities lack an applicable Authorization Record for acting agent A and period P? | Authorization Records' `ex:concernsType` and validity dates, against CQ-2, within the manifest's scope |
| CQ-6 | Which capability types does O's map record as needed (a target entry) with no assessment entry finding them present? | Map entries joined on `ex:concernsType` and `ex:assessedPresence` |
| CQ-7 *(rev. v0.4)* | For which act types does O have a sourcing arrangement, with which provider, and for which does O also bear a capability indexing that act type? | Two-party sourcing statements describing O (CAP-23), joined to CQ-1 and CQ-2 |
| CQ-8 | Which capability targets does O have, and which already match a capability O bears? | Targets' `ex:concernsType` joined to CQ-1 |
| CQ-9 | Which APQC catalog nodes are standing functions with a capability class? | `ex:designatesProcessType` to a K1 class |
| CQ-10 | Which capability classes have not passed G1-T? | K1 classes without a PASS G1-T record |
| CQ-11 | Which acts develop capability C, as distinct from realizing it? | CAP-06 review records (no ontology relation yet, OI-4) |
| CQ-12 *(rev. v0.4)* | Does O bear an instance of every capability class listed as a required component of standing function F? | `coverage_register.json` entry for F, joined to CQ-1. Answers component possession only, not integrated ability (CD16) |
| CQ-13 *(new)* | Which of O's capability-bearing claims lack a supporting present-finding assessment? | Has capability triples without a CAP-26 assessment |
| CQ-14 *(new)* | Which of O's sourcing arrangements have no sourcing assessment of the dependence? | Sourcing statements describing O with no Capability Sourcing Assessment about them |

## 8. Validation

The BCO adds two human tests (G1-T and G1-I), one reasoner gate (D2), an asserted-graph SHACL pass (C-A) and a manifest schema check to the existing BPO harness. Everything else extends gates that already run.

**G1-T — type admission** *(v0.4, R4-02)*. Asked once per capability class, with no particular organization in view. A reviewer answers all five as stated and records them against the class; a PASS licenses the Disposition subclass assertion (CAP-04).

1. **Bearer kind.** Is the bearer an Organization? (No → Skill or Agent Capability.)
2. **Basis kind.** Can the basis of capabilities of this type be stated as member agents in an organizational arrangement, without counting artifacts as basis? (No → reclassify, or OI-14.)
3. **Organizational, not individual.** Do realizations of this type run through coordination across organizational positions, rather than one member's skill alone? (No → Skill.)
4. **Non-deontic.** Is every index member describable without standing or authorization? (No → re-index to the non-deontic act.)
5. **Exercise, not development.** Is every index member an exercise of the capability rather than its development (CD5)? (No → remove it or record the justification.)

**G1-I — instance attribution** *(new, R4-02)*. Asked for each claim that a particular organization bears a capability. The answers are recorded as the supporting Capability Assessment that CAP-26 requires.

1. **Candidate basis.** Which members or positions ground it (CAP-25)? Artifacts are never named as basis.
2. **Ability evidence.** Members with the relevant skills in the positions concerned, or a recorded realization. Organization charts, charters, responsibility assignments and Authorization Records do not count.
3. **Own performance.** Are the acts performed by the organization's own members? (No → record a Capability Sourcing Statement, not a bearing claim.)
4. **Enabling conditions.** Which artifacts do the acts need, and are they available? Unavailability does not change the possession finding; it is an adequacy matter for the assessment.
5. **Fragility.** Does the capability depend on one indispensable member? Record it; it does not change the finding.

**Gate changes**

| Gate | Existing tool | BCO addition |
| --- | --- | --- |
| A Syntax | rdflib | Capability module, fixtures, scope file and coverage register parsed |
| B IRI resolution | rdflib + pinned CCO closure | CAP-05, CAP-13, CAP-22; CCO IRIs in §5 re-verified |
| C SHACL | pyshacl + `apqc_shapes.ttl` | CAP-01 to CAP-09, CAP-11, CAP-12, CAP-14, CAP-17, CAP-19, CAP-20, CAP-22 to CAP-31 |
| C-A SHACL on the asserted graph | pyshacl without inference, run before any reasoner | CAP-21 |
| M Manifest schema (new) | JSON Schema validator | Every completeness manifest matches the CD15 schema |
| D Reasoner | ELK via ROBOT | Unchanged; EL subset only |
| D2 DL reasoner | HermiT via ROBOT | CAP-10 candidates, CAP-16 |
| Query tests | SPARQL in `qa/` | CQ-1 to CQ-14; CAP-18 positive and negative cases |
| F Semantic review | Human | G1-T and G1-I records; CAP-04, CAP-06, CAP-07, CAP-09, CAP-10, CAP-25, CAP-30 |

C-A catches what D2 cannot: where an `only` restriction exists, a reasoner classifies a misasserted act into the permitted type, so the check must see asserted types only.

**D2 at release.** D2 runs at release rather than on every commit. On an ordinary commit an absent DL reasoner gives SKIP, as Gates B and D do. At a release or acceptance checkpoint it is FAIL.

## 9. Migration of existing capability work

The BPO already holds four capability classes in slice 1.0, about 40 scoped capability names in `capabilities/`, an agent manifest, and one authorization class affected by R4. Nothing is re-created; each item is refactored in place.

| Item | Current state | Change | Rule |
| --- | --- | --- | --- |
| `ex:StrategicPlanningCapability` | Under `cco:ont00000568`; scoped to 6 processes | Generate its `ex:enablesProcess` index from the scope file; run G1-T. No `only` without a CAP-30 review | CD3, CD4 |
| `ex:BusinessModelGovernanceCapability` | Under `cco:ont00000568`; comment cites "maintain" (1.4.2) and "establish governance" (1.4.3); absent from the scope file | Add a scope entry indexing the maintain acts; index 1.4.3 only with a CD5 justification | CD5 |
| `ex:CustomerExperienceManagementCapability` | Under `cco:ont00000568`; scoped to 4 processes; definition says "design and improve" | Review each index member under CD5 before G1-T | CD5 |
| `ex:CompetitiveAnalysisCapability` — bearer | Under `cco:ont00001379`; borne by an analyst Agent | Re-home under `cco:ont00000089` Skill in the BPO if the bearer is a person; out of BCO scope | CD1 |
| `ex:CompetitiveAnalysisCapability` — restriction | `some` realization of `ex:P19945` | Separate BPO decision. Recommended: drop `some`; index `ex:P19945`; add `only` only after review | CD4, CD8 (by analogy) |
| Other `capability_scope.json` names (Procurement, Treasury Management and others) | Declarations not located in slice 1.0 | Audit each against CAP-01 to CAP-03, then G1-T | CAP-13 |
| Overlapping scopes | Supply Chain Management, Human Capital Management and Financial Management each cover narrower capabilities' processes | Record the narrower capabilities as components in `coverage_register.json`; assert subclass links only after CAP-10 review | CD9, CD16 |
| `capabilities/capability_scope.json` | Capability → processes | Unchanged in structure; now the source of the mandatory index | CD12 |
| `capabilities/coverage_register.json` *(new)* | — | Create, keyed by APQC catalog concept (`ex:PCF_<id>`) of each standing function | CD16, CAP-22 |
| `capabilities/agents.json` | Software agents listed against Organization Capability classes | Retype as a description-layer manifest using `ex:concernsType`; check consumers first (OI-10) | CD13, CD14 |
| BPO `ex:BusinessAuthorization` *(new, R4-05)* | Slice 1.0 declares it under `cco:ont00000751`, as output of 1.4.1.2 | BPO-side decision: retype as an Authorization Record, or keep it under the occurred-act convention of CAP-28 | OI-16 |
| v0.2 `ex:concernsCapabilityType` | Specified, never implemented | Implement as `ex:concernsType` only | CD14 |
| Generated `enablesProcess` / `requiresCapability` | Generated from the scope file | Keep the first as the index; stop generating the second | CD12 |

**Order:** ratify RP-1 first, because it decides what every G1-T record argues. Then RP-2 and RP-3, which decide what the scope file generates. Then refactor the four slice-1.0 classes as the reference set, then the remaining scope entries section by section, following the daemon's per-section loop.

### 9.1 Reconciling the v0.1 `bc:` vocabulary

The reviewer's v0.1 package declares seven classes in `https://example.org/BusinessCapabilityOntology#`. Neither that namespace nor this one is published, so v0.4 uses a controlled rename recorded in a migration manifest, `docs/migration/bc-v0.1-to-v0.4.json`, with old IRI, new IRI, decision and definition change for each term. No `owl:equivalentClass` is asserted, because every term's definition changed (TM-5).

| v0.1 class (`bc:`) | v0.4 class (`ex:`) | Decision |
| --- | --- | --- |
| `BusinessCapability` | `BusinessCapability` | Rename; grounding definition revised (CD2) |
| `BusinessCapabilityDescription` | — | Not carried. Type-level meaning lives in class definitions and catalog nodes (TM-1, OI-17) |
| `BusinessCapabilityMap` | `CapabilityMap` | Rename; entries constrained to assessments and targets |
| `BusinessCapabilityAssessment` | `CapabilityAssessment` | Rename; narrowed to possession findings with a mandatory finding |
| `BusinessCapabilityMaturityAssessment` | `CapabilityAssessment` + `CapabilityMaturityRating` | Split: the evaluation is an assessment; the ordinal result is a rating citing it (TM-4) |
| `BusinessCapabilitySourcingAssessment` | `CapabilitySourcingAssessment` | Rename; now about a sourcing statement, which is a separate v0.4 class (TM-2) |
| `BusinessCapabilityTargetStateSpecification` | `CapabilityTargetStateSpecification` | Rename; parent moves from `cco:ont00000965` to `cco:ont00000974` Plan; the end state it serves is a separate `CapabilityTarget` (TM-3) |

The v0.1 target-state class also covered obtaining access to external capacity. That scope survives: a v0.4 Target-State Specification may prescribe a sourcing arrangement as one of its acts.

## 10. Ratification, open issues and acceptance

Ten decisions need ratification before any requirement is promoted. RP-1 is the one to settle first: every G1-T record argues from it. RP-9 and RP-10 are new in v0.4 and have not been reviewed.

**Ratification register**

| ID | Decision | v0.4 proposal | R4 position | Status |
| --- | --- | --- | --- | --- |
| RP-1 | Grounding boundary (CD1, CD2) | The organization alone bears the disposition; its basis is its member agents; owned or controlled artifacts are enabling conditions; a system bearer is tracked as OI-14 | Revise | Revised |
| RP-2 | Realization index (CD4) | Mandatory `ex:enablesProcess` index; `only` optional with an exhaustiveness review; CAP-21 against the index | Revise | Revised |
| RP-3 | Enablement relations (CD12) | `enablesProcess` an annotation with no causal entailment, now also the index; `requiresCapability` withdrawn | Approve | Unchanged in substance |
| RP-4 | Agent manifest (CD13) | Description-layer manifest; functions borne by the computing artifact | Approve in principle | Consumers to be checked (OI-10) |
| RP-5 | Namespace | Mint a permanent namespace before release; `ex:` is `http://example.org/apqc#` | Approve | Unchanged |
| RP-6 | Type references (CD14) | `ex:concernsType`; map entries; a mandatory finding on every assessment; `partial` cites its criteria | Approve with correction | Corrected |
| RP-7 | Closed-world evidence (CD15) | Authorization Records instead of prospective Action Permissions; JSON completeness manifest; typed validity dates | Revise | Revised |
| RP-8 | Functional coverage (CD16) | Component possession only; register keyed by APQC catalog concept in its own file; integration assessed, never derived | Revise | Revised |
| RP-9 | Information-layer vocabulary (CD17) | Seven description classes; sourcing assessment and target-state specification kept distinct; no capability description ICE | — (new) | New, unreviewed |
| RP-10 | Admission vs attribution (CD3) | G1-T for classes, G1-I for each bearing claim, recorded as a supporting assessment | Proposed by R4 | New, unreviewed |

**Open issues**

- **OI-1** Pin BFO, CCO and the BPO slices by content hash before any executable release. This also settles the 2024-11-05 / 2024-11-06 discrepancy.
- **OI-4** No relation yet links a development act to the capability it brings about. CQ-11 is answered by review records until one is chosen.
- **OI-6** Locate the declarations of `enablesProcess` and `requiresCapability`; they are not in `apqc-ext.ttl` or slice 1.0.
- **OI-7** The staging state (CD3) sits outside BFO's role/disposition split. It must stay transitional and is counted by CQ-10.
- **OI-8** Verify against the pinned closure the CCO IRIs taken from reviews: `cco:ont00001889`, `cco:ont00001898`, `cco:ont00001982`, `cco:ont00001010`, `cco:ont00001811`, `cco:ont00001942`, `cco:ont00001910`, `cco:ont00000974` and `cco:ont00000506`. Choose the CCO value data property that carries a rating's ordinal value.
- **OI-9** An earlier review reported an existential realization of `ex:P20955` on the governance capability. The current slice 1.0 text has no such restriction; confirm whether it lives in another module.
- **OI-10** Changing `agents.json` may affect whatever consumes it for routing. Check consumers before RP-4 lands.
- **OI-11** *(narrowed)* The manifest schema is fixed in CD15. Still open: the evidence-graph IRIs, and whether the manifest reuses the closed-world rule form of the house specification standard.
- **OI-12** *(closed in v0.4)* Validity uses `schema:validFrom` and `schema:validThrough` typed `xsd:date`.
- **OI-13** Fix the schema and versioning of `coverage_register.json`, including whether a function's components may themselves be functions.
- **OI-14** *(new)* A socio-technical system bearer, a material entity whose parts include both members and artifacts, would let capability loss track platform loss. Decide whether any capability class needs it before artifact-heavy capabilities pass G1-T.
- **OI-15** *(new)* An integrated-adequacy assessment of a function with no capability class of its own has no K1 class to concern. Decide whether it concerns the catalog concept instead.
- **OI-16** *(new, BPO-side)* `ex:BusinessAuthorization ⊑ cco:ont00000751` in slice 1.0 entails a permitted process for every business authorization the BPO records.
- **OI-17** *(new)* If capability dictionaries must travel as versioned information artifacts, revisit TM-1.
- **OI-18** *(new)* Multi-party sourcing (brokers, intermediaries, provider networks) is outside the two-party record.
- **OI-19** *(new)* Confirm that the CCO Plan pattern treats a plan's objectives as continuant parts, which CAP-31 assumes.

**Known limits (0.4)**

- A capability persists when an enabling artifact is lost; the loss shows only as unavailability in an assessment (CD2).
- No temporal qualification of has capability. CQ-4 asks about capabilities borne at query time.
- No capability parthood. Overlap is handled by reviewed specialization and the coverage register.
- No degrees of capability in the reality layer; maturity lives in ratings of existing instances.
- Type references, the sourcing convention and the realization index are annotations or conventions, so a reasoner draws nothing from them. SHACL is their only enforcement.
- Absence answers are only as good as the manifests behind them.

**Acceptance checkpoints**

- [ ] CP-0 RP-1 to RP-10 ratified; ADR-002 accepted.
- [ ] CP-1 Four slice-1.0 classes refactored with their index. Every fixture checked by Gates B, C, C-A and M fails as stated, including CAP-21 and CAP-25 to CAP-31. Gates A–D green.
- [ ] CP-2 Gate D2 has run, an absent reasoner counted as FAIL, and the CAP-10 and CAP-16 fixtures fail as stated. CQ-1 to CQ-14 answered over a fixture organization, with CAP-18's positive and negative cases.
- [ ] CP-3 Every scope entry audited, with a G1-T record or an explicit staging status; `coverage_register.json` populated; the `bc:` migration manifest complete.

## Sources

- [BusinessProcessOntology README](https://github.com/Skreen5hot/BusinessProcessOntology)
- [ADR-001 Category and upper-level modeling](https://github.com/Skreen5hot/BusinessProcessOntology/blob/main/docs/adr/ADR-001-category-and-upper-level-modeling.md)
- [Slice 1.0 reality module](https://raw.githubusercontent.com/Skreen5hot/BusinessProcessOntology/main/ontology/slices/apqc_1_0.ttl)
- [Shared act genera apqc-ext.ttl](https://raw.githubusercontent.com/Skreen5hot/BusinessProcessOntology/main/ontology/apqc-ext.ttl)
- [capability\_scope.json](https://raw.githubusercontent.com/Skreen5hot/BusinessProcessOntology/main/capabilities/capability_scope.json) · [agents.json](https://raw.githubusercontent.com/Skreen5hot/BusinessProcessOntology/main/capabilities/agents.json) · [role\_anchors.json](https://raw.githubusercontent.com/Skreen5hot/BusinessProcessOntology/main/capabilities/role_anchors.json)

Reviews R2 (of v0.1.0-draft.1), R3 (of v0.2.0-draft.1) and R4 (of v0.3.0-draft.1), and the R4 reviewer's v0.1 term mapping, were supplied by the architect on 2026-10-22 and are not published; their findings are carried in §0.1 to §0.3.
