# Capability Term Inventory — source evidence

What other projects say a capability is, recorded entry by entry with where each one came
from. **This is source evidence, not vocabulary, and not an admission to the ontology.**
Nothing here is a BCO term, a vocabulary concept, a ratification or a decision; scope
approval D6 makes this directory the evidence location, and Amendment 4 forbids any
inventory operation from minting an ontology IRI or generating a class, property,
subclass axiom or ratification act. `tools/inventory/harvest_bpo.py` enforces that on
every run (below).

## The phases

| Phase | What | State |
|---|---|---|
| I-1 | BPO harvest, with Q-12 and Q-13 re-measured | **this directory**; its APQC withholding lifted by E7 (**`e7-release.md`**) |
| I-2a | Rights review of the public catalogs: APQC PCF 7.4 and 8.0, FEAF-II BRM 3.1, FIBF | **`rights.yaml`**; decided 2026-10-28 (`docs/decisions/2026-10-28-i2a-decided.md`) |
| I-2b | APQC PCF 7.4, every element, from BPO's catalog with APQC's notice (decision of 2026-10-29) | **`pcf-7.4-entries.yaml`**; E4 method decided, no element judged; PCF 8.0 deferred |
| I-2c | Federal catalogs: FEAF-II BRM and FIBF | **`feaf-brm-entries.yaml`, `fibf-*.yaml`**; approved and merged 2026-10-30, the HR lists' text withheld |
| I-3 | Restricted catalogs, citation and coverage only | not started |
| I-4 | Crosswalk, triage and report | not started |
| I-5 | Recommendation of a first catalog tranche, for the architect's separate approval | not started |

The phases are as the scope proposal stated them; the architect's approval, with its
amendments, is `docs/decisions/2026-10-27-capability-inventory-scope-approved.md`. I-2 is
split into I-2a, I-2b and I-2c, each its own reviewed pull request, by decision E1
(`docs/decisions/2026-10-28-i2-and-bpo-repin-decided.md`); I-3 to I-5 are not authorized.

Phase I-1 does not group, deduplicate or triage. Two BPO items that look like the same
capability are two entries; a class BPO declares in two modules keeps both declarations
side by side. That is I-4's work, and doing it here would hide the evidence a later
reviewer needs in order to disagree with it.

## The files

| File | What | Written by |
|---|---|---|
| `bpo-entries.yaml` | one entry per BPO source item, never merged | `harvest_bpo.py --rebuild` |
| `bpo-findings.yaml` | counts at the selected commit and at the baseline, and the diff; IRIs only | `harvest_bpo.py --rebuild` |
| `NOTICE.md` | the attribution BPO's licence requires, and where the PCF text released by E7 came from | `harvest_bpo.py --rebuild` |
| `e7-release.md` | E7: what lifting I-1's withholding changed, and the digests the I-1 approval recorded | hand, checked by `tests/test_inventory.py` |
| `rights.yaml` | I-2a: per source and edition, the rights evidence pinned by digest, findings, decision points | hand, checked by `rights.py` |
| `feaf-brm-entries.yaml` | I-2c: FEAF-II BRM 3.1, both OMB documents kept apart | `harvest_federal.py --rebuild` |
| `fibf-entries.yaml` | I-2c: FIBF functions and activities | `harvest_federal.py --rebuild` |
| `fibf-business-capabilities.yaml` | I-2c: FIBF business capabilities, each with the homonym flag | `harvest_federal.py --rebuild` |
| `fibf-snapshot.yaml` | I-2c: every pinned FIBF document, its status, draft and duplicate findings, FIBF-2 a columns | `harvest_federal.py --rebuild` |
| `NOTICE-federal.md` | I-2c: the attribution of the federal text (OMB; GSA and the standards lead agencies) | `harvest_federal.py --rebuild` |
| `pcf-7.4-entries.yaml` | I-2b: every PCF 7.4 element as BPO's catalog states it, under APQC's notice; not MIT | `harvest_pcf.py --write` |
| `README.md` | this file | hand |

The pins are `config/inventory-sources.yaml`: BPO `main` HEAD on 2026-10-27, resolved to
commit `bc64e91839378e1926189c01bf184d6a22d5c1b7` (v0.4.1), every input file with its
SHA-256, and the baseline, commit `66131945b525c54f44e4962f32bb1f52dfa0cd12`, which
`config/upstream-sources.yaml` vendors. Re-pinning the vendored extract is a separate
decision (D1); this directory does not do it. E7's release reads BPO at the PCF pin in
`config/inventory-pcf-sources.yaml` (its `i1_release` block), not here: this file is an
approved I-1 output and E7 leaves it unchanged.

