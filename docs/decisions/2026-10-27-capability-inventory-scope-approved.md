# Decision record — Capability Term Inventory: scope approved with amendments; Phase I-1 authorized, 2026-10-27

Recorded verbatim by Claude Code (`claude-opus-5-5`) on 2026-10-27, at the statement the
product owner and architect, Aaron Damiano, made in session. The act is his.

**What it is about:** the scope proposal for a Capability Term Inventory, which the agent
put to the architect in session on 2026-10-27. It set out source tiers A to C, the depth per
source, licence handling, the output format, phases I-1 to I-5, and decisions D1 to D6.
The proposal was made in conversation and is not a file in the repository; the decision
below states the parts it approves and amends.

---

````text
Subject: Architect Decision — Capability Term Inventory Scope Proposal
I approve the Capability Term Inventory scope proposal, subject to the amendments below.
This approval authorizes Phase I-1, the BPO harvest, and establishes the approved scope for subsequent phases. Each later phase remains subject to its own PR review.
Decisions D1–D6
D1 — Approved. Harvest from the current BPO `main` HEAD resolved to an immutable commit SHA. Record that commit, compare it against the existing pinned baseline, and keep BPO dependency re-pinning as a separate decision.
D2 — Approved. Use APQC PCF 7.4 as the primary edition, with an 8.0 delta, subject to edition-specific licensing checks.
D3 — Approved. Restricted catalogs are citation-only. Do not reproduce their capability names, definitions or other protected catalog content in the repository without established permission.
D4 — Approved: exclude defence catalogs. Do not include JCA or NAF in this inventory phase.
D5 — Approved with qualification. Harvest PCF levels 1–2 and level-3 nodes independently verified as standing functions. Do not classify an item as a capability solely from its label or hierarchy level.
D6 — Approved. Establish `docs/sources/inventory/` as the source-evidence location. This does not make its contents part of the approved vocabulary.
Required amendments

1. FIBF coverage: Include actual FIBF Business Capability entries, separately from federal functions and activities, while retaining their source-defined meanings.
2. Provenance: Retain every source entry independently with its identifier, hierarchy, version, locator and rights status. Crosswalk groupings are hypotheses requiring review, not declarations of equivalent capability types.
3. Licensing: Record the applicable license evidence and attribution obligations per source and edition. Do not presume that BPO's MIT license overrides upstream APQC conditions.
4. Admission boundary: Inventory triage is not G1-T type admission. No inventory operation may mint ontology IRIs or generate ontology classes, object properties, subclass axioms or vocabulary ratification acts.

Implementation direction
Proceed with I-1 — BPO harvest as a separate pull request.
Recalculate the BPO capability class count, capability-scope entry count, Q-12 violations and Q-13 shared-class inconsistencies from the selected commit. Do not treat previously reported counts as fixed.
Maintain the approved separation between Stage 01 source evidence, Stage 03 taxonomy development, and Stage 05 ontology formalization.
Later phases must remain separately reviewable and cannot introduce vocabulary concepts without the established proposal and approval process.
Record this decision in `docs/decisions/`, preserving the decisions and amendments above.
Approval applies to the inventory scope and Phase I-1 authorization, not to automatic admission of any candidate capability type.
````

---

## Effect

- **Phase I-1 is authorized** as its own pull request: harvest BPO at its `main` HEAD
  resolved to a commit, record that commit, compare against the pinned baseline, and
  recalculate the capability class count, the capability-scope entry count, the Q-12
  violations and the Q-13 inconsistencies from that commit.
- **Phases I-2 to I-5 are scoped, not authorized.** Each comes as its own pull request for
  review.
- **Approved scope, as amended:**
  - Sources: BPO (tier A). FEAF-II BRM and FIBF (tier B), with actual FIBF Business
    Capability entries kept separate from federal functions and activities, in their
    source-defined meanings (amendment 1). APQC PCF 7.4 levels 1–2, plus level-3 nodes
    independently verified as standing functions, with an 8.0 delta (tier B′; D2, D5).
    Restricted catalogs as citations only (tier C; D3).
  - Excluded: defence catalogs (JCA, NAF; D4); metamodel standards and process-capability
    ratings.
  - Every source entry is kept independently, with its identifier, hierarchy, version,
    locator and rights status. Crosswalk groupings are hypotheses for review (amendment 2).
  - Licence evidence and attribution obligations are recorded per source and edition, and
    BPO's MIT licence is not presumed to override APQC's conditions (amendment 3).
- **Boundaries:**
  - `docs/sources/inventory/` holds source evidence and is not approved vocabulary (D6).
  - Triage is not G1-T admission. No inventory operation mints ontology IRIs or generates
    classes, object properties, subclass axioms or ratification acts (amendment 4).
  - Stage 01 source evidence, Stage 03 taxonomy and Stage 05 formalization stay separate.
  - No vocabulary concept enters except through the established proposal and approval
    process.

## Noted when the BPO commit was resolved

BPO `main` resolved to `bc64e91839378e1926189c01bf184d6a22d5c1b7` (v0.4.1), six commits past
the pinned baseline `66131945b525c54f44e4962f32bb1f52dfa0cd12`. Between them, BPO v0.4.0
(`327ea2c`) moved every BPO IRI from `http://example.org/apqc#` to
`https://fandaws.com/ontology/bpo#`, and v0.4.1 (`dda9fa5`) renamed the prefix label `ex:`
to `bpo:` with no IRI change. BPO announced both in two notices to the BCO, filed in the same
pull request as this record (`communications/bpo/incoming/2026-10-23-namespace-v0-4-0.md` and
`…/2026-10-23-prefix-v0-4-1.md`). The I-1 harvest therefore records BPO's new IRIs and
compares against the baseline under the mapping BPO gave. Re-pinning stays a separate
decision under D1.

## What this does not do

- It does not admit, ratify or mint any capability type, concept or IRI.
- It does not re-pin BPO or change the vendored extract.
- It does not authorize phases I-2 to I-5, which each come for their own review.
