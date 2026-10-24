# Ontological Review and Critique: Business Capability Ontology (BCO) Vocabulary

Revision recommended before ratification

## 1. Executive Assessment

Overall judgment: The proposed Business Capability Ontology (BCO) demonstrates considerable ontological discipline and a coherent architectural direction. However, several foundational modeling decisions require clarification or revision before the vocabulary should be ratified as BFO/CCO-conformant.

The most consequential issues concern the nature of a Business Capability as a disposition, its material basis, the distinction between capability types and capability instances, and the treatment of capability assessments, maps, and targets as Information Content Entities.

The document contains 14 proposed concepts organized into two SKOS concept schemes: five business capabilities in the catalog and nine supporting metamodel concepts.

### Assessment by dimension

| Dimension                          | Assessment                                              |
| ---------------------------------- | ------------------------------------------------------- |
| BFO upper-ontology alignment       | Promising, with important unresolved commitments        |
| CCO reuse and subclassing          | Strong foundation; formal mappings require verification |
| Ontological definitions            | Generally clear but sometimes unnecessarily restrictive |
| Class-versus-instance discipline   | Needs substantial clarification                         |
| Relations and realization modeling | Several critical design questions                       |
| Inclusiveness and exclusiveness    | Uneven, especially among catalog capabilities           |
| Provenance and traceability        | Strong documentation; evidence strength varies          |
| Readiness for ratification         | Not yet recommended                                     |

### Principal conclusion

I would retain the core architecture but revise its ontological commitments before ratification.

Three decisions are especially worth preserving:

- A Business Capability is something an organization has, not an activity it performs.
- An assessment or rating of a capability is not the capability itself.
- A target for acquiring a capability does not entail that the capability already exists.

These distinctions are valuable and broadly compatible with BFO and CCO.

The principal risk is that the ontology may translate useful business architecture conventions into overly restrictive ontological definitions, thereby excluding legitimate organizational capabilities or creating unnecessary dependencies on a particular management methodology.

The review below distinguishes what is supported by the provided BFO 2020 and CCO 2.0 reference files from what remains unverified in the BCO's actual Turtle and OWL implementation.

## 2. Foundational Ontological Issues

### Finding 1 — Business Capability as a Disposition

Severity: High — requires explicit architectural justification

The proposed definition states:

> An Organization Capability that is a Disposition inhering in an Organization, whose material basis is constituent member agents of that organization in their organizational arrangement, and that, when realized, is realized in Planned Acts of the types in its realization index.

The superclass selection is defensible.

The provided CCO Agent Ontology identifies:

| Existing class          | IRI               | Ontological classification        |
| ----------------------- | ----------------- | --------------------------------- |
| Organization Capability | `cco:ont00000568` | Subclass of Agent Capability      |
| Agent Capability        | `cco:ont00001379` | Subclass of BFO Realizable Entity |
| Disposition             | `BFO_0000016`     | Subclass of BFO Realizable Entity |
| Organization            | `cco:ont00001180` | Subclass of Group of Agents       |

CCO defines an Organization Capability through the organization's capacity to realize the capability in intentional acts.

The BCO adds the stronger assertion that every Business Capability is specifically a BFO Disposition.

This is not automatically inconsistent with CCO, since CCO places Agent Capability under Realizable Entity rather than explicitly requiring that every Agent Capability be a Disposition.

However, it is a substantive ontological commitment, not merely terminological refinement.

BFO dispositions are internally grounded realizable entities whose realizations depend on the physical makeup of their bearers. For an organization, this raises difficult questions about whether its capacity arises from the constitution of its members, institutional organization, or some combination.

For example, an organization may have employees with the necessary expertise but lack authorization, contractual access, or coordination to perform a particular activity.

The BCO needs to distinguish:

Possessing the capability, having authorization to exercise it, and having the current circumstances necessary for its realization.

These are not equivalent.

Recommendation: Retain Disposition as the working parent, but make the criteria for an organization-borne disposition explicit. Test the modeling choice against cases where organizational membership remains constant but authority, procedures, resources, or coordination change.

The classification is defensible, but its validity should be established through these cases rather than assumed from business architecture usage.

### Finding 2 — Restricting the Material Basis to Member Agents

Severity: Critical — central architectural weakness

The document deliberately excludes technology, equipment, and facilities from the material basis of a Business Capability, describing them instead as enabling conditions.

This distinction is too categorical.

BFO's existing relation `has material basis` (`BFO_0000218`) connects a Disposition to a Material Entity that is a continuant part of its bearer and in virtue of whose parthood the disposition exists.

