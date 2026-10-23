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
   not the spec's `ex:`. That string appears in exactly two places — `AUTHORED_NAMESPACE`
   in `tools/ontology/validate.py` and the SPARQL targets in
   `shapes/wellformedness_shapes.ttl` — and `tests/test_namespace.py` requires them to
   agree. When RP-5 mints the permanent namespace, change both in one commit.
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
