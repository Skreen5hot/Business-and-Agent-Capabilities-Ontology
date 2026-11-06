# Decision record — SE-1 approved as an exception, SE-2 closed, 2026-11-06

Recorded verbatim by Claude Code (`claude-opus-5-5`) on 2026-11-06, from the decision the
architect, Aaron Damiano, gave in session. The act is the architect's.

## What it is about

| Field | Value |
| --- | --- |
| Items | SE-1 and SE-2, §10 source adequacy of `specifications/Business-Capability-Ontology-v0.5.0-draft.3.md` at `c3f1ba2`, SHA-256 `2224f869b0ec7a1e31b0afc1c2b403ad222ea290c334bff48a93ebbb6516c574` (accepted for ratification 2026-11-04) |
| Evidence decided on | `docs/proposals/2026-11-05-se1-se2-source-exceptions.md` at `2287b77`, SHA-256 `2824ce0321c92318963b1b1d68eced96ef8c76cea776ed4c3b48baf80e1d4479`: §3, SE-2 closes by reading; SE-1 option A |
| Register at | `docs/sources/register.yaml` at `2287b77`: SRC-GOV-01 and SRC-IND-04 at V; SRC-OG-03, SRC-ISO-05 and SRC-IND-06 at S |
| CP-0 items | 15 and 16 of `docs/proposals/2026-11-05-cp0-closure-matrix.md`, decision 5 |

## The decision

The question put was "How should SE-1 and SE-2 be settled?", with the answers "Approve and
close" and "Push only". The architect answered:

````text
Approve and close
````

## The acts it contains

1. **SE-1 is approved as an exception**, option A of the evidence note, for the three
   sources still unread: ArchiMate 3.2 (SRC-OG-03), ISO 9000:2015 3.6.12 (SRC-ISO-05) and
   ITIL (SRC-IND-06). They stay at S in CD1's departures table. CD1's departure rests on the
   seven sources at V or P: UAF 1.3, NAF v4.1, IOF Core, BACM 1.1, VDML 1.1 and TM Forum
   GB1029C at V, and ISO 19440 at P. TM Forum (SRC-IND-04) left the exception when the
   architect read it on 2026-11-05.
2. **SE-2 is closed by reading.** SRC-GOV-01, DoDAF DM2, is at V for the claim CD2 makes,
   scoped to the DM2 conceptual data model page. No exception is needed.
3. **CP-0 items 15 and 16 are closed.**

## How it was carried out

- **This record.** The specification is not edited. CD1's table and §10 still show the old
  ratings, and still name ISO 9000:2015, which is withdrawn. The evidence note's §4 lists
  these for the next reviewed version.
- **Status lines.** These are updated:
  - the evidence note;
  - the CP-0 closure matrix;
  - `docs/HANDOFF.md`;
  - the roadmap's state row and its amendment log.

  Each proposal's body is unchanged.

## What it does not do

- It changes no CD, requirement or model, and edits no register entry.
- It does not decide RP-3 to RP-9, ADR-002 or the stage-completion record. CP-0 stays open,
  and OWL still waits for all of CP-0 and D5.
- It mints and asserts nothing, and makes no G1-I claim.
