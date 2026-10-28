# Development

How to work in this repository. For *why* it is built this way, read
`docs/process/PROCESS.md`. For what is actually here and what is not, read
`docs/HANDOFF.md` first.

The tooling is carried from the Application Requirement Ontology (ARO) and
adapted; where it differs, this file says so.

---

## Setup

Python 3.12. Dependencies are pinned exactly, and the pinning is verified the one way it
can be — by installing into an empty environment and running the suite there:

```bash
python -m venv .venv
.venv/Scripts/activate          # Windows;  source .venv/bin/activate elsewhere
python -m pip install -r requirements-dev.txt
python -m pytest tests/ -q -p no:randomly
```

`tools/` is deliberately not an installed package. It is a directory of
scripts that the tests import by path, so there is no build step between
writing a tool and testing the tool that ships.

The suite takes seconds today, because the authored corpus is two empty
module headers. It will not stay that way: in ARO the same suite takes six
to eleven minutes over 63,000 triples.

---

## The checks, and what each one actually asserts

Run in this order; each is cheap until the last.

```bash
python tools/layout.py                        # the contract describes the tree
python tools/licensing/disposition.py         # one disposition per tracked file
python tools/licensing/disposition.py --check # nothing unpublishable is tracked
python tools/ontology/vendor_upstream.py      # the extracts cover what is named
python tools/ontology/validate.py --gate      # no new ontology findings
python tools/ontology/corpus_digest.py        # measure the authored ontology
python tools/ontology/validate.py             # the SHACL ladder
python tools/sources/build_register.py        # the citation register's rules; Markdown is fresh
python tools/vocab/build.py                   # ADR-003's vocabulary rules; the Turtle is fresh
python tools/conceptual/check_models.py       # every conceptual model meets its format contract
python tools/site/vendor_assets.py            # the vendored site assets match their pins (offline)
python tools/inventory/harvest_bpo.py         # the inventory's pins, rights rule and admission guard (offline)
python tools/inventory/rights.py              # the I-2a rights review: pins, no catalog content, short quotes (offline)
python tools/inventory/harvest_federal.py     # the I-2c federal catalogs: digests, snapshot, rights posture, admission guard (offline)
python -m pytest tests/ -q -p no:randomly     # all of the above, plus the falsifications
```

| Command | What it will refuse |
|---|---|
| `layout.py` | a declared component whose path does not exist; two components sharing an id; a generated artifact that names no generator and does not admit it has none |
| `disposition.py` | a file matching two rules, or none; an adjudication naming no file; a `LICENSE` naming zero or two recognised licences |
| `disposition.py --check` | a tracked file that may not be redistributed; a vendored extract whose required attribution is missing from `vendor/NOTICE.md`, a vendored site asset whose attribution is missing from `vendor/site/NOTICE.md`, or an inventory entries file (`source-evidence`) whose source's attribution is missing from the notice its pin names (`docs/sources/inventory/NOTICE.md` for I-1, `NOTICE-federal.md` for I-2c) |
| `vendor_upstream.py` | an upstream term the corpus, the shapes or the specification names that no extract describes (spec terms the last build recorded as unresolvable excepted); an extract whose digest is not what the manifest records |
| `validate.py --gate` | a rung with more findings than `config/validation-baseline.json` records, a rung with fewer that has not been re-recorded, a shape set the fixture does not exercise, a rung blocked on missing vocabulary, a violation against a vendored term, and a rung the baseline does not mention |
| `validate.py --record` | raising any recorded count without `--accept-regression "<why>"`. Lowering is always free |
| `vocab/build.py` | everything in ADR-003 a schema cannot say: an unreadable section 4, a metamodel definition, an authored status, a record naming no row (and, once one record exists, a row with no record), a broken decision citation or act (including an act without both approvals by declared persons, or without a reachable validation commit and a non-empty gate list), a record changed after ratification, an unknown source, a missing locator, a weak or missing departure claim, a consistent-with with no support or support on another relation, a definition sharing six words with a registered quote, a malformed notation, a catalog genus that is neither a vendored BFO/CCO class nor a metamodel concept's designated class, a foundational ancestor that is not a vendored BFO/CCO class above that genus, a record that revises another in a shallow clone, an undeclared agent, a status act not by a Person, and committed Turtle that is not a fresh build |
| `check_models.py` | a conceptual model (`src/02_conceptual_models/CM-*.md`) missing a title line, a Field/Value row, any of the ten section headings or their order; a pattern without a Mermaid diagram; a diagram without a `**Reading the diagram.**` paragraph after it, outside the flowchart subset, with a node label that is not a section 4 concept heading or an edge label that is not a section 5 Relationship, and a concept or relationship no diagram shows; a concept missing a section 4.2 bullet; a malformed relationship table; a decision point without exactly one `**Decision:**` (pending, or an existing `docs/decisions/` record) or two options; a traceability table whose CQ set is not the specification's section 7 set, or that names an undefined pattern, concept or RL id; an unnumbered assumption or open question, or an open question without exactly one of `*Carried forward.*` / `*Blocks approval.*`; approval while a decision is pending or a question blocks it; a `cco:`/`obo:`/`ex:` token not in the vendored extracts or a `bcom:`/`bcoc:` token not in the generated vocabulary (diagrams exempt); any other file in the models directory. Conceptual adequacy is not its question (standard section 7) |
| `vendor_assets.py` | a vendored site asset (`vendor/site/`) whose sha256 is not its pin in `config/site-vendor.yaml`, a LICENSE that does not support the pinned SPDX id, and a `vendor/site/NOTICE.md` that is not a fresh generation. `--fetch` additionally refuses a tarball whose npm integrity or shasum is not pinned, a host other than registry.npmjs.org, and any member the pin does not list |
| `harvest_bpo.py` | inventory outputs (`docs/sources/inventory/`) whose recorded input digests are not the pins in `config/inventory-sources.yaml`; an entry missing a field, of an unknown kind, with an id not `INV-BPO-<local name>-<kind>` or a commit other than the pin; a withheld entry carrying label or definition text, an entry with APQC evidence or a PCF code that is not withheld; findings counts that disagree with the entries; a stale `NOTICE.md`; and, in that directory, any file not YAML or Markdown, any RDF serialization, any IRI in `AUTHORED_NAMESPACES`, any ratification key. `--rebuild`/`--confirm` additionally refuse a host other than raw.githubusercontent.com, a URL not naming its commit, a digest other than the pin, a baseline other than the vendored BPO pin, and CCO anchors whose pinned labels differ |
| `rights.py` | a `docs/sources/inventory/rights.yaml` outside its closed schema; a repeated source, a register id the register does not hold, a status other than evidence-complete, gap or deferred, terms other than unambiguous, ambiguous or not-established; a gap or deferral without a gap reason, a complete source with one, ambiguous terms with no open question; evidence without a sha256, retrieval date or what was checked, on a host other than the rights holders' (obamawhitehouse.archives.gov, ussm.gsa.gov, www.gsa.gov; apqc.org only as browser-read text with its normalisation), BPO evidence without a full commit; a catalog field outside the findings block or a PCF, FIBF or BRM code anywhere; a quote over 15 words, a quotation mark outside a quote, a quote from unlisted evidence; a decision point with one option; an `architect_decision` that does not point at an existing decision record; an authored-namespace IRI, RDF text or a ratification key. `--confirm` additionally refuses any other host and any document whose refetched bytes (never the cache's) or archive members no longer have the pinned digest |
| `harvest_federal.py` | federal inventory outputs (`feaf-brm-entries.yaml`, `fibf-entries.yaml`, `fibf-business-capabilities.yaml`, `fibf-snapshot.yaml`) recording a digest other than `rights.yaml`'s for the documents `config/inventory-federal-sources.yaml` names; a BRM output without both documents (BRM-2 c); a snapshot that is not exactly `rights.yaml`'s 40 FIBF candidates in order; a document `rights.yaml` marks with a MITRE notice listed as harvested, or a withheld document carrying anything beyond its locator, digest and status; an entry from a document the snapshot does not mark harvested, missing a field, of an unknown kind or level, with an id its own fields do not produce, without a locator (sheet and row, page, or HTML line), or with text in a withheld field; a FIBF business capability without its homonym flag; counts that disagree with the entries; any data value naming ITIL, TBM, AXELOS, PeopleCert or Technology Business Management; a stale `NOTICE-federal.md`; and the I-1 admission guard over the directory. `--rebuild`/`--confirm` additionally refuse a digest other than the pin, a host other than ussm.gsa.gov, www.gsa.gov and obamawhitehouse.archives.gov, a workbook whose header cells moved, a mapping column (FIBF-2 a) read into entries, and any harvested text equal to a MITRE-marked workbook's |
| `build_register.py` | a claim status other than exactly V, P, S, K or L; a quote over 15 words, with a missing, malformed or duplicate key, placed other than once, or a second quote in one entry; a quotation mark typed into entry prose; an SRC id in any tracked file that names no entry; an entry count other than 63; a committed Markdown register that is not a fresh generation |