## What an entry is

- **`capability-class`** — every class in BPO's namespace whose `rdfs:subClassOf`
  closure, over every harvested module plus the full pinned CCO and BFO, reaches CCO
  Organization Capability (`cco:ont00000568`). Each module that types the class
  `owl:Class` is one item under `declarations`, with its own line, locator,
  `owl:versionInfo`, direct named superclasses (`hierarchy`), labels and definitions.
  `designated_by` lists the PCF catalog nodes that bridge to the class with
  `bpo:designatesProcessType` (BPO ADR-001 R4), and `enables_process` every
  `bpo:enablesProcess` triple from it, with the module that asserts it and the target's
  kind (`act`, `capability`, `act-and-capability`, `unresolved`).
- **`scope-entry`** — every key of BPO's `capabilities/capability_scope.json` except
  `_doc`. A different kind from the class even when the IRI is the same, because it is
  a different statement in a different file. Its processes keep the table's order.
  `capability_class_entry` names the class entry with the same IRI, when there is one;
  it is a cross-reference, not a merge.
- **Standing functions** — none. BPO's ADR-001 R5 says a standing-function node is
  catalog-only and R6 that it should get an Organization Capability bridged from it, but
  BPO records no marker of the standing-function judgement on any node. The bridge is not
  that marker (R4 bridges processes and capabilities alike, and R6 is a "should"), and the
  approval forbids inferring the judgement from labels or hierarchy level, so no entry of
  this kind is recorded. The bridges are kept, as `designated_by`, for whoever takes the
  question up.

Every entry has a stable id, `INV-BPO-<local name>-<kind>`, its IRI as at the selected
commit, `version.commit`, `rights_status`, `apqc_evidence` and `pcf_code`.

## The rights rule

BPO is MIT, and its own text is redistributed here under that licence with the
attribution in `NOTICE.md`. BPO's licence cannot waive APQC's conditions on the Process
Classification Framework, so (Amendment 3) every literal the harvest can tie to the PCF
was **withheld** when I-1 was approved: the field held `{withheld: apqc-terms-unverified}`,
and the IRI and PCF code were kept. E7 has since released it (below); the rule still runs,
and still decides which entries are PCF material. An entry is tied to the PCF when BPO
itself says so:

1. **IRI scheme** — its local name is `P<digits>` or `PCF_<digits>`, BPO's D7 scheme for
   a class minted from a PCF node and for a catalog node (stated in every slice header);
2. **annotation** — it carries `bpo:pcfID`, `bpo:hierarchyID` or `bpo:apqcSourceText`,
   the provenance annotations BPO's catalog layer declares for PCF material;
3. **text match** — one of its labels or definitions equals, ignoring case and
   whitespace, a PCF catalog node's `skos:prefLabel` or `bpo:apqcSourceText`;
4. **text contains** — one of its labels or definitions contains such a PCF name of two
   or more words as a whole run of words, ignoring case and punctuation (a definition in
   BPO's own wording that reproduces a PCF element's name);
5. **shared text** — one of its labels or definitions equals text withheld on another
   class by any of these rules, so the same words are not published under a second IRI.

The evidence is listed on each entry, so every tie to the PCF can be checked. What the
rule cannot see is PCF text BPO paraphrased closely without carrying an annotation; that
residue was why I-1's status said *unverified*. E7 does not change it: text the rule does
not tie to the PCF stays recorded as BPO's (`bpo-mit`), and a close paraphrase the rule
cannot see stays a stated limit of the rule, not a finding. The APQC evidence BPO carried at the harvest commit — its PCF 7.4 workbook,
whose last sheet holds APQC's copyright and attribution notice — is pinned by digest in
the config and listed in `NOTICE.md`; it is not reproduced here.

`bpo-findings.yaml` holds IRIs and counts only, so nothing in it is subject to the rule.

### E7: the withholding lifted

Decision E7 (`docs/decisions/2026-10-28-i2-and-bpo-repin-decided.md`) required a separate
reviewed pull request to lift I-1's withholding, with the I-1 approval and historical
outputs kept traceable; the architect's decision of 2026-10-29 (section 5) authorized
preparing it, and its section 3 takes all PCF material from BPO at a pinned commit that
carries BPO's `NOTICE.md`. `harvest_bpo.py` applies it as a separate step after the rule
(`release`):

