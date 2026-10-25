# Formal Review of the Five BCO Turtle Artifacts

Conditional approval — not ready for OWL ratification

## 1. Executive assessment

I examined the five uploaded Turtle files directly, including their RDF declarations, concept definitions, metadata, cross-file references, and provenance structures.

The artifacts constitute a coherent, machine-readable controlled vocabulary with substantial provenance information. They do not yet constitute a formally axiomatized BFO/CCO ontology.

This is an important distinction. The implementation appears deliberately designed to manage the vocabulary separately from its eventual OWL representation. That is a defensible architecture, provided its limitations are understood.

### RDF validation results

| Artifact             | RDF triples | Parse result |
| -------------------- | ----------- | ------------ |
| `bco-vocabulary.ttl` | 63          | Pass         |
| `bco-sources.ttl`    | 272         | Pass         |
| `bco-metamodel.ttl`  | 340         | Pass         |
| `bco-catalog.ttl`    | 104         | Pass         |
| `bco-agents.ttl`     | 8           | Pass         |
| Combined graph       | 787         | Pass         |

All five files parse successfully using RDFLib's Turtle parser.

Across the combined graph, I verified:

- 9 metamodel SKOS concepts.
- 5 capability catalog SKOS concepts.
- 2 SKOS concept schemes.
- 63 bibliographic source records.
- 2 declared provenance agents.
- 21 locally defined vocabulary terms, consisting of 20 annotation properties and one datatype.

### Most important finding

OWL classes declared in these files

# 0

OWL subclass axioms

# 0

OWL object properties declared

# 0

For example, `bcom:BusinessCapability` is declared as a `skos:Concept`. It has a `bco:designatesClass` annotation pointing to `bco:BusinessCapability` and a `bco:specParent` annotation identifying its intended parents.

However, these annotations do not assert:

```
bco:BusinessCapability
    a owl:Class ;
    rdfs:subClassOf
        cco:ont00000568 ,
        obo:BFO_0000016 .
```

The absence of these triples is not necessarily an error in a vocabulary-management artifact. It becomes an error only if this material is represented as an executable OWL ontology or if downstream applications assume that it contains enforceable BFO/CCO semantics.

Recommendation: Retain the SKOS vocabulary architecture, but make its non-axiomatic status explicit and maintain a separate, formally validated OWL ontology layer if logical reasoning or conformance testing is required.

## 2. Cross-file integrity and provenance

The referential integrity of the artifacts is generally strong.

| Validation                               | Result                                                                     |
| ---------------------------------------- | -------------------------------------------------------------------------- |
| Concept labels and definitions           | Pass — exactly one of each per concept                                     |
| Concept-to-scheme membership             | Pass — all 14 resolve                                                      |
| Metamodel concept-to-class designation   | Pass — all 9 have designated class IRIs                                    |
| External superclass identifiers          | Pass — all six distinct parent IRIs located in supplied BFO/CCO references |
| Source-reference resolution              | Pass — no dangling source references                                       |
| Source-reference relation metadata       | Pass                                                                       |
| `consistent-with` support classification | Pass — all 30 classified                                                   |
| `departs-from` justifications            | Pass — all 12 have notes and claim indices                                 |
| Concept-to-agent attribution             | Pass                                                                       |
| Current-record digest correspondence     | Pass — hashes match their current-record IRI suffixes                      |
| Historical revision resolution           | Incomplete — 14 historical record targets are not included                 |

There are 54 concept-to-source-reference links, involving 43 distinct source-reference resources and 21 distinct bibliographic sources.

That degree of provenance is unusual for an early-stage ontology, and worth preserving.

### Finding A — Claim verification provenance loses detail

High priority

In `bco-sources.ttl`, source records have `bco:claimStatus` assertions.

For example, `bcos:SRC-OG-01` has three separate status values: `K`, `L`, and `S`.

However, the output does not identify the individual claims to which those statuses apply. RDF triples are unordered, so consumers cannot infer correspondence from the sequence of values.

Meanwhile, the metamodel uses `bco:citesClaim` with integer values, typically `1`, for departure justifications.

The result is a provenance gap: the generated RDF identifies a claim number, but the claim's text and corresponding status are not fully recoverable from the five submitted artifacts.

Recommendation: Preserve the claim index, claim text, and status as a single structured record in the generated provenance representation. The appropriate implementation could use RDF resources and existing annotation/provenance properties; no new domain object property is inherently required.

This is a problem with the completeness of the exported provenance graph, not proof that the underlying YAML register is incorrect.

### Finding B — Historical revision chains are incomplete

Each of the 14 current concept records has a `prov:wasRevisionOf` assertion.

All 14 historical targets are absent from the submitted graphs.

This is valid RDF, but historical revision details cannot be inspected from these artifacts alone.

If the repository maintains a separate historical record store, this may be intentional. The specification should identify that store and explain how historical versions are retrieved.

Also, matching a record digest to an IRI suffix verifies internal naming consistency, not the correctness of the digest relative to the source YAML. That stronger check requires the source content and hashing algorithm.

