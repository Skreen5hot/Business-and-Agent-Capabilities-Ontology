# Decision record — RP-2 ratified, with CD5, 2026-11-04

Recorded verbatim by Claude Code (`claude-opus-5-5`) on 2026-11-04, from the decision the
architect, Aaron Damiano, gave in session. The act is the architect's.

## What it is about

| Field | Value |
| --- | --- |
| Item | RP-2, the realization index (CD4), in `specifications/Business-Capability-Ontology-v0.5.0-draft.3.md` at `c3f1ba2`, SHA-256 `2224f869b0ec7a1e31b0afc1c2b403ad222ea290c334bff48a93ebbb6516c574` (accepted for ratification 2026-11-04) |
| Check decided on | `docs/proposals/2026-11-04-rp2-faithfulness-check.md` at `2b2135f` (PR #37), SHA-256 `86dc2a0b080ef67b6b266b5b34370b90a35716be01dc475885008b5b3f64fd87` |

## The decision

The recorder asked:

````text
Do you ratify RP-2, with CD5, on the check's recommended terms?
````

The architect answered:

````text
Ratify RP-2
````

**On the text as received.** The answer is the label of the reply button the recorder
offered. That button's full message read "RP-2 ratified as the check recommends, CD5
included; begin drafting the tranche 1 G1-T records for my review." Only the label
arrived. The record quotes only what arrived, and reads it as a yes to the question it
answered, which named CD5 and the check's recommended terms. **If the architect meant
RP-2 without CD5, that is a correction to this record**, made as a new record.

## The acts it contains, as read

1. **RP-2 is ratified as carried in draft.3:**
   - CD4;
   - CAP-03, CAP-05, CAP-21, CAP-30 and CAP-34;
   - the provider-performance rule in CD2's text (assigned to RP-2 by the D4 decision of
     2026-11-04, act 5).
2. **On the check's three recommended terms** (§6):
   - CAP-34's witness is a member agent of the bearer. Naming the organization alone does
     not satisfy it.
   - The authorization and development exclusions are carried by G1-T questions 4 and 5
     at review. RP-2 adds no automated check for them.
   - **CD5 (development and realization) is ratified with RP-2.**
3. **Option B's gate is met.** RP-1, RP-2 and RP-10 are ratified, so G1-T review of tranche
   1 may begin, and a review may record PASS or FAIL. The reviewer is Aaron Damiano (D4
   decision, act 9). Drafts are prepared for review, and an automated draft is not a
   signature.

## How it was carried out

- `docs/proposals/2026-11-04-rp2-faithfulness-check.md`: its status line records this decision.
- `docs/ROADMAP.md`: D4's note and the revision table.
- `CLAUDE.md` and `docs/HANDOFF.md`: what is ratified now.
- The tranche 1 G1-T records are drafted for the reviewer, on their own branch, stacked on
  the tranche 1 readiness record (PR #36).

## What it does not do

- It does not ratify RP-3 to RP-9, decide RP-5, accept ADR-002, approve SE-1 or SE-2, or
  complete CP-0 or D4.
- It does not choose the performance relation for CAP-34 (OI-8, Stage 05), and it adds no
  gate for deontic or development index members.
- No G1-T record exists yet, so it admits nothing. It mints nothing and asserts no OWL.
- The specification is not edited. Its §10 register records the ratification in its next
  reviewed version.