The restriction therefore has a precise ontological meaning. A material basis cannot simply mean whatever the architecture considers an organizational resource.

Consider a company whose essential production capability depends on a specialized machine, or a financial institution whose transaction-processing capability depends on a configured technical system.

If the system is permanently removed, does the organization still possess the same capability, albeit in an unavailable state? Or has the underlying capacity actually ceased to exist?

The answer cannot be stipulated uniformly for every capability.

The present wording risks making a capability independent of resources that are constitutive of the organization's ability to exercise it.

Recommendation: Replace the universal member-only material-basis restriction with a more carefully justified principle.

The ontology should distinguish material constitution, organizational configuration, necessary enabling conditions, and temporary realization constraints. These distinctions should be represented using existing BFO/CCO relations where applicable, rather than introducing a new object property.

The documented `has material basis` relation should only be asserted where its full BFO definition is satisfied.

An important qualification is necessary here: CCO defines an Organization as a Group of Agents, and a Group of Agents as an Object Aggregate whose parts are Agents. Consequently, equipment should not simply be asserted as part of the organization to solve this problem. The BCO is right to distinguish organizational members from external resources.

The issue is whether the selected material basis and enabling conditions adequately explain the existence and persistence of each capability.

### Finding 3 — Capability Types Versus Capability Instances

Severity: Critical — the most important formal modeling issue

The vocabulary employs several different representations of a capability:

| Representation        | Example                                                     | Ontological role                                    |
| --------------------- | ----------------------------------------------------------- | --------------------------------------------------- |
| Capability type       | Competitive Analysis                                        | A kind of organizational capability                 |
| Capability instance   | A particular firm's competitive analysis capability         | A disposition inhering in a particular organization |
| SKOS concept          | `bcoc:CompetitiveAnalysis`                                  | A controlled-vocabulary concept                     |
| Capability assessment | An evaluation of whether the firm possesses that capability | An Information Content Entity                       |
| Capability target     | A requirement that the firm acquire the capability          | An Objective                                        |

These entities are not interchangeable.

The document introduces the catalog's five capabilities as SKOS concepts, whereas its metamodel terms have separately designated `bco:` classes.

For example, `bcoc:CompetitiveAnalysis` is explicitly given as a catalog concept IRI, but the excerpt does not identify a corresponding OWL class.

That distinction matters.

An organization does not literally bear a SKOS concept as a BFO Disposition. It bears an instance of an appropriately defined capability class.

Similarly, an assessment concerning a capability type cannot automatically use the same object-property pattern as an assessment about an existing capability instance.

Required clarification: Determine whether the five catalog entries are intended to be OWL classes, SKOS concepts indexing OWL classes, or controlled vocabulary concepts without corresponding OWL classes.

The BCO must also specify how its assessments, targets, and sourcing statements refer to a capability type. An OWL class is not automatically an ordinary BFO Entity instance to which `is about` can be applied.

Possible representations must be assessed under the existing CCO/BFO vocabulary and OWL modeling rules. Simply using the same label for a concept and a class does not establish ontological identity.

I would make this a ratification-blocking issue.

### Finding 4 — The Realization Index

Severity: High

The Business Capability definition ends with:

> ... realized in Planned Acts of the types in its realization index.

This introduces an important modeling dependency without explaining its ontological status.

The phrase "realization index" could denote a table of mappings between capability classes and Planned Act classes, an information artifact used to specify realization patterns, or a collection of formal OWL restrictions.

Those alternatives have different semantics.

In particular, a capability is a realizable entity even when it has never been realized. BFO does not require an actual realization for a disposition to exist.

Consequently, an OWL existential restriction requiring every Business Capability instance to have an actual realization would be too strong if the intended model includes dormant capabilities.

The appropriate existing BFO relations include:

| Relation           | IRI           | Application                                                                      |
| ------------------ | ------------- | -------------------------------------------------------------------------------- |
| has realization    | `BFO_0000054` | Connects a realizable entity to an actual realization                            |
| realizes           | `BFO_0000055` | Connects a process to a realizable entity that it realizes                       |
| has material basis | `BFO_0000218` | Identifies the material basis of a disposition when the defining conditions hold |

The realization index can describe intended or possible realization types without asserting that all those realizations have actually occurred.

Recommendation: Specify whether the index is descriptive metadata, a formal class mapping, or both. Keep possible realizations separate from actual realizations.

No new object property is justified at this stage.

