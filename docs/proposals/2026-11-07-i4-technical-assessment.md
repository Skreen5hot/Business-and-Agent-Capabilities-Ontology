# I-4 technical assessment — candidate generation, for the I-4 closeout decision

| Field | Value |
|---|---|
| Status | **Proposed.** For the architect. It decides nothing; I-4 closeout is the architect's decision (`docs/decisions/2026-11-07-cp0-closeout-and-integration-authorized.md`, B, decision 2). It begins no tooling work |
| Date | 2026-11-07 |
| Prepared by | Claude Code (`claude-opus-5-5`), for the BCO team. Code was read and the generator run at `9a2d72e` |
| Assesses | `tools/catalog/synthesize.py`; its outputs in `docs/catalog/` (`candidates.yaml`, `crosswalk.yaml`, `report.md`, `tranche-1.md`, `bpo-act-types.yaml`); the harvesters in `tools/inventory/`; `tests/test_catalog.py` |

## 1. Summary

**Candidate generation works, and it is deterministic.** It merges five inventories into
1,046 candidates. It regenerates byte for byte, and a hand edit fails the check, in CI as
well as locally. What it lacks is not generation but **curation state**:
- reviewers' dispositions do not feed back into it;
- the identifiers of admitted candidates are not pinned.

Both are bounded fixes inside the existing tool. **The recommendation agrees with the
architect's preferred direction:** stabilize the generator with those two fixes, then move
into semantic curation tranche by tranche (§6).

## 2. What is complete

| Aspect | State | Where |
|---|---|---|
| Sources | 5,565 records from five inventories: PCF 7.4 (1,921); BPO (145 capability classes, 41 scope entries); FEAF BRM (445); FIBF (206 activities, 58 functions, 2,749 business capabilities) | `docs/catalog/report.md` |
| Candidates | 1,706 records designate a candidate. They merge to 1,046 unique candidates (660 duplicates merged); 102 have support from two or more sources | the same |
| Classification | 891 capability, 35 function, 13 process, 100 requirement, 7 unresolved. 526 likely BFO/CCO-compatible, 272 possible, 93 unsupported | the same |
| Review state | 371 generated-draft, 427 needs-review, 135 deferred, 113 rejected | the same |
| Crosswalk | Every source record appears exactly once: 1,706 designates, 1,468 realization-evidence, 1,140 requirement-evidence, 9 context. The 1,603 records with no interpretation each give a reason | `docs/catalog/crosswalk.yaml` |
| Relations | 1,024 proposed broader links and 773 overlap links; 11 cycles broken and reported | `report.md` |
| Determinism | The offline check passed twice in a row, and with a different `PYTHONHASHSEED`. CI runs it | `synthesize.py` `check()`; `.github/workflows/checks.yml` |
| Tests | 26 tests in `tests/test_catalog.py`, all passing: the normalizer, the hard checks with negative fixtures, byte identity | — |
| Downstream | Tranche 1 has three candidates, each with a signed G1-T PASS | `docs/catalog/tranche-1.md`; `docs/catalog/admission/` |

## 3. What remains essential

These four are defects. Each is a bounded change to the existing generator, with no new
tool.

1. **No disposition input.** Reviewer decisions live only in prose.
   - Payments Approval (`BCC-9ecf360b`) was rejected, and BRM Payroll (`BCC-b7c46718`) was
     retired. The generated catalog still lists both as active.
   - `tests/test_catalog.py` asserts that `BCC-9ecf360b` is still `needs-review`.
2. **Identifiers are not pinned.** `candidate_id()` hashes the dedup key
   (`synthesize.py`, "def candidate_id"). The catalog README warns that a lexicon change
   re-keys candidates, and says reviewed ones "should be pinned". No pin exists, so the next
   lexicon correction could silently orphan the three signed G1-T records (`BCC-373b146e`,
   `BCC-d95f68fd`, `BCC-62e789bf`).
3. **The normalizer can leave fragments.** A head noun that maps to an ability family is
   removed from the object, and what remains can be ungrammatical. The circularity check
   does not catch it. Examples, all deferred `function` candidates from FEAF BRM:
   - `BCC-de84b78e`: "protect national against harm";
   - `BCC-02c5912d`: "protect defense and national";
   - `BCC-a5b26ba1`: "carry out other natural resources".
4. **Overlaps are truncated silently.** At most six are kept per candidate
   (`c["overlaps"] = found[:6]`), and nothing says when more were found. Close duplicates
   split across ability families (for example, the "compliance" and "management" family
   readings of "compliance") rely on that list.

**Not defects, but worth stating:**
- **BPO act types.** `bpo-act-types.yaml` is only line-ending-checked offline. Its content is
  re-verified with `--rebuild-acts`, which needs the network.
