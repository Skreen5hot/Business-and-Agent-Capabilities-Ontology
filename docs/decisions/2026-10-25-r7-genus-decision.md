# Decision record — R7 Finding E: catalog genus recorded as immediate parent plus foundational ancestor, 2026-10-25

Recorded verbatim by the setup agent (Claude Code, `claude-opus-5-5`) on 2026-10-25, at the
statement the product owner and architect, Aaron Damiano, made in session. The act is his.

---

````text
1. Record both: the immediate genus as bco:BusinessCapability, the class the metamodel concept already designates, and the CCO class as the foundational ancestor, in a separate annotation. This matches the text and claims nothing new.

Proceed
````

---

## What it answers

Review R7 (`reviews/R7-turtle-artifact-review.md`), Finding E. All five catalog definitions
name the genus "a business capability", but the generated `bco:definitionGenus` pointed at
`cco:ont00000568` (Organization Capability), because `bco:BusinessCapability` is not minted.
The reviewer asked that the five references not be changed silently, so this is the
architect's decision on how to change them.

The agent offered two options. The architect chose option 1, quoted above. Option 2 was to
keep CCO as the genus and reword the definitions to "an organization capability…".

## Effect

- Each catalog concept records **two** annotations:
  - `bco:definitionGenus`, the **immediate** genus: `bco:BusinessCapability`, the class
    `bcom:BusinessCapability` already designates with `bco:designatesClass`;
  - a separate annotation, the **foundational ancestor**: `cco:ont00000568`.
- **This claims nothing new.** `bco:BusinessCapability` stays unminted. No OWL class,
  subclass axiom or object property is asserted. The annotations record the intended
  hierarchy as the definitions' text already states it.
- **"Proceed"** clears the rest of the R7 response the agent proposed:
  - claim-level provenance in the export (Finding A);
  - published prior-record nodes, with the history documented (B);
  - comments on `bco:PCFCode` and `bco:lifecycleStatus` (F, G);
  - the five catalog wording refinements, as editorial revisions keeping the same IRIs;
  - filing R7 with a disposition that defers C and D to the OWL layer;
  - correcting CLAUDE.md's statement that the vocabulary has no concepts.

## What this does not do

No concept is ratified; all 14 remain Draft. RP-1, RP-10 and the OWL layer (R7 C and D) are
not decided here.
