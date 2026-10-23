# Business and Agent Capabilities Ontology

**Status: draft / exploratory. No ADR-002 ratification or v0.4 ontology implementation is implied.**

A workspace for developing the Business Capability Ontology (BCO) in alignment with BFO 2020, CCO 2.0, and the companion [Business Process Ontology](https://github.com/Skreen5hot/BusinessProcessOntology).

## Current sources

- **[BCO specification v0.4.0-draft.1](specifications/Business-Capability-Ontology-v0.4.0-draft.1.md)** — latest requirements and target design. **Not an implementation.**
- **[R5 review of v0.4 against artifacts](reviews/R5-v0.4-artifact-review.md)** — unresolved issues and validation gaps; review findings are recommendations, not ratified changes.
- **[Ontology draft v0.1.0](drafts/BusinessCapabilityOntology_draft_v0.1.0/README.md)** — earlier Turtle ontology, SHACL sketches, sample fixtures, tests, audit and proposed ADR. **Does not implement v0.4.**
- [Specification v0.3.0-draft.1](specifications/Business-Capability-Ontology-v0.3.0-draft.1.md) — historical predecessor, retained for design provenance.

## Organization

```text
specifications/        Normative candidates and versioned specifications (currently all draft)
reviews/               Review findings and recommendations
drafts/                Versioned prototype artifacts, preserved without semantic migration
docs/                  Intake inventory, checksums and provenance
```

The v0.1 ontology remains under `drafts/` to avoid giving the impression that its classes, axioms, or tests represent a reviewed v0.4 release.  Do not copy its proposed ADR-002 over the accepted ADR-001 in the companion BPO repository. No BPO files have been imported or vendored into this repository.

## Validation and known limitations

The historical v0.1 package includes its own `docs/VALIDATION.md` and `tests/check_draft.py`. The R5 review records further blockers (material basis policy, maturity-value encoding, instance evidence, and migration of BPO existential restrictions). **No v0.4 SHACL, OWL DL, or SPARQL acceptance suite has been executed or claimed here.**

See [docs/ARTIFACT-INVENTORY.md](docs/ARTIFACT-INVENTORY.md) for source provenance and checksum details. Files from the v0.1 package are preserved byte-for-byte.
