---
team: BPO
name: Business Process Ontology
repository: https://github.com/Skreen5hot/BusinessProcessOntology
---

# BPO

The Business Process Ontology says what an organization does; the BCO says what it can
do, and takes its act types from BPO's reality layer (spec v0.4 section 1).

**What this repository takes from BPO:** `ontology/apqc-ext.ttl`, vendored as a pinned
partial extract — see `config/upstream-sources.yaml` (id `bpo`) for the commit and digest.

**What BPO should know about this repository:** that it pins a BPO commit, and so depends
on that commit staying reachable; and that the spec proposes moving BPO's capability
classes into a BCO module (spec section 2), which is BPO's call as much as this one's.

BPO keeps its side of the record in its own `communications/bco/` (from BPO commit
`8f6622c`), under this protocol adopted unchanged, with its own copy of the checker
(`scripts/communications.py`). A message BPO sends is written in its `outgoing/` there;
the copy here, in `incoming/`, names that file and commit as its `source`.

**Announced by BPO (2026-10-23):** it will move every IRI it owns from
`http://example.org/apqc#` to `https://fandaws.com/ontology/bpo#`, and send the mapping
and landing commit here first. Every BPO IRI the BCO references changes with it.
BPO did so in v0.4.0 (`327ea2c`, notice filed 2026-10-27); the BCO re-pinned its vendored
extract to v0.4.1 (`bc64e91`) on 2026-10-28.