## 3. Critique of the Five Catalog Capability Definitions

The principal problem across these entries is excessive use of particular activities as defining characteristics of the capability.

Examples of activities are useful, but an exhaustive list of management practices can inadvertently become a necessary condition of class membership.

| Capability                     | Assessment           | Principal concern                                                                                         |
| ------------------------------ | -------------------- | --------------------------------------------------------------------------------------------------------- |
| Business Model Governance      | Revise               | The definition makes maintenance and revision central and distinguishes initial establishment too rigidly |
| Competitive Analysis           | Significant revision | The internal coordination requirement excludes potentially valid organizational capabilities              |
| Customer Experience Management | Revise               | Requires a particular collection of strategy, assessment, and design activities                           |
| Strategic Planning             | Revise               | Overly prescriptive about mission, vision, and organizational planning structure                          |
| Treasury Management            | Significant revision | Ties capability identity to particular treasury practices, investment policies, and hedging strategies    |

### 3.1 Business Model Governance

The distinction between developing a capability and realizing an existing capability is useful.

However, the definition's assertion that acts first establishing oversight are not realizations of the capability requires care.

An organization could already possess a capacity for governance and exercise it when establishing a new business-model governance arrangement. Conversely, it might acquire that capacity through the establishment activity.

The character of the particular act does not, by itself, settle whether the capability already exists.

Suggested revised definition:

> A Business Capability that is realizable in Planned Acts by which an Organization evaluates, maintains, or directs changes to its Business Models.

This is a provisional formulation. "Business Model" would need to be resolved to an authorized class or carefully defined business-domain concept before formal encoding.

The distinction between acquisition and realization should be explained in the specification rather than embedded as an absolute exclusion in the class definition.

### 3.2 Competitive Analysis

The present definition requires analysis to be:

> ... carried out through coordinated work among its own members rather than resting on one analyst's skill alone.

This confuses an organizational capability with one particular organizational realization arrangement.

Consider an incorporated consulting company employing one analyst who performs competitive analysis for the company.

If the organization genuinely bears the relevant disposition, the fact that only one member performs the analysis should not automatically exclude the case.

Likewise, an organization may retain an internally grounded capability to direct, integrate, and evaluate competitive intelligence while obtaining some underlying research externally.

Suggested revised definition:

> A Business Capability that is realizable in Planned Acts by which an Organization obtains and analyzes information about actual or potential competitors for use in organizational decision-making.

The analysis should determine whether this captures the intended capability without conflating it with a person's Skill.

The decisive criterion should be the bearer and its capacity, not the number of individuals executing the work.

### 3.3 Customer Experience Management

This definition requires the organization to appraise customer experiences, set a customer-experience strategy, and design interactions and supporting structures.

These activities are related, but a capability need not necessarily encompass all of them.

A company might possess a well-developed ability to manage customer interactions without having a separately articulated customer-experience strategy.

The definition should establish whether the BCO intends an integrated, enterprise-wide capability or a broader capability to manage customer experience.

Suggested revised definition:

> A Business Capability that is realizable in Planned Acts by which an Organization evaluates and directs the management of its interactions with customers in relation to their experiences.

This avoids prescribing a particular strategy-development methodology.

### 3.4 Strategic Planning

The current definition requires mission statements, long-term vision, and enterprise-wide and business-unit strategies.

Those characteristics are common in formal strategic-management systems, but they are not universal.

An organization may conduct strategic planning without business units, formal mission statements, or long-range planning documents.

Suggested revised definition:

> A Business Capability that is realizable in Planned Acts by which an Organization formulates or revises its objectives and strategies for future organizational action.

This should be checked against CCO's existing `Objective` and `Plan` classes and against the boundary between strategic planning and broader organizational planning.

### 3.5 Treasury Management

The current definition requires financial oversight, cash tracking and reconciliation, investment policy, and hedging strategy.

These are recognizable treasury activities. Nevertheless, requiring all of them appears overly restrictive.

For instance, a small business may effectively manage liquidity, cash, and financial obligations without engaging in hedging activities.

Suggested revised definition:

> A Business Capability that is realizable in Planned Acts by which an Organization manages its cash positions, liquidity, funding, and financial exposures in support of its financial obligations and objectives.

This still requires testing against accounting, financial reporting, investment management, and financial risk management.

### Catalog-wide recommendation

The five revised definitions are candidates for further testing, not final OWL-ready definitions.

They should each be evaluated for necessary and sufficient distinguishing characteristics. Conjunctive or disjunctive wording should be formalized only after checking its effect on class membership.

