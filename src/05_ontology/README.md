# Stage 05 — Ontology

**Status:** specified, not written. The two modules specification v0.4 section 2 names
are `owl:Ontology` headers only. No BCO ontology term exists; none is minted before
ADR-002 is ratified.

| Path | Will hold |
|---|---|
| `apqc-cap.ttl` | Business Capability, the capability classes with their realization index, reviewed unions |
| `apqc-cap-desc.ttl` | the seven description-layer classes and the Authorization Record |

Both are in the corpus digest (`config/corpus-digest.json`) and the validation ladder.
How to write the first term is in `docs/DEVELOPMENT.md`. Standard: not yet supplied.

These files were under `ontology/` until 2026-10-25. Their git history is under that
path; `git log --follow` reaches it.
