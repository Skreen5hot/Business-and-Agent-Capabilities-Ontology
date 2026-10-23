# OMG and ISO standards as authoritative sources for "capability" / "business capability"

Scope: OMG VDML, BMM, BACM, UAF; ISO 15704, 19439, 19440, ISO/IEC/IEEE 42010, ISO/IEC 21838-2 (BFO), ISO 9000, ISO 22301; ISO/IEC 330xx and CMMI process capability. Research date: 2026-10-23.

BCO commitments these entries are checked against:
- **C1**: a Business Capability is a BFO disposition borne by an Organization, not by a person, system or role.
- **C2**: its material basis is the organization's member agents in their arrangement.
- **C3**: it is realized in business processes, whose act types come from BPO/APQC PCF.
- **C4**: having an ability is distinct from being assigned, authorized or responsible.
- **C5**: maps, assessments, maturity ratings, sourcing statements and target states are information content entities (ICEs) about capabilities, not the capabilities themselves.

Method note: I downloaded the OMG PDFs (VDML 1.1, BMM 1.3, BACM 1.1, BACM 1.2 beta, UAF 1.3 DMM) and extracted their text with pdftotext. Every clause number given for an OMG source was read in the document itself. For ISO sources I read only the free iTeh preview of ISO 19440:2020 (Foreword, Introduction, Clause 3 up to entry 3.51) and the public ISO catalogue pages. Any ISO claim not drawn from those pages is marked unverified or listed as a gap. ISO text is paraphrased throughout. Each source has at most one verbatim quotation, under 15 words.

Licence summary for OMG specifications: all of the OMG documents above carry the standard OMG "USE OF SPECIFICATION – TERMS, CONDITIONS & NOTICES" front matter, as read in the PDFs. The specifications are free to download. The licence lets you use the specification to create and distribute software and special-purpose specifications based on it. You may copy and distribute the specification only if:
- the copyright and permission notices are kept;
- the use is informational, with no posting on network computers and no commercial resale;
- the specification is not modified.

So redistributing a whole OMG PDF (for example, vendoring it into a public repository or site) is not permitted. Short attributed quotation and paraphrase in a derived specification are consistent with the licence's grant to build "special purpose specifications". The IPR mode for VDML and BACM is "Non-Assert" ([OMG VDML page](https://www.omg.org/spec/VDML/); [OMG BACM page](https://www.omg.org/spec/BACM)).

