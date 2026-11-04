# Tranche 1 — readiness record (Phase I-5), revision 3

| Field | Value |
| --- | --- |
| Status | **Approved for evaluation**: all three candidates (`docs/decisions/2026-11-04-i5-tranche-1-approved-for-evaluation.md`; `docs/decisions/2026-11-04-i5-proceed-payroll-synonym-ap-hold-lifted.md`). Not admitted: each waits for the ratified admission test (D4). Ready for evaluation is not approved for ontology inclusion |
| Candidates | T1-01 BCC-373b146e, T1-02 BCC-d95f68fd (canonical; BRM Payroll BCC-b7c46718 retired into it as a designation), T1-03 BCC-62e789bf (hold lifted on the seven-act index) |
| Catalog reviewed | `docs/catalog/candidates.yaml` at `9854052` (SHA-256 `4242de571a4b14309634bbab7c9513ae625d9214b82dcdf6c15e1fda3c6297d9`) |
| Specification | v0.4.0-draft.1 (in force for the tooling). G1-T is §8; it is not ratified (D4), so no record below can be a PASS |
| Conceptual model | CM-01, approved 2026-10-26 (SHA-256 `292c8f36…1ccc`) |
| Revisions | 1, proposed: `f320a67`, rebased as `1948237` (`docs/decisions/2026-11-03-i5-first-tranche-directed.md`). 2, the first decision of 2026-11-04 applied: `b7930e7`, rebased as `35c85ea`. 3, this one: the second decision of 2026-11-04 applied |
| Recorded by | Claude Code (`claude-opus-5-5`), 2026-11-03 and 2026-11-04 |

The sections follow roadmap §7's eight conditions. The readiness review keeps four things
apart: **source terminology** (the labels below), **vocabulary ratification** (none is
proposed here), **taxonomy classification** (§5) and **OWL subclass assertion** (none: every
class stays under `cco:ont00000568` alone until it passes G1-T, CD3).

