# Decision record — CM-02 scope: S-1a decided; clarifications directed before approval, 2026-10-31

Recorded verbatim by Claude Code (`claude-opus-5-5`) on 2026-10-31, from the review the
product owner and architect, Aaron Damiano, gave in session. The acts are the architect's.

**What it is about:** the CM-02 scope and integration-boundary note,
`docs/proposals/2026-10-31-cm02-scope-note.md`, revision 1, as proposed in pull request
#32 at `6db7183271076a58b16f947288e96d395970c3d2` (SHA-256
`874e10df79729e05714b0647d9aef9b98c54d93f817cae99f5b2e75f353f0a27`), with CI passing at
that commit.

**The acts it contains:**

1. S-1 decided: Option S-1a. Artificial systems are included in CM-02's scope as subject
   matter. It is a scope decision only: it does not establish that an artificial system is
   an Agent, bears an Agent Capability, or has functions identical to Agent Capabilities.
2. Three clarifications directed (artificial-system agency, member-wise capabilities,
   organizational enabling conditions), with the distinctions CM-02 must preserve and the
   governance points stated.
3. Approval of the note as the D2 baseline recommended, subject to the clarifications. The
   note is **not yet approved**: the updated proposal is returned for recording, and D2
   completes only when the architect approves and records it.

It authorizes no full CM-02 modeling, specification ratification or Agent Capability
formalization, and no ontology class, object property, namespace or OWL axiom.

---

````text
Architect Review Recommendation — D2 CM-02 Scope Note
Reference: PR #32 — CM-02 Scope and Integration Boundary
Recommended disposition: Approve with targeted clarifications.
Decision S-1 — Artificial Systems
Select Option S-1a: INCLUDE ARTIFICIAL SYSTEMS.
Artificial systems are included as subject matter for the CM-02 Agent Capability Conceptual Domain Model.
This is a scope decision only. It does not establish that an artificial system is an Agent, that it bears an Agent Capability, or that its functions are identical to Agent Capabilities.
CM-02 must investigate these distinctions using existing BFO and CCO classifications.
The conceptual analysis should distinguish:

1. Software agents considered as information or software specifications.
2. Deployed material computing systems executing software.
3. Agent Capabilities realized through Planned Acts.
4. Artifact Functions borne by designed material artifacts.
5. Activities performed autonomously, under human direction, or as part of organizational processes.

The distinction between an artifact's Function and an Agent Capability must be evaluated without assuming those categories are either equivalent or necessarily disjoint.
D2 Scope Note — Recommended Approval
I recommend approving the proposed CM-02 scope note as the D2 scope and integration-boundary baseline, subject to these clarifications:
1. Artificial-system agency
Clarify that apparent autonomous behavior alone does not establish CCO Agent classification. The complete CM-02 must determine the necessary conditions for Agent Capability attribution and evaluate whether candidate artificial systems satisfy them.
2. Member-wise capabilities
Clarify that member-wise group capability means the relevant capabilities belong to individual members. Such collective attribution must not be confused with an Organization Capability inhering in the organization.
3. Organizational enabling conditions
Preserve CM-01's approved DP-1 grounding boundary. An artificial system remains outside the material basis of a Business Capability under the adopted organizational modeling policy. It is an enabling condition only for capabilities whose realization actually depends on it.
CM-01 Integration
The CM-02 scope decision does not reopen DP-1, DP-2, or CM-01's approval.
CM-02 must preserve the distinction between:

* Individual capabilities and organizational capabilities.
* Organizational material basis and member-borne Skills.
* Artifact Functions and genuine Agent Capabilities.
* Organizational capability possession and collective member-wise capability attribution.
* Software-agent routing descriptions and actual capability-bearing entities.

Governance
The full CM-02 must resolve its material conceptual questions, especially C-1, before its own Stage 02 approval.
No new ontology class, object property, namespace, or OWL axiom is authorized by the scope decision.
Before selecting formal relationships, the subsequent ontology-development stage must check the Extended Relations Ontology first, followed by the relevant CCO domain ontology, and reuse existing constructs wherever applicable.
Please make the three clarifications in the scope note, preserve the approved CM-01 baseline, and return the updated proposal for recording under the established governance procedure.
Approval of D2 does not authorize full CM-02 modeling, specification ratification, or Agent Capability formalization. Those activities remain subject to their respective roadmap gates.
````
