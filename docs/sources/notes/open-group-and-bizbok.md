# The Open Group (TOGAF, ArchiMate) and the Business Architecture Guild (BIZBOK) as sources for "business capability"

Research date: 2026-10-23. Method note: since some point before this date, the Open Group's online
publication sites (pubs.opengroup.org, for both TOGAF 10 and ArchiMate 3.1/3.2) redirect
anonymous readers to an SSO login (identity.opengroup.org). businessarchitectureguild.org returned
HTTP 403 to the fetch tool. So the primary texts could **not** be read directly in this pass.
The findings below come from (a) the publisher's free sample of the TOGAF 10 Business Architecture
compilation (front matter, table of contents, referenced-documents list), (b) the Open Group
publications catalogue, (c) the Open Group licensing page, (d) press releases, and (e) secondary
sources that quote the definitions. Each claim says which kind of source it rests on. Anything I
know only from memory is in Gaps, marked "UNVERIFIED", and must not go into the ontology until
someone with Open Group or Guild access checks it against the text.

Copyright: per instructions, at most one verbatim quote under 15 words per source; the rest is
paraphrase.

---

## Q1. TOGAF Standard, 10th Edition, and the TOGAF Series Guides (Business Capabilities, Value Streams, Business Models, Organization Mapping)

### Takeaway
TOGAF 10 (C220, April 2022) puts business capability in a Series Guide, *Business Capabilities,
Version 2* (G211, 25 April 2022, which supersedes G189, June 2018). The guide treats a capability
as an ability of the business that people, processes, information and resources implement. It
keeps capability maps separate from organization, value-stream and process views and links them
by cross-mapping. The Organization Mapping guide says business units or third parties "possess
or use" capabilities, which partly supports and partly complicates BCO's
"borne by an Organization" commitment.

