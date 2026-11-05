# SE-1 and SE-2, the source exceptions — evidence for CP-0 decision 5

| Field | Value |
|---|---|
| Status | **Proposed.** For the architect. It decides nothing; closing or approving an exception is the architect's act |
| Closes | CP-0 closure matrix items 15 and 16 (`docs/proposals/2026-11-05-cp0-closure-matrix.md`, decision 5) |
| Read from | Specification v0.5.0-draft.3 §3 CD1's departures table, §10 source adequacy (SHA-256 `2224f869…c574`); `docs/sources/register.yaml`; the five sources' own sites, 2026-11-05 |
| Prepared by | Claude Code (`claude-opus-5-5`), 2026-11-05 |

## 1. What the exceptions are

The roadmap's source-adequacy gate requires every source the specification relies on to be
at V or P in the register, or under an approved exception. §10 asks for two exceptions, each
"to close by" CP-0, by reading the primary, dropping the source, or approval:

- **SE-1.** CD1 says frameworks admit bearers other than organizations. Four sources in its
  departures table are at S or L: ArchiMate 3.2 (SRC-OG-03), TM Forum GB1029C (SRC-IND-04),
  ISO 9000:2015 3.6.12 (SRC-ISO-05) and ITIL (SRC-IND-06).
- **SE-2.** CD2 says DoDAF DM2 counts technology inside the capability. Its source,
  SRC-GOV-01, was at S because the site "returned 403".

## 2. What reading found

Each primary was attempted on 2026-11-05 in the built-in browser. No account was created,
no terms were accepted and no bot check was answered.

| Source | Attempt | Result | Register now |
|---|---|---|---|
| SRC-GOV-01, DoDAF DM2 | The DoD CIO's DM2 conceptual data model page, now served under `/Library/DoD-Architecture-Framework/` | **Read.** It defines Capability through "ways and means (activities and resources)". A Resource includes performers and materiel, and a Performer may be human, automated, or both. So technology is on the capability side, as CD2 and SF-06 say | **V**, scoped to that page. The definition paraphrase is corrected: a Service is a Performer giving access to capabilities. The companion's sentence on DM2 services is corrected to match |
| SRC-OG-03, ArchiMate 3.2 | The 3.2 and 3.1 online chapters at pubs.opengroup.org | Redirected to an Open Group sign-in. Registration is free, but creating an account is not the agent's to do | S; L, with the date recorded |
| SRC-IND-04, TM Forum GB1029C | The standard's page | Held the agent at a bot-verification page. **The architect read it**, signed in as a member, on the v2.0.0 HTML page (the PDF download did not work), and transcribed the definition in session. It takes ArchiMate's wording: a capability is possessed by an active structure element, such as an organization, person or system. It adds that capabilities are realized by people, processes, information and systems | **V**, scoped to the definition on that page, with who read it recorded |
| SRC-ISO-05, ISO 9000:2015 | The catalogue page, and the Online Browsing Platform at 3.6.12 | The catalogue page confirms number 45481 and edition 4. It also shows **ISO 9000:2015 is withdrawn, revised by ISO 9000:2026**. The platform shows the term only after its Terms of Use are accepted, which were not | S. The number is no longer "unverified", and the citation records the withdrawal |
| SRC-IND-06, ITIL | The register's glossary copy at it.utah.edu | No longer served. ITIL itself is paid | S. The dead link is recorded |

## 3. What remains to decide

**SE-2 can close.** Its source is now at V for the claim CD2 makes, so no exception is
needed. Two caveats: the scope is one page, not the v2.02 PDF or the data dictionary; and
SF-06 already rested on NAF and UAF at V.

**SE-1 shrinks to three sources.** TM Forum is now at V and supports CD1's claim. ArchiMate,
ISO 9000 and ITIL stay at S. TM Forum's realization sentence also places systems on the
capability side, beside DM2, which adds to SF-06 (CD2), not to SE-1. The options for the
remaining three are §10's three:

| | Option | What it takes | Effect |
|---|---|---|---|
| A | **Approve SE-1 as an exception for the three.** Recommended | The architect's act | §10's reason stands. CD1's departure is already established by seven sources at V or P: UAF 1.3, NAF v4.1, IOF Core, BACM 1.1, VDML 1.1 and TM Forum GB1029C at V, and ISO 19440 at P. The three only lengthen the list. Nothing in CD1's text changes |
| B | **Drop the three from CD1's departures table** | A new reviewed version of the specification | CD1 is ratified under RP-1, so this is not an editorial change. The departure stands; its list is shorter |
| C | **Read the three primaries** | Access the agent cannot obtain alone: an Open Group account for ArchiMate (free); the architect's permission to accept ISO's browsing terms; an ITIL licence | Each source read would move to V or P. ISO raises a further question: whether CD1 should cite the 2026 edition, now that 2015 is withdrawn |

**C can be partial.** An Open Group account and ISO's terms would cover two of the three in
one sitting, and the exception would then shrink to ITIL alone.

## 4. For the next specification version, whatever is decided

- CD1's table and §10 name ISO 9000:2015, which is now withdrawn.
- CD1's table and §10 still show TM Forum at S; L, and CD2's sources and §10 still show DM2 at S.

The decision records do not edit draft.3, so these wait for the next reviewed version.

## 5. Boundary

This note adds no candidate, act, object property or OWL. It changes no CD, requirement or
model, and adds no source. The register changes are dated status records for entries
already cited. It makes no G1-I claim and declares no part of CP-0 complete.
