# G1-T tranche 2: supplementary review of the seven corrected records

## 1. Header

| Field | Value |
|---|---|
| Reviewer | An independently instantiated Claude agent, model Claude Opus 5.5 (`claude-opus-5-5`), acting as synthetic ontology reviewer in an Ontologist capacity. It took no part in drafting the records reviewed |
| Date | 2026-11-14 |
| Scope | The seven records left PENDING REVIEW by the architect's decision, part 4: T2-02, T2-04, T2-17, T2-24, T2-25, T2-31 and T2-43, in `docs/catalog/admission/G1T-T2-batch.md`, revision 3, as on disk. No other candidate is reviewed |
| Governing decision | `docs/decisions/2026-11-14-g1t-tranche-2-batch-decided.md`: part 4 (the corrections), part 2 (the Formulation reading of question 4), part 5 (the strict summary-act rule) |
| Test applied | G1-T, specification v0.5.0-draft.3 §8, with CD2, CD4, CD5, CD7, CAP-04, CAP-06 and CAP-07; tranche-1 precedent `G1T-T1-02-payroll-processing.md` and `G1T-T1-03-accounts-payable-processing.md` |
| Evidence read | Each record's definition, grounding, index, exclusions, taxonomy and answers; the PCF 7.4 name and description of every index member and every exclusion relied on (`docs/sources/inventory/pcf-7.4-entries.yaml`); the BPO genus and outputs of every member (`docs/catalog/bpo-act-types.yaml`); the vocabulary entries in `src/01_controlled_vocabulary/catalog.yaml`; the independent review of 2026-11-07 |
| Standing of this review | Analytical evidence for the named signing reviewer (decision, part 6). It is not a signature, records no finding in any record's signature table, and admits nothing |

## 2. Findings

| Id | Concept | Finding | Reason |
|---|---|---|---|
| T2-02 | Corporate Card Management | PASS | Correction applied; every clause has a non-deontic member; `P20931` handles applications and does not decide them |
| T2-04 | Capital Investment Appraisal | PASS | Correction applied; `P10847` prepares and evaluates the financial justification; the `part-of` link to Capital Planning holds and is not equivalence |
| T2-17 | Control Environment and Risk Objective Formulation | PASS | Correction applied; the three Formulation acts are non-deontic on the Formulation reading, which extends to them on its own terms |
| T2-24 | Cost Driver and Critical Activity Analysis | PASS | Correction applied; the definition is exactly the three analysis acts; no ability to plan, control or reduce spending is claimed |
| T2-25 | Financial Performance Analysis | PENDING REVIEW | "Projects" and "against its targets" rest only on the excluded summary act `P10741`; `P10786` and `P10787` need their keep-reasons corrected |
| T2-31 | Customer Credit Management | PASS | Correction applied; `P14187` (output a credit assessment) evaluates whether credit should be extended without deciding it; no clause grants, alters or withdraws standing |
| T2-43 | Internal Control Effectiveness Monitoring | PASS | Correction applied; `P10918` monitors control effectiveness; no claim to operate controls remains |

## 3. Per class

### T2-02 — Corporate Card Management

**Correction applied as specified: yes.** "Set their terms" is gone from the definition, the
grounding and the answers; `P20929` is excluded (SUMMARY, its parts including `P20934` and
`P20935`). The definition matches the vocabulary entry, which keeps the same IRI and records
`revises` with the revision-2 digest.

1. Bearer: yes. Cards are on the organization's account with its issuer and settled from its accounts.
2. Basis: yes. Card administrators and payables members; issuer platform and expense system are enabling. F1's manual alternative holds.
3. Arrangements: yes, through the issuer relationship and the organization's accounts (b1).
4. Non-deontic: yes. `P20931`'s PCF description is "Handling ... credit card applications for business expenses": handling, not deciding; no approval appears in it. `P20932` obtains cards from the issuer; `P20933` handles the card accounts. Every grant, change or withdrawal of spending standing (`P20930`, `P20934`, `P20935`, and the summary `P20929`, described as "handling and authoring credit cards") is out. The definition's "processing requests for cards" claims no standing.
5. Exercise: yes. `P20932` (Act of Acquisition) carries an adequate CAP-06 reason.

