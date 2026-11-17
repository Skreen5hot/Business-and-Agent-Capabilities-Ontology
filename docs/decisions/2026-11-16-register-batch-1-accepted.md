# Decision record — Coverage register batch 1 accepted; RD-1 decided (Payroll Processing keyed to PCF_10732), 2026-11-16

Recorded verbatim by Claude Code (`claude-opus-5-5`) on 2026-11-16, from the decision the
architect, Aaron Damiano, Product Owner and Ontology Architect, gave in session on PR #59
(`stage06/register-1` at `9fe5342`). The acts are the architect's. This record makes none.

## What it is about

`stage06/register-1` at `9fe5342e` (PR #59, before this record):

| Record | SHA-256 at `9fe5342` |
| --- | --- |
| `src/06_knowledge_graph/coverage-register.json` (batch 1 as proposed: 4 functions, 20 waiting) | `afd21125091ff40bf1d389d490de835a18d779ce4ed2d2135f3ee4af6849f0a6` |
| `src/06_knowledge_graph/register-batch-1-review.md` (the synthetic domain review, with RD-1) | `59101c24292621d838abdd721aee76207c6c25269f66c7de4144835699d4cc68` |
| `src/06_knowledge_graph/scope-audit.yaml` (the 41-entry audit) | `763bf1ac77b0b438b4bc494c9ff35bf5581e2ef285a3ff002b9c0ceed95d4b00` |
| `src/06_knowledge_graph/bc-migration.yaml` (the `bc:` migration manifest) | `372a53330e03cb8de326bd2068aa833437aa9d862692440cd0c637d4a8b992ae` |
| `src/06_knowledge_graph/upstream-conformance.json` (the S06-U2 record) | `9b98dfcd5dc74c07302a1a00e58f76bae48cb1f7dd255638bb475c756fc97434` |

## The question put

> Accept register batch 1, keying Payroll Processing to PCF_10732?

RD-1's options, as the review states them: (a) key Payroll Processing to `PCF_10732`, with
`bco:PayrollProcessing` as its whole-function class and Pay Management and Payroll Tax
Processing as its components; (b) key it to `PCF_10497`; (c) leave it waiting.

## The decision

> Accept, key 10732

## What this record reads it as

- **Batch 1 is accepted as one batch**, under direction D of the decision of 2026-11-16
  (`docs/decisions/2026-11-16-stage06-standard-and-first-increment.md`), with the review's
  substantive findings 3 and 4 applied as they were at `9fe5342`.
- **RD-1 is decided as option (a).** Payroll Processing (`BCC-d95f68fd`) is keyed to
  `https://fandaws.com/ontology/bpo#PCF_10732`. Its concept still cites both 10497 and 10732;
  the register records the choice and both cited elements, and nothing about 10497 is
  asserted or withdrawn.

## What it does not decide

- No other key choice. The generator applies a recorded choice only to the grouping it names
  and only among the elements its concept cites.
- Nothing in the ontology: no triple, class or subclass link is written.
- Not the FIBF rights-document drift, which stays open for the architect's review.
- Not CP-3's closure, nor Stage 06 completion, which needs a real, authorized organization
  evidence graph (decision of 2026-11-16, H).

## Applied by

- `tools/kg/register.py`: `KEY_CHOICES` names `BCC-d95f68fd` → `10732`, citing this record;
  the register's `status` cites this record.
- `config/coverage-register.schema.json`: an optional `key_choice` on a function.
- `src/06_knowledge_graph/coverage-register.json`, regenerated: 5 functions, 19 waiting.
