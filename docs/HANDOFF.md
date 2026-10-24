# Handoff — state of the repository

Written 2026-10-23, in the commit that set the repository up. It is a snapshot: the
numbers below were measured then, and the tests named beside them are what keeps them
true afterwards. Where this file and a test disagree, the test is right and this file is
stale.

---

## 1. The one-paragraph version

This repository develops the **Business Capability Ontology (BCO)**: what an organization
*can* do, alongside the Business Process Ontology's account of what it *does*. The design
is specification v0.4.0-draft.1, which is a draft awaiting ratification. **No BCO term has
been written.** What exists is the setup to write them under: ARO's layout contract,
licensing classification, pinned upstream vendoring (BFO, CCO v2.0 and now BPO), a SHACL
gate with falsification fixtures, a corpus digest, CI, and the method in
`docs/process/PROCESS.md`. The two ontology modules the spec names are empty headers, so
every green check about the ontology is green about nothing — the fixtures are the only
evidence the checks work.

## 2. What is in the tree

| Path | What | Trust |
|---|---|---|
| `specifications/…v0.4.0-draft.1.md` | the spec in force: CD1–CD17, CAP-01–CAP-29, RP-1–RP-10 | DRAFT; nothing normative until ratified |
| `specifications/…v0.3.0-draft.1.md` | superseded predecessor | provenance only |
| `reviews/R5-v0.4-artifact-review.md` | review of v0.4 against the v0.1 package | recommendations, not ratified |
| `drafts/BusinessCapabilityOntology_draft_v0.1.0/` | the earlier `bc:` Turtle package | preserved byte-for-byte; **never loaded** |
| `ontology/apqc-cap.ttl`, `ontology/apqc-cap-desc.ttl` | the two modules spec §2 names | `owl:Ontology` headers only |
| `shapes/` | wellformedness shapes (from ARO) and the vocabulary shapes (P4), each with its fixture | exercised by the fixtures, constraint by constraint |
| `vendor/` | BFO, CCO, BPO partial extracts + NOTICE | generated from pins; digest-checked |
| `config/` | layout contract, pins, manifests, baseline, digest | see `docs/DEVELOPMENT.md` |
| `tools/`, `tests/` | ARO's generic tooling, adapted | the suite and CI |
| `docs/decisions/` | the architect's acts and choices, verbatim | one entry: setup choices |
| `docs/sources/` | citation register of 63 sources on business capability, with the research notes behind it. The entries are data (`register.yaml`), the analysis prose is `register-companion.md`, and the Markdown register is generated from both by `tools/sources/build_register.py` | research input, not evidence; entries marked S, K or L are unverified against their primary text. The register's rules (claim status, quote length and keys, SRC ids, entry count, freshness) are hard failures (`tests/test_sources_register.py`) |
| `vocab/`, `tools/vocab/`, `config/vocab-schema.*`, `requirements-vocab.txt` | the controlled-vocabulary build (ADR-003, P3): authored YAML, generated Turtle in `vocab/generated/`, the LinkML schema and its JSON Schema | the tool and its checks; **no terms yet** (P5). See section 5.10 |
| `communications/` | messages to and from BPO and ARO, under `communications/README.md` | checked by `tools/communications.py`; the vendoring-pin request to BPO was acknowledged (BPO `8f6622c`), and BPO announced a namespace move to `https://fandaws.com/ontology/bpo#` |
| `docs/ARTIFACT-INVENTORY.md`, `docs/artifact-manifest.json` | the 2026-10-22 import record | held to its digests by a test |

## 3. What is ready to rely on

- **The layout contract describes the tree,** both directions (`tests/test_repository_layout.py`).
- **Every tracked file has exactly one licensing disposition,** and nothing unpublishable
  is tracked (`tests/test_licensing.py`). `docs/Reference/` is declared `tracked: false`
  for licensed frameworks — BIZBOK, TOGAF, BIAN, the APQC PCF.
