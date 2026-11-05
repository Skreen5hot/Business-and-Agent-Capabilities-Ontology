# Business Capability Ontology — Specification & Requirements

Oct 31, 2026 · Aaron Damiano

| Field | Value |
| --- | --- |
| Title | Business Capability Ontology — Specification & Requirements |
| Type | Ontology specification and requirements for the Business Capability module, built on the Business Process Ontology |
| Version | 0.5.0-draft.1 (supersedes 0.4.0-draft.1) |
| Date | 2026-10-31 |
| Author | Aaron Damiano; drafted by the BCO team (Claude Code, `claude-opus-5-5`) |
| Status | DRAFT under roadmap step D3. Not accepted for ratification. Nothing in it is normative until the architect ratifies it at CP-0 (D4) |
| Domain | Enterprise architecture: organizational capabilities and their realization in business processes (BFO 2020 / CCO 2.0) |

## 0. Document control

This is a DRAFT for review. Nothing in it is normative until the architect ratifies it,
and every requirement stays DRAFT until its falsifying fixture exists. v0.5 is prepared
under the architect's authorization of D3 (`docs/decisions/2026-10-31-d2-d3-authorized.md`)
and the approved roadmap (`docs/ROADMAP.md`, revision 2, sections 4 to 6).

| Field | Value |
| --- | --- |
| Document ID | BCO-SPEC |
| Ratifying architect | Aaron Damiano |
| Decision record | Lands as ADR-002 "Organizational Capabilities and Their Realization", under `docs/adr/`, once ratified |
| Repository | [Skreen5hot/Business-and-Agent-Capabilities-Ontology](https://github.com/Skreen5hot/Business-and-Agent-Capabilities-Ontology). Act types come from the [Business Process Ontology](https://github.com/Skreen5hot/BusinessProcessOntology) (BPO) |
| Version history | 0.1.0-draft.1 → R2 → 0.2.0-draft.1 → R3 → 0.3.0-draft.1 → R4 and v0.1 term mapping → 0.4.0-draft.1 → CM-01, DP-1, DP-2, R5, R8, R9 → 0.5.0-draft.1 |
| Conceptual baseline | CM-01, the Business Capability Conceptual Domain Model, approved 2026-10-26 (`src/02_conceptual_models/CM-01-business-capability.md`; `docs/decisions/2026-10-26-cm01-approved-r8-r9-accepted.md`; stakeholder-review erratum `docs/decisions/2026-10-30-cm01-stakeholder-review-erratum.md`). Where this specification and CM-01 differ in meaning, CM-01 governs, and the difference is a defect here |
| Prior vocabulary | The reviewer's v0.1 Turtle package (`bc:` namespace) is reconciled in §9.1 |

**Dependencies.** Each is pinned by commit and SHA-256 in `config/upstream-sources.yaml`,
and vendored as a partial extract under `vendor/`. Pinning every dependency by content hash
for an *executable release* is still OI-1.

| Dependency | Version | Role |
| --- | --- | --- |
| BFO 2020 | ISO/IEC 21838-2 (SRC-ISO-01) | Upper ontology |
| CCO | 2.0 (SRC-FO-01) | Mid-level. Supplies Agent Capability, Organization Capability, Skill, Action Permission and the measurement ICEs |
| BPO | The pinned commit in `config/upstream-sources.yaml` | Act types (the D9 genera of `apqc-ext.ttl` and the slices), the catalog bridge of ADR-001 R4 to R6, and `capability_scope.json` |

### Prefixes

v0.4 wrote `ex:` both for BPO's terms and for terms the BCO would mint. v0.5 corrects
that under the 2026-10-28 re-pin decision R3 (`docs/decisions/2026-10-28-i2-and-bpo-repin-decided.md`).
Every Turtle fragment here uses these bindings:

| Prefix | Namespace | Used for |
| --- | --- | --- |
| `bco:` | `https://fandaws.com/ontology/bco#` | Terms the BCO mints. Provisional until RP-5 fixes the permanent namespace (ADR-003 D1) |
| `ex:` | `https://fandaws.com/ontology/bpo#` | BPO's terms only: act types, catalog concepts, and BPO's annotations `ex:enablesProcess` and `ex:designatesProcessType`. A temporary binding, to be renamed `bpo:` in a reviewed update coordinated with CM-01. Never a BCO term |
| `cco:` | `https://www.commoncoreontologies.org/` | CCO |
| `obo:` | `http://purl.obolibrary.org/obo/` | BFO |
| `dct:`, `schema:` | Dublin Core terms; schema.org | Provenance and validity |
| `acme:` | `https://example.org/acme#` | Illustrative instance data in this document only. Never minted, published or loaded |

Every CCO and BFO identifier this specification writes is declared in the vendored
extracts. Two relations it needs are named by label only, because the extracts do not yet
carry them: BFO's *has member part* and BFO's *has participant*. Their IRIs are verified,
and the extract rebuilt, before any shape uses them (OI-8).

## 0.1 What v0.5 changes, and where

v0.5 carries the decisions taken since v0.4 into the specification text. Most of them were
taken through CM-01. It answers review R5 (§0.2) and reserves the place of the
domain-practitioner review (§0.3). The table names every decision and the sections it
changes, so that nothing is left uncarried.

| Decision or input | What it settled | Sections changed |
| --- | --- | --- |
| **DP-1** (RP-1), Option A with a1 to a4, 2026-10-25 (`docs/decisions/2026-10-25-dp1-rp1-grounding-boundary.md`) | The organization alone bears a business capability. Its basis is the relevant member agent or agents, one possibly sufficing, never an abstract set (a1). A basis is asserted only for an admitted type (a2). Constitution, configuration, enabling conditions and temporary constraints are kept apart (a3). A socio-technical bearer is kept open (a4). Permanently removing an essential platform does not by itself end a capability | CD1, CD2, §4 Business Capability, §5 has material basis, §8 G1-T question 2 and G1-I question 1, CAP-25, OI-14, RP-1 |
| **Bearer departures** (CM-01 Q-08; roadmap F-1) | The organization-only bearer is a narrowing every source family exceeds (SF-05). The departures are listed by source and clause | CD1 |
| **DP-2** (RP-10), Option A with b1, b3, b4, b5, b2 rejected, 2026-10-26 (`docs/decisions/2026-10-26-dp2-rp10-admission-attribution.md`) | Type admission (G1-T) and instance attribution (G1-I) are separate tests. G1-T question 3 asks about the organization's arrangements, which may involve one member (b1). Constant-membership cases are worked in every review (b3). A failing type is reclassified or removed, never left staged (b4). G1-I separates capacity from exercise (b5). No interest condition (b2 rejected; a departure from SF-04) | CD3, CD8, §8 G1-T and G1-I, CAP-04, CAP-26, CAP-32, OI-7, RP-10 |
| **R8 disposition**, accepted 2026-10-26, R8-07 qualified by R9 | Multiple classification (R8-05). Capacity distinguished from exercise (R8-06, through b5). The four aspects of functional coverage and adequacy (R8-07) | §4 specific capability classes, CD8, CD16 |
| **R9 disposition**, accepted in full 2026-10-26 | Functional Adequacy Assessment is a distinct category, with three findings, each met, partly met or not met against required criteria. A Standing Function designates a whole-function type only where one is defined, and that type is distinct from the component types. Enabling conditions are restricted to what is relevant to a capability's realization. CM-02 is planned | CD2, CD16, CD17, §4, CAP-22, CAP-33, CQ-9, CQ-12, OI-15, RP-8, RP-9 |
| **CM-01 approval guidance**, 2026-10-26 | Reuse BFO/CCO classes and relations. Never infer adequacy from component possession. Distinguish inadequate evidence from a finding of "not met". Availability depends on whether adequate alternatives exist. Evaluate the formal representation of Functional Adequacy Assessment before deciding whether a further class is needed. Resolve the BPO act-index dependencies before formal implementation | CD2, CD14, CD16, CD17, §3.1, §9, OI-20 |
| **CM-01 stakeholder-review erratum**, 2026-10-30 | CM-01's stakeholder-review gate was met by the architect's review of draft.5 as product owner, not by R8 and R9 | §0 Conceptual baseline (cited); no requirement changes |
| **CM-02 scope**, approved 2026-10-31 under D2 (`docs/decisions/2026-10-31-d2-cm02-scope-approved.md`) | The Agent Capability module's scope and boundary with this one. Artificial systems are in CM-02's scope as subject matter (S-1a) | §1 module boundary, CD1, CD13 |
| **Re-pin R3**, 2026-10-28 | `ex:` is a temporary binding for BPO's genera only, and a BCO term is never written with it | §0 Prefixes; every Turtle fragment; §4; §5 |
| **Roadmap AD-1 to AD-3**, 2026-10-30 | Business Capability is the first module. A practitioner review of CM-01 comes before CP-0. Terminology and taxonomy are reviewed per formalization tranche | §1, §0.3, §10 CP-0 |
| **Review R5** (`reviews/R5-v0.4-artifact-review.md`) | Sixteen findings on v0.4 against the v0.1 package and BPO | §0.2, and the sections its rows name |
| **Functional adequacy** (roadmap F-2; specification OI-15) | An adequacy statement about a function with no capability type of its own is directed at the Standing Function, as its own kind of statement | CD16, CD17, OI-15 |

Review dispositions R2 to R4, and the v0.1 term mapping, are in v0.4 §0.1 to §0.3. v0.5
does not repeat them, and they still stand as recorded there.

## 0.2 Review disposition (R5 → v0.5)

Review R5 compared v0.4 with the v0.1 artifact package and with BPO's public `main`. Its
recommendation was to keep the architecture and revise before ADR-002. v0.5 answers its 16
findings: 13 accepted as written and 3 accepted with an amended fix. None is rejected. **These
dispositions are proposed.** Accepting them is the architect's act, at the acceptance of
v0.5 for ratification.

| ID | Finding (R5 ref) | Disposition | v0.5 change |
| --- | --- | --- | --- |
| R5-01 | The member-agent-only basis is stronger than CCO's formal restrictions; CAP-25 rejects artifacts but requires no positive basis evidence | Accepted | CD2 states the basis rule as BCO's modeling policy under DP-1, not a CCO entailment. CAP-25 requires each basis object to be a named agent that is a member part of the bearer. G1-I question 1 must name candidate basis members or positions |
| R5-02 | CAP-20's ordinal value has no CCO-consistent encoding: the integer-value property R5 names (its identifier is not in the vendored extract, so it is not repeated here) is defined on an Information Bearing Entity | Accepted | CAP-20 is marked not executable until Stage 05 chooses an encoding that is consistent with CCO (roadmap F-7). No integer property is placed on the rating ICE. The v0.4 instance-pattern comment is withdrawn |
| R5-03 | BPO slice 1.0 does carry `obo:BFO_0000054 some ex:P20955` on `ex:BusinessModelGovernanceCapability` | Accepted | OI-9 is confirmed for the inspected `main`. Removing it is a BPO change, and raising it with BPO is the architect's call. Other slices are checked before closure (§9, roadmap F-11) |
| R5-04 | The assessment's targets are inconsistent: the definition says it describes an organization, while CAP-26 and the example say it describes the capability instance | Accepted | CD14 states one pattern, following CM-01: an assessment describes the organization, is about the capability instance only when one is identified, and carries one `bco:concernsType`. An absent finding links no instance. Fixtures cover swapped and missing targets |
| R5-05 | CAP-21 checks the act's type but not that the organization performed it | Accepted with amendment | New CAP-34 requires a participation witness: a member agent of the bearer participates in the realizing act. R5 named BFO *has participant*. v0.5 leaves the choice of relation to Stage 05, under the reuse order of §3.1, and mints none |
| R5-06 | CAP-26 checks `has capability` triples only; the inverse `capability of`, or BFO `bearer of`, bypasses it | Accepted | CAP-26 applies to every asserted K1 individual. Each must have exactly one Organization bearer and one supporting assessment, whichever direction the bearing is asserted in. The graph is normalized to `cco:ont00001954` first |
| R5-07 | CQ-5's applicability rules are underspecified | Accepted with amendment | CD15 gains an applicability table with proposed rules for each dimension R5 names, each with positive and negative fixtures. Revocation and supersession need a term v0.5 does not mint, so they are excluded from complete graphs and tracked as OI-21 |
| R5-08 | `ex:enablesProcess` is a generated annotation whose label sounds causal | Accepted | CD12 and CAP-03 state that it is an admissible-realization index, not actual enablement. Gate B checks that it is declared an `owl:AnnotationProperty`, and the generator's output is tested. The old generator stays until its consumers are audited |
| R5-09 | "Losing an artifact makes a capability unavailable; it does not make it cease" is categorical | Accepted with amendment | DP-1's commitment stands as decided ("does not *by itself* end"). CD2 adds the case R5 raises: when a platform's loss also removes members' embodied capacity, the basis changes, and G1-I is re-asked. A type whose review shows an artifact is constitutive goes to OI-14. Fixture pair as R5 proposes |
| R5-10 | Function review should follow BFO's origins, not the fact that an organization is designed | Accepted | CD6 and CAP-09 state the criterion from BFO's definition of function: physical make-up that exists through evolution or through intentional design in order to realize processes of a sort |
| R5-11 | `partial` needs a reportable criterion | Accepted | CD14: `partial` means partial coverage of a declared assessment criterion, never partial being. `dct:conformsTo` names a criterion with an identifier. CAP-27 checks it |
| R5-12 | "No triple generated from CQ-12" is a pipeline property that SHACL cannot see | Accepted | CAP-29 moves to generator and provenance tests. An assertion-level rule stays: an integration, availability or adequacy finding appears only in a Functional Adequacy Assessment that cites criteria and evidence (CAP-33) |
| R5-13 | CCO's Plan already has continuant part some Objective; CAP-31 still needs a named target | Accepted | CAP-31 stays a check on named objects. OI-19 is narrowed: the vendored extract carries no restrictions, so the axiom is confirmed when the extract is rebuilt at Stage 05 |
| R5-14 | The parent's definition says every capability is realized per its index, but the parent is exempt from the index | Accepted | §4: the parent is defined by realizability in Planned Acts. The index is required of named specific classes (CAP-03) |
| R5-15 | Dropping the capability description ICE loses portability | Accepted | OI-17 stays open. No redundant ICE is introduced |
| R5-16 | v0.4's new files are not executable | Accepted | §2 marks every module file as proposed backlog, not as satisfying any CAP requirement |

## 0.3 Domain-practitioner review (AD-2)

**Status: not yet conducted.** Under AD-2, a domain practitioner reviews CM-01 before this
specification is submitted for ratification. The architect's approval of CM-01 stands; the
review supplements it.

- **Reviewer.** At least one practitioner with demonstrable enterprise capability-modeling
  experience, named with the capacity acted in: business architect, capability-planning
  practitioner, or FIBF standards-lead-agency analyst. Independence from the drafting team is
  preferred. Qualifications and capacity are documented before the review counts (roadmap
  O-3, open).
- **What it evaluates in CM-01.**
  1. Do the Business Capability definitions represent recognizable organizational abilities?
  2. Are the boundaries among capability, process, skill, authorization and enabling
     condition ontologically and practically defensible?
  3. Do the functional coverage and adequacy constructs support real capability-planning
     decisions?
  4. Do representative sourcing, dormant-capability and organizational-grounding scenarios
     behave as intended?
- **What it records.** Each practitioner's identity and capacity, findings, proposed
  dispositions, and the artifacts each finding affects.
- **What follows.** The architect decides each disposition. Accepted findings are carried
  into this specification before CP-0, and this section then lists them with the sections
  they change. A finding that requires changing CM-01 is a new, reviewed and approved CM-01
  version, never a silent edit. The reviewer judges domain applicability and practical
  meaning. BFO/CCO alignment, conceptual changes and the acceptance of dispositions remain
  the architect's.

## 1. Purpose, scope and non-goals

The Business Capability Ontology (BCO) says what an organization can do. The Business
Process Ontology (BPO) says what it does. The BCO takes its act types from the BPO reality
layer and adds the dispositions those acts realize. It operationalizes ADR-001 R5 and R6:
R5 sends standing-function nodes ("Manage X") to capabilities, and R6 says to model them
under CCO Organization Capability. Neither rule says when a capability is a BFO
disposition, what bears it, or what realizes it. This specification does, as CM-01
models it.

**Modules and the release boundary** (roadmap AD-1). This specification covers the
**Business Capability module**, the first release. It is not represented as covering the
Agent Capability domain.

- **Agent Capability module.** The abilities of agents other than an organization taken as
  a whole are CM-02's: a person's Skills, member-wise abilities of a group, and what acting
  artificial systems bear. Artificial systems are included as subject matter only. Whether
  one is a CCO Agent, bears an Agent Capability or bears an artifact function is for CM-02
  to establish (`docs/proposals/2026-10-31-cm02-scope-note.md`, approved under D2).
  Nothing in this module formalizes them. CM-02 is not a prerequisite for this module's
  formalization, and approving this module authorizes no Agent Capability class.
- **What this module keeps, whatever CM-02 finds.** A system is never a member agent. It
  is outside the material basis of every business capability. It is an enabling condition
  only of capabilities whose realization actually depends on it. A software agent bears no
  Organization Capability, and an agent manifest is a routing description (CD13).
- **Integrated ontology.** Only a release that integrates and validates both modules may
  claim comprehensive Business and Agent Capability coverage.

**In scope**

- Organization capability classes: their bearer, grounding basis, enabling conditions,
  and realization by BPO act types.
- The boundaries between capability and role, permission, skill, artifact function and
  plan.
- A description and assessment layer: maps, capability assessments, functional adequacy
  assessments, maturity, sourcing and target state, as ICEs about capabilities.
- Validation rules extending BPO Gates A to D.

**Non-goals**

- Person-borne abilities beyond reusing CCO Skill, member-wise abilities, and artificial
  systems' abilities. These belong to CM-02.
- A new act-type hierarchy. Act types come from the BPO reality layer and `apqc-ext.ttl`
  only.
- A maturity scoring method. The BCO represents assessments; it does not prescribe how to
  score.
- Deontic logic. Permissions and requirements are reused from CCO, not reasoned over.
- Industry capability frameworks (BIZBOK, BIAN). These may enter later as further catalog
  schemes, subject to their access terms.

## 2. Architecture

The BCO adds two layers to the BPO's two. Capabilities point down to the acts that realize
them. Descriptions point down to the capabilities they are about. Nothing in the capability
layer points up. The catalog bridge is ADR-001 R4, unchanged: a catalog node that passes R5
designates a process class, and a standing-function node designates a capability class under
R6, where one is defined (CD16).

**Module layout (proposed backlog).** None of these files satisfies a CAP requirement until
its fixtures run (R5-16).

| File | Content |
| --- | --- |
| `src/05_ontology/apqc-cap.ttl` | `bco:BusinessCapability`, the capability classes as tranches admit them, and any reviewed K2 unions. An empty ontology header today |
| `src/05_ontology/apqc-cap-desc.ttl` | The description-layer classes and the Authorization Record. An empty ontology header today |
| `shapes/` | CAP shapes beside the existing ones; CAP-21 runs on the asserted graph only |
| BPO `capabilities/capability_scope.json` | Kept in BPO; generates the realization index (CD4, CD12) |
| `coverage_register.json` *(new; location fixed at Stage 06)* | Standing function (APQC catalog concept) → required component capability classes (CD16) |
| Evidence manifests *(new)* | Completeness manifests for evidence graphs, checked by Gate M (CD15) |
| `bc:` migration manifest *(new)* | Term-by-term rename record for the v0.1 vocabulary (§9.1) |
| `docs/adr/ADR-002-organizational-capabilities.md` | This specification's decisions, once ratified |

Capability classes that BPO's slices declare are candidates for type admission, not
admitted types (CM-01 Q-12). They move into the BCO only through a formalization tranche
(roadmap §7).

## 3. Design decisions (CD1–CD17)

These seventeen commitments carry the design. Each is proposed, not ratified. A tag such as
*(v0.5, DP-1)* marks a decision changed in that version, and names the decision or finding
it was changed under. They are numbered CD to avoid collision with methodology D1 to D9 and
ADR-001 R1 to R7.

Three questions run through them, and the specification keeps them apart:

- **admissibility**: can capabilities of this type be genuine dispositions? Settled per
  type, by G1-T;
- **possession**: does this organization bear one? Settled per claim, by evidence (G1-I);
- **adequacy**: is what it bears integrated, available and sufficient for its purpose?
  Settled by assessments, never derived from possession.

**CD1 — Bearer** *(v0.4, R4-01; v0.5, DP-1, D2)*. A Business Capability inheres in a
`cco:ont00001180` Organization, and in nothing else.

- A person's ability is a CCO Skill (`cco:ont00000089`). Abilities several agents have
  member by member, and whatever acting artificial systems bear, are also outside this
  module. They belong to the Agent Capability module (CM-02).
- A member's skill is evidence for an organization's capability (G1-I question 2), never
  the capability itself.

**The departures, by source and clause** (SF-05; CM-01 Q-08). No source restricts the
bearers of capability to organizations, so this is a deliberate narrowing. Each source
below admits other bearers:

| Source | Clause | What it admits | Register |
| --- | --- | --- | --- |
| UAF Domain Metamodel 1.3 | Strategic::Taxonomy::Capability | Any CapableElement: operational agent, service, actual resource, actual organization | SRC-OMG-04 (V) |
| NATO Architecture Framework v4.1 | Glossary, p. 154; Capability Configuration | Capability realized by configurations of people and technology | SRC-GOV-04 (V) |
| IOF Core 202603 | Capability | Any independent continuant | SRC-FO-02 (V) |
| BACM 1.1 | §7.3.4.5 OrgUnit | OrgUnits that include individuals | SRC-OMG-03 (V) |
| VDML 1.1 | §7.1.7, as register finding SF-05 cites it | Providers other than organizations | SRC-OMG-01 (V for the entry; the clause is not quoted in the entry and is re-read before ratification) |
| ISO 19440:2020 | 3.6, the Capability construct | Capability attributes of a Resource | SRC-ISO-02 (P, clause 3) |
| ArchiMate 3.2 | Capability, strategy layer | Organization, person or system | SRC-OG-03 (S; L) |
| TM Forum GB1029C | Business Capability Map | Active structure elements: organization, person or system | SRC-IND-04 (S; L) |
| ISO 9000:2015 | 3.6.12 | Any object | SRC-ISO-05 (S) |
| ITIL | Glossary lineage (v3) | Organizations, people, processes, applications, services | SRC-IND-06 (S) |

The last four rest on secondary sources. The source-adequacy gate requires V or P, or an
approved exception, so each is listed in §10 as an exception requested (SE-1). Sending
person-borne abilities to Skill has primary-text precedent:

- UAF's Personnel Competence (SRC-OMG-04, V);
- BACM's PerformerRole (SRC-OMG-03, V);
- IOF's agential capability (SRC-FO-02, V);
- the Enterprise Ontology's SKILL (SRC-FO-09, V).

**Ratification item RP-1.**

**CD2 — Grounding basis** *(v0.2, R2-04; v0.4, R4-01; v0.5, DP-1, R5-01, R5-09, R9)*. As
decided under DP-1 (Option A with a1 to a4), four things are kept apart (a3):

1. **Material constitution: the basis.** The relevant member agent or agents of the
   organization, in virtue of whose being organized as they are the organization has the
   capability (a1). One indispensable member can suffice. The basis is never the
   arrangement, never an abstract set, and never an artifact, owned or not.
2. **Organizational configuration: the arrangement.** Positions, reporting and decision
   lines, routines and coordination. It is the reason the basis grounds the capability. It
   is not itself material. A change to it can make or end a capability without any change
   of membership.
3. **Enabling conditions.** Every artifact, facility, data set or outside service *relevant
   to the capability's realization* (R9), owned or not, internal or sourced. Each takes part
   in realizations. An artifact that plays no part in a capability's realizations is neither
   its basis nor one of its enabling conditions.
4. **Temporary realization constraints.** Outages, missing authorization, circumstances.
   They are recorded as findings in assessments.

- **A modeling policy, not a CCO entailment** (R5-01). That the basis consists of member
  agents only is the BCO's policy, chosen under DP-1. CCO restricts an Organization's *has
  member part* to Agents, and BFO requires the object of `obo:BFO_0000218` to be a material
  part of the bearer. CCO does not by itself forbid every other part of an organization.
  The policy keeps CCO's Organization Capability reusable as is, and satisfies BFO's
  condition for every basis it asserts.
- **A basis only for an admitted type** (a2). Asserting `obo:BFO_0000218` on a capability
  classifies it as a disposition (SF-02), so a basis is asserted only for an instance of a
  type that has passed G1-T (CD3, CAP-25).
- **The commitment, as decided.** Permanently removing an essential platform does not *by
  itself* end a capability. The capability persists, latent, and is assessed as unavailable
  until the platform is replaced. It ends only when its basis or its arrangement goes.
  Whether it is available also depends on whether adequate alternatives exist (CM-01
  approval guidance).
  - The commitment is the BCO's, not claimed to be universal. Defence and
    enterprise-architecture frameworks that count technology inside the capability depart
    from it: NAF and UAF Capability Configurations (SRC-GOV-04, SRC-OMG-04, V), APQC
    (SRC-IND-01, P), TOGAF G211 (SRC-OG-02, P; L) and DM2 (SRC-GOV-01, S) (SF-06).
- **When a platform's loss reaches the basis** (R5-09). Losing a platform can also remove
  what members can do: staff whose only skill was operating it. Then the basis or
  arrangement has changed, and G1-I is asked again. That is a change in the members, not
  the platform's loss ending the capability.
  - A type whose review shows an artifact is constitutive, so that losing it ends the
    ability rather than suspending it, is not forced into this pattern. It goes to the
    socio-technical question a4 keeps open (OI-14), which NAF and UAF support.
- **Ownership and control sort dependencies only.** They decide whether an enabling
  condition is internal, or an external dependency recorded by a sourcing statement.
- **The provider's work is the provider's.** When another organization's staff perform the
  acts, the consumer bears no capability for them. Internal capability and sourcing may
  coexist for the same acts.
- **Fragility is not reclassification.** A capability resting on one indispensable member
  is still organizational if its realizations run through organizational arrangements.
  Losing that member can end it.
- **Ability, not assignment.** An organization chart, an assigned responsibility, a charter
  or an authorization shows that the organization is responsible or permitted, not that it
  is able (G1-I).
- **Ratification item RP-1.**

**CD3 — Admission and attribution** *(v0.4, R4-02; v0.5, DP-2)*. Two tests, kept apart.

- **Type admission, G1-T** (§8). It is asked once per capability class, with no particular
  organization in view. A pass licenses asserting the class under `obo:BFO_0000016`, and
  licenses no organization's claim to bear one.
- **Instance attribution, G1-I.** It is asked for each claim that an organization bears a
  capability, and recorded as the supporting Capability Assessment (CAP-26).
- **Staging is transitional.** A class not yet admitted stays under `cco:ont00000568`
  alone. BFO 2020 divides realizables into dispositions and roles, so a class that fails
  G1-T is reclassified or removed. It is never left staged (b4, CAP-32).
- **No interest condition** (b2 rejected). IOF and Beverley et al. require an agent with an
  interest in a capability's realization (SRC-FO-02, SRC-FO-03, V; SF-04). The BCO does not
  ask it: no reviewer asked for it, and an organization's own interest plausibly satisfies
  it anyway. This is a recorded departure from both, and can be revisited.
- **Ratification item RP-10.**

**CD4 — Realization index** *(v0.2, R2-01; v0.3, R3-04; v0.4, R4-03)*. Every specific
capability class carries a mandatory realization index: one or more `ex:enablesProcess`
annotations. Each names a BPO reality-layer act class or a D9 genus.

- The index lists admissible realization types. It makes no modal claim and no claim of
  exhaustiveness.
- **No index member is a capability class.** BPO's index entries that name classes under
  Organization Capability must be re-indexed to the acts those functions contain before any
  BCO class takes its index from BPO (CM-01 Q-12; OI-20).
- **`only` is optional and reviewed.** A class may also carry `obo:BFO_0000054 only
  <Filler>`, but only with a review record defending the index as exhaustive (CAP-30). The
  filler is the single index member, or a K2 union of the members.
- **Classes are primitive.** A capability's identity is its bearer kind (CD1), its grounding
  (CD2) and its realization index together. The textual definition states all three. No
  equivalence axiom is claimed.
- **Observed realizations are checked on asserted data.** An act that `realizes` a capability
  must have an asserted type under one of the capability's index members (CAP-21). It must
  also have a member agent of the bearer as a participant (CAP-34, R5-05).
- **Coverage is not here.** Whether an organization can carry out a whole function is CD16.
- **Non-deontic indexing.** Index members must be describable without deontic success
  conditions. Where a BPO act is institutional, the capability indexes to the non-deontic
  act it contains; standing is a role or a permission.

**CD5 — Development and realization** *(v0.2, R2-09)*. Developing capability C and realizing
C are different relations an act can stand in. An act counts as a realization of C only
when it is justified as an exercise of C. That it brings C about or improves it is not that
justification.

- One act may do both: practice that exercises a capability can also strengthen it.
- An act may develop C while realizing a different capability, as when change management
  builds a new governance capability.
- Example: "Maintain business models" realizes business model governance capability.
  "Establish business model governance" develops it, and realizes it only if separately
  justified as an exercise.

**CD6 — Overlap with Function** *(v0.4, R4-11; v0.5, R5-10)*. Business Capability is not
declared disjoint from BFO Function. A capability class may be classified under
`obo:BFO_0000034` only with a justification record.

- The record must show what BFO's definition requires: that the bearer has the physical
  make-up grounding the capability because it came into being through evolution or through
  intentional design in order to realize processes of that sort (CAP-09).
- That an organization was purposefully designed does not by itself show this.

**CD7 — Capability is not role or permission.** No capability definition may mention
assignment, responsibility, authorization, license or mandate. "Able but not authorized" and
"authorized but not able" must both be representable without contradiction.

**CD8 — Capacity, not exercise** *(v0.5, DP-2 b5, R8-06)*.

- No capability class carries an existential realization axiom, and a capability that has
  never been exercised is admissible.
- It is also attributable: evidence of capacity can support a present finding on its own.
  A recorded realization supports a finding but is never required.
- Evidence of past exercise supports a present finding only together with evidence that the
  basis and arrangement are still in place.

**CD9 — Primitive classes, reviewed specialization** *(v0.3, R3-01; v0.4, R4-10; v0.5,
R8-05)*. `rdfs:subClassOf` between capability classes means specialization only.

- **A parent means any ability within its function.** Every accounting capability is a
  financial-management capability of some kind. A parent does not mean complete ability to
  carry out the function.
- **Review establishes membership, not similarity.** A subclass link is asserted only when
  review establishes that every instance of the narrower disposition is an instance of the
  broader one, in bearer, grounding and realization. Overlapping or nested realization
  types alone are insufficient.
- **Candidates come from the index.** A pair is a candidate (CAP-10) when every index member
  of the narrower class falls under some index member of the broader one.
- **Multiple classification.** A capability may be an instance of several applicable
  classes. Recording one primary class is an application convention, not a principle of the
  model.
- **Nothing is induced.** Neither the coverage register (CD16) nor APQC partonomy generates
  subclass links.

**CD10 — Member-wise bearing is not organizational bearing** *(v0.2, R2-13)*.

- Organization-to-capability uses `cco:ont00001954` (has capability), with inverse
  `cco:ont00001889` (capability of).
- `cco:ont00001898` (aggregate has capability) is read as each member bearing its own
  capability of the type. It is not the aggregate bearing one, and it never stands in for a
  Business Capability.
- Member-wise attribution is CM-02's subject.

**CD11 — Descriptions are about, not of** *(v0.4, R4-08, R4-12)*. Description-layer ICEs
refer to organizations and capability instances by `cco:ont00001808` (is about) or its
subproperties: `cco:ont00001982` (describes) and `cco:ont00001811` (is a ordinal
measurement of). Directive ICEs may use `cco:ont00001942` (prescribes). A capability listed
in a map is not thereby asserted to exist.

- **What is forbidden is narrow.** No ICE may bear a capability or realize one. Provenance,
  authorship, carrier and parthood relations on ICEs are unaffected (CAP-11).
- **Sourcing is a two-party record, by convention.** A Capability Sourcing Statement
  concerns exactly two organizations. It `describes` the consumer, is about the provider,
  and carries one `bco:concernsType` naming the act class sourced.
  - This is an application convention validated by SHACL (CAP-23), not a meaning that
    `describes` or `is about` has in CCO.
  - Brokers, intermediaries and provider networks are out of scope (OI-18).
  - Contractor and customer roles corroborate where they exist.

**CD12 — The realization index is an annotation** *(v0.4, R4-03; v0.5, R5-08)*. BPO's
`capability_scope.json` generates `ex:enablesProcess`, the mandatory realization index of
CD4. It is an `owl:AnnotationProperty` with no causal or modal entailment. Its label is
historical: it means *admissible realization*, not actual enablement.

- `requiresCapability` stays withdrawn. Read as stated, it would say every act of a type
  needs an organization bearing the capability, which is false whenever a contractor or a
  single person performs it.
- Each scope entry is checked against CD5 before it enters the index.
- Generation is tested on its output. The legacy generator is not removed until its
  consumers are audited.

**CD13 — Agent manifests describe; they do not bear** *(v0.2, R2-11; v0.5, D2)*. BPO's
`capabilities/agents.json` lists software agents against capability classes. No software
agent bears an Organization Capability (CD1).

- Software is information content, not a material entity, so it bears no BFO realizable.
  Any artifact function belongs to the deployed computing artifact that executes it.
- The manifest is an ICE that designates the capability types an agent serves (CD14). It
  keeps its routing use.
- Under CD2, the computing artifact is outside the basis of every business capability. It is
  an enabling condition only of those whose realization actually depends on it.
- What an artificial system bears is CM-02's question, approved as in scope under D2
  (S-1a). Nothing here presumes the answer, and nothing CM-02 finds changes this module's
  treatment.

**CD14 — Type references and findings** *(v0.3, R3-02; v0.4, R4-09; v0.5, R5-04, R5-11)*. An
ICE that concerns a class rather than an instance carries the annotation `bco:concernsType`,
valued with a capability class or act class IRI.

- **One assessment pattern** (R5-04, following CM-01). A Capability Assessment:
  - `describes` the organization;
  - is about the capability instance only when one is identified;
  - carries exactly one `bco:concernsType`;
  - states exactly one finding.

  An absent finding links no instance.
- **Maps carry entries, not types.** A Capability Map has its entries as continuant parts
  (`obo:BFO_0000178`). Each entry is a Capability Assessment or a Capability Target with
  exactly one `bco:concernsType`. A Functional Adequacy Assessment is never a map entry.
- **Every assessment states its finding.** Each Capability Assessment carries one
  `bco:assessedPresence` (`present`, `absent` or `partial`), whether or not it links a
  capability instance. A `present` finding is an evidential claim, not proof that the
  disposition exists.
- **`partial` is partial coverage of a declared criterion** (R5-11). It cites the criterion
  through `dct:conformsTo`, by an identifier that can be reported: a component set, a
  declared scope or an evaluation criterion. It never means a fraction of a disposition.
- **Inadequate evidence is not a finding** (CM-01 approval guidance). An assessor who cannot
  establish presence or absence records no finding, rather than `absent`. Likewise, a
  Functional Adequacy Assessment that cannot establish a dimension does not record "not
  met". The bearing claim then has no supporting assessment, and CQ-13 reports it.
- Rejected: punning, and per-type designator individuals. The pattern mirrors
  `ex:designatesProcessType` and stays in OWL 2 DL.

**CD15 — Closed-world evidence** *(v0.3, R3-03; v0.4, R4-05, R4-14; v0.5, R5-07)*. OWL
reasoning stays open-world. Absence questions are evaluated over named evidence graphs,
whose completeness is declared in a manifest.

- **Authorization Records, not Action Permissions.** CCO defines `cco:ont00000751` as a
  regulation that permits some process, so typing a prospective license as one asserts that
  a permitted process exists. The register therefore holds `bco:AuthorizationRecord`s. Each
  is about the acting agent, names the permitted act class with `bco:concernsType`, carries
  `schema:validFrom` and `schema:validThrough` as `xsd:date`, and cites its authority with
  `dct:source`.
- **Action Permission once an act occurs.** A `cco:ont00000751` individual is asserted only
  for an authorization of an act that actually occurred, and it `permits` that act
  (`cco:ont00001910`).
- **The completeness manifest lives outside OWL.** It is a JSON artifact with a fixed schema:
  graph IRI, organization, acting agents, covered act classes, start and end dates, and
  authority sources. A graph is complete only within that scope.
- **Answers are bounded.** "No applicable authorization recorded within the declared scope",
  never "not authorized". Outside any manifest, an absence question returns *unknown*.
- **Applicability** (R5-07). These rules are proposed for RP-7. Each has a positive and a
  negative fixture.

| Dimension | Proposed rule |
| --- | --- |
| Act type | A record applies to acts of its named class and of every class under it in the asserted hierarchy |
| Agent | A record applies to the agent it is about. A record about a member person does not apply to the organization, or the reverse |
| Period | A record applies on a date from its `schema:validFrom` to its `schema:validThrough`, inclusive |
| Overlap | Any one applicable record suffices. Overlapping records are not an error |
| Several authorities | Each record is judged alone. Which authority governs is not reasoned over (no deontic logic) |
| Revocation and supersession | Not representable without a term v0.5 does not mint. A graph holding a revoked or superseded record may not be declared complete (OI-21) |
| Scope | A question outside a manifest's graph, organization, agents, act classes or dates returns *unknown* (CAP-18) |

**CD16 — Functional coverage and adequacy** *(v0.3, R3-01; v0.4, R4-06, R4-07; v0.5, R8-07,
R9)*. Whether an organization can perform a standing function is four questions, not one.
Each is answered by a different thing, and none is inferred from another (CM-01 §6).

| Aspect | Answered by | Never derived from |
| --- | --- | --- |
| Possession of components | Has capability joined to the coverage register (CQ-12) | — |
| Integration and coordination | The integration finding of a Functional Adequacy Assessment | Possession |
| Operational availability | Its availability finding, citing enabling conditions and sourcing statements | Possession; integration |
| Adequacy for the function | Its adequacy finding, against its criteria | Any of the three above |

- **The coverage register** is keyed by the APQC catalog concept of each standing function
  (`ex:PCF_<id>`), which keeps ADR-001's catalog–reality separation. It lists the
  *component* capability classes the function requires.
- **Designation is conditional** (R9). A Standing Function designates at most one
  *whole-function* capability class, and only where one has been defined. Otherwise it is
  represented only by its register entry.
  - The whole-function class is never one of its own components (CAP-22).
  - Bearing every component does not entail bearing the whole-function class, and neither
    settles adequacy.
  - Whether an organization bears the whole-function class is a Capability Assessment
    concerning that class.
- **Integration, availability and adequacy are assessed, never derived.** They are the three
  findings of one Functional Adequacy Assessment directed at the Standing Function (CD17).
  None is generated from a CQ-12 result (CAP-29, CAP-33). This answers OI-15: an adequacy
  statement about a function with no capability class of its own concerns the function, not
  a class.
- **No generated axioms.** Listing a component creates no subclass link, and a function need
  not have a capability class of its own.
- **Ratification item RP-8.**

**CD17 — Information-layer scope** *(v0.4, TM-1 to TM-5; v0.5, R9)*. The description layer
has seven classes and one conceptual category whose representation is not yet chosen.

- Three distinctions from the v0.1 vocabulary are kept:
  - a sourcing statement (the arrangement) is distinct from a sourcing assessment (the
    dependence on it);
  - a capability target (the end state) is distinct from a target-state specification (the
    plan to reach it);
  - a maturity rating (the ordinal result) is distinct from the assessment that produced it.
- **Functional Adequacy Assessment** (R9) is a distinct category, a sibling of Capability
  Assessment, never a kind of it:
  - it describes exactly one Organization and assesses adequacy for exactly one Standing
    Function;
  - it concerns no capability class and states no presence finding;
  - it states exactly three findings: integration and coordination, operational
    availability, and adequacy for the function;
  - each finding is *met*, *partly met* or *not met*, relative to the criteria it conforms
    to, which are required.

  Whether it is represented as an eighth description class or otherwise is evaluated at
  Stage 05 before any class is added (CM-01 approval guidance; roadmap F-7). Its
  requirements (CAP-33) hold whichever representation is chosen.
- What a capability type means is stated once, in the class definition and its catalog
  node. No separate description ICE restates it (TM-1, OI-17).
- **Ratification item RP-9.**

### 3.1 Formalization questions

Three questions about the formal representation were raised before formalization so that
they are settled deliberately, not discovered in OWL. None reopens DP-1 or DP-2. Each is a
formalization issue, unless investigating it shows a genuine contradiction with approved
conceptual meaning. Such a contradiction goes to change control on CM-01.

1. **Material basis and disposition.** The question is how to represent an admitted
   capability type consistently with BFO and the existing decisions. The disposition and
   material-basis pattern (`obo:BFO_0000016`, `obo:BFO_0000218`) is applied to a specific
   capability type only after its G1-T admission (CD2 a2, CD3). The form of a plural basis
   is a Stage 05 question (roadmap F-5).
2. **Conditional standing-function designation.** Designation (CD16) is represented with
   existing patterns: information entities, annotations such as `ex:designatesProcessType`,
   and validation, evaluated during formalization and reusing BFO/CCO relations wherever
   possible. A conceptual relationship authorizes no new object property.
3. **Capabilities never exercised.** The existence or attribution of an unrealized
   capability (CD8) is distinct from the absence of recorded realizations. Closed-world
   evidence rules apply to bounded absence queries (CD15, CQ-4), never as a condition for
   bearing a BFO disposition.

**Relation reuse order.** Before any formal relationship is selected, Stage 05 checks CCO's
Extended Relation Ontology first, then the relevant CCO domain ontology, and reuses an
existing construct wherever one applies (the architect's D2 review and approval, 2026-10-31).

## 4. Terms

The module mints:

- the generic parent `bco:BusinessCapability`;
- the specific capability classes, tranche by tranche;
- a K2 union only where a reviewed `only` restriction needs one;
- seven description-layer classes, and possibly an eighth (CD17);
- one evidence-register class;
- two annotation properties.

Everything else is reused. Each term lists what it does not imply, because that is where
misuse starts. No term is minted by this specification. Each is minted in a formalization
tranche, under the IRI policy of ADR-003 D1.

**Reality layer**

| Term | Definition | Parents | Does not imply |
| --- | --- | --- | --- |
| Business Capability `bco:BusinessCapability` *(rev. v0.5)* | An Organization Capability that is a Disposition inhering in an Organization, whose material basis is the relevant member agent or agents of that organization as organized, and that is realizable in Planned Acts the organization's members perform on its behalf. | `cco:ont00000568`, `obo:BFO_0000016` | That it has ever been realized. That it is available now (enabling conditions may be missing). That the organization is authorized. That any one member bears it. That any artifact is its basis. That it was designed (Function). |
| Specific capability classes (strategic planning capability and the rest) | Each states its bearer kind, grounding and realization index in its definition, and carries one or more `ex:enablesProcess` (CD4, CAP-03). | `bco:BusinessCapability` after G1-T; `cco:ont00000568` alone before (CD3) | That any organization bears one. That the class is OWL-defined. That a parent means complete ability to carry out its function (CD9). That an instance falls under no other class (CD9). |
| Realization union `bco:<Name>Realization` | A Planned Act class defined as the union of a capability's index members, used only as the filler of a reviewed `only` restriction. | `cco:ont00000228` | That every instance realizes this organization's capability. That the bearer can perform every member type. |

The parent's definition speaks of realizability in Planned Acts. The index is required
of each named specific class, not of the parent (R5-14).

**Description layer** (CD17)

| Term | Definition | Parent | Does not imply |
| --- | --- | --- | --- |
| Capability Map `bco:CapabilityMap` | A Descriptive ICE that describes an organization and has, as continuant parts, the Capability Assessments and Capability Targets that are its entries. | `cco:ont00000853` | That any listed capability exists. That the arrangement of entries is parthood among capabilities. |
| Capability Assessment `bco:CapabilityAssessment` *(rev. v0.5)* | A Descriptive ICE that describes an organization with respect to the presence, absence or partial presence of a capability of one given type, is about that capability where one is identified, states that finding, and cites its evidence and criteria. | `cco:ont00000853` | That the finding is true. That an instance exists. That `partial` is a fraction of a disposition. That inadequate evidence is an absent finding. |
| Capability Maturity Rating `bco:CapabilityMaturityRating` | An Ordinal Measurement ICE that ranks an existing Organization Capability instance on a specified ordinal scale, carrying its ordinal value and citing the assessment that produced it. The value's encoding is chosen at Stage 05 (R5-02). | `cco:ont00001010` | Graded capability subclasses. Any particular scale or scoring method. Use for an absent capability. |
| Capability Sourcing Statement `bco:CapabilitySourcingStatement` | A Descriptive ICE that describes an Organization's arrangement for obtaining performances of one specified Planned Act class from one other Organization. | `cco:ont00000853` | That the consumer lacks an internal capability for the same acts. That the consumer bears the provider's capability. A multi-party arrangement. |
| Capability Sourcing Assessment `bco:CapabilitySourcingAssessment` | A Descriptive ICE that is about a Capability Sourcing Statement and describes the consumer's dependence on that arrangement on stated criteria and evidence: operational risk, possibility of substitution, and whether the consumer bears an internal capability for the sourced acts. | `cco:ont00000853` | That the dependence is a defect. That the consumer lacks an internal capability. |
| Capability Target `bco:CapabilityTarget` | An Objective that prescribes that an organization come to bear a capability of one given type. | `cco:ont00000476` | That the capability is absent now. How it is to be reached. |
| Capability Target-State Specification `bco:CapabilityTargetStateSpecification` | A Plan that prescribes the acts through which an organization is to reach one or more Capability Targets, such as recruitment, training, technology deployment or a sourcing arrangement, and has those targets as continuant parts. | `cco:ont00000974` | That the plan has been adopted or carried out. That the targets will be met. |
| Functional Adequacy Assessment *(new, R9; representation open)* | A statement that describes one Organization with respect to one Standing Function, and states three findings, each met, partly met or not met against required criteria: integration and coordination, operational availability, and adequacy for the function. | To be chosen at Stage 05 (CD17) | That the organization bears a whole-function capability. That any finding follows from component possession. That it is a Capability Assessment or a map entry. |

**Evidence register** (CD15)

| Term | Definition | Parent | Does not imply |
| --- | --- | --- | --- |
| Authorization Record `bco:AuthorizationRecord` | A Descriptive ICE that is about an agent and records an authorization for that agent to perform acts of one act class during a stated period, citing the authority that issued it. | `cco:ont00000853` | That any permitted act occurred. That the authorization is valid in fact. That it is a `cco:ont00000751` Action Permission. |

**Annotation properties**

| Term | Use | Value |
| --- | --- | --- |
| `bco:concernsType` | Identifies the capability class or act class an ICE concerns (CD14) | A capability class IRI or an act class IRI |
| `bco:assessedPresence` | Records the finding of every Capability Assessment (CD14) | `present`, `absent` or `partial` |

**Reused without change:**

- CCO: `cco:ont00001180` Organization, `cco:ont00000568` Organization Capability,
  `cco:ont00001379` Agent Capability, `cco:ont00000089` Skill, `cco:ont00000751` Action
  Permission, `cco:ont00001010` Ordinal Measurement ICE, `cco:ont00000974` Plan,
  `cco:ont00000476` Objective, `cco:ont00000853` Descriptive ICE.
- BFO: `obo:BFO_0000218` has material basis.
- Dublin Core `dct:source`, `dct:conformsTo`; schema.org `schema:validFrom`,
  `schema:validThrough`.
- BPO: `ex:enablesProcess`, `ex:designatesProcessType`, the act genera, and the
  description classes `ex:InternalCapabilityData`, `ex:CoreCompetencyAnalysis` and
  `ex:RequiredCapabilityList`.

## 5. Relations and core pattern

The module mints no object property. It uses existing BFO, CCO, Dublin Core and schema.org
terms, plus BPO's two annotations and its own two. Every relation chosen at Stage 05 follows
the reuse order of §3.1.

| Relation | IRI | Use in BCO | Constraint |
| --- | --- | --- | --- |
| has capability / capability of | `cco:ont00001954` / `cco:ont00001889` | Organization ↔ its Business Capability | Normalized to `cco:ont00001954`; supported by G1-I evidence (CAP-26) |
| has material basis | `obo:BFO_0000218` | Capability → constituent member agent or agents | Only for an admitted type; each object a member part of the bearer; never an artifact (CD2, CAP-25) |
| has member part | BFO; IRI verified at Stage 05 | Organization → member agent | Evidence for CAP-25 |
| has participant | BFO, or a CCO agent-participation relation; chosen at Stage 05 | Realizing act → member agent of the bearer | Participation witness (CAP-34) |
| aggregate has capability | `cco:ont00001898` | Member-wise claims only | Never for a Business Capability (CD10) |
| has realization / realizes | `obo:BFO_0000054` / `obo:BFO_0000055` | Capability ↔ act instance | Asserted act type under an index member (CAP-21); `only` optional and reviewed (CAP-30) |
| has continuant part | `obo:BFO_0000178` | Map → its entries; Target-State Specification → its targets | CD14, CD17 |
| is about / describes | `cco:ont00001808` / `cco:ont00001982` | ICE → organization, agent, capability instance or other ICE | Assessment pattern (CD14); sourcing two-party convention (CD11) |
| is a ordinal measurement of | `cco:ont00001811` | Maturity rating → capability instance | Instance must exist |
| prescribes | `cco:ont00001942` | Directive ICE → entity it prescribes | — |
| permits | `cco:ont00001910` | Action Permission → an act that occurred | Never on a prospective authorization (CAP-28) |
| ordinal measurement annotation | `cco:ont00001739` | Not used on ratings | Reserved for the measured entity (R4-13) |
| source / conforms to | `dct:source` / `dct:conformsTo` | Evidence and authority; scale or criteria | CD14, CD15, CAP-20 |
| valid from / valid through | `schema:validFrom` / `schema:validThrough` | Authorization Record validity, `xsd:date` | CD15 |
| enables process | `ex:enablesProcess` (BPO annotation) | Capability class → act class | Admissible-realization index (CD4, CD12) |
| designates process type | `ex:designatesProcessType` (BPO annotation) | Catalog node → capability class | ADR-001 R4; conditional for standing functions (CD16) |
| concerns type | `bco:concernsType` (annotation) | ICE → capability class or act class | CD14 |
| assessed presence | `bco:assessedPresence` (annotation) | Assessment → its finding | Mandatory (CD14) |

**Class pattern.** The index is mandatory. The `only` restriction is shown commented out,
because it needs a CAP-30 review record. The class is staged until G1-T passes.

```turtle
bco:StrategicPlanningCapability a owl:Class ;
    rdfs:subClassOf cco:ont00000568 ;               # bco:BusinessCapability once G1-T passes
    ex:enablesProcess ex:P10037 , ex:P10045 , ex:P10039 ,
                      ex:P10043 , ex:P10020 , ex:P19949 .   # realization index (BPO act classes)

# Only with an exhaustiveness review record (CAP-30):
# bco:StrategicPlanningCapability rdfs:subClassOf
#     [ a owl:Restriction ; owl:onProperty obo:BFO_0000054 ;
#       owl:allValuesFrom bco:StrategicPlanningRealization ] .
```

**Instance pattern 1 — possession, a realization and a rating.** The assessment is the G1-I
evidence for the bearing claim. It describes the organization and is about the capability
(CD14). The rating cites the assessment. The basis is asserted only once the class is
admitted (CD2 a2).

```turtle
acme:acme a cco:ont00001180 ;                        # Organization
    cco:ont00001954 acme:acme_spc .                  # has capability
acme:acme_spc a bco:StrategicPlanningCapability .
acme:acme_2027_mission a ex:P10037 ;                 # asserted type, an index member
    obo:BFO_0000055 acme:acme_spc .                  # realizes
    # participation witness (CAP-34): a planning-office member participates; relation per §3.1
acme:acme_spc_assessment a bco:CapabilityAssessment ;   # G1-I evidence
    cco:ont00001982 acme:acme ;                      # describes the organization
    cco:ont00001808 acme:acme_spc ;                  # is about the identified capability
    bco:concernsType bco:StrategicPlanningCapability ;
    bco:assessedPresence "present" ;
    dct:source acme:acme_strategy_staffing_record , acme:acme_2027_mission .
acme:acme_spc_rating a bco:CapabilityMaturityRating ;
    cco:ont00001811 acme:acme_spc ;                  # is a ordinal measurement of
    dct:conformsTo acme:house_maturity_scale ;
    dct:source acme:acme_spc_assessment .
    # ordinal value: encoding chosen at Stage 05 (R5-02)
```

**Instance pattern 2 — a map with entries (CD14).**

```turtle
acme:acme_map a bco:CapabilityMap ;
    cco:ont00001982 acme:acme ;
    obo:BFO_0000178 acme:acme_map_e1 , acme:acme_map_e2 , acme:acme_map_e3 .
acme:acme_map_e1 a bco:CapabilityAssessment ;
    cco:ont00001982 acme:acme ;
    cco:ont00001808 acme:acme_spc ;
    bco:concernsType bco:StrategicPlanningCapability ;
    bco:assessedPresence "present" .
acme:acme_map_e2 a bco:CapabilityAssessment ;
    cco:ont00001982 acme:acme ;                      # absent: no instance link
    bco:concernsType bco:TreasuryManagementCapability ;
    bco:assessedPresence "absent" .
acme:acme_map_e3 a bco:CapabilityTarget ;
    cco:ont00001808 acme:acme ;
    bco:concernsType bco:TreasuryManagementCapability .
```

**Instance pattern 3 — a two-party sourcing statement and its assessment (CD11, CD17).**

```turtle
acme:acme_payroll_sourcing a bco:CapabilitySourcingStatement ;
    cco:ont00001982 acme:acme ;                      # consumer
    cco:ont00001808 acme:payco ;                     # provider
    bco:concernsType ex:ActOfRemuneration .          # act class sourced (BPO genus)
acme:acme_payroll_dependence a bco:CapabilitySourcingAssessment ;
    cco:ont00001808 acme:acme_payroll_sourcing ;
    dct:conformsTo acme:vendor_dependence_criteria ;
    dct:source acme:acme_vendor_review_2026 .
```

**Instance pattern 4 — a prospective authorization, and the manifest that bounds the
register (CD15).**

```turtle
acme:acme_filing_auth a bco:AuthorizationRecord ;    # not cco:ont00000751
    cco:ont00001808 acme:acme ;                      # acting agent
    bco:concernsType ex:ActOfReporting ;             # act class authorized (BPO genus)
    schema:validFrom "2026-01-01"^^xsd:date ;
    schema:validThrough "2026-12-31"^^xsd:date ;
    dct:source acme:state_regulator_portal .
```

```json
{
  "graph": "acme:graph_acme_authorizations",
  "organization": "acme:acme",
  "acting_agents": ["acme:acme"],
  "act_classes": ["ex:ActOfReporting"],
  "start": "2026-01-01",
  "end": "2026-12-31",
  "authority_sources": ["acme:internal_register", "acme:state_regulator_portal"]
}
```

**Instance pattern 5 — a target and the plan to reach it (CD17).**

```turtle
acme:acme_treasury_target a bco:CapabilityTarget ;
    cco:ont00001808 acme:acme ;
    bco:concernsType bco:TreasuryManagementCapability .
acme:acme_treasury_plan a bco:CapabilityTargetStateSpecification ;
    obo:BFO_0000178 acme:acme_treasury_target .      # has continuant part
```

**Pattern 6 — a functional adequacy assessment (CD16, CD17), in prose.** "Acme, Manage
treasury operations: integration partly met (the cash and risk teams hand off by
spreadsheet), availability met, adequacy not met against the 2026 liquidity criteria." It
cites the CQ-12 answer and the Capability Assessments as evidence, and derives none of its
findings from them. No Turtle is given, because its representation is a Stage 05 choice.

**Reasoner profile.** `owl:allValuesFrom` and `owl:unionOf` appear only on reviewed classes.
They are outside OWL 2 EL, so Gate D (ELK) ignores them and Gate D2 checks them. D2 blocks a
release if it cannot run (§8).

## 6. Requirements

There are thirty-three live requirements and one retired, all DRAFT. IDs are stable across
versions. CAP-32 to CAP-34 are new in v0.5. Each requirement names the fixture that must make
it fail; where a positive case matters, the fixture also names what must pass. FAIL blocks a
build. WARN goes to the review queue.

A requirement whose encoding depends on a Stage 05 choice is marked *(encoding at Stage 05)*.
It is not executable until that choice is made, and it may not be reported as passing.

**Class kinds.** Each class in the capability module is exactly one of:

- **K1 capability class:** under `cco:ont00000568`. `bco:BusinessCapability` is the K1
  parent, and is exempt from CAP-03.
- **K2 realization union:** a union class declared in the module, used only as the filler of
  a reviewed `only` restriction.
- **K3 information class:** an ICE class declared in `apqc-cap-desc.ttl`, covering the
  description layer and the evidence register.

| ID | Requirement | Fixture (fails unless noted) | Level · Gate | Traces |
| --- | --- | --- | --- | --- |
| CAP-01 | Every class in the capability module is exactly one of K1, K2 or K3. | A class under none; a K2 union no `only` restriction uses | FAIL · C | CD1 |
| CAP-02 | No K1 class has a `some` restriction on `obo:BFO_0000054`. | `bco:BadCap ⊑ BFO_0000054 some ex:P10037` | FAIL · C | CD8 |
| CAP-03 *(rev. v0.5)* | Every K1 class except the parent carries one or more `ex:enablesProcess`, each a reality-layer act class or a D9 genus, never a class under `cco:ont00000568`. It carries at most one `only` restriction on `obo:BFO_0000054`, whose filler is its single index member or a K2 union of exactly its index members. `ex:enablesProcess` is declared an `owl:AnnotationProperty`. | A K1 class with no index; an index value that is a catalog node; an index value under Organization Capability; an `only` filler that adds a class not in the index; `ex:enablesProcess` declared an object property | FAIL · B, C | CD4, CD12, R5-08 |
| CAP-04 | A K1 class asserted under `obo:BFO_0000016` or `bco:BusinessCapability` carries a G1-T record (PASS, reviewer, date, the constant-membership cases worked). No organization-specific evidence is required. | A Disposition subclass with no G1-T record; a record without the worked cases | FAIL · C, F | CD3, DP-2 b3 |
| CAP-05 | Every member of a K2 union is a member of the capability's index and never a catalog node. | Union containing `ex:PCF_17040` | FAIL · B, C | CD4 |
| CAP-06 | An index member that is or falls under `ex:ActOfDevelopment`, `ex:ActOfImprovement`, `ex:ActOfOrganizationalEstablishment` or `ex:ActOfAcquisition` needs a review record saying why it exercises the capability. | Governance capability indexing an improvement act with no record | WARN · C, F | CD5 |
| CAP-07 | A K1 definition contains no deontic terms (authoriz-, licen-, mandat-, responsib-, assign-, permit-). | Definition "capacity to fulfill its regulatory mandate" | WARN · C | CD7 |
| CAP-08 | The bearer of a K1 instance, in either direction of has capability, is a `cco:ont00001180` Organization. | `agent.strategy_lead.v1` has capability `acme:acme_spc`; `acme:acme_spc` capability of a person | FAIL · C | CD1, CD13 |
| CAP-09 *(rev. v0.5)* | A K1 class is placed under `obo:BFO_0000034` Function only with a justification record meeting CD6's criterion, and is never declared disjoint from it. | A Function subclass with no record; a record arguing only that the organization was designed; a disjointness axiom | FAIL · C, F | CD6, R5-10 |
| CAP-10 | Every candidate pair under CD9's index rule is reviewed, and the review records why every instance of the narrower is an instance of the broader. | A subclass link resting only on realization overlap | WARN · D2, F | CD9 |
| CAP-11 | No K3 individual is the subject of has capability, bearer of, realizes or has realization. Other relations on ICEs are unaffected. | A map that has capability fails; a map with `dct:creator` passes | FAIL · C | CD11 |
| CAP-12 | `cco:ont00001898` never has a K1 object. | Aggregate-has-capability to `acme:acme_spc` | FAIL · C | CD10 |
| CAP-13 | Every `capability_scope.json` key and listed process resolves to a declared class. | Key `ex:NoSuchCapability` | FAIL · B | CD12 |
| CAP-14 | No `requiresCapability` triple is generated. | Any such triple in the build | FAIL · C | CD12 |
| CAP-15 | *Retired in v0.2.* Hybrid sourcing is normal, not an exception. | — | — | R2-15 |
| CAP-16 | Every K1 class, every K2 union and every index member is satisfiable under a DL reasoner, and the module is consistent. Accepted at CP-2. | An index member declared disjoint from its own parent | FAIL · D2 | CD4 |
| CAP-17 *(rev. v0.5)* | Capability Assessments, targets, sourcing statements and Authorization Records each carry exactly one `bco:concernsType` (a K1 class for the first two, an act class for the last two). Maps, sourcing assessments and Functional Adequacy Assessments carry none. A map has at least one assessment or target entry via `obo:BFO_0000178`, and no Functional Adequacy Assessment as an entry. | A map with a type annotation; an assessment with two; an Authorization Record naming a capability class; a map with an adequacy assessment as entry | FAIL · C | CD14, CD15, CD17 |
| CAP-18 | An absence query returns *unknown* unless a manifest covers the graph, organization, agent, act class and dates asked. Each applicability rule of CD15 has a positive and a negative case. | Fails: a query for a date outside the manifest returns an empty set. Passes: an in-scope query returns "none recorded" | FAIL · query | CD15, R5-07 |
| CAP-19 | No ICE is the bearer of any realizable entity. | A software ICE bearing an artifact function | FAIL · C | CD13 |
| CAP-20 *(rev. v0.5; encoding at Stage 05)* | Every Capability Maturity Rating has `cco:ont00001811` to an existing K1 instance, exactly one ordinal value in the encoding Stage 05 chooses, one `dct:conformsTo` scale, and a `dct:source` that is a Capability Assessment. `cco:ont00001739` is never asserted on a rating, and no property whose domain excludes ICEs is used for the value. | A rating with no value; a value given by `cco:ont00001739`; a value given by a property defined on Information Bearing Entities | FAIL · C | CD17, R4-13, R5-02 |
| CAP-21 | For every act that `realizes` a K1 instance, the act's asserted type falls under one of the capability's index members in the asserted class hierarchy, checked before any reasoning. | An act asserted only as `ex:P10729` (scoped to Accounting) realizing `acme:acme_spc` | FAIL · C-A | CD4 |
| CAP-22 *(rev. v0.5)* | Every coverage register key resolves to an APQC catalog concept, and every component to a K1 class. No `rdfs:subClassOf` is generated from the register. A whole-function class that a standing function designates is never among that function's own components. | A key that is a K1 class; an unresolved component; a function listing its designated whole-function class as a component | FAIL · B, C | CD16, R9 |
| CAP-23 | A Capability Sourcing Statement `describes` exactly one Organization and is about exactly one other Organization. | Three organizations; two `describes` targets | FAIL · C | CD11 |
| CAP-24 | Every Authorization Record is about exactly one agent, has exactly one `schema:validFrom` and one `schema:validThrough` typed `xsd:date`, and at least one `dct:source`. | A plain-string date; no authority source | FAIL · C | CD15 |
| CAP-25 *(rev. v0.5)* | `obo:BFO_0000218` is asserted from a Business Capability only if its class has passed G1-T. Each object is a named agent that is a member part of the bearer, and never an artifact. G1-I evidence names the candidate basis members or positions. | Has material basis `acme:acme_core_platform`; a basis agent that is not a member part of the bearer; a basis on a staged class. Passes: member-part and basis assertions on an admitted class | FAIL · C, F | CD2, DP-1 a1 and a2, R5-01 |
| CAP-26 *(rev. v0.5)* | Every asserted K1 individual has exactly one Organization bearer, whichever direction the bearing is asserted in, after normalizing to `cco:ont00001954`. It is supported by a Capability Assessment that describes that organization, is about that instance, matches its type and finds it `present`. The assessment cites at least one source that is not an organization chart, charter, responsibility assignment or Authorization Record. A source showing only past exercise is accompanied by one showing the basis and arrangement still in place. | Has capability with no assessment; bearing asserted only as capability of, with no assessment; an assessment citing only an Authorization Record; an assessment citing only a past realization | FAIL · C | CD3, CD8, R5-04, R5-06, DP-2 b5 |
| CAP-27 *(rev. v0.5)* | Every Capability Assessment has exactly one `bco:assessedPresence`. A `partial` finding has a `dct:conformsTo` naming a criterion with an identifier. | An assessment with no finding; a `partial` with no criterion; a `partial` citing a criterion with no identifier | FAIL · C | CD14, R5-11 |
| CAP-28 | No individual is typed `cco:ont00000751` unless it `permits` an asserted act instance, and no Authorization Record is typed `cco:ont00000751`. | A prospective license typed Action Permission | FAIL · C | CD15 |
| CAP-29 *(rev. v0.5)* | No assessment, finding or has capability triple is generated from a CQ-12 result. Checked by generator and provenance tests, not by SHACL on the final graph. | A pipeline step writing an "integrated" finding from CQ-12 | FAIL · generator test | CD16, R5-12 |
| CAP-30 | Every `only` restriction on a K1 class has an exhaustiveness review record. | An `only` restriction with no record | FAIL · C, F | CD4 |
| CAP-31 | Every Capability Target-State Specification has at least one named Capability Target as continuant part. | A target-state plan with none | FAIL · C | CD17, R5-13 |
| CAP-32 *(new)* | No K1 class with a failing G1-T record remains staged under `cco:ont00000568` alone. It is reclassified or removed. | A class with a FAIL record still in the module unchanged | FAIL · C, F | CD3, DP-2 b4 |
| CAP-33 *(new; encoding at Stage 05)* | Every Functional Adequacy Assessment describes exactly one Organization, is directed at exactly one Standing Function, and states exactly three findings (integration and coordination, availability, adequacy), each met, partly met or not met, each with criteria it conforms to and at least one cited source. No integration, availability or adequacy finding appears in a Capability Assessment. | An adequacy assessment with two findings; a finding without criteria; a Capability Assessment stating an integration finding | FAIL · C | CD16, CD17, R9, R5-12 |
| CAP-34 *(new; encoding at Stage 05)* | For every act that `realizes` a K1 instance, some member agent of the bearer participates in the act. The participation relation is chosen under §3.1, and no new property is minted. | A provider's process asserted to realize the consumer's capability, with no member of the consumer participating. Passes: a member participates | FAIL · C | CD2, CD4, R5-05 |

## 7. Competency questions

The module is done when each question has a SPARQL query that returns the expected answer
over a fixture organization. Questions marked ‡ ask about absence. They are answered only
within a manifest's declared scope, and return *unknown* otherwise (CD15, CAP-18). The
fourteen questions are those CM-01 traces in its §8.

| ID | Question | Answered by |
| --- | --- | --- |
| CQ-1 | Which capabilities does organization O bear? | `cco:ont00001954` from O, after normalization |
| CQ-2 | Which BPO act types are admissible realizations of capability type C? | C's `ex:enablesProcess` index |
| CQ-3 | Which capabilities did this act instance realize? | `obo:BFO_0000055` from the act, filtered by CAP-21 and CAP-34 |
| CQ-4 ‡ | Which capabilities that O bears at query time have no recorded realization in period P? | Realization log within its manifest's scope. An empty answer says nothing about whether O bears them (CD8) |
| CQ-5 ‡ | Which index act types of O's capabilities lack an applicable Authorization Record for acting agent A and period P? | Authorization Records under CD15's applicability rules, against CQ-2, within the manifest's scope |
| CQ-6 | Which capability types does O's map record as needed (a target entry) with no assessment entry finding them present? | Map entries joined on `bco:concernsType` and `bco:assessedPresence` |
| CQ-7 | For which act types does O have a sourcing arrangement, with which provider, and for which does O also bear a capability indexing that act type? | Two-party sourcing statements describing O (CAP-23), joined to CQ-1 and CQ-2 |
| CQ-8 | Which capability targets does O have, and which already match a capability O bears? | Targets' `bco:concernsType` joined to CQ-1 |
| CQ-9 *(rev. v0.5)* | Which APQC catalog nodes are standing functions with a whole-function capability class? | `ex:designatesProcessType` to a K1 class. A standing function with none is represented only by its register entry (CD16) |
| CQ-10 | Which capability classes have not passed G1-T? | K1 classes without a PASS G1-T record |
| CQ-11 | Which acts develop capability C, as distinct from realizing it? | CAP-06 review records (no ontology relation yet, OI-4) |
| CQ-12 *(rev. v0.5)* | Does O bear an instance of every capability class listed as a required component of standing function F? | The register entry for F, joined to CQ-1. Answers component possession only. Integration, availability and adequacy are the findings of a Functional Adequacy Assessment, never this answer (CD16) |
| CQ-13 | Which of O's capability-bearing claims lack a supporting present-finding assessment? | K1 individuals without a CAP-26 assessment |
| CQ-14 | Which of O's sourcing arrangements have no sourcing assessment of the dependence? | Sourcing statements describing O with no Capability Sourcing Assessment about them |

## 8. Validation

The BCO adds two human tests (G1-T and G1-I), one reasoner gate (D2), an asserted-graph
SHACL pass (C-A), a manifest schema check and generator tests to the existing harness.
Everything else extends gates that already run.

**G1-T — type admission** *(v0.4, R4-02; v0.5, DP-1, DP-2)*. It is asked once per capability
class, with no particular organization in view. A reviewer answers all five questions and
records them against the class. A PASS licenses the Disposition subclass assertion (CAP-04).

1. **Bearer kind.** Is the bearer an Organization? (No → the ability is not a business
   capability. It is a Skill or another Agent Capability, which is CM-02's.)
2. **Basis kind** *(DP-1)*. Can the basis of capabilities of this type be stated as the
   relevant member agent or agents, as organized, without counting any artifact as basis?
   (No, because an artifact is constitutive → OI-14, the socio-technical question a4 keeps
   open. Otherwise → reclassify.)
3. **Through the organization's arrangements** *(b1)*. Do realizations of this type run
   through the organization's arrangements, which may involve a single member, rather than
   one person's skill exercised on their own account? (No → Skill.)
4. **Non-deontic.** Is every index member describable without standing or authorization?
   (No → re-index to the non-deontic act.)
5. **Exercise, not development.** Is every index member an exercise of the capability rather
   than its development (CD5)? (No → remove it, or record the justification.)

Review rules:

- **Worked cases** *(b3)*. Every review works R6's constant-membership cases, the DP-1 table
  in CM-01, and records them.
- **No permanent staging** *(b4)*. A type that fails is reclassified or removed, never left
  staged (CAP-32).
- **No interest condition** *(b2 rejected)*. No sixth question is asked (CD3).

**G1-I — instance attribution** *(v0.4, R4-02; v0.5, DP-2 b5, R5-01)*. It is asked for each
claim that a particular organization bears a capability. The answers are recorded as the
supporting Capability Assessment that CAP-26 requires.

1. **Candidate basis.** Which members or positions ground it (CAP-25)? Name them. Artifacts
   are never named as basis.
2. **Evidence of capacity** *(b5)*. Is there evidence that the organization is able now?
   For example: members with the relevant skills in the positions concerned, the arrangement
   that coordinates them in place, and, where available, a demonstration short of real
   performance (an exercise, a test, a simulation, a qualification).
   - A recorded realization supports the finding but is never required.
   - A finding resting only on past exercise must also show that the basis and arrangement
     are still in place.
   - Organization charts, charters, responsibility assignments and Authorization Records do
     not count.
3. **Who would perform** *(b5)*. Would the realizing acts be performed by the organization's
   own members? (No → record a Capability Sourcing Statement, not a bearing claim.)
4. **Enabling conditions.** Which artifacts and services do the acts depend on, are they
   available, and are there adequate alternatives? Unavailability does not change the
   possession finding. It is an availability matter for the assessments.
5. **Fragility.** Does the capability depend on one indispensable member? Record it; it does
   not change the finding.

Where the evidence cannot settle question 1 or 2, the assessor records no finding (CD14).

**Gate changes**

| Gate | Existing tool | BCO addition |
| --- | --- | --- |
| A Syntax | rdflib | Capability module, fixtures, scope file and coverage register parsed |
| B IRI resolution | rdflib, pinned extracts | CAP-03 (annotation declaration), CAP-05, CAP-13, CAP-22; every CCO, BFO and BPO IRI in this specification verified against the extracts |
| C SHACL | pyshacl, `shapes/` | CAP-01 to CAP-09, CAP-11, CAP-12, CAP-14, CAP-17, CAP-19, CAP-20, CAP-22 to CAP-28, CAP-30 to CAP-34 |
| C-A SHACL on the asserted graph | pyshacl without inference, before any reasoner | CAP-21 |
| G Generator tests (new) | Python tests | CAP-29; the realization index generated from the scope file |
| M Manifest schema (new) | JSON Schema validator | Every completeness manifest matches the CD15 schema |
| D Reasoner | ELK | Unchanged; EL subset only |
| D2 DL reasoner | HermiT | CAP-10 candidates, CAP-16 |
| Query tests | SPARQL | CQ-1 to CQ-14; CAP-18 positive and negative cases |
| F Semantic review | Human | G1-T and G1-I records; CAP-04, CAP-06, CAP-07, CAP-09, CAP-10, CAP-25, CAP-30, CAP-32 |

C-A catches what D2 cannot. Where an `only` restriction exists, a reasoner classifies a
misasserted act into the permitted type, so the check must see asserted types only.

**D2 at release.** D2 runs at release rather than on every commit. On an ordinary commit,
an absent DL reasoner gives SKIP, as Gates B and D do. At a release or acceptance
checkpoint, it is FAIL.

## 9. Migration of existing capability work

BPO holds four capability classes in slice 1.0, about 40 scoped capability names in
`capabilities/`, an agent manifest, and one authorization class. It also declares 145
classes under Organization Capability across its slices (CM-01 Q-12).

- Nothing is re-created in BPO. Each item is a candidate for a BCO formalization tranche,
  or a BPO-side change.
- Raising BPO-side changes with BPO is the architect's call, under `communications/`.

| Item | Current state (BPO) | Change | Rule |
| --- | --- | --- | --- |
| `ex:StrategicPlanningCapability` | Under `cco:ont00000568`; scoped to 6 processes | A candidate for `bco:StrategicPlanningCapability`: take its index from the scope file once OI-20 clears; run G1-T. No `only` without a CAP-30 review | CD3, CD4 |
| `ex:BusinessModelGovernanceCapability` | Under `cco:ont00000568`. Its comment cites "maintain" (1.4.2) and "establish governance" (1.4.3). Absent from the scope file. Carries `obo:BFO_0000054 some ex:P20955` (R5-03) | Index the maintain acts; index 1.4.3 only with a CD5 justification. The existential restriction is removed in BPO before any tranche takes the class (OI-9) | CD5, CD8 |
| `ex:CustomerExperienceManagementCapability` | Under `cco:ont00000568`; scoped to 4 processes; definition says "design and improve" | Review each index member under CD5 before G1-T | CD5 |
| `ex:CompetitiveAnalysisCapability`, bearer | Under `cco:ont00001379`; borne by an analyst | A person's ability: CM-02's subject, and out of this module. Re-homing it under `cco:ont00000089` is BPO's decision | CD1 |
| `ex:CompetitiveAnalysisCapability`, restriction | `some` realization of `ex:P19945` | BPO decision. Recommended: drop `some`; index `ex:P19945`; add `only` only after review | CD4, CD8 |
| Other `capability_scope.json` names | Declarations not located in slice 1.0 | Audit each against CAP-01 to CAP-03, then G1-T | CAP-13 |
| Index entries naming capability classes | 14 of 361 `enablesProcess` entries name classes under Organization Capability, all slice 12.0 (CM-01 Q-12) | Re-indexed in BPO to the acts the functions contain, before any BCO class takes its index from BPO | CD4, CAP-03, OI-20 |
| Shared classes declared inconsistently | 115 classes in two or more BPO modules; 52 with differing definitions; 4 with differing superclasses (CM-01 Q-13) | Which definition governs is BPO's to settle. Validated before Stage 05 | OI-20 |
| Overlapping scopes | Supply Chain Management, Human Capital Management and Financial Management each cover narrower capabilities' processes | Record the narrower capabilities as components in the coverage register. Assert subclass links only after CAP-10 review | CD9, CD16 |
| `capabilities/coverage_register.json` *(new)* | — | Create, keyed by the APQC catalog concept of each standing function | CD16, CAP-22 |
| `capabilities/agents.json` | Software agents listed against Organization Capability classes | Retype as a description-layer manifest using `bco:concernsType`; check consumers first (OI-10) | CD13, CD14 |
| `ex:BusinessAuthorization` | Slice 1.0 declares it under `cco:ont00000751` | BPO-side decision: retype as an Authorization Record, or keep it under the occurred-act convention of CAP-28 | OI-16 |
| v0.4 `ex:concernsType`, `ex:assessedPresence` | Specified with the wrong prefix | Minted as `bco:concernsType` and `bco:assessedPresence` | §0 Prefixes |
| Generated `enablesProcess` / `requiresCapability` | Generated from the scope file | Keep the first as the index; stop generating the second | CD12 |

**Order.** Ratify RP-1 and RP-10 first, because they decide what every G1-T record argues.
Then RP-2 and RP-3, which decide what the scope file generates. Then clear OI-20, and take
the four slice-1.0 classes as the first candidates of a tranche (roadmap §7).

### 9.1 Reconciling the v0.1 `bc:` vocabulary

The reviewer's v0.1 package declares seven classes in
`https://example.org/BusinessCapabilityOntology#`. Neither that namespace nor this one is
published, so the BCO uses a controlled rename, recorded in a migration manifest with old
IRI, new IRI, decision and definition change for each term. No `owl:equivalentClass` is
asserted, because every term's definition changed (TM-5).

| v0.1 class (`bc:`) | BCO class (`bco:`) | Decision |
| --- | --- | --- |
| `BusinessCapability` | `BusinessCapability` | Rename; grounding definition revised (CD2) |
| `BusinessCapabilityDescription` | — | Not carried. Type-level meaning lives in class definitions and catalog nodes (TM-1, OI-17) |
| `BusinessCapabilityMap` | `CapabilityMap` | Rename; entries constrained to assessments and targets |
| `BusinessCapabilityAssessment` | `CapabilityAssessment` | Rename; narrowed to possession findings with a mandatory finding |
| `BusinessCapabilityMaturityAssessment` | `CapabilityAssessment` + `CapabilityMaturityRating` | Split: the evaluation is an assessment; the ordinal result is a rating citing it (TM-4) |
| `BusinessCapabilitySourcingAssessment` | `CapabilitySourcingAssessment` | Rename; now about a sourcing statement, which is a separate class (TM-2) |
| `BusinessCapabilityTargetStateSpecification` | `CapabilityTargetStateSpecification` | Rename; parent moves to `cco:ont00000974` Plan; the end state it serves is a separate `CapabilityTarget` (TM-3) |

The v0.1 target-state class also covered obtaining access to external capacity. That scope
survives: a Target-State Specification may prescribe a sourcing arrangement as one of its
acts.

The v0.1 maturity sample lacks a value, scale and source. It becomes an intentional bad
fixture for CAP-20 until upgraded. The synthetic unexercised-capability sample stays, and
can pass CAP-26 only with evidence of capacity (R5 migration matrix).

## 10. Ratification, open issues and acceptance

Ten decisions need ratification before any requirement is promoted. RP-1 and RP-10 were
decided conceptually through CM-01 (DP-1, DP-2). Ratifying them here confirms that this
text carries those decisions faithfully, not that it reopens them.

**Ratification register**

| ID | Decision | v0.5 proposal | Status |
| --- | --- | --- | --- |
| RP-1 | Grounding boundary (CD1, CD2) | As DP-1 decided: organization-only bearer; basis the relevant member agent or agents as organized, a modeling policy; enabling conditions relevant to realization; the platform-loss commitment; OI-14 open. Departures listed | Carried from DP-1 |
| RP-2 | Realization index (CD4) | Mandatory `ex:enablesProcess` index; no capability class as index member; `only` optional with an exhaustiveness review; CAP-21 and CAP-34 | Revised (R5-05) |
| RP-3 | Enablement relations (CD12) | `ex:enablesProcess` an annotation meaning admissible realization; `requiresCapability` withdrawn | Revised wording (R5-08) |
| RP-4 | Agent manifest (CD13) | Description-layer manifest; the computing artifact an enabling condition only where relevant; what systems bear is CM-02's | Consumers to be checked (OI-10) |
| RP-5 | Namespace | A permanent namespace before release. Provisionally `https://fandaws.com/ontology/bco#` (ADR-003 D1). `ex:` binds BPO only | Open |
| RP-6 | Type references and findings (CD14) | `bco:concernsType`; one assessment pattern; map entries; a mandatory finding; `partial` against an identified criterion; inadequate evidence is no finding | Revised (R5-04, R5-11) |
| RP-7 | Closed-world evidence (CD15) | Authorization Records; JSON completeness manifest; typed validity dates; applicability rules | Revised (R5-07) |
| RP-8 | Functional coverage and adequacy (CD16) | Component possession only; conditional designation of a whole-function class; integration, availability and adequacy as findings of a Functional Adequacy Assessment, never derived | Revised (R9) |
| RP-9 | Information-layer vocabulary (CD17) | Seven description classes, and the Functional Adequacy Assessment as a category whose representation Stage 05 evaluates | Revised (R9) |
| RP-10 | Admission vs attribution (CD3, §8) | As DP-2 decided: G1-T per class (question 3 per b1; b3 and b4 as review rules); G1-I per claim (questions 2 and 3 per b5); no interest condition | Carried from DP-2 |

**Source adequacy.** Under the roadmap's source-adequacy gate, every source this
specification relies on is at V or P in the source register, or under an approved
exception. The exceptions requested:

| ID | Claim | Sources at S or L | Why an exception, not removal | To close by |
| --- | --- | --- | --- | --- |
| SE-1 | CD1: these frameworks admit bearers other than organizations | ArchiMate 3.2 (SRC-OG-03), TM Forum GB1029C (SRC-IND-04), ISO 9000:2015 3.6.12 (SRC-ISO-05), ITIL (SRC-IND-06) | They only add to a departure the V and P sources already establish. If they are excluded, the departure stands, but its list is incomplete | Before CP-0: read each primary or drop it from the list |
| SE-2 | CD2: DM2 counts technology inside the capability | DoDAF DM2 (SRC-GOV-01) | It only adds to SF-06, which NAF and UAF already establish at V | Before CP-0 |

No claim here rests on a source at K. Management-literature definitions recorded at K
(SRC-MS-05, SRC-MS-06 and others) are not cited.

**Open issues**

- **OI-1** Pin every dependency by content hash for an executable release. The vendored
  extracts are pinned; an executable release is not yet.
- **OI-4** No relation yet links a development act to the capability it brings about. CQ-11
  is answered by review records until one is chosen (roadmap F-6).
- **OI-6** Locate the declarations of `enablesProcess` and `requiresCapability` in BPO
  (roadmap F-9).
- **OI-7** The staging state (CD3) sits outside BFO's role/disposition split. It is bounded
  by CAP-32 and counted by CQ-10 (roadmap F-10).
- **OI-8** *(widened)* Verify against the pinned closure every CCO and BFO IRI taken from
  reviews, and add BFO's *has member part* and *has participant* to the extracts before
  CAP-25 or CAP-34 uses them (roadmap F-8).
- **OI-9** *(confirmed)* `obo:BFO_0000054 some ex:P20955` exists on
  `ex:BusinessModelGovernanceCapability` at the inspected BPO `main` (R5-03). It is removed
  in BPO, and other slices are checked, before any tranche takes the class (roadmap F-11).
- **OI-10** Changing `agents.json` may affect whatever consumes it for routing. Check
  consumers before RP-4 lands (roadmap O-13).
- **OI-11** The evidence-graph IRIs, and whether the manifest reuses the closed-world rule
  form of the house specification standard (roadmap F-13).
- **OI-13** Fix the schema and versioning of the coverage register, including whether a
  function's components may themselves be functions (roadmap F-14).
- **OI-14** A socio-technical system bearer, a material entity whose parts include both
  members and artifacts, for a type whose review shows an artifact is constitutive. Kept
  open by DP-1 a4; no current type needs it (roadmap F-15).
- **OI-15** *(answered conceptually)* An adequacy statement about a function with no
  capability class of its own is a Functional Adequacy Assessment directed at the Standing
  Function (CD16, CD17). Its representation is open (roadmap F-7).
- **OI-16** *(BPO-side)* `ex:BusinessAuthorization ⊑ cco:ont00000751` in slice 1.0 entails a
  permitted process for every business authorization BPO records (roadmap F-12).
- **OI-17** If capability dictionaries must travel as versioned information artifacts,
  revisit TM-1 (roadmap F-18).
- **OI-18** Multi-party sourcing (brokers, intermediaries, provider networks) is outside the
  two-party record (roadmap F-17).
- **OI-19** *(narrowed)* R5 confirms that CCO's Plan has continuant part some Objective. The
  vendored extract carries no restrictions, so this is confirmed against a rebuilt extract at
  Stage 05.
- **OI-20** *(new)* BPO integration dependencies: index entries that name capability
  classes (CM-01 Q-12), inconsistent shared-class declarations (Q-13), and slice act types
  not yet vendored (Q-14). Resolved before formal implementation (CM-01 approval guidance;
  roadmap O-9).
- **OI-21** *(new)* Revocation and supersession of Authorization Records need a
  representation. Until there is one, a graph holding such a record is not declared
  complete (CD15).
- **OI-22** *(new)* The ordinal value encoding of a maturity rating, and the representation
  of the Functional Adequacy Assessment and of its findings (R5-02, CD17; roadmap F-7).

**Known limits (0.5)**

- A capability persists when an enabling artifact is lost. The loss shows only as
  unavailability in an assessment, unless members' capacity is lost with it (CD2).
- No temporal qualification of has capability. CQ-4 asks about capabilities borne at query
  time.
- No capability parthood. Overlap is handled by reviewed specialization and the coverage
  register.
- No degrees of capability in the reality layer. Maturity lives in ratings of existing
  instances.
- Type references, the sourcing convention and the realization index are annotations or
  conventions, so a reasoner draws nothing from them. SHACL is their only enforcement.
- Absence answers are only as good as the manifests behind them.
- Person-borne, member-wise and artificial-system abilities are outside this module (CM-02).

**Acceptance checkpoints**

- [ ] **CP-0**: all of the following.
  - The practitioner review is recorded, and its accepted dispositions are carried into
    §0.3.
  - CM-02's approved scope is carried (done in v0.5: §1, CD1, CD13).
  - The R5 dispositions are accepted.
  - The source-adequacy exceptions are approved or closed.
  - RP-1 to RP-10 are ratified, and ADR-002 is accepted.
  - The permanent namespace is decided (RP-5).
- [ ] **CP-1**: the first tranche's classes are formalized with their index.
  - Every fixture checked by Gates B, C, C-A, G and M fails as stated, including CAP-21 and
    CAP-25 to CAP-34.
  - Gates A to D are green.
  - Requirements marked *encoding at Stage 05* have their encoding chosen.
- [ ] **CP-2**: Gate D2 has run, with an absent reasoner counted as FAIL.
  - The CAP-10 and CAP-16 fixtures fail as stated.
  - CQ-1 to CQ-14 are answered over a fixture organization, with CAP-18's positive and
    negative cases.
- [ ] **CP-3**: every scope entry is audited, with a G1-T record or an explicit staging
  status.
  - The coverage register is populated.
  - The `bc:` migration manifest is complete.

## Sources

Every external work is cited by its identifier in the source register,
`docs/sources/register.yaml`, with the evidence status recorded there (V, P, S, K, L).
Findings SF-01 to SF-10 are in `docs/sources/register-companion.md`.

| Register ID | Work | Status | Cited for |
| --- | --- | --- | --- |
| SRC-ISO-01 | ISO/IEC 21838-2:2021, BFO 2020 (OWL) | V (OWL) | Disposition, realizable entity, function, has material basis (CD2, CD3, CD6) |
| SRC-FO-01 | Common Core Ontologies v2.0 | V | Organization, Agent Capability, Organization Capability, Skill, the relations of §5 |
| SRC-FO-02 | IOF Core 202603 | V | Capability under disposition; any independent continuant as bearer; interest condition (CD1, CD3) |
| SRC-FO-03 | Beverley et al., *Capabilities: An Ontology* | V | Capability under disposition; interest condition (CD3) |
| SRC-FO-09 | Uschold et al., *The Enterprise Ontology* | V | SKILL as a person's capability (CD1) |
| SRC-OMG-01 | VDML 1.1 | V (entry) | Bearer departure (CD1) |
| SRC-OMG-03 | BACM 1.1 | V | OrgUnit including individuals; PerformerRole (CD1) |
| SRC-OMG-04 | UAF Domain Metamodel 1.3 | V | CapableElement; Personnel Competence; Capability Configuration (CD1, CD2) |
| SRC-GOV-04 | NAF v4.1 | V | Capability Configuration (CD1, CD2) |
| SRC-ISO-02 | ISO 19440:2020 | P (clause 3) | Capability construct, 3.6 (CD1) |
| SRC-IND-01 | APQC Process Classification Framework | P | Technology on the capability side (CD2); the catalog bridge |
| SRC-OG-02 | TOGAF Series Guide G211 | P; L | Technology on the capability side (CD2) |
| SRC-OG-03, SRC-IND-04, SRC-ISO-05, SRC-IND-06, SRC-GOV-01 | ArchiMate 3.2; TM Forum GB1029C; ISO 9000:2015; ITIL; DoDAF DM2 | S (and L) | Under exceptions SE-1 and SE-2 |

**Repository sources**

- CM-01, approved: `src/02_conceptual_models/CM-01-business-capability.md`.
- Decision records: DP-1, DP-2, the CM-01 approval, the stakeholder-review erratum, the
  re-pin, the roadmap direction, D2 and D3 authorization, the CM-02 scope approval, all
  under `docs/decisions/`.
- The CM-02 scope note: `docs/proposals/2026-10-31-cm02-scope-note.md`.
- Reviews and dispositions: `reviews/R5-v0.4-artifact-review.md`; `reviews/R8-disposition.md`;
  `reviews/R9-disposition.md`.
- The roadmap: `docs/ROADMAP.md`, revision 2.
- The previous version: `specifications/Business-Capability-Ontology-v0.4.0-draft.1.md`,
  whose §0.1 to §0.3 hold the R2 to R4 dispositions.
- BPO, at the commit pinned in `config/upstream-sources.yaml`: `ontology/apqc-ext.ttl`;
  slice 1.0; `capabilities/capability_scope.json` and `agents.json`; ADR-001.
