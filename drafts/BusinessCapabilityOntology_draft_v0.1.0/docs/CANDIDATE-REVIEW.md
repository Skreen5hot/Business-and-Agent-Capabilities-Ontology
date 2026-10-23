# Existing BPO capability migration review — not OWL assertions

**Source:** public `ontology/slices/apqc_1_0.ttl` at `main`, inspected 2026-10-22. The candidate links also appear as non-logical `rdfs:seeAlso` annotations in `alignment/bpo-review-links.ttl`.

| BPO class | Current superclass | Potential act anchor | Grounding / bearer questions | Draft migration decision |
|---|---|---|---|---|
| `ex:StrategicPlanningCapability` | `cco:ont00000568` Organization Capability | `ex:P17040` is a verified planning act, but may represent only part of the relevant recurring work | What organizational capacities support this capacity? Can planning be entirely delegated? Are the required members part of the bearer? | **HOLD**; no disposition subclass |
| `ex:BusinessModelGovernanceCapability` | `cco:ont00000568` Organization Capability | No realization act type approved here | Separate *establishing* a governance regime from *carrying out* governance reviews or decisions | **HOLD**; no disposition subclass |
| `ex:CustomerExperienceManagementCapability` | `cco:ont00000568` Organization Capability | No realization act type approved here | Distinguish external customer-experience platform/service from organizational internal capacity to oversee/interpret it | **HOLD**; no disposition subclass |
| `ex:CompetitiveAnalysisCapability` | `cco:ont00001379` Agent Capability with `BFO_0000054 some ex:P19945` | `ex:P19945` (Analyze competitors, PCF 19945) verified | Is its bearer a person with a Skill, an Organization with an Organization Capability, or a broader Agent? Does its present restriction accidentally require historical actual realization? | **HOLD**; review and possible split |

## Proposed curator evidence card

Create one evidence card per candidate before formal promotion:

1. **Existing capability class IRI:** exact BPO IRI, label, definition, current superclasses/restrictions.
2. **Proposed non-deontic act type IRI:** BPO reality-class IRI and definition; explain why the act is suitable as a potential realization, not just a capability-development act.
3. **Bearer:** named kind of CCO Organization and member boundary (not vendor network).
4. **Disposition basis:** explain material constitution/coordination, not simply a plan or contract.
5. **Dependency classification:** internal basis / external condition / outsourced performance / legal standing.
6. **Function:** classify independently if an artifact-function reading is defensible; do not infer from purposeful organizational design alone.
7. **Evidence:** tests, observed executions, member capacities, supplier facts, documented assumptions.
8. **Maturity and aspirations:** place assessments and desired states in the information layer; do not create grades as capability subtypes.
9. **Proposed axioms:** minimal changes, no existential `has realization` restriction unless modeling a genuinely necessarily-realized class (normally **not** appropriate for a disposition).
10. **Review outcome:** accept, reject, split, or defer, with explanation.

## Why the act index is not yet a machine-readable property

`ex:designatesProcessType` is already an annotation between APQC catalog nodes and BPO process/capability classes, not a general ontological relation expressing what a disposition can potentially realize. `BFO_0000054` only relates a disposition to an actual process, and thus cannot serve as a universal-to-universal potential index without incorrectly requiring an actual instance. A production indexing pattern must be chosen and vetted separately; no new object property has been created in the draft.
