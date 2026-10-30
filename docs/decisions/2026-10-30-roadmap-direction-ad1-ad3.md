# Decision record — roadmap approved in principle; AD-1 to AD-3 decided; revision directed, 2026-10-30

Recorded verbatim by Claude Code (`claude-opus-5-5`) on 2026-10-30, from the direction the
product owner and architect, Aaron Damiano, gave in session. The acts are the architect's.

**What it is about:** `docs/ROADMAP.md`, revision 1, as proposed in pull request #29 at
`594818bdbcc8a321d5e7fe468e8777e34ddb4963` (SHA-256
`1e84ade2034198b197d94827a8d5feab76f59df6d51235112fb0f3b121c3ad6b`).

**The acts it contains:**

1. Revision 1 approved in principle, subject to the revisions directed.
2. AD-1, Business Capability first; Agent Capability follows: approved.
3. AD-2, domain-practitioner review before specification ratification: approved.
4. AD-3, reviewed terminology and taxonomy per formalization tranche: approved.
5. A revised roadmap directed, to be returned for final approval before it governs.

It authorizes preparation of the revised roadmap and nothing else: not CM-02,
specification v0.5, or Stages 03 to 06.

---

````text
# Architect Direction — BCO Roadmap Revision and Approval Conditions

**Subject:** BCO Formal Development Roadmap — Architectural Decisions and Required Revisions

**Decision:** Approved in principle, subject to the revisions below.

I have reviewed the proposed BCO roadmap and accept its overall architecture: a sequential decision and ontology-development path, supported by parallel terminology and source-evidence workstreams.

I am establishing three architectural decisions that must govern the revised roadmap.

## 1. Architectural Decisions

### AD-1 — Business Capability First; Agent Capability Follows

**Decision: APPROVED.**

The first formal ontology release will focus on **Business Capabilities**, using the approved CM-01 Business Capability Conceptual Domain Model as its conceptual baseline.

The broader Agent Capability domain will follow through CM-02.

The roadmap must therefore distinguish:

- **Business Capability module:** Uses approved CM-01 and proceeds through specification ratification, formalization, knowledge graph development, and release.
- **Agent Capability module:** Requires an approved CM-02 conceptual model before its formalization begins.
- **Integrated ontology:** Requires subsequent integration and validation of both modules before claiming comprehensive Business and Agent Capability coverage.

At D2, approve the scope and boundary of CM-02, including its relationship to CCO Agent Capability, Organization Capability, Skill, and the approved organizational grounding model.

**Completing CM-02 is not a prerequisite for beginning Business Capability formalization.**

However, CM-02 must be fully developed, reviewed, and approved under the Stage 02 standard before any Agent Capability extensions are formalized.

The first release must not be represented as covering the entire Agent Capability domain.

### AD-2 — Domain-Practitioner Review Before Specification Ratification

**Decision: APPROVED.**

Move the domain-practitioner review currently planned for D5 to **before D4, the CP-0 specification ratification gate**.

The review must evaluate CM-01's suitability for enterprise capability modeling, particularly:

- Whether Business Capability definitions reflect recognizable organizational abilities.
- Whether the boundaries among capability, process, skill, authorization, and enabling condition are defensible.
- Whether functional coverage and adequacy support actual capability-planning decisions.
- Whether representative sourcing, dormant-capability, and organizational-grounding cases behave as intended.

The review must identify the capacity in which the reviewer acts—for example, business architect or capability-planning practitioner.

The architect's previous approval of CM-01 remains valid. Practitioner review supplements that approval.

Any substantive finding requiring modification to approved CM-01 must follow the existing change-control procedure. Do not silently modify the approved model.

The review's findings and accepted dispositions must be incorporated into specification v0.5 before CP-0 ratification.

CM-02 will require its own practitioner review before its eventual approval.

### AD-3 — Reviewed Terminology and Taxonomy Per Formalization Tranche

**Decision: APPROVED.**

Stage 05 must not begin formalizing a set of classes until the terminology and taxonomy relevant to that implementation tranche have been reviewed.

This is a **per-tranche requirement**, not a requirement to complete the entire enterprise capability taxonomy or thesaurus before formalization begins.

For each proposed formalization tranche, require:

1. A defined list of candidate ontology classes.
2. Reviewed preferred terms and definitions.
3. Identified conceptual distinctions and applicable BFO/CCO candidate parents.
4. Source provenance and relevant supporting evidence.
5. Reviewed taxonomic relationships, where applicable.
6. G1-T admission evidence for each class before it is asserted as an admitted Business Capability disposition.
7. Traceability to CM-01, applicable competency questions, and the ratified specification.

The formalization review must distinguish **source terminology, vocabulary ratification, taxonomy classification, and OWL subclass assertions**.

No lexical match, catalog relationship, source hierarchy, or taxonomy link automatically becomes an OWL axiom.

A complete Stage 04 thesaurus is not a universal prerequisite to beginning Stage 05, although tranche-specific terminology relationships must be resolved where they affect formalization.

## 2. Required Changes to the D1–D8 Decision Path

Retain the existing D1–D8 structure, with the following revisions.

| Step | Required revision |
|---|---|
| **D1 — Roadmap** | Incorporate AD-1 through AD-3, the modular release boundary, and the revised entry and exit gates. |
| **D2 — CM-02 scope** | Establish CM-02's scope and integration boundary. Do not require full CM-02 approval before Business Capability formalization. |
| **D3 — Specification v0.5** | Incorporate approved CM-01 decisions and R8/R9 corrections; conduct domain-practitioner review before submitting the specification for ratification. |
| **D4 — CP-0** | Require accepted practitioner-review dispositions, ratification of all applicable specification decisions, ADR-002, and permanent namespace decisions. |
| **D5 — Formalization readiness** | Approve the Stage 05 standard, validation architecture, and reviewed terminology/taxonomy baseline for the first implementation tranche. |
| **D6 — Stage 05 formalization** | Formalize approved Business Capability tranches, perform class-specific G1-T admission, verify BFO/CCO alignments, and satisfy CP-1/CP-2 and conceptual-fidelity gates. |
| **D7 — Stage 06 knowledge graph** | Require an approved Stage 06 standard before starting; implement G1-I evidence-backed attributions and the applicable instance-level requirements. |
| **D8 — Release** | Establish the release standard, dependency checks, licensing review, consumer-impact assessment, and versioned-release evidence before publication. |

**Important:** Stage 05 work on the Business Capability module must not be blocked merely because CM-02 is unfinished.

Conversely, approval of the Business Capability module provides no authorization to introduce new Agent Capability ontology classes without the required CM-02 review and relevant formalization gates.

## 3. Required Changes to the Terminology Lane

Retain T1–T8 and their parallel relationship to the decision path.

Make the following corrections.

**T1 — Stage 01 standard**

Approve a formal Stage 01 standard before future vocabulary ratifications.

Preserve previously approved artifacts and decisions. Identify any gaps against the new standard without retroactively invalidating completed work unless a material defect is found.

**T2 — Vocabulary review**

Separate controlled-vocabulary acceptance from G1-T admission.

A catalog concept can be accepted as a vocabulary item without establishing that it designates an admitted BFO disposition class.

**T3 — Terminology reconciliation**

Before formalization, reconcile the existing 14 draft vocabulary concepts with the approved CM-01 conceptual model, including Functional Adequacy Assessment.

Document which conceptual categories require vocabulary entries, which reuse existing terms, and which require no new term.

Do not automatically create a vocabulary entry for every conceptual-model concept.

**T5 — Inventory**

Retain separate authorization for I-3, I-4, and I-5. Preserve source provenance, licensing restrictions, and the distinction between candidate terminology and admitted ontology classes.

**T6 — Standing-function classifications**

Use the approved CM-01 conceptual criteria to judge standing-function candidates.

Do not make T6 dependent on selecting final OWL properties. Formal implementation belongs to Stage 05.

**T7 — First catalog tranche**

Treat the approved inventory's recommended first tranche as a source of candidates, not automatic type admissions.

Each admitted formal class must satisfy the applicable G1-T and formalization-review requirements.

**T8 — Taxonomy and thesaurus**

Approve the relevant Stage 03 and Stage 04 standards before beginning those stages.

Provide a reviewed taxonomy baseline for each formalization tranche. Full taxonomy and thesaurus completion is not a blanket prerequisite for Stage 05.

## 4. Correct the Formalization-Risk Language in D3

The three issues currently described under specification v0.5 should be revised as follows.

