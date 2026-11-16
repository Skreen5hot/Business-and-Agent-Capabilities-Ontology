# Conceptual-fidelity trace — Stage 05, first tranche

| Field | Value |
|---|---|
| Status | Prepared for the architect under the decision of 2026-11-15, H (`docs/decisions/2026-11-15-d6-class-increment-accepted.md`). A trace, not a review: it changes no class, definition, index or finding |
| Module | `src/05_ontology/apqc-cap.ttl`, written from `src/05_ontology/tranche-1.yaml` by `tools/ontology/formalize.py` |
| Conceptual baseline | CM-01, approved 2026-10-26, `src/02_conceptual_models/CM-01-business-capability.md` (SHA-256 `292c8f36d64075b9663e159985a15b448aa933c3b5ed4baff3b2a556ca861ccc`) |
| Admission baseline | the signed G1-T records: T1-02 and T1-03 at `7515f44`; the tranche 2 batch at `1fdb2c5` (SHA-256 `b44ec9ea…90ef`), signed in `docs/catalog/admission/G1T-T2-signature.md` |
| Kept current by | `tests/test_formalization.py::test_the_fidelity_trace_matches_the_module`, which reads the class table below and requires it to agree with the tranche record and the module, row for row |

Derived in part from the APQC Process Classification Framework® 7.4 (element IDs in the
BPO act IRIs the indexes name, under APQC's notice in `NOTICE.md`). APQC does not endorse
this work.

## 1. CM-01 elements and their encoding

| CM-01 element | What CM-01 says | Encoded as | Held by |
|---|---|---|---|
| Business Capability (concept) | borne by an Organization; grounded in its members as organized; realized only by acts that exercise it. Preliminary alignment: under `cco:ont00000568`, and under `obo:BFO_0000016` only for a type that has passed type admission | `bco:BusinessCapability` under `cco:ont00000568` and `obo:BFO_0000016`, with `bcom:BusinessCapability`'s definition, which is the ratified §4 row | standard S2; `formalize.py` (the parent's parents and definition); ratification of CD1 to CD3 admits it (CD3) |
| Capability Type (concept) | a kind of business capability, identified by bearer kind, grounding and realization index; not a catalog node or a vocabulary concept, which designate it | one `owl:Class` per admitted type, its IRI the concept's local name in `bco#` (S1), its definition the signed one | S05-T1 (`formalize.py`; `tests/test_formalization.py`) |
| RL-02 is an instance of | a capability falls under one or more Capability Types | the classes are the types; instances are typed with them (CP-1 fixtures) | the instance shapes; CQ-1 |
| RL-09 records admission of | a Type Admission Record says whether capabilities of the type can be dispositions of an organization; about a type, never an organization | each class's signed G1-T PASS, cited in the tranche record by path, commit and SHA-256; the class is written under the parent only after it (S4) | S05-C9; CQ-10 |
| RL-10 has realization index | mandatory for every specific type | one or more `bpo:enablesProcess` on each specific class | S05-C3 |
| RL-11 lists as admissible | acts of this type may realize capabilities of the indexing type; not exhaustive; development acts need a reason | one `bpo:enablesProcess` per signed member, and no others; no `only` restriction (no CAP-30 review); no development member in this tranche | S05-T1, S05-C3, S05-C4, S05-C7 |
| RL-15 specializes | reviewed only (CD9, CAP-10); never induced from coverage or numbering | not written: every specific class is directly and only under the parent; HermiT reports 0 CAP-10 candidates | S3 test; S05-D2 |
| RL-01 bears | Organization has the capability | `cco:ont00001954`, inverse `cco:ont00001889` | CAP-08 (instance shapes); CQ-1 |
| RL-04 and RL-05 has as basis, consists of | the members, one possibly sufficing; never an artifact; only for admitted types | `obo:BFO_0000218` to a member part (`obo:BFO_0000115`) that is an agent | CAP-25, CAP-35 (instance shapes) |
| RL-12 realizes | the act exercises the capability; its asserted type under an index member | `obo:BFO_0000055` and `obo:BFO_0000054` | CAP-21 (Gate C-A); CQ-3 |
| RL-14 is performed by | members carry out the act; a provider's staff leave the consumer with a sourcing arrangement | `cco:ont00001833` has agent and `cco:ont00001787` agent in (the Stage 05 encoding; the Extended Relation Ontology has no relation for agency) | CAP-34; CQ-3 |
| RL-13 develops | no formal relation chosen (OI-4) | not encoded | CQ-11 not demonstrated |
| RL-16 to RL-23 (the description layer) | maps, assessments, findings, targets, sourcing, authorization | not encoded: the description-layer terms are not minted | the blocked CP-1 and CP-2 items (`src/05_ontology/README.md`) |

