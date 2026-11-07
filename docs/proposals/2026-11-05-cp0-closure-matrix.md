# CP-0 closure matrix and the next decision package (D4)

| Field | Value |
|---|---|
| Status | **Proposed.** For the architect. It decides nothing; each closure below is the architect's act. *Since:* item 14 closed 2026-11-05, CD6 to CD11 ratified (`docs/decisions/2026-11-05-cd6-cd11-ratified.md`); items 15 and 16 closed 2026-11-06, SE-1 approved as an exception and SE-2 closed by reading (`docs/decisions/2026-11-06-se1-approved-se2-closed.md`); item 7 closed 2026-11-06, RP-3 ratified (`docs/decisions/2026-11-06-rp3-ratified.md`); item 8 closed 2026-11-06, RP-4 ratified (`docs/decisions/2026-11-06-rp4-ratified.md`); items 10 to 13 closed 2026-11-06, RP-6 to RP-9 ratified (`docs/decisions/2026-11-06-rp6-rp9-ratified.md`); this status line is the only change |
| Directed by | The execution directive of 2026-11-05, act 5, recorded verbatim on PR #38 in `docs/decisions/2026-11-05-g1t-approval-provenance-corrected.md` |
| Read from | `docs/ROADMAP.md` (D4 row, §9, §11 O-5 and O-6), specification v0.5.0-draft.3 §10 (ratification register, source adequacy, CP-0 checklist; SHA-256 `2224f869…c574`), the decision records of 2026-11-03 to 2026-11-05 |
| Prepared by | Claude Code (`claude-opus-5-5`), 2026-11-05 |

CP-0 is defined twice, in the spec's §10 checklist and in the roadmap's D4 row, and the two
agree. The roadmap adds two things: "every other applicable specification decision
ratified", and an exit recorded "with a stage-completion record". OWL needs CP-0 and D5
(Option B). G1-T admission review needs only RP-1, RP-2 and RP-10, which are ratified.

## 1. The matrix

| # | Obligation | State | Evidence | To close it |
|---|---|---|---|---|
| 1 | Practitioner review recorded, its dispositions accepted | **Done** | R11; `docs/decisions/2026-11-03-r11-disposition-accepted.md` | — |
| 2 | CM-02's approved scope carried | **Done** | spec §1, CD1, CD13; `docs/decisions/2026-10-31-d2-cm02-scope-approved.md` | — |
| 3 | R5 and R10 dispositions accepted | **Done** | D4 decision of 2026-11-04, P2 and P3 | — |
| 4 | RP-1 (CD1, CD2) | **Ratified** 2026-11-04 | `docs/decisions/2026-11-04-d4-rp1-rp10-ratified-option-b.md` | — |
| 5 | RP-2 (CD4; CD5 included) | **Ratified** 2026-11-04 | `docs/decisions/2026-11-04-rp2-ratified.md`. The reply was the button label "Ratify RP-2", read as covering CD5 | — unless the architect corrects the CD5 reading |
| 6 | RP-10 (CD3, §8), with admission of the parent class | **Ratified** 2026-11-04; the parent is not minted | the D4 decision, acts 6 and 7 | — |
| 7 | RP-3: `ex:enablesProcess` an annotation; `requiresCapability` withdrawn (CD12) | Draft, "Revised wording (R5-08)" | spec §10 register | Faithfulness check, then ratification. OI-6, finding BPO's declarations, is best done first |
| 8 | RP-4: agent manifest is description-layer (CD13) | Draft, "Consumers to be checked (OI-10)" | spec §10; roadmap O-13 | Check, then ratification. **Decide whether the OI-10 consumer check must come before ratification** |
| 9 | RP-5: the permanent namespace | **Open** | spec §10 "Open"; `tools/ontology/validate.py` `AUTHORED_NAMESPACES`, provisional "pending RP-5" | **The architect's decision**, including `#` versus `/` for all five ADR-003 D1 namespaces. Then one commit changes the list, every shape filter and `tools/vocab/build.py` |
| 10 | RP-6: type references, findings, assessment evidence (CD14) | Draft, "Revised" | spec §10 | Check, then ratification |
| 11 | RP-7: closed-world evidence (CD15) | Draft, "Revised (R5-07)" | spec §10 | Check, then ratification |
| 12 | RP-8: functional coverage and adequacy (CD16) | Draft, "Revised (R9)" | spec §10 | Check, then ratification |
| 13 | RP-9: information-layer vocabulary (CD17) | Draft, "Revised (R9, R10-03, R11 P-06)" | spec §10 | Check, then ratification |
| 14 | "Every other applicable specification decision" (roadmap D4) | **Undefined.** CD6 to CD11 sit in no register item | RP-2 check: "CD5 to CD11 are not in the register"; spec CD section: each "is proposed, not ratified" | **The architect decides the treatment**: ratify CD6 to CD11, or record them as design commitments under the ratified items that cite them |
| 15 | SE-1: CD1's list of frameworks with non-organization bearers (ArchiMate, TM Forum, ISO 9000, ITIL) | **Open**; sources at S | spec §10 source adequacy; `docs/sources/register.yaml` | One of: read the primaries and raise them to V or P; drop them from CD1 (a spec edit); or the architect approves the exception |
| 16 | SE-2: DoDAF DM2 in CD2 | **Open**; SRC-GOV-01 at S ("site returned 403") | the same | The same three options |
| 17 | ADR-002 accepted | **Not written.** `docs/adr/` holds only ADR-003 | spec §0: it "lands as ADR-002 … once ratified" | Draft ADR-002 for v0.5 after the RPs, then the architect accepts it. **Settle its target**: the layout contract and ADR-003 reserve it "for specification v0.4" |
| 18 | D4 stage-completion record | Not started | roadmap D4 row and §10 | Written last, then approved |

