# G1-T type admission record — T1-03 Accounts payable processing capability

| Field | Value |
|---|---|
| Status | **DRAFT, not signed.** Prepared for the reviewer. An automated draft is not a signature (D4 decision of 2026-11-04, act 9) |
| Recommended finding | **PASS** |
| Reviewer | Aaron Damiano, the named approving reviewer for tranche 1 |
| Review date | — (set by the reviewer) |
| Candidate | BCC-62e789bf, catalog key `administration\|account payable`; tranche id T1-03. Hold lifted on its seven-act index, 2026-11-04 |
| Test | G1-T, specification v0.5.0-draft.3 §8 (`c3f1ba2`, SHA-256 `2224f869…c574`), ratified under RP-1, RP-2 (with CD5) and RP-10 on 2026-11-04 (`docs/decisions/2026-11-04-d4-rp1-rp10-ratified-option-b.md`, `docs/decisions/2026-11-04-rp2-ratified.md`) |
| Evidence | `docs/catalog/tranche-1.md` revision 3 (SHA-256 `155cf9e9…a10c`); `docs/catalog/candidates.yaml` (SHA-256 `4242de57…97d9`); BPO act types at the I-1 pin `bc64e91` |
| Drafted by | Claude Code (`claude-opus-5-5`), 2026-11-04 |

A PASS licenses asserting this class under `obo:BFO_0000016` (disposition), and so under
`bco:BusinessCapability`, for this class only (CAP-04). It licenses no organization's claim
to bear one (G1-I). Under Option B, nothing is asserted in OWL before all of CP-0 and D5.

Derived in part from the APQC Process Classification Framework® 7.4 (element names and
IDs, under APQC's notice in `NOTICE.md`). APQC does not endorse this work.

## The class as tested

**Definition** (tranche-1 §2, checked against CAP-07: no deontic terms). A business
capability of an organization to verify the amounts it owes its suppliers against what was
ordered and invoiced, resolve the exceptions, settle them by payment, account for them,
and answer inquiries about them, grounded in the organization's members as organized.

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
| 3 | **Through the organization's arrangements.** Do realizations run through its arrangements, not one person's skill on their own account? | **Yes** | Verification against purchase orders (`P10869`) depends on purchasing's records, exception resolution on purchasing and receiving, and payment on treasury: the work crosses positions. A one-person AP function still pays the organization's suppliers on its behalf (b1) |
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

To be completed by the reviewer only. The drafting agent leaves it blank.

| Finding (PASS / FAIL) | Reviewer | Date | Notes |
|---|---|---|---|
| | | | |