## 2. The 40 classes

Every row is verified by `formalize.py` before the module is written:

- the definition is the vocabulary concept's, and equals the signed record's;
- the index is the signed index, member by member and in order;
- the concept's record digest is the one the signature or the readiness package names.

| G1-T | Class | CM-01 element | Admission (signed record) | Concept record | Parent asserted | Index |
|---|---|---|---|---|---|---|
| — | `bco:BusinessCapability` | Business Capability | ratification of CD1 to CD3 (`docs/decisions/2026-11-04-d4-rp1-rp10-ratified-option-b.md`) | `bcom:BusinessCapability` (spec §4 row) | `cco:ont00000568`, `obo:BFO_0000016` | — (CAP-03 excepts the parent) |
| T1-02 | `bco:PayrollProcessing` | Capability Type (RL-09 admission) | `G1T-T1-02-payroll-processing.md` at `7515f44`, `f41e29cc40df…` | `defbd4f3400f…` | `bco:BusinessCapability` | 11 |
| T1-03 | `bco:AccountsPayableProcessing` | Capability Type (RL-09 admission) | `G1T-T1-03-accounts-payable-processing.md` at `7515f44`, `b49935b79b40…` | `7d60551d0870…` | `bco:BusinessCapability` | 7 |
| T2-08 | `bco:FinancialReporting` | Capability Type (RL-09 admission) | `G1T-T2-batch.md` §T2-08 at `1fdb2c5`, `b44ec9ea2af7…` | `84e3c1a7ea9b…` | `bco:BusinessCapability` | 10 |
| T2-09 | `bco:FixedAssetAccounting` | Capability Type (RL-09 admission) | `G1T-T2-batch.md` §T2-09 at `1fdb2c5`, `b44ec9ea2af7…` | `d7432dbd9211…` | `bco:BusinessCapability` | 8 |
| T2-10 | `bco:GeneralLedgerAccounting` | Capability Type (RL-09 admission) | `G1T-T2-batch.md` §T2-10 at `1fdb2c5`, `b44ec9ea2af7…` | `d7c19172b362…` | `bco:BusinessCapability` | 9 |
| T2-12 | `bco:TradeProductClassification` | Capability Type (RL-09 admission) | `G1T-T2-batch.md` §T2-12 at `1fdb2c5`, `b44ec9ea2af7…` | `578838efeef4…` | `bco:BusinessCapability` | 1 |
| T2-13 | `bco:RestrictedPartyScreening` | Capability Type (RL-09 admission) | `G1T-T2-batch.md` §T2-13 at `1fdb2c5`, `b44ec9ea2af7…` | `1e5990ec6e5b…` | `bco:BusinessCapability` | 1 |
| T2-15 | `bco:TradePreferenceManagement` | Capability Type (RL-09 admission) | `G1T-T2-batch.md` §T2-15 at `1fdb2c5`, `b44ec9ea2af7…` | `c005bde58329…` | `bco:BusinessCapability` | 1 |
| T2-16 | `bco:InternalControlReporting` | Capability Type (RL-09 admission) | `G1T-T2-batch.md` §T2-16 at `1fdb2c5`, `b44ec9ea2af7…` | `f92d82551826…` | `bco:BusinessCapability` | 4 |
| T2-18 | `bco:InternationalRateMonitoring` | Capability Type (RL-09 admission) | `G1T-T2-batch.md` §T2-18 at `1fdb2c5`, `b44ec9ea2af7…` | `768596eaf4e8…` | `bco:BusinessCapability` | 1 |
| T2-19 | `bco:CrossBorderFundsTransferManagement` | Capability Type (RL-09 admission) | `G1T-T2-batch.md` §T2-19 at `1fdb2c5`, `b44ec9ea2af7…` | `7d28476b319f…` | `bco:BusinessCapability` | 1 |
| T2-22 | `bco:TimeReporting` | Capability Type (RL-09 admission) | `G1T-T2-batch.md` §T2-22 at `1fdb2c5`, `b44ec9ea2af7…` | `eee8ad6a3634…` | `bco:BusinessCapability` | 4 |
| T2-28 | `bco:AccountsReceivableProcessing` | Capability Type (RL-09 admission) | `G1T-T2-batch.md` §T2-28 at `1fdb2c5`, `b44ec9ea2af7…` | `fb5d4e1f8541…` | `bco:BusinessCapability` | 4 |
| T2-29 | `bco:CustomerDeductionManagement` | Capability Type (RL-09 admission) | `G1T-T2-batch.md` §T2-29 at `1fdb2c5`, `b44ec9ea2af7…` | `955724f77555…` | `bco:BusinessCapability` | 5 |
| T2-30 | `bco:CollectionsManagement` | Capability Type (RL-09 admission) | `G1T-T2-batch.md` §T2-30 at `1fdb2c5`, `b44ec9ea2af7…` | `f88b4eacc76e…` | `bco:BusinessCapability` | 5 |
| T2-34 | `bco:TaxProcessing` | Capability Type (RL-09 admission) | `G1T-T2-batch.md` §T2-34 at `1fdb2c5`, `b44ec9ea2af7…` | `66fa1dc7eb2e…` | `bco:BusinessCapability` | 6 |
| T2-36 | `bco:InHouseBankAccountManagement` | Capability Type (RL-09 admission) | `G1T-T2-batch.md` §T2-36 at `1fdb2c5`, `b44ec9ea2af7…` | `76db9f3f639c…` | `bco:BusinessCapability` | 6 |
| T2-39 | `bco:ForeignExchangeRiskManagement` | Capability Type (RL-09 admission) | `G1T-T2-batch.md` §T2-39 at `1fdb2c5`, `b44ec9ea2af7…` | `d89a321f2a82…` | `bco:BusinessCapability` | 6 |
| T2-41 | `bco:InterestRateRiskManagement` | Capability Type (RL-09 admission) | `G1T-T2-batch.md` §T2-41 at `1fdb2c5`, `b44ec9ea2af7…` | `274a45072c91…` | `bco:BusinessCapability` | 4 |
| T2-01 | `bco:PaymentProcessing` | Capability Type (RL-09 admission) | `G1T-T2-batch.md` §T2-01 at `1fdb2c5`, `b44ec9ea2af7…` | `daea7d6c0040…` | `bco:BusinessCapability` | 2 |
| T2-03 | `bco:ExpenseReimbursementProcessing` | Capability Type (RL-09 admission) | `G1T-T2-batch.md` §T2-03 at `1fdb2c5`, `b44ec9ea2af7…` | `8987978e0bf5…` | `bco:BusinessCapability` | 3 |
| T2-05 | `bco:CapitalProjectAccounting` | Capability Type (RL-09 admission) | `G1T-T2-batch.md` §T2-05 at `1fdb2c5`, `b44ec9ea2af7…` | `9a41381d4c1f…` | `bco:BusinessCapability` | 4 |
| T2-07 | `bco:AccountingPolicyManagement` | Capability Type (RL-09 admission) | `G1T-T2-batch.md` §T2-07 at `1fdb2c5`, `b44ec9ea2af7…` | `e4b4f0aa8ca7…` | `bco:BusinessCapability` | 2 |
| T2-11 | `bco:LetterOfCreditManagement` | Capability Type (RL-09 admission) | `G1T-T2-batch.md` §T2-11 at `1fdb2c5`, `b44ec9ea2af7…` | `33ef90f2c43d…` | `bco:BusinessCapability` | 1 |
| T2-14 | `bco:TradeDocumentation` | Capability Type (RL-09 admission) | `G1T-T2-batch.md` §T2-14 at `1fdb2c5`, `b44ec9ea2af7…` | `d5db68e30409…` | `bco:BusinessCapability` | 4 |
| T2-20 | `bco:PayManagement` | Capability Type (RL-09 admission) | `G1T-T2-batch.md` §T2-20 at `1fdb2c5`, `b44ec9ea2af7…` | `ac7202489c6e…` | `bco:BusinessCapability` | 8 |
| T2-21 | `bco:PayrollTaxProcessing` | Capability Type (RL-09 admission) | `G1T-T2-batch.md` §T2-21 at `1fdb2c5`, `b44ec9ea2af7…` | `c044f73d0943…` | `bco:BusinessCapability` | 3 |
| T2-23 | `bco:CostAccounting` | Capability Type (RL-09 admission) | `G1T-T2-batch.md` §T2-23 at `1fdb2c5`, `b44ec9ea2af7…` | `3675f36e6609…` | `bco:BusinessCapability` | 4 |
| T2-26 | `bco:FinancialPlanningBudgetingAndForecasting` | Capability Type (RL-09 admission) | `G1T-T2-batch.md` §T2-26 at `1fdb2c5`, `b44ec9ea2af7…` | `d24cefca1073…` | `bco:BusinessCapability` | 3 |
| T2-32 | `bco:CustomerInvoicing` | Capability Type (RL-09 admission) | `G1T-T2-batch.md` §T2-32 at `1fdb2c5`, `b44ec9ea2af7…` | `092b0d0ab201…` | `bco:BusinessCapability` | 5 |
| T2-33 | `bco:TaxPlanning` | Capability Type (RL-09 admission) | `G1T-T2-batch.md` §T2-33 at `1fdb2c5`, `b44ec9ea2af7…` | `48d1d244d6c7…` | `bco:BusinessCapability` | 2 |
| T2-35 | `bco:CashManagement` | Capability Type (RL-09 admission) | `G1T-T2-batch.md` §T2-35 at `1fdb2c5`, `b44ec9ea2af7…` | `f6a47b9b2f07…` | `bco:BusinessCapability` | 3 |
| T2-38 | `bco:CounterpartyCreditExposureManagement` | Capability Type (RL-09 admission) | `G1T-T2-batch.md` §T2-38 at `1fdb2c5`, `b44ec9ea2af7…` | `eb9144e87f75…` | `bco:BusinessCapability` | 4 |
| T2-40 | `bco:HedgingTransactionExecution` | Capability Type (RL-09 admission) | `G1T-T2-batch.md` §T2-40 at `1fdb2c5`, `b44ec9ea2af7…` | `8cddd9730947…` | `bco:BusinessCapability` | 4 |
| T2-42 | `bco:TreasuryPolicyManagement` | Capability Type (RL-09 admission) | `G1T-T2-batch.md` §T2-42 at `1fdb2c5`, `b44ec9ea2af7…` | `08579dbf7b83…` | `bco:BusinessCapability` | 5 |
| T2-04 | `bco:CapitalInvestmentAppraisal` | Capability Type (RL-09 admission) | `G1T-T2-batch.md` §T2-04 at `1fdb2c5`, `b44ec9ea2af7…` | `5abaec58e928…` | `bco:BusinessCapability` | 1 |
| T2-17 | `bco:ControlEnvironmentAndRiskObjectiveFormulation` | Capability Type (RL-09 admission) | `G1T-T2-batch.md` §T2-17 at `1fdb2c5`, `b44ec9ea2af7…` | `f2d245a014d6…` | `bco:BusinessCapability` | 3 |
| T2-43 | `bco:InternalControlEffectivenessMonitoring` | Capability Type (RL-09 admission) | `G1T-T2-batch.md` §T2-43 at `1fdb2c5`, `b44ec9ea2af7…` | `706f8aeaeba1…` | `bco:BusinessCapability` | 1 |
| T2-25 | `bco:FinancialPerformanceAnalysis` | Capability Type (RL-09 admission) | `G1T-T2-batch.md` §T2-25 at `1fdb2c5`, `b44ec9ea2af7…` | `d72a4c76071b…` | `bco:BusinessCapability` | 4 |

