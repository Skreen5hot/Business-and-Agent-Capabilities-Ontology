# Semantic-curation tranche 2 — PCF 9.0 Financial Resources Management

| Field | Value |
|---|---|
| Status | **Curated**, for the architect's review of the issues in section 6. Admits no class: G1-T admission, the Stage 03 standard and Stage 05 stay the architect's (`docs/decisions/2026-11-07-curation-tranche-2-approved.md`, C) |
| Date | 2026-11-07 |
| Scope | `BCC-4fda51aa` and the 72 candidates beneath it, plus `BCC-ded8ed18` (PCF 9.8.2), which the generator's cycle-breaking left outside the walk |
| Records | `docs/catalog/tranche-2-review.yaml` (every disposition and link); `src/01_controlled_vocabulary/catalog.yaml` (the concepts); `docs/catalog/dispositions.yaml` (merges, rejections, pins) |
| Standard | `docs/proposals/2026-11-07-stage-03-taxonomy-standard.md`, **proposed**: the links below are *classified*, not validated, until it is approved |

## 1. The figures

| Measure | Value |
|---|---|
| Candidates dispositioned, of 72 | **72**: 63 accepted, 5 merged, 3 rejected, 1 deferred. The root and the 9.8.2 addition are accepted too |
| Distinct normalized concepts | **65**: 64 new, and the pilot `bcoc:TreasuryManagement` revised (alternative label, broader, candidate). The vocabulary now holds 69 catalog concepts |
| Definitions reviewed and accepted | **64 of 65**, after the synthetic domain review (section 4). The pilot Treasury Management keeps its definition, pending its next revision (R26). Payroll Processing and Accounts Payable Processing carry their signed tranche-1 definitions unchanged |
| Proposed links | **89**, every one classified: 60 kept (4 of them reclassified from the PCF reading to specialization), 2 re-targeted, 11 rejected or dropped as incorrect, 3 kept with a target outside the tranche, 4 redundant, 6 carried by a merge, 3 held |
| Links added by review | **7** |
| `broader` written to the vocabulary | 66, each a kept specialization or component between two tranche concepts |
| Ready for G1-T admission | **43** (section 5); 2 already admitted (T1-02, T1-03); 15 not ready; 5 capability areas not proposed |

## 2. Dispositions that are not acceptances