- the labels and definitions of each withheld entry are read from the **same module** at
  BPO `2e55edd9e86a0bc20fa88a21595cc61402faa5dc`, the commit
  `config/inventory-pcf-sources.yaml` pins for the PCF; its `i1_release` block pins each
  module by sha256, and each module's ontology header must carry APQC's notice in its
  `dct:rights`;
- the text is released only if it **equals, literal for literal,** what I-1 withheld at
  `bc64e91`; a difference is a refusal and a question for the architect, because it would
  publish text nobody reviewed under I-1. At E7 every one was equal;
- the declaration gains `text_from` (the line at the release commit), the entry's
  `rights_status` becomes `apqc-pcf-7.4`, and `apqc_evidence` keeps the reason it is
  PCF material;
- the entries file gains APQC's notice (`apqc_notice`, from BPO's `NOTICE.md`, held to the
  pinned digest) and a `release` block naming the commit, every input digest and the
  authority.

Everything else is I-1's harvest unchanged: the harvest commit `bc64e91` on every entry,
the baseline `66131945`, `bpo-findings.yaml`, `config/inventory-sources.yaml`, and every
entry the rule did not tie to the PCF, byte for byte. `e7-release.md` records the
digests the I-1 approval recorded, the digests now, the counts released and the equality
measured; the approved versions are in git at the I-1 merge commit `ba8df1a`.

## Regenerating, and what is checked

```bash
python tools/inventory/harvest_bpo.py             # offline check (before committing; CI)
python tools/inventory/harvest_bpo.py --rebuild   # fetch the pinned files, rewrite the outputs
python tools/inventory/harvest_bpo.py --confirm   # fetch, harvest, require byte-identity
```

