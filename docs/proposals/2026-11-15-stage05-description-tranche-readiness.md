# Stage 05 description tranche — readiness record

| Field | Value |
|---|---|
| Status | Prepared under the architect's decision of 2026-11-15, B-1 (`docs/decisions/2026-11-15-b1-b4-approved-cap34-confirmed.md`), which authorizes this tranche and its implementation together, and asks for this record. It is not a separate approval, and it decides nothing |
| Date | 2026-11-15 |
| Drafted by | Claude Code (`claude-opus-5-5`), for the BCO team |
| Tranche record | `src/05_ontology/tranche-2-description.yaml`, which `tools/ontology/formalize.py` verifies field by field before writing `src/05_ontology/apqc-cap-desc.ttl` |
| Standard | `docs/standards/stage-05-ontology.md`, §2, as it applies to information terms (its amendment history records this tranche) |

## 1. What is in the tranche

These are information content entity classes (K3, specification §6) and two annotation
properties. None of them is a capability type, so no G1-T record, realization index or
CAP-06 review applies (B-1: "G1-T is not applicable to them"). No class is under
`cco:ont00000568`, and none is linked to another BCO class.

| Class | Concept (`tools/vocab/build.py --digest`) | Parent: §4 row, decision | In the CCO extract |
|---|---|---|---|
| `bco:CapabilityMap` | `bcom:CapabilityMap` `d762f799e086…` | `cco:ont00000853` Descriptive ICE (§4) | yes |
| `bco:CapabilityAssessment` | `bcom:CapabilityAssessment` `b027d5a8891f…` | `cco:ont00000853` (§4) | yes |
| `bco:CapabilityMaturityRating` | `bcom:CapabilityMaturityRating` `591c5e0c298f…` | `cco:ont00001010` Ordinal Measurement ICE (§4) | yes |
| `bco:CapabilitySourcingStatement` | `bcom:CapabilitySourcingStatement` `4b9b70a16165…` | `cco:ont00000853` (§4) | yes |
| `bco:CapabilitySourcingAssessment` | `bcom:CapabilitySourcingAssessment` `460d4b1d480f…` | `cco:ont00000853` (§4) | yes |
| `bco:CapabilityTarget` | `bcom:CapabilityTarget` `b4945a8dee4e…` | `cco:ont00000476` Objective (§4) | yes |
| `bco:CapabilityTargetStateSpecification` | `bcom:CapabilityTargetStateSpecification` `d65c797315db…` | `cco:ont00000974` Plan (§4) | yes |
| `bco:AuthorizationRecord` | `bcom:AuthorizationRecord` `d2f3430f2fad…` | `cco:ont00000853` (§4, CD15) | yes |
| `bco:FunctionalAdequacyAssessment` | none: its §4 row has no IRI ("representation open"), so the vocabulary cannot hold a record for it (D4-no-row). Its label and definition are read from that row | `cco:ont00000853`, as B-1 decided | yes |

| Annotation property | Label (§5) | Use (§4, verbatim) |
|---|---|---|
| `bco:concernsType` | concerns type | Identifies the capability class or act class an ICE concerns (CD14) |
| `bco:assessedPresence` | assessed presence | Records the finding of every Capability Assessment (CD14) |

`formalize.py` checks each row against its sources:

- each concept's label and definition from the vocabulary build;
- the concept's record digest;
- that the concept designates this class (`bco:designatesClass`);
- the §4 definition and Parent cell, read from the specification at SHA-256
  `2224f869b0ec…`;
- the parent's declaration in the vendored CCO extract;
- for the adequacy assessment, the decision's wording;
- for the properties, §4's use and §5's label.

**Open source checks or errata:** none affects these terms. The three source checks of
`docs/catalog/tranche-2-followup.md` concern capability types (T2-02, T2-24, T2-31), not
information terms. **Taxonomy links:** none. Each class has its one CCO parent and nothing
else.

## 2. The Functional Adequacy Assessment: reuse check

B-1 asks for this check before the class is declared, against the pinned Extended Relation
Ontology and the relevant CCO domain ontology. Both were read whole, from CCO v2.0 at
`510dad7` (`CommonCoreOntologiesMerged.ttl`, SHA-256 `e609db27…`):

- **Extended Relation Ontology.** It declares 39 object properties and 22 annotation
  properties, and no class. Nothing in it can be the assessment.
