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
| `reviews/R6-vocabulary-review.md`, `reviews/R6-disposition.md` | external review of the 14 Draft vocabulary terms, filed verbatim; the disposition of it, accepted 2026-10-24 | the review is the reviewer's; the disposition was accepted (section 5.13) |
| `reviews/R7-turtle-artifact-review.md`, `reviews/R7-disposition.md` | external review of the five generated vocabulary Turtle files, filed verbatim; the proposed disposition of it | the review is the reviewer's; Finding E is decided (`docs/decisions/2026-10-25-r7-genus-decision.md`), the rest is a proposal until the architect accepts it (section 5.14) |
| `drafts/BusinessCapabilityOntology_draft_v0.1.0/` | the earlier `bc:` Turtle package | preserved byte-for-byte; **never loaded** |
| `src/` | the six development stages, each directory with a README stating its status (section 5.15) | 01 and 05 hold the files below; 02 is in progress; 03, 04, 06 are empty |
| `src/05_ontology/apqc-cap.ttl`, `src/05_ontology/apqc-cap-desc.ttl` | the two modules spec §2 names | `owl:Ontology` headers only |
| `shapes/` | wellformedness shapes (from ARO) and the vocabulary shapes (P4), each with its fixture | exercised by the fixtures, constraint by constraint |
| `vendor/` | BFO, CCO, BPO partial extracts + NOTICE | generated from pins; digest-checked |
| `config/` | layout contract, pins, manifests, baseline, digest | see `docs/DEVELOPMENT.md` |
| `tools/`, `tests/` | ARO's generic tooling, adapted | the suite and CI |
| `docs/decisions/` | the architect's acts and choices, verbatim | one entry: setup choices |
| `docs/standards/` | the ontology development standards the architect supplies, verbatim | one: Stage 02, Conceptual Modeling (2026-10-25) |
| `docs/sources/` | citation register of 63 sources on business capability, with the research notes behind it. The entries are data (`register.yaml`), the analysis prose is `register-companion.md`, and the Markdown register is generated from both by `tools/sources/build_register.py` | research input, not evidence; entries marked S, K or L are unverified against their primary text. The register's rules (claim status, quote length and keys, SRC ids, entry count, freshness) are hard failures (`tests/test_sources_register.py`) |
| `src/01_controlled_vocabulary/`, `tools/vocab/`, `config/vocab-schema.*`, `requirements-vocab.txt` | the controlled-vocabulary build (ADR-003, P3): authored YAML, generated Turtle in `src/01_controlled_vocabulary/generated/`, the LinkML schema and its JSON Schema | the tool and its checks; since P5, 9 metamodel and 5 catalog concepts, all **Draft**. See sections 5.10 to 5.12 |
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
- **The vocabulary shapes fire** (P4; 51 since R6, 75 since R7): each constraint message on
  the fixture case named for it, and none on the positive controls
  (`tests/test_ontology_checks.py`).
- **The concept shapes select the real concepts** (P5): with every definition and
  departure note stripped in memory, each of the 14 concepts and each `departs-from`
  reference is reported (`test_the_real_concepts_and_departures_are_selected`).
- **The claim and record shapes select the real claims and records** (R7): with every
  claim status, then every record digest, stripped in memory, each of the 83 claims, each
  `departs-from` reference, and each current or revising record is reported
  (`test_the_real_claims_and_records_are_selected`).

## 4. Where the specification stands

v0.4.0-draft.1 (2026-10-22). Its own order for what comes next (§9, §10): ratify **RP-1**
first, because it decides what every G1-T record argues; then RP-2 and RP-3; then the rest;
then ADR-002. CP-0 is "RP-1 to RP-10 ratified; ADR-002 accepted". Nothing has been ratified.

