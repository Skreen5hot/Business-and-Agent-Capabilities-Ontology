# Decision record — Controlled vocabulary: direction and P0–P5 plan approved, 2026-10-23

Recorded verbatim by the setup agent (Claude Code, `claude-opus-5-5`) on 2026-10-23, at the
statement the product owner and architect, Aaron Damiano, made in session. The act is his.

**What this approves:** the direction for a Canonically Controlled Vocabulary (CCV), its scope
boundaries, and the P0–P5 rollout plan.

**What it does not do:** it does not ratify ADR-003, the P0 decision record. ADR-003 is drafted
from this approval and goes to the architect for a separate ratification act. It also ratifies
no vocabulary term and no part of specification v0.4.

---

````text
This addresses the root problems cleanly. As PO, I am approving this revised direction, the scope boundaries, and the updated rollout plan.

Here are the formal decisions and approvals on your four points:

1. **Spec §4 as Metamodel Source of Truth:** Approved. Having a single source of truth for the metamodel terms avoids duplicate maintenance and inevitable drift. Extracting definitions at build time directly from spec v0.4 §4—with CI verifying the match—is the right architecture. The vocabulary layer will strictly supply the provenance wrappers, register links, and lifecycle metadata.
2. **Draft Baseline & Real Ratification Acts:** Agreed. All terms entering in P5 must enter as `Draft`. No term will carry or compute `Ratified` without a genuine, unalterable act citing a full 40-character commit hash, valid path, and verified SHA-256 digest.
3. **Source Register Rigor:** Approved. We will strictly enforce the V/P/S/K/L taxonomy. Requiring `departs-from` annotations to cite a verified (V) or primary (P) claim protects the ontology from diverging based on secondary or unverified assertions. The 15-word quote limit and `SRC-…-Qn` keys must be hard CI failures.
4. **Minor Cleanups:** Approved across the board.
* Fully derive `lifecycleStatus` and `owl:deprecated` (never hand-authored in YAML).
* Require typed literals for `skos:notation` (`bco:PCFCode`) and pin the edition to 7.4.
* Place `sources#` in its own declared graph/home outside the SKOS concept wellformedness filter.
* Formally declare agent IRIs under our namespace rather than referencing floating URIs.



---

### Plan Approval & Sequencing

The **P0–P5 plan is approved**. The out-of-scope boundaries (deferring `#` vs. `/` to RP-5, and holding BPO catalog alignments until their namespace move) remain locked.

We will run the phases with the following handoffs:

| Phase | Developer Deliverable | PO Responsibility |
| --- | --- | --- |
| **P0: Decisions** | Draft the ADR capturing: sibling namespaces (`bco#`, `bco-metamodel#`, `bco-catalog#`, `sources#`), decision citation format (path + 40-char commit + SHA-256), immutable IRIs / revision policy, and spec §4 definition extraction. | **Review and formally ratify the ADR.** |
| **P1: Register as Data** | Deliver `docs/sources/register.yaml`, the generator for `register.md`, and the 15-word max + V/P/S/K/L validation tests. | *None (Dev self-contained; verified by green CI).* |
| **P2: LinkML Trial** | Run the determinism trial with pinned LinkML, evaluate `gen-shacl` byte stability, and provide the written go/no-go recommendation. | **Accept/sign off on the go/no-go decision.** |
| **P3: `tools/vocab/**` | Implement the YAML $\to$ Turtle build tool, deterministic serialization, derived status logic, ADR digest checkers, and spec §4 extraction tests. | *None (Dev self-contained; verified by green CI).* |
| **P4: Shapes & Site** | Implement `AUTHORED_NAMESPACES`, updated wellformedness shapes, negative test fixtures, and the site Vocabulary page. | *None (Dev self-contained; verified by green CI).* |
| **P5: Pilot** | Deliver the 8 metamodel terms and 5 catalog terms (Strategic Planning, Treasury Management, Competitive Analysis, Business Model Governance, Customer Experience Management) as `Draft`. | **Review the drafts on the generated site and stage the first ratification act.** |

### Next Steps

Run **P0** first. Please open the branch and draft the P0 decision record for my review.

Once P0 is submitted, you have the green light to open **P1** (`register.yaml`) and **P2** (LinkML trial) as parallel workstreams.
````

---

## What it rests on

The four points it answers, and the plan table it approves, were the agent's review of the
architect's second CCV proposal, given in session on 2026-10-23. The spec it names is
`specifications/Business-Capability-Ontology-v0.4.0-draft.1.md`, SHA-256
`c55fb36cdb0a38d5c87fa3bdcc458ebe55d741770104d64ddbb64a1625768f9f`. The source register it
names is `docs/sources/business-capability-definition-sources.md` at commit
`8f5c4a1b04e0d5249d0f5b4225998bbef5ec9a76` on `main`.

## Effect

- **P0 starts:** ADR-003 is drafted on branch `ccv/p0-decisions` for the architect's review
  and ratification.
- **P1 and P2 may start once P0 is submitted.** "Submitted" means ADR-003 is handed to the
  architect for review. It does not mean ratified.
- **Locked out of scope:** the `#` vs `/` question, which stays with RP-5, and BPO catalog
  alignments, which wait for BPO's namespace move.

## Notes the record must carry

- **"pin the edition to 7.4"** is the PCF edition BPO is built on (its `CLAUDE.md` at
  `6613194`). APQC published PCF 8.0 in March 2026 (register SRC-IND-01). Pinning 7.4 matches
  BPO and does not adopt 8.0.
- **"`sources#`"** is written without a project prefix. ADR-003 §D1 proposes a concrete IRI
  for it and asks the architect to confirm.
- **"P3: `tools/vocab/**`"** is quoted as written; the closing backtick is missing in the
  original. The phase is P3, `tools/vocab/`.