Licence summary for ISO standards: ISO standards are paid, copyrighted documents ("© ISO 2020 – All rights reserved" on ISO 19440:2020, per the [iTeh preview](https://cdn.standards.iteh.ai/samples/74491/2045fbd5664f4ea387f29eaa07fd903e/ISO-19440-2020.pdf)). They cannot be redistributed. Definitions must be paraphrased, or quoted only briefly with attribution. The ISO Online Browsing Platform (OBP) shows terms and definitions free of charge, but I could not reach it with automated fetches: it is JavaScript-rendered and sits behind a Cloudflare check.

---

## Q1. OMG VDML 1.1: CapabilityDefinition, CapabilityOffer, CapabilityMethod, CapabilityLibrary

### Takeaway
VDML 1.1 is the clearest formal precedent for separating a library-level capability definition from an organization's actual offer of it. A CapabilityOffer has exactly one provider, an OrgUnit, and is backed by managed resources (Stores, Pools of Actors). Reusable CapabilityMethods (activity networks) deliver it. The methodOwner of a method is a separate OrgUnit from the provider. VDML lines up closely with C2, C3 and C4. It is weaker on C1, because it also lets individual Actors in Positions provide capabilities.

### Cited Findings

**Register entry**
- **Citation:** Object Management Group, *Value Delivery Modeling Language (VDML)*, Version 1.1, OMG Document Number formal/18-09-03. The PDF front matter gives the release date as October 2018. The OMG spec page lists the publication date as March 2018 (the date of the XMI, dtc/18-03-04). Status: formal. IPR mode: Non-Assert. — [OMG VDML page](https://www.omg.org/spec/VDML/); [PDF](https://www.omg.org/spec/VDML/1.1/PDF)
- **Canonical URL:** https://www.omg.org/spec/VDML/1.1/ (machine-readable XMI: https://www.omg.org/spec/VDML/20180201/vdml.xmi) — [OMG VDML page](https://www.omg.org/spec/VDML/)
- **Licence/access:** Free download under the standard OMG licence (see the summary above). Whole-document redistribution is not permitted. — [PDF front matter](https://www.omg.org/spec/VDML/1.1/PDF)
- **Authority:** Consortium (de jure within OMG) formal specification. Not an international standard.

**Definition of capability (paraphrased)**
- §7.2.5.3.1 (CapabilityLibrary Class): a Capability is the ability to do a particular kind of work and deliver the value that is wanted. The exact wording is "the ability to perform a particular kind of work and deliver desired value". — [VDML 1.1 §7.2.5.3.1](https://www.omg.org/spec/VDML/1.1/PDF)
- §7.2.2.3.3 (CapabilityOffer Class): a CapabilityOffer is that same ability, achieved by applying resources managed together, and possibly based on formalized methods (CapabilityMethods). Its superclass is MeasurableElement. — [VDML 1.1 §7.2.2.3.3](https://www.omg.org/spec/VDML/1.1/PDF)

**Related terms and structure**
- **CapabilityOffer properties (§7.2.2.3.3):**
  - `capability: Capability [0..1]`: the library entry being offered.
  - `capabilityProvider: OrgUnit [1]`: the OrgUnit that owns, manages and provides the offer.
  - `method: CapabilityMethod [0..*]`
  - `capabilityResource: Store [0..*]`: the resources that support the capability.
  - `applyingActivity: Activity [0..*]`
  - `location`
  - `releaseControl`: work-priority strategy.
  - `heatIndex: MeasuredCharacteristic`: compared against a scenario threshold to flag the offer for transformation focus and for heat-map display (§8.7).

  — [VDML 1.1 §7.2.2.3.3](https://www.omg.org/spec/VDML/1.1/PDF)
- **OrgUnit (§7.2.2.3.1):** an administrative or functional organizational Collaboration that is responsible for defined resources. It covers the company itself, business units, departments, committees, projects and task forces. Properties: `position`, `capabilityOffer`, `ownedMethod`, `ownedStore`. — [VDML 1.1 §7.2.2.3.1](https://www.omg.org/spec/VDML/1.1/PDF)
- **OrgUnit as the only provider of sharable capabilities (§7.1.7):** OrgUnit is the only Collaboration type that owns resources (people, machines, intellectual property). It is therefore the only Collaboration that provides sharable capabilities. — [VDML 1.1 §7.1.7](https://www.omg.org/spec/VDML/1.1/PDF)
- **Actors in Positions also provide Capabilities (§7.1.7):** some Capabilities of an OrgUnit are provided by Actors (humans or machines) in OrgUnit Positions. More complex ones require Collaborations of OrgUnit participants, defined by CapabilityMethods. — [VDML 1.1 §7.1.7](https://www.omg.org/spec/VDML/1.1/PDF)
- **CapabilityMethod (§7.1.8, §7.2.2.4.1):**
  - It is a Collaboration specification: Activities, DeliverableFlows, BusinessItems, capabilityRequirements and Roles that deliver a Capability and its value contributions.
  - It does not own resources; it receives them while performing its Activities.
  - Properties: `methodOwner: OrgUnit [1]`, `supportedCapability: CapabilityOffer [0..*]`, `methodResource`, `implementedPractice`.
  - It is likened to a reusable business process definition, but at a higher abstraction that is statistical and focused on value.
  - It may be engaged by an Activity of another Collaboration as a "sub-Collaboration".

  — [VDML 1.1 §7.1.8, §7.2.2.4.1](https://www.omg.org/spec/VDML/1.1/PDF)
- **Owner/provider split (§7.1.8, Fig. 7-2):** the methodOwner OrgUnit has responsibility and authority to develop and modify the method design. Provider OrgUnits are responsible for operating the method and for the supporting resources. Fig. 7-2 example: OrgUnit Z owns the method for Capability B, while OrgUnits X and Y provide Capability B using it. — [VDML 1.1 §7.1.8](https://www.omg.org/spec/VDML/1.1/PDF)
- **Activity (§7.1.9):** an Activity identifies the type of Capability it requires by referring to a CapabilityDefinition (its capabilityRequirement). It also names the Role to be filled by a Participant who provides that Capability. The Participant may be an Actor (human or automaton) or a Collaboration (usually an OrgUnit using a CapabilityMethod). — [VDML 1.1 §7.1.9](https://www.omg.org/spec/VDML/1.1/PDF)
- **CapabilityLibrary (§7.2.5.3.1):** contains a taxonomy of Capabilities (CapabilityDefinitions and CapabilityCategories) that is applied to keep capability definitions consistent. Offers or Activities linked to the same Capability count as similar. — [VDML 1.1 §7.2.5.3.1](https://www.omg.org/spec/VDML/1.1/PDF)
- **CapabilityDefinition (§7.2.5.3.2):** a standardized definition that keeps the CapabilityOffers of OrgUnits and the capabilityRequirements of Activities consistent. Properties: input/output CapabilityDependency, `capabilityResourceDefinition`, `practiceDefinition`. — [VDML 1.1 §7.2.5.3.2](https://www.omg.org/spec/VDML/1.1/PDF)
- **CapabilityCategory and Capability (abstract) (§7.2.5.3.3–7.2.5.3.4):** a CapabilityCategory groups similar CapabilityDefinitions, and categories can form a hierarchy. Capability (abstract) is the parent of both, with parent/child hierarchy links. §7.2.5.3.4 admits that industry libraries find it hard to draw a strict line between definitions and categories. — [VDML 1.1 §7.2.5.3.3–7.2.5.3.4](https://www.omg.org/spec/VDML/1.1/PDF)
- **CapabilityDependency (§7.2.5.3.5):** one Capability needs a deliverable from another. It may suggest DeliverableFlows between Activities. — [VDML 1.1 §7.2.5.3.5](https://www.omg.org/spec/VDML/1.1/PDF)

**Bearing on BCO commitments**
- **C1 (bearer is an Organization): partly agrees, partly conflicts.** The *offer* has exactly one OrgUnit provider (§7.2.2.3.3), and OrgUnits are the only Collaborations that provide sharable capabilities (§7.1.7). However, §7.1.7 and §7.1.9 also have individual Actors (humans, machines) providing Capabilities to fill Activity Roles. VDML therefore does not restrict capability bearers to organizations. Also, VDML's OrgUnit covers committees, projects and task forces, which is broader than a legal or formal organization. — [VDML 1.1](https://www.omg.org/spec/VDML/1.1/PDF)
- **C2 (material basis = member agents in their arrangement): agrees.** An offer is the ability gained by "applying resources that are managed together". Its `capabilityResource` Stores and Pools of Actors in Positions are named explicitly (§7.1.7, §7.2.2.3.3). — [VDML 1.1](https://www.omg.org/spec/VDML/1.1/PDF)
- **C3 (realized in business processes): agrees.** CapabilityMethods are activity networks that deliver the capability, compared to reusable process definitions (§7.1.8). Activities require capabilities through capabilityRequirement (§7.1.9). — [VDML 1.1](https://www.omg.org/spec/VDML/1.1/PDF)
- **C4 (ability vs assignment/authority/responsibility): agrees strongly.** VDML separates:
  - the provider of the capability (`capabilityProvider`);
  - the party with responsibility and authority over method design (`methodOwner`);
  - the assignment of persons to Positions and Performer Roles (§7.1.7, §7.1.8, Fig. 7-2).

  — [VDML 1.1](https://www.omg.org/spec/VDML/1.1/PDF)
- **C5 (descriptions are ICEs): agrees in structure.** The library-level CapabilityDefinition is explicitly a "standardized definition" used to keep offers consistent (§7.2.5.3.2). Measurements such as `heatIndex` are MeasuredCharacteristics attached to the offer (§7.2.2.3.3). Caveat: VDML is a MOF metamodel, so every VDML element, including CapabilityOffer, is itself a model element (a description). VDML does not commit to a real-world disposition. — [VDML 1.1](https://www.omg.org/spec/VDML/1.1/PDF)

### Inferences
- **Mapping to BCO.** The natural mapping is:
  - VDML CapabilityDefinition ≈ a BCO capability *type* (class) or a capability-definition ICE.
  - VDML CapabilityOffer ≈ the BCO disposition instance borne by a specific Organization.
  - `capabilityResource`/Pools ≈ the material basis (C2).
  - CapabilityMethod ≈ a plan specification or process type that realizes it (C3).
  - `methodOwner` ≈ a responsibility or authority role (C4).
- **Restricting BCO to organizations is a deliberate narrowing of VDML.** Wherever VDML lets an Actor (person or machine) provide a capability, BCO would class the Actor's ability as a different thing (e.g., a person's competence/skill disposition or an artifact function), not a Business Capability.
- **VDML gives no ontological status to "capability".** It is a metamodel for value modelling and simulation (ReleaseControl, heatIndex, discrete event simulation). BCO can cite it as structural precedent, not as a definition of what kind of entity a capability is.

### Gaps
- I did not check whether VDML 1.1 defines any constraint that a CapabilityOffer's capability must match the capabilityRequirement of the Activities it is applied to; only the prose (§7.1.9) suggests it.
- I did not verify whether a VDML 1.2 or later revision is in progress as of October 2026. The OMG page lists 1.1 as the current formal version ([OMG VDML page](https://www.omg.org/spec/VDML/)).

---

## Q2. OMG BMM 1.3: does it define capability?

### Takeaway
No. BMM 1.3 has no Capability concept. "Capability" appears only as one item in the list that defines Means, alongside device, regime, technique, instrument and others. BMM's realization link runs from Business Process to Course of Action, not to capability. Organization Unit, Business Process and Asset are placeholders defined outside BMM. BMM is useful to BCO mainly as precedent that plans, strategies and courses of action are directive or plan content, i.e., on the description layer.

### Cited Findings

**Register entry**
- **Citation:** Object Management Group, *Business Motivation Model (BMM)*, Version 1.3, OMG Document Number formal/15-05-19. The PDF is dated May 2015; the spec page says April 2015. Status: formal. — [OMG BMM page](https://www.omg.org/spec/BMM/); [PDF](https://www.omg.org/spec/BMM/1.3/PDF)
- **Canonical URL:** https://www.omg.org/spec/BMM/1.3/ (RDF/JSON-LD "About" files are also published) — [OMG BMM page](https://www.omg.org/spec/BMM/)
- **Licence/access:** Free download under the standard OMG licence (same front-matter terms as VDML). — [PDF](https://www.omg.org/spec/BMM/1.3/PDF)
- **Authority:** Consortium formal specification.

**Definition of capability**
- BMM gives no definition of its own. §8.3 defines a Means as any of a list of things (device, capability, regime, technique, restriction, agency, instrument or method) that can be called on, activated or enforced to achieve Ends. — [BMM 1.3 §8.3](https://www.omg.org/spec/BMM/1.3/PDF)
- §8.3 also says a Means does not specify the business-process steps needed to exploit it, or responsibility for those steps. It specifies only "the capabilities that can be exploited to achieve the desired Ends". — [BMM 1.3 §8.3](https://www.omg.org/spec/BMM/1.3/PDF)

**Related terms**
- **Course of Action (§8.3.3):** an approach or plan for configuring some aspect of the enterprise to achieve Desired Results. Strategies and Tactics are its categories. §8.3.3 states that Courses of Action are not Business Processes; Business Processes can realize them. — [BMM 1.3 §8.3.3](https://www.omg.org/spec/BMM/1.3/PDF)
- **Business Process (§7.3.9, §8.6.2):** a placeholder. Business Processes realize Courses of Action (fact type "business process realizes course of action"). — [BMM 1.3](https://www.omg.org/spec/BMM/1.3/PDF)
- **Organization Unit (§8.6.1):** a placeholder linked to plan elements for accountability. — [BMM 1.3](https://www.omg.org/spec/BMM/1.3/PDF)
- **Asset (§8.6.3):** a placeholder with two kinds, Fixed Asset and Resource. §8.6.3 notes that a BMM may include Assets not valued financially, "such as skills of people in the enterprise". — [BMM 1.3](https://www.omg.org/spec/BMM/1.3/PDF)

**Bearing on BCO commitments**
- **C1:** silent. BMM has no capability bearer, and Organization Unit is a placeholder.
- **C2:** silent. BMM's Assets placeholder includes people's skills, but it is not tied to a capability.
- **C3:** analogous but different. In BMM, the thing processes realize is a Course of Action (a plan or approach), not a capability (§8.3.3).
- **C4:** agrees in spirit. §8.3 separates Means from both the process steps that exploit them and the responsibility for those steps.
- **C5:** agrees. Courses of Action, Strategies, Tactics and Directives are plan or directive content, which matches BCO's treatment of target states and sourcing statements as ICEs. — [BMM 1.3](https://www.omg.org/spec/BMM/1.3/PDF)

### Inferences
- BMM treats capability as a kind of Means, so in BMM terms a capability is something one *employs*. This fits BCO's disposition reading (an ability one can call on) but carries no ontological commitment.
- BACM's Strategy package (Q3) reuses BMM-like Means/Ends. It is the OMG place where capability and strategy actually connect.

### Gaps
- None material. BMM 1.3 is the current formal version per [OMG](https://www.omg.org/spec/BMM/).

---

## Q3. OMG business architecture work (BACM) and UAF capability definitions; status as of 2026

### Takeaway
The OMG Business Architecture Core Metamodel (BACM) is no longer only an RFP:
- **1.0:** formal, August 2024.
- **1.1:** formal, September 2026 (formal/26-09-01).
- **1.2:** in beta, September 2026 (dtc/26-03-26).

BACM defines Capability as the ability a *business* has to produce an Outcome without saying how. It separates:
- CapabilityBehavior: variant behaviour descriptions, linked to processes;
- CapabilityImplementation: Roles, Performers and resources;
- PerformerRole assignment: which conveys authority and responsibility.

UAF 1.3 (DMM formal/25-10-01) defines Capability as an enterprise's ability to achieve a desired effect. However, it lets any CapableElement (operational agents, services, actual resources, including actual organizations) "exhibit" a capability under environmental conditions. That contradicts C1's restriction to organizations. UAF keeps personnel Competence as a separate concept.

### Cited Findings

**Register entry: BACM**
- **Citation:** Object Management Group, *Business Architecture Core Metamodel (BACM)*, Version 1.1, OMG Document Number formal/26-09-01, dated September 2026. Copyright holders include the Business Architecture Guild, Mega, VDMBee, Thematix, BPM.com, Capsifi, Model Driven Solutions and EDM Council. IPR mode: "non-assert" (§6.3). — [BACM 1.1 PDF](https://www.omg.org/spec/BACM/1.1/PDF); [OMG BACM page](https://www.omg.org/spec/BACM)
- **Version history (per the OMG page):**
  - 1.0 formal, August 2024;
  - 1.1 formal, September 2026;
  - 1.2 Beta 1, September 2026: PDF dtc/26-03-26, TTL dtc/26-02-18, XMI dtc/26-06-07.

  Beta documents are informational; only the formal version governs compliance. — [OMG BACM page](https://www.omg.org/spec/BACM); [BACM 1.2 Beta1](https://www.omg.org/spec/BACM/1.2/Beta1/PDF)
- **Search-snippet discrepancy:** an earlier search snippet described 1.1 as "beta (March 2025)" with 13 open issues on the 1.1b1 tracker. The current OMG page and the downloaded PDF show 1.1 as formal (September 2026). The beta snippet is stale. — [OMG BACM issues](https://issues.omg.org/issues/spec/BACM/1.1b1); [OMG BACM page](https://www.omg.org/spec/BACM)
- **Licence/access:** free download under the standard OMG licence terms (read in the 1.1 PDF front matter). — [BACM 1.1 PDF](https://www.omg.org/spec/BACM/1.1/PDF)
- **Authority:** Consortium formal specification. It is the OMG business architecture standard, developed with the Business Architecture Guild.

**BACM definition of Capability (paraphrased)**
- §7.3.2.7 (Class Capability, base class AbstractCapability), first sentence: Capability is a generalization over variations in behaviour, and in the structures applied to that behaviour, all of which produce the same general Outcome. — [BACM 1.1 §7.3.2.7](https://www.omg.org/spec/BACM/1.1/PDF)
- §7.3.2.7, second sentence: a Capability is "the ability a business has to produce an Outcome" without specifying how the Outcome is produced. — [BACM 1.1 §7.3.2.7](https://www.omg.org/spec/BACM/1.1/PDF)
- §7.1.1 (non-normative overview): Capability is an abstraction of a unit of work that does not say how the work is done. It is specified by the Outcomes it produces and needs, where Outcomes are states of BusinessObjects or InformationItems. — [BACM 1.1 §7.1.1](https://www.omg.org/spec/BACM/1.1/PDF)
- The overview also says Capabilities that support ValueStreamStages represent abilities the business must have to produce value for customers. — [BACM 1.1 §7.1.1](https://www.omg.org/spec/BACM/1.1/PDF)
- The BACM 1.2 Beta 1 page describes the business capability as "an abstraction representing what a business does but not how". — [OMG BACM page](https://www.omg.org/spec/BACM)

**BACM: related terms**
- **Constraint on hierarchy (§7.3.2.7):** Capabilities may be decomposed in a strict hierarchy but *may not be specialized*. The stated constraint is that Capability instances may own other Capability instances but may not aggregate or generalize them. — [BACM 1.1 §7.3.2.7](https://www.omg.org/spec/BACM/1.1/PDF)
- **Modelling patterns (§7.3.2.7):** six permitted patterns combine Capability with or without CapabilityBehaviors, CapabilityImplementations, Roles, Performers and Resources. All other configurations are disallowed. — [BACM 1.1 §7.3.2.7](https://www.omg.org/spec/BACM/1.1/PDF)
- **CapabilityBehavior (§7.3.2.8):** a behaviour description or specification, such as process diagrams or procedure manuals. It also covers rules, regulations and policies. CapabilityBehaviors "deliver" a Capability as variant ways of producing similar Outcomes. They are not decomposable but may be associated with Processes. — [BACM 1.1 §7.3.2.8](https://www.omg.org/spec/BACM/1.1/PDF)
- **CapabilityImplementation (§7.3.2.9):** a collection of Roles, AbstractBusinessObjects and Performers that may implement a Capability, CapabilityBehavior, Process or Activity. It can represent planned resourcing or actual organizational elements. — [BACM 1.1 §7.3.2.9](https://www.omg.org/spec/BACM/1.1/PDF)
- **PerformerRole (§7.3.2.16):** the skills, knowledge and willingness to use them in producing a Capability's Outcomes. When a PerformerRole is assigned to a Performer (`assignTo_2`), the Performer acquires the authority and responsibility the role defines. — [BACM 1.1 §7.3.2.16](https://www.omg.org/spec/BACM/1.1/PDF)
- **Performer (§7.3.4.6):** an entity capable of performing PerformerRoles, specialized as OrgUnit or System. Performers are generally described by skills or abilities (§7.1.3). — [BACM 1.1 §7.3.4.6, §7.1.3](https://www.omg.org/spec/BACM/1.1/PDF)
- **OrgUnit (§7.3.4.5):** covers human organizations *and individuals* capable of acting as performers. It is linked to CapabilityImplementation by a «shortcut» association `staffs`, and to other OrgUnits by `Responsible`. LegalEntity specializes OrgUnit. — [BACM 1.1 §7.3.4.5](https://www.omg.org/spec/BACM/1.1/PDF)
- **Process package (§7.1.4):** process models and capability models are complementary perspectives, linked through Outcomes. Processes and Activities can implement ValueStreams and ValueStreamStages and share Roles with Capabilities. — [BACM 1.1 §7.1.4](https://www.omg.org/spec/BACM/1.1/PDF)
- **Extensions (§7.2.7):** a MOF Extension (MEF) mechanism applies business-architecture frameworks and tags. — [BACM 1.1 §7.2.7](https://www.omg.org/spec/BACM/1.1/PDF)
- **Instances as sets (§7.1):** model instances of BACM metaclasses represent "types or sets of entities" in a real or imagined business, with intensional or extensional semantics. — [BACM 1.1 §7.1](https://www.omg.org/spec/BACM/1.1/PDF)

**BACM: bearing on BCO commitments**
- **C1:** partly agrees, partly conflicts.
  - Agrees: Capability is the ability of "a business", i.e., the enterprise as a whole.
  - Conflicts: no association names a bearing organization. Capability-to-organization links run only through CapabilityImplementation and `staffs`.
  - Conflicts: BACM's OrgUnit explicitly includes *individuals* (§7.3.4.5).
- **C2:** agrees in substance. CapabilityImplementation, the Performers and Resources assigned to a Capability's Roles, is the closest metamodel analogue of a material basis (§7.3.2.9).
- **C3:** agrees. CapabilityBehaviors deliver Capabilities and may be associated with Processes. Capability and process models share Outcomes and Roles (§7.3.2.8, §7.1.4).
- **C4:** agrees. Ability (Capability, Performer abilities) is kept apart from the assignment that confers authority and responsibility (PerformerRole `assignTo_2`, §7.3.2.16) and from the `Responsible` association between OrgUnits (§7.3.4.5).
- **C5:** structurally compatible. BACM is a metamodel whose elements are descriptions. BACM itself models "intangible" InformationItems that can be *about* BusinessObjects (§7.1.1). I did not find assessment or maturity metaclasses in the sections I read (see Gaps).
- **Conflict for BCO typing:** BACM forbids capability *specialization* (§7.3.2.7). If BCO models capability types with `rdfs:subClassOf` hierarchies (e.g., a BPO/APQC-aligned taxonomy), that conflicts with BACM's strict decomposition-only rule. — [BACM 1.1](https://www.omg.org/spec/BACM/1.1/PDF)

**Register entry: UAF**
- **Citation:** Object Management Group, *Unified Architecture Framework (UAF) Domain Metamodel*, Version 1.3, OMG Document Number formal/25-10-01 [smsc/25-10-01], PDF dated September 2025. The OMG spec page gives publication as April 2026. — [OMG UAF page](https://www.omg.org/spec/UAF/); [UAF 1.3 DMM PDF](https://www.omg.org/spec/UAF/1.3/DMM/PDF)
- **Licence/access:** free download under the standard OMG licence. — [UAF 1.3 DMM PDF](https://www.omg.org/spec/UAF/1.3/DMM/PDF)
- **Authority:** Consortium formal specification, defence- and enterprise-architecture oriented (DoDAF/MODAF/NAF lineage).

**UAF 1.3 definition of Capability (paraphrased)**
- Domain MetaModel::Strategic::Taxonomy::Capability, DMM p.~141. Generalizations: PropertySet, Desirer, PhaseableElement, AffectableElement, SubjectOfStrategicConstraint.
- Capability is "An enterprise's ability to Achieve a desired effect". The effect is realized through ways and means (e.g., CapabilityConfigurations) with specified measures. — [UAF 1.3 DMM, Strategic::Taxonomy](https://www.omg.org/spec/UAF/1.3/DMM/PDF)

**UAF: related terms**
- **CapableElement** (Traceability, abstract): a structural element that can exhibit capabilities. — [UAF 1.3 DMM](https://www.omg.org/spec/UAF/1.3/DMM/PDF)
- **Exhibits** (Traceability, MeasurableElement): relates a CapableElement to a Capability it meets under specific environmental conditions. — [UAF 1.3 DMM](https://www.omg.org/spec/UAF/1.3/DMM/PDF)
- **Elements that specialize CapableElement:** OperationalAgent, Service, ActualResource and ActualService. ActualOrganization specializes ActualResponsibleResource, and ActualOrganizationalResource specializes ActualResource. I read these generalization lines directly, but traced only part of the ActualOrganization chain. — [UAF 1.3 DMM](https://www.omg.org/spec/UAF/1.3/DMM/PDF)
- **MapsToCapability** (Traceability): an Activity contributes to providing a Capability. — [UAF 1.3 DMM](https://www.omg.org/spec/UAF/1.3/DMM/PDF)
- **Organization** (Personnel::Taxonomy): a group of OrganizationalResources (Persons, Posts, Organizations, Responsibilities) associated for a purpose. OrganizationalResource is the abstract parent of Organization, Person, Post and Responsibility. — [UAF 1.3 DMM](https://www.omg.org/spec/UAF/1.3/DMM/PDF)
- **Competence** (Personnel::Constraints): a specific set of abilities defined by knowledge, skills and aptitude. Related tuples: CompetenceForRole, RequiresCompetence, CompetenceToConduct (Function), ProvidesCompetence. — [UAF 1.3 DMM](https://www.omg.org/spec/UAF/1.3/DMM/PDF)
- **CapabilityConfiguration:** specializes ResourceArchitecture. — [UAF 1.3 DMM](https://www.omg.org/spec/UAF/1.3/DMM/PDF)

**UAF: bearing on BCO commitments**
- **C1:** conflicts. UAF's definition is enterprise-level, but the Exhibits relation lets agents, services and resources of any kind (persons, systems, organizations) exhibit Capabilities.
- **C2:** partly agrees. Capability is realized through ways and means such as CapabilityConfigurations, which are resource architectures.
- **C3:** agrees. Activities map to (contribute to providing) Capabilities.
- **C4:** agrees implicitly. Responsibility, Post and Competence are separate personnel constructs.
- **C5:** partly agrees.
  - Measures attach to the Exhibits and MapsToCapability tuples (MeasurableElement), and capability phasing sits on Strategic phases.
  - However, Capability itself is a PropertySet. It is a typed set of measurable properties, not a disposition.
  - UAF is effect-oriented: a capability is an ability to achieve an effect, not to perform a kind of work.

  — [UAF 1.3 DMM](https://www.omg.org/spec/UAF/1.3/DMM/PDF)

### Inferences
- **BACM 1.1 is the most directly relevant OMG source for the term "business capability"** and the most current (formal September 2026). Its core sense ("ability a business has", "what not how", Outcome-specified) agrees with BCO's disposition reading at the enterprise level.
- **BACM's metamodel is silent on BFO categories.** It models Capability as a model element standing for "types or sets" (§7.1). BCO would need to state that a BACM Capability element corresponds to a BCO capability type, and that the instance-level disposition is borne by an Organization.
- **BACM's Outcome-centric identity criterion is worth noting for BCO.** A capability is individuated by the Outcomes it produces, not by the process that realizes it. This is compatible with BFO: a disposition's type is fixed by its realization type, and BCO could tie realization types to BPO act types whose outputs are the Outcomes.
- **UAF's effect-based definition and its broad CapableElement set make it a poor anchor for C1.** It is still a useful authority that enterprise capability is distinct from personnel Competence.

### Gaps
- I did not retrieve the original BACM RFP (OMG document number and date) or the full submission history; only formal and beta documents were consulted.
- I did not read BACM 1.2 Beta 1's changes to Capability. The changebar is dtc/26-04-01.
- I did not check BACM Annex A (term definitions) or whether BACM has any assessment or maturity metaclass.
- Version-status note: whether a BACM OWL/TTL is published for 1.1 formal (as opposed to the 1.2 beta TTL) was not confirmed.
- UAF 1.3: the date discrepancy (PDF September 2025 vs page April 2026) is unresolved. Probably adoption versus publication.

---

## Q4. ISO enterprise-modelling family (15704, 19439, 19440), ISO/IEC/IEEE 42010, ISO/IEC 21838-2 (BFO), ISO 9000 / 22301

### Takeaway
ISO 19440:2020 gives two senses of the term:
- a general one, ability to perform a specified activity (3.5);
- an enterprise-modelling construct, Capability (3.6). This is a collection of capability attributes of a Resource (the capability it provides) or of an Enterprise Activity (the capability it requires).

So in ISO 19440 the bearer is a *Resource*, not specifically an organization. The 2020 edition also removed Functional Entity in favour of "active Resource". ISO/IEC 21838-2 (BFO) has no capability class. Its disposition (internally grounded) versus role (externally grounded) distinction is the formal basis for C1, C2 and C4. ISO 9000:2015 defines capability as an object's ability to realize an output that meets requirements (3.6.12). That is an output-quality sense, and the standard refers statistical process capability to ISO 3534-2.

### Cited Findings

**Register entry: ISO 19440:2020**
- **Citation:** ISO 19440:2020, *Enterprise modelling and architecture — Constructs for enterprise modelling*, Edition 2, 2020-05, 110 pp. ISO/TC 184/SC 5. It replaces ISO 19440:2007 (*Enterprise integration — Constructs for enterprise modelling*), which is withdrawn. — [ISO catalogue 74491](https://www.iso.org/standard/74491.html); [ISO catalogue 33834 (2007)](https://www.iso.org/standard/33834.html)
- **Licence/access:** paid and copyrighted; all rights reserved. Clause 3 is partly visible in the free iTeh preview. — [iTeh preview PDF](https://cdn.standards.iteh.ai/samples/74491/2045fbd5664f4ea387f29eaa07fd903e/ISO-19440-2020.pdf)
- **Authority:** normative international standard.

**ISO 19440:2020: definitions (paraphrased; source is the iTeh preview, Clause 3)**
- **3.5 capability (general sense):** "ability to perform a specified activity". — [ISO 19440:2020 3.5](https://cdn.standards.iteh.ai/samples/74491/2045fbd5664f4ea387f29eaa07fd903e/ISO-19440-2020.pdf)
- **3.6 Capability (enterprise-modelling construct):** a specialization of the Enterprise Object construct. It represents the collection of capability characteristics, expressed as capability attributes, of either a Resource (the capability it provides) or an Enterprise Activity (the capability it requires). — [ISO 19440:2020 3.6](https://cdn.standards.iteh.ai/samples/74491/2045fbd5664f4ea387f29eaa07fd903e/ISO-19440-2020.pdf)
- **Core constructs (3.13 examples):** Domain, Business Process, Enterprise Activity, Service, Event, Enterprise Object, Enterprise Object View, Organizational Unit (3.55), Decision Centre, Role, Product, Order, Capability and Performance Indicator. — [ISO 19440:2020](https://cdn.standards.iteh.ai/samples/74491/2045fbd5664f4ea387f29eaa07fd903e/ISO-19440-2020.pdf)
- **Derived constructs (3.22 examples):** Organizational Role, Operational Role, Person Profile, Stakeholder, User, Co-provider and Functionality. — [ISO 19440:2020](https://cdn.standards.iteh.ai/samples/74491/2045fbd5664f4ea387f29eaa07fd903e/ISO-19440-2020.pdf)
- **Capitalization convention (Introduction):** construct names are capitalized precisely to distinguish the Capability construct from the general usage of "capability". — [ISO 19440:2020 Introduction](https://cdn.standards.iteh.ai/samples/74491/2045fbd5664f4ea387f29eaa07fd903e/ISO-19440-2020.pdf)
- **3.39 functional category:** a grouping of entities for expressing a common purpose or capability. — [ISO 19440:2020](https://cdn.standards.iteh.ai/samples/74491/2045fbd5664f4ea387f29eaa07fd903e/ISO-19440-2020.pdf)
- **3.40 Functionality:** a derived construct (specializing Role) for what a product or service can or cannot do for a User. — [ISO 19440:2020](https://cdn.standards.iteh.ai/samples/74491/2045fbd5664f4ea387f29eaa07fd903e/ISO-19440-2020.pdf)
- **3.23 design specification phase:** adapted from ISO 19439:2006 3.13, with the word "capabilities" replaced by "Enterprise Activities". — [ISO 19440:2020](https://cdn.standards.iteh.ai/samples/74491/2045fbd5664f4ea387f29eaa07fd903e/ISO-19440-2020.pdf)
- **Location of the full construct:** Clause 7.14 (Purpose, Description, Usage, Construct template for Capability, p. 53). Resource is Clause 7.13 with its template at 7.13.4. Organizational Unit is defined at 3.55. — [ISO 19440:2020 table of contents](https://cdn.standards.iteh.ai/samples/74491/2045fbd5664f4ea387f29eaa07fd903e/ISO-19440-2020.pdf)
- **Foreword changes from the 2007 edition:**
  - Functional Entity was eliminated and replaced by "active Resource";
  - a Role core construct was introduced, generalizing Organizational Role, Operational Role and Person Profile;
  - a Performance Indicator core construct was added;
  - Enterprise Activities became decomposable.

  — [ISO 19440:2020 Foreword](https://cdn.standards.iteh.ai/samples/74491/2045fbd5664f4ea387f29eaa07fd903e/ISO-19440-2020.pdf)

**ISO 19440:2020: bearing on BCO commitments**
- **C1:** conflicts. The provided Capability belongs to a Resource (now including active Resources such as people, machines and IT), not specifically to an Organization. Organizational Unit is a separate construct. Whether a 19440 Organizational Unit can bear a Capability was not visible in the preview.
- **C2:** silent.
- **C3:** agrees by analogy. The required Capability of an Enterprise Activity mirrors VDML's capabilityRequirement. Capability links what activities need to what resources provide.
- **C4:** agrees. Role constructs (Organizational and Operational Role, Person Profile) are separate from Capability.
- **C5:** agrees. The construct is explicitly a collection of capability *attributes* and is distinguished typographically from the real-world ability. This is direct ISO precedent for separating the descriptive model element from the thing described. — [ISO 19440:2020](https://cdn.standards.iteh.ai/samples/74491/2045fbd5664f4ea387f29eaa07fd903e/ISO-19440-2020.pdf)

**Register entry: ISO 19439:2006**
- **Citation:** ISO 19439:2006, *Enterprise integration — Framework for enterprise modelling*, Edition 1. Last reviewed and confirmed in 2015 per ISO. It defines four enterprise model views, conformant with ISO 15704. The EN version has a 2007 corrigendum. — [ISO catalogue 33833](https://www.iso.org/standard/33833.html); [SIS SS-EN ISO 19439:2006](https://www.sis.se/en/produkter/manufacturing-engineering/industrial-automation-systems/industrial-process-measurement-and-control/sseniso194392006/)
- **Licence/access and authority:** paid and copyrighted; normative international standard.
- **Use of "capabilities":** ISO 19439 used "capabilities" in its design-specification-phase definition (3.13). ISO 19440:2020 replaced it with "Enterprise Activities", per the SOURCE note at 19440:2020 3.23. — [ISO 19440:2020 3.23](https://cdn.standards.iteh.ai/samples/74491/2045fbd5664f4ea387f29eaa07fd903e/ISO-19440-2020.pdf)

**Register entry: ISO 15704:2019**
- **Citation:** ISO 15704:2019, *Enterprise modelling and architecture — Requirements for enterprise-referencing architectures and methodologies*, Edition 2, 2019-12, 76 pp. — [ISO catalogue 71890](https://www.iso.org/standard/71890.html)
- **Scope:** sets a reference base of concepts and requirements for enterprise architectures and modelling languages. It explicitly does not define standard enterprises, organizational structures, processes or data. — [ISO catalogue 71890](https://www.iso.org/standard/71890.html)
- **Licence/access and authority:** paid; normative international standard.
- **Capability definition:** I could not verify whether it defines "capability" (see Gaps).

**Register entry: ISO/IEC 21838-2:2021 (BFO 2020)**
- **Citation:** ISO/IEC 21838-2:2021, *Information technology — Top-level ontologies (TLO) — Part 2: Basic Formal Ontology (BFO)*. Paid from ISO/IEC. — [IEC webstore](https://webstore.iec.ch/publication/72703)
- **Free source:** the BFO 2020 OWL artefacts are free under CC BY 4.0 from the BFO-2020 GitHub repository. This repository vendors `bfo-core.ttl` at commit 044490fc. — [BFO-2020 bfo-core.ttl](https://raw.githubusercontent.com/BFO-ontology/BFO-2020/044490fc5100ffed6df7d4d15cbc167698b6fdee/src/owl/bfo-core.ttl)
- **Authority:** normative international standard; also the BCO's top-level ontology.
- **Disposition (BFO_0000016), elucidation paraphrased:** a realizable entity such that:
  - if it ceases to exist, its bearer is physically changed;
  - it is realized when, and because, the bearer is in special physical circumstances;
  - it is realized in virtue of the bearer's physical make-up.

  Alt label: "internally-grounded realizable entity". — [BFO-2020 bfo-core.ttl](https://raw.githubusercontent.com/BFO-ontology/BFO-2020/044490fc5100ffed6df7d4d15cbc167698b6fdee/src/owl/bfo-core.ttl)
- **Role (BFO_0000023), elucidation paraphrased:** a realizable entity that exists because its bearer is in some special physical, social or institutional circumstances it need not be in. Losing the role does not change the bearer's physical make-up. Alt label: "externally-grounded realizable entity". — [BFO-2020 bfo-core.ttl](https://raw.githubusercontent.com/BFO-ontology/BFO-2020/044490fc5100ffed6df7d4d15cbc167698b6fdee/src/owl/bfo-core.ttl)
- **Realizable entity (BFO_0000017):** a specifically dependent continuant that inheres in an independent continuant (not a spatial region), of a type whose instances are realized in processes of a correlated type. — [BFO-2020 bfo-core.ttl](https://raw.githubusercontent.com/BFO-ontology/BFO-2020/044490fc5100ffed6df7d4d15cbc167698b6fdee/src/owl/bfo-core.ttl)
- **Function (BFO_0000034):** a disposition that exists because of evolution or intentional design. — [BFO-2020 bfo-core.ttl](https://raw.githubusercontent.com/BFO-ontology/BFO-2020/044490fc5100ffed6df7d4d15cbc167698b6fdee/src/owl/bfo-core.ttl)
- **No capability class:** BFO 2020 has no "capability" class. — [BFO-2020 bfo-core.ttl](https://raw.githubusercontent.com/BFO-ontology/BFO-2020/044490fc5100ffed6df7d4d15cbc167698b6fdee/src/owl/bfo-core.ttl)
- **Note on text identity:** I did not compare the ISO text of 21838-2 to the OWL elucidations word for word.

**ISO/IEC 21838-2: bearing on BCO commitments**
- **C1 and C2:** supports. A disposition must inhere in an independent continuant and be grounded in its physical make-up. For an organization, that make-up can only be its members and their arrangement, so C2 is what makes C1 coherent in BFO.
- **C3:** supports. A realizable entity is realized in processes of a correlated type.
- **C4:** supports strongly. The disposition/role split is exactly the ability-versus-assignment split.
- **C5:** silent in BFO itself; CCO's ICE handles it.

**Register entry: ISO 9000:2015**
- **Citation:** ISO 9000:2015, *Quality management systems — Fundamentals and vocabulary*. — [ISO catalogue 45481](https://www.iso.org/standard/45481.html) (catalogue page not fetched; number from general knowledge, unverified)
- **3.6.12 capability, paraphrased from the ERA terminology collection's reproduction of the entry:** the ability of an object to realize an output that will meet the requirements for that output. Note 1 refers process-capability terms in statistics to ISO 3534-2. — [ERA terminology: capability](https://www.era.europa.eu/era-railway-terminology-collection/capability/term_1/sms_safety_culture_human_and_organisational_factor)
- **Bearing on BCO:**
  - C1: conflicts. "Object" is anything perceivable or conceivable, so there is no bearer restriction.
  - C3: weakly agrees. The ability is to realize an output, which is output-centred like BACM's Outcome.
  - Otherwise silent.
- **Licence/access and authority:** paid; normative international standard.

### Inferences
- **No ISO standard reviewed restricts capability bearers to organizations.**
  - ISO 19440 attaches provided capability to Resources.
  - ISO 9000 attaches it to any object.

  So C1 is a BCO design choice. It is motivated by BACM, VDML and UAF enterprise-level usage, not mandated by ISO.
- **ISO 19440's provided-versus-required split is a useful pattern for BCO.** Required Capability belongs to an Enterprise Activity; provided Capability belongs to a Resource. BCO could represent "required capability" as an ICE, or as a type-level relation from a BPO act type, distinct from the borne disposition.
- **ISO 19440's Capability construct is closer to a capability profile than to a capability.** It is a collection of capability attributes, i.e., a description, which supports treating such profiles as ICEs (C5).

### Gaps
- **ISO 19440:2020 Clause 7.14 and entries 3.55 and 3.66–3.67.** I could not read the full Capability construct (purpose, description, usage, template) or the Organizational Unit and Resource definitions; they lie outside the free preview. The ISO OBP could not be fetched (Cloudflare challenge).
- **ISO 15704:2019.** Whether it defines capability is unverified; its preview was not retrieved.
- **ISO 19439:2006.** Whether a review after 2015 confirmed or withdrew it is not verified for 2026.
- **ISO/IEC/IEEE 42010:2022.** Edition 2, November 2022 ([ISO catalogue 74393](https://committee.iso.org/standard/74393.html)). I found no source showing that it defines "capability". Its terminology centres on entity of interest, stakeholder, concern, viewpoint, view and architecture description framework ([NORA wiki](https://noraonline.nl/wiki/ISO_42010), secondary). My belief that 42010 does not define capability is unverified.
- **ISO 9000:2015 3.10.4 competence.** Not verified this session. I recall it is defined as the ability to apply knowledge and skills to achieve intended results, but that is unconfirmed.
- **ISO 22301:2019 and ISO 22300:2021.** Not researched. I found no source on whether they define "capability" or a "business continuity capability".

---

## Q5. Process capability (ISO/IEC 330xx, CMMI): a different sense of capability

### Takeaway
In ISO/IEC 33020:2019 and in CMMI, "capability" is a quality characteristic of a *process*, or of an organization's performance in a single practice area. It is rated on an ordinal scale of capability levels. This is a different sense from organizational or business capability, and BCO should treat it as such. In BCO terms, a process capability level is at most an ICE: an assessment result *about* how a capability is exercised (C5). It is not the capability itself.

### Cited Findings

**Register entry: ISO/IEC 33020:2019**
- **Citation:** ISO/IEC 33020:2019, *Information technology — Process assessment — Process measurement framework for assessment of process capability*, Edition 2. Confirmed at review in 2026 per ISO. It replaces ISO/IEC 33020:2015, which is withdrawn. — [ISO catalogue 78526](https://www.iso.org/standard/78526.html); [SNV listing](https://connect.snv.ch/en/isoiec-33020-2019)
- **Process capability (paraphrased from the ISO catalogue abstract):** a process quality characteristic about a process's ability to consistently meet current or projected business goals. — [ISO catalogue 78526](https://www.iso.org/standard/78526.html)
- **How levels are derived:** the framework produces process (capability) attribute ratings, together called a process profile, and derives a process capability level from them. — [ISO catalogue 78526](https://www.iso.org/standard/78526.html)
- **Licence/access and authority:** paid; normative international standard.

**Register entry: ISO/IEC 33001:2015**
- **Citation:** ISO/IEC 33001:2015, *Information technology — Process assessment — Concepts and terminology*.
- **Status:** I did not verify its definitions or its current edition (see Gaps).

**Register entry: CMMI (ISACA / CMMI Institute)**
- **Capability level:** rates performance in an individual practice area. Levels run from 0 (Incomplete) to 3 (Defined). — [CMMI Institute: levels](https://cmmiinstitute.com/learning/appraisals/levels)
- **Maturity level:** describes the organization across a set of practice areas, from 1 to 5 (Initial to Optimizing). — [CMMI Institute: levels](https://cmmiinstitute.com/learning/appraisals/levels)
- **Version 3.0 change:** Maturity Level 2 is defined as all practice areas at Capability Level 2 (secondary source). — [Process Group: changes in CMMI v3](https://processgroup.com/changes-in-cmmi-v3)
- **Licence/access and authority:** proprietary industry model; access is by licence from ISACA. It is not an ISO standard.

**Bearing on BCO commitments**
- **C1:** conflicts in sense, not in fact.
  - In 330xx, the bearer of "process capability" is a process, and processes cannot bear dispositions in BFO.
  - In CMMI, the bearer is the organization's performance in a practice area.
- **C3:** different. Process capability is a property *of* the process, not something realized *in* the process.
- **C5:** agrees. Capability levels, maturity levels and process profiles are assessment outputs, i.e., ICEs about how a capability is exercised. — [ISO catalogue 78526](https://www.iso.org/standard/78526.html); [CMMI Institute](https://cmmiinstitute.com/learning/appraisals/levels)

### Inferences
- **BCO should register "process capability" and "capability level" as homonyms.**
  - A process capability level can be modelled as an ICE (a measurement or rating) about the processes that realize an organization's capability, or about the organization's disposition to perform them consistently.
  - BFO processes cannot bear dispositions, so the literal ISO/IEC 33020 sense cannot be imported.
- **ISO 9000:2015 3.6.12 Note 1 marks a third, statistical sense.** It points statistical process capability to ISO 3534-2: the spread of process output relative to specification. That is another homonym to keep apart.

### Gaps
- ISO/IEC 33001:2015's terminology entries (process capability, capability level, process attribute) were not verified, and its current edition is unknown.
- CMMI v3.0's official model text was not consulted; only the CMMI Institute web page and a secondary consultancy page were used.
- ISO 3534-2 was not consulted.

---

## Q6. Conflicts across sources: capability as a characteristic of a process, of an organization, or of a resource

### Takeaway
The sources split along two axes.
- **Bearer:**
  - organization or business: BACM; VDML offers; UAF definition text;
  - any resource, actor or object: ISO 19440 provided Capability; ISO 9000; UAF Exhibits; VDML Actors;
  - process: ISO/IEC 33020; CMMI.
- **What a capability is about:**
  - kind of work or activity: VDML; ISO 19440;
  - outcome or output: BACM; ISO 9000;
  - effect: UAF.

All the modelling standards agree on C4, separating ability from assignment and responsibility. Most give precedent for C5, keeping descriptions and definitions apart from what they describe. None is a formal ontology. Only ISO/IEC 21838-2 supplies the disposition category BCO uses.

### Cited Findings
- **Organization or business as bearer:**
  - BACM: ability "a business" has (§7.3.2.7). — [BACM 1.1](https://www.omg.org/spec/BACM/1.1/PDF)
  - VDML: CapabilityOffer has exactly one OrgUnit provider (§7.2.2.3.3). — [VDML 1.1](https://www.omg.org/spec/VDML/1.1/PDF)
  - UAF: "an enterprise's ability" (Strategic::Taxonomy::Capability). — [UAF 1.3 DMM](https://www.omg.org/spec/UAF/1.3/DMM/PDF)
- **Resource, actor or object as bearer:**
  - ISO 19440:2020 3.6: a Resource's provided Capability. — [ISO 19440:2020 preview](https://cdn.standards.iteh.ai/samples/74491/2045fbd5664f4ea387f29eaa07fd903e/ISO-19440-2020.pdf)
  - VDML §7.1.7, §7.1.9: Actors (human or machine) provide Capabilities. — [VDML 1.1](https://www.omg.org/spec/VDML/1.1/PDF)
  - UAF Exhibits: any CapableElement. — [UAF 1.3 DMM](https://www.omg.org/spec/UAF/1.3/DMM/PDF)
  - ISO 9000:2015 3.6.12: any object. — [ERA terminology](https://www.era.europa.eu/era-railway-terminology-collection/capability/term_1/sms_safety_culture_human_and_organisational_factor)
  - BACM's OrgUnit includes individuals (§7.3.4.5). — [BACM 1.1](https://www.omg.org/spec/BACM/1.1/PDF)
- **Process as bearer:**
  - ISO/IEC 33020:2019: process capability. — [ISO 78526](https://www.iso.org/standard/78526.html)
  - CMMI: capability level per practice area. — [CMMI Institute](https://cmmiinstitute.com/learning/appraisals/levels)
- **Requirement-side capability:** a capability can also be something an activity *requires*, not just something an entity has.
  - ISO 19440:2020 3.6: Enterprise Activity's required Capability. — [ISO 19440:2020 preview](https://cdn.standards.iteh.ai/samples/74491/2045fbd5664f4ea387f29eaa07fd903e/ISO-19440-2020.pdf)
  - VDML §7.1.9: an Activity's capabilityRequirement. — [VDML 1.1](https://www.omg.org/spec/VDML/1.1/PDF)
- **Competence of persons kept separate from enterprise capability:**
  - UAF Competence. — [UAF 1.3 DMM](https://www.omg.org/spec/UAF/1.3/DMM/PDF)
  - BACM PerformerRole skills (§7.3.2.16). — [BACM 1.1](https://www.omg.org/spec/BACM/1.1/PDF)
- **Capability hierarchy:**
  - BACM forbids specialization and allows only strict decomposition (§7.3.2.7). — [BACM 1.1](https://www.omg.org/spec/BACM/1.1/PDF)
  - VDML allows category/definition hierarchies and concedes that the boundary between definition and category is fuzzy (§7.2.5.3.4). — [VDML 1.1](https://www.omg.org/spec/VDML/1.1/PDF)
  - UAF has CapabilityGeneralization, a taxonomic relation. — [UAF 1.3 DMM](https://www.omg.org/spec/UAF/1.3/DMM/PDF)

### Inferences
- **The BCO commitment set is a defensible synthesis.** It matches BACM, VDML and UAF on enterprise-level ability; BFO on disposition versus role; and VDML, BACM and ISO 19440 on separating definition, assignment and description. It narrows:
  - VDML, UAF, ISO 19440 and ISO 9000 on who can bear a capability (C1);
  - 330xx and CMMI on what "capability" means at all.

  The BCO spec should state these narrowings explicitly as departures, each with its source and clause.
- **Recommended authority ranking for citing a definition of business capability:**
  1. BACM 1.1 (OMG formal, 2026; the term is its central concept);
  2. VDML 1.1 (OMG formal; the definition/offer/method structure);
  3. UAF 1.3 (OMG formal; enterprise effect sense);
  4. ISO 19440:2020 (international standard; resource and activity sense; paid);
  5. ISO 9000:2015 (international standard; generic quality sense).

  Process capability (ISO/IEC 33020, CMMI) should be cited only as a contrasting homonym.
- **BACM's no-specialization rule against UAF's CapabilityGeneralization is a real cross-standard conflict.** BCO must take a side when building capability types, especially if they are derived from BPO/APQC process categories.

### Gaps
- I found no published paper that maps ISO 19440's Capability construct to BFO, or that compares VDML/BACM capability with BFO dispositions. Academic literature was outside this scope; one candidate is the arXiv/CEUR work on capabilities as dispositions, seen in search results but not read.
