# Ontology Development Standard
## Stage 03 — Taxonomy (proposed)

| Field | Value |
|---|---|
| Status | **Proposed**, for the architect's approval (`docs/decisions/2026-11-07-curation-tranche-2-approved.md`, A3). Until it is approved, no taxonomy relationship is *validated*. A link reviewed under this draft is *classified*, and the classification is held for confirmation. On approval, this text moves to `docs/standards/stage-03-taxonomy.md` |
| Date | 2026-11-07 |
| Drafted by | Claude Code (`claude-opus-5-5`), for the BCO team |
| Applies to | The `broader` links of the controlled vocabulary's catalog concepts (`src/01_controlled_vocabulary/catalog.yaml`), and the structured review records that classify them (`docs/catalog/tranche-<n>-review.yaml`) |

## 1. Purpose

A taxonomy link says how two capability concepts stand to each other. This standard fixes:
- the kinds of link;
- what evidence each kind needs;
- how a link is reviewed;
- how the review is traced back to its source.

A link is a statement about meaning, made before formalization. It is not an axiom.

## 2. Relationship kinds

Every proposed link between two concepts gets exactly one of these classifications.

| Kind | Meaning | Test | What it may become at Stage 05 |
|---|---|---|---|
| **specialization** | Every exercise of the narrower capability is an exercise of the broader. The narrower is the broader with its object or manner restricted ("foreign exchange risk management" under "financial risk management") | Substitution: "an organization able to do N is, by that ability, able to do B" holds for any bearer. The narrower's differentia adds a restriction and removes nothing | A candidate for `rdfs:subClassOf`, only after G1-T for both classes and the formalization review (CD9) |
| **component** | The narrower is one of the abilities the broader's work comprises, and not a kind of it ("cash management" within "treasury management"). This is how catalog hierarchies such as PCF's are mostly built | Coverage: exercising N is doing part of B's work, but having N alone is not having B | Never a subclass axiom. It stays a SKOS `broader` (partitive), and where CD16 applies it is recorded in the functional-coverage register |
| **incorrect** | Neither of the above. Its reason is one of: *homonym* (the sources' words match, their meanings do not); *containment artifact* (shared label words only); *reversed* (the direction is wrong); *dependency* (B uses N's result, but N is neither a part nor a kind of B: time reporting feeding payroll, tranche 1 §5) | — | Removed from `broader`, and recorded with its reason. A dependency is recorded as such, never as a parent |

A link may also be **re-targeted**: classified against a different broader than the one proposed, with the reason recorded.

Only *specialization* and *component* links are written as `broader` in the vocabulary. The review record keeps every link's kind, so a SKOS `broader` never stands alone for meaning.

## 3. Evidence

| Kind | Evidence required |
|---|---|
| specialization | The two definitions, showing the restriction. Where the classes have realization indexes, the narrower's admissible acts are a subset of the broader's genera |
| component | A source hierarchy (with record and locator) or the broader's definition naming the work, plus the definition test above |
| incorrect | The reason (homonym, containment artifact, reversed, dependency), with the definitions or source that show it |

Source hierarchy alone is evidence for *component*, never for *specialization*. A link that only object containment proposed (shared label words) needs one of the definition tests before it is kept.

## 4. Review

1. **Ontologist (drafting).** The development team classifies each proposed link and
   records the classification, with evidence and reason, in the tranche's review record.
   Routine classification needs no individual approval.
2. **Synthetic domain review.** A product-owner-authorized synthetic practitioner reviews
   the tranche once (docs/decisions/2026-11-02-r11-practitioner-validation-decided.md). Its
   identity and capacity are recorded. A substantive finding reopens the links it names; a
   routine one is applied and noted.
3. **Proxy Domain Expert (architect).** Material disagreements, and any link a later
   formalization depends on, are consolidated for the architect.

**Review criteria for each link:**
- Is the kind right, by its test?
- Does the evidence support it?
- Is the direction right?
- Does the link duplicate another path?
- Do both definitions still read correctly in the light of the link?

## 5. Traceability

Every classified link records:
- the narrower and broader concepts;
- the catalog candidates it came from;
- the generator's proposed basis (`hierarchy:` record pair, or `object-containment:` words);
- its kind, its action (kept, re-targeted, rejected, added) and the reason;
- the reviewer.

Links the reviewers add, which the generator did not propose, are marked *added*. The generated catalog is never edited. Concepts cite their candidates (`catalog_candidates`), and the crosswalk keeps every source record.

## 6. Quality gate

A tranche's taxonomy is **validated** when:
- this standard is approved;
- every proposed link in scope is classified;
- the synthetic review has no unresolved substantive finding;
- the vocabulary's `broader` links equal the kept specialization and component links;
- the validation gate (`tools/vocab/build.py`, the vocabulary shapes, the tests) passes.

Until the standard is approved, the same work is reported as *classified*.

## 7. Boundary

- This standard authorizes no OWL axiom, object property or class.
- It does not make the full taxonomy a prerequisite of Stage 05. Each formalization tranche needs a reviewed baseline for its own concepts and their ancestors (roadmap T8).
