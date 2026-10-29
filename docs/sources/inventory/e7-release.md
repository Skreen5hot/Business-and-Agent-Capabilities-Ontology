# E7 — Inventory I-1's APQC withholding lifted

Prepared on 2026-10-29 by Claude Code (`claude-opus-5-5`) for the architect's review, on
branch `stage/inventory-e7` from I-2b (`2dd326f`). This is a record of a change, not an
act of the architect's: the I-1 approval (`docs/decisions/2026-10-27-inventory-i1-approved.md`)
is not edited, and it stays the record of what was approved.

## Authority

- **E7**, conditionally approved in `docs/decisions/2026-10-28-i2-and-bpo-repin-decided.md`:
  after I-2a establishes the rights, lifting I-1's APQC withholding needs a separate
  reviewed PR, and the I-1 approval and historical outputs must stay traceable.
- **The decision of 2026-10-29** (`docs/decisions/2026-10-29-apqc-pcf-sourcing-decided.md`):
  section 3 takes all PCF 7.4 material from BPO at a pinned commit that carries BPO's
  `NOTICE.md`; section 4 puts APQC's notice on every PCF-bearing artifact; section 5
  authorizes preparing the E7 PR. It authorizes no vocabulary concept, class, property,
  IRI or type-admission result, and this change makes none.

## What was withheld, and what is released

I-1's rule (five kinds of evidence, unchanged and still run) tied 59 of 186 entries to
the PCF. All 59 are capability-class entries with one declaration each; no scope entry
was tied. Every withheld field is released:

| Released | Fields | Literals |
|---|---|---|
| labels | 59 | 60 (59 `rdfs:label`, 1 `skos:altLabel`) |
| definitions | 59 | 59 (`skos:definition`) |
| **total** | **118** | **119** |

Why each entry was tied (`apqc_evidence`; an entry can carry several kinds): annotation
52, IRI scheme 39, text equal to a catalog literal 38, text containing a catalog name 9,
text shared with a withheld class 2. 47 of the 59 carry a PCF code.

Each released entry's `rights_status` is `apqc-pcf-7.4` (was `apqc-terms-unverified`),
and its declaration gains `text_from`, the line it was read from at the release commit.
`apqc_evidence`, `pcf_code`, the harvest commit, the locators and everything else on the
entry are I-1's.

## Where the text came from, and the equality measured

- **I-1's harvest commit**, unchanged: BPO `bc64e91839378e1926189c01bf184d6a22d5c1b7`;
  the baseline, unchanged: `66131945b525c54f44e4962f32bb1f52dfa0cd12`.
- **The release commit**: BPO `2e55edd9e86a0bc20fa88a21595cc61402faa5dc`, the first that
  carries BPO's `NOTICE.md`, already pinned for I-2b. The nine modules that declare a
  withheld class are pinned by sha256 in the `i1_release` block of
  `config/inventory-pcf-sources.yaml`, and listed with their digests in `NOTICE.md` in
  this directory and in the `release` block of `bpo-entries.yaml`. APQC's notice comes
  from BPO's `NOTICE.md` (sha256
  `ab7d5122a2d6384b9f380f13b76bb94c31295c69aeaa56f7b1ccdf25b79953e3`) and digests to
  `582e0ea522de7927c22838ff302adfb95d247b4bd1d96fd9b73edfc83c1c7f2c`, the pinned value.
  All were fetched from raw.githubusercontent.com at the commit; nothing from apqc.org.
- **Each module carries the notice.** Each of the nine modules' ontology header has one
  `dct:rights` whose APQC part equals that notice; the tool requires it.
- **Equality.** For each of the 118 fields, the literals (property, language, text) at
  `2e55edd` were compared with those at `bc64e91`: **0 differ**. The same fields at the
  baseline `66131945`, under BPO ADR-002's namespace mapping, also equal the `bc64e91`
  text (0 differ); that is for information, since I-1 harvested `bc64e91`. Between
  `bc64e91` and `2e55edd` each of the nine modules gained one line, the `dct:rights`
  line on its ontology header, so every `text_from` line is one more than I-1's locator.
  The tool enforces the equality on every `--rebuild` and `--confirm`: a difference
  stops the build, as a question for the architect.

## I-1's files: the digests the approval recorded, and at E7

