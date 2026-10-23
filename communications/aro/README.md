---
team: ARO
name: Application Requirement Ontology
repository: https://github.com/Skreen5hot/ApplicationRequirementOntology
---

# ARO

The Application Requirement Ontology is where this repository's tooling and method come
from (`docs/process/PROCESS.md`, `tools/`, the layout contract), carried at ARO commit
`733538a` on 2026-10-23.

**What ARO should know about this repository:** the carried `vendor_upstream.py`
partitions extract triples by subject namespace, which put four CCO-only annotations into
the BFO extract under BFO's licence; this repository's copy attributes each triple to the
file that asserts it (`docs/HANDOFF.md` §5.7). ARO's copy still does the former. No
message about it has been sent yet.

ARO's own cross-team record cites messages in IntegratedAgent's `experiments/comms/` by
repository, path, commit and digest — the same binding this folder's `source` field uses.
