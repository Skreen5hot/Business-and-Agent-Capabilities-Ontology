# BCO roadmap

**Status: revision 2, approved by the architect on 2026-10-31; it is the governing
development plan** (`docs/decisions/2026-10-31-roadmap-revision-2-approved.md`). It orders work and authorizes none: each step starts only
when the architect authorizes it and its entry gate is met. No ontology class, object
property, subclass axiom or vocabulary ratification is authorized by it.

| Revision | Date | What |
|---|---|---|
| 1 | 2026-10-30 | Proposed after the architect directed that the plan recommended after the Ontology Template exchange be followed (`docs/decisions/2026-10-30-template-not-adopted-roadmap-directed.md`) |
| 2 | 2026-10-30 | Revised under the architect's direction approving revision 1 in principle and deciding AD-1 to AD-3 (`docs/decisions/2026-10-30-roadmap-direction-ad1-ad3.md`). Section 12 maps that direction to this text |

It replaces HANDOFF §7, which dated from the repository's setup.

## 1. What governs this roadmap

### Architectural decisions (approved 2026-10-30)

- **AD-1 — Business Capability first; Agent Capability follows.** The first formal release
  covers Business Capabilities, on the approved CM-01 baseline. Agent Capability follows
  through CM-02. Completing CM-02 is not a prerequisite for Business Capability
  formalization; an approved CM-02 is a prerequisite for formalizing any Agent Capability
  extension.
- **AD-2 — Domain-practitioner review before specification ratification.** It comes before
  CP-0 (D4), evaluates CM-01 for enterprise capability modeling, and supplements, without
  replacing, the architect's approval of CM-01.
- **AD-3 — Reviewed terminology and taxonomy per formalization tranche.** Stage 05 does not
  formalize a set of classes until the terminology and taxonomy for that tranche are
  reviewed. It is per tranche, not a whole-taxonomy prerequisite.

### Decisions this roadmap preserves and does not reopen

- CM-01's approved conceptual baseline (2026-10-26), with its stakeholder-review erratum.
- DP-1, the organizational grounding decision.
- DP-2, the separation of type admission (G1-T) from instance attribution (G1-I).
- The accepted R8 and R9 dispositions.
- The approved inventory and licensing decisions, including the closure decision of
  2026-10-30.
- The BPO namespace migration and its recorded identifier mappings (2026-10-28).
- The documented BPO realization-index and shared-class issues, retained as formalization
  dependencies (CM-01 Q-12 to Q-14).

### Principles from the Ontology Template exchange

The BCO does not adopt the template. From the exchange (`communications/example/`):

1. One decision path, with terminology and source-evidence lanes beside it, joining at
   named gates. No lane writes an OWL axiom.
2. A standard before a stage.
3. Source terminology is not vocabulary is not taxonomy is not an OWL subclass assertion.
   No lexical match, catalog relationship, source hierarchy or taxonomy link becomes an
   axiom by itself.
4. A review counts for the gate its kind meets; every review record states the capacity the
   reviewer acted in.
5. A decision names the documents it changes, and each of them carries it.
6. Closure before each new phase, distinguishing blocking from deferrable issues.

## 2. Modules and the release boundary

| Module | Conceptual baseline | Path | Release |
|---|---|---|---|
| **Business Capability** | CM-01, approved | D3 to D8 | the **first release**. It covers Business Capabilities and is not represented as covering the Agent Capability domain |
| **Agent Capability** | CM-02, to be modeled, practitioner-reviewed and approved under the Stage 02 standard | its own Stage 05 tranches after CM-02's approval, through the same gates | a later release |
| **Integrated ontology** | CM-01 and CM-02 | integration and validation of both modules | only after it may a release claim comprehensive Business and Agent Capability coverage |

Approving the Business Capability module authorizes no Agent Capability ontology class.
Stage 05 work on the Business Capability module is not blocked because CM-02 is
unfinished.

## 3. Where things stand (2026-10-30)

| Stage or item | State |
|---|---|
| Specification | v0.4.0-draft.1; predates CM-01; nothing ratified; CP-0 not met |
| Stage 01, controlled vocabulary | 14 concepts (9 metamodel, 5 catalog), all Draft; no Stage 01 standard (ADR-003 stands in) |
| Stage 02, conceptual models | CM-01 approved 2026-10-26 (stakeholder-review erratum of 2026-10-30); CM-02 planned, not started |
| Capability Term Inventory (Stage 01 source evidence) | I-1, I-2a, I-2b, I-2c and E7 done; closure set complete; E4 method decided, nothing judged; I-3 to I-5 not authorized |
| Stage 03, taxonomy | not started; no standard |
| Stage 04, thesaurus | not started; no standard |
| Stage 05, ontology | specified, not written; no standard beyond the specification's gates |
| Stage 06, knowledge graph | not started; no standard |

