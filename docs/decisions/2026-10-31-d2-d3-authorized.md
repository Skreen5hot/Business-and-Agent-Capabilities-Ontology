# Decision record — D2 and D3 authorized, 2026-10-31

Recorded verbatim by Claude Code (`claude-opus-5-5`) on 2026-10-31, from the direction the
product owner and architect, Aaron Damiano, gave in session. The acts are the architect's.

**What it is about:** steps D2 and D3 of `docs/ROADMAP.md`, revision 2, as approved and
amended on main at `5b5ac7cfc4a6b5c3ecd7f2892222a7f53dbf0e69` (SHA-256
`5dc3f93deb754b7d004d32045b69d40eaf1553c716f3f7beb9b4baee761c4262`): row D2 and row D3
of section 4, section 5 (what specification v0.5 does) and section 6 (the
domain-practitioner review).

**The acts it contains:**

1. D2, the CM-02 scope and integration-boundary note: authorized, with no change to the
   roadmap's definition, and with five required contents, a length guide, and its review,
   approval and completion criterion.
2. D3, Business Capability specification v0.5 and the domain-practitioner review of CM-01:
   authorized, with no change to roadmap sections 5 or 6, and with its completion
   criterion.
3. O-3 stays open. The BCO team is to nominate at least one qualified practitioner and
   document the reviewer's qualifications and capacity before the review counts under
   AD-2.
4. The authorization boundary and the dependency clarification: D2 and D3 may proceed
   concurrently; both must complete before D4.

The roadmap stays unchanged. This record is the only change the direction makes to the
repository.

**What the three CCO identifiers name:** checked against the vendored extract on
2026-10-31: `cco:ont00001379` is "Agent Capability", `cco:ont00000568` is "Organization
Capability", and `cco:ont00000089` is "Skill", as the direction states.

---

````text
Architect Direction — D2 and D3
Governing baseline: `docs/ROADMAP.md`, revision 2, approved at commit `5b5ac7cfc4a6b5c3ecd7f2892222a7f53dbf0e69`.
D2 — CM-02 scope and integration boundary
Decision: Authorized.
Changes to the roadmap's D2 definition: None.
The BCO team is authorized to develop the CM-02 scope and integration-boundary note under the existing Stage 02 conceptual-modeling standard.
Conditions and required contents
The scope note shall be a concise, independently reviewable document containing:

1. Purpose and scope. Identify what the future Agent Capability module will represent, its intended use, and what is explicitly outside its scope.
2. CCO alignment. Explain the conceptual relationship among CCO Agent Capability (`ont00001379`), Organization Capability (`ont00000568`), and Skill (`ont00000089`). Distinguish capabilities borne by persons from capabilities borne by organizations, including why organizational capability is not automatically reducible to an aggregation of individual skills.
3. Integration with CM-01. Identify how Agent Capability interfaces with the approved Business Capability model, particularly DP-1's organizational grounding decision. The note must preserve the existing distinction between the organizational basis of a capability and the enabling conditions relevant to its realization.
4. Module boundaries and dependencies. Identify shared concepts, intended integration points, exclusions, unresolved conceptual questions, and matters appropriately deferred to the full CM-02.
5. Implications for formalization. Identify potential BFO/CCO alignment questions without prematurely selecting OWL properties, introducing classes, or establishing logical axioms.

The note should be approximately 2–4 pages, excluding references, if that is sufficient to explain the boundary. Clarity and completeness take precedence over length.
Review and approval: The BCO team drafts the scope note. The architect reviews and approves it under D2. This scope approval does not substitute for CM-02's later practitioner review and full conceptual-model approval.
Completion criterion: D2 is complete when the architect approves and records the scope note.
A full CM-02 is not required for Business Capability specification development, formalization, or release. Agent Capability ontology formalization remains dependent on its separately approved conceptual model.
D3 — Specification v0.5 and practitioner review
Decision: Authorized.
Changes to roadmap §5 or §6: None.
The BCO team is authorized to prepare Business Capability specification v0.5 and arrange and conduct the domain-practitioner review of CM-01, under the approved roadmap and applicable standards.
Specification v0.5
The specification shall implement §5 in full, including:

