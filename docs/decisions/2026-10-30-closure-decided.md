# Decision record — closure set: PR #18, PR #20, the source register and E4, 2026-10-30

Claude Code (`claude-opus-5-5`) recorded this verbatim on 2026-10-30, from the statement the
product owner and architect, Aaron Damiano, made in session. The acts are the architect's.

**What it is about:**

| Item | Commit | SHA-256 (LF bytes at that commit) |
|---|---|---|
| PR #18: `communications/bpo/outgoing/2026-10-28-repin-acknowledgment.md` | `d00c763` | `67ca4413c6bb5c21235189de3a3a05251ad83bd5e38b434a91c98da320b19d3d` |
| PR #18: `docs/decisions/2026-10-28-bpo-repin-migration-erratum.md` | `d00c763` | `ff36b2d74f816ef830884992d7378b7f3e3c2a7fee4131d59a16e25721a37735` |
| PR #20: `docs/sources/inventory/fibf-business-capabilities.yaml` | `c061216` | `a7af841cfd4807a164410f7fb9aca2aab5d252c2f62fceb601692471089ed17b` |
| PR #20: `docs/sources/inventory/fibf-snapshot.yaml` | `c061216` | `8fd99676bd0b72d6bd2599ffac613fde74a5c0f772d52d140c9987211464871f` |
| PR #20: `tools/inventory/harvest_federal.py` | `c061216` | `a0efe5c074a0b88d79785b35d62a8a4abd02acb594da850b0f3839fb0d3f3238` |
| The #17 record, `docs/decisions/2026-10-28-bpo-repin-approved.md` | `a8fb873` | `c183aa23df7f2d481051e6dc85b16fd2acc348ac199c085498bc3b417c258979` |
| The source register, `docs/sources/register.yaml` | `a8fb873` | `a49bf34026c06debe1352c38537ec995352aeda46fd8a03ad4f3cc733ae9a203` |
| E4 as first decided, `docs/decisions/2026-10-28-i2-and-bpo-repin-decided.md` | `a8fb873` | `0a8b10a308a697c300b747163ce84bd312aeaff864202ea95c034b3fd50a44a0` |

PR #18 was merged before this record was written, as merge commit `a8fb873` (its head
`d00c763` merged with `main` at `05be175`, and checked first). Each can be checked with
`git show <commit>:<path> | sha256sum`.

---

````text
Subject: Closure Decisions — PR #18, PR #20, Source Register, and E4
I have reviewed the outstanding items and want them closed before starting additional inventory work.
PR #18 — APPROVED FOR MERGE
I accept the BPO acknowledgment and the separately recorded migration erratum.
The acknowledgment has already been delivered to BPO and must not be sent again.
Preserve the immutable outgoing communication and historical records. Merge PR #18 after confirming the reviewed content and required checks remain valid.
PR #20 — APPROVED SUBJECT TO ONE RIGHTS CORRECTION
I accept the I-2c inventory architecture, federal-source harvesting approach, source pins, generated evidence records, and the implemented MITRE and ITIL/TBM safeguards.
I specifically decide:

1. HR capability lists: Withhold the public labels and descriptions of the eleven HR lists linked to `communityshare.mitre.org` pending adequate provenance or rights evidence. Preserve their locators, identifiers, hashes and withholding status.
2. Shared codes: Permit retention of identifiers appearing in independently redistributable government source documents, without treating code overlap as blanket permission to reproduce restricted material.
3. Six-word screening: Accept the implemented overlap screen as a technical safeguard, not as proof of copyright clearance.

Do not silently release withheld material in subsequent phases.
The FEAF-II BRM extraction may remain table-based, but its documentation must continue to identify the 20 business functions and 20 services omitted because they appear only in tree diagrams.
After the targeted HR correction, regenerate affected outputs, rerun all required checks on the resulting PR head, and record the updated counts and hashes.
If the checks pass and no additional material issue arises, PR #20 is authorized for merge.
Smaller corrections — APPROVED
PR #17: Add a separate factual erratum clarifying that the upstream extract-rebuild GitHub Actions job runs on scheduled or manually dispatched workflows, rather than automatically on every `main` push. Preserve the original approved record.
SRC-GOV-05: Reconcile the FIBF source-register entry with the verified copyright and third-party provenance evidence. Avoid describing all FIBF content as unconditionally public domain.
SRC-GOV-06: Add the verified OMB FEAF-II BRM 3.1 primary sources, with source locators and digests, and update the verification claims. Preserve historical secondary references as such where useful.
E4: I approve Option A: independently justified, documented, architect-reviewed classification of level-3 standing-function candidates against CM-01.
This closes E4's method decision only. No standing-function candidate is approved by this act. Present actual candidate judgments through their separate review process.
Required closure procedure
Please:

1. Merge PR #18 under the approved communication disposition.
2. Make the narrowly scoped HR withholding correction to #20, validate the final branch and merge it.
3. Submit the #17 erratum, source-register corrections and E4 decision record as one small documentation/governance PR, with appropriate validation.
4. Preserve approved historical records and all source-version provenance.
5. Report the resulting merge commits and confirm that no outstanding decision from this closure set remains.

