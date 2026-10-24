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
python -m pytest tests/ -q -p no:randomly     # all of the above, plus the falsifications
```

| Command | What it will refuse |
|---|---|
| `layout.py` | a declared component whose path does not exist; two components sharing an id; a generated artifact that names no generator and does not admit it has none |
| `disposition.py` | a file matching two rules, or none; an adjudication naming no file; a `LICENSE` naming zero or two recognised licences |
| `disposition.py --check` | a tracked file that may not be redistributed; a vendored extract whose required attribution is missing from `vendor/NOTICE.md` |
| `vendor_upstream.py` | an upstream term the corpus, the shapes or the specification names that no extract describes (spec terms the last build recorded as unresolvable excepted); an extract whose digest is not what the manifest records |
| `validate.py --gate` | a rung with more findings than `config/validation-baseline.json` records, a rung with fewer that has not been re-recorded, a shape set the fixture does not exercise, a rung blocked on missing vocabulary, a violation against a vendored term, and a rung the baseline does not mention |
| `validate.py --record` | raising any recorded count without `--accept-regression "<why>"`. Lowering is always free |
| `vocab/build.py` | everything in ADR-003 a schema cannot say: an unreadable section 4, a metamodel definition, an authored status, a record naming no row (and, once one record exists, a row with no record), a broken decision citation or act, a record changed after ratification, an unknown source, a missing locator, a weak or missing departure claim, a definition sharing six words with a registered quote, a malformed notation, an undeclared agent, a status act not by a Person, and committed Turtle that is not a fresh build |
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
| `ontology/apqc-cap.ttl` | Business Capability, the capability classes with their `enablesProcess` index, reviewed unions |
| `ontology/apqc-cap-desc.ttl` | the seven description-layer classes and the Authorization Record |

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
    path: ontology/apqc-cap.ttl
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
| `bpo` | `main@6613194`, `ontology/apqc-ext.ttl` only | the D9 registry of shared act genera |

**Seeds come from three places.** The authored modules and the shapes, as in ARO — and,
here, the specification in force (role `specification`), read for `cco:`, `obo:` and `ex:`
terms. A spec term no pinned file describes is recorded in `config/upstream-extracts.json`
under `named_by_specification_described_by_no_pinned_file` rather than refused. Today that
list is 61 `ex:` terms: the ones the BCO will mint, BPO process classes from slices that
are not vendored, and the spec's worked-example individuals. Every `cco:` and `obo:` term
the spec names resolves.

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
specification and R5 review, a term explorer, module and status pages, and downloads with
checksums. The method is BFO-Aligned ValueNet's; the builder is rewritten for this
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
| `site/src/assets/` | the stylesheet and the explorer's scripts, copied verbatim |
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
(`layout.vocabulary_files()`), never from `vocab/*.yaml` -- a test records every file the
build opens and refuses one. It shows the authored namespaces (prefixes read from the
Turtle's own bindings), both schemes, each concept's labels, definition, derived status,
notation, designated class, drafting agent and sources (SRC id, relation, locator,
departure note), the citations of only those register entries a concept cites -- the full
register is not published; that is the architect's call -- and the declared agents. While
there is no concept it shows the `vocabulary_empty` notice from `site.json`. A concept in
no scheme or two, or with no label, definition or status, stops the build. Vocabulary
concepts are not in the explorer's `data/terms.json`; that was optional in P4 and is not
done.

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

ADR-003 is the specification; `tools/vocab/` implements it. P3 ships the tool and
**no terms**: the metamodel and catalog files hold empty lists until P5.

| File | Holds | Edited by |
|---|---|---|
| `vocab/metamodel.yaml` | one provenance wrapper per spec section 4 row (`bcom:`): sources, drafting agent, notes, status inputs. Never a definition | hand |
| `vocab/catalog.yaml` | catalog concepts (`bcoc:`): labels, a genus-differentia definition with its `genus`, `broader`, a PCF 7.4 `notation`, sources | hand |
| `vocab/agents.yaml` | declared agents (`bcoa:`): the architect as a Person, `claude-opus-5-5` as a SoftwareAgent on his behalf | hand |
| `vocab/generated/*.ttl` | `bco-vocabulary`, `bco-metamodel`, `bco-catalog`, `bco-sources`, `bco-agents` | `tools/vocab/build.py --write` |
| `config/vocab-schema.yaml` | the LinkML schema of the three YAML files | hand |
| `config/vocab-schema.json` | its `gen-json-schema` output, LF | `tools/vocab/schema_check.py --write` |

```bash
python tools/vocab/build.py                 # check: ADR-003's rules, then freshness
python tools/vocab/build.py --write         # regenerate vocab/generated/
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

**The staging rule.** Once `vocab/metamodel.yaml` lists one concept, every concrete row
needs a record (`D4-row-uncovered`) and every record must name a row (`D4-no-row`).
While the list is empty, coverage is not checked; P5 adds all nine at once.

**The concept record digest** is what a ratification act cites, so it is defined
exactly: the authored YAML mapping minus `ratified_by`, plus -- for a metamodel concept
-- `spec_row_content`, the row's `{label, iri, definition, parents, does_not_imply}`;
serialised as `json.dumps(..., sort_keys=True, ensure_ascii=False,
separators=(",", ":"))`, UTF-8, no trailing newline; SHA-256, lowercase hex. The row is
inside so that a spec change to a Ratified concept's definition breaks the
ratification, as D3 and D4 require. `--digest` prints it.

**Status is derived (D5).** Deprecated if `is_replaced_by` names a live concept (a
missing, self, chained or cyclic replacement is a finding); else Ratified if
`ratified_by` cites an act that lists this IRI with this record digest; else the authored
`Draft` or `Candidate`. `lifecycle_status` and `owl:deprecated` in YAML are refused.

**A ratification act** is a decision record holding exactly one fenced block:

````text
```bco-ratification
agent: https://fandaws.com/ontology/bco-agents#aaron-damiano
concepts:
  - iri: https://fandaws.com/ontology/bco-catalog#TreasuryManagement
    record_sha256: <python tools/vocab/build.py --digest bcoc:TreasuryManagement>
```
````

IRIs in full; a CURIE, wildcard, namespace, scheme IRI or any other key is refused. The
agent must be a declared `prov:Person` (D8). Each concept then cites the act:
`ratified_by: {path, commit, sha256}` -- the path under `docs/decisions/` or
`docs/adr/`, a full commit reachable from `origin/main` or `main`, and the SHA-256 of
`git show <commit>:<path>`, all recomputed (D2). The block is read from that commit's
blob, not the working tree. An act is the architect's: an agent records it verbatim,
and never writes one on its own initiative.

**Sources (D6).** Every reference names a register id, a locator and a relation;
`departs-from` also needs a `departure_note` and `claim`, the 1-based index of an entry
claim at V or P (`claims_at_or_above`). A catalog definition sharing a 6-word run with
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
and 33 cases built to break the schema. `gen-shacl` and `gen-owl` are never run.

---

## The vocabulary in the validation ladder (P4)

**How it gets in.** The five generated files in `vocab/generated/` carry `vocabulary: true`
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
| `vocabulary_shapes.ttl` | concepts (scheme, tagged prefLabel per language, definition, no stored narrower, derived status, deprecation iff replacement, ratified only with a citation, a declared drafting agent); metamodel concepts' designated class; catalog notations typed `bco:PCFCode`; source references (resolves to a `bcos:` record, locator, relation enum, `departs-from` with a note and a claim); every subject in `bcos:` and `bcoa:`; persons named; software agents with a model identifier acting for a declared person; ratification references with an act path, a 40-hex commit and a 64-hex digest other than the empty file's |

`vocabulary_shapes.ttl` is hand-written (P2: `gen-shacl` is no-go), every constraint has a
fixed `sh:message` with no substitution, and `tests/test_ontology_checks.py` maps every
message to its case in `shapes/vocabulary_bad_examples.ttl` and requires it to fire on that
focus node. Note that `validate.py` runs every shape set against **all** fixtures loaded
together, so a case in one fixture is also seen by the other shape set; the positive-control
checks are per rung.

**What the real data shows at P4:** the concept shapes conform vacuously -- there are no
concepts until P5 -- and only the fixture shows they work. The source-record and agent shapes
run over the 63 records and 2 agents and find nothing; `test_the_real_records_and_agents_are_selected`
strips every citation in memory to show all 63 records really are selected.

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

- **The spec writes BCO terms as `ex:`.** That prefix is BPO's namespace. Copying a Turtle
  example out of the spec mints a term in BPO's namespace under `example.org`, and
  `tests/test_namespace.py` will refuse it.