- **Information Entity Ontology.** It declares 86 classes. Descriptive ICE
  (`cco:ont00000853`) has four direct subclasses: Measurement ICE, Measurement Unit,
  Predictive ICE and Reference System. None of them is an evaluative statement with
  findings.
- **Every CCO class whose label speaks of assessing, evaluating, appraising, auditing,
  reporting, reviewing or adequacy.**
  - Act of Appraisal (`cco:ont00000636`) is an act, a process, not an information entity.
  - Report (`cco:ont00000624`) is a Document, a material artifact that bears information,
    not the information itself.
  - Act of Reporting (`cco:ont00000151`) is an act.
- **BPO at the pin.** No class names an adequacy assessment or evaluation. Its
  description classes (`ex:InternalCapabilityData` and the others in §4) concern
  capabilities, not functions.

No existing class expresses the distinction, so `bco:FunctionalAdequacyAssessment` is
declared, under `cco:ont00000853` as decided. It is not under `bco:CapabilityAssessment`,
and a test holds that.

## 3. Upstream terms the tranche and its shapes use

Every CCO and BFO IRI below is declared in the vendored extract after
`tools/ontology/vendor_upstream.py --rebuild`. Before this tranche the seeding read
`prefix:local` names in shape SPARQL, which brought in the new ones.

- `cco:ont00001982` describes and `cco:ont00001808` is about.
- `cco:ont00001811` is a ordinal measurement of.
- `cco:ont00001910` permits, `cco:ont00000751` Action Permission and
  `cco:ont00000228` Planned Act.
- `cco:ont00001739` ordinal measurement annotation, never used on a rating.
- `cco:ont00000253` Information Bearing Entity, the domain of CCO's value properties.
- The agent classes `cco:ont00001017`, `cco:ont00001262`, `cco:ont00000300` and
  `cco:ont00001180`.
- `obo:BFO_0000178` has continuant part and `obo:BFO_0000015` process.

BPO's `ex:designatesProcessType` is declared `owl:AnnotationProperty` in
`ontology/apqc-catalog.ttl` at the pin `bc64e91`, and only that declaration enters the
extract (B-3). No catalog node and no APQC text enters it.

The Dublin Core and schema.org terms are the ones the specification itself chose (§4,
"Reused without change"; §5). The two schema.org terms the encodings below add were read at
schema.org:

- `schema:ratingValue`: "The rating for the content", domainIncludes Rating, rangeIncludes
  Number and Text.
- `schema:reviewAspect`: "This Review or Rating is relevant to this part or facet of the
  itemReviewed", domainIncludes Guide, Rating and Review, rangeIncludes Text.

schema.org's domainIncludes entails no type, so neither puts the subject under a
schema.org class. Both encodings were confirmed on 2026-11-16
(`docs/decisions/2026-11-16-stage05-completion-accepted.md`) as RDF/SHACL encoding conventions:
a rating stays a CCO Ordinal Measurement Information Content Entity and a finding a
Descriptive Information Content Entity, neither a Schema.org Rating or Review, and no
equivalence is asserted.

## 4. Encodings chosen at Stage 05 (no term minted)

| Requirement | Encoding | Why |
|---|---|---|
| CAP-20, the rating's ordinal value (R5-02: "encoding chosen at Stage 05") | `schema:ratingValue`, exactly one | CCO's value properties all have the domain Information Bearing Entity, which a rating is not (CAP-20 forbids them), and `cco:ont00001739` is reserved for the measured entity |
| CAP-33, the adequacy assessment's three findings (CD17: "representation open") | Each finding is a continuant part (`obo:BFO_0000178`) of the assessment, typed `cco:ont00000853`. The dimension is `schema:reviewAspect`: "integration and coordination", "operational availability" or "adequacy for the function". The finding is `schema:ratingValue`: "met", "partly met" or "not met". Each also has `dct:conformsTo`, `dct:source` and `dct:date`. The assessment describes its Organization and is about its standing function's catalog concept (a `skos:Concept`, CD16's key) | B-1: "using verified existing properties and SHACL constraints. Do not invent object properties". Parthood is the relation §5 already uses for maps and plans |
| CAP-34, the performance witness | `cco:ont00001833` has agent / `cco:ont00001787` agent in | Confirmed by the architect (N-4) |

These are for the architect to confirm or change, as CAP-34's was. A change would edit the
shapes and fixtures, not the module.