Do not begin I-3, I-4, I-5 or additional taxonomy development until this closure set is complete.
These decisions do not authorize ontology IRIs, OWL classes, object properties, subclass assertions, or new vocabulary admissions.
````

---

## Effect

- **PR #18.** Merged. Its outgoing message is the record of an acknowledgment already
  delivered as BPO issue #1, and it is not sent again.
- **PR #20, HR capability lists.** The eleven HR business-capability lists are the
  `fibf-doc-hr-*-1` workbooks. Their external-link targets point at files on
  `communityshare.mitre.org`.
  - Their entries keep their identifiers, locators, document digests and withholding status.
  - Their labels and descriptions are withheld as `text-in-document-linking-mitre-host`.
  - `config/inventory-federal-sources.yaml` names the eleven and cites this record.
  - The harvester refuses a harvested workbook that links to a MITRE host and is not named
    there, so a new one cannot be released silently.
- **PR #20, shared codes and the six-word screen.** Identifiers from independently
  redistributable government documents are kept. The overlap screen is a safeguard, not a
  clearance.
- **PR #20, the BRM.** Extraction stays table-based. The documentation keeps naming the 20
  business functions and 20 services that appear only in the tree diagrams.
- **The governance PR:**
  - the #17 erratum, as a separate record;
  - the SRC-GOV-05 and SRC-GOV-06 corrections;
  - E4's method record.
- **E4.** The method is decided as Option A. No standing-function candidate is approved.

## PR #20 after the HR correction

`tools/inventory/harvest_federal.py --rebuild` regenerated the outputs from the cached
pinned documents. The offline check and a rebuild test pass.

| Count | Before (`c061216`) | After |
|---|---|---|
| FIBF business capabilities | 2,749 | 2,749 |
| of which with text withheld | 6 | 1,563 |
| withheld as `text-in-document-linking-mitre-host` | 0 | 1,557 |
| withheld as `text-in-mitre-marked-document` | 6 | 6 |
| FIBF functions and activities, with text withheld | 58 + 206, 15 | 58 + 206, 15 |
| BRM entries | 445 | 445 |
| FIBF documents: harvested / withheld-mitre / withheld-ambiguous | 19 / 21 / 0 | 19 / 21 / 0 |

The 1,557 entries are every entry from the eleven HR lists. Each keeps its id, code,
parent codes, locator and document digest. Only its `description` (the capability
statement; these entries have no name) and its `rights_status` changed. No entry from any
other document changed.

| File | SHA-256 at `c061216` | SHA-256 after |
|---|---|---|
| `docs/sources/inventory/fibf-business-capabilities.yaml` | `a7af841cfd4807a164410f7fb9aca2aab5d252c2f62fceb601692471089ed17b` | `0dcc107f3b4cfaf8236e6e757a4be27fa0efb1c2ee66a10cb86ff8db7d082b1a` |
| `docs/sources/inventory/fibf-snapshot.yaml` | `8fd99676bd0b72d6bd2599ffac613fde74a5c0f772d52d140c9987211464871f` | `e66fb1561a9392953f15dd21b13edee6e6db91b209247fc4ab60ed737cc67532` |
| `docs/sources/inventory/fibf-entries.yaml` | `e6e9a5b9ad5fbe4c88b327b74c317a3ba4712e7d88369ea9ff91d44749e55f5d` | `cc7c80b1957c3ce5eb5cd96e877ff64422ae18c3ede327c3e562f22bc8297eff` |
| `docs/sources/inventory/feaf-brm-entries.yaml` | `4582816177418cf3944b1eb7337c846e745c37c39d41181464efebde6aab76f1` | `3cb7ef37439c7fd3623be8f36075aafa6d93d0746e252e682de83b59dae620e4` |
| `docs/sources/inventory/NOTICE-federal.md` | `8edcf35038a0be5b922cbcdd276b6cb8da89dc8ecf1542597e25305e9141fa35` | unchanged |
| `config/inventory-federal-sources.yaml` | `e370c49a4382ad98c859c2c38cff6a3b7ba9dc2963cf28b9849a4ca3b8d968d9` | `1f84d61ca7e84168086d2a71bdcc0ffc109d27b5f2b2455593be107a00d62d8b` |
| `tools/inventory/harvest_federal.py` | `a0efe5c074a0b88d79785b35d62a8a4abd02acb594da850b0f3839fb0d3f3238` | `3a177659fc4e402e70a04f286b39bafa12444e5254dd0b88499e72623cf43272` |

`fibf-entries.yaml` and `feaf-brm-entries.yaml` changed only in their header's list of
decisions, which now names this record.

## What this does not do

- It does not authorize ontology IRIs, OWL classes, object properties, subclass assertions
  or vocabulary admissions.
- It does not authorize I-3, I-4, I-5 or further taxonomy development before the closure
  set is complete.
- It does not release any withheld material.
