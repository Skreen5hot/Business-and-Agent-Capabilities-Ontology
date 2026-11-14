# Q-12 — recommendation for one consolidated BPO issue

| Field | Value |
|---|---|
| Status | **Proposed**, for the architect (`docs/decisions/2026-11-07-stage-03-ratified-g1t-review-authorized.md`, C). Not a communication: sending anything to BPO is the architect's call, under `communications/README.md`. It changes no BPO file and proposes no replacement act class |
| Date | 2026-11-07 |
| BPO pin | `bc64e91839378e1926189c01bf184d6a22d5c1b7` (Phase I-1), read through `docs/catalog/bpo-act-types.yaml` and `docs/sources/inventory/bpo-entries.yaml` |
| Builds on | `docs/catalog/tranche-2-q12.md` (the 13 blocked concepts and their dependencies), accepted as corrected |

The decision asks, before any retyping, whether each source class is actually
misclassified, or whether the BCO concept needs a different existing realization mapping.
The answer differs for the two groups.

## 1. The nine, and the designating classes of nine more: probably misclassified in BPO

BPO declares a class `bpo:P<element id>` for each PCF element it carries. Of 1823 such classes
at the pin, 1784 are typed under an act genus and 39 under `cco:ont00000568` (Organization
Capability). Nothing in the PCF separates the 39 from the rest:
- they sit at levels 2, 3 and 4, as act-typed classes do;
- 15 of the 39 are leaf processes with no children, such as 9.7.2.5 *Manage cash flows*;
- 41 other PCF elements named *Manage …* with child processes are typed as acts.

BPO's own capability classes are a separate set, named `…Capability` (for example
`bpo:TreasuryManagementCapability`), which designate PCF elements and enable processes. So the
39 `P` classes look like process types typed under a capability class by mistake, not
deliberate capabilities. For eight of the nine blocked concepts there is **no different
existing mapping**: each designating element is a leaf process, so no other BPO act class
covers it, and only BPO can unblock them. The ninth, Financial Planning and Management
Accounting (9.1), has four children, but they are its own components (Financial Planning,
Budgeting and Forecasting; Cost Accounting; Cost Management; Financial Performance
Management), so it raises the capability-area question of section 2 rather than a mapping
one.

The 39, with the tranche-2 dependency marked:

| BPO class | PCF element | Children | Declared at the pin | Tranche 2 |
|---|---|---|---|---|
| `bpo:P20866` | 8.7 Create and manage support services/solutions | 8 | `ontology/slices/apqc_8_0.ttl` line 1097 |  |
| `bpo:P20914` | 8.7.7 Manage infrastructure resource administration | 6 | `ontology/slices/apqc_8_0.ttl` line 1114 |  |
| `bpo:P10728` | 9.1 Perform planning and management accounting | 4 | `ontology/slices/apqc_9_0.ttl` line 951 | blocks a concept |
| `bpo:P10788` | 9.1.4.7 Manage continuous cost improvement | 0 | `ontology/slices/apqc_9_0.ttl` line 1276 | blocks a concept |
| `bpo:P10734` | 9.7 Manage treasury operations | 6 | `ontology/slices/apqc_9_0.ttl` line 2812 | designating class of a concept |
| `bpo:P10758` | 9.7.1 Manage treasury policies and procedures | 8 | `ontology/slices/apqc_9_0.ttl` line 2826 | designating class of a concept |
| `bpo:P10759` | 9.7.2 Manage cash | 8 | `ontology/slices/apqc_9_0.ttl` line 2926 | designating class of a concept |
| `bpo:P10894` | 9.7.2.2 Manage cash equivalents | 0 | `ontology/slices/apqc_9_0.ttl` line 2952 | blocks a concept |
| `bpo:P10897` | 9.7.2.5 Manage cash flows | 0 | `ontology/slices/apqc_9_0.ttl` line 2983 | blocks a concept |
| `bpo:P10899` | 9.7.2.7 Manage and oversee banking relationships | 0 | `ontology/slices/apqc_9_0.ttl` line 3004 | blocks a concept |
| `bpo:P10760` | 9.7.3 Manage in-house bank accounts | 7 | `ontology/slices/apqc_9_0.ttl` line 3025 | designating class of a concept |
| `bpo:P10901` | 9.7.3.1 Manage in-house bank accounts for subsidiaries | 0 | `ontology/slices/apqc_9_0.ttl` line 3041 |  |
| `bpo:P10761` | 9.7.4 Manage debt and investment | 8 | `ontology/slices/apqc_9_0.ttl` line 3118 |  |
| `bpo:P10908` | 9.7.4.2 Manage financial intermediary relationships | 0 | `ontology/slices/apqc_9_0.ttl` line 3143 | blocks a concept |
| `bpo:P10909` | 9.7.4.3 Manage liquidity | 0 | `ontology/slices/apqc_9_0.ttl` line 3153 | blocks a concept |
| `bpo:P10910` | 9.7.4.4 Manage issuer exposure | 0 | `ontology/slices/apqc_9_0.ttl` line 3163 | blocks a concept |
| `bpo:P11208` | 9.7.5 Monitor and execute risk and hedging transactions | 6 | `ontology/slices/apqc_9_0.ttl` line 3214 | designating class of a concept |
| `bpo:P11209` | 9.7.5.2 Manage interest rate risk | 4 | `ontology/slices/apqc_9_0.ttl` line 3236 | designating class of a concept |
| `bpo:P11210` | 9.7.5.3 Manage foreign exchange risk | 5 | `ontology/slices/apqc_9_0.ttl` line 3293 | designating class of a concept |
| `bpo:P11211` | 9.7.5.4 Manage exposure risk | 4 | `ontology/slices/apqc_9_0.ttl` line 3361 | designating class of a concept |
| `bpo:P20137` | 9.7.5.5 Execute hedging transactions | 5 | `ontology/slices/apqc_9_0.ttl` line 3420 | designating class of a concept |
| `bpo:P16958` | 9.7.6 Manage financial fraud/dispute cases | 0 | `ontology/slices/apqc_9_0.ttl` line 3497 | blocks a concept |
| `bpo:P19228` | 10.2.4.4 Manage safety, security, and access to sites | 0 | `ontology/slices/apqc_10_0.ttl` line 1123 |  |
| `bpo:P19250` | 10.3.2.5 Manage maintenance work safety | 0 | `ontology/slices/apqc_10_0.ttl` line 1313 |  |
| `bpo:P17060` | 11.1 Manage enterprise risk | 3 | `ontology/slices/apqc_11_0.ttl` line 474 |  |
| `bpo:P11010` | 12.1 Build investor relationships | 3 | `ontology/slices/apqc_12_0.ttl` line 599 |  |
| `bpo:P11035` | 12.1.1 Plan, build, and manage lender relations | 0 | `ontology/slices/apqc_12_0.ttl` line 614 |  |
| `bpo:P11036` | 12.1.2 Plan, build, and manage analyst relations | 0 | `ontology/slices/apqc_12_0.ttl` line 627 |  |
| `bpo:P11038` | 12.2.1 Manage government relations | 6 | `ontology/slices/apqc_12_0.ttl` line 658 |  |
| `bpo:P11039` | 12.2.2 Manage relations with quasi-government bodies | 4 | `ontology/slices/apqc_12_0.ttl` line 675 |  |
| `bpo:P11040` | 12.2.3 Manage relations with trade or industry groups | 3 | `ontology/slices/apqc_12_0.ttl` line 690 |  |
| `bpo:P11041` | 12.2.4 Manage lobby activities | 0 | `ontology/slices/apqc_12_0.ttl` line 704 |  |
| `bpo:P11012` | 12.3 Manage relations with board of directors | 2 | `ontology/slices/apqc_12_0.ttl` line 887 |  |
| `bpo:P11013` | 12.4 Manage legal and ethical issues | 9 | `ontology/slices/apqc_12_0.ttl` line 933 |  |
| `bpo:P11045` | 12.4.2 Manage corporate governance policies | 0 | `ontology/slices/apqc_12_0.ttl` line 960 |  |
| `bpo:P11047` | 12.4.4 Ensure compliance | 2 | `ontology/slices/apqc_12_0.ttl` line 980 |  |
| `bpo:P11048` | 12.4.5 Manage outside counsel | 6 | `ontology/slices/apqc_12_0.ttl` line 1016 |  |
| `bpo:P11049` | 12.4.6 Protect intellectual property | 4 | `ontology/slices/apqc_12_0.ttl` line 1113 |  |
| `bpo:P17471` | 13.3 Manage enterprise quality | 4 | `ontology/slices/apqc_13_0.ttl` line 1348 |  |

