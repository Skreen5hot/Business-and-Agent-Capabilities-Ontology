# G1-T type admission record — T1-02 Payroll processing capability

| Field | Value |
|---|---|
| Status | **Signed: PASS**, by the reviewer, 2026-11-05 (`docs/decisions/2026-11-05-g1t-tranche-1-signed.md`). Drafted by an agent for the reviewer; the signature is the reviewer's own confirmation below (D4 decision of 2026-11-04, act 9) |
| Finding | **PASS** (recommended in the draft; confirmed by the reviewer) |
| Reviewer | Aaron Damiano, the named approving reviewer for tranche 1 |
| Review date | 2026-11-05 |
| Candidate | BCC-d95f68fd, catalog key `administration\|payroll`; tranche id T1-02. Alternative designation: FEAF-II BRM "Payroll" (BCC-b7c46718, retired into this candidate on 2026-11-04) |
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
capability of an organization to determine, for each pay period, what each of its
employees is owed and what must be withheld, from recorded time and earnings, to pay it and
remit what is withheld, to account and report for it, and to answer its employees about
it, grounded in the organization's members as organized.

**Realization index** (CD4; tranche-1 §4, drawn act by act from two components, every
excluded act's reason recorded there):

| Member | Via (PCF) | Component | Genus (BPO) |
|---|---|---|---|
| `bpo:P10858` | 9.5.2.1 Enter employee time worked into payroll system | BCC-d105ff07 | Act of Information Processing |
| `bpo:P10859` | 9.5.2.2 Maintain and administer employee earnings information | BCC-d105ff07 | Act of Accounting |
| `bpo:P10860` | 9.5.2.3 Maintain and administer applicable deductions | BCC-d105ff07 | Act of Accounting |
| `bpo:P10861` | 9.5.2.4 Monitor changes in tax status of employees | BCC-d105ff07 | Act of Monitoring |
| `bpo:P10862` | 9.5.2.5 Process and distribute payments | BCC-d105ff07 | Act of Remuneration |
| `bpo:P10863` | 9.5.2.6 Process and distribute manual checks | BCC-d105ff07 | Act of Financial Transaction |
| `bpo:P10864` | 9.5.2.7 Process period-end adjustments | BCC-d105ff07 | Act of Accounting |
| `bpo:P10865` | 9.5.2.8 Respond to employee payroll inquiries | BCC-d105ff07 | Act of Information Processing |
| `bpo:P10866` | 9.5.3.3 Calculate and pay applicable payroll taxes | BCC-394909c1 | Act of Financial Transaction |
| `bpo:P10867` | 9.5.3.4 Produce and distribute employee annual tax statements | BCC-394909c1 | Act of Reporting |
| `bpo:P10868` | 9.5.3.5 File regulatory payroll tax forms | BCC-394909c1 | Act of Reporting |

Excluded (11): summary acts (`P10497`, `P10732`, `P10753`, `P10754`, `P10755`);
policy-setting and tax planning (`P10853`, `P14075`); Time Reporting's acts (`P10854` to
`P10857`), as a separate capability whose output payroll consumes.

Index checks: every member is a BPO act type, none a capability class or catalog node
(CAP-03); none is under a CAP-06 development genus; no `only` restriction is proposed
(CAP-30 not engaged).

## The five questions

| # | Question (§8) | Answer | Reasons and evidence |
|---|---|---|---|
| 1 | **Bearer kind.** Is the bearer an Organization? | **Yes** | Pay is owed by the employer, and payroll is run for it. PCF places payroll in two enterprise categories (7.5.4, 9.5), and BRM in central personnel management (B10.805.624). A payroll clerk's skill is evidence, not the capability (CD1) |
| 2 | **Basis kind.** Can the basis be stated as the relevant member agents, as organized, without counting any artifact as basis? | **Yes** | The basis is the payroll, HR and finance members who keep earnings and deduction data, compute pay, disburse it and report it. The payroll system, bank interfaces and tax tables are enabling conditions. Payroll was computed by hand before payroll systems existed and still can be at small scale, so no system is constitutive of the type (worked case 4). That is a claim about the type, not about every organization: manual operation need not be feasible for every organization at every scale, and where an irreversible loss leaves no feasible alternative, CD2 sends the question back to basis kind rather than continuing the attribution (review of 2026-11-05). OI-14 is not engaged |
| 3 | **Through the organization's arrangements.** Do realizations run through its arrangements, not one person's skill on their own account? | **Yes** | Earnings and deductions come from HR, the computation and disbursement from payroll and finance, and remittance and filing through the organization's tax reporting. In a firm with one bookkeeper, the bookkeeper still pays the organization's employees from its accounts, on its behalf (b1) |
| 4 | **Non-deontic.** Is every index member describable without standing or authorization? | **Yes** | Each member computes, records, pays, reports or answers. Filing tax forms (`P10868`) discharges an obligation, and confers no standing. Approving a payroll run, where an organization requires it, is not in the index |
| 5 | **Exercise, not development.** Is every index member an exercise rather than its development (CD5)? | **Yes** | Setting payroll policies (`P10853`) and planning to reduce tax liability (`P14075`) are formulation, and are out. Every member is part of running a pay cycle or its period-end and annual reporting |

## Review rules

**Worked cases** (b3; CM-01 DP-1 table, under Option A as decided):

| Case | Applied to this type |
|---|---|
| Authority withdrawn (licence lapses) | A lapsed payroll-tax registration or bank mandate withdraws standing to remit or disburse, recorded by an Authorization Record. The members can still compute and prepare pay. Unchanged |
| Procedures or coordination dismantled | If the hand-off of time and earnings data from HR to payroll is dismantled, no member can determine what is owed. The capability can end with no change in membership |
| Enabling system lost temporarily | A payroll-system outage at a cut-off date: assessed unavailable, with any manual run recorded as the alternative (G1-I question 4); possession unchanged |
| Enabling system decommissioned permanently | Persists latently, assessed unavailable until replaced. Manual computation is a feasible alternative at least at small scale, so the system is not constitutive of the type. That feasibility is not claimed for every organization. If an organization's scale made the loss irreversible with no alternative, the CD2 escalation sends the type back to question 2 |
| Outside provider takes over the acts | The commonest case for payroll (CQ-7). A bureau's staff perform the runs. The organization keeps the capability only if its own members can still perform them. Otherwise a Capability Sourcing Statement records the arrangement. This is CAP-34's own vendor fixture: an Acme clerk who supplies inputs and receives the report takes part, and does not perform |

**No permanent staging** (b4): if the reviewer finds FAIL, the class is reclassified or
removed, not left under `cco:ont00000568`.

**No interest condition** (b2 rejected): no sixth question.

## Reviewer's confirmation

Completed by the reviewer, Aaron Damiano, in session on 2026-11-05, and transcribed
verbatim into this table by the drafting agent (`docs/decisions/2026-11-05-g1t-tranche-1-signed.md`).

| Finding (PASS / FAIL) | Reviewer | Date | Notes |
|---|---|---|---|
| PASS | Aaron Damiano | 2026-11-05 (given as 11/5/2026) | Confirm all five answers and worked cases. Accept the eleven-act index, including P10865. Preserve CD2 escalation, the distinction from Time Reporting, and CAP-34 outsourcing treatment. |