1. Explicit propagation of DP-1, DP-2, accepted R8/R9 dispositions, the CM-01 stakeholder-review erratum, the approved CM-02 scope when available, and accepted practitioner-review findings. Include a traceability table identifying each decision and the specification sections affected.
2. Source citations by register identifier, with evidence status V or P or an individually approved exception under the source-adequacy gate. An unsupported claim must not be represented as validated.
3. Explicit treatment of the three outstanding formalization questions:
   * Material basis and disposition, with G1-T admission preceding application of the formal pattern to a specific capability type.
   * Conditional standing-function designation, evaluated for reuse of existing BFO/CCO and information-entity, annotation, and validation patterns without presuming a new object property.
   * Capabilities never exercised, distinguishing capability existence and attribution from the absence of recorded realizations, with closed-world reasoning restricted to appropriately bounded evidence queries.
4. Correction of the `ex:` prefix to BPO genera only, consistent with the approved re-pin.

These formalization questions must not be used to reopen DP-1 or DP-2. A genuine contradiction with approved conceptual meaning must instead enter change control.
Practitioner review
The review shall address all four questions in roadmap §6:

1. Do the Business Capability definitions represent recognizable organizational abilities?
2. Are the boundaries among capability, process, skill, authorization, and enabling condition ontologically and practically defensible?
3. Do the proposed functional coverage and adequacy constructs support real capability-planning decisions?
4. Do representative sourcing, dormant-capability, and organizational-grounding scenarios behave as intended?

The review must record each practitioner's identity, professional capacity, findings, proposed dispositions, and affected artifacts.
The reviewer evaluates domain applicability and practical meaning. The architect retains authority over BFO/CCO alignment, conceptual changes, and acceptance of dispositions.
Accepted findings must be incorporated into specification v0.5 before CP-0.
Any finding requiring a substantive change to approved CM-01 must be handled through a new, reviewed and approved CM-01 version. Silent modification of the approved conceptual baseline is not authorized.
Practitioner reviewer(s) — O-3
Status: Not yet identified or engaged.
The BCO team shall nominate at least one practitioner with demonstrable enterprise capability-modeling experience, serving in one of the capacities permitted by roadmap §6: business architect, capability-planning practitioner, or FIBF standards-lead-agency analyst.
A practitioner independent of the drafting team is preferred. The team shall document the proposed reviewer's qualifications and capacity before the review is accepted as satisfying AD-2.
O-3 remains open until a qualified reviewer is identified and engaged. D3 may begin, but it cannot complete without the practitioner review and accepted dispositions.
D3 completion criterion
D3 is complete only when the specification review round has been answered, the practitioner review is recorded, the architect has accepted the dispositions, the accepted changes have been carried into v0.5, and the architect accepts v0.5 for ratification.
Acceptance for ratification is not itself specification ratification.
Authorization boundary
This direction authorizes:

* Preparation and approval review of the D2 CM-02 scope note.
* Preparation and review of Business Capability specification v0.5.
* Identification and engagement of qualified practitioner reviewers.
* Execution and documentation of the CM-01 practitioner review.
* Preparation of proposed dispositions and necessary change-control submissions.

This direction does not authorize:

* Ratification of specification v0.5 or completion of CP-0 (D4).
* Reopening DP-1, DP-2, or the approved CM-01 baseline outside formal change control.
* Approval or development of the full CM-02 beyond the authorized scope note.
* Creation or ratification of Agent Capability ontology classes.
* Creation of new object properties, subclass axioms, or other OWL commitments.
* Vocabulary ratification or initiation of Stages 03–06.
* Modification of the approved roadmap outside its documented amendment process.

Dependency clarification: D2 and D3 may proceed concurrently. D2's approved scope must be incorporated into v0.5 when available and must be approved before D4. D3 cannot exit until O-3 is satisfied. Both D2 and D3 must complete before D4 can begin.
The roadmap remains unchanged. All decisions and accepted dispositions shall be recorded, versioned, and propagated into their affected artifacts under the existing governance process.
Final direction: Authorize D2 and D3 as defined above. Preserve the approved conceptual baseline, maintain the existing authorization boundaries, and return the completed artifacts for the required architectural approvals.
````
