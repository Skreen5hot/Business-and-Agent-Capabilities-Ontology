# RP-6 to RP-9 faithfulness check — the description layer and its evidence (CD14 to CD17)

| Field | Value |
|---|---|
| Status | **Decided 2026-11-06**: RP-6 to RP-9 ratified together (`docs/decisions/2026-11-06-rp6-rp9-ratified.md`). The text decided on is this check at `d525f32`; this status line is the only change since |
| Date | 2026-11-06 |
| Prepared by | Claude Code (`claude-opus-5-5`), for the BCO team |
| Closes, if decided | CP-0 closure matrix items 10 to 13, decision 4 (`docs/proposals/2026-11-05-cp0-closure-matrix.md`) |
| Text checked | `specifications/Business-Capability-Ontology-v0.5.0-draft.3.md` at `c3f1ba2`, SHA-256 `2224f869b0ec7a1e31b0afc1c2b403ad222ea290c334bff48a93ebbb6516c574`: CD14 to CD17, the §10 register rows, the description-layer and evidence-register term tables, and CAP-17, CAP-18, CAP-20, CAP-22, CAP-24, CAP-27 to CAP-29, CAP-31 and CAP-33 |
| Checked against | CM-01, approved (SHA-256 `292c8f36d64075b9663e159985a15b448aa933c3b5ed4baff3b2a556ca861ccc`): P3 and P4, the concepts from Capability Map to Functional Adequacy Assessment, and RL-16 to RL-39. The R9, R10 and R11 dispositions, accepted. R11's acceptance (`docs/decisions/2026-11-03-r11-disposition-accepted.md`) carries P-01 to P-07 into v0.5 and "changes neither CM-01, DP-1 nor DP-2" |
| Upstream IRIs | Each verified in the vendored extracts: `cco:ont00000853`, `cco:ont00000476`, `cco:ont00000974`, `cco:ont00001010`, `cco:ont00001811`, `cco:ont00000751`, `cco:ont00001910` and `obo:BFO_0000178` (*has continuant part*, the direction CD14 needs) |

## 1. One package or four

The closure matrix asked whether RP-6 to RP-9 are one package or four. This note checks
each on its own (§§2 to 5), so the architect can decide either way. They are one design:
- CD14's assessment pattern is what CD16 and CD17 build on;
- CD15's Authorization Record carries CD14's type reference;
- CD17's classes are what CD14 to CD16 constrain.

**Recommended: one collective act naming all four**, as for CD6 to CD11. Each section's
points can be stated in it.

## 2. RP-6 — type references and findings (CD14)

The register: "`bco:concernsType`; one assessment pattern; map entries and how to read
them; a mandatory finding; every completed assessment against identified criteria stating
a threshold, on cited and dated evidence, with an as-of date (`dct:date`); availability
and fragility recorded with the finding; an incomplete evaluation is not an assessment;
inadequate evidence is no finding". Status: "Revised (R5-04, R5-11, R10-03, R11)".

| CD14 (draft.3) | CM-01 (approved) | Faithful |
|---|---|---|
| An ICE that concerns a class carries `bco:concernsType`; no punning, no designator individuals | RL-18 *concerns type*: "refers to a kind, with no claim that an instance exists"; formal treatment left to Stage 05, where "the specification proposes an annotation" | Yes. CM-01 leaves the form open, and CD14 fills it as CM-01 anticipated |
| An assessment describes the organization, is about an instance only when one is identified, concerns one type and states one finding | Capability Assessment: "Concerns exactly one Capability Type; states exactly one Presence Finding; is about a particular Business Capability only when one is identified"; RL-16, RL-19, RL-22 | Yes, point for point |
| A map has its entries as continuant parts; each entry an assessment or a target; never a Functional Adequacy Assessment | Capability Map: "Its entries are its parts"; RL-17 *has entry*; the Functional Adequacy Assessment is "not a map entry" | Yes. `obo:BFO_0000178` *has continuant part* is the right direction |
| A map entry concerns a type; only an assessment's finding speaks of possession; levels and labels are not possession or parthood | Capability Map: "Listing a capability does not assert that it exists; the map's layout (levels, groupings) is not parthood among capabilities" | Yes. R11 P-05 and P-07 make it explicit for practitioners |
| Every completed assessment: exactly one presence value, at least one criterion, at least one dated evidence source, one as-of date | Capability Assessment: "stating that finding and citing its evidence and criteria"; Presence Finding: "Exactly one per assessment"; RL-20, RL-21 | Yes. The threshold and the as-of date are R11 additions (P-02, P-03), accepted for v0.5 without changing CM-01 |
| `partial` is partial coverage of the criteria, never part of a disposition | Presence Finding: "Partial never means a fraction of a capability" | Yes |
| Superseded rather than overwritten; supersession's form is OI-24 | Not in CM-01 | An R11 addition (P-03). It adds a rule without contradicting anything |
| Availability and member dependence are recorded as content, not as a finding (OI-25) | Capability Assessment: "The availability and sourcing of this capability are assessed here, never derived" | Yes. Both say *assessed, not derived*; CD14 adds that the content is not the presence finding |
| An incomplete evaluation is not an assessment; inadequate evidence is never `absent` | Capability Assessment's definition requires the finding and the citations; Evidence: assignment records "never suffice alone" | Yes. R10-03 follows from CM-01's definition, as CD14 says |

