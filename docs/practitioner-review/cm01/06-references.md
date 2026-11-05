# References

Each document is identified by its path in the project's repository and the SHA-256 digest of the exact text supplied to you. A copy of each is supplied with this package. The status column says how much weight each document carries.

## Approved — the subject of the review

| Document | Version and digest | Status | Read it for |
| --- | --- | --- | --- |
| CM-01 Business Capability Conceptual Domain Model, `src/02_conceptual_models/CM-01-business-capability.md` | 0.1.0. SHA-256 `292c8f36d64075b9663e159985a15b448aa933c3b5ed4baff3b2a556ca861ccc` | **Approved** 2026-10-26 as the conceptual baseline. The approved text is draft.5 (SHA-256 `a59e3cd4149693ce388deaa7c8953242a8c3355e4c7eef96d094c8e90a75b5a0`); version 0.1.0 differs from it only in recording the approval | Everything: §1 scope, §3 the five patterns, §4 concepts, §6 boundaries, §7 DP-1 and DP-2, §9 assumptions and open questions |
| DP-1 decision record, `docs/decisions/2026-10-25-dp1-rp1-grounding-boundary.md` | As supplied | **Approved** (2026-10-25): Option A with amendments a1 to a4 | The grounding boundary, if you want the decision itself rather than CM-01's account of it |
| DP-2 decision record, `docs/decisions/2026-10-26-dp2-rp10-admission-attribution.md` | As supplied | **Approved** (2026-10-26): Option A with amendments b1, b3, b4 and b5; b2 rejected | Admission and attribution |
| Erratum to CM-01 §10, `docs/decisions/2026-10-30-cm01-stakeholder-review-erratum.md` | As supplied | A correction of record (2026-10-30). CM-01 itself is unchanged | CM-01 §10 credits two earlier ontological reviews, R8 and R9, with meeting its stakeholder-review gate. The erratum corrects that: the gate was met by the architect's review as product owner. Your review is a separate practitioner review, which supplements that approval |

CM-01 is also published on the project's public site, on its Models page.

## Proposed — context only, not the subject of the review

| Document | Version and digest | Status | Read it for |
| --- | --- | --- | --- |
| BCO Specification, `specifications/Business-Capability-Ontology-v0.5.0-draft.2.md` | 0.5.0-draft.2. SHA-256 `7b0911b8eeb51201396e228b98c588dade7d616a3ba154a752b4d227ee3e956b` | **Proposed.** A draft under architectural review. Not ratified, and may change | How CM-01 is proposed to become formal rules. Its §3 design decisions (CD1 to CD17), §7 competency questions and §8 tests G1-T and G1-I are the most readable parts. Its §6 validation requirements (CAP-nn) and Turtle examples are technical and optional |

The specification currently in force is version 0.4.0-draft.1, itself a draft; v0.5 is proposed to replace it. You do not need to read v0.4.

## How to tell approved from proposed

- Anything in CM-01, DP-1 or DP-2 is **approved**. You may still disagree with it (file 01).
- Anything that appears only in the v0.5 specification is **proposed**: design decisions (CD), requirements (CAP), ratification points (RP), and open issues (OI). Comments on it are welcome, but the review is of CM-01.
- Where the two seem to differ, CM-01 is the approved statement. A difference you notice is itself a useful finding.
