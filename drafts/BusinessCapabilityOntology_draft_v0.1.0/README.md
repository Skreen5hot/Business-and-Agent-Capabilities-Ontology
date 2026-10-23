# Business Capability Ontology — proposed companion draft v0.1.0

**PROPOSED / UNAPPROVED** · 2026-10-22 · BFO 2020 / CCO 2.0 (2024-11 releases)

This package is a conservative first version of a companion ontology to [BusinessProcessOntology](https://github.com/Skreen5hot/BusinessProcessOntology). It contains **one proposed realist capability class and six proposed information classes**, not a completed enterprise-wide capability taxonomy.

**Begin with [`docs/ADR-002-business-capabilities.md`](docs/ADR-002-business-capabilities.md).** In particular, the grounding problem is handled *before* assigning the disposition type.

## Ontology commitments

- `bc:BusinessCapability` is a CCO Organization Capability **and** BFO Disposition. It is not declared equivalent to the two-class intersection.
- Bearer = actual CCO Organization (aggregate of agents), not the organization plus all subcontractors' resources.
- Supplier-enabled delivery claims and sourcing arrangements are represented in the assessment/description layer, unless internal grounding is independently established.
- A capability can exist even when it has never been realized; there is deliberately **no** `has realization some Process` restriction.
- The ontology is neutral on whether an instance is also a BFO Function; it makes no disjointness claim.
- Capability types are conceptually indexed to suitable BPO Planned Act types, but the potential-realization *class-to-class* bridge remains unsolved in OWL under the existing object properties. Do not use actual `BFO has realization` to encode mere potential.
- Organizations' roles and permissions, the institutional status of an act, and prescribed plans remain distinct from capabilities.
- No new object properties. No inferred dispositions from SKOS maps, contracts, maturity ratings, or target-state plans.

## Layout

| File | Purpose |
|---|---|
| `ontology/business-capability-core.ttl` | One realist class `bc:BusinessCapability` |
| `ontology/business-capability-information.ttl` | Six ICE classes: description, map, assessment, maturity, sourcing, target state |
| `alignment/bpo-review-links.ttl` | **Non-logical annotation** review links to four existing BPO capability classes |
| `examples/synthetic-illustration.ttl` | Synthetic ABox showing an **unexercised** asserted disposition and separate ICEs |
| `shapes/capability-data-shapes.ttl` | Optional SHACL instance-data-quality checks; not upper-ontology logical axioms |
| `docs/ADR-002-business-capabilities.md` | Proposed normative decisions, open issues, competency questions |
| `docs/IRI-AUDIT.md` | Exact IRI / class / property and BPO audit ledger |
| `docs/VALIDATION.md` | Validations actually run vs not run |
| `tests/check_draft.py` | Offline structural tests using `rdflib` |

## How to inspect

```bash
python -m pip install rdflib
python tests/check_draft.py
```

These static tests do not claim OWL DL logical consistency. A rigorous integration run requires the BPO repository's pinned CCO closure, configured ontology-IRI resolution, and its SHACL / ROBOT reasoner gates. See `docs/VALIDATION.md`.

## Integration proposal — not an automatic migration

1. Present ADR-002 for approval and choose a production namespace.
2. Run the complete repository-wide capability and realization-restriction audit, including the `capabilities/` directory.
3. Determine the act-index relation representation and validate the physical-grounding admission standard.
4. Refactor existing BPO capability classes **only after** their individual bearer/grounding/latency reviews.
5. Validate the integrated ontology with BPO gates A–D and repeat competency questions with real examples.

## Definition policy

Each new class has an explicit immediate parent (`rdfs:subClassOf`), human label, genus–differentia `skos:definition`, `rdfs:comment`, and `skos:example`. These terms are *new proposals*, deliberately separated from existing CCO classes.

## Scope caveats

Example.org IRIs are provisional and not guaranteed dereferenceable. The public repository's mutable `main` was inspected through accessible file views, not fetched as a complete clone; no claim is made about the full `capabilities/` folder. CCO classes and properties have been verified from the user-provided PDF renderings; full merged-file logical validation is still outstanding.

No publication license has been selected for the new draft; choose it before distribution as an official repository module. Referenced BPO code and CCO/BFO dependency licenses are independent of this proposal.
