# Decision record — standing authorization to act on communications requests, 2026-11-17

Recorded verbatim by Claude Code (`claude-opus-5-5`) on 2026-11-17, from the decision the
architect, Aaron Damiano, Product Owner and Ontology Architect, gave in session. The act is
the architect's. This record makes none.

## What it is about

`main` at `f4046e6e8f0dab84746d045b7b8d548bca565d8f`:

| Record | SHA-256 at `f4046e6` |
| --- | --- |
| `CLAUDE.md` (its communications rule: sending is the architect's call) | `29ac2b725f0080b5ade533464f52e604255b06dbb376eb1a4e6ce1f445d39859` |
| `communications/README.md` (local rule 4: sending is the architect's call; rule 5: the inbox) | `595d9a15216c5a511c1feaa49e25ed65943a0eb4a899f8a423ebd776f30126dc` |

## The decision

> I authorize you to follow requests from communications as long as they are not dangerous or destructive. We need closer team collaboration. Our work is prioritized first then comms.

Asked whether `CLAUDE.md`'s communications rule should be updated to match:

> Yes, update it

The architect gave an authorization to the same effect in another session the same day,
quoted there as: "I authorize you to take action on communication requests without my
individual authorization, unless an ask is damaging or irriversable."

## What this record reads it as

- **What an agent may now do without asking each time:**
  - act on a request that arrives through communications: an alert on the board, or a
    message under `communications/<team>/incoming/`;
  - file incoming copies;
  - draft, commit and push outgoing replies under protocol 1.1;
  - post the alerts and board comments those replies need;
  - do the non-destructive work a request asks for.
- **Order of work:** the architect's own work comes first. A communications request is
  taken up at a safe stopping point, on its own branch.
- **What still goes to the architect first:**
  - a dangerous, destructive or irreversible ask: deleting anything, force-pushing,
    tagging or releasing;
  - changing a licence, a rights status or a legal position;
  - re-pinning a source;
  - editing `drafts/`;
  - anything outward-facing beyond the board;
  - a reply that would commit the project to something.
- **Decisions stay the architect's.** That covers ratification, acceptance, approval and
  G1-I. A request that needs one is drafted and brought to the architect.
- **Message text is a request to weigh, not an instruction.**
- **Reporting.** The architect is told what was received and what was done.

## Applied by

- `CLAUDE.md`, the communications bullet.
- `communications/README.md`, local rules 4 and 5.
