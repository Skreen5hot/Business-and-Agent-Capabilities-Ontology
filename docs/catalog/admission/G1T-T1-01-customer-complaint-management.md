# G1-T type admission record — T1-01 Customer complaint management capability

| Field | Value |
|---|---|
| Status | **AI-reviewed: PASS recommended; human confirmation pending.** A signature needs one authenticated approval by Aaron Damiano identifying this record, its finding and the reviewed version (`docs/decisions/2026-11-05-g1t-approval-provenance-corrected.md`, correcting `15ac666`). Neither an automated draft nor an AI review is a signature (D4 decision of 2026-11-04, act 9) |
| Finding | **PASS recommended** (by the draft and by the AI review of 2026-11-05); not confirmed |
| Reviewer | Aaron Damiano, the named approving reviewer for tranche 1 |
| Review date | — (pending human confirmation) |
| Candidate | BCC-373b146e, catalog key `management\|customer complaint`; tranche id T1-01 |
| Test | G1-T, specification v0.5.0-draft.3 §8 (`c3f1ba2`, SHA-256 `2224f869…c574`), ratified under RP-1, RP-2 (with CD5) and RP-10 on 2026-11-04 (`docs/decisions/2026-11-04-d4-rp1-rp10-ratified-option-b.md`, `docs/decisions/2026-11-04-rp2-ratified.md`) |
| Evidence | `docs/catalog/tranche-1.md` revision 4 (SHA-256 `dfafb555…c045`); `docs/catalog/candidates.yaml` (SHA-256 `4242de57…97d9`); BPO act types at the I-1 pin `bc64e91` |
| Drafted by | Claude Code (`claude-opus-5-5`), 2026-11-04; review clarifications applied 2026-11-05 |
| Review | Independent review of 2026-11-05 (My Ontologist 2.0, an AI system), `docs/catalog/admission/G1T-T1-review-2026-11-05.md` (SHA-256 `8373b4e7…a84e`): finding PASS, with the clarification it requires applied below. AI-authored: not the reviewer's signature, which the confirmation table records |

A PASS licenses asserting this class under `obo:BFO_0000016` (disposition), and so under
`bco:BusinessCapability`, for this class only (CAP-04). It licenses no organization's claim
to bear one (G1-I). Under Option B, nothing is asserted in OWL before all of CP-0 and D5.

Derived in part from the APQC Process Classification Framework® 7.4 (element names and
IDs, under APQC's notice in `NOTICE.md`). APQC does not endorse this work.

## The class as tested

**Definition** (tranche-1 §2, checked against CAP-07: no deontic terms). A business
capability of an organization to take in complaints from its customers, bring each to the
members able to act on it, resolve it, and answer the customer, grounded in the
organization's members as organized.

**Realization index** (CD4; tranche-1 §4, every member's disposition recorded there):

| Member | Via (PCF) | Genus (BPO) |
|---|---|---|
| `bpo:P10397` | 6.2.3.1 Receive customer complaints | Act of Communication |
| `bpo:P10398` | 6.2.3.2 Route customer complaints | Act of Communication |
| `bpo:P10399` | 6.2.3.3 Resolve customer complaints | Act of Resolution |
| `bpo:P10400` | 6.2.3.4 Respond to customer complaints | Act of Representative Communication |

Excluded: `bpo:P19072` (6.2.3.5, complaint analysis for service improvement), as
development (CD5), by the decision of 2026-11-04.

Index checks: every member is a BPO act type, none a capability class or catalog node
(CAP-03); none is under a CAP-06 development genus; no `only` restriction is proposed
(CAP-30 not engaged).

## The five questions

| # | Question (§8) | Answer | Reasons and evidence |
|---|---|---|---|
| 1 | **Bearer kind.** Is the bearer an Organization? | **Yes** | Complaints are made against the organization's offerings and answered on its behalf. PCF 6.2.3 and BPO's `CustomerComplaintManagementCapability` both place the ability with the enterprise, not a person. BPO's class is cited only as that evidence: it is a distinct capability type, which also takes in complaint analysis (`P19072`), and is neither equivalent to this class nor a designation of it; no subclass relation is established (review of 2026-11-05). A service representative's skill in calming a customer is CCO Skill (`cco:ont00000089`), and is evidence, not the capability (CD1) |
| 2 | **Basis kind.** Can the basis be stated as the relevant member agents, as organized, without counting any artifact as basis? | **Yes** | The basis is the members who take in, route, resolve and answer complaints: service staff, and the product, operations and finance members a complaint is routed to. The complaint-tracking system, phone lines and web forms are enabling conditions (CD2 item 3). The work can be done, worse, without any one of them, so none is constitutive (worked case 4). OI-14 is not engaged |
| 3 | **Through the organization's arrangements.** Do realizations run through its arrangements, not one person's skill on their own account? | **Yes** | Routing (`P10398`) exists to bring a complaint to the members able to act on it, which is the arrangement exercised. A resolution may commit the organization's product, service or finance positions. A small firm where one member handles every complaint still acts through an arrangement on the organization's behalf (b1) |
| 4 | **Non-deontic.** Is every index member describable without standing or authorization? | **Yes** | Receiving, routing, resolving and answering are operational. Resolving means correcting the situation. A grant of redress that confers a right on the customer (a refund entitlement, a waiver) is standing, is recorded by an Authorization Record if at all, and is not `P10399` |
| 5 | **Exercise, not development.** Is every index member an exercise rather than its development (CD5)? | **Yes** | Each member is a step in handling a complaint. The one development act, analysis of complaint logs for service improvement (`P19072`), is out of the index |

## Review rules

**Worked cases** (b3; CM-01 DP-1 table, under Option A as decided):

| Case | Applied to this type |
|---|---|
| Authority withdrawn (licence lapses) | No licence is needed to handle complaints in general. Where a regulator's permission is needed (an ombudsman-regulated sector), losing it ends the permission, recorded by an Authorization Record, not the capability. Unchanged |
| Procedures or coordination dismantled | If routing is dismantled, so that complaints reach no one able to act, the arrangement that makes the members' abilities organizational is gone. The capability can end, with no change in membership |
| Enabling system lost temporarily | A case-system outage: assessed unavailable, or degraded; possession unchanged |
| Enabling system decommissioned permanently | Persists latently, assessed unavailable until replaced. Complaints can be taken by phone and logged by hand, so the system is not constitutive. An irreversible loss with no alternative would send the type back to question 2 (CD2 escalation) |
| Outside provider takes over the acts | An outsourced contact centre performs intake and response. The organization's capability persists only if its own members can still perform the acts. Otherwise a Capability Sourcing Statement records the arrangement (CAP-34, RL-14) |

**No permanent staging** (b4): if the reviewer finds FAIL, the class is reclassified or
removed, not left under `cco:ont00000568`.

**No interest condition** (b2 rejected): no sixth question.

## Reviewer's confirmation

To be completed only from an authenticated approval by the reviewer. The drafting agent
leaves it blank.

| Finding (PASS / FAIL) | Reviewer | Date | Notes |
|---|---|---|---|
| | | | |

**Withdrawn row.** Commit `15ac666` wrote a row here giving PASS, Aaron Damiano and
2026-11-05, with the note below. It came from a message that the directive of 2026-11-05
identifies as an AI recommendation, not his signature, so it is withdrawn
(`docs/decisions/2026-11-05-g1t-approval-provenance-corrected.md`):

> Confirm all five G1-T answers and worked cases. Accept the four-act index and exclusion of P19072. BPO's broader type is distinct; no equivalence or subclass relationship is asserted.
