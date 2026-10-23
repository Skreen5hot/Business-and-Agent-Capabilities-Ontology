# CLAUDE.md — project grounding

The Business Capability Ontology (BCO), aligned to BFO 2020 / CCO v2.0, taking its act types
from the Business Process Ontology (BPO). Read `docs/HANDOFF.md` for the state,
`docs/DEVELOPMENT.md` for how to run things, `docs/process/PROCESS.md` for the method.

## What is true right now

- The design is `specifications/Business-Capability-Ontology-v0.4.0-draft.1.md`. **It is a
  draft.** Nothing in it is normative until the architect ratifies it (RP-1 to RP-10, then
  ADR-002). Do not implement a CD or CAP item as if it were decided.
- `ontology/apqc-cap.ttl` and `ontology/apqc-cap-desc.ttl` are empty `owl:Ontology` headers.
  No BCO term exists.
- `drafts/BusinessCapabilityOntology_draft_v0.1.0/` is preserved byte-for-byte and checked
  against its own checksums. **Never edit it**, and never load its Turtle as ontology.

## Rules that are easy to break

- **Namespace.** Author BCO terms in `https://fandaws.com/ontology/bco#` (provisional,
  pending RP-5). The spec writes them as `ex:`, which is BPO's namespace — do not copy spec
  Turtle examples verbatim. Reference BPO act types by their `ex:` IRIs; never redeclare them.
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

## Before committing

```bash
.venv/Scripts/python tools/layout.py
.venv/Scripts/python tools/licensing/disposition.py --check
.venv/Scripts/python tools/ontology/vendor_upstream.py
.venv/Scripts/python tools/ontology/validate.py --gate
.venv/Scripts/python -m pytest tests/ -q -p no:randomly
.venv/Scripts/python tools/site/build_site.py && .venv/Scripts/python tools/site/check_site.py
```

The public site is for external validators and is built from the repository at deploy
time; never commit `_site/`, and never type a figure into `site/` that the build can
read.

If the ontology changed: `tools/ontology/corpus_digest.py -o config/corpus-digest.json`, and
`tools/ontology/validate.py --record` if a finding was fixed. Commit messages carry the
reasoning — what was wrong, why the fix is the fix, what was measured, what is not covered.
Nothing is pushed without the architect's say-so.
