# Proposal — Inventory Phase I-2: public catalogs

| Field | Value |
|---|---|
| Status | Proposal for the architect's authorization. **Not a decision.** |
| Date | 2026-10-28 |
| Prepared by | Claude Code (`claude-opus-5-5`), at the architect's request |
| Governs | `docs/decisions/2026-10-27-capability-inventory-scope-approved.md` (approved scope: D2, D5, amendments 1–3) |
| Conditions carried | `docs/decisions/2026-10-27-inventory-i1-approved.md`: I-2 verifies the applicable rights before redistribution of PCF-derived material expands |
| Depends on | I-1, merged at `ba8df1a` |

## 1. What I-2 is

The approved scope defines I-2 as the public catalogs. It runs the APQC terms check first,
then harvests:

- PCF 7.4 levels 1–2, plus level-3 nodes independently verified as standing functions;
- the PCF 8.0 delta;
- the FEAF-II Business Reference Model;
- the Federal Integrated Business Framework (FIBF).

Like I-1, I-2 produces source evidence only. It mints no IRI and generates no class,
property, axiom or vocabulary term (amendment 4). It groups and triages nothing; that is
I-4.

This proposal sets out how I-2 would be done and the decisions it needs from you before
any catalog text is written.

## 2. Proposed shape: three pull requests

| PR | Content | Writes catalog text? |
|---|---|---|
| **I-2a Rights** | For each source and edition: the terms document, pinned by digest; what the terms permit for names, descriptions, codes and hierarchy, and derivative works; the attribution required; open questions. Ends in a decision point for you | No |
| **I-2b APQC PCF** | 7.4 levels 1–2; level-3 standing-function candidates (section 5); the 8.0 delta (section 6) | Only as far as your I-2a decision allows |
| **I-2c Federal catalogs** | FEAF-II BRM and FIBF, with FIBF Business Capability entries in a file of their own (amendment 1) | Only for documents that I-2a found redistributable |

Each PR is reviewed before the next begins. Your I-2a decision is what tells I-2b and I-2c
whether text, or only codes and hierarchy, may be written.

## 3. The sources

| Source | Edition | File in hand | Register's provisional terms | Depth |
|---|---|---|---|---|
| APQC PCF, Cross-Industry (SRC-IND-01) | 7.4 | Yes. APQC's Excel export, committed to BPO and pinned in I-1 (`K014749_…Excel Version 7.4.xlsx`, SHA-256 `0e6e24b6…7d24`) | Free with registration under the licence terms shipped in the download; the register notes the file was not read and redistribution appears restricted | Levels 1–2, plus verified level-3 standing functions |
| APQC PCF, Cross-Industry (SRC-IND-01) | 8.0 (24 Mar 2026) | **No.** BPO does not carry it (SF-09) | As 7.4, unverified | Delta against 7.4 |
| FEAF-II Consolidated Reference Model, BRM (SRC-GOV-06) | BRM 3.1 (2013) | **No.** The register cites only secondary sources (Wikipedia, CIO-Wiki; claim status S) | Public domain, unverified against a primary copy | Levels 1–2 as the BRM names them |
| FIBF (SRC-GOV-05) | Per domain document as GSA publishes it; the register cites FMCF-3 FFM Business Capabilities (FY 2024) | **No** | Public domain | Functions and activities; Business Capability entries separately |

Measured from BPO's catalog at `bc64e91`, PCF 7.4 has 13 level-1 categories, 72 level-2
process groups and 350 level-3 nodes (1,921 nodes in total). I-2b would re-count these from
APQC's file itself rather than from BPO's transformation of it.

## 4. Entries and outputs

Every entry is kept separately, as in I-1 (amendment 2). Each has:

- a stable id, `INV-<source>-<code>-<kind>`;
- the register id and the edition;
- the source's own code;
- its hierarchy (parent code and level);
- a locator (sheet and row, or page);
- its rights status;
- its name and description, or the withheld marker where the rights do not allow the text.

Proposed files in `docs/sources/inventory/`:

| File | Entry kinds |
|---|---|
| `rights.yaml` (I-2a) | One record per source and edition: terms document and digest, findings, attribution text, your decision when made |
| `pcf-7.4-entries.yaml` | `pcf-category` (level 1), `pcf-process-group` (level 2), `pcf-standing-function-candidate` (level 3) |
| `pcf-8.0-delta.yaml` | `pcf-delta`: added, retired, renamed, re-coded or moved, keyed by PCF element id |
| `feaf-brm-entries.yaml` | The BRM's own levels, named as the BRM names them |
| `fibf-entries.yaml` | `fibf-function`, `fibf-activity` |
| `fibf-business-capabilities.yaml` | `fibf-business-capability`, in the source's own meaning |

