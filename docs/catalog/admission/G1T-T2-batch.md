# G1-T batch review — tranche 2, 43 candidate classes

| Field | Value |
|---|---|
| Status | **Prepared for batch review. Not signed.** Each class's PASS or FAIL is the named reviewer's, recorded in its confirmation row. A draft recommendation is not a finding (`docs/decisions/2026-11-07-tranche-2-accepted-g1t-preparation-authorized.md`, A3: preparation, not admission) |
| Reviewer | To be named by the architect. Tranche 1's named approving reviewer was Aaron Damiano |
| Candidates | The 43 that `docs/catalog/tranche-2.md` (section 5) reports ready, ids T2-01 to T2-43 |
| Test | G1-T, specification v0.5.0-draft.3 §8 (`c3f1ba2`, SHA-256 `2224f869…c574`), ratified under RP-1, RP-2 (with CD5) and RP-10 on 2026-11-04 (`docs/decisions/2026-11-04-d4-rp1-rp10-ratified-option-b.md`, `docs/decisions/2026-11-04-rp2-ratified.md`), applied as in tranche 1's signed records |
| Evidence | `docs/catalog/candidates.yaml` (SHA-256 `0eb60d5b703ac0f17063e9bc8317d5ecb381e41e4ef84ea7e48c43e6a0160d93`); `docs/catalog/bpo-act-types.yaml` (SHA-256 `25be29e5d4df6b7d8671128a7fae4cafa20aec2a6ac53cb2dbae2f8f76b800eb`), BPO act types at the I-1 pin `bc64e91`; `docs/catalog/tranche-2-review.yaml` (SHA-256 `cf9d1409791d2bfda01c09fe0af816962fa1bc682bede1ef40e966426ff6a71c`) |
| Drafted by | Claude Code (`claude-opus-5-5`), 2026-11-07 |

A PASS licenses asserting the class under `obo:BFO_0000016` (disposition), and so under
`bco:BusinessCapability`, for that class only (CAP-04). It licenses no organization's claim
to bear one (G1-I). Under Option B, nothing is asserted in OWL before all of CP-0 and D5.

