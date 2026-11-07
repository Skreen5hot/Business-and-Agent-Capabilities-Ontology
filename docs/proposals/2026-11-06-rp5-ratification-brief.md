# RP-5 ratification brief — the permanent namespace, on the domain held

| Field | Value |
|---|---|
| Status | **Proposed.** For the architect. It decides nothing; ratifying RP-5 is the architect's act |
| Date | 2026-11-06 |
| Prepared by | Claude Code (`claude-opus-5-5`), for the BCO team |
| Closes, if decided | CP-0 closure matrix item 9, decision 6 (`docs/proposals/2026-11-05-cp0-closure-matrix.md`); the release check of spec §10, "The permanent namespace is decided (RP-5)" |
| Builds on | `docs/proposals/2026-11-05-rp5-namespace-options.md` at `718c8e7`, SHA-256 `9a4e12d0f19cf558d2bfb8906b4a55e634b0ba3456ed88b9c7b5cff51e8f2996` |
| Text checked | `specifications/Business-Capability-Ontology-v0.5.0-draft.3.md` at `c3f1ba2`, SHA-256 `2224f869b0ec7a1e31b0afc1c2b403ad222ea290c334bff48a93ebbb6516c574`: §1 prefixes, §10 RP-5. ADR-003 D1 and "Out of scope, locked" |

## 1. The input this brief rests on

The options note left one question the team could not settle: whether the architect will
hold `fandaws.com` for the long term (§4 of that note). Asked in session on 2026-11-06,
"Is fandaws.com a domain you will keep for the ontology's IRIs?", the architect answered:

```text
Yes, keep it
```

That is a statement of intent, not the ratification. On that basis the options note
recommends **Option A**: keep the domain, keep hash IRIs, for all five namespaces.

## 2. What ratifying Option A would fix

| Part | Under Option A |
|---|---|
| Authority | `https://fandaws.com/ontology/`, held by the architect |
| Form | `#` (hash) for all five namespaces |
| Scope | All five namespaces of ADR-003 D1, together |

So the five IRIs become permanent exactly as they are now:

| Prefix | Namespace | Holds |
|---|---|---|
| `bco:` | `https://fandaws.com/ontology/bco#` | Ontology terms |
| `bcom:` | `https://fandaws.com/ontology/bco-metamodel#` | Metamodel concepts |
| `bcoc:` | `https://fandaws.com/ontology/bco-catalog#` | Catalog concepts |
| `bcos:` | `https://fandaws.com/ontology/bco-sources#` | Source records |
| `bcoa:` | `https://fandaws.com/ontology/bco-agents#` | Declared agents |

**No IRI changes.** Nothing minted, generated or recorded is renamed, and
`tests/test_namespace.py` needs no new strings. BPO's own namespace,
`https://fandaws.com/ontology/bpo#`, is on the same domain in the same form. Option A asks
nothing of BPO, so no message to BPO is needed.

## 3. Three points the ratification should settle

Each of these has a recommendation; the architect may decide any of them otherwise.

1. **Ontology-document IRIs.** The two module headers are named
   `https://fandaws.com/ontology/bco/apqc-cap` and `…/bco/apqc-cap-desc`. The vendored
   extracts are named under `https://fandaws.com/ontology/bco/vendor/` (`EXTRACT_BASE` in
   `tools/ontology/vendor_upstream.py`). These are slash paths. Under hash form they fall
   outside every authored namespace: `bco/…` does not start with `bco#`.
   - **Recommendation:** keep them. Record that `https://fandaws.com/ontology/bco/` names
     ontology documents, and that no term is minted there.
   - The options note offered moving `EXTRACT_BASE` to `bco-vendor/`. That mattered under
     slash form. Under hash form, moving it would regenerate every vendored extract and
     `config/upstream-extracts.json` for no gain in separation.
2. **Resolution.** Today no BCO IRI resolves, and the public site says so. Hash IRIs need
   one document per namespace, served at the namespace IRI without its `#`.
   - **Recommendation:** RP-5 fixes identity only. Serving those five documents is a
     release obligation at D8, recorded as such. It is not a CP-0 condition.
   - Until then the site keeps saying the IRIs do not resolve, but no longer calls them
     provisional.
3. **Version IRIs.** RP-5 does not decide how releases are versioned, for example
   `owl:versionIRI` paths. **Recommendation:** leave that to Stage 05 and the release
   process, where the module headers are written.

## 4. What would change once ratified

No IRI changes. The word "provisional", and "pending RP-5", come out of the places that
say it. In one commit:

| File | Today | After |
|---|---|---|
| `tools/ontology/validate.py` (`AUTHORED_NAMESPACES` comment) | "the architect's provisional choice of 2026-10-23 pending RP-5" | Permanent, citing the RP-5 record |
| `tests/test_namespace.py` (docstring) | "all provisional pending RP-5" | The same |
| `shapes/wellformedness_shapes.ttl` (comment) | "All provisional until RP-5 mints permanent ones" | The same. The comment only; no constraint changes, so no new fixture |
| `src/05_ontology/apqc-cap.ttl`, `apqc-cap-desc.ttl` | Header comment and `rdfs:comment`: "PROVISIONAL", "Namespace provisional pending RP-5" | The same. This changes the ontology, so `config/corpus-digest.json` is regenerated |
| `site/content/site.json`, `site/pages/vocabulary.html`, `tools/site/build_site.py` (the "(provisional)" label) | The IRI notice and the vocabulary page call the namespaces provisional | Permanent. The notice still says the IRIs do not resolve yet |
| `CLAUDE.md`, `docs/DEVELOPMENT.md`, `docs/HANDOFF.md` §5.1 | "provisional, pending RP-5" | Permanent, citing the record |
| Roadmap, closure matrix, this brief, the options note | Open | Status lines only |

**Left unchanged:**
- **The specification.** Its §1 "Provisional until RP-5" and its §10 row wait for the next
  reviewed version, as with every earlier ratification.
- **ADR-003.** It is ratified, so its body stays as written. Its "`#` versus `/` …: RP-5" is
  answered by the decision record.
- **Records and reviews** that say "provisional". They were true when written.

## 5. Recommended disposition

**Ratify RP-5 as Option A:**
- `https://fandaws.com/ontology/`, held by the architect;
- hash form;
- all five ADR-003 D1 namespaces, permanent as they stand.

Also adopt §3's three recommendations:
- ontology-document IRIs stay under `bco/`, with no term minted there;
- serving the namespace documents is a D8 release obligation;
- version IRIs are left to Stage 05.

## 6. What this brief does not do

It ratifies nothing and changes no namespace, list, shape, module or page. It registers
nothing with any service and sends no message to BPO. It mints nothing and adds no object
property or OWL. ADR-002 and the stage-completion record remain CP-0 obligations.