## 3. Metamodel review

The nine metamodel concepts remain semantically useful, but their current formal representation is incomplete.

| Concept                               | Assessment                | Remaining concern                                                       |
| ------------------------------------- | ------------------------- | ----------------------------------------------------------------------- |
| Authorization Record                  | Accept with clarification | An authorization record must remain distinct from a valid authorization |
| Business Capability                   | Conditional               | Disposition, material basis, realization index                          |
| Capability Assessment                 | Revise                    | Meaning of partial presence and type reference                          |
| Capability Map                        | Revise                    | Mixed descriptive and directive contents                                |
| Capability Maturity Rating            | Largely acceptable        | Ordinal scale and measurement target                                    |
| Capability Sourcing Assessment        | Largely acceptable        | Necessary assessment criteria                                           |
| Capability Sourcing Statement         | Conditional               | Class-level act reference and sourcing semantics                        |
| Capability Target                     | Strong                    | Representation of desired capability types                              |
| Capability Target-State Specification | Strong                    | Target linkage and formal Plan restrictions                             |

### Finding C — Business Capability is not yet formally axiomatized

The metamodel correctly records two intended parents for `bco:BusinessCapability`:

`cco:ont00000568` — Organization Capability

`obo:BFO_0000016` — Disposition

Both references exist in the supplied ontologies.

More importantly, CCO 2.0 already supplies a formal pattern for Organization Capability, including an equivalence axiom using Agent Capability and the `capability of` relation (`cco:ont00001889`) to an Organization.

This should be reused rather than reconstructed through custom relations.

The BCO's narrower material-basis restriction remains an architectural choice requiring justification.

It is especially important to distinguish the BFO relation `has material basis` (`BFO_0000218`) from ordinary resource dependency. The relation requires a material entity that is a continuant part of the disposition's bearer and contributes to its bearing that disposition.

A software system, production facility, or externally supplied service cannot simply be treated as an organizational member to satisfy that restriction.

Assessment: The proposed class is plausible, and no direct inconsistency was established. Formal conformance remains untested because the intended subclass and restriction axioms have not been emitted.

### Finding D — The capability type reference problem is unresolved

This remains my principal concern.

A Capability Target refers to a capability type that an organization is intended to acquire.

A Capability Maturity Rating instead concerns an existing capability instance.

A Capability Assessment may state the absence of a capability of a particular type.

These distinct referencing requirements cannot all be implemented by treating a capability class, a SKOS concept, and an individual disposition as interchangeable.

The new `bco:designatesClass` annotation is a useful step toward separating vocabulary concepts from OWL classes.

However, the artifacts do not yet show the actual implementation of that separation in assessments, targets, or instance data.

Recommendation: Document three explicit patterns: capability-type designation, instance-level capability attribution, and prospective reference to a capability type that has no existing instance.

These should use authorized BFO/CCO relations wherever possible, with vocabulary metadata remaining outside the domain reasoning layer.

## 4. Capability catalog review

The catalog is materially improved from the earlier vocabulary.

The `skos:changeNote` annotations show that the previous restrictive definitions have been revised. In particular, the definitions no longer require multiple employees to realize Competitive Analysis or require hedging as a necessary component of Treasury Management.

The change from "realized in" to "realizable in" is also important: it better accommodates capabilities that have not yet been exercised.

### Remaining definition issues

| Capability                     | Current assessment         | Suggested adjustment                                                                          |
| ------------------------------ | -------------------------- | --------------------------------------------------------------------------------------------- |
| Business Model Governance      | Good                       | "Decides how they should change" should permit deciding that no change is needed              |
| Competitive Analysis           | Good                       | Consider whether competitors must always be organizations                                     |
| Customer Experience Management | Good, somewhat conjunctive | Clarify whether understanding and shaping experience are both always necessary                |
| Strategic Planning             | Good                       | "Long-range" may unnecessarily exclude some forms of strategic planning                       |
| Treasury Management            | Needs refinement           | "Ensures" suggests guaranteed success rather than an ability to undertake treasury management |

The Treasury Management wording is the most significant residual problem.

A capability can exist despite unsuccessful realization. A company's treasury team might have the ability to manage liquidity while nevertheless experiencing a funding shortage.

Therefore, the definition should not make successful payment outcomes necessary for possessing the capability.

One candidate for further evaluation is:

> A Business Capability that is realizable in Planned Acts by which an Organization manages its cash positions, liquidity, funding, and financial exposures in support of meeting its financial obligations.

This is a proposed refinement, not a newly authorized OWL class definition.

### Finding E — The catalog's recorded genus does not match its textual genus

Medium-high priority

All five catalog entries use the textual genus "A business capability."

Yet each `bco:definitionGenus` points directly to:

`cco:ont00000568` — Organization Capability.

The metamodel separately identifies the proposed class:

`bco:BusinessCapability`.

These choices are potentially inconsistent.

