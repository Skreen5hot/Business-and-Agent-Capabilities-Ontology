# Ontology Development Standard
## Stage 02 — Conceptual Modeling

**Status:** Approval-ready  
**Primary Responsibility:** Ontologist / Semantic Engineer, in collaboration with domain subject matter experts  
**Primary Artifact:** Conceptual Domain Model

---

## 1. Purpose

The Conceptual Modeling stage establishes a coherent, shared, representation-independent understanding of the domain to be modeled.

Its purpose is to identify the principal categories of things in the domain, their distinguishing characteristics, meaningful relationships, and conceptual boundaries necessary to support the intended requirements and competency questions.

Conceptual models provide an architectural target for subsequent ontology formalization without prematurely prescribing the formal constructs used to implement them.

**Conceptual modeling establishes what the ontology is intended to represent. Ontology formalization determines how that representation is implemented.**

## 2. Governing Principles

### 2.1 Semantic and Representation Independence

Conceptual models MUST remain independent of the physical and logical schemas of source databases, application interfaces, serialization formats, and implementation technologies.

Source schemas MAY inform domain understanding but MUST NOT dictate the conceptual structure or classification of domain entities.

Differences in source data types, field names, character encodings, storage mechanisms, and other implementation details MUST NOT determine conceptual classifications.

### 2.2 Conceptual Clarity

Conceptual models MUST identify the principal domain entities, explain their intended meanings, distinguish related categories, and describe their meaningful associations.

The emphasis is on establishing conceptual understanding rather than selecting formal ontology constructs.

### 2.3 Preliminary Foundational Alignment

Conceptual modeling SHOULD be informed by foundational and mid-level ontologies, including BFO and CCO where applicable.

Potential alignments MAY be identified to guide conceptual analysis.

However, exact superclass assignments, formal property selections, ontological restrictions, and logical axioms are not required during this stage.

Such decisions belong to ontology formalization.

### 2.4 Explicit Conceptual Relationships

Relationships in conceptual models MUST communicate the intended associations between domain concepts.

These relationships are conceptual and do not necessarily correspond directly to OWL object properties.

Conceptual relationships MAY be directional, symmetric, or undirected, as appropriate to the intended meaning.

Their formal interpretation, including property reuse, logical characteristics, and restrictions, is determined during ontology formalization.

### 2.5 Human Interpretability

Conceptual models MUST provide clear, human-readable representations suitable for review by domain stakeholders and ontology engineers.

Diagrams MUST be accompanied by textual explanations identifying the concepts and relationships depicted.

### 2.6 Progressive Formalization

Conceptual modeling MUST preserve the flexibility necessary for subsequent ontological analysis.

Conceptual distinctions SHOULD be sufficiently developed to guide formalization without requiring every formal modeling decision to be resolved in advance.

## 3. Inputs

Conceptual modeling draws upon:

- Controlled vocabulary terms and candidate definitions
- Domain expertise and stakeholder requirements
- Business and analytical use cases
- Competency questions
- Existing conceptual models and design patterns
- Relevant foundational and domain ontologies
- Applicable architecture and governance decisions

Additional documentation, including existing data models and source schemas, MAY be used to inform understanding of the domain.

## 4. Modeling Activities

### 4.1 Establish Scope

Define the domain boundaries, modeling objectives, intended use cases, and relevant competency questions.

Identify what is included and excluded from the model.

### 4.2 Identify Principal Concepts

Identify the major categories of things necessary to describe the domain.

For each concept, document:

- Preferred name
- Natural-language description
- Distinguishing characteristics
- Relevant examples
- Conceptual boundaries
- Relationships to other concepts

Concept descriptions need not satisfy the requirements of formal ontological definitions.

### 4.3 Establish Conceptual Relationships

Identify meaningful associations among concepts.

Document the intended meaning of each relationship, its direction where meaningful, and any significant qualifications.

Relationships MAY be expressed using domain terminology without requiring immediate selection of corresponding OWL properties.

### 4.4 Develop Conceptual Patterns

Organize related concepts into coherent, reusable modeling patterns.

Each pattern SHOULD illustrate a meaningful structure or recurring relationship in the domain.

Patterns MAY be informed by established ontological design patterns, but their formal implementation is deferred to ontology formalization.

### 4.5 Evaluate Conceptual Boundaries

Identify important distinctions between related concepts.

Determine whether concepts represent distinct categories, alternative descriptions of the same category, or different aspects of a broader phenomenon.

Document ambiguities requiring further analysis.

### 4.6 Record Assumptions and Open Questions

Document the principal conceptual decisions, supporting assumptions, unresolved questions, and potential alternatives.

Questions concerning formal BFO/CCO classification, logical axioms, and property selection MAY be deferred to the ontology formalization stage.

Unresolved questions MAY be carried forward when they do not materially prevent agreement on the intended conceptual representation.

Conceptual ambiguities that materially affect the intended meaning, scope, or principal relationships MUST be resolved before approval.

