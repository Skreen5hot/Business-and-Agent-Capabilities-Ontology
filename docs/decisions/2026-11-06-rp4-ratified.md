# Decision record — RP-4 ratified, 2026-11-06

Recorded verbatim by Claude Code (`claude-opus-5-5`) on 2026-11-06, from the decision the
architect, Aaron Damiano, gave in session. The act is the architect's.

## What it is about

| Field | Value |
| --- | --- |
| Item | RP-4, the agent manifest (CD13), in `specifications/Business-Capability-Ontology-v0.5.0-draft.3.md` at `c3f1ba2`, SHA-256 `2224f869b0ec7a1e31b0afc1c2b403ad222ea290c334bff48a93ebbb6516c574` (accepted for ratification 2026-11-04) |
| Evidence decided on | `docs/proposals/2026-11-06-rp4-faithfulness-check.md` at `e1da561`, SHA-256 `715fc7aafdc7dd9ec80a5ac1424859c5774bbdcedf080e1f0c3e1174b9197e45` |
| BPO investigated at | the pin `bc64e91839378e1926189c01bf184d6a22d5c1b7`, and main `14a1e2cd3769cd79c4be9cdfc6fe113167de3f57` |
| CP-0 item | 8 of `docs/proposals/2026-11-05-cp0-closure-matrix.md`, decision 3; and OI-10 for CP-0 |

## The decision

````text
Subject: Architect Decision — RP-4 Agent Manifest Ratification
Decision: RP-4 APPROVED FOR RATIFICATION.
I approve CD13 of specification v0.5.0-draft.3 as the binding BCO treatment of BPO's Agent Manifest.
1. Agent Manifest semantics
The manifest is descriptive routing information associating software-agent identifiers with capability types they serve.
It is not evidence that:

* A software agent bears an Organization Capability.
* A software agent bears any other Agent Capability.
* An organization bears a capability merely because its software agent is listed.
* A BPO capability class has passed BCO's G1-T type-admission gate.

Software considered as information content is not itself a material bearer of a BFO realizable entity.
Whether deployed artificial systems qualify as agents or bear Agent Capabilities remains a CM-02 question.
2. Organizational grounding boundary
The deployed computing artifact remains outside the material basis of Business Capabilities under approved DP-1.
It is an enabling condition only for capabilities whose realization actually depends on it.
No manifest entry establishes organizational capability bearing, material basis or realization.
3. Multiple capability associations
The existing BPO JSON may associate one software-agent identifier with multiple capability types.
This does not contradict CM-01's rule that an individual conceptual Agent Manifest record concerns exactly one capability type.
If the manifest is subsequently represented in OWL, model each type-specific record separately under the approved information-layer pattern.
No immediate migration or retyping of the BPO file is required.
4. OI-10 and upstream compatibility
Accept the documented consumer investigation for CP-0.
Close OI-10 for its CP-0 evidence requirement, recording that the identified BPO consumer is `scripts/matchability.py` and that no BCO consumer was found in the investigated repositories.
Retain the existing D8 release consumer-impact check for external or subsequently discovered consumers.
Do not modify BPO's `agents.json`, routing script or ontology files as a condition of this decision.
Any BPO semantic cleanup is a separate upstream matter and is not authorized or required here.
5. Recording and scope
Record RP-4 as ratified against the exact reviewed specification revision and the RP-4 evidence document.
Close the corresponding CP-0 ratification item.
No new ontology class, object property, namespace or OWL axiom is authorized.
CM-01, DP-1, DP-2 and the approved CM-02 scope remain unchanged.
Final disposition: RP-4 ratified. No further RP-4 review is required. Proceed with the remaining CP-0 decisions and bulk capability development.
````

## The acts it contains

1. **RP-4 is ratified.** CD13 of draft.3 is the binding BCO treatment of BPO's agent
   manifest.
2. **What the manifest means.** It is descriptive routing information: software-agent
   identifiers with the capability types they serve. It is no evidence of four things:
   - that a software agent bears an Organization Capability;
   - that it bears any other Agent Capability;
   - that an organization bears a capability because its agent is listed;
   - that a BPO capability class has passed G1-T.

   Software as information content bears no BFO realizable. Whether deployed artificial
   systems are agents, or bear Agent Capabilities, stays CM-02's question.
3. **Grounding boundary.** Under DP-1, the deployed computing artifact is outside the
   material basis of every Business Capability. It is an enabling condition only where
   realization depends on it. No manifest entry establishes bearing, basis or realization.
4. **Several types per agent.** An `agents.json` entry may list several capability types.
   That does not contradict CM-01's one-type-per-record rule. In OWL, each type-specific
   record is modeled separately. BPO's file needs no migration or retyping now.
5. **OI-10 is closed for CP-0.** The BPO consumer identified is `scripts/matchability.py`,
   and no BCO consumer was found in the repositories investigated. The D8 release
   consumer-impact check is kept, for consumers outside them or found later.
6. **BPO is not changed.** No change to `agents.json`, the routing script or the ontology
   files is a condition, and BPO semantic clean-up is neither authorized nor required.
7. **CP-0 item 8 (decision 3) is closed.**
8. **Scope.** No class, object property, namespace or OWL axiom is authorized. CM-01, DP-1,
   DP-2 and CM-02's approved scope are unchanged, and no further RP-4 review is required.

## How it was carried out

- **This record.** The specification is not edited. Its §10 register and OI-10 wait for the
  next reviewed version.
- **Status lines.** These are updated:
  - `CLAUDE.md`, `docs/DEVELOPMENT.md` and `docs/HANDOFF.md`;
  - the roadmap's D4 row, its state row, its O-13 row and its amendment log;
  - the status lines of the evidence note and of the CP-0 closure matrix.

  Each proposal's body is unchanged.

## What it does not do

- It ratifies no other register item. RP-6 to RP-9 stay drafts, and RP-5 is open.
- It sends no message to BPO and changes nothing upstream.
- It mints and asserts nothing, and makes no G1-I claim. CP-0 stays open, and OWL still
  waits for all of CP-0 and D5.
