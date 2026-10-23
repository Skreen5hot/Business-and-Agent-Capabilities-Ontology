# Source and IRI verification ledger — BCO v0.1.0 draft

**Audited:** 2026-10-22.  
**Source A:** user-supplied PDF renderings of OWL/Turtle sources: `BFO .pdf`, `Agent.pdf`, `Extended Relations Ontology.pdf`, `Information Entity Ontology.pdf`, `Event Ontology.pdf`. Label, asserted class parent, domain/range, and definitions were checked in the relevant source text.  
**Source B:** public GitHub `main` browser views of `Skreen5hot/BusinessProcessOntology`, inspected on this date. This is a **partial repository inspection**, not a complete local clone.  
**Critical caveat:** a parsed PDF's apparent textual completeness does not substitute for obtaining and reasoning over the actual merged OWL dependency closure.

## Verified external classes

| IRI (short form) | Label in supplied source | Asserted direct superclass / characterization | Source |
|---|---|---|---|
| `obo:BFO_0000016` | disposition | `BFO_0000017` realizable entity; disjoint with role | BFO 2020 |
| `obo:BFO_0000034` | function | `BFO_0000016` disposition | BFO 2020 |
| `obo:BFO_0000023` | role | `BFO_0000017` realizable entity; disjoint with disposition | BFO 2020 |
| `cco:ont00001379` | Agent Capability | `obo:BFO_0000017` realizable entity | Agent Ontology 2.0 |
| `cco:ont00000568` | Organization Capability | `cco:ont00001379`; equivalent to Agent Capability with some `capability of` Organization | Agent Ontology 2.0 |
| `cco:ont00000089` | Skill | `cco:ont00001379`; equivalent to Agent Capability with some `capability of` Person | Agent Ontology 2.0 |
| `cco:ont00001180` | Organization | `cco:ont00000300` Group of Agents | Agent Ontology 2.0 |
| `cco:ont00000300` | Group of Agents | `obo:BFO_0000027` object aggregate | Agent Ontology 2.0 |
| `cco:ont00001017` | Agent | `obo:BFO_0000040` material entity; equivalent to material entity bearing Agent Capability | Agent Ontology 2.0 |
| `cco:ont00000228` | Planned Act | `cco:ont00000005` Act | Event Ontology 2.0 |
| `cco:ont00000958` | Information Content Entity | `obo:BFO_0000031` GDC | Information Entity Ontology 2.0 |
| `cco:ont00000853` | Descriptive Information Content Entity | `cco:ont00000958` | Information Entity Ontology 2.0 |
| `cco:ont00000965` | Prescriptive Information Content Entity | `cco:ont00000958` | Information Entity Ontology 2.0 |
| `cco:ont00001163` | Measurement Information Content Entity | `cco:ont00000853` | Information Entity Ontology 2.0 |
| `cco:ont00001010` | Ordinal Measurement Information Content Entity | `cco:ont00001163` | Information Entity Ontology 2.0 |

### Important nuance

CCO Agent Capability's exact direct parent is **Realizable Entity**, *not* Disposition. The new `bc:BusinessCapability` makes the disposition assertion explicit. `Organization Capability` is itself a kind of `Agent Capability`; the two are not disjoint.

## Verified external object properties

| IRI | Label in supplied source | Domain | Range | Notes / source |
|---|---|---|---|---|
| `cco:ont00001954` | has capability | Agent | Agent Capability | subproperty of BFO bearer of; Agent Ontology |
| `cco:ont00001889` | capability of | Agent Capability | Agent | inverse of has capability; subproperty of BFO inheres in; Agent Ontology |
| `cco:ont00001898` | aggregate has capability | Group of Agents | Agent Capability | subproperty of `ont00001836`; Agent Ontology; **avoid for emergent capabilities** |
| `cco:ont00001836` | aggregate bearer of | Object Aggregate | SDC or GDC | definition includes every other member bearing a same-type dependent continuant; Extended Relations Ontology |
| `cco:ont00001956` | aggregate has disposition | Object Aggregate | Disposition | subproperty of `ont00001836`; Extended Relations Ontology; **avoid as default** |
| `obo:BFO_0000196` | bearer of | independent continuant, not spatial region | SDC | BFO 2020 |
| `obo:BFO_0000197` | inheres in | SDC | independent continuant, not spatial region | BFO 2020 |
| `obo:BFO_0000054` | has realization | Realizable Entity | Process | inverse of realizes; BFO 2020 |
| `obo:BFO_0000055` | realizes | Process | Realizable Entity | BFO 2020 |
| `cco:ont00001808` | is about | ICE | Entity | Information Entity Ontology |
| `cco:ont00001811` | is a ordinal measurement of | Ordinal Measurement ICE | (no explicit range in supplied block) | subproperty of is a measurement of, inverse of is measured by ordinal; Information Entity Ontology |
| `cco:ont00001942` | prescribes | Prescriptive ICE | (no explicit range in supplied block) | subproperty of is about; Information Entity Ontology |

**No object properties are created in any of the draft Turtle modules.** In particular, `rdfs:seeAlso` used in the alignment is a built-in annotation, not a new object relation.

## Verified BPO terms (GitHub 2026-10-22)

Public source: https://github.com/Skreen5hot/BusinessProcessOntology/blob/main/ontology/slices/apqc_1_0.ttl

Namespace explicitly printed in the slice: `@prefix ex: <http://example.org/apqc#> .`

| Full local term | Label | Observed superclass / condition | Draft treatment |
|---|---|---|---|
| `ex:StrategicPlanningCapability` | Strategic Planning Capability | `cco:ont00000568` | Candidate only; physical grounding review |
| `ex:BusinessModelGovernanceCapability` | Business Model Governance Capability | `cco:ont00000568` | Candidate only; distinguish formation from operation |
| `ex:CustomerExperienceManagementCapability` | Customer Experience Management Capability | `cco:ont00000568` | Candidate only; external resource and boundary review |
| `ex:CompetitiveAnalysisCapability` | Competitive Analysis Capability | `cco:ont00001379`; `has realization some ex:P19945` | Candidate only; determine if bearer is Person or Organization, remove unwanted latency restriction before migration |
| `ex:P19945` | Analyze competitors | `ex:ActOfAnalysis`; BPO PCF 19945 / 1.1.1.1 | Existing reviewed act class; *actual process instances* may provide realization evidence |
| `ex:ActOfAnalysis` | Act of Analysis | local BPO shared genus | Existing BPO; do not duplicate |

**BPO design rules:** accepted [ADR-001](https://github.com/Skreen5hot/BusinessProcessOntology/blob/main/docs/adr/ADR-001-category-and-upper-level-modeling.md) R4 bridges catalog concepts to reality classes using `ex:designatesProcessType` as an annotation; R6 allows standing-function categories to be classes under Organization Capability. Its README describes a catalog/reality split and pinned CCO 2.0 closure. At present this draft does not add any `ex:designatesProcessType` assertion or recast BPO's APQC curatorial structure as an ontology taxonomy.

### What has NOT been checked

- A complete clone of the live repository, particularly the `capabilities/` directory and all process slices.
- The complete machine-readable merged CCO 2.0 OWL closure.
- The public repository commit SHA (the inspection used the mutable `main` ref).
- Any additional realization restrictions hidden in BPO modules not inspected here.
- Reasoner consistency of the full CCO/BFO/BPO import closure.
- Full SHACL validation under the repository's existing harness.

The draft must not be described as *fully CCO/BFO validated* until those checks are done.