**No discrepancy in CD14.** One wording point in CM-01 itself:

- **Criteria.** CM-01's Assessment Criteria entry says criteria are "Required for a
  partial finding and for a sourcing assessment". Its Capability Assessment entry says
  every assessment cites "its evidence and criteria". R10-03 resolved this the stricter
  way, so CD14 and CAP-27 require criteria for every finding. CD14 follows CM-01's
  definition; the narrower sentence is a candidate for CM-01's next reviewed version, like
  R11's P-10. It needs no new version now.

Left open, and not settled by ratifying RP-6:
- OI-23, whether an incomplete evaluation is represented at all;
- OI-24, supersession;
- OI-25, recorded content.

`bco:concernsType` and `bco:assessedPresence` are minted at Stage 05, not by ratification.

## 3. RP-7 — closed-world evidence (CD15)

The register: "Authorization Records; JSON completeness manifest; typed validity dates;
applicability rules". Status: "Revised (R5-07)".

| CD15 (draft.3) | CM-01 (approved) | Faithful |
|---|---|---|
| OWL stays open-world; absence questions are answered over named graphs, complete only within a declared scope | Evidence Scope: "Turns an empty result into 'none recorded within the scope'; outside every scope the answer to an absence question is unknown" | Yes |
| An Authorization Record is about the agent, names the act class, has typed start and end dates, and cites its authority | Authorization Record: "About the acting agent; names one BPO Act Type; has a start and end date; cites its authority. Prospective"; RL-31, RL-32 | Yes |
| Not an Action Permission, because CCO's definition would assert a permitted act exists | Authorization Record: "Not an Action Permission"; Action Permission: "Never used for a prospective authorization" | Yes. `cco:ont00000751` is Action Permission in the extract |
| An Action Permission only for an act that occurred, and it `permits` it | Action Permission: "exists in this model only once there is an act to permit"; RL-33 | Yes. `cco:ont00001910` is *permits* |
| The manifest is JSON outside OWL; the answer is never "not authorized" | Evidence Scope: "Its representation (the specification's JSON manifest) is an implementation"; "'not authorized' is never an answer" | Yes |
| The applicability rules (act type, agent, period, overlap, several authorities, revocation, scope) | Not in CM-01. Authority: "deontic reasoning is out of scope" | Additions, consistent with CM-01. The "several authorities" rule keeps deontic reasoning out, as CM-01 does |

**No discrepancy in CD15.** Two points the architect accepts with RP-7:

1. **The applicability table is "proposed for RP-7"** in CD15's own words. Ratifying RP-7
   adopts it as written, each rule with its positive and negative fixture.
2. **Revocation has no representation yet** (OI-21). Until it does, a graph holding a
   revoked or superseded record may not be declared complete. That limits what can be
   answered; it is not a contradiction. The evidence-graph IRIs are OI-11.

The Dublin Core and schema.org terms CD15 uses (`dct:source`, `schema:validFrom`,
`schema:validThrough`) are not vendored. Checking them is D5 work under OI-8, not a CP-0
item.

## 4. RP-8 — functional coverage and adequacy (CD16)

The register: "Component possession only; conditional designation of a whole-function
class; integration, availability and adequacy as findings of a Functional Adequacy
Assessment, never derived". Status: "Revised (R9)".

