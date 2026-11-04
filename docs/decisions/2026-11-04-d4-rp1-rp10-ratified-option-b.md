# Decision record — D4: RP-1 and RP-10 ratified, P1 to P3 accepted, sequencing Option B, 2026-11-04

Recorded verbatim by Claude Code (`claude-opus-5-5`) on 2026-11-04, from the decision the
architect, Aaron Damiano, gave in session. The acts are the architect's.

## What it is about

| Field | Value |
| --- | --- |
| Text ratified and accepted | `specifications/Business-Capability-Ontology-v0.5.0-draft.3.md` at `c3f1ba2` (PR #34), SHA-256 `2224f869b0ec7a1e31b0afc1c2b403ad222ea290c334bff48a93ebbb6516c574` |
| Brief decided on | `docs/proposals/2026-11-04-g1t-ratification-brief-rp1-rp10.md` at `7bd032d` (PR #37), SHA-256 `f8c6e5bb45fcb2c82d6f01185d8ead55d4f0ab25c90d833270d7d1f4073ac99d` |
| R5 disposition | draft.3 §0.2, rows R5-01 to R5-16 |
| R10 disposition | `reviews/R10-disposition.md` at `c3f1ba2`; draft.3 §0.4, rows R10-01 to R10-04 |

## The decision

````text
# D4 — G1-T Ratification Decision

Decision: Proceed with ratification and adopt sequencing Option B.

The objective is to make tranche 1 eligible for formal admission testing without prematurely authorizing OWL implementation.

## 1. Sequencing — OPTION B APPROVED

Amend the roadmap so that the first tranche may undergo G1-T admission review once RP-1, RP-2, and RP-10 are ratified.

This separates two gates:

| Gate                    | Requirement                                                  | Permitted result       |
| ----------------------- | ------------------------------------------------------------ | ---------------------- |
| Type admission          | RP-1, RP-2, RP-10 ratified; individual G1-T review completed | Recorded PASS or FAIL  |
| Ontology implementation | Full CP-0 and D5 formalization authorization                 | OWL classes and axioms |

RP-5, ADR-002, and SE-1/SE-2 remain CP-0 obligations. None is waived.

Option C is rejected. A capability must not pass an admission test whose realization-evidence rules remain unratified.

The proposed roadmap amendment is consistent with the dependency analysis in [PR #37](https://github.com/Skreen5hot/Business-and-Agent-Capabilities-Ontology/pull/37?utm_source=chatgpt.com).&#x20;

[image](https://www.google.com/s2/favicons?domain=https://github.com\&sz=32)

GitHub



## 2. Preconditions P1–P3 — ACCEPTED

I accept the following together as one architectural decision:

| Precondition         | Decision                                                                                                             |
| -------------------- | -------------------------------------------------------------------------------------------------------------------- |
| P1 — D3 exit         | Accept specification v0.5.0-draft.3, commit `c3f1ba2`, SHA-256 ending `c574`, as the text for ratification.          |
| P2 — R5 disposition  | Accept all 16 dispositions: 13 as written and 3 with the documented amendments.                                      |
| P3 — R10 disposition | Accept all four corrections, including CAP-35, CAP-34, assessment evidence requirements, and parent-class admission. |

The accepted dispositions resolve their review findings for this stage. They do not automatically close unrelated implementation issues or complete CP-0.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://github.com\&sz=32)

GitHub



## 3. RP-1 — RATIFIED

Ratify CD1 and CD2 as carried in draft.3, including their documented additions.

The approved interpretation is:

- The Organization alone bears a Business Capability.
- Its material basis is one or more relevant member agents as organized, not artifacts.
- CAP-35 requires a positive, identified member-grounding witness for each asserted Business Capability instance.
- This is an explicit BCO modeling policy, not an entailment imposed by CCO.
- Loss of an enabling platform does not automatically extinguish the capability; evidence that its basis has changed triggers reassessment.

The provider-performance rule belongs to RP-2, as the brief recommends.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://github.com\&sz=32)

GitHub



## 4. RP-10 — RATIFIED

Ratify CD3 and §8, including all five G1-T questions and three review rules.

Specifically, questions 4 and 5 are now binding for G1-T evaluation. Authorization and standing cannot substitute for an operational ability. Capability-development acts cannot count as exercise without the required justification.

Parent-class decision: Accept R10-04. The joint RP-1/RP-10 ratification serves as the architectural admission record for `bco:BusinessCapability`, with its proposed placement under BFO Disposition and CCO Organization Capability.

That record provides admission authority for the parent; it does not mint the class. Its formalization remains conditional on CP-0 and D5. No specific capability inherits admission from it.

Every specific candidate must pass its own G1-T.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://github.com\&sz=32)

GitHub



## 5. RP-2 — FAITHFULNESS CHECK AUTHORIZED

Perform the same point-by-point check used for RP-1 and RP-10, covering CD4, R5-05, R10-02, CAP-21 and CAP-34.

Pay particular attention to the distinction between participation and performance, the mandatory realization index, and the exclusion of authorization and development evidence.

RP-2 is not yet ratified. Bring forward its checked disposition for the next decision. Do not record a PASS until ratification is complete.

## 6. G1-T reviewer — ASSIGNED

The specification identifies Aaron Damiano as ratifying architect. Assign Aaron Damiano as the named approving reviewer for tranche 1.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://github.com\&sz=32)

GitHub



Claude Code or another drafting agent may prepare the G1-T records, compile evidence, and recommend a finding. The reviewer must independently confirm each record and provide the actual recorded approval. An automated draft is not a signature.

Each PASS must identify the reviewer, review date, five reasoned answers, supporting evidence, and completed constant-membership cases. No default PASS is permitted.

## 7. Immediate execution

Record these decisions verbatim, with the specification digest, on PR #37. Amend the roadmap for Option B, complete the RP-2 faithfulness check, and run the required checks.

The next decision is RP-2 ratification. After it, begin formal admission testing of the three existing I-5 candidates.

The acceptance boundary is unchanged: no new object properties, no added candidates, no OWL implementation, and no premature declaration that CP-0 is complete.

Proceed.
````

The decision arrived with citation residue from the tool it was written in: the
`?utm_source=chatgpt.com` suffix, the `&#x20;` entities, and the "[image]" favicon links,
each followed by "GitHub". They are kept as received. None is an instruction, and none is
a source this repository relies on.

## The acts it contains

1. **Sequencing, Option B.** The first tranche may undergo G1-T review once RP-1, RP-2 and
   RP-10 are ratified, and a G1-T review may record PASS or FAIL. OWL classes and axioms
   still need full CP-0 and D5. RP-5, ADR-002, SE-1 and SE-2 remain CP-0 obligations; none
   is waived. **Option C is rejected.** The roadmap is amended to match.
2. **P1 accepted: D3's exit.** Specification v0.5.0-draft.3 (`c3f1ba2`, SHA-256 above) is
   the text for ratification.
3. **P2 accepted.** All 16 R5 dispositions: 13 as written, 3 with their documented
   amendments (R5-05, R5-07, R5-09).
4. **P3 accepted.** All four R10 corrections: R10-01 (CAP-35), R10-02 (CAP-34), R10-03
   (assessment evidence), R10-04 (parent-class admission). The accepted dispositions
   resolve their findings for this stage. They do not close unrelated implementation
   issues or complete CP-0.
5. **RP-1 ratified**: CD1 and CD2 as carried in draft.3, with their documented additions,
   under the interpretation stated in section 3. The provider-performance rule belongs to
   RP-2.
6. **RP-10 ratified**: CD3 and §8, with all five G1-T questions and the three review rules.
   Questions 4 and 5 are binding.
7. **R10-04 accepted for the parent.** The joint RP-1 and RP-10 ratification is the
   architectural admission record for `bco:BusinessCapability`, placed under
   `obo:BFO_0000016` (disposition) and `cco:ont00000568` (Organization Capability). It
   does not mint the class. Formalization waits for CP-0 and D5, no specific capability
   inherits admission from it, and every specific candidate must pass its own G1-T.
8. **RP-2's faithfulness check is authorized**, covering CD4, R5-05, R10-02, CAP-21 and
   CAP-34. RP-2 is not ratified. No PASS may be recorded until it is.
9. **G1-T reviewer for tranche 1: Aaron Damiano.** A drafting agent may prepare records,
   compile evidence and recommend a finding. The reviewer confirms each record
   independently and gives the recorded approval; an automated draft is not a signature.
   Each PASS names the reviewer and review date, and gives five reasoned answers,
   supporting evidence and the completed constant-membership cases. No default PASS.
10. **Next decision: RP-2 ratification.** After it, formal admission testing of the three
    I-5 candidates begins.
11. **Unchanged boundary:** no new object properties, no added candidates, no OWL
    implementation, no declaration that CP-0 is complete.

## How it was carried out

- `docs/ROADMAP.md`: the T7 and D6 rows, D4's note, and the revision table record Option B
  (act 1).
- `docs/proposals/2026-11-04-g1t-ratification-brief-rp1-rp10.md`: its status line records
  this decision.
- `docs/proposals/2026-11-04-rp2-faithfulness-check.md`: the RP-2 check (act 8).
- `CLAUDE.md` and `docs/HANDOFF.md`: what is ratified now.
- The specification is not edited. Its §10 register and its CP-0 checklist record these
  ratifications in its next reviewed version, which is the next change to its text.

## What it does not do

It mints, admits and asserts nothing in OWL. It does not ratify RP-2 to RP-9, decide RP-5,
accept ADR-002, approve SE-1 or SE-2, or complete CP-0 or D4. No specific capability class
has a G1-T record. CM-01 is unchanged.
