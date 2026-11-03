# Tranche 1 — readiness record (Phase I-5), draft for the architect's review

| Field | Value |
| --- | --- |
| Status | **Proposed.** A recommendation for formal review, not an approval (`docs/decisions/2026-11-03-i5-first-tranche-directed.md`) |
| Candidates | BCC-373b146e, BCC-d95f68fd, BCC-62e789bf, as the product owner named them |
| Catalog reviewed | `docs/catalog/candidates.yaml` at `9854052` (SHA-256 `4242de571a4b14309634bbab7c9513ae625d9214b82dcdf6c15e1fda3c6297d9`) |
| Specification | v0.4.0-draft.1 (in force for the tooling). G1-T is §8; it is not ratified (D4), so no record below can be a PASS |
| Conceptual model | CM-01, approved 2026-10-26 (SHA-256 `292c8f36…1ccc`) |
| Recorded by | Claude Code (`claude-opus-5-5`), 2026-11-03 |

The sections follow roadmap §7's eight conditions. The readiness review keeps four things
apart: **source terminology** (the labels below), **vocabulary ratification** (none is
proposed here), **taxonomy classification** (§5) and **OWL subclass assertion** (none: every
class stays under `cco:ont00000568` alone until it passes G1-T, CD3).

Derived in part from the APQC Process Classification Framework® 7.4 (element names and
IDs, cited from `docs/sources/inventory/pcf-7.4-entries.yaml`, under APQC's notice in
`NOTICE.md`). APQC does not endorse this work.

## Summary

| Candidate | Recommendation | What must happen before admission |
| --- | --- | --- |
| **BCC-373b146e** Customer Complaint Management Capability | **Ready for G1-T**, once G1-T is ratified | Record a reason for, or remove, the complaint-analysis act (CD5) |
| **BCC-d95f68fd** Payroll Processing Capability | **Ready for G1-T, with one resolution**: absorb BRM "Payroll" (BCC-b7c46718) as a federal synonym | Decide whether the index is drawn from the three component candidates; record a reason for two policy-setting acts (CD5) |
| **BCC-62e789bf** Accounts Payable Processing Capability | **Not ready as indexed**: one index member is an authorization act | Re-index "Approve payments" to a non-deontic act or remove it (G1-T question 4); settle the e-commerce member's scope |

Not in the tranche: **Procurement Capability (BCC-cc2de1a5)**, excluded by the direction
until its differentia is corrected. The generator now flags it and 24 other candidates
whose labels name only an ability (`9854052`). **Payments Approval Capability
(BCC-9ecf360b)** is rejected as a type: both of its acts authorize payment, which is
standing, not ability (CM-01, Authorization Record).

## 1. Candidate classes

| Tranche id | Candidate | Catalog key | Classification | Compatibility | Flags at `9854052` |
| --- | --- | --- | --- | --- | --- |
| T1-01 | BCC-373b146e | `management\|customer complaint` | capability | likely | none |
| T1-02 | BCC-d95f68fd | `administration\|payroll` | capability | likely | none |
| T1-03 | BCC-62e789bf | `administration\|account payable` | capability | likely | deontic index member |

The product owner's table recorded "no automated flags" for BCC-62e789bf. That was true
at `4625d0c`. The deontic flag added in `9854052` now applies to it.

## 2. Preferred terms and checked definitions

Each definition is rewritten from the generated draft, checked against CM-01's Business
Capability (borne by an Organization, grounded in its members as organized, realized only
by acts that exercise it) and CAP-07 (no deontic terms: none of authoriz-, licen-,
mandat-, responsib-, assign-, permit-).

**T1-01 Customer complaint management capability.**
*Generated:* "…to direct and control customer complaint on a continuing basis…". This is
too generic: it fits any management capability.
*Checked:* A business capability of an organization to take in complaints from its
customers, bring each to the members able to act on it, resolve and answer it, and
analyze complaints and how they were handled, grounded in the organization's members as
organized.

