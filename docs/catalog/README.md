# Candidate Capability Catalog (Phase I-4)

Candidate Business Capability types, derived in bulk from every permitted source record of
the Capability Term Inventory, with the crosswalk that traces each one back. Directed by
the architect on 2026-11-03 (`docs/decisions/2026-11-03-bulk-capability-synthesis-directed.md`),
which authorized I-4 and expanded it to the systematic derivation of candidates.
**I-4 is closed** (2026-11-07, `docs/decisions/2026-11-07-adr002-accepted-cp0-complete.md`, act 3): the generation baseline was accepted
and its four corrections made, reviewers' dispositions in effect, reviewed identifiers
pinned, qualified objects read whole, and truncated overlap lists counted.

**These are candidates, not types.** Nothing here is admitted (G1-T), ratified, minted or
axiomatized. A `BCC-xxxxxxxx` identifier is an inventory identifier, never an IRI. The
classifications are preliminary, rule-based, and state their reasons. Formal admission and
formalization follow the established gates (CM-01, DP-1, DP-2, the specification's G1-T).
The inventories under `docs/sources/inventory/` are read, never edited: every source entry
stays independent (scope approval, amendment 2), and the inventory's admission guard runs
over this directory (amendment 4).

The counts, by source and by outcome, are in **`report.md`**, computed by the generator.
No figure is typed into this README.

## The files

| File | What | Written by |
| --- | --- | --- |
| `candidates.yaml` | the catalog: one record per candidate | `synthesize.py --write` |
| `crosswalk.yaml` | every source record (all five inventories), its frame, and its interpretation or the reason it has none | `synthesize.py --write` |
| `report.md` | the counts the direction asks for, the classification and review breakdowns, the quality flags and the exceptions | `synthesize.py --write` |
| `bpo-act-types.yaml` | BPO's act types at the Phase I-1 pin, each with its genus and outputs: IRIs only | `synthesize.py --rebuild-acts` |
| `dispositions.yaml` | the pinned identifiers of reviewed candidates and the reviewers' recorded dispositions, each citing its record; read by the generator, never written by it | hand, from a recorded decision or review |
| `README.md` | this file | hand |

The three YAML files carry APQC's notice (`apqc_notice`): they cite PCF element IDs and
derive names and definitions from PCF element names. They are listed in
`config/inventory-pcf-sources.yaml` and in `NOTICE.md`, and `tools/licensing/pcf_notice.py`
holds them to it. FIBF text withheld under the closure decision of 2026-10-30 is never
read: the generator sees only the committed inventory, where it is already withheld.

## The method

`tools/catalog/synthesize.py` runs eight steps over the inventories, in order.

1. **Extract.** Every entry of `bpo-entries.yaml` (I-1), `pcf-7.4-entries.yaml` (I-2b),
   `feaf-brm-entries.yaml`, `fibf-entries.yaml` and `fibf-business-capabilities.yaml`
   (I-2c) becomes one record, with its parent from the source's own hierarchy: the PCF
   parent element; the FIBF or BRM parent code in the same document (or, for FIBF, in
   another workbook of the same domain, with codes padded to three digits); the BPO named
   superclass.
2. **Normalize.** Each label is read into a *frame*: the verbs, an **ability family**,
   and an **object phrase**. Imperative labels ("Develop and manage X") give their verbs;
   noun-phrase labels ("Records Disposal Approval", BPO class names) give a trailing
   nominal; a label that names only an artifact ("Acquisition Plan") gets the family the
   artifact implies and is marked `action_inferred`. Light verbs (perform, conduct) yield
   to the nominal after them. Acronyms are expanded, plurals folded, and a few synonyms
   merged (human capital and human resources; vendor and supplier). When the nominal is
   preceded by an adjective that would be left as the whole object ("National Defense",
   "Strategic Planning"), the frame keeps the phrase whole as its object and is marked
   `qualified`. The frame's **key**
   is the family and the folded object. The lexicon (verbs, nominals, artifact heads,
   families) is in the tool, stated, and reviewable.
3. **Generate.** A *coarse* record designates the candidate its key names: PCF levels 1
   to 3, every FIBF function and activity, every BRM mission sector, business function and
   service, every BPO capability class and scope entry. A *fine* record (PCF levels 4 and
   5, a FIBF business capability) designates only when its key is already a candidate's
   or recurs under two different parents: an ability that recurs across contexts is a
   capability in its own right; one that does not is a step of its parent. Records with
   the same key merge into one candidate, across sources. That is where duplicates go:
   process and capability are not assumed to correspond one to one.
4. **Crosswalk.** Every record that does not designate is attached to the nearest
   ancestor that does: a PCF process as **realization evidence** (with its BPO act type),
   a FIBF business capability as **requirement evidence**, a FIBF or BRM record as
   **context**. A record with nothing to attach to keeps a stated reason.
5. **Relate.** *Broader* links come from the source hierarchies (a record's nearest
   designating ancestor) and from object containment within one family ("supplier
   contract negotiation" under "contract negotiation"). A cycle is broken at its weakest
   link and reported. *Narrower* is the inverse. *Overlaps* are candidates with the same
   object under another ability, or a similar object (token Jaccard 0.5 or more) under the
   same one. *Synonyms* are the source labels merged into the candidate.
6. **Classify.** In order, the first rule that applies:

   | Classification | Rule | Review status |
   | --- | --- | --- |
   | `unresolved` | no object can be read; or every label names an artifact, the ability only inferred, from federal sources | deferred |
   | `requirement` | supported only by FIBF business capabilities, outcome-based requirement records (E5 homonym) | rejected as a type, kept as evidence |
   | `role` | the label names an agent or body and no act | rejected as a type |
   | `skill` | the object names a person's ability, outside training or developing it (CD1) | rejected as a type |
   | `function` | a catalog's top level (PCF category, BRM mission sector or business function), or a PCF level 1 or 2 label coordinating three or more objects | deferred: a whole-function type is defined only where one is (CD16, R9); E4 is open |
   | `process` | one act episode with a definite end (approve, issue, submit, register…) and no process beneath it | rejected; its acts pass to the broader candidate |
   | `capability` | otherwise: an organization's ability, with a family, an object and source support | generated-draft, needs-review or deferred |

   A `capability` is **likely** BFO/CCO-compatible when it has BPO act types as
   realization evidence (directly, or through narrower candidates), **possible** when it
   has only requirement evidence or several source records, and **unsupported** (deferred)
   when one record and nothing else stands behind it. *Likely* means only that the
   candidate fits CM-01's pattern under Organization Capability (`cco:ont00000568`) with a
   draftable realization index; the disposition alignment is decided at G1-T.
7. **Review.** The dispositions recorded in `dispositions.yaml` govern the generated
   status (below), and pinned identifiers replace the hash for reviewed candidates.
8. **Check.** Hard checks refuse to write: every source record is in the crosswalk exactly
   once, with an interpretation or a reason; identifiers are unique and well formed;
   every link points at a candidate; broader and narrower are inverse; every definition
   states the genus; the admission guard passes (no authored-namespace IRI, no RDF, no
   ratification key); every pinned key is still generated under its identifier, every
   disposition is pinned and in effect, and a retired candidate is retired into an active
   one. Quality findings are reported, not fatal: definitions sharing eight
   consecutive words with a source description, duplicate names, broken cycles, and the
   flags on each candidate.

### The flags

| Flag | Meaning |
| --- | --- |
| `no BPO act type: realization index to be drawn` | federal or BPO-only support; the index must be drawn before G1-T |
| `realization evidence only through narrower candidates` | the candidate's acts are its components' |
| `development-act-genus (CAP-06: needs a recorded reason)` | an act type under a development genus is in its evidence (CM-01, BPO Act Type) |
| `act type typed under a capability class (Q-12)` | BPO types the act under Organization Capability or a capability class |
| `BPO index member is not an act (Q-12)` | a BPO `enablesProcess` target is a capability or catalog node |
| `generic object: named with its broader candidate` | the object ("results", "risk") picks out nothing without its context |
| `qualified object: …` | the label is an adjective and an ability noun ("Strategic Planning"). The differentia is the neutral "carry out strategic planning" (or "carry out economic and financial work" when there is no noun at all), and a reader writes the real one |
| `residual category: …` | the source's "Other …" heading; the differentia says it is the source's residual work |
| `circular differentia: …` | the object is only ability words, one of them the candidate's own family ("Procurement": "obtain procurement"). The differentia is reduced to "carry out procurement", and a reader writes the real one |
| `deontic index member (G1-T question 4: …)` | an act in the evidence approves, authorizes, certifies or licenses: it confers standing, and must be re-indexed to the non-deontic act or removed |

## A candidate record

| Field | What |
| --- | --- |
| `id` | `BCC-` and the first eight hex digits of the SHA-256 of `key`, or, for a reviewed candidate, the identifier pinned in `dispositions.yaml` |
| `name` | object and ability nominal(s) from the best-ranked designating record (BPO, then PCF by level, then FIBF, then BRM) |
| `key` | the ability family and folded object that identify the candidate |
| `definition` | genus (Business Capability, CM-01; preliminary alignment Organization Capability) and differentia (the family's ability phrase over the object, the broader candidate, the act genera in its evidence). Written from the frame, never copied from a description |
| `bearer` | `cco:ont00001180` Organization, with the source context (cross-industry, federal, or both) |
| `distinctive_ability` | family, ability phrase, object |
| `classification`, `classification_reason` | as above |
| `bfo_cco_compatibility` | likely, possible, unsupported, not-assessed, not-a-capability |
| `review` | status, justification, flags. Where a disposition is recorded: `disposition` (status, date, record, and `into` for a retired candidate) and `generated`, the status the generator would give; the candidate retired into lists `retired_into_it` |
| `sources` | every designating record: inventory id, source, kind, code, PCF element id and level, label |
| `realization_evidence` | act types (genus, the record it comes through), act genera, outputs, processes beneath, FIBF requirement records, absorbed process candidates |
| `broader`, `narrower` | with the basis of each broader link (`hierarchy:` child<parent, or `object-containment:`) |
| `duplicates_merged`, `synonyms`, `overlaps` | as above. At most six overlaps are kept; `overlaps_truncated` (shown, found) says when more were found |

## Dispositions and pinned identifiers

`dispositions.yaml` is the catalog's one hand-authored input. An entry is added only from a
recorded decision or review, which it cites; the file decides nothing.

- **Pins.** Every candidate a review record cites by identifier (`tranche-1.md`,
  `admission/`, `docs/decisions/`) is pinned, key to identifier, and a test holds it to
  that. If a lexicon change re-keys a pinned candidate, the offline check fails; the fix is
  to pin the new key under the same identifier, never to drop the pin.
- **Dispositions.** `rejected`, or `retired` into another candidate. The recorded status
  governs; the generated one stays beside it, and every source record keeps its provenance.

## Regenerating, and what is checked

```bash
python tools/catalog/synthesize.py                 # offline check (before committing; CI)
python tools/catalog/synthesize.py --write         # regenerate candidates, crosswalk, report
python tools/catalog/synthesize.py --rebuild-acts  # re-read BPO's act types, then --write
```

The offline check regenerates everything in memory from the committed inventories and
`bpo-act-types.yaml`, runs the hard checks and the admission guard, and requires byte
identity with the committed files, so a hand edit fails. The output does not depend on
Python's hash seed. `--rebuild-acts` reads BPO's modules at the I-1 pin
(`config/inventory-sources.yaml`) through `harvest_bpo.py`'s digest-checked fetch, from
`.upstream-cache/` or raw.githubusercontent.com, and labels the genera from the modules
and the pinned full CCO and BFO.

## Limits

- **The normalizer is a lexicon, not a reader.** A label it misreads gets a wrong frame,
  and the candidate a wrong key; the crosswalk shows every frame so a reviewer can see
  why. Close paraphrases in different words ("staff onboarding" and "employee
  orientation") are not merged; the overlaps list is the place to find them.
- **Identifiers follow keys, except pinned ones.** A change to the lexicon that changes a
  key changes an unreviewed candidate's identifier. The 2026-11-07 stabilization re-keyed
  34 unreviewed candidates, among them two the I-4 assessment cited as fragments
  (`BCC-de84b78e`, now `BCC-3c30ed94`; `BCC-02c5912d`, now `BCC-cf593747`). Reviewed
  candidates are pinned.
- **Coverage gaps are the evidence's.** The FIBF HR business-capability lists' text is
  withheld and their functions are not harvested, so they have no interpretation; the
  report counts them by reason. I-3 (restricted catalogs) is not authorized.
- **The family is a hypothesis about the act genus.** The report counts how often BPO's
  own genus agrees, over specific families and genera only. Management and governance are
  realized in acts of many genera and are left out of that count.
- **Classification is not admission.** A `capability` here has passed no G1-T question.
  A `function` has had no E4 judgement. Definitions are drafts for a reviewer.
