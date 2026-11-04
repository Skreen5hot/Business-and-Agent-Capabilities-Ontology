# RP-2 faithfulness check — the realization index (CD4), for ratification

| Field | Value |
|---|---|
| Status | **Proposed**, for the architect's decision. RP-2 is not ratified, and no G1-T record may be a PASS until it is |
| Date | 2026-11-04 |
| Prepared by | Claude Code (`claude-opus-5-5`), for the BCO team |
| Authorized by | The D4 decision of 2026-11-04, act 8 (`docs/decisions/2026-11-04-d4-rp1-rp10-ratified-option-b.md`) |
| Text checked | `specifications/Business-Capability-Ontology-v0.5.0-draft.3.md` at `c3f1ba2`, SHA-256 `2224f869b0ec7a1e31b0afc1c2b403ad222ea290c334bff48a93ebbb6516c574`, accepted for ratification on 2026-11-04 |
| Checked against | CM-01, approved (SHA-256 `292c8f36d64075b9663e159985a15b448aa933c3b5ed4baff3b2a556ca861ccc`): Realization Index, BPO Act Type, Act, RL-10 to RL-14. R5-05 (`reviews/R5-v0.4-artifact-review.md`) and R10-02 (`reviews/R10-disposition.md`), both accepted 2026-11-04 |
| Scope, as directed | CD4, R5-05, R10-02, CAP-21, CAP-34; with attention to participation and performance, the mandatory index, and the exclusion of authorization and development evidence |

## 1. What RP-2 is

The register (§10) states RP-2 as: "Mandatory `ex:enablesProcess` index; no capability
class as index member; `only` optional with an exhaustiveness review; CAP-21, and CAP-34
for performance rather than participation". Its status is "Revised (R5-05, R10-02)". The
provider-performance rule in CD2's text belongs here (D4 decision, act 5).

Unlike RP-1 and RP-10, RP-2 has no decision point of its own (no DP). Its faithfulness is
checked against the approved CM-01 and the review dispositions accepted on 2026-11-04.
The index has been in the specification since v0.2 (R2-01), and was revised in v0.3
(R3-04) and v0.4 (R4-03).

## 2. CD4 against CM-01, element by element

| CD4 (draft.3) | CM-01 (approved) | Faithful |
|---|---|---|
| Every specific capability class carries a mandatory realization index, one or more `ex:enablesProcess` annotations; the parent is exempt (CAP-03, R5-14) | Realization Index: "Mandatory for every specific Capability Type"; RL-10 "Mandatory for every specific type" | Yes |
| Each member names a BPO reality-layer act class or a D9 genus | BPO Act Type: "BCO uses BPO's act types and never declares its own" | Yes |
| The index lists admissible realization types; no modal claim, no exhaustiveness | Realization Index: "claims neither that the list is complete nor that every act of a listed type needs a capability"; RL-11 "Not exhaustive, not modal" | Yes |
| No index member is a capability class; BPO's entries naming capability classes are re-indexed first (Q-12, OI-20) | Realization Index, Boundaries: "A catalog node is never an index member, and neither is a capability type"; the 14 BPO breaches (Q-12) | Yes |
| `only` is optional, and only with a review record defending exhaustiveness (CAP-30) | RL-11: "exhaustiveness needs review (CAP-30)" | Yes |
| Classes are primitive; identity is bearer kind, grounding and index; no equivalence axiom | not stated in CM-01; a formalization choice consistent with it | Consistent; adds a formalization rule |
| An act that `realizes` a capability has an asserted type under an index member (CAP-21) | RL-12 "The act's asserted type falls under an index member (CAP-21)"; Act, Boundaries: "must be asserted, not inferred" | Yes |
| The act is also performed by a member agent of the bearer, not merely one taking part (CAP-34; RL-14; R5-05, R10-02) | RL-14 *is performed by*; Act: "An act performed by a provider's staff realizes the provider's capability, not the consumer's" | Yes, and stricter (§3) |
| Coverage is not here (CD16) | Realization Index: "Not coverage (P5)" | Yes |
| Non-deontic indexing: members describable without deontic success conditions; an institutional act indexes to the non-deontic act it contains | Realization Index: "must be describable without standing or authorization (CD4)" | Yes (§4) |

**No discrepancy found in CD4.**

## 3. Participation and performance (R5-05, R10-02, CAP-34)

| Step | What it said | Where it is now |
|---|---|---|
| R5-05 (v0.4 review) | CAP-21 checks the act's type, not that the organization did it; a vendor's process could pass. Proposed BFO *has participant* (`obo:BFO_0000057`) or a CCO agent relation, with no new property | Accepted with amendment: CAP-34 added, requiring a performance witness. *Has participant* not adopted for the check |
| R10-02 (v0.5 draft.1 review) | Draft.1's CAP-34 asked only for participation; that is not enough. Align with CM-01 RL-14, add the vendor fixture, choose the relation at Stage 05, mint nothing | Accepted (draft.2): CAP-34 requires a member agent of the bearer to **perform** each realizing act |

CAP-34 as written: at least one member agent of the bearer performs the act. Taking part in
an act others perform does not count, and neither does naming only the organization as
performer. The fixtures are the vendor case (PayCo staff run Acme's payroll while an Acme
clerk supplies inputs and receives the report), a provider's process with no consumer
member, and an act whose only named performer is the organization. The passes are an Acme
member performing the act, and a joint performance by an Acme member and vendor staff.

