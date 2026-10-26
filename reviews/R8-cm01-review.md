BCO Stage 02 — CM-01 Review Findings and Required DP-1 Decision

I've completed a review of CM-01 against the BCO Specification v0.4.0-draft.1, the Stage 02 Conceptual Modeling Standard, the recorded architectural choices, and the supplied BFO/CCO and BPO artifacts.

Overall assessment: CM-01 provides a strong conceptual foundation. Its five-pattern organization should be retained. However, several high-priority issues need resolution before approval.

Our immediate priority is DP-1 (RP-1): The Grounding Boundary.

### 1. DP-1 — Architectural Decision Required (Critical)

We need to establish precisely what bears a Business Capability, what materially grounds it, and what merely enables its realization.

The central question is:

Does a Business Capability inhere exclusively in an Organization, with its member agents providing the material basis and technical artifacts serving as enabling conditions? Or can constitutive artifacts form part of the grounding of certain capability types?

CM-01 presents four alternatives:

- Option A: Organization bearer; member-agent material basis; artifacts are enabling conditions.
- Option B: Socio-technical system bearer for every capability.
- Option C: Organization/member-agent grounding by default, with socio-technical grounding permitted for reviewed capability types.
- Option D: Defer material-basis specification until formalization.

Recommendation: Option A, with amendments a1–a4, subject to the architect's explicit decision.

This maintains direct reuse of CCO Organization Capability and preserves the distinction between an organization's disposition and the resources necessary for its realization.

However, adopting Option A requires acknowledging an important consequence: permanently removing an essential platform does not automatically eliminate the organization's capability. Under this model, the capability may persist but become unavailable.

We must explicitly document this commitment rather than assume it is universally true.

If Option A is adopted, implement the following conceptual revisions:

1. Material basis: Clarify that the basis consists of the relevant constituent member agent or agents. Do not classify the organizational arrangement itself as material, and do not require multiple members when a single indispensable member may suffice.
2. Type admission: Assert a material basis only where the capability type has passed the applicable disposition-admission review.
3. Four-way distinction: Explicitly separate material constitution, organizational configuration, enabling conditions, and temporary realization constraints.
4. Future flexibility: Retain OI-14 for cases where evidence suggests that socio-technical grounding is necessary. Record the rationale and consequences of the selected boundary.

Direct ask: Please present DP-1 to the architect for an explicit selection of Option A, B, C, or D, including separate acceptance or rejection of the applicable amendments. My recommendation is Option A with a1–a4, but this is not an approval decision.

The decision record must capture the selected option, rationale, acknowledged limitations, and implications for CM-01.

Do not mark DP-1 resolved or CM-01 approved without that decision.

### 2. Correct the Capability Basis Description (High)

CM-01 describes Capability Basis as an aggregate of member agents while also permitting organizational capabilities dependent on one indispensable member.

These statements require reconciliation.

Revise the conceptual description to accommodate a single constituent member or an appropriate plurality of members without conflating material entities with abstract sets or organizational arrangements.

Ensure that the basis satisfies the intended BFO material-basis semantics when formalized.

### 3. Remove the Unique Most-Specific Capability Type Restriction (High)

CM-01 currently states that each Business Capability instantiates exactly one most-specific Capability Type.

This unnecessarily restricts multiple classification and potential multiple inheritance.

Revise the statement to permit a capability instance to instantiate multiple applicable types. A single primary classification may be maintained as an application convention if required, but it should not be imposed as a universal ontological principle.

### 4. Reconcile Dormant Capabilities with Instance Attribution (High)

The specification permits capabilities that have never been realized.

However, G1-I's current emphasis on actual performance risks excluding those capabilities.

Revise the instance-attribution criteria to distinguish evidence of an organization's genuine capacity from evidence that it has previously exercised that capacity.

Actual performance may support attribution, but it must not be a universal prerequisite.

Coordinate this correction with DP-2 (RP-10). Resolve DP-1 first because its grounding decision determines part of the type-admission and attribution criteria.

### 5. Clarify Functional Adequacy Assessments (High)

CM-01 correctly distinguishes component capability possession from integrated organizational ability.

However, the conceptual target of a functional-adequacy assessment remains insufficiently specified.

Clarify how an assessment evaluates whether an organization can perform a Standing Function adequately, without automatically inferring that ability from possession of the listed component capabilities.

The conceptual model must distinguish:

- Possession of component capabilities.
- Integration and coordination of those capabilities.
- Operational availability.
- Adequacy for performing the intended function.

Do not introduce new ontology classes or object properties merely to resolve this at Stage 02.

### 6. Verify BPO Act-Type Alignment (Integration Priority)

The supplied BPO modules contain both process-oriented classes and classes already categorized as Organization Capabilities.

Before using these classes in realization patterns, verify that each referenced BPO identifier actually denotes the intended kind of act.

Also review repeated shared-class declarations for inconsistent definitions and superclass assignments.

These are integration dependencies that should be documented now and validated before formal OWL implementation.

### Required Deliverables

Please provide:

1. A decision-ready DP-1 recommendation, with the selected option proposed, its amendments, tradeoffs, and effects on the grounding and bearer relationships.
2. A revised CM-01 draft addressing the high-priority conceptual findings, without presuming approval of DP-1 or DP-2.
3. A traceability summary identifying the affected conceptual patterns, relationships, competency questions, and specification sections.
4. An updated decision register identifying what requires architectural approval versus what may be deferred to Stage 05.

### Important Scope Constraint

We are currently in Stage 02 — Conceptual Modeling, not formal ontology implementation.

Do not introduce new OWL axioms, classes, or object properties as part of these corrections. Preserve representation independence and reuse BFO/CCO concepts at the conceptual level.

Once DP-1 and DP-2 have been explicitly decided and the conceptual corrections reviewed, CM-01 can be considered for approval. The subsequent BCO specification revision should incorporate those decisions.

Priority order: Resolve DP-1 → reconcile grounding descriptions → address dormant capability attribution and DP-2 → clarify remaining conceptual boundaries → prepare CM-01 for approval.
