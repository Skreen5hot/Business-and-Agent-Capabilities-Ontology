# R10 Disposition — Specification v0.5.0-draft.1: Architectural Review

Disposition drafted by Claude Code (claude-opus-5-5) at the architect's direction, 2026-10-31. It answers review R10 of specification 0.5.0-draft.1 with 0.5.0-draft.2 on the same pull request. It decides nothing. Accepting this disposition, accepting the R5 disposition, and accepting v0.5 for ratification are the architect's acts.

| Field | Value |
| --- | --- |
| Status | Proposed. Not accepted |
| Review | `reviews/R10-v05-draft1-review.md`, filed verbatim as received |
| Reviewed artifact | `specifications/Business-Capability-Ontology-v0.5.0-draft.1.md` 0.5.0-draft.1 (commit `853fc0a`, SHA-256 `c4dbd0e2fc8d3ec8d3c3bf0c515d69f6f8bbc590960e6f4c703706c14fc74635`). Kept unchanged as review provenance |
| Answered in | `specifications/Business-Capability-Ontology-v0.5.0-draft.2.md` 0.5.0-draft.2, on the same branch (`spec/v0.5`, PR #33). Its §0.4 summarizes this table |
| Decisions it rests on | CM-01, approved 2026-10-26; DP-1 and DP-2; the R8 and R9 dispositions as accepted; the D2 scope approval. None is reopened, and no CM-01 text changes |
| Effect on status | None. Draft.2 is under review, filed as `documentation`, not as the specification in force. v0.4 keeps that role. No ratification record is altered |

R10 kept draft.1's architecture and required four corrections. This disposition answers them in four rows: three accepted and done in draft.2, and one clarification given in draft.2. Nothing R10 accepted is redesigned. No class, object property, subclass axiom or IRI is minted, and no vocabulary concept is ratified.

## Change summary

1. **A positive grounding witness (R10-01).** Every asserted Business Capability instance now needs at least one asserted basis, `obo:BFO_0000218`, to an identified member agent of its bearer. That is the new CAP-35.
   - The supporting assessment (CAP-26) shows that the organization is able. The witness says in which members that ability is grounded.
   - The single-member case is kept: one member suffices (DP-1 a1).
   - The witness is a member agent. Every basis object still falls under CAP-25: a member part of the bearer, never an artifact.
   - An instance of a class not yet admitted is an Organization Capability claim, not a Business Capability claim. No basis is asserted for it (a2), so it needs no witness. CQ-1 reports it apart.
2. **Performance, not participation (R10-02).** CAP-34 now requires a member agent of the bearer to *perform* the realizing act, following CM-01 RL-14 (*is performed by*).
   - Taking part in an act that others perform does not satisfy it. Neither does naming only the organization as performer.
   - The vendor-performance fixture is added: PayCo staff run Acme's payroll while an Acme clerk takes part without performing.
   - The relation is chosen at Stage 05 under §3.1's reuse order. None is minted.
   - *has participant* is no longer the relation the check names.
3. **Criteria and evidence on every completed assessment (R10-03).** CM-01 defines a Capability Assessment as stating one finding and citing its evidence and criteria. CD14 and CAP-27 now require that for every finding, not only `partial`:
   - exactly one finding;
   - at least one `dct:conformsTo` naming criteria with a `dct:identifier`;
   - at least one `dct:source`.

   The other parts of this correction:
   - An evaluation without a finding, criteria or evidence is an *incomplete evaluation*. It is not a Capability Assessment and is never a map entry. Nothing is minted for it, and how it is represented, if at all, is OI-23.
   - `absent`, *partly met* and *not met* must rest on evidence that establishes them, never on a failure to find evidence. Gate C checks that criteria and evidence are cited. Gate F checks that the evidence establishes a negative finding.
   - CAP-33 carries the same rule for Functional Adequacy Assessments.
   - Instance patterns 1, 2 and 6 now cite criteria and evidence. The map's `absent` entry rests on evidence of the lack. An incomplete evaluation is shown kept out of the map.
4. **Parent-class admission (R10-04).** `bco:BusinessCapability` is the definition G1-T tests specific types against. It is not a specific type and has no index, so G1-T cannot be asked of it.
   - Its admission is the architect's ratification of CD1 to CD3 (RP-1, RP-10) at CP-0. That ratification record is its admission record, and it is minted only after it.
   - Admission does not pass down. CAP-04 now requires every specific class to carry a PASS G1-T record of its own. No specific class may cite the parent's record.
   - CAP-32 still applies to each specific class.

Counts: 34 live requirements (CAP-35 added) and 1 retired; 14 competency questions (CQ-1, CQ-6 and CQ-13 annotated); one open issue added (OI-23). §0.2's R5 rows R5-01, R5-05 and R5-11 are updated to match. The R5 disposition stays proposed.

## Disposition table

"§" without a document is spec 0.5.0-draft.2. Fixture lists are the requirement's "Fixture" column. Each fails unless marked *passes*. A fixture marked (F) is a gate F review case, not a SHACL case.

| ID | Finding (R10 ref) | Disposition | Sections revised | Validation requirements | Fixtures |
| --- | --- | --- | --- | --- | --- |
| R10-01 | Positive grounding evidence: CAP-25 constrains asserted bases but requires none. Define an enforceable grounding-evidence requirement consistent with DP-1 and G1-I. Keep the single-member case. No artifact parts in the basis | Accepted (done in draft.2) | §0.1 DP-1 row; §0.2 R5-01; CD2 new bullet "A grounding witness for every bearing claim"; §5 has material basis row; §5 instance pattern 1 (single-member basis, class admitted); CQ-1; §8 G1-I question 1; §8 gates C and F; §10 RP-1, OI-8, CP-1 | **CAP-35** (new; FAIL · C, F): every Business Capability instance has at least one `obo:BFO_0000218` to an identified member agent of its bearer, and those members are the ones G1-I question 1 names. CAP-25 is unchanged and still constrains each basis object | *Negative:* a Business Capability instance with a bearer and a supporting `present` assessment but no basis (R10's required fixture); an instance whose only basis is an artifact (also CAP-25); (F) a basis member the G1-I record does not name. *Passes:* a single-member basis, the sole treasurer of a small firm; a staged-class instance with no basis (not a Business Capability instance, a2) |
| R10-02 | Organizational performance witness: participation is insufficient. Align CAP-34 with CM-01 RL-14. Add a vendor-performance fixture. The relation is a Stage 05 decision; no new object property | Accepted (done in draft.2) | §0 Prefixes (*is performed by* named by label, replacing *has participant*); §0.2 R5-05; CD2 "The provider's work is the provider's"; CD4; §5 relation table (row *is performed by*); §5 instance pattern 1 comment; §5 new paragraph "The vendor case" after instance pattern 3; §8 G1-I question 3; §10 RP-2, OI-8 | **CAP-34** (revised; FAIL · C; encoding at Stage 05): at least one member agent of the bearer performs every act that realizes a K1 instance. Taking part does not satisfy it, nor does naming only the organization as performer | *Negative:* the vendor case, where PayCo staff perform a payroll run asserted to realize Acme's capability while an Acme clerk takes part (supplies inputs, receives the report) without performing it (R10's required fixture); a provider's process with no consumer member involved; an act whose only named performer is the organization. *Passes:* an Acme member performs the act; an act performed jointly by an Acme member and vendor staff |
| R10-03 | Assessment evidence and criteria. Align CD14, CAP-27, CAP-33 and the examples with CM-01: every completed assessment has one finding on identifiable criteria and evidence. Keep incomplete evaluations apart. Never turn inadequate evidence into `absent` or *not met*. Review the map entries | Accepted (done in draft.2) | §0.2 R5-11; CD14 (three new bullets replacing two); CD17 (Functional Adequacy Assessment findings); §4 Capability Assessment and Functional Adequacy Assessment rows; §5 source / conforms to row; §5 instance pattern 1 (criteria added), pattern 2 (map entries rewritten; incomplete evaluation shown outside), pattern 6 (evidence per finding; the incomplete case); CQ-6, CQ-13; §8 G1-I closing sentence; §8 gate F; §10 RP-6, RP-9, OI-23 (new), CP-0 | **CAP-27** (revised; FAIL · C, F): exactly one finding, at least one `dct:conformsTo` to criteria with a `dct:identifier`, and at least one `dct:source`, for every finding. Negative findings rest on evidence that establishes them (F). **CAP-33** (revised; FAIL · C, F; encoding at Stage 05): each adequacy finding cites evidence that establishes it. A statement that cannot establish all three is incomplete, and *not met* is never put in place of an unestablished dimension | *CAP-27 negative:* an evaluation typed as an assessment with no finding; two findings; a `present` or `absent` finding with no criteria; criteria with no identifier; an `absent` finding with no source; (F) an `absent` finding whose only source records that no evidence of presence was found. *CAP-27 passes:* an `absent` finding citing criteria and a staffing review that establishes the lack; an incomplete evaluation kept out of the graph. *CAP-33 negative:* two findings; a finding without criteria; a *not met* finding with no source; (F) a *not met* finding whose only source records that the dimension could not be assessed; an integration finding in a Capability Assessment |
| R10-04 | Parent-class admission: state how the generic parent satisfies architectural approval or G1-T. Specific types still need their own G1-T | Clarified (done in draft.2) | CD3 new bullet "The parent is admitted architecturally, not by G1-T"; §4 Business Capability row (Parents column); §6 class kinds (K1); §8 G1-T opening paragraph; §8 gate F (the parent's ratification record); §10 RP-10 | **CAP-04** (revised; FAIL · C, F): every specific class under `obo:BFO_0000016` or `bco:BusinessCapability` carries its own PASS G1-T record. The parent cites the ratification record that admits it. No other class may cite that record. CAP-32 is unchanged | *Negative:* a specific class under the parent with no G1-T record of its own; a record without the worked cases; a specific class citing the parent's ratification record as its admission; the parent minted with no ratification record. *Passes:* the parent citing its record; a specific class with its own PASS |

**Tally:** 3 accepted and done in draft.2 · 1 clarified in draft.2 (4 rows).

## Points for the architect to check

These are choices draft.2 makes in answering R10. None is a decision taken.

- **CAP-34 is stricter than RL-14's range.** CM-01 RL-14 lets an act be performed by a Member Agent *or an Organization*. CAP-34 still lets the organization be named as performer, but does not count that as the witness, because it is the claim the check exists to support. If naming the organization should suffice in some case, CAP-34 needs an exception.
- **The parent's admission record is the ratification act.** Draft.2 proposes that the RP-1 and RP-10 ratification at CP-0 is what admits `bco:BusinessCapability`, rather than a separate architectural admission record. A separate record would work equally well. The rule that admission never passes down is the same either way.
- **Incomplete evaluations get no representation in v0.5.** They are kept out of the graph, and OI-23 asks whether to represent them. This avoids minting anything, but it means a graph cannot show that an evaluation is under way.
- **Criteria identifiers use `dct:identifier`.** Draft.1 required "an identifier" without naming the property. Draft.2 names `dct:identifier`, which is from Dublin Core, a vocabulary already in use, not a BCO term.

## Traceability summary

| R10 item | CM-01 | Decisions | Requirements | Competency questions | Open issues |
| --- | --- | --- | --- | --- | --- |
| 01 Grounding witness | P1; Business Capability, Capability Basis, Member Agent; RL-03, RL-04, RL-05, RL-23; the DP-1 table | DP-1 a1, a2; DP-2 (G1-I) | CAP-35 (new), CAP-25, CAP-26 | CQ-1 | OI-8 |
| 02 Performance witness | P2; RL-14 | DP-2 b5 (question 3) | CAP-34, CAP-21 | CQ-3 | OI-8 |
| 03 Assessment evidence and criteria | P3, P5; Capability Assessment, Presence Finding, Assessment Criteria, Evidence, Functional Adequacy Assessment; RL-19, RL-20, RL-21; CM-01 approval guidance | R9 (accepted) | CAP-27, CAP-33, CAP-26 | CQ-6, CQ-13 | OI-23 (new) |
| 04 Parent admission | Capability Type, Type Admission Record; RL-09 | DP-1, DP-2 (RP-1, RP-10) | CAP-04, CAP-32 | CQ-10 | OI-7 |
