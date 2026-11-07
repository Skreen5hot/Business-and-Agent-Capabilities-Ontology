# Decision record — RP-5 ratified, 2026-11-07

Recorded verbatim by Claude Code (`claude-opus-5-5`) on 2026-11-07, from the decision the
architect, Aaron Damiano, gave in session. The act is the architect's.

## What it is about

| Field | Value |
| --- | --- |
| Item | RP-5, the permanent namespace, in `specifications/Business-Capability-Ontology-v0.5.0-draft.3.md` at `c3f1ba2`, SHA-256 `2224f869b0ec7a1e31b0afc1c2b403ad222ea290c334bff48a93ebbb6516c574` (accepted for ratification 2026-11-04); and ADR-003's "`#` versus `/` for every namespace above: RP-5" |
| Design decided on | `docs/proposals/2026-11-06-rp5-ratification-brief.md` at `8521ea2`, SHA-256 `e4786674ebb19d7a0a868314f0cf2267d18486bdeb2e9c1288f28f2b4e8e7db9` |
| Built on | `docs/proposals/2026-11-05-rp5-namespace-options.md` at `718c8e7`, SHA-256 `9a4e12d0f19cf558d2bfb8906b4a55e634b0ba3456ed88b9c7b5cff51e8f2996` |
| CP-0 item | 9 of `docs/proposals/2026-11-05-cp0-closure-matrix.md`, decision 6 |

## The decision

````text
Subject: Architect Approval — RP-5 Permanent Namespace
Decision: RP-5 OPTION A APPROVED.
I approve the RP-5 namespace design presented in `2026-11-06-rp5-ratification-brief.md`.
The following decisions are binding:

1. Retain `fandaws.com` and the existing hash-based term IRI structure. No namespace migration is authorized.
2. Make the five proposed namespace values permanent, explicitly listing their full IRIs in the ratification record.
3. Retain the existing slash-based ontology-document and vendored-extract IRIs. Do not mint ontology terms under those document paths.
4. Treat namespace resolution and publication as D8 release obligations, not CP-0 blockers.
5. Defer version-IRI implementation to Stage 05.
6. Preserve BPO's independently governed namespace and existing upstream identifiers.

Implementation authorization: Record RP-5 as ratified, close its CP-0 item, and make the proposed administrative updates to code comments, namespace tests, shapes, module headers and documentation.
Preserve historical decision records and existing term IRIs.
After completing RP-5, proceed directly to ADR-002 and the Stage Completion Record.
Do not initiate another namespace review or broaden the work. Our priority is completing CP-0 and advancing the capability catalog into semantic normalization, taxonomy and ontology formalization.
````

## The acts it contains

1. **RP-5 is ratified as Option A.** The authority is `https://fandaws.com/ontology/`, held
   by the architect, in hash form. No namespace migration is authorized.
2. **The five namespaces are permanent**, with these full IRIs:

   | Prefix | Namespace | Holds |
   | --- | --- | --- |
   | `bco:` | `https://fandaws.com/ontology/bco#` | Ontology terms |
   | `bcom:` | `https://fandaws.com/ontology/bco-metamodel#` | Metamodel concepts |
   | `bcoc:` | `https://fandaws.com/ontology/bco-catalog#` | Catalog concepts |
   | `bcos:` | `https://fandaws.com/ontology/bco-sources#` | Source records |
   | `bcoa:` | `https://fandaws.com/ontology/bco-agents#` | Declared agents |

3. **Document IRIs.** The slash-based ontology-document IRIs (`https://fandaws.com/ontology/bco/apqc-cap`,
   `https://fandaws.com/ontology/bco/apqc-cap-desc`) and the vendored-extract IRIs (under
   `https://fandaws.com/ontology/bco/vendor/`) are kept. No ontology term is minted under
   those document paths.
4. **Resolution and publication** of the namespaces are D8 release obligations, not CP-0
   blockers.
5. **Version IRIs** are deferred to Stage 05.
6. **BPO.** Its independently governed namespace, `https://fandaws.com/ontology/bpo#`, and
   the existing upstream identifiers are preserved.
7. **CP-0 item 9 (decision 6) is closed.**
8. **Implementation.** The administrative updates the brief lists (§4) are authorized.
   Historical decision records and existing term IRIs are preserved. Next come ADR-002 and
   the stage-completion record. No further namespace review is started, and the work is not
   broadened.

## How it was carried out

No IRI changed. In the same commit as this record, "provisional" and "pending RP-5" come
out of the places that said it:

- **Code comments:** the `AUTHORED_NAMESPACES` comment in `tools/ontology/validate.py`, and
  the namespace comment in `shapes/wellformedness_shapes.ttl` (a comment only; no
  constraint changed).
- **The namespace test:** the docstring of `tests/test_namespace.py`. Its strings are
  unchanged.
- **Module headers:** the header comment and `rdfs:comment` of `src/05_ontology/apqc-cap.ttl`
  and `src/05_ontology/apqc-cap-desc.ttl`. `config/corpus-digest.json` is regenerated.
- **The site:** the IRI notice in `site/content/site.json`, the namespaces paragraph in
  `site/pages/vocabulary.html`, and the "(provisional)" label in `tools/site/build_site.py`.
  The notice still says the IRIs do not resolve yet.
- **Status lines:** `CLAUDE.md`, `docs/DEVELOPMENT.md` and `docs/HANDOFF.md` §5.1; the
  roadmap's state, D4, D8 and O-6 rows and its amendment log; the closure matrix, the
  options note and the brief. Each proposal's body is unchanged.

**Not changed:**
- **The specification.** Its §1 "Provisional until RP-5" and its §10 row wait for the next
  reviewed version.
- **ADR-003.** It is ratified, and its body stays as written. This record answers its
  "`#` versus `/`" line.
- **Earlier records and reviews** that say "provisional". They were true when written.

## What it does not do

- It does not decide ADR-002 or the stage-completion record, so CP-0 stays open. OWL still
  waits for all of CP-0 and D5.
- It serves nothing, registers nothing with any service, and sends no message to BPO.
- It mints and asserts nothing, and makes no G1-I claim.
