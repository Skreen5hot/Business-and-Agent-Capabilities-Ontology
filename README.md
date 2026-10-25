# Business and Agent Capabilities Ontology

> **New here?** Read [`docs/HANDOFF.md`](docs/HANDOFF.md) first. It states what is actually
> in this repository and what is not — in particular, that the specification is a draft
> and **no ontology term has been written yet**. [`docs/DEVELOPMENT.md`](docs/DEVELOPMENT.md)
> is how to run things; [`docs/process/PROCESS.md`](docs/process/PROCESS.md) is why it is
> built this way.

The Business Capability Ontology (BCO) says what an organization can do. The Business
Process Ontology (BPO) says what it does. The BCO takes its act types from the BPO reality
layer and adds the dispositions those acts realize.

It is developed in alignment with BFO 2020, CCO 2.0, and the companion
[Business Process Ontology](https://github.com/Skreen5hot/BusinessProcessOntology).

**Status: draft.** No ADR-002 ratification and no v0.4 ontology implementation is implied.

**Reviewing it?** The site at https://skreen5hot.github.io/Business-and-Agent-Capabilities-Ontology/ renders the specification and the
review, lets you search the terms, and shows what is ratified and what is not — no clone
needed.

## Current sources

- **[BCO specification v0.4.0-draft.1](specifications/Business-Capability-Ontology-v0.4.0-draft.1.md)**
  — requirements and target design. Not an implementation, and not normative until ratified.
- **[R5 review of v0.4 against artifacts](reviews/R5-v0.4-artifact-review.md)** — unresolved
  issues and validation gaps; recommendations, not ratified changes.
- **[R6 review of the vocabulary](reviews/R6-vocabulary-review.md)** — an external ontological
  review of the 14 Draft terms, with its **[proposed disposition](reviews/R6-disposition.md)**.
- **[Ontology draft v0.1.0](drafts/BusinessCapabilityOntology_draft_v0.1.0/README.md)** — an
  earlier Turtle ontology, SHACL sketches, fixtures, tests, audit and proposed ADR. Preserved
  byte-for-byte; does not implement v0.4 and is never loaded as ontology.
- [Specification v0.3.0-draft.1](specifications/Business-Capability-Ontology-v0.3.0-draft.1.md)
  — superseded, kept for design provenance.

## Organization

```text
specifications/   the specification in force, and its predecessors
reviews/          review findings and recommendations
src/              the six development stages, each with a README stating its status:
  01_controlled_vocabulary/   the vocabulary YAML and its generated Turtle (ADR-003)
  02_conceptual_models/       Stage 02, in progress; its standard is in docs/standards/
  03_taxonomy/, 04_thesaurus/, 06_knowledge_graph/   not started
  05_ontology/                the BCO modules spec §2 names (headers only until ADR-002)
shapes/           SHACL shapes, and the fixtures built to break them
vendor/           pinned partial extracts of BFO, CCO and BPO, with attribution
drafts/           the v0.1 package, preserved
config/           layout contract, upstream pins, manifests, baseline, digest
tools/            layout, licensing, vendoring, validation and digest tools
site/             the public site's pages, copy and assets (built by tools/site/)
tests/            the suite, including the falsifications
docs/             handoff, development, process, decisions, standards, import record
```

## Foundations

BFO 2020 is the upper ontology. CCO v2.0 supplies Organization, Agent Capability, Skill,
Action Permission and the measurement ICEs. BPO supplies the act types a capability is
realized by.

All three are vendored under [`vendor/`](vendor/) as pinned partial extracts rather than
resolved over the network at validation time. Each carries only the terms this repository
or its specification names plus their named ancestry. The extracts are **not** the upstream
ontologies: every axiom whose object is an anonymous class expression is dropped, so they
cannot be used to claim consistency with BFO, CCO or BPO.

Pins, digests and licences are in [`config/upstream-sources.yaml`](config/upstream-sources.yaml);
what was taken and what was left is in [`config/upstream-extracts.json`](config/upstream-extracts.json);
attribution, which all three licences require, is in [`vendor/NOTICE.md`](vendor/NOTICE.md)
and is checked rather than assumed.

```bash
python tools/ontology/vendor_upstream.py             # offline verify
python tools/ontology/vendor_upstream.py --confirm   # fetch and compare
python tools/ontology/vendor_upstream.py --rebuild   # fetch and rewrite
```

## Checks

```bash
python -m venv .venv && .venv/Scripts/activate      # Windows; source .venv/bin/activate elsewhere
python -m pip install -r requirements-dev.txt
python -m pytest tests/ -q -p no:randomly
```

The same checks run in CI on every push. What each one refuses is in
[`docs/DEVELOPMENT.md`](docs/DEVELOPMENT.md).

## Reference material

Capability frameworks such as BIZBOK, TOGAF and BIAN, and the APQC Process Classification
Framework, are licensed works. This repository cites them and does not redistribute them.
That is enforced rather than described: [`config/repository-layout.yaml`](config/repository-layout.yaml)
declares `docs/Reference/` `tracked: false`, and the suite fails if anything there is ever
committed.

## Provenance

The initial import (2026-10-22) is recorded file by file, with digests, in
[`docs/ARTIFACT-INVENTORY.md`](docs/ARTIFACT-INVENTORY.md). The repository's tooling and
method are carried from the
[Application Requirement Ontology](https://github.com/Skreen5hot/ApplicationRequirementOntology);
decisions are recorded in [`docs/decisions/`](docs/decisions/).

## Licence

[MIT](LICENSE). The vendored extracts carry their upstream licences: BFO CC BY 4.0, CCO
BSD-3-Clause, BPO MIT.
