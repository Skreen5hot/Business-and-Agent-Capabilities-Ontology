Architectural Review R10 — BCO Specification v0.5.0-draft.1
Reviewed artifact: `specifications/Business-Capability-Ontology-v0.5.0-draft.1.md`
Reference: PR #33
Disposition: REVISION REQUIRED BEFORE ACCEPTANCE FOR RATIFICATION
I have reviewed specification v0.5.0-draft.1 against the approved CM-01 conceptual model, DP-1, DP-2, the accepted R8 and R9 dispositions, the D2 scope decision, and the governing D3 roadmap requirements.
The specification substantially satisfies the four D3 drafting requirements. Its overall architecture is retained.
I accept the direction of the new CAP-32, CAP-33 and CAP-34 requirements, but further corrections are required before the R5 disposition can be accepted and the specification advanced as the candidate for CP-0 ratification.
R10-01 — Positive grounding evidence
Disposition: Revision required.
CAP-25 correctly constrains asserted material-basis relations but does not clearly require positive grounding evidence for every asserted Business Capability instance.
Resolve this gap by defining an enforceable grounding-evidence requirement consistent with DP-1 and G1-I.
Add a negative fixture for an asserted capability instance lacking the required grounding witness.
Do not weaken the approved single-member grounding case or introduce artifact parts into the organizational material basis.
R10-02 — Organizational performance witness
Disposition: Revision required.
CAP-34 currently requires organizational-member participation.
Participation alone may be insufficient to establish that the organization, through its members, performed the act that realizes its capability.
Align CAP-34 with CM-01 RL-14, distinguishing performance by organizational members from incidental participation in externally performed work.
Add a negative vendor-performance fixture in which a customer employee participates without performing the relevant work.
The formal relation remains a Stage 05 decision under the approved BFO/CCO reuse procedure.
No new object property is authorized.
R10-03 — Assessment evidence and criteria
Disposition: Revision required.
Align CD14, CAP-27, CAP-33 and the instance examples with CM-01's definition of Capability Assessment.
Every completed Capability Assessment must have a single finding supported by identifiable criteria and evidence.
Distinguish incomplete or unsupported evaluations from completed assessments, and never convert inadequate evidence into an `absent` or `not met` finding.
Review the illustrative Capability Map entries accordingly.
R10-04 — Parent-class admission
Disposition: Clarification requested.
State how the generic Business Capability parent satisfies the applicable architectural approval or G1-T requirement.
Individual specific capability types must continue to require their own G1-T admission.
Matters accepted without further redesign
I accept the following as appropriate for the current draft:

* Incorporation of DP-1 and DP-2.
* Functional Adequacy Assessment as a distinct conceptual category.
* Conditional Standing Function designation.
* Whole-function versus component capability distinctions.
* Separation of BPO and BCO namespaces.
* Separation of Business Capability and Agent Capability module scope.
* The revised treatment of source evidence and recorded departures.
* The formalization questions and relation-reuse order in §3.1.
* Deferral of the actual representation of ordinal measurement values and Functional Adequacy Assessment findings to Stage 05.

Decisions not yet taken
The R5 disposition remains proposed.
SE-1 and SE-2 remain subject to primary-source verification, removal of unsupported claims, or separately justified exceptions.
The authorization-applicability rules of CD15 remain proposals for RP-7.
Domain-practitioner review must be completed and its accepted findings incorporated before CP-0.
No specification ratification is granted by this review.
Required next action
Please:

1. File this review under the established review process.
2. Prepare v0.5.0-draft.2 addressing R10-01 through R10-04.
3. Provide a disposition table mapping each finding to the exact revised sections, validation requirements and fixtures.
4. Retain the previous draft and its digest as review provenance.
5. Keep the specification under review; do not promote it to the normative specification role or alter existing ratification records.
6. Return draft.2 for architectural review.

The architecture is accepted as the working design. Acceptance for ratification and CP-0 remain pending.
