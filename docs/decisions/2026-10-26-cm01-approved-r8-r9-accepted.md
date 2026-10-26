# Decision record — CM-01 approved as the Stage 02 conceptual baseline; R8 and R9 dispositions accepted, 2026-10-26

Recorded verbatim by Claude Code (`claude-opus-5-5`) on 2026-10-26, at the statement the
product owner and architect, Aaron Damiano, made in session. The acts are his. The
statement contains three acts, recorded here together because they were made together;
each is identified below so that each status it changes can cite it.

---

````text
Subject: Architect Decision — CM-01 draft.5 Approval and R8/R9 Dispositions
I have completed my review of CM-01 version 0.1.0-draft.5 and the R8 and R9 dispositions.
The following decisions are approved for recording.
Decision 1 — CM-01 draft.5
APPROVED as the Stage 02 Business Capability Conceptual Domain Model.
Approved artifact SHA-256:
`a59e3cd4149693ce388deaa7c8953242a8c3355e4c7eef96d094c8e90a75b5a0`
I confirm that the model satisfies the Stage 02 conceptual modeling quality gates sufficiently to proceed with subsequent ontology development.
The five conceptual patterns are retained. DP-1 and DP-2 remain as previously decided.
Decision 2 — R8 Disposition
ACCEPTED, with R8-07 qualified by the corrections adopted in R9.
The disposition's historical record should remain intact. The acceptance record should reference the subsequent DP-1 and DP-2 decisions and their implementation in CM-01.
Decision 3 — R9 Disposition
ACCEPTED in full.
I specifically approve:

1. Introducing Functional Adequacy Assessment as a distinct conceptual category, separate from Capability Assessment.
2. Using the three assessment dimensions: integration and coordination, operational availability, and adequacy for the function.
3. Using the finding values: met, partly met, and not met, relative to explicit Assessment Criteria.
4. Making Standing Function designation of whole-function Capability Types conditional.
5. Distinguishing whole-function Capability Types from required component Capability Types.
6. Restricting Enabling Conditions to entities and circumstances relevant to a capability's realization.
7. Recording the planned CM-02 Agent Capability Conceptual Domain Model.

Implementation Guidance
This approval establishes the conceptual baseline, not final OWL axiomatization or specification ratification.
In specification v0.5 and subsequent modeling stages:

* Preserve the approved BFO/CCO distinctions and reuse existing classes and relations.
* Do not infer functional adequacy from component capability possession.
* Distinguish inadequate evidence from a finding of "not met."
* Recognize that losing an enabling artifact may affect availability without terminating the capability; availability also depends on whether adequate alternatives exist.
* Evaluate the formal representation of Functional Adequacy Assessment before deciding whether an additional OWL class is necessary.
* Resolve the documented BPO act-index integration dependencies before formal ontology implementation.

Do not alter the approved CM-01 content silently. Any subsequent substantive changes must follow the project's version-control and review procedures.
Recording
Please record these three approval acts, preserving this decision text and the approved artifact's full SHA-256.
Update the R8 and R9 disposition statuses and CM-01's approval status through the established governance process.
CM-01 is approved as the Stage 02 conceptual baseline for Business Capabilities. The broader Agent Capability model remains a separate planned deliverable.
````

---

## Act 1 — CM-01 approved

| Field | Value |
| --- | --- |
| Artifact | `src/02_conceptual_models/CM-01-business-capability.md`, version 0.1.0-draft.5 |
| Approved SHA-256 | `a59e3cd4149693ce388deaa7c8953242a8c3355e4c7eef96d094c8e90a75b5a0` |
| Verified against | `git show 1fa8b5a2011b66768431e239bd4e6eccfec80b6c:src/02_conceptual_models/CM-01-business-capability.md` (the commit that wrote draft.5) and the same path at `aa4b131ff7188ba639542967972a28bf1965001a`, both hashed before this record was written; the two agree, and the working file had the same digest |
| What it establishes | The Stage 02 conceptual baseline for Business Capabilities. Not OWL axiomatization, not specification ratification, not ratification of any vocabulary concept |
| Retained | The five conceptual patterns; DP-1 and DP-2 as decided |

**Recording the approval in the model.** The model's own §10 Review status must cite this
act, and its checker requires that it does. Writing that citation changes the file's bytes,
so the file in the repository after this record is not byte-identical to the approved
artifact. To keep that from being a silent alteration, the citation is made as a
status-only revision, numbered 0.1.0. Its revision history lists every line it changes,
all of them approval-status lines, and the commit that makes it shows the full diff
against the approved draft.5. The approved content is the text at the digest above, which
`git show 1fa8b5a:src/02_conceptual_models/CM-01-business-capability.md` reproduces exactly.

## Act 2 — R8 disposition accepted

`reviews/R8-disposition.md`, accepted, with row R8-07 qualified by the corrections adopted in
R9. The disposition's rows are left as written; only its Status row changes, to cite this
act. As the architect asked, the acceptance is read together with what followed R8:

- DP-1 (RP-1), Option A with a1–a4, decided 2026-10-25
  (`docs/decisions/2026-10-25-dp1-rp1-grounding-boundary.md`) on draft.2 at `5db0bfc`, and
  applied in draft.3 at `1b0c36f`.
- DP-2 (RP-10), Option A with b1, b3, b4 and b5, b2 rejected, decided 2026-10-26
  (`docs/decisions/2026-10-26-dp2-rp10-admission-attribution.md`) on draft.3 at `1b0c36f`,
  and applied in draft.4 at `8428d0c`. Amendment b5 is the G1-I change R8 row R8-06
  proposed.
- R8-07's qualification: draft.5 at `1fa8b5a` made the functional adequacy statement a
  separate Functional Adequacy Assessment (R9 row R9-01), already noted in row R8-07.

## Act 3 — R9 disposition accepted in full

`reviews/R9-disposition.md`, accepted in full, including the seven points the statement
lists: the Functional Adequacy Assessment as a distinct category; its three dimensions;
the finding values met, partly met and not met against explicit criteria; conditional
designation by a Standing Function; whole-function against component Capability Types;
Enabling Conditions restricted to what is relevant to a capability's realization; and the
planned CM-02 Agent Capability Conceptual Domain Model.

## Implementation guidance carried forward

The guidance in the statement binds specification v0.5 and later stages. It is carried,
not acted on, here. In particular, two of its points refine CM-01 in ways the approved text
does not yet state: distinguishing inadequate evidence from a finding of "not met", and
availability depending on whether adequate alternatives exist. Neither is written into
CM-01 by this record. Under the statement's last instruction, writing them in would be a
substantive change for the version-control and review procedure, so they are recorded in
`docs/HANDOFF.md` as inputs to v0.5 and to the next revision of CM-01.

## What this does not do

- It does not ratify RP-1, RP-10 or any other ratification point in the specification, or
  accept ADR-002; specification v0.5 has yet to be drafted.
- It does not ratify any vocabulary concept; all 14 remain Draft.
- It admits no capability type and asserts no OWL; `src/05_ontology/` stays empty.
- It does not start CM-02, which remains planned.
- It does not merge pull request #11.
