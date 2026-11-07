# CP-0 stage-completion record (D4) — for the architect's decision

| Field | Value |
|---|---|
| Status | **Approved** 2026-11-07 by the architect, who declared CP-0 complete (`docs/decisions/2026-11-07-adr002-accepted-cp0-complete.md`, act 2), as reviewed at `6aae53e`, SHA-256 `0d0cfc0366e5bb05d53c7a6559d622a083f15f37b9be41328715c6e1f743b13f`. Since then only the status line, §1, items 17 and 18, the integration line and §8 changed, to record the decision |
| Date | 2026-11-07 |
| Prepared by | Claude Code (`claude-opus-5-5`), for the BCO team |
| Gate | D4, CP-0: specification §10 acceptance checkpoint and roadmap D4 row; the form is roadmap §10, "Stage-completion record" |
| Verifies | `docs/proposals/2026-11-05-cp0-closure-matrix.md`, items 1 to 18 |

## 1. Verdict for decision

**All eighteen CP-0 obligations are satisfied, and CP-0 is complete** (`docs/decisions/2026-11-07-adr002-accepted-cp0-complete.md`).
Items 1 to 16 were satisfied by earlier recorded acts. The architect's approval of ADR-002
(`docs/adr/ADR-002-organizational-capabilities.md`) and of this record satisfied items 17 and
18 on 2026-11-07. ADR-002's consistency check found no architectural contradiction; its six
documentary discrepancies are administrative follow-ups.

## 2. Approved deliverables

| Deliverable | Version | Approval |
|---|---|---|
| Specification v0.5.0-draft.3 | `c3f1ba2`, SHA-256 `2224f869b0ec7a1e31b0afc1c2b403ad222ea290c334bff48a93ebbb6516c574` | Accepted for ratification 2026-11-04, D3's exit (`docs/decisions/2026-11-04-d4-rp1-rp10-ratified-option-b.md`, act 2); ratified item by item (§4) |
| CM-01, Business Capability conceptual model | SHA-256 `292c8f36d64075b9663e159985a15b448aa933c3b5ed4baff3b2a556ca861ccc` | Approved 2026-10-26 (`docs/decisions/2026-10-26-cm01-approved-r8-r9-accepted.md`); erratum `docs/decisions/2026-10-30-cm01-stakeholder-review-erratum.md` |
| CM-02 scope note | `docs/proposals/2026-10-31-cm02-scope-note.md`, SHA-256 `35036ef2d6d0111f851af043c72cd733e83bc9e05774b014734b1d7dbc573a77` | Approved 2026-10-31 (`docs/decisions/2026-10-31-d2-cm02-scope-approved.md`) |
| ADR-002 | `docs/adr/ADR-002-organizational-capabilities.md` at `6aae53e`, SHA-256 `71f97176e14d4dfd7338e75284699be7fed5276473492c6b3f47a622c6a4bbf1` | Accepted 2026-11-07 (`docs/decisions/2026-11-07-adr002-accepted-cp0-complete.md`) |

## 3. Applicable standard and reviewers

- **Standard.** No Stage 05 standard exists, and none is required for D4. CP-0 is defined by
  the specification's §10 checklist and the roadmap's D4 row, which agree (closure matrix
  §1). CM-01 was made under `docs/standards/stage-02-conceptual-modeling.md`. The
  governance gates of roadmap §9 apply: practitioner review, source adequacy, decision
  propagation, closure, stage completion.
- **Reviewers.**
  - Aaron Damiano, architect, ratifying authority; Proxy Domain Expert for business
    process content.
  - R11, the product-owner-authorized synthetic practitioner, stands for the practitioner
    review (`docs/decisions/2026-11-02-r11-practitioner-validation-decided.md`).
  - R5 and R10, the specification reviews, with dispositions accepted.

## 4. Decisions and dispositions — the eighteen items verified

Each row was checked by reading the cited record. "Closed" means a recorded act of the
architect closes it.