**T1-02 Payroll processing capability.**
*Generated:* "…to administer the recurring work of payroll…". This restates the name.
*Checked:* A business capability of an organization to determine, for each pay period,
what each of its employees is owed and what must be withheld, from time and earnings
records, and to pay it and account for it, grounded in the organization's members as
organized.

**T1-03 Accounts payable processing capability.**
*Generated:* "…to administer the recurring work of accounts payable…". This restates the
name.
*Checked:* A business capability of an organization to receive, verify and record the
amounts it owes its suppliers, settle them by payment, account for them, and answer
inquiries about them, grounded in the organization's members as organized.

## 3. Conceptual distinctions and candidate BFO/CCO parents

| Candidate | Parent before G1-T | Parent after a G1-T PASS | Distinguished from |
| --- | --- | --- | --- |
| T1-01 | `cco:ont00000568` Organization Capability | Business Capability, under `obo:BFO_0000016` Disposition (CD3) | the complaint-handling process (PCF 6.2.3, its acts); a customer service representative's skill (CM-01 Skill); authority to grant redress (an Authorization Record) |
| T1-02 | `cco:ont00000568` | as above | payroll as a catalog area (PCF 7.5.4 and 9.5 designate it); a payroll provider's capability (a Capability Sourcing Statement, G1-I question 3); authority to disburse funds |
| T1-03 | `cco:ont00000568` | as above | the approval of payment (standing, not ability); the AP system (an enabling condition, never basis: G1-T question 2) |

**Disposition interpretation**, the same for all three: each is read as a disposition of
the organization that is realized in acts of the kinds in its index, and that persists
while no such act occurs. It is grounded in members in positions (DP-1, Option A), not in
the systems they use. Losing an essential system leaves the capability in place and
changes its availability (CD2; CM-01 Enabling Condition).

## 4. Source provenance and evidence

| Candidate | Designating records | Rights |
| --- | --- | --- |
| T1-01 | BPO class `CustomerComplaintManagementCapability` (INV-BPO-CustomerComplaintManagementCapability-capability-class); PCF 6.2.3 "Manage customer complaints" (INV-PCF74-10389) | BPO MIT; PCF under APQC's notice |
| T1-02 | PCF 7.5.4 "Administer payroll" (INV-PCF74-10497); PCF 9.5 "Process payroll" (INV-PCF74-10732). Proposed synonym: FEAF-II BRM "Payroll" (INV-FEAF-BRM-SCD-624-brm-service, INV-FEAF-BRM-TAX-B10.805.624-brm-service) | PCF under APQC's notice; BRM U.S. Government work |
| T1-03 | PCF 9.6.1 "Process accounts payable (AP)" (INV-PCF74-10756) | PCF under APQC's notice |

Every record is harvested at a pinned commit or document digest, under the rights
decisions of 2026-10-28 and 2026-10-29. **Source adequacy:** the evidence is catalog
evidence: what the sources say an organization does, not a study showing that these are
dispositions. That is G1-T's to judge, and no source-adequacy exception is requested.

**Realization evidence: proposed realization indexes.** These are BPO act types at the
I-1 pin (`docs/catalog/bpo-act-types.yaml`), with BPO's genus. Each index lists what is
admissible and claims no completeness (CAP-30).

T1-01, five members, all through PCF 6.2.3:

| Act type | PCF | Genus (BPO) | Note |
| --- | --- | --- | --- |
| `bpo:P10397` | 6.2.3.1 Receive customer complaints | Act of Communication | |
| `bpo:P10398` | 6.2.3.2 Route customer complaints | Act of Communication | |
| `bpo:P10399` | 6.2.3.3 Resolve customer complaints | Act of Resolution | |
| `bpo:P10400` | 6.2.3.4 Respond to customer complaints | Act of Representative Communication | |
| `bpo:P19072` | 6.2.3.5 Analyze customer complaints and response/redressal | Act of Analysis | **CD5 question:** analysis of the handling, used to improve it, is development. Keep it with a recorded reason (the analysis is part of handling complaints), or remove it |

