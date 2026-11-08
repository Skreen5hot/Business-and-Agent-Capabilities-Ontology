# Decision record — tranche 2 accepted as the working baseline, G1-T preparation authorized, 2026-11-07

Recorded verbatim by Claude Code (`claude-opus-5-5`) on 2026-11-07, from the direction the
architect, Aaron Damiano, gave in session. The act is the architect's.

## What it is about

| Field | Value |
| --- | --- |
| Accepts | Semantic-curation tranche 2 at `a115b14ac108f8b9fe376cf294e9985815033b90` (`docs/decisions/2026-11-07-curation-tranche-2-approved.md`): `docs/catalog/tranche-2.md`, SHA-256 `7129502abd9b13c72411c7ca2fed99a9c15388cd206fdc0dbaefdebd39f9b317`; `docs/catalog/tranche-2-review.yaml`, SHA-256 `3334397feddfe9862cbabe740f99df8900b8a1e231a2d9e20fc151df3e7487e8` |
| Rules for | `docs/proposals/2026-11-07-stage-03-taxonomy-standard.md` at `a115b14`, SHA-256 `6882e4659cc3e95c44daa50bb5601f199056f02424df8e208a422588b888a3ed`, to be aligned and resubmitted |

## The decision

The text below is as received. It ends mid-word in section C ("Routine terminolo"); the
rest of section C was not received, and nothing in this record supplies it.

````text
Subject: Architectural Direction — Accept Tranche 2 and Advance Semantic Curation
I have reviewed the Tranche 2 completion report.
Decision: ACCEPT THE TRANCHE 2 CURATION RESULTS AS THE WORKING TERMINOLOGY BASELINE, SUBJECT TO FINAL ARTIFACT VERIFICATION.
The work represents meaningful progress toward the Business Capability Ontology. Do not initiate another general review of the 72 candidates.
A. Authorized Now
1. Publish Tranche 2 for repository review
Push commit `a115b14` and open a PR containing the curated vocabulary, link classifications, review dispositions, tests, and tranche report.
Preserve the historical records and signed G1-T admissions.
Do not merge unapproved Stage 03 normative content merely because the PR passes CI.
2. Finalize the Stage 03 standard
I approve the following architectural rules for Stage 03:

* `kind-of` identifies proposed genuine conceptual specialization.
* `part-of` identifies a reviewed partitive or functional-component relationship. It does not automatically assert BFO continuant parthood or OWL subclass relationships between dispositions.
* `incorrect` is a review disposition, not a semantic relationship.
* SKOS broader relationships must remain distinguishable from proposed OWL subclass relationships.
* Every retained relationship requires provenance and a recorded justification.
* Unresolved relationships remain unresolved rather than being forced into the taxonomy.

Align the proposed Stage 03 standard with these rules and submit its exact text for final ratification. No additional framework or ontology properties are authorized.
3. Prepare the 43 reported G1-T-ready candidates for batch review
I authorize preparation and evidence checking for the 43 candidates.
For each candidate, provide its normalized definition, proposed BFO/CCO classification, grounding rationale, realization-index evidence, relevant taxonomy review, and G1-T pass/fail reasoning.
Use existing BPO act classes and the approved admission criteria. Do not invent act types to compensate for missing mappings.
This authorizes G1-T preparation, not automatic admission or OWL generation.
4. Resolve the minor reporting discrepancies
Reconcile the concept-status and taxonomy-link counts using generated records. Identify which normalized concepts are already admitted, ready, not ready, or outside the G1-T review scope.
Preserve the Treasury Management definition pending its recorded revision.
B. Matters Deferred
Q-12 — BPO act-type defects
Keep the affected concepts blocked where no valid realization-index evidence exists.
Prepare a consolidated list of the 13 affected concepts and their exact BPO dependencies. We will decide separately whether an upstream correction or an existing valid act-type mapping is appropriate.
Held root links
Keep Internal Control and Global Trade Management unresolved until the relevant cross-domain concepts are available.
Do not change a concept's intended meaning to fit the PCF 9.0 hierarchy.
Cross-domain duplicates and homonyms
Retain them in the curation queue with source traceability. Resolve them during the relevant domain's review, not through unsupported automatic merges.
C. Scaling Direction
I support adopting a standing semantic-curation method for subsequent domains once the Stage 03 standard is approved.
The objective is to avoid requiring a new architectural proposal for every domain.
Use one consolidated synthetic domain review per tranche under our established project governance. Routine terminolo
````

## The acts it contains

1. **Tranche 2 is accepted** as the working terminology baseline, subject to final artifact
   verification. There is to be no further general review of the 72 candidates.
2. **Publication (A1).** `a115b14` is pushed for repository review in a pull request, with
   the historical records and signed G1-T admissions preserved. Passing CI does not license
   merging unapproved Stage 03 normative content.
3. **Six Stage 03 rules are approved (A2):**
   - `kind-of` is proposed conceptual specialization;
   - `part-of` is a reviewed partitive or functional-component relationship, asserting
     neither BFO continuant parthood nor an OWL subclass relation between dispositions;
   - `incorrect` is a review disposition, not a relationship;
   - SKOS `broader` stays distinguishable from proposed OWL subclass relations;
   - every retained relationship has provenance and a recorded justification;
   - unresolved relationships stay unresolved.

   The proposed standard is to be aligned with them and its exact text submitted for final
   ratification. No further framework and no ontology properties are authorized.
4. **G1-T preparation for the 43 ready candidates (A3).** For each one: its definition,
   proposed BFO/CCO classification, grounding rationale, realization-index evidence,
   taxonomy review, and PASS or FAIL reasoning. Only existing BPO act classes and the
   approved admission criteria are used, and no act type is invented. It authorizes
   preparation, not admission or OWL.
5. **Reconciliation (A4).** The concept-status and link counts are reconciled from the
   generated records, and each normalized concept is placed as admitted, ready, not ready
   or outside G1-T scope. The Treasury Management definition is preserved until its
   recorded revision.
6. **Deferred (B):**
   - **Q-12.** The affected concepts stay blocked where no valid realization-index
     evidence exists. A consolidated list of the 13 and their exact BPO dependencies is
     prepared; whether to seek an upstream correction or an existing valid mapping is to
     be decided separately.
   - **Held root links.** Internal Control and Global Trade Management stay unresolved
     until the cross-domain concepts exist, and no concept's meaning is changed to fit PCF
     9.0.
   - **Duplicates and homonyms.** They stay in the curation queue with source traceability,
     to be resolved in their domains' reviews, not by automatic merges.
7. **Scaling (C, as received).** A standing semantic-curation method is supported for later
   domains once the Stage 03 standard is approved, without a new proposal per domain, and
   with one consolidated synthetic domain review per tranche. The rest of section C was not
   received.

## What it does not do

It ratifies no standard, admits no class, writes no OWL and asserts no subclass axiom.
