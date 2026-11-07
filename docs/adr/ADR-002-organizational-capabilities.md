# ADR-002 — Organizational Capabilities and Their Realization

| Field | Value |
| --- | --- |
| Status | **ACCEPTED** 2026-11-07 by the architect (`docs/decisions/2026-11-07-adr002-accepted-cp0-complete.md`, act 1), as reviewed at `6aae53e`, SHA-256 `71f97176e14d4dfd7338e75284699be7fed5276473492c6b3f47a622c6a4bbf1`. This status line is the only change since |
| Date | 2026-11-07 |
| Drafted by | Claude Code (`claude-opus-5-5`), a software agent, at the direction of Aaron Damiano (`docs/decisions/2026-11-07-cp0-closeout-and-integration-authorized.md`, act A1) |
| Ratifies | The architect, Aaron Damiano |
| Consolidates | `specifications/Business-Capability-Ontology-v0.5.0-draft.3.md` at `c3f1ba2`, SHA-256 `2224f869b0ec7a1e31b0afc1c2b403ad222ea290c334bff48a93ebbb6516c574`, as ratified item by item from 2026-11-04 to 2026-11-07 |
| Conceptual baseline | CM-01, approved 2026-10-26, SHA-256 `292c8f36d64075b9663e159985a15b448aa933c3b5ed4baff3b2a556ca861ccc`. Where this ADR or the specification differs from CM-01 in meaning, CM-01 governs |
| Numbering | ADR-001 is BPO's. ADR-003 reserved this number "for specification v0.4"; the specification's §0 and §2 give it to v0.5 ("Lands as ADR-002 … once ratified"). This ADR follows the specification (consistency check, item 1) |

## Context

The specification v0.5.0-draft.3 carries seventeen design commitments (CD1 to CD17), ten
ratification items (RP-1 to RP-10) and two source exceptions. The architect has ratified all
of them, in eight acts. The specification itself is not edited after ratification, and it
stays a draft until CP-0 is approved. This ADR is where the ratified decisions are found
together, and it is the decision record the specification names.

**It adds nothing.** Each decision below is a summary of a ratified text; the ratified text
is the specification's §3 wording, read with the qualifications its ratification record
states. Where this ADR's wording and a ratified text differ, the ratified text governs and
the difference is a defect here. No question settled in those records is reopened.

## Decisions

### Grounding and admission (RP-1, RP-10)

Ratified 2026-11-04: `docs/decisions/2026-11-04-d4-rp1-rp10-ratified-option-b.md`, acts 5 to 7.
Carried from DP-1 (`docs/decisions/2026-10-25-dp1-rp1-grounding-boundary.md`) and DP-2
(`docs/decisions/2026-10-26-dp2-rp10-admission-attribution.md`).

| CD | Decision |
| --- | --- |
| **CD1** Bearer | A Business Capability inheres in an Organization (`cco:ont00001180`) and nothing else. A person's ability is a CCO Skill; member-wise and artificial-system abilities are CM-02's. This is a deliberate narrowing, its departures listed by source and clause |
| **CD2** Grounding basis | Four things are kept apart: the basis (the relevant member agent or agents, as organized; one can suffice; never an artifact or an abstract set), the arrangement, enabling conditions relevant to realization, and temporary constraints. The basis rule is a BCO modeling policy, not a CCO entailment. A basis is asserted only for an admitted type, and every asserted Business Capability instance has an identified member witness (CAP-35). Losing an essential platform does not by itself end a capability; a change in the basis triggers reassessment |
| **CD3** Admission and attribution | G1-T admits a type, once per class, with all five questions and the three review rules binding. G1-I attributes a capability to an organization, per claim. No interest condition. Staging is transitional |
| **Parent admission** | The joint RP-1 and RP-10 ratification is the architectural admission record of `bco:BusinessCapability` under `obo:BFO_0000016` and `cco:ont00000568`. It is not minted until formalization, and no specific class inherits admission from it |

### Realization (RP-2, RP-3)