`--rebuild` and `--confirm` fetch only from raw.githubusercontent.com at the pinned
commits (BPO's files, BPO's LICENSE and evidence, the full CCO and BFO pinned in
`config/upstream-sources.yaml`, and E7's modules and `NOTICE.md` at the PCF pin),
checking every digest; downloads are cached in `.upstream-cache/`. Two rebuilds produce
identical bytes. Nothing is fetched from apqc.org.

The offline check refuses: outputs whose recorded input digests are not the pins; an
entry missing a field, with an unknown kind, an id that is not
`INV-BPO-<local name>-<kind>`, or a commit other than the pin; an entry or field still
withheld; an entry with APQC evidence or a PCF code that is not released, or a released
one with none; a released declaration without its label and definition lists or whose
`text_from` is not a line of its module at the release commit; an `apqc_notice` that is
not the pinned notice, or a `release` block other than the pins give; counts in the
findings that disagree with the entries; a `NOTICE.md` that is not a fresh generation;
and, over every file in this directory, anything but YAML or
Markdown, anything that reads as an RDF serialization, any IRI in this repository's
authored namespaces (`AUTHORED_NAMESPACES` in `tools/ontology/validate.py`), and any
ratification or vocabulary key.

## The rights review (Phase I-2a)

`rights.yaml` is a review, not a decision, and holds no catalog content: no PCF, BRM or
FIBF name, description, code or hierarchy. For each source and edition it records the
rights holder, the evidence (each document's URL or BPO path, sha256, retrieval date and
what was checked in it), findings on names, descriptions, codes and hierarchy, derivative
works, attribution and restrictions, the open questions, decision points with options and
a recommendation, and an `architect_decision` that only points at the architect's act in
`docs/decisions/`. The decisions of 2026-10-28 are in
`docs/decisions/2026-10-28-i2a-decided.md`. Quotes are the operative words of a
notice only, at most 15 words each. The documents are downloaded to
`.upstream-cache/i2a/`, which is gitignored; none is committed. The file is hand-written,
because it is judgement; `tools/inventory/rights.py` holds its shape and its pins.

What it found, in short (the full summary is the file's `summary_for_the_architect`):

| Source | Status | Terms | The point to decide |
|---|---|---|---|
| APQC PCF 7.4 | evidence complete | ambiguous | The workbook's notice grants use, copying, publication and derivative works if the notice travels with them; APQC's website Terms (July 2026) bar public distribution unless an APQC licence agreement permits it, and bar AI use. The architect resolved the publication posture on 2026-10-29 (`docs/decisions/2026-10-29-apqc-pcf-sourcing-decided.md`): published from BPO, with APQC's notice. The clarification request was not sent |
| APQC PCF 8.0 | gap | not established | Deferred on 2026-10-29 until a version upgrade is planned |
| FEAF-II BRM 3.1 | evidence complete | unambiguous | Primary OMB documents found where the architect said, pinned, with no notice; US Government work |
| FIBF | evidence complete | ambiguous | 25 domain pages and 39 workbooks pinned; 21 workbooks carry a MITRE copyright line with unlimited rights for the Government; two embed ITIL and TBM mappings |

```bash
python tools/inventory/rights.py             # offline check (before committing; CI)
python tools/inventory/rights.py --confirm   # refetch every pinned document, require its digest
```

The offline check refuses a record outside its closed schema (an unknown key is where
catalog content would go); a source repeated, with a register id the register does not
hold, an unknown status or terms value, a gap or deferral without a reason, a complete
source with one, or ambiguous terms with no open question; evidence without a sha256, a
retrieval date or what was checked, on a host other than the rights holders' (a secondary
transcription is refused), BPO evidence without a full commit, browser-read text without
its normalisation; a catalog field (label, name, definition, description, functions,
activities, capabilities and the like) outside the findings block, or a code in a
catalog's own pattern; a quote over 15 words, a quotation mark outside a quote, a quote
from evidence the source does not list; a decision point with fewer than two options; an
`architect_decision` that is not a pointer to an existing decision record; and the
admission guard's refusals (authored-namespace IRIs, RDF text, ratification keys).
`--confirm` fetches only from obamawhitehouse.archives.gov, ussm.gsa.gov, www.gsa.gov
and, for BPO evidence without a local clone, raw.githubusercontent.com, and always from
the network rather than the cache: a moved digest means the publisher changed the
document, which is a new edition for the architect, not a re-pin. apqc.org is never
fetched: it challenges scripted clients and its Terms forbid automated access.

## The federal catalogs (Phase I-2c)

Harvested under the architect's I-2a decisions of 2026-10-28
(`docs/decisions/2026-10-28-i2a-decided.md`): BRM-1 a and BRM-2 c for the BRM, FIBF-1 c,
FIBF-2 a and FIBF-3 a for FIBF. `tools/inventory/harvest_federal.py` reads the pinned
documents from `.upstream-cache/i2a/` (named by sha256, gitignored; a missing one is fetched
from its pinned URL and must match). The pins are `config/inventory-federal-sources.yaml`,
which names evidence items whose URL and digest stay in `rights.yaml`, so each document has
one pin. Nothing is minted, grouped or merged; every entry names its document, the
document's digest and a locator (page; sheet and row; or, for the EEO page, the HTML line).
Ids are `INV-<source>-<code>-<kind>`; a code repeated inside one document keeps one entry
per row, its id carrying the row.

**FEAF-II BRM 3.1** (`feaf-brm-entries.yaml`, register SRC-GOV-06). Both OMB documents,
kept apart (BRM-2 c): the service codes and definitions table (`INV-FEAF-BRM-SCD-...`,
`brm-service`) and the taxonomy appendix (`INV-FEAF-BRM-TAX-...`: `brm-mission-sector` from
the section headings, `brm-business-function` and `brm-service` from the table rows), levels
named as the BRM names them. A service row also records the mission sector and business
function its own columns print, as printed. The taxonomy states its structure on page 1
(10 mission sectors, 40 business functions, 228 services) and its tables print 20 business
function rows and 208 service rows; the rest, 20 business functions and 20 services,
appear only in the tree diagrams, which are not harvested (the extraction stays
table-based under the closure decision of 2026-10-30). The two PDFs are read with pypdf (pinned in `requirements-dev.txt`) for
their objects only; the tool places every glyph itself and assigns it to a column by
position, and every row is accounted for or the build refuses.

**FIBF** (register SRC-GOV-05). `fibf-snapshot.yaml` lists every pinned FIBF document
(FIBF-3 a) with its status:

- **harvested**: no MITRE notice in `rights.yaml` *and* none in the bytes, and no other
  copyright, licence or proprietary notice in any header, footer, drawing, document
  property or cell. The rights were validated from the bytes, not taken from `rights.yaml`
  alone; they agree for every document.
- **withheld-mitre** (FIBF-1 c): the content is not harvested, and the snapshot lists the
  document by locator, digest and status only.
- **withheld-ambiguous**: `rights.yaml` and the bytes disagree, or another notice is present;
  treated as restricted. None today.

Draft status comes from the bytes (a cover drawing reading "Draft") or the pinned domain
page (the ITS page calls its functions and activities draft); duplicates are workbooks
whose every cell is identical (the two contract-writing workbooks), recorded both ways and
never merged. Functions and activities are in `fibf-entries.yaml`; business capabilities,
in FIBF's own meaning, are in `fibf-business-capabilities.yaml`, each with
`homonym_flag: true` (E5): a FIBF business capability is an outcome-based requirement
record, not a BCO capability type, and is neither equated with one nor excluded.

Inside a harvested document a field's text is withheld, keeping the code, when it equals
(two words or more, case and punctuation ignored) a cell of a withheld MITRE-marked
workbook or contains a whole such cell of six words or more, or when it names ITIL, TBM, AXELOS, PeopleCert or Technology Business
Management or equals a cell of a FIBF-2 a mapping column (a column whose header names
them or half of whose cells do, and the ITS workbook's cost-categorization sheet). No
mapping column is read; the snapshot lists every column that names them. Not harvested:
other FIBF components (service measures, data elements, scenarios), bibliographies, hidden
working sheets, and the EEO page's activity and capability tables, which are empty in the
pinned bytes (the browser fills them from a resource that is not pinned).

**The eleven HR business-capability lists** (`fibf-doc-hr-*-1`) carry no notice, but
their external-link targets point at files on `communityshare.mitre.org`
(`external_links_to_mitre_host` in the snapshot). Under the closure decision of 2026-10-30
(`docs/decisions/2026-10-30-closure-decided.md`), their labels and descriptions are withheld
pending adequate provenance or rights evidence, as `text-in-document-linking-mitre-host`.
Their entries keep their identifiers, locators and document digests, and their snapshot
records say `text_withheld`. `config/inventory-federal-sources.yaml` names them in
`text_withheld_documents`. The tool requires that list to be exactly the harvested
workbooks that link to a MITRE host: a new one is refused until it is listed, and one
leaves the list only by a decision. Withheld text is never released silently, in this
phase or a later one.

The same decision keeps codes that appear in independently redistributable government
documents. Code overlap is not permission to reproduce restricted material. The six-word
overlap screen is a technical safeguard, not proof of copyright clearance.

```bash
python tools/inventory/harvest_federal.py             # offline check (before committing; CI)
python tools/inventory/harvest_federal.py --rebuild   # harvest the cached pinned documents, rewrite
python tools/inventory/harvest_federal.py --confirm   # refetch every document, require byte-identity
```

The offline check refuses what `docs/DEVELOPMENT.md` lists for `harvest_federal.py`;
`--rebuild` and `--confirm` also refuse any harvested text equal to a MITRE-marked
workbook's, which needs those workbooks' bytes. `--confirm` fetches only from ussm.gsa.gov, www.gsa.gov
and obamawhitehouse.archives.gov, never from the cache. The register's SRC-GOV-05
and SRC-GOV-06 entries were corrected from this evidence under the closure decision of
2026-10-30.

## The APQC PCF (Phase I-2b): published from BPO, with APQC's notice

**The posture.** On 2026-10-29 the architect replaced APQC-1's citation-only posture
(`docs/decisions/2026-10-29-apqc-pcf-sourcing-decided.md`): PCF 7.4 element IDs,
hierarchy IDs, names and descriptions may be published, taken **only** from BPO's
repository at a pinned commit that carries BPO's `NOTICE.md`, with APQC's notice —
copied from that file, not retyped — on every PCF-bearing artifact, and a check that
refuses one without it. APQC-2 (the clarification request) is withdrawn and APQC80-1
(PCF 8.0) deferred with the 7.4-to-8.0 comparison. Nothing is ever fetched from apqc.org.
The first I-2b, which read the workbook into internal evidence and published only a status
record, is withdrawn with the posture it served: the workbook is no longer read,
`pcf-status.yaml` and the `--pcf80` delta are gone, and `.inventory-internal/` stays
gitignored only so a stale local copy cannot be committed (delete it).

**The source.** `config/inventory-pcf-sources.yaml` pins BPO commit
`2e55edd9e86a0bc20fa88a21595cc61402faa5dc`, the first with `NOTICE.md`, and two files by
sha256: `ontology/apqc-catalog.ttl` (every element as a SKOS concept with `bpo:pcfID`,
`bpo:hierarchyID`, `skos:prefLabel`, `bpo:apqcSourceText`, `skos:broader`) and `NOTICE.md`.
I-1's `config/inventory-sources.yaml` is an approved output and is not edited; the
vendored extract's pin in `config/upstream-sources.yaml` moves only by re-pin.

**The notice.** `harvest_pcf.py` takes APQC's notice from the blockquote under "## APQC's
notice" in BPO's `NOTICE.md`, unwrapping its `> ` lines into one paragraph, and refuses
unless it digests to the pinned `apqc_notice_sha256` and equals the APQC part of the
catalog's one `dct:rights` (after BPO's framing sentence and a blank line) at the same
commit. Both outputs record the `NOTICE.md` digest.

**What an entry is.** One per catalog element, sorted by hierarchy id: `id`
(`INV-PCF74-<element id>`), `pcf_element_id`, `pcf_hierarchy_id`, `level` (from the
hierarchy id: `N.0` is 1, `N.M` is 2, otherwise the number of components, checked against
BPO's level comment), `parent_pcf_element_id` (the `skos:broader`, which must be the
hierarchy parent), `name`, `description`, `bpo_iri`, `locator` (the line of the node in the
catalog at the pinned commit) and `bpo_bridge`: the capability-class entries of
`bpo-entries.yaml` whose `designated_by` names that element's catalog node, and those whose
own `pcf_code` is its id — evidence, not proof (I-1 found the bridge is not a
standing-function marker), recorded with the input's digest. The header carries the
citation, `apqc_notice`, `apqc_notice_source`, the statement that the material is APQC's
and not under this repository's MIT licence, that APQC does not endorse this work, that
APQC's marks are used only to identify the source, the counts per level, **E4 open** (no
element is judged a standing function or a capability; E4 Option A needs written,
architect-approved judgements) and **PCF 8.0 deferred**.