**FIBF Business Capabilities are kept apart and flagged.** The register records that FIBF's
business capabilities are requirement records, outcome-based needs tied to authoritative
references. SF-10 lists them among the homonyms of "capability". I-2c records them in
their source-defined meaning, as amendment 1 requires. Each carries a homonym flag, so that
I-4 does not read them as capability types without a review.

**How entries are produced:**

- Machine-readable files (the PCF workbooks) are read by a generator from the pinned bytes,
  as in I-1.
- PDFs are read by an extraction script that records page locators. Where extraction is
  unreliable, rows are transcribed by hand, and a check requires a page locator on every
  row.
- The I-1 checks carry over: pins and digests, the admission guard, and the rights rule (a
  withheld or cite-only entry carries no text). A generated `NOTICE.md` holds each source's
  attribution.

## 5. Level-3 standing functions (D5)

D5 admits a level-3 node only when it is independently verified as a standing function. It
forbids classifying a node from its label or hierarchy level alone. I-1 found that BPO
records no standing-function marker. So I-2 has to apply a method of its own, and the method
is yours to approve.

**Option A, recommended: a recorded judgement against CM-01, reviewed by you.** A level-3
node becomes a `pcf-standing-function-candidate` only when a written judgement says that it
names an ongoing function rather than a bounded process. The test is CM-01's Standing
Function concept. Each judgement states its reason and cites at least one piece of evidence
other than the node's label or level, for example:

- a public catalog (FIBF or the BRM) names the same function as a function;
- the node's children are recurring cycles rather than steps towards an end;
- BPO bridges the node to an Organization Capability (ADR-001 R4/R6). This counts as
  evidence, not proof, since I-1 found the bridge is not a marker.

The candidates go to you in the I-2b PR. None counts as verified until you accept the list.

**Option B: defer all level-3 nodes to I-4 triage.** I-2b then harvests levels 1–2 only.
This is simpler, but it postpones the part of D5 that admits level-3 standing functions.

## 6. The PCF 8.0 delta (D2)

- The delta compares 7.4 with 8.0 at levels 1–3, keyed by PCF element id, which persists
  across editions. Each change is recorded as added, retired, renamed, re-coded or moved.
- If the rights allow only identifiers, the delta records ids and change types without
  names.
- The 8.0 file needs an APQC registration to download. I cannot create that account, so the
  delta depends on decision E3.

## 7. Rights handling until you decide

- No PCF name or description is written before your I-2a decision.
- The I-1 entries withheld as `apqc-terms-unverified` stay withheld. Lifting any of them
  changes outputs whose digests your I-1 approval records, so that needs an act of its own
  (decision E7).
- BRM and FIBF text is written only for documents that I-2a has shown to be US Government
  works with no third-party material.
- If APQC's terms are unclear, one route is to ask APQC for written permission. That would be
  a message to another organization, so sending it is your call.

## 8. Decisions requested

| # | Question | Recommendation |
|---|---|---|
| E1 | Split I-2 into I-2a (rights), I-2b (PCF) and I-2c (FEAF, FIBF), each reviewed before the next? | Yes |
| E2 | How is the APQC posture settled? | I-2a presents the terms and findings and you decide. If the terms are ambiguous, ask APQC (your call to send). Until then, PCF entries carry codes and hierarchy only |
| E3 | Who obtains the PCF 8.0 file? | You download it under your registration. It stays outside the repository unless the rights allow redistribution, and it is pinned by digest. The delta waits until then |
| E4 | Level-3 standing-function method (section 5) | Option A |
| E5 | FIBF scope | Every FIBF domain document GSA publishes at harvest time, enumerated and pinned in I-2a: functions and activities, plus Business Capability entries in their own file with the homonym flag |
| E6 | FEAF-II BRM without a primary copy | Require a primary OMB copy, pinned by digest. If none can be located, record a gap and leave the BRM out rather than harvest from secondary sources |
| E7 | When the rights permit, lift the withholding on I-1's BPO entries? | Yes, in a separate small PR after your I-2a decision, since it changes I-1 outputs whose digests you approved |

## 9. Not in scope

- Phases I-3 to I-5; any grouping, triage or crosswalk.
- New vocabulary concepts, IRIs, classes, properties or axioms.
- Changes to BPO, or re-pinning the vendored BPO extract (proposed separately in
  `docs/proposals/2026-10-28-bpo-repin.md`).
- Restricted catalogs (I-3) and defence catalogs (excluded, D4).
