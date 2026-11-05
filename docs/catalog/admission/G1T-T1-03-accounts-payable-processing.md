# G1-T type admission record — T1-03 Accounts payable processing capability

| Field | Value |
|---|---|
| Status | **Signed: PASS**, by the reviewer, 2026-11-05 (`docs/decisions/2026-11-05-g1t-tranche-1-signed.md`). Drafted by an agent for the reviewer; the signature is the reviewer's own confirmation below (D4 decision of 2026-11-04, act 9) |
| Finding | **PASS** (recommended in the draft; confirmed by the reviewer) |
| Reviewer | Aaron Damiano, the named approving reviewer for tranche 1 |
| Review date | 2026-11-05 |
| Candidate | BCC-62e789bf, catalog key `administration\|account payable`; tranche id T1-03. Hold lifted on its seven-act index, 2026-11-04 |
| Test | G1-T, specification v0.5.0-draft.3 §8 (`c3f1ba2`, SHA-256 `2224f869…c574`), ratified under RP-1, RP-2 (with CD5) and RP-10 on 2026-11-04 (`docs/decisions/2026-11-04-d4-rp1-rp10-ratified-option-b.md`, `docs/decisions/2026-11-04-rp2-ratified.md`) |
| Evidence | `docs/catalog/tranche-1.md` revision 4 (SHA-256 `dfafb555…c045`); `docs/catalog/candidates.yaml` (SHA-256 `4242de57…97d9`); BPO act types at the I-1 pin `bc64e91` |
| Drafted by | Claude Code (`claude-opus-5-5`), 2026-11-04; review clarifications applied 2026-11-05 |
| Review | Independent review of 2026-11-05 (My Ontologist 2.0, an AI system), `docs/catalog/admission/G1T-T1-review-2026-11-05.md` (SHA-256 `8373b4e7…a84e`): finding PASS, with the clarifications it requires applied below. AI-authored: not the reviewer's signature, which the confirmation table records |

A PASS licenses asserting this class under `obo:BFO_0000016` (disposition), and so under
`bco:BusinessCapability`, for this class only (CAP-04). It licenses no organization's claim
to bear one (G1-I). Under Option B, nothing is asserted in OWL before all of CP-0 and D5.

Derived in part from the APQC Process Classification Framework® 7.4 (element names and
IDs, under APQC's notice in `NOTICE.md`). APQC does not endorse this work.

## The class as tested

**Definition** (tranche-1 §2, checked against CAP-07: no deontic terms). A business
capability of an organization to verify the amounts it owes its suppliers against what was
invoiced and, where a purchase order applies, what was ordered, resolve the exceptions,
settle them by payment, account for them, and answer inquiries about them, grounded in the
organization's members as organized. (Revision 4 qualifies purchase-order matching, so that
a supplier invoice with no purchase order is not excluded; review of 2026-11-05.)

**Realization index** (CD4; tranche-1 §4, rebuilt from the twelve inventoried 9.6.1 acts,
none relabelled):

| Member | Via (PCF) | Genus (BPO) |
|---|---|---|
| `bpo:P10869` | 9.6.1.1 Verify AP pay file with purchase order vendor master file | Act of Appraisal |
| `bpo:P10871` | 9.6.1.3 Audit invoices and key data in AP system | Act of Appraisal |
| `bpo:P10873` | 9.6.1.5 Process financial accruals and reversals | Act of Accounting |
| `bpo:P10875` | 9.6.1.7 Research/Resolve payable exceptions | Act of Information Processing |
| `bpo:P10876` | 9.6.1.8 Process payments | Act of Financial Transaction |
| `bpo:P10877` | 9.6.1.9 Respond to AP inquiries | Act of Communication |
| `bpo:P10879` | 9.6.1.11 Adjust accounting records | Act of Accounting |

Excluded (5): `P10872` Approve payments (standing) and `P10870` electronic commerce (not
payables work), both removed by the decision of 2026-11-04; the summary act `P10756`;
`P10874`, the enterprise's tax returns; `P10878`, records retention.

