# Decision record — the R11 disposition accepted as proposed, 2026-11-03

Recorded verbatim by Claude Code (`claude-opus-5-5`) on 2026-11-03, from the architect's
answer in session. The act is the architect's, Aaron Damiano's.

**What it is about:** the question put to the architect on 2026-11-02, "Do you accept the
R11 disposition as carried into draft.3?", about:

- `reviews/R11-disposition.md` at `31e168a` (SHA-256
  `90c3b7761eaa9362548d7e3405dd204f25f725ca2e5fe5bdc2d6de22515b5432`), the disposition of
  the eleven findings of R11 (`reviews/R11-cm01-practitioner-desk-review.md`, SHA-256
  `a7d774e6235383f30e85c42b3a15a7f162c8506111d4648b59a9f633ff6fa7cc`);
- `specifications/Business-Capability-Ontology-v0.5.0-draft.3.md` at `31e168a` (SHA-256
  `820175359c30f6599518c6df133e3bdeb9972f63a401d57958efa06682337b99`), which carries it.

The answer was given by choosing the option labeled "Accept as proposed".

## The act

````text
Accept as proposed
````

## How this record reads it

This is the recorder's reading, not part of the act:

- **Every row of the R11 disposition is accepted as written**: 6 accepted for v0.5 (P-01,
  P-02, P-04, P-05, P-09, P-10), 2 accepted in part (P-03, P-06), 2 already answered with a
  clarification (P-07, P-08), and 1 accepted with no specification change (P-11).
- **The text carrying them in draft.3 stands.** Roadmap §6's condition that accepted
  dispositions go into v0.5 before CP-0 is met for R11.
- **What "as proposed" settles in the disposition's points for the architect:**
  - *The P-01 escalation trigger* applies DP-1 a4 as decided. It does not extend a4.
  - *Q-06*: not made a CP-0 or release condition. R11's request is recorded in OI-24.
  - *P-10*: answered in the specification. CM-01 §4's example remains a candidate for
    CM-01's next reviewed version, and no new version is opened.
  - *`dct:date`*: carried in draft.3 as RP-6 proposes it. Like every RP item, it is
    confirmed at ratification.

## What changes

| Document | Change |
| --- | --- |
| `reviews/R11-disposition.md` | Status: accepted 2026-11-03, citing this record |
| `specifications/Business-Capability-Ontology-v0.5.0-draft.3.md` | Status lines only: the header, the §0.3 Disposition row and column, and the CP-0 checklist. No requirement changes |
| `docs/ROADMAP.md` | The §9 practitioner-review gate: R11's dispositions accepted and carried into v0.5; a revision-table row |
| `docs/HANDOFF.md` | The R11 disposition accepted |

## What it does not do

- It does not accept the R5 or R10 dispositions, or draft.3 for ratification.
- It does not approve the source-adequacy exceptions, ratify RP-1 to RP-10, accept
  ADR-002, or decide the namespace. CP-0 is not met.
- It changes neither CM-01, DP-1 nor DP-2.
