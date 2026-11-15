# Tranche 2 — follow-up after the signature: wording notes and `P14057`

| Field | Value |
|---|---|
| Status | Triage under the architect's direction of 2026-11-15 (`docs/decisions/2026-11-15-tranche-2-remaining-issues-and-d5-preparation.md`, D and E). Not a review, and not a G1-T record. It changes no signed definition, realization index or finding |
| Date | 2026-11-15 |
| Signed baseline | `docs/catalog/admission/G1T-T2-batch.md`, revision 5, SHA-256 `b44ec9ea2af76a9cbf48fcb125a94b93c88076475603532bf23fc32106bd90ef`. It is kept byte for byte, so the corrections below are entered here as errata and not edited into it |
| Notes triaged | The non-blocking notes in section 3 of `docs/catalog/admission/G1T-T2-supplementary-review.md` (SHA-256 `1430f89b…b648`) on the six types it passed. Its T2-25 findings were settled by the architect's final direction on T2-25 and are not repeated |

Derived in part from the APQC Process Classification Framework® 7.4 (element names and
IDs, and the short descriptions quoted from it, under APQC's notice in `NOTICE.md`). APQC
does not endorse this work.

## 1. Triage

Each note is one of four kinds:

- **Erratum.** An explanation, exclusion reason or reference in the signed batch is
  corrected here (section 2). The definition, index and finding are unchanged.
- **Source check.** The note shows a possible mismatch between a BPO act's source meaning
  and an admitted definition. A focused check of that type is done before it is formalized
  (section 3), and only that type is returned to the architect if the check finds a
  substantive defect.
- **Held.** The correction is editorial, but it would change a vocabulary record's digest,
  which the signature record lists (section 4).
- **Closed.** Nothing to do.

| # | Type | The note, in short | Kind | Where |
|---|---|---|---|---|
| N1 | T2-02 Corporate Card Management | "Reconciling ... and settling them" rests on `P20933` alone | Source check | §3, SC-1 |
| N2 | T2-02 | `P20932`'s CAP-06 reason says the capability "provides" a card | Erratum | §2, E-1 |
| N3 | T2-04 Capital Investment Appraisal | `P10751` is also a summary act, coded Q4 rather than SUMMARY | Erratum | §2, E-2 |
| N4 | T2-17 Control Environment and Risk Objective Formulation | The Formulation reading is applied by extension. The label abbreviates "process objectives and risks" | Closed | The signature's Confirmation 1 extends the reading. The definition governs the label |
| N5 | T2-24 Cost Driver and Critical Activity Analysis | The part-of link's reason reads as an input relation | Erratum | §2, E-3 |
| N6 | T2-24 | `P10780`'s description limits critical activities to the finance function | Source check | §3, SC-2 |
| N7 | T2-31 Customer Credit Management | `P10792`'s description ("account payable reports") does not match its name | Source check and erratum | §3, SC-3; §2, E-4 |
| N8 | T2-31 | The definition says nothing of reporting; "and report on them" is optional | Closed | Adding it would change a signed definition. Not required by the review |
| N9 | T2-31 and T2-02 | The definitional source cites only the summary elements (`P10742`, `P20929`) | Held | §4 |
| N10 | T2-43 Internal Control Effectiveness Monitoring | `P10919`'s exclusion reason ends "not its operation"; OTHER would fit better than Q5 | Erratum | §2, E-5 |

## 2. Errata to the signed batch

Each erratum governs over the batch's text where the two differ. Each one names the
batch line, as the batch is at the signed digest.

| Id | Batch line | Reads | Corrected to | What it does not change |
|---|---|---|---|---|
| E-1 | 262 (T2-02, `bpo:P20932` index row) | "CAP-06: ordering a card from the issuer is how the capability provides one to a member: an exercise, not an enlargement of the capability" | "CAP-06: ordering obtains the card from the issuer for a member's business use: an exercise, not an enlargement of the capability" | The member, its genus and the CAP-06 finding |
| E-2 | 373 (T2-04, `bpo:P10751` exclusion row) | "the designating process joins capital planning with project approval, and its name makes approval part of it" | Unchanged, with this added: "It is also a summary act over four children (PCF 9.4.1), so SUMMARY applies too. Either code excludes it; Q4 is kept as signed" | The code (Q4) and the exclusion |
| E-3 | 1352 (T2-24, taxonomy row) | "coverage: identifying and measuring cost drivers and critical activities is part of the analysis on which managing costs draws; …" | "coverage: identifying and measuring cost drivers and critical activities is part of deciding which costs to avoid or reduce, which is Cost Management's work as its definition states it; …", with the rest of the row kept | The link (retained, `part-of`), and no subclass axiom |
| E-4 | 1709 (T2-31, `bpo:P10792` index row) | "process beneath it" | "process beneath it. Its PCF description speaks of accounts-payable reports, which does not match its name; the name and its place under 9.2.1 govern, as the review of 2026-11-07 held for T2-05" | The member |
| E-5 | 2346 (T2-43, `bpo:P10919` exclusion row) | "… which is Internal Control Design's work or the capability's improvement, not its operation" | "… which is Internal Control Design's work or the capability's improvement, not monitoring. OTHER (another capability's object) would describe it as exactly as Q5; Q5 is kept as signed" | The code (Q5) and the exclusion |

## 3. Focused source checks, before the affected type is formalized

Each check has one question, asked of the cited PCF and BPO records only. It does not
reopen the type's G1-T record. A check that finds a substantive defect isolates the type
from its formalization tranche and returns that change alone to the architect.

| Id | Type | Question | Evidence to read | Until it is done |
|---|---|---|---|---|
| SC-1 | T2-02 `bcoc:CorporateCardManagement` | Does `P20933` (9.6.3.4 Manage corporate credit card accounts; PCF: "Handling credit card accounts of business customers"; Act of Accounting, output an account statement) cover "reconciling what is spent on them and settling them"? The architect's part 4 accepted that reading, and no separate settlement act exists at the BPO pin | The PCF entry, the BPO class and its output, and PCF 9.6.3's other children | T2-02 is not formalized |
| SC-2 | T2-24 `bcoc:CostDriverAndCriticalActivityAnalysis` | `P10780` (9.1.3.3 Determine critical activities) describes "those business activities carried out by the financial function". Does the definition's "its critical activities" outrun it, or does the name govern, as elsewhere? | The PCF entry and the BPO class | T2-24 is not formalized |
| SC-3 | T2-31 `bcoc:CustomerCreditManagement` | Does `P10792` (9.2.1.6 Produce credit/collection reports), whose description speaks of accounts-payable reports, support "monitor their credit activity"? | The PCF entry, the BPO class and its output, and PCF 9.2.1's other children | T2-31 is not formalized |

## 4. Held: definitional-source locators

For T2-31 and T2-02, the vocabulary entry's definitional source still cites only the
summary element (`P10742`, `P20929`), and the narrowed concepts cite their index members.
Updating the locator changes the vocabulary record's digest, and the signature record
lists that digest. The update is held for the architect, who may choose either option:

1. **Now.** Apply it as a `revises` change with a change note, in a commit of its own, and
   name the new digests.
2. **When the type is formalized.** Apply it then, as part of that type's Stage 05 record.

The definition, index and finding do not change either way.

## 5. `bpo:P14057`, queued for semantic curation

| Field | Value |
|---|---|
| Act | `bpo:P14057`, PCF 9.1.2.2 *Perform profit center accounting*. PCF: "Determining the revenue, profits, and losses incurred by each unit within the organization that produces profit." |
| BPO typing at the pin | `bpo:ActOfAccounting`, output `bpo:ProfitabilityAnalysis`. Declared in `ontology/slices/apqc_9_0.ttl`, line 1069, at `bc64e91` (`docs/catalog/bpo-act-types.yaml`) |
| Where it stands | Excluded from T2-23 Cost Accounting as OTHER (batch line 1297). The exclusion is kept. Not in T2-25 Financial Performance Analysis, and not to be added to it merely to place the act. No concept's index holds it, and it has no catalog candidate of its own: it is evidence beneath Cost Accounting's candidate (`docs/catalog/candidates.yaml`, `via: INV-PCF74-14057`) |
| Recorded as | Source evidence for a possible distinct concept, *Profit Centre Accounting*. No concept, IRI or class is created |
| When | The next semantic-curation batch that covers PCF 9.1, with the other acts left without a concept (review of 2026-11-07, MD-6) |
| The comparison to make then | Its meaning and specialization against Cost Accounting (what products, services, processes and projects cost) and against Financial Performance Analysis (appraising the performance and profitability of products, customers or activities). Profit-centre results are a unit's revenue, profit and loss, which neither definition names |
| If a distinct type is justified | The normal path: a vocabulary concept under the controlled-vocabulary build, its links under the Stage 03 standard, and its own G1-T record. No OWL class or object property is authorized |