RP-2 ratified 2026-11-04 (`docs/decisions/2026-11-04-rp2-ratified.md`); RP-3 ratified
2026-11-06 (`docs/decisions/2026-11-06-rp3-ratified.md`).

| CD | Decision |
| --- | --- |
| **CD4** Realization index | Every specific capability class carries one or more `bpo:enablesProcess` naming BPO act classes or genera; no index member is a capability class. `only` is optional and needs an exhaustiveness review. Observed realizations are checked on asserted data (CAP-21), and are performed by a member agent of the bearer, not merely participated in (CAP-34). With CAP-03, CAP-05 and CAP-30 |
| **Provider performance** | Assigned to RP-2. When another organization's staff perform the acts, the consumer bears no capability for them |
| **CD5** Development and realization | Developing a capability and realizing it are different relations. An act realizes C only when justified as an exercise of C. Ratified with RP-2 |
| **CD12** The index is an annotation | `bpo:enablesProcess` means admissible realization: no actual realization, causal enablement, exhaustiveness or bearer requirement. `bpo:requiresCapability` is withdrawn from BCO; the rejection is of its prerequisite reading, not a claim that BPO's declaration is inconsistent. BPO modules carrying it stay outside BCO's effective graph (`config/upstream-sources.yaml`, `excluded_modules`) |

### Commitments outside the register (CD6 to CD11)

Ratified 2026-11-05 as one decision (`docs/decisions/2026-11-05-cd6-cd11-ratified.md`).

| CD | Decision |
| --- | --- |
| **CD6** Overlap with Function | Not disjoint from BFO Function. Classification under `obo:BFO_0000034` only with a justification record (CAP-09) |
| **CD7** Not role or permission | No capability definition mentions assignment, responsibility, authorization, license or mandate |
| **CD8** Capacity, not exercise | No existential realization axiom. An unexercised capability is admissible and attributable |
| **CD9** Primitive classes, reviewed specialization | `rdfs:subClassOf` means specialization only, asserted after review of bearer, grounding and realization. Nothing is induced from the coverage register or APQC partonomy |
| **CD10** Member-wise bearing | `cco:ont00001954` for organization to capability. `cco:ont00001898` is member-wise and never stands in for a Business Capability |
| **CD11** Descriptions are about, not of | Description ICEs refer by `cco:ont00001808` and its subproperties. No ICE bears or realizes a capability. A sourcing statement is a two-party record by convention (CAP-23) |

### Agents (RP-4)

Ratified 2026-11-06 (`docs/decisions/2026-11-06-rp4-ratified.md`).

| CD | Decision |
| --- | --- |
| **CD13** Agent manifests describe | BPO's `agents.json` is routing description. It is no evidence that a software agent, or an organization, bears a capability, or that a BPO class passed G1-T. Software bears no realizable; the computing artifact is an enabling condition only where realization depends on it. What artificial systems bear is CM-02's. Each type-specific manifest record is modeled separately; BPO's file needs no change |

### Description and evidence (RP-6 to RP-9)

Ratified 2026-11-06 as one decision (`docs/decisions/2026-11-06-rp6-rp9-ratified.md`).

| CD | Decision |
| --- | --- |
| **CD14** Type references and findings | `bco:concernsType` for an ICE that concerns a class. A completed Capability Assessment concerns one type, states one presence finding, cites criteria and evidence, and records its as-of date. An incomplete evaluation is not an assessment, and insufficient evidence never becomes `absent`. Map entries and hierarchy establish no possession, specialization or parthood |
| **CD15** Closed-world evidence | Authorization Records, not Action Permissions, for prospective authorization; the applicability table adopted. An absence query returns "no applicable authorization recorded within the declared complete scope" or *unknown*, never a legal conclusion. A register with unresolved revocation or supersession is not declared complete |
| **CD16** Functional coverage and adequacy | Four questions kept distinct; integration, availability and adequacy never follow from component possession. A Standing Function designates a whole-function type only where one is defined and independently admitted. A register entry generates no subclass axiom, possession assertion or adequacy judgment (CAP-29, tested by generator and provenance tests) |
| **CD17** Information-layer scope | Seven description-layer classes: Capability Map, Capability Assessment, Capability Maturity Rating, Capability Sourcing Statement, Capability Sourcing Assessment, Capability Target, Capability Target-State Specification. The Functional Adequacy Assessment is a distinct category with three independently supported findings; whether it needs an eighth class is Stage 05's. Existing BFO and CCO constructs are evaluated before any class is minted, and the Extended Relation Ontology first for relations |

