# Ontology Development Standard
## Stage 03 — Taxonomy

| Field | Value |
|---|---|
| Status | **Ratified** on 2026-11-07, with two binding clarifications (`docs/decisions/2026-11-07-stage-03-ratified-g1t-review-authorized.md`, A1), which section 2 records and sections 3 and 6 apply. The text submitted for ratification was `docs/proposals/2026-11-07-stage-03-taxonomy-standard.md` at `72401ef`; its rules were approved earlier the same day (`docs/decisions/2026-11-07-tranche-2-accepted-g1t-preparation-authorized.md`, A2). A substantive change is a new, reviewed version |
| Date | 2026-11-07 (first proposed under `docs/decisions/2026-11-07-curation-tranche-2-approved.md`, A3; aligned the same day) |
| Drafted by | Claude Code (`claude-opus-5-5`), for the BCO team |
| Applies to | The `broader` links of the controlled vocabulary's catalog concepts (`src/01_controlled_vocabulary/catalog.yaml`), and the structured review records that classify them (`docs/catalog/tranche-<n>-review.yaml`) |

## 1. Purpose

A taxonomy link says how two capability concepts stand to each other. This standard fixes:
- the relationship kinds a reviewed link may have;
- the dispositions a review may record;
- what evidence each needs;
- how a link is reviewed and traced back to its source.

A link is a statement about meaning, made before formalization. It is not an axiom.

## 2. The approved rules

These are the architect's rules of 2026-11-07, as approved. The sections below apply them.

1. `kind-of` identifies proposed genuine conceptual specialization.
2. `part-of` identifies a reviewed partitive or functional-component relationship. It does
   not automatically assert BFO continuant parthood or OWL subclass relationships between
   dispositions.
3. `incorrect` is a review disposition, not a semantic relationship.
4. SKOS broader relationships must remain distinguishable from proposed OWL subclass
   relationships.
5. Every retained relationship requires provenance and a recorded justification.
6. Unresolved relationships remain unresolved rather than being forced into the taxonomy.

**Binding clarifications** (ratification, 2026-11-07). They add no relationship kind:

- **C1.** A `kind-of` relationship requires genuine specialization of the capability
  disposition: every instance of the narrower capability type must also be an instance of
  the broader type. Shared terminology, bearer similarities and realization-index overlap
  alone do not establish subclasshood.
- **C2.** A source hierarchy is supporting evidence for a proposed functional-component
  (`part-of`) relationship, not sufficient proof by itself. The relationship must also
  satisfy the conceptual coverage test.

## 3. Relationship kinds

A retained link has exactly one of two kinds. There are no others.

| Kind | Meaning | Test | What it may become at Stage 05 |
|---|---|---|---|
| **`kind-of`** | Proposed specialization: every exercise of the narrower capability is an exercise of the broader. The narrower is the broader with its object or manner restricted ("foreign exchange risk management" under "financial risk management") | Substitution: "an organization able to do N is, by that ability, able to do B" holds for any bearer, so that every instance of the narrower disposition is an instance of the broader (C1). The narrower's differentia adds a restriction and removes nothing; where the broader's definition is a conjunction, the narrower must meet every conjunct. Shared words, a shared bearer kind or overlapping indexes are not enough | A *proposal* for `rdfs:subClassOf`, considered only after G1-T for both classes and the formalization review (CD9). A `kind-of` link asserts no subclass axiom |
| **`part-of`** | Reviewed partitive or functional component: the narrower is one of the abilities the broader's work comprises, and not a kind of it ("cash management" within "treasury management"). Catalog hierarchies such as PCF's are mostly built this way | Coverage: exercising N is doing part of B's work, as B's definition states that work, but having N alone is not having B. A source hierarchy supports the link and does not prove it (C2) | Never a subclass axiom, and not by itself BFO continuant parthood between the dispositions. Any formal reading is a Stage 05 decision of its own; where CD16 applies, the link is recorded in the functional-coverage register |

## 4. Review dispositions

Every proposed link, and every link a reviewer adds, gets exactly one disposition.

| Disposition | Meaning | Kind |
|---|---|---|
| **retained** | The relationship holds, with its kind recorded | `kind-of` or `part-of` |
| **incorrect** | No relationship holds. The reason is one of: *homonym* (the sources' words match, their meanings do not); *containment artifact* (shared label words only); *reversed* (the direction is wrong); *dependency* (B uses N's result, but N is neither a part nor a kind of B: time reporting feeding payroll, tranche 1 §5); *rejected candidate* (an end of the link is not a concept, because its candidate was rejected) | none: `incorrect` is a disposition, not a relationship (rule 3) |
| **unresolved** | Neither kind can be established on the evidence available, for example because the right broader concept is not yet curated | none: the link is not written, and no kind is assigned to make it fit (rule 6). It stays in the review record until the concept it needs exists |

