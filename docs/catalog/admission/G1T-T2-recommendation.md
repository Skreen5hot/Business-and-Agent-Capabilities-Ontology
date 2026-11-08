# G1-T tranche 2 — consolidated review and batch admission recommendation

| Field | Value |
|---|---|
| Status | **For the architect's batch decision** (`docs/decisions/2026-11-07-stage-03-ratified-g1t-review-authorized.md`, B and E). One decision, not 43 approvals. Admits nothing: a class is admitted only by a signed PASS in its confirmation row |
| Date | 2026-11-07 |
| Records | `docs/catalog/admission/G1T-T2-batch.md`, revision 2 (the 43 records); `docs/catalog/admission/G1T-T2-review-2026-11-07.md` (the independent review, filed as received, SHA-256 `7c7efb831cf6a5276fe6e173cea34f4a3f40af7f4d5adae3e8e881c175671e08`) |
| Drafting | Claude Code (`claude-opus-5-5`), Ontologist (drafting) |
| Independent review | An independently instantiated Claude agent, model Claude Opus 5.5 (`claude-opus-5-5`), as a synthetic ontology reviewer in an Ontologist capacity, 2026-11-07. It took no part in the drafting run, was given the files and the rules but not the drafter's reasoning, and reviewed revision 1 at `72401ef`. It is a different instance, with a different function, from the finance-domain practitioner who reviewed the terminology. Its review is not a signature |
| Preserved | T1-02 and T1-03, signed 2026-11-05, unchanged and not re-reviewed |

## 1. Counts

| Finding | Count | Classes |
|---|---|---|
| PASS | **33** | Batch A (17) and Batch B (16), section 4 |
| PENDING REVIEW | **10** | T2-02, T2-04, T2-06, T2-17, T2-24, T2-25, T2-27, T2-31, T2-37, T2-43 |
| FAIL | **0** | — |

PENDING REVIEW is not a failure and not an admission. No class fails a G1-T question on its
bearer, basis or arrangements. The pending classes either need a decision or a correction,
or are recommended for withdrawal as capability areas.

No PASS rests on the cited IRIs existing or on the draft's recommendation. The review
re-read all 182 members and 56 exclusions of revision 1 against the evidence. It found
the drafting recommendation wrong in ten classes, and the records themselves deficient in
all 43 (section 3).

## 2. The eight open questions

| # | Class | Question | Resolution |
|---|---|---|---|
| OQ-1 | T2-02 Corporate Card Management | Question 4 | **Not met as drafted.** "Set their terms" is the deontic work the index excludes, and the summary act `bpo:P20929` has the three Q4 acts as parts. It passes once the phrase is deleted and the summary act removed. PENDING |
| OQ-2 | T2-04 Capital Planning | One-act index | **A thin index is admissible, and there is no wait for BPO.** But "identify" and "budget for them" have no member, so the definition must narrow to appraising the financial case (`bpo:P10847`). That changes the type, so the label ("Capital Planning" or "Capital Investment Appraisal") is the architect's. PENDING |
| OQ-3 | T2-06 Financial Accounting | Area or type | **A capability area.** Its only member was the level-2 summary act PCF 9.3, the same shape as 9.4 and 9.6, which are already withheld as areas. Withdraw from G1-T. PENDING |
| OQ-4 | T2-07 Accounting Policy Management | Question 4 | **Met, on the Formulation reading.** Formulating and publishing a policy is describable without standing; adopting it with authority is a separate act, outside the index, as T1-02 treated policy-setting. The definition's "set" becomes "formulate". PASS |
| OQ-5 | T2-17 Internal Control Design | Question 4 | **Met for the three leaf acts, not for the summary act `bpo:P10762`**, whose parts assign responsibility and establish a board. With it out, no member defines a control, so the scope needs a decision: narrow to defining the control environment and risk objectives, or hold. PENDING |
| OQ-6 | T2-27 Revenue and Receivables Management | Area or type | **A capability area.** Its definition joins five components' work, over one level-2 summary act whose source description matches none of them. Withdraw from G1-T. PENDING |
| OQ-7 | T2-31 Customer Credit Management | Question 4 | **Not met as drafted.** Setting a customer's credit limit grants standing, as approving a card limit does (T2-02, `bpo:P20934`). Reword the definition to evaluating requests and the credit to be extended; remove the summary act `bpo:P10742`; move `bpo:P14188` (credit-scoring criteria) out under Q5. PENDING |
| OQ-8 | T2-42 Treasury Policy Management | Question 4 | **Met, on the same Formulation reading as OQ-4.** "Set" becomes "formulate"; `bpo:P10885` also carries a Q4 note; `bpo:P10889` (audit) stays, with a note. PASS |

