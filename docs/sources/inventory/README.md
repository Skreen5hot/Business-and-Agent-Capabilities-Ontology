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
| I-2b | APQC PCF: 7.4 levels 1–3 and the 8.0 delta, as internal evidence; citation and counts in public (APQC-1 c) | **`pcf-status.yaml`**; E4 judgements deferred |
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
| `pcf-status.yaml` | I-2b: the PCF citation, the posture, counts per level and the digests of the internal evidence; no PCF content | `harvest_pcf.py --write` |
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
| APQC PCF 7.4 | evidence complete | ambiguous | The workbook's notice grants use, copying, publication and derivative works if the notice travels with them; APQC's website Terms (July 2026) bar public distribution unless an APQC licence agreement permits it, and bar AI use. A clarification request is drafted (`docs/proposals/2026-10-28-apqc-clarification-request.md`); sending it is the architect's act |
| APQC PCF 8.0 | gap | not established | The file needs the architect's registration; its notice is unread |
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

## The APQC PCF (Phase I-2b): internal evidence, public status

**What is public, and why so little.** The architect's APQC-1 c
(`docs/decisions/2026-10-28-i2a-decided.md`) makes the public posture *citation only*
until APQC answers the clarification request in writing: no PCF-derived entry — name,
description, code or hierarchy — is published in this repository or on the site, and
(E2) no substantial catalog structure. This repository is public. So the only I-2b file
here is `pcf-status.yaml`: the citation (APQC, the PCF Cross-Industry 7.4, the BPO commit
and path that hold the workbook, and its sha256), the posture, aggregate counts per level
and per entry kind, the sha256 of each internal output, and the state of E4 and of PCF
8.0. It holds no PCF name, description, element id, hierarchy id or parent.

**What is internal.** `tools/inventory/harvest_pcf.py --write` reads the PCF 7.4 workbook
BPO commits (pinned in `config/inventory-sources.yaml`) and writes, under
`.inventory-internal/i2b/` — gitignored, declared `tracked: false`, never committed:

| Internal file | What |
|---|---|
| `pcf-7.4-entries.yaml` | `pcf-category` (level 1), `pcf-process-group` (level 2) and `pcf-level-3-unjudged` (level 3), each with id `INV-PCF74-<element id>-<kind>`, element id, hierarchy id, parent, level, locator (sheet and row), name and description as the workbook gives them; level-3 entries carry BPO's bridge evidence |
| `pcf-7.4-e4-worksheet.yaml` | one empty row per level-3 node for the E4 judgement: judgement, reason, independent evidence (each with its locator), judged by, judged on |
| `pcf-7.4-to-8.0-delta.yaml` | once 8.0 is supplied: added, retired, renamed, re-coded, moved, keyed by element id, levels 1–3 |

The digests of the first two are in `pcf-status.yaml`, so the internal evidence a
reviewer is shown can be proved to be the evidence the record describes. The tool refuses
to write PCF-derived output anywhere but the internal directory, and, inside the
repository, anywhere git tracks or does not ignore (without git it writes nothing there).
`--internal-dir` may point outside the repository instead.

**BPO's bridge, as evidence.** A level-3 entry records the capability-class entries of
`bpo-entries.yaml` whose `designated_by` names a catalog node with that PCF code
(`bpo:designatesProcessType`, BPO ADR-001 R4/R6), and those whose own `pcf_code` is that
code. It is derived mechanically from the committed I-1 file, whose digest is recorded.
It is evidence, not proof: I-1 found that the bridge is not a standing-function marker.

**E4 is deferred.** E4 (Option A) asks for a written judgement of each level-3 node
against CM-01's Standing Function, with a reason, independent evidence and a locator,
submitted for the architect's approval. That needs someone to read the nodes' names, and
whether APQC's Terms allow an AI tool to process PCF content is question 6 of the
clarification request. So no judgement is made, no level-3 node is called a candidate, and
the worksheet stays empty, until APQC answers question 6 or the architect decides
explicitly how the judgements are to be made.

**PCF 8.0.** The architect obtains the 8.0 workbook under the architect's own
registration (APQC80-1 a); nothing here downloads it, and nothing ever fetches from
apqc.org. Keep the file **outside this repository** (for example in a Downloads folder;
`*.xlsx` is gitignored too, but outside is safer) and pass its path:

```bash
python tools/inventory/harvest_pcf.py --write --pcf80 "<path to the 8.0 .xlsx>"
```

The tool records the file's sha256 and size, requires it to be an xlsx, reads it with
the same reader (refusing a changed layout rather than guessing), writes the delta
internally and puts only its digests and its counts per change type in
`pcf-status.yaml`. Without `--pcf80`, 8.0 is reported as a gap and the run succeeds; once
the record says 8.0 was supplied, later runs carry that block over and say so, and
`--pcf80` re-derives it. Once the file is in hand, its in-file notice (the copyright sheet
and footers) must be pinned in `rights.yaml` by digest as an amendment to I-2a, closing
the `apqc-pcf-8.0` gap there; that amendment is a separate, reviewed change, and the file
itself is not committed unless its terms permit (E3).

```bash
python tools/inventory/harvest_pcf.py             # offline check (before committing; CI)
python tools/inventory/harvest_pcf.py --write     # build the internal outputs and the status record
python tools/inventory/harvest_pcf.py --confirm   # fetch the workbook from GitHub if not cached, require byte identity
```

The workbook is read from `.upstream-cache/` (where `harvest_bpo.py` and `rights.py`
cache it); `--write` and `--confirm` fetch it, if absent, from raw.githubusercontent.com at
the pinned BPO commit, requiring its sha256. The offline check refuses a status record
that is not the generator's rendering of its data, leaves its closed schema, disagrees
with the pins or `rights.yaml`, has counts that do not add up, records an E4 judgement, or
carries a catalog key (name, description, hierarchy id, parent and the like), a string
that reads as a PCF hierarchy id or holds a run of five or more digits, an
authored-namespace IRI, RDF text or a ratification key. With the workbook cached it also
requires byte identity with a fresh build, no PCF name, description or element id from
that build anywhere in the record, and the recorded digests on any internal output
present. CI has no copy of the workbook, so it runs the shape and guard checks; the weekly
network job runs `--confirm`, after `harvest_bpo.py --confirm` has cached the workbook.
On a new machine, `--write` regenerates the internal outputs, and their digests must then
match the record.