### 4.7 Review with Stakeholders

Review the conceptual model for clarity, coherence, scope, and suitability for its intended requirements.

Confirm that the principal concepts and relationships reflect a shared understanding of the domain.

## 5. Required Deliverables

Each conceptual model MUST include:

| Artifact | Purpose |
|---|---|
| Model identifier and title | Identify the model |
| Scope and purpose | Explain the domain and modeling objective |
| Conceptual diagram | Illustrate concepts and relationships |
| Textual description | Explain the diagram in natural language |
| Concept descriptions | Describe principal concepts and distinctions |
| Relationship descriptions | Explain intended associations |
| Conceptual boundaries | Identify important distinctions and exclusions |
| Requirements traceability | Relate the model to relevant use cases or competency questions |
| Assumptions and open questions | Record issues for subsequent analysis |
| Review status | Document stakeholder agreement |

Preliminary BFO/CCO alignment, candidate ontology terms, and implementation recommendations MAY be included but are not required for approval.

The standard does not prescribe a particular diagramming notation or require that these deliverables be maintained as separate files.

## 6. Outputs

The primary output is an approved Conceptual Domain Model.

This model establishes:

1. The domain concepts that the ontology should represent.
2. The important distinctions among those concepts.
3. The intended conceptual relationships.
4. The boundaries and scope of the representation.
5. The requirements the formal ontology is expected to support.
6. Any unresolved questions that must be addressed during ontology development.

The conceptual model serves as a design input to ontology formalization.

It does not need to contain OWL declarations, logical axioms, finalized BFO/CCO assignments, or implementation-specific validation constraints.

## 7. Quality Gates

A conceptual model is ready for formalization when:

- [ ] The purpose and scope are clearly defined.
- [ ] Principal domain concepts have been identified and described.
- [ ] Important conceptual distinctions are documented.
- [ ] Meaningful relationships are represented and explained.
- [ ] The model addresses the intended requirements and competency questions.
- [ ] Diagrams and textual descriptions are consistent.
- [ ] Significant ambiguities and assumptions have been documented.
- [ ] No unresolved conceptual question materially prevents agreement on the intended representation.
- [ ] Domain stakeholders have reviewed the model.
- [ ] The model provides sufficient conceptual clarity to guide ontology formalization.

Approval does not require finalized ontology classes, superclass assignments, OWL properties, or logical axioms.

Automated checks MAY verify documentation completeness, internal references, and artifact consistency.

Conceptual adequacy and stakeholder agreement require human review.

## 8. Relationship to Other Ontology Development Stages

### 8.1 Taxonomy and Thesaurus

Taxonomy, thesaurus, and conceptual modeling activities MAY inform one another and proceed iteratively.

Existing classification structures and terminological associations MAY provide inputs to conceptual modeling.

The conceptual model may also inform the subsequent organization and clarification of domain terminology and classifications.

Terminological hierarchies and associations do not automatically become formal ontological relationships.

### 8.2 Ontology Formalization

The formalization stage interprets the approved conceptual model using the selected ontological framework.

This includes:

- Selecting and reusing ontology classes and properties
- Establishing formal BFO/CCO alignments
- Defining subclass relationships
- Developing formal class definitions
- Introducing logical restrictions and axioms
- Evaluating logical consistency and satisfiability

Formalization decisions MUST preserve the intended conceptual meaning or explicitly document justified changes.

### 8.3 Data Mapping and Integration

Source data is mapped to the formal ontology through appropriate mappings and transformations.

Physical schema differences are resolved at the integration level rather than imposed upon the conceptual model.

### 8.4 Metadata Schemas and Validation

SHACL, LinkML, JSON Schema, and similar technologies MAY define validation rules or data contracts for particular representations.

These mechanisms do not independently establish the conceptual meaning of the domain.

## 9. Change Management

Conceptual models MUST be version-controlled.

Changes affecting principal domain concepts, conceptual boundaries, or intended relationships SHOULD undergo stakeholder review.

Ontology formalization MAY reveal ambiguities or deficiencies requiring revisions to an approved conceptual model.

Such revisions MUST be documented and reconciled with the conceptual design.

Approval establishes a stable design baseline, not an irreversible freeze.

## 10. Definition of Done

The Conceptual Modeling stage is complete when a coherent, representation-independent conceptual model has been documented, reviewed, and accepted as a sufficient basis for ontology formalization.

The approved model MUST clearly communicate:

- What the ontology is intended to represent
- Why the principal concepts are distinguished
- How those concepts are meaningfully related
- What conceptual boundaries apply
- Which requirements and competency questions the model must support

**The stage does not require completion of formal ontological classifications, property selection, or logical axiomatization.**

These responsibilities belong to the subsequent Ontology Formalization stage.

---

## Guiding Principle

**Conceptual modeling defines the intended representation of the domain. Ontology formalization translates that representation into formally defined entities, relationships, and axioms using the selected ontological framework.**