SHA-256 over LF bytes. The approved bytes are at the I-1 merge commit: check with
`git show ba8df1a:<path> | sha256sum`. `tests/test_inventory.py` requires every approved
digest below to be the one the approval records, and the first four files to have the
digest in the "At E7" column.

| File | At I-1 approval (`ba8df1a`) | At E7 | | What changed |
|---|---|---|---|---|
| `config/inventory-sources.yaml` | `9b6043ccc49e97654571d6ade41d67a9fb49039dfe0ce7e785664d43ebfa9a52` | `9b6043ccc49e97654571d6ade41d67a9fb49039dfe0ce7e785664d43ebfa9a52` | unchanged | I-1's pins, unchanged; E7's pins are in `config/inventory-pcf-sources.yaml` |
| `docs/sources/inventory/bpo-entries.yaml` | `2fd975314aa3ac839aa70ede2ec4e1dd0e78e47628d18a4878689dd5a6f5fe7b` | `96fd4631c9d5f01a20c6064919ea5b5a9b690ed9ee7344977d1ca8c4425edb42` | changed | the 59 withheld entries released, `apqc_notice` and `release` added; the other 127 entries byte-identical |
| `docs/sources/inventory/bpo-findings.yaml` | `2d0278739c088fe184947f9ee2896c0ad44885ba1c7169ad808136bd73b006e7` | `2d0278739c088fe184947f9ee2896c0ad44885ba1c7169ad808136bd73b006e7` | unchanged | IRIs and counts only; nothing in it was withheld |
| `docs/sources/inventory/NOTICE.md` | `1c56161da6e0a95a9fff228920fed8e47ce0cdc021ffcf56c420623a6d6a29de` | `519078d8718d80fbfcef78abe7c39369dc93d05d67a6bc196984349e5b7a5623` | changed | the APQC section says what was released, from where, and where the notice is |
| `docs/sources/inventory/README.md` | `edd8d13b213d10dcb2a253d25a002eb156efc209ca5f6312dd59762744205273` | `1f3f6b95b06e0e83b7d2c4297605551df55dc3cb138b77148fb39041deea44d8` | changed | the rights rule in the past tense, the E7 step, the check's refusals (also changed by I-2a and I-2b before E7) |
| `tools/inventory/harvest_bpo.py` | `3d7f4cd26170c5ffd8dba10a8a8de17f60f6c1e0bd0e6c3b858cbc7b20382609` | `0e6e172d7e10284068d683497025f9f8b7cf4926739c1cc8302f621d6969c595` | changed | the `release` step and its checks (also changed by the re-pin and I-2b before E7) |

## Other files E7 changed

| File | Before E7 (`2dd326f`) | At E7 | What |
|---|---|---|---|
| `NOTICE.md` | `cc1f3e89258f8b1faecac6135a4e603f5495046e058cb5bf7f40821159f99d38` | `bb77922bf8a318cf05e042ec2e737684e24a8c1710c2ab3cca624793797c937d` | generated; lists `bpo-entries.yaml` as carrying the notice |
| `docs/sources/inventory/pcf-7.4-entries.yaml` | `1a427e0cafe7d0341a598aee591c104a7263cf9dc4affa6301ef02d712a5545a` | `0f91b5f08fa3f6a0ec87bc4afe08190654ef88eb8ddbeea20fe6f54c19579f64` | generated; only `bridge_input.sha256`, the digest of `bpo-entries.yaml`, changed |

Also changed: `config/inventory-pcf-sources.yaml` (the `i1_release` pins; `exceptions`
now empty), `tools/licensing/pcf_notice.py` and `tools/licensing/disposition.py`
(comments), `config/repository-layout.yaml` (this file, and descriptions),
`tests/test_inventory.py` and `tests/test_pcf_notice.py`, and `docs/HANDOFF.md`.

## The notice gate

`tools/licensing/pcf_notice.py` finds two PCF-bearing files, `pcf-7.4-entries.yaml` and
`bpo-entries.yaml`; both carry APQC's notice, and its exception list is empty (it held
`bpo-entries.yaml`, "awaits E7").

## What E7 does not do

- It does not change I-1's rule, harvest commit, baseline, findings or pins, or any entry
  the rule did not tie to the PCF.
- It does not change `rights.yaml`, `config/upstream-sources.yaml`, the BRM or FIBF work,
  or anything in `drafts/`.
- It mints no IRI and admits nothing: the inventory is still source evidence.
- No site page shows inventory text, so no page gains PCF text or a footer notice.