The BCO should also decide whether its catalog represents a mutually exclusive capability taxonomy or an intentionally overlapping classification system. These are not equivalent design goals.

## 4. Critique of the Nine Metamodel Concepts

The metamodel is more ontologically mature than the capability catalog. In particular, its use of Information Content Entities to represent assessments, targets, and plans is generally sound.

Nevertheless, several definitions leave important semantic distinctions unresolved.

| Metamodel concept                     | Assessment        | Required improvement                                                                        |
| ------------------------------------- | ----------------- | ------------------------------------------------------------------------------------------- |
| Authorization Record                  | Sound direction   | Distinguish documented authorization from the authorization or role itself                  |
| Business Capability                   | Major revision    | Resolve material basis, bearer, type-reference, and realization questions                   |
| Capability Assessment                 | Major revision    | Define the meanings of presence, absence, and partial presence                              |
| Capability Map                        | Major revision    | Clarify descriptive versus prescriptive information and the purpose of the map              |
| Capability Maturity Rating            | Generally sound   | Specify the assessed attribute, scale, and measurement basis                                |
| Capability Sourcing Assessment        | Moderate revision | Clarify dependence and the assessment's necessary characteristics                           |
| Capability Sourcing Statement         | Moderate revision | Clarify provider cardinality and the distinction between description and actual arrangement |
| Capability Target                     | Strong            | Formalize reference to capability type and target conditions                                |
| Capability Target-State Specification | Strong            | Clarify how the Plan incorporates its Objectives                                            |

### 4.1 Authorization Record

The class is appropriately placed under CCO's Descriptive Information Content Entity.

However, an authorization record and the authorization it records are ontologically distinct.

The existence of a document stating that an agent is authorized does not necessarily make the authorization valid or effective.

CCO already supplies the Organization Member Role class (`cco:ont00000175`) and the BFO framework for roles.

Recommendation: Preserve the descriptive character of the Authorization Record. State explicitly that the record provides information about authorization and does not itself establish that the agent currently bears an authorization-conferring role.

If the ontology must represent the actual authorization, first examine existing CCO roles, directives, and relations rather than introducing a new object property.

### 4.2 Capability Assessment

The most problematic phrase is:

> ... presence, absence or partial presence of a capability of one given type ...

The meaning of partial presence is unclear.

A particular disposition either exists or does not exist at a given time. However, an organization can exhibit varying levels of readiness, operational availability, reliability, or proficiency in relation to a capability type.

Those measures must not be collapsed into the ontological existence of the disposition.

For example, a manufacturer might possess a production capability that is temporarily unavailable because of a power outage. This does not necessarily mean the capability is only partially present.

Alternatively, a capability category may contain several distinguishable subcapabilities, only some of which are present.

In that case, partial presence may be an assessment of a collection of capability types rather than a property of one capability instance.

Recommendation: Specify precisely whether partial presence refers to an incomplete capability configuration, an aggregation of subcapabilities, or a graded assessment of operational capacity.

Also specify the assessed organization, capability type, temporal context, and evidential basis.

A particularly important OWL consideration is that absence cannot ordinarily be inferred merely because an existing capability assertion is missing. Under OWL's open-world semantics, not knowing that a capability exists is not equivalent to knowing that it is absent.

An explicit assessment of absence is legitimate as an Information Content Entity, but the assessment should not be mistaken for an automatically established ontological fact.

### 4.3 Capability Map

The proposed definition is:

> A Descriptive ICE that describes an organization and has, as continuant parts, the Capability Assessments and Capability Targets that are its entries.

This differs intentionally from conventional capability maps that primarily organize capability types into taxonomies or decompositions.

That architectural decision is permissible, but it deserves closer scrutiny.

The BCO appears to divide the representation into two components: a catalog classifying capability types and an organization-specific map describing capability assessments and targets.

That distinction is useful.

However, the map combines two kinds of information:

- Capability Assessments are descriptive.
- Capability Targets are Objectives and therefore directive.

In CCO, Descriptive Information Content Entity (`cco:ont00000853`) and Directive Information Content Entity are distinct categories.

A Descriptive ICE having a Directive ICE as a part does not by itself create an OWL contradiction. Nevertheless, the intended meaning of the whole needs clarification.

Recommendation: Define whether the map is a description of an organization's current capability state, a representation of both current and desired states, or an integrated management artifact containing descriptive and directive entries.