Derived in part from the APQC Process Classification Framework® 7.4 (element names and
IDs, under APQC's notice in `NOTICE.md`). APQC does not endorse this work.

## 1. How the indexes were drawn

Each index (CD4) is drawn act by act from the candidate's realization evidence in the
generated catalog, and only from existing BPO act types at the pin. No act type is invented.
An act is left out for one of these reasons, which each class's table names:

| Code | Reason | Rule |
|---|---|---|
| CAP-03 | BPO types the class under a capability class, so it is not an act (Q-12) | CAP-03 |
| Q4 | It grants, alters or withdraws standing or authorization | G1-T question 4 |
| Q5 | It governs or develops the capability rather than exercising it: setting the policies for its own practice, or establishing organizational structure | G1-T question 5, CD5, CAP-06 |
| OTHER | It is another concept's work, or outside the definition (named) | the definition |
| HOMONYM | It is a different ability that the generator's key merged in | tranche-2 review |

Approval is treated as deontic, as Payments Approval was (tranche 1, act 5). An act whose
name joins work with its approval is left out whole, because BPO's class cannot be split.
A development-genus act that is kept carries its CAP-06 reason. Acts of candidates merged or
rejected into a class are taken where the tranche-2 review assigned them.

A component's acts are not taken into its broader concept's index, whether the link is
`part-of` or `kind-of`. Each index is the class's own evidence.

## 2. The batch

| Id | Candidate | Concept | Index | Excluded | Draft recommendation |
|---|---|---|---|---|---|
| T2-01 | BCC-9511900a | Payment Processing | 2 | 0 | PASS |
| T2-02 | BCC-ea6d1c4a | Corporate Card Management | 4 | 3 | PASS, with question 4 for the reviewer |
| T2-03 | BCC-35c8111b | Expense Reimbursement Processing | 4 | 2 | PASS |
| T2-04 | BCC-15e92684 | Capital Planning | 1 | 4 | PASS, or hold until BPO separates planning from approval |
| T2-05 | BCC-95b092a2 | Capital Project Accounting | 5 | 1 | PASS |
| T2-06 | BCC-60d672db | Financial Accounting | 1 | 0 | PASS, or treat as a capability area |
| T2-07 | BCC-e8acc1f8 | Accounting Policy Management | 2 | 3 | PASS, with question 4 for the reviewer |
| T2-08 | BCC-792537f9 | Financial Reporting | 11 | 0 | PASS |
| T2-09 | BCC-e3c8bd37 | Fixed-Asset Accounting | 9 | 1 | PASS |
| T2-10 | BCC-8b431985 | General Ledger Accounting | 10 | 0 | PASS |
| T2-11 | BCC-4f5c2f36 | Letter of Credit Management | 1 | 0 | PASS |
| T2-12 | BCC-e1fa4843 | Trade Product Classification | 1 | 2 | PASS |
| T2-13 | BCC-f6799472 | Restricted Party Screening | 1 | 0 | PASS |
| T2-14 | BCC-c5e7dca0 | Trade and Customs Documentation | 4 | 0 | PASS |
| T2-15 | BCC-0c80b752 | Trade Preference Management | 1 | 0 | PASS |
| T2-16 | BCC-b55668bc | Internal Control Reporting | 5 | 0 | PASS |
| T2-17 | BCC-80a63f8e | Internal Control Design | 4 | 2 | PASS, with question 4 for the reviewer |
| T2-18 | BCC-5dfa2101 | International Rate Monitoring | 1 | 0 | PASS |
| T2-19 | BCC-bf62316a | Cross-Border Funds Transfer Management | 1 | 0 | PASS |
| T2-20 | BCC-d105ff07 | Pay Management | 9 | 0 | PASS |
| T2-21 | BCC-394909c1 | Payroll Tax Processing | 4 | 1 | PASS |
| T2-22 | BCC-85fbcb90 | Time Reporting | 5 | 1 | PASS |
| T2-23 | BCC-302a390a | Cost Accounting | 6 | 1 | PASS |
| T2-24 | BCC-b47b8fed | Cost Management | 4 | 1 | PASS |
| T2-25 | BCC-cedf0899 | Financial Performance Management | 7 | 1 | PASS |
| T2-26 | BCC-87e1811c | Financial Planning, Budgeting and Forecasting | 4 | 2 | PASS |
| T2-27 | BCC-1cccc689 | Revenue and Receivables Management | 1 | 0 | PASS, or treat as a capability area |
| T2-28 | BCC-6587dedf | Accounts Receivable Processing | 5 | 1 | PASS |
| T2-29 | BCC-cebf0da8 | Customer Deduction and Adjustment Management | 6 | 1 | PASS |
| T2-30 | BCC-c4904759 | Collections Management | 6 | 1 | PASS |
| T2-31 | BCC-b7ff0eac | Customer Credit Management | 5 | 3 | PASS, with question 4 for the reviewer |
| T2-32 | BCC-8a70a337 | Customer Invoicing | 6 | 0 | PASS |
| T2-33 | BCC-ce052840 | Tax Planning | 3 | 1 | PASS |
| T2-34 | BCC-52f0795a | Tax Processing | 7 | 1 | PASS |
| T2-35 | BCC-a1c5454d | Cash Management | 3 | 6 | PASS |
| T2-36 | BCC-749adb52 | In-House Bank Account Management | 6 | 2 | PASS |
| T2-37 | BCC-132e1b29 | Financial Risk Management | 2 | 5 | PASS |
| T2-38 | BCC-3e668a26 | Counterparty Credit Exposure Management | 4 | 1 | PASS |
| T2-39 | BCC-7c04ea8a | Foreign Exchange Risk Management | 6 | 1 | PASS |
| T2-40 | BCC-8fdf31c6 | Hedging Transaction Execution | 4 | 2 | PASS |
| T2-41 | BCC-0564598d | Interest Rate Risk Management | 4 | 1 | PASS |
| T2-42 | BCC-7757c12b | Treasury Policy Management | 5 | 4 | PASS, with question 4 for the reviewer |
| T2-43 | BCC-ded8ed18 | Internal Control Operation and Monitoring | 2 | 1 | PASS |

No draft recommends FAIL. 8 leave an open question to the reviewer, named in each class's
section: question 4 for 5 policy, design, credit and card classes; whether two summary
classes are capability areas; and a one-act index for Capital Planning. Other classes
carry notes for the reviewer that explain an answer, not open questions.

## 3. Evidence checks

The drafting script checked each of these, and stopped on any failure:
- every index member is a BPO act type at the pin, in the class's own realization evidence or in that of a candidate the review merged or rejected into it (6 brought in that way);
- no member is typed under a capability class (17 such acts excluded under CAP-03);
- every member's PCF record is in the PCF inventory;
- no member has a development genus without a CAP-06 reason (1 kept with one);
- every excluded act is in the evidence, so nothing is excluded that was never there;
- no definition has a CAP-07 deontic stem.

In all, the 43 indexes have 182 members, and 56 acts are excluded.

## 4. The classes

### T2-01 — Payment Processing

| Field | Value |
|---|---|
| Candidate | BCC-9511900a, catalog key `administration\|payment`; concept `bcoc:PaymentProcessing` |
| Definition | A business capability of an organization to make the payments it has decided to make, by the means and on the dates due, and record each payment made, grounded in the organization's members as organized. (checked against CAP-07: no deontic terms) |
| Proposed classification | `bco:BusinessCapability` (CM-01), under `obo:BFO_0000016` (disposition) on a PASS; foundational ancestor `cco:ont00000568` (Organization Capability), as the vocabulary records; bearer `cco:ont00001180` (Organization) |
| Grounding | **Basis:** the payables and payroll members who release payments, by the means and on the dates set, and record them, as organized. **Enabling, not basis:** the banking interfaces, payment files and the ledger. **Arrangements:** payments are made from the organization's accounts, on its behalf, under its payment runs |

**Realization index** (2):

| Member | Via (PCF) | Genus (BPO) | Evidence |
|---|---|---|---|
| `bpo:P10862` | 9.5.2.5 Process and distribute payments | Act of Remuneration | designating record |
| `bpo:P10876` | 9.6.1.8 Process payments | Act of Financial Transaction | designating record |

**Taxonomy review** (`docs/catalog/tranche-2-review.yaml`; classified, not validated):

| Link | Disposition | Reason |
|---|---|---|
| Payment Processing → Accounts Payable Processing | retained, `part-of`, kept | tranche 1 §5: a component of T1-03, not a subtype |
| Payment Processing → Pay Management | retained, `part-of`, kept | tranche 1 §5: a component of T1-02's pay management, not a subtype |

| # | Question (§8) | Draft answer |
|---|---|---|
| 1 | Bearer kind: an Organization? | **Yes**. The work is the organization's: payments are made from the organization's accounts, on its behalf, under its payment runs |
| 2 | Basis kind: member agents as organized, no artifact counted? | **Yes**. The payables and payroll members who release payments, by the means and on the dates set, and record them. The banking interfaces, payment files and the ledger are enabling conditions; the work can be done with other tools, so none is constitutive of the type |
| 3 | Through the organization's arrangements? | **Yes**. Realizations run through its division of work and its accounts and records, not one person's skill on their own account |
| 4 | Non-deontic index? | **Yes**. No member grants, alters or withdraws standing or authorization |
| 5 | Exercise, not development (CD5)? | **Yes** |

**Draft recommendation:** PASS.

**Notes for the reviewer:**
- Both index members are already in signed indexes (T1-02, T1-03). The draft reads that as consistent with a component, not as double counting.

| Finding (PASS / FAIL) | Reviewer | Date | Notes |
|---|---|---|---|
|  |  |  |  |

### T2-02 — Corporate Card Management

| Field | Value |
|---|---|
| Candidate | BCC-ea6d1c4a, catalog key `management\|corporate credit card`; concept `bcoc:CorporateCardManagement` |
| Definition | A business capability of an organization to provide payment cards to its members for business spending, set their terms, reconcile what is spent with them and settle the card accounts, grounded in the organization's members as organized. (checked against CAP-07: no deontic terms) |
| Proposed classification | `bco:BusinessCapability` (CM-01), under `obo:BFO_0000016` (disposition) on a PASS; foundational ancestor `cco:ont00000568` (Organization Capability), as the vocabulary records; bearer `cco:ont00001180` (Organization) |
| Grounding | **Basis:** the card programme administrators and accounts-payable members who handle card requests, card accounts and their settlement, as organized. **Enabling, not basis:** the card issuer's platform and the expense system. **Arrangements:** cards are issued on the organization's account with its issuer, and settled from its accounts |

**Realization index** (4):

| Member | Via (PCF) | Genus (BPO) | Evidence |
|---|---|---|---|
| `bpo:P20929` | 9.6.3 Manage corporate credit cards | Act of Card Administration | designating record |
| `bpo:P20931` | 9.6.3.2 Process corporate credit card requests | Act of Card Administration | process beneath it |
| `bpo:P20932` | 9.6.3.3 Order corporate credit cards | Act of Acquisition | process beneath it; CAP-06: ordering a card from the issuer is how the capability provides one to a member: an exercise, not an enlargement of the capability |
| `bpo:P20933` | 9.6.3.4 Manage corporate credit card accounts | Act of Accounting | process beneath it |

**Excluded** (3):

| Act | Via (PCF) | Code | Reason |
|---|---|---|---|
| `bpo:P20930` | 9.6.3.1 Establish corporate credit card policies and approval limits | Q4 | setting card policies and approval limits fixes members' spending authority |
| `bpo:P20934` | 9.6.3.5 Approve/Change credit limits | Q4 | approving or changing a credit limit confers or alters a holder's standing to spend |
| `bpo:P20935` | 9.6.3.6 Cancel/Deactivate credit card | Q4 | cancelling or deactivating a card withdraws a holder's standing to spend |

**Taxonomy review** (`docs/catalog/tranche-2-review.yaml`; classified, not validated):

| Link | Disposition | Reason |
|---|---|---|
| Corporate Card Management → Accounts Payable and Expense Reimbursement Management | retained, `part-of`, kept | PCF hierarchy; the narrower's work is part of the broader's, not a kind of it |

| # | Question (§8) | Draft answer |
|---|---|---|
| 1 | Bearer kind: an Organization? | **Yes**. The work is the organization's: cards are issued on the organization's account with its issuer, and settled from its accounts |
| 2 | Basis kind: member agents as organized, no artifact counted? | **Yes**. The card programme administrators and accounts-payable members who handle card requests, card accounts and their settlement. The card issuer's platform and the expense system are enabling conditions; the work can be done with other tools, so none is constitutive of the type |
| 3 | Through the organization's arrangements? | **Yes**. Realizations run through its division of work and its accounts and records, not one person's skill on their own account |
| 4 | Non-deontic index? | **Yes, for the reviewer to confirm** (below); excluded as deontic: `P20930`, `P20934`, `P20935` |
| 5 | Exercise, not development (CD5)? | **Yes**; kept with a CAP-06 reason: `P20932` |

**Draft recommendation:** PASS, with question 4 for the reviewer.

**Notes for the reviewer:**
- The definition's 'set their terms' and 'provide payment cards' sit close to delegated spending authority. The draft keeps the administrative acts and excludes every act that grants, alters or withdraws a holder's standing. The reviewer decides whether question 4 is met.

| Finding (PASS / FAIL) | Reviewer | Date | Notes |
|---|---|---|---|
|  |  |  |  |

### T2-03 — Expense Reimbursement Processing

| Field | Value |
|---|---|
| Candidate | BCC-35c8111b, catalog key `administration\|expense reimbursement`; concept `bcoc:ExpenseReimbursementProcessing` |
| Definition | A business capability of an organization to check the expenses its members claim for work done on its behalf against its rules and their receipts, and repay those that qualify, grounded in the organization's members as organized. (checked against CAP-07: no deontic terms) |
| Proposed classification | `bco:BusinessCapability` (CM-01), under `obo:BFO_0000016` (disposition) on a PASS; foundational ancestor `cco:ont00000568` (Organization Capability), as the vocabulary records; bearer `cco:ont00001180` (Organization) |
| Grounding | **Basis:** the accounts-payable or expense members who check claims against the rules and receipts and repay them, as organized. **Enabling, not basis:** the expense system and the payment interfaces. **Arrangements:** members claim from and are repaid by the organization, under its rules, from its accounts |

**Realization index** (4):

| Member | Via (PCF) | Genus (BPO) | Evidence |
|---|---|---|---|
| `bpo:P10757` | 9.6.2 Process expense reimbursements | Act of Financial Transaction | designating record |
| `bpo:P10881` | 9.6.2.2 Capture and report relevant tax data | Act of Reporting | process beneath it |
| `bpo:P10883` | 9.6.2.4 Process reimbursements and advances | Act of Financial Transaction | process beneath it |
| `bpo:P10884` | 9.6.2.5 Manage personnel accounts | Act of Accounting | process beneath it |

**Excluded** (2):

| Act | Via (PCF) | Code | Reason |
|---|---|---|---|
| `bpo:P10880` | 9.6.2.1 Establish and communicate expense reimbursement policies and approval limits | Q5 | establishing reimbursement policies and approval limits: setting the policies that govern this capability's own practice shapes the capability rather than exercising it (tranche-1 practice, T1-02 question 5); the limits are also deontic |
| `bpo:P10882` | 9.6.2.3 Approve reimbursements and advances | Q4 | approving reimbursements and advances is an authorization, as Payments Approval was (tranche 1, act 5) |

**Taxonomy review** (`docs/catalog/tranche-2-review.yaml`; classified, not validated):

| Link | Disposition | Reason |
|---|---|---|
| Expense Reimbursement Processing → Accounts Payable and Expense Reimbursement Management | retained, `part-of`, kept | PCF hierarchy; the narrower's work is part of the broader's, not a kind of it |

| # | Question (§8) | Draft answer |
|---|---|---|
| 1 | Bearer kind: an Organization? | **Yes**. The work is the organization's: members claim from and are repaid by the organization, under its rules, from its accounts |
| 2 | Basis kind: member agents as organized, no artifact counted? | **Yes**. The accounts-payable or expense members who check claims against the rules and receipts and repay them. The expense system and the payment interfaces are enabling conditions; the work can be done with other tools, so none is constitutive of the type |
| 3 | Through the organization's arrangements? | **Yes**. Realizations run through its division of work and its accounts and records, not one person's skill on their own account |
| 4 | Non-deontic index? | **Yes**. No member grants, alters or withdraws standing or authorization; excluded as deontic: `P10882` |
| 5 | Exercise, not development (CD5)? | **Yes**; excluded: `P10880` |

**Draft recommendation:** PASS.

| Finding (PASS / FAIL) | Reviewer | Date | Notes |
|---|---|---|---|
|  |  |  |  |

### T2-04 — Capital Planning

| Field | Value |
|---|---|
| Candidate | BCC-15e92684, catalog key `governance\|capital planning and project`; concept `bcoc:CapitalPlanning` |
| Definition | A business capability of an organization to identify and evaluate proposed capital investments, budget for them, and prepare the financial case on which a decision to proceed is made, grounded in the organization's members as organized. (checked against CAP-07: no deontic terms) |
| Proposed classification | `bco:BusinessCapability` (CM-01), under `obo:BFO_0000016` (disposition) on a PASS; foundational ancestor `cco:ont00000568` (Organization Capability), as the vocabulary records; bearer `cco:ont00001180` (Organization) |
| Grounding | **Basis:** the finance and planning members who identify, evaluate and budget capital investments and prepare their financial case, as organized. **Enabling, not basis:** the planning models and the capital budget. **Arrangements:** proposals are gathered and evaluated through the organization's capital-planning cycle, for its decision |

**Realization index** (1):

| Member | Via (PCF) | Genus (BPO) | Evidence |
|---|---|---|---|
| `bpo:P10847` | 9.4.1.4 Conduct financial justification for project approval | Act of Appraisal | process beneath it |

**Excluded** (4):

| Act | Via (PCF) | Code | Reason |
|---|---|---|---|
| `bpo:P10751` | 9.4.1 Perform capital planning and project approval | Q4 | the designating process joins capital planning with project approval, and its name makes approval part of it |
| `bpo:P10844` | 9.4.1.1 Develop capital investment policies and procedures | Q5 | developing capital investment policies: setting the policies that govern this capability's own practice shapes the capability rather than exercising it (tranche-1 practice, T1-02 question 5) |
| `bpo:P10845` | 9.4.1.2 Develop and approve capital expenditure plans and budgets | Q4 | developing and approving capital plans and budgets joins the planning with its approval |
| `bpo:P10846` | 9.4.1.3 Review and approve capital projects and fixed-asset acquisitions | Q4 | reviewing and approving capital projects is the decision the definition leaves out |

**Taxonomy review** (`docs/catalog/tranche-2-review.yaml`; classified, not validated):

| Link | Disposition | Reason |
|---|---|---|
| Capital Planning → Capital Expenditure Management | retained, `part-of`, kept | PCF hierarchy; the narrower's work is part of the broader's, not a kind of it |

| # | Question (§8) | Draft answer |
|---|---|---|
| 1 | Bearer kind: an Organization? | **Yes**. The work is the organization's: proposals are gathered and evaluated through the organization's capital-planning cycle, for its decision |
| 2 | Basis kind: member agents as organized, no artifact counted? | **Yes**. The finance and planning members who identify, evaluate and budget capital investments and prepare their financial case. The planning models and the capital budget are enabling conditions; the work can be done with other tools, so none is constitutive of the type |
| 3 | Through the organization's arrangements? | **Yes**. Realizations run through its division of work and its accounts and records, not one person's skill on their own account |
| 4 | Non-deontic index? | **Yes**. No member grants, alters or withdraws standing or authorization; excluded as deontic: `P10751`, `P10845`, `P10846` |
| 5 | Exercise, not development (CD5)? | **Yes**; excluded: `P10844` |

**Draft recommendation:** PASS, or hold until BPO separates planning from approval.

**Notes for the reviewer:**
- Excluding the three acts that join planning with approval leaves a one-act index (P10847). The reviewer may accept a thin index, or hold the class until BPO separates planning from approval.

| Finding (PASS / FAIL) | Reviewer | Date | Notes |
|---|---|---|---|
|  |  |  |  |

### T2-05 — Capital Project Accounting

| Field | Value |
|---|---|
| Candidate | BCC-95b092a2, catalog key `accounting\|capital project`; concept `bcoc:CapitalProjectAccounting` |
| Definition | A business capability of an organization to account for the costs of capital projects while they are under way, and transfer them to fixed assets when the projects are complete, grounded in the organization's members as organized. (checked against CAP-07: no deontic terms) |
| Proposed classification | `bco:BusinessCapability` (CM-01), under `obo:BFO_0000016` (disposition) on a PASS; foundational ancestor `cco:ont00000568` (Organization Capability), as the vocabulary records; bearer `cco:ont00001180` (Organization) |
| Grounding | **Basis:** the accounting members who code, record and track capital-project costs and capitalize them on completion, as organized. **Enabling, not basis:** the project ledger and the fixed-asset register. **Arrangements:** project costs are recorded in the organization's ledgers by its accounting rules |

**Realization index** (5):

| Member | Via (PCF) | Genus (BPO) | Evidence |
|---|---|---|---|
| `bpo:P10752` | 9.4.2 Perform capital project accounting | Act of Accounting | designating record |
| `bpo:P10848` | 9.4.2.1 Create project account codes | Act of Accounting | process beneath it |
| `bpo:P10849` | 9.4.2.2 Record project-related transactions | Act of Accounting | process beneath it |
| `bpo:P10850` | 9.4.2.3 Monitor and track capital projects and budget spending | Act of Monitoring | process beneath it |
| `bpo:P10851` | 9.4.2.4 Close/capitalize projects | Act of Selection | process beneath it |

**Excluded** (1):

| Act | Via (PCF) | Code | Reason |
|---|---|---|---|
| `bpo:P10852` | 9.4.2.5 Measure financial returns on completed capital projects | OTHER | measuring returns on completed projects is Financial Performance Management's work, not project accounting |

**Taxonomy review** (`docs/catalog/tranche-2-review.yaml`; classified, not validated):

| Link | Disposition | Reason |
|---|---|---|
| Capital Project Accounting → Capital Expenditure Management | retained, `part-of`, kept | PCF hierarchy; the narrower's work is part of the broader's, not a kind of it |

| # | Question (§8) | Draft answer |
|---|---|---|
| 1 | Bearer kind: an Organization? | **Yes**. The work is the organization's: project costs are recorded in the organization's ledgers by its accounting rules |
| 2 | Basis kind: member agents as organized, no artifact counted? | **Yes**. The accounting members who code, record and track capital-project costs and capitalize them on completion. The project ledger and the fixed-asset register are enabling conditions; the work can be done with other tools, so none is constitutive of the type |
| 3 | Through the organization's arrangements? | **Yes**. Realizations run through its division of work and its accounts and records, not one person's skill on their own account |
| 4 | Non-deontic index? | **Yes**. No member grants, alters or withdraws standing or authorization |
| 5 | Exercise, not development (CD5)? | **Yes** |

**Draft recommendation:** PASS.

| Finding (PASS / FAIL) | Reviewer | Date | Notes |
|---|---|---|---|
|  |  |  |  |

### T2-06 — Financial Accounting

| Field | Value |
|---|---|
| Candidate | BCC-60d672db, catalog key `accounting\|general accounting and reporting`; concept `bcoc:FinancialAccounting` |
| Definition | A business capability of an organization to keep its financial records by accepted accounting principles and prepare from them the financial statements it reports, grounded in the organization's members as organized. (checked against CAP-07: no deontic terms) |
| Proposed classification | `bco:BusinessCapability` (CM-01), under `obo:BFO_0000016` (disposition) on a PASS; foundational ancestor `cco:ont00000568` (Organization Capability), as the vocabulary records; bearer `cco:ont00001180` (Organization) |
| Grounding | **Basis:** the accounting members who keep the financial records and prepare the statements, as organized. **Enabling, not basis:** the general ledger and the accounting systems. **Arrangements:** the records are the organization's books, kept under its accounting policies |

**Realization index** (1):

| Member | Via (PCF) | Genus (BPO) | Evidence |
|---|---|---|---|
| `bpo:P10730` | 9.3 Perform general accounting and reporting | Act of Accounting | designating record |

**Taxonomy review** (`docs/catalog/tranche-2-review.yaml`; classified, not validated):

| Link | Disposition | Reason |
|---|---|---|
| Financial Accounting → Financial Resource Management | retained, `part-of`, kept | PCF hierarchy; the narrower's work is part of the broader's, not a kind of it |
| Financial Reporting → Financial Accounting | retained, `part-of`, kept | PCF hierarchy; the narrower's work is part of the broader's, not a kind of it |
| General Ledger Accounting → Financial Accounting | retained, `part-of`, kept | PCF hierarchy; the narrower's work is part of the broader's, not a kind of it |
| Fixed-Asset Accounting → Financial Accounting | retained, `part-of`, kept | PCF hierarchy; the narrower's work is part of the broader's, not a kind of it |
| Accounting Policy Management → Financial Accounting | retained, `part-of`, kept | PCF hierarchy; the narrower's work is part of the broader's, not a kind of it |
| Financial Accounting → BCC-81d8f125 (outside the tranche) | retained, `kind-of`, added | financial accounting is accounting with its object restricted; the target is outside the tranche |

| # | Question (§8) | Draft answer |
|---|---|---|
| 1 | Bearer kind: an Organization? | **Yes**. The work is the organization's: the records are the organization's books, kept under its accounting policies |
| 2 | Basis kind: member agents as organized, no artifact counted? | **Yes**. The accounting members who keep the financial records and prepare the statements. The general ledger and the accounting systems are enabling conditions; the work can be done with other tools, so none is constitutive of the type |
| 3 | Through the organization's arrangements? | **Yes**. Realizations run through its division of work and its accounts and records, not one person's skill on their own account |
| 4 | Non-deontic index? | **Yes**. No member grants, alters or withdraws standing or authorization |
| 5 | Exercise, not development (CD5)? | **Yes** |

**Draft recommendation:** PASS, or treat as a capability area.

**Notes for the reviewer:**
- The index is the one summary act PCF 9.3. Its four components (General Ledger Accounting, Fixed-Asset Accounting, Financial Reporting, Accounting Policy Management) are part-of links, so their acts are not taken into this index. The reviewer may prefer to treat it as a capability area (CD16, E4).

| Finding (PASS / FAIL) | Reviewer | Date | Notes |
|---|---|---|---|
|  |  |  |  |

### T2-07 — Accounting Policy Management

| Field | Value |
|---|---|
| Candidate | BCC-e8acc1f8, catalog key `management\|financial policy and procedure`; concept `bcoc:AccountingPolicyManagement` |
| Definition | A business capability of an organization to set, publish and maintain the accounting and financial-reporting policies and procedures its members follow, grounded in the organization's members as organized. (checked against CAP-07: no deontic terms) |
| Proposed classification | `bco:BusinessCapability` (CM-01), under `obo:BFO_0000016` (disposition) on a PASS; foundational ancestor `cco:ont00000568` (Organization Capability), as the vocabulary records; bearer `cco:ont00001180` (Organization) |
| Grounding | **Basis:** the controllership members who draft, publish and maintain accounting and reporting policies, as organized. **Enabling, not basis:** the policy manual and its publication channels. **Arrangements:** the policies are the organization's, issued through its controllership for its members to follow |

**Realization index** (2):

| Member | Via (PCF) | Genus (BPO) | Evidence |
|---|---|---|---|
| `bpo:P10816` | 9.3.1.2 Establish accounting policies | Act of Formulation | process beneath it |
| `bpo:P20604` | 9.3.1.3 Publish accounting policies | Act of Communication | process beneath it |

**Excluded** (3):

| Act | Via (PCF) | Code | Reason |
|---|---|---|---|
| `bpo:P10815` | 9.3.1.1 Negotiate service-level agreements | OTHER | negotiating service-level agreements is not accounting-policy work |
| `bpo:P10817` | 9.3.1.4 Set and enforce approval limits | Q4 | setting and enforcing approval limits fixes who may approve what |
| `bpo:P10818` | 9.3.1.5 Establish common financial systems | OTHER | establishing common financial systems sets up enabling artifacts, which are not basis and not policy work |

**Taxonomy review** (`docs/catalog/tranche-2-review.yaml`; classified, not validated):

| Link | Disposition | Reason |
|---|---|---|
| Accounting Policy Management → Financial Accounting | retained, `part-of`, kept | PCF hierarchy; the narrower's work is part of the broader's, not a kind of it |

| # | Question (§8) | Draft answer |
|---|---|---|
| 1 | Bearer kind: an Organization? | **Yes**. The work is the organization's: the policies are the organization's, issued through its controllership for its members to follow |
| 2 | Basis kind: member agents as organized, no artifact counted? | **Yes**. The controllership members who draft, publish and maintain accounting and reporting policies. The policy manual and its publication channels are enabling conditions; the work can be done with other tools, so none is constitutive of the type |
| 3 | Through the organization's arrangements? | **Yes**. Realizations run through its division of work and its accounts and records, not one person's skill on their own account |
| 4 | Non-deontic index? | **Yes, for the reviewer to confirm** (below); excluded as deontic: `P10817` |
| 5 | Exercise, not development (CD5)? | **Yes** |

**Draft recommendation:** PASS, with question 4 for the reviewer.

**Notes for the reviewer:**
- Question 4: the draft holds that formulating and publishing a policy is describable without standing, and that adopting it with authority is a separate act, not in the index. The reviewer decides.

| Finding (PASS / FAIL) | Reviewer | Date | Notes |
|---|---|---|---|
|  |  |  |  |

### T2-08 — Financial Reporting

| Field | Value |
|---|---|
| Candidate | BCC-792537f9, catalog key `reporting\|financial reporting`; concept `bcoc:FinancialReporting` |
| Definition | A business capability of an organization to prepare its financial statements, and the reports drawn from them, and present them to its management, its board and outside parties, grounded in the organization's members as organized. (checked against CAP-07: no deontic terms) |
| Proposed classification | `bco:BusinessCapability` (CM-01), under `obo:BFO_0000016` (disposition) on a PASS; foundational ancestor `cco:ont00000568` (Organization Capability), as the vocabulary records; bearer `cco:ont00001180` (Organization) |
| Grounding | **Basis:** the reporting and consolidation members who prepare the statements and the reports drawn from them, as organized. **Enabling, not basis:** the ledger, the consolidation system and the reporting templates. **Arrangements:** the statements are the organization's, prepared from its books and issued in its name |

**Realization index** (11):

| Member | Via (PCF) | Genus (BPO) | Evidence |
|---|---|---|---|
| `bpo:P10750` | 9.3.4 Perform financial reporting | Act of Reporting | designating record |
| `bpo:P10837` | 9.3.4.1 Prepare business unit financial statements | Act of Reporting | process beneath it |
| `bpo:P10838` | 9.3.4.2 Prepare consolidated financial statements | Act of Reporting | process beneath it |
| `bpo:P10839` | 9.3.4.3 Perform business unit reporting/review management reports | Act of Reporting | process beneath it |
| `bpo:P10840` | 9.3.4.4 Perform consolidated reporting/review of cost management reports | Act of Reporting | process beneath it |
| `bpo:P10841` | 9.3.4.5 Prepare statements for board review | Act of Reporting | process beneath it |
| `bpo:P10842` | 9.3.4.6 Produce quarterly/annual filings and shareholder reports | Act of Reporting | process beneath it |
| `bpo:P10843` | 9.3.4.7 Produce regulatory reports | Act of Reporting | process beneath it |
| `bpo:P14074` | 9.3.4.8 Perform legal and management consolidation | Act of Accounting | process beneath it |
| `bpo:P10770` | 9.10.4 Report results | Act of Reporting | from BCC-5caed753 (merged) |
| `bpo:P11042` | 12.3.1 Report financial results | Act of Reporting | from BCC-18ef14d6 (merged) |

**Taxonomy review** (`docs/catalog/tranche-2-review.yaml`; classified, not validated):

| Link | Disposition | Reason |
|---|---|---|
| Financial Reporting → Financial Accounting | retained, `part-of`, kept | PCF hierarchy; the narrower's work is part of the broader's, not a kind of it |

| # | Question (§8) | Draft answer |
|---|---|---|
| 1 | Bearer kind: an Organization? | **Yes**. The work is the organization's: the statements are the organization's, prepared from its books and issued in its name |
| 2 | Basis kind: member agents as organized, no artifact counted? | **Yes**. The reporting and consolidation members who prepare the statements and the reports drawn from them. The ledger, the consolidation system and the reporting templates are enabling conditions; the work can be done with other tools, so none is constitutive of the type |
| 3 | Through the organization's arrangements? | **Yes**. Realizations run through its division of work and its accounts and records, not one person's skill on their own account |
| 4 | Non-deontic index? | **Yes**. No member grants, alters or withdraws standing or authorization |
| 5 | Exercise, not development (CD5)? | **Yes** |

**Draft recommendation:** PASS.

**Notes for the reviewer:**
- From the merged BCC-5caed753, only P10770 (PCF 9.10.4, reporting foreign exchange results) is taken. Its second record, P17489 (PCF 13.3.2.2.2, summarizing evaluation results), is a homonym the key merged, and is not brought in.

| Finding (PASS / FAIL) | Reviewer | Date | Notes |
|---|---|---|---|
|  |  |  |  |

### T2-09 — Fixed-Asset Accounting

| Field | Value |
|---|---|
| Candidate | BCC-e3c8bd37, catalog key `accounting\|fixed-asset`; concept `bcoc:FixedAssetAccounting` |
| Definition | A business capability of an organization to record its fixed assets and account for their cost and its consumption over their useful lives, from acquisition to disposal, keeping the asset register consistent with the ledger, grounded in the organization's members as organized. (checked against CAP-07: no deontic terms) |
| Proposed classification | `bco:BusinessCapability` (CM-01), under `obo:BFO_0000016` (disposition) on a PASS; foundational ancestor `cco:ont00000568` (Organization Capability), as the vocabulary records; bearer `cco:ont00001180` (Organization) |
| Grounding | **Basis:** the fixed-asset accountants who keep the register and record additions, changes, depreciation and disposals, as organized. **Enabling, not basis:** the fixed-asset register and the ledger. **Arrangements:** the assets are the organization's, accounted for in its books by its policies |

**Realization index** (9):

| Member | Via (PCF) | Genus (BPO) | Evidence |
|---|---|---|---|
| `bpo:P10749` | 9.3.3 Perform fixed-asset accounting | Act of Accounting | designating record |
| `bpo:P10829` | 9.3.3.2 Maintain fixed-asset master data files | Act of Accounting | process beneath it |
| `bpo:P10830` | 9.3.3.3 Process and record fixed-asset additions and retires | Act of Accounting | process beneath it |
| `bpo:P10831` | 9.3.3.4 Process and record fixed-asset adjustments, enhancements, revaluations, and transfers | Act of Accounting | process beneath it |
| `bpo:P10832` | 9.3.3.5 Process and record fixed-asset maintenance and repair expenses | Act of Accounting | process beneath it |
| `bpo:P10833` | 9.3.3.6 Calculate and record depreciation expense | Act of Accounting | process beneath it |
| `bpo:P10834` | 9.3.3.7 Reconcile fixed-asset ledger | Act of Accounting | process beneath it |
| `bpo:P10835` | 9.3.3.8 Track fixed-assets including physical inventory | Act of Monitoring | process beneath it |
| `bpo:P10836` | 9.3.3.9 Provide fixed-asset data to support tax, statutory, and regulatory reporting | Act of Reporting | process beneath it |

**Excluded** (1):

| Act | Via (PCF) | Code | Reason |
|---|---|---|---|
| `bpo:P10828` | 9.3.3.1 Establish fixed-asset policies and procedures | Q5 | establishing fixed-asset policies and procedures: setting the policies that govern this capability's own practice shapes the capability rather than exercising it (tranche-1 practice, T1-02 question 5) |

**Taxonomy review** (`docs/catalog/tranche-2-review.yaml`; classified, not validated):

| Link | Disposition | Reason |
|---|---|---|
| Fixed-Asset Accounting → Financial Accounting | retained, `part-of`, kept | PCF hierarchy; the narrower's work is part of the broader's, not a kind of it |

| # | Question (§8) | Draft answer |
|---|---|---|
| 1 | Bearer kind: an Organization? | **Yes**. The work is the organization's: the assets are the organization's, accounted for in its books by its policies |
| 2 | Basis kind: member agents as organized, no artifact counted? | **Yes**. The fixed-asset accountants who keep the register and record additions, changes, depreciation and disposals. The fixed-asset register and the ledger are enabling conditions; the work can be done with other tools, so none is constitutive of the type |
| 3 | Through the organization's arrangements? | **Yes**. Realizations run through its division of work and its accounts and records, not one person's skill on their own account |
| 4 | Non-deontic index? | **Yes**. No member grants, alters or withdraws standing or authorization |
| 5 | Exercise, not development (CD5)? | **Yes**; excluded: `P10828` |

**Draft recommendation:** PASS.

| Finding (PASS / FAIL) | Reviewer | Date | Notes |
|---|---|---|---|
|  |  |  |  |

### T2-10 — General Ledger Accounting

| Field | Value |
|---|---|
| Candidate | BCC-8b431985, catalog key `accounting\|general accounting`; concept `bcoc:GeneralLedgerAccounting` |
| Definition | A business capability of an organization to record its financial transactions in its ledgers by accepted accounting principles, close its books for each period, and keep its accounts reconciled, grounded in the organization's members as organized. (checked against CAP-07: no deontic terms) |
| Proposed classification | `bco:BusinessCapability` (CM-01), under `obo:BFO_0000016` (disposition) on a PASS; foundational ancestor `cco:ont00000568` (Organization Capability), as the vocabulary records; bearer `cco:ont00001180` (Organization) |
| Grounding | **Basis:** the general-ledger accountants who post, adjust, reconcile and close the books, as organized. **Enabling, not basis:** the general ledger and the chart of accounts. **Arrangements:** the ledger is the organization's, kept by its accounting calendar and rules |

**Realization index** (10):

| Member | Via (PCF) | Genus (BPO) | Evidence |
|---|---|---|---|
| `bpo:P10748` | 9.3.2 Perform general accounting | Act of Accounting | designating record |
| `bpo:P10819` | 9.3.2.1 Maintain chart of accounts | Act of Accounting | process beneath it |
| `bpo:P10820` | 9.3.2.2 Process journal entries | Act of Accounting | process beneath it |
| `bpo:P10821` | 9.3.2.3 Process allocations | Act of Accounting | process beneath it |
| `bpo:P10822` | 9.3.2.4 Process period end adjustments | Act of Accounting | process beneath it |
| `bpo:P10823` | 9.3.2.5 Post and reconcile intercompany transactions | Act of Accounting | process beneath it |
| `bpo:P10824` | 9.3.2.6 Reconcile general ledger accounts | Act of Accounting | process beneath it |
| `bpo:P10825` | 9.3.2.7 Perform consolidations and process eliminations | Act of Accounting | process beneath it |
| `bpo:P10826` | 9.3.2.8 Prepare trial balance | Act of Accounting | process beneath it |
| `bpo:P10827` | 9.3.2.9 Prepare and post management adjustments | Act of Accounting | process beneath it |

**Taxonomy review** (`docs/catalog/tranche-2-review.yaml`; classified, not validated):

| Link | Disposition | Reason |
|---|---|---|
| General Ledger Accounting → Financial Accounting | retained, `part-of`, kept | PCF hierarchy; the narrower's work is part of the broader's, not a kind of it |
| General Ledger Accounting → BCC-81d8f125 (outside the tranche) | retained, `kind-of`, redundant | true, but covered through Financial Accounting, which is linked to the target instead |

| # | Question (§8) | Draft answer |
|---|---|---|
| 1 | Bearer kind: an Organization? | **Yes**. The work is the organization's: the ledger is the organization's, kept by its accounting calendar and rules |
| 2 | Basis kind: member agents as organized, no artifact counted? | **Yes**. The general-ledger accountants who post, adjust, reconcile and close the books. The general ledger and the chart of accounts are enabling conditions; the work can be done with other tools, so none is constitutive of the type |
| 3 | Through the organization's arrangements? | **Yes**. Realizations run through its division of work and its accounts and records, not one person's skill on their own account |
| 4 | Non-deontic index? | **Yes**. No member grants, alters or withdraws standing or authorization |
| 5 | Exercise, not development (CD5)? | **Yes** |

**Draft recommendation:** PASS.

| Finding (PASS / FAIL) | Reviewer | Date | Notes |
|---|---|---|---|
|  |  |  |  |

### T2-11 — Letter of Credit Management

| Field | Value |
|---|---|
| Candidate | BCC-4f5c2f36, catalog key `formulation\|letter of credit`; concept `bcoc:LetterOfCreditManagement` |
| Definition | A business capability of an organization to arrange letters of credit for its trade, by which a bank assures payment to a seller once agreed conditions are met, and present the documents they call for, grounded in the organization's members as organized. (checked against CAP-07: no deontic terms) |
| Proposed classification | `bco:BusinessCapability` (CM-01), under `obo:BFO_0000016` (disposition) on a PASS; foundational ancestor `cco:ont00000568` (Organization Capability), as the vocabulary records; bearer `cco:ont00001180` (Organization) |
| Grounding | **Basis:** the trade-finance or treasury members who apply for letters of credit and present their documents, as organized. **Enabling, not basis:** the bank's trade-finance platform and the trade documents. **Arrangements:** the letters of credit are arranged with the organization's banks for its own trade |

**Realization index** (1):

| Member | Via (PCF) | Genus (BPO) | Evidence |
|---|---|---|---|
| `bpo:P14098` | 9.11.10 Prepare letter of credit | Act of Formulation | designating record |

**Taxonomy review** (`docs/catalog/tranche-2-review.yaml`; classified, not validated):

| Link | Disposition | Reason |
|---|---|---|
| Letter of Credit Management → Global Trade Management | retained, `part-of`, kept | PCF hierarchy; the narrower's work is part of the broader's, not a kind of it |

| # | Question (§8) | Draft answer |
|---|---|---|
| 1 | Bearer kind: an Organization? | **Yes**. The work is the organization's: the letters of credit are arranged with the organization's banks for its own trade |
| 2 | Basis kind: member agents as organized, no artifact counted? | **Yes**. The trade-finance or treasury members who apply for letters of credit and present their documents. The bank's trade-finance platform and the trade documents are enabling conditions; the work can be done with other tools, so none is constitutive of the type |
| 3 | Through the organization's arrangements? | **Yes**. Realizations run through its division of work and its accounts and records, not one person's skill on their own account |
| 4 | Non-deontic index? | **Yes**. No member grants, alters or withdraws standing or authorization |
| 5 | Exercise, not development (CD5)? | **Yes** |

**Draft recommendation:** PASS.

**Notes for the reviewer:**
- The bank's undertaking to pay is the bank's standing, not the organization's. Preparing the application and the documents is describable without the organization's standing, so the draft answers question 4 yes.

| Finding (PASS / FAIL) | Reviewer | Date | Notes |
|---|---|---|---|
|  |  |  |  |

### T2-12 — Trade Product Classification

| Field | Value |
|---|---|
| Candidate | BCC-e1fa4843, catalog key `analysis\|product`; concept `bcoc:TradeProductClassification` |
| Definition | A business capability of an organization to classify the goods and services it trades under the tariff and control classifications that apply to them, grounded in the organization's members as organized. (checked against CAP-07: no deontic terms) |
| Proposed classification | `bco:BusinessCapability` (CM-01), under `obo:BFO_0000016` (disposition) on a PASS; foundational ancestor `cco:ont00000568` (Organization Capability), as the vocabulary records; bearer `cco:ont00001180` (Organization) |
| Grounding | **Basis:** the trade-compliance members who classify the organization's goods under tariff and control lists, as organized. **Enabling, not basis:** the tariff schedules, control lists and the product master. **Arrangements:** the classifications are the organization's declarations about its own goods |

**Realization index** (1):

| Member | Via (PCF) | Genus (BPO) | Evidence |
|---|---|---|---|
| `bpo:P14092` | 9.11.3 Classify products | Act of Analysis | designating record |

**Excluded** (2):

| Act | Via (PCF) | Code | Reason |
|---|---|---|---|
| `bpo:P10112` | 3.1.1.5 Evaluate existing products/services | HOMONYM | PCF 3.1.1.5 evaluates products for marketing, a different ability the key merged |
| `bpo:P10783` | 9.1.4.2 Evaluate new products | HOMONYM | PCF 9.1.4.2 evaluates new products financially, a different ability the key merged |

**Taxonomy review** (`docs/catalog/tranche-2-review.yaml`; classified, not validated):

| Link | Disposition | Reason |
|---|---|---|
| Trade Product Classification → Global Trade Management | retained, `part-of`, kept | PCF hierarchy; the narrower's work is part of the broader's, not a kind of it; the trade sense of the candidate (PCF 9.11.3) |
| Trade Product Classification → BCC-a975ebc6 (outside the tranche) | incorrect (homonym) | homonym: PCF 3.1.1.5 evaluates products for marketing, a different ability the key merged |
| Trade Product Classification → Financial Performance Management | incorrect (homonym) | homonym: PCF 9.1.4.2 evaluates new products financially, a different ability the key merged |

| # | Question (§8) | Draft answer |
|---|---|---|
| 1 | Bearer kind: an Organization? | **Yes**. The work is the organization's: the classifications are the organization's declarations about its own goods |
| 2 | Basis kind: member agents as organized, no artifact counted? | **Yes**. The trade-compliance members who classify the organization's goods under tariff and control lists. The tariff schedules, control lists and the product master are enabling conditions; the work can be done with other tools, so none is constitutive of the type |
| 3 | Through the organization's arrangements? | **Yes**. Realizations run through its division of work and its accounts and records, not one person's skill on their own account |
| 4 | Non-deontic index? | **Yes**. No member grants, alters or withdraws standing or authorization |
| 5 | Exercise, not development (CD5)? | **Yes** |

**Draft recommendation:** PASS.

| Finding (PASS / FAIL) | Reviewer | Date | Notes |
|---|---|---|---|
|  |  |  |  |

### T2-13 — Restricted Party Screening

| Field | Value |
|---|---|
| Candidate | BCC-f6799472, catalog key `verification\|sanctioned party list`; concept `bcoc:RestrictedPartyScreening` |
| Definition | A business capability of an organization to check the parties it would trade with against the lists of sanctioned and restricted parties that apply, before and during its dealings with them, grounded in the organization's members as organized. (checked against CAP-07: no deontic terms) |
| Proposed classification | `bco:BusinessCapability` (CM-01), under `obo:BFO_0000016` (disposition) on a PASS; foundational ancestor `cco:ont00000568` (Organization Capability), as the vocabulary records; bearer `cco:ont00001180` (Organization) |
| Grounding | **Basis:** the trade-compliance members who screen counterparties against the lists, as organized. **Enabling, not basis:** the screening service and the published lists. **Arrangements:** the screening is done before and during the organization's own dealings |

**Realization index** (1):

| Member | Via (PCF) | Genus (BPO) | Evidence |
|---|---|---|---|
| `bpo:P14090` | 9.11.1 Screen sanctioned party list | Act of Appraisal | designating record |

**Taxonomy review** (`docs/catalog/tranche-2-review.yaml`; classified, not validated):

| Link | Disposition | Reason |
|---|---|---|
| Restricted Party Screening → Global Trade Management | retained, `part-of`, kept | PCF hierarchy; the narrower's work is part of the broader's, not a kind of it |

| # | Question (§8) | Draft answer |
|---|---|---|
| 1 | Bearer kind: an Organization? | **Yes**. The work is the organization's: the screening is done before and during the organization's own dealings |
| 2 | Basis kind: member agents as organized, no artifact counted? | **Yes**. The trade-compliance members who screen counterparties against the lists. The screening service and the published lists are enabling conditions; the work can be done with other tools, so none is constitutive of the type |
| 3 | Through the organization's arrangements? | **Yes**. Realizations run through its division of work and its accounts and records, not one person's skill on their own account |
| 4 | Non-deontic index? | **Yes**. No member grants, alters or withdraws standing or authorization |
| 5 | Exercise, not development (CD5)? | **Yes** |

**Draft recommendation:** PASS.

| Finding (PASS / FAIL) | Reviewer | Date | Notes |
|---|---|---|---|
|  |  |  |  |

### T2-14 — Trade and Customs Documentation

| Field | Value |
|---|---|
| Candidate | BCC-c5e7dca0, catalog key `data\|trade`; concept `bcoc:TradeDocumentation` |
| Definition | A business capability of an organization to prepare and keep the records of its cross-border shipments, and give customs authorities the information the law requires of it, grounded in the organization's members as organized. (checked against CAP-07: no deontic terms) |
| Proposed classification | `bco:BusinessCapability` (CM-01), under `obo:BFO_0000016` (disposition) on a PASS; foundational ancestor `cco:ont00000568` (Organization Capability), as the vocabulary records; bearer `cco:ont00001180` (Organization) |
| Grounding | **Basis:** the trade-compliance and logistics members who prepare shipment records and give customs what the law requires, as organized. **Enabling, not basis:** the customs filing systems and the shipment records. **Arrangements:** the declarations are the organization's, for its own shipments |

**Realization index** (4):

| Member | Via (PCF) | Genus (BPO) | Evidence |
|---|---|---|---|
| `bpo:P14095` | 9.11.7 Document trade | Act of Reporting | designating record |
| `bpo:P14094` | 9.11.6 Communicate with customs | Planned Act, Act of Communication | from BCC-6daa0467 (merged) |
| `bpo:P19593` | 9.11.4 Perform currency conversion | Act of Analysis | from BCC-b7928257 (rejected) |
| `bpo:P14093` | 9.11.5 Calculate duty | Act of Accounting | from BCC-46cbe926 (rejected) |

**Taxonomy review** (`docs/catalog/tranche-2-review.yaml`; classified, not validated):

| Link | Disposition | Reason |
|---|---|---|
| Trade and Customs Documentation → Global Trade Management | retained, `part-of`, kept | PCF hierarchy; the narrower's work is part of the broader's, not a kind of it |

| # | Question (§8) | Draft answer |
|---|---|---|
| 1 | Bearer kind: an Organization? | **Yes**. The work is the organization's: the declarations are the organization's, for its own shipments |
| 2 | Basis kind: member agents as organized, no artifact counted? | **Yes**. The trade-compliance and logistics members who prepare shipment records and give customs what the law requires. The customs filing systems and the shipment records are enabling conditions; the work can be done with other tools, so none is constitutive of the type |
| 3 | Through the organization's arrangements? | **Yes**. Realizations run through its division of work and its accounts and records, not one person's skill on their own account |
| 4 | Non-deontic index? | **Yes**. No member grants, alters or withdraws standing or authorization |
| 5 | Exercise, not development (CD5)? | **Yes** |

**Draft recommendation:** PASS.

**Notes for the reviewer:**
- Three members come from candidates merged or rejected into it: communicating with customs (merged), and currency conversion and duty calculation (rejected as single act episodes, their acts kept as this concept's evidence).

| Finding (PASS / FAIL) | Reviewer | Date | Notes |
|---|---|---|---|
|  |  |  |  |

### T2-15 — Trade Preference Management

| Field | Value |
|---|---|
| Candidate | BCC-0c80b752, catalog key `administration\|trade preference`; concept `bcoc:TradePreferenceManagement` |
| Definition | A business capability of an organization to establish that its goods qualify for reduced or zero duty under trade agreements and programs, and claim and document that treatment, grounded in the organization's members as organized. (checked against CAP-07: no deontic terms) |
| Proposed classification | `bco:BusinessCapability` (CM-01), under `obo:BFO_0000016` (disposition) on a PASS; foundational ancestor `cco:ont00000568` (Organization Capability), as the vocabulary records; bearer `cco:ont00001180` (Organization) |
| Grounding | **Basis:** the trade-compliance members who establish origin and qualification, and claim and document the treatment, as organized. **Enabling, not basis:** the origin records and the agreement rules. **Arrangements:** the claims are the organization's, for its own goods |

**Realization index** (1):

| Member | Via (PCF) | Genus (BPO) | Evidence |
|---|---|---|---|
| `bpo:P14096` | 9.11.8 Process trade preferences | Act of Reporting | designating record |

**Taxonomy review** (`docs/catalog/tranche-2-review.yaml`; classified, not validated):

| Link | Disposition | Reason |
|---|---|---|
| Trade Preference Management → Global Trade Management | retained, `part-of`, kept | PCF hierarchy; the narrower's work is part of the broader's, not a kind of it |

| # | Question (§8) | Draft answer |
|---|---|---|
| 1 | Bearer kind: an Organization? | **Yes**. The work is the organization's: the claims are the organization's, for its own goods |
| 2 | Basis kind: member agents as organized, no artifact counted? | **Yes**. The trade-compliance members who establish origin and qualification, and claim and document the treatment. The origin records and the agreement rules are enabling conditions; the work can be done with other tools, so none is constitutive of the type |
| 3 | Through the organization's arrangements? | **Yes**. Realizations run through its division of work and its accounts and records, not one person's skill on their own account |
| 4 | Non-deontic index? | **Yes**. No member grants, alters or withdraws standing or authorization |
| 5 | Exercise, not development (CD5)? | **Yes** |

**Draft recommendation:** PASS.

**Notes for the reviewer:**
- Claiming preferential treatment asserts an entitlement under a trade agreement. The index act prepares and documents the claim, and confers no standing, so the draft answers question 4 yes.

| Finding (PASS / FAIL) | Reviewer | Date | Notes |
|---|---|---|---|
|  |  |  |  |

### T2-16 — Internal Control Reporting

| Field | Value |
|---|---|
| Candidate | BCC-b55668bc, catalog key `reporting\|internal control compliance`; concept `bcoc:InternalControlReporting` |
| Definition | A business capability of an organization to report on the state of its internal controls, and on compliance with them, to those inside and outside it who need to know, grounded in the organization's members as organized. (checked against CAP-07: no deontic terms) |
| Proposed classification | `bco:BusinessCapability` (CM-01), under `obo:BFO_0000016` (disposition) on a PASS; foundational ancestor `cco:ont00000568` (Organization Capability), as the vocabulary records; bearer `cco:ont00001180` (Organization) |
| Grounding | **Basis:** the control and compliance members who report on the controls to management, auditors and outside parties, as organized. **Enabling, not basis:** the control-testing records and the reporting templates. **Arrangements:** the reports are the organization's, issued through its control function |

**Realization index** (5):

| Member | Via (PCF) | Genus (BPO) | Evidence |
|---|---|---|---|
| `bpo:P10764` | 9.8.3 Report on internal controls compliance | Act of Reporting | designating record |
| `bpo:P10923` | 9.8.3.1 Report to external auditors | Act of Communication | process beneath it |
| `bpo:P10924` | 9.8.3.2 Report to regulators, share-/debt-holders, securities exchanges, etc. | Act of Communication | process beneath it |
| `bpo:P10925` | 9.8.3.3 Report to third parties | Act of Communication | process beneath it |
| `bpo:P10926` | 9.8.3.4 Report to internal management | Act of Communication | process beneath it |

**Taxonomy review** (`docs/catalog/tranche-2-review.yaml`; classified, not validated):

| Link | Disposition | Reason |
|---|---|---|
| Internal Control Reporting → Internal Control | retained, `part-of`, kept | PCF hierarchy; the narrower's work is part of the broader's, not a kind of it |

| # | Question (§8) | Draft answer |
|---|---|---|
| 1 | Bearer kind: an Organization? | **Yes**. The work is the organization's: the reports are the organization's, issued through its control function |
| 2 | Basis kind: member agents as organized, no artifact counted? | **Yes**. The control and compliance members who report on the controls to management, auditors and outside parties. The control-testing records and the reporting templates are enabling conditions; the work can be done with other tools, so none is constitutive of the type |
| 3 | Through the organization's arrangements? | **Yes**. Realizations run through its division of work and its accounts and records, not one person's skill on their own account |
| 4 | Non-deontic index? | **Yes**. No member grants, alters or withdraws standing or authorization |
| 5 | Exercise, not development (CD5)? | **Yes** |

**Draft recommendation:** PASS.

| Finding (PASS / FAIL) | Reviewer | Date | Notes |
|---|---|---|---|
|  |  |  |  |

### T2-17 — Internal Control Design

| Field | Value |
|---|---|
| Candidate | BCC-80a63f8e, catalog key `formulation\|internal control policy and procedure`; concept `bcoc:InternalControlDesign` |
| Definition | A business capability of an organization to define the controls, policies and procedures intended to give reasonable assurance that its operations are effective, its financial reporting reliable and its conduct compliant, grounded in the organization's members as organized. (checked against CAP-07: no deontic terms) |
| Proposed classification | `bco:BusinessCapability` (CM-01), under `obo:BFO_0000016` (disposition) on a PASS; foundational ancestor `cco:ont00000568` (Organization Capability), as the vocabulary records; bearer `cco:ont00001180` (Organization) |
| Grounding | **Basis:** the control, risk and finance members who define the controls, policies, objectives and tolerances, as organized. **Enabling, not basis:** the control framework documents. **Arrangements:** the controls are the organization's, defined for its own operations and reporting |

**Realization index** (4):

| Member | Via (PCF) | Genus (BPO) | Evidence |
|---|---|---|---|
| `bpo:P10762` | 9.8.1 Establish internal controls, policies, and procedures | Act of Formulation | designating record |
| `bpo:P10915` | 9.8.1.2 Define and communicate code of ethics | Act of Formulation | process beneath it |
| `bpo:P11250` | 9.8.1.4 Define business process objectives and risks | Act of Formulation | process beneath it |
| `bpo:P11251` | 9.8.1.5 Define entity/unit risk tolerances | Act of Formulation | process beneath it |

**Excluded** (2):

| Act | Via (PCF) | Code | Reason |
|---|---|---|---|
| `bpo:P10914` | 9.8.1.1 Establish board of directors and audit committee | Q5 | establishing a board and an audit committee is organizational establishment, a development act (CAP-06 genus), and changes the basis |
| `bpo:P10916` | 9.8.1.3 Assign roles and responsibility for internal controls | Q4 | assigning roles and responsibility for controls confers responsibility (CAP-07 stems) |

**Taxonomy review** (`docs/catalog/tranche-2-review.yaml`; classified, not validated):

| Link | Disposition | Reason |
|---|---|---|
| Internal Control Design → BCC-41f11e7f (outside the tranche) | incorrect (containment artifact) | containment artifact on 'procedure': designing internal controls defines controls such as segregation of duties, not only procedures, so substitution fails |
| Internal Control Design → Internal Control | retained, `part-of`, kept | PCF hierarchy; the narrower's work is part of the broader's, not a kind of it |

| # | Question (§8) | Draft answer |
|---|---|---|
| 1 | Bearer kind: an Organization? | **Yes**. The work is the organization's: the controls are the organization's, defined for its own operations and reporting |
| 2 | Basis kind: member agents as organized, no artifact counted? | **Yes**. The control, risk and finance members who define the controls, policies, objectives and tolerances. The control framework documents are enabling conditions; the work can be done with other tools, so none is constitutive of the type |
| 3 | Through the organization's arrangements? | **Yes**. Realizations run through its division of work and its accounts and records, not one person's skill on their own account |
| 4 | Non-deontic index? | **Yes, for the reviewer to confirm** (below); excluded as deontic: `P10916` |
| 5 | Exercise, not development (CD5)? | **Yes**; excluded: `P10914` |

**Draft recommendation:** PASS, with question 4 for the reviewer.

**Notes for the reviewer:**
- Question 4, as for Accounting Policy Management: the draft holds that defining a control or a code of ethics is describable without standing, and that adopting it is separate. The reviewer decides.

| Finding (PASS / FAIL) | Reviewer | Date | Notes |
|---|---|---|---|
|  |  |  |  |

### T2-18 — International Rate Monitoring

| Field | Value |
|---|---|
| Candidate | BCC-5dfa2101, catalog key `monitoring\|international rate`; concept `bcoc:InternationalRateMonitoring` |
| Definition | A business capability of an organization to follow the exchange and interest rates in the markets where it operates and bring them to those who manage its international funds, grounded in the organization's members as organized. (checked against CAP-07: no deontic terms) |
| Proposed classification | `bco:BusinessCapability` (CM-01), under `obo:BFO_0000016` (disposition) on a PASS; foundational ancestor `cco:ont00000568` (Organization Capability), as the vocabulary records; bearer `cco:ont00001180` (Organization) |
| Grounding | **Basis:** the treasury members who follow exchange and interest rates and pass them on, as organized. **Enabling, not basis:** the market-data feeds. **Arrangements:** the rates are gathered for the organization's own international funds management |

**Realization index** (1):

| Member | Via (PCF) | Genus (BPO) | Evidence |
|---|---|---|---|
| `bpo:P10767` | 9.10.1 Monitor international rates | Act of Monitoring | designating record |

**Taxonomy review** (`docs/catalog/tranche-2-review.yaml`; classified, not validated):

| Link | Disposition | Reason |
|---|---|---|
| International Rate Monitoring → International Funds Management | retained, `part-of`, kept | PCF hierarchy; the narrower's work is part of the broader's, not a kind of it |

| # | Question (§8) | Draft answer |
|---|---|---|
| 1 | Bearer kind: an Organization? | **Yes**. The work is the organization's: the rates are gathered for the organization's own international funds management |
| 2 | Basis kind: member agents as organized, no artifact counted? | **Yes**. The treasury members who follow exchange and interest rates and pass them on. The market-data feeds are enabling conditions; the work can be done with other tools, so none is constitutive of the type |
| 3 | Through the organization's arrangements? | **Yes**. Realizations run through its division of work and its accounts and records, not one person's skill on their own account |
| 4 | Non-deontic index? | **Yes**. No member grants, alters or withdraws standing or authorization |
| 5 | Exercise, not development (CD5)? | **Yes** |

**Draft recommendation:** PASS.

| Finding (PASS / FAIL) | Reviewer | Date | Notes |
|---|---|---|---|
|  |  |  |  |

### T2-19 — Cross-Border Funds Transfer Management

| Field | Value |
|---|---|
| Candidate | BCC-bf62316a, catalog key `management\|transaction`; concept `bcoc:CrossBorderFundsTransferManagement` |
| Definition | A business capability of an organization to move money across borders for its trade and investments, converting between currencies and choosing the means of payment, grounded in the organization's members as organized. (checked against CAP-07: no deontic terms) |
| Proposed classification | `bco:BusinessCapability` (CM-01), under `obo:BFO_0000016` (disposition) on a PASS; foundational ancestor `cco:ont00000568` (Organization Capability), as the vocabulary records; bearer `cco:ont00001180` (Organization) |
| Grounding | **Basis:** the treasury members who move money across borders and choose the means of payment, as organized. **Enabling, not basis:** the banks' payment networks. **Arrangements:** the transfers are made from the organization's accounts, for its own trade and investments |

**Realization index** (1):

| Member | Via (PCF) | Genus (BPO) | Evidence |
|---|---|---|---|
| `bpo:P10768` | 9.10.2 Manage transactions | Act of Financial Transaction | designating record |

**Taxonomy review** (`docs/catalog/tranche-2-review.yaml`; classified, not validated):

| Link | Disposition | Reason |
|---|---|---|
| Cross-Border Funds Transfer Management → International Funds Management | retained, `part-of`, kept | PCF hierarchy; the narrower's work is part of the broader's, not a kind of it |

| # | Question (§8) | Draft answer |
|---|---|---|
| 1 | Bearer kind: an Organization? | **Yes**. The work is the organization's: the transfers are made from the organization's accounts, for its own trade and investments |
| 2 | Basis kind: member agents as organized, no artifact counted? | **Yes**. The treasury members who move money across borders and choose the means of payment. The banks' payment networks are enabling conditions; the work can be done with other tools, so none is constitutive of the type |
| 3 | Through the organization's arrangements? | **Yes**. Realizations run through its division of work and its accounts and records, not one person's skill on their own account |
| 4 | Non-deontic index? | **Yes**. No member grants, alters or withdraws standing or authorization |
| 5 | Exercise, not development (CD5)? | **Yes** |

**Draft recommendation:** PASS.

| Finding (PASS / FAIL) | Reviewer | Date | Notes |
|---|---|---|---|
|  |  |  |  |

### T2-20 — Pay Management

| Field | Value |
|---|---|
| Candidate | BCC-d105ff07, catalog key `management\|pay`; concept `bcoc:PayManagement` |
| Definition | A business capability of an organization to determine the gross pay each employee is owed for a period, bonuses and other compensation included, and carry it through to payment, grounded in the organization's members as organized. (checked against CAP-07: no deontic terms) |
| Proposed classification | `bco:BusinessCapability` (CM-01), under `obo:BFO_0000016` (disposition) on a PASS; foundational ancestor `cco:ont00000568` (Organization Capability), as the vocabulary records; bearer `cco:ont00001180` (Organization) |
| Grounding | **Basis:** the payroll members who keep earnings data and compute and pay gross pay, as organized. **Enabling, not basis:** the payroll system and the bank interfaces. **Arrangements:** pay is owed by the organization and paid from its accounts, as in T1-02 |

**Realization index** (9):

| Member | Via (PCF) | Genus (BPO) | Evidence |
|---|---|---|---|
| `bpo:P10754` | 9.5.2 Manage pay | Act of Financial Transaction | designating record |
| `bpo:P10858` | 9.5.2.1 Enter employee time worked into payroll system | Act of Information Processing | process beneath it |
| `bpo:P10859` | 9.5.2.2 Maintain and administer employee earnings information | Act of Accounting | process beneath it |
| `bpo:P10860` | 9.5.2.3 Maintain and administer applicable deductions | Act of Accounting | process beneath it |
| `bpo:P10861` | 9.5.2.4 Monitor changes in tax status of employees | Act of Monitoring | process beneath it |
| `bpo:P10862` | 9.5.2.5 Process and distribute payments | Act of Remuneration | process beneath it |
| `bpo:P10863` | 9.5.2.6 Process and distribute manual checks | Act of Financial Transaction | process beneath it |
| `bpo:P10864` | 9.5.2.7 Process period-end adjustments | Act of Accounting | process beneath it |
| `bpo:P10865` | 9.5.2.8 Respond to employee payroll inquiries | Act of Information Processing | process beneath it |

**Taxonomy review** (`docs/catalog/tranche-2-review.yaml`; classified, not validated):

| Link | Disposition | Reason |
|---|---|---|
| Payment Processing → Pay Management | retained, `part-of`, kept | tranche 1 §5: a component of T1-02's pay management, not a subtype |
| Pay Management → Payroll Processing | retained, `part-of`, kept | tranche 1 §5: a component (CD16), not a subtype |

| # | Question (§8) | Draft answer |
|---|---|---|
| 1 | Bearer kind: an Organization? | **Yes**. The work is the organization's: pay is owed by the organization and paid from its accounts, as in T1-02 |
| 2 | Basis kind: member agents as organized, no artifact counted? | **Yes**. The payroll members who keep earnings data and compute and pay gross pay. The payroll system and the bank interfaces are enabling conditions; the work can be done with other tools, so none is constitutive of the type |
| 3 | Through the organization's arrangements? | **Yes**. Realizations run through its division of work and its accounts and records, not one person's skill on their own account |
| 4 | Non-deontic index? | **Yes**. No member grants, alters or withdraws standing or authorization |
| 5 | Exercise, not development (CD5)? | **Yes** |

**Draft recommendation:** PASS.

**Notes for the reviewer:**
- All nine members are in T1-02's signed index already. Pay Management is a part-of component of Payroll Processing, so the overlap is expected.

| Finding (PASS / FAIL) | Reviewer | Date | Notes |
|---|---|---|---|
|  |  |  |  |

### T2-21 — Payroll Tax Processing

| Field | Value |
|---|---|
| Candidate | BCC-394909c1, catalog key `management\|payroll tax`; concept `bcoc:PayrollTaxProcessing` |
| Definition | A business capability of an organization to calculate, withhold, remit and report the taxes due on its employees' pay, and reconcile what it remitted with what was due, grounded in the organization's members as organized. (checked against CAP-07: no deontic terms) |
| Proposed classification | `bco:BusinessCapability` (CM-01), under `obo:BFO_0000016` (disposition) on a PASS; foundational ancestor `cco:ont00000568` (Organization Capability), as the vocabulary records; bearer `cco:ont00001180` (Organization) |
| Grounding | **Basis:** the payroll and tax members who calculate, withhold, remit and report payroll taxes, as organized. **Enabling, not basis:** the payroll system and the tax tables. **Arrangements:** the taxes are the organization's obligations as employer, met from its accounts |

**Realization index** (4):

| Member | Via (PCF) | Genus (BPO) | Evidence |
|---|---|---|---|
| `bpo:P10755` | 9.5.3 Manage and process payroll taxes | Act of Financial Transaction | designating record |
| `bpo:P10866` | 9.5.3.3 Calculate and pay applicable payroll taxes | Act of Financial Transaction | process beneath it |
| `bpo:P10867` | 9.5.3.4 Produce and distribute employee annual tax statements | Act of Reporting | process beneath it |
| `bpo:P10868` | 9.5.3.5 File regulatory payroll tax forms | Act of Reporting | process beneath it |

**Excluded** (1):

| Act | Via (PCF) | Code | Reason |
|---|---|---|---|
| `bpo:P14075` | 9.5.3.1 Develop tax plan | OTHER | developing a tax plan is Tax Planning's work, excluded from T1-02 for the same reason |

**Taxonomy review** (`docs/catalog/tranche-2-review.yaml`; classified, not validated):

| Link | Disposition | Reason |
|---|---|---|
| Payroll Tax Processing → Tax Management | retained, `part-of`, kept | the organization's tax work covers payroll taxes; component, not specialization, so that payroll tax operations stay distinct from tax planning and from general tax processing (decision of 2026-11-04, act 3) |
| Payroll Tax Processing → Payroll Processing | retained, `part-of`, kept | tranche 1 §5: a component (CD16), not a subtype |

| # | Question (§8) | Draft answer |
|---|---|---|
| 1 | Bearer kind: an Organization? | **Yes**. The work is the organization's: the taxes are the organization's obligations as employer, met from its accounts |
| 2 | Basis kind: member agents as organized, no artifact counted? | **Yes**. The payroll and tax members who calculate, withhold, remit and report payroll taxes. The payroll system and the tax tables are enabling conditions; the work can be done with other tools, so none is constitutive of the type |
| 3 | Through the organization's arrangements? | **Yes**. Realizations run through its division of work and its accounts and records, not one person's skill on their own account |
| 4 | Non-deontic index? | **Yes**. No member grants, alters or withdraws standing or authorization |
| 5 | Exercise, not development (CD5)? | **Yes** |

**Draft recommendation:** PASS.

| Finding (PASS / FAIL) | Reviewer | Date | Notes |
|---|---|---|---|
|  |  |  |  |

### T2-22 — Time Reporting

| Field | Value |
|---|---|
| Candidate | BCC-85fbcb90, catalog key `reporting\|time`; concept `bcoc:TimeReporting` |
| Definition | A business capability of an organization to record, by period, the time its members work, are absent or bill, and make that record available to those who pay, bill or plan with it, grounded in the organization's members as organized. (checked against CAP-07: no deontic terms) |
| Proposed classification | `bco:BusinessCapability` (CM-01), under `obo:BFO_0000016` (disposition) on a PASS; foundational ancestor `cco:ont00000568` (Organization Capability), as the vocabulary records; bearer `cco:ont00001180` (Organization) |
| Grounding | **Basis:** the members who record time and the supervisors and HR members who review and report it, as organized. **Enabling, not basis:** the time-recording system. **Arrangements:** the record is the organization's, kept for its pay, billing and planning |

**Realization index** (5):

| Member | Via (PCF) | Genus (BPO) | Evidence |
|---|---|---|---|
| `bpo:P10753` | 9.5.1 Report time | Act of Information Processing | designating record |
| `bpo:P10854` | 9.5.1.2 Collect and record employee time worked | Act of Information Processing | process beneath it |
| `bpo:P10855` | 9.5.1.3 Analyze and report paid and unpaid leave | Act of Analysis | process beneath it |
| `bpo:P10856` | 9.5.1.4 Monitor regular, overtime, and other hours | Act of Monitoring | process beneath it |
| `bpo:P10857` | 9.5.1.5 Analyze and report employee utilization | Act of Analysis | process beneath it |

**Excluded** (1):

| Act | Via (PCF) | Code | Reason |
|---|---|---|---|
| `bpo:P10853` | 9.5.1.1 Establish policies and procedures | Q5 | establishing time-reporting policies and procedures: setting the policies that govern this capability's own practice shapes the capability rather than exercising it (tranche-1 practice, T1-02 question 5) |

**Taxonomy review** (`docs/catalog/tranche-2-review.yaml`; classified, not validated):

| Link | Disposition | Reason |
|---|---|---|
| Time Reporting → Payroll Processing | incorrect (dependency) | dependency: payroll uses recorded time, but time reporting is a separate capability (tranche 1 §5; BRM separates them) |

| # | Question (§8) | Draft answer |
|---|---|---|
| 1 | Bearer kind: an Organization? | **Yes**. The work is the organization's: the record is the organization's, kept for its pay, billing and planning |
| 2 | Basis kind: member agents as organized, no artifact counted? | **Yes**. The members who record time and the supervisors and HR members who review and report it. The time-recording system are enabling conditions; the work can be done with other tools, so none is constitutive of the type |
| 3 | Through the organization's arrangements? | **Yes**. Realizations run through its division of work and its accounts and records, not one person's skill on their own account |
| 4 | Non-deontic index? | **Yes**. No member grants, alters or withdraws standing or authorization |
| 5 | Exercise, not development (CD5)? | **Yes**; excluded: `P10853` |

**Draft recommendation:** PASS.

**Notes for the reviewer:**
- It has no broader concept after the tranche-1 dependency finding. Its parent is in workforce management (PCF 7.x), not yet curated. G1-T does not need a broader.

| Finding (PASS / FAIL) | Reviewer | Date | Notes |
|---|---|---|---|
|  |  |  |  |

### T2-23 — Cost Accounting

| Field | Value |
|---|---|
| Candidate | BCC-302a390a, catalog key `accounting\|cost`; concept `bcoc:CostAccounting` |
| Definition | A business capability of an organization to determine what its products, services, processes and projects cost, by recording, allocating and analyzing their costs, grounded in the organization's members as organized. (checked against CAP-07: no deontic terms) |
| Proposed classification | `bco:BusinessCapability` (CM-01), under `obo:BFO_0000016` (disposition) on a PASS; foundational ancestor `cco:ont00000568` (Organization Capability), as the vocabulary records; bearer `cco:ont00001180` (Organization) |
| Grounding | **Basis:** the cost accountants who record, allocate and analyze costs, as organized. **Enabling, not basis:** the costing system and the ledger. **Arrangements:** the costs are the organization's, accounted for by its costing method |

**Realization index** (6):

| Member | Via (PCF) | Genus (BPO) | Evidence |
|---|---|---|---|
| `bpo:P10739` | 9.1.2 Perform cost accounting and control | Act of Accounting | designating record |
| `bpo:P10774` | 9.1.2.1 Perform inventory accounting | Act of Accounting | process beneath it |
| `bpo:P14057` | 9.1.2.2 Perform profit center accounting | Act of Accounting | process beneath it |
| `bpo:P10775` | 9.1.2.3 Perform cost of sales analysis | Act of Analysis | process beneath it |
| `bpo:P10776` | 9.1.2.4 Perform product costing | Act of Analysis | process beneath it |
| `bpo:P10777` | 9.1.2.5 Perform variance analysis | Act of Analysis | process beneath it |

**Excluded** (1):

| Act | Via (PCF) | Code | Reason |
|---|---|---|---|
| `bpo:P11175` | 9.1.2.6 Report on profitability | OTHER | reporting on profitability is Financial Performance Management's work |

**Taxonomy review** (`docs/catalog/tranche-2-review.yaml`; classified, not validated):

| Link | Disposition | Reason |
|---|---|---|
| Cost Accounting → Financial Planning and Management Accounting | retained, `part-of`, kept | PCF hierarchy; the narrower's work is part of the broader's, not a kind of it |

| # | Question (§8) | Draft answer |
|---|---|---|
| 1 | Bearer kind: an Organization? | **Yes**. The work is the organization's: the costs are the organization's, accounted for by its costing method |
| 2 | Basis kind: member agents as organized, no artifact counted? | **Yes**. The cost accountants who record, allocate and analyze costs. The costing system and the ledger are enabling conditions; the work can be done with other tools, so none is constitutive of the type |
| 3 | Through the organization's arrangements? | **Yes**. Realizations run through its division of work and its accounts and records, not one person's skill on their own account |
| 4 | Non-deontic index? | **Yes**. No member grants, alters or withdraws standing or authorization |
| 5 | Exercise, not development (CD5)? | **Yes** |

**Draft recommendation:** PASS.

| Finding (PASS / FAIL) | Reviewer | Date | Notes |
|---|---|---|---|
|  |  |  |  |

### T2-24 — Cost Management

| Field | Value |
|---|---|
| Candidate | BCC-b47b8fed, catalog key `management\|cost`; concept `bcoc:CostManagement` |
| Definition | A business capability of an organization to plan and control what it spends, deciding which costs to avoid or reduce in view of what it earns, grounded in the organization's members as organized. (checked against CAP-07: no deontic terms) |
| Proposed classification | `bco:BusinessCapability` (CM-01), under `obo:BFO_0000016` (disposition) on a PASS; foundational ancestor `cco:ont00000568` (Organization Capability), as the vocabulary records; bearer `cco:ont00001180` (Organization) |
| Grounding | **Basis:** the finance and operations members who plan and control spending against cost drivers, as organized. **Enabling, not basis:** the cost models and the budget. **Arrangements:** the decisions on costs are the organization's, made through its planning and control cycle |

**Realization index** (4):

| Member | Via (PCF) | Genus (BPO) | Evidence |
|---|---|---|---|
| `bpo:P10740` | 9.1.3 Perform cost management | Planned Act | designating record |
| `bpo:P10778` | 9.1.3.1 Determine key cost drivers | Act of Identification (discernment sense) | process beneath it |
| `bpo:P10779` | 9.1.3.2 Measure cost drivers | Planned Act, Act of Measuring | process beneath it |
| `bpo:P10780` | 9.1.3.3 Determine critical activities | Act of Identification (discernment sense) | process beneath it |

**Excluded** (1):

| Act | Via (PCF) | Code | Reason |
|---|---|---|---|
| `bpo:P10781` | 9.1.3.4 Manage asset resource deployment and utilization | OTHER | managing the deployment and use of assets is asset management's work (PCF 10.0), not cost management |

**Taxonomy review** (`docs/catalog/tranche-2-review.yaml`; classified, not validated):

| Link | Disposition | Reason |
|---|---|---|
| Continuous Cost Improvement → Cost Management (proposed: → Financial Performance Management) | retained, `kind-of`, retargeted | continuous cost improvement is cost management done as a standing practice (manner restricted); PCF places it under financial performance |
| Cost Management → Financial Planning and Management Accounting | retained, `part-of`, kept | PCF hierarchy; the narrower's work is part of the broader's, not a kind of it |

| # | Question (§8) | Draft answer |
|---|---|---|
| 1 | Bearer kind: an Organization? | **Yes**. The work is the organization's: the decisions on costs are the organization's, made through its planning and control cycle |
| 2 | Basis kind: member agents as organized, no artifact counted? | **Yes**. The finance and operations members who plan and control spending against cost drivers. The cost models and the budget are enabling conditions; the work can be done with other tools, so none is constitutive of the type |
| 3 | Through the organization's arrangements? | **Yes**. Realizations run through its division of work and its accounts and records, not one person's skill on their own account |
| 4 | Non-deontic index? | **Yes**. No member grants, alters or withdraws standing or authorization |
| 5 | Exercise, not development (CD5)? | **Yes** |

**Draft recommendation:** PASS.

| Finding (PASS / FAIL) | Reviewer | Date | Notes |
|---|---|---|---|
|  |  |  |  |

### T2-25 — Financial Performance Management

| Field | Value |
|---|---|
| Candidate | BCC-cedf0899, catalog key `analysis\|financial performance`; concept `bcoc:FinancialPerformanceManagement` |
| Definition | A business capability of an organization to assess the profitability and financial performance of the organization and of its units, products, customers and projects against its targets, and act on the results, grounded in the organization's members as organized. (checked against CAP-07: no deontic terms) |
| Proposed classification | `bco:BusinessCapability` (CM-01), under `obo:BFO_0000016` (disposition) on a PASS; foundational ancestor `cco:ont00000568` (Organization Capability), as the vocabulary records; bearer `cco:ont00001180` (Organization) |
| Grounding | **Basis:** the financial-analysis members who assess profitability and performance and act on the results, as organized. **Enabling, not basis:** the management-reporting and analytics tools. **Arrangements:** the assessment is of the organization and its units, against its own targets |

**Realization index** (7):

| Member | Via (PCF) | Genus (BPO) | Evidence |
|---|---|---|---|
| `bpo:P10741` | 9.1.4 Evaluate and manage financial performance | Planned Act | designating record |
| `bpo:P10782` | 9.1.4.1 Assess customer and product profitability | Act of Appraisal | process beneath it |
| `bpo:P10783` | 9.1.4.2 Evaluate new products | Act of Appraisal | process beneath it |
| `bpo:P10784` | 9.1.4.3 Perform life cycle costing | Act of Analysis | process beneath it |
| `bpo:P10785` | 9.1.4.4 Optimize customer and product mix | Act of Selection | process beneath it |
| `bpo:P10786` | 9.1.4.5 Track performance of new-customer and product strategies | Act of Monitoring | process beneath it |
| `bpo:P10787` | 9.1.4.6 Prepare activity-based performance measures | Act of Analysis | process beneath it |

**Excluded** (1):

| Act | Via (PCF) | Code | Reason |
|---|---|---|---|
| `bpo:P10788` | 9.1.4.7 Manage continuous cost improvement | CAP-03 | typed under Organization Capability, not an act |

**Taxonomy review** (`docs/catalog/tranche-2-review.yaml`; classified, not validated):

| Link | Disposition | Reason |
|---|---|---|
| Continuous Cost Improvement → Cost Management (proposed: → Financial Performance Management) | retained, `kind-of`, retargeted | continuous cost improvement is cost management done as a standing practice (manner restricted); PCF places it under financial performance |
| Financial Performance Management → BCC-4b2ce5d3 (outside the tranche) | incorrect (containment artifact) | containment artifact: the shared word 'performance'; benchmarking is not broader than financial performance management |
| Financial Performance Management → Financial Planning and Management Accounting | retained, `part-of`, kept | PCF hierarchy; the narrower's work is part of the broader's, not a kind of it |
| Trade Product Classification → Financial Performance Management | incorrect (homonym) | homonym: PCF 9.1.4.2 evaluates new products financially, a different ability the key merged |

| # | Question (§8) | Draft answer |
|---|---|---|
| 1 | Bearer kind: an Organization? | **Yes**. The work is the organization's: the assessment is of the organization and its units, against its own targets |
| 2 | Basis kind: member agents as organized, no artifact counted? | **Yes**. The financial-analysis members who assess profitability and performance and act on the results. The management-reporting and analytics tools are enabling conditions; the work can be done with other tools, so none is constitutive of the type |
| 3 | Through the organization's arrangements? | **Yes**. Realizations run through its division of work and its accounts and records, not one person's skill on their own account |
| 4 | Non-deontic index? | **Yes**. No member grants, alters or withdraws standing or authorization |
| 5 | Exercise, not development (CD5)? | **Yes** |

**Draft recommendation:** PASS.

**Notes for the reviewer:**
- P10783 (evaluating new products) is in this index, where the review placed it. The same record is a homonym for Trade Product Classification and is excluded there.

| Finding (PASS / FAIL) | Reviewer | Date | Notes |
|---|---|---|---|
|  |  |  |  |

### T2-26 — Financial Planning, Budgeting and Forecasting

| Field | Value |
|---|---|
| Candidate | BCC-87e1811c, catalog key `planning\|planning, budgeting and forecasting`; concept `bcoc:FinancialPlanningBudgetingAndForecasting` |
| Definition | A business capability of an organization to set its financial goals for future periods, allocate resources to its parts and periods through budgets, and forecast its financial results and position as conditions change, grounded in the organization's members as organized. (checked against CAP-07: no deontic terms) |
| Proposed classification | `bco:BusinessCapability` (CM-01), under `obo:BFO_0000016` (disposition) on a PASS; foundational ancestor `cco:ont00000568` (Organization Capability), as the vocabulary records; bearer `cco:ont00001180` (Organization) |
| Grounding | **Basis:** the planning and analysis members who set financial goals, prepare budgets and forecasts, and analyze variances, as organized. **Enabling, not basis:** the planning models and the budgeting system. **Arrangements:** the plans and budgets are the organization's, prepared through its planning cycle |

**Realization index** (4):

| Member | Via (PCF) | Genus (BPO) | Evidence |
|---|---|---|---|
| `bpo:P10738` | 9.1.1 Perform planning/budgeting/forecasting | Act of Formulation | designating record |
| `bpo:P10772` | 9.1.1.2 Prepare periodic budgets and plans | Act of Formulation | process beneath it |
| `bpo:P10773` | 9.1.1.4 Prepare periodic financial forecasts | Act of Prediction | process beneath it |
| `bpo:P20136` | 9.1.1.5 Perform variance analysis against forecasts and budgets | Act of Analysis | process beneath it |

**Excluded** (2):

| Act | Via (PCF) | Code | Reason |
|---|---|---|---|
| `bpo:P10771` | 9.1.1.1 Develop and maintain budget policies and procedures | Q5 | developing and maintaining budget policies and procedures: setting the policies that govern this capability's own practice shapes the capability rather than exercising it (tranche-1 practice, T1-02 question 5) |
| `bpo:P20135` | 9.1.1.3 Operationalize and implement plans to achieve budget | OTHER | carrying out the plans to achieve the budget is the operating work of every part of the organization, not planning |

**Taxonomy review** (`docs/catalog/tranche-2-review.yaml`; classified, not validated):

| Link | Disposition | Reason |
|---|---|---|
| Financial Planning, Budgeting and Forecasting → Financial Planning and Management Accounting | retained, `part-of`, kept | PCF hierarchy; the narrower's work is part of the broader's, not a kind of it |

| # | Question (§8) | Draft answer |
|---|---|---|
| 1 | Bearer kind: an Organization? | **Yes**. The work is the organization's: the plans and budgets are the organization's, prepared through its planning cycle |
| 2 | Basis kind: member agents as organized, no artifact counted? | **Yes**. The planning and analysis members who set financial goals, prepare budgets and forecasts, and analyze variances. The planning models and the budgeting system are enabling conditions; the work can be done with other tools, so none is constitutive of the type |
| 3 | Through the organization's arrangements? | **Yes**. Realizations run through its division of work and its accounts and records, not one person's skill on their own account |
| 4 | Non-deontic index? | **Yes**. No member grants, alters or withdraws standing or authorization |
| 5 | Exercise, not development (CD5)? | **Yes**; excluded: `P10771` |

**Draft recommendation:** PASS.

| Finding (PASS / FAIL) | Reviewer | Date | Notes |
|---|---|---|---|
|  |  |  |  |

### T2-27 — Revenue and Receivables Management

| Field | Value |
|---|---|
| Candidate | BCC-1cccc689, catalog key `accounting\|revenue`; concept `bcoc:RevenueAndReceivablesManagement` |
| Definition | A business capability of an organization to recognize the revenue it earns, and extend credit to, invoice, record and collect what its customers owe it, grounded in the organization's members as organized. (checked against CAP-07: no deontic terms) |
| Proposed classification | `bco:BusinessCapability` (CM-01), under `obo:BFO_0000016` (disposition) on a PASS; foundational ancestor `cco:ont00000568` (Organization Capability), as the vocabulary records; bearer `cco:ont00001180` (Organization) |
| Grounding | **Basis:** the revenue-accounting, credit, billing and collections members, as organized. **Enabling, not basis:** the billing system and the receivables ledger. **Arrangements:** the revenue and receivables are the organization's, recognized and collected under its policies |

**Realization index** (1):

| Member | Via (PCF) | Genus (BPO) | Evidence |
|---|---|---|---|
| `bpo:P10729` | 9.2 Perform revenue accounting | Act of Accounting | designating record |

**Taxonomy review** (`docs/catalog/tranche-2-review.yaml`; classified, not validated):

| Link | Disposition | Reason |
|---|---|---|
| Revenue and Receivables Management → Financial Resource Management | retained, `part-of`, kept | PCF hierarchy; the narrower's work is part of the broader's, not a kind of it |
| Accounts Receivable Processing → Revenue and Receivables Management | retained, `part-of`, kept | PCF hierarchy; the narrower's work is part of the broader's, not a kind of it |
| Customer Invoicing → Revenue and Receivables Management | retained, `part-of`, kept | PCF hierarchy; the narrower's work is part of the broader's, not a kind of it |
| Customer Credit Management → Revenue and Receivables Management | retained, `part-of`, kept | PCF hierarchy; the narrower's work is part of the broader's, not a kind of it |
| Collections Management → Revenue and Receivables Management | retained, `part-of`, kept | PCF hierarchy; the narrower's work is part of the broader's, not a kind of it |
| Customer Deduction and Adjustment Management → Revenue and Receivables Management | retained, `part-of`, kept | PCF hierarchy; the narrower's work is part of the broader's, not a kind of it |

| # | Question (§8) | Draft answer |
|---|---|---|
| 1 | Bearer kind: an Organization? | **Yes**. The work is the organization's: the revenue and receivables are the organization's, recognized and collected under its policies |
| 2 | Basis kind: member agents as organized, no artifact counted? | **Yes**. The revenue-accounting, credit, billing and collections members. The billing system and the receivables ledger are enabling conditions; the work can be done with other tools, so none is constitutive of the type |
| 3 | Through the organization's arrangements? | **Yes**. Realizations run through its division of work and its accounts and records, not one person's skill on their own account |
| 4 | Non-deontic index? | **Yes**. No member grants, alters or withdraws standing or authorization |
| 5 | Exercise, not development (CD5)? | **Yes** |

**Draft recommendation:** PASS, or treat as a capability area.

**Notes for the reviewer:**
- The index is the one summary act PCF 9.2. The definition joins recognition, credit, invoicing, recording and collection. The reviewer may prefer to treat it as a capability area (CD16, E4), as for Financial Accounting.

| Finding (PASS / FAIL) | Reviewer | Date | Notes |
|---|---|---|---|
|  |  |  |  |

### T2-28 — Accounts Receivable Processing

| Field | Value |
|---|---|
| Candidate | BCC-6587dedf, catalog key `administration\|account receivable`; concept `bcoc:AccountsReceivableProcessing` |
| Definition | A business capability of an organization to record what its customers owe it, apply the payments they make, and keep each customer's account correct and current, grounded in the organization's members as organized. (checked against CAP-07: no deontic terms) |
| Proposed classification | `bco:BusinessCapability` (CM-01), under `obo:BFO_0000016` (disposition) on a PASS; foundational ancestor `cco:ont00000568` (Organization Capability), as the vocabulary records; bearer `cco:ont00001180` (Organization) |
| Grounding | **Basis:** the receivables members who record amounts owed, apply payments and keep accounts current, as organized. **Enabling, not basis:** the receivables ledger and the bank lockbox or payment feeds. **Arrangements:** the receivables are the organization's, kept in its books |

**Realization index** (5):

| Member | Via (PCF) | Genus (BPO) | Evidence |
|---|---|---|---|
| `bpo:P10744` | 9.2.3 Process accounts receivable (AR) | Act of Accounting | designating record |
| `bpo:P10800` | 9.2.3.2 Receive/Deposit customer payments | Act of Financial Transaction | process beneath it |
| `bpo:P10801` | 9.2.3.3 Apply cash remittances | Act of Financial Transaction | process beneath it |
| `bpo:P10802` | 9.2.3.4 Prepare AR reports | Act of Reporting | process beneath it |
| `bpo:P10803` | 9.2.3.5 Post AR activity to the general ledger | Act of Accounting | process beneath it |

**Excluded** (1):

| Act | Via (PCF) | Code | Reason |
|---|---|---|---|
| `bpo:P10799` | 9.2.3.1 Establish AR policies | Q5 | establishing receivables policies: setting the policies that govern this capability's own practice shapes the capability rather than exercising it (tranche-1 practice, T1-02 question 5) |

**Taxonomy review** (`docs/catalog/tranche-2-review.yaml`; classified, not validated):

| Link | Disposition | Reason |
|---|---|---|
| Accounts Receivable Processing → Revenue and Receivables Management | retained, `part-of`, kept | PCF hierarchy; the narrower's work is part of the broader's, not a kind of it |

| # | Question (§8) | Draft answer |
|---|---|---|
| 1 | Bearer kind: an Organization? | **Yes**. The work is the organization's: the receivables are the organization's, kept in its books |
| 2 | Basis kind: member agents as organized, no artifact counted? | **Yes**. The receivables members who record amounts owed, apply payments and keep accounts current. The receivables ledger and the bank lockbox or payment feeds are enabling conditions; the work can be done with other tools, so none is constitutive of the type |
| 3 | Through the organization's arrangements? | **Yes**. Realizations run through its division of work and its accounts and records, not one person's skill on their own account |
| 4 | Non-deontic index? | **Yes**. No member grants, alters or withdraws standing or authorization |
| 5 | Exercise, not development (CD5)? | **Yes**; excluded: `P10799` |

**Draft recommendation:** PASS.

| Finding (PASS / FAIL) | Reviewer | Date | Notes |
|---|---|---|---|
|  |  |  |  |

### T2-29 — Customer Deduction and Adjustment Management

| Field | Value |
|---|---|
| Candidate | BCC-cebf0da8, catalog key `management\|adjustment and deduction`; concept `bcoc:CustomerDeductionManagement` |
| Definition | A business capability of an organization to investigate, resolve and record the deductions its customers take from their payments and the adjustments made to their accounts, grounded in the organization's members as organized. (checked against CAP-07: no deontic terms) |
| Proposed classification | `bco:BusinessCapability` (CM-01), under `obo:BFO_0000016` (disposition) on a PASS; foundational ancestor `cco:ont00000568` (Organization Capability), as the vocabulary records; bearer `cco:ont00001180` (Organization) |
| Grounding | **Basis:** the receivables and deductions members who investigate, resolve and record customer deductions, as organized. **Enabling, not basis:** the deduction-tracking and receivables systems. **Arrangements:** the deductions are taken from payments owed to the organization, and settled in its books |

**Realization index** (6):

| Member | Via (PCF) | Genus (BPO) | Evidence |
|---|---|---|---|
| `bpo:P10746` | 9.2.5 Manage and process adjustments/deductions | Act of Accounting | designating record |
| `bpo:P10810` | 9.2.5.2 Analyze adjustments | Act of Analysis | process beneath it |
| `bpo:P10811` | 9.2.5.3 Correspond/Negotiate with customer | Act of Formulation | process beneath it |
| `bpo:P10812` | 9.2.5.4 Discuss resolution with internal parties | Act of Formulation | process beneath it |
| `bpo:P10813` | 9.2.5.5 Prepare chargeback invoices | Act of Accounting | process beneath it |
| `bpo:P10814` | 9.2.5.6 Process related entries | Act of Accounting | process beneath it |

**Excluded** (1):

| Act | Via (PCF) | Code | Reason |
|---|---|---|---|
| `bpo:P10809` | 9.2.5.1 Establish policies/procedures for adjustments | Q5 | establishing adjustment policies and procedures: setting the policies that govern this capability's own practice shapes the capability rather than exercising it (tranche-1 practice, T1-02 question 5) |

**Taxonomy review** (`docs/catalog/tranche-2-review.yaml`; classified, not validated):

| Link | Disposition | Reason |
|---|---|---|
| Customer Deduction and Adjustment Management → Revenue and Receivables Management | retained, `part-of`, kept | PCF hierarchy; the narrower's work is part of the broader's, not a kind of it |

| # | Question (§8) | Draft answer |
|---|---|---|
| 1 | Bearer kind: an Organization? | **Yes**. The work is the organization's: the deductions are taken from payments owed to the organization, and settled in its books |
| 2 | Basis kind: member agents as organized, no artifact counted? | **Yes**. The receivables and deductions members who investigate, resolve and record customer deductions. The deduction-tracking and receivables systems are enabling conditions; the work can be done with other tools, so none is constitutive of the type |
| 3 | Through the organization's arrangements? | **Yes**. Realizations run through its division of work and its accounts and records, not one person's skill on their own account |
| 4 | Non-deontic index? | **Yes**. No member grants, alters or withdraws standing or authorization |
| 5 | Exercise, not development (CD5)? | **Yes**; excluded: `P10809` |

**Draft recommendation:** PASS.

**Notes for the reviewer:**
- BPO types negotiating with the customer (P10811) and discussing resolution internally (P10812) as acts of formulation. The draft takes BPO's typing as it is.

| Finding (PASS / FAIL) | Reviewer | Date | Notes |
|---|---|---|---|
|  |  |  |  |

### T2-30 — Collections Management

| Field | Value |
|---|---|
| Candidate | BCC-c4904759, catalog key `management\|collection`; concept `bcoc:CollectionsManagement` |
| Definition | A business capability of an organization to pursue, settle or write off the amounts its customers owe and have not paid when due, grounded in the organization's members as organized. (checked against CAP-07: no deontic terms) |
| Proposed classification | `bco:BusinessCapability` (CM-01), under `obo:BFO_0000016` (disposition) on a PASS; foundational ancestor `cco:ont00000568` (Organization Capability), as the vocabulary records; bearer `cco:ont00001180` (Organization) |
| Grounding | **Basis:** the collections members who pursue, settle and write off overdue amounts, as organized. **Enabling, not basis:** the collections and receivables systems. **Arrangements:** the amounts are owed to the organization, and pursued and written off in its name |

**Realization index** (6):

| Member | Via (PCF) | Genus (BPO) | Evidence |
|---|---|---|---|
| `bpo:P10745` | 9.2.4 Manage and process collections | Act of Accounting | designating record |
| `bpo:P10805` | 9.2.4.2 Analyze delinquent account balances | Act of Analysis | process beneath it |
| `bpo:P10806` | 9.2.4.3 Correspond/Negotiate with delinquent accounts | Act of Formulation | process beneath it |
| `bpo:P10807` | 9.2.4.4 Discuss account resolution with internal parties | Act of Formulation | process beneath it |
| `bpo:P10808` | 9.2.4.5 Process adjustments/write off balances | Act of Accounting | process beneath it |
| `bpo:P14007` | 9.2.4.6 Perform recovery workout | Act of Formulation | process beneath it |

**Excluded** (1):

| Act | Via (PCF) | Code | Reason |
|---|---|---|---|
| `bpo:P10804` | 9.2.4.1 Establish policies for delinquent accounts | Q5 | establishing policies for delinquent accounts: setting the policies that govern this capability's own practice shapes the capability rather than exercising it (tranche-1 practice, T1-02 question 5) |

**Taxonomy review** (`docs/catalog/tranche-2-review.yaml`; classified, not validated):

| Link | Disposition | Reason |
|---|---|---|
| Default Account Management → Collections Management | retained, `kind-of`, kept | default accounts are overdue accounts in a further state, and Collections Management's definition covers pursuing, settling and writing off (PCF 9.2.4.5): collections with its object restricted. Reclassified from the PCF reading |
| Collections Management → Revenue and Receivables Management | retained, `part-of`, kept | PCF hierarchy; the narrower's work is part of the broader's, not a kind of it |

| # | Question (§8) | Draft answer |
|---|---|---|
| 1 | Bearer kind: an Organization? | **Yes**. The work is the organization's: the amounts are owed to the organization, and pursued and written off in its name |
| 2 | Basis kind: member agents as organized, no artifact counted? | **Yes**. The collections members who pursue, settle and write off overdue amounts. The collections and receivables systems are enabling conditions; the work can be done with other tools, so none is constitutive of the type |
| 3 | Through the organization's arrangements? | **Yes**. Realizations run through its division of work and its accounts and records, not one person's skill on their own account |
| 4 | Non-deontic index? | **Yes**. No member grants, alters or withdraws standing or authorization |
| 5 | Exercise, not development (CD5)? | **Yes**; excluded: `P10804` |

**Draft recommendation:** PASS.

**Notes for the reviewer:**
- P14007 (recovery workout) is also the only act BPO wires to Default Account Management, which stays not ready (docs/catalog/tranche-2-q12.md).

| Finding (PASS / FAIL) | Reviewer | Date | Notes |
|---|---|---|---|
|  |  |  |  |

### T2-31 — Customer Credit Management

| Field | Value |
|---|---|
| Candidate | BCC-b7ff0eac, catalog key `administration\|customer credit`; concept `bcoc:CustomerCreditManagement` |
| Definition | A business capability of an organization to evaluate requests from customers to buy on credit, set and review the credit it extends to each, and monitor how that credit is used, grounded in the organization's members as organized. (checked against CAP-07: no deontic terms) |
| Proposed classification | `bco:BusinessCapability` (CM-01), under `obo:BFO_0000016` (disposition) on a PASS; foundational ancestor `cco:ont00000568` (Organization Capability), as the vocabulary records; bearer `cco:ont00001180` (Organization) |
| Grounding | **Basis:** the credit members who evaluate applications, set and review limits and monitor their use, as organized. **Enabling, not basis:** the credit-scoring tools and the receivables ledger. **Arrangements:** the credit is the organization's, extended on its terms |

**Realization index** (5):

| Member | Via (PCF) | Genus (BPO) | Evidence |
|---|---|---|---|
| `bpo:P10742` | 9.2.1 Process customer credit | Act of Accounting | designating record |
| `bpo:P14187` | 9.2.1.3 Analyze credit scoring history | Act of Analysis | process beneath it |
| `bpo:P14188` | 9.2.1.4 Forecast credit scoring requirement | Act of Formulation | process beneath it |
| `bpo:P10791` | 9.2.1.5 Review existing accounts | Act of Appraisal | process beneath it |
| `bpo:P10792` | 9.2.1.6 Produce credit/collection reports | Act of Reporting | process beneath it |

**Excluded** (3):

| Act | Via (PCF) | Code | Reason |
|---|---|---|---|
| `bpo:P10789` | 9.2.1.1 Establish credit policies | Q5 | establishing credit policies: setting the policies that govern this capability's own practice shapes the capability rather than exercising it (tranche-1 practice, T1-02 question 5) |
| `bpo:P10790` | 9.2.1.2 Analyze/Approve new account applications | Q4 | approving new account applications grants a customer standing to buy on credit |
| `bpo:P10793` | 9.2.1.7 Reinstate or suspend accounts based on credit policies | Q4 | reinstating or suspending accounts grants or withdraws that standing |

**Taxonomy review** (`docs/catalog/tranche-2-review.yaml`; classified, not validated):

| Link | Disposition | Reason |
|---|---|---|
| Customer Credit Management → Revenue and Receivables Management | retained, `part-of`, kept | PCF hierarchy; the narrower's work is part of the broader's, not a kind of it |

| # | Question (§8) | Draft answer |
|---|---|---|
| 1 | Bearer kind: an Organization? | **Yes**. The work is the organization's: the credit is the organization's, extended on its terms |
| 2 | Basis kind: member agents as organized, no artifact counted? | **Yes**. The credit members who evaluate applications, set and review limits and monitor their use. The credit-scoring tools and the receivables ledger are enabling conditions; the work can be done with other tools, so none is constitutive of the type |
| 3 | Through the organization's arrangements? | **Yes**. Realizations run through its division of work and its accounts and records, not one person's skill on their own account |
| 4 | Non-deontic index? | **Yes, for the reviewer to confirm** (below); excluded as deontic: `P10790`, `P10793` |
| 5 | Exercise, not development (CD5)? | **Yes**; excluded: `P10789` |

**Draft recommendation:** PASS, with question 4 for the reviewer.

**Notes for the reviewer:**
- The definition's 'set and review the credit it extends' names a limit, an amount the organization decides, and the draft reads that as describable without standing. Granting and withdrawing a customer's standing are excluded. The reviewer decides question 4.

| Finding (PASS / FAIL) | Reviewer | Date | Notes |
|---|---|---|---|
|  |  |  |  |

### T2-32 — Customer Invoicing

| Field | Value |
|---|---|
| Candidate | BCC-8a70a337, catalog key `transaction\|customer`; concept `bcoc:CustomerInvoicing` |
| Definition | A business capability of an organization to prepare and send its customers accurate invoices for what it has sold them, and correct those invoices when needed, grounded in the organization's members as organized. (checked against CAP-07: no deontic terms) |
| Proposed classification | `bco:BusinessCapability` (CM-01), under `obo:BFO_0000016` (disposition) on a PASS; foundational ancestor `cco:ont00000568` (Organization Capability), as the vocabulary records; bearer `cco:ont00001180` (Organization) |
| Grounding | **Basis:** the billing members who keep billing data and prepare, send and correct invoices, as organized. **Enabling, not basis:** the billing system and the customer and product master files. **Arrangements:** the invoices are the organization's claims on its customers |

**Realization index** (6):

| Member | Via (PCF) | Genus (BPO) | Evidence |
|---|---|---|---|
| `bpo:P10743` | 9.2.2 Invoice customer | Act of Accounting | designating record |
| `bpo:P10794` | 9.2.2.1 Maintain customer/product master files | Act of Accounting | process beneath it |
| `bpo:P10795` | 9.2.2.2 Generate customer billing data | Act of Accounting | process beneath it |
| `bpo:P10796` | 9.2.2.3 Transmit billing data to customers | Act of Communication | process beneath it |
| `bpo:P10797` | 9.2.2.4 Post receivable entries | Act of Accounting | process beneath it |
| `bpo:P10798` | 9.2.2.5 Resolve customer billing inquiries | Act of Accounting | process beneath it |

**Taxonomy review** (`docs/catalog/tranche-2-review.yaml`; classified, not validated):

| Link | Disposition | Reason |
|---|---|---|
| Customer Invoicing → Revenue and Receivables Management | retained, `part-of`, kept | PCF hierarchy; the narrower's work is part of the broader's, not a kind of it |

| # | Question (§8) | Draft answer |
|---|---|---|
| 1 | Bearer kind: an Organization? | **Yes**. The work is the organization's: the invoices are the organization's claims on its customers |
| 2 | Basis kind: member agents as organized, no artifact counted? | **Yes**. The billing members who keep billing data and prepare, send and correct invoices. The billing system and the customer and product master files are enabling conditions; the work can be done with other tools, so none is constitutive of the type |
| 3 | Through the organization's arrangements? | **Yes**. Realizations run through its division of work and its accounts and records, not one person's skill on their own account |
| 4 | Non-deontic index? | **Yes**. No member grants, alters or withdraws standing or authorization |
| 5 | Exercise, not development (CD5)? | **Yes** |

**Draft recommendation:** PASS.

| Finding (PASS / FAIL) | Reviewer | Date | Notes |
|---|---|---|---|
|  |  |  |  |

### T2-33 — Tax Planning

| Field | Value |
|---|---|
| Candidate | BCC-ce052840, catalog key `formulation\|tax strategy and plan`; concept `bcoc:TaxPlanning` |
| Definition | A business capability of an organization to forecast its tax liabilities, assess the tax effects of what it intends to do, and set its tax strategy accordingly, grounded in the organization's members as organized. (checked against CAP-07: no deontic terms) |
| Proposed classification | `bco:BusinessCapability` (CM-01), under `obo:BFO_0000016` (disposition) on a PASS; foundational ancestor `cco:ont00000568` (Organization Capability), as the vocabulary records; bearer `cco:ont00001180` (Organization) |
| Grounding | **Basis:** the tax members who forecast liabilities, assess effects and set tax strategy, as organized. **Enabling, not basis:** the tax models. **Arrangements:** the strategy is the organization's, set for its own obligations |

**Realization index** (3):

| Member | Via (PCF) | Genus (BPO) | Evidence |
|---|---|---|---|
| `bpo:P10765` | 9.9.1 Develop tax strategy and plan | Act of Formulation | designating record |
| `bpo:P10927` | 9.9.1.1 Develop foreign, national, state, and local tax strategy | Act of Formulation | process beneath it |
| `bpo:P10928` | 9.9.1.2 Consolidate and optimize total tax plan | Act of Formulation | process beneath it |

**Excluded** (1):

| Act | Via (PCF) | Code | Reason |
|---|---|---|---|
| `bpo:P10929` | 9.9.1.3 Maintain tax master data | OTHER | maintaining tax master data is Tax Processing's record-keeping |

**Taxonomy review** (`docs/catalog/tranche-2-review.yaml`; classified, not validated):

| Link | Disposition | Reason |
|---|---|---|
| Tax Planning → Tax Management | retained, `part-of`, kept | PCF hierarchy; the narrower's work is part of the broader's, not a kind of it |

| # | Question (§8) | Draft answer |
|---|---|---|
| 1 | Bearer kind: an Organization? | **Yes**. The work is the organization's: the strategy is the organization's, set for its own obligations |
| 2 | Basis kind: member agents as organized, no artifact counted? | **Yes**. The tax members who forecast liabilities, assess effects and set tax strategy. The tax models are enabling conditions; the work can be done with other tools, so none is constitutive of the type |
| 3 | Through the organization's arrangements? | **Yes**. Realizations run through its division of work and its accounts and records, not one person's skill on their own account |
| 4 | Non-deontic index? | **Yes**. No member grants, alters or withdraws standing or authorization |
| 5 | Exercise, not development (CD5)? | **Yes** |

**Draft recommendation:** PASS.

**Notes for the reviewer:**
- For a planning capability, formulating the plan is the exercise, not its development (CD5), so the formulation acts are in.

| Finding (PASS / FAIL) | Reviewer | Date | Notes |
|---|---|---|---|
|  |  |  |  |

### T2-34 — Tax Processing

| Field | Value |
|---|---|
| Candidate | BCC-52f0795a, catalog key `administration\|tax`; concept `bcoc:TaxProcessing` |
| Definition | A business capability of an organization to determine, declare, pay and account for the taxes it owes on its income, property, transactions and services, and keep the records that support them, grounded in the organization's members as organized. (checked against CAP-07: no deontic terms) |
| Proposed classification | `bco:BusinessCapability` (CM-01), under `obo:BFO_0000016` (disposition) on a PASS; foundational ancestor `cco:ont00000568` (Organization Capability), as the vocabulary records; bearer `cco:ont00001180` (Organization) |
| Grounding | **Basis:** the tax members who prepare returns, account for taxes and answer inquiries, as organized. **Enabling, not basis:** the tax engines and the ledger. **Arrangements:** the taxes are the organization's obligations, declared and paid in its name |

**Realization index** (7):

| Member | Via (PCF) | Genus (BPO) | Evidence |
|---|---|---|---|
| `bpo:P10766` | 9.9.2 Process taxes | Planned Act | designating record |
| `bpo:P10931` | 9.9.2.2 Prepare tax returns | Act of Reporting | process beneath it |
| `bpo:P10932` | 9.9.2.3 Prepare foreign taxes | Act of Reporting | process beneath it |
| `bpo:P10933` | 9.9.2.4 Calculate deferred taxes | Act of Accounting | process beneath it |
| `bpo:P10934` | 9.9.2.5 Account for taxes | Act of Accounting | process beneath it |
| `bpo:P10935` | 9.9.2.6 Monitor tax compliance | Act of Monitoring | process beneath it |
| `bpo:P10936` | 9.9.2.7 Address tax inquiries | Act of Reporting | process beneath it |

**Excluded** (1):

| Act | Via (PCF) | Code | Reason |
|---|---|---|---|
| `bpo:P10930` | 9.9.2.1 Perform tax planning/strategy | OTHER | tax planning and strategy is Tax Planning's work |

**Taxonomy review** (`docs/catalog/tranche-2-review.yaml`; classified, not validated):

| Link | Disposition | Reason |
|---|---|---|
| Tax Processing → Tax Management | retained, `part-of`, kept | PCF hierarchy; the narrower's work is part of the broader's, not a kind of it |

| # | Question (§8) | Draft answer |
|---|---|---|
| 1 | Bearer kind: an Organization? | **Yes**. The work is the organization's: the taxes are the organization's obligations, declared and paid in its name |
| 2 | Basis kind: member agents as organized, no artifact counted? | **Yes**. The tax members who prepare returns, account for taxes and answer inquiries. The tax engines and the ledger are enabling conditions; the work can be done with other tools, so none is constitutive of the type |
| 3 | Through the organization's arrangements? | **Yes**. Realizations run through its division of work and its accounts and records, not one person's skill on their own account |
| 4 | Non-deontic index? | **Yes**. No member grants, alters or withdraws standing or authorization |
| 5 | Exercise, not development (CD5)? | **Yes** |

**Draft recommendation:** PASS.

**Notes for the reviewer:**
- Filing a return discharges an obligation and confers no standing, as in T1-02 for payroll tax forms.

| Finding (PASS / FAIL) | Reviewer | Date | Notes |
|---|---|---|---|
|  |  |  |  |

### T2-35 — Cash Management

| Field | Value |
|---|---|
| Candidate | BCC-a1c5454d, catalog key `management\|cash`; concept `bcoc:CashManagement` |
| Definition | A business capability of an organization to track its cash positions across its accounts and move cash among them, so that it is positioned where it is used, grounded in the organization's members as organized. (checked against CAP-07: no deontic terms) |
| Proposed classification | `bco:BusinessCapability` (CM-01), under `obo:BFO_0000016` (disposition) on a PASS; foundational ancestor `cco:ont00000568` (Organization Capability), as the vocabulary records; bearer `cco:ont00001180` (Organization) |
| Grounding | **Basis:** the treasury and cash members who reconcile positions and move cash among accounts, as organized. **Enabling, not basis:** the banking portals and the treasury system. **Arrangements:** the cash is the organization's, in its accounts |

**Realization index** (3):

| Member | Via (PCF) | Genus (BPO) | Evidence |
|---|---|---|---|
| `bpo:P10893` | 9.7.2.1 Manage and reconcile cash positions | Act of Accounting | process beneath it |
| `bpo:P10895` | 9.7.2.3 Process and oversee electronic fund transfers (EFTs) | Act of Financial Transaction | process beneath it |
| `bpo:P10898` | 9.7.2.6 Produce cash management accounting transactions and reports | Act of Reporting | process beneath it |

**Excluded** (6):

| Act | Via (PCF) | Code | Reason |
|---|---|---|---|
| `bpo:P10759` | 9.7.2 Manage cash | CAP-03 | typed under Organization Capability, not an act |
| `bpo:P10894` | 9.7.2.2 Manage cash equivalents | CAP-03 | typed under Organization Capability, not an act |
| `bpo:P10896` | 9.7.2.4 Develop cash flow forecasts | OTHER | cash flow forecasts are Cash Flow Management's work |
| `bpo:P10897` | 9.7.2.5 Manage cash flows | CAP-03 | typed under Organization Capability, not an act |
| `bpo:P10899` | 9.7.2.7 Manage and oversee banking relationships | CAP-03 | typed under Organization Capability, not an act |
| `bpo:P10900` | 9.7.2.8 Analyze, negotiate, resolve, and confirm bank fees | OTHER | bank fees are Banking Relationship Management's work |

**Taxonomy review** (`docs/catalog/tranche-2-review.yaml`; classified, not validated):

| Link | Disposition | Reason |
|---|---|---|
| Cash Equivalent Management → Cash Management | retained, `part-of`, kept | PCF hierarchy; the narrower's work is part of the broader's, not a kind of it |
| Cash Management → Treasury Management | retained, `part-of`, kept | PCF hierarchy; the narrower's work is part of the broader's, not a kind of it |
| Banking Relationship Management → Cash Management | retained, `part-of`, kept | PCF hierarchy; the narrower's work is part of the broader's, not a kind of it |
| Cash Flow Management → Cash Management | retained, `part-of`, kept | PCF hierarchy; the narrower's work is part of the broader's, not a kind of it |

| # | Question (§8) | Draft answer |
|---|---|---|
| 1 | Bearer kind: an Organization? | **Yes**. The work is the organization's: the cash is the organization's, in its accounts |
| 2 | Basis kind: member agents as organized, no artifact counted? | **Yes**. The treasury and cash members who reconcile positions and move cash among accounts. The banking portals and the treasury system are enabling conditions; the work can be done with other tools, so none is constitutive of the type |
| 3 | Through the organization's arrangements? | **Yes**. Realizations run through its division of work and its accounts and records, not one person's skill on their own account |
| 4 | Non-deontic index? | **Yes**. No member grants, alters or withdraws standing or authorization |
| 5 | Exercise, not development (CD5)? | **Yes** |

**Draft recommendation:** PASS.

| Finding (PASS / FAIL) | Reviewer | Date | Notes |
|---|---|---|---|
|  |  |  |  |

### T2-36 — In-House Bank Account Management

| Field | Value |
|---|---|
| Candidate | BCC-749adb52, catalog key `management\|in-house bank account`; concept `bcoc:InHouseBankAccountManagement` |
| Definition | A business capability of an organization to run accounts that its own units, subsidiaries among them, hold with a central treasury of the organization, and settle, lend and pay through those accounts as a bank would, grounded in the organization's members as organized. (checked against CAP-07: no deontic terms) |
| Proposed classification | `bco:BusinessCapability` (CM-01), under `obo:BFO_0000016` (disposition) on a PASS; foundational ancestor `cco:ont00000568` (Organization Capability), as the vocabulary records; bearer `cco:ont00001180` (Organization) |
| Grounding | **Basis:** the central treasury members who run the units' accounts and settle, lend and pay through them, as organized. **Enabling, not basis:** the in-house bank system. **Arrangements:** the accounts are held with the organization's own central treasury, for its units |

**Realization index** (6):

| Member | Via (PCF) | Genus (BPO) | Evidence |
|---|---|---|---|
| `bpo:P10902` | 9.7.3.2 Manage and facilitate inter-company borrowing transactions | Planned Act, Act of Loaning | process beneath it |
| `bpo:P10903` | 9.7.3.3 Manage centralized outgoing payments on behalf of subsidiaries | Act of Financial Transaction | process beneath it |
| `bpo:P10904` | 9.7.3.4 Manage central incoming payments on behalf of subsidiaries | Act of Financial Transaction | process beneath it |
| `bpo:P10905` | 9.7.3.5 Manage internal payments and netting transactions | Act of Financial Transaction | process beneath it |
| `bpo:P10906` | 9.7.3.6 Calculate interest and fees for in-house bank accounts | Act of Accounting | process beneath it |
| `bpo:P10907` | 9.7.3.7 Provide account statements for in-house bank accounts | Act of Communication | process beneath it |

**Excluded** (2):

| Act | Via (PCF) | Code | Reason |
|---|---|---|---|
| `bpo:P10760` | 9.7.3 Manage in-house bank accounts | CAP-03 | typed under Organization Capability, not an act |
| `bpo:P10901` | 9.7.3.1 Manage in-house bank accounts for subsidiaries | CAP-03 | typed under Organization Capability, not an act |

**Taxonomy review** (`docs/catalog/tranche-2-review.yaml`; classified, not validated):

| Link | Disposition | Reason |
|---|---|---|
| In-House Bank Account Management → Treasury Management | retained, `part-of`, kept | PCF hierarchy; the narrower's work is part of the broader's, not a kind of it |
| In-House Bank Account Management → In-House Bank Account Management | retained, `kind-of`, merged | the candidate was merged into In-House Bank Account Management |

| # | Question (§8) | Draft answer |
|---|---|---|
| 1 | Bearer kind: an Organization? | **Yes**. The work is the organization's: the accounts are held with the organization's own central treasury, for its units |
| 2 | Basis kind: member agents as organized, no artifact counted? | **Yes**. The central treasury members who run the units' accounts and settle, lend and pay through them. The in-house bank system are enabling conditions; the work can be done with other tools, so none is constitutive of the type |
| 3 | Through the organization's arrangements? | **Yes**. Realizations run through its division of work and its accounts and records, not one person's skill on their own account |
| 4 | Non-deontic index? | **Yes**. No member grants, alters or withdraws standing or authorization |
| 5 | Exercise, not development (CD5)? | **Yes** |

**Draft recommendation:** PASS.

| Finding (PASS / FAIL) | Reviewer | Date | Notes |
|---|---|---|---|
|  |  |  |  |

### T2-37 — Financial Risk Management

| Field | Value |
|---|---|
| Candidate | BCC-132e1b29, catalog key `monitoring\|risk and hedging transaction`; concept `bcoc:FinancialRiskManagement` |
| Definition | A business capability of an organization to identify and measure its exposure to losses from movements in financial markets and in the standing of its counterparties, and limit that exposure, hedging it where it chooses to, grounded in the organization's members as organized. (checked against CAP-07: no deontic terms) |
| Proposed classification | `bco:BusinessCapability` (CM-01), under `obo:BFO_0000016` (disposition) on a PASS; foundational ancestor `cco:ont00000568` (Organization Capability), as the vocabulary records; bearer `cco:ont00001180` (Organization) |
| Grounding | **Basis:** the treasury risk members who identify and measure exposures and decide how to limit them, as organized. **Enabling, not basis:** the risk and treasury systems. **Arrangements:** the exposures are the organization's, limited under its risk policy |

**Realization index** (2):

| Member | Via (PCF) | Genus (BPO) | Evidence |
|---|---|---|---|
| `bpo:P12974` | 9.7.5.1 Develop risk management/hedging strategy | Act of Formulation | process beneath it |
| `bpo:P11214` | 9.7.5.6 Produce hedge accounting transactions and reports | Act of Reporting | process beneath it |

**Excluded** (5):

| Act | Via (PCF) | Code | Reason |
|---|---|---|---|
| `bpo:P11208` | 9.7.5 Monitor and execute risk and hedging transactions | CAP-03 | typed under Organization Capability, not an act |
| `bpo:P11209` | 9.7.5.2 Manage interest rate risk | CAP-03 | typed under Organization Capability, not an act |
| `bpo:P11210` | 9.7.5.3 Manage foreign exchange risk | CAP-03 | typed under Organization Capability, not an act |
| `bpo:P11211` | 9.7.5.4 Manage exposure risk | CAP-03 | typed under Organization Capability, not an act |
| `bpo:P20137` | 9.7.5.5 Execute hedging transactions | CAP-03 | typed under Organization Capability, not an act |

**Taxonomy review** (`docs/catalog/tranche-2-review.yaml`; classified, not validated):

| Link | Disposition | Reason |
|---|---|---|
| Interest Rate Risk Management → Financial Risk Management | retained, `kind-of`, kept | interest rate risk is one kind of financial risk: the object restricted. Reclassified from the PCF reading |
| Financial Risk Management → Treasury Management | retained, `part-of`, kept | PCF hierarchy; the narrower's work is part of the broader's, not a kind of it |
| Counterparty Credit Exposure Management → Financial Risk Management | retained, `kind-of`, kept | counterparty credit exposure is one kind of financial risk: the object restricted. Reclassified from the PCF reading |
| Foreign Exchange Risk Management → Financial Risk Management | retained, `kind-of`, kept | foreign exchange risk is one kind of financial risk: the object restricted. Reclassified from the PCF reading |
| Hedging Transaction Execution → Financial Risk Management | retained, `part-of`, kept | executing hedges is one means by which financial risk is limited, not a kind of risk management |
| Financial Risk Management → BCC-44f37d0e (outside the tranche) | retained, `kind-of`, added | financial risk management is risk management with its object restricted; the target is outside the tranche |

| # | Question (§8) | Draft answer |
|---|---|---|
| 1 | Bearer kind: an Organization? | **Yes**. The work is the organization's: the exposures are the organization's, limited under its risk policy |
| 2 | Basis kind: member agents as organized, no artifact counted? | **Yes**. The treasury risk members who identify and measure exposures and decide how to limit them. The risk and treasury systems are enabling conditions; the work can be done with other tools, so none is constitutive of the type |
| 3 | Through the organization's arrangements? | **Yes**. Realizations run through its division of work and its accounts and records, not one person's skill on their own account |
| 4 | Non-deontic index? | **Yes**. No member grants, alters or withdraws standing or authorization |
| 5 | Exercise, not development (CD5)? | **Yes** |

**Draft recommendation:** PASS.

**Notes for the reviewer:**
- P12974 (developing a hedging strategy) is kept: deciding where the organization chooses to hedge is part of this capability's exercise, which its definition names, not policy for another capability. The four kind-of children's acts are not taken into this index.

| Finding (PASS / FAIL) | Reviewer | Date | Notes |
|---|---|---|---|
|  |  |  |  |

### T2-38 — Counterparty Credit Exposure Management

| Field | Value |
|---|---|
| Candidate | BCC-3e668a26, catalog key `management\|exposure risk`; concept `bcoc:CounterpartyCreditExposureManagement` |
| Definition | A business capability of an organization to measure the credit exposure it has to its customers and other counterparties, keep it within limits, secure it with collateral, and review it periodically, grounded in the organization's members as organized. (checked against CAP-07: no deontic terms) |
| Proposed classification | `bco:BusinessCapability` (CM-01), under `obo:BFO_0000016` (disposition) on a PASS; foundational ancestor `cco:ont00000568` (Organization Capability), as the vocabulary records; bearer `cco:ont00001180` (Organization) |
| Grounding | **Basis:** the credit-risk members who measure exposures, resolve limit breaches, manage collateral and review counterparties, as organized. **Enabling, not basis:** the exposure and collateral systems. **Arrangements:** the exposures are the organization's, against its own limits |

**Realization index** (4):

| Member | Via (PCF) | Genus (BPO) | Evidence |
|---|---|---|---|
| `bpo:P19584` | 9.7.5.4.1 Determine current customer exposures and limit exceptions | Act of Analysis | process beneath it |
| `bpo:P19585` | 9.7.5.4.2 Resolve customer exposure limit violations | Act of Selection | process beneath it |
| `bpo:P19586` | 9.7.5.4.3 Manage customer collateral | Act of Financial Transaction | process beneath it |
| `bpo:P19587` | 9.7.5.4.4 Perform annual customer credit reviews | Act of Appraisal | process beneath it |

**Excluded** (1):

| Act | Via (PCF) | Code | Reason |
|---|---|---|---|
| `bpo:P11211` | 9.7.5.4 Manage exposure risk | CAP-03 | typed under Organization Capability, not an act |

**Taxonomy review** (`docs/catalog/tranche-2-review.yaml`; classified, not validated):

| Link | Disposition | Reason |
|---|---|---|
| Counterparty Credit Exposure Management → Financial Risk Management | retained, `kind-of`, kept | counterparty credit exposure is one kind of financial risk: the object restricted. Reclassified from the PCF reading |
| Counterparty Credit Exposure Management → BCC-44f37d0e (outside the tranche) | retained, `kind-of`, redundant | true, but covered through Financial Risk Management, which is linked to the target instead |
| Issuer Credit Exposure Management → Counterparty Credit Exposure Management | retained, `kind-of`, added | an issuer whose obligations it holds is a counterparty: issuer credit exposure is counterparty credit exposure with its object restricted |

| # | Question (§8) | Draft answer |
|---|---|---|
| 1 | Bearer kind: an Organization? | **Yes**. The work is the organization's: the exposures are the organization's, against its own limits |
| 2 | Basis kind: member agents as organized, no artifact counted? | **Yes**. The credit-risk members who measure exposures, resolve limit breaches, manage collateral and review counterparties. The exposure and collateral systems are enabling conditions; the work can be done with other tools, so none is constitutive of the type |
| 3 | Through the organization's arrangements? | **Yes**. Realizations run through its division of work and its accounts and records, not one person's skill on their own account |
| 4 | Non-deontic index? | **Yes**. No member grants, alters or withdraws standing or authorization |
| 5 | Exercise, not development (CD5)? | **Yes** |

**Draft recommendation:** PASS.

**Notes for the reviewer:**
- Resolving limit violations (P19585) applies limits already set. It sets none, and confers no standing.

| Finding (PASS / FAIL) | Reviewer | Date | Notes |
|---|---|---|---|
|  |  |  |  |

### T2-39 — Foreign Exchange Risk Management

| Field | Value |
|---|---|
| Candidate | BCC-7c04ea8a, catalog key `management\|foreign exchange risk`; concept `bcoc:ForeignExchangeRiskManagement` |
| Definition | A business capability of an organization to measure its exposure to losses from changes in exchange rates, forecast their effect on it, and hedge that exposure where it chooses to, grounded in the organization's members as organized. (checked against CAP-07: no deontic terms) |
| Proposed classification | `bco:BusinessCapability` (CM-01), under `obo:BFO_0000016` (disposition) on a PASS; foundational ancestor `cco:ont00000568` (Organization Capability), as the vocabulary records; bearer `cco:ont00001180` (Organization) |
| Grounding | **Basis:** the treasury members who measure currency exposure, decide hedge requirements and trade, as organized. **Enabling, not basis:** the market-data feeds and the dealing platforms. **Arrangements:** the exposures and trades are the organization's, under its risk policy |

**Realization index** (6):

| Member | Via (PCF) | Genus (BPO) | Evidence |
|---|---|---|---|
| `bpo:P19579` | 9.7.5.3.1 Manage foreign exchange market data | Act of Monitoring | process beneath it |
| `bpo:P19580` | 9.7.5.3.2 Determine foreign exchange exposure for all currencies | Act of Analysis | process beneath it |
| `bpo:P19581` | 9.7.5.3.3 Determine foreign exchange hedge requirements in accordance with risk policy | Act of Selection | process beneath it |
| `bpo:P19582` | 9.7.5.3.4 Execute foreign exchange trades | Act of Financial Transaction | process beneath it |
| `bpo:P19583` | 9.7.5.3.5 Manage foreign exchange balance sheet risk | Act of Monitoring | process beneath it |
| `bpo:P10769` | 9.10.3 Monitor currency exposure/hedge currency | Act of Analysis | from BCC-8fc1f306 (merged) |

**Excluded** (1):

| Act | Via (PCF) | Code | Reason |
|---|---|---|---|
| `bpo:P11210` | 9.7.5.3 Manage foreign exchange risk | CAP-03 | typed under Organization Capability, not an act |

**Taxonomy review** (`docs/catalog/tranche-2-review.yaml`; classified, not validated):

| Link | Disposition | Reason |
|---|---|---|
| Foreign Exchange Risk Management → Financial Risk Management | retained, `kind-of`, kept | foreign exchange risk is one kind of financial risk: the object restricted. Reclassified from the PCF reading |
| Foreign Exchange Risk Management → BCC-44f37d0e (outside the tranche) | retained, `kind-of`, redundant | true, but covered through Financial Risk Management, which is linked to the target instead |

| # | Question (§8) | Draft answer |
|---|---|---|
| 1 | Bearer kind: an Organization? | **Yes**. The work is the organization's: the exposures and trades are the organization's, under its risk policy |
| 2 | Basis kind: member agents as organized, no artifact counted? | **Yes**. The treasury members who measure currency exposure, decide hedge requirements and trade. The market-data feeds and the dealing platforms are enabling conditions; the work can be done with other tools, so none is constitutive of the type |
| 3 | Through the organization's arrangements? | **Yes**. Realizations run through its division of work and its accounts and records, not one person's skill on their own account |
| 4 | Non-deontic index? | **Yes**. No member grants, alters or withdraws standing or authorization |
| 5 | Exercise, not development (CD5)? | **Yes** |

**Draft recommendation:** PASS.

| Finding (PASS / FAIL) | Reviewer | Date | Notes |
|---|---|---|---|
|  |  |  |  |

### T2-40 — Hedging Transaction Execution

| Field | Value |
|---|---|
| Candidate | BCC-8fdf31c6, catalog key `implementation\|hedging transaction`; concept `bcoc:HedgingTransactionExecution` |
| Definition | A business capability of an organization to enter into, carry out and later adjust the derivative and other transactions that offset the financial exposures it has decided to hedge, grounded in the organization's members as organized. (checked against CAP-07: no deontic terms) |
| Proposed classification | `bco:BusinessCapability` (CM-01), under `obo:BFO_0000016` (disposition) on a PASS; foundational ancestor `cco:ont00000568` (Organization Capability), as the vocabulary records; bearer `cco:ont00001180` (Organization) |
| Grounding | **Basis:** the treasury dealers who enter into, adjust and unwind hedges, as organized. **Enabling, not basis:** the dealing platforms and the confirmations systems. **Arrangements:** the hedges are the organization's contracts with its counterparties |

**Realization index** (4):

| Member | Via (PCF) | Genus (BPO) | Evidence |
|---|---|---|---|
| `bpo:P19588` | 9.7.5.5.1 Measure physical positions | Act of Appraisal | process beneath it |
| `bpo:P19589` | 9.7.5.5.2 Establish hedges | Act of Selection | process beneath it |
| `bpo:P19590` | 9.7.5.5.3 Unwind hedges | Act of Financial Transaction | process beneath it |
| `bpo:P11213` | 9.7.5.5.4 Evaluate and refine hedging positions | Act of Selection | process beneath it |

**Excluded** (2):

| Act | Via (PCF) | Code | Reason |
|---|---|---|---|
| `bpo:P20137` | 9.7.5.5 Execute hedging transactions | CAP-03 | typed under Organization Capability, not an act |
| `bpo:P11215` | 9.7.5.5.5 Monitor credit | OTHER | monitoring counterparty credit is Counterparty Credit Exposure Management's work |

**Taxonomy review** (`docs/catalog/tranche-2-review.yaml`; classified, not validated):

| Link | Disposition | Reason |
|---|---|---|
| Hedging Transaction Execution → Financial Risk Management | retained, `part-of`, kept | executing hedges is one means by which financial risk is limited, not a kind of risk management |

| # | Question (§8) | Draft answer |
|---|---|---|
| 1 | Bearer kind: an Organization? | **Yes**. The work is the organization's: the hedges are the organization's contracts with its counterparties |
| 2 | Basis kind: member agents as organized, no artifact counted? | **Yes**. The treasury dealers who enter into, adjust and unwind hedges. The dealing platforms and the confirmations systems are enabling conditions; the work can be done with other tools, so none is constitutive of the type |
| 3 | Through the organization's arrangements? | **Yes**. Realizations run through its division of work and its accounts and records, not one person's skill on their own account |
| 4 | Non-deontic index? | **Yes**. No member grants, alters or withdraws standing or authorization |
| 5 | Exercise, not development (CD5)? | **Yes** |

**Draft recommendation:** PASS.

| Finding (PASS / FAIL) | Reviewer | Date | Notes |
|---|---|---|---|
|  |  |  |  |

### T2-41 — Interest Rate Risk Management

| Field | Value |
|---|---|
| Candidate | BCC-0564598d, catalog key `management\|interest rate risk`; concept `bcoc:InterestRateRiskManagement` |
| Definition | A business capability of an organization to measure its exposure to losses from changes in interest rates on what it borrows and what it holds, and limit that exposure, grounded in the organization's members as organized. (checked against CAP-07: no deontic terms) |
| Proposed classification | `bco:BusinessCapability` (CM-01), under `obo:BFO_0000016` (disposition) on a PASS; foundational ancestor `cco:ont00000568` (Organization Capability), as the vocabulary records; bearer `cco:ont00001180` (Organization) |
| Grounding | **Basis:** the treasury members who measure interest-rate exposure, decide hedge requirements and trade, as organized. **Enabling, not basis:** the market-data feeds and the dealing platforms. **Arrangements:** the exposures are on the organization's own borrowing and holdings |

**Realization index** (4):

| Member | Via (PCF) | Genus (BPO) | Evidence |
|---|---|---|---|
| `bpo:P19575` | 9.7.5.2.1 Manage interest rate market data | Act of Monitoring | process beneath it |
| `bpo:P19576` | 9.7.5.2.2 Determine interest rate exposure for all markets | Act of Analysis | process beneath it |
| `bpo:P19577` | 9.7.5.2.3 Determine interest rate hedge requirements in accordance with risk policy | Act of Selection | process beneath it |
| `bpo:P19578` | 9.7.5.2.4 Execute interest rate trades | Act of Financial Transaction | process beneath it |

**Excluded** (1):

| Act | Via (PCF) | Code | Reason |
|---|---|---|---|
| `bpo:P11209` | 9.7.5.2 Manage interest rate risk | CAP-03 | typed under Organization Capability, not an act |

**Taxonomy review** (`docs/catalog/tranche-2-review.yaml`; classified, not validated):

| Link | Disposition | Reason |
|---|---|---|
| Interest Rate Risk Management → Financial Risk Management | retained, `kind-of`, kept | interest rate risk is one kind of financial risk: the object restricted. Reclassified from the PCF reading |
| Interest Rate Risk Management → BCC-44f37d0e (outside the tranche) | retained, `kind-of`, redundant | true, but covered through Financial Risk Management, which is linked to the target instead |

| # | Question (§8) | Draft answer |
|---|---|---|
| 1 | Bearer kind: an Organization? | **Yes**. The work is the organization's: the exposures are on the organization's own borrowing and holdings |
| 2 | Basis kind: member agents as organized, no artifact counted? | **Yes**. The treasury members who measure interest-rate exposure, decide hedge requirements and trade. The market-data feeds and the dealing platforms are enabling conditions; the work can be done with other tools, so none is constitutive of the type |
| 3 | Through the organization's arrangements? | **Yes**. Realizations run through its division of work and its accounts and records, not one person's skill on their own account |
| 4 | Non-deontic index? | **Yes**. No member grants, alters or withdraws standing or authorization |
| 5 | Exercise, not development (CD5)? | **Yes** |

**Draft recommendation:** PASS.

| Finding (PASS / FAIL) | Reviewer | Date | Notes |
|---|---|---|---|
|  |  |  |  |

### T2-42 — Treasury Policy Management

| Field | Value |
|---|---|
| Candidate | BCC-7757c12b, catalog key `management\|treasury policy and procedure`; concept `bcoc:TreasuryPolicyManagement` |
| Definition | A business capability of an organization to set, publish and keep current the rules and procedures under which its treasury invests, borrows, hedges and handles cash, grounded in the organization's members as organized. (checked against CAP-07: no deontic terms) |
| Proposed classification | `bco:BusinessCapability` (CM-01), under `obo:BFO_0000016` (disposition) on a PASS; foundational ancestor `cco:ont00000568` (Organization Capability), as the vocabulary records; bearer `cco:ont00001180` (Organization) |
| Grounding | **Basis:** the treasury members who draft, publish, monitor, audit and revise treasury policies and procedures, as organized. **Enabling, not basis:** the policy documents. **Arrangements:** the policies are the organization's, issued through its treasury |

**Realization index** (5):

| Member | Via (PCF) | Genus (BPO) | Evidence |
|---|---|---|---|
| `bpo:P10886` | 9.7.1.2 Establish and publish treasury policies | Act of Formulation | process beneath it |
| `bpo:P10887` | 9.7.1.3 Develop treasury procedures | Act of Formulation | process beneath it |
| `bpo:P10888` | 9.7.1.4 Monitor treasury procedures | Act of Monitoring | process beneath it |
| `bpo:P10889` | 9.7.1.5 Audit treasury procedures | Act of Appraisal | process beneath it |
| `bpo:P10890` | 9.7.1.6 Revise treasury procedures | Act of Formulation | process beneath it |

**Excluded** (4):

| Act | Via (PCF) | Code | Reason |
|---|---|---|---|
| `bpo:P10758` | 9.7.1 Manage treasury policies and procedures | CAP-03 | typed under Organization Capability, not an act |
| `bpo:P10885` | 9.7.1.1 Establish scope and governance of treasury operations | Q5 | establishing the scope and governance of treasury operations sets up the treasury itself, which develops the capability |
| `bpo:P10891` | 9.7.1.7 Develop and confirm internal controls for treasury | OTHER | internal controls for treasury are Internal Control Design's work |
| `bpo:P10892` | 9.7.1.8 Define system security requirements | OTHER | system security requirements are not treasury policy work |

**Taxonomy review** (`docs/catalog/tranche-2-review.yaml`; classified, not validated):

| Link | Disposition | Reason |
|---|---|---|
| Treasury Policy Management → Treasury Management | retained, `part-of`, kept | PCF hierarchy; the narrower's work is part of the broader's, not a kind of it |

| # | Question (§8) | Draft answer |
|---|---|---|
| 1 | Bearer kind: an Organization? | **Yes**. The work is the organization's: the policies are the organization's, issued through its treasury |
| 2 | Basis kind: member agents as organized, no artifact counted? | **Yes**. The treasury members who draft, publish, monitor, audit and revise treasury policies and procedures. The policy documents are enabling conditions; the work can be done with other tools, so none is constitutive of the type |
| 3 | Through the organization's arrangements? | **Yes**. Realizations run through its division of work and its accounts and records, not one person's skill on their own account |
| 4 | Non-deontic index? | **Yes, for the reviewer to confirm** (below) |
| 5 | Exercise, not development (CD5)? | **Yes**; excluded: `P10885` |

**Draft recommendation:** PASS, with question 4 for the reviewer.

**Notes for the reviewer:**
- Question 4, as for Accounting Policy Management.

| Finding (PASS / FAIL) | Reviewer | Date | Notes |
|---|---|---|---|
|  |  |  |  |

### T2-43 — Internal Control Operation and Monitoring

| Field | Value |
|---|---|
| Candidate | BCC-ded8ed18, catalog key `management\|control`; concept `bcoc:InternalControlOperation` |
| Definition | A business capability of an organization to carry out the controls it has defined and monitor whether they operate as designed and are complied with, grounded in the organization's members as organized. (checked against CAP-07: no deontic terms) |
| Proposed classification | `bco:BusinessCapability` (CM-01), under `obo:BFO_0000016` (disposition) on a PASS; foundational ancestor `cco:ont00000568` (Organization Capability), as the vocabulary records; bearer `cco:ont00001180` (Organization) |
| Grounding | **Basis:** the control owners and compliance members who carry out the controls and test whether they work, as organized. **Enabling, not basis:** the control-testing tools. **Arrangements:** the controls are the organization's, operated in its own processes |

**Realization index** (2):

| Member | Via (PCF) | Genus (BPO) | Evidence |
|---|---|---|---|
| `bpo:P21574` | 9.8.2 Operate controls and monitor compliance with internal controls policies and procedures | Planned Act | designating record |
| `bpo:P10918` | 9.8.2.1 Monitor control effectiveness | Act of Monitoring | process beneath it |

**Excluded** (1):

| Act | Via (PCF) | Code | Reason |
|---|---|---|---|
| `bpo:P10919` | 9.8.2.2 Remediate control deficiencies | Q5 | remediating control deficiencies changes the controls, which is Internal Control Design's work or the capability's improvement, not its operation |

**Taxonomy review** (`docs/catalog/tranche-2-review.yaml`; classified, not validated):

| Link | Disposition | Reason |
|---|---|---|
| Internal Control → Internal Control Operation and Monitoring | incorrect (reversed) | reversed: operating controls (PCF 9.8.2) is a component of internal control, not its parent; a containment artifact of the word 'control' |
| Internal Control Operation and Monitoring → Internal Control | retained, `part-of`, added | PCF 9.8.2 under 9.8: operating and monitoring controls is part of internal control's work, by its definition |

| # | Question (§8) | Draft answer |
|---|---|---|
| 1 | Bearer kind: an Organization? | **Yes**. The work is the organization's: the controls are the organization's, operated in its own processes |
| 2 | Basis kind: member agents as organized, no artifact counted? | **Yes**. The control owners and compliance members who carry out the controls and test whether they work. The control-testing tools are enabling conditions; the work can be done with other tools, so none is constitutive of the type |
| 3 | Through the organization's arrangements? | **Yes**. Realizations run through its division of work and its accounts and records, not one person's skill on their own account |
| 4 | Non-deontic index? | **Yes**. No member grants, alters or withdraws standing or authorization |
| 5 | Exercise, not development (CD5)? | **Yes**; excluded: `P10919` |

**Draft recommendation:** PASS.

| Finding (PASS / FAIL) | Reviewer | Date | Notes |
|---|---|---|---|
|  |  |  |  |

## 5. Not in this batch

The 15 not-ready concepts, and the reasons, are in `docs/catalog/tranche-2.md`, section 5.
Thirteen of them wait on Q-12 (`docs/catalog/tranche-2-q12.md`). The 5 capability areas
are not proposed for G1-T (CD16, E4). T1-02 and T1-03 are already signed and are not
re-reviewed here.
