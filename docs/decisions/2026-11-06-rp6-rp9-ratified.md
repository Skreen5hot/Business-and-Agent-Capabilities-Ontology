# Decision record — RP-6 to RP-9 ratified, 2026-11-06

Recorded verbatim by Claude Code (`claude-opus-5-5`) on 2026-11-06, from the decision the
architect, Aaron Damiano, gave in session. The act is the architect's.

## What it is about

| Field | Value |
| --- | --- |
| Items | RP-6 (CD14), RP-7 (CD15), RP-8 (CD16) and RP-9 (CD17), in `specifications/Business-Capability-Ontology-v0.5.0-draft.3.md` at `c3f1ba2`, SHA-256 `2224f869b0ec7a1e31b0afc1c2b403ad222ea290c334bff48a93ebbb6516c574` (accepted for ratification 2026-11-04) |
| Evidence decided on | `docs/proposals/2026-11-06-rp6-rp9-faithfulness-check.md` at `d525f32`, SHA-256 `11fa50fe536f4dde851afc305889866b5a952c66ef88e95ec47911a937016912` |
| CP-0 items | 10 to 13 of `docs/proposals/2026-11-05-cp0-closure-matrix.md`, decision 4 |

## The decision

````text
Subject: Architect Decision — Collective Ratification of RP-6 through RP-9
Decision: RP-6, RP-7, RP-8 and RP-9 RATIFIED.
I approve design commitments CD14, CD15, CD16 and CD17 as carried in Business Capability Ontology specification v0.5.0-draft.3.
This is one collective ratification decision. No further individual RP-6 through RP-9 approval proposals are required.
RP-6 — Type References and Findings
Ratified.
Every completed Capability Assessment must concern exactly one capability type, state exactly one Presence Finding, identify its criteria, cite supporting evidence, and record its as-of date.
An incomplete evaluation is not a completed Capability Assessment.
Insufficient evidence must never be converted into an `absent` finding.
Capability Maps contain assessments and targets. Map entries and hierarchy do not automatically establish possession, specialization or capability parthood.
Where CM-01's Assessment Criteria description is narrower than its Capability Assessment definition, the specification follows the approved assessment meaning. Record the wording inconsistency for CM-01's next reviewed revision; do not reopen CM-01 now.
Keep OI-23, OI-24 and OI-25 open for Stage 05.
RP-7 — Closed-World Authorization Evidence
Ratified.
Adopt CD15, including its applicability table governing act type, agent, validity period, overlapping records, multiple authorities, revocation and supersession, and manifest scope.
Authorization Records describe prospective authorization without asserting that a permitted act occurred.
Evidence-register absence queries must return either:

* No applicable authorization recorded within the declared complete scope; or
* Unknown when the required completeness scope is unavailable.

They must never infer that an agent is legally unauthorized merely because a record was not found.
An applicable record establishes recorded authorization information, not a legal conclusion about the authority or validity of that authorization.
Retain OI-21 concerning revocation and supersession, and OI-11 concerning evidence-register identifiers and manifests. Registers affected by unresolved revocation or supersession must not be declared complete.
RP-8 — Functional Coverage and Adequacy
Ratified.
Retain the four distinct questions:

1. Possession of component capabilities.
2. Integration and coordination.
3. Operational availability.
4. Adequacy for the standing function.

No finding concerning integration, availability or adequacy follows automatically from component possession.
A Standing Function designates a whole-function Capability Type only where one has been defined and independently admitted.
No subclass axiom, capability-possession assertion or adequacy judgment is generated from a coverage-register entry.
CM-01 Q-07 remains open as previously recorded.
CAP-29's prohibition on automatically generated adequacy findings must be validated through generator and provenance tests.
RP-9 — Information-Layer Scope
Ratified.
Retain the seven proposed description-layer classes and the distinct conceptual category of Functional Adequacy Assessment.
A Functional Adequacy Assessment is not a Capability Assessment and must not be treated as a map entry.
Its three findings— integration, availability and adequacy—must be independently supported by required criteria and evidence.
Whether Functional Adequacy Assessment requires an eighth description-layer class or can be represented using existing ontology constructs remains a Stage 05 decision.
Before minting any additional class, evaluate existing BFO/CCO constructs. For formal relations, consult the Extended Relation Ontology first, then the applicable domain ontology.
Recording and Next Steps
Record this as one architectural decision against the exact specification draft.3 revision.
Close RP-6, RP-7, RP-8 and RP-9 in the CP-0 register.
Do not reopen CM-01, DP-1, DP-2 or the earlier R8–R11 dispositions.
Do not create additional object properties or OWL axioms through this ratification.
Keep the outstanding Stage 05 representation issues visible, but do not let them generate another CP-0 review cycle.
Following this decision, proceed directly to RP-5, ADR-002 and the Stage Completion Record, subject to the remaining recorded CP-0 requirements.
Prioritize completion of CP-0 and the source-supported bulk capability development already directed.
Final disposition: RP-6 through RP-9 ratified together.
````

