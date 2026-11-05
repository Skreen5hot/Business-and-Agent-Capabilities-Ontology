# Decision record — CD6 to CD11 ratified, 2026-11-05

Recorded verbatim by Claude Code (`claude-opus-5-5`) on 2026-11-05, from the decision the
architect, Aaron Damiano, gave in session. The act is the architect's.

## What it is about

| Field | Value |
| --- | --- |
| Items | CD6, CD7, CD8, CD9, CD10 and CD11, §3 of `specifications/Business-Capability-Ontology-v0.5.0-draft.3.md` at `c3f1ba2`, SHA-256 `2224f869b0ec7a1e31b0afc1c2b403ad222ea290c334bff48a93ebbb6516c574` (accepted for ratification 2026-11-04) |
| Evidence decided on | `docs/proposals/2026-11-05-cd6-cd11-treatment.md` at `2df604e`, SHA-256 `edf61644a111d6126505db7161d6642811befbf7a29a527fc4118c281abe4ce6`, option A |
| CP-0 item | 14 of `docs/proposals/2026-11-05-cp0-closure-matrix.md`, "every other applicable specification decision" (roadmap D4) |

## The decision

````text
Subject: Architect Decision — Ratification of CD6–CD11
Decision: OPTION A APPROVED.
I approve the collective ratification of design decisions CD6, CD7, CD8, CD9, CD10 and CD11, as written in Business Capability Ontology specification v0.5.0-draft.3.
These decisions establish the following:

* CD6: Function classification requires specific BFO justification; Business Capability is not declared disjoint from Function.
* CD7: Capability is distinct from organizational role, responsibility, assignment and authorization.
* CD8: Capability does not require previous realization or an existential realization axiom.
* CD9: Capability subclass relationships represent genuine ontological specialization, not process decomposition, similarity or catalog hierarchy.
* CD10: Member-wise capability attribution is not organizational capability bearing.
* CD11: Information Content Entities describing capabilities are not themselves the capabilities they describe.

This decision closes CP-0 item 14 concerning the ratification status of these six design commitments.
Implementation boundaries

1. Preserve the existing CD6–CD11 wording. Do not introduce new architectural commitments through this decision.
2. Retain the approved CM-01 conceptual baseline and DP-1/DP-2 decisions.
3. Apply the existing CAP requirements during formalization, including checking inherited BPO realization restrictions.
4. Do not introduce new ontology classes, object properties or axioms merely by recording this ratification.
5. Use the existing review and admission processes for specific capability types and subclass relationships.

Record this as one collective architectural decision, explicitly identifying all six ratified commitments and the exact specification revision on which the decision rests.
Update the CP-0 status and affected decision-register references.
No additional individual ratification proposals for CD6–CD11 are required.
Other outstanding CP-0 items remain governed by their existing decisions.
Proceed with the remaining necessary work, prioritizing delivery of the comprehensive, source-supported capability catalog and its eventual ontology formalization.
````

## The acts it contains

1. **CD6 to CD11 are ratified as one collective decision**, as written in v0.5.0-draft.3
   at the digest above. The six are:
   - **CD6**, overlap with Function;
   - **CD7**, capability is not role or permission;
   - **CD8**, capacity, not exercise;
   - **CD9**, primitive classes, reviewed specialization;
   - **CD10**, member-wise bearing is not organizational bearing;
   - **CD11**, descriptions are about, not of.

   The ratified text is §3's wording. The decision's one-line summaries describe it; they
   do not replace it.
2. **CP-0 item 14 is closed for CD6 to CD11.** With CD5 ratified under RP-2, every CD in §3
   outside the register is now ratified. CD1 to CD4 are ratified under RP-1, RP-2 and
   RP-10. CD12 to CD17 remain with RP-3, RP-4 and RP-6 to RP-9.
3. **No separate ratification proposals** for CD6 to CD11 are required.
4. **Implementation boundaries.** The decision sets five, quoted above:
   - the wording is preserved, and no new commitment enters through this decision;
   - CM-01 and DP-1/DP-2 stand;
   - the existing CAP requirements apply at formalization, including the check of
     inherited BPO realization restrictions (CAP-02; OI-9);
   - no class, object property or axiom is introduced by recording it;
   - specific types and subclass links go through the existing review and admission
     processes (G1-T; CAP-10).

## How it was carried out

- **This record.** The specification is not edited. Its §3 lead-in still reads "Each is
  proposed, not ratified", and §10 has no row for these six. The next reviewed version
  records them, as it records RP-1, RP-2 and RP-10.
- **Status lines.** These are updated to say CD6 to CD11 are ratified:
  - `CLAUDE.md`;
  - `docs/DEVELOPMENT.md`;
  - `docs/HANDOFF.md`;
  - the roadmap's D4 row and its amendment log;
  - the status lines of the treatment note and the CP-0 closure matrix.

  Each proposal's body is unchanged.

## What it does not do

- It ratifies no register item. RP-3 to RP-9 stay drafts.
- It does not decide RP-5, SE-1, SE-2, ADR-002 or the stage-completion record. CP-0 stays
  open, and OWL still waits for all of CP-0 and D5.
- It mints and asserts nothing, and makes no G1-I claim.
