# BCO roadmap

**Status: proposed, for the architect's approval.** The architect directed on 2026-10-30
that the BCO follow the plan recommended after the Ontology Template exchange, starting
with this roadmap (`docs/decisions/2026-10-30-template-not-adopted-roadmap-directed.md`).
This document renders that plan as steps, each with its entry gate, its standard and its
exit. **It orders work; it authorizes none.** A step starts when the architect authorizes
it, and every gate below that is new is proposed until this roadmap is approved.

It replaces HANDOFF §7, which dated from the repository's setup.

## Principles carried from the template exchange

The BCO does not adopt the Ontology Template. These principles, from the exchange
(`communications/example/`), shape the steps below:

1. **One decision path, with terminology lanes beside it.** Decisions are taken in order:
   scope and competency questions, sources, conceptual model, specification ratification,
   formalization, instances. The controlled vocabulary, inventory, taxonomy and thesaurus
   run alongside, join the path at named gates, and never write an OWL axiom.
2. **A standard before a stage.** No stage starts without its standard.
3. **Evidence is not vocabulary is not admission.** Type admission (G1-T) is not instance
   attribution (G1-I). Conceptual approval is not specification ratification is not OWL.
4. **A review counts for the gate its kind meets.** Every review record states the
   capacity the reviewer acted in.
5. **A decision names the documents it changes**, and each of them carries it.
6. **A closure gate before each new phase**: every open decision closed, or carried
   forward by name.

## Where things stand (2026-10-30)

| Stage or item | State |
|---|---|
| Specification | v0.4.0-draft.1; predates CM-01; nothing ratified; CP-0 not met |
| Stage 01, controlled vocabulary | 14 concepts (9 metamodel, 5 catalog), all Draft; no Stage 01 standard (ADR-003 stands in) |
| Stage 02, conceptual models | CM-01 approved 2026-10-26 (stakeholder-review erratum of 2026-10-30); CM-02 planned, not started |
| Capability Term Inventory (Stage 01 source evidence) | I-1, I-2a, I-2b, I-2c and E7 done; closure set complete; E4 method decided, nothing judged; I-3 to I-5 not authorized |
| Stage 03, taxonomy | not started; no standard |
| Stage 04, thesaurus | not started; no standard |
| Stage 05, ontology | specified, not written; no standard beyond the specification's gates |
| Stage 06, knowledge graph | not started; no standard |

## The decision path

Each step's exit is the next step's entry gate.

| Step | What | Entry gate | Standard | Exit |
|---|---|---|---|---|
| **D1** | This roadmap | the architect's direction of 2026-10-30 | — | the architect approves it |
| **D2** | **CM-02 scope and boundary**: Agent Capability's scope, and its boundary with CM-01, whose capability basis is the organization's member agents. Scope only; the full model comes later | D1 | Stage 02 standard | the architect approves the scope note |
| **D3** | **Specification v0.5** (below) | D2 | the specification's own review process | a review round answered; the architect accepts v0.5 as the draft to ratify |
| **D4** | **CP-0**: RP-1 to RP-10 ratified, ADR-002 accepted, the permanent namespace minted (RP-5) | D3 | spec §10 | the architect's ratification acts, recorded |
| **D5** | **Stage 05 standard**, and a domain-practitioner review of CM-01 and of CM-02 as far as it then stands | D4 | — (writing it is the step) | the architect approves the standard; the practitioner review is recorded with its capacity |
| **D6** | **Stage 05, formalization**: G1-T per class, alignment, axioms, shapes, reasoners; CP-1 and CP-2. Before the first realization index, decide whether BPO's process slices are vendored (CD4, RP-2) | D5 | Stage 05 standard; spec gates A–D, C-A, M, D2, F | CP-2 met, and the conceptual-fidelity check passes |
| **D7** | **Stage 06, knowledge graph**: G1-I attributions on recorded assessments; the coverage register; the `bc:` migration; CP-3 | D6 | a Stage 06 standard, approved first | CP-3 met |
| **D8** | **Release and maintenance**: versioned release, deprecation policy, consumer impact (OI-10), upstream re-pins | D7 | a release standard, approved first | first release |