| # | Obligation | State | Record |
|---|---|---|---|
| 1 | Practitioner review recorded, dispositions accepted | Closed | `docs/decisions/2026-11-03-r11-disposition-accepted.md` |
| 2 | CM-02's approved scope carried | Closed | `docs/decisions/2026-10-31-d2-cm02-scope-approved.md`; spec §1, CD1, CD13 |
| 3 | R5 and R10 dispositions accepted | Closed | `docs/decisions/2026-11-04-d4-rp1-rp10-ratified-option-b.md`, acts 3 and 4 |
| 4 | RP-1 (CD1, CD2) | Ratified 2026-11-04 | the same, act 5 |
| 5 | RP-2 (CD4, with CD5) | Ratified 2026-11-04 | `docs/decisions/2026-11-04-rp2-ratified.md` |
| 6 | RP-10 (CD3, §8), parent admission | Ratified 2026-11-04 | D4 decision, acts 6 and 7 |
| 7 | RP-3 (CD12) | Ratified 2026-11-06 | `docs/decisions/2026-11-06-rp3-ratified.md` |
| 8 | RP-4 (CD13), OI-10 for CP-0 | Ratified 2026-11-06 | `docs/decisions/2026-11-06-rp4-ratified.md` |
| 9 | RP-5, the namespace | Ratified 2026-11-07 | `docs/decisions/2026-11-07-rp5-ratified.md` |
| 10–13 | RP-6 to RP-9 (CD14 to CD17) | Ratified 2026-11-06 | `docs/decisions/2026-11-06-rp6-rp9-ratified.md` |
| 14 | Every other applicable specification decision (CD6 to CD11) | Ratified 2026-11-05 | `docs/decisions/2026-11-05-cd6-cd11-ratified.md` |
| 15 | SE-1 | Approved as an exception 2026-11-06 | `docs/decisions/2026-11-06-se1-approved-se2-closed.md` |
| 16 | SE-2 | Closed by reading 2026-11-06 | the same |
| 17 | ADR-002 accepted | Accepted 2026-11-07 | `docs/decisions/2026-11-07-adr002-accepted-cp0-complete.md`, act 1 |
| 18 | This record | Approved 2026-11-07 | `docs/decisions/2026-11-07-adr002-accepted-cp0-complete.md`, act 2 |

**Coverage.** Every CD (CD1 to CD17) and every register item (RP-1 to RP-10) is ratified by
one of the records above. The CP-0 checklist's six conditions are items 1; 2; 3; 15 and 16;
4 to 14 with 17; and 9.

