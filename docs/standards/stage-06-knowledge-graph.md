# Ontology Development Standard
## Stage 06 — Knowledge Graph

| Field | Value |
|---|---|
| Status | **Approved** on 2026-11-16 with the architect's binding directions A to J (`docs/decisions/2026-11-16-stage06-standard-and-first-increment.md`), ratified as the text of the PR that integrated it. The approved text is `docs/proposals/2026-11-16-stage-06-knowledge-graph-standard.md`, which this file matches except for the title's "(proposed)" and this status row. It authorizes the register-first increment, not any evidence increment. A substantive change is a new, reviewed version |
| Date | 2026-11-16 |
| Drafted by | Claude Code (`claude-opus-5-5`), for the BCO team |
| Applies to | Everything under `src/06_knowledge_graph/`: the production coverage register, the CP-3 scope audit, the `bc:` migration manifest, and production evidence graphs with their completeness manifests and G1-I records |
| Rests on | Specification v0.5.0-draft.3 (§2's artifacts, CD14 to CD17, §8's G1-I and gates, §9, §10's CP-3, OI-11, OI-13, OI-21); the Stage 05 standard and its accepted tranches; ADR-003 D1 and RP-5 (namespaces); the rights posture (`docs/sources/inventory/rights.yaml`, O-2); roadmap D7 and §10 |

## 1. Purpose

Stage 06 records what is true of particular things, and what is known about the coverage of
standing functions, using the classes Stage 05 wrote. It writes data, not terms. It mints no
class or property, and it does not reopen a Stage 05 tranche or a G1-T record.

Its data has three kinds, each with its own gate:

| Kind | What it is | Settled by |
|---|---|---|
| **Register and migration data** | The coverage register (CD16), the CP-3 scope audit, the `bc:` migration manifest (§9.1) | The architect's acceptance of each batch after a synthetic domain review (§5), checked by schema and tests |
| **Organization-specific evidence** | Named evidence graphs about one organization: its members, assessments, ratings, sourcing statements, Authorization Records, targets and plans | G1-I per possession claim (Gate F), Gate M per graph, the instance and description shapes |
| **Derived query answers** | CQ results over register and evidence data | The approved method of each CQ. Never written back as source assertions (CAP-29) |

## 2. What an increment needs before any data is written

Stage 06 proceeds in increments, and the architect approves each one's scope. An evidence
increment's record names:

1. **its scope**: the organization, the period, the agents and the act classes;
2. **its sources**: each with its rights to use and disclose it;
3. **its persons**: the consent or privacy safeguards for anyone it names;
4. **its instance namespace**: approved as K1 requires;
5. **its assessor and its Gate F reviewer**, both named;
6. **the open issues that limit it** (OI-11, OI-21 and others), with the limit each places
   on the answers.

An increment with an open rights, consent or namespace question writes nothing. None of
these is invented, and confidential information never enters the public repository by
default.

## 3. Authoring rules

**K1 — Three kinds of IRI.**

| Kind | What | Rule |
|---|---|---|
| Ontology-term IRIs | Classes, properties and vocabulary concepts in ADR-003 D1's five namespaces | Minted only by Stage 05 or `tools/vocab/build.py`. Never used for an organization, a person or any other individual |
| Externally reused IRIs | BFO, CCO and BPO terms, BPO catalog nodes, the v0.1 `bc:` IRIs | Referenced, never redeclared. Each is verified at its pin |
| Instance-data IRIs | Real organizations, members, assessments, evidence graphs (OI-11) | Need a separate instance-data namespace, decided with the first evidence increment, when its organization and publication rights are known. Until then none is minted |

Register and migration data use only identifiers whose creation or reuse is already
authorized. If a register needs a new identifier, the need is escalated before anything is
minted.

**K2 — Test and production stay apart.** A production file never names a `fixture_` IRI,
and a fixture never sits in a production path. A fixture result is never reported as a
production result, and the reverse. A fictional organization or a synthetic fixture is never
production evidence.

**K3 — Nothing is derived into the data.** CQ answers, register joins and reasoner
classifications are not written back as source assertions. A whole-function claim is never
derived from components (CD16). A register entry produces no subclass link (CAP-29).

**K4 — Possession needs a signed G1-I assessment.** G1-T admission says a type is a
Business Capability type. It says nothing about whether an organization bears one.
`cco:ont00001954` from an organization to a capability is asserted only with a supporting
Capability Assessment (CAP-26). That assessment's G1-I record answers questions 1 to 5 and
is signed PASS or FAIL by the named Gate F reviewer. Where question 1 or 2 cannot be
settled, no finding is recorded (CD14). A negative or partial finding is recorded only when
the evidence supports it, and a PASS is never made to fit a deadline.

**K5 — Every assessment keeps its record.** Each assessment keeps:

- its criteria (`dct:conformsTo`);
- its source evidence (`dct:source`);
- its date (`dct:date`);
- its reviewer;
- its finding.

A finding never rests only on what G1-I question 2 excludes: organization charts, charters,
responsibility assignments or Authorization Records. Missing data is never read as an
adverse finding: no record means no finding, not `absent`.

**K6 — Absence is bounded.** Every evidence graph has a completeness manifest that passes
Gate M, or absence questions over it are answered *unknown*. A graph that holds a revoked or
superseded Authorization Record may not be declared complete (OI-21).

**K7 — Persons.** A person named as a basis member is personal data. A committed file names
one only where the increment record states the consent or other basis for it. Otherwise the
evidence graph stays outside the public repository; only its manifest, digest and G1-I
record enter.

**K8 — The register (OI-13, decided for version 1).**

- **Keys.** Each entry is keyed by one standing function's identifier, whose reuse is
  verified at its pin.
- **Components.** The component field holds only capability types, as approved class IRIs
  written in a Stage 05 module. It never holds:
  - a capability individual;
  - a functional unit;
  - an act type;
  - an APQC process node.
- **Whole-function class.** If one is defined, it is never one of its own components
  (CAP-22).
- **What an entry implies.** A component list does not imply that any organization
  possesses those capabilities. Possession does not establish integration, availability or
  whole-function adequacy.
- **Extending the model.** Any extension of the component model needs its own semantic
  justification.
- **APQC material** follows the conservative rights rule:
  - No APQC name, definition, hierarchy description or reconstructed catalog content is
    published because its identifier is available.
  - The rights basis of each identifier and relationship is verified before it is
    distributed. Material whose public redistribution is not established is kept private
    or withheld.
  - An attribution notice is not permission.

**K9 — Change control.** Register, audit and manifest entries are versioned. A change to an
accepted entry goes in a new reviewed batch. A finding is superseded only by a later
assessment, never edited (OI-24 bounds the answer meanwhile).

**K10 — The audit and the migration decide nothing.**

- **The scope audit** records, for each entry, what BPO declares and, separately, what the
  BCO has independently accepted. It never admits a BPO type, changes its classification
  or creates a subclass assertion.
- **The migration manifest** records identifier migration separately from semantic
  equivalence. It never creates an `owl:sameAs`, an `owl:equivalentClass` or a replacement
  IRI without justified and separately approved semantics.

## 4. Validation architecture

Stage 05's ladder, reasoners and Gate M run unchanged. Stage 06 adds the checks below. **As
in Stage 05, each new check arrives in the same commit as its negative fixture and its
positive controls.**

| Id | Check | Gate | When it runs | Fails on |
|---|---|---|---|---|
| S06-R1 | The coverage register matches its JSON Schema | JSON Schema | every commit | an unknown field; a missing version; a malformed IRI |
| S06-R2 | CAP-22 and K8 over the production register: each key is verified at its pin; each component is a written K1 class; no whole-function class among its own components; no component of another kind | Gate B, pytest | every commit | an unresolved key or component; an act, node or individual as a component; a self-listing |
| S06-R3 | Gate G: running CQ-9 and CQ-12 over the register adds no triple to any graph | pytest | every commit | a generated triple |
| S06-A1 | The CP-3 audit has exactly one row per scope entry at the pin. BPO's declaration and the BCO's acceptance are separate fields, and every BCO acceptance cites its record | pytest | every commit | a missing or extra entry; a disposition outside the closed list; a citation that does not resolve; an acceptance with no record |
| S06-MG | The `bc:` migration manifest has one row per v0.1 class, read from the checksummed draft. Every row states its semantic relation separately from its identifier migration. No row asserts `owl:sameAs` or `owl:equivalentClass` | pytest | every commit | a missing class; a new IRI not written in a module; an equivalence |
| S06-E1 | Each production evidence graph passes the instance and description shapes, Gate C-A and its Gate M manifest | SHACL, M | every commit with evidence data | any violation |
| S06-E2 | Each possession claim in a production graph cites a signed G1-I record that names its basis members (CAP-35) and keeps K5's fields | pytest, Gate F | every commit with evidence data | a claim with no record; a record not signed; a basis the record does not name |
| S06-E3 | K2 and K7: no fixture IRI in a production path, no production file under `tests/`, no person named without the increment's stated basis | pytest | every commit | either mixing; an undeclared person |
| S06-U1 | The upstream refetch (`vendor_upstream.py --rebuild`) runs in an auditable CI workflow, verifying each pinned file's digest | CI | each repin; a Stage 06 PR that changes the upstream config; before any release or conformance claim | a digest mismatch; the job skipped |
| S06-U2 | HermiT consistency over the BCO modules with the complete pinned BFO and CCO. Records the closure actually loaded (each file and its digest) and the result | reasoner | before CP-3 closes, before Stage 06 completes, before any release | inconsistency; an absent reasoner (FAIL) |

Gate F stays human. For evidence data, it judges whether the cited evidence establishes the
finding against its threshold (CAP-26, CAP-27, CAP-33, CAP-35). A machine check never stands
in for it.

**Upstream conformance, stated precisely.** S06-U2 extends conformance from the partial
extracts to the complete BFO and CCO at their pins. BPO stays limited to the import
boundary (Stage 05 §4), because the excluded modules carry capability assertions
incompatible with it (RP-3). **Full BPO conformance is not claimed.** That limit is reported
explicitly: the boundary is not weakened, and a failing check is never disabled. Two more
limits stay open:

- the act labels wait on BPO's re-pin (N-2);
- the Q-12 concepts wait on BPO's answer (N-5).

## 5. Review

| Role | What it reviews |
|---|---|
| Ontologist (drafting) | Increment records; register batches, the audit and the migration manifest; G1-I records drafted from evidence |
| Synthetic domain reviewer (separate, per register batch, under the accepted process) | The batch's component relationships, source evidence and function identifiers. It reports semantic disputes |
| Assessor (named per evidence increment) | Answers G1-I questions 1 to 5 from the evidence |
| Gate F reviewer (named per evidence increment) | Signs each G1-I record PASS or FAIL |
| Proxy Domain Expert (the architect) | Approves each increment's scope. Accepts each register batch as a whole, with any substantive semantic dispute submitted with it. Decides rights, consent and namespace questions |

## 6. Stage completion

**CP-3 closes** when all of these hold:

- every scope entry is audited (S06-A1);
- the coverage register is populated for the accepted scope, in accepted batches;
- the `bc:` migration manifest is complete (S06-MG);
- S06-U1 and S06-U2 have run at the closing commit.

CP-3 is necessary but not sufficient.

**Stage 06 completes** only when, in addition, there is at least one real organization
evidence graph with all of these:

1. an identified organization and an approved instance namespace;
2. evidence whose use and disclosure are authorized;
3. any required consent or privacy safeguards;
4. a named assessor and reviewer;
5. at least one signed G1-I decision, supported by dated, sourced evidence;
6. the applicable validation (S06-E1 to S06-E3) and competency queries run successfully;

and a stage-completion record in roadmap §10's form has been accepted.

A negative or partial finding counts if the evidence genuinely supports it. If no suitable
evidence can lawfully be obtained, Stage 06 stays partially complete. A fictional
organization or a synthetic fixture never substitutes for production evidence.

## 7. Boundary

This standard:

- mints no class or property, and reopens no G1-T record or Stage 05 tranche;
- authorizes no release, which is D8's under its own standard;
- does not move BPO data into the BCO, or change BPO (`capabilities/agents.json` and
  `ex:BusinessAuthorization` are BPO's decisions under §9);
- does not represent revocation, supersession of assessments, or multi-party sourcing
  (OI-21, OI-24, OI-18), and every answer states those limits;
- authorizes no evidence increment: each needs its own approved scope.