The existing BFO `has continuant part` relation (`BFO_0000178`) is relevant, but use of that relation alone does not settle the classification question.

### 4.4 Capability Maturity Rating

This concept is comparatively strong.

The proposed parent, Ordinal Measurement Information Content Entity (`cco:ont00001010`), is supported by the supplied CCO Information Entity Ontology.

CCO also provides:

`cco:ont00001811` — is a ordinal measurement of

This relation can connect an ordinal measurement to the entity being measured, subject to its defined semantics.

The main concern is not its BFO placement but the meaning of maturity.

Does the rating measure the capability's reliability of realization, its operational performance, its organizational institutionalization, or something else?

These are potentially different measurement dimensions.

Recommendation: Retain the class as an Ordinal Measurement ICE, but require the specification of the ranking criterion, ordinal scale, applicable time, and evidence.

Do not treat a maturity rating as though it were an intrinsic quality inhering in the disposition itself.

### 4.5 Capability Sourcing Assessment

This is an appropriate candidate for a Descriptive ICE.

Its differentia, however, enumerates operational risk, substitutability, and internal capability availability.

The language may imply that every assessment must address all three.

If these are mandatory, the specification should say so. If they are examples of assessment criteria, they should not be made necessary conditions of the class.

The document should also distinguish the consumer's dependence on a supplier from the consumer's dependence on a sourcing arrangement.

These can differ when multiple providers or substitutions are available.

### 4.6 Capability Sourcing Statement

The definition confines each statement to performances of one Planned Act class obtained from one other Organization.

This may be an intentional normalization choice, and it can work.

However, the ontology should specify how it represents arrangements involving several providers, several act types, or changes in suppliers over time.

It should also distinguish the existence of an actual sourcing arrangement from the existence of an Information Content Entity describing that arrangement.

The statement may be inaccurate, outdated, proposed, or conditional. Its existence does not establish that the described sourcing relationship currently exists.

### 4.7 Capability Target

This is among the best modeled terms in the document.

CCO's Objective (`cco:ont00000476`) is a Directive Information Content Entity prescribing a projected state that an agent intends to achieve.

A requirement for an organization to come to possess a particular capability fits this structure.

The key unresolved question is how the Objective formally refers to the desired capability type without requiring a corresponding capability instance to exist already.

Recommendation: Preserve the definition and resolve its class-reference mechanism.

### 4.8 Capability Target-State Specification

This is also well aligned with CCO.

CCO defines Plan (`cco:ont00000974`) as a Directive Information Content Entity prescribing intended acts for achieving an Objective. Its formal axioms include a requirement for a continuant part that is an Objective.

Consequently, the BCO's requirement that a target-state specification contain Capability Targets is consistent with the existing Plan pattern.

The remaining work is to distinguish the intended acts from their actual realizations and to clarify how multiple objectives are incorporated.

No new object property appears necessary.

## 5. SKOS and OWL Architecture

Severity: High

The coexistence of SKOS concept schemes and BFO/CCO OWL classes is not inherently problematic.

It can be a valuable design pattern, particularly when an ontology must serve both knowledge representation and business vocabulary management.

However, the document needs to make the purpose of each representation explicit.

Recommended conceptual separation

OWL ontology layer

Defines types of entities, subclass relationships, dispositions, information entities, and the object properties between their instances.

Explicitly documented correspondence

SKOS vocabulary layer

Organizes catalog concepts, preferred labels, definitions, alternative labels, and navigational relationships.

This separation raises four verification questions.

First, does every catalog capability concept correspond to a formally declared OWL class, or are some concepts purely classificatory?

Second, how does the BCO distinguish an OWL subclass assertion from a `skos:broader` relationship? These relations do not have identical semantics.

Third, how are capability types referenced by assessments and targets? A SKOS concept identifying a type must not inadvertently be treated as the corresponding instance of a disposition.

Fourth, are the class definitions and SKOS definitions synchronized without conflating the two resources?

The excerpt does not provide enough formal triples to answer these questions.

The architecture may already implement them correctly, but the generated vocabulary page alone is not evidence that the OWL semantics are correct.

## 6. Provenance and Standards Compliance

The provenance documentation is a notable strength.

The BCO records sources, different forms of alignment and departure, drafting agents, and provisional statuses. It also acknowledges when a cited source was available only as an abstract, summary, or preview.

This level of documentation is useful for ontology governance.

There are nevertheless three concerns.

### 6.1 Consistency is not necessarily formal support

The designation `consistent-with` is sometimes applied to sources that support the general business capability perspective rather than the precise proposed definition.