Defects: none blocking. Two notes for the signer:
- "Reconciling ... and settling them" rests on `P20933` alone (Act of Accounting, output an account statement), read as account handling. The architect's part 4 accepts that reading; no separate settlement act exists at the pin.
- `P20932`'s CAP-06 reason says ordering is "how the capability provides one to a member". "Obtains the card from the issuer" would avoid echoing revision 2's "provide", which sat near conferring standing. Editorial only.

### T2-04 — Capital Investment Appraisal (formerly Capital Planning)

**Correction applied as specified: yes.** Renamed; definition narrowed to "prepare and evaluate
the financial justification for its proposed capital investments"; `P10847` is the single
index member; no act type is invented; `bcoc:CapitalPlanning` is kept unchanged as a grouping,
and the new concept has its own IRI, `broader` Capital Planning.

1. Bearer: yes. The proposals are the organization's own.
2. Basis: yes. Finance and planning members; models and cost data enabling; spreadsheet appraisal feasible.
3. Arrangements: yes. The justification is prepared for the organization's own decision.
4. Non-deontic: yes. `P10847`'s description ("validate any project's business case", weighing benefits against costs) is appraisal; its output is a financial justification. The approval it serves is a separate act, and `P10751`, `P10845` and `P10846`, which join planning with approval, are out.
5. Exercise: yes. `P10844` (developing capital investment policies) is rightly Q5.

Narrowed type: the `part-of` link to Capital Planning passes the coverage test, since Capital
Planning's definition names preparing "the financial case on which a decision to proceed is
made". It is not equivalent: Capital Planning also identifies investments and budgets for
them, which this type does not claim.

Defects: none. Note: `P10751` (PCF 9.4.1) is also a summary act over four children; coding it
Q4 rather than SUMMARY is defensible, since both apply, but SUMMARY would match T2-17, T2-24
and T2-43.

### T2-17 — Control Environment and Risk Objective Formulation (formerly Internal Control Design)

**Correction applied as specified: yes.** Renamed; definition narrowed to the code of ethics
(`P10915`), process objectives and risks (`P11250`) and entity/unit risk tolerances
(`P11251`); `P10762` excluded (SUMMARY); the taxonomy says the type does not establish the
whole of internal control design.

