# Coverage register, batch 1: synthetic domain review

| Field | Value |
|---|---|
| Batch | `src/06_knowledge_graph/coverage-register.json`, batch 1 as reviewed: 4 functions, 20 groupings waiting (5 and 19 after RD-1) |
| Authority | The decision of 2026-11-16, D (`docs/decisions/2026-11-16-stage06-standard-and-first-increment.md`): one batch, a separate synthetic domain review, and only substantive disputes escalated with the batch |
| Reviewer | A synthetic domain practitioner (finance, accounting, tax and payroll operations), `claude-opus-5-5`: an independent agent instance given the files only and working read-only, as product-owner-authorized synthetic practitioner validation (`docs/decisions/2026-11-02-r11-practitioner-validation-decided.md`). It does not decide anything |
| Drafting | Claude Code (`claude-opus-5-5`), the Ontologist |
| Date | 2026-11-16 |
| Status | Batch accepted by the architect on 2026-11-16, and RD-1 decided as option (a) (`docs/decisions/2026-11-16-register-batch-1-accepted.md`) |

## What the reviewer was given

- **The batch:** the register.
- **The definitions:** the catalog definitions of each concept it names.
- **The source links:** the Stage 03 review links it was drawn from (`docs/catalog/tranche-2-review.yaml`).
- **The keys:** the PCF inventory (`docs/sources/inventory/pcf-7.4-entries.yaml`), to check each key against its concept.

The reviewer was not given the Ontologist's reasoning. It was asked, for each function:

- whether the key is right;
- whether each component is genuinely a component;
- whether a necessary component is missing;
- whether the whole-function entries are sound.

It was also asked whether any waiting reason looked wrong.

## Findings and dispositions

| # | Function | Finding (summarized) | Kind | Disposition |
|---|---|---|---|---|
| 1 | `PCF_10730`, Financial Accounting | The key is right. The four components match the four children of the node, and each kept link's reason matches the parent definition. Consolidation, intercompany, revenue recognition and lease accounting have no concept: a catalog gap, not a register omission | Minor | No change. The gap is recorded here for a later curation tranche |
| 2 | `PCF_10736`, Tax Management | The key is right. Payroll Tax Processing comes from outside the node's PCF subtree, though it is a genuine component by the definition and the kept link. A join on the PCF hierarchy alone would miss it. Tax audit and dispute work, and the tax on payables, have no concept | Minor | **Applied.** The generator now writes a note on any component whose PCF element is outside the key's subtree. The gaps are recorded here |
| 3 | `PCF_10756`, Accounts Payable Processing | The key and the one component are right. But the function's other work (invoice verification and matching, exceptions, accruals, inquiries) sits in the whole-function class's own index, not in any component. Read as a full breakdown, the list understates the function | **Substantive** | **Applied.** Every entry with a whole-function class now carries the note "Not a complete breakdown: the function's work outside the listed components belongs to the whole-function class itself". Payment approval (a rejected candidate) and the tax on payables are recorded as catalog gaps |
| 4 | `PCF_10754`, Pay Management | The same single-component issue. The part-of claim is consistent with the indexes. Time Reporting is rightly excluded, since its link was rejected as a dependency | **Substantive** | **Applied**, by the same note as finding 3 |
| 5 | Both single-component functions | Payment Processing is shared by Accounts Payable and Pay Management. That is sound as a type. Operationally, though, payroll disbursement differs from paying suppliers | Minor | **Applied.** The generator now notes every shared component, saying that a shared type does not imply one arrangement serves both functions |
| 6 | Payroll Processing (`BCC-d95f68fd`), waiting | It waits only because its concept cites two PCF elements, 10497 (under human resources) and 10732 (under financial resources), so it has no single key. Otherwise it is complete: the class is written and both components are written and kept. For a finance register, 10732 is the natural key | **Substantive** | **Escalated as RD-1.** Choosing a key between two cited elements is a semantic choice, not something the generator's rule should make. It stays waiting until decided |
| 7 | The other 19 waiting groupings | Spot-checked; each reason holds. None should clearly be in the batch, and none of the four functions should be out | Minor | No change |

The reviewer's overall judgment: **accept with the substantive findings applied.** Findings 3 and 4 are applied. Finding 6 is RD-1.

## Disputes for the architect

**RD-1: Payroll Processing's key.**
- **The issue:** its concept cites PCF 7.4 elements 10497 and 10732. The batch's rule requires exactly one, so the grouping waits.
- **Options:**
  - (a) key it to `PCF_10732`, with `bco:PayrollProcessing` as its whole-function class and Pay Management and Payroll Tax Processing as its components;
  - (b) key it to `PCF_10497`;
  - (c) leave it waiting.
- **Recommendation:** (a), as the reviewer suggests. The register is drawn from the financial-resources tranche, and the 10497 placement is the one Stage 03 kept outside the tranche.
- **What changes:** either (a) or (b) adds a key choice to the generator's inputs. Nothing in the ontology changes.
- **Decided:** option (a), on 2026-11-16 (`docs/decisions/2026-11-16-register-batch-1-accepted.md`). The generator's `KEY_CHOICES` keys `BCC-d95f68fd` to `PCF_10732`, and the register records both cited elements.

## Catalog gaps the review recorded

These are not register defects. Each is a candidate for a later curation tranche:

- consolidation and intercompany accounting;
- revenue recognition and lease accounting;
- tax audit and dispute work;
- the tax on payables;
- payment approval (a candidate rejected at Stage 03).