If the catalog entries are intended to be subclasses of BCO Business Capability, that class is their immediate genus, whereas CCO Organization Capability is an ancestor.

If the catalog entries are intended to be direct specializations of CCO Organization Capability, the use of "business capability" as their genus requires an explanation.

Recommendation: Resolve the intended hierarchy before generating OWL classes. The `definitionGenus` annotation should distinguish the immediate parent from any more general foundational ancestor.

Do not silently change the five references until the architectural decision has been made.

## 5. Vocabulary and namespace review

The namespace scheme is well separated:

| Namespace | Role                                     |
| --------- | ---------------------------------------- |
| `bco:`    | Core BCO terms and vocabulary properties |
| `bcom:`   | Metamodel concepts and provenance        |
| `bcoc:`   | Catalog concepts and provenance          |
| `bcos:`   | Bibliographic source records             |
| `bcoa:`   | Provenance agents                        |

The separation makes it possible to assign stable identities to the ontology classes, the vocabulary concepts describing those classes, and the sources documenting them.

I would retain it.

### Finding F — `bco:PCFCode` is incompletely constrained

The vocabulary declares:

`bco:PCFCode rdf:type rdfs:Datatype`

Its definition specifies APQC PCF 7.4 element identifiers.

However, the artifacts provide no lexical restriction, example values, or actual data using that datatype.

A conforming RDF consumer therefore has insufficient information to validate whether a literal is a valid PCF code, beyond the prose definition.

For a future operational release, specify its permitted lexical form and how edition-specific validation is performed.

### Finding G — Lifecycle status is descriptive rather than enforceable

All 14 concepts are correctly marked `Draft`.

The vocabulary defines four lifecycle values: Draft, Candidate, Ratified, and Deprecated.

However, the values are plain literals, and the present files do not define machine-enforceable transition constraints.

This is acceptable if the build script is the authoritative lifecycle validator, as the comments indicate.

It should simply be documented that lifecycle enforcement takes place in the build process, not through these RDF triples alone.

## 6. BFO/CCO relationship reuse

I checked the relevant foundational constructs against the supplied BFO and CCO references, including the Extended Relations, Agent, and Information Entity ontologies.

The existing relations provide useful starting points for the eventual OWL layer.

| Modeling requirement                                  | Existing property           | IRI               |
| ----------------------------------------------------- | --------------------------- | ----------------- |
| Connect an organizational capability to its bearer    | capability of               | `cco:ont00001889` |
| Represent the material basis of a disposition         | has material basis          | `BFO_0000218`     |
| Connect a realizable entity to its actual realization | has realization             | `BFO_0000054`     |
| Express the inverse realization relationship          | realizes                    | `BFO_0000055`     |
| Connect an ICE to an entity it concerns               | is about                    | `cco:ont00001808` |
| Connect an ordinal measurement to its subject         | is a ordinal measurement of | `cco:ont00001811` |
| Express appropriate continuant parthood               | has continuant part         | `BFO_0000178`     |

Using an existing property still requires satisfying its domain, range, and intended semantics.

In particular, `is about` does not automatically establish a way for a capability target to reference an OWL class as a type. That requires an explicit representational design.

No new domain object property is justified by the evidence presently available.

## 7. Recommended dispositions

| Finding                               | Priority | Disposition                     |
| ------------------------------------- | -------- | ------------------------------- |
| A — Claim-level provenance            | High     | Revise RDF export               |
| B — Historical revisions              | Medium   | Document or publish history     |
| C — Formal Business Capability axioms | High     | Resolve before OWL ratification |
| D — Type versus instance reference    | Critical | Resolve before OWL ratification |
| E — Catalog genus mismatch            | High     | Clarify hierarchy               |
| F — PCF datatype constraints          | Low      | Improve before operational use  |
| G — Lifecycle validation              | Low      | Document build-time enforcement |

## 8. Final recommendation

As a SKOS vocabulary and provenance export

Acceptable draft

As a formal BFO/CCO OWL ontology

Not yet demonstrated

The generated artifacts have a coherent internal structure, successfully parse, maintain consistent source links, and preserve the drafting and review history. The five catalog definitions are notably more inclusive than their earlier versions.

I would not recommend abandoning or substantially restructuring the vocabulary architecture.

The next step should be a formal ontology layer that implements the approved class hierarchy and permitted relations, without conflating SKOS catalog concepts, OWL classes, and particular capabilities possessed by organizations.

That layer can then be tested using an OWL reasoner against the approved BFO/CCO release. The current artifacts cannot establish OWL consistency or BFO/CCO conformance by themselves.

My overall conclusion is that the vocabulary engineering is largely sound, while the formal ontology engineering remains unfinished. The highest-value work is to resolve the capability type-reference pattern and the intended Business Capability subclass hierarchy before introducing formal axioms.

The review is limited to the five submitted Turtle files and the supplied BFO/CCO references; I did not have the generator, source YAML, complete specification, or historical record store needed to validate build reproducibility and full lifecycle governance.
