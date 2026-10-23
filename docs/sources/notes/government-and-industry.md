# Government/defence architecture frameworks and industry reference models: how they define "capability" (as of 23 October 2026)

Scope: a register of authoritative sources for the BCO. The BCO commitments being tested are:
(C1) a capability is a BFO disposition; (C2) it is borne by an Organization, not a person, system or role;
(C3) its material basis is the organization's member agents in their arrangement; (C4) it is realized in
business processes (BPO/APQC act types); (C5) ability is distinct from assignment, authorization or responsibility;
(C6) maps, assessments, maturity ratings, sourcing statements and target states are ICEs *about* capabilities.

Method note: about 25 tool calls (searches, fetches, one local PDF text extraction). dodcio.defense.gov,
dowcio.war.gov and tmforum.org returned HTTP 403 to the fetcher, so the DoDAF and TM Forum definitions below come
from search-engine extracts of those official pages, not from a full read. Where a claim rests on a secondary or
vendor page, it says so. Paraphrases are mine; quotations are under 15 words and attributed.

## Q1. US DoD: DoDAF 2.02 / DM2, JCIDS (CJCSI 5123.01), DoD Dictionary; is DoDAF current?

### Takeaway
DoDAF 2.02 (August 2010) is still the DoD CIO's stated "official and current" version in 2026. Its DM2
Capability is an *ability to achieve a desired effect* through combinations of ways and means (activities and
resources). That is ability-plus-resource-combination, close to BFO disposition-with-material-basis, but the
bearer is left general (resources/performers), not Organization. JCIDS, the source DM2 says it aligns with, was
ordered disestablished in 2025.

