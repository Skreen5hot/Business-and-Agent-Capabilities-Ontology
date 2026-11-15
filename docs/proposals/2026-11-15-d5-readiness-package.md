# D5 — formalization readiness package, first Business Capability tranche

| Field | Value |
|---|---|
| Status | **For the architect's approval** (direction of 2026-11-15, F, `docs/decisions/2026-11-15-tranche-2-remaining-issues-and-d5-preparation.md`). It authorizes no Stage 05 implementation and no OWL capability class. Section 1 lists what is asked |
| Date | 2026-11-15 |
| Prepared by | Claude Code (`claude-opus-5-5`), for the BCO team |
| Baseline | `main` at `e41eb072b32f8ce726ded8d71d16c17f400f4764`, PR #51 merged. Upstream pins: BFO `044490fc`, CCO `510dad76`, BPO `bc64e918` (`config/upstream-sources.yaml`) |
| Roadmap row | D5, formalization readiness: the Stage 05 standard; the validation architecture; the first tranche's reviewed terminology and taxonomy baseline; the BPO dependencies Q-12 to Q-14 validated |

Derived in part from the APQC Process Classification Framework® 7.4 (element names and
IDs, under APQC's notice in `NOTICE.md`). APQC does not endorse this work.

## 1. What is asked

| Id | Decision | Recommendation |
|---|---|---|
| D5-1 | Approve the Stage 05 standard, `docs/proposals/2026-11-15-stage-05-ontology-standard.md` | Approve |
| D5-2 | Approve its validation architecture (standard §5): the per-commit checks S05-T1, S05-C1 to S05-C9 and S05-B; ELK per commit; HermiT at the checkpoint | Approve |
| D5-3 | Approve the first tranche's readiness (section 2): `bco:BusinessCapability` and 39 admitted types. The other 3 join as each passes its source check | Approve |
| D5-4 | Settle the roadmap's T1, T2 and T3 dependencies for this tranche (section 7, B1) | Accept this package's terminology review (section 3) as T2's acceptance of the 42 terms, for formalization only. Defer T1 and T3, which do not touch these classes |
| D5-5 | Approve widening the BPO extract (Q-14; section 6.3) | Approve, using the existing vendoring tool |
| D5-6 | Confirm how CD12 applies to BCO-minted classes (section 6.4) | Each index is written from the signed G1-T record, and S05-T1 checks it against that record. BPO's `capability_scope.json` is not used for these classes |
| D5-7 | Approve adding the reasoners ELK and HermiT, through a pinned ROBOT jar, as a validation dependency (section 7, B4) | Approve. Java 23 is present; no reasoner is installed today |

Once D5-1 to D5-3 are approved, Stage 05 implementation still needs its own go-ahead from
the architect (direction F: "Return the readiness package for my approval before
generating OWL capability classes").

## 2. The proposed first tranche

**One module:** `src/05_ontology/apqc-cap.ttl`.

**What it holds:** the parent and the specific capability classes, each placed under
standard S3, and nothing else.

**What it does not hold:**

- the description layer (`apqc-cap-desc.ttl`), whose terms T3 has not yet reconciled;
- K2 unions and `only` restrictions, since no CAP-30 review exists;
- the coverage register (CD16; its location is fixed at Stage 06);
- any individual.

| G1-T | Concept | Proposed class | Label | Index | Concept record digest | Readiness |
|---|---|---|---|---|---|---|
| — | `bcom:BusinessCapability` | `bco:BusinessCapability` | Business Capability | — (the parent; CAP-03 excepts it) | see `metamodel.yaml` | admitted by ratification, RP-1 (CD3) |
| T1-02 | `bcoc:PayrollProcessing` | `bco:PayrollProcessing` | Payroll Processing | 11 | `defbd4f3400f…` | ready |
| T1-03 | `bcoc:AccountsPayableProcessing` | `bco:AccountsPayableProcessing` | Accounts Payable Processing | 7 | `7d60551d0870…` | ready |
| T2-08 | `bcoc:FinancialReporting` | `bco:FinancialReporting` | Financial Reporting | 10 | `84e3c1a7ea9b…` | ready |
| T2-09 | `bcoc:FixedAssetAccounting` | `bco:FixedAssetAccounting` | Fixed-Asset Accounting | 8 | `d7432dbd9211…` | ready |
| T2-10 | `bcoc:GeneralLedgerAccounting` | `bco:GeneralLedgerAccounting` | General Ledger Accounting | 9 | `d7c19172b362…` | ready |
| T2-12 | `bcoc:TradeProductClassification` | `bco:TradeProductClassification` | Trade Product Classification | 1 | `578838efeef4…` | ready |
| T2-13 | `bcoc:RestrictedPartyScreening` | `bco:RestrictedPartyScreening` | Restricted Party Screening | 1 | `1e5990ec6e5b…` | ready |
| T2-15 | `bcoc:TradePreferenceManagement` | `bco:TradePreferenceManagement` | Trade Preference Management | 1 | `c005bde58329…` | ready |
| T2-16 | `bcoc:InternalControlReporting` | `bco:InternalControlReporting` | Internal Control Reporting | 4 | `f92d82551826…` | ready |
| T2-18 | `bcoc:InternationalRateMonitoring` | `bco:InternationalRateMonitoring` | International Rate Monitoring | 1 | `768596eaf4e8…` | ready |
| T2-19 | `bcoc:CrossBorderFundsTransferManagement` | `bco:CrossBorderFundsTransferManagement` | Cross-Border Funds Transfer Management | 1 | `7d28476b319f…` | ready |
| T2-22 | `bcoc:TimeReporting` | `bco:TimeReporting` | Time Reporting | 4 | `eee8ad6a3634…` | ready |
| T2-28 | `bcoc:AccountsReceivableProcessing` | `bco:AccountsReceivableProcessing` | Accounts Receivable Processing | 4 | `fb5d4e1f8541…` | ready |
| T2-29 | `bcoc:CustomerDeductionManagement` | `bco:CustomerDeductionManagement` | Customer Deduction and Adjustment Management | 5 | `955724f77555…` | ready |
| T2-30 | `bcoc:CollectionsManagement` | `bco:CollectionsManagement` | Collections Management | 5 | `f88b4eacc76e…` | ready |
| T2-34 | `bcoc:TaxProcessing` | `bco:TaxProcessing` | Tax Processing | 6 | `66fa1dc7eb2e…` | ready |
| T2-36 | `bcoc:InHouseBankAccountManagement` | `bco:InHouseBankAccountManagement` | In-House Bank Account Management | 6 | `76db9f3f639c…` | ready |
| T2-39 | `bcoc:ForeignExchangeRiskManagement` | `bco:ForeignExchangeRiskManagement` | Foreign Exchange Risk Management | 6 | `d89a321f2a82…` | ready |
| T2-41 | `bcoc:InterestRateRiskManagement` | `bco:InterestRateRiskManagement` | Interest Rate Risk Management | 4 | `274a45072c91…` | ready |
| T2-01 | `bcoc:PaymentProcessing` | `bco:PaymentProcessing` | Payment Processing | 2 | `daea7d6c0040…` | ready |
| T2-03 | `bcoc:ExpenseReimbursementProcessing` | `bco:ExpenseReimbursementProcessing` | Expense Reimbursement Processing | 3 | `8987978e0bf5…` | ready |
| T2-05 | `bcoc:CapitalProjectAccounting` | `bco:CapitalProjectAccounting` | Capital Project Accounting | 4 | `9a41381d4c1f…` | ready |
| T2-07 | `bcoc:AccountingPolicyManagement` | `bco:AccountingPolicyManagement` | Accounting Policy Management | 2 | `e4b4f0aa8ca7…` | ready |
| T2-11 | `bcoc:LetterOfCreditManagement` | `bco:LetterOfCreditManagement` | Letter of Credit Management | 1 | `33ef90f2c43d…` | ready |
| T2-14 | `bcoc:TradeDocumentation` | `bco:TradeDocumentation` | Trade and Customs Documentation | 4 | `d5db68e30409…` | ready |
| T2-20 | `bcoc:PayManagement` | `bco:PayManagement` | Pay Management | 8 | `ac7202489c6e…` | ready |
| T2-21 | `bcoc:PayrollTaxProcessing` | `bco:PayrollTaxProcessing` | Payroll Tax Processing | 3 | `c044f73d0943…` | ready |
| T2-23 | `bcoc:CostAccounting` | `bco:CostAccounting` | Cost Accounting | 4 | `3675f36e6609…` | ready |
| T2-26 | `bcoc:FinancialPlanningBudgetingAndForecasting` | `bco:FinancialPlanningBudgetingAndForecasting` | Financial Planning, Budgeting and Forecasting | 3 | `d24cefca1073…` | ready |
| T2-32 | `bcoc:CustomerInvoicing` | `bco:CustomerInvoicing` | Customer Invoicing | 5 | `092b0d0ab201…` | ready |
| T2-33 | `bcoc:TaxPlanning` | `bco:TaxPlanning` | Tax Planning | 2 | `48d1d244d6c7…` | ready |
| T2-35 | `bcoc:CashManagement` | `bco:CashManagement` | Cash Management | 3 | `f6a47b9b2f07…` | ready |
| T2-38 | `bcoc:CounterpartyCreditExposureManagement` | `bco:CounterpartyCreditExposureManagement` | Counterparty Credit Exposure Management | 4 | `eb9144e87f75…` | ready |
| T2-40 | `bcoc:HedgingTransactionExecution` | `bco:HedgingTransactionExecution` | Hedging Transaction Execution | 4 | `8cddd9730947…` | ready |
| T2-42 | `bcoc:TreasuryPolicyManagement` | `bco:TreasuryPolicyManagement` | Treasury Policy Management | 5 | `08579dbf7b83…` | ready |
| T2-02 | `bcoc:CorporateCardManagement` | `bco:CorporateCardManagement` | Corporate Card Management | 3 | `83e0745a61f9…` | source check SC-1 first |
| T2-04 | `bcoc:CapitalInvestmentAppraisal` | `bco:CapitalInvestmentAppraisal` | Capital Investment Appraisal | 1 | `5abaec58e928…` | ready |
| T2-17 | `bcoc:ControlEnvironmentAndRiskObjectiveFormulation` | `bco:ControlEnvironmentAndRiskObjectiveFormulation` | Control Environment and Risk Objective Formulation | 3 | `f2d245a014d6…` | ready |
| T2-24 | `bcoc:CostDriverAndCriticalActivityAnalysis` | `bco:CostDriverAndCriticalActivityAnalysis` | Cost Driver and Critical Activity Analysis | 3 | `38250849e2b2…` | source check SC-2 first |
| T2-31 | `bcoc:CustomerCreditManagement` | `bco:CustomerCreditManagement` | Customer Credit Management | 3 | `e909d335d100…` | source check SC-3 first |
| T2-43 | `bcoc:InternalControlEffectivenessMonitoring` | `bco:InternalControlEffectivenessMonitoring` | Internal Control Effectiveness Monitoring | 1 | `706f8aeaeba1…` | ready |
| T2-25 | `bcoc:FinancialPerformanceAnalysis` | `bco:FinancialPerformanceAnalysis` | Financial Performance Analysis | 4 | `d72a4c76071b…` | ready |
Every type has a signed PASS:

- **T1-02 and T1-03** are signed in `docs/decisions/2026-11-05-g1t-tranche-1-signed.md`.
- **The T2 rows** are signed in `docs/decisions/2026-11-14-g1t-tranche-2-signed.md`.

The record digests above are the ones the signature record lists, recomputed now by
`tools/vocab/build.py` and identical. Across the 42 types the indexes hold 169 member
slots: 156 distinct BPO act classes, since some acts are shared, as CD4 allows.

**The 3 waiting on a source check:**

- T2-02 Corporate Card Management;
- T2-24 Cost Driver and Critical Activity Analysis;
- T2-31 Customer Credit Management.

Each waits on one focused source check (`docs/catalog/tranche-2-followup.md`, §3). The
direction calls for these checks before formalization. Each is one question about one
act. A check that finds nothing joins its type to the tranche without a new readiness
review. A check that finds a defect returns that type alone to the architect.

**Kept out, and why:**

| Kept out | Count | Reason |
|---|---|---|
| Q-12-blocked concepts | 10 | No justified realization index (decision B2 to B4). They are isolated: no proposed class references them, and none of the 42 depends on them (section 6.1) |
| Capability areas | 11 | Not proposed for G1-T: 5 classified as areas at curation, 3 withdrawn on 2026-11-14, and 3 decided on 2026-11-15. Each is a vocabulary concept only |
| Functional groupings | 5 | The concepts the narrowed types came from. Vocabulary concepts only |
| T1-01, Customer Complaint Management | 1 | Admitted under G1-T on 2026-11-05, but it has no vocabulary concept yet. It waits for one |
| Other concepts not ready | 2 | Export and Import Control; International Funds Management: no act type in their evidence |
| Pilot concepts outside tranche 2 | 4 | Strategic Planning, Competitive Analysis, Business Model Governance, Customer Experience Management: no G1-T record |

## 3. Terminology, definitions and taxonomy

**Terminology.** Each class takes its vocabulary concept's preferred label and its
definition. Each definition is the one signed under G1-T, checked against CAP-07, and all
are in `src/01_controlled_vocabulary/catalog.yaml`, generated into `bco-catalog.ttl`.

They were reviewed in four stages:

1. the Ontologist's curation;
2. the synthetic domain practitioner (30 findings, all applied);
3. the independent G1-T review and the supplementary review;
4. the architect's batch decision, final direction and signature.

All 74 catalog concepts and the 9 metamodel concepts are Draft. None is ratified (D5-4).

**The parent's definition** is specification §4's, carried by `bcom:BusinessCapability`.

**Taxonomy.** Every link of the 42 is in `docs/catalog/tranche-2-review.yaml`, classified
under the Stage 03 standard:

| Links from an admitted type | Count | What it becomes at Stage 05 |
|---|---|---|
| retained `part-of`, broader not admitted | 35 | Nothing. No subclass axiom; a `part-of` link has no formal reading (standard S6) |
| retained `part-of`, broader admitted | 4 | Nothing, for the same reason. Payroll Tax Processing and Pay Management to Payroll Processing; Payment Processing to Accounts Payable Processing and to Pay Management |
| retained `kind-of`, broader not admitted | 7 | Nothing yet. The broader is not a class. Each stays a proposal under CD9 until both ends are admitted |
| `incorrect` or `unresolved` | 7 | Nothing (Stage 03 rule 6) |

No retained `kind-of` link joins two admitted types, so no CAP-10 review is needed for
this tranche. Every class's only named parent is `bco:BusinessCapability`.

## 4. The signed records and exact baselines

| Record | SHA-256 at `e41eb07` |
|---|---|
| `docs/catalog/admission/G1T-T2-batch.md`, revision 5 (the signed T2 baseline) | `b44ec9ea2af76a9cbf48fcb125a94b93c88076475603532bf23fc32106bd90ef` |
| `docs/catalog/admission/G1T-T2-signature.md` (signed) | `18b0e1569beb18c5b88643b54be3d8b431506da8d44566426d3962384b4d9f1e` |
| `docs/decisions/2026-11-14-g1t-tranche-2-signed.md` | `ebc549d5fe8a94bd611bdd5e9bbcbd5da960b96315102503b7bda06c5b9e6369` |
| `docs/catalog/admission/G1T-T1-02-payroll-processing.md` | `92bb7d35b50ddda65a63c368476ccc73022df2333a120e3d419e1546e5fdf4fa` |
| `docs/catalog/admission/G1T-T1-03-accounts-payable-processing.md` | `e65018013e38d2f2b9c86c2d5e18f41a67665c32fad0221698c5f14521646b32` |
| `docs/decisions/2026-11-05-g1t-tranche-1-signed.md` | `cf9783011fad7b998fa0b53b2530111969b1fee67e89b218d1a75a2d85991751` |
| `docs/decisions/2026-11-04-d4-rp1-rp10-ratified-option-b.md` (the parent's admission) | `45188fb4543d14dca5acc12137fa9d30f8095403dec0f7ca34f090a43837b632` |
| `specifications/Business-Capability-Ontology-v0.5.0-draft.3.md` | `2224f869b0ec7a1e31b0afc1c2b403ad222ea290c334bff48a93ebbb6516c574` |
| `docs/adr/ADR-002-organizational-capabilities.md` | `89ef45c65901576f9efcdb0c6db94b85b4333e8f17e9635253a79183d84a2fdd` |
| `src/02_conceptual_models/CM-01-business-capability.md` | `292c8f36d64075b9663e159985a15b448aa933c3b5ed4baff3b2a556ca861ccc` |
| `docs/standards/stage-03-taxonomy.md` | `cb235960104f315ed17c3f82fb648db62761b834b7e22cd974a8f8c3e9503926` |
| `src/01_controlled_vocabulary/catalog.yaml` | `8dddb1e6872ad8615cd3e396edadef98d5c2316eee57b0ca5f29241ada03ac05` |
| `src/01_controlled_vocabulary/metamodel.yaml` | `3feaf2fb267bd970b2e1594f45e348d5ccb409db44451a25cd3f9322a1acfa47` |
| `docs/catalog/bpo-act-types.yaml` (BPO act types at the pin) | `25be29e5d4df6b7d8671128a7fae4cafa20aec2a6ac53cb2dbae2f8f76b800eb` |

The errata in `docs/catalog/tranche-2-followup.md` §2 apply on top of the signed batch.
None changes a definition, an index or a finding.

## 5. BFO and CCO reuse, verified at the pins

Every IRI and axiom below was read from the pinned files, fetched and checked by digest on
2026-11-15:

- CCO merged, `e609db27…fe5b`;
- BFO core, `6944e2c9…3b3b`.

None is asserted from memory.

| Use | IRI | Verified at the pin | In the vendored extract today |
|---|---|---|---|
| Parent of `bco:BusinessCapability` | `cco:ont00000568` Organization Capability | `⊑ cco:ont00001379` Agent Capability `⊑ obo:BFO_0000017` realizable entity | yes |
| Parent of `bco:BusinessCapability` | `obo:BFO_0000016` disposition | `⊑ obo:BFO_0000017`. Disjoint with `obo:BFO_0000023` role, and with nothing else on this path, so the two parents are compatible | yes |
| Not used as a parent | `obo:BFO_0000034` function | `⊑ obo:BFO_0000016`. CAP-09 governs it | yes |
| Realization (instances, later tranches) | `obo:BFO_0000054` has realization / `obo:BFO_0000055` realizes | domain realizable entity, range process; inverses | yes |
| Material basis (instances, later) | `obo:BFO_0000218` has material basis | domain disposition, range material entity | yes |
| Bearer membership (instances, later) | `obo:BFO_0000115` has member part / `obo:BFO_0000129` member part of | domain and range material entity. Specification §5's "IRI verified at Stage 05" is now verified | **no**: added by `--rebuild` when first used |
| Bearing (instances, later) | `cco:ont00001954` has capability / `cco:ont00001889` capability of | domain Agent, range Agent Capability; inverses | yes |
| Index-member genera from CCO | `cco:ont00000366` Information Processing, `ont00000511` Planning, `ont00000836` Financial Instrument Use, `ont00000379` Representative Communication, `ont00000449` Remuneration, `ont00000636` Appraisal, `ont00000402` Communication, `ont00000345` Measuring, `ont00000371` Prediction, `ont00000884` Loaning | each reaches `cco:ont00000228` Planned Act | 4 of the 10 (379, 402, 449, 836); the rest by `--rebuild` (Q-14) |

All 18 genera of the 156 members reach Planned Act, and none falls under
`cco:ont00000568`. There are 11 BPO genera:

- 6 reach it through a CCO class above: Accounting, Analysis, Monitoring, Selection and
  Identification through Information Processing, and Formulation through Planning;
- 5 are declared directly under Planned Act, or under a vendored CCO act: Financial
  Transaction, Card Administration, Reporting, Remuneration and Acquisition.

Acquisition is the one CD5 development genus. Its single member, `P20932`, has a CAP-06
reason in T2-02's record.

The other 7 genera are CCO classes themselves.

**Relations.** The first tranche writes no object property assertion and needs none. The
only non-RDF(S)/OWL/SKOS predicate it writes is `ex:enablesProcess`, BPO's
`owl:AnnotationProperty`, declared in `ontology/capabilities_roles.ttl` line 55 at the pin.
That declaration is vendored under section 6.3.

## 6. BPO integration, for the classes actually proposed

### 6.1 Q-12, capability-typed index entries

| Group | Count | How it is handled |
|---|---|---|
| Members of the 42 indexes typed under `cco:ont00000568` | **0** | Verified member by member against `bpo-act-types.yaml` and the pinned slices. S05-C3 keeps it so |
| Admitted types whose designating BPO class is capability-typed (`docs/catalog/tranche-2-q12.md` §3: Cash Management, In-House Bank Account Management, Counterparty Credit Exposure Management, Foreign Exchange Risk Management, Hedging Transaction Execution, Interest Rate Risk Management, Treasury Policy Management; the eighth listed there, Financial Risk Management, was withdrawn as an area) | 7 | The designating class is excluded from the index (CAP-03), as signed. The proposed class makes no reference to it: no equivalence, no subclass, no mapping. A mapping to BPO's capability classes is deferred (section 7, D4) |
| The 10 blocked concepts | 10 | Not in the tranche. They wait on BPO's answer to `BCO-BPO-2026-11-15-q12-capability-typing-inquiry`. No proposed class depends on them |

The inquiry found that BPO's typing of the 39 classes is deliberate (ADR-001 R5 and R6,
cited in each class's comment). That does not change anything here, because none of them
is an index member.

### 6.2 Q-13, inconsistent shared declarations

At the pin, BPO's declarations relevant to the tranche were checked across all of BPO's
modules:

- **The 156 members.** Each is declared once (155 in `ontology/slices/apqc_9_0.ttl`, 1 in
  `apqc_12_0.ttl`), with one superclass set.
- **The 11 BPO genera.** Each has a single superclass set across every module that
  declares it.
- **Definitions.** Only `bpo:ActOfReporting` carries two different definitions, across
  five modules.

The BCO relies on typing only, never on a genus's definition text. Q-13 therefore does not
block this tranche. The extract takes each declaration from one named module (standard §4).
Which definition of Act of Reporting is authoritative is BPO's to settle. Deferred (D3).

### 6.3 Q-14, act types not vendored

This is the one BPO dependency that blocks executable validation. Without the members'
declarations, CAP-03 (S05-C3) and Gate B cannot check an index.

The widening adds to the BPO extract:

- the declarations of the 156 members, from `apqc_9_0.ttl` (SHA-256 `a7247e5f…df6d`) and
  `apqc_12_0.ttl` (`827e94b6…bfec`) at `bc64e91`;
- the 8 BPO genera not yet vendored, with their superclasses;
- `bpo:enablesProcess`'s declaration, from `capabilities_roles.ttl` (`6a8aeaf8…ed7d`).

The CCO extract gains the 6 genera above and their ancestors, and the BFO extract gains
`obo:BFO_0000115` and `obo:BFO_0000129` when first used. None of the three BPO files
is in RP-3's excluded list, and none imports anything.

The vendoring tool takes one URL per source today (`config/upstream-sources.yaml`, the
`bpo` note). The change is a configuration change if two more BPO sources can be declared,
one per file. Otherwise it is a small change to `tools/ontology/vendor_upstream.py`. It is
not new generator infrastructure. `--confirm` proves the result is derived from the pins.
It lands in the first implementation commit, with `config/upstream-extracts.json` and
`vendor/NOTICE.md` regenerated.

### 6.4 CD12 and the source of the index

CD12, which is ratified, has BPO's `capability_scope.json` generate `ex:enablesProcess`.
That file keys BPO's own capability classes (`bpo:StrategicPlanningCapability` and the
rest). It knows nothing of the 42 BCO concepts, whose indexes were drawn act by act,
reviewed and signed.

Proposed (D5-6): for a BCO-minted class, the signed G1-T record is the index's source. The
module carries the index as authored annotations, and S05-T1 fails on any difference from
the record. CD12's substance is kept:

- the index is an annotation with no causal or modal entailment;
- no `requiresCapability` is written (CAP-14);
- each member was checked against CD5 at G1-T.

This reads CD12 as written for BPO-held classes. If the architect reads it as binding on
BCO-minted classes too, the alternative is to propose entries to BPO's scope file, which
would put BCO's signed indexes under BPO's control. That is not recommended.

## 7. Blocking and deferred dependencies

**Blocking**, before the first class is written:

| Id | Dependency | Blocks | Resolved by |
|---|---|---|---|
| B1 | Roadmap D5's T1, T2 and T3 entries. T1 (the Stage 01 standard) is not supplied, T2 (vocabulary acceptance) has not been done, and T3 (terminology reconciliation) has not been done | The whole tranche, as the roadmap reads | D5-4: the architect accepts section 3 as T2's tranche-scoped acceptance and defers T1 and T3, or directs otherwise. T3 concerns the 14 metamodel and description-layer concepts, none of which this tranche writes |
| B2 | Q-14: member declarations not vendored | S05-C3 and Gate B on every index | D5-5, then the widening in the first implementation commit |
| B3 | Approval of the standard and its checks | All authoring | D5-1, D5-2 |
| B4 | No reasoner installed | S05-D now; S05-D2 at the tranche's checkpoint (CP-2) | D5-7. It blocks completion, not authoring: ELK reports SKIP while it is absent, as Gates B and D already do |
| B5 | The three source checks SC-1 to SC-3 | T2-02, T2-24 and T2-31 only | `docs/catalog/tranche-2-followup.md` §3, one check each |

**Deferred.** None blocks this tranche:

| Id | Dependency | Why it does not block | Gate it is due by |
|---|---|---|---|
| D1 | Q-12 for the 10 blocked concepts; BPO's answer | No proposed class depends on them | Before any of them is proposed for G1-T |
| D2 | The locator updates held for T2-02 and T2-31 (`docs/catalog/tranche-2-followup.md` §4) | No definition, index or finding changes | When each type is formalized, or now if the architect prefers |
| D3 | Q-13 for Act of Reporting's two definitions | Typing is consistent; the BCO uses typing only | Before a definition of a BPO genus is cited |
| D4 | Any mapping from a BCO class to a BPO capability class (the 7 designating classes; the spec's plan to move BPO's capability classes into the BCO) | No axiom is written between them | A tranche of its own, if ever |
| D5 | The description layer, K2 unions, `only` restrictions, the coverage register, instance-level CAP shapes | Not in this tranche (standard §8) | Their own tranches |
| D6 | The `ex:` prefix moving to `bpo:` (decision of 2026-10-28, R3) | A prefix, not an IRI | Spec v0.5's aligned version and CM-01's next version |
| D7 | `P14057` and the MD-6 orphan acts | They affect no admitted index | The next semantic-curation batch over PCF 9.1 |
| D8 | The conceptual-fidelity gate and the Ontology Template's P6 offer | It applies once a module has terms | D6, at stage completion |
| D9 | Ratification of the vocabulary concepts | Readiness keeps ratification apart from OWL (roadmap §7) | A Stage 01 standard (T1) |

## 8. What this package does not do

- It writes no OWL, mints no IRI, vendors nothing and installs nothing.
- It reopens no G1-T record, and changes no definition, index, link or finding.
- It does not approve itself: D5 is the architect's act.
