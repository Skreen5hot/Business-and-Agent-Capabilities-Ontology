# Decision record — D2 complete: the CM-02 scope note, revision 2, approved, 2026-10-31

Recorded verbatim by Claude Code (`claude-opus-5-5`) on 2026-10-31, from the approval the
product owner and architect, Aaron Damiano, gave in session. The act is the architect's.
It is a separate act from the review of revision 1, which decided S-1 (S-1a) and directed
three clarifications (`docs/decisions/2026-10-31-cm02-scope-s1-decided.md`). That record
and revision 1 (`6db7183`) stay as they are.

## What it is about

| Field | Value |
| --- | --- |
| Document | `docs/proposals/2026-10-31-cm02-scope-note.md`, revision 2 |
| Approved at | `a3a417594f4499f05e6a1bb9b97d71cf525d7c58` (pull request #32), with CI passing at that commit |
| SHA-256 of the approved text | `5753fb9f514adecabbe1f18d2a4b11f4519393538a32459c127447c1a627a6e6`, checked against `git show a3a4175:docs/proposals/2026-10-31-cm02-scope-note.md` before this record was written |
| SHA-256 after the administrative revision | `35036ef2d6d0111f851af043c72cd733e83bc9e05774b014734b1d7dbc573a77`. Only the Status row changed, to say the note is approved and cite this record. The conceptual content is unchanged |

## The act

````text
Subject: Architect Approval — D2 CM-02 Scope Note, Revision 2
I have completed my review of PR #32, revision 2, commit `a3a4175`.
Decision: APPROVED.
I approve `docs/proposals/2026-10-31-cm02-scope-note.md`, revision 2, as the formal CM-02 scope and integration-boundary baseline under roadmap step D2.
Findings
I confirm that the three clarifications required by my review of revision 1 have been satisfactorily implemented.
1. Artificial-system agency — Accepted
Option S-1a remains decided. Artificial systems are included in CM-02's investigative scope.
Their inclusion does not establish that they are CCO Agents, bear Agent Capabilities, or have functions equivalent to Agent Capabilities.
The five required distinctions are adequately represented. C-1 must be resolved before the full CM-02 conceptual model is approved.
2. Member-wise capabilities — Accepted
The revision correctly distinguishes capabilities borne by individual members from Organization Capabilities borne by an organization.
Collective attribution must not be treated as organizational capability possession.
3. Enabling conditions — Accepted
The revision preserves DP-1's approved organizational grounding boundary.
Artificial systems remain outside the material basis of Business Capabilities under CM-01's modeling policy. They are enabling conditions only where the realization of the relevant capability actually depends on them.
CCO terminology
I accept the use of the official name Extended Relation Ontology.
The required relation-selection procedure remains: examine the Extended Relation Ontology first, then the applicable CCO domain ontology, and reuse existing relations wherever possible.
Approval scope
This approval:

* Completes the architectural decision required for D2.
* Preserves the existing CM-01 approval and DP-1 and DP-2 decisions.
* Establishes the approved scope against which full CM-02 development will subsequently be reviewed.
* Does not approve the completed CM-02 conceptual model.
* Does not authorize Agent Capability formalization.
* Does not introduce or approve any new ontology class, object property, IRI or OWL axiom.
* Does not itself ratify specification v0.5.

Recording and merge instructions
Please:

1. Record this D2 approval as a new decision act, distinct from the existing revision-1 S-1a decision.
2. Pin the approval to the full commit SHA and SHA-256 digest of the revision-2 scope note.
3. Preserve revision 1 and its previous review record for traceability.
4. Update the proposal's approval status, Stage 02 README, roadmap status, and applicable handoff references.
5. Preserve the approved conceptual content without substantive changes.
6. Merge PR #32 only after required CI checks pass against the final reviewed revision, using the established merge-commit procedure.

If changing document status changes the file digest, retain both the approved revision-2 source digest and the subsequent administrative revision digest.
Final disposition: CM-02 D2 scope note revision 2 APPROVED. D2's architectural approval requirement is satisfied.
````

## What it does

- D2 is complete: the note is the CM-02 scope and integration-boundary baseline, against
  which the full CM-02 will be reviewed. Roadmap open decision O-4 is decided.
- S-1a stands. C-1 must be resolved before the full CM-02 is approved.
- Stage 05 selects relations from CCO's Extended Relation Ontology first, then the
  applicable CCO domain ontology, reusing existing relations wherever possible.

## What it does not do

- It does not approve the full CM-02 or authorize its development beyond what the roadmap
  allows, and does not authorize Agent Capability formalization.
- It introduces or approves no ontology class, object property, IRI or OWL axiom.
- It does not ratify specification v0.5, and does not reopen CM-01, DP-1 or DP-2.