`validate.py` writes a report with `-o config/validation-report.json`. That file is
gitignored on purpose: it is a measurement, not a pin. `config/corpus-digest.json`
**is** committed, because a test compares it against a fresh measure — regenerate it
in the commit that changes the ontology:

```bash
python tools/ontology/corpus_digest.py -o config/corpus-digest.json
```

---

## Writing the first BCO term

The two modules spec v0.4 §2 names exist as `owl:Ontology` headers only:

| File | Will hold |
|---|---|
| `src/05_ontology/apqc-cap.ttl` | Business Capability, the capability classes with their `enablesProcess` index, reviewed unions |
| `src/05_ontology/apqc-cap-desc.ttl` | the seven description-layer classes and the Authorization Record |

Before the first term is minted:

1. **ADR-002 is ratified.** The spec is a draft; nothing in it is normative until the
   architect ratifies it (RP-1, RP-2, RP-7 to RP-10 pending). Record the act in
   `docs/decisions/`, and land the ADR itself under `docs/adr/` (spec §2).
2. **The namespace is the provisional one.** Author in `https://fandaws.com/ontology/bco#`,
   not the spec's `ex:`. It is the first of `AUTHORED_NAMESPACES` in
   `tools/ontology/validate.py`, ADR-003 D1's five (the other four are the vocabulary's,
   minted only by `tools/vocab/build.py`). The shapes' SPARQL filters name the same strings
   inside literals -- `shapes/wellformedness_shapes.ttl` names `bco#`, `bco-metamodel#` and
   `bco-catalog#`; `shapes/vocabulary_shapes.ttl` names all five -- and
   `tests/test_namespace.py` requires the list, the shapes and `tools/vocab/build.py`'s
   `NAMESPACES` to agree, and shows, filter by filter, that a stale string selects nothing.
   When RP-5 mints permanent namespaces, change all of them in one commit.
3. **BPO terms are referenced, not redeclared.** A realizing act type is an `ex:` IRI
   from the vendored BPO extract. If the term you need is not in
   `vendor/bpo/bpo-ext-bco-extract.ttl`, re-vendor (below); if it lives in a BPO file
   that is not vendored at all (slices, catalog), that is the widening listed in
   `docs/HANDOFF.md` §5.

Then, in the same commit as the term:

```bash
python tools/ontology/vendor_upstream.py --rebuild     # if it names a new upstream term
python tools/ontology/validate.py --gate               # wellformedness now has a subject
python tools/ontology/corpus_digest.py -o config/corpus-digest.json
python -m pytest tests/ -q -p no:randomly
```

---

## Adding a file

Every tracked file must be declared in `config/repository-layout.yaml`. An undeclared file
fails the suite in both directions: it has no stated role, and a declared component whose
path is missing is a contract describing something that is not there.

```yaml
  - id: ontology.cap                  # stable; queries and tests reference the id, not the path
    path: src/05_ontology/apqc-cap.ttl
    role: ontology-module
    description: >-
      What it is, and anything a reader would otherwise have to reconstruct.
```

Roles are not labels — each carries a consequence, and the set of known roles is read
from the licensing tool so the two cannot drift:

| Role | Means |
|---|---|
| `ontology-module`, `ontology-module-set` | authored ontology; in the validation data graph and the corpus digest |
| `ontology-validation` | SHACL shapes; **not** in the data graph |
| `test-fixture` | expected to be invalid on purpose; must never be loaded as ontology |
| `generated-artifact` | derived; must name a `generator`, or declare itself `orphaned` with the reason |
| `specification` | the specification in force; read by the vendoring tool for the upstream terms it names. A superseded spec is re-roled `documentation` in the commit that supersedes it |
| `historical-draft` | preserved as imported; never loaded. The v0.1 package |
| `vendored-ontology` | somebody else's, redistributed under their licence, attribution required |
| `third-party-reference` | somebody else's, **not** redistributable |
| `source-evidence` | another project's text harvested into the Capability Term Inventory (`docs/sources/inventory/`), redistributed under its pinned licence (`config/inventory-sources.yaml`, `config/inventory-federal-sources.yaml`), attribution required; YAML, never loaded as Turtle |
| `documentation`, `configuration`, `tool`, `project-licence` | as they sound |

Two fields worth knowing:

- **`tracked: false`** — the files may exist locally and must never be committed. Stronger
  than `.gitignore`, because an already-tracked file stays tracked. This is what stands
  between `docs/Reference/` and publishing a licensed capability framework.
- **`generator:` / `orphaned:`** — exactly one is required of a `generated-artifact`.

Adding a new *role* means adding a licensing rule for it in
`tools/licensing/disposition.py`. The test will tell you; do it deliberately rather than
letting a file inherit a guess.

---

## Adding a shape set

**In the same commit, or not at all:** a new shape set arrives with negative fixture cases
that break it, each named for the constraint it targets, plus positive controls that must
survive. Declare the fixture as its own `test-fixture` component; `validate.py` loads every
one the contract declares.

`shapes/vocabulary_shapes.ttl` with `shapes/vocabulary_bad_examples.ttl` (P4) is the
worked example: one case per constraint, named for it, and `VOCABULARY_CONSTRAINTS` in
`tests/test_ontology_checks.py` mapping each message to the focus node it must fire on.