## 4. The decision path

Each step's exit is the next step's entry gate, except where a row says otherwise.

| Step | What | Entry gate | Standard | Exit |
|---|---|---|---|---|
| **D1** | **This roadmap**, with AD-1 to AD-3, the modular release boundary and the gates below | the architect's direction of 2026-10-30 | — | the architect's final approval; it then governs |
| **D2** | **CM-02 scope and integration boundary**: Agent Capability's scope; its relation to CCO's Agent Capability, Organization Capability and Skill, and to CM-01's approved organizational grounding (DP-1). Scope only | D1, and the architect's authorization | Stage 02 standard | the architect approves the scope note. Full CM-02 is **not** required for any Business Capability step |
| **D3** | **Specification v0.5** for the Business Capability module (section 5), and the **domain-practitioner review** of CM-01 (section 6) before v0.5 is submitted for ratification | D1, and the architect's authorization. D2's approved scope is carried in when available, and is required before D4 | the specification's review process; the Stage 02 standard for the review of CM-01 | a review round answered; the practitioner review recorded, its dispositions accepted and carried into v0.5; the architect accepts v0.5 for ratification |
| **D4** | **CP-0**: accepted practitioner-review dispositions; RP-1 to RP-10 and every other applicable specification decision ratified; ADR-002 accepted; the permanent namespace decided (RP-5) | D2 and D3 | spec §10 | the architect's ratification acts, recorded with a stage-completion record |
| **D5** | **Formalization readiness**: the Stage 05 standard; the validation architecture; the reviewed terminology and taxonomy baseline for the first tranche (section 7); the BPO integration dependencies validated (Q-12 to Q-14) | D4; T1, T2 and T3; for the first tranche, T8's reviewed baseline | — (writing the standard is part of the step) | the architect approves the standard, the validation architecture and the first tranche's readiness |
| **D6** | **Stage 05 formalization**, Business Capability tranches: class-by-class G1-T admission; BFO/CCO alignment verified against the pins; CP-1 and CP-2; the conceptual-fidelity gate | D5, per tranche | Stage 05 standard; spec gates A–D, C-A, M, D2, F | CP-2 met for the tranche; conceptual fidelity passes; a stage-completion record |
| **D7** | **Stage 06 knowledge graph**: G1-I evidence-backed attributions on recorded assessments; the coverage register; the `bc:` migration; the applicable instance-level requirements; CP-3 | D6, and an approved Stage 06 standard | Stage 06 standard | CP-3 met; a stage-completion record |
| **D8** | **Release** of the Business Capability module | D7, and an approved release standard | release standard | dependency checks, licensing review, consumer-impact assessment (OI-10) and versioned-release evidence recorded; the architect authorizes publication |

## 5. What specification v0.5 does (D3)

1. **Carries the approved decisions forward**, with a table naming each decision and the
   sections it changes:
   - DP-1 (RP-1) into CD1 and CD2, and the organization-only bearer's departures by source
     and clause (CM-01 Q-08);
   - DP-2 (RP-10) into CD3 and §8 (G1-T and G1-I);
   - the R8 and R9 corrections: Functional Adequacy Assessment, conditional standing-function
     designation, whole-function against component types, and "relevant to its realization"
     into CD16 and CD17; and OI-15;
   - the CM-01 stakeholder-review erratum;
   - D2's approved CM-02 scope, as the module boundary;
   - the practitioner review's accepted dispositions (AD-2).
2. **Cites its sources by register id**, at V or P or under an approved exception (the
   source-adequacy gate). v0.4 cites no register entry by id; 26 of the register's 63
   entries have no claim at V or P.
3. **States how three formalization questions will be settled**, without reopening DP-1 or
   DP-2. Each is a formalization issue unless its investigation shows a genuine
   contradiction with approved conceptual meaning, which goes to change control:
   - **Material basis and disposition.** The question is how to represent an admitted
     capability type consistently with BFO and the existing decisions. The formal
     disposition and material-basis pattern applies to a specific Business Capability type
     only after its G1-T admission.
   - **Standing-function designation.** Conditional designation is represented with
     existing information-entity, annotation and validation patterns, evaluated during
     formalization, reusing BFO/CCO relations wherever possible. A conceptual relationship
     authorizes no new object property.
   - **Capabilities never exercised.** The existence or attribution of an unrealized
     capability is distinct from the absence of recorded realizations. Closed-world evidence
     rules apply to bounded absence queries (CD15), never as a condition for bearing a BFO
     disposition.
