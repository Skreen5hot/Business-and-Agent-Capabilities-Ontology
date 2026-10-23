# Formal-ontology and conceptual-modelling treatments of "capability" (register for the BCO)

Scope note. BCO draft commitments assessed below, abbreviated:
- **C1** capability is a BFO disposition (obo:BFO_0000016);
- **C2** borne by a CCO Organization (cco:ont00001180);
- **C3** material basis (obo:BFO_0000218) is the organization's member agents in their arrangement;
- **C4** realized in business processes;
- **C5** having a capability (ability) is distinct from being assigned / authorized / responsible;
- **C6** capability maps, assessments, maturity ratings are information content entities (ICEs) ABOUT capabilities.

Ontology versions read directly for this note (2026-10-23): BFO 2020 `bfo-core.ttl` at commit 044490f (repo vendored extract), CCO merged file on the `develop` branch with versionIRI `https://www.commoncoreontologies.org/2026-08-13/CommonCoreOntologiesMerged` (CCO's GitHub release list shows v2.2 published 2026-08-14 and v2.1 on 2026-04-04), the repo's vendored CCO v2.0-2024-11-06 extract (commit 510dad7), and IOF Core `Core.rdf` from `iofoundry/ontology` master, versionIRI `.../ontology/202603/core/Core/`.

## Q1. BFO 2020 (ISO/IEC 21838-2:2021), Arp/Smith/Spear 2015, and Smith-school papers on capability

### Takeaway
BFO itself has no "capability" class. It supplies disposition, function, role, realizable entity and `has material basis`. The main Smith-school paper, Beverley, Limbaugh, Merrell, Koch & Smith, "Capabilities: An Ontology" (2024), defines a capability as a disposition in whose realization some organism or group of organisms has, or had, an interest. It places capability between disposition and function, says organizations can bear capabilities, and treats authority-style "capability" as a role, outside its sense. That supports C1, C2 and C5. BFO's `has material basis` is defined only for dispositions and requires the basis to be a continuant part of the bearer, which bears directly on C3.

### Cited Findings
**Register entry: BFO 2020 / ISO/IEC 21838-2:2021**
- Citation: ISO/IEC 21838-2:2021, *Information technology — Top-level ontologies (TLO) — Part 2: Basic Formal Ontology (BFO)*, ISO/IEC JTC 1, 2021. The ISO catalogue page is https://www.iso.org/standard/74572.html; it returned HTTP 403 to the fetch, so edition and status were not re-verified. OWL artefact: BFO-2020 GitHub repo `src/owl/bfo-core.ttl`, commit 044490fc… — [bfo-core.ttl source](https://raw.githubusercontent.com/BFO-ontology/BFO-2020/044490fc5100ffed6df7d4d15cbc167698b6fdee/src/owl/bfo-core.ttl)
- Licence/access: the ISO standard is paywalled (an ISO sales product; not re-verified because of the 403). The BFO-2020 OWL files are openly available on GitHub. Authority: **international standard**.
- In the vendored extract, obo:BFO_0000016 (disposition) is a subclass of obo:BFO_0000017 (realizable entity) and is disjoint with obo:BFO_0000023 (role). Its elucidation says that if the disposition ceases to exist, its bearer is physically changed, and that it is realized in virtue of the bearer's physical make-up — [BFO-2020 bfo-core.ttl](https://raw.githubusercontent.com/BFO-ontology/BFO-2020/044490fc5100ffed6df7d4d15cbc167698b6fdee/src/owl/bfo-core.ttl) (checked in `vendor/bfo/bfo-core-bco-extract.ttl` lines 79–86)
- Realizable entity (BFO_0000017) is elucidated as a specifically dependent continuant inhering in an independent continuant that is not a spatial region, of a type whose instances are realized in processes of a correlated type. Its examples include roles, functions and dispositions — [BFO-2020 bfo-core.ttl](https://raw.githubusercontent.com/BFO-ontology/BFO-2020/044490fc5100ffed6df7d4d15cbc167698b6fdee/src/owl/bfo-core.ttl) (extract lines 88–94)
- Function (BFO_0000034) is a subclass of disposition — [BFO-2020 bfo-core.ttl](https://raw.githubusercontent.com/BFO-ontology/BFO-2020/044490fc5100ffed6df7d4d15cbc167698b6fdee/src/owl/bfo-core.ttl) (extract line 135)
- `has material basis` (BFO_0000218) has rdfs:domain disposition. Its definition: b has material basis c iff b is a disposition, c is a material entity, there is a bearer d of b, c is a continuant part of d at some t, and d has b *because* c is part of d at t. The inverse is `material basis of` (BFO_0000127), with range disposition — [BFO-2020 bfo-core.ttl](https://raw.githubusercontent.com/BFO-ontology/BFO-2020/044490fc5100ffed6df7d4d15cbc167698b6fdee/src/owl/bfo-core.ttl) (extract lines 170–172, 233–236)

**Register entry: Arp, Smith & Spear (2015)**
- Citation: Arp R, Smith B, Spear AD. *Building Ontologies with Basic Formal Ontology*. MIT Press, 2015. Licence/access: commercial book (paywalled). Authority: **peer-reviewed academic (scholarly monograph)**. Not fetched directly. Beverley et al. 2024 cite it as their ref [25], as the source of a test for telling roles from dispositions: does gaining or losing the realizable entity require a physical change in the bearer? — [Beverley et al. 2024, §3 and ref. 25](https://arxiv.org/abs/2405.00183v2)

**Register entry: Beverley, Limbaugh, Merrell, Koch & Smith (2024)**
- Citation: Beverley J, Limbaugh D, Merrell E, Koch PM, Smith B. "Capabilities: An Ontology." arXiv:2405.00183, v1 30 Apr 2024, v2 16 Aug 2024 (cs.AI, cs.LO). Licence: **CC BY 4.0**. The arXiv record gives no venue. Authority: **preprint** by BFO's principal author — [arXiv record](https://arxiv.org/abs/2405.00183v2)
- Definition (paraphrased): a capability is a disposition in whose realization some organism or group of organisms has, or had, an interest. "Has an interest in" is a primitive relation, with stated necessary conditions — [arXiv PDF §4](https://www.arxiv.org/pdf/2405.00183)
- Placement: capability is a class between BFO disposition and BFO function. All functions are capabilities, and all capabilities are dispositions. The authors explicitly do *not* propose adding capability to the BFO hierarchy; they offer it as a resource for the community — [arXiv PDF §4–5](https://www.arxiv.org/pdf/2405.00183)
- Bearers: the paper says organizations, buildings and machines can bear capabilities, and that collectives can have capabilities that arise from how they are configured. Its examples are two soldiers together able to engage aircraft, and dancing the foxtrot. Immaterial entities such as sites cannot bear capabilities, because they lack material parts — [arXiv PDF §1, §3](https://www.arxiv.org/pdf/2405.00183)
- Ability versus authority: the paper notes a natural-language use of "capability" meaning being allowed or having the authority to act, for example a temporary promotion conferring the "capability to issue orders". It classifies that sense on the role side and calls it "orthogonal to the sense at issue here". It also says roles and capabilities are often co-instantiated in one bearer: a role's realization depends on the bearer's capabilities — [arXiv PDF §3](https://www.arxiv.org/pdf/2405.00183)
- Organizational example: FedEx is described as possessing a logistics capability before it recognized it. The point is that a capability can exist, and be discovered, independently of anyone being aware of it — [arXiv PDF §4](https://www.arxiv.org/pdf/2405.00183)
- The paper cites the DoD definition (an ability to achieve a desired effect through combinations of means and ways to perform tasks) and calls definitions built on "ability"/"is able to" potentially circular — [arXiv PDF §2](https://www.arxiv.org/pdf/2405.00183)
- It cites Röhl & Jansen (2014), "Why functions are not special dispositions" (*J. Biomed. Semantics* 5:27), a dissenting view on the function/disposition relation — [arXiv PDF refs](https://www.arxiv.org/pdf/2405.00183)
- It cites an earlier related paper: Merrell, Limbaugh, Anderson & Smith, "Mental Capabilities", ICBO 2019, which also places capability between function and disposition — [PhilArchive record MERC-14](https://philarchive.org/rec/MERC-14) (the record was surfaced by search and not opened)
- Bearing on BCO: **C1 agrees.** The capability is a disposition, and the authors use the gain/loss-of-physical-change test. **C2 agrees.** Organizations and groups are explicitly admitted as bearers. **C3 agrees in spirit.** Collective capabilities depend on how members are configured, though the paper does not use `has material basis` for organizations. **C4 agrees.** Capabilities are realized through processes. **C5 agrees strongly**, through the authority-as-role argument. **C6 is silent on ICEs**, although the paper notes that tests, diplomas and certifications measure or signal capabilities. **Divergence:** Beverley et al. add an *interest* condition, which BCO's draft does not state.

### Inferences
- BCO's C1 has direct Smith-school support. The definition "disposition in whose realization some agent/organism has an interest" is shared by Beverley et al. 2024 and IOF Core (Q3). BCO could decide explicitly whether to adopt the interest condition; for a business capability the organization's own interest would plausibly satisfy it.
- C3 is formally checkable against BFO. `has material basis` requires the basis to be a continuant part of the bearer. In CCO (verified, Q2), Organization ⊑ Group of Agents ⊑ BFO object aggregate (BFO_0000027), and Group of Agents is defined as having only Agents as *member parts* (BFO_0000115). Member parts are continuant parts in BFO, so an aggregate of member agents can be the material basis. "Their arrangement", however, is not a material entity and cannot itself be the `has material basis` object. The arrangement belongs in the "because" clause, or as a relational quality, not as the basis.
- Because BFO_0000218's domain is disposition, using it with a BCO capability under CCO Organization Capability (a realizable entity) would *entail* that the capability is a disposition. That is consistent with C1, and C1 is needed to use the relation at all.

### Gaps
- The ISO catalogue page was not reachable (403), so the edition, confirmation status and price of ISO/IEC 21838-2 as of October 2026 were not verified.
- The text of Arp/Smith/Spear 2015 was not consulted directly. Its role/disposition test is reported via Beverley et al.'s citation.
- No peer-reviewed published version of Beverley et al. 2024 was found; the arXiv record lists no venue.

## Q2. Common Core Ontologies: Agent Capability, Organization Capability, Skill

### Takeaway
In both CCO v2.0 (the 2024-11-06 vendored extract) and the current `develop` merged file (versionIRI 2026-08-13, matching the v2.2 release), Agent Capability (cco:ont00001379) is a direct subclass of BFO realizable entity (BFO_0000017), **not** of disposition. Organization Capability (ont00000568) and Skill (ont00000089) are subclasses of Agent Capability. No CCO documentation found explains the choice of realizable entity over disposition.

### Cited Findings
**Register entry: Common Core Ontologies**
- Citation: CUBRC Inc. / CCO community, *Common Core Ontologies*, GitHub `CommonCoreOntology/CommonCoreOntologies`. Releases: v2.0-2024-11-06 (2024-11-06), v2.1 (2026-04-04), v2.2 (2026-08-14), from the GitHub releases API. Licence: **BSD 3-Clause** (merged file header: `dcterms:license`, "BSD 3-Clause", rights "CUBRC Inc."). Authority: **community ontology** (mid-level, BFO-aligned) — [CCO repository](https://github.com/CommonCoreOntology/CommonCoreOntologies); [merged TTL, develop](https://raw.githubusercontent.com/CommonCoreOntology/CommonCoreOntologies/develop/src/cco-merged/CommonCoreOntologiesMerged.ttl)
- Agent Capability (ont00001379): `rdfs:subClassOf obo:BFO_0000017` in both the v2.0 extract and develop 2026-08-13. Its definition calls it a Realizable Entity that inheres in a Material Entity "in virtue of that Material Entity's capacity to realize it in some Planned Act" — [CCO merged TTL (develop)](https://raw.githubusercontent.com/CommonCoreOntology/CommonCoreOntologies/develop/src/cco-merged/CommonCoreOntologiesMerged.ttl); [v2.0 at 510dad7](https://raw.githubusercontent.com/CommonCoreOntology/CommonCoreOntologies/510dad76be0ef710b65a421075af912af25342b7/src/cco-merged/CommonCoreOntologiesMerged.ttl)
- The v2.0 extract cites the Stanford Encyclopedia of Philosophy entry "Agency" (Schlosser, Winter 2019) as a definition source for Agent Capability — [v2.0 merged TTL](https://raw.githubusercontent.com/CommonCoreOntology/CommonCoreOntologies/510dad76be0ef710b65a421075af912af25342b7/src/cco-merged/CommonCoreOntologiesMerged.ttl) (extract line 212)
- Organization Capability (ont00000568) ⊑ Agent Capability. Definition: an Agent Capability inhering in an Organization to the extent of the Organization's capacity to realize it in Intentional Acts of a certain type. It is unchanged in develop — [CCO merged TTL (develop)](https://raw.githubusercontent.com/CommonCoreOntology/CommonCoreOntologies/develop/src/cco-merged/CommonCoreOntologiesMerged.ttl)
- Skill (ont00000089) ⊑ Agent Capability, with the same pattern for a Person — [CCO merged TTL (develop)](https://raw.githubusercontent.com/CommonCoreOntology/CommonCoreOntologies/develop/src/cco-merged/CommonCoreOntologiesMerged.ttl)
- Relations: `has capability` (ont00001954; Agent → Agent Capability), `capability of` (ont00001889; inheres in an Agent), `aggregate has capability` (ont00001898) and `capability of aggregate` (ont00001880; Object Aggregate). In develop, `has capability` and `aggregate has capability` are re-expressed as `=Def` inverses — [CCO merged TTL (develop)](https://raw.githubusercontent.com/CommonCoreOntology/CommonCoreOntologies/develop/src/cco-merged/CommonCoreOntologiesMerged.ttl)
- Organization (ont00001180) ⊑ Group of Agents (ont00000300). It is defined as a Group of Agents that can bear roles, has members, and has a set of organization rules. Group of Agents ⊑ BFO object aggregate (BFO_0000027), defined as having only Agents as member parts (BFO_0000115) — [CCO merged TTL (develop)](https://raw.githubusercontent.com/CommonCoreOntology/CommonCoreOntologies/develop/src/cco-merged/CommonCoreOntologiesMerged.ttl)
- The definition wording has changed across releases. A 2021 snapshot of the Agent Ontology ties Agent Capability to an agent's capacity for intentional acts, while 2024+ uses "Material Entity … Planned Act". This comes from search snippets of Archivo snapshots and was not opened — [Archivo AgentOntology 2024-12-17](https://akswnc7.informatik.uni-leipzig.de/dstreitmatter/archivo/ontologyrepository.com/CommonCoreOntologies--Mid--AgentOntology/2024.12.17-054002/CommonCoreOntologies--Mid--AgentOntology_type=parsed.ttl)
- **Conflicting claim:** a web-search summary said Agent Capability is a subclass of BFO disposition. This is **contradicted** by the OWL files read directly, where the parent is BFO_0000017 in both v2.0 and develop 2026-08-13 — [CCO merged TTL (develop)](https://raw.githubusercontent.com/CommonCoreOntology/CommonCoreOntologies/develop/src/cco-merged/CommonCoreOntologiesMerged.ttl)

**Register entry: Jensen et al. (2024), "The Common Core Ontologies"**
- Citation: Jensen M, De Colle G, Kindya S, More C, Cox AP, Beverley J. "The Common Core Ontologies." arXiv:2404.17758 (v2), also posted on the FOIS 2024 site. Authority: **preprint / conference paper** — [arXiv PDF](https://arxiv.org/pdf/2404.17758v2); [FOIS 2024 copy](https://utwente.nl/en/eemcs/fois2024/resources/papers/jensen-et-al-the-common-core-ontologies.pdf)
- A text search of the paper found no discussion of capability. It describes the Agent Ontology as covering agents, organizations and the roles they bear — [arXiv PDF](https://arxiv.org/pdf/2404.17758v2)
- Bearing on BCO: **C1 conflicts with CCO's parent, but CCO does not forbid it.** CCO asserts the more general realizable entity, so a BCO subclass under both Organization Capability and disposition is logically consistent; nothing asserts disjointness. **C2 agrees** (Organization Capability inheres in an Organization). **C3: CCO is silent** on material basis. **C4 is partly aligned**: CCO says capabilities are realized in Planned Acts / Intentional Acts, and BPO act types presumably sit there. **C5: CCO is silent** in the capability definitions, though roles are separate classes. **C6: CCO is silent** about capability ICEs, though CCO has `is measured by ordinal` (ont00001963) near these terms in the extract.

### Inferences
- CCO's choice of realizable entity is plausibly deliberate neutrality: it leaves open whether some agent capabilities are externally grounded, like roles. No source states this rationale, so BCO's "disposition" stance is an extra commitment that BCO must justify itself. Beverley et al. 2024 (co-authored by a CCO paper author, Beverley) is the best available justification.
- Note that IOF's Capability annotation `adaptedFrom` points to CCO's AgentOntology (Q3), yet IOF placed it under disposition. This is a precedent for a BFO-family ontology adapting CCO's capability notion into a disposition.

### Gaps
- No CCO design note, issue or paper explaining realizable entity rather than disposition was found. The CCO GitHub issues were not searched exhaustively.
- I read the `develop` branch merged file, not the `v2.2` tag. They are presumed equivalent from the matching dates, but this was not byte-checked.

## Q3. Industrial Ontologies Foundry (IOF Core): capability

### Takeaway
IOF Core (release 202603, MIT licence) defines `Capability` as a subclass of BFO disposition: a "disposition in whose realization some agent has an interest". It asserts BFO function as a subclass of Capability, and lets any independent continuant bear a capability. The IOF Production Planning module adds `agential capability` (a capability borne by an Agent; synonym: skill).

### Cited Findings
**Register entry: IOF Core Ontology**
- Citation: Industrial Ontologies Foundry, *IOF Core Ontology*, release 202603, versionIRI `https://spec.industrialontologies.org/ontology/202603/core/Core/`, from the `iofoundry/ontology` GitHub repo (`core/Core.rdf`). Licence: **MIT** (`dcterms:license http://opensource.org/licenses/MIT` in Core.rdf). Authority: **community ontology** (BFO-based mid-level) — [IOF Core Core.rdf](https://raw.githubusercontent.com/iofoundry/ontology/master/core/Core.rdf); [IOF Core portal release 202603](https://spec.industrialontologies.org/portal/release/202603/core.html)
- `iof:Capability` (`https://spec.industrialontologies.org/ontology/construct/Capability`) ⊑ obo:BFO_0000016 (disposition). Natural-language definition: "disposition in whose realization some agent has an interest". FOL axiom: Capability(x) → Disposition(x) — [IOF Core.rdf](https://raw.githubusercontent.com/iofoundry/ontology/master/core/Core.rdf)
- Explanatory notes (paraphrased): (1) capability narrows BFO disposition by requiring an Agent interested in its realization; (2) it covers "proper" capabilities, not task-based ones such as a stone used to kill; (3) all functions are capabilities, and BFO function is intended to sit directly under capability; (4) not all capabilities are functions. Its examples include a team's capability to play professional football. The class is annotated `adaptedFrom` the CCO AgentOntology — [IOF Core.rdf](https://raw.githubusercontent.com/iofoundry/ontology/master/core/Core.rdf)
- Core.rdf asserts obo:BFO_0000034 (function) `rdfs:subClassOf` iof:Capability — [IOF Core.rdf](https://raw.githubusercontent.com/iofoundry/ontology/master/core/Core.rdf)
- `capability of` / `has capability`: the bearer range/domain is BFO independent continuant (BFO_0000004). The examples are artefacts (lathe, temperature sensor, pH meter) — [IOF Core.rdf](https://raw.githubusercontent.com/iofoundry/ontology/master/core/Core.rdf)
- IOF Core also has `Agent` ⊑ BFO material entity, `Organization` ⊑ `OrganizedGroupOfAgents`, and `BusinessProcess` ⊑ `PlannedProcess` with an Agent participant — [IOF Core.rdf](https://raw.githubusercontent.com/iofoundry/ontology/master/core/Core.rdf)
- `agential capability` (Production Planning module, release 202601): a capability borne by an Agent, with the usage note "Synonym: skill" — [IOF AgentialCapability page](https://spec.industrialontologies.org/portal/release/202601/productionplanning/AgentialCapability.html)
- The same capability→disposition axiom appears in the IOF FOL formalization paper hosted by Autodesk Research — [First-Order Logic Formalization of the IOF (PDF)](https://research.autodesk.com/app/uploads/2023/03/AFirst-OrderLogicFormalizationoftheIndustrialOntologies.pdf_recbLRa49HGewQ8gF.pdf) (surfaced by search, not opened). Beverley et al. 2024 cite it as Smith B et al., JOWO 2019, CEUR 2518 — [arXiv PDF refs](https://www.arxiv.org/pdf/2405.00183)
- The IOF Core paper is Drobnjakovic, Kulvatunyou, Ameri, Will, Smith & Jones (FOMI 2022), according to a search summary of the dblp listing — [dblp Kulvatunyou](https://dblp.uni-trier.de/pid/61/6418.html) (not opened)
- Bearing on BCO: **C1 agrees.** **C2 agrees as a special case**: IOF allows any independent continuant to bear a capability, and organizations are agents in IOF. **C3: IOF is silent** on material basis for capability, though its notes say a car air conditioner's function forms "some material basis" of the car's ability. **C4 agrees**: IOF BusinessProcess is a PlannedProcess, so realization in business processes is expressible. **C5 and C6: IOF is silent.**

### Inferences
- IOF is the strongest *published-ontology* precedent for C1. It is a BFO-aligned community ontology that asserts capability ⊑ disposition and cites CCO as the source it adapted. Its definition matches Beverley et al. 2024 almost word for word, except that IOF requires an *agent* where Beverley et al. say "organism or group of organisms".

### Gaps
- No standalone peer-reviewed IOF "capability" paper by Kulvatunyou or Drobnjakovic was found. The capability treatment appears to live in the ontology annotations and the FOL formalization paper.
- The IOF portal HTML for release 202603 was too long for the fetch to reach the Capability entry, so the GitHub master Core.rdf was used. It is presumed to be release 202603 from its versionIRI.

## Q4. UFO/OntoUML and ArchiMate (Azevedo et al. 2015; Calhau, Almeida, Guizzardi; Sales et al.)

### Takeaway
The UFO line of work treats capability as a disposition, a UFO "aspect", that inheres in an object and is manifested in events. Azevedo et al. 2015 used this to criticise ArchiMate, which models capability as a *behaviour* element. Calhau, Almeida & Guizzardi (2024) extend it with capabilities as "valuable" dispositions, emergent versus resultant capabilities of systems such as organizations, and a capability level as a quality (maturity). This broadly agrees with C1, C2 and C4. It treats resource assignment as allocating components to functional roles in the organization-as-system, which fits C3 and C5.

### Cited Findings
**Register entry: Azevedo et al. (2015)**
- Citation: Azevedo CLB, Iacob M-E, Almeida JPA, van Sinderen M, Ferreira Pires L, Guizzardi G. "Modeling resources and capabilities in enterprise architecture: A well-founded ontology-based proposal for ArchiMate." *Information Systems* 54 (2015) 235–262. DOI 10.1016/j.is.2015.04.008 (online 23 May 2015). Access: the Twente repository lists the final published PDF under the "Taverne" (Dutch copyright-act open access) arrangement; at the publisher it is Elsevier, subscription. Authority: **peer-reviewed academic (journal)** — [University of Twente record](https://research.utwente.nl/en/publications/modeling-resources-and-capabilities-in-enterprise-architecture-a-/)
- Content (paraphrased from the abstract): an ontological analysis, using UFO, of a proposed extension of ArchiMate with resource, capability and competence. It identifies semantic problems and revises the metamodel, evaluated on two industrial cases — [University of Twente record](https://research.utwente.nl/en/publications/modeling-resources-and-capabilities-in-enterprise-architecture-a-/)
- As characterised by Calhau et al. 2024: Azevedo et al. analysed capability using UFO's notion of disposition, concluding that capabilities are neither behaviour (events) nor structure (objects) but dispositions that characterise objects and are manifested through events. They also proposed "capability bundles" that aggregate capabilities with resources and link individual competences to organizational capabilities — [Calhau et al. 2024 PDF](https://conferences.big.tuwien.ac.at/biweek2024/pdfs/biweek2024_paper_150.pdf)
- The EDOC 2013 predecessor: Azevedo et al., "An Ontology-Based Well-Founded Proposal for Modeling Resources and Capabilities in ArchiMate", 17th IEEE EDOC 2013, pp. 39–48 — [Calhau et al. 2024 refs](https://conferences.big.tuwien.ac.at/biweek2024/pdfs/biweek2024_paper_150.pdf)

**Register entry: Calhau, Almeida & Guizzardi (2024)**
- Citation: Calhau RF, Almeida JPA, Guizzardi G. "Ontological Analysis of Advanced Capability Modeling in ArchiMate: A First Step Towards Language Revision." Hosted in the BIWEEK 2024 proceedings at TU Wien; the exact workshop/series was not confirmed. Access: free PDF. Authority: **peer-reviewed academic (workshop)** — [PDF](https://conferences.big.tuwien.ac.at/biweek2024/pdfs/biweek2024_paper_150.pdf)
- In the UFO capability ontology described there, capabilities are a mixin of "valuable" dispositions that inhere in a (non-agentive or agentive) capable object, including systems. They have a capability level as a quality, corresponding to maturity. A capability manifestation is triggered by a context situation and brings about an outcome, and may consume inputs and produce outputs (role-mixins played by objects) — [Calhau et al. 2024](https://conferences.big.tuwien.ac.at/biweek2024/pdfs/biweek2024_paper_150.pdf)
- They distinguish complex from atomic capabilities (parts of capabilities of the same bearer) and emergent from resultant capabilities of a system (an organization as a system). Emergent capabilities arise from interacting capabilities of parts and are absent from the parts in isolation. Capability "decomposition" in maps therefore has two meanings: detailing, independent of structure, and partitioning, which follows the whole/part structure — [Calhau et al. 2024](https://conferences.big.tuwien.ac.at/biweek2024/pdfs/biweek2024_paper_150.pdf)
- Criticism of ArchiMate: ArchiMate makes capability a (strategy) behaviour element, which contradicts capability as potentiality. The paper says "capabilities do not correspond to behaviors (events)". ArchiMate's resources mix tangible assets with skills and know-how, which are aspect-like — [Calhau et al. 2024](https://conferences.big.tuwien.ac.at/biweek2024/pdfs/biweek2024_paper_150.pdf)
- Resource assignment: assigning resources to an organizational capability means the resources are allocated to functional roles, as components of the organization-as-system (for example a team), whose own capabilities contribute to the organization's capability — [Calhau et al. 2024](https://conferences.big.tuwien.ac.at/biweek2024/pdfs/biweek2024_paper_150.pdf)
- Related works cited by Calhau et al. 2024: Calhau, Almeida, Kokkula & Guizzardi, "Modeling competences in enterprise architecture: from knowledge, skills, and attitudes to organizational capabilities", *Software and Systems Modeling* (2024); Calhau et al., "A system core ontology for capability emergence modeling", EDOC 2023, Springer, pp. 3–20; and Sales et al. on value in ArchiMate, which treats capabilities as dispositions with valuable impacts on a value subject — [Calhau et al. 2024 refs and §5](https://conferences.big.tuwien.ac.at/biweek2024/pdfs/biweek2024_paper_150.pdf)

**Register entry: ArchiMate 3.2 (The Open Group, 2023)**
- Citation: The Open Group, *ArchiMate 3.2 Specification*, 2023, https://pubs.opengroup.org/architecture/archimate3-doc/. Licence: Open Group copyright; free to read online with registration for the PDF. Authority: **industry consortium standard** (not ISO) — [reference via Calhau et al. 2024, ref. 45](https://conferences.big.tuwien.ac.at/biweek2024/pdfs/biweek2024_paper_150.pdf)
- Treatment (paraphrased): a capability is an ability possessed by an active structure element (an organization, person or system), and it is classified as a strategy-layer behaviour element — [Calhau et al. 2024 §2](https://conferences.big.tuwien.ac.at/biweek2024/pdfs/biweek2024_paper_150.pdf). The search summary of an unofficial reference-card copy gave matching wording — [org2.knuba.edu.ua copy](https://org2.knuba.edu.ua/mod/resource/view.php?id=71428) (secondary, unofficial)
- Bearing on BCO (UFO line): **C1 agrees** (disposition). **C2 agrees** and is broader, since any capable object, including non-agentive ones, can bear a capability. **C3 is close**: emergent organizational capabilities grounded in interacting components in functional roles parallel "members in their arrangement". **C4 agrees** (manifested in events/processes). **C5 is implicit**: assignment is allocation to roles, which differs from having a capability. **C6 partly conflicts**: UFO models maturity as a *quality* (capability level) inhering in the capability, whereas BCO treats maturity ratings as ICEs about capabilities. The two are compatible if BCO distinguishes the quality from the rating ICE that measures it. ArchiMate itself **conflicts with C1** (capability as behaviour).

### Inferences
- The UFO "capability level as quality" pattern implies a BCO design question: is there a BFO quality (or a disposition-degree) that a maturity *rating* (ICE) is about, or does the rating directly concern the capability? In BFO a quality cannot inhere in a disposition (SDCs inhere in independent continuants), so the UFO pattern cannot be copied literally into BFO.
- Calhau's emergent/resultant distinction is a ready source for BCO's account of "arrangement" in C3.

### Gaps
- The full Azevedo et al. 2015 article could not be fetched (nemo.inf.ufes.br refused connections). Its treatment of capability is reported through its abstract and Calhau et al.'s characterisation.
- The exact venue/series for Calhau et al. 2024 (BIR workshop, CEUR or Springer) was not confirmed.
- ArchiMate 3.2 was not read directly from pubs.opengroup.org.

## Q5. Capability-Driven Development / CaaS; Loucopoulos & Kavakli (CODEK)

### Takeaway
In CDD (the CaaS FP7 project) a capability combines ability (know-how) and capacity (resources) that enables an *enterprise* to achieve a goal in a given context. It is delivered by executing business processes and is a design/requirements element. Its bearer (the enterprise) and process realization match C2 and C4. Folding resources (capacity) and context into the capability, and using it as a design artefact, conflicts with a pure disposition reading (C1) and blurs C6.

### Cited Findings
**Register entry: Bērziša et al. (2015)**
- Citation: Bērziša S, et al. (20 authors in total). "Capability Driven Development: An Approach to Designing Digital Enterprises." *Business & Information Systems Engineering* 57(1), 15–25, 2015. DOI 10.1007/s12599-014-0362-0. Access: Springer (AIS eLibrary record available). Authority: **peer-reviewed academic (journal)** — [AIS eLibrary record](https://aisel.aisnet.org/bise/vol57/iss1/3); [RTU record](https://ortus.rtu.lv/science/lv/publications/20532). (The full author list was not retrieved; the search summary confirmed only "Berzisa and 19 co-authors".)
- The CDD meta-model links goals, KPIs, capabilities, context and capability delivery patterns, validated in three industrial cases — [AIS eLibrary record](https://aisel.aisnet.org/bise/vol57/iss1/3)

**Register entry: CaaS project, "Definitions of concepts"**
- Citation: CaaS (Capability as a Service) FP7 project, "Definitions of concepts — The full meta-model of CDD", caas-project.eu. Access: open web page; no licence stated. Authority: **project documentation (grey literature)** — [CaaS definitions](https://caas-project.eu/definitions/)
- Definition: capability is "the ability and capacity that enable an enterprise to achieve a business goal" in a certain context. Associations: a Capability is required by a Goal, *requires* one or more Business Processes (it is delivered by executing them), requires a Context Set, is supported by a Pattern (the solution realizing it in context), and influences KPIs and context indicators. Its stated purpose is to formulate the requirements for the ability to accomplish a business goal — [CaaS definitions](https://caas-project.eu/definitions/)
- A CDD tutorial glosses ability as know-how, capacity as having the resources, and context as knowing when to do what — [CaaS tutorial (SlideShare)](https://www.slideshare.net/slideshow/full-tutorial-on-capability-driven-development/51055070) (from a search summary, not opened)
- Book: Sandkuhl K, Stirna J (eds.), *Capability Management in Digital Enterprises*, Springer 2018, DOI 10.1007/978-3-319-90424-5 — [Springer](https://link.springer.com/book/10.1007/978-3-319-90424-5?page=1)

**Register entry: Loucopoulos & Kavakli, CODEK**
- Citation: Loucopoulos P, Kavakli E. "Capability Oriented Enterprise Knowledge Modeling: The CODEK Approach." In Karagiannis D et al. (eds.), *Domain-Specific Conceptual Modeling*, Springer 2016, pp. 197–215, DOI 10.1007/978-3-319-39417-6_9. Authority: **peer-reviewed academic (book chapter)** — [NEMO 2016 lecture page](https://nemo.omilab.org/nemo/2016/lectures/14-Kavakli.html) (bibliographic details from a search summary)
- Treatment (paraphrased from lecture abstracts): capability is the integrating concept across contextual, service, operational and teleological views of an enterprise, and is tied to the strategic-management notion of dynamic capability — [NEMO 2016 lecture](https://nemo.omilab.org/nemo/2016/lectures/14-Kavakli.html); [NEMO 2015 lecture](https://nemo.omilab.org/nemo/2015/lectures/12-Kavakli.html)
- Bearing on BCO (CDD/CaaS): **C1 conflicts.** Capability includes resources (capacity) and is context-indexed, closer to a configuration or bundle than to a disposition. **C2 agrees** (an enterprise bears it). **C3 is partly aligned**: "capacity" (resources) resembles a material-basis notion but is put *inside* the capability. **C4 agrees** (delivered by executing business processes). **C5 is silent.** **C6 conflicts or blurs**: the CDD Capability doubles as a design/requirements artefact, which BCO would classify as an ICE (a capability specification or requirement) prescribing or describing a capability.

### Inferences
- A BCO crosswalk from CDD would map CDD "Capability" in part to a BCO capability (disposition), CDD "capacity/resources" to the material-basis side, and CDD "Pattern"/design elements to ICEs (plan or directive specifications).

### Gaps
- The verbatim CDD BISE 2015 definition was not read from the article itself; the CaaS project page is the source for the definition.
- No formal CODEK meta-model or capability definition was retrieved.

## Q6. Other capability ontologies and reviews: Enterprise Ontology (1998), TOVE, Offerman et al. (2017)

### Takeaway
The Enterprise Ontology (Uschold et al. 1998) treats CAPABILITY as a *relationship* between a potential actor and an activity specification. It explicitly separates capability ("can") from AUTHORITY ("may"), noting that an authority holder need not have the capability. This strongly supports C5 while conflicting with C1 (relation, not disposition) and C4 (the relatum is a specification, not a process). TOVE's organization ontology centres on roles, authority and empowerment; no TOVE capability construct was found.

### Cited Findings
**Register entry: Uschold, King, Moralee & Zorgios (1998)**
- Citation: Uschold M, King M, Moralee S, Zorgios Y. "The Enterprise Ontology." *The Knowledge Engineering Review* 13(1), 31–89, 1998 (special issue "Putting Ontologies to Use"). DOI 10.1017/S0269888998001088. Access: Cambridge University Press (paywalled); an author draft is freely hosted by AIAI Edinburgh. Authority: **peer-reviewed academic (journal)** — [Cambridge](https://www.cambridge.org/core/journals/knowledge-engineering-review/article/enterpriseontology/17080176D5F06DEAEA8DBB2BAA9F8398); [AIAI author PDF](https://www.aiai.ed.ac.uk/publications/documents/1998/98-ker-ent-ontology.pdf)
- CAPABILITY is defined as a Relationship between a Potential Actor and an ACTIVITY SPECIFICATION, denoting the actor's ability to perform the specified activities. SKILL is a capability whose actor is a Person and whose ability is practised or demonstrated to a measurable degree — [AIAI author PDF §4.3](https://www.aiai.ed.ac.uk/publications/documents/1998/98-ker-ent-ontology.pdf)
- AUTHORITY is the right of an Actor to execute an Activity Specification. Its notes say the holder need not have the CAPABILITY, that a MACHINE may hold authority, and that "CAPABILITY vs AUTHORITY is analogous to that of `can' vs `may'" — [AIAI author PDF §4.1](https://www.aiai.ed.ac.uk/publications/documents/1998/98-ker-ent-ontology.pdf)
- ACTIVITY OWNER (the actor responsible for an activity) and RESOURCE (the role of an entity used or consumed in an activity) are separate terms — [AIAI author PDF §4.1, §4.4](https://www.aiai.ed.ac.uk/publications/documents/1998/98-ker-ent-ontology.pdf)
- Bearing on BCO: **C1 conflicts** (capability as relationship). **C2 is partly aligned**: the Potential Actor can include organizational units. **C3 is silent.** **C4 conflicts in form**: capability relates to an activity *specification* rather than being realized in processes. **C5 agrees strongly**: capability, authority and responsibility (Activity Owner) are three separate notions. **C6 is silent.**

**Register entry: TOVE organization ontology (Fox, Barbuceanu, Gruninger, Lin)**
- Citation: Fox MS, Barbuceanu M, Gruninger M, Lin J. "An Organisation Ontology for Enterprise Modelling", reported in a search summary as published in *Computers in Industry* (1996). Authority: **peer-reviewed academic** — [EIL TOVE project page](https://eil.mie.utoronto.ca/projects/tove-project/); [TOVE overview](https://en.wikipedia.org/wiki/TOVE_Project) (tertiary)
- Treatment: the organization ontology covers activities, agents, roles, positions, goals, communication, authority and commitment, and links structure to behaviour through *empowerment*, an agent's right to perform status-changing actions. Searches found no capability construct — [EIL TOVE project page](https://eil.mie.utoronto.ca/projects/tove-project/) (via a search summary)
- Bearing on BCO: TOVE's empowerment is on the *authority* side, so it is evidence for keeping C5's distinction. It is otherwise **silent** on capability.

**Register entry: Offerman, Stettina & Plaat (2017)**
- Citation: Offerman T, Stettina CJ, Plaat A. "Business Capabilities: A Systematic Literature Review and a Research Agenda." *2017 International Conference on Engineering, Technology and Innovation (ICE/ITMC)*, IEEE, pp. 383–393. DOI 10.1109/ICE.2017.8279911 (the Leiden repository gives 2018 for the same DOI). Access: author PDF free at LIACS/Leiden. Authority: **peer-reviewed academic (conference)** — [Leiden repository](https://scholarlypublications.universiteitleiden.nl/access/item%3A4093818/download); [LIACS PDF](https://liacs.leidenuniv.nl/~plaata1/Offerman2017_SLR.pdf)
- From the abstract (per a search summary): the authors reviewed 720 studies, analysed 20 in depth, proposed a new definition of business capability, and positioned capabilities as the link between strategy ("why") and implementation ("how") — [LIACS PDF](https://liacs.leidenuniv.nl/~plaata1/Offerman2017_SLR.pdf)

**Other found but unread**
- Derguech, Bhiri & Curry, "Using Ontologies for Business Capability Modeling: Describing what Services and Processes Achieve", per a search summary: capabilities as entities made of actions and related properties — [University of Galway record](https://research.universityofgalway.ie/en/publications/using-ontologies-for-business-capability-modeling-describing-what-4/) (not opened)
- A UFO-based thesis on organizational capabilities in defence frameworks (DoDAF/MODAF/NAF), UFES — [UFES repository](https://dspace5.ufes.br/handle/10/9838) (not opened)

### Inferences
- The Enterprise Ontology is the clearest classic precedent for C5's three-way split: ability (capability), authority, and responsibility (activity owner). BFO-style ontologies (Beverley et al.) reach the same split by classifying authority as a role.

### Gaps
- The Offerman et al. PDF download failed, so their proposed definition is **not recorded**.
- No TOVE capability or skill construct was found. TOVE's resource ontology papers were not checked.
- The Wissotzki/Sandkuhl capability-management literature review was not located in this pass.
- The CODEK and Derguech et al. definitions were not retrieved.

## Q7. Where sources conflict with BCO commitments

### Takeaway
Conflicts cluster in three places: (a) **capability as relation or behaviour, not disposition**, in the Enterprise Ontology and ArchiMate; (b) **capability as including resources/context or as a design artefact**, in CDD/CaaS; (c) **bearer scope**, where IOF and UFO let any independent continuant or object, including artefacts, bear capabilities and CCO admits object aggregates. CCO's own parent class (realizable entity) is more general than BCO's disposition, but it does not contradict it. No formal source found conflicts with C5. The UFO maturity-as-quality pattern needs care for C6.

### Cited Findings
- Capability as relationship (actor ↔ activity specification): conflicts with C1/C4 — [Enterprise Ontology, AIAI PDF](https://www.aiai.ed.ac.uk/publications/documents/1998/98-ker-ent-ontology.pdf)
- Capability as behaviour element: conflicts with C1 and is criticised by UFO analyses — [Calhau et al. 2024](https://conferences.big.tuwien.ac.at/biweek2024/pdfs/biweek2024_paper_150.pdf)
- Capability as ability *and capacity (resources)* in context, and as a requirements/design element: conflicts with C1 and blurs C6 — [CaaS definitions](https://caas-project.eu/definitions/)
- Capability under realizable entity, not disposition: more general than C1, not contradictory — [CCO merged TTL (develop)](https://raw.githubusercontent.com/CommonCoreOntology/CommonCoreOntologies/develop/src/cco-merged/CommonCoreOntologiesMerged.ttl)
- Capability borne by any independent continuant (lathe, sensor): broader than C2, though C2 is a legitimate specialisation — [IOF Core.rdf](https://raw.githubusercontent.com/iofoundry/ontology/master/core/Core.rdf)
- Capability as an interest-relative disposition: BCO is silent on interest — [Beverley et al. 2024](https://www.arxiv.org/pdf/2405.00183); [IOF Core.rdf](https://raw.githubusercontent.com/iofoundry/ontology/master/core/Core.rdf)
- Authority-sense "capability" is a role and orthogonal to ability: agrees with C5 — [Beverley et al. 2024 §3](https://www.arxiv.org/pdf/2405.00183); the can/may split agrees with C5 — [Enterprise Ontology §4.1](https://www.aiai.ed.ac.uk/publications/documents/1998/98-ker-ent-ontology.pdf)
- Capability level (maturity) as a quality inhering in the capability (UFO): in tension with C6 and not directly expressible in BFO — [Calhau et al. 2024](https://conferences.big.tuwien.ac.at/biweek2024/pdfs/biweek2024_paper_150.pdf)

### Inferences
- **Authority ranking for BCO's purposes:** ISO/IEC 21838-2 (international standard) > CCO and IOF Core (community ontologies, BFO-aligned) > Azevedo et al. 2015, Bērziša et al. 2015, Uschold et al. 1998, Offerman et al. 2017 (peer-reviewed) > Calhau et al. 2024 (peer-reviewed workshop) > Beverley et al. 2024 and Jensen et al. 2024 (preprints; Jensen also at FOIS 2024) > CaaS web definitions (grey literature).
- The strongest formal backing for C1 + C2 + C5 together is Beverley et al. 2024 plus IOF Core. The strongest formal backing for C3's mechanics is BFO's `has material basis` definition combined with CCO Organization ⊑ object aggregate with member parts. That combination works for the *members*; the *arrangement* must be expressed some other way.

### Gaps
- None of the sources found treats capability maps or maturity assessments explicitly as ICEs (C6). That framing appears to be BCO's own, consistent with general BFO/CCO ICE practice, but no capability-specific citation was found.
