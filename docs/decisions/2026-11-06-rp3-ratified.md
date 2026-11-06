# Decision record — RP-3 ratified, 2026-11-06

Recorded verbatim by Claude Code (`claude-opus-5-5`) on 2026-11-06, from the decision the
architect, Aaron Damiano, gave in session. The act is the architect's.

## What it is about

| Field | Value |
| --- | --- |
| Item | RP-3, enablement relations (CD12), in `specifications/Business-Capability-Ontology-v0.5.0-draft.3.md` at `c3f1ba2`, SHA-256 `2224f869b0ec7a1e31b0afc1c2b403ad222ea290c334bff48a93ebbb6516c574` (accepted for ratification 2026-11-04) |
| Check decided on | `docs/proposals/2026-11-06-rp3-faithfulness-check.md` at `a4ba28a`, SHA-256 `90aadc4b87522506d017636f0a0746e818dfe1c914874a98e1fb1bf89d50cbcd` |
| BPO checked at | `bc64e91839378e1926189c01bf184d6a22d5c1b7`, the inventory and vendoring pin |
| CP-0 item | 7 of `docs/proposals/2026-11-05-cp0-closure-matrix.md`, decision 2; and OI-6 |

## The decision

````text
**Subject: Architect Decision — RP-3 Ratification**

**Decision: RP-3 RATIFIED, with one technical clarification.**

I approve CD12 of specification v0.5.0-draft.3 as the binding BCO treatment of the BPO enablement relations.

**1. `bpo:enablesProcess` — Approved**

Reuse the existing BPO annotation property as the realization index.

Its meaning in BCO is that acts of the indexed type are admissible realizations of the capability type.

It does not assert actual realization, causal enablement, exhaustiveness or a requirement that every act instance have a particular capability bearer.

**2. `bpo:requiresCapability` — Withdrawn from BCO**

BCO must not generate, assert or rely on this property as a prerequisite for performing an act.

Its intended interpretation is inappropriate for BCO's organizational capability model, especially in individual-performance and outsourced-performance cases.

Clarification: the BPO object-property declaration alone does not entail a universal capability-possession requirement. The rejection concerns the intended prerequisite semantics, not a claim that the declaration is intrinsically inconsistent in OWL.

This decision does not alter the upstream BPO ontology.

**3. Import boundary**

BCO must exclude BPO modules containing the unwanted `requiresCapability` assertions from its effective ontology graph.

Verify both direct and transitive imports, as well as assembled graphs, so the excluded statements cannot enter indirectly.

Continue reusing permitted BPO act types and realization-index evidence.

Record the import boundary in the implementation configuration. No upstream BPO modification is required for RP-3.

**4. OI-6 and CP-0**

The declarations have been located and checked against pinned BPO commit `bc64e91839378e1926189c01bf184d6a22d5c1b7`.

Close OI-6 insofar as it concerns locating and identifying the declarations.

Record RP-3 as ratified and close CP-0 decision item 2.

Any implementation checks of the import boundary belong to Stage 05 validation; they do not require another RP-3 architectural review.

**5. Scope**

No new ontology classes, object properties or axioms are authorized.

Do not open a separate BPO cleanup project as a condition of proceeding.

**Final disposition: RP-3 ratified. Continue with the remaining CP-0 work and capability development.**
````

## The acts it contains

1. **RP-3 is ratified.** CD12 of draft.3 is the binding BCO treatment of BPO's enablement
   relations.
2. **`bpo:enablesProcess` is reused as the realization index.** In BCO it means that acts of
   the indexed type are admissible realizations of the capability type. It asserts no
   actual realization, no causal enablement, no exhaustiveness, and no requirement that
   every act have a particular bearer.
3. **`bpo:requiresCapability` is withdrawn from BCO.** BCO does not generate, assert or rely
   on it. The clarification is part of the act: the rejection is of its intended
   prerequisite reading, not a claim that BPO's object-property declaration is
   inconsistent in OWL or entails a universal requirement. The check's §3 and §4 said
   BPO's comment "states" that reading; the clarification governs.
4. **The import boundary.** BPO modules carrying `requiresCapability` assertions are kept
   out of BCO's effective ontology graph, directly, transitively and in assembled graphs.
   Permitted BPO act types and realization-index evidence continue to be reused.
5. **OI-6 is closed** as far as locating and identifying the declarations goes.
6. **CP-0 item 7 (decision 2) is closed.**
7. **Scope.** No class, object property or axiom is authorized. BPO is not changed, and no
   BPO clean-up is a condition of going on. Implementation checks of the boundary belong to
   Stage 05 validation and need no further RP-3 review.

## How it was carried out

- **The import boundary is recorded in configuration**, on BPO's entry in
  `config/upstream-sources.yaml`, as `excluded_modules`:
  - `ontology/capabilities_wiring.ttl`, with 356 `requiresCapability` triples;
  - `ontology/delivery_processes.ttl`, with 5.

  `ontology/capabilities_roles.ttl` carries the declaration but no assertion. It is not on
  the list, so its `enablesProcess` declaration stays available for CAP-03's gate B check.
  No tool reads the key yet; enforcing it is Stage 05's.
- **The boundary was measured as it stands on 2026-11-06:**
  - No tracked RDF file in the repository contains `requiresCapability`.
  - No authored, vocabulary or vendored file carries an `owl:imports`. The only ones are
    in `drafts/`, which is never loaded.
  - The vendored BPO source, `apqc-ext.ttl` at the pin, imports nothing. Its one
    `owl:imports` line is commented out.
  - The validation data graph is assembled from the layout's declared files. Its only BPO
    content is the vendored extract of `apqc-ext.ttl`; neither excluded module is among them.
  - The inventory harvest reads all three modules, as source evidence: the
    `enablesProcess` triples are realization-index evidence. It writes YAML records, not
    ontology, and none of them is in the data graph.
- **Status lines** are updated:
  - `CLAUDE.md`, `docs/DEVELOPMENT.md` and `docs/HANDOFF.md`;
  - the roadmap's D4 row, its state row and its amendment log;
  - the status lines of the check and of the CP-0 closure matrix.

  Each proposal's body is unchanged. The specification is not edited; its §10 and OI-6
  wait for the next reviewed version.

## What it does not do

- It ratifies no other register item. RP-4 and RP-6 to RP-9 stay drafts, and RP-5 is open.
- It sends no message to BPO and changes nothing upstream.
- It mints and asserts nothing, and makes no G1-I claim. CP-0 stays open, and OWL still
  waits for all of CP-0 and D5.