## The acts it contains

1. **RP-6, RP-7, RP-8 and RP-9 are ratified together**, as one decision: CD14 to CD17 as
   carried in draft.3. No separate proposals are required.
2. **RP-6, assessments.** A completed Capability Assessment:
   - concerns one type and states one Presence Finding;
   - identifies its criteria, cites its evidence and records its as-of date.

   An incomplete evaluation is not one, and insufficient evidence never becomes `absent`.
   Map entries and hierarchy establish no possession, specialization or parthood. Where
   CM-01's Assessment Criteria entry is narrower than its Capability Assessment
   definition, the specification follows the definition. The inconsistency is recorded
   for CM-01's next reviewed revision, and CM-01 is not reopened. OI-23, OI-24 and OI-25
   stay open for Stage 05.
3. **RP-7, authorization evidence.** CD15 is adopted with its applicability table. An
   Authorization Record describes a prospective authorization, and asserts no permitted
   act. An absence query returns one of two answers:
   - "no applicable authorization recorded within the declared complete scope";
   - *unknown*.

   It never concludes that an agent is legally unauthorized. An applicable record is
   recorded information, not a legal conclusion about the authorization. OI-21 and OI-11
   stay open, and a register affected by unresolved revocation or supersession is not
   declared complete.
4. **RP-8, coverage and adequacy.** The four questions stay distinct. Integration,
   availability and adequacy never follow from component possession. A Standing Function
   designates a whole-function type only where one is defined **and independently
   admitted**. A coverage-register entry generates no subclass axiom, possession
   assertion or adequacy judgment. Q-07 stays open. CAP-29 is validated by generator and
   provenance tests.
5. **RP-9, the information layer.** Seven description-layer classes, and the Functional
   Adequacy Assessment as a distinct category. It is not a Capability Assessment and not a
   map entry, and each of its three findings is supported on its own criteria and evidence.
   Whether it needs an eighth class is a Stage 05 decision. Before any class is minted,
   existing BFO and CCO constructs are evaluated; for relations, the Extended Relation
   Ontology is consulted first, then the applicable domain ontology.
6. **CP-0 items 10 to 13 (decision 4) are closed.**
7. **Scope.** CM-01, DP-1, DP-2 and the R8 to R11 dispositions are not reopened. No object
   property or OWL axiom is created. The Stage 05 representation issues stay visible, and
   they generate no further CP-0 review cycle.
8. **Next.** RP-5, ADR-002 and the stage-completion record, then the source-supported
   bulk capability development already directed.

## How it was carried out

- **This record.** The specification is not edited. Its §10 register and the open issues
  wait for the next reviewed version.
- **The CM-01 wording inconsistency** is listed in `src/02_conceptual_models/README.md`,
  under candidates for CM-01's next reviewed version. That list also carries the two
  candidates already recorded:
  - R11 P-10's example (`docs/decisions/2026-11-03-r11-disposition-accepted.md`);
  - the `ex:` to `bpo:` prefix change (`docs/decisions/2026-10-28-i2-and-bpo-repin-decided.md`, R3).

  CM-01's text is not changed.
- **Status lines.** These are updated:
  - `CLAUDE.md`, `docs/DEVELOPMENT.md` and `docs/HANDOFF.md`;
  - the roadmap's D4 row, its state row and its amendment log;
  - the status lines of the check and of the CP-0 closure matrix.

  Each proposal's body is unchanged.

## What it does not do

- It does not decide RP-5, ADR-002 or the stage-completion record. CP-0 stays open, and
  OWL still waits for all of CP-0 and D5.
- It mints and asserts nothing, and makes no G1-I claim. It decides none of the open issues
  it names.
