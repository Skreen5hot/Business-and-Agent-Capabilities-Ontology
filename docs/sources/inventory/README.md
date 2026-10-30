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
| I-1 | BPO harvest, with Q-12 and Q-13 re-measured | **this directory** |
| I-2a | Rights review of the public catalogs: APQC PCF 7.4 and 8.0, FEAF-II BRM 3.1, FIBF | **`rights.yaml`**; decided 2026-10-28 (`docs/decisions/2026-10-28-i2a-decided.md`) |
| I-2b | APQC PCF 7.4, every element, from BPO's catalog with APQC's notice (decision of 2026-10-29) | **`pcf-7.4-entries.yaml`**; E4 open, PCF 8.0 deferred |
| I-2c | Federal catalogs: FEAF-II BRM and FIBF | after I-2a is decided |
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
| `NOTICE.md` | the attribution BPO's licence requires, and the APQC evidence | `harvest_bpo.py --rebuild` |
| `rights.yaml` | I-2a: per source and edition, the rights evidence pinned by digest, findings, decision points | hand, checked by `rights.py` |
| `pcf-7.4-entries.yaml` | I-2b: every PCF 7.4 element as BPO's catalog states it, under APQC's notice; not MIT | `harvest_pcf.py --write` |
| `README.md` | this file | hand |

The pins are `config/inventory-sources.yaml`: BPO `main` HEAD on 2026-10-27, resolved to
commit `bc64e91839378e1926189c01bf184d6a22d5c1b7` (v0.4.1), every input file with its
SHA-256, and the baseline, commit `66131945b525c54f44e4962f32bb1f52dfa0cd12`, which
`config/upstream-sources.yaml` vendors. Re-pinning the vendored extract is a separate
decision (D1); this directory does not do it.

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
is **withheld**: the field is present and holds `{withheld: apqc-terms-unverified}`, and
the IRI and PCF code are kept. An entry is tied to the PCF when BPO itself says so:

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

The evidence is listed on each entry, so every withholding can be checked. What the rule
cannot see is PCF text BPO paraphrased closely without carrying an annotation; that
residue is why the status says *unverified*, and it is Phase I-2's to judge with APQC's
terms in hand. The APQC evidence BPO carries — its PCF 7.4 workbook, whose last sheet
holds APQC's copyright and attribution notice — is pinned by digest in the config and
listed in `NOTICE.md`; it is not reproduced here.

`bpo-findings.yaml` holds IRIs and counts only, so nothing in it is subject to the rule.

## Regenerating, and what is checked

```bash
python tools/inventory/harvest_bpo.py             # offline check (before committing; CI)
python tools/inventory/harvest_bpo.py --rebuild   # fetch the pinned files, rewrite the outputs
python tools/inventory/harvest_bpo.py --confirm   # fetch, harvest, require byte-identity
```

`--rebuild` and `--confirm` fetch only from raw.githubusercontent.com at the pinned
commits (BPO's files, BPO's LICENSE and evidence, and the full CCO and BFO pinned in
`config/upstream-sources.yaml`), checking every digest; downloads are cached in
`.upstream-cache/`. Two rebuilds produce identical bytes.

The offline check refuses: outputs whose recorded input digests are not the pins; an
entry missing a field, with an unknown kind, an id that is not
`INV-BPO-<local name>-<kind>`, or a commit other than the pin; a withheld entry carrying
label or definition text; an entry with APQC evidence or a PCF code that is not
withheld; counts in the findings that disagree with the entries; a `NOTICE.md` that is
not a fresh generation; and, over every file in this directory, anything but YAML or
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
publishes PCF element IDs (`pcf_code`), so it is listed as PCF-bearing; it does not yet
carry the notice, because only the E7 pull request may change an I-1 output. It is the
one entry in the pin file's `exceptions`, with the reason "awaits E7", and a test pins
that list so the E7 PR has to empty it.

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