4. Corrects the `ex:` prefix to BPO's genera only (the 2026-10-28 re-pin, R3).

## 6. Domain-practitioner review (AD-2)

Before D4. It supplements the architect's approval of CM-01; it does not replace it.

- **Reviewer and capacity.** At least one practitioner, each named with the capacity
  acted in: a business architect, a capability-planning practitioner, or a FIBF
  standards-lead-agency analyst.
- **What it evaluates in CM-01:**
  - whether Business Capability definitions reflect recognizable organizational
    abilities;
  - whether the boundaries among capability, process, skill, authorization and enabling
    condition are defensible;
  - whether functional coverage and adequacy support actual capability-planning
    decisions;
  - whether representative sourcing, dormant-capability and organizational-grounding cases
    behave as intended.
- **What it records:** reviewer, capacity, findings, proposed dispositions, and the
  artifacts each finding affects.
- **What follows:** accepted dispositions go into v0.5 before CP-0. A finding that requires
  changing CM-01 goes through change control: a new, reviewed version of CM-01, never a
  silent edit.
- **CM-02** has its own practitioner review before its approval.

## 7. Stage 05 readiness, per tranche (AD-3)

A tranche is a named set of candidate classes proposed for formalization together. Stage 05
formalizes a tranche only when its readiness record holds:

1. the list of candidate ontology classes;
2. reviewed preferred terms and definitions;
3. the conceptual distinctions, and the candidate BFO/CCO parents;
4. source provenance and supporting evidence, under the source-adequacy and rights gates;
5. reviewed taxonomic relationships, where applicable;
6. G1-T admission evidence for each class, before it is asserted as an admitted Business
   Capability disposition;
7. traceability to CM-01, the applicable competency questions and the ratified
   specification;
8. the tranche-specific terminology relationships that affect formalization, resolved.

The readiness review keeps four things apart: **source terminology**, **vocabulary
ratification**, **taxonomy classification** and **OWL subclass assertion**. A complete
Stage 03 taxonomy or Stage 04 thesaurus is not a prerequisite.

## 8. The terminology and source-evidence lane

These run beside the decision path. None writes an OWL axiom.

| Step | What | Entry gate | Joins the path at |
|---|---|---|---|
| **T1** | **Stage 01 standard.** Approved before any further vocabulary ratification. Existing artifacts and decisions are preserved; gaps against the standard are identified, and completed work is invalidated only for a material defect | D1, and authorization | before any vocabulary ratification (T2) |
| **T2** | **Vocabulary review and acceptance**, under T1. Vocabulary acceptance is separate from G1-T admission: a catalog concept may be accepted as a vocabulary item without establishing that it designates an admitted BFO disposition class. The five catalog concepts are reviewed against the R6 rewrite | T1 | metamodel terms follow the ratified specification (D4); tranche terms feed the readiness record (section 7) |
| **T3** | **Terminology reconciliation**: the 14 draft concepts against approved CM-01, including Functional Adequacy Assessment, documenting which conceptual categories need a vocabulary entry, which reuse an existing term, and which need none. No entry is created automatically for every conceptual-model concept | D1, and authorization | before D5 |
| **T4** | **Homonym register**, seeded from the inventory's findings (ISO/IEC 33020 and CMMI "capability"; FIBF "business capability", flag E5), as source evidence | authorization | Stage 04 takes it up under its standard (T8); tranche readiness consults it |
| **T5** | **Inventory I-3** (restricted catalogs, citation and coverage only), **I-4** (crosswalk, deduplication, triage) and **I-5**, each authorized separately. Source provenance, licensing restrictions, and the line between candidate terminology and admitted classes are preserved | each phase's authorization; the rights and provenance gate for every new source | I-4 feeds T8 and tranche readiness |
| **T6** | **E4 standing-function judgments**, on the approved CM-01 criteria and the decided E4 method (Option A). Not dependent on choosing OWL properties; formal representation belongs to Stage 05 | authorization | D6, where designation is represented |
| **T7** | **First catalog tranche** (I-5): a recommendation of candidates, for the architect's separate approval. Candidates, not type admissions: each class still needs G1-T and the formalization review | I-4, and D4 (it applies the ratified admission test) | a tranche readiness record (section 7), then D6 |
| **T8** | **Stage 03 taxonomy** and **Stage 04 thesaurus**, each after its standard is approved. A reviewed taxonomy baseline for each formalization tranche; full completion is not a prerequisite for Stage 05 | each stage's standard; I-4 for the taxonomy | each tranche's readiness record |

## 9. Governance gates