## 3. What the trace finds

- **Every class traces to CM-01 and to its admission.** The parent traces to the concept
  Business Capability and to its ratification. Each specific class traces to Capability
  Type, admitted by its signed G1-T record (RL-09).
- **Every definition is the signed definition**, and every index is the signed index:
  160 members over 147 distinct acts.
- **Nothing is asserted that CM-01 reserves for review.** No specialization (RL-15), no
  development relation (RL-13), and no description-layer relation (RL-16 to RL-23).
- **One difference in wording, not in meaning.** CM-01 aligns Business Capability under
  `obo:BFO_0000016` "only for a type that has passed type admission". The parent asserts
  that disposition parent itself, because the architect's ratification of CD1 to CD3
  admitted the parent (CD3, R10-04). CM-01 predates that ratification; the D5 record's
  parent-alignment table recorded the same point as aligned in effect.

## 4. Addendum: the description tranche (B-1)

Section 1's last row ("not encoded") described the first tranche. Under the decision of
2026-11-15, B-1 (`docs/decisions/2026-11-15-b1-b4-approved-cap34-confirmed.md`), the
description layer is now written in `apqc-cap-desc.ttl`. Its classes are information terms
that CM-01 names, not Capability Types, so no G1-T record traces them; each traces to its
metamodel concept and its section 4 row (`src/05_ontology/tranche-2-description.yaml`,
checked by `formalize.py`).

