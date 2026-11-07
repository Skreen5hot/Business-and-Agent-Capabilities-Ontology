# Semantic-curation tranche 2 — implementation proposal, for decision 3

| Field | Value |
|---|---|
| Status | **Proposed.** For the architect. It decides nothing. Semantic curation is the architect's decision 3 (`docs/decisions/2026-11-07-cp0-closeout-and-integration-authorized.md`, B), requested in `docs/decisions/2026-11-07-adr002-accepted-cp0-complete.md`, D |
| Date | 2026-11-07 |
| Prepared by | Claude Code (`claude-opus-5-5`), for the BCO team |
| Read from | `docs/catalog/candidates.yaml` after the I-4 stabilization; `docs/catalog/tranche-1.md`; `src/01_controlled_vocabulary/catalog.yaml`; `config/vocab-schema.yaml`; roadmap T5, T7, T8, D5 and D6 |

## 1. Proposal in brief

Curate one PCF category end to end: **Financial Resources Management (PCF 9.0,
`BCC-4fda51aa`) and the 72 candidates beneath it.** Curation turns each candidate into a
reviewed outcome:
- a normalized Draft concept in the controlled vocabulary;
- a recorded merge, retirement or rejection;
- or a deferral, with its reason.

The subtree's links become a reviewed taxonomy, and the candidates proposed as classes go
to G1-T with drafted evidence. The tooling is what exists; one small vocabulary-schema
change, and a Stage 03 standard, need approval (§6).

## 2. Why this category

| Measure (generated catalog) | Value |
|---|---|
| Candidates beneath `BCC-4fda51aa` | 72: 71 `capability`, 1 `process` |
| Review status | 32 generated-draft, 36 needs-review, 2 deferred, 2 rejected |
| With BPO act types in their realization evidence | 68 |
| Supported by two or more sources | 24 |
| Proposed broader links within it | 88 |
| Overlap links within it | 26 |
| Direct subareas | 11, from Treasury Operations Management (17 beneath it) to Internal Control (2) |

- **Continuity.** It already holds two of the three admitted tranche-1 classes:
  - Payroll Processing, T1-02, `BCC-d95f68fd`;
  - Accounts Payable Processing, T1-03, `BCC-62e789bf`.

  It also holds the reviewed components of those two classes. The pilot concept
  `bcoc:TreasuryManagement` is already in the vocabulary.
- **Evidence.** Nearly every candidate has act types, so a realization index can be drawn
  from evidence for each one rather than written from scratch.
- **Size.** It is large enough to measure, and coherent enough for one reviewer to judge.

## 3. Expected outputs, and how the milestone is measured

| Output | Where | Measure |
|---|---|---|
| A disposition for every candidate in scope: accepted, merged into another, retired, rejected, or deferred with a reason | `docs/catalog/dispositions.yaml` (with its pin), cited from the tranche record | candidates dispositioned, of 72 |
| **Normalized concepts**: preferred label, original genus-differentia definition, `broader`, PCF notation, sources, Draft status | `src/01_controlled_vocabulary/catalog.yaml`, built by `tools/vocab/build.py` into SKOS | concepts written; target is every accepted candidate |
| **Reviewed definitions**: every flag on the candidate is cleared or answered; checked against CD7 and CD8; the originality tripwire passes | the tranche record, one row per concept | definitions passed by the reviewer |
| **Validated taxonomy**: every proposed broader link confirmed, re-targeted or rejected, and each kept one typed as specialization or as component | the concepts' `broader`, and the tranche record | links validated, of 88 |
| **Readiness for formalization**: for each class proposed for admission, its realization index and drafted G1-T evidence | `docs/catalog/tranche-2.md`, then `docs/catalog/admission/` | G1-T records drafted; PASS signed |

The flags give the review its first worklist:
- 21 act types typed under a capability class (Q-12);
- 4 deontic index members;
- 4 qualified objects;
- 4 generic objects;
- 2 with no act type;
- 2 with a development genus;
- 1 circular.

## 4. Review process

The roles are the ones the repository already uses:
- the BCO team drafts, as Ontologist;
- the architect reviews as Proxy Domain Expert, for the domain;
- an independent AI-authored review is filed verbatim, as for tranche 1.

The work goes in three batches, one pull request each, in this order:
1. Treasury and international funds;
2. the accounting areas;
3. payables, payroll, tax, trade and internal control.

Each batch passes two reviews.

1. **Terminology.**
   - The preferred label is chosen from the merged source labels, and the rest are kept as
     alternative labels.
   - Each definition is written from the frame and the evidence, never from source text.
   - Merges are made where the overlap list or the reviewer finds one ability under two
     names.
2. **Taxonomy.** Each broader link is judged as one of three kinds:
   - **specialization**: the narrower is a kind of the broader. Only this kind can later
     support `rdfs:subClassOf` (CD9), after the formalization review.
   - **component**: a part of the broader's work, as the PCF hierarchy mostly is. It is
     kept as a SKOS `broader` with its kind recorded, and never becomes a subclass axiom.
     Where CD16 applies, it goes to the functional-coverage register.
   - **wrong**: removed, with the reason.

**No generated broader link is asserted as a subclass relation**, and no candidate becomes
an OWL class automatically.

## 5. Flow to G1-T and formalization

1. Each candidate's disposition is recorded and pinned.
2. An accepted candidate becomes a Draft concept, and its reviewed taxonomy links are
   recorded.
3. Each concept proposed as a class gets drafted G1-T evidence: bearer, grounding,
   realization index, the five questions. The named reviewer signs PASS or FAIL.
4. Formalization starts only after D5: the Stage 05 standard, the validation
   architecture, and BPO's Q-12 to Q-14. Then each passed concept becomes a class in
   `src/05_ontology/apqc-cap.ttl`, linked by `designates_class`. That is decision 4,
   gated by D6.

## 6. Tooling, and what needs approval

**Reused unchanged:**
- `synthesize.py`, with its dispositions and pins;
- `tools/vocab/build.py`, the vocabulary shapes and the validation gate;
- the tranche and admission record forms;
- `tools/conceptual/check_models.py`.

No generator change is proposed.

**Needs approval:**
1. **Two vocabulary-schema slots**, under ADR-003's revision rules and checked by
   `schema_check.py`:
   - `alt_label`, emitted as `skos:altLabel`;
   - `candidate`, the `BCC-` identifier the concept came from.

   Without them, the merged labels and the trace back to the catalog have nowhere to go.
2. **A Stage 03 standard.** Roadmap T8 makes one the condition for a reviewed taxonomy
   baseline. A short standard covering link kinds, evidence and review would be drafted
   for approval with batch 1.
3. **The reviewer named** for the terminology, taxonomy and G1-T reviews of the tranche.

## 7. Not in this proposal

- No OWL, subclass axiom, object property or Stage 05 work.
- No change to the generator.
- No further harvesting, and no I-3.
- Nothing outside the PCF 9.0 subtree.

A reviewer may still find that a candidate's best broader lies outside the subtree; that
link is recorded but not curated here.