### Register entry: citation, URL and access
- **TOGAF Standard, 10th Edition**, a standard of The Open Group, document **C220**, published
  **April 2022**. Library URL: www.opengroup.org/library/c220. Source: the referenced-documents
  list in the TOGAF 10 Business Architecture compilation sample — [Van Haren sample PDF](https://download.boekhuis.nl/9789401809054_fragm-docb.pdf)
- **TOGAF Series Guide: Business Capabilities, Version 2**, document **G211**, ISBN
  1-947754-69-0, published **25 Apr 2022**. It **supersedes G189**, 29 pages, type "The Open Group
  Guide", status "Adopted", prepared by the Architecture Forum Business Architecture Work Stream. Canonical URL
  https://publications.opengroup.org/g211 (www.opengroup.org/library/g211 redirects there) —
  [Open Group publications catalogue](https://publications.opengroup.org/g211)
- **Version 1:** TOGAF Series Guide: Business Capabilities, **G189**, **June 2018** —
  [Van Haren sample, referenced documents](https://download.boekhuis.nl/9789401809054_fragm-docb.pdf)
- Companion guides, all April 2022: **Value Streams (G178)**, **Business Models (G18A)**,
  **Information Mapping (G190)**, **Business Scenarios (G176)**. The 2022 compilation also includes
  an **Organization Mapping** guide, whose document number did not appear in the sample's
  reference list. Other cited Open Group works: **Capability-Based Planning … Using the TOGAF and ArchiMate Standards (G193, July 2019)**;
  **Open Business Architecture (O-BA) Part I (P161, July 2016)**; **ArchiMate 3.1 (C197, Nov 2019)** —
  [Van Haren sample](https://download.boekhuis.nl/9789401809054_fragm-docb.pdf)
- Book form: *The TOGAF Standard, 10th Edition — Business Architecture* (Van Haren, 26 Apr 2022;
  a "2025 Update" was published 30 June 2025 and still lists Business Capabilities **Version 2**,
  so no Version 3 had appeared by mid-2025) — [Van Haren 2025 update listing](https://www.vanharen.net/store/the-togafr-standard-10th-edition-business-architecture-2025-update);
  [Van Haren 2022 listing](https://www.vanharen.net/store/the-togafr-standard-10th-edition-business-architecture)
- **Access:** the catalogue page says the HTML edition can be read online and that downloading
  requires a login. It does not say whether the download is free —
  [catalogue](https://publications.opengroup.org/g211). In this session, pubs.opengroup.org
  pages for TOGAF 10 redirected to an Open Group SSO login, so reading online now also appears to
  need a (free?) account (direct observation; the terms on the login page were not read). The
  book edition says "Copyright protected. Use is for Single Users only via a VHP Approved
  License" — [Van Haren sample](https://download.boekhuis.nl/9789401809054_fragm-docb.pdf).
  Redistribution: there is no evidence that it is allowed; treat it as **not redistributable**.
  Quote briefly with attribution.

### Cited Findings
- **Structure of G211 (verifiable section numbers, from the compilation's table of contents):**
  §10 "What is a Business Capability?". §10.1 Defining a Business Capability, with §10.1.1 Naming
  Convention and §10.1.2 Description. §10.2 "Elements to Implement Business Capabilities", with
  §10.2.1 **People**, §10.2.2 **Processes**, §10.2.3 **Information**, §10.2.4 **Resources**.
  §11 Business Capability Mapping: §11.1.1 Organizational Structure, §11.1.2 Business Model,
  §11.2.1 Business Capability **Stratification**, §11.2.2 **Leveling**. §12 Impact and Benefits.
  §13 Mapping to other perspectives: §13.1 **Heat Mapping**, §13.2.1 **Capability/Organization
  Mapping**, §13.2.2 **Capability/Value Stream Mapping**, §13.2.3 **Capability/Business Process
  Mapping**. §14 Using Capability Maps with the TOGAF Standard. (Section numbers are the
  compilation's: the guide is Part 2 of the book. The standalone G211 numbers its chapters from 1,
  so these become roughly §2–§6 there.) —
  [Van Haren sample ToC](https://download.boekhuis.nl/9789401809054_fragm-docb.pdf)
- **Value Streams guide (Part 3 of the compilation):** §17.3 "Mapping Capabilities to Value Stream
  Stages"; §19.2 "Mapping Value Streams to Business Capabilities"; §19.3 "Heat Mapping Scenario";
  App. B compares the value chain, value network and Lean value stream —
  [Van Haren sample ToC](https://download.boekhuis.nl/9789401809054_fragm-docb.pdf)
- **G211's purpose (Open Group's own summary):** it answers what a business capability is and how
  capability maps are built and aligned with other Business Architecture viewpoints for business
  planning — [catalogue](https://publications.opengroup.org/g211)
- **The Open Group's division of labour among the maps:** the compilation's front matter says
  capability mapping shows *what* a business does, value stream mapping shows *how it delivers
  value* to stakeholders, and the organization map identifies the business units or third parties
  that "possess or use those capabilities" and take part in value streams —
  [Van Haren sample, "This Document"](https://download.boekhuis.nl/9789401809054_fragm-docb.pdf)
- **Lineage:** the Business Models guide says it follows Business Architecture Guild best
  practice, and the compilation thanks the Guild for permission to reuse graphics. A Guild
  representative (Chalon Mullins) was a contributor to Business Capabilities version 1 —
  [Van Haren sample](https://download.boekhuis.nl/9789401809054_fragm-docb.pdf). TOGAF's
  business-capability material is therefore closely tied to BIZBOK, not independent of it.
- **Wording of TOGAF's definition (secondary sources only):** vendor documentation says
  "Business Capability" entered the TOGAF specification with **TOGAF 9.2**, beside the older,
  higher-level "Capability". It paraphrases the definition as an ability a business possesses or
  exchanges to achieve a particular purpose —
  [Unicom System Architect TOGAF help](https://support.unicomsi.com/manuals/systemarchitect/114100/Architecting_and_designing/TOGAF1495890.html).
  The same vendor glossary describes TOGAF's general "Capability" in capability-based-planning
  terms: a business-focused outcome delivered by completing one or more work packages —
  [Unicom (via search)](https://support.unicomsi.com/manuals/systemarchitect/114100/Architecting_and_designing/TOGAF1496371.html)
- **Capability Increment (secondary):** described as a discrete portion of a capability
  architecture that delivers specific value. When all increments are complete, the capability is
  realized — [Orbus glossary (vendor)](https://orbussoftware.com/resources/glossary/term/capability-increment)
- **Function vs capability in TOGAF 9.2 (critical secondary analysis):** Graham Berrisford
  reports that TOGAF 9.2 defines Business Function as something that delivers business
  capabilities closely aligned to an organization, and uses "function" to mean a unit of business
  capability. On that reading TOGAF largely equates function and capability, maps functions to
  organization units many-to-many, and defines capabilities independently of processes. He objects
  that a function cannot "deliver" a capability, because capabilities are used, not delivered —
  [Berrisford, "Functions and capabilities in business architecture and TOGAF"](https://grahamberrisford.com/00EAframeworks/03TOGAF/AMTOGpapers/Business%20architecture%20(inc%20capabilities%20and%20value%20streams)%20in%20TOGAF.htm)
  (TOGAF 9.2 wording, not re-checked against TOGAF 10).

### Bearing on BCO commitments (TOGAF 10 / G211)
| BCO commitment | TOGAF position | Basis |
|---|---|---|
| Capability is a disposition (an ability) | **Agrees in substance.** It is defined as an "ability" of the business, not as an activity or an asset | Secondary paraphrases above; G211 §10.1 title |
| Borne by an Organization, not a person/system/role | **Mostly agrees, with nuance.** The bearer is "a business"/"enterprise". The Organization Mapping guide says business units **or third parties** possess capabilities, so bearers include sub-organizations and external partners. TOGAF's older generic "Capability" (pre-9.2) is broader (UNVERIFIED wording, see Gaps) | Sample front matter |
| Material basis = member agents in arrangement | **Partly agrees / broader.** G211 §10.2 lists people, processes, information and resources as the elements that *implement* a capability. BCO would count only people (agents) as the material basis, and treat information as ICEs and resources as participants. TOGAF uses "implement" loosely | G211 ToC §10.2.1–10.2.4 |
| Realized in business processes | **Agrees.** §13.2.3 cross-maps capabilities to business processes, and capability is defined independently of process (Berrisford) | ToC; Berrisford |
| Ability distinct from assignment/responsibility | **Agrees implicitly.** Capability/organization mapping (§13.2.1) is a separate cross-map, and the organization map records who "possesses or uses" a capability. TOGAF does not formally separate possession from accountability | Sample front matter; ToC |
| Maps, assessments, maturity, target states are ICEs about capabilities | **Agrees in practice.** Capability maps, heat maps (§13.1) and capability increments (TOGAF capability-based planning) are architecture artifacts and deliverables, i.e. descriptions. "Capability increment" is an architecture-planning unit, and BCO should model it as a plan/ICE, not a part of the disposition | ToC; Orbus |

**Authority rating:** de jure consortium standard (TOGAF Standard, C220). The Series Guides are
"guidance" positioned as part of the standard rather than its normative core (the compilation
calls them the guidance part of the standard) — [Van Haren sample](https://download.boekhuis.nl/9789401809054_fragm-docb.pdf).
Practically, it is a **de facto industry standard**.

### Inferences
- Because G211 shares authors and graphics with the Guild, TOGAF and BIZBOK should be read as
  one family of definitions (ability-to-achieve-purpose), not two independent authorities.
- "Business units or third parties possess or use" means BCO must decide whether an
  organizational *sub-unit* can bear a capability (under CCO a sub-organization is itself a
  cco:Organization, so this is compatible) and how a capability "used" but not borne by the focal
  organization is represented (sourcing statements: BCO's ICE layer).
- G211's people/process/information/resources list is the familiar "PPT+information" bundle
  view. It conflicts with BCO only if read as *what a capability is*. G211's section title says
  these *implement* capabilities, which is compatible with treating them as the material basis
  plus participants.

### Gaps
- UNVERIFIED (memory; check in C220 "Introduction and Core Concepts", Definitions chapter, and
  G211 §1/§10.1): TOGAF 9.2 §3.21 defined Business Capability as a particular ability a business
  may possess or exchange to achieve a specific purpose. TOGAF 9.2 §3.27 defined Capability as an
  ability that an organization, person or system possesses. TOGAF 10 is believed to carry these
  forward in its Definitions chapter (Introduction and Core Concepts, Ch. 3), but the TOGAF 10
  section numbers could not be read. If the generic "Capability" definition is confirmed, it
  **conflicts** with BCO's organization-only bearer (it allows a person or system).
- TOGAF 10 definitions of Value Stream, Business Function, Business Service, Process and
  Organization Unit could not be read: the online text is behind SSO. Berrisford's
  quotations are TOGAF 9.2.
- G211's exact naming convention (§10.1.1: noun-based? "object + action"?) and its leveling and
  stratification scheme (§11.2.1–11.2.2: strategic/core/supporting?) were not seen.
- Whether a G211 Version 3 or a TOGAF 10 Business Capabilities update was published between
  July 2025 and October 2026 was not established. The latest evidence found (the June 2025
  compilation) shows Version 2.
- Whether the free online reading still needs only free registration, or now needs membership,
  is not confirmed. The SSO redirect was observed, but the terms were not.

---

## Q2. ArchiMate Specification: Capability, Resource, Value Stream, Course of Action, and what realizes a capability

### Takeaway
**ArchiMate 4 (released April 2026) is now the current edition**; 3.2 (2022) is superseded. In
3.x, Capability is a strategy-layer behavior element, defined as an ability that an **active
structure element — an organization, person, or system —** possesses, and it is realized by core
(business/application/technology) behavior elements. The bearer range **conflicts** with BCO's
organization-only commitment. The ArchiMate 4 strategy-domain text could not be read.

### Register entry: citation, URL and access
- **ArchiMate 4 Specification**, The Open Group, **released April 2026** (publisher listings: 24
  April 2026); document number not found. Downloads: https://www.opengroup.org/archimate-licensed-downloads —
  [Open Group licensed downloads](https://www.opengroup.org/archimate-licensed-downloads);
  [Van Haren listing](https://www.vanharen.net/store/archimater-4-specification)
- **ArchiMate 3.2 Specification**, The Open Group, **2022**. It was a comparatively minor revision of
  3.1 — [Visual Paradigm summary (vendor)](https://guides.visual-paradigm.com/2026/02/). The document
  number is believed to be C226, but this is UNVERIFIED; a search did not confirm it.
- **ArchiMate 3.1 Specification**, **C197**, **November 2019** —
  [Van Haren TOGAF BA sample, referenced documents](https://download.boekhuis.nl/9789401809054_fragm-docb.pdf).
  Online at pubs.opengroup.org/architecture/archimate31-doc/ (now behind SSO).
- **ArchiMate 4 Snapshot 1** (non-final working draft built on 3.2, mid-2025), publications.opengroup.org/s250 —
  [Visual Paradigm (vendor)](https://archimate.visual-paradigm.com/archimate-next-a-new-era-in-enterprise-architecture-modeling/)
- **Access/licence (ArchiMate 4):** download requires registration. ArchiMate Forum members get an
  annual Member Licence for internal use. Non-members get a free personal **90-day Evaluation
  Licence**, then either a free perpetual **Non-Commercial Licence** or an annual paid
  **Commercial Licence**. If no licence is taken, the documentation must be deleted. The page says
  nothing about redistribution: treat it as **not redistributable**. The licences also apply to
  translations — [Open Group licensed downloads](https://www.opengroup.org/archimate-licensed-downloads)

### Cited Findings
- **Capability definition (3.2):** the Open Group's 3.2 reference card and a community feedback
  issue give it as an ability that an active structure element, such as an organization, person,
  or system, possesses. They add that capabilities typically aim at goals or at delivering value by
  realizing an outcome, and that capabilities are realized by core elements —
  [Open Group ArchiMate community feedback issue #13 (via search; fetch blocked by bot protection)](https://community.opengroup.org/archimate-community/workgroups/archimate-feedback/-/issues/13).
  Short quote (ArchiMate 3.2): "an ability that an active structure element … possesses".
- **Section:** an exam-prep site places the definition in Chapter 7 (Strategy Elements). It cites
  §7.2 "Structure Elements", which looks wrong: Capability is a strategy *behavior* element —
  [certempire (low reliability)](https://certempire.com/exam/oga-031-exam-questions/question/3/).
  Treat the section number as unverified.
- **Relationships (secondary):** capabilities may serve other capabilities (3.1 spec, quoted via
  search). Vendor guides map Capability ← realized by Business Process/Function, and Value Stream
  ← realized by Business Process, and describe Resources as assigned to Capabilities. One vendor
  source has Capability realizing Value Stream, which contradicts the others —
  [Visual Paradigm ArchiMate 3.2 layer-integration guide (vendor)](https://www.visual-paradigm.com/guide/bridging-strategy-and-execution-a-comprehensive-guide-to-archimate-3-2-layer-integration/);
  [ArchiMate 3.1 Ch. 7 (search snippet)](https://pubs.opengroup.org/architecture/archimate31-doc/chap07.html)
- **ArchiMate 4 changes (secondary):** the concept count fell from about 60 to 42. Business,
  application and technology behavior were merged into a common domain, layers were renamed
  domains, Role and Collaboration were generalized, and relationship multiplicity was added. The
  removed elements reported are interactions, Constraint, Contract, Gap and Representation.
  Capability and Resource are **not** reported as removed or changed —
  [Visual Paradigm, "What's New in ArchiMate 4"](https://guides.visual-paradigm.com/2026/02/);
  [Visual Paradigm, ArchiMate 4 overview](https://archimate.visual-paradigm.com/archimate-next-a-new-era-in-enterprise-architecture-modeling/)
- **Academic critique:** an ontological (UFO-based) analysis of capability modeling in
  ArchiMate, aimed at language revision, exists: *Ontological analysis of advanced capability
  modeling in ArchiMate: a first step towards language revision* (NEMO group, UFES, 2024) —
  [NEMO PDF (server refused connection; title only)](https://nemo.inf.ufes.br/wp-content/papercite-data/pdf/ontological_analysis_of_advanced_capability_modeling_in_archimate_a_first_step_towards_language_revision_2024.pdf)
- **Maturity/assessment as description (vendor):** Bizzdesign (Marc Lankhorst, 21 Sep 2025)
  scores capabilities on strategic importance, maturity (across people, process, information,
  technology) on a CMMI-style five-level scale, and adaptability, using expert-panel Likert
  ratings. These are assessments *about* capabilities —
  [Bizzdesign blog](https://bizzdesign.com/blog/improving-the-use-of-capabilities-in-business-architecture/)
  (the URL served the post "Measuring Business Capabilities for Successful Transformation").

### Bearing on BCO commitments (ArchiMate 3.2; 4 presumed the same)
| BCO commitment | ArchiMate position | Basis |
|---|---|---|
| Disposition/ability | **Agrees:** "ability … possesses"; capability is a behavior-ish strategy element, distinct from the processes that realize it | Definition |
| Bearer = Organization only | **Conflicts:** organization, **person or system** may possess a capability | Definition |
| Material basis = member agents | **Partly agrees:** Resources (assets owned by an actor) are assigned to capabilities, and active structure is the possessor. ArchiMate does not distinguish bearer from material basis | Secondary relationship reports |
| Realized in business processes | **Agrees, with a different sense of "realize":** core behavior elements (processes, functions, also application/technology behavior) *realize* the capability. That is ArchiMate's design-time realization relationship (the element "is the implementation of" the capability), not BFO's process-realizes-disposition. Application/technology behavior also realizes capabilities, which would make non-organizational behavior a realizer | Secondary reports |
| Ability vs assignment | **Silent/partial:** assignment links active structure to behavior. There is no separate notion of authorization or responsibility for capabilities | — |
| Maps etc. are ICEs | **Silent:** ArchiMate models are themselves descriptions. Capability "increments"/levels are commonly modeled with specialization or plateaus, not as capability-intrinsic | — |

**Authority rating:** de jure consortium **normative standard** (The Open Group), and the de facto
EA modeling-language standard.

### Inferences
- ArchiMate's "realization" is a model-level traceability relation. Mapping it straight onto
  BFO `realizes` (process → disposition) would be a category mistake for application/technology
  behavior and for "resource realizes capability"-style vendor readings.
- ArchiMate's person/system bearer is the main formal conflict with BCO. BCO can call
  person/system "capabilities" *abilities* or *functions* of those bearers (BFO
  disposition/function borne by a person or artifact), and keep "Business Capability" for
  organizations.

### Gaps
- The ArchiMate 4 text for Capability, Resource, Value Stream and Course of Action was not read.
  It is unknown whether the definition, bearer range or realization rules changed.
- UNVERIFIED (memory): in 3.1/3.2, Ch. 7 numbering is §7.2 Structure Elements (§7.2.1 Resource),
  §7.3 Behavior Elements (§7.3.1 Capability, §7.3.2 Value Stream, §7.3.3 Course of Action), and
  a later section on relationships with motivation and core elements (Resource realized by core
  structure elements; Capability realized by core behavior elements; Course of Action realizes
  outcomes and is related to capabilities/resources). Value Stream was added in 3.1.
- The ArchiMate 3.2 document number and exact publication month were not verified.
- The content of the NEMO 2024 paper could not be retrieved.

---

## Q3. Business Architecture Guild, BIZBOK Guide

### Takeaway
The current edition is **BIZBOK Guide v15 (announced 8 April 2026)**; v14 came out on 26 March
2025. The Guild defines a business capability as a particular ability or capacity that a business
may possess or exchange to achieve a purpose or outcome. Its mapping principles describe *what*,
not *who/how*: capabilities are stable, non-redundant, defined once per enterprise, and
organization- and technology-agnostic, with many-to-many cross-maps to value streams and
processes. The Guide is free to Guild members. Non-member and redistribution terms were not
confirmed.

### Register entry: citation, URL and access
- **A Guide to the Business Architecture Body of Knowledge (BIZBOK Guide) v15**, Business
  Architecture Guild, announced **8 April 2026** (PRNewswire, San Francisco). v15 clarified the
  language, usage context and cross-mapping of Capability and Value Mapping, and updated reference
  models: Common, Financial Services, Government, Healthcare, IDO, Insurance, Manufacturing,
  Telecommunications, Transportation. The Guide is **free to Guild members** and is written by
  member volunteers — [v15 press release](https://digital-release.kxan.com/business/press-releases/cision/20260408SF29398/business-architecture-guild-releases-bizbok-guide-v15)
- **v14**, announced **26 March 2025**. It enhanced Capability and Value Mapping —
  [v14 press release](https://redmondspokesman.com/?p=22215)
- Canonical site: https://www.businessarchitectureguild.org (returned 403 to automated fetch).
- **Access:** member-only (free with membership; membership is paid, price not checked).
  Redistribution: no evidence that it is allowed; treat it as **not redistributable**. Several
  "bizbok_guide.pdf" hits on unrelated domains (php.net, fordham.edu, bps.go.id, sky.it subpaths)
  look like spam/piracy pages and were **deliberately not opened or used**.

### Cited Findings
- **Definition (BIZBOK, version unstated, quoted 2017):** a capability is a particular ability or
  capacity that a business may possess or exchange to achieve a specific purpose or outcome.
  Short quote: "a particular ability or capacity that a business may possess or exchange" —
  [Burlton, Business Rules Journal 18(10), Oct 2017](https://www.brcommunity.com/articles.php?id=b927)
- **Mapping principles (as reported by Burlton, citing the Guild):** capabilities are named as
  nouns or gerunds, while processes are verb–noun. The map is agnostic of organization and
  technology, concise and non-redundant, and describes what the business does, not how. It stays
  stable unless the business model changes. There is one map per enterprise, each capability
  defined once. An automated capability is still a business capability. Capabilities relate to
  value-creating processes many-to-many, and neither is decomposed into the other. A capability
  name carries no performance level —
  [Burlton 2017](https://www.brcommunity.com/articles.php?id=b927)
- **Tiers/levels (as reported by Burlton):** three categories, which Burlton calls Guiding, Core
  and Enabling. Mapping typically starts at three to four levels of decomposition —
  [Burlton 2017](https://www.brcommunity.com/articles.php?id=b927). (The Guild's own tier names
  may differ; see Gaps.)
- **Object-based naming critique:** BIZBOK ties each capability to a business object, which
  yields many "X Management" capabilities. This critique comes from a Bizzdesign author, per a
  search summary of [Bizzdesign](https://bizzdesign.com/blog/improving-the-use-of-capabilities-in-business-architecture/).
  The page fetched at that URL was a different post, so the attribution is weak.
- **Organization:** TOGAF's Organization Mapping guide, which is Guild-derived, describes the
  organization map as identifying the business units and third parties that possess or use
  capabilities — [Van Haren sample](https://download.boekhuis.nl/9789401809054_fragm-docb.pdf).

### Bearing on BCO commitments (BIZBOK)
| BCO commitment | BIZBOK position | Basis |
|---|---|---|
| Disposition/ability | **Agrees:** "ability or capacity" that a business "may possess" | Definition |
| Bearer = Organization | **Agrees:** the bearer is "a business". "Possess **or exchange**" adds a tradeable/sourced reading that BCO must model in the description layer (sourcing), not as transferring a disposition | Definition |
| Material basis = member agents | **Silent/neutral:** capabilities are defined independently of who and how; automation does not make one non-business | Burlton |
| Realized in processes | **Agrees:** many-to-many with processes, kept as separate domains. Value streams are enabled by capabilities through cross-mapping | Burlton; v15 release |
| Ability ≠ assignment | **Agrees:** organization-agnostic mapping; who possesses or uses a capability is a separate organization cross-map | Burlton; TOGAF org map |
| Maps/assessments are ICEs | **Agrees:** the map is an artifact. Performance and heat-mapping are cross-map assessments, and a capability name carries no performance level | Burlton |

**Authority rating:** **de facto industry standard** (practitioner body of knowledge from a
non-profit professional association). Not a formal standard, and not academic.

### Inferences
- The BIZBOK definition (ability *or capacity*, possess *or exchange*, *purpose or outcome*) is
  the most disposition-friendly of the three sources. BCO's draft definition is closest to it.
- "Capacity" brings in a quantitative reading (how much the business can do). BFO would treat
  that as a quality or measurement of the disposition, or as an ICE (assessment), not as part of the
  disposition.

### Gaps
- The v15 (or v14) definition text and its section numbers were not read. The definition above is
  from a 2017 secondary quote and may have been reworded since: v14 and v15 both "clarified"
  capability language.
- UNVERIFIED (memory): BIZBOK Part 2.2 (Capability Mapping) uses tiers named
  **strategic/direction-setting, core/customer-facing, supporting**, and up to level 1–6
  decomposition. BIZBOK also defines a **"capability instance"** (where a capability is
  implemented in a business unit or partner, used for capability-to-organization cross-mapping and
  heat-mapping) and "capability behavior" in its metamodel. These would map well onto BCO
  (instance ≈ a specific organization's bearing of the disposition). Not confirmed.
- Non-member access (purchase? excerpt chapters?), licence wording and quoting terms were not
  confirmed: the site returned 403. Reference-model access terms (members only?) were not confirmed.
- No verified Guild text was found on capability assessment/heat-mapping scales.

---

## Q4. Formal conflicts among the sources

### Takeaway
All three agree that a capability is an **ability** (not an activity, not an asset) and describes
*what* rather than *how*. They differ on **(a) bearer range**: ArchiMate allows any active
structure (organization, person, system); TOGAF and BIZBOK say "a business", with third parties
possible. They differ on **(b) constitution**: G211 lists people, process, information and
resources as implementing elements, which the bundle view reads as constitutive. And on **(c)
"realization"**: in ArchiMate it is a model traceability relation, not a BFO process-realizes-disposition.

### Cited Findings
- ArchiMate bearer = organization, person or system —
  [Open Group community issue (via search)](https://community.opengroup.org/archimate-community/workgroups/archimate-feedback/-/issues/13)
- BIZBOK bearer = "a business"; possess **or exchange** —
  [Burlton 2017](https://www.brcommunity.com/articles.php?id=b927)
- TOGAF org map: business units **or third parties** possess or use capabilities —
  [Van Haren sample](https://download.boekhuis.nl/9789401809054_fragm-docb.pdf)
- TOGAF G211 §10.2: People, Processes, Information, Resources implement capabilities —
  [Van Haren sample ToC](https://download.boekhuis.nl/9789401809054_fragm-docb.pdf)
- TOGAF (9.2) treats function as a unit of capability, a conflation that Berrisford criticizes —
  [Berrisford](https://grahamberrisford.com/00EAframeworks/03TOGAF/AMTOGpapers/Business%20architecture%20(inc%20capabilities%20and%20value%20streams)%20in%20TOGAF.htm)
- TOGAF's generic "Capability" in capability-based planning is outcome/work-package oriented
  (secondary) — [Unicom](https://support.unicomsi.com/manuals/systemarchitect/114100/Architecting_and_designing/TOGAF1496371.html)

### Inferences
- "Ability" (TOGAF/BIZBOK/ArchiMate) aligns with a BFO disposition. "What the business does"
  (mapping guidance) is a *description* slogan, not a competing ontology. The real competitor is
  the **bundle** view (capability = people + process + information + technology). BCO answers it
  by splitting the bundle: people → material basis; process → realization; information/technology
  → participants or ICEs.
- TOGAF's planning-sense "Capability" (an outcome delivered by work packages, built in
  increments) is a different sense from the business capability. BCO should treat it as a
  planned/target-state ICE, not as a disposition.

### Gaps
- No primary text from any of the three sources was read in this pass, because of SSO and 403
  barriers. Before RP ratification, someone with an Open Group account and Guild membership
  should check every UNVERIFIED item above, especially TOGAF 10 Ch. 3 definitions, G211 §10.1,
  ArchiMate 4 Strategy chapter, and BIZBOK v15 §2.2.
