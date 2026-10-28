# Draft message — acknowledgment to BPO of the re-pin (for authorization)

| Field | Value |
|---|---|
| Status | **Draft. Not sent.** Sending is a separate act needing the architect's authorization (R4, `docs/decisions/2026-10-28-i2-and-bpo-repin-decided.md`) |
| Why it is here and not in `communications/bpo/outgoing/` | That folder holds messages *sent* (`communications/README.md`), and a committed message never changes. Its BCO ref must also name the commit that lands the re-pin, which exists only once this pull request is merged |
| On authorization | The message below is filed in `communications/bpo/outgoing/` with the BCO merge commit and file digest filled in (marked `<…>`), committed, and delivered to BPO's `communications/bco/incoming/` under the shared protocol |

---

```markdown
---
id: BCO-BPO-<date sent>-repin-acknowledgment
from: BCO
to: BPO
date: <date sent>
type: acknowledgment
subject: BCO re-pinned apqc-ext.ttl to v0.4.1 (bc64e91) under the https://fandaws.com/ontology/bpo# namespace
in_reply_to: BPO-BCO-2026-10-23-namespace-v0-4-0
refs:
  - repo: Skreen5hot/BusinessProcessOntology
    commit: bc64e91839378e1926189c01bf184d6a22d5c1b7
    path: ontology/apqc-ext.ttl
    sha256: a8119728796872a1814aace8130a32cc8e42961b0bd5feaa28b736d60a0cc6fd
  - repo: Skreen5hot/BusinessProcessOntology
    commit: bc64e91839378e1926189c01bf184d6a22d5c1b7
    path: LICENSE
    sha256: 2154e0221f7e5119b2d45842fcd4be421c11c5d64a459601f2c35f53710c487a
  - repo: Skreen5hot/Business-and-Agent-Capabilities-Ontology
    commit: <BCO merge commit of the re-pin>
    path: config/upstream-sources.yaml
    sha256: <SHA-256 of that file at that commit>
author: Claude Code (agent), drafted at Aaron Damiano's direction
requires_act: false
---

# BCO re-pinned apqc-ext.ttl to v0.4.1

Thank you for the v0.4.0 and v0.4.1 notices. The BCO has re-pinned its vendored extract of
`ontology/apqc-ext.ttl` from `6613194` to `bc64e91` (v0.4.1), in BCO commit `<…>`.

## What we checked

- At your re-pin target `327ea2c`, the file is graph-isomorphic to `6613194` with the base
  rewritten, ignoring `owl:versionInfo`, as your notice said.
- At `bc64e91` it differs further only in 14 `rdfs:comment` literals, where your prose now
  writes `bpo:` for `ex:`, and in `owl:versionInfo`. Three of those comments are on genera
  we vendor (Improvement, Organizational Establishment, Remuneration).
- No label, definition or `rdfs:subClassOf` axiom of the six genera we vendor changed.
- Your `LICENSE` is unchanged.

## What changed on our side

- The six genera are now referenced at `https://fandaws.com/ontology/bpo#<LocalName>`, local
  names unchanged. We assert no equivalence between the old and new IRIs.
- Our prefix label stays `ex:` for now, bound to your new namespace and used for your genera
  only. We will move to `bpo:` with our specification v0.5.
- `6613194` no longer needs to stay reachable for the vendored extract. Our capability
  inventory still records it as its historical baseline, by digest, so we would still
  appreciate it staying reachable.

This closes the loop your v0.4.0 notice offered. Nothing here needs an answer.
```
