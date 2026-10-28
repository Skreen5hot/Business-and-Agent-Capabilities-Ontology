# Decision record — BPO re-pin (PR #15) approved for merge, 2026-10-28

Claude Code (`claude-opus-5-5`) recorded this verbatim on 2026-10-28, from the statement the
product owner and architect, Aaron Damiano, made in session. The act is the architect's.

**What it is about:** pull request #15, the re-pin of the vendored BPO extract under R1–R5
of `docs/decisions/2026-10-28-i2-and-bpo-repin-decided.md`. It was reviewed at head commit
`f0fd0094e9b9582726ad8c234fa6334d749a0d34`, with its migration record
`docs/decisions/2026-10-28-bpo-repin-migration.md`.

| Item | Value |
|---|---|
| Pull request | #15, `stage/bpo-repin`. It was opened against `stage/proposals-i2-repin` (PR #14) and retargeted to `main` once #14 merged |
| Reviewed head | `f0fd0094e9b9582726ad8c234fa6334d749a0d34`, a single commit. It was the same commit before and after the retargeting |
| PR #14, merged first | merge commit `f21c5e48b7e5a27049f576a56dc3c416778bd66f` (2026-10-28T09:48:04Z), tree `77bb4f16a7c20611d1efcaadc7572082ced036ed`. This tree is identical to that of #14's head `c12e277`, which was #15's base. So retargeting changed neither #15's base content nor its diff: 24 files |
| Merge commit | `6731f591bc03622d630c87f5f6be91bce9b88651` (merge commit, 2026-10-28T09:49:00Z) |
| Tree | `d3892c380957a8b228904dbb9a40667b14210727` at both the reviewed head and the merge commit. What was merged is byte-identical to what was reviewed |
| Checks at the reviewed head | `Contract, licensing, tests`, `Vocabulary schema (LinkML)` and `Build and check` passed. `Deploy to Pages` and `Extracts still rebuild from the pinned sources` were skipped, because they run only on `main` and on the weekly schedule |
| Verification condition | `vendor_upstream.py --confirm` was run against `f0fd009` on 2026-10-28T09:46:49Z, with an empty download cache. Its output is attached to the PR: https://github.com/Skreen5hot/Business-and-Agent-Capabilities-Ontology/pull/15#issuecomment-6465765517. All three extracts and `vendor/NOTICE.md` are byte-identical to a fresh build from the pinned upstream files. The fetched files match the pinned SHA-256 values. A rebuild of `config/upstream-extracts.json` from the same fetch is byte-identical to the committed file |

## Final source pins at the merge commit

These are from `config/upstream-sources.yaml`:

| Source | Commit | Release | File SHA-256 | Namespace | Prefix |
|---|---|---|---|---|---|
| BFO | `044490fc5100ffed6df7d4d15cbc167698b6fdee` | `release-2024-01-29` | `6944e2c96a0d8709dc15ae5364792019e208061eda3f32311af4f3b8d8443a3b` | `http://purl.obolibrary.org/obo/` | `obo` |
| CCO | `510dad76be0ef710b65a421075af912af25342b7` | `v2.0-2024-11-06` | `e609db27478a2c8b52b9bb5eb5ac979ac323510e851c368e4d9ec7d1c153fe5b` | `https://www.commoncoreontologies.org/` | `cco` |
| BPO `ontology/apqc-ext.ttl` | `bc64e91839378e1926189c01bf184d6a22d5c1b7` | `v0.4.1 (main@bc64e91)` | `a8119728796872a1814aace8130a32cc8e42961b0bd5feaa28b736d60a0cc6fd` | `https://fandaws.com/ontology/bpo#` | `ex`, a temporary binding for BPO's genera only (R3) |
| BPO `LICENSE` | `bc64e91839378e1926189c01bf184d6a22d5c1b7` | | `2154e0221f7e5119b2d45842fcd4be421c11c5d64a459601f2c35f53710c487a` | | |

The Capability Term Inventory's historical BPO baseline stays
`66131945b525c54f44e4962f32bb1f52dfa0cd12` (R5).

## Files as reviewed

SHA-256 over the LF bytes at the merge commit:

