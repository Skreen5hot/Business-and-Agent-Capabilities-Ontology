# CLAUDE.md — project grounding

The Business Capability Ontology (BCO), aligned to BFO 2020 / CCO v2.0, taking its act types
from the Business Process Ontology (BPO). Read `docs/HANDOFF.md` for the state,
`docs/DEVELOPMENT.md` for how to run things, `docs/process/PROCESS.md` for the method.

## What is true right now

- The design is `specifications/Business-Capability-Ontology-v0.5.0-draft.3.md`, accepted for
  ratification on 2026-11-04 (D3's exit). **RP-1, RP-2 and RP-10 are ratified** (CD1 to CD5,
  §8's G1-T and G1-I; `docs/decisions/2026-11-04-d4-rp1-rp10-ratified-option-b.md`,
  `docs/decisions/2026-11-04-rp2-ratified.md`), **CD6 to CD11** with them
  (`docs/decisions/2026-11-05-cd6-cd11-ratified.md`), **RP-3** (CD12;
  `docs/decisions/2026-11-06-rp3-ratified.md`), **RP-4** (CD13;
  `docs/decisions/2026-11-06-rp4-ratified.md`), **RP-6 to RP-9** (CD14 to CD17;
  `docs/decisions/2026-11-06-rp6-rp9-ratified.md`) and **RP-5** (the namespace;
  `docs/decisions/2026-11-07-rp5-ratified.md`); the first record is also the architectural
  admission of the parent `bco:BusinessCapability`, which is not minted. **ADR-002 is
  accepted and CP-0 is complete** (2026-11-07, `docs/decisions/2026-11-07-adr002-accepted-cp0-complete.md`); the ratified commitments
  are binding, and draft.3 is kept as the historical ratification baseline. Since 2026-11-15
  draft.3 is also the specification in force for the tooling (layout role `specification`;
  `docs/decisions/2026-11-15-spec-v0.5-in-force.md`), so the metamodel definitions are its §4 rows. Do not implement an unratified
  CAP item as if it were decided. Under Option B, G1-T review may now record PASS or
  FAIL, signed by the named reviewer; OWL waits for D5, which CP-0 does not authorize. v0.4.0-draft.1 is kept as the prior
  version.
- The repository follows six stages, `src/01_controlled_vocabulary/` to
  `src/06_knowledge_graph/` (`docs/decisions/2026-10-25-stage-02-choices.md`); each stage
  directory's README states its status. Stage 02 (Conceptual Modeling) runs under
  `docs/standards/stage-02-conceptual-modeling.md`. CM-01 (Business Capability) was approved
  on 2026-10-26 as the Stage 02 baseline (`docs/decisions/2026-10-26-cm01-approved-r8-r9-accepted.md`);
  never change an approved model silently — a substantive change is a new, reviewed
  version. CM-02 (Agent Capability) is planned, not started. The
  vocabulary was under `vocab/` and the modules under `ontology/` until 2026-10-25;
  records, ADRs and reviews written before then use the old paths, and stay as written.
- **D6 is authorized for the first tranche** (`docs/decisions/2026-11-15-v05-transition-approved-d6-authorized.md`). `src/05_ontology/apqc-cap.ttl` holds
  `bco:BusinessCapability` and 39 capability classes with their signed indexes, written by
  `tools/ontology/formalize.py --write` from `src/05_ontology/tranche-1.yaml` and never by
  hand. Under B-1 to B-4 (`docs/decisions/2026-11-15-b1-b4-approved-cap34-confirmed.md`)
  `apqc-cap-desc.ttl` holds the description layer (nine information classes and the
  annotation properties `bco:concernsType` and `bco:assessedPresence`), written the same way
  from `src/05_ontology/tranche-2-description.yaml`. Gate M (`tools/ontology/manifests.py`)
  checks the CD15 manifests. CQ-11 is answered from the signed review records, by an
  approved exception; CAP-34's has agent is confirmed. **Both Stage 05 tranches are
  complete** (accepted 2026-11-16, `docs/decisions/2026-11-16-stage05-completion-accepted.md`),
  validated against test fixtures, with CP-1 and CP-2 under the qualifications of the
  completion record's section 9; CAP-20's and CAP-33's schema.org encodings are confirmed as
  encoding conventions only. No release and no production G1-I assertion.
- **Stage 06** runs under `docs/standards/stage-06-knowledge-graph.md` (approved 2026-11-16,
  `docs/decisions/2026-11-16-stage06-standard-and-first-increment.md`). Only the register-first increment is
  authorized: the 41-entry scope audit, a coverage-register batch, the `bc:` migration
  manifest and the upstream checks. No real organization evidence, no instance IRI, no APQC
  names or definitions. **CP-3 is closed** (2026-11-17, `docs/decisions/2026-11-17-cp3-closed.md`), but CP-3 is not Stage 06
  completion, which needs a real, authorized organization evidence graph.
  Before the first tranche, the only `bco:` IRIs with triples were the controlled
  vocabulary's annotation properties and the `bco:PCFCode` datatype, declared in the generated
  `src/01_controlled_vocabulary/generated/bco-vocabulary.ttl` (accepted 2026-10-24, `docs/decisions/2026-10-24-p3-accepted.md`).
  The vocabulary holds 83 concepts (9 metamodel, 74 catalog: 5 pilots, 64 from
  semantic-curation tranche 2, `docs/decisions/2026-11-07-curation-tranche-2-approved.md`, and 5
  narrowed types from the G1-T batch decision, `docs/decisions/2026-11-14-g1t-tranche-2-batch-decided.md`), all Draft and none
  ratified; its generated Turtle is in the validation data graph
  (layout `vocabulary: true`) under `shapes/vocabulary_shapes.ttl`, and not in the corpus digest.
