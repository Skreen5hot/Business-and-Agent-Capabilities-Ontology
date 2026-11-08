# Decision record — semantic-curation tranche 2 approved, 2026-11-07

Recorded verbatim by Claude Code (`claude-opus-5-5`) on 2026-11-07, from the decision the
architect, Aaron Damiano, gave in session. The act is the architect's.

## What it is about

| Field | Value |
| --- | --- |
| Approves | `docs/proposals/2026-11-07-curation-tranche-2-proposal.md` at `80d4966`, SHA-256 `7523df25e3f9d5623235691794123cb048bbcb8ed1547347740d97df0fa5df16`, on PR #48 |
| Decides | The architect's decision 3 (`docs/decisions/2026-11-07-cp0-closeout-and-integration-authorized.md`, B), for PCF 9.0's subtree |

## The decision

````text
Subject: Architect Decision — PR #48 Semantic Curation Tranche 2
Decision: APPROVED WITH IMPLEMENTATION CLARIFICATIONS.
I approve proceeding with semantic curation of the 72 candidates in Financial Resources Management (PCF 9.0), as proposed in PR #48.
This authorization covers the full three-batch tranche. It is not limited to another pilot exercise.
A. Work Authorized Now
1. Semantic normalization
Review all 72 candidates and record a supported disposition for each: accepted, merged, retired, rejected or deferred.
For accepted concepts, produce preferred labels, appropriate alternative labels, original genus–differentia definitions, source traceability and preliminary conceptual classification.
Do not simply copy APQC labels or mechanically transform process names into capabilities.
2. Vocabulary-schema changes
Approve an `alt_label` field using the existing `skos:altLabel` property.
Approve a candidate-provenance field, but make it capable of recording multiple BCC identifiers where several generated candidates are merged into one concept.
Preserve the full source crosswalk. These fields do not authorize new ontology object properties or OWL classes.
3. Stage 03 standard
Prepare a concise Stage 03 taxonomy standard covering relationship types, evidence, review criteria and traceability.
Submit it for approval before declaring any taxonomy relationships validated.
Semantic terminology work may proceed while the standard is prepared.
4. Taxonomy development
Review the proposed broader relationships individually in the curation workflow.
Distinguish:

* Genuine ontological specialization.
* Functional component or coverage relationships.
* Incorrect relationships requiring rejection.

Do not translate APQC hierarchy or generic SKOS broader relationships directly into OWL subclass axioms.
Preserve the relationship classifications in structured review records.
5. Review process
Use the project's approved synthetic domain-review approach. Record reviewer identity and capacity.
The development team may perform routine terminology normalization and preliminary taxonomy analysis without seeking individual approval for every candidate.
Consolidate material ontological disagreements and G1-T admission decisions for architectural review.
Do not require another independent review cycle for each batch unless it identifies a substantive problem.
B. Deliverables
Complete the three proposed batches:

1. Treasury and international funds.
2. Accounting areas.
3. Payables, payroll, tax, trade and internal control.

For the full tranche, report:

* Candidates dispositioned out of 72.
* Distinct normalized concepts produced.
* Definitions reviewed and accepted.
* Proposed taxonomy links validated, reclassified or rejected.
* Candidates ready for G1-T admission.
* Outstanding substantive issues and source limitations.

Preserve existing reviewed concepts, identifiers and G1-T admission records.
C. Decisions Reserved
This approval does not authorize automatic G1-T admission, Stage 05 implementation or generation of OWL classes.
The Stage 03 standard still requires my approval before its validation gate is considered complete.
Formalization requires the previously established Stage 05 authorization and adherence to existing BFO/CCO classes and relations.
D. Development Priority
Do not expand the candidate generator or build additional general-purpose infrastructure.
Use the existing tooling and produce the normalized concepts and reviewed taxonomy.
After completing this tranche, provide a recommendation for scaling the same approach across the remaining candidate catalog. We should not repeat the entire governance process for each subsequent domain.
Proceed with Tranche 2 semantic curation under these conditions. The immediate deliverable is actual normalized ontology terminology and defensible taxonomy—not another implementation proposal.
````

## The acts it contains

1. **Tranche 2 is approved in full**: all 72 candidates beneath PCF 9.0, in three batches,
   each with a supported disposition (accepted, merged, retired, rejected or deferred). An
   accepted concept gets a preferred label, alternative labels, an original
   genus-differentia definition, source traceability and a preliminary classification.
   APQC labels are not copied, and process names are not turned into capabilities
   mechanically.
2. **Two vocabulary-schema fields are approved:**
   - `alt_label`, as `skos:altLabel`;
   - a candidate-provenance field that can hold several `BCC-` identifiers.

   The crosswalk is kept whole. Neither field authorizes an object property or an OWL
   class.
3. **A Stage 03 standard is to be prepared** and submitted. No taxonomy relationship is
   declared validated before it is approved, but terminology work may proceed meanwhile.
4. **Each proposed broader link is reviewed** as specialization, component or coverage, or
   incorrect, and the classification is kept in structured review records. Neither the APQC
   hierarchy nor a SKOS `broader` becomes an OWL subclass axiom.
5. **Review:**
   - It uses the approved synthetic domain review, with the reviewer's identity and
     capacity recorded.
   - Routine normalization and preliminary taxonomy need no approval per candidate.
   - Material disagreements and G1-T admissions are consolidated for the architect.
   - There is no independent review per batch unless a substantive problem appears.
6. **Deliverables:** the three batches, and for the tranche: candidates dispositioned of
   72, distinct concepts, definitions reviewed and accepted, links validated, reclassified
   or rejected, candidates ready for G1-T, and outstanding issues and source limitations.
   Reviewed concepts, identifiers and G1-T records are preserved.
7. **Reserved:** G1-T admission, Stage 05 and OWL classes. The Stage 03 standard's
   approval also remains the architect's.
8. **Priority:** no generator expansion and no general-purpose infrastructure. After the
   tranche, a recommendation for scaling the approach across the catalog, without
   repeating the whole governance process for each domain.

## How it was carried out

- **Schema (act 2).** `alt_label` and `catalog_candidates` were added to
  `config/vocab-schema.yaml`, with `config/vocab-schema.json` regenerated by
  `tools/vocab/schema_check.py`. `tools/vocab/build.py` checks them and emits
  `skos:altLabel` and `bco:catalogCandidate`, a literal annotation property, with tests.
- **Standard (act 3).** It is in `docs/proposals/2026-11-07-stage-03-taxonomy-standard.md`,
  proposed. Every link is reported as *classified*.
- **Curation (acts 1, 4, 6).** The results are in four places:
  - `docs/catalog/tranche-2-review.yaml`, the structured record;
  - `docs/catalog/tranche-2.md`, the report with the figures;
  - `src/01_controlled_vocabulary/catalog.yaml`, the concepts;
  - `docs/catalog/dispositions.yaml`, the merges, the rejection and the pins, from which
    the catalog was regenerated.
- **Review (act 5).** One synthetic domain review of the whole tranche gave 30 findings, 19
  of them substantive, all applied. One candidate the generator had left outside the walk
  (PCF 9.8.2) was added on its finding. The report consolidates the material issues.

## What it does not do

It admits no class, writes no OWL, asserts no subclass axiom, and changes no generator.