| File | SHA-256 |
|---|---|
| `config/upstream-sources.yaml` | `b3f52b7b8e0ff485cac0d90d656bc58d6ec517a275a490e674326b05dae97216` |
| `config/upstream-extracts.json` | `a965e66d609e576ad19cb8a24ab787e6544545fea922c52293219f392bd7abac` |
| `vendor/bpo/bpo-ext-bco-extract.ttl` | `059f01139ff5c02dcf070d8472c56854177e538015249102d353ea45ea25c4bd` |
| `vendor/bfo/bfo-core-bco-extract.ttl` | `586ce381c9386c500efeb515d7951babc1039faecaa57c01960783de77af4811` |
| `vendor/cco/cco-bco-extract.ttl` | `f096418168324c66670bf04c735d90cf8cac41eeab493b6f910eb423ac230804` |
| `vendor/NOTICE.md` | `a913e60afde26c75d334d5521613602f2b7827e11ec542c48a259dbe886c3d2b` |
| `docs/decisions/2026-10-28-bpo-repin-migration.md` | `f7cafd49cf4589178efbc85c883dddc06bc6b7d876be6bb42bf914c5050fb349` |
| `docs/proposals/2026-10-28-bpo-repin-acknowledgment-draft.md` | `e5ba19e74dafbfe3e48c5499f5366c622bc48f46bb8cc3d802cc1c0a6b45e409` |
| `tools/ontology/vendor_upstream.py` | `510e2e0fe1cda0f125971969fa3cb1240c1c8f4f75379043dc52b689606f1182` |
| `tools/inventory/harvest_bpo.py` | `55769bac3efce832882bdb3cef7a1e7be4102492804d59024d63732601bf8cdb` |
| `config/inventory-sources.yaml` | `9b6043ccc49e97654571d6ade41d67a9fb49039dfe0ce7e785664d43ebfa9a52`, unchanged from the I-1 approval |

Each can be checked with `git show 6731f59:<path> | sha256sum`.

---

````text
I have reviewed PR #15 against the approved R1–R5 decisions, including the migration record, source configuration, regenerated extracts, manifest behavior, inventory cross-check, tests, and acknowledgment draft.
Decision: APPROVED FOR MERGE, subject to the verification condition below.
I explicitly accept the following:
R1 — Re-pin: Accepted. The new BPO commit and namespace are approved.
R2 — Identifier migration: Accepted. The six old-to-new IRI mappings and semantic comparisons are appropriately documented. No equivalence assertions are introduced. The approved CM-01 conceptual content remains unchanged.
R3 — Unresolved specification names: Accepted. I confirm that the 61 specification names not described by pinned upstream files should remain recorded exactly as written, without attribution to BPO's namespace.
This implements the approved requirement that proposed BCO terms must not be misrepresented as BPO entities. Their definitive namespace treatment remains part of specification v0.5.
R4 — Acknowledgment: The proposed communication is accepted as a draft only. This decision does not authorize sending it to BPO.
R5 — I-1 preservation: Accepted. The historical baseline and approved inventory outputs remain unchanged. The revised cross-check appropriately distinguishes the historical baseline from the current vendored pin.
Verification condition: Because the upstream-rebuild GitHub Actions job was skipped, record a successful `vendor_upstream.py --confirm` run against PR head `f0fd009`, showing that the committed extracts reproduce from the pinned upstream files. The existing reported local verification may satisfy this condition if its output is attached to the PR and tied to that commit.
Once the verification is recorded and required checks remain passing:

1. Merge PR #14 first.
2. Confirm PR #15 remains targeted correctly and contains only the reviewed changes.
3. Merge PR #15 using a merge commit.
4. Record the resulting merge commit and final source pins.

Do not send the BPO acknowledgment without separate authorization.
Do not rename `ex:` to `bpo:` or alter the approved CM-01 during this merge. Complete that change through the reviewed specification v0.5 and CM-01 revision process.
PR #15 is approved for merge under these conditions.
````

---

## Effect

- **The verification condition is met.** The `--confirm` output was attached to PR #15 and tied
  to `f0fd009` before any merge.
- **The steps were done in the order the decision gives:**
  1. PR #14 was merged first, at `f21c5e4`.
  2. PR #15 was retargeted to `main`. It still held only `f0fd009`, the 24 reviewed files.
  3. PR #15 was merged with a merge commit, at `6731f59`.
  4. This record states that merge commit and the final pins.
- **Accepted:**
  - **R1:** BPO is pinned at `bc64e91`, in `https://fandaws.com/ontology/bpo#`.
  - **R2:** the six old-to-new IRI mappings and the semantic comparison are accepted, with no
    equivalence assertion. CM-01's approved content is unchanged.
  - **R3:** the 61 unresolved specification names stay recorded as the specification writes
    them, attributed to no namespace.
  - **R5:** I-1's historical baseline and outputs are unchanged, and the two-state
    cross-check is accepted.
- **Standing conditions:**
  - The BPO acknowledgment is a draft only. Sending it needs separate authorization.
  - The rename from `ex:` to `bpo:`, and any change to CM-01, go through the reviewed
    specification v0.5 and the CM-01 revision process. This merge made neither.

## What this does not do

- It does not send the acknowledgment to BPO. It also does not file it in
  `communications/bpo/outgoing/`.
- It does not rename the `ex:` prefix, and it does not edit CM-01 or the specification.
- It does not decide anything about Inventory I-2a (PR #16), I-2b, I-2c or I-3 to I-5.
