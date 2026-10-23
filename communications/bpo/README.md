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

BPO has no communications folder of its own yet, so there is no path for an incoming
message to cite. Until there is, an incoming message's `source` points at wherever the
original was written.