Index checks: every member is a BPO act type, none a capability class or catalog node
(CAP-03); none is under a CAP-06 development genus; no `only` restriction is proposed
(CAP-30 not engaged).

## The five questions

| # | Question (§8) | Answer | Reasons and evidence |
|---|---|---|---|
| 1 | **Bearer kind.** Is the bearer an Organization? | **Yes** | The amounts are the organization's debts to its suppliers, settled from its accounts. PCF 9.6.1 places the ability with the enterprise. A clerk's skill at matching invoices is evidence, not the capability (CD1) |
| 2 | **Basis kind.** Can the basis be stated as the relevant member agents, as organized, without counting any artifact as basis? | **Yes** | The basis is the AP, purchasing and finance members who match, audit, resolve, accrue, pay and answer. The AP system, the vendor master file and payment rails are enabling conditions. Matching and payment can be done by hand, so none is constitutive (worked case 4). OI-14 is not engaged |
| 3 | **Through the organization's arrangements.** Do realizations run through its arrangements, not one person's skill on their own account? | **Yes** | The acts are performed through the organization's arrangements and on its behalf: verification draws on its records of what was ordered and received where a purchase order applies (`P10869`), and payment draws on its accounts. These arrangements often cross purchasing, receiving and treasury positions, but that is common, not required. A one-person AP function still acts through an arrangement and pays the organization's suppliers on its behalf (b1; review of 2026-11-05) |
| 4 | **Non-deontic.** Is every index member describable without standing or authorization? | **Yes** | "Approve payments" (`P10872`) was removed (decision of 2026-11-04, act 4); approval is standing, which an Authorization Record states. The verification that precedes approval is in the index as `P10869` and `P10871`. No member is relabelled. Processing a payment (`P10876`) executes it, and does not authorize it |
| 5 | **Exercise, not development.** Is every index member an exercise rather than its development (CD5)? | **Yes** | The summary act, whose source description includes developing AP policies and procedures, is out. Every member is part of handling an amount owed |

## Review rules

**Worked cases** (b3; CM-01 DP-1 table, under Option A as decided):

| Case | Applied to this type |
|---|---|
| Authority withdrawn (licence lapses) | A signatory's payment authority is withdrawn, or a bank mandate lapses. Payment cannot be released, which is recorded by an Authorization Record. The members can still verify, resolve and account. Unchanged. This is the "able but not authorized" case CD7 requires to be representable |
| Procedures or coordination dismantled | If the three-way match with purchasing and receiving is dismantled, members can no longer verify what is owed. The capability can end with no change in membership |
| Enabling system lost temporarily | An AP-system outage: assessed unavailable or degraded, with manual matching recorded as the alternative; possession unchanged |
| Enabling system decommissioned permanently | Persists latently, assessed unavailable until replaced. Manual matching and payment are feasible, so the system is not constitutive. The CD2 escalation applies only if no feasible alternative exists |
| Outside provider takes over the acts | An AP outsourcer's staff perform matching and payment. The organization keeps the capability only if its own members can still perform the acts. Otherwise a Capability Sourcing Statement records the arrangement (CAP-34). A member who only approves the outsourcer's payment run takes part, and does not perform |

**No permanent staging** (b4): if the reviewer finds FAIL, the class is reclassified or
removed, not left under `cco:ont00000568`.

**No interest condition** (b2 rejected): no sixth question.

## Reviewer's confirmation

Completed by the reviewer, Aaron Damiano, in session on 2026-11-05, and transcribed
verbatim into this table by the drafting agent (`docs/decisions/2026-11-05-g1t-tranche-1-signed.md`).

| Finding (PASS / FAIL) | Reviewer | Date | Notes |
|---|---|---|---|
| PASS | Aaron Damiano | 2026-11-05 (given as 11/5/2026) | Confirm all five answers and worked cases. Accept the seven-act index, including P10877; retain the exclusion of payment authorization. Accept non-purchase-order invoices and single-member organizational arrangements. |
