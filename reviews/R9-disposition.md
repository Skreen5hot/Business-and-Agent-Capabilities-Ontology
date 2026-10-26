# R9 Disposition — CM-01 draft.4: Final Review Findings and Approval Conditions

Disposition drafted by Claude Code (claude-opus-5-5) at the architect's direction, 2026-10-26. It answers review R9 of CM-01 0.1.0-draft.4 with 0.1.0-draft.5 on the same pull request. It decides nothing: approving CM-01, and accepting this disposition and R8's, are the architect's.

| Field | Value |
| --- | --- |
| Status | Accepted in full 2026-10-26 by the architect, Aaron Damiano — `docs/decisions/2026-10-26-cm01-approved-r8-r9-accepted.md` (act 3) |
| Review | `reviews/R9-cm01-draft4-review.md`, filed verbatim as received |
| Reviewed artifact | `src/02_conceptual_models/CM-01-business-capability.md` 0.1.0-draft.4 (commit `8428d0c`, SHA-256 `b4e0b713…b452`), and `reviews/R8-disposition.md` |
| Answered in | The same file at 0.1.0-draft.5, on the same branch |
| Decisions it rests on | DP-1 (`docs/decisions/2026-10-25-dp1-rp1-grounding-boundary.md`) and DP-2 (`docs/decisions/2026-10-26-dp2-rp10-admission-attribution.md`); neither is reopened |
| Effect on status | None. CM-01 stays unapproved; the R8 disposition stays proposed |

R9 accepts the implementation of DP-1 and DP-2, recommends accepting the R8 disposition with one qualification, and asks for three targeted corrections before approval, plus a roadmap entry. This disposition answers it in 8 rows, all accepted and done here, none rejected, with no redesign: the five patterns and both decisions are unchanged.

## Change summary for final approval review

1. **Functional adequacy is its own kind of statement.** Draft.4 directed a Capability Assessment at a Standing Function. That broke the concept's own rules: a Capability Assessment concerns exactly one Capability Type and states exactly one Presence Finding. Draft.5 adds one conceptual concept, **Functional Adequacy Assessment**, a sibling of Capability Assessment rather than a kind of it.
   - It describes one Organization and assesses adequacy for one Standing Function (RL-39).
   - It states exactly three findings: integration and coordination, operational availability, and adequacy for the function. Each finding is met, partly met or not met against required criteria.
   - None of its findings is derived from component possession.
   - Capability Assessment's rules now hold without exception.
   - No OWL property, class or axiom is introduced. How the new statement is represented is left to Stage 05 and spec v0.5 (RP-9: the specification's seven description classes).
2. **Standing Function designation is conditional.** A Standing Function designates at most one *whole-function* Capability Type, and only where one has been defined. Otherwise it is represented only by its Coverage Register Entry.
   - The whole-function type is distinct from the *component* types the entry requires, and is never one of its own components.
   - Bearing every component does not entail bearing the whole-function type. Neither settles adequacy.
   - P5 now draws three Capability Type positions: whole-function, component, and broader type. The designation arrow is dashed in P5 and in the overview.
3. **"Every artifact is enabling" is scoped.** It now reads: every artifact *relevant to a capability's realization* is an enabling condition of it. An artifact that plays no part in its realizations is neither its basis nor one of its enabling conditions.
   - The platform-loss commitment and the DP-1 decision are unchanged, and the text says so.
   - DP-1's recorded options table keeps its original wording, as the record of what was decided between.
4. **Quality gates reconfirmed.** In §10, "no unresolved conceptual question" and "sufficient clarity for formalization" are reconfirmed after the corrections, as the drafter's assessment for the architect to confirm.

Counts: 33 concepts (one added), 39 relationships (none added; RL-39's source changed), 6 diagrams, 14 competency questions traced, 0 decision points pending.

## Disposition table

Row IDs are this disposition's own. "§" without a document is CM-01 draft.5.

| ID | Finding (R9 ref) | Disposition | Where the change lives |
| --- | --- | --- | --- |
| R9-01 | R8 disposition: accept, with a qualification to R8-07 | Accepted (done here) | `reviews/R8-disposition.md` row R8-07 now carries the qualification and points here. Accepting the R8 disposition remains the architect's act |
| R9-02 | 1: reconcile functional-adequacy assessments with Capability Assessment's one-type, one-finding rules; settle the category and finding requirements with no OWL | Accepted (done here) | §4 new concept Functional Adequacy Assessment; §4 Capability Assessment (rules stated as holding without exception, adequacy removed); RL-39 source changed; RL-16 and RL-21 sources extended; RL-18 qualification; P5 diagram and reading; §6 adequacy table and paragraph; CQ-12 note; Q-05 |
| R9-03 | 2: is designation by a Standing Function universal or conditional; distinguish whole-function from component types | Accepted (done here): conditional | §4 Standing Function and Capability Type; RL-35 qualification; P5 diagram (three type positions, dashed designation) and reading; overview diagram (dashed) and reading; §6 new boundary row; CQ-9 note |
| R9-04 | 3: qualify "every artifact is enabling" to artifacts relevant to the capability's realization; keep the platform-loss commitment | Accepted (done here) | §4 Enabling Condition; RL-07; §6 grounding paragraph (with a sentence that the qualification changes neither decision nor commitment); §6 homonym note. DP-1's options table is left as recorded |
| R9-05 | Update descriptions, qualifications, diagrams and quality gates | Accepted (done here) | As in R9-02 to R9-04; §7 decision register gains a row for the draft.5 corrections and names CD16, CD17, RP-8 and RP-9 for v0.5; §10 counts and stakeholder-review row |
| R9-06 | Reconfirm the two §10 gates after the corrections | Accepted (done here) | §10 quality gates, both marked reconfirmed in draft.5 for the architect to confirm |
| R9-07 | No redesign; keep the five patterns and the DP-1 and DP-2 decisions | Answered by the change set | Patterns P1–P5 unchanged in scope; only P5 and the overview diagrams change; no decision record edited; one concept added and no relationship added |
| R9-08 | Record a complementary Agent Capability conceptual model in the ontology development roadmap, as a scope dependency | Accepted (done here) | The repository has no separate roadmap file; its plan of record is each stage README plus `docs/HANDOFF.md`. Recorded as CM-02 (working title), planned and not started, in `src/02_conceptual_models/README.md` "Planned models", with what it would cover (CD1 Skill and Agent Capability, CD10 member-wise abilities, CD13 computing-artifact functions) and why CM-01 depends on it; and in HANDOFF. Starting it and setting its scope are the architect's |

**Tally:** 7 accepted and done here · 1 answered by the change set (8 rows).

## Traceability summary

| R9 item | Patterns | Concepts (§4) | Relationships (§5) | Competency questions | Specification sections |
| --- | --- | --- | --- | --- | --- |
| 1 Adequacy statement | P5, P3 | Functional Adequacy Assessment (new), Capability Assessment, Standing Function, Assessment Criteria | RL-16, RL-18, RL-21, RL-39 | CQ-12 | CD14, CD16, CD17, CAP-17, CAP-27, CAP-29, OI-15, RP-9 |
| 2 Designation | P5, overview | Standing Function, Capability Type, Coverage Register Entry | RL-35, RL-37, RL-38 | CQ-9, CQ-12 | CD16, ADR-001 R4–R6, OI-13, RP-8 |
| 3 Artifact scope | P1 | Enabling Condition | RL-07 | — | CD2, RP-1 (as decided) |

## Offers

- A dedicated roadmap file (for example `docs/ROADMAP.md`) collecting the stage plan, CM-02 and specification v0.5, if the architect prefers one place to the stage READMEs.
