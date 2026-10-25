# Stage 01 — Controlled Vocabulary

**Status:** in place, under ADR-003. 14 concepts (9 metamodel, 5 catalog), all **Draft**;
none ratified.

| Path | What it is |
|---|---|
| `metamodel.yaml` | metamodel concept records (`bcom:`), one per concrete row of specification section 4; provenance only, never a definition. Edited by hand |
| `catalog.yaml` | catalog concept records (`bcoc:`). Edited by hand |
| `agents.yaml` | declared agents (`bcoa:`). Edited by hand |
| `generated/` | the five Turtle files `tools/vocab/build.py --write` builds from the YAML. Never edited |

The rules are ADR-003's (`docs/adr/`), enforced by `tools/vocab/build.py`; how to work
here is in `docs/DEVELOPMENT.md`. Standard: not yet supplied.

These files were under `vocab/` until 2026-10-25. Their git history is under that path;
`git log --follow` reaches it.
