# ADR-002 (PROPOSED): Grounded Business Capabilities and Their Descriptions

**Status:** Proposed — requires maintainer review; does NOT amend accepted ADR-001  
**Draft date:** 2026-10-22  
**Version:** 0.1.0  
**Dependencies:** BFO 2020; CCO 2.0 (Agent Ontology 2024-11-05, other cited modules 2024-11-06); [BusinessProcessOntology](https://github.com/Skreen5hot/BusinessProcessOntology) at its public `main` state inspected on 2026-10-22.  
**Scope:** companion Business Capability Ontology (BCO), not an automatic transformation of the full APQC catalog.

## 1. Context: grounding is prior to subclassing

BFO Disposition (`BFO_0000016`) is a realizable entity whose realization occurs in virtue of its bearer's physical makeup. A lost disposition implies a physical change in that bearer. CCO Organization (`ont00001180`) is a Group of Agents (`ont00000300`), which is an Object Aggregate. Consequently, **'the organization can deliver X' does not imply 'the organization bears a Disposition to do X.'**

The BPO's accepted ADR-001, R6, recommends representing standing-function PCF categories by subclasses of CCO Organization Capability (`ont00000568`). CCO Organization Capability is an Agent Capability and a Realizable Entity; its stated parent is NOT Disposition. This draft creates a deliberately narrower candidate class and a separate ICE layer for descriptions and claims.

## 2. Decision: split the ontological senses

**D1. Narrowly grounded realist class.** `bc:BusinessCapability` is a subclass of both `cco:ont00000568` (Organization Capability) and `obo:BFO_0000016` (Disposition). The class is not asserted equivalent to their intersection: not every Organization Capability which happens to be a Disposition is automatically a business capability in the intended scope. Each instance requires a real CCO Organization bearer.

**D2. Organization boundary.** The organization's members, together with their embodied capacities and organization as a materially constituted aggregate, ground the candidate disposition. Contractors' people, a vendor's servers, and other independent external entities do not become material constituents merely through agreements. A firm may have an internal disposition to coordinate a provider while the provider bears the disposition to execute the outsourced act. Merely being able to procure a result is not the same as bearing the full performance disposition.

**D3. External conditions versus material bases.** External data, software service availability, and permissions can be conditions of a realization, or evidence of dependence; not all external reliance destroys an internally grounded disposition. The admission test examines the type of performance: does the organization itself have an internally grounded capacity to perform that act, as distinct from commissioning another agent to perform it? This cannot be answered by vendor presence alone. A sourcing assessment records unresolved cases without asserting a disposition.

**D4. Changing membership.** CCO's treatment of Organization as an aggregate makes membership changes compatible with continued organization identity in ordinary modeling practice. It does *not* settle persistence of the very same disposition through total turnover. We assume an organization may remain capable across replacement when a continuous and sufficient materially grounded coordination of member capacities persists. The numerical identity and physical-basis criteria remain an open metaphysical question; do not infer capability persistence simply from the organization's persistent ID.

**D5. Act-type indexing.** Capability *kinds* are indexed intensionally to defined types of CCO Planned Act (`ont00000228`). The authoritative initial vocabulary is BPO's reality-layer process classes, not its SKOS catalog hierarchy. A capability's index is the act as physically/informationally identifiable; *institutional success conditions*, legal standing, permission, and recognized authority are modeled separately. 'Assemble and transmit application data' may be an act index; 'legally originate a mortgage' must not be made a capability index while the standing is hidden inside the disposition differentia. The act taxonomy is curated, not mechanically copied from APQC's partonomy.

**D6. Do not mandate an actual realization.** No axiom `BusinessCapability subClassOf (has realization some PlannedAct)` or act-specific analog is asserted. Such an axiom entails that every instance has an existing realization process, excluding unexercised capabilities. BFO `has realization` (`BFO_0000054`) and `realizes` (`BFO_0000055`) are reserved for actual occurrences. A potential-realization indexing link is not yet adequately expressed by the available object-property vocabulary, so the correlation remains documented in definitions, external review registers, and competency tests, **not a newly minted object property**.

**D7. Function overlap.** Do not assert `BusinessCapability disjointWith Function`. BFO Function (`BFO_0000034`) is already a subtype of Disposition. If a particular capability also meets BFO's intentional-design/evolution criteria, overlap is permitted; organizational intentional design alone is not sufficient evidence that the bearer is an artifact function bearer. The business capability differentia uses performance type and grounding, not origin.

**D8. Explicit description and assessment layer.** Most business architecture content is ICEs. Define a small set of information classes:
- Business Capability Description, Map, Assessment, Sourcing Assessment: subclasses of CCO Descriptive ICE (`ont00000853`);
- Business Capability Maturity Assessment: a specialized assessment and CCO Ordinal Measurement ICE (`ont00001010`);
- Business Capability Target-State Specification: CCO Prescriptive ICE (`ont00000965`).

A capability description or target does **not** entail the existence of a matching disposition. An assessment may describe the organization without presupposing an independent disposition. Maturity *ratings* are measurement ICE instances, not capability subclasses.

**D9. Reuse only existing object properties.** The model employs CCO `has capability` (`ont00001954`) / `capability of` (`ont00001889`), CCO `is about` (`ont00001808`), `is a ordinal measurement of` (`ont00001811`), `prescribes` (`ont00001942`) when appropriate, and BFO `has realization` / `realizes` for actual events. No additional object properties are defined. Avoid CCO `aggregate has capability` (`ont00001898`) and `aggregate has disposition` (`ont00001956`) as defaults: each is a subproperty of `aggregate bearer of` (`ont00001836`), whose CCO definition entails member-wise bearing of same-type dependent continuants and therefore does not straightforwardly capture emergent capacities.

**D10. BPO coexistence and migration.** Do not redefine or auto-promote existing `ex:` capability classes. The current Section 1.0 BPO slice includes `ex:StrategicPlanningCapability`, `ex:BusinessModelGovernanceCapability`, `ex:CustomerExperienceManagementCapability` (all Organization Capability), and `ex:CompetitiveAnalysisCapability` (Agent Capability plus an existential `has realization some ex:P19945`). All are review candidates, not asserted subclasses of `bc:BusinessCapability`. The latter example reveals the latent-capability issue but the correct resolution requires deciding whether its bearer is a person or organization, and then examining process participation.

**D11. Process development is not process realization.** An act that establishes strategic-planning capacity, installs governance, hires staff, or configures supporting systems can establish a disposition without being an act realizing that disposition. Do not infer that `Establish X` realizes the ongoing capacity to `Maintain/Perform X`. Review candidate BPO links individually.

**D12. Namespace, imports, and versioning.** `https://example.org/BusinessCapabilityOntology#` is a temporary namespace used only for this review draft. Deployers must approve an owned namespace and version IRI. OWL imports use CCO ontology IRIs and require local mappings to pinned CCO 2.0 closure in the BPO's validation harness. The alignment module contains annotation-only candidate pointers and deliberately does not import an existing BPO slice with unresolved modeling commitments.

## 3. Modeling patterns and no-go rules

### Existing bearer relations

```
Organization —cco:has capability→ BusinessCapability
BusinessCapability —cco:capability of→ Organization
ActualPlannedAct —BFO:realizes→ BusinessCapability        [ONLY if actual]
BusinessCapability —BFO:has realization→ ActualPlannedAct [ONLY if actual]
Description —cco:is about→ Organization OR actual capability instance
MaturityAssessment —cco:is a ordinal measurement of→ Organization OR established capability instance
TargetStateSpecification —cco:prescribes→ suitable target process/entity, when applicable
```

These are example ABox assertion patterns, not mandatory class-level existential axioms. `cco:prescribes` has specific CCO semantics: for an occurrent it prescribes a rule/guide; for a continuant it supplies a model. Do not confuse `is about` with `prescribes`.

### Prohibited inference patterns

1. APQC `skos:broader` implies `rdfs:subClassOf` for dispositions.
2. `has capability` is inferred from a capability map entry or maturity score.
3. `BusinessCapability` is inferred from an agreement with a vendor.
4. `BusinessCapability` is inferred solely from a regulator's authorization.
5. A capability subclass has an existential BFO realization restriction solely to index the kind of process it *could* realize.
6. A BPO act named `Establish X` is automatically treated as a realization of a continuing `X` capability.
7. `aggregate has capability` is used to encode a non-member-wise emergent organizational disposition.
8. Business Capability is asserted disjoint from Function.

## 4. Admission process for a proposed domain capability

The curator must record (outside the OWL subclass axiom, pending a vetted annotation profile):
- an existing or reviewed non-deontic BPO/CCO Planned Act type, with exact class IRI and definition;
- the proposed organizational bearer type and its constituent agent scope;
- a defensible narrative of material grounding, including human/organizational coordination;
- which external systems/agents enable performance and whether their performance is wrongly ascribed to the organization;
- whether an act *develops* the capability or is a possible *realization*;
- institutional permissions/roles separately, where relevant;
- evidence and epistemic status: proposed, asserted, tested, observed, disputed;
- why no available existing CCO class already covers the desired class.

The draft intentionally does not mint a new `potential realization type` object property. A *typed capacity to carry out a kind of act* cannot be expressed via the BFO `has realization` relation without committing to actual realization, and OWL object properties cannot directly point to OWL classes without a metamodeling choice. The adequate solution for this indexing requirement is OPEN (annotation-based registry, OWL punning, or a separate information model with reviewed semantics).

## 5. Concrete competency questions

**CQ01 (grounding):** Given an organization that outsources every fraud-analysis act, can the system avoid inferring an internal fraud-analysis disposition solely from delivery records? Expected: YES; no disposition inference.

**CQ02 (latent capability):** Can an asserted, grounded organizational disposition exist without an instance of its realizing act? Expected: YES.

**CQ03 (roles):** Can an organization be authorized to perform an act and yet fail to possess a disposition for the relevant non-deontic act type? Expected: YES.

**CQ04 (function):** Can a capability instance also be a BFO Function if separately justified? Expected: POSSIBLY; no disjointness.

**CQ05 (maturity):** Does assigning maturity rank 3 create a new subclass of `BusinessCapability` or entail its existence? Expected: NO.

**CQ06 (APQC):** Does `skos:broader` between APQC catalog concepts yield `subClassOf` among capabilities? Expected: NO.

**CQ07 (BPO migration):** Can the existing `ex:CompetitiveAnalysisCapability` be made explicitly organizational without first reviewing bearer and `has realization some ex:P19945`? Expected: NO.

**CQ08 (persistence):** Does organizational persistence entail identity of the capability instance after total membership replacement? Expected: NOT DETERMINED in this draft.

**CQ09 (realization):** May a documented actual BPO process instance realize an organizational disposition? Expected: YES, subject to BFO's participant and bearer conditions.

**CQ10 (sourcing):** May a capability assessment truthfully describe reliance on a supplier without asserting that supplier's disposition belongs to the focal organization? Expected: YES.

## 6. Unresolved review decisions (blocking for v1.0)

**U1 — Rigorous grounding test:** What precisely counts as a sufficient *material constitution* for emergent group-level dispositions? Coordination through organizational rules is informational and must not be mistaken for the aggregate's material parts.

**U2 — Membership/identity:** Can a disposition remain numerically identical across total membership turnover? CCO/BFO axioms cited here do not decide.

**U3 — Act-index representation:** Choose a vetted, machine-queryable bridge from a capability universal to its *potential* realization act universal, without false existential restrictions or newly minted object properties.

**U4 — Institutional acts:** Define consistently how to split juridical/authorized transaction types from underlying non-deontic processes, particularly for legal originations and regulatory submissions.

**U5 — Function intersection:** Clarify whether organizational design qualifies as BFO Function's artifact-design origin condition for any organizational disposition.

**U6 — Assessment profile:** Choose the existing CCO vocabulary to encode ordinal rank, measurement scale, date, provenance, uncertainty, method, and negative findings. This draft only types assessment ICEs and optionally identifies their subjects.

**U7 — BPO migration:** Run a repository-wide audit, including the `capabilities/` directory, of capabilities, realization existentials, class ownership, annotation bridge, and the current test harness. Only a portion of the public repository was inspected for this draft.

**U8 — Validation:** Full OWL DL coherence, BFO/CCO import closure consistency, and BPO integration gates must be executed in the target repository. They have not been run in this environment.

## 7. Consequences

Benefits: preserves BFO realism; treats procurement and external dependencies explicitly; supports actual, unexercised, and aspirational capability statements without equivocation; reuses BPO process classes and CCO terms.

Costs: organizations need evidential grounding before disposition assertions; not every enterprise capability-map entry becomes a realist class; act-indexing is not yet fully machine-actionable; existing BPO capability axioms require review, not blind migration.

## 8. References

- **BFO 2020** as provided in `BFO .pdf`, especially `BFO_0000016`, `BFO_0000034`, `BFO_0000023`, `BFO_0000054`, `BFO_0000055`.
- **CCO 2.0** attached PDF serializations: `Agent.pdf` (Agent Capability, Organization Capability, Skill, Organization, bearer relations), `Extended Relations Ontology.pdf` (aggregate-bearing relations), `Event Ontology.pdf` (Planned Act), `Information Entity Ontology.pdf` (ICE categories and relations).
- **BPO repo:** https://github.com/Skreen5hot/BusinessProcessOntology
- **ADR-001:** https://github.com/Skreen5hot/BusinessProcessOntology/blob/main/docs/adr/ADR-001-category-and-upper-level-modeling.md
- **Current 1.0 reality slice:** https://github.com/Skreen5hot/BusinessProcessOntology/blob/main/ontology/slices/apqc_1_0.ttl
- **Methodology:** https://github.com/Skreen5hot/BusinessProcessOntology/blob/main/apqc_to_bfo_cco_methodology.md

No source excerpt here is reproduced as a copyright-dependent extended quotation; definitions of the new classes are original proposed drafting language.