| CM-01 element | Encoded as | Held by |
|---|---|---|
| Capability Map, Capability Assessment, Capability Maturity Rating, Capability Sourcing Statement, Capability Sourcing Assessment, Capability Target, Capability Target-State Specification, Authorization Record | one `owl:Class` each, under its section 4 CCO parent, with its concept's label and definition | `formalize.py`; `tests/test_description.py` |
| Functional Adequacy Assessment | `bco:FunctionalAdequacyAssessment` under `cco:ont00000853` (B-1); its three findings as continuant parts (readiness record, section 4) | CAP-33 shapes |
| RL-16 describes | `cco:ont00001982` | CAP-23, CAP-26, CAP-33 |
| RL-17 has entry | `obo:BFO_0000178` | CAP-17 |
| RL-18 concerns type | `bco:concernsType` (annotation) | CAP-17 |
| RL-19 states | `bco:assessedPresence` (annotation) | CAP-27 |
| RL-20 cites as evidence | `dct:source` | CAP-26, CAP-27 |
| RL-21 conforms to | `dct:conformsTo` | CAP-20, CAP-27, CAP-33 |
| RL-22 is about | `cco:ont00001808` | CAP-26; the CD14 absent-finding rule |
| RL-23 supports bearing of | not a relation: a present assessment that describes the bearer, is about the instance and concerns its class (DP-2, Option A) | CAP-26; CQ-13 |

No subclass link, object property or individual was added. Agent Manifest (RL-18's other
subject) is not in the tranche: specification §4 mints no class for it (CD13).