**Faithful to RL-14 and both dispositions.** Three points the architect accepts with RP-2:

1. **CAP-34 is stricter than RL-14's range.** RL-14 allows an Organization as performer.
   CAP-34 lets the organization be named, but does not count that as the witness, because
   the organization's performance is the claim the check exists to support. R10's
   disposition put this to the architect, and the 2026-11-04 acceptance of R10-02 took it
   as written. Ratifying RP-2 confirms it. An exception would need a revision.
2. **BFO's *realizes* and CAP-34 ask different things, without conflict.** BFO's
   elucidation of *realizes* (`obo:BFO_0000055`, vendored) requires that the bearer
   participate in the realizing process. CAP-34 adds that a member of the bearer performs
   it. The first is BFO's condition on the organization, the second is BCO's evidence of it.
3. **The performance relation is not yet chosen, and that blocks encoding, not
   ratification.** Neither a CCO "is performed by" relation nor an agent-participation
   relation is in the vendored extracts (checked: no label containing "performed" or
   "has agent"). OI-8 covers it. The relation is chosen at Stage 05 under §3.1's reuse
   order, and none is minted. CAP-34 is marked "encoding at Stage 05".

## 4. Authorization and development evidence

The decision asked for attention here. Both exclusions are in the text. Neither has a
mechanical check that would have caught tranche 1's cases.

| Exclusion | Where it is stated | What enforces it | Gap |
|---|---|---|---|
| **Authorization and standing** | CD4 "Non-deontic indexing"; CD7 (definitions); G1-T question 4, ratified under RP-10 | G1-T question 4, at review (gate F). CAP-07 checks **definitions** for deontic words, as WARN. No requirement checks **index members** | An approval act typed under a neutral genus passes every automated gate. Tranche 1's `bpo:P10872` "Approve payments" is typed under Planned Act (`cco:ont00000228`); only the review caught it. The catalog's deontic flag is a screen on labels, not a gate |
| **Development** | CD5; CM-01 Realization Index ("acts that exercise the capability, not develop it"); G1-T question 5, ratified under RP-10 | CAP-06, as WARN, for members under four BPO genera: Act of Development, Act of Improvement, Act of Organizational Establishment, Act of Acquisition. G1-T question 5 at review | The genus list is narrower than CD5. Tranche 1's development exclusions were under **Act of Formulation** (`P10853`, `P14075`) and **Act of Analysis** (`P19072`), which CAP-06 does not list. CD5 is a judgement about the act, which a genus can only approximate |

**Neither gap makes RP-2 unfaithful.** CM-01 makes both exclusions review judgements, and
G1-T questions 4 and 5 are now binding. They mean the review, not the gates, carries both
exclusions. Two consequences for the architect, neither needed to ratify RP-2:

- **CD5 and CD7 are not ratification items.** §10's ten items cover CD1 to CD4 and CD12 to
  CD17. CD5 to CD11 are not in the register. G1-T questions 4 and 5 apply CD5 and CD4's
  non-deontic rule, and RP-10 made those questions binding. The text the questions point
  to has not been ratified on its own. **Recommended:** ratify RP-2 as covering CD4 and
  CD5 together, since CD5 is the criterion of CM-01's Realization Index. Or record that
  CD5 to CD11 are carried as design commitments under the ratified items that cite them.
- **Optional hardening for a later revision**, not proposed now: a CAP-06 genus list that
  includes formulation and analysis acts used for improvement, and a WARN on index members
  whose BPO output is an approval or authorization. Either is a specification change, and
  needs a reviewed version.

## 5. CAP-21

CAP-21: every act that `realizes` a K1 instance has an asserted type under one of the
capability's index members in the asserted class hierarchy, checked before any reasoning
(gate C-A). It is faithful to RL-12 and to CM-01's Act ("must be asserted, not inferred").
The reason it runs before reasoning (§8): where an `only` restriction exists, a reasoner
would classify a misasserted act into the permitted type. Its fixture (`ex:P10729`, scoped
to Accounting, realizing a strategic planning capability) is the right kind of negative.

## 6. Recommended disposition

**Ratify RP-2 as carried in draft.3:**

- CD4;
- CAP-03, CAP-05, CAP-21, CAP-30 and CAP-34;
- the provider-performance rule in CD2.

Make three points explicit in the ratification:

1. CAP-34's witness is a member agent; naming the organization alone does not satisfy it
   (§3 point 1).
2. The authorization and development exclusions are carried by G1-T questions 4 and 5 at
   review, and RP-2 adds no automated check for them (§4).
3. CD5 is ratified with RP-2, or recorded as a design commitment under RP-10 (§4).
   **Recommended: with RP-2.**

With RP-1, RP-2 and RP-10 ratified, Option B's gate for G1-T review is met. The G1-T records
for tranche 1 can then be drafted for Aaron Damiano's review. Each PASS needs:
- the reviewer and the review date;
- five reasoned answers;
- the supporting evidence;
- the completed constant-membership cases.

No PASS is the default.

## 7. What this check does not do

It ratifies nothing and changes no text. RP-3 (whether `ex:enablesProcess` is an annotation)
and OI-6 (where BPO declares it) are separate items. RP-5, ADR-002, SE-1 and SE-2 remain
CP-0 obligations.
