# Validation results — BCO draft v0.1.0

**Run date:** 2026-10-22. **Decision status:** Draft; not an OWL DL consistency certificate.

## Executed checks

| Check | Result | Evidence |
|---|---|---|
| RDF/Turtle syntax parse of all five TTL files | **PASS** | `rdflib.Graph.parse` |
| New OWL classes count and annotations | **PASS** | Exactly 7 new `owl:Class` nodes, with labels, genus–differentia definitions, comments and examples |
| New `owl:ObjectProperty` declarations | **PASS** | 0 new object properties |
| Realist class ancestry | **PASS** | Both CCO Organization Capability (`ont00000568`) and BFO Disposition (`BFO_0000016`) explicitly asserted |
| Unintended Function disjointness | **PASS** | No disjointness or equivalence of Business Capability with Function |
| `has realization` existential property restrictions in the draft | **PASS** | None |
| Existing BPO classes redefined or promoted | **PASS** | 0 class redefinitions; alignment annotations only |
| Example latent disposition | **PASS** | Asserts a Business Capability with its organization bearer, no realization triple |
| Local cross-file IRI checks | **PASS** | All cited BFO/CCO identifiers used in the modeling commitments were found by exact identifier in relevant supplied PDFs |
| Optional SHACL shapes RDF syntax | **PASS** | TTL syntax parsed successfully |

These are **static structural checks**. They do not prove all classes coherent or all axioms consistent after importing dependencies.

Example command and visible output:

```text
python tests/check_draft.py
PARSE OK alignment/bpo-review-links.ttl (14 triples)
PARSE OK examples/synthetic-illustration.ttl (17 triples)
PARSE OK ontology/business-capability-core.ttl (15 triples)
PARSE OK ontology/business-capability-information.ttl (44 triples)
PARSE OK shapes/capability-data-shapes.ttl (22 triples)
PASS: 7 new classes (1 realist, 6 ICE), 0 new object properties,
      0 inferred or existential realizations, no BPO class redefinitions.
```

## Not executed — DO NOT describe as passing

| Test | Status | Why |
|---|---|---|
| Full BFO 2020 + CCO 2.0 merged-file reasoning | **NOT RUN** | The exact machine-readable dependency closure was not available in this workspace; the provided PDFs were reference serializations |
| OWL DL logical consistency / unsatisfiability (ROBOT/ELK or HermiT) | **NOT RUN** | ROBOT was not installed and the integration closure not assembled |
| SHACL validation with `pyshacl` | **NOT RUN** | `pyshacl` was not installed; optional shapes have been parsed, not evaluated |
| BPO existing Gates A–D with integrated ontology | **NOT RUN** | The complete live repository, including runtime configuration and vendored closure, was not cloned |
| Full GitHub repository-wide capability audit | **NOT DONE** | Partial inspection of accepted ADR-001, README, methodology, shared act modules and `apqc_1_0.ttl`; `capabilities/` not enumerated |
| CCO 2.0 merged-release byte-for-byte provenance pin | **NOT VERIFIED** | The attached CCO PDF files state version 2.0, but the upstream merge digest has not been compared |
| Domain expert validation for function overlap, grounding, act indexing | **OPEN** | Substantive philosophical/ontological questions; not decidable by a syntax parser |
| Maturity value/scale provenance profile | **OPEN** | Only the Information Content Entity typing and ordinal target relation are proposed |

## Required integration sequence

1. Install/fetch BPO's pinned CCO 2.0 dependency closure and capture immutable upstream digests and BPO commit SHA.
2. Replace example.org with an approved IRI base, configure local `owl:imports` resolution.
3. Merge core and information modules with CCO closure; run OWL DL profile, ELK or HermiT, test coherence and unsatisfiable classes, including BFO disjointness.
4. Execute `pyshacl` on the optional shapes with a suitable OWL/RDFS inference setting and realistic positive/negative ABox fixtures; refine shapes as needed.
5. Inspect BPO's entire capability inventory, external provider dependencies, and latent realization restrictions. Do not import the full BPO slice into the alignment during review.
6. Run BPO Gates A–D and related semantic human reviews, then answer ADR competency questions with observed positive and counter-examples.
7. Only afterward consider release status beyond 'Proposed'.

## Key interpretation warning

A **syntax pass** cannot validate BFO dispositional grounding. The asserted material basis of an organizational disposition is a substantive claim and requires evidence; no SHACL shape here is presented as an adequate proof of metaphysical grounding.
