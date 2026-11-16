# Stage 06, first increment — bounded implementation proposal

| Field | Value |
|---|---|
| Status | **Proposed**, for the architect's decision, with the proposed Stage 06 standard (`docs/proposals/2026-11-16-stage-06-knowledge-graph-standard.md`). Authorizes nothing until decided |
| Date | 2026-11-16 |
| Drafted by | Claude Code (`claude-opus-5-5`), for the BCO team |
| Basis | The decision of 2026-11-16 (`docs/decisions/2026-11-16-stage05-completion-accepted.md`, 6) |

## 1. Recommendation in one paragraph

Make the first increment **register data only**: the CP-3 scope audit, a first production
coverage register over the 39 written classes, and the `bc:` migration manifest. Add the
upstream checks the standard requires (S06-U1, S06-U2). **No organization, person or
evidence graph is written.** All three artifacts have real sources at the pins, need no new
namespace and name no person, and together they are CP-3. Production evidence graphs and
G1-I attributions need decisions only the architect can make (an organization, evidence
rights, consent, a namespace). They are a second increment, scoped in section 5 so those
decisions can be taken in parallel.

## 2. First production-data scope

| # | Artifact | Source, at its pin | Scope | Location |
|---|---|---|---|---|
| P1 | **CP-3 scope audit** | BPO `capabilities/capability_scope.json` at `bc64e91`, as harvested in `docs/sources/inventory/bpo-entries.yaml` (41 scope entries; 3 keys are not capability classes, per `bpo-findings.yaml`) | Every entry, each given exactly one disposition: *written* (cites its tranche record and G1-T record), *staged* (cites its open check or staging status), *person-borne, CM-02*, *not a capability class*, or *BPO-side* (§9 table) | `src/06_knowledge_graph/scope-audit.yaml` |
| P2 | **Coverage register v1** | BPO catalog nodes at `bc64e91` (keys); `src/05_ontology/apqc-cap.ttl` (components) | Only standing functions whose every component is one of the 39 written classes. The candidates are drafted from the functional groupings the catalog already keeps. Two examples are `bcoc:FinancialPerformanceManagement` and `bcoc:CapitalPlanning`, whose part-of narrowed types (`FinancialPerformanceAnalysis`, `CapitalInvestmentAppraisal`) are written. A grouping whose narrowed type is held back, such as `bcoc:CostManagement`, waits. Each entry is approved by the architect | `src/06_knowledge_graph/coverage-register.json`, schema `config/coverage-register.schema.json` |
| P3 | **`bc:` migration manifest** | The seven v0.1 classes in `drafts/BusinessCapabilityOntology_draft_v0.1.0/`, read under its checksums and never loaded as ontology; specification §9.1 | One row per v0.1 class: old IRI, new IRI or *not carried*, decision, definition change. No equivalence | `src/06_knowledge_graph/bc-migration.yaml` |
| P4 | **Upstream checks** | `config/upstream-sources.yaml` | S06-U1: the refetch job runs on this increment's PR (made to trigger on changes to the upstream config, or run by dispatch) and is recorded. S06-U2: HermiT over the complete pinned BFO and CCO plus the two modules | CI; `tools/ontology/reason.py` |

What P2's register will not claim:

- It is not a complete register: the 3 held-back types (N-3) and the 13 Q-12 concepts
  (N-5) cannot be components yet, so a function that needs them is left out, and listed as
  waiting.
- No entry implies that an organization performs the function, or that the function is
  adequate (CD16).

## 3. Evidence-quality gates

The first increment writes no evidence, so it runs S06-R1 to S06-R3, S06-A1, S06-MG and
S06-U1 to S06-U2. The standard fixes the gates every later evidence increment must pass
before its data is committed:

1. **Gate M** on a manifest for each graph, with OI-21's rule: no complete graph holds a
   revoked record.
2. **The instance and description shapes and Gate C-A** over the graph (S06-E1).
3. **A signed G1-I record** for each bearing claim (S06-E2). Gate F judges sufficiency
   against the stated threshold. A finding resting only on charts, charters, assignments
   or Authorization Records fails.
4. **Dated, sourced, thresholded findings** (K5), each source a record in `bco-sources#`
   with its rights status.
5. **Persons** (K7): named only on a stated basis, otherwise the graph stays outside the
   repository and only its manifest, digest and G1-I record enter.
6. **Separation** (K2, S06-E3): no fixture data in production paths, or the reverse.

## 4. Coverage-register responsibilities

| Responsibility | Who |
|---|---|
| Drafting a register entry: the key node verified at the pin, its components, and the reasons | Ontologist |
| Approving each entry, and each change to one | Architect |
| Deciding whether committing PCF node identifiers is within the rights posture | Architect (O-2), under `pcf_notice.py` |
| Deciding OI-13: whether a component may itself be a function. Recommended for v1: no (components are capability classes only) | Architect |
| Keeping the register consistent with the module (S06-R2) and generating nothing from it (S06-R3) | The check suite, run on every commit |
| Marking a function as standing, where BPO marks none (`docs/HANDOFF.md` §5.16) | Architect, per entry, recorded in the register |

## 5. The second increment, scoped (not proposed for authorization now)

The second increment would write the first production evidence graph: one organization,
one period and a bounded set of act classes and agents, with G1-I records. It needs five
decisions first:

- **E-a:** the organization, and whose evidence it is;
- **E-b:** the evidence's rights;
- **E-c:** the consent basis for any person named, or a decision to keep the graph out of
  the public repository (K7);
- **E-d:** the namespace for individuals and graph IRIs (OI-11, K1);
- **E-e:** the named assessor and Gate F reviewer.

None of these has a default the repository can supply.

## 6. Decisions requested

| # | Decision | Recommendation |
|---|---|---|
| K-1 | Approve the Stage 06 standard as proposed, or with changes | Approve |
| K-2 | Authorize the first increment, P1 to P4, as bounded in section 2 | Authorize |
| K-3 | Register location and schema (OI-13, part): `src/06_knowledge_graph/coverage-register.json` with `config/coverage-register.schema.json`, versioned, components only capability classes in v1 | Approve |
| K-4 | Rights for P2: commit the catalog nodes' IRIs (which carry PCF identifiers) with no text, under `pcf_notice.py` | The architect's call under O-2; the increment writes no key until it is made |
| K-5 | Upstream: require S06-U1 and S06-U2 in this increment, rather than only before a release | Require |
| K-6 | Whether Stage 06 completion (D7) requires at least one production evidence graph, or CP-3 alone | Decide with the second increment's E-a to E-e |

## 7. What this does not do

It does not reopen Stage 05, mint any term, assert any bearing, sourcing, authorization or
adequacy claim about a real organization, change BPO, or authorize a release.
