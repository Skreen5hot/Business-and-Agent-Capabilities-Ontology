# Communications

The record of what this repository has said to, and heard from, the teams it depends on
or that depend on it.

This record follows the communications protocol, version 1.1:
Skreen5hot/communications, PROTOCOL.md at 05068d800506bae6bbf66f6cb11d4eccc6adb312, sha256
fb3a06309eb5ecd5920a7737789df524000e5447f86c008ec16fee6203d9d74d.

That file is the only copy of the rules with authority: what a message is, its header,
the rules on editing, status, refs, decisions, agents, sending and digests, and how
messages are announced on the board (the repository's Discussions). This README does not
restate them. It states what this record adds, as the protocol allows (§ Adopting).

```text
communications/
  README.md                 this file: the protocol version followed, and the local rules
  <team>/README.md          who the team is and where its repository lives
  <team>/incoming/          messages received, copied verbatim with their source
  <team>/outgoing/          messages sent
```

## Teams

| Folder | Code in ids | Team | In `correspondents.yaml` |
|---|---|---|---|
| `bpo/` | `BPO` | Business Process Ontology | yes, `BPO` |
| `example/` | `EXAMPLE` | Ontology Template | yes, as an alias of `OT`. This record keeps the alias it already uses (§ Codes) |
| `aro/` | `ARO` | Application Requirement Ontology | **no.** No message has been exchanged. Adding ARO there is a pull request to the communications repository, needed before a first message to ARO |

This repository's own code is `BCO`.

## Local rules

These add to the protocol and do not contradict it.

1. **The checker.** `tools/communications.py` checks every message against the protocol
   and lists the threads still open. `tests/test_communications.py` runs the same checks
   on every push. It follows renames, so a byte-identical move passes. It refuses a
   message whose bytes have had more than one state, and a message that was deleted
   (Rule 1).
2. **Adding a team.** Create `communications/<team>/README.md` with a header naming the
   team and its repository (see `bpo/README.md`), and add the team's code to `TEAMS` in
   `tools/communications.py`. The checker refuses a message folder for a team it does not
   know. A new team also needs its entry in `correspondents.yaml` (§ Codes).
3. **Decisions.** The decision record is `docs/decisions/` (Rule 4).
4. **Sending is the architect's call.** That includes posting an alert or commenting on
   the board. An agent may draft a message and preview its alert (with the communications
   repository's `tools/alert.py`, without `--post`), but posts nothing without the
   architect's say-so. Whatever it posts is named as an agent's (Rule 5).
5. **The inbox at session start.** An agent gets no GitHub notifications. When a session
   starts, it checks the board's **Alerts** category for messages to `BCO` not yet held in
   `incoming/`, with the communications repository's `tools/inbox.py --code BCO`, and
   reports any it finds to the architect.
6. **Messages before the board.** Every message recorded before this adoption was sent
   before the board existed. None of them needs an alert (§ Alerts, 1).

Nothing here is published on the site.