I agree with all eight. OQ-7 corrects my drafting: T2-31 and T2-02 treated the same kind of
limit differently.

## 3. Material defects

**In the records, all now corrected in revision 2.** All four were drafting errors of mine,
and the review is right on each:

| | Defect | Correction in revision 2 |
|---|---|---|
| MD-1 | No record carried the worked constant-membership cases (b3). CAP-04 fails a record without them, so every record would have failed | Five cases, worked by family (section 2 of the batch), adopted by each record |
| MD-2 | 25 indexes kept their designating summary act. Tranche 1's signed practice excluded every summary act, a class's own included | All 25 excluded under a SUMMARY code: 182 members become 157. The review also allows a narrower rule (keep a summary act when every child is kept, 5 classes). I applied the stricter one, consistent with tranche 1. The architect may choose the other |
| MD-3 | The question 2 and 3 answers were boilerplate. Question 3's "division of work" implied several positions, contrary to b1 | Question 2 names the family's feasible alternative and keeps the CD2 escalation. Question 3 states that the arrangements may be one member |
| MD-4 | The rule kept `kind-of` subtypes' acts out of a supertype's index | Rule corrected. It affects only T2-37 |
| MD-5 | The same kind of act carried different exclusion codes | Aligned (`P20930`, `P10885`) |

**In definitions: the review's MD-7, not applied.** Sixteen PASS classes (Batch B) and the
seven to re-present need definition corrections. They are listed exactly in each record's
"Correction proposed" row. They change terminology the architect accepted as the baseline,
so they are put to the decision here. Typical cases:
- deleting a clause with no index member, as in T2-11 "present the documents" and T2-21 "reconcile";
- removing success phrasing, as in T2-32 "accurate" and T2-35 "so that it is positioned";
- naming what the index holds, as in T2-14 duty calculation and value conversion;
- the Formulation reading, as in T2-07 and T2-42.

**Not conditions of admission** (MD-6, curation follow-ups): eight acts excluded as
"another concept's work" are held by no concept's index, and the tranche-2 review should
assign them at its next revision.

## 4. Recommendation for one batch decision

1. **Batch A, 17 classes: admit on the named reviewer's signature of the revision-2
   records.** No definition changes: T2-08, 09, 10, 12, 13, 15, 16, 18, 19, 22, 28, 29, 30, 34,
   36, 39, 41.
2. **Batch B, 16 classes: approve their definition corrections (MD-7), then admit on
   signature.** The classes are T2-01, 03, 05, 07, 11, 14, 20, 21, 23, 26, 32, 33, 35, 38, 40
   and 42.
   - On approval, I apply the corrections to the vocabulary, each concept revision citing
     its prior record, and to the records. The corrected definitions are checked against
     CAP-07 before signature.
   - T2-07 and T2-42 also need the Formulation reading of question 4 accepted. If the
     reviewer rejects it, the two are reclassified, not staged (b4).
3. **Withdraw three as capability areas**: T2-06 Financial Accounting, T2-27 Revenue and
   Receivables Management, T2-37 Financial Risk Management. This is the treatment already
   given to the five tranche-2 areas. It is not a FAIL, and their components stand on their
   own indexes.
4. **Re-present seven after correction, in one short supplementary review**, each with the
   choice it needs:

   | Class | Choice needed |
   |---|---|
   | T2-02 Corporate Card Management | the definition fix and removal of the summary act |
   | T2-31 Customer Credit Management | the definition fix and removal of the summary act |
   | T2-04 Capital Planning | the narrowed definition and its label |
   | T2-17 Internal Control Design | narrow the scope or hold |
   | T2-43 Internal Control Operation and Monitoring | narrow the scope or hold |
   | T2-24 Cost Management | narrow or hold |
   | T2-25 Financial Performance Management | bound "act on the results", and decide on `bpo:P10785` |

   None of them needs a new BPO act type.
5. **Name the reviewer** who signs. Tranche 1's was Aaron Damiano.

This would admit up to 33 classes from tranche 2 at signature, 17 at once and 16 after one
round of definition corrections. Nothing becomes OWL: under Option B, nothing is asserted
before all of CP-0 and D5.

## 5. Remaining Q-12 dependencies

None of the 43 is blocked by Q-12. Seven of the eight concepts with a capability-typed
designating class pass: T2-35, 36, 38, 39, 40, 41 and 42. The eighth, T2-37, is recommended
for withdrawal for another reason. The 13 blocked concepts stay out of the batch. The
recommendation on them, one upstream issue and three BCO-side questions, is
`docs/proposals/2026-11-07-bpo-q12-issue-recommendation.md`.
