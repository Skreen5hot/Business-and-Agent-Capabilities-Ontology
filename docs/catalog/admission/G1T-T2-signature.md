# G1-T tranche 2 — consolidated signature record, 33 classes

| Field | Value |
|---|---|
| Status | **Prepared for signature. Not signed.** Prepared under `docs/decisions/2026-11-14-g1t-tranche-2-batch-decided.md`, part 6. No class below is admitted until the named reviewer's signature is recorded here, in his own words |
| Signing reviewer | Aaron Damiano, Product Owner and Ontology Architect (part 6) |
| Records signed | `docs/catalog/admission/G1T-T2-batch.md`, revision 3, SHA-256 `a755609be887fe226c45d6614d81eeaad39289084a617b5a272c7644699962fb`: the 33 sections listed below, each with its definition, grounding, realization index, exclusions, worked cases, taxonomy and five G1-T answers |
| Vocabulary | each concept's record digest below, as `tools/vocab/build.py --digest <concept>` prints it |
| Independent evidence | `docs/catalog/admission/G1T-T2-review-2026-11-07.md` (SHA-256 `7c7efb831cf6a5276fe6e173cea34f4a3f40af7f4d5adae3e8e881c175671e08`): PASS for all 33. It is analytical evidence, not the signature |
| Not here | the 7 records of part 4: the supplementary review (`docs/catalog/admission/G1T-T2-supplementary-review.md`) found 6 PASS, which await the architect's direction, and left T2-25 PENDING REVIEW; and the 3 withdrawn capability areas (part 3) |
| Prepared by | Claude Code (`claude-opus-5-5`), 2026-11-14. It records no finding and no signature |

A signed PASS licenses asserting the class under `obo:BFO_0000016` (disposition), and so under `bco:BusinessCapability`, for that class only (CAP-04). It licenses no organization's claim to bear one (G1-I). No OWL is written before D5.