T1-02. Its own two act types are summary acts (`bpo:P10497`, Act of Administration;
`bpo:P10732`, Act of Financial Transaction). The acts that do the work belong to its three
narrower candidates. **Proposed:** the index is the union of those components' acts,
minus the policy-setting members:

| From | Act types | Note |
| --- | --- | --- |
| BCC-85fbcb90 Time Reporting (PCF 9.5.1) | `bpo:P10753`, `P10854`, `P10855`, `P10856`, `P10857` | `bpo:P10853` "Establish policies and procedures" (Act of Formulation) sets up the capability: **CD5, out unless a reason is recorded** |
| BCC-d105ff07 Pay Management (PCF 9.5.2) | `bpo:P10754`, `P10858` to `P10865` | `P10862` is under BPO's Act of Remuneration (itself under CCO's Act of Remuneration, per the vendored extract): the core exercise |
| BCC-394909c1 Payroll Taxes (PCF 9.5.3) | `bpo:P10755`, `P10866`, `P10867`, `P10868` | `bpo:P14075` "Develop tax plan" (Act of Formulation): **CD5, out unless a reason is recorded** |

T1-03, twelve members through PCF 9.6.1:

| Act type | PCF | Genus (BPO) | Note |
| --- | --- | --- | --- |
| `bpo:P10756` | 9.6.1 Process accounts payable (AP) | Act of Financial Transaction | summary act |
| `bpo:P10869` | 9.6.1.1 Verify AP pay file with purchase order vendor master file | Act of Appraisal | |
| `bpo:P10870` | 9.6.1.2 Maintain/Manage electronic commerce | Act of Monitoring | **scope:** e-commerce channel upkeep is not payables work; propose removal |
| `bpo:P10871` | 9.6.1.3 Audit invoices and key data in AP system | Act of Appraisal | |
| `bpo:P10872` | 9.6.1.4 Approve payments | Planned Act | **G1-T question 4 fails:** approval confers standing. Re-index to the review that precedes approval, which BPO does not yet type, or remove |
| `bpo:P10873` | 9.6.1.5 Process financial accruals and reversals | Act of Accounting | |
| `bpo:P10874` | 9.6.1.6 Process payables taxes | Act of Reporting | BPO's genus is questionable for a tax payment; a question for BPO, not a blocker |
| `bpo:P10875` | 9.6.1.7 Research/Resolve payable exceptions | Act of Information Processing | |
| `bpo:P10876` | 9.6.1.8 Process payments | Act of Financial Transaction | the core exercise |
| `bpo:P10877` | 9.6.1.9 Respond to AP inquiries | Act of Communication | |
| `bpo:P10878` | 9.6.1.10 Retain records | Act of Information Processing | |
| `bpo:P10879` | 9.6.1.11 Adjust accounting records | Act of Accounting | |

## 5. Taxonomic relationships (proposed, for Stage 03)

| Candidate | Broader (catalog) | Narrower (catalog) | Proposal |
| --- | --- | --- | --- |
| T1-01 | BCC-af1062de Customer Service Contacts Planning and Management (PCF 6.2) | none | keep; the broader is a component area, not yet reviewed |
| T1-02 | BCC-12db59b1 Employees Reward and Retention (PCF 7.5); BCC-4fda51aa Financial Resources Management (PCF 9.0, a `function`) | BCC-85fbcb90, BCC-d105ff07, BCC-394909c1 | one type with two catalog placements: PCF puts payroll under both HR and Finance, and that is designation, not two types. The narrower links are proper parts of the ability, not subtypes, so record them as components (CD16), not as `rdfs:subClassOf` |
| T1-03 | BCC-0fe1f7f0 Accounts Payable and Expense Reimbursements Processing (PCF 9.6) | BCC-9ecf360b Payments Approval (reject); BCC-9511900a Payments Processing and Distribution | keep the broader. Drop Payments Approval. Payments Processing and Distribution is shared with payroll (it merges PCF 9.5.2.5 and 9.6.1.8), so it is a component of both, not a subtype of either |

