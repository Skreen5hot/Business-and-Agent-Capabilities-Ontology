# Stage 06, first increment: bounded implementation proposal

| Field | Value |
|---|---|
| Status | **Approved with binding directions A to J** (`docs/decisions/2026-11-16-stage06-standard-and-first-increment.md`). The reviewed version is this file at `ed5780a`, SHA-256 `509a25c7…6687f`. This text is amended to match the directions. Section 6 records the decisions, and section 8 lists each place where the reviewed text conflicted with them. The register-first increment is authorized once this PR confirms the match. The second increment is not authorized |
| Date | 2026-11-16 |
| Drafted by | Claude Code (`claude-opus-5-5`), for the BCO team |
| Basis | The decision of 2026-11-16 (`docs/decisions/2026-11-16-stage05-completion-accepted.md`, 6) |

## 1. The increment

The first increment is **register and migration data only**:

- the CP-3 scope audit;
- a first coverage-register batch over the 39 written classes;
- the `bc:` migration manifest;
- the upstream checks, S06-U1 and S06-U2.

**No organization, person or evidence graph is written.** All of this rests on real sources
at their pins and needs no instance namespace. It works toward CP-3, which is necessary but
not sufficient for Stage 06 completion (standard §6).

## 2. Scope

| # | Artifact | Source, at its pin | Scope | Location |
|---|---|---|---|---|
| P1 | **CP-3 scope audit** | BPO `capabilities/capability_scope.json` at `bc64e91`, as harvested in `docs/sources/inventory/bpo-entries.yaml` (41 scope entries; 3 keys are not capability classes, per `bpo-findings.yaml`) | One row per entry. **What BPO declares**, as harvested, is kept apart from **what the BCO has independently accepted**: a written class with its tranche and G1-T records, a staged concept with its open check, person-borne (CM-02), or nothing accepted. The row's next step is BPO-side, a BCO tranche, or none. The audit admits nothing, reclassifies nothing, and creates no subclass assertion (K10) | `src/06_knowledge_graph/scope-audit.yaml` |
| P2 | **Coverage register, batch 1** | Function keys verified at the BPO pin; components from `src/05_ontology/apqc-cap.ttl` | Standing functions whose every component type is one of the 39 written classes. Candidates are drafted from the functional groupings the catalog already keeps. For example, `bcoc:FinancialPerformanceManagement` and `bcoc:CapitalPlanning` are groupings whose part-of narrowed types (`FinancialPerformanceAnalysis`, `CapitalInvestmentAppraisal`) are written. A grouping whose narrowed type is held back, such as `bcoc:CostManagement`, waits. Components are class IRIs only (K8) | `src/06_knowledge_graph/coverage-register.json`, schema `config/coverage-register.schema.json` |
| P3 | **`bc:` migration manifest** | The seven v0.1 classes in `drafts/BusinessCapabilityOntology_draft_v0.1.0/`, read under its checksums and never loaded as ontology; specification §9.1 | One row per v0.1 class: the old IRI; the identifier migration (to a written `bco:` class, or *not carried*); the semantic relation, stated separately and never an equivalence; the decision; and the definition change | `src/06_knowledge_graph/bc-migration.yaml` |
| P4 | **Upstream checks** | `config/upstream-sources.yaml` | S06-U1: the refetch job runs in an auditable CI workflow on this increment's PR, verifying each pinned digest. S06-U2: HermiT over the complete pinned BFO and CCO plus the BCO modules, recording the closure loaded and the result | CI; `tools/ontology/reason.py` |

What batch 1 does not claim:

- It is not a complete register. The 3 held-back types (N-3) and the 13 Q-12 concepts (N-5)
  cannot be components yet, so a function that needs them is listed as waiting.
- No entry implies that an organization possesses the components, or that possession
  establishes integration, availability or adequacy (D-C).

## 3. Evidence-quality gates

The first increment writes no evidence. It runs S06-R1 to S06-R3, S06-A1, S06-MG, S06-U1 and
S06-U2. Every later evidence increment must pass the gates the standard fixes before its
data is committed:

1. Gate M on each graph's manifest, under OI-21's rule: no complete graph holds a revoked
   record.
2. The instance and description shapes and Gate C-A (S06-E1).
3. A signed G1-I record for each possession claim (K4, S06-E2). G1-T admission alone
   establishes no possession.
4. K5's fields on every assessment: criteria, source evidence, date, reviewer and finding.
   Missing data is never an adverse finding.
5. Persons (K7), and test and production kept apart (K2, S06-E3).

## 4. Coverage-register responsibilities