| Gate | Requirement | Applies at |
|---|---|---|
| **Standard supplied** | a stage starts only under its approved standard | every stage; the release |
| **Practitioner review** | a recorded review: reviewer, capacity, findings, dispositions, affected artifacts | before CP-0 (D3–D4) for CM-01; before CM-02's approval; after any substantive CM-01 change |
| **Source adequacy** | a source a specification or decision relies on is at the required status (V or P), or under a documented exception approved specifically: the affected claims, the justification, the approving authority, and the stage by which it must be closed | D3; every decision record; tranche readiness |
| **Rights and provenance** | the decision authority for licensing and redistribution is the architect, as on every rights decision so far (I-2a, the APQC decisions, E7, the closure decision), unless the architect designates another (open decision O-2). No harvesting or publication beyond the approved rights posture | every new source (T5); the site; D8 |
| **Conceptual fidelity** | every authored class and logical axiom traces to its governing conceptual model, the ratified specification, or a separately approved architectural decision. An incompatibility found in formalization goes to change control; meaning is never changed silently | D6; the Agent Capability module's formalization |
| **Decision propagation** | every decision record names the documents it changes, and each of them cites it | every decision |
| **Closure** | blocking decisions are distinguished from deferrable issues. A deferred issue has a named owner, rationale, affected dependencies and a latest permissible resolution gate. A material blocker is not carried forward again without an explicit architectural decision | before each new phase |
| **Stage completion** | a stage-completion record (section 10) | D4, D5, each D6 tranche, D7, D8; CM-02's approval; each inventory phase's closure |

## 10. Standards and stage completion

### Standards matrix

| Stage or step | Standard | State | Needed before |
|---|---|---|---|
| Stage 01, controlled vocabulary | Stage 01 standard (T1) | not supplied; ADR-003 stands in | further vocabulary ratification |
| Stage 02, conceptual models | `docs/standards/stage-02-conceptual-modeling.md` | in force | — |
| Source evidence (inventory) | the scope approval of 2026-10-27 and its amendments; the rights review | in force | — |
| Stage 03, taxonomy | Stage 03 standard | not supplied | Stage 03 (T8) |
| Stage 04, thesaurus | Stage 04 standard | not supplied | Stage 04 (T8) |
| Stage 05, ontology | Stage 05 standard, with the validation architecture | not supplied; the specification's gates exist | D6 |
| Stage 06, knowledge graph | Stage 06 standard | not supplied | D7 |
| Release | release standard | not supplied | D8 |

### Stage-completion record

At each major gate, one record states, citing existing artifacts rather than copying them:

- the approved deliverables, with immutable versions or digests;
- the applicable standard;
- the reviewers and their capacities;
- the decisions and dispositions;
- the validation results;
- the outstanding non-blocking issues, each with owner and latest resolution gate;
- the upstream dependencies and source pins;
- the approval authority and the completion decision.

## 11. Open decisions and dependencies

**Blocking** issues stop the gate named; **deferrable** issues have a latest permissible
resolution gate. The owner of every decision is the architect, Aaron Damiano; the drafting
owner is the BCO team.

### Blocking

| Id | Issue | Blocks | Source |
|---|---|---|---|
| O-1 | Final approval of this roadmap | D1, and every step | this document |
| O-2 | Decision authority for licensing and redistribution: confirm the architect, or designate another | new harvests (T5); D8 | direction §5 |
| O-3 | Practitioner reviewer(s) identified and engaged | D3's exit; D4 | AD-2 |
| O-4 | CM-02 scope and integration boundary | D4 | D2, AD-1 |
| O-5 | RP-1 to RP-10 and the other applicable specification decisions ratified; ADR-002 accepted | D4 | spec §10 |
| O-6 | Permanent namespace (RP-5) | D4 | spec RP-5; ADR-003 D1 |
| O-7 | Stage 01 standard | T2's ratifications | T1 |
| O-8 | Stage 05 standard and validation architecture | D5 | AD-3 |
| O-9 | BPO integration: index entries that name capability classes (Q-12); inconsistent shared-class declarations (Q-13); slice act types not vendored (Q-14); raising them with BPO is the architect's call | D5 | CM-01 carry-forward |
| O-10 | First tranche's readiness record, including its reviewed taxonomy baseline | D6, first tranche | AD-3 |
| O-11 | Stage 06 standard | D7 | direction §2 |
| O-12 | Release standard; pinning every dependency by content hash for an executable release (OI-1) | D8 | spec OI-1 |
| O-13 | Consumers of `agents.json` checked before RP-4 lands (OI-10) | D8; RP-4's effect | spec OI-10 |