1. Bearer: yes. The code, objectives and tolerances are the organization's.
2. Basis: yes. Control, risk and finance members; framework documents enabling.
3. Arrangements: yes.
4. Non-deontic: yes, on the Formulation reading. All three members are BPO Acts of Formulation, with outputs a code of ethics, process control objectives with a risk assessment, and a risk tolerance specification. The reading the architect approved for T2-07 and T2-42 rests on a ground that holds here unchanged: formulating, drafting and communicating a directive content is describable without standing, and adopting it with authority is a separate act outside the index (F3's authority-withdrawn case). A code of ethics is a policy in all but name. A risk tolerance (PCF: "the specific maximum risk to take in quantitative terms") states what the organization is prepared to bear, not who may approve what, so it is not an approval limit like the excluded `P20930` or `P10880`; neither description of `P11250` or `P11251` contains an approval. `P10916` (assigning roles and responsibility) and `P10914` (establishing a board) are rightly out. The definition uses no CAP-07 stem.
5. Exercise: yes. The formulations are this capability's own product, not the setting of its own practice; `P10914` is rightly out as organizational establishment.

Narrowed type: the `part-of` link to Internal Control Design passes coverage. All three acts
sit under PCF 9.8.1, and Internal Control Design's definition names defining the policies
meant to give reasonable assurance. It is not equivalent, because no member defines a control.

Defects: none. Notes: the signer should record that the Formulation reading is applied here by
extension, as the decision approved it by name only for T2-07 and T2-42. The label's "Risk
Objective" abbreviates "process objectives and risks"; the definition is the authority.

### T2-24 — Cost Driver and Critical Activity Analysis (formerly Cost Management)

**Correction applied as specified: yes.** Renamed; definition limited to identifying and
measuring cost drivers and identifying critical activities; `P10740` excluded (SUMMARY);
Cost Management kept as a grouping; the taxonomy states that no ability to plan, control or
reduce spending is inferred.

1. Bearer: yes.
2. Basis: yes. Finance and operations members; cost models and activity data enabling.
3. Arrangements: yes.
4. Non-deontic: yes. Identification (`P10778`, `P10780`) and measuring (`P10779`) carry no standing.
5. Exercise: yes. No development genus; `P10781` is rightly OTHER.

Narrowed type: the `part-of` link to Cost Management passes coverage. PCF 9.1.3.3 says
determining critical activities shows "where costs cannot be slashed", which is part of
deciding which costs to avoid, the grouping's definition. It is not equivalent: no member
plans, controls or decides spending.

Defects: none. Note: the link's reason ("the analysis on which managing costs draws") reads
as an input relation; "part of deciding which costs to avoid or reduce" states the coverage
directly. `P10780`'s PCF description limits critical activities to the finance function,
which the definition's "its critical activities" does not; the name governs, as elsewhere.

### T2-25 — Financial Performance Analysis (formerly Financial Performance Management)

**Correction applied as specified: partly.** Renamed; "and act on the results" deleted;
`P10785` excluded under Q5 (CD5); `P10741` excluded (SUMMARY). The architect also directed a
review of the remaining acts against the narrower definition, keeping only those that
genuinely concern financial appraisal, analysis or monitoring. The record's review of them
leaves two gaps, and the definition still claims more than the index holds.

1. Bearer: yes.
2. Basis: yes. Financial-analysis members; reporting tools enabling.
3. Arrangements: yes.
4. Non-deontic: yes. No member grants, alters or withdraws standing.
5. Exercise: met only once the keep-reasons below are corrected.

Members against the definition:
- `P10782` (customer and product profitability, output a profitability analysis), `P10783` (new-product evaluation, under 9.1.4, as the earlier review accepted) and `P10784` (life-cycle costing): financial appraisal of products and customers. Keep.
- `P10786` (track performance of new-customer and product strategies): its PCF description adds "Prepare strategies to improve sales and profits", which is the acting on results the architect removed and the same CD5 ground on which `P10785` was excluded. The record keeps it without addressing this.
- `P10787` (prepare activity-based performance measures): the record keeps it as "constructing the measures performance is assessed by". On that reading it sets the criteria for this capability's own practice, the ground on which T2-31 excludes `P14188` under Q5. Its PCF description supports a different reading, under which it should stay: "Evaluating performance based on different sets of activities created by management to measure performance". The activities are created by management; this act evaluates performance by them.

Definition against the index: no member assesses projects. "Projects", and "against its
targets" ("checking and achieving predetermined financial targets"), come only from the
excluded summary act `P10741`. "Of the organization and of its units" has at most indirect
support, through `P10787`. This is the pattern for which the earlier review held T2-17, T2-24
and T2-43: a definition clause resting only on a summary act.

Narrowed type: the `part-of` link to Financial Performance Management passes coverage, and the
type is not equivalent to it, once the definition is bounded as below.

**Corrections required:**
1. Definition: "A business capability of an organization to assess the profitability and financial performance of its products, customers and activities, including the evaluation of new products, life-cycle costing and tracking the performance of its customer and product strategies, grounded in the organization's members as organized." Or keep the present wording without "and projects" and without "against its targets". The vocabulary entry changes to match.
2. `P10787`: replace the keep-reason with the description-based one ("evaluates performance by activity-based measures management has set; it does not set them"). If the signer reads the act as setting the measures, exclude it under Q5, consistent with `P14188`.
3. `P10786`: record a CD5 justification (the act is identified by its name, tracking; the strategy preparation in its description is not taken into the definition, and the index makes no exhaustiveness claim, CD4), or exclude it under Q5 as `P10785` was. Either is admissible. Silence is not.

With these applied, PASS.

### T2-31 — Customer Credit Management

**Correction applied as specified: yes.** The definition is reworded to evaluation, analysis,
account review and monitoring; `P10742` excluded (SUMMARY); `P14188` moved out under Q5; no
clause grants, changes or withdraws credit standing. It matches the vocabulary entry, same
IRI, `revises` recorded.

1. Bearer: yes. The customers and receivables are the organization's.
2. Basis: yes. Credit members; scoring tools and ledger enabling.
3. Arrangements: yes.
4. Non-deontic: yes. Does a member evaluate credit requests? Yes: `P14187`'s output is a credit assessment, and its PCF description is reviewing past credit scores "to determine the if a line of credit will be extended" to potential customers, or more to existing accounts. The decision to extend is `P10790` ("Checking and accepting new requests"), excluded as Q4, so the first clause does not outrun the index, provided "evaluate" is read as assessing a request and not disposing of it. `P10793` (reinstate or suspend) is rightly out.
5. Exercise: yes. `P10789` and `P14188` (forecasting credit-score requirements, PCF: "based on established credit policies") set the criteria for this capability's own practice and are rightly Q5.

Clause-to-member mapping: evaluate requests and analyze the credit evidence, `P14187`; review
their accounts, `P10791`; monitor their credit activity, `P10791` (PCF: "regularly review
existing accounts") and `P10792` (credit and collection reports).

Defects: none blocking. Notes:
- `P10792`'s PCF description speaks of "account payable reports about payments to be made", which does not match its name. The name and its place under 9.2.1 govern, as the earlier review held for T2-05; the record should say so.
- The definition says nothing of reporting. Reading `P10792` as monitoring through reports is adequate. Adding "and report on them" would make the mapping explicit, but is not required.
- The vocabulary entry's definitional source still cites only the summary element 9.2.1 (`P10742`). That is the provenance the decision preserves, but the five narrowed concepts cite their index members, and so could this one. The same applies to T2-02 (`P20929`).

### T2-43 — Internal Control Effectiveness Monitoring (formerly Internal Control Operation and Monitoring)

**Correction applied as specified: yes.** Renamed; definition limited to monitoring whether
controls operate as intended and satisfy their assessment criteria; `P21574` excluded
(SUMMARY); the taxonomy says the type does not establish the ability to operate every control.

1. Bearer: yes.
2. Basis: yes. Control owners and compliance members; testing tools enabling; manual testing feasible.
3. Arrangements: yes.
4. Non-deontic: yes. `P10918` (Act of Monitoring, output a control effectiveness assessment; PCF: observe "the effectiveness of policies, procedures, techniques, and mechanisms") claims no standing. Operating controls, which includes approvals, is no longer claimed.
5. Exercise: yes. `P10919` (remediate deficiencies) is rightly out.

Narrowed type: the `part-of` link to `bcoc:InternalControlOperation` (label "Internal Control
Operation and Monitoring") passes coverage, since that concept's definition names monitoring
whether controls operate as designed. It is not equivalent: it also carries out the controls.

Defects: none. Note: `P10919`'s exclusion reason still ends "not its operation". Since the type
is now monitoring, "not monitoring" fits, and OTHER (remediating changes the controls, another
capability's object) would describe it more exactly than Q5.

## 4. Defects to escalate

1. **T2-25, Financial Performance Analysis.** The corrected definition still claims what no
   member supports: "projects" and "against its targets" rest only on the excluded summary act
   `P10741`. The record's keep-reason for `P10787` would, by the `P14188` precedent, exclude it.
   `P10786`'s description includes preparing strategies to improve sales and profits, the CD5
   ground on which `P10785` was excluded, and the record does not address it. These follow
   from the decision's own instruction to review the remaining acts against the narrower
   definition, and from Batch B's rule that unsupported clauses be removed. They are not a
   conflict with the decision. Required corrections are in section 3. T2-25 stays PENDING
   REVIEW until they are applied.

No conflict with the architect's decision was found in the other six. The extension of the
Formulation reading to T2-17 is in line with the decision's grounds, but the decision names
only T2-07 and T2-42, so the signer should confirm it when signing.