A retained link also records what was done with it:

| Action | Meaning | Written as `broader` |
|---|---|---|
| kept | retained as proposed | yes, when both ends are concepts |
| retargeted | retained against a different broader than the one proposed, with the reason | yes, to the new broader |
| added | proposed by a reviewer rather than the generator | yes, when both ends are concepts |
| kept-outside | retained, with an end in a domain not yet curated | no, until that end is a concept |
| redundant | holds, but follows from another retained path | no |
| merged | carried by a merge into another candidate | through the concept it merged into, if at all |

An incorrect link's action is *rejected*, or *dropped* when its reason is a rejected
candidate. An unresolved link's action is *held*.

## 5. SKOS `broader` and proposed subclass relations

Only retained links are written to the vocabulary, and both kinds are written as
`skos:broader` (rule 4). The kind is never read from the `broader` link: it is read from the
review record, which gives every link its kind. So:
- a `skos:broader` asserts only the SKOS hierarchy, never `rdfs:subClassOf`;
- the proposed subclass relations are exactly the retained `kind-of` links in the review
  records, and nothing else;
- no SKOS extension, OWL property or annotation carries the kind. The review record does,
  and its tests hold it to the vocabulary.

## 6. Evidence and justification

Every retained link has a recorded justification (`reason`) and provenance (rule 5).

| Disposition and kind | Evidence required |
|---|---|
| retained, `kind-of` | The two definitions, showing the restriction and that every instance of the narrower is an instance of the broader (C1). Overlapping realization indexes may support this, never establish it |
| retained, `part-of` | The coverage test, recorded in the link's reason by naming the work in the broader's definition that the narrower does (C2). A source hierarchy (record and locator) supports it, and is never enough alone |
| incorrect | The reason, with the definitions or source records that show it |
| unresolved | What is missing, and what would resolve it |

A source hierarchy is supporting evidence for `part-of`, never proof of it, and no evidence for `kind-of`. A link proposed
only by object containment (shared label words) needs one of the definition tests before it
is retained.

## 7. Review

1. **Ontologist (drafting).** The development team classifies each link and records it in
   the tranche's review record, with evidence and reason. Routine classification needs no
   approval of its own.
2. **Synthetic domain review.** A product-owner-authorized synthetic practitioner reviews
   the tranche once (`docs/decisions/2026-11-02-r11-practitioner-validation-decided.md`).
   Its identity and capacity are recorded. A substantive finding reopens the links it
   names; a routine one is applied and noted.
3. **Proxy Domain Expert (architect).** Material disagreements, unresolved links, and any
   link a later formalization depends on, are consolidated for the architect.

**Review criteria for each link:**
- Does the relationship hold at all, or is it incorrect or unresolved?
- If it holds, is the kind right, by its test?
- Does the evidence support it, and is the direction right?
- Does it duplicate another retained path?
- Do both definitions still read correctly in the light of it? A definition is never
  changed only to make a link fit a source hierarchy.

## 8. Traceability

Every link in a review record records:
- the narrower and broader candidates, and so their concepts;
- its provenance: for a proposed link, the generator's basis (a `hierarchy:` record pair or
  `object-containment:` words); for an added link, the review that added it;
- its disposition, its kind if retained, its action and its reason;
- for a retargeted link, the new broader.

The record's reviewers, with their roles and capacities, are the reviewers of every link in
it. The generated catalog is never edited. Concepts cite their candidates
(`catalog_candidates`), and the crosswalk keeps every source record.

## 9. Quality gate

A tranche's taxonomy is **validated** when:
- this standard is ratified;
- every link in scope has a disposition;
- every retained link has a kind, a reason and provenance;
- the synthetic review has no unresolved substantive finding;
- the vocabulary's `broader` links equal the retained links that section 4 writes;
- the validation gate (`tools/vocab/build.py`, the vocabulary shapes and the tests) passes.

Unresolved links do not prevent validation; they are reported as unresolved. Until the
standard is ratified, the same work is reported as *classified*.

## 10. Boundary

- This standard authorizes no OWL axiom, object property, annotation property or class, and
  no SKOS extension.
- It does not make the full taxonomy a prerequisite of Stage 05. Each formalization tranche
  needs a reviewed baseline for its own concepts and their ancestors (roadmap T8).