| Candidate | Disposition | Into / reason |
|---|---|---|
| BCC-9ecf360b Payments Approval | rejected | rejected 2026-11-04 (tranche 1, act 5); unchanged |
| BCC-b7928257 Currency Conversion | rejected | one act episode (converting a foreign-currency value to local currency, for customs valuation under PCF 9.11): realization evidence for Trade and Customs Documentation, as duty calculation is; not a capability type |
| BCC-6daa0467 Customs Communication | merged | → BCC-c5e7dca0 (Trade and Customs Documentation). communicating with customs is giving customs authorities the information the law requires, which trade documentation records; one ability |
| BCC-46cbe926 Duty Calculation | rejected | one act episode with no process beneath it (calculating a duty for customs valuation): realization evidence for Trade and Customs Documentation, not a capability type. The generator's classification is confirmed |
| BCC-6ae95cc4 Restitution Handling | deferred | a likely homonym: the source describes restitution and fines owed to authorities, while in trade-compliance practice 'restitution' usually names export refunds owed to the organization. No concept is written until the source's sense is settled |
| BCC-8fc1f306 Currency Exposure Monitoring | merged | → BCC-7c04ea8a (Foreign Exchange Risk Management). PCF 9.10.3 (currency exposure and hedging) and 9.7.5.3 (foreign exchange risk) describe one ability under two branches; the generator's keys differ only in wording |
| BCC-5caed753 Results Reporting (in International Funds and Consolidation Management) | merged | → BCC-792537f9 (Financial Reporting). PCF 9.10.4 reports foreign exchange gains and losses: financial reporting restricted to one source of results (its recording of the entries is General Ledger Accounting's work). Its second record, PCF 13.3.2.2.2, is a homonym the key merged; it stays in the crosswalk as evidence |
| BCC-18ef14d6 Financial Results Reporting | merged | → BCC-792537f9 (Financial Reporting). reporting financial results to the board (PCF 12.3.1) is financial reporting to one audience |
| BCC-aebe5ec1 In-house Bank Accounts for Subsidiaries Management | merged | → BCC-749adb52 (In-House Bank Account Management). the in-house bank's accounts for subsidiaries are the main scope of in-house banking, not a separate ability; named in the concept's definition |

## 3. The concepts

By batch. *Area* marks a broad or conjunctive capability area, not proposed for G1-T (CD16, E4).

**Batch 1, treasury and international funds.**

| Concept | Preferred label | Candidates | Broader | G1-T |
|---|---|---|---|---|
| `bcoc:FinancialResourceManagement` | Financial Resource Management *(area)* | BCC-4fda51aa | — | not proposed: a capability area |
| `bcoc:InternationalFundsManagement` | International Funds Management | BCC-87e3a26b | Financial Resource Management, Treasury Management | not ready: no act type in its evidence |
| `bcoc:InternationalRateMonitoring` | International Rate Monitoring | BCC-5dfa2101 | International Funds Management | ready |
| `bcoc:CrossBorderFundsTransferManagement` | Cross-Border Funds Transfer Management | BCC-bf62316a | International Funds Management | ready |
| `bcoc:TreasuryManagement` | Treasury Management | BCC-0ba10d44 | Financial Resource Management | not ready: every act type in its evidence is typed under a capability class (Q-12) |
| `bcoc:CashManagement` | Cash Management | BCC-a1c5454d | Treasury Management | ready |
| `bcoc:BankingRelationshipManagement` | Banking Relationship Management | BCC-a750d13a | Cash Management, Financial Intermediary Relationship Management | not ready: every act type in its evidence is typed under a capability class (Q-12) |
| `bcoc:CashEquivalentManagement` | Cash Equivalent Management | BCC-314dba7d | Cash Management | not ready: every act type in its evidence is typed under a capability class (Q-12) |
| `bcoc:CashFlowManagement` | Cash Flow Management | BCC-d71abe9a | Cash Management | not ready: every act type in its evidence is typed under a capability class (Q-12) |
| `bcoc:DebtAndInvestmentManagement` | Debt and Investment Management *(area)* | BCC-ec93ca56 | Treasury Management | not proposed: a capability area |
| `bcoc:FinancialIntermediaryRelationshipManagement` | Financial Intermediary Relationship Management | BCC-d6966c88 | Debt and Investment Management | not ready: every act type in its evidence is typed under a capability class (Q-12) |
| `bcoc:IssuerCreditExposureManagement` | Issuer Credit Exposure Management | BCC-13b94120 | Debt and Investment Management, Counterparty Credit Exposure Management | not ready: every act type in its evidence is typed under a capability class (Q-12) |
| `bcoc:LiquidityManagement` | Liquidity Management | BCC-4464d04f | Treasury Management | not ready: every act type in its evidence is typed under a capability class (Q-12) |
| `bcoc:FinancialFraudAndDisputeCaseManagement` | Financial Fraud and Dispute Case Management | BCC-9b5ec2fd | Treasury Management | not ready: every act type in its evidence is typed under a capability class (Q-12) |
| `bcoc:InHouseBankAccountManagement` | In-House Bank Account Management | BCC-749adb52, BCC-aebe5ec1 | Treasury Management | ready |
| `bcoc:FinancialRiskManagement` | Financial Risk Management | BCC-132e1b29 | Treasury Management | ready |
| `bcoc:CounterpartyCreditExposureManagement` | Counterparty Credit Exposure Management | BCC-3e668a26 | Financial Risk Management | ready |
| `bcoc:ForeignExchangeRiskManagement` | Foreign Exchange Risk Management | BCC-7c04ea8a, BCC-8fc1f306 | Financial Risk Management | ready |
| `bcoc:HedgingTransactionExecution` | Hedging Transaction Execution | BCC-8fdf31c6 | Financial Risk Management | ready |
| `bcoc:InterestRateRiskManagement` | Interest Rate Risk Management | BCC-0564598d | Financial Risk Management | ready |
| `bcoc:TreasuryPolicyManagement` | Treasury Policy Management | BCC-7757c12b | Treasury Management | ready |

**Batch 2, accounting areas.**

| Concept | Preferred label | Candidates | Broader | G1-T |
|---|---|---|---|---|
| `bcoc:CapitalExpenditureManagement` | Capital Expenditure Management *(area)* | BCC-9305456f | Financial Resource Management | not proposed: a capability area |
| `bcoc:CapitalPlanning` | Capital Planning | BCC-15e92684 | Capital Expenditure Management | ready |
| `bcoc:CapitalProjectAccounting` | Capital Project Accounting | BCC-95b092a2 | Capital Expenditure Management | ready |
| `bcoc:FinancialAccounting` | Financial Accounting | BCC-60d672db | Financial Resource Management | ready |
| `bcoc:AccountingPolicyManagement` | Accounting Policy Management | BCC-e8acc1f8 | Financial Accounting | ready |
| `bcoc:FinancialReporting` | Financial Reporting | BCC-792537f9, BCC-5caed753, BCC-18ef14d6 | Financial Accounting | ready |
| `bcoc:FixedAssetAccounting` | Fixed-Asset Accounting | BCC-e3c8bd37 | Financial Accounting | ready |
| `bcoc:GeneralLedgerAccounting` | General Ledger Accounting | BCC-8b431985 | Financial Accounting | ready |
| `bcoc:FinancialPlanningAndManagementAccounting` | Financial Planning and Management Accounting | BCC-ca61edb4 | Financial Resource Management | not ready: every act type in its evidence is typed under a capability class (Q-12) |
| `bcoc:CostAccounting` | Cost Accounting | BCC-302a390a | Financial Planning and Management Accounting | ready |
| `bcoc:CostManagement` | Cost Management | BCC-b47b8fed | Financial Planning and Management Accounting | ready |
| `bcoc:FinancialPerformanceManagement` | Financial Performance Management | BCC-cedf0899 | Financial Planning and Management Accounting | ready |
| `bcoc:ContinuousCostImprovement` | Continuous Cost Improvement | BCC-3421f274 | Cost Management | not ready: every act type in its evidence is typed under a capability class (Q-12) |
| `bcoc:FinancialPlanningBudgetingAndForecasting` | Financial Planning, Budgeting and Forecasting | BCC-87e1811c | Financial Planning and Management Accounting | ready |
| `bcoc:RevenueAndReceivablesManagement` | Revenue and Receivables Management | BCC-1cccc689 | Financial Resource Management | ready |
| `bcoc:AccountsReceivableProcessing` | Accounts Receivable Processing | BCC-6587dedf | Revenue and Receivables Management | ready |
| `bcoc:CustomerDeductionManagement` | Customer Deduction and Adjustment Management | BCC-cebf0da8 | Revenue and Receivables Management | ready |
| `bcoc:CollectionsManagement` | Collections Management | BCC-c4904759 | Revenue and Receivables Management | ready |
| `bcoc:DefaultAccountManagement` | Default Account Management | BCC-38b3c836 | Collections Management | not ready: every act type in its evidence is typed under a capability class (Q-12) |
| `bcoc:CustomerCreditManagement` | Customer Credit Management | BCC-b7ff0eac | Revenue and Receivables Management | ready |
| `bcoc:CustomerInvoicing` | Customer Invoicing | BCC-8a70a337 | Revenue and Receivables Management | ready |

**Batch 3, payables, payroll, tax, trade and internal control.**

| Concept | Preferred label | Candidates | Broader | G1-T |
|---|---|---|---|---|
| `bcoc:PayablesAndReimbursementManagement` | Accounts Payable and Expense Reimbursement Management *(area)* | BCC-0fe1f7f0 | Financial Resource Management | not proposed: a capability area |
| `bcoc:AccountsPayableProcessing` | Accounts Payable Processing | BCC-62e789bf | Accounts Payable and Expense Reimbursement Management | admitted: T1-03, signed PASS 2026-11-05 |
| `bcoc:PaymentProcessing` | Payment Processing | BCC-9511900a | Accounts Payable Processing, Pay Management | ready |
| `bcoc:CorporateCardManagement` | Corporate Card Management | BCC-ea6d1c4a | Accounts Payable and Expense Reimbursement Management | ready |
| `bcoc:ExpenseReimbursementProcessing` | Expense Reimbursement Processing | BCC-35c8111b | Accounts Payable and Expense Reimbursement Management | ready |
| `bcoc:GlobalTradeManagement` | Global Trade Management *(area)* | BCC-05445216 | — | not proposed: a capability area |
| `bcoc:ExportAndImportControl` | Export and Import Control | BCC-cd7f1007 | Global Trade Management | not ready: no act type in its evidence |
| `bcoc:LetterOfCreditManagement` | Letter of Credit Management | BCC-4f5c2f36 | Global Trade Management | ready |
| `bcoc:TradeProductClassification` | Trade Product Classification | BCC-e1fa4843 | Global Trade Management | ready |
| `bcoc:RestrictedPartyScreening` | Restricted Party Screening | BCC-f6799472 | Global Trade Management | ready |
| `bcoc:TradeDocumentation` | Trade and Customs Documentation | BCC-c5e7dca0, BCC-6daa0467 | Global Trade Management | ready |
| `bcoc:TradePreferenceManagement` | Trade Preference Management | BCC-0c80b752 | Global Trade Management | ready |
| `bcoc:InternalControl` | Internal Control | BCC-5a4bc396 | — | not ready: every act type in its evidence is typed under a capability class (Q-12) |
| `bcoc:InternalControlReporting` | Internal Control Reporting | BCC-b55668bc | Internal Control | ready |
| `bcoc:InternalControlDesign` | Internal Control Design | BCC-80a63f8e | Internal Control | ready |
| `bcoc:PayrollProcessing` | Payroll Processing | BCC-d95f68fd, BCC-b7c46718 | Financial Resource Management | admitted: T1-02, signed PASS 2026-11-05 |
| `bcoc:PayManagement` | Pay Management | BCC-d105ff07 | Payroll Processing | ready |
| `bcoc:PayrollTaxProcessing` | Payroll Tax Processing | BCC-394909c1 | Payroll Processing, Tax Management | ready |
| `bcoc:TimeReporting` | Time Reporting | BCC-85fbcb90 | — | ready |
| `bcoc:TaxManagement` | Tax Management | BCC-c64ca466 | Financial Resource Management | not ready: every act type in its evidence is typed under a capability class (Q-12) |
| `bcoc:TaxPlanning` | Tax Planning | BCC-ce052840 | Tax Management | ready |
| `bcoc:TaxProcessing` | Tax Processing | BCC-52f0795a | Tax Management | ready |
| `bcoc:InternalControlOperation` | Internal Control Operation and Monitoring | BCC-ded8ed18 | Internal Control | ready |

## 4. The synthetic domain review

One review of the whole tranche, as the decision directs (A5). **Reviewer:** synthetic domain practitioner (finance, treasury, controllership), `claude-opus-5-5`, an independent agent instance given the files and the project's rules but not the drafter's reasoning. **Capacity:** the product-owner-authorized synthetic practitioner (`docs/decisions/2026-11-02-r11-practitioner-validation-decided.md`). **Verdict:** accept with substantive corrections. 30 findings, 19 substantive. The drafter checked the three findings that turned on the evidence against the PCF records (R1, R3, R13), and they held.

Applied: every substantive finding, and the routine findings that changed a text. The main changes:

- R1: `BCC-3e668a26` re-read from its child elements as **Counterparty Credit Exposure Management**, not investment concentration; Issuer Credit Exposure Management now specializes it
- R3: the deferred `BCC-cebf0da8` accepted as **Customer Deduction and Adjustment Management**, from PCF 9.2.5's children
- R4, R5, R6, R7: Revenue and Receivables Management (recognition, not plan comparison); Financial Planning and Management Accounting, broad enough for its components; Financial Performance Management as profitability; Accounting Policy Management narrowed, and its added link from Treasury Policy dropped
- R2, R14, R21, R22: one specialization upheld by broadening Collections (PCF 9.2.4.5 writes off); one rejected as a containment artifact; three direct links to Risk Management made redundant by linking Financial Risk Management once; the root's outward link re-reasoned
- R12: Internal Control and Global Trade Management fail the coverage test against Financial Resource Management, so their links to it are **held** as PCF placements (section 6)
- R13: PCF 9.8.2 (`BCC-ded8ed18`) curated as **Internal Control Operation and Monitoring**, a component of Internal Control
- R16, R17: currency conversion rejected like duty calculation, both as customs-valuation acts; trade restitution deferred as a likely homonym
- R8, R9, R10: readiness notes name the acts each index excludes
- R15, R20, R25, R27, R30 and others: definitions no longer phrased by success, no longer listing practices that would exclude organizations; non-synonym alternative labels removed

Not applied: R26 (re-phrase the pilot Treasury Management in the tranche-2 pattern) waits for that record's next revision; R24 (a parent for Time Reporting) and R29 (tax accounting) are recorded in section 6.

## 5. Candidates ready for G1-T admission

*Ready* means an accepted capability type with a reviewed definition, a classified position, and at least one act type in its evidence that BPO types as an act, so that a realization index can be drawn. It is not an admission: each needs its G1-T record and a reviewer's PASS.

| Candidate | Concept | Acts usable / in evidence | Notes for the index |
|---|---|---|---|
| BCC-9511900a | Payment Processing | 2 / 2 | — |
| BCC-ea6d1c4a | Corporate Card Management | 7 / 7 | the index excludes its deontic acts (G1-T question 4); a development act needs a recorded reason (CAP-06) |
| BCC-35c8111b | Expense Reimbursement Processing | 6 / 6 | the index excludes its deontic acts (G1-T question 4) |
| BCC-15e92684 | Capital Planning | 5 / 5 | — |
| BCC-95b092a2 | Capital Project Accounting | 6 / 6 | — |
| BCC-60d672db | Financial Accounting | 1 / 1 | — |
| BCC-e8acc1f8 | Accounting Policy Management | 5 / 5 | the index excludes P10817 (setting approval limits: deontic) and P10815 (service-level agreements: not policy work); P10818 (common financial systems) needs a CAP-06 record or is out |
| BCC-792537f9 | Financial Reporting | 9 / 9 | — |
| BCC-e3c8bd37 | Fixed-Asset Accounting | 10 / 10 | — |
| BCC-8b431985 | General Ledger Accounting | 10 / 10 | — |
| BCC-4f5c2f36 | Letter of Credit Management | 1 / 1 | — |
| BCC-e1fa4843 | Trade Product Classification | 3 / 3 | the index takes only PCF 9.11.3's acts; the homonym records' are out |
| BCC-f6799472 | Restricted Party Screening | 1 / 1 | — |
| BCC-c5e7dca0 | Trade and Customs Documentation | 1 / 1 | — |
| BCC-0c80b752 | Trade Preference Management | 1 / 1 | — |
| BCC-b55668bc | Internal Control Reporting | 5 / 5 | — |
| BCC-80a63f8e | Internal Control Design | 6 / 6 | a development act needs a recorded reason (CAP-06) |
| BCC-5dfa2101 | International Rate Monitoring | 1 / 1 | — |
| BCC-bf62316a | Cross-Border Funds Transfer Management | 1 / 1 | — |
| BCC-d105ff07 | Pay Management | 9 / 9 | — |
| BCC-394909c1 | Payroll Tax Processing | 5 / 5 | — |
| BCC-85fbcb90 | Time Reporting | 6 / 6 | — |
| BCC-302a390a | Cost Accounting | 7 / 7 | — |
| BCC-b47b8fed | Cost Management | 5 / 5 | — |
| BCC-cedf0899 | Financial Performance Management | 7 / 8 | — |
| BCC-87e1811c | Financial Planning, Budgeting and Forecasting | 6 / 6 | — |
| BCC-1cccc689 | Revenue and Receivables Management | 1 / 1 | — |
| BCC-6587dedf | Accounts Receivable Processing | 6 / 6 | — |
| BCC-cebf0da8 | Customer Deduction and Adjustment Management | 7 / 7 | — |
| BCC-c4904759 | Collections Management | 7 / 7 | — |
| BCC-b7ff0eac | Customer Credit Management | 8 / 8 | — |
| BCC-8a70a337 | Customer Invoicing | 6 / 6 | — |
| BCC-ce052840 | Tax Planning | 4 / 4 | — |
| BCC-52f0795a | Tax Processing | 8 / 8 | — |
| BCC-a1c5454d | Cash Management | 5 / 9 | P10896 (cash flow forecasts: Cash Flow Management's) and P10900 (bank fees: Banking Relationship Management's) are out |
| BCC-749adb52 | In-House Bank Account Management | 6 / 8 | — |
| BCC-132e1b29 | Financial Risk Management | 2 / 7 | — |
| BCC-3e668a26 | Counterparty Credit Exposure Management | 4 / 5 | — |
| BCC-7c04ea8a | Foreign Exchange Risk Management | 5 / 6 | — |
| BCC-8fdf31c6 | Hedging Transaction Execution | 5 / 6 | — |
| BCC-0564598d | Interest Rate Risk Management | 4 / 5 | — |
| BCC-7757c12b | Treasury Policy Management | 8 / 9 | P10885 (establishing treasury governance) needs a CAP-06 record; P10891 (treasury internal controls: Internal Control Design's) and P10892 (system security requirements) are out |
| BCC-ded8ed18 | Internal Control Operation and Monitoring | 3 / 3 | — |

**Not ready:** Export and Import Control (no act type in its evidence); Internal Control (every act type in its evidence is typed under a capability class (Q-12)); International Funds Management (no act type in its evidence); Financial Planning and Management Accounting (every act type in its evidence is typed under a capability class (Q-12)); Continuous Cost Improvement (every act type in its evidence is typed under a capability class (Q-12)); Default Account Management (every act type in its evidence is typed under a capability class (Q-12)); Tax Management (every act type in its evidence is typed under a capability class (Q-12)); Treasury Management (every act type in its evidence is typed under a capability class (Q-12)); Banking Relationship Management (every act type in its evidence is typed under a capability class (Q-12)); Cash Equivalent Management (every act type in its evidence is typed under a capability class (Q-12)); Cash Flow Management (every act type in its evidence is typed under a capability class (Q-12)); Financial Intermediary Relationship Management (every act type in its evidence is typed under a capability class (Q-12)); Issuer Credit Exposure Management (every act type in its evidence is typed under a capability class (Q-12)); Liquidity Management (every act type in its evidence is typed under a capability class (Q-12)); Financial Fraud and Dispute Case Management (every act type in its evidence is typed under a capability class (Q-12)).

## 6. For the architect: material issues and source limitations

1. **Q-12 holds back the concepts whose only act type is BPO's designating class.** BPO types the designating act class of many candidates, treasury's above all, under a capability class. The readiness counts use only the PCF processes beneath, which BPO types as acts. Where none exists, the concept waits for BPO: 13 concepts, listed in section 5 as not ready.
2. **Two components of the root fail its coverage test (R12).** Internal Control (operations, reporting and compliance) and Global Trade Management (export control, screening, classification) are placed under PCF 9.0, but neither is financial resource work. Their links are held, not written. A governance, risk and compliance parent, and a trade-compliance parent, belong to later domains. The alternative, narrowing Internal Control to control over financial reporting, would change its meaning; that choice is the architect's.
3. **Re-targetings that depart from PCF.** Liquidity Management sits under Treasury Management, not Debt and Investment. Continuous Cost Improvement specializes Cost Management. International Funds Management is also a component of Treasury Management. Each is reasoned in the review record.
4. **PCF 9.10 'consolidation' read as cash concentration**, from its description, not financial consolidation, which is PCF 9.3.4.8 under Financial Reporting.
5. **Payroll tax.** It is kept as a *component* of Tax Management, not a specialization, so that payroll tax operations stay distinct from tax planning and general tax processing (decision of 2026-11-04, act 3).
6. **Debt and Investment Management stays conjunctive**, as an area. Whether to split it is open.
7. **Homonyms the generator merged.** `BCC-e1fa4843` merged trade product classification with two product-evaluation records, and `BCC-5caed753` merged foreign exchange results reporting with an evaluation summary. The concepts take the trade and reporting senses, and the indexes exclude the homonyms' acts.
8. **Likely duplicates outside the tranche**, for the domains that hold them: `BCC-93d835ff` (financial policy), `BCC-b26e4444` (fixed-asset project accounting), `BCC-336f001a` (global trade), `BCC-5ff7b78f` (restitution), `BCC-eb85d5ea` (international funds), `BCC-7ec6ff6b` (payments).
9. **Gaps.** Time Reporting has no broader after the tranche-1 dependency finding; its parent is in workforce management (PCF 7.x). Tax accounting (income tax provision) has no concept here.
10. **Source limitations.** PCF 7.4 is the only source for most concepts: 24 candidates had two or more sources, and the BRM supports only Time Reporting and Payroll. PCF descriptions are short and sometimes garbled (9.2.5), so the children were read where the description was thin.
11. **Two deferrals**, `BCC-6ae95cc4` (restitution) and, before the review, `BCC-cebf0da8`, show where a reader's judgement settled what the source left open.

## 7. Recommendation for scaling across the catalog

The tranche took one decision, one review and one report. The rest of the catalog can follow the same path **without a new proposal or decision per domain**:

1. **Approve the Stage 03 standard once**, and with it a standing rule. A domain is curated under the standard and this tranche's practice (`tranche-<n>-review.yaml`, concepts with `catalog_candidates`, dispositions, one report), with no proposal of its own.
2. **One synthetic domain review per domain**, given the files and the rules, not the drafter's reasoning. Substantive findings are applied or escalated; the architect sees only the consolidated issues (this report's section 6) and one G1-T batch per domain.
3. **G1-T in batches.** This tranche leaves 43 candidates ready. One batch per domain, each record drafted from the ready list and its index notes, signed by the named reviewer, keeps admission from becoming the bottleneck.
4. **Order by readiness and overlap**, from the generated catalog (candidates beneath each top-level function, *likely* capabilities first):
    Business Capabilities Development and Management (`BCC-d3d393bd`, 77 likely); Human Capital Development and Management (`BCC-1eb6fb26`, 55 likely); Vision and Strategy Development (`BCC-86cffc27`, 40 likely); Products and Services Marketing and Selling (`BCC-bd41c4ec`, 39 likely); Assets Acquisition, Construction and Management (`BCC-e12d8a9d`, 30 likely); External Relationship Management (`BCC-2f433e00`, 26 likely); Supply Chain for Physical Products Management (`BCC-0784e083`, 24 likely); Enterprise Risk Compliance Remediation and Resiliency Management (`BCC-230d43c6`, 21 likely); Services Delivery (`BCC-89a29da5`, 16 likely). Human capital comes next: it holds tranche 1's Employees Reward and Retention, and Time Reporting's missing parent. Each domain also settles the duplicates this one found for it (section 6, item 8).
5. **Carry the lessons into the practice, not into new tooling:**
    - read the source's child elements where a description is thin (R1, R3);
    - test each component link against the broader's definition, not the hierarchy alone (R12);
    - walk the scope by source code as well as by generated links, since the generator's cycle-breaking can drop an element (R13);
    - use alternative labels for synonyms only (R19).

    The scripts that wrote this tranche's records stayed outside the repository, as the decision asks (D).
6. **Raise Q-12 with BPO.** It is the largest single block on G1-T readiness here, and sending that message is the architect's call.

## 8. Boundary

No OWL, subclass axiom, object property or G1-T admission. No change to the generator. The generated catalog is regenerated from the dispositions, and the crosswalk keeps every source record.