### Deferrable

| Id | Issue | Latest gate | Source |
|---|---|---|---|
| F-1 | Organization-only bearer departures by source and clause | D3 | CM-01 Q-08 |
| F-2 | Integrated-adequacy assessment of a function with no capability class of its own | D3 | spec OI-15 |
| F-3 | Material-basis representation for an admitted type (section 5) | D6, per tranche | R5; direction §4 |
| F-4 | Formal placement under disposition; reuse of CCO's Organization Capability pattern | D6 | CM-01 Q-09 |
| F-5 | Form of a plural basis (object aggregate or several assertions) | D6 | CM-01 carry-forward |
| F-6 | Relation for develops (CQ-11) | D6 | CM-01 Q-03; spec OI-4 |
| F-7 | Treatment of concerns type and of RL-39; finding value sets, including adequacy findings; maturity-value encoding | D6 | CM-01 carry-forward; R5 |
| F-8 | CCO identifiers taken from reviews, verified against the pins | D6 | spec OI-8 |
| F-9 | Declarations of `enablesProcess` and `requiresCapability` | D6 | spec OI-6 |
| F-10 | The staging state, kept transitional | D6 | spec OI-7 |
| F-11 | The reported existential realization on the governance capability; migration of BPO existential restrictions | D6 | spec OI-9; R5 |
| F-12 | `ex:BusinessAuthorization` under CCO's permission class (BPO-side) | D6, for any tranche touching authorization | spec OI-16 |
| F-13 | Instance evidence; the evidence-graph IRIs | D7 | R5; spec OI-11 |
| F-14 | Schema and versioning of `coverage_register.json` | D7 | spec OI-13 |
| F-15 | A socio-technical system bearer | CM-02's approval | spec OI-14; CM-01 Q-15 |
| F-16 | PCF edition (7.4 or 8.0); PCF 8.0 deferred | T7 | CM-01 Q-11 |
| F-17 | Multi-party sourcing; components that are functions; parthood among capabilities; temporal bearing | D8, as a declared scope limit of the first release if still open | CM-01 Q-04, Q-07, Q-10, Q-06 |
| F-18 | Versioned capability dictionaries (TM-1) | D8 | spec OI-17 |

## 12. Change summary

How the architect's direction of 2026-10-30 maps to this revision.

| Direction | Revision 2 |
|---|---|
| AD-1, Business Capability first | §1; §2 (modules and release boundary); D2 and the note under §2 |
| AD-2, practitioner review before CP-0 | §1; D3 and D4; §6; the practitioner-review gate (§9) |
| AD-3, per-tranche terminology and taxonomy | §1; D5 and D6; §7; T2, T3, T7 and T8 |
| §2, D1–D8 revisions | §4, row by row: D1 approval; D2 scope only; D3 with the practitioner review; D4 with accepted dispositions and namespace; D5 renamed formalization readiness; D6 tranches with G1-T; D7 with its standard; D8 with dependency, licensing and consumer-impact checks |
| §2, Stage 05 not blocked by CM-02; no Agent Capability classes | §2 |
| §3, T1 | T1: preserve approved work; identify gaps; invalidate only for material defects |
| §3, T2 | T2: vocabulary acceptance separate from G1-T. Revision 1's "re-check the five catalog concepts" is folded into T2 |
| §3, T3 | T3 is now terminology reconciliation. Revision 1's T3, vocabulary ratification acts, is folded into T2 under T1 |
| §3, T5 | T5: I-3, I-4 and I-5 each authorized separately |
| §3, T6 | T6: CM-01 criteria; no longer waits for D3 |
| §3, T7 | T7: candidates, not admissions |
| §3, T8 | T8: per-tranche taxonomy baseline; no blanket prerequisite |
| §4, formalization-risk language | §5 item 3, rewritten: no reopening of DP-1 or DP-2; G1-T before the pattern; existing patterns, no new object property; bounded absence queries |
| §5, governance gates | §9 (practitioner review, source adequacy with exceptions, rights authority, conceptual fidelity, closure with blocking and deferrable issues, stage completion); §10 (stage-completion record) |
| §6, preserve decisions | §1, "Decisions this roadmap preserves"; O-9 for the BPO issues |
| §7 deliverables 1–8 | 1 §4; 2 §8; 3 §2; 4 §6 and D3–D4; 5 §7; 6 §10; 7 §11; 8 this section |
| §8, authorization boundary | the status line; nothing here starts CM-02, v0.5, or Stages 03 to 06 |

## 13. What is kept as it is

Decisions recorded verbatim with digests; errata as new records; one reviewed pull request
per phase; communications under `communications/README.md`.
