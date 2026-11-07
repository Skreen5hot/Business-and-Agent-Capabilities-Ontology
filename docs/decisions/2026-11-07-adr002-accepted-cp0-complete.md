# Decision record — ADR-002 accepted, CP-0 complete, I-4 stabilization authorized, 2026-11-07

Recorded verbatim by Claude Code (`claude-opus-5-5`) on 2026-11-07, from the decision the
architect, Aaron Damiano, gave in session. The act is the architect's.

## What it is about

The three documents of PR #46, as reviewed at commit `6aae53e`:

| Document | SHA-256 at `6aae53e` | Effect |
| --- | --- | --- |
| `docs/adr/ADR-002-organizational-capabilities.md` | `71f97176e14d4dfd7338e75284699be7fed5276473492c6b3f47a622c6a4bbf1` | Accepted (act 1); CP-0 item 17 |
| `docs/proposals/2026-11-07-cp0-stage-completion-record.md` | `0d0cfc0366e5bb05d53c7a6559d622a083f15f37b9be41328715c6e1f743b13f` | Approved; CP-0 complete (act 2); CP-0 item 18 |
| `docs/proposals/2026-11-07-i4-technical-assessment.md` | `e5fedf8f04d1b94e5519a5675da43750281d778781516ef37b3d95e121c2ba88` | Conclusion accepted; four corrections authorized (act 3) |

## The decision

````text
Subject: Architectural Decision — ADR-002, CP-0 Completion, and I-4 Stabilization
I have reviewed PR #46 and the three submitted documents.
A. Decisions Approved Now
1. ADR-002 — APPROVED
I approve ADR-002 as the consolidated architectural decision record for the Business Capability module.
It accurately consolidates the previously ratified decisions without introducing new architectural commitments.
Preserve the authority of the original ratification records where a summary differs from the underlying decision.
The six identified documentary discrepancies are accepted as administrative follow-up items. They do not reopen the architecture or block CP-0.
2. CP-0 — APPROVED AND COMPLETE
I approve the Stage Completion Record and declare CP-0 complete.
For accuracy, correct the record's accounting: items 1–16 were previously satisfied; approval of ADR-002 and this completion record satisfies items 17 and 18.
All eighteen CP-0 obligations are now satisfied under this architectural decision.
The ratified design commitments are binding. Preserve specification draft.3 as the historical ratification baseline. Bring the normative specification documentation into alignment with the ratification records through the existing controlled update process, without changing approved meanings or creating another CP-0 approval cycle.
CP-0 completion does not itself authorize Stage 05 ontology implementation.
3. I-4 — GENERATION BASELINE ACCEPTED; LIMITED STABILIZATION AUTHORIZED
I accept the technical assessment's conclusion that the bulk candidate-generation mechanism is substantially complete.
I authorize only the four identified corrections:

* Make recorded reviewer dispositions effective in the generated catalog, preserving historical provenance.
* Pin candidate identifiers that have been reviewed or admitted, including the three existing signed G1-T records.
* Correct the normalization rule that generates ungrammatical fragments.
* Report overlap truncation explicitly so reviewers know when candidate comparisons are incomplete.

These corrections must remain within the existing generator and its tests.
Preserve deterministic regeneration, source traceability, and prior admission records. Add regression tests for the corrected behavior.
Correct the stale I-4 and I-5 status statements to reflect actual authorization and completion states.
Once these four corrections pass validation, I-4 may be marked closed under this decision. No additional architectural approval is needed unless a substantive modeling conflict emerges.
B. Integration Authorized
You may record this architectural decision, update ADR-002 and the Stage Completion Record to their approved states, and merge PR #46 after the required CI checks pass.
You may also implement and merge the four explicitly authorized I-4 corrections after successful validation.
No additional approval proposal is required for purely administrative status changes or faithful implementation of these decisions.
C. Work Not Yet Authorized
Do not interpret these approvals as permission to:

* Develop a new general-purpose knowledge-engineering framework.
* Expand the synthesis generator beyond the four approved corrections.
* Automatically promote candidate capabilities into OWL classes.
* Assert generated broader links as OWL subclass relationships.
* Begin Stage 05 formalization before the applicable readiness gate is approved.

D. Next Architectural Decision
After recording CP-0 completion and stabilizing I-4, present a concise implementation proposal for the first substantial semantic-curation tranche.
The proposal should identify the existing candidates to be normalized, the expected outputs, the proposed terminology and taxonomy review process, and how the results will flow into G1-T admission and eventual OWL formalization.
Reuse the existing tooling wherever possible.
I want the next development milestone measured by actual normalized concepts, reviewed definitions, validated taxonomic relationships, and readiness for formalization.
Final decisions: ADR-002 approved; CP-0 complete; I-4 generation baseline accepted; four bounded I-4 corrections authorized. Semantic-curation and Stage 05 implementation authorization remain separate decisions.
````

## The acts it contains

1. **ADR-002 is accepted** as the consolidated decision record for the Business Capability
   module. Where it differs from a ratification record, the record governs. Its six
   documentary discrepancies are administrative follow-ups; they reopen nothing and do not
   block CP-0.
2. **CP-0 is complete.** The stage-completion record is approved, with its accounting
   corrected: items 1 to 16 were already satisfied, and this decision satisfies items 17 and
   18. The ratified commitments are binding. Specification v0.5.0-draft.3 is kept as the
   historical ratification baseline; the normative specification is brought into line with
   the ratification records through the controlled update process, with no change of
   meaning and no further CP-0 cycle. CP-0 does not by itself authorize Stage 05.
3. **I-4's generation baseline is accepted**, and four corrections are authorized, within the
   existing generator and its tests: dispositions made effective, with provenance kept;
   reviewed and admitted candidate identifiers pinned, the three signed G1-T records
   included; the fragment-producing normalization rule corrected; overlap truncation
   reported. Regeneration stays deterministic and traceable, prior admission records are
   kept, and each correction has a regression test. The stale I-4 and I-5 status lines are
   corrected. When the four pass validation, I-4 is closed under this decision.
4. **Integration is authorized:** recording this decision, putting ADR-002 and the record in
   their approved states, merging PR #46 after CI, and implementing and merging the four
   corrections after validation.
5. **Not authorized:** a general-purpose knowledge-engineering framework; generator work
   beyond the four corrections; promoting candidates to OWL classes automatically; asserting
   generated broader links as subclass axioms; Stage 05 before its readiness gate.
6. **Next decision:** after CP-0 is recorded and I-4 stabilized, a concise implementation
   proposal for the first substantial semantic-curation tranche, reusing existing tooling.
   Semantic curation and Stage 05 remain separate decisions.

## How it was carried out

- **Approved states.** ADR-002's status line says Accepted, citing this record. The
  stage-completion record's status line, its verdict, its table rows 17 and 18 and its
  completion decision say what this decision did; its integration line says #45 is merged.
  Nothing else in either document changed.
- **Status lines.** `CLAUDE.md`, `docs/DEVELOPMENT.md`, `docs/HANDOFF.md`, the closure matrix's
  status line, and the roadmap's state, D4 and O-5 rows and amendment log say CP-0 is
  complete.
- **Not done here:** the I-4 corrections (a separate PR under act 3), the specification's
  aligned version (act 2), and the curation proposal (act 6).

## What it does not do

It mints and asserts nothing, admits no candidate, and begins no Stage 03, 04 or 05 work.
