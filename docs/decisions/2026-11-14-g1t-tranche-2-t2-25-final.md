# Decision record — G1-T tranche 2: T2-25 final direction, 2026-11-14

Recorded verbatim by Claude Code (`claude-opus-5-5`) on 2026-11-14, from the direction the
architect, Aaron Damiano, gave in session. The act is the architect's. It signs nothing.

## What it is about

T2-25, Financial Performance Analysis (candidate BCC-cedf0899, concept
`bcoc:FinancialPerformanceAnalysis`), in revision 4 of the batch record, PR #50 as pushed at
`060e7b9`:

| Record | SHA-256 at `060e7b9` |
| --- | --- |
| `docs/catalog/admission/G1T-T2-batch.md` (revision 4) | `64f6758032d62bc0d2ed8ecee85fe5dc3f8fe23df71b59ddb46a228eed2cf1fe` |
| `docs/catalog/admission/G1T-T2-signature.md` (prepared for 39) | `8cd6f00b3b2d2cebfe762a5fbd8eb7eb20f042782867751928b7816052904c44` |
| `bcoc:FinancialPerformanceAnalysis`, concept record (`tools/vocab/build.py --digest`) | `bb3270ca30bb0f4a438cd070be8de9e6f4c88ea47f92c6a9fc0cecfbb052296a` |

It follows `docs/decisions/2026-11-14-g1t-tranche-2-t2-25-and-the-six.md`.

## The direction

````text
Subject: PR #50 — Final Architectural Direction on T2-25 Only
Decision: ACCEPT THE NARROWED T2-25 CONCEPT WITH TWO FINAL CORRECTIONS.
I have reviewed Financial Performance Analysis, T2-25, revision 4.
1. Definition
Retain the preferred label Financial Performance Analysis and its existing concept IRI, `bcoc:FinancialPerformanceAnalysis`.
Use this definition:
"A business capability that inheres in an organization and is realizable through its organized members' appraisal and analysis of the financial performance and profitability of its products, customers, or activities."
Do not enumerate specific BPO acts in the definition. Preserve those distinctions in the realization index.
2. Realization index
Retain:

* `bpo:P10782`
* `bpo:P10783`
* `bpo:P10784`
* `bpo:P10787`

Exclude `bpo:P10786` under Q5/CD5 because its source description also includes developing strategies to improve sales and profits. We should not use its monitoring label to disregard that broader source meaning.
Keep `bpo:P10785` and summary act `bpo:P10741` excluded as previously decided.
The final index therefore contains four act types.
3. Change control
Preserve the prior T2-25 definition, realization-index history and source provenance. Record the revised definition and exclusion rationale against the existing candidate and concept identifiers.
This is a correction to an unsigned, not-yet-formalized capability type. It does not require another ontology IRI or alter the retained Financial Performance Management functional grouping.
4. G1-T disposition
Once these exact corrections have been verified, add T2-25 to the consolidated G1-T signature record as eligible for admission.
No further general synthetic review is required. The named signing reviewer retains responsibility for the final G1-T finding and signature.
Do not mark T2-25 admitted before that signature. No OWL implementation is authorized.
This direction concerns T2-25 only. Do not reopen the other 39 candidates or introduce unrelated changes to PR #50.
````

## Acts it contains

1. **Definition.** The concept keeps its label and IRI; its definition becomes the one given
   above, verbatim, recorded as a revision of the revision-4 record.
2. **Realization index.** Four members: `P10782`, `P10783`, `P10784`, `P10787`. `P10786` is
   excluded under Q5 (CD5); `P10785` and `P10741` stay excluded.
3. **Change control.** The prior definitions, index history and sources are kept in the
   batch record and the concept's change notes; the candidate and concept identifiers do not
   change, and Financial Performance Management stays as it is.
4. **G1-T disposition.** Once the corrections are verified, T2-25 enters
   `docs/catalog/admission/G1T-T2-signature.md` as eligible for admission on signature.

## What it does not do

- It signs nothing and admits nothing; the G1-T finding and the signature are the named
  reviewer's.
- It starts no further review, and reopens none of the other 39.
- It writes no OWL.
