# Business Capability Ontology — Specification & Requirements

Oct 22, 2026 · @Aaron Damiano

| Field | Value |
| --- | --- |
| Title | Business Capability Ontology — Specification & Requirements |
| Type | Ontology specification and requirements; companion module to the Business Process Ontology |
| Version | 0.3.0-draft.1 (supersedes 0.2.0-draft.1) |
| Date | 2026-10-22 |
| Author | Aaron |
| Status | DRAFT — response to review R3; ADR-002 ratification pending RP-2, RP-6 and RP-7 |
| Domain | Enterprise architecture: organizational capabilities and their realization in business processes (BFO 2020 / CCO 2.0) |

## 0. Document control

This is a DRAFT for ratification. Nothing in it is normative until the architect ratifies it, and every requirement stays DRAFT until its falsifying fixture exists.

| Field | Value |
| --- | --- |
| Document ID | BPO-SPEC-CAP |
| Ratifying architect | Aaron |
| Decision record | Lands as ADR-002 "Organizational Capabilities and Their Realization"; folds into Methodology at next bump |
| Repository | [Skreen5hot/BusinessProcessOntology](https://github.com/Skreen5hot/BusinessProcessOntology) |
| Version history | 0.1.0-draft.1 → review R2 → 0.2.0-draft.1 → review R3 → 0.3.0-draft.1 |

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
| `ontology/apqc-cap.ttl` | `ex:BusinessCapability`, realization unions, all capability classes, moved out of the slices |
| `ontology/apqc-cap-desc.ttl` | The five description-layer classes |
| `ontology/apqc_shapes.ttl` | CAP shapes added beside the existing ones |
| `capabilities/capability_scope.json` | Kept as the source for realization unions (CD12), and extended with a `components` field as the coverage register (CD16) |
| `docs/adr/ADR-002-organizational-capabilities.md` | This spec's decisions, once ratified |

Moving capability classes out of the slices follows D9's single-source rule for shared terms. Slices that need them inline the declarations, as they already do for act genera.

## 3. Design decisions (CD1–CD16)

These sixteen commitments carry the design. Each is proposed, not ratified; those marked *revised* or *new* changed in v0.2 or v0.3, under the R2 or R3 finding named. They are numbered CD to avoid collision with methodology D1–D9 and ADR-001 R1–R7.

**CD1 — Bearer.** A Business Capability inheres in a `cco:ont00001180` Organization. Capabilities borne by a person are CCO Skill or Agent Capability and are out of this module's scope, except as contributors to an organization's basis (CD2).

**CD2 — Grounding basis** *(revised, R2-04, R2-05)*. The material basis of a Business Capability is the organization's operative configuration: its members in their organizational positions, the material artifacts it owns or has operational control of, and the arrangements among them.

- **Basis is not the conditions of realization.** Other organizations may take part in a realization without entering the basis. A retailer that coordinates deliveries through carriers can bear a logistics-coordination capability grounded in its own staff and systems; the carrier bears its own delivery capability.
- **The boundary is kept.** When the basis itself lies in another organization (the provider's staff do the work on the provider's systems), the consumer bears no capability for those acts. Its arrangement is recorded as a Capability Sourcing Statement. Internal capability and sourcing may coexist for the same acts.
- **Fragility is not reclassification.** A capability may depend on one indispensable member and still be organizational, provided its realization runs through organizational arrangements. Key-person dependency is recorded in a Capability Assessment; losing that member can end the disposition.
- **Ability, not assignment** *(v0.3, R3-06)*. The owns-or-controls rule bounds where the basis may lie; it is not evidence that a basis exists. An organization chart, an assigned responsibility, a governance charter or an authorization shows that the organization is responsible or permitted, not that it is materially able. G1 requires evidence of ability: members with the relevant skills in the positions concerned, the artifacts the acts need, or a recorded realization. A recorded realization is sufficient but not required, which keeps CD8 intact.
- **Ratification item RP-1** (refined in v0.3).

**CD3 — Disposition admissibility.** A capability class may be asserted `rdfs:subClassOf obo:BFO_0000016` (Disposition) only after it passes the grounding test G1 (§8). Until then it stays under `cco:ont00000568` alone.

- That unasserted state is a staging state, not a final category. BFO 2020 divides realizables into dispositions and roles, so a class that fails G1 must be reclassified (as a role, an assessment ICE, or deleted), never left neutral.

**CD4 — Realization constraint** *(revised, R2-01, R2-02)*. Each capability class carries one necessary condition on its realizations: `obo:BFO_0000054 only <RealizationType>`. This limits what can count as an exercise of the capability. It does not define the capability.

- **Classes are primitive.** A capability's identity is its bearer kind (CD1), its grounding (CD2) and its realization type together. The textual definition states all three; G1 reviews the first two. No equivalence axiom is claimed.
- **The realization type** *(v0.3, R3-04)* is, in order of preference, a BPO reality-layer act class or a D9 genus used directly, or a named union of such classes (`ex:<Name>Realization`) declared in the capability module. A union is minted only where a capability admits more than one act class. It means each realization is one of the member types, not that the bearer can perform all of them.
- **Coverage is not here.** Whether an organization can carry out a whole business function is functional coverage (CD16), not a property of any one capability's realization type.
- **Non-deontic indexing.** The realization type must be describable without deontic success conditions. Where a BPO act is institutional (success depends on standing, such as submitting to a regulator), the capability indexes to the non-deontic act it contains. Standing is a role or `cco:ont00000751` Action Permission.

**CD5 — Development and realization** *(revised, R2-09)*. Developing capability C and realizing C are different relations an act can stand in. An act counts as a realization of C only when it is justified as an exercise of C. That the act brings C about or improves it is not that justification.

- One act may do both: practice that exercises a capability can also strengthen it.
- An act may develop C while realizing a different capability, as when change management builds a new governance capability.
- Example: "Maintain business models" realizes business model governance capability. "Establish business model governance" develops it, and realizes it only if it is separately justified as an exercise.

**CD6 — Overlap with Function.** Business Capability is not declared disjoint from BFO Function. Its differentia is individuation by bearer, grounding and realization type, whether or not the organization was designed to have it. No capability class is asserted to be a Function.

**CD7 — Capability is not role or permission.** No capability definition may mention assignment, responsibility, authorization, license or mandate. "Able but not authorized" and "authorized but not able" must both be representable without contradiction.

**CD8 — No latency exclusion.** No capability class carries an existential realization axiom. A capability that has never been exercised is admissible.

**CD9 — Primitive classes, reviewed taxonomy** *(revised, R2-01, R2-08, R3-01)*. Capability classes are primitive OWL classes, and `rdfs:subClassOf` between them means specialization only.

- **A parent means any ability within its function.** Every accounting capability is a financial-management capability of some kind. A parent capability does not mean complete ability to carry out the function, and bearing a subclass instance says nothing about bearing its siblings.
- **Links are reviewed, not mirrored.** When one capability's realization type is entailed under another's, the pair is a candidate for a subclass link (CAP-10). It is asserted only after review confirms the two dispositions also agree in bearer kind and grounding.
- **Nothing is induced.** Neither the coverage register (CD16) nor APQC partonomy (`has process part`) generates subclass links.

**CD10 — Member-wise bearing is not organizational bearing** *(revised, R2-13)*. Organization-to-capability uses `cco:ont00001954` (has capability), with inverse `cco:ont00001889` (capability of). `cco:ont00001898` (aggregate has capability) says each member bears its own capability instance of the type, not that the aggregate bears one shared instance. It therefore never stands in for a Business Capability and is used only for member-wise claims.

**CD11 — Descriptions are about, not of** *(revised, R2-12, R3-07)*. Description-layer ICEs relate to organizations and capability instances by `cco:ont00001808` (is about) or its CCO subproperties: `cco:ont00001982` (describes) for maps, assessments and sourcing statements, and `cco:ont00001811` (is a ordinal measurement of) for maturity ratings. Directive ICEs may use `cco:ont00001942` (prescribes). A capability listed in a map is not thereby asserted to exist. Catalog nodes reach capability classes through the ADR-001 R4 bridge, `ex:designatesProcessType`.

- **Sourcing convention.** A Capability Sourcing Statement `describes` exactly one organization, the consumer. Every other organization it is about is a provider. It carries exactly one `ex:concernsType`, naming the act class sourced. Where the parties bear `cco:ont00000506` Contractor Role or `ex:CustomerRole`, those roles corroborate the structure; they do not define it (CAP-23).

**CD12 — The generated enablement relations are bridges, not axioms.** `capabilities/capability_scope.json` drives generated `enablesProcess` and derived `requiresCapability` relations. Their declarations are not in `apqc-ext.ttl` or slice 1.0, so their OWL status is unverified (OI-6).

- `enablesProcess` (capability class → act class) means that act class is a member of the capability's realization union (CD4). It is an annotation with no causal or modal entailment.
- `requiresCapability` is withdrawn from generation. Read as stated, it would say every act of a type needs an organization bearing the capability, which is false whenever a contractor or a single person performs it.
- Each scope entry is checked against CD5 before it enters a union.

**CD13 — Agent manifests describe; they do not bear** *(revised, R2-11)*. `capabilities/agents.json` lists software agents (for example `agent.strategy_lead.v1`) against Organization Capability classes. No software agent bears an Organization Capability (CD1).

- Software is information content, not a material entity, so it bears no BFO realizable. Any artifact function belongs to the deployed computing artifact that executes the software.
- The manifest is an ICE that designates the capability types an agent serves (CD14). It keeps its routing use.
- When the organization operates that computing artifact, the artifact and its function are part of the organization's material basis (CD2).

**CD14 — Type references** *(new in v0.2, R2-06; generalized in v0.3, R3-02, R3-03)*. An ICE that concerns a class rather than an instance carries the annotation `ex:concernsType`, whose value is the class IRI. The class may be a capability class (absent, prospective or sourced capabilities) or an act class (sourcing statements and permission records). It replaces v0.2's `ex:concernsCapabilityType`.

- **Maps carry entries, not types.** A Capability Map has its entries as continuant parts (`obo:BFO_0000178`). Each entry is a Capability Assessment (the type is present, absent or partial) or a Capability Target (the type is needed), and carries exactly one `ex:concernsType`. The map itself carries none.
- **Assessments state their finding.** An assessment without an instance link records its result with the annotation `ex:assessedPresence`, valued `present`, `absent` or `partial`.
- When a capability instance exists, the ICE also relates to it through CD11's relations. The annotation then identifies the type; the object property identifies the instance.
- Rejected: **punning** (the punned individual is not tied to the class's extension, so queries over it mislead), and **per-type designator individuals** (a third registry beside the catalog and the class list).
- The pattern mirrors `ex:designatesProcessType`, which ADR-001 R4 already uses to point an individual at a class. It adds no object property and stays in OWL 2 DL.

**CD15 — Closed-world declarations** *(new in v0.2, R2-07; completed in v0.3, R3-03)*. OWL reasoning stays open-world. Competency questions about absence are evaluated over named evidence graphs whose completeness is declared for a stated scope.

- **Two evidence graphs.** The realization log records acts and the capabilities they realize. The permission register records Action Permissions (`cco:ont00000751`).
- **A permission record names its scope.** Each is about the acting agent (`cco:ont00001808`), carries one `ex:concernsType` naming the act class it permits, and states its validity period with `dct:valid`. When the permitted act has occurred, the record also `permits` it (`cco:ont00001910`). Authorization for one act class says nothing about another, even under the same capability.
- **A completeness declaration names what it covers.** It is a Descriptive ICE that identifies the graph and states the organization, the acting agents, the period (`dct:valid`) and the authority sources consulted (`dct:source`). The graph is complete only for that scope. An internal register declared complete does not cover authorizations held only by an external authority unless that authority is a listed source.
- **Answers are bounded.** An answer reads "no recorded authorization within the declared scope", never "not authorized". Outside any declaration, an absence question returns *unknown*.

**CD16 — Functional coverage** *(new, R3-01)*. Coverage of a standing business function is a separate structure from capability specialization (CD9) and from recorded performance (CD15).

- **The coverage register** is the `components` field added to `capability_scope.json`. For each standing function it lists the capability classes the function requires.
- **Coverage is a query.** Organization O covers function F when O bears an instance of every component listed for F (CQ-12). The answer is about what O bears, not about what it has performed.
- **No generated axioms.** Listing a component does not make it a subclass of the function's capability, and a function's capability class need not exist. Where one does, it keeps CD9's broad reading.

## 4. Terms

The module mints five kinds of term: the generic parent `ex:BusinessCapability`; the specific capability classes; a named realization union only where a capability admits more than one act class; five description-layer classes; and two annotation properties. Everything else is reused. Each term lists what it does not imply, because that is where misuse starts.

**Reality layer**

| Term | Definition | Parents | Does not imply |
| --- | --- | --- | --- |
| Business Capability `ex:BusinessCapability` | An Organization Capability that is a Disposition inhering in an Organization in virtue of the organized material capacities of its members and of the material artifacts it owns or has operational control of, and that, when realized, is realized in Planned Acts of a specified type. | `cco:ont00000568`, `obo:BFO_0000016` | That it has ever been realized. That the organization is authorized to exercise it. That any one member bears it. That it was designed (Function). That no other organization takes part in its realizations. That an assigned responsibility establishes it. |
| Specific capability classes (`ex:StrategicPlanningCapability` and the rest) | Each states its bearer kind, its grounding and its realization type in its definition (CD4). | `ex:BusinessCapability` after G1; `cco:ont00000568` alone before (CD3) | That the class is OWL-defined. That a parent means complete ability to carry out its function (CD9). |
| Realization union `ex:<Name>Realization` | A Planned Act class defined as the union of the BPO act classes whose instances are the only admissible realizations of a given capability class. Minted only when there is more than one such class. | `cco:ont00000228` | That every instance realizes this organization's capability. That the bearer can perform every member type (CD4). |

**Description layer**

| Term | Definition | Parent | Does not imply |
| --- | --- | --- | --- |
| Capability Map `ex:CapabilityMap` | A Descriptive ICE that describes an organization and has, as continuant parts, the Capability Assessments and Capability Targets that are its entries. | `cco:ont00000853` | That any listed capability exists. That the arrangement of entries is parthood among capabilities. |
| Capability Assessment `ex:CapabilityAssessment` | A Descriptive ICE that describes an organization with respect to the presence, absence or partial presence of a capability of one given type, on stated evidence. | `cco:ont00000853` | That the assessment is true. That an instance exists (an absent capability is referenced by type). |
| Capability Maturity Rating `ex:CapabilityMaturityRating` | An Ordinal Measurement ICE that ranks an existing Organization Capability instance relative to a specified ordinal assessment scale, and records its ordinal value, the scale and its provenance. | `cco:ont00001010` | Graded capability subclasses. Any particular scale or scoring method. Use for an absent or prospective capability; that is an assessment. |
| Capability Sourcing Statement `ex:CapabilitySourcingStatement` | A Descriptive ICE that describes an Organization's arrangement for obtaining performances of one specified Planned Act class from another Organization. | `cco:ont00000853` | That the consumer lacks an internal capability for the same acts. That the consumer bears the provider's capability. |
| Capability Target `ex:CapabilityTarget` | An Objective that prescribes that an organization come to bear a capability of one given type. | `cco:ont00000476` | That the capability is absent now. |

**Annotation properties**

| Term | Use | Value |
| --- | --- | --- |
| `ex:concernsType` | Identifies the capability class or act class an ICE concerns (CD14). Replaces v0.2's `ex:concernsCapabilityType` | A capability class IRI or an act class IRI |
| `ex:assessedPresence` | Records the finding of a Capability Assessment that has no instance link (CD14) | `present`, `absent` or `partial` |

**Reused without change:** `cco:ont00001180` Organization · `cco:ont00000568` Organization Capability · `cco:ont00001379` Agent Capability · `cco:ont00000089` Skill · `cco:ont00000751` Action Permission · `cco:ont00001010` Ordinal Measurement ICE · BPO `ex:InternalCapabilityData`, `ex:CoreCompetencyAnalysis`, `ex:RequiredCapabilityList`.

## 5. Relations and core pattern

The module mints no object property. It uses existing CCO, BFO and Dublin Core terms plus four annotation properties. R2 and R3 verified the CCO IRIs below against the supplied files; Gate B re-checks them against the pinned closure (OI-8).

| Relation | IRI | Use in BCO | Constraint |
| --- | --- | --- | --- |
| has capability / capability of | `cco:ont00001954` / `cco:ont00001889` | Organization ↔ its Business Capability | Default bearer link (CD10) |
| aggregate has capability | `cco:ont00001898` | Member-wise claims only | Never for a Business Capability (CD10) |
| has realization / realizes | `obo:BFO_0000054` / `obo:BFO_0000055` | Capability ↔ act instance | Class level: `only`, never `some` (CD4, CD8); instance level checked by CAP-21 |
| has continuant part | `obo:BFO_0000178` | Capability Map → its entries | CD14 |
| is about | `cco:ont00001808` | ICE → organization or agent | Or a subproperty below (CD11) |
| describes | `cco:ont00001982` | Map, assessment or sourcing statement → organization | Sourcing: exactly one target, the consumer (CD11) |
| is a ordinal measurement of | `cco:ont00001811` | Maturity rating → capability instance | Instance must exist |
| ordinal measurement annotation | `cco:ont00001739` | Maturity rating → its ordinal value | CAP-20 |
| prescribes | `cco:ont00001942` | Directive ICE → entity it prescribes | — |
| permits | `cco:ont00001910` | Action Permission → an act that occurred | Instance level only (CD15) |
| valid / source / conforms to | `dct:valid` / `dct:source` / `dct:conformsTo` | Validity period; evidence and authority sources; rating scale | CD15, CAP-20 |
| designates process type | `ex:designatesProcessType` (annotation) | Catalog node → capability class | ADR-001 R4, unchanged |
| enables process | `ex:enablesProcess` (annotation) | Capability class → member of its realization type | CD12 |
| concerns type | `ex:concernsType` (annotation) | ICE → capability class or act class | CD14 |
| assessed presence | `ex:assessedPresence` (annotation) | Assessment → its finding | CD14 |

**Class pattern** (scope taken from `capability_scope.json`). The restriction is a necessary condition only; the class is primitive.

```turtle
ex:StrategicPlanningRealization a owl:Class ;
    rdfs:subClassOf cco:ont00000228 ;
    owl:equivalentClass [ a owl:Class ; owl:unionOf (
        ex:P10037 ex:P10045 ex:P10039 ex:P10043 ex:P10020 ex:P19949 ) ] .

ex:StrategicPlanningCapability a owl:Class ;
    rdfs:subClassOf ex:BusinessCapability ,          # only after G1 passes
        [ a owl:Restriction ;
          owl:onProperty obo:BFO_0000054 ;           # has realization
          owl:allValuesFrom ex:StrategicPlanningRealization ] .   # necessary, not sufficient
```

**Instance pattern 1 — able, exercised once.** Authorization is deliberately absent: it attaches to acts through the permission register (CD15), never to the capability. v0.1 labelled this example "separately authorized" without showing it; that label is withdrawn.

```turtle
ex:acme a cco:ont00001180 ;                          # Organization
    cco:ont00001954 ex:acme_spc .                    # has capability
ex:acme_spc a ex:StrategicPlanningCapability .
ex:acme_2027_mission a ex:P10037 ;                   # asserted type, checked by CAP-21
    obo:BFO_0000055 ex:acme_spc .                    # realizes
ex:acme_spc_rating a ex:CapabilityMaturityRating ;
    cco:ont00001811 ex:acme_spc ;                    # is a ordinal measurement of
    cco:ont00001739 "3" ;                            # ordinal value
    dct:conformsTo ex:house_maturity_scale ;
    dct:source ex:acme_2027_review .
```

**Instance pattern 2 — a map with entries, one present and one absent (CD14).**

```turtle
ex:acme_map a ex:CapabilityMap ;
    cco:ont00001982 ex:acme ;                        # describes the organization
    obo:BFO_0000178 ex:acme_map_e1 , ex:acme_map_e2 .  # has continuant part
ex:acme_map_e1 a ex:CapabilityAssessment ;
    cco:ont00001982 ex:acme_spc ;                    # instance exists
    ex:concernsType ex:StrategicPlanningCapability .
ex:acme_map_e2 a ex:CapabilityAssessment ;
    cco:ont00001982 ex:acme ;
    ex:concernsType ex:TreasuryManagementCapability ;
    ex:assessedPresence "absent" .
```

**Instance pattern 3 — a sourcing statement (CD11).** The single `describes` target is the consumer; the other organization it is about is the provider.

```turtle
ex:acme_payroll_sourcing a ex:CapabilitySourcingStatement ;
    cco:ont00001982 ex:acme ;                        # consumer
    cco:ont00001808 ex:payco ;                       # provider
    ex:concernsType ex:ActOfRemuneration .           # act class sourced
ex:payco obo:BFO_0000196 ex:payco_contractor_role .  # corroborating role
ex:payco_contractor_role a cco:ont00000506 .         # Contractor Role
```

**Instance pattern 4 — a permission record and its completeness declaration (CD15).**

```turtle
ex:acme_filing_permit a cco:ont00000751 ;            # Action Permission
    cco:ont00001808 ex:acme ;                        # acting agent
    ex:concernsType ex:ActOfReporting ;              # act class permitted
    dct:valid "start=2026-01-01; end=2026-12-31" .
ex:acme_permits_2026 a cco:ont00000853 ;             # completeness declaration
    cco:ont00001808 ex:graph_acme_permissions ;
    dct:valid "start=2026-01-01; end=2026-12-31" ;
    dct:source ex:internal_register , ex:state_regulator_portal .
```

**Reasoner profile.** `owl:allValuesFrom` and `owl:unionOf` are outside OWL 2 EL, so Gate D (ELK) ignores them. Gate D2 checks them with a DL reasoner and blocks a release if it cannot run (§8).

## 6. Requirements

Twenty-three live requirements and one retired, all DRAFT. IDs are stable across versions; CAP-21 to CAP-24 are new in v0.3. Each names the fixture that must make it fail; a requirement is promoted only when that fixture exists in the bad-examples set and fails as stated. FAIL blocks a build; WARN goes to `qa/queries/warn` for review.

**Class kinds.** Several requirements apply to one kind only. Each class in the capability module is exactly one of:

- **K1 capability class:** under `cco:ont00000568`. `ex:BusinessCapability` itself is the K1 parent and is exempt from CAP-03.
- **K2 realization union** *(narrowed in v0.3)*: a union class declared in the module, under `cco:ont00000228`, used as some K1 class's filler. A BPO act class used directly as a filler is not a module class and is not K2.
- **K3 description class:** an ICE class declared in `apqc-cap-desc.ttl`.

| ID | Requirement | Falsifying fixture | Level · Gate | Traces |
| --- | --- | --- | --- | --- |
| CAP-01 | Every class in the capability module is exactly one of K1, K2 or K3. | A class under none; a K2 union no K1 class uses | FAIL · C | CD1, R2-03 |
| CAP-02 | No K1 class has a `some` restriction on `obo:BFO_0000054`. | `ex:BadCap ⊑ BFO_0000054 some ex:P10037` | FAIL · C | CD8 |
| CAP-03 *(rev. v0.3)* | Every K1 class except the parent has exactly one `only` restriction on `obo:BFO_0000054`. Its filler is a reality-layer act class, a D9 genus, or a K2 union. | A K1 class with none; one with two; a filler that is `ex:CapabilityMap` | FAIL · C | CD4, R3-04 |
| CAP-04 *(rev. v0.3)* | A K1 class asserted under `obo:BFO_0000016` or `ex:BusinessCapability` carries a G1 record (PASS, reviewer, date) citing at least one ability-evidence item that is not a responsibility, governance or authorization document. | A PASS record citing only an organization chart | FAIL · C, F | CD2, CD3, R3-06 |
| CAP-05 | Every member of a K2 union is a reality-layer act class or a D9 genus, never a catalog node. | Union containing `ex:PCF_17040` | FAIL · B, C | CD4, R7 |
| CAP-06 | A realization-type member that is or falls under `ex:ActOfDevelopment`, `ex:ActOfImprovement`, `ex:ActOfOrganizationalEstablishment` or `ex:ActOfAcquisition` needs a review record saying why it exercises the capability. | Governance capability with an improvement act and no record | WARN · C, F | CD5, R2-09 |
| CAP-07 | A K1 definition contains no deontic terms (authoriz-, licen-, mandat-, responsib-, assign-, permit-). | Definition "capacity to fulfill its regulatory mandate" | WARN · C | CD7 |
| CAP-08 | The subject of `cco:ont00001954` with a K1 object is a `cco:ont00001180` Organization. | `agent.strategy_lead.v1` has capability `ex:acme_spc` | FAIL · C | CD1, CD13 |
| CAP-09 | No K1 class is asserted under, or disjoint from, `obo:BFO_0000034` Function. | Either assertion | FAIL · C | CD6 |
| CAP-10 | Each pair of K1 classes whose realization types are entailed one under the other is listed as a candidate, and stays WARN until reviewed as asserted or rejected. | Procurement and Supply Chain Management with no review record | WARN · D2, F | CD9, R2-08 |
| CAP-11 | A K3 individual relates to an organization or capability only by `cco:ont00001808` or one of its subproperties, never by has capability or realizes. | A Capability Map that has capability | FAIL · C | CD11, R2-12 |
| CAP-12 | `cco:ont00001898` never has a K1 object. | Aggregate-has-capability to `ex:acme_spc` | FAIL · C | CD10 |
| CAP-13 | Every `capability_scope.json` key and listed process resolves to a declared class. | Key `ex:NoSuchCapability` | FAIL · B | CD12 |
| CAP-14 | No `ex:requiresCapability` triple is generated. | Any such triple in the build | FAIL · C | CD12 |
| CAP-15 | *Retired in v0.2.* Hybrid sourcing is normal, not an exception. | — | — | R2-15 |
| CAP-16 | Every K1 class, every K2 union, every filler and every union member is satisfiable under a DL reasoner, and the module is consistent. Accepted at CP-2. | `ex:P10037` declared disjoint from its own parent, leaving the capability satisfiable | FAIL · D2 | CD4, R2-10, R3-09 |
| CAP-17 *(rev. v0.3)* | Every Capability Assessment, Capability Target and Capability Sourcing Statement carries exactly one `ex:concernsType`: a K1 class for assessments and targets, an act class for sourcing statements. A Capability Map carries none, and has at least one entry via `obo:BFO_0000178`, each an assessment or a target. An assessment with no instance link carries one `ex:assessedPresence`. | A map with two type annotations; an assessment with two; an absent-type assessment with no finding | FAIL · C | CD14, R3-02 |
| CAP-18 *(rev. v0.3)* | An absence query returns *unknown* unless a completeness declaration names the graph queried and covers, through `dct:valid` and its stated scope, the organization, acting agent and period asked, with at least one `dct:source`. | A query for a period outside the declaration's `dct:valid` returns an empty set | FAIL · query | CD15, R3-03 |
| CAP-19 | No ICE is the bearer of any realizable entity. | A software ICE bearing an artifact function | FAIL · C | CD13, R2-11 |
| CAP-20 *(rev. v0.3)* | Every Capability Maturity Rating has `cco:ont00001811` to an existing K1 instance, exactly one ordinal value via `cco:ont00001739`, exactly one `dct:conformsTo` scale, and at least one `dct:source`. | A rating with no value; a rating with no scale | FAIL · C | §4, R3-08 |
| CAP-21 *(new)* | For every act that `realizes` a K1 instance, the act's asserted type falls under that capability's filler in the asserted class hierarchy. Checked on the asserted graph, before reasoning, so the `only` restriction cannot supply the type. | An act asserted only as `ex:P10729` (scoped to Accounting) realizing `ex:acme_spc`; it passes D2 by inference | FAIL · C (asserted graph) | CD4, R3-05 |
| CAP-22 *(new)* | Every `components` entry in the coverage register resolves to a K1 class, and no `rdfs:subClassOf` is generated from the register. | Component `ex:NoSuchCapability`; a build step emitting subclass links from components | FAIL · B, C | CD16, R3-01 |
| CAP-23 *(new)* | A Capability Sourcing Statement `describes` exactly one Organization (the consumer) and is about at least one other Organization (the provider). | Two `describes` targets; no provider | FAIL · C | CD11, R3-07 |
| CAP-24 *(new)* | Every Action Permission in the permission register is about exactly one agent, carries one `ex:concernsType` naming an act class, and has one `dct:valid`. | A permission whose type is a capability class; one with no `dct:valid` | FAIL · C | CD15, R3-03 |

## 7. Competency questions

The module is done when each question has a SPARQL query in `qa/` that returns the expected answer over a fixture organization. Questions marked ‡ ask about absence. They are answered only over a declared-complete evidence graph and return *unknown* otherwise (CD15, CAP-18).

| ID | Question | Answered by |
| --- | --- | --- |
| CQ-1 | Which capabilities does organization O bear? | `cco:ont00001954` from O |
| CQ-2 | Which BPO act types are admissible realizations of capability type C? | C's filler, or the members of its K2 union |
| CQ-3 | Which capabilities did this act instance realize? | `obo:BFO_0000055` from the act, filtered by CAP-21 |
| CQ-4 ‡ *(rev. v0.3)* | Which capabilities that O bears at query time have no recorded realization in period P, within the declared-complete realization log? | Realization log graph and its declaration for O and P |
| CQ-5 ‡ *(rev. v0.3)* | Which admissible realization act types of O's capabilities lack an applicable authorization record for acting agent A and period P, within the declared-complete permission register? | Permission records' `ex:concernsType` and `dct:valid`, against CQ-2 for each of O's capabilities |
| CQ-6 *(rev. v0.3)* | Which capability types does O's map record as needed (a target entry) with no assessment entry finding them present? | Map entries joined on `ex:concernsType` and `ex:assessedPresence` |
| CQ-7 *(rev. v0.3)* | For which act types does O have a sourcing arrangement, with which provider, and for which of them does O also bear a capability whose realization type includes that act type? | Sourcing statements that `describe` O (CAP-23), joined to CQ-1 and CQ-2 |
| CQ-8 | Which capability targets does O have, and which already match a capability O bears? | Targets' `ex:concernsType` joined to CQ-1 |
| CQ-9 | Which APQC catalog nodes are standing functions with a capability class? | `ex:designatesProcessType` to a K1 class |
| CQ-10 | Which capability classes are still in the staging state? | K1 classes without a PASS G1 record |
| CQ-11 | Which acts develop capability C, as distinct from realizing it? | CAP-06 review records (no ontology relation yet, OI-4) |
| CQ-12 *(rev. v0.3)* | Does O cover standing function F, that is, bear an instance of every capability class listed for F? | Coverage register `components` for F, joined to CQ-1 (CD16) |

## 8. Validation

The BCO adds one human test (G1) and one reasoner gate (D2) to the existing BPO harness. Everything else extends gates that already run.

**G1 — the grounding test** *(revised, R2-04, R2-05)*. A capability class may be placed under Disposition only when a reviewer answers all seven questions as stated and records the answers against the class. Questions 3, 5 and 6 changed in v0.2; question 7 was added in v0.3 (R3-06).

1. **Bearer.** Is the bearer an Organization? (No → it is a Skill or Agent Capability.)
2. **Basis.** Can its material basis be named as members in positions, owned or controlled artifacts, and arrangements? The record lists them.
3. **Internal basis.** Does that basis lie within the organization, whoever else takes part in its realizations? (No → record a Capability Sourcing Statement instead.)
4. **Non-deontic.** Is its realization type describable without standing or authorization? (No → re-index to the non-deontic act it contains.)
5. **Organizational, not individual.** Do its realizations run through organizational arrangements (coordination across positions, or artifacts the organization controls) rather than one member's skill alone? (No → that member's Skill.) A key-person dependency still passes and is recorded in a Capability Assessment.
6. **Exercise, not development.** Is every member of its realization type justified as an exercise of it (CD5)? (No → remove the member or record the justification.)
7. **Ability, not assignment.** Does the record cite evidence that the organization is materially able to perform the acts: members with the relevant skills in the positions concerned, the artifacts the acts need, or a recorded realization? An organization chart, an assigned responsibility, a charter or an authorization is not such evidence. (No → staging state.)

**Gate changes**

| Gate | Existing tool | BCO addition |
| --- | --- | --- |
| A Syntax | rdflib | Capability module and fixtures parsed |
| B IRI resolution | rdflib + pinned CCO closure | CAP-05, CAP-13, CAP-22; scope file and coverage register resolve; CCO IRIs in §5 re-verified |
| C SHACL | pyshacl + `apqc_shapes.ttl` | CAP-01 to CAP-09, CAP-11, CAP-12, CAP-14, CAP-17, CAP-19, CAP-20, CAP-22 to CAP-24; ADR-001 shape (c) retained |
| C-A SHACL on the asserted graph (new) | pyshacl without `-a` inference, run before any reasoner | CAP-21 |
| D Reasoner | ELK via ROBOT | Unchanged; EL subset only |
| D2 DL reasoner | HermiT via ROBOT | CAP-10 candidates, CAP-16 |
| Query tests | SPARQL in `qa/` | CQ-1 to CQ-12; CAP-18 |
| F Semantic review | Human | G1 records; CAP-04 evidence; CAP-06, CAP-07, CAP-10 triage |

C-A is the gate that catches what D2 cannot: an `only` restriction lets a reasoner classify a misasserted act into the permitted type, so the check must see only asserted types.

**D2 at release** *(revised, R2-16)*. D2 runs at release rather than on every commit, so the per-commit loop keeps ELK's speed. On an ordinary commit an absent DL reasoner gives SKIP, as Gates B and D already do. At a release or acceptance checkpoint an absent reasoner is FAIL: a release is never marked validated without D2 having run.

## 9. Migration of existing capability work

The BPO already holds four capability classes in slice 1.0, about 40 scoped capability names in `capabilities/`, and an agent manifest. Nothing is re-created; each item is refactored in place.

| Item | Current state | Change | Rule |
| --- | --- | --- | --- |
| `ex:StrategicPlanningCapability` | Under `cco:ont00000568`; no realization axiom; scoped to 6 processes | Add a K2 union of the 6 and the `only` axiom; run G1 with ability evidence | CD3, CD4 |
| `ex:BusinessModelGovernanceCapability` | Under `cco:ont00000568`; no realization axiom; comment cites "maintain" (1.4.2) and "establish governance" (1.4.3); absent from the scope file | Index to the maintain acts; include 1.4.3 only with a CD5 justification; add a scope entry | CD5 |
| `ex:CustomerExperienceManagementCapability` | Under `cco:ont00000568`; scoped to 4 processes; definition says "design and improve" | Review each scope entry under CD5 before G1 | CD5 |
| `ex:CompetitiveAnalysisCapability` — bearer | Under `cco:ont00001379`; borne by an analyst Agent | Re-home under `cco:ont00000089` Skill in the BPO if the bearer is a person; out of BCO scope. Mint an organizational counterpart only if one is needed | CD1 |
| `ex:CompetitiveAnalysisCapability` — restriction | `some` realization of `ex:P19945` | Separate BPO decision, not implied by the re-homing. Recommended `only`, with the single act class as a direct filler | CD8 (by analogy), CD4 |
| Other `capability_scope.json` names (Procurement, Treasury Management and others) | Declarations not located in slice 1.0 | Audit each against CAP-01 to CAP-03, then G1 | CAP-13 |
| Overlapping scopes | Supply Chain Management covers the Planning, Procurement and Production processes; Human Capital Management covers Workforce Planning, Talent Acquisition and Workforce Deployment; Financial Management covers Accounting's two | Record the narrower capabilities as `components` of the broader function (CD16). Assert subclass links only where CAP-10 review confirms specialization | CD9, CD16 |
| `capability_scope.json` *(new in v0.3)* | Maps capability → processes only | Add a `components` field (function → capability classes) as the coverage register; the existing process lists are unchanged | CD16, CAP-22 |
| `capabilities/agents.json` | Software agents listed against Organization Capability classes | Retype as a description-layer manifest using `ex:concernsType`; no bearing assertions | CD13, CD14 |
| v0.2 `ex:concernsCapabilityType` | Specified in v0.2, not yet implemented | Implement as `ex:concernsType` only | CD14 |
| Generated `enablesProcess` / `requiresCapability` | Generated from the scope file; OWL status unverified | Keep the first as an annotation; stop generating the second | CD12 |

**Order:** ratify RP-1 and RP-3 first, because they decide what the scope file means. Then refactor the four slice-1.0 classes as the reference set, then the remaining scope entries section by section, following the daemon's existing per-section loop.

## 10. Ratification, open issues and acceptance

Eight decisions need ratification before any requirement is promoted. R3 recommended approving RP-1 and RP-3 to RP-5, and approving the principle of RP-2, RP-6 and RP-7 once their requirements were consistent; v0.3 supplies those requirements. RP-8 is new in v0.3 and has not been reviewed.

**Ratification register**

| ID | Decision | v0.3 proposal | R3 position | Status |
| --- | --- | --- | --- | --- |
| RP-1 | Grounding boundary (CD2) | Basis within what the organization owns or controls; ability evidence required (G1 Q7) | Approve with minor refinement | Refinement made |
| RP-2 | Realization constraint (CD4, CD9) | `only` as a necessary condition; direct act-class fillers; unions only where needed; CAP-21 on the asserted graph | Revise | Revised |
| RP-3 | Enablement relations (CD12) | `enablesProcess` an annotation with no causal entailment; `requiresCapability` withdrawn | Approve | Unchanged |
| RP-4 | Agent manifest (CD13) | Description-layer manifest; functions borne by the material computing artifact | Approve | Unchanged |
| RP-5 | Namespace | Mint a permanent namespace before release; `ex:` is `http://example.org/apqc#` | Approve | Unchanged |
| RP-6 | Type references (CD14) | One annotation `ex:concernsType`; maps carry entries; CAP-17 rewritten | Approve pattern, amend validation | Amended |
| RP-7 | Closed-world declarations (CD15) | Permission records name act type, agent and period; declarations state their scope and sources | Approve principle, amend implementation | Amended |
| RP-8 | Functional coverage (CD16) | Coverage register as a `components` field; coverage is a query; no generated axioms | — (new) | New, unreviewed |

**Open issues**

- **OI-1** Pin BFO, CCO and the BPO slices by content hash before any executable release. This also settles the 2024-11-05 / 2024-11-06 discrepancy.
- **OI-4** No relation yet links a development act to the capability it brings about. CQ-11 is answered by review records until one is chosen.
- **OI-6** Locate the declarations of `enablesProcess` and `requiresCapability`; they are not in `apqc-ext.ttl` or slice 1.0.
- **OI-7** The staging state (CD3) sits outside BFO's role/disposition split. It must stay transitional and is counted by CQ-10.
- **OI-8** Verify against the pinned closure the CCO IRIs taken from R2 and R3: `cco:ont00001889`, `cco:ont00001898`, `cco:ont00001982`, `cco:ont00001010`, `cco:ont00001811`, `cco:ont00001942`, `cco:ont00001739`, `cco:ont00001910`, and `cco:ont00000506`. For `cco:ont00001739`, confirm its property kind and range before CAP-20's shape is written.
- **OI-9** An earlier review reported an existential realization of `ex:P20955` on the governance capability. The current slice 1.0 text has no such restriction. Confirm whether it lives in another module or an older version.
- **OI-10** Changing `agents.json` may affect whatever consumes it for routing. Check consumers before RP-4 lands.
- **OI-11** *(narrowed in v0.3)* CD15 now fixes what a completeness declaration states. Still open: the IRIs of the two evidence graphs, and whether the declaration reuses the closed-world rule form of the house specification standard.
- **OI-12** *(new)* Choose one encoding for `dct:valid`: the DCMI Period string used in §5, or typed start and end dates.
- **OI-13** *(new)* Fix the schema and versioning of the `components` field, including whether a function's components may themselves be functions.

**Known limits (0.2)**

- No capability parthood. Overlap is handled by reviewed subclassing (CD9) and by the coverage register (CD16).
- No degrees of capability in the reality layer; maturity lives in ratings of existing instances.
- No temporal qualification of has capability. CQ-4 therefore asks about capabilities borne at query time, not those borne during the period P it examines.
- Type references (CD14) and the sourcing convention (CD11) are structural, so a reasoner draws nothing from them. SHACL (CAP-17, CAP-23) is their only enforcement.
- Absence answers are only as good as the completeness declarations behind them.

**Acceptance checkpoints**

- [ ] CP-0 RP-1 to RP-8 ratified; ADR-002 accepted.
- [ ] CP-1 Four slice-1.0 classes refactored. Every CAP fixture checked by Gates B, C and C-A fails as stated, including CAP-21. Gates A–D green.
- [ ] CP-2 Gate D2 has run, with an absent reasoner counted as FAIL, and the CAP-10 and CAP-16 fixtures fail as stated. CQ-1 to CQ-12 answered over a fixture organization, with declared-complete graphs for CQ-4 and CQ-5.
- [ ] CP-3 Every `capability_scope.json` entry audited, with a G1 record or an explicit staging status, and every standing function's `components` recorded.

## Sources

- [BusinessProcessOntology README](https://github.com/Skreen5hot/BusinessProcessOntology)
- [ADR-001 Category and upper-level modeling](https://github.com/Skreen5hot/BusinessProcessOntology/blob/main/docs/adr/ADR-001-category-and-upper-level-modeling.md)
- [Slice 1.0 reality module](https://raw.githubusercontent.com/Skreen5hot/BusinessProcessOntology/main/ontology/slices/apqc_1_0.ttl)
- [Shared act genera apqc-ext.ttl](https://raw.githubusercontent.com/Skreen5hot/BusinessProcessOntology/main/ontology/apqc-ext.ttl)
- [capability\_scope.json](https://raw.githubusercontent.com/Skreen5hot/BusinessProcessOntology/main/capabilities/capability_scope.json) · [agents.json](https://raw.githubusercontent.com/Skreen5hot/BusinessProcessOntology/main/capabilities/agents.json) · [role\_anchors.json](https://raw.githubusercontent.com/Skreen5hot/BusinessProcessOntology/main/capabilities/role_anchors.json)

Reviews R2 (of v0.1.0-draft.1) and R3 (of v0.2.0-draft.1) were supplied by the architect on 2026-10-22 and are not published; their findings are carried in §0.1 and §0.2.
