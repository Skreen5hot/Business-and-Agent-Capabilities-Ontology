# Decision record — bulk capability synthesis directed; I-4 authorized and expanded, 2026-11-03

Recorded verbatim by Claude Code (`claude-opus-5-5`) on 2026-11-03, from the direction the
product owner and architect, Aaron Damiano, gave in session. The acts are the architect's.

**What it is about:** Phase I-4 of the Capability Term Inventory (crosswalk, deduplication
and triage), scoped by the approval of 2026-10-27
(`docs/decisions/2026-10-27-capability-inventory-scope-approved.md`) and not authorized
until now, and the source inventories it reads, on main at
`ee48c61` (SHA-256 of each file):

| Inventory | SHA-256 |
| --- | --- |
| `docs/sources/inventory/bpo-entries.yaml` (I-1) | `96fd4631c9d5f01a20c6064919ea5b5a9b690ed9ee7344977d1ca8c4425edb42` |
| `docs/sources/inventory/pcf-7.4-entries.yaml` (I-2b) | `0f91b5f08fa3f6a0ec87bc4afe08190654ef88eb8ddbeea20fe6f54c19579f64` |
| `docs/sources/inventory/feaf-brm-entries.yaml` (I-2c) | `3cb7ef37439c7fd3623be8f36075aafa6d93d0746e252e682de83b59dae620e4` |
| `docs/sources/inventory/fibf-entries.yaml` (I-2c) | `cc7c80b1957c3ce5eb5cd96e877ff64422ae18c3ede327c3e562f22bc8297eff` |
| `docs/sources/inventory/fibf-business-capabilities.yaml` (I-2c) | `0dcc107f3b4cfaf8236e6e757a4be27fa0efb1c2ee66a10cb86ff8db7d082b1a` |

and CM-01 as approved (`src/02_conceptual_models/CM-01-business-capability.md`, SHA-256
`292c8f36d64075b9663e159985a15b448aa933c3b5ed4baff3b2a556ca861ccc`).

## The direction

````text
Subject: Immediate Product Owner Course Correction — Bulk Capability Development
We are changing development priorities immediately.
The objective of the Business and Agent Capabilities Ontology is to develop a comprehensive, BFO/CCO-aligned capability ontology from our source material.
We are not copying APQC process names as capabilities. We are also not limiting the project to a handful of capability classes.
Our repository already contains thousands of source records. We have completed substantial source harvesting but have not performed the comprehensive capability synthesis that should follow it.
I am directing you to prioritize this work now.
1. Begin bulk capability synthesis
I authorize the I-4 crosswalk and triage work, expanded explicitly to include systematic derivation of candidate Business Capability types from all available, permitted source evidence.
Process the full existing source inventories, not just a small demonstration sample.
Use BPO’s Organization Capability classes, BPO act types, APQC process evidence, FIBF, FEAF BRM, and other authorized source evidence.
Do not assume a one-to-one correspondence between processes and capabilities.
2. Produce an original Candidate Capability Catalog
For each proposed capability, record:

* Candidate name and unique provisional inventory identifier.
* Original genus–differentia definition.
* Proposed organizational bearer and distinctive ability.
* Source identifiers and provenance.
* Supporting BPO act types or other realization evidence.
* Proposed broader and narrower capability relationships.
* Overlapping candidates, duplicates and synonyms.
* Preliminary classification as capability, process, skill, function, role, requirement, or unresolved.
* Review status and justification.

Candidate identifiers must not become ontology IRIs until formally admitted.
3. Automate the work
Develop the extraction, candidate-generation, normalization, crosswalk and preliminary classification workflow to handle thousands of source records.
Use bulk generation and automated consistency checks, followed by systematic quality review and exception handling.
Do not require individual product-owner approval for every draft candidate.
Preserve all source evidence independently. Do not automatically generate OWL classes, object properties or subclass axioms.
4. Make scale and coverage measurable
Report:

* Total source records processed, by source.
* Candidate capabilities generated.
* Unique candidates after deduplication.
* Candidates classified as likely BFO/CCO-compatible capabilities.
* Candidates rejected or deferred, with reasons.
* Source records lacking a proposed capability interpretation.
* Relationships and supporting realization evidence identified.

These counts must come from generated artifacts.
I expect substantial candidate coverage across the source material. Do not invent or inflate capability classes merely to meet a numerical target.
5. Change the immediate deliverable
The next substantial deliverable is the complete initial Candidate Capability Catalog and its traceable crosswalk.
Pause nonblocking specification refinements and new governance work that do not directly contribute to this deliverable.
The existing CM-01 architecture, DP-1, DP-2, licensing decisions and BFO/CCO requirements remain authoritative.
Formal type admission and ontology axiomatization follow the established gates, but preliminary candidate development should be performed at scale.
Do not respond with another roadmap or an extended proposal. Implement the bulk synthesis and present the resulting catalog, counts and quality findings for review.
The goal is to move from thousands of source records to a comprehensive, genuinely developed Business Capability taxonomy and ontology.
````

## The acts it contains

1. **I-4 is authorized**, expanded to the systematic derivation of candidate Business
   Capability types from all available, permitted source evidence, over the full
   inventories.
2. **The deliverable** is the initial Candidate Capability Catalog and its traceable
   crosswalk, with the nine fields per candidate and the seven counts the direction lists,
   the counts taken from generated artifacts.
3. **Draft candidates need no individual approval.** Formal type admission (G1-T) and
   axiomatization still follow the established gates.
4. **Priority:** nonblocking specification refinements and new governance work that do not
   contribute to the deliverable are paused.

## What stays as it was

- CM-01, DP-1, DP-2, the licensing decisions (APQC's notice on every PCF-bearing file;
  the FIBF text withheld under the closure decision of 2026-10-30) and the BFO/CCO
  requirements remain authoritative.
- Scope approval amendment 4: no inventory operation mints an ontology IRI or generates a
  class, object property, subclass axiom or ratification act. Candidate identifiers are
  not IRIs.
- Amendment 2: every source entry is kept independently; groupings are hypotheses for
  review. The inventories are read, never edited.
- I-3 (restricted catalogs) and I-5 (a tranche recommendation for separate approval) are
  not authorized by this direction. E4 (written standing-function judgements) is not
  performed by it: the catalog's classifications are preliminary.

## What it does not do

It admits, ratifies or mints nothing. It does not change the specification, the roadmap's
gates or CP-0.