The spec's CAP requirements (CAP-01 to CAP-29, §6) are the obvious next set. Each row of
that table already names a falsifying case — the "Fixture (fails unless noted)" column —
which is the negative fixture written out in prose. A CAP constraint whose fixture case does not exist yet stays
DRAFT, which is what the spec says too (§0: "every requirement stays DRAFT until its
falsifying fixture exists").

Why both kinds of case: a shape set reporting zero against the corpus is ambiguous on its
own — clean data and a constraint selecting nothing look identical — and a fixture where
everything fails cannot show that a constraint discriminates. In ARO,
`capabilities_roles_shapes.ttl` reported 202 violations while CCO was missing and zero the
moment it was vendored, and nothing distinguished that zero until named fixture cases
existed.

List the new constraint messages by name in `tests/test_ontology_checks.py`, as
`WELLFORMEDNESS_CONSTRAINTS` does. A count would be satisfied by any N violations.

---

## Working with the vendored upstream

BFO, CCO and BPO are pinned partial extracts, not `owl:imports`. Nothing resolves over the
network at validation time.

```bash
python tools/ontology/vendor_upstream.py            # offline verify — runs in CI
python tools/ontology/vendor_upstream.py --confirm  # fetch and require byte-identity
python tools/ontology/vendor_upstream.py --rebuild  # fetch and rewrite
```

| id | pin | why this one |
|---|---|---|
| `bfo` | release-2024-01-29 | the same pin ARO uses |
| `cco` | v2.0-2024-11-06 | BPO's act genera were anchored and verified against v2.0; ARO pins v2.2 |
| `bpo` | v0.4.1 (`main@bc64e91`), `ontology/apqc-ext.ttl` only | the D9 registry of shared act genera; re-pinned 2026-10-28 from `6613194` after BPO's namespace move |

**Seeds come from three places.** The authored modules and the shapes, as in ARO — and,
here, the specification in force (role `specification`), read for `cco:`, `obo:` and `ex:`
terms. A spec term no pinned file describes is recorded in `config/upstream-extracts.json`
under `specification_names_described_by_no_pinned_file` rather than refused, as the spec
writes them and attributed to no namespace (manifest format 2, since the 2026-10-28 re-pin:
the spec writes `ex:` for BPO's terms and for the BCO's own, so expanding them under BPO's
namespace would attribute BCO classes to BPO, which R3 forbids). Today that list is 61
`ex:` names: the ones the BCO will mint, BPO process classes from slices that are not
vendored, and the spec's worked-example individuals. Every `cco:` and `obo:` term the spec
names resolves.

**When you must rebuild:** whenever the corpus, the shapes or the spec name an upstream
term that is not yet vendored. The offline check catches it — that is exactly what it is
for — and the message names the terms.

**BPO's licence is read from its LICENSE file,** because its Turtle states none. The pin
names a `statement_url` at the same commit with its own digest, and the build requires
`MIT License` to appear there. The tool refuses a `statement_url` that does not name the
pinned commit.

**What the extracts leave out:** every axiom whose object is an anonymous class
expression. That is recorded in each file's header and in `config/upstream-extracts.json`,
and it means these files cannot support a consistency claim against BFO, CCO or BPO.

**One change from ARO's tool:** a selected triple is written into the extract of the file
that asserts it, not the extract whose namespace its subject is in. CCO's merged file
annotates BFO terms, and ARO's tool wrote four of those annotations into the BFO extract
under BFO's licence. ARO's copy still does this.

Downloads cache in `.upstream-cache/` (gitignored). The weekly CI job re-fetches and
requires the committed extracts to be byte-identical.

---

## The public site

Published at https://skreen5hot.github.io/Business-and-Agent-Capabilities-Ontology/ by `.github/workflows/pages.yml`, for external validators: the rendered
specification, every review under `reviews/` with its disposition, a term explorer, the
vocabulary, the conceptual models, module and status pages, and downloads with checksums. The method is BFO-Aligned ValueNet's; the builder is rewritten for this
repository.

```bash
python tools/site/build_site.py      # into _site/ (gitignored)
python tools/site/check_site.py      # the checks the workflow runs before deploying
python -m pytest tests/test_site.py -q -p no:randomly
```

To look at it locally, serve `_site/` and open it — every URL is relative, so it works
from any path:

```bash
python -m http.server 8765 --directory _site
```

| Where | What lives there |
|---|---|
| `site/pages/<key>.html` | one body fragment per page, with `{{placeholders}}` |
| `site/content/site.json` | navigation, notices, and words a person chose — never a figure |
| `site/src/assets/` | the stylesheet, the explorer's scripts and the Models page's `models.js`, copied verbatim |
| `vendor/site/` | third-party files the site serves (Mermaid), pinned in `config/site-vendor.yaml`; written only by `tools/site/vendor_assets.py --fetch` |
| `tools/site/build_site.py` | fills the placeholders from the repository; one function per value |

**Nothing on the site is typed if it can be read.** Versions, counts, digests, licences
and the RP table come from the spec, the layout contract, the pins and the manifests at
build time. A new page is a fragment plus a navigation entry; the build refuses a fragment
no navigation entry reaches and a placeholder nothing fills.

**The build refuses ambiguity in authored terms**: no label, no definition, or two of
either in one language stops it, because which one is published would otherwise be
decided by traversal order. This will matter the day the first BCO term lands.

**The Vocabulary page (P4)** is `site/pages/vocabulary.html`, filled by
`vocabulary_values` in `tools/site/build_site.py` from the generated Turtle
(`layout.vocabulary_files()`), never from `src/01_controlled_vocabulary/*.yaml` -- a test records every file the
build opens and refuses one. It shows the authored namespaces (prefixes read from the
Turtle's own bindings), both schemes, each concept's labels, definition, derived status,
notation, designated class, genus and foundational ancestor (catalog, since R7),
drafting agent and sources (SRC id, relation, locator, departure note, and since R7 the
cited claim's index and status), the citations of only those register entries a concept
cites -- the full register is not published; that is the architect's call -- and the
declared agents. While
there is no concept it shows the `vocabulary_empty` notice from `site.json`. A concept in
no scheme or two, or with no label, definition or status, stops the build. Vocabulary
concepts are not in the explorer's `data/terms.json`; that was optional in P4 and is not
done.

**The Reviews page** is `site/pages/review.html` (URL `review/`, kept so that links
already sent to validators still resolve), filled by `reviews_values`. It renders every
`reviews/*.md`: a review is named `R<n>-<words>.md`, and `R<n>-disposition.md` is the
project's proposed disposition of review R<n>, rendered directly after it and labelled as
a proposal. Each section has its own `<h2>`, source link and SHA-256, and every heading id
inside it carries the section's prefix (`r5-`, `r6-`, `r6-disposition-`), so two reviews
with a "Summary" heading cannot mint the same id. The build refuses a misnamed file, two
reviews with one number, a disposition with no review, and any id the page would carry
twice; `check_site.py` refuses a repeated id on any page.

**The Models page** is `site/pages/models.html` (URL `models/`), filled by
`models_values`. It renders every conceptual model whole through `render_markdown`, each
under its own `<h2>` and id prefix (`cm-01-`), with identifier, version, status and
approval state read from the model (its Field/Value table and its section 10 Review
status table, through `check_models.read_model`), a source link and SHA-256. The build
runs `tools/conceptual/check_models.py` first and refuses on any finding. Mermaid blocks
become `<pre class="mermaid">` holding the escaped source, so with JavaScript off the
source is what a reader sees. The page alone loads two scripts: Mermaid, copied from
`vendor/site/mermaid/` to `assets/vendor/mermaid/` and held to its pinned sha256 by the
build, and `site/src/assets/js/models.js`, which runs it with `securityLevel: "strict"`.
The pins are `config/site-vendor.yaml`; `python tools/site/vendor_assets.py --fetch`
re-vendors from them (the registry tarball only), and the default run verifies offline.
With no model, the page shows the `models_empty` notice.

**Deployment** is from the artifact the checks ran against, after a second build on the
same runner has produced an identical tree. Pull requests build, check, and upload a
preview artifact; only `main` deploys.

---

## The citation register

`docs/sources/business-capability-definition-sources.md` is generated. Never edit it;
the suite compares it byte for byte with a fresh generation.

| File | Holds | Edited by |
|---|---|---|
| `docs/sources/register.yaml` | every entry: id, authority, citation, URLs, licence and access terms, paraphrased definition, quotes, claims | hand |
| `docs/sources/register-companion.md` | the analysis prose: summary, how to read the register, consensus, fault lines and conflict matrix, discrepancies, SF-01 to SF-13, gaps | hand |
| `docs/sources/business-capability-definition-sources.md` | the two combined, the entry tables rendered where the companion's directive line stands | `build_register.py --write` |

```bash
python tools/sources/build_register.py            # check: findings, then freshness
python tools/sources/build_register.py --write    # regenerate after editing either source
python tools/sources/build_register.py --claims SRC-OMG-03 --at-least P
```

**A claim's status is one letter.** V, P, S, K or L, as the companion defines them.
Anything that qualifies it goes in `scope` (the part of the source the status covers,
rendered in parentheses) or `note` (rendered after a semicolon). `V (OWL)` as a status is
refused.

**Quotation marks are never typed into entry prose.** A verbatim quotation is a quote:
`{key: SRC-OMG-01-Q1, text: ...}` in the entry's `quotes`, at most 15 words, placed in
prose as `{Q1}`, exactly once. A title or a term's name that needs quotation marks is a
declared mention, `{mention:...}`. The register's own rule allows one quote per entry
(`MAX_QUOTES_PER_ENTRY`); the `Qn` keys would allow more if the architect relaxes it.
The companion's analysis prose is not under these rules: its few quoted phrases are
not keyed.

**SRC ids are checked everywhere.** Every tracked UTF-8 file is scanned for
`SRC-<family>-<nn>`, with the shorthand the analysis uses (`SRC-FO-01, -02`,
`SRC-OG-01/02`) expanded, and an id that names no entry is a finding. A test that needs
an unknown id builds it at run time, or the scan finds the test.

**The entry count is pinned** at 63 (`EXPECTED_ENTRY_COUNT`), the count when the register
became data. Adding or retiring an entry changes the constant and the companion's
"records N sources" in the same commit; the tool checks the companion states the real
count.

For P3, `claims_at_or_above(data, src_id, "P")` returns an entry's claims at V or P, and
raises on an unknown id rather than returning the empty list an unverified entry returns.

---

## The controlled vocabulary (P3)

ADR-003 is the specification; `tools/vocab/` implements it. P3 shipped the tool with
no terms. **P5 added the pilot vocabulary:** 9 metamodel concepts, one per concrete
section 4 row, and 5 catalog concepts (Strategic Planning, Treasury Management,
Competitive Analysis, Business Model Governance, Customer Experience Management), all
Draft and none ratified. The catalog records carry no `notation`, `broader` or
`designates_class`; the header of `src/01_controlled_vocabulary/catalog.yaml` says why. Review R7 (2026-10-25)
changed the export: claims are resources, prior records are described, and the catalog
genus is recorded as an immediate genus plus a foundational ancestor -- sections below.

| File | Holds | Edited by |
|---|---|---|
| `src/01_controlled_vocabulary/metamodel.yaml` | one provenance wrapper per spec section 4 row (`bcom:`): sources, drafting agent, notes, status inputs. Never a definition | hand |
| `src/01_controlled_vocabulary/catalog.yaml` | catalog concepts (`bcoc:`): labels, a genus-differentia definition with its immediate `genus` and its `foundational_ancestor`, `broader`, a PCF 7.4 `notation`, sources | hand |
| `src/01_controlled_vocabulary/agents.yaml` | declared agents (`bcoa:`): the architect as a Person, `claude-opus-5-5` as a SoftwareAgent on his behalf | hand |
| `src/01_controlled_vocabulary/generated/*.ttl` | `bco-vocabulary`, `bco-metamodel`, `bco-catalog`, `bco-sources`, `bco-agents` | `tools/vocab/build.py --write` |
| `config/vocab-schema.yaml` | the LinkML schema of the three YAML files | hand |
| `config/vocab-schema.json` | its `gen-json-schema` output, LF | `tools/vocab/schema_check.py --write` |

```bash
python tools/vocab/build.py                 # check: ADR-003's rules, then freshness
python tools/vocab/build.py --write         # regenerate src/01_controlled_vocabulary/generated/
python tools/vocab/build.py --digest bcoc:X # the record digest an act cites
python tools/vocab/spec_terms.py            # what section 4 parses to
python -m pytest tests/test_vocab.py -q -p no:randomly

# LinkML, in its own venv -- never in .venv:
py -3.12 -m venv .venv-vocab
.venv-vocab/Scripts/python -m pip install -r requirements-vocab.txt
.venv-vocab/Scripts/python tools/vocab/schema_check.py
```

The three YAML files must exist; an absent file is a finding, not an empty list. The
vocabulary is not an `ontology-module`, so it is not in the corpus digest. Since P4 its
generated Turtle is in the SHACL data graph and the wellformedness population -- see "The
vocabulary in the validation ladder (P4)" below.

**The metamodel comes from section 4 (D4).** `tools/vocab/spec_terms.py` reads every
table in `## 4. Terms` whose header is `Term | Definition | Parent(s) | Does not imply`.
A row is concrete when its Term cell is exactly a label followed by one `ex:` name in a
code span (optionally followed by `*(...)*`), and the label with non-alphanumerics
removed spells the local name. A row naming a placeholder (`ex:<Name>Realization`) or
one example standing for a family ("`ex:StrategicPlanningCapability` and the rest") is
a template, excluded with its reason. Any other row fails the build rather than being
classified by a guess. Today: 9 concrete rows, 2 excluded, and the
annotation-properties table skipped by header. A record is `bcom:<LocalName>` with
`spec_row: ex:<LocalName>`; its definition, label, parents and "Does not imply" are the
row's, verbatim, and its `bco:designatesClass` is `bco:<LocalName>`.

**The staging rule.** Once `src/01_controlled_vocabulary/metamodel.yaml` lists one concept, every concrete row
needs a record (`D4-row-uncovered`) and every record must name a row (`D4-no-row`).
While the list is empty, coverage is not checked; P5 added all nine at once, so coverage
is checked on every build now.

**The concept record digest** is what a ratification act cites, so it is defined
exactly: the authored YAML mapping minus `ratified_by`, plus -- for a metamodel concept
-- `spec_row_content`, the row's `{label, iri, definition, parents, does_not_imply}`;
serialised as `json.dumps(..., sort_keys=True, ensure_ascii=False,
separators=(",", ":"))`, UTF-8, no trailing newline; SHA-256, lowercase hex. The row is
inside so that a spec change to a Ratified concept's definition breaks the
ratification, as D3 and D4 require. `--digest` prints it.

**Verifying a record digest against the YAML** (review R7, Finding B). A digest in the
Turtle (`bco:recordSha256`, and the suffix of `<ns>record-<digest>`) can be checked
without the build, at any commit:

```bash
git show <commit>:src/01_controlled_vocabulary/catalog.yaml   # or metamodel.yaml
git show <commit>:vocab/catalog.yaml                           # a commit before 2026-10-25
```

The YAML was under `vocab/` until the stage layout moved it on 2026-10-25; every prior
record recorded so far was written there.

```python
import hashlib, json, yaml
record = next(r for r in yaml.safe_load(text)["concepts"] if r["id"] == "bcoc:TreasuryManagement")
body = {k: v for k, v in record.items() if k != "ratified_by"}
# a metamodel concept also needs body["spec_row_content"]: the section 4 row's
# {label, iri, definition, parents, does_not_imply}, as tools/vocab/spec_terms.py
# reads them from that commit's specification
raw = json.dumps(body, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
print(hashlib.sha256(raw).hexdigest())
```

`created` must stay a quoted string, or YAML reads it as a timestamp and the JSON is
not the same. `test_the_real_prior_records_resolve_and_verify` does exactly this for
every prior record the vocabulary publishes.

**Status is derived (D5).** Deprecated if `is_replaced_by` names a live concept (a
missing, self, chained or cyclic replacement is a finding); else Ratified if
`ratified_by` cites an act that lists this IRI with this record digest; else the authored
`Draft` or `Candidate`. `lifecycle_status` and `owl:deprecated` in YAML are refused.

**A ratification act** is a decision record holding exactly one fenced block:

````text
```bco-ratification
agent: https://fandaws.com/ontology/bco-agents#aaron-damiano
approvals:
  editorial: https://fandaws.com/ontology/bco-agents#aaron-damiano
  ontological: https://fandaws.com/ontology/bco-agents#aaron-damiano
validation:
  commit: <the full 40-hex commit the gates ran at, reachable from main>
  gates:
    - python tools/ontology/validate.py --gate
    - python -m pytest tests/ -q -p no:randomly
concepts:
  - iri: https://fandaws.com/ontology/bco-catalog#TreasuryManagement
    record_sha256: <python tools/vocab/build.py --digest bcoc:TreasuryManagement>
```
````

All four keys are required. IRIs in full; a CURIE, wildcard, namespace, scheme IRI or
any other key is refused. The agent, and both approvers, must be declared `prov:Person`s
(D8); one person may give both approvals. `validation.commit` is a full 40-hex SHA that
`origin/main` or `main` reaches, and `gates` is the non-empty list of gate commands that
passed at it, each once. The build checks the commit; it does not re-run the gates -- the
list is the act's statement. `approvals` and `validation` were added in answer to review
R6, section 6.3 (authorship is not approval, and provenance is not validation); they
extend the format P3 accepted and leave ADR-003 D5's content -- explicit IRIs, each with
its record digest -- unchanged. Refusal codes: `D5-act-approval-missing`,
`D5-act-approval-shape`, `D8-approver-not-person`, `D5-act-validation-shape`,
`D5-act-validation-commit`, `D5-act-validation-unreachable`, `D5-act-validation-gates`. Each concept then cites the act:
`ratified_by: {path, commit, sha256}` -- the path under `docs/decisions/` or
`docs/adr/`, a full commit reachable from `origin/main` or `main`, and the SHA-256 of
`git show <commit>:<path>`, all recomputed (D2). The block is read from that commit's
blob, not the working tree. An act is the architect's: an agent records it verbatim,
and never writes one on its own initiative.

**Register claims (review R7, Finding A).** `bco-sources.ttl` publishes each claim of
each register entry as a resource of its own: `bcos:<SRC id>-claim-<n>`, where n is the
claim's 1-based position in `register.yaml`. The record links it with `bco:hasClaim`; the
claim carries `bco:claimIndex` (n, `xsd:integer`), `bco:claimStatus` (exactly one of V,
P, S, K, L) and, where the register has them, `bco:claimScope` and `bco:claimNote`. A
`departs-from` reference's `bco:citesClaim` is that claim's IRI. The record itself no
longer carries `bco:claimStatus`: its statuses were an unordered bag, and nothing said
which claim each one qualified. The register has no claim text -- a claim is its status,
scope and note -- so none is published. Reordering an entry's claims renames them; the
IRI is the register's order, not a content digest.

**Prior records (review R7, Finding B).** A record's `revises` names the digest of the
record it replaces, and the graph says `<current record> prov:wasRevisionOf
<ns>record-<digest>`. That prior record is described in the same file: a `prov:Entity`
with its `bco:recordSha256`, and, where git settles it, `bco:recordCommit` (the commit
that introduced it) and its own `prov:wasRevisionOf`, from the `revises` it carried at
that commit, recursively. The build finds the commit by recomputing record digests over
the non-merge commits HEAD reaches that touched `metamodel.yaml`, `catalog.yaml` or
`specifications/`, each with that commit's own section 4 rows (read through that commit's
layout contract): a commit introduces a digest when its tree yields it and its parent's
does not, and the earliest by commit time, then hash, wins. A digest no commit yields
still gets its node, without a commit. The YAML moved from `vocab/` to
`src/01_controlled_vocabulary/` on 2026-10-25, so the search follows the move: it covers
every path any layout contract HEAD reaches has declared for `vocab.metamodel` or
`vocab.catalog`, and reads each commit's YAML at the path that commit's own contract
declares.
`test_a_prior_record_is_found_across_a_move_of_the_yaml` holds it to that. Four
consequences:

- **It needs the full history.** CI checks out with `fetch-depth: 0`; a shallow clone is
  the finding `D3-history-shallow` (only when some record revises another), because it
  would silently drop commits and the Turtle would differ.
- **Merge with a merge commit**, as this repository does. The introducing commit of a
  record written on a branch is a branch commit; a squash merge would leave `main`
  without it, the build on `main` would find a different commit, and the committed
  Turtle would be stale.
- **A move of the YAML changes its path in the layout contract, in the same commit.** The
  search reads a commit's YAML where that commit's contract says it is; a move that left
  the contract behind would hide the records before it.
- **The full history of a record is in git, not in the graph.** `git log --full-history
  -- src/01_controlled_vocabulary/catalog.yaml src/01_controlled_vocabulary/metamodel.yaml
  vocab/catalog.yaml vocab/metamodel.yaml` lists the commits that changed records;
  `git show <commit>:<path>`, at the path that commit holds it, gives a record as it
  stood; the digest check above matches it to a node. The `rdfs:comment` on
  `bco:recordCommit` and `bco:recordSha256` says the same.

**The catalog genus (review R7, Finding E;
`docs/decisions/2026-10-25-r7-genus-decision.md`).** `genus` is the definition's
**immediate** genus: a vendored BFO or CCO class, or the class a metamodel concept
designates. All five catalog concepts name `bco:BusinessCapability`, which
`bcom:BusinessCapability` designates. `foundational_ancestor` is a vendored BFO or CCO
class above it -- a section 4 parent of the designated class, or a vendored superclass of
one; for an upstream genus, a vendored superclass of the genus -- and all five name
`cco:ont00000568`. They are published as `bco:definitionGenus` and
`bco:foundationalAncestor`, annotations both. Nothing is minted: `bco:BusinessCapability`
is declared nowhere, and no `owl:Class` or `rdfs:subClassOf` is emitted. Refusal codes:
`catalog-genus`, `catalog-ancestor`, `catalog-ancestor-unrelated`. ADR-003 D4 says a
catalog definition has "a BFO/CCO genus"; since R7 that is the foundational ancestor, and
the immediate genus may be a designated `bco:` class, by the architect's decision.

**What the RDF cannot enforce (review R7, Findings F and G)** is said in the generated
vocabulary: `bco:PCFCode`'s `rdfs:comment` says its five-digit lexical form is assumed
and unchecked against a real code, that no concept carries a notation until one is
verified in BPO's catalog, and that edition-specific validation is the build's;
`bco:lifecycleStatus`'s says the value is derived and enforced by `tools/vocab/build.py`
(D5), not by the triples alone.

**Sources (D6).** Every reference names a register id, a locator and a relation;
`departs-from` also needs a `departure_note` and `claim`, the 1-based index of an entry
claim at V or P (`claims_at_or_above`). `consistent-with` also needs `support`
(review R6, section 6.1): `definitional` when the source backs something the definition
itself says that not every concept in the scheme shares -- its genus as placed, or a
differentia -- and `contextual` when it backs only a view the whole scheme rests on, such
as capability as an ability distinct from process. `adapted-from` is definitional by
nature and `departs-from` supports nothing, so `support` on either is refused
(`D6-support-missing`, `D6-support-value`, `D6-support-misplaced`). It is published as
`bco:support` on the reference node and shown on the Vocabulary page. A catalog definition sharing a 6-word run with
any registered quote, after lowercasing and splitting on non-letters, fails with the
quote's key.

**IRIs (D9).** Exactly ADR-003 D1's five namespaces. Provenance nodes are minted from
content: `<ns>source-<sha256>`, `<ns>ratification-<sha256>` of the canonical JSON, and
`<ns>record-<record digest>`, in the concept's own namespace. Written by
`vendor_upstream.serialise` with a vocabulary prefix table, which refuses a blank node.

**LinkML is go-limited.** `config/vocab-schema.yaml` describes the YAML; the build
re-checks everything it says, so the main suite never imports LinkML.
`tools/vocab/schema_check.py` runs in the `vocab-schema` CI job: it regenerates the JSON
Schema three times (twice from the root, once from a copy at another path), requires the
LF bytes to match the committed file, and runs `linkml validate` over the authored files
and 38 cases built to break the schema. `gen-shacl` and `gen-owl` are never run.

---

## The vocabulary in the validation ladder (P4)

**How it gets in.** The five generated files in `src/01_controlled_vocabulary/generated/` carry `vocabulary: true`
in `config/repository-layout.yaml`; `layout.vocabulary_files()` returns them, and
`tools/ontology/validate.py` loads them into the data graph beside the ontology modules and
the vendored extracts. Only a `generated-artifact` may carry the attribute. A violation
against any IRI in `AUTHORED_NAMESPACES` -- a concept, a source record, an agent -- counts
as an authored finding. `tools/ontology/vendor_upstream.py` seeds from them too, so an
upstream term a concept names (a section 4 parent, a catalog genus) gets vendored.

**Not in the corpus digest,** on purpose. The vocabulary is its own generated measurement:
`tools/vocab/build.py` rebuilds it and compares it byte for byte. And `bco-sources.ttl` is
generated from the citation register, so folding it into the digest would move the
ontology's measure on every register edit -- the same reason the vendored extracts are kept
out.

**Two shape sets see it.**

| Shapes | Population |
|---|---|
| `wellformedness_shapes.ttl` | `owl:Class` in `bco#`; `skos:Concept` in `bco-metamodel#` and `bco-catalog#` (D1). Not sources or agents (D8) |
| `vocabulary_shapes.ttl` | concepts (scheme, tagged prefLabel per language, definition, no stored narrower, derived status, deprecation iff replacement, ratified only with a citation, a declared drafting agent); metamodel concepts' designated class; catalog concepts' notation typed `bco:PCFCode`, exactly one genus (a BFO/CCO IRI or a metamodel concept's designated class) and exactly one foundational ancestor (a BFO/CCO IRI); source references (resolves to a `bcos:` record, locator, relation enum, `departs-from` with a note and a claim that is a claim of the cited source at V or P, `consistent-with` with exactly one `bco:support` of definitional or contextual, and no support on any other relation); every source record in `bcos:` (type, identifier, citation, at least one claim of its own, no status of its own, no index twice); every claim (`<record>-claim-<n>`: one positive integer index matching its name, one status from V/P/S/K/L, belongs to a record); records, current and prior (a `prov:Entity` with one digest that its IRI names, every `prov:wasRevisionOf` target described, a 40-hex commit if any); every subject in `bcoa:`; persons named; software agents with a model identifier acting for a declared person; ratification references with an act path, a 40-hex commit and a 64-hex digest other than the empty file's |

`vocabulary_shapes.ttl` is hand-written (P2: `gen-shacl` is no-go), every constraint has a
fixed `sh:message` with no substitution, and `tests/test_ontology_checks.py` maps every
message to its case in `shapes/vocabulary_bad_examples.ttl` and requires it to fire on that
focus node. Note that `validate.py` runs every shape set against **all** fixtures loaded
together, so a case in one fixture is also seen by the other shape set; the positive-control
checks are per rung.

**What the real data shows at P4:** the concept shapes conformed vacuously -- there were
no concepts until P5 -- and only the fixture showed they work. The source-record and agent
shapes run over the 63 records and 2 agents and find nothing; `test_the_real_records_and_agents_are_selected`
strips every citation in memory to show all 63 records really are selected.

**What the real data shows since R7:** the claim shape runs over the register's 83
claims and the record shape over 14 current and 19 prior records, and both find nothing.
`test_the_real_claims_and_records_are_selected` strips every claim status, and then every
record digest, in memory, and requires each claim, each departs-from reference, and each
current or revising record to be reported, and nothing else.

**What the real data shows at P5:** the concept shapes run over 14 real concepts and their
source references and find nothing, in both rungs (`validation.vocabulary` and
`validation.wellformedness`, 0 authored findings each). `test_the_real_concepts_and_departures_are_selected`
strips every definition and every departure note in memory and requires each of the 14
concepts and each `departs-from` reference to be reported, and nothing else.

---

## Conventions

### Paying down a finding

Findings are recorded per shape set in `config/validation-baseline.json` (zero today), and
the gate requires the file to describe reality — *more* is a regression, *fewer* means
re-record so the reduction shows up in a diff:

```bash
python tools/ontology/validate.py --record     # after fixing something
```

`--record` refuses to raise a count without `--accept-regression "<why>"`, and writes the
reason beside the number it excuses.

### Recording a decision

The architect's acts go in `docs/decisions/YYYY-MM-DD-<slug>.md`: the act verbatim, who
and when, the digest or commit of what it is about (recomputed from the committed file
before recording), and its effect. See the 2026-10-23 entry for the shape. An agent may
record an act; it never performs one.

### The rest

**Falsify every check.** A passing test is not evidence. Evidence is a passing test plus a
demonstration that it can fail: revert the fix, require *that specific* check to fail,
restore, confirm.

**And verify the mutation moved what is measured.** A changed file digest is not enough.
Assert the number you expect to move has moved, *then* run the check.

**Stage before you mutate.** `git checkout --` restores from the index; unstaged work is
destroyed.

**Commit messages carry the reasoning, not the diff.** What was wrong, why the fix is the
fix, what was measured, and what is still not covered.

**Say what was not done.** Every record states its own limits.

**Line endings are content.** `.gitattributes` pins LF repository-wide. A CRLF inside a
`skos:definition` is part of that literal's value, and the import's recorded digests are
over LF bytes.

**Derive, never transcribe.** Paths come from the layout contract. Licences are read from
`LICENSE` and from the upstream artifact. Upstream namespaces are read from the pins.
Counts are measured.

---

## Traps

Inherited from ARO, because none of them announces itself.

- **`| head` and `| tail` mask exit codes.** The pipeline exits with the *last* command's
  status.
- **`text=True` in `subprocess` decodes as cp1252 on Windows**, which corrupts multi-byte
  sequences and then blames the file. Decode explicitly as UTF-8.
- **rdflib renames blank nodes on every parse.** Compare ground triples plus a blank-node
  *shape* digest — `tools/ontology/corpus_digest.py` is the worked version.
- **`all()` over an empty sequence is `True`.** `validate.passed_of` is the guard.
- **Scanning file text finds the comment explaining the rule.** Parse and check terms.
- **A green shape set is ambiguous on its own.** Clean data and a constraint selecting
  nothing look identical — and with an empty corpus, every shape set is green.

One that is specific to this repository:

- **The spec writes BCO terms as `ex:`.** That prefix is bound to BPO's namespace, as a
  temporary prefix for BPO's genera only. Copying a Turtle example out of the spec mints a
  term in BPO's namespace, and `tests/test_namespace.py` will refuse a term under the
  `example.org` the spec still names.
