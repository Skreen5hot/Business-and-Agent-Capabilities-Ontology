# CLAUDE.md — project grounding

The Business Capability Ontology (BCO), aligned to BFO 2020 / CCO v2.0, taking its act types
from the Business Process Ontology (BPO). Read `docs/HANDOFF.md` for the state,
`docs/DEVELOPMENT.md` for how to run things, `docs/process/PROCESS.md` for the method.

## What is true right now

- The design is `specifications/Business-Capability-Ontology-v0.4.0-draft.1.md`. **It is a
  draft.** Nothing in it is normative until the architect ratifies it (RP-1 to RP-10, then
  ADR-002). Do not implement a CD or CAP item as if it were decided.
- The repository follows six stages, `src/01_controlled_vocabulary/` to
  `src/06_knowledge_graph/` (`docs/decisions/2026-10-25-stage-02-choices.md`); each stage
  directory's README states its status. Stage 02 (Conceptual Modeling) runs under
  `docs/standards/stage-02-conceptual-modeling.md`. CM-01 (Business Capability) was approved
  on 2026-10-26 as the Stage 02 baseline (`docs/decisions/2026-10-26-cm01-approved-r8-r9-accepted.md`);
  never change an approved model silently — a substantive change is a new, reviewed
  version. CM-02 (Agent Capability) is planned, not started. The
  vocabulary was under `vocab/` and the modules under `ontology/` until 2026-10-25;
  records, ADRs and reviews written before then use the old paths, and stay as written.
- `src/05_ontology/apqc-cap.ttl` and `src/05_ontology/apqc-cap-desc.ttl` are empty `owl:Ontology` headers.
  No BCO ontology term exists. The only `bco:` IRIs with triples are the controlled
  vocabulary's annotation properties and the `bco:PCFCode` datatype, declared in the generated
  `src/01_controlled_vocabulary/generated/bco-vocabulary.ttl` (accepted 2026-10-24, `docs/decisions/2026-10-24-p3-accepted.md`).
  Since P5 the vocabulary holds 14 concepts (9 metamodel, 5 catalog), all Draft and none
  ratified; its generated Turtle is in the validation data graph
  (layout `vocabulary: true`) under `shapes/vocabulary_shapes.ttl`, and not in the corpus digest.
- `drafts/BusinessCapabilityOntology_draft_v0.1.0/` is preserved byte-for-byte and checked
  against its own checksums. **Never edit it**, and never load its Turtle as ontology.

## Rules that are easy to break

- **Namespaces.** This repository mints IRIs only in the five namespaces of ADR-003 D1, listed
  as `AUTHORED_NAMESPACES` in `tools/ontology/validate.py` (all provisional, pending RP-5):
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
  under the protocol in `communications/README.md`. A committed message is never edited;
  a correction is a new message replying to it. Sending one is the architect's call.

## Before committing

```bash
.venv/Scripts/python tools/layout.py
.venv/Scripts/python tools/licensing/disposition.py --check
.venv/Scripts/python tools/ontology/vendor_upstream.py
.venv/Scripts/python tools/ontology/validate.py --gate
.venv/Scripts/python tools/communications.py
.venv/Scripts/python tools/vocab/build.py
.venv/Scripts/python tools/conceptual/check_models.py
.venv/Scripts/python tools/site/vendor_assets.py
.venv/Scripts/python tools/inventory/harvest_bpo.py
.venv/Scripts/python tools/inventory/rights.py
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