For example, agreement with the distinction between capabilities and processes does not establish that the specific definition of Treasury Management is ontologically complete.

The provenance model would benefit from distinguishing direct definitional support from general contextual consistency.

### 6.2 Reference versions must be reconciled

The BCO cites CCO releases and development versions through August 2026.

The supplied CCO 2.0 reference PDFs are principally dated November 2024.

I verified relevant BFO/CCO distinctions against those supplied PDFs, including Organization Capability, Agent Capability, Skill, Plan, Objective, Planned Act, and Ordinal Measurement ICE.

I have not established that all claims about the referenced 2026 CCO versions or other external standards are accurate. That requires the exact referenced source artifacts.

Before ratification, the BCO should identify its authoritative imported versions and verify that all class IRIs, property IRIs, axioms, and definitions match those versions.

### 6.3 Provenance should distinguish authorship from approval

The document appropriately distinguishes an AI drafting agent from the human authority responsible for ratification.

However, a draft's provenance does not establish that its definitions have passed conceptual or logical validation.

The ratification process should separately record editorial approval, ontological approval, and successful automated validation.

## 7. Recommended Ratification Tests

I recommend conducting the following tests before approving the vocabulary.

| Test                          | Required result                                                                                                |
| ----------------------------- | -------------------------------------------------------------------------------------------------------------- |
| 1. Class identity             | Every proposed class has an unambiguous IRI, parent class, and intended ontological category                   |
| 2. Catalog alignment          | Every SKOS capability concept has a documented relationship, if any, to an OWL class                           |
| 3. Disposition persistence    | The model distinguishes temporary inability to perform from loss of a capability                               |
| 4. Material basis             | Every asserted material basis satisfies BFO's material-basis relation                                          |
| 5. Non-realized capability    | An organization may possess a capability without having previously realized it                                 |
| 6. Absence assessment         | A negative assessment can be recorded without treating missing OWL information as proof of absence             |
| 7. Capability type target     | An Objective can identify a desired capability type without asserting an existing capability instance          |
| 8. Sourcing                   | Multiple suppliers and externally executed acts can be represented without inconsistent capability attribution |
| 9. Information classification | Assessments, Objectives, Plans, and Maps retain their correct CCO categorizations                              |
| 10. Logical consistency       | The integrated ontology is checked using an OWL 2 reasoner and appropriate validation constraints              |

Of these, tests 2, 3, 4, 5, and 7 are particularly important because they test the central capability model rather than merely the supporting administrative vocabulary.

Reasoner consistency is necessary but insufficient: a logically consistent ontology can still encode an incorrect account of business reality.

## 8. Priority of Recommended Changes

### 1

Resolve capability type and instance representation

Specify the formal relationship between OWL capability classes, SKOS catalog concepts, and capability instances. This underpins assessments, targets, sourcing, and maps.

### 2

Finalize the disposition and material-basis commitments

Demonstrate that the proposed restrictions correctly distinguish capability possession, organizational constitution, and enabling conditions.

### 3

Formalize the realization index

Explain how possible realization types are represented without requiring actual realizations of every capability instance.

### 4

Revise the five catalog definitions

Remove unnecessary implementation-specific conditions and test their inclusiveness and exclusiveness.

### 5

Clarify information entities and provenance

Resolve assessment states, map composition, rating semantics, source-version traceability, and authority for approval.

## 9. Final Ontological Judgment

The BCO is a credible draft, and its separation of organizational abilities from business activities and information artifacts is fundamentally worth preserving.

I particularly support using CCO Organization Capability as the starting point, distinguishing capability possession from capability maturity, representing acquisition targets as Objectives, and representing plans as directive information rather than as the processes they prescribe.

My strongest reservation concerns the attempt to make a single model of organizational capability simultaneously satisfy a precise BFO dispositional account and a highly specific business architecture methodology.

These perspectives are compatible only when their assumptions are made explicit and tested.

In particular, an ontology should not make something a necessary characteristic of a capability merely because it is customary, desirable, or prescribed by a particular management framework.

Final recommendation: Do not ratify the current vocabulary unchanged. Preserve its architecture, resolve the formal class/type and realization issues, test the material-basis commitments, and revise the capability definitions for greater ontological generality.

The next most valuable review would be of the actual generated Turtle/OWL, not merely the vocabulary page. That would allow verification of subclass axioms, object-property domains and ranges, SKOS mappings, OWL restrictions, and consistency against the exact imported BFO/CCO versions.