### Cited Findings
**Register entry: DoDAF 2.02 / DM2 Capability data group**
- Citation: *DoD Architecture Framework Version 2.02*, DoD Chief Information Officer, approved August 2010. A
  "Change 1" draft is dated 2015-01-19 (Vol I and Vol IV PDFs). The site is now also served under dowcio.war.gov
  with the same text. — [DoD CIO DoDAF home](https://dodcio.defense.gov/DODAF/); [DoDAF v2.02 PDF](https://dodcio.defense.gov/Portals/0/Documents/DODAF/DoDAF_v2-02_web.pdf); [Chg 1 Vol I draft](https://dodcio.defense.gov/Portals/0/Documents/DODAF2/DoDAF%20v2.02%20Chg%201%20Vol%20I%20Final%202015-01-19.pdf)
- Status: the DoD CIO site still describes 2.02 as the official, current version, approved as of August 2010. It
  also notes that DARS (the DoD Architecture Registry System) and the DoDAF Journal were removed as no longer
  supported. The Change 1 document is labelled DRAFT; I could not confirm it was finalized. — [DoD CIO DoDAF](https://dodcio.defense.gov/DODAF/dodaf2); [dowcio.war.gov mirror](https://dowcio.war.gov/DODAF)
- Canonical URLs: Capability meta-model page https://dodcio.defense.gov/DODAF/dodaf20_capability_mm; glossary
  https://dodcio.defense.gov/DODAF/dodaf20_glossary.aspx — [DoDAF capability data group](https://dodcio.defense.gov/DODAF/dodaf20_capability_mm); [DoDAF glossary](https://dodcio.defense.gov/DODAF/dodaf20_glossary.aspx)
- Licence: a US Government work, so public domain in the US (17 U.S.C. §105). No restrictive notice was observed in
  the search extracts. Redistribution is permitted.
- Definition, paraphrased: Capability is the ability to achieve a desired effect under specified (performance)
  standards and conditions, through combinations of ways and means (activities and resources), to perform a set of
  activities. DM2 says this matches the JCIDS Instruction. — [DoDAF Capability data group](https://dodcio.defense.gov/DODAF/dodaf20_capability_mm); [DoDAF glossary](https://dodcio.defense.gov/DODAF/dodaf20_glossary.aspx)
- Related DM2 semantics, paraphrased from the same page: ways and means are read in DM2 as Activities and
  Resources. A Desired Effect is a desired state of a Resource, so a capability is "about states". A Desired Effect
  is the result or outcome of an action. A Service normally does not supply the desired effect itself; it gives
  access to the activities and resources that would. — [DoDAF Capability data group](https://dodcio.defense.gov/DODAF/dodaf20_capability_mm)
- Short quotation (DM2 glossary): "The ability to achieve a Desired Effect under specified [performance] standards
  and conditions…" (truncated). — [DoDAF glossary](https://dodcio.defense.gov/DODAF/dodaf20_glossary.aspx)

**Register entry: JCIDS (CJCSI 5123.01 and the JCIDS Manual)**
- Status: the JCIDS Manual was last publicly updated in 2021, per a CRS primer (Nov 2024) that calls JCIDS the
  main DoD process for determining weapon-system requirements. — [CRS IF12817](https://www.congress.gov/crs_external_products/IF/PDF/IF12817/IF12817.4.pdf)
- Disestablishment: the SecDef memo "Reforming the Joint Requirements Process to Accelerate Fielding of Warfighting
  Capabilities" directs the VCJCS to begin disestablishing JCIDS at once. It recasts the JROC around an annual list
  of Key Operational Problems and creates a Requirements and Resourcing Alignment Board and a Mission Engineering
  and Integration Activity. Dates conflict: the press reports an August 2025 memo, and the official PDF on
  media.defense.gov is dated 7 November 2025 (posted 10 November). — [Official memo PDF](https://media.defense.gov/2025/Nov/10/2003819442/-1/-1/1/REFORMING-THE-JOINT-REQUIREMENTS-PROCESS-TO-ACCELERATE-FIELDING-OF-WARFIGHTING-CAPABILITIES.PDF); [Breaking Defense, Aug 2025](https://breakingdefense.com/2025/08/pentagon-terminating-jcids-process-as-part-of-larger-acquisition-reform-memo/); [Inside Government Contracts, Oct 2025](https://www.insidegovernmentcontracts.com/2025/10/jcids-rewired-what-dods-new-requirements-memo-means/)
- DOTMLPF-P is the JCIDS analysis lens for choosing non-materiel or materiel solutions to a capability gap. It is
  the first step of the Functional Solutions Analysis. (Secondary source: AcqNotes.) — [AcqNotes DOTMLPF analysis](https://acqnotes.com/acqnote/acquisitions/dotmlpf-analysis)
- Licence: CJCS documents are US Government works and public domain, unless a distribution limitation is marked.

**Register entry: DoD Dictionary of Military and Associated Terms (formerly JP 1-02)**
- Secondary sources attribute two "capability" senses to JP 1-02 (2009 ed.): (a) the ability to execute a
  specified course of action, with a note that it may or may not come with an intention; (b) the longer
  "desired effect under specified standards and conditions" form. — [SEBoK glossary: Capability](https://sebokwiki.org/wiki/Capability_(glossary)); [Wikipedia: Capability (systems engineering)](https://en.wikipedia.org/wiki/Capability_(systems_engineering))
- The dictionary says its terms are approved DoD terminology for general use by all DoD components (2010 ed., as
  amended through Feb 2016, hosted by DTIC). — [DTIC AD1029823](https://apps.dtic.mil/sti/html/tr/AD1029823/index.html); [FAS mirror of JP 1-02](https://irp.fas.org/doddir/dod/jp1_02.pdf)
- Licence: US Government work, public domain.

### Inferences
- BCO C1 (disposition): **agrees in substance.** "Ability … under specified conditions" has the shape of a
  disposition, realized when the conditions hold. The extra clause "through combinations of ways and means" puts the
  resources in the definiens, which mixes bearer/basis with the disposition. The BCO should cite DM2 as support for
  "ability", and say it rejects DM2's folding of resources into the capability.
- C2 (Organization bearer): **silent to mildly conflicting.** DM2 does not restrict the bearer. Capability is tied
  to Performers/Resources, and a system can be one.
- C3 (material basis = member agents in arrangement): **agrees in spirit.** "Combinations of … means (resources)"
  is the nearest framework analogue of a material basis.
- C4 (realized in processes): **agrees.** Capability is "to perform a set of activities". CV-6
  (capability-to-operational-activity mapping) is the DoDAF product for this.
- C5 (ability vs assignment): **silent.** DM2 does not mix in authority, but it gives no explicit separation either.
- C6 (description layer): **agrees structurally.** CV-1 to CV-7 are views, that is, descriptions about capabilities.
- Authority rating: government normative (DoD), though aging. DoDAF has not been formally replaced, and the JCIDS
  anchor is being dismantled. Expect DM2 to keep serving as a historical and structural reference.
- The DoD Dictionary "course of action" sense is pure ability. It is the clean ability-only definition in the US
  defence corpus, but it has no organizational bearer.

### Gaps
- The CV-1 to CV-7 product definitions were not retrieved this session; the DoD CIO pages returned 403. From the
  DoDAF 2.02 Vol II structure (not re-verified here) they are: CV-1 Vision, CV-2 Capability Taxonomy, CV-3
  Capability Phasing, CV-4 Capability Dependencies, CV-5 Capability to Organizational Development Mapping, CV-6
  Capability to Operational Activities Mapping, CV-7 Capability to Services Mapping. Verify against the
  [DoDAF v2.02 PDF](https://dodcio.defense.gov/Portals/0/Documents/DODAF/DoDAF_v2-02_web.pdf) before citing
  section and page numbers.
- No verbatim current CJCSI 5123.01 (letter version I or J?) definition was retrieved. A secondary site calls 5123.01I
  current; that is unconfirmed. It is unclear whether CJCSI 5123.01 has been rescinded since the 2025 memo.
- The current online DoD Dictionary entry for "capability" was not checked against the 2016 text. It needs a
  direct look at jcs.mil (Joint Electronic Library).
- No source found on whether DoD formally adopted OMG UAF in place of DoDAF.

## Q2. NATO Architecture Framework v4 (NAF) and the capability (C-) views; UAF lineage; MODAF

### Takeaway
NAF v4.1 (ArchiMate Implementation Guide, Architecture Capability Team / Digital Policy Committee, June 2026)
defines Capability as the *expected ability of one or more resources* to deliver an effect, outcome or course of
action. It separates Capability Configuration, a building block of people and technology that implements processes
to realize a capability, which is the nearest analogue of a BFO material basis. Like DM2, the bearer is resources,
not specifically organizations.

### Cited Findings
- Citation: *NATO Architecture Framework v4.1, ArchiMate Implementation Guide*, Architecture Capability Team,
  Digital Policy Committee, dated 2026.06 (cover). It is based on the OMG UAF 1.2 Domain Meta-Model and ArchiMate
  3.2. — [NATO PDF](https://www.nato.int/content/dam/nato/webready/documents/publications-and-reports/NATO-Architecture-Framework-ArchiMate-v4-1-en.pdf)
- C-views in this guide (table of contents): §5 C1 Capability Taxonomy (p.17), §6 C2 Enterprise Vision (p.20),
  §7 C3 Capability Dependencies (p.23), §8 C4 Standard Processes (p.25), §9 C5 Effects (p.27), §10 C7 Performance
  Criteria (p.30), §11 C8 Planning Constraints (p.32). No C6 section appears in this guide. — [NATO PDF](https://www.nato.int/content/dam/nato/webready/documents/publications-and-reports/NATO-Architecture-Framework-ArchiMate-v4-1-en.pdf)
- C1 (§5, p.17), paraphrased: C1 identifies capabilities and organizes them into specialization and aggregation
  taxonomies, *independent of their implementation*. It may group them (Capability Group) and attach Effectiveness
  Criteria. In ArchiMate, hierarchy is composition and specialization is the specialization relation. — [NATO PDF §5](https://www.nato.int/content/dam/nato/webready/documents/publications-and-reports/NATO-Architecture-Framework-ArchiMate-v4-1-en.pdf)
- Glossary (PDF p.154), paraphrased: **Capability** is the expected ability of one or more resources to deliver a
  specified type of effect or outcome, or a specified course of action. **Capability Configuration** is a solution
  building block that combines physical resources (people, technology) and implements processes to realize a
  Capability. **Capability Group** is two or more capabilities forming a complete unit (and may be a taxonomy).
  **Work Package** delivers changes to realize a Capability Increment. — [NATO PDF glossary](https://www.nato.int/content/dam/nato/webready/documents/publications-and-reports/NATO-Architecture-Framework-ArchiMate-v4-1-en.pdf)
- Short quotation: Capability is "The expected ability of one or more resources to deliver a specified type of
  effect". — NAF v4.1 ArchiMate Implementation Guide, glossary, p.154. — [NATO PDF](https://www.nato.int/content/dam/nato/webready/documents/publications-and-reports/NATO-Architecture-Framework-ArchiMate-v4-1-en.pdf)
- Phases and increments: C2 holds the Enterprise Phases (ArchiMate plateaus) that capabilities aim at. C8 (Planning
  Constraints) holds Capability Milestones, Capability Increments and the capabilities they deliver, and may trace
  Capability Configurations to Capabilities. — [NATO PDF §6, §11](https://www.nato.int/content/dam/nato/webready/documents/publications-and-reports/NATO-Architecture-Framework-ArchiMate-v4-1-en.pdf)
- Organization term in the same glossary, paraphrased: an organized group of people with a particular purpose, such
  as a business, a government department or a team. — [NATO PDF glossary](https://www.nato.int/content/dam/nato/webready/documents/publications-and-reports/NATO-Architecture-Framework-ArchiMate-v4-1-en.pdf)
- UAF lineage (vendor paraphrase of OMG UAF 1.2): Capability is the enterprise's ability to achieve a desired
  effect, realized through combinations of ways and means (e.g. CapabilityConfigurations) with specified measures.
  CapabilityConfiguration is a composite of physical and human resources assembled to meet a capability. —
  [No Magic UAF 1.2 docs](https://docs.nomagic.com/display/UAF12P2024x/Capability); [Unicom System Architect UAF CapabilityConfiguration](https://support.unicomsi.com/manuals/systemarchitect/1149/Architecting_and_designing/UAF2058937.html)
- UAF was built as a broader successor to UPDM, drawing on MODAF, DoDAF and NAF. — [NDIA 2016, Hause](https://ndia.dtic.mil/wp-content/uploads/2016/systems/18931_UAFHumanViewsV3.pdf)
- Licence: no copyright, licence or distribution statement surfaced in the extracted text of the NAF v4.1 guide
  (grep for copyright, licen, distribut found none). It is published openly on nato.int. — [NATO PDF](https://www.nato.int/content/dam/nato/webready/documents/publications-and-reports/NATO-Architecture-Framework-ArchiMate-v4-1-en.pdf)

### Inferences
- C1: **agrees.** "Expected ability" is dispositional wording; "expected" even hints at the unrealized character.
- C2: **conflicts on the letter.** The bearer is "one or more resources", which in NAF covers systems and
  equipment. But Organization is itself a NAF resource type, so an organization-borne capability is a permitted
  special case. The BCO narrows, and does not contradict, NAF.
- C3: **strong agreement.** Capability Configuration (people plus technology, arranged, implementing processes) is
  almost exactly "member agents in their arrangement". The BCO should note that NAF counts technology in the
  configuration, while the BCO limits the basis to member agents. Decide whether artifacts are part of the basis or
  only participants.
- C4: **agrees.** Configurations implement processes to realize capability; C4 is "Standard Processes".
- C5: **silent.** Roles and posts are separate NAF elements, and no capability-as-authority sense was seen.
- C6: **agrees.** C1 to C8 are viewpoints. Effectiveness Criteria are requirements attached to capabilities, which
  fits the BCO's ICE-about-capability layer.
- Authority rating: government (alliance) normative for NATO architecture work; current edition June 2026.
- MODAF: retired by the UK MOD in favour of NAF v4 / UAF (my understanding; no source retrieved this session). Its
  StV views were the ancestors of the DoDAF CVs and NAF C-views, so it adds nothing distinct here.

### Gaps
- The NAF v4 core documentation (Chapter 1-3, the NAF Meta-Model / NAF IM) was not retrieved. Definitions were taken
  from the ArchiMate implementation guide's glossary, which may paraphrase the NAF IM.
- No NATO capability *taxonomy* content (e.g. the NATO Defence Planning Process capability hierarchy) was retrieved.
  Its classification and access are unknown.
- The normative OMG UAF 1.2 text was not retrieved; only vendor paraphrases were used.
- MODAF retirement date and status were not sourced this session.

## Q3. US federal civilian: FEA Business Reference Model and the Federal Integrated Business Framework (FIBF)

### Takeaway
The FIBF (GSA Office of Shared Solutions and Performance Improvement, formerly USSM) treats "business capabilities"
as **outcome-oriented requirements** (needs) tied to authoritative references and data standards. It does not treat
them as abilities of organizations. In BCO terms, an FIBF business capability is a requirement-type ICE, not a
disposition.

### Cited Findings
- FIBF has five components: Federal Business Lifecycles (functions and activities), Business Capabilities, Business
  Use Cases, Standard Data Elements, and Service Measures. Business Capabilities are described as outcome-based needs
  linked to federal authoritative references, forms, inputs, outputs and data standards. The page gives no version,
  date or licence. — [GSA FIBF page](https://ussm.gsa.gov/fibf/)
- Short quotation: lifecycles are "comprised of functions and activities". — [GSA FIBF](https://ussm.gsa.gov/fibf/)
- In Federal Financial Management, the FIBF business capabilities are published as Federal Financial Management
  System Requirements (FFMSRs) in the FMCF-3 document (FY 2024 release on GSA; a Treasury v1.1 of 24 June 2022 was
  marked as proposed updates). — [GSA FMCF-3 FFMSRs FY2024](https://ussm.gsa.gov/assets/files/downloads/fm/FMCF-3%20FFM%20Business%20Capabilities%20(FFMSRs)_FY%202024%20Release.pdf); [Treasury FFMSR PDF](https://www.fiscal.treasury.gov/files/fmqsmo/ffm-business-capabilities-(ffmmsrs).pdf)
- Per-function FIBF pages exist (e.g. HR, Talent Development), and ICAM has its own FIBF. — [FIBF HR TD](https://ussm.gsa.gov/fibf-hr-td/); [ICAM FIBF](https://idmanagement.gov/icam-fibf/)
- Policy hook: OMB M-19-16 (April 2019) is linked from the FIBF page as the governing memo. — [GSA FIBF](https://ussm.gsa.gov/fibf/)
- FEAF-II: the Consolidated Reference Model (six reference models, including the BRM) gives OMB and agencies a common
  vocabulary for describing investments. The BRM organizes federal operations by mission and support areas and
  business functions, not by agency. (Secondary sources.) — [Wikipedia: FEA](https://en.wikipedia.org/wiki/Federal_enterprise_architecture); [CIO-Wiki CRM](https://cio-wiki.com/wiki/Consolidated_Reference_Model_(CRM))
- Licence: GSA, Treasury and OMB publications are US Government works, so public domain. No reuse terms appear on
  the FIBF page. — [GSA FIBF](https://ussm.gsa.gov/fibf/)

### Inferences
- C1/C2: **conflicts by category.** An FIBF "business capability" is a statement of what a business function must
  achieve or support (requirements in the FFMSRs). In the BCO it belongs in the description layer (C6) as a
  requirement or target-state ICE that *prescribes* a capability. It is not the capability.
- C4: **agrees indirectly.** FIBF capabilities hang off functions and activities, the counterpart of BPO act types.
- C5: **silent.**
- C6: **strong support.** The FIBF itself shows that "capability" in federal usage is often the name of a
  requirement record.
- Authority rating: government normative (OMB-mandated) for US federal shared services. The FEA BRM is legacy and
  largely dormant.

### Gaps
- No formal standalone definition of "business capability" was found on FIBF pages; the FFMSR PDF front matter
  was not read.
- FEA BRM 3.1 (2013) primary text was not retrieved. Its status in 2026 is unconfirmed (likely dormant).

## Q4. BIAN (banking)

### Takeaway
BIAN publishes a Service Landscape (current v14.0, February 2026) whose Service Domains are described as elemental
business capability partitions, plus a separate Business Capability Model aligned to it. The material is
copyright BIAN, "All rights reserved", and gated behind registration or membership. It is **not CC-BY**, so it
cannot be relied on for redistribution.

### Cited Findings
- Versions: Service Landscape 14.0 (Feb 2026), 13.0 (Jun 2025), 12.0 (Nov 2023), 11.0 (Dec 2022). The 11.0 notes
  list a new release of the Business Capability Model. The page shows "© 2026 BIAN. All rights reserved."
  Portal access needs a registration form, with member login for more. — [BIAN BCM page](https://bian.org/bian-business-capability-model/)
- Hierarchy, paraphrased (Open Group ArchiMate-BIAN, SL v7.0): a Business Area is too coarse to count as a
  capability; a Business Domain is a coarse, non-atomic business capability that partitions banking in a mutually
  exclusive, collectively exhaustive way; a Service Domain is the finest partition and the elemental building block,
  defining a unique, discrete business capacity. — [Open Group ArchiMate-BIAN ch.3](https://digital-portfolio.opengroup.org/archimate-bian/latest/01-doc/chap03.html)
- The BCM-to-Service-Landscape alignment paper (2023) carries "Copyright 2023 by BIAN Association. All rights
  reserved." — [BIAN BCM relationship PDF](https://bian.org/wp-content/uploads/2023/08/BIAN-BCM-Relationship-with-BIAN-Service-Landscape-Final.pdf)

### Inferences
- BIAN's "capability" is a functional partition of the banking business (what is done). It is used as a stable
  reference taxonomy, with the bearer implicit (the bank). C1: **silent** on ontology, and it reads as a
  function-type classification. C2: **implicitly agrees** (the enterprise). C4: **agrees** (service domains host
  service operations and behaviour). C6: a BIAN landscape is a capability-map ICE.
- Authority rating: de facto industry standard (banking), consortium-owned, restrictive licence. Cite it; do not
  vendor or embed its content.

### Gaps
- The exact licence text for the Service Landscape downloads (end-user terms) was not seen. Whether non-members may
  reuse names in an open ontology is unknown, so ask BIAN.
- No BIAN formal definition sentence of "business capability" was retrieved from the BCM paper body.

## Q5. APQC Process Classification Framework (PCF)

### Takeaway
APQC keeps the PCF as a **process** taxonomy and treats capabilities as a separate construct that combines people,
process, information and technology. APQC frames capabilities as what a firm needs on hand to do work, and processes
as the work. The PCF also has a process category for *managing* business capabilities (category 13.0 in v7.x/8.0).
The PCF is free with registration under APQC's licence terms (some industry versions co-developed with IBM).

### Cited Findings
- APQC article "Business Capabilities and How They Relate to Processes" (June 2024, full text members-only):
  capability models are combinations of people, process, information and technology, and identify the assets
  (tools, skills, capacities) needed to do work. — [APQC resource](https://www.apqc.org/resource-library/resource-listing/business-capabilities-and-how-they-relate-processes)
- PCF Category 13.0 "Develop and Manage Business Capabilities": definitions and key measures published for PCF
  version 8.0 (24 March 2026) and earlier 7.2.1. In v6.1.1 the category was 12.0. — [APQC 13.0 PCF 8.0](https://www.apqc.org/resource-library/resource-listing/130-develop-and-manage-business-capabilities-definitions-and-1); [APQC 13.0 PCF 7.2.1](https://www.apqc.org/resource-library/resource-listing/130-develop-and-manage-business-capabilities-definitions-and-0); [PCF 6.1.1 PDF (Qld Govt)](https://www.forgov.qld.gov.au/__data/assets/pdf_file/0027/319842/apqc_pcf_ver_6.1.1-final.pdf)
- Cross-industry PCF 7.4 (Aug 2024) is circulating. A copy is hosted by IFRC. — [PCF 7.4 PDF (IFRC copy)](https://solutions.ifrc.org/sites/default/files/2024-10/K014750_APQC%20Process%20Classification%20Framework%20(PCF)%20-%20Cross%20Industry%20-%20PDF%20Version%207.4.pdf)
- Licence: industry PCFs v7.2.2 were co-developed with IBM. They are subject to specific licence terms shipped
  inside the download, and 7.2.2 updated the licence and attribution language without changing framework elements.
  — [APQC Banking PCF 7.2.2](https://www.apqc.org/resource-library/resource-listing/apqc-process-classification-framework-pcf-banking-pcf-pdf-0)

### Inferences
- PCF 8.0 (March 2026) appears to be the current edition, superseding 7.4. **Check that BPO's pinned PCF version
  matches.** This is a version-drift risk for BPO and BCO.
- C3: **agrees in part.** APQC's "people, process, information, technology" is a DOTMLPF-like resource-combination
  view. That is a material-basis view, but the BCO's basis (member agents) is narrower than APQC's.
- C4: **agrees.** APQC explicitly distinguishes capabilities from the processes in the PCF and relates them, which is
  exactly the BCO's realized-in relation.
- C6: **agrees.** PCF 13.0 makes "define and manage business capabilities" a process. Its outputs (capability
  definitions, maps, assessments) are ICEs about capabilities.
- Authority rating: de facto industry (non-profit). Licence is free with registration plus attribution;
  redistribution of the framework text appears restricted (licence file not read).

### Gaps
- The PCF licence file text was not read. Redistribution, derivative-work and attribution clauses are unverified;
  read the licence shipped with the 7.4/8.0 download.
- Whether APQC publishes a standalone *capability model* (not just the article and category 13.0) was not
  established. None was found.
- The PCF 8.0 release date and changes to the cross-industry framework are only inferred from the category-13.0
  resource page.

## Q6. ITIL 4 and COBIT 2019

### Takeaway
Both use "capability" in senses that, for the BCO, sit mostly in the **description layer**. COBIT capability levels
(0-5) are ratings of how well a *process* performs, and maturity attaches to focus areas. ITIL (v3 lineage) separates
resources (things an organization has) from capabilities (the ability to use them), which is a useful ability-vs-basis
precedent.

### Cited Findings
- COBIT 2019 (ISACA, 2018-), paraphrased: each governance and management objective's process can operate at a
  capability level from 0 to 5, which measures how well it is implemented and performing. Maturity levels apply to
  focus areas. Figure 6.2 of *COBIT 2019 Framework: Introduction and Methodology* defines the levels (level 0: the
  process lacks basic capability). — [ISACA: effective capability and maturity assessment](https://www.isaca.org/resources/news-and-trends/industry-news/2020/effective-capability-and-maturity-assessment-using-cobit-2019); [ISACA: defining target capability levels](https://www.isaca.org/resources/news-and-trends/industry-news/2019/defining-target-capability-levels-in-cobit-2019-a-proposal-for-refinement)
- Level names vary across secondary guides; one study guide warns that the CMMI-style labels are not the official
  COBIT list. — [open-exam-prep COBIT 2019 §14.2](https://open-exam-prep.com/study-guides/cobit-2019/performance-management/capability-levels-0-5)
- ITIL (v3 glossary lineage), paraphrased: an asset is any resource or capability. Training material contrasts
  resources (things) with capabilities (the ability to use resources to create value). — [ITIL V3 Glossary (Univ. Utah copy)](https://it.utah.edu/_resources/documents/itil/ITILV3_Glossary.pdf); [Wikiversity ITIL Foundation](https://en.wikiversity.org/wiki/ITIL/Foundation/Service_Management)
- Short quotation (ITIL V3 training slides): "Capabilities are the ability to use resources to create value". —
  [SlideShare ITIL V3 Foundations](https://www.slideshare.net/slideshow/itil-v3-foundations-introduction-lifecycle-and-phases-29544649/29544649)

### Inferences
- COBIT C1/C2: **conflicts if read naively.** "Capability" in COBIT is a *process attribute rating*, not an
  organizational disposition. For the BCO, a COBIT capability level is a maturity/assessment ICE (C6), about a
  process or capability. This is the clearest example of why C6 is needed.
- ITIL C1/C3: **agrees.** Resource vs capability maps neatly to material basis vs disposition. C2: the ITIL v3 sense
  lets organizations, people, processes, applications and services all bear capability, so it **conflicts** with
  the BCO's organization-only bearer.
- Authority: COBIT 2019, de facto industry (ISACA, paid / member-discounted publications). ITIL 4, de facto industry
  (PeopleCert-owned since 2021, proprietary, paid).

### Gaps
- The ITIL 4 (2019) official glossary entry for "capability" was not retrieved. ITIL 4 wording may differ from v3;
  check the PeopleCert/Axelos ITIL 4 glossary.
- ISACA access terms for COBIT 2019 publications (free to members? priced for non-members) were not confirmed this
  session.

## Q7. TM Forum (eTOM, SID, ODA, Capability Map)

### Takeaway
The TM Forum Capability Framework / Business Capability Map (GB1029C v2.0.0; reference map GB1007A v4.0.0) defines a
capability as an ability possessed by an *active structure element* (organization, person or system), focused on
business outcomes. This is ArchiMate's definition, and it is broader than the BCO's organization-only bearer. ODA
did not map capabilities as of late 2024.

### Cited Findings
- Paraphrased: the TM Forum Capability Framework (TMF-CF) rests on Capability, an ability that an active structure
  element (organization, person or system) possesses, focused on business outcomes. The Capability Map is a
  building block of business architecture, used in value-stream modelling and portfolio planning. — [TM Forum GB1029C Capability Map v2.0.0](https://www.tmforum.org/resources/standard/gb1029c-business-capability-map-v2-0-0); [TM Forum Business Capability Framework](https://www.tmforum.org/oda/business-capability-framework-2)
- Related: GB1007A Business Architecture Capability Reference Map v4.0.0; GB1007 Business Architecture Concepts and
  Principles v3.0. — [GB1007A](https://www.tmforum.org/resources/standard/gb1007a-business-architecture-capability-reference-map-v4-0-0/); [GB1007](https://www.tmforum.org/resources/how-to-guide/gb1007-business-architecture-concepts-and-principles-v3-0)
- A TM Forum community thread (Oct 2024) notes that the ODA model still has no capabilities mapping; mapping of
  business capabilities, SID entities and ODA functions is in progress in GB1027C (Zero-Touch Partnering). —
  [TM Forum Community thread](https://engage.tmforum.org/discussion/business-capability-missing-from-oda)

### Inferences
- C1: **agrees** ("ability"). C2: **conflicts.** The bearer may be a person or system. C4: **agrees** (outcome
  focus, value streams). C6: the Capability Map is an ICE.
- Authority: de facto industry (telecoms). Many TM Forum standards are free to members and some are public; access
  for these documents is unconfirmed (tmforum.org returned 403).

### Gaps
- GB1029C / GB1007A access terms, publication dates and whether they are 2026-current were not verified.
- eTOM (GB921) and SID (GB922) contain no capability definition that I could confirm.

## Q8. Gartner, Forrester, vendors (LeanIX/SAP, Ardoq); classification across sources

### Takeaway
Gartner frames business capability modelling as representing the organization's "business anchor model"
independently of structure, process, people or domain. It is a statement about the *map*, not about what a
capability is. Vendors follow the ArchiMate/TOGAF "ability that a business possesses" pattern.

### Cited Findings
- Gartner IT Glossary, paraphrased: business capability modelling is a technique for representing an organization's
  business anchor model, independent of its structure, processes, people or domains. Short quotation: "independent
  of the organization's structure, processes, people or domains". — [Gartner glossary](https://gcom.pdo.aws.gartner.com/en/information-technology/glossary/business-capability-modeling)
- Ardoq ships BIAN v12.0 as a framework resource (vendor reuse of BIAN content). — [Ardoq help: BIAN v12.0](https://help.ardoq.com/en/articles/470398-frameworks-resources-bian-v12-0-in-ardoq)

### Inferences
- Gartner, on C6: **agrees.** The model is a representation, kept independent of organization and process, which
  supports treating capability maps as ICEs and capabilities as stable, process-independent entities. Authority:
  analyst (proprietary; glossary freely viewable).
- Classification of the sources by what "capability" denotes:
  - **Ability (disposition-like):** DoD Dictionary (course of action), NAF v4.1 ("expected ability of …
    resources"), UAF, TM Forum / ArchiMate, ITIL (ability to use resources).
  - **Ability via a combination of resources (DOTMLPF-P style):** DoDAF DM2 / JCIDS (ways and means), APQC article
    (people, process, information, technology), UAF/NAF Capability Configuration (the resource side, separated out).
  - **Effect/outcome or requirement:** FIBF (outcome-oriented needs / requirements), DM2 in part (capability "is
    about states" via Desired Effect).
  - **Functional partition / taxonomy node:** BIAN business domains and service domains.
  - **Rating of process performance:** COBIT 2019 capability levels.
- Only NAF and UAF give a separate, named thing for the arrangement of people plus technology that realizes the
  capability (Capability Configuration). That is the best authoritative precedent for the BCO's material-basis
  commitment (C3), and it contradicts C3 only in admitting technology.
- None of the sources found restricts the bearer to Organization (C2). Each is either silent or wider (resources,
  people, systems). C2 is a BCO design choice, defensible as a narrowing, not something the literature already holds.
- None explicitly addresses C5 (ability vs assignment/authority). The BCO would be the first to make that separation
  explicit; DoDAF CV-5 (capability to organizational development mapping) is the closest place where the two meet.

### Gaps
- Forrester's definition was not retrieved.
- The LeanIX (SAP) definition was not retrieved this session.
- The Ardoq definition was not retrieved this session.
- The ArchiMate 3.2 / TOGAF definition (The Open Group) was outside this brief. It is likely the common root of the
  TM Forum and vendor wording, so it is worth a separate register entry.