None of these is an OWL assertion. The "broader" links in the catalog mix whole-part and
kind-of relations, and Stage 03 has to separate them.

## 6. G1-T admission evidence (drafted; no PASS is possible before D4)

Questions as specification v0.4 §8 states them, with question 2 as DP-1 settled it.

| Question | T1-01 Complaints | T1-02 Payroll | T1-03 Payables |
| --- | --- | --- | --- |
| 1 Bearer is an Organization | Yes: handled for the organization by several members | Yes | Yes |
| 2 Basis is members in an arrangement, no artifact counted | Yes: service, product and finance positions in a routing arrangement; the case system is an enabling condition | Yes: payroll staff, HR and finance positions; the payroll system is an enabling condition | Yes: AP clerks, buyers and the reviewers who prepare approvals; the AP system is an enabling condition |
| 3 Organizational, not individual | Yes: intake, routing and resolution cross positions | Yes: time, earnings, deductions and payment cross HR and finance | Yes: matching, exception resolution and payment cross purchasing and finance |
| 4 Every index member non-deontic | Yes, as indexed. Granting redress is excluded | Yes, once the two CD5 items are settled (they are formulation, not deontic) | **No:** `bpo:P10872` Approve payments |
| 5 Exercise, not development | One question: `bpo:P19072` | Two questions: `bpo:P10853`, `bpo:P14075` | Yes |
| Draft outcome | Pass expected, given a CD5 reason or removal | Pass expected, given the index decision and the CD5 items | Fail as indexed; pass expected after re-indexing |

These are drafts by the recorder, for a reviewer. CAP-04 requires a PASS record with
reviewer and date, and none is given here.

## 7. Traceability

| To | T1-01 | T1-02 | T1-03 |
| --- | --- | --- | --- |
| CM-01 | P1 (capability and bearer), P2 (realization by BPO acts), Realization Index, Enabling Condition | as T1-01, plus P5 (catalog designation from two nodes) and Capability Sourcing Statement (outsourced payroll) | as T1-01, plus Authorization Record (the approval act) |
| Competency questions | CQ-2 (index), CQ-10 (not yet admitted), CQ-11 (the CD5 act) | CQ-2, CQ-7 (payroll is commonly sourced), CQ-10, CQ-11 | CQ-2, CQ-5 (approval needs an Authorization Record, not an index member), CQ-10 |
| Specification (draft) | CD3, CD4, CD5; CAP-03, CAP-04, CAP-06, CAP-07 | the same | the same |

The ratified specification does not exist yet (RP-1 to RP-10, ADR-002). This
traceability is to the drafts and must be re-checked at ratification.

## 8. Terminology relationships that affect formalization

| Item | Resolution proposed |
| --- | --- |
| BRM "Payroll" (BCC-b7c46718, key `provision\|payroll`) and Payroll Processing (`administration\|payroll`) | the same capability under two keys. Record BRM "Payroll" as a synonym of T1-02 and retire BCC-b7c46718 as a duplicate. The generator did not merge them because the BRM label has no action word |
| BPO's class `CustomerComplaintManagementCapability` | the source term for T1-01. BPO's class is not reused or redeclared: BCO would mint its own term at admission, and BPO's class is a designation of it |
| "Process" in two of the names | the names name the ability, not the process. A reviewer may prefer "payroll capability" and "accounts payable capability" |
| Homonym register (roadmap T4) | none of the three is a homonym of an ISO/IEC 33020, CMMI or FIBF use |

## What the architect is asked to decide

1. Whether to approve the tranche of three as the first candidates for G1-T, on the
   conditions in the Summary.
2. For T1-02: whether the realization index is drawn from its three components (§4).
3. For T1-03: re-index the approval act, or remove it.

Approving the tranche admits no type, accepts no vocabulary concept, and asserts nothing
in OWL (roadmap §7, T7).