- **The vendored extracts are complete for what is named,** carry no blank nodes, attribute
  every triple to the file it came from, and say in their headers that they are partial
  (`tests/test_upstream_vendoring.py`).
- **The import is what it said it was:** every imported file except the two rewritten at
  setup matches the inventory's digest, and the v0.1 package passes its own
  `SHA256SUMS.txt` (`tests/test_imported_artifacts.py`).
- **The wellformedness shapes fire,** on the fixture, constraint by constraint, and do not
  fire on the positive controls (`tests/test_ontology_checks.py`). With a namespace filter
  pointed elsewhere they select nothing, which is shown rather than assumed, once per
  namespace each shape set filters on (`tests/test_namespace.py`).
- **The vocabulary shapes fire** (P4): each of 47 constraint messages on the fixture case
  named for it, and none on the positive controls (`tests/test_ontology_checks.py`).

## 4. Where the specification stands

v0.4.0-draft.1 (2026-10-22). Its own order for what comes next (§9, §10): ratify **RP-1**
first, because it decides what every G1-T record argues; then RP-2 and RP-3; then the rest;
then ADR-002. CP-0 is "RP-1 to RP-10 ratified; ADR-002 accepted". Nothing has been ratified.

R5 records further blockers: material basis policy, maturity-value encoding, instance
evidence, and migration of BPO existential restrictions.

## 5. What not to trust, and what is not done

### 5.1 The namespace is provisional

BCO terms are to be authored in `https://fandaws.com/ontology/bco#`, the architect's
choice of 2026-10-23 pending **RP-5**; ADR-003 D1 adds four sibling namespaces for the
vocabulary (`bco-metamodel#`, `bco-catalog#`, `bco-sources#`, `bco-agents#`). The spec
writes terms as `ex:` in BPO's `http://example.org/apqc#`. When RP-5 is decided, change
`AUTHORED_NAMESPACES` in `tools/ontology/validate.py`, `NAMESPACES` in
`tools/vocab/build.py`, and every SPARQL filter in `shapes/wellformedness_shapes.ttl` and
`shapes/vocabulary_shapes.ttl` in one commit; `tests/test_namespace.py` fails until all
agree. The module headers and the site's IRI notice name the provisional namespace in prose
too.

### 5.2 BPO is vendored from one file

Only `ontology/apqc-ext.ttl` at BPO `6613194`: 6 act genera. The reality-layer slices, the
catalog and `capabilities_*.ttl` are not here, so BPO process classes the spec names
(`ex:P10020` and others) resolve to nothing. They are listed in
`config/upstream-extracts.json` under `named_by_specification_described_by_no_pinned_file`,
alongside the terms the BCO will mint and the spec's worked-example individuals — 61 in
all, unsorted by kind. Widening BPO means teaching `vendor_upstream.py` to take more than
one url per source; it is not just a config change.

BPO's own namespace is under `example.org`, which is reserved for documentation. That is
BPO's RP-5, not this repository's.

### 5.3 The extracts are partial, deliberately

Every axiom whose object is an anonymous class expression is dropped (34 today). A reasoner
over these files derives less than one over the upstream, and they cannot support a
consistency claim against BFO, CCO or BPO. No reasoner runs here at all yet; the spec's
Gate D (ELK) has no counterpart.

### 5.4 Nothing about the ontology has been measured

The SHACL ladder runs, conforms, and has a baseline of zero — over 8 triples of module
headers. The corpus digest is a digest of those headers. Both are set up so that the first
real term is measured on the commit that adds it; neither says anything about the BCO yet.

### 5.5 A spec fact the extracts confirm

CCO v2.0 puts Organization Capability under *realizable entity*, not *disposition*. CD3's
explicit `rdfs:subClassOf obo:BFO_0000016` is therefore an assertion the BCO makes, not one
it inherits. Pinned by `test_the_extracts_say_what_cd1_and_cd3_assume`.

### 5.6 Not carried over from ARO