**`NOTICE.md` at the repository root** separates this repository's MIT work from the PCF
material, lists every PCF-bearing file (from `pcf_bearing` in the pin file), reproduces
APQC's notice and records where it was copied from. Phase I-1's `bpo-entries.yaml`
publishes PCF element IDs (`pcf_code`) and, since E7, the labels and definitions I-1 had
withheld, so it is listed as PCF-bearing and carries the notice. Until E7 it was the one
entry in the pin file's `exceptions` ("awaits E7"); E7 emptied the list, and a test pins
it empty.

```bash
python tools/inventory/harvest_pcf.py             # offline check (before committing; CI)
python tools/inventory/harvest_pcf.py --write     # fetch BPO's two files (cache, else GitHub), write both outputs
python tools/inventory/harvest_pcf.py --confirm   # fetch, rebuild in memory, require byte identity
python tools/licensing/pcf_notice.py              # the repository-wide notice gate
```

The offline check refuses an entries file that is not the generator's rendering of its
data, leaves its closed schema, has a header other than the pins, `rights.yaml` and the
decision give, an `apqc_notice` with another digest, a malformed, repeated or unsorted
entry, a parent not one level up, counts that disagree, a bridge that is not what the
committed `bpo-entries.yaml` gives, a stale `NOTICE.md`, CRLF, or the admission guard's
refusals. With BPO's files cached (or under `--confirm`, weekly in CI) both outputs must
also be a byte-identical rebuild; that is what catches a consistent hand edit of a name
or description, which the offline check cannot tell from BPO's text.

**The gate.** `tools/licensing/pcf_notice.py` reads every tracked YAML, JSON and RDF file.
A file is PCF-bearing when it holds a PCF id key (`pcf_code`, `pcf_element_id`,
`pcf_hierarchy_id`, `hierarchy_id`, `element_id`, ...) or asserts `bpo:pcfID`,
`bpo:hierarchyID` or `bpo:apqcSourceText` (by local name, in any namespace) or BPO's PCF
scheme. Each must carry the notice — for YAML or JSON a top-level `apqc_notice` equal to
it, for RDF exactly one `dct:rights` on exactly one ontology header containing it — unless
it has an exception; `NOTICE.md` must reproduce the pinned notice, be fresh, and list
exactly the PCF-bearing files. **What it cannot see:** prose. Markdown and HTML are not
read, and BPO IRIs that embed PCF element IDs (`bpo:PCF_<id>`, `bpo:P<id>`) are identifiers,
not catalog data, wherever they appear (`bpo-findings.yaml`, the specification, reviews).