### Namespace (RP-5)

Ratified 2026-11-07 (`docs/decisions/2026-11-07-rp5-ratified.md`). Hash IRIs under
`https://fandaws.com/ontology/`, held by the architect, permanent for all five ADR-003 D1
namespaces: `bco#`, `bco-metamodel#`, `bco-catalog#`, `bco-sources#`, `bco-agents#`. Document
and vendored-extract IRIs stay under the slash path `bco/`, where no term is minted.
Resolution is a D8 obligation, version IRIs Stage 05's. BPO's namespace is BPO's.

### Sources (SE-1, SE-2)

Decided 2026-11-06 (`docs/decisions/2026-11-06-se1-approved-se2-closed.md`). SE-1 is approved
as an exception for ArchiMate 3.2, ISO 9000:2015 and ITIL, which stay at S in CD1's
departures; the departure rests on seven sources at V or P, TM Forum GB1029C among them. SE-2
is closed: DoDAF DM2 is at V for CD2's claim.

## Consequences

- **Nothing is minted by this ADR.** OWL classes and axioms wait for CP-0 and D5. Each
  specific capability type needs its own PASS G1-T record, and no generated candidate becomes
  an admitted class.
- **No new object property** is authorized by any decision above. Conceptual relationships
  are represented with existing BFO and CCO constructs or annotations, evaluated at Stage 05.
- **The specification stays a draft** until CP-0 is approved. Accepting this ADR does not by
  itself promote it to normative status.
- **Open issues stay open** with their owners and gates (the stage-completion record lists
  them): OI-1, OI-4, OI-7, OI-8, OI-9, OI-11, OI-13, OI-14, OI-16 to OI-25, and CM-01 Q-06,
  Q-07 and Q-12 to Q-14. None is decided here.

## Consistency check

The ratified decisions were read against one another and against CM-01. **No architectural
contradiction was found.** These are documentary discrepancies, none of which changes
meaning:

1. **This ADR's target.** ADR-003 and `config/repository-layout.yaml` reserve ADR-002 for
   v0.4. The specification gives it to v0.5, which the architect's records ratified. ADR-003
   is ratified and stays as written; the layout's description is corrected in the commit that
   adds this ADR.
2. **The specification's text is pre-ratification.** Its header, §3 ("Each is proposed, not
   ratified"), CD15 ("proposed for RP-7") and §10's register and statuses read as before.
   That is by design; the next reviewed version records the ratifications.
3. **CD1's departures table** shows TM Forum GB1029C at "S; L". The SE-1 record raised it to
   V. The record governs.
4. **Prefix.** The specification writes `ex:enablesProcess`; the RP-3 record writes
   `bpo:enablesProcess`. Same IRI. The rename is a CM-01 next-version candidate.
5. **CM-01's Assessment Criteria entry** is narrower than its Capability Assessment
   definition. The RP-6 to RP-9 decision follows the definition and lists the wording for
   CM-01's next reviewed version (`src/02_conceptual_models/README.md`).
6. **CD5's ratification** rests on the RP-2 reply, read as covering CD5; the RP-2 record
   then stated it as an act. The closure matrix noted the reading; no correction was made.

## What this ADR does not do

It ratifies nothing, and accepting it is the architect's act. It declares no part of CP-0
complete, mints and asserts nothing, makes no G1-I claim, and changes no other document's
meaning.