## 2. The four with component acts: a BCO question first, then one upstream gap

`bpo:InternalControlCapability`, `bpo:TaxManagementCapability`,
`bpo:DefaultAccountManagementCapability` and `bpo:TreasuryManagementCapability` are capability
classes by design, and not misclassified. What is missing is different for each:

| Concept | What blocks it | Where it is resolved |
|---|---|---|
| Internal Control | BPO has no act class for PCF 9.8 (element 10735). Its wiring names its three components' acts | **BCO**: whether it is a capability area, as the G1-T review recommends for Financial Accounting and Revenue and Receivables (CD16, E4). If it is, it needs no index of its own |
| Tax Management | No act class for PCF 9.9 (10736). Its wiring names only a payroll-tax act | **BCO**: the same area question; it has two components, Tax Planning and Tax Processing |
| Treasury Management | `bpo:P10734` (PCF 9.7) is one of the 39 above. Its wiring names one act from each of four components | **Both**: the pilot's definition is awaiting revision (R26), and its designating class is in the upstream list |
| Default Account Management | No act class for PCF 9.2.4.7 (14008). Its wiring names `bpo:P14007` (9.2.4.6, recovery workout), which Collections Management's index also takes | **BCO** may accept `bpo:P14007` as an existing mapping, since recovery workout is the handling of defaulted accounts. Otherwise, **upstream**: an act class for 9.2.4.7 |

## 3. The issue, if the architect sends one

One issue to BPO, with two questions, quoting the classes by IRI, module and line at the pin:

1. **Are the 39 `bpo:P…` classes typed under `cco:ont00000568` intended as capabilities, or
   as process types?** If process types, which act genus does BPO assign each? The BCO does
   not propose one, and does not assume Planned Act.
2. **Are act classes intended for PCF elements 10735 (9.8), 10736 (9.9) and 14008 (9.2.4.7)?**
   BPO designates them by capability classes but declares no act class for them.

Meanwhile the BCO needs nothing from BPO for the 43 in the G1-T batch. The eight affected
concepts there draw their indexes from processes BPO types as acts, and the review passes
seven of them (the eighth, Financial Risk Management, is recommended for withdrawal as a
capability area for other reasons).

## 4. What the architect decides

- Whether to send the issue, and through which channel.
- For Internal Control, Tax Management and Financial Planning and Management Accounting:
  whether to treat them as capability areas.
- For Default Account Management: whether `bpo:P14007` is an acceptable existing mapping.
- Treasury Management stays as it is until R26.
