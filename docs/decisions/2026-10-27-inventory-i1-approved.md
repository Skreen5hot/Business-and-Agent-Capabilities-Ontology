# Decision record — Inventory I-1 (BPO harvest) approved for merge, 2026-10-27

Recorded verbatim by Claude Code (`claude-opus-5-5`) on 2026-10-27, at the statement the
product owner and architect, Aaron Damiano, made in session. The act is his.

**What it is about:** pull request #12, Phase I-1 of the Capability Term Inventory, as
reviewed at head commit `a29bdd4939b63cecf17930ffa9e63f18adb84f1b`, under the scope approval
in `docs/decisions/2026-10-27-capability-inventory-scope-approved.md`.

| Item | Value |
|---|---|
| Pull request | #12, `stage/inventory-i1` into `main` |
| Reviewed head | `a29bdd4939b63cecf17930ffa9e63f18adb84f1b` |
| Merge commit | `ba8df1a707e6766851f6563c99c65e680514d81d` (merge commit, 2026-10-27T11:57:53Z) |
| Tree | `2fc971639e654c1605f29b72c57a55741ff213fa` at both the reviewed head and the merge commit: what was merged is byte-identical to what was reviewed |
| Checks at the reviewed head | `Contract, licensing, tests`, `Vocabulary schema (LinkML)` and `Build and check` passed; `Deploy to Pages` and `Extracts still rebuild from the pinned sources` were skipped, as they run only on `main` and on the weekly schedule. The repository has no branch protection, so these are the checks the workflows define |

The source pins and findings as reviewed, SHA-256 over the LF bytes at the merge commit:

| File | SHA-256 |
|---|---|
| `config/inventory-sources.yaml` | `9b6043ccc49e97654571d6ade41d67a9fb49039dfe0ce7e785664d43ebfa9a52` |
| `docs/sources/inventory/bpo-entries.yaml` | `2fd975314aa3ac839aa70ede2ec4e1dd0e78e47628d18a4878689dd5a6f5fe7b` |
| `docs/sources/inventory/bpo-findings.yaml` | `2d0278739c088fe184947f9ee2896c0ad44885ba1c7169ad808136bd73b006e7` |
| `docs/sources/inventory/NOTICE.md` | `1c56161da6e0a95a9fff228920fed8e47ce0cdc021ffcf56c420623a6d6a29de` |
| `docs/sources/inventory/README.md` | `edd8d13b213d10dcb2a253d25a002eb156efc209ca5f6312dd59762744205273` |
| `tools/inventory/harvest_bpo.py` | `3d7f4cd26170c5ffd8dba10a8a8de17f60f6c1e0bd0e6c3b858cbc7b20382609` |

Each can be checked with `git show ba8df1a:<path> | sha256sum`.

---

````text
Subject: Review Disposition — Inventory I-1, PR #12
I have reviewed Inventory I-1 in PR #12, including the inventory README, generated entries and findings, pinned sources, APQC withholding rules, generator, and associated tests.
Decision: APPROVED FOR MERGE.
The implementation is accepted as satisfying the approved I-1 scope.
I specifically accept:

1. The selected BPO commit `bc64e91839378e1926189c01bf184d6a22d5c1b7`, retained separately from the vendored baseline.
2. The source-faithful inventory of capability classes and capability-scope entries, without automatic grouping or vocabulary admission.
3. The five APQC withholding rules, including the two additional rules for contained PCF text and shared text.
4. The decision not to infer standing-function classifications where BPO provides no explicit classification marker.
5. The generated Q-12 and Q-13 integration findings and the associated reproducibility and validation checks.

Conditions and follow-up:

* Merge only with required repository checks passing.
* Preserve the documented uncertainty concerning APQC licensing and close paraphrases. I-2 must verify the applicable rights before expanding redistribution of PCF-derived material.
* Keep the BPO integration findings separate from corrective changes to BPO.
* Do not re-pin the vendored BPO dependency as part of this approval.
* Do not generate ontology classes, object properties, subclass axioms, or approved vocabulary terms from inventory entries.

This decision authorizes merging I-1 only.
Phases I-2 through I-5 remain independently reviewable and require their own authorization under the established governance process.
Please record the approval against PR #12's exact merge commit and preserve the source pins and findings as reviewed.
````

---

## Effect

- **I-1 is merged** at `ba8df1a`, with the checks above passing at the reviewed head.
- **Accepted:**
  - the BPO pin `bc64e91`, kept apart from the vendored baseline `66131945`;
  - the inventory of 145 capability-class entries and 41 scope entries, with no grouping
    or admission;
  - the five withholding rules (59 of 186 entries withheld);
  - no standing-function entries, since BPO records no marker;
  - the Q-12 and Q-13 findings in `bpo-findings.yaml` and the checks that reproduce them.
- **Standing conditions:**
  - The APQC-rights uncertainty and the close-paraphrase residue stay documented. I-2
    verifies the rights before any PCF-derived material is redistributed further.
  - The BPO integration findings (Q-12, Q-13) are findings about BPO. Any correction to
    BPO is BPO's, and goes through the communications protocol on the architect's call;
    it is not made here.
  - The vendored BPO dependency stays pinned at `66131945`.
  - No ontology class, object property, subclass axiom or approved vocabulary term is
    generated from inventory entries.

## What this does not do

- It does not authorize phases I-2 to I-5. Each needs its own authorization.
- It does not re-pin BPO, change the vendored extract, or change CM-01.
- It does not admit, ratify or mint any capability type, concept or IRI.
