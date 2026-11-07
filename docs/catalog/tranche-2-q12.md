# Tranche 2 — the Q-12 dependencies

| Field | Value |
|---|---|
| Status | **For the architect's separate decision** (`docs/decisions/2026-11-07-tranche-2-accepted-g1t-preparation-authorized.md`, B): an upstream correction, or an existing valid act-type mapping. Decides nothing, and proposes no act type |
| Date | 2026-11-07 |
| BPO pin | `bc64e91839378e1926189c01bf184d6a22d5c1b7` (Phase I-1), read through `docs/catalog/bpo-act-types.yaml` and `docs/sources/inventory/bpo-entries.yaml` |
| Question | CM-01 Q-12: an index member must be an act type (CAP-03). BPO types some of the classes the catalog would index under a capability class, `cco:ont00000568` (Organization Capability), so they cannot be index members |

Derived in part from the APQC Process Classification Framework® 7.4 (element names and
IDs, under APQC's notice in `NOTICE.md`). APQC does not endorse this work.

The 13 concepts stay blocked: none is in the G1-T batch. Every IRI, typing, module and line
below is read from the generated records, not from memory.

## 1. Nine concepts whose only act evidence is capability-typed

For each, BPO's class for the designating PCF element is typed as a capability, and no
process beneath it is in the evidence. A correction upstream would retype that class under
an act genus. No existing BPO act type in the evidence could stand in for it.

| Concept | Candidate | BPO class | PCF element | Typed under | Declared at the pin |
|---|---|---|---|---|---|
| Financial Planning and Management Accounting | BCC-ca61edb4 | `bpo:P10728` | PCF 9.1 Perform planning and management accounting | `cco:ont00000568` (Organization Capability) | `ontology/slices/apqc_9_0.ttl line 951` |
| Continuous Cost Improvement | BCC-3421f274 | `bpo:P10788` | PCF 9.1.4.7 Manage continuous cost improvement | `cco:ont00000568` (Organization Capability) | `ontology/slices/apqc_9_0.ttl line 1276` |
| Banking Relationship Management | BCC-a750d13a | `bpo:P10899` | PCF 9.7.2.7 Manage and oversee banking relationships | `cco:ont00000568` (Organization Capability) | `ontology/slices/apqc_9_0.ttl line 3004` |
| Cash Equivalent Management | BCC-314dba7d | `bpo:P10894` | PCF 9.7.2.2 Manage cash equivalents | `cco:ont00000568` (Organization Capability) | `ontology/slices/apqc_9_0.ttl line 2952` |
| Cash Flow Management | BCC-d71abe9a | `bpo:P10897` | PCF 9.7.2.5 Manage cash flows | `cco:ont00000568` (Organization Capability) | `ontology/slices/apqc_9_0.ttl line 2983` |
| Financial Intermediary Relationship Management | BCC-d6966c88 | `bpo:P10908` | PCF 9.7.4.2 Manage financial intermediary relationships | `cco:ont00000568` (Organization Capability) | `ontology/slices/apqc_9_0.ttl line 3143` |
| Issuer Credit Exposure Management | BCC-13b94120 | `bpo:P10910` | PCF 9.7.4.4 Manage issuer exposure | `cco:ont00000568` (Organization Capability) | `ontology/slices/apqc_9_0.ttl line 3163` |
| Liquidity Management | BCC-4464d04f | `bpo:P10909` | PCF 9.7.4.3 Manage liquidity | `cco:ont00000568` (Organization Capability) | `ontology/slices/apqc_9_0.ttl line 3153` |
| Financial Fraud and Dispute Case Management | BCC-9b5ec2fd | `bpo:P16958` | PCF 9.7.6 Manage financial fraud/dispute cases | `cco:ont00000568` (Organization Capability) | `ontology/slices/apqc_9_0.ttl line 3497` |

## 2. Four concepts whose BPO wiring names only their components' acts

The designating class is a BPO capability class, typed under `cco:ont00000568`. BPO's
`enablesProcess` wiring (`ontology/capabilities_wiring.ttl`) links it to act types, and
those are valid act types. But each is the act of one of the concept's components, so an
index drawn from them would not be the concept's own. Tranche 2's first count missed these
acts (`docs/catalog/tranche-2.md`, section 1a).

**Internal Control** (`bcoc:InternalControl`, BCC-5a4bc396).

| Role | BPO class | PCF element | Typed under | Declared at the pin |
|---|---|---|---|---|
| designating class | `bpo:InternalControlCapability` | PCF 9.8 Manage internal controls | `cco:ont00000568` (Organization Capability) | `ontology/slices/apqc_9_0.ttl line 256` |
| enablesProcess target | `bpo:P10762` | PCF 9.8.1 Establish internal controls, policies, and procedures | `bpo:ActOfFormulation` (Act of Formulation) | `ontology/slices/apqc_9_0.ttl line 3516` |
| enablesProcess target | `bpo:P10764` | PCF 9.8.3 Report on internal controls compliance | `bpo:ActOfReporting` (Act of Reporting) | `ontology/slices/apqc_9_0.ttl line 3626` |
| enablesProcess target | `bpo:P21574` | PCF 9.8.2 Operate controls and monitor compliance with internal controls policies and procedures | `cco:ont00000228` (Planned Act) | `ontology/slices/apqc_9_0.ttl line 3589` |

Readiness: no designating act type, since BPO's InternalControlCapability is a capability class (Q-12); BPO's enablesProcess names three act types (P10762, P21574, P10764), each the designating act of one of its three components, so an index would be the union of theirs; whether it is a capability area (CD16, E4) is open, and its link to the root is unresolved.

**Default Account Management** (`bcoc:DefaultAccountManagement`, BCC-38b3c836).

| Role | BPO class | PCF element | Typed under | Declared at the pin |
|---|---|---|---|---|
| designating class | `bpo:DefaultAccountManagementCapability` | — | `cco:ont00000568` (Organization Capability) | `ontology/slices/apqc_9_0.ttl line 676` |
| enablesProcess target | `bpo:P14007` | PCF 9.2.4.6 Perform recovery workout | `bpo:ActOfFormulation` (Act of Formulation) | `ontology/slices/apqc_9_0.ttl line 1629` |

Readiness: no designating act type, since BPO's DefaultAccountManagementCapability is a capability class (Q-12); BPO's enablesProcess names only P14007 (recovery workout, PCF 9.2.4.6), which Collections Management's index also takes; whether that one act suffices is the reviewer's question.

**Tax Management** (`bcoc:TaxManagement`, BCC-c64ca466).

| Role | BPO class | PCF element | Typed under | Declared at the pin |
|---|---|---|---|---|
| designating class | `bpo:TaxManagementCapability` | PCF 9.9 Manage taxes | `cco:ont00000568` (Organization Capability) | `ontology/slices/apqc_9_0.ttl line 251` |
| enablesProcess target | `bpo:P10866` | PCF 9.5.3.3 Calculate and pay applicable payroll taxes | `bpo:ActOfFinancialTransaction` (Act of Financial Transaction) | `ontology/slices/apqc_9_0.ttl line 2474` |

Readiness: no designating act type, since BPO's TaxManagementCapability is a capability class (Q-12); BPO's enablesProcess names only P10866 (payroll taxes), Payroll Tax Processing's act, which does not cover the definition.

**Treasury Management** (`bcoc:TreasuryManagement`, BCC-0ba10d44).

| Role | BPO class | PCF element | Typed under | Declared at the pin |
|---|---|---|---|---|
| designating class | `bpo:P10734` | PCF 9.7 Manage treasury operations | `cco:ont00000568` (Organization Capability) | `ontology/slices/apqc_9_0.ttl line 2812` |
| designating class | `bpo:TreasuryManagementCapability` | — | `cco:ont00000568` (Organization Capability) | `ontology/slices/apqc_9_0.ttl line 246` |
| enablesProcess target | `bpo:P10885` | PCF 9.7.1.1 Establish scope and governance of treasury operations | `bpo:ActOfFormulation` (Act of Formulation) | `ontology/slices/apqc_9_0.ttl line 2844` |
| enablesProcess target | `bpo:P10893` | PCF 9.7.2.1 Manage and reconcile cash positions | `bpo:ActOfAccounting` (Act of Accounting) | `ontology/slices/apqc_9_0.ttl line 2941` |
| enablesProcess target | `bpo:P12974` | PCF 9.7.5.1 Develop risk management/hedging strategy | `bpo:ActOfFormulation` (Act of Formulation) | `ontology/slices/apqc_9_0.ttl line 3226` |
| enablesProcess target | `bpo:P14079` | PCF 9.7.4.1 Establish investment policy | `bpo:ActOfFormulation` (Act of Formulation) | `ontology/slices/apqc_9_0.ttl line 3133` |

Readiness: its designating class P10734 is typed under a capability class (Q-12); BPO's enablesProcess names four act types (P10885, P10893, P12974, P14079), one from each of four components; its definition is preserved pending its recorded revision (R26).

## 3. Affected, but not blocked

These 8 ready concepts have a capability-typed designating class too. Their indexes
are drawn from the processes beneath, which BPO types as acts, so they are in the G1-T
batch. The designating class is excluded from each index (CAP-03), as the batch says.

| Concept | Candidate | BPO class | PCF element | Declared at the pin |
|---|---|---|---|---|
| Cash Management | BCC-a1c5454d | `bpo:P10759` | PCF 9.7.2 Manage cash | `ontology/slices/apqc_9_0.ttl line 2926` |
| In-House Bank Account Management | BCC-749adb52 | `bpo:P10760` | PCF 9.7.3 Manage in-house bank accounts | `ontology/slices/apqc_9_0.ttl line 3025` |
| Financial Risk Management | BCC-132e1b29 | `bpo:P11208` | PCF 9.7.5 Monitor and execute risk and hedging transactions | `ontology/slices/apqc_9_0.ttl line 3214` |
| Counterparty Credit Exposure Management | BCC-3e668a26 | `bpo:P11211` | PCF 9.7.5.4 Manage exposure risk | `ontology/slices/apqc_9_0.ttl line 3361` |
| Foreign Exchange Risk Management | BCC-7c04ea8a | `bpo:P11210` | PCF 9.7.5.3 Manage foreign exchange risk | `ontology/slices/apqc_9_0.ttl line 3293` |
| Hedging Transaction Execution | BCC-8fdf31c6 | `bpo:P20137` | PCF 9.7.5.5 Execute hedging transactions | `ontology/slices/apqc_9_0.ttl line 3420` |
| Interest Rate Risk Management | BCC-0564598d | `bpo:P11209` | PCF 9.7.5.2 Manage interest rate risk | `ontology/slices/apqc_9_0.ttl line 3236` |
| Treasury Policy Management | BCC-7757c12b | `bpo:P10758` | PCF 9.7.1 Manage treasury policies and procedures | `ontology/slices/apqc_9_0.ttl line 2826` |

## 4. What the decision would choose between

- **An upstream correction.** BPO retypes each class in section 1, and the designating
  classes of section 2, under an act genus, or declares an act type for the PCF element
  beside the capability class. Sending that request to BPO is the architect's call, under
  `communications/README.md`.
- **An existing valid mapping.** For section 2, the components' act types already exist.
  Taking them as the broader concept's index would make its index the union of its
  components'. That is a CD16 question as much as a Q-12 one. For section 1, no existing
  act type in the evidence fits, so this option would need act types found elsewhere in
  BPO and reviewed one by one.

Either way, no act type is invented here, and none of the 13 is admitted until it has an
index and a signed G1-T record.
