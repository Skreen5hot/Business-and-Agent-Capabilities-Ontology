# Ontology Development Standard
## Stage 06 — Knowledge Graph (proposed)

| Field | Value |
|---|---|
| Status | **Proposed**, for the architect's approval, as the decision of 2026-11-16 directs (`docs/decisions/2026-11-16-stage05-completion-accepted.md`, 6). Not in force. It authorizes no production data. Once approved, it moves to `docs/standards/stage-06-knowledge-graph.md`, as the Stage 05 standard did. The first increment under it is proposed separately (`docs/proposals/2026-11-16-stage06-first-increment-proposal.md`) |
| Date | 2026-11-16 |
| Drafted by | Claude Code (`claude-opus-5-5`), for the BCO team |
| Applies to | Everything under `src/06_knowledge_graph/`: the production coverage register, the CP-3 scope audit, the `bc:` migration manifest, and production evidence graphs with their completeness manifests and G1-I records |
| Rests on | Specification v0.5.0-draft.3 (§2's artifacts, CD14 to CD17, §8's G1-I and gates, §9, §10's CP-3, OI-11, OI-13, OI-21), the Stage 05 standard and its accepted tranches, ADR-003 D1 and RP-5 (namespaces), the rights posture (`docs/sources/inventory/rights.yaml`, O-2), roadmap D7 and §10 |

## 1. Purpose

Stage 06 records what is true of particular things, and what is known about the coverage of
standing functions, using the classes Stage 05 wrote. It writes data, not terms. It mints no
class or property, and it does not reopen a Stage 05 tranche or a G1-T record.

Its data has three kinds, each with its own gate:

| Kind | What it is | Settled by |
|---|---|---|
| **Register data** | The coverage register (CD16), the CP-3 scope audit, the `bc:` migration manifest (§9.1) | The architect's approval of each entry, checked by schema and SHACL |
| **Evidence data** | Named evidence graphs about one organization: its members, assessments, ratings, sourcing statements, Authorization Records, targets and plans | G1-I per bearing claim (Gate F), Gate M per graph, the instance and description shapes |
| **Derived answers** | CQ results over register and evidence data | The approved method of each CQ; never written back as triples (CAP-29) |

## 2. What an increment needs before any data is written

Stage 06 proceeds in increments. Each needs the architect's approval of an increment record
naming:

1. **its scope**: which register entries, or which organization, period, agents and act
   classes;
2. **its sources**: each with its rights status, and for evidence data, the consent and
   privacy basis for any person it names;
3. **its namespace**: the authored namespace any new individual is minted in (§3, K1);
4. **its reviewers**: for evidence data, the named assessor and the Gate F reviewer;
5. **the open issues that limit it** (OI-11, OI-13, OI-21 and others), with the limit each
   places on the answers.

An increment with an open rights, consent or namespace question writes nothing.

## 3. Authoring rules

**K1 — IRIs.** No IRI is minted outside ADR-003 D1's five namespaces, as RP-5 made them
permanent. Register data and the migration manifest need no new IRI: their keys are BPO
catalog nodes (`ex:PCF_<id>`), written BCO classes, and the v0.1 IRIs. Individuals and
evidence-graph IRIs (OI-11) need a namespace that none of the five is for. Choosing one
changes `AUTHORED_NAMESPACES` and every shape filter in one commit, under its own decision,
before the first evidence increment.

**K2 — Production and fixture data never mix.** A production file never names a
`fixture_` IRI, and a fixture never sits in a production path. A fixture result is never
reported as a production result, and the reverse.

**K3 — Nothing is inferred into the data.** CQ answers, register joins and reasoner
classifications are not written back. In particular, a whole-function bearing claim is
never derived from components (CD16), and no subclass link comes from a register entry
(CAP-29).

**K4 — Every bearing claim has its G1-I record.** `cco:ont00001954` from an organization to
a capability instance is asserted only with a supporting Capability Assessment (CAP-26).
Its answers to G1-I questions 1 to 5 are recorded, and signed PASS or FAIL by the named Gate
F reviewer. Where questions 1 or 2 cannot be settled, no finding is recorded (CD14).

**K5 — Evidence is dated, sourced and thresholded.** Every finding has its criteria
(`dct:conformsTo`), its evidence (`dct:source`) and its date (`dct:date`). It never rests
only on what G1-I question 2 excludes: organization charts, charters, responsibility
assignments or Authorization Records.

**K6 — Absence is bounded.** Every evidence graph has a completeness manifest that passes
Gate M, or it is answered as having none (*unknown*). A graph that holds a revoked or
superseded Authorization Record may not be declared complete (OI-21).

**K7 — Persons.** A person named as a basis member is personal data. It is named in a
committed file only where the increment record states the consent or other basis for it.
Otherwise the evidence graph stays outside the public repository, and only its manifest,
digest and G1-I record enter.

**K8 — The register.** Each entry is keyed by one standing function's catalog node, verified
at the BPO pin, and lists component capability classes. Each component is a written K1
class. The whole-function class, if one is defined, is never one of its own components
(CAP-22). Only the node's IRI enters, never its text; committing PCF identifiers follows the
rights posture (O-2) and `tools/licensing/pcf_notice.py`.

**K9 — Change control.** Register, audit and manifest entries are versioned. A change of
an approved entry is a new reviewed version. A finding is superseded only by a later
assessment, never edited (OI-24 bounds the answer meanwhile).

## 4. Validation architecture

Stage 05's ladder, reasoners and Gate M run unchanged. Stage 06 adds the checks below. **As
in Stage 05, a new check arrives with its negative fixture and positive controls in the same
commit.**

| Id | Check | Gate | When it runs | Fails on |
|---|---|---|---|---|
| S06-R1 | The coverage register matches its JSON Schema | M-like (JSON Schema) | every commit | an unknown field; a missing version; a malformed IRI |
| S06-R2 | CAP-22 over the production register: each key is a catalog node at the pin; each component is a written K1 class; no whole-function class among its own components | Gate B, pytest | every commit | an unresolved key or component; a component that is not written; a self-listing |
| S06-R3 | Gate G: running CQ-9 and CQ-12 over the register adds no triple to any graph | pytest | every commit | a generated triple |
| S06-A1 | The CP-3 audit has exactly one disposition per scope entry at the pin | pytest | every commit | a missing or extra entry; a disposition outside the closed list; a G1-T citation that does not resolve |
| S06-MG | The `bc:` migration manifest has one row per v0.1 class, read from the checksummed draft; no row asserts `owl:equivalentClass` | pytest | every commit | a missing class; a new IRI not written in a module; an equivalence |
| S06-E1 | Each production evidence graph passes the instance and description shapes, Gate C-A, and its Gate M manifest | SHACL, M | every commit with evidence data | any violation |
| S06-E2 | Each bearing claim in a production graph cites a signed G1-I record that names its basis members (CAP-35) | pytest, Gate F | every commit with evidence data | a claim with no record; a record not signed; a basis the record does not name |
| S06-E3 | K2 and K7: no fixture IRI in a production path, no production file under `tests/`, and no person named without the increment's stated basis | pytest | every commit | either mixing; an undeclared person |
| S06-U1 | The upstream refetch job (`vendor_upstream.py --rebuild`) has run green at the commit cited | CI | each repin, and before any release or conformance claim | a digest mismatch; the job skipped |
| S06-U2 | HermiT consistency over the complete pinned BFO and CCO, the BCO modules, and the production data | reasoner | before Stage 06 completion and any release | inconsistency; an absent reasoner (FAIL) |

Gate F stays human. For evidence data it judges whether the cited evidence establishes the
finding against its threshold (CAP-26, CAP-27, CAP-33, CAP-35). A machine check never
stands in for it.

**Upstream conformance.** S06-U2 extends conformance from partial extracts to the complete
BFO and CCO at their pins. BPO stays limited to the import boundary (Stage 05 §4), because
the excluded modules assert what RP-3 forbids. Full BPO conformance therefore is not
claimed. The act labels wait on BPO's re-pin (N-2), and the Q-12 concepts on BPO's answer
(N-5).

## 5. Review

| Role | What it reviews |
|---|---|
| Ontologist (drafting) | Increment records, register entries, the audit, the migration manifest; G1-I records drafted from evidence |
| Assessor (named per increment) | Answers G1-I questions 1 to 5 from the evidence |
| Gate F reviewer (named per increment; may be the Proxy Domain Expert) | Signs each G1-I record PASS or FAIL |
| Proxy Domain Expert (the architect) | Approves each increment record and each register entry; decides rights, consent and namespace questions |

## 6. Stage completion

Stage 06 is complete when:

- CP-3 is met (specification §10): every scope entry is audited, the coverage register is
  populated for the approved scope, and the `bc:` migration manifest is complete;
- every production evidence graph written passes S06-E1 to S06-E3, with a signed G1-I record
  per bearing claim;
- S06-U1 and S06-U2 have run at the completion commit;
- a stage-completion record in roadmap §10's form is accepted.

Whether D7 also requires at least one production evidence graph is the architect's call (K-6
in the first increment's proposal).

## 7. Boundary

This standard:

- mints no class or property, and reopens no G1-T record or Stage 05 tranche;
- authorizes no release, which is D8's under its own standard;
- does not move BPO data into the BCO, or change BPO (`capabilities/agents.json` and
  `ex:BusinessAuthorization` are BPO's decisions under §9);
- does not represent revocation, supersession of assessments, or multi-party sourcing
  (OI-21, OI-24, OI-18): answers state those limits.