**Material basis and disposition**

Do not reopen DP-1 or DP-2 merely because a proposed OWL representation entails Disposition.

The relevant question is how to represent an admitted capability type consistently with BFO and the existing decisions.

Require G1-T admission before applying the formal disposition/material-basis pattern to a specific Business Capability type.

**Standing-function designation**

Do not describe conditional designation as a problem of creating an OWL class.

Evaluate the appropriate existing information-entity, annotation, and validation patterns during formalization. Reuse existing BFO/CCO relations wherever possible.

No new object property is authorized by the conceptual relationship alone.

**Capabilities never exercised**

Distinguish the existence or attribution of an unrealized capability from the absence of recorded realizations.

Closed-world evidence rules are appropriate for bounded absence queries, not as a general condition for possessing a BFO disposition.

These are formalization issues unless their investigation reveals a genuine contradiction in approved conceptual meaning.

## 5. Strengthen the Governance Gates

Add the following requirements.

### Practitioner-review gate

Require a recorded practitioner review before specification ratification, including reviewer role, findings, dispositions, and affected artifacts.

### Source-adequacy gate

A source relied upon by a specification or decision must meet the required evidence status or have a documented, specifically approved exception.

Exceptions must identify the affected claims, justification, approving authority, and the stage by which any unresolved issue must be closed.

### Rights and provenance gate

Identify the designated decision authority for licensing and redistribution rather than referring generically to "Legal."

Do not permit new source harvesting or publication beyond the approved rights posture.

### Conceptual-fidelity gate

Every authored ontology class and logical axiom must trace to its governing conceptual model, ratified specification, or separately approved architectural decision.

Where formalization reveals an incompatibility, escalate it through change control rather than silently changing conceptual meaning.

### Closure gate

Distinguish blocking decisions from deferrable issues.

A deferred issue requires a named owner, rationale, affected dependencies, and a latest permissible resolution gate.

A material blocker cannot be repeatedly carried forward without an explicit architectural decision.

### Stage Completion Record

At each major stage gate, record:

- Approved deliverables and immutable versions or digests.
- Applicable standard.
- Reviewers and their capacities.
- Decisions and dispositions.
- Validation results.
- Outstanding nonblocking issues.
- Relevant upstream dependencies and source pins.
- Approval authority and completion decision.

These records may reference existing artifacts rather than duplicate them.

## 6. Preserve Existing Architectural Decisions

The roadmap revision must not reopen or overwrite:

- CM-01's approved conceptual baseline.
- DP-1's organizational grounding decision.
- DP-2's separation of type admission and instance attribution.
- Accepted R8 and R9 dispositions.
- Approved inventory and licensing decisions.
- The BPO namespace migration and its recorded identifier mappings.

Also retain the documented BPO realization-index and shared-class issues as formalization dependencies.

No new ontology classes, object properties, subclass axioms, or vocabulary ratifications are authorized by this roadmap revision.

## 7. Deliverables Requested

Please prepare a revised roadmap for final architectural approval containing:

1. An updated D1–D8 decision path with corrected prerequisites and exit gates.
2. An updated T1–T8 terminology lane showing where reviewed terminology and taxonomy join the formalization path.
3. A clear modular release boundary for Business Capabilities and Agent Capabilities.
4. Domain-practitioner review before CP-0.
5. Per-tranche Stage 05 readiness criteria.
6. A standards and stage-completion governance matrix.
7. A consolidated list of open decisions and dependencies, identifying blocking versus deferrable items.
8. A change summary mapping these instructions to the revised roadmap sections.

Update the proposed roadmap and related planning references, including HANDOFF where appropriate.

Do not change existing ratified decision records or approved conceptual artifacts merely to reflect the new roadmap.

Submit the revised roadmap through the existing pull-request review process.

## 8. Authorization Boundary

**I approve the architectural direction and the three decisions AD-1, AD-2, and AD-3.**

This authorizes preparation of the revised roadmap.

It does **not** authorize starting CM-02, specification v0.5 development, Stage 03, Stage 04, Stage 05, or Stage 06 without their respective approvals and entry gates.

The revised roadmap must be returned for final approval before it becomes the governing development plan.

**The objective is incremental development without compromising conceptual completeness, BFO/CCO alignment, terminology governance, or the integrity of previously approved decisions.**
````