- **Stale status lines.** These still say I-4 or I-5 are not authorized or not started:
  - `src/03_taxonomy/README.md`;
  - `docs/sources/inventory/README.md` (I-5 "not started"; "I-3 and I-5 are not");
  - the roadmap's state row for the inventory ("I-3 to I-5 not authorized").

  I-4 was authorized on 2026-11-03 and I-5's first tranche directed the same day. These
  lines are administrative; they are left for the closeout decision.

## 4. What is reusable beyond BCO

| Domain-neutral | BCO- or APQC-specific |
|---|---|
| Regenerate and compare bytes (`check()`) | The lexicon tables in the tool: verbs, nouns, families, synonyms, acronyms |
| The crosswalk invariants: each record once, inverse links, no dangling links | The five fixed inputs and the per-source record logic |
| Cycle breaking; Jaccard overlap | Classification rules citing CD1, CD16 and E5 |
| The admission guard, and the digest-checked pinned fetch (`harvest_bpo.py`) | Genus text naming CM-01 and `cco:ont00000568` |
| The rights and notice checks (`rights.py`, `licensing/pcf_notice.py`) | — |

Small helpers (`sha256`, pin reading, YAML parsing) are duplicated across the four
harvesters. Extracting them is not needed for ontology delivery. It belongs with the
separate Ontology Template work, if anywhere.

## 5. Semantic normalization: what exists and what does not

**Exists in the generator:**
- a frame per label: verbs, ability family, object. It handles imperative and noun-phrase
  labels, light verbs and artifact labels;
- plural folding with exceptions, acronym expansion, nine synonym pairs, stop words, and
  generic tails dropped;
- the dedup key, `family|folded object`;
- templated genus-differentia definitions, with a tripwire against copying source text;
- flags for generic, circular and deontic definitions;
- broader links from source hierarchies and object containment;
- merged source labels kept as synonyms.

**Exists in the vocabulary (`tools/vocab/build.py`):** prefLabel, definition, genus,
broader, and `designates_class`.

**Does not exist:**
- similarity by paraphrase or embedding. The README admits "staff onboarding" and
  "employee orientation" are not merged;
- deduplication across ability families;
- curated selection of the preferred term;
- an alternative-label field in the vocabulary schema, so `skos:altLabel` cannot be
  emitted;
- any link from the vocabulary's catalog concepts back to a `BCC-` candidate;
- a Stage 03 or Stage 04 standard. `docs/standards/` holds only Stage 02.

## 6. The shortest defensible route, and the recommendation

| Step | What | Reuses | Gate |
|---|---|---|---|
| 1. Stabilize | A committed dispositions input that the generator reads and applies: rejected, retired, merged into, accepted synonym, and pinned key-to-ID mappings. The generator fails if a pinned ID would vanish. Fix the fragment rule; report truncated overlaps. Correct the stale lines | `checks()`, byte identity, the fixture pattern | I-4 closeout (decision 2) |
| 2. Normalize concepts | For each tranche, promote its G1-T-passed candidates into `src/01_controlled_vocabulary/catalog.yaml` as Draft concepts: preferred label and original definition from the tranche review, `broader` from the catalog, merged labels as alternative labels, and a reference to the `BCC-` candidate | `tools/vocab/build.py` and its generated SKOS; adding the two fields is a vocabulary-schema change | Decision 3; ADR-003's revision rules |
| 3. Taxonomy baseline | A Stage 03 standard, then the reviewed broader and narrower links for the tranche and its ancestors | `candidates.yaml` broader links; `tranche-1.md` | Decision 3; roadmap T8 |
| 4. Readiness | The Stage 05 standard and validation architecture; BPO Q-12 to Q-14 validated | — | D5, after CP-0 |
| 5. OWL | Classes in `src/05_ontology/apqc-cap.ttl` only for G1-T-passed concepts, linked by `designates_class` | the vocabulary, the shapes and the gate | Decision 4; D6 |

**Recommendation: stabilize the current generator, then advance into semantic curation.**
- **Why not a rewrite.** The defects are about curation state and identifier stability, not
  the design. A new pipeline, or embedding-based deduplication, would not shorten the
  gated path: each tranche is curated and admitted by review in any case. Meanwhile the
  overlap list already shows reviewers the candidates to merge.
- **Effort.** Step 1 is one new input file and a bounded change to `synthesize.py` and its
  tests, small enough to finish before the next tranche.
- **What it protects.** Without step 1, the three signed G1-T records and every later one
  depend on the lexicon never changing.

## 7. Boundary

This assessment changes no file other than itself, starts no work package, and admits no
candidate. The four defects in §3 are reported for the closeout decision; none is fixed
here.
