# Treatment of CD6 to CD11 — evidence for CP-0 decision 1

| Field | Value |
|---|---|
| Status | **Proposed.** For the architect. It decides nothing; the treatment is the architect's act |
| Closes | CP-0 closure matrix item 14, "every other applicable specification decision" (`docs/proposals/2026-11-05-cp0-closure-matrix.md`, decision 1) |
| Read from | Specification v0.5.0-draft.3 §3 and §10 (SHA-256 `2224f869…c574`); CM-01, approved 2026-10-26 (`src/02_conceptual_models/CM-01-business-capability.md`); the decision records of 2026-11-04 and 2026-11-05 |
| Prepared by | Claude Code (`claude-opus-5-5`), 2026-11-05 |

## 1. The gap

§3 says of all seventeen commitments: "Each is proposed, not ratified." §10's register has
ten items, covering CD1 to CD4 and CD12 to CD17. CD5 was ratified with RP-2
(`docs/decisions/2026-11-04-rp2-ratified.md`). **CD6 to CD11 belong to no register item.**
The roadmap's D4 row requires "every other applicable specification decision ratified", so
CP-0 cannot close until their status is settled.

## 2. Where each one is carried

"Ratified carrier" means a ratified register item whose text carries the commitment.
"Approved" means CM-01, the Stage 02 baseline. Requirements (CAP) are not ratified.

| CD | Commitment | Ratified carrier | Draft carrier | CM-01 (approved) | Already applied |
|---|---|---|---|---|---|
| CD6 | Overlap with Function: never disjoint from `obo:BFO_0000034`; placement under it only with a justification record meeting BFO's origin criterion (R5-10) | **None** | CAP-09 only | **Not carried.** It is an OWL placement rule, Stage 05's concern | — |
| CD7 | Not role or permission: no deontic words in definitions; "able but not authorized" and "authorized but not able" both representable | **Partly.** G1-T question 4 (RP-10) and CD4's non-deontic indexing (RP-2) cover **index members**, not definitions | CAP-07 (WARN) | P1; §6 boundaries "Able / permitted" and "Capability / role" | T1-03's worked case cites CD7 for "able but not authorized", in a record signed PASS |
| CD8 | Capacity, not exercise: no existential realization axiom; capacity evidence can suffice; past exercise needs present basis | **Partly.** §8 G1-I questions 2 and 3 carry b5 (RP-10). The no-`some` rule is not carried | CAP-02, CAP-26, CQ-4 | P2; Evidence concept; §6 boundary "Capacity / exercise" | G1-I is not yet applied |
| CD9 | Primitive classes, reviewed specialization: subclass means membership, established by review; nothing induced from coverage or APQC | **None** | CD14 (RP-6) and CD16 (RP-8) cite it; CAP-10 | RL-15; P5 (catalog, specialization and coverage); §6 boundary "Specialization / coverage" | — |
| CD10 | Member-wise bearing is not organizational bearing: `cco:ont00001898` never stands in for a Business Capability | **None** | CAP-12; CM-02's scope | Organization and Skill boundaries; §6 boundary "Organizational / individual" | — |
| CD11 | Descriptions are about, not of: description-layer ICEs refer by is-about and its subproperties; no ICE bears or realizes; two-party sourcing convention | **None** | §5 instance pattern 3 with CD17 (RP-9); CAP-11, CAP-23 | P3; §6 boundary "Description / described" | — |

Two results:

- **No CD in this range is fully carried by a ratified item.** CD7 and CD8 are partly
  carried by RP-10 and RP-2. CD9 and CD11 are cited only by drafts. CD6 and CD10 have no
  carrier at all.
- **Five of the six are already in the approved model.** CD7 to CD11 are in CM-01, approved
  as the Stage 02 baseline. Only CD6 is not, because it concerns OWL placement.

## 3. The treatments

**A. Ratify CD6 to CD11 together, as carried in draft.3.** Recommended.
- This settles item 14 in one act, and it follows the precedent of CD5, which was ratified
  outside the register.
- The next reviewed version of the specification adds a register row for them, as it will
  record the other ratifications.
- **Check:** section 2 is the check. Five of the six match approved text. CD6 rests on
  R5-10, accepted, and on BFO 2020's definition of function, which is at V (SRC-ISO-01). The
  architect may still ask for an RP-2-style point-by-point check first.

**B. Record them as design commitments carried under the items that cite them.**
- This needs no ratification now. Each CD would be settled when its carrier is settled.
- It leaves CD6 and CD10 with no carrier, so item 14 would stay open for them.
- CD9 and CD11 would wait on RP-6, RP-8 and RP-9.
- A signed PASS (T1-03) would keep resting on CD7, whose definition rule is not ratified.

**C. Ratify CD6, CD7 and CD10 now; carry CD8, CD9 and CD11 under RP-10, RP-6, RP-8 and RP-9.**
- This ratifies only the three commitments that nothing else will settle.
- It splits one section of the specification across four decisions, and CD8's no-`some`
  rule is still carried by no item.

## 4. What the decision would read

For A, the wording offered for the architect's act is:

> Ratify CD6 to CD11 as carried in specification v0.5.0-draft.3, SHA-256
> `2224f869…c574`.

The record would quote the architect's words verbatim, with that digest. It would not edit
the specification.

## 5. Boundary

This note adds no candidate, act, object property or OWL. It changes no CD, no requirement
and no approved model. It makes no G1-I claim and declares no part of CP-0 complete.