| CD16 (draft.3) | CM-01 (approved) | Faithful |
|---|---|---|
| Four questions, each answered by a different thing, none inferred from another | CM-01 §6 and Standing Function: "Its coverage is component possession, not integrated ability" | Yes |
| The coverage register is keyed by the function's catalog concept and lists component capability classes | Coverage Register Entry: "Keyed by the standing function's catalog node"; RL-37, RL-38 | Yes |
| A Standing Function designates at most one whole-function class, never one of its components; bearing every component does not entail it | Standing Function: "Designates at most one whole-function Capability Type ... its whole-function type is never one of those components, and bearing all the components does not entail bearing it" | Yes, almost word for word |
| Integration, availability and adequacy are the three findings of one Functional Adequacy Assessment, never generated from CQ-12 | Functional Adequacy Assessment: "none of its findings is derived from them (CAP-29)" | Yes |
| No generated axioms; listing a component creates no subclass link | Coverage Register Entry: "Generates no specialization and no assessment" | Yes |

**No discrepancy in CD16.** CM-01's Q-07, whether a component may itself be a function,
stays open; CD16 does not decide it. CAP-29 is a generator and provenance test (R5-12), not
a shape. The coverage register file in §9 is created at formalization, and ratifying RP-8
does not require it now.

## 5. RP-9 — information-layer vocabulary (CD17)

The register: "Seven description classes, and the Functional Adequacy Assessment as a
category whose representation Stage 05 evaluates, each finding dated, against a stated
threshold, on cited evidence". Status: "Revised (R9, R10-03, R11 P-06)".

| CD17 (draft.3) | CM-01 (approved) | Faithful |
|---|---|---|
| Seven description classes: map, assessment, maturity rating, sourcing statement, sourcing assessment, target, target-state specification | CM-01 has a vocabulary entry for each of the seven, and an eighth, `bcom:AuthorizationRecord`. The specification counts that one separately as its evidence-register class (CD15) | Yes. Seven plus one is CM-01's eight |
| Three distinctions kept: statement and assessment; target and plan; rating and assessment | Capability Sourcing Assessment: "the arrangement (statement) and the dependence on it (assessment) are distinct"; Capability Target: "Says what end state, not how to reach it"; Capability Maturity Rating: "produced by an assessment" | Yes |
| The Functional Adequacy Assessment is a sibling of Capability Assessment: one organization, one Standing Function, no type, three findings, each met, partly met or not met against required criteria | Functional Adequacy Assessment, word for word in substance; RL-39 | Yes |
| Each finding dated, with threshold and evidence (R11 P-06); an incomplete one records no finding and never *not met* | Functional Adequacy Assessment: criteria "are therefore required"; the dating and the threshold are R11 additions | Yes, with R11's additions |
| Its representation is evaluated at Stage 05 before any class is added | Functional Adequacy Assessment: "how it is represented ... is for Stage 05 and specification v0.5 (RP-9)" | Yes. CM-01 hands this exact question to RP-9, and RP-9 hands it to Stage 05 (F-7) without presuming the answer |
| A type's meaning is stated once, in its class definition and catalog node; no description ICE restates it | Not in CM-01; TM-1 and OI-17 | An addition, consistent with Capability Catalog Concept |
| Presentation is the application layer's | Not in CM-01 | An R11 addition (P-06), which governs nothing in the ontology |

**No discrepancy in CD17.** Ratifying RP-9 fixes the seven classes and leaves the eighth
open. It mints none of them; each is minted in a formalization tranche.

## 6. Recommended disposition

**Ratify RP-6, RP-7, RP-8 and RP-9 together as carried in draft.3:** CD14 to CD17, with
the requirements that trace to them: CAP-17, CAP-18, CAP-20, CAP-22, CAP-24, CAP-27, CAP-28,
CAP-29, CAP-31 and CAP-33.

Make five points explicit in the ratification:

1. **RP-6.** Criteria are required for every Capability Assessment, following CM-01's
   definition and R10-03. CM-01's narrower sentence on Assessment Criteria is a wording
   candidate for its next reviewed version, and no new version is opened.
2. **RP-6.** OI-23, OI-24 and OI-25 stay open for Stage 05.
3. **RP-7.** CD15's applicability table is adopted as the rule set. OI-21 (revocation) and
   OI-11 (graph IRIs) stay open, with the completeness limit CD15 states.
4. **RP-8.** Q-07 stays open. CAP-29 is checked by generator tests.
5. **RP-9.** Seven description classes. The Functional Adequacy Assessment's
   representation is decided at Stage 05.

With RP-6 to RP-9 ratified, every register item except RP-5 is ratified. CP-0 would then
need RP-5, ADR-002 and the stage-completion record.

## 7. What this check does not do

It ratifies nothing and changes no text. It mints no class or annotation property, and adds
no candidate, object property or OWL. It opens no CM-01 version and decides none of the
open issues it names. RP-5, ADR-002 and the stage-completion record remain CP-0 obligations.
