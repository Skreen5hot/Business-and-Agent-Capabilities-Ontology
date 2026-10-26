# Decision record — DP-2 (RP-10), admission and attribution: Option A with amendments b1, b3, b4 and b5; b2 rejected, 2026-10-26

Recorded verbatim by Claude Code (`claude-opus-5-5`) on 2026-10-26, at two statements the
product owner and architect, Aaron Damiano, made in session. The act is his.

---

The statement:

````text
DP-2 (RP-10): I choose Option A and accept amendments b1, b3, b4 and b5 as written in CM-01 0.1.0-draft.3 (SHA-256 837440ecf65f0ae34b9c2eb1fc47f6f9faf9b5dcae0e8420dbe0d7c95d57a80f). On b2 (interest condition): [accept or reject]. Record it.
````

The statement left b2 as the placeholder "[accept or reject]", which came from the reply
button the agent had offered. The agent asked, and the architect answered by selecting:

````text
Reject b2
````

The option selected was described to him as: "No sixth G1-T question. The record states
that BCO declines the interest condition for now and why: no reviewer asked for it, and an
organization's own interest plausibly satisfies it anyway. It can be revisited."

---

## What it is about

| Field | Value |
| --- | --- |
| Decision point | DP-2, which is specification RP-10 (admission and attribution, CD3, §8 G1-T and G1-I) |
| Text decided on | `src/02_conceptual_models/CM-01-business-capability.md`, 0.1.0-draft.3 |
| At commit | `1b0c36f` (PR #11, branch `stage/cm-01`) |
| SHA-256 of that text | `837440ecf65f0ae34b9c2eb1fc47f6f9faf9b5dcae0e8420dbe0d7c95d57a80f`, checked against `git show 1b0c36f:src/02_conceptual_models/CM-01-business-capability.md` before this record was written |
| Option chosen | **A** — two tests. A Type Admission Record (G1-T) is written once per capability type, with no organization in view, and a pass admits the type as a kind of disposition. Each claim that an organization bears a capability needs a supporting Capability Assessment answering G1-I. A type not yet admitted is staged under Organization Capability, transitionally |
| Amendments accepted | **b1** — G1-T question 3 asks whether realizations run through the organization's arrangements, which may involve one member, not through coordination across several positions (R6-08). **b3** — R6 Finding 1's constant-membership cases (the DP-1 table) are worked examples in every type review. **b4** — a type that fails G1-T is reclassified or removed, never left staged. **b5** — G1-I separates capacity from exercise: question 2 asks for evidence of capacity, with a recorded realization as supporting evidence that is never required; question 3 asks who *would* perform realizing acts; a present finding resting only on past exercise must also show the basis and arrangement are still in place (R8 finding 4) |
| Amendment rejected | **b2** — SF-04's interest condition is not added as a sixth G1-T question. The reason, as given in the option the architect selected: no reviewer asked for it, and an organization's own interest plausibly satisfies it anyway. It can be revisited |

## Rationale, as the decided text states it

From CM-01 draft.3 §7 DP-2, the drafter's recommendation the architect adopted: A is the
only option that keeps admission a matter of types and attribution a matter of evidence
about one organization, which is R7 Finding D's split and R6 Finding 1's request for
explicit criteria. b1 removes the one-analyst objection without weakening the
organizational test. b5 makes G1-I consistent with CD8: without it, a capability the
specification says may never have been realized could never be shown present.

## Limitations acknowledged

- A staging state outside BFO's role/disposition split (specification OI-7), bounded by b4
  but not removed.
- Two kinds of record to maintain: one Type Admission Record per type, one supporting
  assessment per bearing claim.
- BCO departs from both BFO-family precedents (IOF Core; Beverley et al.) on the interest
  condition (SF-04), by the rejection of b2.

## Effect

- CM-01 is revised to apply the decision (0.1.0-draft.4): the relationships that depended
  on DP-2 (records admission of; supports bearing of) become commitments; the G1-T and G1-I
  changes are stated in §6; Q-02 is closed; DP-2's decision line cites this record.
- With DP-1 and DP-2 both decided, no open question in CM-01 blocks approval. Approval
  itself still needs the architect's review of draft.4 and an approval act.
- Specification v0.5 is to carry the decision into CD3, §8 G1-T (question 3 per b1; b3 and
  b4 as review rules) and G1-I (questions 2 and 3 per b5), CAP-04, CAP-26, OI-7, and to
  record the SF-04 departure.

## What this does not do

- It does not approve CM-01, accept the R8 disposition (still proposed), ratify RP-10 in
  the specification, or ratify any vocabulary concept; all 14 remain Draft.
- It admits no capability type: no Type Admission Record exists, and no type has passed
  G1-T.
- It asserts no OWL: `src/05_ontology/` stays empty.