- `drafts/BusinessCapabilityOntology_draft_v0.1.0/` is preserved byte-for-byte and checked
  against its own checksums. **Never edit it**, and never load its Turtle as ontology.

## Rules that are easy to break

- **Namespaces.** This repository mints IRIs only in the five namespaces of ADR-003 D1, listed
  as `AUTHORED_NAMESPACES` in `tools/ontology/validate.py` (permanent since RP-5, `docs/decisions/2026-11-07-rp5-ratified.md`):
  `https://fandaws.com/ontology/bco#` for ontology terms; `bco-metamodel#` and `bco-catalog#`
  for vocabulary concepts; `bco-sources#` and `bco-agents#` for source records and agents.
  Vocabulary IRIs are minted by `tools/vocab/build.py`, never by hand. The spec writes `ex:`
  both for BPO's terms and for terms the BCO will mint (spec v0.5 corrects it) — do not copy
  spec Turtle examples verbatim. Since the 2026-10-28 re-pin, `ex:` is a temporary prefix for
  BPO's genera only, bound to `https://fandaws.com/ontology/bpo#`
  (`docs/decisions/2026-10-28-i2-and-bpo-repin-decided.md`, R3): reference BPO act types
  through it, never redeclare them, and never write a BCO term with it. A namespace change edits the list and
  every shape's SPARQL filter in one commit; `tests/test_namespace.py` fails until they agree.
- **Every tracked file is declared** in `config/repository-layout.yaml` with a role. A new
  file without a declaration fails the suite.
- **A new shape set arrives with its negative fixture** and positive controls in the same
  commit, and its constraint messages are listed by name in `tests/test_ontology_checks.py`.
- **Generated files are regenerated, never edited**: `vendor/**`, `vendor/NOTICE.md`,
  `config/upstream-extracts.json`, `config/validation-baseline.json`,
  `config/corpus-digest.json`. Each names its generator in the layout contract.
- **Verify before asserting an upstream IRI.** Grep the vendored extract, or rebuild with
  `--rebuild` if the term is not there yet; never assert a `cco:`/`obo:` IRI from memory.
- **Decisions are the architect's.** Record an act verbatim in `docs/decisions/` with the
  digest of what it is about; never perform one.
- **Line endings are LF** (`.gitattributes`). Digests in this repository are over LF bytes.
  On Windows, write files as bytes (`write_bytes`), not `write_text`, which writes CRLF.
- **Communications with other teams** go in `communications/<team>/{incoming,outgoing}/`
  under the communications protocol 1.1 (`Skreen5hot/communications`, `PROTOCOL.md`),
  which `communications/README.md` pins with this record's local rules. A committed message
  is never edited, moved with changed bytes, or deleted; a correction is a new message
  replying to it. Messages are announced on that repository's Discussions board. Sending a
  message, posting an alert or commenting there is the architect's call. At session start,
  check the board's Alerts for messages to `BCO` (`tools/inbox.py --code BCO` there) and
  report any to the architect.

## Before committing

```bash
.venv/Scripts/python tools/layout.py
.venv/Scripts/python tools/licensing/disposition.py --check
.venv/Scripts/python tools/ontology/vendor_upstream.py
.venv/Scripts/python tools/ontology/validate.py --gate
.venv/Scripts/python tools/ontology/formalize.py
.venv/Scripts/python tools/ontology/manifests.py
.venv/Scripts/python tools/kg/register.py
.venv/Scripts/python tools/ontology/reason.py --checkpoint
.venv/Scripts/python tools/communications.py
.venv/Scripts/python tools/vocab/build.py
.venv/Scripts/python tools/conceptual/check_models.py
.venv/Scripts/python tools/site/vendor_assets.py
.venv/Scripts/python tools/inventory/harvest_bpo.py
.venv/Scripts/python tools/inventory/rights.py
.venv/Scripts/python tools/inventory/harvest_pcf.py
.venv/Scripts/python tools/licensing/pcf_notice.py
.venv/Scripts/python tools/catalog/synthesize.py
.venv/Scripts/python -m pytest tests/ -q -p no:randomly
.venv/Scripts/python tools/site/build_site.py && .venv/Scripts/python tools/site/check_site.py
```

The public site is for external validators and is built from the repository at deploy
time; never commit `_site/`, and never type a figure into `site/` that the build can
read.

If `config/vocab-schema.yaml` or `src/01_controlled_vocabulary/*.yaml` changed, also run
`.venv-vocab/Scripts/python tools/vocab/schema_check.py` in a venv with
`requirements-vocab.txt` (LinkML; never installed into `.venv`). If the vocabulary
inputs changed, `tools/vocab/build.py --write` regenerates `src/01_controlled_vocabulary/generated/`.

If the ontology changed: `tools/ontology/corpus_digest.py -o config/corpus-digest.json`, and
`tools/ontology/validate.py --record` if a finding was fixed. Commit messages carry the
reasoning — what was wrong, why the fix is the fix, what was measured, what is not covered.
Nothing is pushed without the architect's say-so.