R5 records further blockers: material basis policy, maturity-value encoding, instance
evidence, and migration of BPO existential restrictions. R6 (section 5.13) adds wording
points for spec v0.5 and sends its material-basis finding to RP-1 and its admissibility
finding to RP-10.

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
- A models page drawn from the ontology, as ValueNet's is. The BCO has no authored term
  to draw yet. The Models page that exists (`models/`, since Stage 02) renders the
  conceptual models instead: their Mermaid source, drawn in the browser by a pinned,
  vendored Mermaid 11.4.1 (`config/site-vendor.yaml`, `vendor/site/`), loaded on that
  page only. It was checked in one engine (the desktop app's browser), dark scheme, by
  eye.

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
  ADR-003 D8 describes into `src/01_controlled_vocabulary/generated/bco-sources.ttl` (id, citation, claim
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

`tools/vocab/build.py` turns `src/01_controlled_vocabulary/{metamodel,catalog,agents}.yaml` into five Turtle
files in `src/01_controlled_vocabulary/generated/`, committed and compared with a fresh build in CI and in
`tests/test_vocab.py`. ADR-003 D1-D9 are enforced there; `docs/DEVELOPMENT.md` "The
controlled vocabulary (P3)" says how. State at P3:

- **No terms (at P3; P5 added them, section 5.12).** `src/01_controlled_vocabulary/metamodel.yaml` and `src/01_controlled_vocabulary/catalog.yaml` held empty lists. The
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
  `src/01_controlled_vocabulary/generated/bco-vocabulary.ttl`, as ADR-003 D1 places them. They are not in
  `ontology/`, and no class is minted.
- **The PCF lexical form is assumed** (five digits), not checked against the PCF 7.4
  workbook, which is licensed and not here.
- **D3 history is declared, not verified** (at P3; since R7 the build finds each revised
  record in git history and publishes the commit that introduced it, section 5.14). A
  record's `revises` names the previous record's digest and the graph links the two; at
  P3 nothing checked that digest against the file's git history.
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
  repository's history); `prov:wasRevisionOf` chains and record digests (checked since
  R7: every revision target described, every digest the one its IRI names);
  `dcterms:created`; `skos:broader` pointing at a catalog concept; a `skos:Concept` minted
  in `bco#`, which is outside both populations and is reported by neither shape set.
- **The site page** reads the generated Turtle, never the YAML; it shows citations only
  for register entries a concept cites, so at P4 it showed none. Vocabulary concepts are not
  in the explorer's term index.

### 5.12 The pilot vocabulary is written, and none of it is ratified (P5)

P5 filled `src/01_controlled_vocabulary/metamodel.yaml` and `src/01_controlled_vocabulary/catalog.yaml` for the architect to review on
the site. State at P5:

- **14 concepts, all Draft.** 9 metamodel concepts, one per concrete section 4 row, so
  `D4-row-uncovered` now runs on every build; 5 catalog concepts: Strategic Planning,
  Treasury Management, Competitive Analysis, Business Model Governance and Customer
  Experience Management. No ratification act exists. Ratifying them is the architect's act
  (ADR-003 D5: an explicit list of IRIs, each with its `record_sha256` from
  `tools/vocab/build.py --digest`); the P5 pull request lists all 14.
- **Metamodel definitions are section 4's.** The records carry only provenance. The spec is
  still a draft, so these concepts wrap draft text.
- **Every record cites the register.** Claims cited are at V or P; no S or K claim is
  cited. The organization-only bearer is recorded as `departs-from` UAF 1.3, BACM 1.1
  (OrgUnit), VDML 1.1, NAF v4.1, IOF Core and ISO 19440 3.6; the member-agent basis departs
  from NAF's Capability Configuration; the Capability Map departs from NAF's C1 taxonomy
  view; the Maturity Rating departs from ISO/IEC 33020, CMMI (homonyms) and the UFO
  capability level; the Capability Target departs from CDD/CaaS. CCO is `adapted-from` for
  Business Capability's genus; IOF Core, Beverley et al. and BFO are `consistent-with`.
  ArchiMate (S) is not cited. Where a note records no page or clause, the locator says so.
- **Catalog definitions are original** and pass the quote tripwire. Each takes Business
  Capability as its genus in prose; the `genus` field names `cco:ont00000568`, because
  `bco:BusinessCapability` is not minted and the field must be a vendored BFO/CCO class.
- **No PCF notation.** At BPO `6613194` no PCF 7.4 catalog node designates any of the five
  capability classes; every candidate node (for example `ex:PCF_10734`, `ex:PCF_19945`,
  `ex:PCF_20950`, `ex:PCF_19959`) designates a process class. So the five-digit
  `bco:PCFCode` form is still unconfirmed by a real notation.
- **No `broader`, no `designates_class`:** CD9 needs a review for any link between
  capability classes, and no capability class has passed G1-T (CD3).
- **Competitive Analysis** is the organizational reading. BPO's
  `ex:CompetitiveAnalysisCapability` is an Agent Capability borne by an analyst, which
  section 9 sends to Skill and out of BCO scope; the catalog concept does not designate it.
- **Validation on real data:** `validation.vocabulary` 0 and `validation.wellformedness`
  0 authored findings, over 14 concepts. The baseline did not change.
- **Not changed, and now stale:** the site's status page still says "Authored terms
  checked: 0" and that, with no BCO term written, every shape set conforms vacuously
  (`tools/site/build_site.py`, which counts ontology terms only). The vocabulary rung now
  runs on real concepts. Fixing that sentence is a tool change and was left out of P5.

### 5.13 Review R6 received and answered by a proposed disposition

R6, an external ontological review of the vocabulary page after P5, was received on
2026-10-24 and is filed verbatim as `reviews/R6-vocabulary-review.md`. The reviewer saw the
page, not the specification or the repository. `reviews/R6-disposition.md` answers it in
39 rows: 20 answered by spec v0.4, 8 accepted and done on the R6 branch, 6 accepted for
spec v0.5, 3 deferred to ratification points, 2 to acceptance checkpoints. Every row is a
proposal until the architect accepts the pull request. Both files are on the site's
Reviews page, which now renders every `reviews/*.md`.

**Done on the R6 branch:**
- **The five catalog definitions are general** (R6 section 3): each now says what the
  capability is for, in the form "A business capability, inhering in an organization, that
  is realizable in planned acts by which that organization …", with no enumerated list of
  practices. Competitive Analysis drops "rather than resting on one analyst's skill alone",
  which contradicted CD2's fragility bullet. Business Model Governance drops the CD5
  development clause. Each record has a `change_note` and a `revises` pointing at its P5
  record.
- **consistent-with states its support** (section 6.1): `support: definitional |
  contextual`, required on consistent-with and refused elsewhere, through the schema, the
  build (`bco:support`, the 20th `bco:` annotation property), the shapes (4 new
  constraints), the site and the tests. Of the 41 consistent-with references, 5 are
  definitional, all in the metamodel: IOF Core, Beverley et al. and BFO for Business
  Capability, VDML for the Sourcing Statement, BMM for the Target-State Specification. The
  other 36, including all 16 in the catalog, are contextual: no source in the register
  backs any of the five catalog definitions specifically.
- **A ratification act records its basis** (section 6.3): the `bco-ratification` block
  now requires `approvals` (editorial and ontological, each a declared `prov:Person`) and
  `validation` (a full commit main reaches, and the gate commands that passed there).
  This adds to the format P3 accepted. ADR-003 D5's content, explicit IRIs each with its
  record digest, is unchanged.

**Deferred:**
- **RP-1:** F2, the material basis. The register's SF-03 already flagged the formal half:
  the basis must be an aggregate of member agents, not an "arrangement" or a "set".
- **RP-10:** F1, the criteria for admitting a capability type as an organization-borne
  disposition (G1-T).
- **Spec v0.5 (section 4 text, ADR-003 D4):** the section 4 rule that each capability class
  states its realization index in its definition; the Capability Map's descriptive versus
  directive entries; what a maturity rating measures; whether the Sourcing Assessment's
  three criteria are required; the Sourcing Statement as a description, not the
  arrangement; how a Target-State Specification incorporates its targets. Also for v0.5 and
  RP-10: G1-T question 3 uses the wording that was removed from Competitive Analysis.
- **CP-1 to CP-3:** the reasoner (test 10, Gate D2 at CP-2), and running R6's tests as a
  gate.
- **Accepted as an offer:** a review of `src/01_controlled_vocabulary/generated/` Turtle. Sending it is the
  architect's call.

**Still Draft, all 14, with new record digests.** No digest from the P5 pull request is
valid any more, because every record changed: the catalog definitions, and `support` on
every consistent-with reference. Nothing was ratified, so no act is broken. The digests
are listed in the R6 pull request; `tools/vocab/build.py --digest <curie>` prints any of
them.

**Not done:** the review's temporal-context point on assessments (§4.2) has no row of its
own; the spec's Known limits (0.4) already list "no temporal qualification of has
capability". Whether the catalog revisions are editorial (same IRI) or a change of meaning
(new IRI, ADR-003 D3) is the architect's call; they are treated as editorial here. The
SRC-FO-01 locators still mention the 2026 `develop` file.

### 5.14 Review R7 received and answered by a proposed disposition

R7, an external formal review of the five generated Turtle files after the R6 response, was
received on 2026-10-25 and is filed verbatim as `reviews/R7-turtle-artifact-review.md`. It
finds them an acceptable SKOS vocabulary and provenance export, and not yet a formal
BFO/CCO OWL ontology. The reviewer had the Turtle and the BFO/CCO references only: no
generator, YAML, specification or git history. The architect decided Finding E
(`docs/decisions/2026-10-25-r7-genus-decision.md`) and said "Proceed" on the rest.
`reviews/R7-disposition.md` answers the review in 26 rows: 11 accepted and done on the R7
branch, 4 answered by spec or ADR-003, 5 for spec v0.5, 2 deferred to the OWL layer
(C, formal axioms; D, type versus instance reference, already designed in CD14 with
`ex:concernsType`), 2 to RP-1 and RP-10, 2 noted.

**Done on the R7 branch:**
- **Claims are resources** (Finding A). `bco-sources.ttl` publishes `bcos:<SRC id>-claim-<n>`
  for each of the register's 83 claims, linked by `bco:hasClaim`, with `bco:claimIndex`,
  `bco:claimStatus` and, where the register has them, `bco:claimScope` and `bco:claimNote`.
  `bco:citesClaim` points at the claim, not an integer. The record's unordered
  `bco:claimStatus` bag is gone.
- **Revision chains resolve** (Finding B). Every record a current record revises is
  described: a `prov:Entity` with `bco:recordSha256`, `bco:recordCommit` (the commit that
  introduced it, found in git history) and its own `prov:wasRevisionOf`. 19 prior records:
  14 of P5 at `76b47fc`, 5 of R6 at `137ce61`. The build needs the full history; a shallow
  clone is `D3-history-shallow`. Branches must keep being merged with a merge commit, or
  a branch's introducing commit leaves `main` and the committed Turtle goes stale. How to
  verify a digest against the YAML is in `docs/DEVELOPMENT.md` and in the vocabulary's
  comments.
- **Genus and ancestor** (Finding E). Each catalog concept's `bco:definitionGenus` is the
  immediate genus `bco:BusinessCapability`; the new `bco:foundationalAncestor` records
  `cco:ont00000568`. Nothing is minted: `bco:BusinessCapability` is still declared nowhere,
  and the build emits no `owl:Class` or `rdfs:subClassOf`.
- **The catalog wording** (section 4), as editorial revisions under D3: Treasury Management
  loses "ensures"; Business Model Governance "decides whether and how"; Strategic Planning
  loses "long-range"; Competitive Analysis's competitors are agents; Customer Experience
  Management "understands or shapes" (the disjunction is a choice the change note states
  and the architect may reverse).
- **What the RDF cannot enforce is said** (Findings F and G), as `rdfs:comment`s on
  `bco:PCFCode` and `bco:lifecycleStatus`.
- **`bco:` holds 26 annotation properties and `bco:PCFCode`.** Six were added:
  `hasClaim`, `claimIndex`, `claimScope`, `claimNote`, `recordCommit`,
  `foundationalAncestor`. No object property, no class.
- **26 new shape constraints, 2 retired** (75 in all), each new one with its fixture case
  and positive control; the retired two were the source record's `bco:claimStatus` rules.

**Still Draft, all 14.** The 5 catalog records have new digests (listed in
`reviews/R7-disposition.md`); the 9 metamodel records are unchanged.

**Not done:** the OWL layer (C, D, section 6) and the spec v0.5 wording rows; ADR-003 D4
still says a catalog definition has "a BFO/CCO genus", which since R7 is the foundational
ancestor (a ratified ADR changes only through a new one); the register has no claim text,
so a claim resource carries none.

### 5.15 The stage layout (2026-10-25)

The architect adopted six development stages
(`docs/decisions/2026-10-25-stage-02-choices.md`). A mechanical move put `vocab/` at
`src/01_controlled_vocabulary/` and `ontology/` at `src/05_ontology/`, and gave each
stage directory a README stating its status. No content changed: the generated Turtle
differs only in the paths it names (its three `From:` headers, and the `rdfs:comment`s on
`bco:recordCommit` and `bco:recordSha256`, which now name the old path beside the new one,
because every prior record so far was written at the old one), the corpus digest's ground and shape digests are
unchanged, and every prior record still resolves to the commit it did before. The
prior-record search in `tools/vocab/build.py` now follows the move, reading each commit's
YAML where that commit's own layout contract puts it
(`test_a_prior_record_is_found_across_a_move_of_the_yaml`).

**Not moved:** `shapes/`, `config/`, `docs/`, `tools/`, `vendor/`, `specifications/`,
`reviews/`, `communications/`, `drafts/`, `site/`, `trials/`. Records, ADRs, reviews and
communications written before the move keep the old paths, as written.

**CM-01 (drafted, not approved).** `src/02_conceptual_models/CM-01-business-capability.md`,
0.1.0-draft.2 (answering review R8): five patterns (capability and bearer; realization by BPO acts; description
layer; sourcing and authorization; catalog, specialization and coverage), 6 Mermaid
diagrams, 32 concepts, 39 relationships, CQ-1 to CQ-14 traced. RP-1 and RP-10 are its
decision points DP-1 and DP-2, each with options, the R6 and R7 critiques, register
evidence (SF-01 to SF-06) and a drafter's recommendation that is not a decision.
**Next:** the architect decides DP-1, then DP-2; each is recorded verbatim in
`docs/decisions/` with the model's digest, the model is revised to match, and
specification v0.5 follows.

**Stage 02 tooling.** `tools/conceptual/check_models.py` holds every
`src/02_conceptual_models/CM-*.md` to a format contract: the standard's ten sections in
order, a Mermaid diagram per pattern with a reading after each, every diagram node a
described concept and every edge a described relationship (and none left undrawn), CQ
traceability equal to the specification's section 7, decision points, open questions
marked carried-forward or blocking, and no approval while anything blocks it. It checks
completeness and internal references only; conceptual adequacy is the architect's review
(standard section 7). The site's Models page renders each model, with its approval state
read from its own Review status table.

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