Derived in part from the APQC Process Classification Framework® 7.4 (element names, IDs
and description wording, cited from `docs/sources/inventory/pcf-7.4-entries.yaml`, under
APQC's notice in `NOTICE.md`). APQC does not endorse this work.

## Summary

| Candidate | State after revision 2 | What remains before admission |
| --- | --- | --- |
| **T1-01** Customer Complaint Management | Index of 4, every member justified. The analysis act is excluded | G1-T ratification |
| **T1-02** Payroll Processing | Index of 11, drawn act by act from two of the three components; every policy-setting and summary act excluded. BRM "Payroll" confirmed as a designation of it (§8) | G1-T ratification |
| **T1-03** Accounts Payable Processing | Index rebuilt: 7 members, accepted for evaluation. Both removed acts are out, and three more are excluded | G1-T ratification |

**Payments Approval (BCC-9ecf360b) is rejected as an ability candidate** (decision act 5).
Its source evidence stays where it is, for possible standing-related modeling (CM-01,
Authorization Record): PCF 9.6.1.4 "Approve payments" (INV-PCF74-10872, `bpo:P10872`) and
PCF 6.3.2.8 "Authorize payment" (INV-PCF74-20104, `bpo:P20104`). The generated catalog
still shows it as `needs-review` with the deontic flag; the catalog is the generator's
output and is not hand-edited, and this record is where the disposition lives.

**BRM Payroll (BCC-b7c46718) is retired as a separate active candidate** (second decision of
2026-11-04, act 2): it and T1-02 designate one candidate capability, and BCC-d95f68fd is
canonical. Both BRM source records keep their provenance (§4, §8). The generated catalog
still lists BCC-b7c46718, for the same reason it still lists Payments Approval.

Not in the tranche: **Procurement Capability (BCC-cc2de1a5)**, excluded until its
differentia is corrected (`9854052` flags it and 24 others).

## 1. Candidate classes

| Tranche id | Candidate | Catalog key | Classification | Compatibility | Flags at `9854052` |
| --- | --- | --- | --- | --- | --- |
| T1-01 | BCC-373b146e | `management\|customer complaint` | capability | likely | none |
| T1-02 | BCC-d95f68fd | `administration\|payroll` | capability | likely | none |
| T1-03 | BCC-62e789bf | `administration\|account payable` | capability | likely | deontic index member (cleared by the rebuilt index, §4) |

## 2. Preferred terms and checked definitions

Each definition is rewritten from the generated draft, checked against CM-01's Business
Capability (borne by an Organization, grounded in its members as organized, realized only
by acts that exercise it) and CAP-07 (no deontic terms: none of authoriz-, licen-,
mandat-, responsib-, assign-, permit-). Revision 2 narrows each definition to what its
index now realizes.

**T1-01 Customer complaint management capability.**
*Generated:* "…to direct and control customer complaint on a continuing basis…". Too
generic: it fits any management capability.
*Checked:* A business capability of an organization to take in complaints from its
customers, bring each to the members able to act on it, resolve it, and answer the
customer, grounded in the organization's members as organized.
*Revision 2:* "and analyze complaints and how they were handled" is removed with the
analysis act (§4).

**T1-02 Payroll processing capability.**
*Generated:* "…to administer the recurring work of payroll…". Restates the name.
*Checked:* A business capability of an organization to determine, for each pay period,
what each of its employees is owed and what must be withheld, from recorded time and
earnings, to pay it and remit what is withheld, to account and report for it, and to
answer its employees about it, grounded in the organization's members as organized.
*Revision 2:* "from time and earnings records" becomes "from recorded time and earnings":
recording time is Time Reporting's exercise, and payroll consumes its result (§4).

**T1-03 Accounts payable processing capability.**
*Generated:* "…to administer the recurring work of accounts payable…". Restates the name.
*Checked:* A business capability of an organization to verify the amounts it owes its
suppliers against what was ordered and invoiced, resolve the exceptions, settle them by
payment, account for them, and answer inquiries about them, grounded in the
organization's members as organized.
*Revision 2:* "receive … and record" becomes "verify … against what was ordered and
invoiced", which the rebuilt index realizes. Approval is not in it: whoever approves a
payment exercises standing, which an Authorization Record states (CM-01).

## 3. Conceptual distinctions and candidate BFO/CCO parents

| Candidate | Parent before G1-T | Parent after a G1-T PASS | Distinguished from |
| --- | --- | --- | --- |
| T1-01 | `cco:ont00000568` Organization Capability | Business Capability, under `obo:BFO_0000016` Disposition (CD3) | the complaint-handling process (PCF 6.2.3, its acts); a customer service representative's skill (CM-01 Skill); service improvement from complaint analysis (development, CD5); authority to grant redress (an Authorization Record) |
| T1-02 | `cco:ont00000568` | as above | payroll as a catalog area (PCF 7.5.4 and 9.5 designate it); time reporting (a separate capability whose output it consumes); compensation design (BRM 254); a payroll provider's capability (a Capability Sourcing Statement, G1-I question 3); authority to disburse funds |
| T1-03 | `cco:ont00000568` | as above | the approval of payment (standing, not ability); records retention and tax filing (other capabilities exercised over AP's documents and liabilities); the AP system (an enabling condition, never basis: G1-T question 2) |

**Disposition interpretation**, the same for all three: each is read as a disposition of
the organization that is realized in acts of the kinds in its index, and that persists
while no such act occurs. It is grounded in members in positions (DP-1, Option A), not in
the systems they use. Losing an essential system leaves the capability in place and
changes its availability (CD2; CM-01 Enabling Condition).

## 4. Source provenance and realization evidence

| Candidate | Designating records | Rights |
| --- | --- | --- |
| T1-01 | BPO class `CustomerComplaintManagementCapability` (INV-BPO-CustomerComplaintManagementCapability-capability-class); PCF 6.2.3 "Manage customer complaints" (INV-PCF74-10389) | BPO MIT; PCF under APQC's notice |
| T1-02 | PCF 7.5.4 "Administer payroll" (INV-PCF74-10497); PCF 9.5 "Process payroll" (INV-PCF74-10732). Proposed synonym: FEAF-II BRM "Payroll" (INV-FEAF-BRM-SCD-624-brm-service, INV-FEAF-BRM-TAX-B10.805.624-brm-service) | PCF under APQC's notice; BRM U.S. Government work |
| T1-03 | PCF 9.6.1 "Process accounts payable (AP)" (INV-PCF74-10756) | PCF under APQC's notice |

Every record is harvested at a pinned commit or document digest, under the rights
decisions of 2026-10-28 and 2026-10-29. **Source adequacy:** the evidence is catalog
evidence, what the sources say an organization does, not a study showing that these are
dispositions. That is G1-T's to judge, and no source-adequacy exception is requested.

**Realization indexes.** BPO act types at the I-1 pin (`docs/catalog/bpo-act-types.yaml`),
with BPO's genus, each reached through the PCF record in the "Via" column. Every act the
catalog cites for the candidate, or for a component it draws on, is listed with its
disposition: **in**, or **out** and why. The test for **in** is the decision's: the act
exercises this capability itself, not only a component or a neighbour, and it is neither
policy-setting, summary, development (CD5) nor deontic (G1-T question 4). Each index lists
what is admissible and claims no completeness (CAP-30). No act is relabelled.

### T1-01: 4 in, 1 out

| Act type | Via (PCF) | Genus (BPO) | | Reason |
| --- | --- | --- | --- | --- |
| `bpo:P10397` | 6.2.3.1 Receive customer complaints | Act of Communication | **in** | intake is the first exercise of the ability |
| `bpo:P10398` | 6.2.3.2 Route customer complaints | Act of Communication | **in** | bringing each complaint to the members able to act on it: the organizational arrangement exercised (G1-T question 3) |
| `bpo:P10399` | 6.2.3.3 Resolve customer complaints | Act of Resolution | **in** | the core exercise. Correcting the situation is operational; any grant of redress that confers a right on the customer is standing and is not this act |
| `bpo:P10400` | 6.2.3.4 Respond to customer complaints | Act of Representative Communication | **in** | answering the customer completes the handling |
| `bpo:P19072` | 6.2.3.5 Analyze customer complaints and response/redressal | Act of Analysis | **out** | not demonstrated to exercise the capability: its source description gives its purpose as input to service improvement and customer profiling, which is development of the service (CD5), not handling a complaint (decision act 2) |

### T1-02: 11 in, 11 out

The catalog cites two acts for T1-02 itself and twenty for its three components. Each is
judged on its own; realizing a component is not taken as realizing T1-02.

| Act type | Via (PCF) | Component | Genus (BPO) | | Reason |
| --- | --- | --- | --- | --- | --- |
| `bpo:P10497` | 7.5.4 Administer payroll | T1-02 itself | Act of Administration | **out** | summary act: names the whole area |
| `bpo:P10732` | 9.5 Process payroll | T1-02 itself | Act of Financial Transaction | **out** | summary act |
| `bpo:P10753` | 9.5.1 Report time | BCC-85fbcb90 Time Reporting | Act of Information Processing | **out** | summary act of the component |
| `bpo:P10853` | 9.5.1.1 Establish policies and procedures | BCC-85fbcb90 | Act of Formulation | **out** | policy-setting (CD5) |
| `bpo:P10854` | 9.5.1.2 Collect and record employee time worked | BCC-85fbcb90 | Act of Information Processing | **out** | exercises Time Reporting; payroll consumes the time record but does not make it. BRM separates the two services (613 and 624), and so does this record |
| `bpo:P10855` | 9.5.1.3 Analyze and report paid and unpaid leave | BCC-85fbcb90 | Act of Analysis | **out** | leave tracking and reporting, not pay determination |
| `bpo:P10856` | 9.5.1.4 Monitor regular, overtime, and other hours | BCC-85fbcb90 | Act of Monitoring | **out** | monitoring hours worked is time reporting; overtime pay is determined downstream, in `P10858` and `P10859` |
| `bpo:P10857` | 9.5.1.5 Analyze and report employee utilization | BCC-85fbcb90 | Act of Analysis | **out** | workforce productivity analysis, not payroll |
| `bpo:P10754` | 9.5.2 Manage pay | BCC-d105ff07 Pay Management | Act of Financial Transaction | **out** | summary act of the component |
| `bpo:P10858` | 9.5.2.1 Enter employee time worked into payroll system | BCC-d105ff07 | Act of Information Processing | **in** | takes recorded time into the pay calculation: the start of determining what is owed |
| `bpo:P10859` | 9.5.2.2 Maintain and administer employee earnings information | BCC-d105ff07 | Act of Accounting | **in** | the earnings basis of what each employee is owed |
| `bpo:P10860` | 9.5.2.3 Maintain and administer applicable deductions | BCC-d105ff07 | Act of Accounting | **in** | determining what is withheld |
| `bpo:P10861` | 9.5.2.4 Monitor changes in tax status of employees | BCC-d105ff07 | Act of Monitoring | **in** | keeps withholding correct each period |
| `bpo:P10862` | 9.5.2.5 Process and distribute payments | BCC-d105ff07 | Act of Remuneration | **in** | the core exercise: paying what is owed. Also cited by BCC-9511900a, a shared component (§5) |
| `bpo:P10863` | 9.5.2.6 Process and distribute manual checks | BCC-d105ff07 | Act of Financial Transaction | **in** | paying incorrect or omitted amounts: the same ability, off cycle |
| `bpo:P10864` | 9.5.2.7 Process period-end adjustments | BCC-d105ff07 | Act of Accounting | **in** | accounting for pay and withholding at period end |
| `bpo:P10865` | 9.5.2.8 Respond to employee payroll inquiries | BCC-d105ff07 | Act of Information Processing | **in** | answering for a pay determination draws on the same ability. A reviewer may hold this one out; T1-03's `P10877` is judged the same way |
| `bpo:P10755` | 9.5.3 Manage and process payroll taxes | BCC-394909c1 Payroll Taxes | Act of Financial Transaction | **out** | summary act of the component |
| `bpo:P14075` | 9.5.3.1 Develop tax plan | BCC-394909c1 | Act of Formulation | **out** | planning to reduce liability: formulation (CD5) |
| `bpo:P10866` | 9.5.3.3 Calculate and pay applicable payroll taxes | BCC-394909c1 | Act of Financial Transaction | **in** | determining and remitting what was withheld |
| `bpo:P10867` | 9.5.3.4 Produce and distribute employee annual tax statements | BCC-394909c1 | Act of Reporting | **in** | reports to each employee what was paid and withheld |
| `bpo:P10868` | 9.5.3.5 File regulatory payroll tax forms | BCC-394909c1 | Act of Reporting | **in** | reports pay and withholding to the tax authority. Filing discharges an obligation and confers no standing, so it is not deontic (G1-T question 4) |

The genera are BPO's, read from `bpo-act-types.yaml`, where BPO types several of these
acts directly under CCO genera (Act of Information Processing, `cco:ont00000366`).

**Payroll tax operations are distinct from tax planning and general business tax
preparation** (second decision of 2026-11-04, act 3). The index holds the operations: `P10866`,
`P10867`, `P10868`. Planning (`P14075`) is out above, and T1-03's `P10874`, the
enterprise's tax returns, is out of both indexes.

PCF 9.5.3.2 "Manage tax plan" (INV-PCF74-14076) has no BPO act type at the pin, so the
catalog cites none for it. It would be out in any case, with `P14075`: managing a plan to
reduce liability is formulation.

**Effect on the components.** No act from BCC-85fbcb90 Time Reporting is in the index:
on this reading it is a separate capability whose output T1-02 consumes, not a part of
it. BCC-d105ff07 and BCC-394909c1 contribute every non-summary, non-policy act they have.

### T1-03: 7 in, 5 out

Rebuilt from the twelve acts the inventories already give for PCF 9.6.1. No act was added
from outside them, and none relabelled.

| Act type | Via (PCF) | Genus (BPO) | | Reason |
| --- | --- | --- | --- | --- |
| `bpo:P10756` | 9.6.1 Process accounts payable (AP) | Act of Financial Transaction | **out** | summary act; its source description also takes in developing AP policies and procedures |
| `bpo:P10869` | 9.6.1.1 Verify AP pay file with purchase order vendor master file | Act of Appraisal | **in** | matching what is to be paid against what was ordered |
| `bpo:P10870` | 9.6.1.2 Maintain/Manage electronic commerce | Act of Monitoring | **out** | removed (decision act 4): tracking online transactions is not payables work |
| `bpo:P10871` | 9.6.1.3 Audit invoices and key data in AP system | Act of Appraisal | **in** | checking each invoice before it is paid. This, with `P10869`, is the verification that precedes approval; it is already typed, so nothing needs to be re-indexed from the approval act |
| `bpo:P10872` | 9.6.1.4 Approve payments | Planned Act | **out** | removed (decision act 4): approval exercises standing. Its source description reads as payment processing, which `P10876` already covers; the act is not relabelled to count it |
| `bpo:P10873` | 9.6.1.5 Process financial accruals and reversals | Act of Accounting | **in** | records what is owed before it is paid |
| `bpo:P10874` | 9.6.1.6 Process payables taxes | Act of Reporting | **out** | not shown to be payables work: its source description is preparing the enterprise's tax returns, an exercise of a tax capability |
| `bpo:P10875` | 9.6.1.7 Research/Resolve payable exceptions | Act of Information Processing | **in** | resolving the amounts that fail verification |
| `bpo:P10876` | 9.6.1.8 Process payments | Act of Financial Transaction | **in** | the core exercise: settling by payment. Also cited by BCC-9511900a (§5) |
| `bpo:P10877` | 9.6.1.9 Respond to AP inquiries | Act of Communication | **in** | answering for amounts, dates and discounts owed draws on the same ability |
| `bpo:P10878` | 9.6.1.10 Retain records | Act of Information Processing | **out** | keeping bills for later reference is records retention, exercised over AP's documents, not payables processing |
| `bpo:P10879` | 9.6.1.11 Adjust accounting records | Act of Accounting | **in** | correcting the payables accounts |

With `P10872` out, no index member of T1-03 approves, authorizes, certifies or licenses.
The catalog's deontic flag on BCC-62e789bf stays in the generated file; it describes the
catalog's evidence, not this index.

## 5. Taxonomic relationships (proposed, for Stage 03)

| Candidate | Broader (catalog) | Narrower (catalog) | Proposal |
| --- | --- | --- | --- |
| T1-01 | BCC-af1062de Customer Service Contacts Planning and Management (PCF 6.2) | none | keep; the broader is a component area, not yet reviewed |
| T1-02 | BCC-12db59b1 Employees Reward and Retention (PCF 7.5); BCC-4fda51aa Financial Resources Management (PCF 9.0, a `function`) | BCC-85fbcb90, BCC-d105ff07, BCC-394909c1 | one type with two catalog placements: designation, not two types. BCC-d105ff07 and BCC-394909c1 are components (CD16), not subtypes. BCC-85fbcb90 Time Reporting is proposed as **not** a component: a separate capability T1-02 depends on, as BRM separates them. PCF's placement of 9.5.1 under 9.5 is designation |
| T1-03 | BCC-0fe1f7f0 Accounts Payable and Expense Reimbursements Processing (PCF 9.6) | BCC-9ecf360b Payments Approval (rejected); BCC-9511900a Payments Processing and Distribution | keep the broader. Payments Approval is rejected as an ability candidate and leaves the taxonomy. Payments Processing and Distribution merges PCF 9.5.2.5 and 9.6.1.8, so it is a component of both T1-02 and T1-03, not a subtype of either |

None of these is an OWL assertion. The catalog's "broader" links mix whole-part and
kind-of relations, and Stage 03 has to separate them. No object property is proposed.

## 6. G1-T admission evidence (drafted; no PASS is possible before D4)

Questions as specification v0.4 §8 states them, with question 2 as DP-1 settled it.

| Question | T1-01 Complaints | T1-02 Payroll | T1-03 Payables |
| --- | --- | --- | --- |
| 1 Bearer is an Organization | Yes: handled for the organization by several members | Yes | Yes |
| 2 Basis is members in an arrangement, no artifact counted | Yes: service, product and finance positions in a routing arrangement; the case system is an enabling condition | Yes: payroll, HR and finance positions; the payroll system is an enabling condition | Yes: AP clerks, buyers and finance positions; the AP system is an enabling condition |
| 3 Organizational, not individual | Yes: intake, routing and resolution cross positions | Yes: earnings, deductions, payment and tax reporting cross HR and finance | Yes: matching, exception resolution and payment cross purchasing and finance |
| 4 Every index member non-deontic | Yes. Granting redress is not indexed | Yes. Tax filing is reporting, not standing | Yes, as rebuilt. `P10872` is out |
| 5 Exercise, not development | Yes, with `P19072` out | Yes, with `P10853` and `P14075` out | Yes |
| Draft outcome | Pass expected | Pass expected | Pass expected |

Drafts by the recorder, for a reviewer. CAP-04 requires a PASS record with reviewer and
date, and none is given here.

## 7. Traceability

| To | T1-01 | T1-02 | T1-03 |
| --- | --- | --- | --- |
| CM-01 | P1 (capability and bearer), P2 (realization by BPO acts), Realization Index, Enabling Condition | as T1-01, plus P5 (catalog designation from two nodes) and Capability Sourcing Statement (outsourced payroll) | as T1-01, plus Authorization Record (the approval act, outside the index) |
| Competency questions | CQ-2 (index), CQ-10 (not yet admitted), CQ-11 (the excluded development act) | CQ-2, CQ-7 (payroll is commonly sourced), CQ-10, CQ-11 | CQ-2, CQ-5 (approval needs an Authorization Record, not an index member), CQ-10 |
| Specification (draft) | CD3, CD4, CD5; CAP-03, CAP-04, CAP-06, CAP-07 | the same, plus CD16 (components) | the same |
| Decisions of 2026-11-04 | first, act 2 | first, act 3; second, acts 2 to 4 | first, acts 4 and 5; second, act 5 |

Every index member traces to its PCF record (column "Via") and, for T1-02, to its
originating component. The ratified specification does not exist yet (RP-1 to RP-10,
ADR-002): this traceability is to the drafts and must be re-checked at ratification.

## 8. Terminology relationships that affect formalization

| Item | State |
| --- | --- |
| BRM "Payroll" (BCC-b7c46718, key `provision\|payroll`) and T1-02 (`administration\|payroll`) | **Confirmed: one candidate capability, two designations** (second decision of 2026-11-04, act 2). BCC-d95f68fd is canonical; BCC-b7c46718 is retired as a separate active candidate. BRM "Payroll" (SCD 624, TAX B10.805.624) is recorded as an alternative designation of T1-02, not a new type, with both source records and their provenance kept. BRM's sibling services Time Reporting (613) and Employee Benefits and Compensation (254) stay outside it. No `owl:equivalentClass` is asserted and no object property is proposed |
| BPO's class `CustomerComplaintManagementCapability` | the source term for T1-01. BPO's class is not reused or redeclared: BCO would mint its own term at admission, and BPO's class is a designation of it |
| "Process" in two of the names | the names name the ability, not the process. A reviewer may prefer "payroll capability" and "accounts payable capability" |
| Homonym register (roadmap T4) | none of the three is a homonym of an ISO/IEC 33020, CMMI or FIBF use |

## What remains

1. **All three:** G1-T ratification (D4, roadmap: CP-0). Until then no record above is a
   PASS, and nothing is asserted in OWL (roadmap §7, T7).
2. Nothing else is open in this record. The tranche is not to be expanded (second decision of
   2026-11-04, act 7).