Derived in part from the APQC Process Classification Framework® 7.4 (element IDs, under APQC's notice in `NOTICE.md`). APQC does not endorse this work.

## 1. The classes

| Id | Candidate | Class | Concept | Batch | Index | Independent review | Concept record SHA-256 |
|---|---|---|---|---|---|---|---|
| T2-08 | BCC-792537f9 | Financial Reporting | `bcoc:FinancialReporting` | A | 10 | PASS | `84e3c1a7ea9b2743db2f7ed54ce1d2d835be92c3551dbc6e439496d307abe718` |
| T2-09 | BCC-e3c8bd37 | Fixed-Asset Accounting | `bcoc:FixedAssetAccounting` | A | 8 | PASS | `d7432dbd92113a3f0b4169b5819967a60285e518b8163f69973db30947e50757` |
| T2-10 | BCC-8b431985 | General Ledger Accounting | `bcoc:GeneralLedgerAccounting` | A | 9 | PASS | `d7c19172b362dd43d1c1f2fc0276619b4a7903ed533d932c6656903aecb799b8` |
| T2-12 | BCC-e1fa4843 | Trade Product Classification | `bcoc:TradeProductClassification` | A | 1 | PASS | `578838efeef4dd0a6e188832eb8ace1048e5a80e5ec5bfce3321e177d9a6e298` |
| T2-13 | BCC-f6799472 | Restricted Party Screening | `bcoc:RestrictedPartyScreening` | A | 1 | PASS | `1e5990ec6e5bc10934c92a209bdf9cb167c29623dc9a2408396ab10f8f7900f8` |
| T2-15 | BCC-0c80b752 | Trade Preference Management | `bcoc:TradePreferenceManagement` | A | 1 | PASS | `c005bde58329c3929abf16a3874b14e076ced6c2983464e2ecd00ab4ed505474` |
| T2-16 | BCC-b55668bc | Internal Control Reporting | `bcoc:InternalControlReporting` | A | 4 | PASS | `f92d825518267ec8653d0103db63e5b90deabb11a8a3c6a4ff7bdc4f5a427f3a` |
| T2-18 | BCC-5dfa2101 | International Rate Monitoring | `bcoc:InternationalRateMonitoring` | A | 1 | PASS | `768596eaf4e876ad90684fc805c2ea1e07731df3a528e6b1fb15a8fea9619808` |
| T2-19 | BCC-bf62316a | Cross-Border Funds Transfer Management | `bcoc:CrossBorderFundsTransferManagement` | A | 1 | PASS | `7d28476b319f61682d966ad8a1bf88f42a9315974526ca489a43460ee8e03b27` |
| T2-22 | BCC-85fbcb90 | Time Reporting | `bcoc:TimeReporting` | A | 4 | PASS | `eee8ad6a36343a04a02b477f265e47c5de80e7ad18ace551435cb74b686c5141` |
| T2-28 | BCC-6587dedf | Accounts Receivable Processing | `bcoc:AccountsReceivableProcessing` | A | 4 | PASS | `fb5d4e1f8541402b1de97d78b9d07fa512dc65f96210a8fb9bd1f147fcf68dbd` |
| T2-29 | BCC-cebf0da8 | Customer Deduction and Adjustment Management | `bcoc:CustomerDeductionManagement` | A | 5 | PASS | `955724f77555d30bc5e3998574348f3a9d80f95922c4bdf0cc1f942c543219a3` |
| T2-30 | BCC-c4904759 | Collections Management | `bcoc:CollectionsManagement` | A | 5 | PASS | `f88b4eacc76eecd8d544fd8b51d53ae596f7fd1974b620bec5303cb6abe1725b` |
| T2-34 | BCC-52f0795a | Tax Processing | `bcoc:TaxProcessing` | A | 6 | PASS | `66fa1dc7eb2e5eebdf796e0db9a4393cd272b9e9c3ea4d43843e50b5cde987ac` |
| T2-36 | BCC-749adb52 | In-House Bank Account Management | `bcoc:InHouseBankAccountManagement` | A | 6 | PASS | `76db9f3f639ca399378c9ef2bfe195f8ba42aaccc63961d9b4f7df71c865ad09` |
| T2-39 | BCC-7c04ea8a | Foreign Exchange Risk Management | `bcoc:ForeignExchangeRiskManagement` | A | 6 | PASS | `d89a321f2a826f1c91953c3ce2f0e3a9a493d2ddeb4ada105faf3033893ca198` |
| T2-41 | BCC-0564598d | Interest Rate Risk Management | `bcoc:InterestRateRiskManagement` | A | 4 | PASS | `274a45072c919794f6bf8c82d851ab94955a303db777afdbb5fa89864c3e40c9` |
| T2-01 | BCC-9511900a | Payment Processing | `bcoc:PaymentProcessing` | B | 2 | PASS | `daea7d6c004030621483dd05fd2e3e7e817ddd225cac55a1b5d4a5fd4731a081` |
| T2-03 | BCC-35c8111b | Expense Reimbursement Processing | `bcoc:ExpenseReimbursementProcessing` | B | 3 | PASS | `8987978e0bf5f2fdb87b4431ea2500d7bef6f2119415a18bd1975c6209fa0d87` |
| T2-05 | BCC-95b092a2 | Capital Project Accounting | `bcoc:CapitalProjectAccounting` | B | 4 | PASS | `9a41381d4c1fbfc86412753f330602b139644ea4b8d5263cdea61200469db915` |
| T2-07 | BCC-e8acc1f8 | Accounting Policy Management | `bcoc:AccountingPolicyManagement` | B | 2 | PASS | `e4b4f0aa8ca7f1fadb6f3f14ce41b0522caf8e20cb44eaf32d6cb5e31cd3fef5` |
| T2-11 | BCC-4f5c2f36 | Letter of Credit Management | `bcoc:LetterOfCreditManagement` | B | 1 | PASS | `33ef90f2c43d8788d679e30dfee187a9604ddef286725a8e11868599b5d54711` |
| T2-14 | BCC-c5e7dca0 | Trade and Customs Documentation | `bcoc:TradeDocumentation` | B | 4 | PASS | `d5db68e30409c5a92d66b67af64bccb3538970cbc392a929b87af1582b0a4b2e` |
| T2-20 | BCC-d105ff07 | Pay Management | `bcoc:PayManagement` | B | 8 | PASS | `ac7202489c6ed17bad3673841de5748f7712d7d5efebbaf7202f8ae12312f46d` |
| T2-21 | BCC-394909c1 | Payroll Tax Processing | `bcoc:PayrollTaxProcessing` | B | 3 | PASS | `c044f73d0943b84f5affc5a5d133b45e4b219fb2f21ce7d6728d97f728f66d70` |
| T2-23 | BCC-302a390a | Cost Accounting | `bcoc:CostAccounting` | B | 4 | PASS | `3675f36e660957fa2a8dba61af0b15a11fbb42324b6fdc3d8a7613a6b8df684c` |
| T2-26 | BCC-87e1811c | Financial Planning, Budgeting and Forecasting | `bcoc:FinancialPlanningBudgetingAndForecasting` | B | 3 | PASS | `d24cefca10738718f9d013928ca67d5084a47eb765527e8c712fde8d9d906642` |
| T2-32 | BCC-8a70a337 | Customer Invoicing | `bcoc:CustomerInvoicing` | B | 5 | PASS | `092b0d0ab20129442ab9e02309e5257d99d310055215346e8f026f7844b143e9` |
| T2-33 | BCC-ce052840 | Tax Planning | `bcoc:TaxPlanning` | B | 2 | PASS | `48d1d244d6c7d1856293d3e4a3175d3ef1cded68cc3a7762c07e3938ac7e053c` |
| T2-35 | BCC-a1c5454d | Cash Management | `bcoc:CashManagement` | B | 3 | PASS | `f6a47b9b2f0701cd2ad100be024ed9c625ae964710f5da9537cf4239385dff8f` |
| T2-38 | BCC-3e668a26 | Counterparty Credit Exposure Management | `bcoc:CounterpartyCreditExposureManagement` | B | 4 | PASS | `eb9144e87f75cc267eded102d57ac4b62f257bc74e7b5b89c95f03b5ada7a7ee` |
| T2-40 | BCC-8fdf31c6 | Hedging Transaction Execution | `bcoc:HedgingTransactionExecution` | B | 4 | PASS | `8cddd97309477f744e505c4103da61b63a186a8ab3cc22dd217dbaf697e34a9f` |
| T2-42 | BCC-7757c12b | Treasury Policy Management | `bcoc:TreasuryPolicyManagement` | B | 5 | PASS | `08579dbf7b83f4269ee0226be37629d212633aca89102369032aed7687ef0a19` |

## 2. Final definitions and realization indexes

**T2-08 — Financial Reporting** (Batch A). A business capability of an organization to prepare its financial statements, and the reports drawn from them, and present them to its management, its board and outside parties, grounded in the organization's members as organized.

Index: `bpo:P10837`, `bpo:P10838`, `bpo:P10839`, `bpo:P10840`, `bpo:P10841`, `bpo:P10842`, `bpo:P10843`, `bpo:P14074`, `bpo:P10770`, `bpo:P11042`.

**T2-09 — Fixed-Asset Accounting** (Batch A). A business capability of an organization to record its fixed assets and account for their cost and its consumption over their useful lives, from acquisition to disposal, keeping the asset register consistent with the ledger, grounded in the organization's members as organized.

Index: `bpo:P10829`, `bpo:P10830`, `bpo:P10831`, `bpo:P10832`, `bpo:P10833`, `bpo:P10834`, `bpo:P10835`, `bpo:P10836`.

**T2-10 — General Ledger Accounting** (Batch A). A business capability of an organization to record its financial transactions in its ledgers by accepted accounting principles, close its books for each period, and keep its accounts reconciled, grounded in the organization's members as organized.

Index: `bpo:P10819`, `bpo:P10820`, `bpo:P10821`, `bpo:P10822`, `bpo:P10823`, `bpo:P10824`, `bpo:P10825`, `bpo:P10826`, `bpo:P10827`.

**T2-12 — Trade Product Classification** (Batch A). A business capability of an organization to classify the goods and services it trades under the tariff and control classifications that apply to them, grounded in the organization's members as organized.

Index: `bpo:P14092`.

**T2-13 — Restricted Party Screening** (Batch A). A business capability of an organization to check the parties it would trade with against the lists of sanctioned and restricted parties that apply, before and during its dealings with them, grounded in the organization's members as organized.

Index: `bpo:P14090`.

**T2-15 — Trade Preference Management** (Batch A). A business capability of an organization to establish that its goods qualify for reduced or zero duty under trade agreements and programs, and claim and document that treatment, grounded in the organization's members as organized.

Index: `bpo:P14096`.

**T2-16 — Internal Control Reporting** (Batch A). A business capability of an organization to report on the state of its internal controls, and on compliance with them, to those inside and outside it who need to know, grounded in the organization's members as organized.

Index: `bpo:P10923`, `bpo:P10924`, `bpo:P10925`, `bpo:P10926`.

**T2-18 — International Rate Monitoring** (Batch A). A business capability of an organization to follow the exchange and interest rates in the markets where it operates and bring them to those who manage its international funds, grounded in the organization's members as organized.

Index: `bpo:P10767`.

**T2-19 — Cross-Border Funds Transfer Management** (Batch A). A business capability of an organization to move money across borders for its trade and investments, converting between currencies and choosing the means of payment, grounded in the organization's members as organized.

Index: `bpo:P10768`.

**T2-22 — Time Reporting** (Batch A). A business capability of an organization to record, by period, the time its members work, are absent or bill, and make that record available to those who pay, bill or plan with it, grounded in the organization's members as organized.

Index: `bpo:P10854`, `bpo:P10855`, `bpo:P10856`, `bpo:P10857`.

**T2-28 — Accounts Receivable Processing** (Batch A). A business capability of an organization to record what its customers owe it, apply the payments they make, and keep each customer's account correct and current, grounded in the organization's members as organized.

Index: `bpo:P10800`, `bpo:P10801`, `bpo:P10802`, `bpo:P10803`.

**T2-29 — Customer Deduction and Adjustment Management** (Batch A). A business capability of an organization to investigate, resolve and record the deductions its customers take from their payments and the adjustments made to their accounts, grounded in the organization's members as organized.

Index: `bpo:P10810`, `bpo:P10811`, `bpo:P10812`, `bpo:P10813`, `bpo:P10814`.

**T2-30 — Collections Management** (Batch A). A business capability of an organization to pursue, settle or write off the amounts its customers owe and have not paid when due, grounded in the organization's members as organized.

Index: `bpo:P10805`, `bpo:P10806`, `bpo:P10807`, `bpo:P10808`, `bpo:P14007`.

**T2-34 — Tax Processing** (Batch A). A business capability of an organization to determine, declare, pay and account for the taxes it owes on its income, property, transactions and services, and keep the records that support them, grounded in the organization's members as organized.

Index: `bpo:P10931`, `bpo:P10932`, `bpo:P10933`, `bpo:P10934`, `bpo:P10935`, `bpo:P10936`.

**T2-36 — In-House Bank Account Management** (Batch A). A business capability of an organization to run accounts that its own units, subsidiaries among them, hold with a central treasury of the organization, and settle, lend and pay through those accounts as a bank would, grounded in the organization's members as organized.

Index: `bpo:P10902`, `bpo:P10903`, `bpo:P10904`, `bpo:P10905`, `bpo:P10906`, `bpo:P10907`.

**T2-39 — Foreign Exchange Risk Management** (Batch A). A business capability of an organization to measure its exposure to losses from changes in exchange rates, forecast their effect on it, and hedge that exposure where it chooses to, grounded in the organization's members as organized.

Index: `bpo:P19579`, `bpo:P19580`, `bpo:P19581`, `bpo:P19582`, `bpo:P19583`, `bpo:P10769`.

**T2-41 — Interest Rate Risk Management** (Batch A). A business capability of an organization to measure its exposure to losses from changes in interest rates on what it borrows and what it holds, and limit that exposure, grounded in the organization's members as organized.

Index: `bpo:P19575`, `bpo:P19576`, `bpo:P19577`, `bpo:P19578`.

**T2-01 — Payment Processing** (Batch B). A business capability of an organization to make the payments it has decided to make, by the means and on the dates due, and record each payment made, grounded in the organization's members as organized.

Index: `bpo:P10862`, `bpo:P10876`.

**T2-03 — Expense Reimbursement Processing** (Batch B). A business capability of an organization to repay the expenses its members claim for work done on its behalf, once accepted, and account and report for them, grounded in the organization's members as organized.

Index: `bpo:P10881`, `bpo:P10883`, `bpo:P10884`.

**T2-05 — Capital Project Accounting** (Batch B). A business capability of an organization to account for the costs of capital projects while they are under way, and transfer them to fixed assets when the projects are complete, grounded in the organization's members as organized.

Index: `bpo:P10848`, `bpo:P10849`, `bpo:P10850`, `bpo:P10851`.

**T2-07 — Accounting Policy Management** (Batch B). A business capability of an organization to formulate, publish and revise the accounting and financial-reporting policies and procedures its members follow, grounded in the organization's members as organized.

Index: `bpo:P10816`, `bpo:P20604`.

**T2-11 — Letter of Credit Management** (Batch B). A business capability of an organization to arrange letters of credit for its trade, by which a bank assures payment to a seller once agreed conditions are met, grounded in the organization's members as organized.

Index: `bpo:P14098`.

**T2-14 — Trade and Customs Documentation** (Batch B). A business capability of an organization to prepare and keep the records of its cross-border shipments, value them and calculate the duty on them, and give customs authorities the declarations they call for, grounded in the organization's members as organized.

Index: `bpo:P14095`, `bpo:P14094`, `bpo:P19593`, `bpo:P14093`.

**T2-20 — Pay Management** (Batch B). A business capability of an organization to determine the pay each employee is owed for a period, gross and after deductions, bonuses and other compensation included, and carry it through to payment, grounded in the organization's members as organized.

Index: `bpo:P10858`, `bpo:P10859`, `bpo:P10860`, `bpo:P10861`, `bpo:P10862`, `bpo:P10863`, `bpo:P10864`, `bpo:P10865`.

**T2-21 — Payroll Tax Processing** (Batch B). A business capability of an organization to calculate, remit and report the taxes due on its employees' pay, grounded in the organization's members as organized.

Index: `bpo:P10866`, `bpo:P10867`, `bpo:P10868`.

**T2-23 — Cost Accounting** (Batch B). A business capability of an organization to determine what its products, services, processes and projects cost, by recording, allocating and analyzing their costs, grounded in the organization's members as organized.

Index: `bpo:P10774`, `bpo:P10775`, `bpo:P10776`, `bpo:P10777`.

**T2-26 — Financial Planning, Budgeting and Forecasting** (Batch B). A business capability of an organization to prepare budgets and plans for its parts and future periods, forecast its financial results and position, and analyze actual results against them, grounded in the organization's members as organized.

Index: `bpo:P10772`, `bpo:P10773`, `bpo:P20136`.

**T2-32 — Customer Invoicing** (Batch B). A business capability of an organization to prepare and send its customers invoices for what it has sold them, and correct those invoices when needed, grounded in the organization's members as organized.

Index: `bpo:P10794`, `bpo:P10795`, `bpo:P10796`, `bpo:P10797`, `bpo:P10798`.

**T2-33 — Tax Planning** (Batch B). A business capability of an organization to assess the tax effects of its financial position and of what it intends to do, and formulate and consolidate its tax strategy, grounded in the organization's members as organized.

Index: `bpo:P10927`, `bpo:P10928`.

**T2-35 — Cash Management** (Batch B). A business capability of an organization to track its cash positions across its accounts and move cash among them, to position it where it is used, grounded in the organization's members as organized.

Index: `bpo:P10893`, `bpo:P10895`, `bpo:P10898`.

**T2-38 — Counterparty Credit Exposure Management** (Batch B). A business capability of an organization to measure the credit exposure it has to its customers and other counterparties, resolve breaches of the limits set on it, manage the collateral held against it, and review it periodically, grounded in the organization's members as organized.

Index: `bpo:P19584`, `bpo:P19585`, `bpo:P19586`, `bpo:P19587`.

**T2-40 — Hedging Transaction Execution** (Batch B). A business capability of an organization to measure the positions to be hedged, select and establish hedges, and evaluate, refine and unwind them, grounded in the organization's members as organized.

Index: `bpo:P19588`, `bpo:P19589`, `bpo:P19590`, `bpo:P11213`.

**T2-42 — Treasury Policy Management** (Batch B). A business capability of an organization to formulate, publish and keep current the rules and procedures under which its treasury invests, borrows, hedges and handles cash, grounded in the organization's members as organized.

Index: `bpo:P10886`, `bpo:P10887`, `bpo:P10888`, `bpo:P10889`, `bpo:P10890`.

## 3. Signature

To be completed by the signing reviewer only. As for tranche 1, the signature is his own confirmation given in session, transcribed verbatim with a decision record citing this file's SHA-256. Claude Code does not complete it. A class he does not confirm stays unadmitted, and a FAIL is reclassified or removed, not staged (b4).

| Finding (PASS / FAIL) | Classes | Reviewer | Date | Notes |
|---|---|---|---|---|
|  |  |  |  |  |
