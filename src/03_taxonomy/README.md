# Stage 03 — Taxonomy

**Status:** not started. Nothing is here yet.

The architect's layout describes this stage as a comprehensive collection of terms
(`docs/decisions/2026-10-25-stage-02-choices.md`). Standard: not yet supplied.

## Where the evidence for it is

The Capability Term Inventory, in `docs/sources/inventory/` (its README lists the phases
and their state), records what other catalogs say a capability is, entry by entry with
its source. It is **source evidence, not taxonomy**: the inventory's scope approval keeps
"Stage 01 source evidence, Stage 03 taxonomy development, and Stage 05 ontology
formalization" separate (`docs/decisions/2026-10-27-capability-inventory-scope-approved.md`),
and no inventory entry is a term of this stage until a later decision admits it.

Of the inventory's later phases, I-3 (restricted catalogs) is not authorized. I-4
(crosswalk and triage, expanded to candidate derivation) was authorized on 2026-11-03 and
closed on 2026-11-07 (`docs/decisions/2026-11-07-adr002-accepted-cp0-complete.md`, act 3); its catalog is `docs/catalog/`. I-5's first
tranche was directed on 2026-11-03 and its three G1-T records signed PASS on 2026-11-05
(`docs/catalog/tranche-1.md`). The catalog's broader links are proposals, not taxonomy.
Taxonomy development here waits for its own authorization and its standard.

*Since 2026-11-07:* semantic-curation tranche 2 (`docs/decisions/2026-11-07-curation-tranche-2-approved.md`) classified
every proposed link of PCF 9.0's subtree as specialization, component or incorrect
(`docs/catalog/tranche-2-review.yaml`). Its standard is proposed
(`docs/proposals/2026-11-07-stage-03-taxonomy-standard.md`); until it is approved the
links are classified, not validated.

*Since 2026-11-07, later:* the standard's rules were approved
(`docs/decisions/2026-11-07-tranche-2-accepted-g1t-preparation-authorized.md`, A2), and its
text, aligned with them, is submitted for ratification. The review record now uses its
terms: `kind-of`, `part-of`, and the dispositions retained, incorrect and unresolved.