Open issues OI-21 to OI-25 (Stage 05 representation) are not named by CP-0, and no
document says whether they block it. This matrix treats them as not blocking, which the
architect may correct.

## 2. Where the documents disagree

1. **The spec's header and §10 boxes** still read pre-ratification. This is by design: the
   decision records leave the spec unedited, and the next reviewed version records the
   ratifications.
2. **ADR-002's target** differs: v0.4 in `config/repository-layout.yaml` and ADR-003, v0.5 in
   the spec. BPO also has an ADR-002 of its own, which `config/inventory-sources.yaml` cites.
3. **RP-5's scope** differs. The spec's register names only `bco#`, "before release", while
   ADR-003 sends `#` versus `/` for all five namespaces to RP-5.
4. **The ratification brief's precondition table** still shows P2 and P3 as open. Only its
   status line is updated, as is the convention for decided proposals.

The roadmap's §3 and `docs/DEVELOPMENT.md` were also stale. They are corrected in the
commit that adds this matrix.

## 3. The next decision package

These decisions close CP-0, smallest set first. The team prepares the evidence before
each; the act is the architect's.

| Order | Decision | Evidence the team prepares first |
|---|---|---|
| 1 | **Treatment of CD6 to CD11** (item 14) | A one-page table of CD6 to CD11, each with the RP that cites it, if any |
| 2 | **RP-3** | Faithfulness check, as for RP-2; the OI-6 lookup in BPO |
| 3 | **RP-4**, and whether OI-10 comes first | Faithfulness check; the OI-10 consumer check of `agents.json` |
| 4 | **RP-6 to RP-9** (one package or four) | Four faithfulness checks |
| 5 | **SE-1 and SE-2**: approve, close by reading, or drop | Attempt to read each primary and update its register rating |
| 6 | **RP-5**, `#` versus `/` included | An options note: the five namespaces, what each choice changes, the one-commit change |
| 7 | **ADR-002**, its target settled | The ADR drafted for v0.5 from the ratified items |
| 8 | **The D4 stage-completion record** | Drafted when 1 to 7 are recorded |

Decisions 1, 5 and 6 need no check, so they can be brought forward now. Decisions 2 to 4
wait for their checks. The documents set no order among 2 to 6. They place ADR-002 after
the RPs, and the stage-completion record last.

## 4. Boundary

This matrix adds no candidate, act, object property or OWL. It makes no G1-I claim and
declares no part of CP-0 complete. The G1-T tranche 1 records are a separate matter: they
are "AI-reviewed: PASS recommended; human confirmation pending" until the reviewer signs
(PR #38). Their signature is not a CP-0 obligation.