| Responsibility | Who |
|---|---|
| Drafting the batch: the function identifiers verified at the pin, the components, the reasons, the source evidence and the rights status of each identifier | Ontologist |
| Reviewing the batch's component relationships | A separate synthetic domain reviewer, under the accepted process |
| Accepting the batch as a whole, and deciding any substantive semantic dispute submitted with it | Architect |
| Verifying the rights basis of each identifier and relationship before distribution. Material whose public redistribution is not established is withheld | Ontologist, under the architect's conservative rule (E) |
| Keeping the register consistent with the module (S06-R2), and generating nothing from it (S06-R3) | The check suite, on every commit |

## 5. The second increment, scoped and not authorized

The second increment would write the first real organization evidence graph. Before any
evidence is collected or any G1-I assertion made, the architect decides:

- the organization;
- the data rights;
- the consent and privacy requirements;
- the instance namespace;
- the assessor and the reviewer.

None of these is invented. Confidential information never enters the public repository by
default.

## 6. Decisions

| # | Decision | Decided 2026-11-16 |
|---|---|---|
| K-1 | The Stage 06 standard | **Approved with clarifications** (A, F, G, H). The standard is amended to them, and ratifying the text depends on this PR |
| K-2 | The first increment, P1 to P4 | **Authorized** (B), once this PR confirms the match |
| K-3 | Register location, schema and OI-13 | **Decided** (C). Version 1's components are capability types, as approved class IRIs only. No individuals, functional units, act types or APQC process nodes. Any extension needs its own justification |
| K-4 | Rights for the register's identifiers | **Conservative** (E). Validated, permitted identifiers and mappings only. No APQC names, definitions, hierarchy descriptions or reconstructed content. Rights verified per identifier, otherwise withheld. A notice is not permission. Upstream checks are not blocked by it |
| K-5 | Upstream checks in this increment | **Required** (G): the refetch in an auditable workflow; HermiT with the complete pinned BFO and CCO, its closure and results recorded. No full BPO claim |
| K-6 | Stage 06 completion | **CP-3 necessary, not sufficient** (H). Completion also needs one real, authorized organization evidence graph with a signed G1-I decision. No synthetic substitute counts |
| — | Register approval | **One batch** (D), after a separate synthetic domain review. Only substantive disputes and the batch go to the architect |
| — | Second increment | **Not authorized** (I) |

## 7. What this does not do

This increment does not:

- reopen Stage 05;
- mint any term or instance IRI;
- assert any possession, sourcing, authorization or adequacy claim about a real
  organization;
- change BPO;
- publish APQC catalog content;
- authorize a release.

## 8. Wording at `ed5780a` that conflicted with the directions

| Where | Reviewed wording | Conflict | Now |
|---|---|---|---|
| Standard §6; proposal K-6 | Completion "on CP-3", and K-6 left open | H: CP-3 is not sufficient | §6 requires one real organization evidence graph; K-6 is decided |
| Standard §5; proposal §4 | The architect "approves … each register entry" | D: batch approval | One batch after a synthetic domain review; only disputes are escalated |
| Proposal K-4; standard K8 | "Commit the catalog nodes' IRIs (which carry PCF identifiers) with no text, under `pcf_notice.py`" | E: a notice is not permission; rights are verified per identifier | K8 and K-4 state the conservative rule. Unverified material is withheld |
| Standard K1 | One namespace paragraph | F: three kinds of IRI to be distinguished; no instance IRI in a term namespace | K1 is a table of the three kinds; instance IRIs wait for the second increment |
| Proposal P1 | Dispositions mixed BPO's facts and the BCO's acceptance ("written", "not a capability class") | B: keep what BPO declares apart from what the BCO accepts | Two separate fields; K10 forbids admission, reclassification and subclass assertions |
| Proposal P3; standard S06-MG | "New IRI or *not carried*" | B: identifier migration is not semantic equivalence | The semantic relation is a separate field; no equivalence and no replacement IRI without approved semantics (K10) |
| Proposal K-3 | "Components are capability classes only", recommended | C: decided, with excluded kinds named | K8 names the excluded kinds and the non-implications |
| Standard S06-U1; proposal P4 | "Made to trigger … or run by dispatch" | G: must execute in an auditable workflow | S06-U1 runs on this PR in CI. S06-U2 records the closure |
| Standard K4 and K5 | G1-I required; criteria, evidence and date | A: a reviewer field; missing data is not adverse; G1-T is not possession | K4 and K5 now say so |
| Standard §2 | The architect "approves each increment record" | I: nothing is invented, and confidential information is not committed by default | §2 says so |