The act tool and ratification queue (`tools/act.py`), the spike, WS-3, the FX-SEAM
fixtures, the corpus index, and the jsonschema/owlrl pins. Each is ARO-specific or has
nothing to exercise it here. The act tool is the one most likely to be wanted, once
RP/CD items are being ratified in volume.

### 5.7 Fixed here, still present in ARO

ARO's `vendor_upstream.py` partitions extract triples by subject namespace, so CCO's own
annotations on BFO terms land in the BFO extract under BFO's licence (4 `skos:scopeNote`
triples against these pins). This repository's copy attributes each triple to the file
that asserts it. ARO's has not been changed.

### 5.8 The public site is new, and less reviewed than ValueNet's

The site (https://skreen5hot.github.io/Business-and-Agent-Capabilities-Ontology/) is built by `tools/site/build_site.py`, checked by
`tools/site/check_site.py` and `tests/test_site.py`, and deployed by
`.github/workflows/pages.yml`. Its stylesheet and explorer scripts are ValueNet's, which
were contrast-checked and reviewed in four browser engines there. What was **not**
carried over, and so has not been done for this site:

- ValueNet's browser review (`tools/site/browser_review.py`: four engines, three
  viewports, a committed record) and its accessibility suite. This site was looked at in
  one engine (the Claude desktop app's browser) at desktop and phone width, by eye.
- Running `ranking.js` under Node in the tests, as ValueNet does. The ranking code is
  ValueNet's, unchanged apart from its global name, and is untested here.
- A models page. ValueNet's diagrams are drawn from its ontology; the BCO has no
  authored term to draw yet.

The stylesheet and the two scripts keep ValueNet's `SPDX-License-Identifier: Apache-2.0`
headers, and the tools carried from ARO keep theirs, while this repository's `LICENSE` is
MIT and the licensing tool classifies all of them as MIT. Both source projects are the
same author's, so this is an owner decision rather than a conflict -- but it is
undecided, and the headers and the classifier currently disagree.

### 5.9 The citation register is data, and only data

P1 of the controlled-vocabulary plan made `docs/sources/register.yaml` the source of
truth for the 63 entries, with the Markdown generated from it (ADR-003 D6, which is
still PROPOSED). What it does not do yet:

- **RDF since P3, no shape yet.** `tools/vocab/build.py` generates the `bcos:` records
  ADR-003 D8 describes into `vocab/generated/bco-sources.ttl` (id, citation, claim
  statuses); the shape that checks them is P4.
- **Claims are one per verified part, not per assertion.** Each claim carries the
  verification status the Markdown gave the entry (83 claims across 63 entries), with a
  `scope` and a `note`. It has no locator and no key. A `departs-from` in P3 that needs
  a claim about, say, BACM's OrgUnit can only cite the entry's V claim as a whole until
  claims are split.
- **The companion's quoted phrases are not keyed.** The analysis prose quotes a few
  short phrases (several repeat an entry's quote); the 15-word and key checks cover
  entry quotes only.
- **Two entries broke the one-quote rule** when converted (SRC-GOV-01, SRC-OG-02). The
  second quotation in each was paraphrased; the PR that made the register data lists
  both.

### 5.10 The vocabulary tool exists; the vocabulary does not (P3)

`tools/vocab/build.py` turns `vocab/{metamodel,catalog,agents}.yaml` into five Turtle
files in `vocab/generated/`, committed and compared with a fresh build in CI and in
`tests/test_vocab.py`. ADR-003 D1-D9 are enforced there; `docs/DEVELOPMENT.md` "The
controlled vocabulary (P3)" says how. State at P3:

- **No terms.** `vocab/metamodel.yaml` and `vocab/catalog.yaml` hold empty lists. The
  generated metamodel and catalog files carry their scheme and nothing else. Every check
  is exercised by fixtures built in the tests, not by real records.
- **Section 4 has 9 concrete rows**, not the 8 the approved plan's P5 row names:
  Business Capability, the seven description-layer classes, and Authorization Record.
  Two template rows are excluded by rule. The coverage check (`D4-row-uncovered`) starts
  with the first metamodel record, so P5 brings all nine.
- **Inside the gate since P4.** The vocabulary is not an `ontology-module`, so it is
  not in the corpus digest; since P4 it is in the SHACL data graph and on the site. See
  section 5.11.
- **`bco:` holds 19 annotation properties and `bco:PCFCode`,** declared in the generated
  `vocab/generated/bco-vocabulary.ttl`, as ADR-003 D1 places them. They are not in
  `ontology/`, and no class is minted.
- **The PCF lexical form is assumed** (five digits), not checked against the PCF 7.4
  workbook, which is licensed and not here.
- **D3 history is declared, not verified.** A record's `revises` names the previous
  record's digest and the graph links the two; nothing yet checks that digest against
  the file's git history.
- **LinkML runs in its own CI job** (`vocab-schema`, `requirements-vocab.txt`, 91
  packages). How the pin enters the repository is proposed on the P3 pull request, and
  the architect's acceptance decides it.

### 5.11 The vocabulary is checked and published; there is still nothing in it (P4)

P4 widened `AUTHORED_NAMESPACE` to the list `AUTHORED_NAMESPACES` (ADR-003 D1), moved the
wellformedness concept target to `bco-metamodel#` and `bco-catalog#`, put the generated
vocabulary into the validation data graph (layout `vocabulary: true`), added
`shapes/vocabulary_shapes.ttl` with its fixture, and added the site's Vocabulary page.
State at P4:

- **The concept shapes conform vacuously.** There is no metamodel or catalog concept
  until P5; only the fixture shows those 21 constraints work.
- **The source-record and agent shapes run on real data** -- 63 records, 2 agents -- and
  find nothing. A test strips every citation in memory to show all 63 are selected.
- **Baseline:** `validation.vocabulary` 0 and `validation.wellformedness` 0 authored
  findings.
- **Not in the corpus digest,** deliberately: the vocabulary is its own generated
  measurement, and the sources graph would tie the ontology's digest to the register.
- **What the shapes do not check:** the PCF lexical form (assumed by the build); that a
  ratification act exists and lists the record (the build checks that against the
  repository's history); `prov:wasRevisionOf` chains and record digests;
  `dcterms:created`; `skos:broader` pointing at a catalog concept; a `skos:Concept` minted
  in `bco#`, which is outside both populations and is reported by neither shape set.
- **The site page** reads the generated Turtle, never the YAML; it shows citations only
  for register entries a concept cites, so today it shows none. Vocabulary concepts are not
  in the explorer's term index.

## 6. Outside the repository

- **Nothing is pushed.** The import (`b4d4493`) and the setup commit are local to the
  architect's machine until pushed.
- **CI has not run.** `.github/workflows/checks.yml` is ARO's, adapted; the first push is
  its first run. The weekly job needs the network to reach GitHub raw content for three
  upstreams.
- **ARO and BPO are reference clones** beside this one under `source/repos/`; nothing here
  depends on them being present.

## 7. Suggested next steps

1. Push, and watch the first CI run.
2. Ratify RP-1 (spec §10), and record it in `docs/decisions/`.
3. Write the CAP shapes the spec has fixtures for, each with its negative fixture, before
   the terms they constrain — the spec says a requirement stays DRAFT until its falsifying
   fixture exists.
4. Decide whether the BPO slices need vendoring before the first realization index is
   written (CD4, RP-2): the index points at BPO process classes, and today none resolve.

## 8. Where to look

| For | Read |
|---|---|
| how to run things | `docs/DEVELOPMENT.md` |
| why it is built this way | `docs/process/PROCESS.md` |
| the design | `specifications/Business-Capability-Ontology-v0.4.0-draft.1.md` |
| what was decided, by whom | `docs/decisions/` |
| what is vendored, and what is not | `config/upstream-extracts.json`, `vendor/NOTICE.md` |