### What specification v0.5 does (D3)

1. **Carries the decisions forward**, with a table naming each decision and the sections it
   changes:
   - DP-1 (RP-1) into CD1 and CD2;
   - DP-2 (RP-10) into CD3 and §8;
   - the R9 corrections (Functional Adequacy Assessment, conditional standing-function
     designation, the artifact scope) into CD16 and CD17;
   - the CM-01 stakeholder-review erratum;
   - CM-02's approved scope (D2);
   - CM-01's open questions on BPO's act index (Q-12 to Q-14).
2. **Cites its sources by register id, at V or P or explicitly excused.** v0.4 cites no
   register entry by id. 26 of the register's 63 entries have no claim at V or P; any of
   them v0.5 relies on is verified or excused by name.
3. **Raises the known formalization risks as decision points**, each with options, for the
   architect:
   - formalizing DP-1's basis with BFO's `has material basis` entails Disposition, a
     commitment CM-01 does not make;
   - conditional standing-function designation cannot be an OWL class (a SHACL rule, or an
     information entity);
   - competency questions about a capability never exercised need a closed-world check.
4. Corrects the `ex:` prefix to BPO's genera only (CLAUDE.md, R3 of the 2026-10-28
   re-pin).

## The terminology lane

These run beside the decision path. None writes an OWL axiom.

| Step | What | Entry gate | Joins the path at |
|---|---|---|---|
| **T1** | **Stage 01 standard** | D1 | before any vocabulary concept is ratified |
| **T2** | **Re-check the five catalog concepts** against G1-T (DP-2) and the R6 rewrite | T1 | before any catalog concept is ratified |
| **T3** | **Vocabulary ratification acts** (ADR-003's act) | T1, T2, D4 | metamodel concepts follow the ratified specification terms |
| **T4** | **Homonym register**, seeded from the inventory's findings (ISO/IEC 33020 and CMMI "capability"; FIBF "business capability", flag E5) as source evidence | authorization | Stage 04 takes it up under its standard (T8) |
| **T5** | **Inventory I-3** (restricted catalogs, citation and coverage only) and **I-4** (crosswalk, deduplication, triage) | each authorized separately; a rights review recorded for every new source before any harvest | — |
| **T6** | **E4 judgments** of standing-function candidates | D3 (v0.5 decides how designation is represented) | D6 |
| **T7** | **Inventory I-5**, a first-tranche recommendation | D4 (it applies the ratified admission test) and I-4 | the architect's separate approval; then D6 |
| **T8** | **Stage 03 taxonomy** and **Stage 04 thesaurus** | each stage's standard, approved first; I-4 for the taxonomy | admissions consume G1-T; term relations never become ontological relations by themselves (Stage 02 standard §8.1) |

## Gates every step keeps

| Gate | Where it applies |
|---|---|
| **Standard supplied** | the start of every stage |
| **Rights and provenance** | before any harvest of a new source; withholding by default until reviewed; use is Legal's decision, recorded |
| **Source adequacy** | every source a decision or the specification relies on is at V or P, or excused by name |
| **Domain-practitioner review** | CM-02 approval; any substantive CM-01 change; before Stage 05 (D5). For BCO: a business architect or capability-planning lead, or a FIBF standards-lead-agency analyst |
| **Conceptual fidelity** | Stage 05: each authored term and each axiom cites the CM-01 or CM-02 element, or the decision, it formalizes |
| **Decision propagation** | every decision record names the documents it changes |
| **Closure** | before each new phase |

## What is kept as it is

Decisions recorded verbatim with digests; errata as new records; one reviewed pull request
per phase; communications under `communications/README.md`.
