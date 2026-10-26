# R8 Disposition — CM-01 Review Findings and Required DP-1 Decision

Disposition drafted by Claude Code (claude-opus-5-5) at the architect's direction, 2026-10-25. It answers review R8 of CM-01 0.1.0-draft.1 with CM-01 0.1.0-draft.2 on the same pull request. It decides nothing: DP-1 and DP-2 remain the architect's, and every row that touches them is an input to those decisions.

| Field | Value |
| --- | --- |
| Status | Proposed 2026-10-25, awaiting the architect's acceptance |
| Review | `reviews/R8-cm01-review.md`, filed verbatim as received |
| Reviewed artifact | `src/02_conceptual_models/CM-01-business-capability.md` 0.1.0-draft.1 (PR #11, commit `3b18afb`) |
| Answered in | The same file at 0.1.0-draft.2, on the same branch |
| Specification in force | `specifications/Business-Capability-Ontology-v0.4.0-draft.1.md` (draft; nothing in it is normative until ratified) |
| Decisions it rests on | The Stage 02 choices (`docs/decisions/2026-10-25-stage-02-choices.md`); the R6 and R7 response acceptances |
| Effect on status | None. CM-01 stays unapproved; DP-1 and DP-2 stay pending; no vocabulary record, ontology term or shape changes |

R8 keeps CM-01's five-pattern organization and raises one critical item (DP-1), four high-priority conceptual corrections and one integration dependency. This disposition answers it in 12 rows: 9 accepted and done in draft.2, 1 accepted and proposed to DP-2 as amendment b5, and 2 answered by what CM-01 and its checker already do. None is rejected. The DP-1 decision itself is not made here.

## Disposition table

Row IDs are this disposition's own. "Spec" is specification v0.4.0-draft.1; "§" without a document is CM-01 draft.2.

| ID | Finding (R8 ref) | Disposition | Where the answer or change lives |
| --- | --- | --- | --- |
| R8-01 | 1: present DP-1 for an explicit choice of A, B, C or D, with the amendments accepted or rejected separately | Accepted (done here) | §7 DP-1 is made decision-ready: a table of each option's effect on the bearer and grounding relationships (RL-01, RL-04 to RL-07, Enabling Condition, G1-T question 2, CQ-1, CCO reuse); amendments a1–a4 listed for separate acceptance; what changes in CM-01 if A is chosen; what the decision record must capture. The choice is the architect's and is not made |
| R8-02 | 1: A's consequence (an essential platform removed permanently does not by itself end the capability) must be documented as a commitment, not assumed universal | Accepted (done here) | §7 DP-1, "The commitment A makes, stated so it can be accepted or rejected", naming the sources that disagree (SF-06) and a4's route for revisiting it per type |
| R8-03 | 1: do not mark DP-1 resolved or CM-01 approved without the decision | Answered by the model and its checker | §7 DP-1 reads `**Decision:** pending`; §10 Approved reads `no`. `tools/conceptual/check_models.py` refuses an Approved state while any decision point is pending or any open question blocks approval |
| R8-04 | 1 and 2: the basis is the relevant member agent *or agents*; a single indispensable member may suffice; never the arrangement, never an abstract set | Accepted (done here) | §4 Capability Basis rewritten; RL-05 renamed from "is an aggregate of" to "consists of" (one or more members) in §5 and the P1 diagram; P1 reading; §6 "Organizational / one member" row; DP-1 amendment a1 reworded to match. The form of a plural basis is left to Stage 05 (decision register) |
| R8-05 | 3: remove "exactly one most specific Capability Type"; allow multiple classification, with a primary type at most an application convention | Accepted (done here) | P1 reading; §4 Business Capability and Capability Type; RL-02 qualification; §6 "One type / several types" row |
| R8-06 | 4: separate evidence of capacity from evidence of past exercise, so never-exercised capabilities can be attributed; coordinate with DP-2 after DP-1 | Accepted; the model change is done here, and the G1-I change is proposed to DP-2 as amendment b5 | §4 Evidence (capacity against exercise), Capability Assessment and Business Capability; RL-20; §6 "Capacity / exercise" row; CQ-13 note; §7 DP-2 critique and amendment b5 (G1-I questions 2 and 3 reworded), included in the drafter's recommendation. G1-I's text is spec §8, so the wording change reaches the specification only through DP-2 and v0.5 |
| R8-07 | 5: specify the conceptual target of a functional adequacy assessment, distinguishing possession, integration, availability and adequacy, without new classes or properties | Accepted (done here) | §6 "Functional coverage and adequacy", a four-aspect table naming what answers each aspect and what it is never derived from; RL-39 "assesses adequacy for" (Capability Assessment → Standing Function, dashed) in §5 and the P5 diagram; §4 Capability Assessment and Standing Function; RL-18 qualification; CQ-12 note; Q-05 updated. No concept is added, and RL-39 is a conceptual relationship, not an object property; its formal treatment is deferred (specification OI-15). *Qualified by R9 (R9-01):* draft.4 directed a Capability Assessment at a function, which broke that concept's own rules (exactly one Capability Type, exactly one Presence Finding); draft.5 makes the adequacy statement a separate Functional Adequacy Assessment, with RL-39 as its relationship |
| R8-08 | 6: verify that each referenced BPO identifier denotes the intended kind of act | Accepted (measured here) | §9 Q-12. At BPO's pinned commit `66131945`, with the pinned CCO and BFO: 347 of 361 `enablesProcess` entries name act classes; 14 (all slice 12.0) name classes under Organization Capability. BPO's slices declare 145 capability classes. CM-01 itself cites only the six vendored act genera, all of which reach Planned Act. Re-indexing is BPO's work; raising it with BPO is the architect's call (`communications/`) |
| R8-09 | 6: review repeated shared-class declarations for inconsistent definitions and superclasses | Accepted (measured here) | §9 Q-13: 115 classes declared in two or more BPO modules, 52 with differing definitions (including Act of Reporting and Act of Forecasting), 4 with differing named superclasses. §9 Q-14 records that the vendored extract lacks the slices. Documented now; validated before Stage 05 |
| R8-10 | Deliverable 3: a traceability summary | Accepted (done here) | The table below |
| R8-11 | Deliverable 4: a decision register separating what needs architectural approval from what can wait for Stage 05 | Accepted (done here) | §7, "Decision register" |
| R8-12 | Scope: no new OWL axioms, classes or object properties; preserve representation independence | Answered by the change set | No file under `src/05_ontology/`, `shapes/` or the vocabulary changed. Draft.2 adds no concept; its one new relationship (RL-39) is conceptual, like every relationship in §5 (standard §2.4) |

**Tally:** 9 accepted and done here · 1 accepted and proposed to DP-2 (b5) · 2 answered by the model and its checker (12 rows).

## Traceability summary

What each finding touched in CM-01, which competency questions it bears on, and which specification sections v0.5 would revise if the architect accepts it.

| R8 finding | Patterns | Concepts (§4) | Relationships (§5) | Competency questions | Specification sections |
| --- | --- | --- | --- | --- | --- |
| 1 DP-1 | P1, overview | Capability Basis, Organizational Arrangement, Enabling Condition, Type Admission Record | RL-01, RL-04, RL-05, RL-06, RL-07 | CQ-1 (and CQ-7, CQ-12, CQ-13 under B or C) | CD1, CD2, §8 G1-T question 2, CAP-25, OI-14, RP-1 |
| 2 Basis | P1 | Capability Basis | RL-05 | — | CD2, CAP-25, SF-03 |
| 3 Multiple types | P1, P2 | Business Capability, Capability Type | RL-02 | CQ-1, CQ-3, CQ-8, CQ-12 | §4 Business Capability row, CD9 |
| 4 Capacity and exercise | P1, P3 | Business Capability, Capability Assessment, Evidence | RL-20, RL-23 | CQ-13, CQ-4 | CD3, CD8, §8 G1-I questions 2 and 3, CAP-26, RP-10 |
| 5 Functional adequacy | P5, P3 | Capability Assessment, Standing Function, Assessment Criteria | RL-18, RL-37, RL-38, RL-39 (new) | CQ-12 | CD16, CAP-29, OI-15 |
| 6 BPO alignment | P2, P5 | Realization Index, BPO Act Type, Capability Type | RL-10, RL-11 | CQ-2, CQ-3 | CD4, CD12, CAP-03, CAP-05, CAP-13, §2 module layout, OI-1 |

## How the finding 6 figures were measured

From the BPO repository at commit `66131945b525c54f44e4962f32bb1f52dfa0cd12` (the commit the vendored BPO extract is pinned to), read with `git show` so no working tree was involved: every `ontology/**/*.ttl` except the shapes and bad-example files was parsed with rdflib into one graph, together with the pinned CCO and BFO files from `.upstream-cache/` (the bytes `tools/ontology/vendor_upstream.py` fetched and digest-checked). An `enablesProcess` target counts as an act if its `rdfs:subClassOf` closure reaches CCO Planned Act (`cco:ont00000228`), and as a capability if it reaches Organization Capability (`cco:ont00000568`). A first pass without the full CCO undercounted acts, because BPO's genera reach Planned Act only through CCO act classes; the figures above are from the pass with CCO loaded. "Differing definitions" compares, per class, the set of `obo:IAO_0000115` and `skos:definition` values each module gives it. The script was a scratch check and is not committed; the method is stated so it can be repeated.

## Offers

- A message to BPO under `communications/` reporting Q-12 and Q-13 with the figures above. Drafting it is cheap; sending it is the architect's call.
- After DP-1 and DP-2 are decided, a draft.3 of CM-01 that applies the decisions (the dashed relationships become solid or change as decided) and fills the Approved row only once an approval act exists.
