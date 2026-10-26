Subject: CM-01 draft.4 — Final Review Findings and Approval Conditions
I have completed the review of CM-01 draft.4, SHA-256 `b4e0b713…b452`, and the R8 disposition.
DP-1 and DP-2: Their implementation is accepted as consistent with the recorded architectural decisions. Neither decision needs to be reopened.
R8 disposition: Recommend acceptance with a qualification to R8-07, which requires one final conceptual consistency correction.
CM-01 approval: Recommend deferring approval pending three targeted revisions:

1. RL-39 and Capability Assessment: Reconcile functional-adequacy assessments with the existing requirements that every Capability Assessment concerns exactly one Capability Type and states exactly one Presence Finding. Settle the conceptual category and finding requirements without introducing OWL properties or axioms.
2. Standing Function designation: Clarify whether every Standing Function designates a Capability Type, or whether designation is conditional. Distinguish whole-function types from required component capability types.
3. DP-1 terminology: Qualify "every artifact is enabling" to mean artifacts relevant to a capability's realization. Preserve the architect's accepted platform-loss commitment.

Update the affected conceptual descriptions, relationship qualifications, diagrams, and quality-gate assessments.
The two §10 gates concerning unresolved conceptual ambiguity and sufficient clarity for formalization should be reconfirmed after these corrections.
Do not expand this into a redesign of CM-01. Retain all five existing patterns and the recorded DP-1 and DP-2 decisions.
Please provide the corrected draft and a concise change summary for final approval review.
Separately, record the need for a complementary Agent Capability conceptual model in the ontology development roadmap. This is a broader scope dependency, not a reason to redesign CM-01.