**Integration.** The ratified changes are merged into `main` in dependency order: RP-3
(#42), RP-4 (#43), RP-6 to RP-9 (#44); RP-5 (#45), each after its CI passed, under the
integration authorization of 2026-11-07. Each PR's diff was reviewed for unrelated changes.

## 5. Validation results

On the branch carrying RP-5, with this record's predecessors merged:

| Check | Result |
|---|---|
| `pytest tests/` | 688 passed, 3 skipped |
| `tools/ontology/validate.py --gate` | Corpus conforms, 0 violations; every negative fixture rejected; "No new findings"; ladder 0 findings against authored terms |
| `tools/conceptual/check_models.py` | 1 model, 33 concepts, 39 relationships, 14 CQs traced, 0 decision points pending |
| The other 12 pre-commit tools | Pass |
| Site build and check | 9 pages checked |
| GitHub CI | Passed on each merged PR |

**What this does not cover.** The ontology modules are empty headers, so the validation is
of the repository, the vocabulary and the shapes, not of any capability class. No CAP
requirement is satisfied by an OWL encoding yet; that is CP-1.

## 6. Outstanding non-blocking issues

None of these blocks CP-0. The owner of every decision is the architect, Aaron Damiano; the
drafting owner is the BCO team (roadmap §11).

| Issue | Rationale for deferral | Latest gate |
|---|---|---|
| OI-4 / F-6, develops relation | CQ-11 is answered by review records meanwhile | D6 |
| OI-7 / F-10, staging state | Bounded by CAP-32 | D6 |
| OI-8 / F-8, CCO and BFO IRIs from reviews | Verified against the pins before CAP-25, CAP-34 or CAP-35 use them | D6 |
| OI-9 / F-11, BPO existential realization | Removed in BPO before a tranche takes the class | D6 |
| OI-16 / F-12, `ex:BusinessAuthorization` (BPO-side) | Only tranches touching authorization | D6 |
| OI-19, Plan has part Objective | Confirmed against a rebuilt extract | D6 |
| OI-20 / O-9, BPO integration (CM-01 Q-12 to Q-14) | Blocks D5, not D4 | D5 |
| OI-21, OI-23, OI-24, OI-25, Stage 05 representation | Kept open for Stage 05 by the RP-6 to RP-9 decision, which also said they generate no further CP-0 cycle | D6 |
| OI-22 / F-7, maturity encoding; Functional Adequacy Assessment representation | Stage 05 evaluates | D6 |
| OI-11 / F-13, evidence-graph IRIs | Instance evidence is Stage 06 | D7 |
| OI-13 / F-14, coverage register schema | Stage 06 | D7 |
| OI-14 / F-15, socio-technical bearer | Kept open by DP-1 a4; no current type needs it | CM-02's approval |
| OI-17 / F-18, versioned dictionaries | TM-1 stands meanwhile | D8 |
| OI-18, F-17, multi-party sourcing; components that are functions (Q-07); temporal bearing (Q-06) | Declared scope limits of the first release if still open | D8 |
| OI-1 / O-12, executable-release pinning | Release | D8 |
| OI-10 / O-13, consumers outside the repositories | Closed for CP-0; the release check stays | D8 |
| RP-5's resolution and publication | A release obligation by the RP-5 decision | D8 |
| CM-01 next-version candidates | Listed in `src/02_conceptual_models/README.md`; CM-01 not reopened | CM-01's next reviewed version |
| The specification's next reviewed version | Records the ratifications in its header, §3 and §10 | Before it is promoted to normative status |

The two deferrable items due at D3 are answered: F-1 (departures by source and clause) by
CD1's table and SE-1/SE-2, and F-2 (adequacy without a class) by OI-15, answered
conceptually in CD16 and CD17.

## 7. Upstream dependencies and pins

From `config/upstream-sources.yaml`, vendored as partial extracts under `vendor/`:

| Upstream | Commit | SHA-256 of the pinned source |
|---|---|---|
| BFO 2020 | `044490fc5100ffed6df7d4d15cbc167698b6fdee` | `6944e2c96a0d8709dc15ae5364792019e208061eda3f32311af4f3b8d8443a3b` |
| CCO 2.0 | `510dad76be0ef710b65a421075af912af25342b7` | `e609db27478a2c8b52b9bb5eb5ac979ac323510e851c368e4d9ec7d1c153fe5b` |
| BPO | `bc64e91839378e1926189c01bf184d6a22d5c1b7` | `a8119728796872a1814aace8130a32cc8e42961b0bd5feaa28b736d60a0cc6fd` |

The RP-3 import boundary excludes BPO's `capabilities_wiring.ttl` and
`delivery_processes.ttl` from BCO's effective graph.

## 8. Approval authority and completion decision

- **Authority:** the architect, Aaron Damiano.
- **Completion decision:** *made* 2026-11-07. ADR-002 accepted, this record approved, and
  CP-0 declared complete (`docs/decisions/2026-11-07-adr002-accepted-cp0-complete.md`). Stage 05 is not authorized by it.
- **What CP-0 completion would permit**, per the roadmap: D5, formalization readiness (the
  Stage 05 standard, the validation architecture, the first tranche's reviewed terminology
  and taxonomy baseline, and BPO's Q-12 to Q-14), which also needs T1 to T3 and T8. It
  would not by itself authorize OWL, which needs D5 too, nor admit any candidate.

## 9. Boundary

This record adds no candidate, act, object property or OWL. It makes no G1-I claim, and it
promotes no document to normative status.
