# Proposal — CM-02, C-1: one activity kind, many bearers

| Field | Value |
|---|---|
| Status | **Decided 2026-11-18: the C-1 baseline.** Option A, interpretation (b) with evidence requirements, and the information-artifact distinction are adopted (`docs/decisions/2026-11-18-cm02-c1-decided.md`). Revision 2 applies the decision's three corrections and its list of limitations |
| Date | 2026-11-18 |
| Revision | 1, proposed at `78d4c6e`. 2, the architect's decision applied: sections 2, 5, 6, 8 and 9 |
| Prepared by | Claude Code (`claude-opus-5-5`), for the BCO team |
| Arises from | The architect's direction of 2026-11-18 (`docs/decisions/2026-11-18-cm02-started-c1-first.md`) |
| Governed by | The Stage 02 standard (`docs/standards/stage-02-conceptual-modeling.md`); the approved CM-02 scope note (`docs/proposals/2026-10-31-cm02-scope-note.md`), C-1 |
| Constrained by | CCO's definitions and axioms are used as they are. No class, object property, IRI or OWL axiom is proposed. No source is ingested. CM-01, DP-1 and DP-2 are not reopened |

This note asks one question: how can a single kind of activity, mail sorting, be
something a person, an organization and a machine can each do, when CCO classifies those
abilities by who or what bears them? It proposes an answer to C-1, the conditions for
attributing an Agent Capability, as CM-02's first settled issue.

## 1. What CCO and BFO say, exactly

These definitions and axioms were read from the pinned complete sources: CCO v2.0, merged,
at commit `510dad7` (SHA-256 `e609db27…`), and BFO 2020 core (SHA-256 `6944e2c9…`).
Both digests were checked against `config/upstream-sources.yaml`. The axioms are given in
Manchester-style notation.

| Term | Definition (verbatim) | Logical axioms |
|---|---|---|
| Agent Capability `cco:ont00001379` | "A Realizable Entity that inheres in a Material Entity in virtue of that Material Entity's capacity to realize it in some Planned Act." | `SubClassOf obo:BFO_0000017` (realizable entity). No other axiom, and no disjointness |
| Skill `cco:ont00000089` | "An Agent Capability that inheres in a Person to the extent of that Person's capacity to realize it in Intentional Acts of a certain type." | `EquivalentTo: Agent Capability and (capability of some Person)`; `SubClassOf Agent Capability` |
| Organization Capability `cco:ont00000568` | "An Agent Capability that inheres in an Organization to the extent of that Organization's capacity to realize it in Intentional Acts of a certain type." | `EquivalentTo: Agent Capability and (capability of some Organization)`; `SubClassOf Agent Capability` |
| Agent `cco:ont00001017` | "A Material Entity that bears an Agent Capability." | `EquivalentTo: material entity and (bearer of some Agent Capability)` |
| Person `cco:ont00001262` | "An Animal that is a member of the species Homo sapiens." | `SubClassOf Animal`; alternative label "Human" |

The terms they depend on:

- **capability of** (`cco:ont00001889`). A subproperty of BFO's *inheres in*, with domain
  Agent Capability and range Agent. Its inverse is **has capability** (`cco:ont00001954`).
- **Planned Act** (`cco:ont00000228`, alternative label Intentional Act). "An Act in which
  at least one Agent plays a causative role and which is prescribed by some Directive
  Information Content Entity held by at least one of the Agents." Its only axiom is
  `SubClassOf Act`.
- **Act** (`cco:ont00000005`). "A Process in which at least one Agent plays a causative
  role." Its only axiom is `SubClassOf process`.
- **Artifact Function** (`cco:ont00000323`). "A Function that inheres in some Artifact in
  virtue of that Artifact being designed to be used in processes that require that
  Function to be realized." Its axioms are `SubClassOf function` and
  `SubClassOf inheres in some Material Artifact`.
- **function** (`obo:BFO_0000034`). A disposition that exists because of its bearer's
  physical make-up, which came about through evolution or intentional design "in order to
  realize processes of a certain sort". It is `SubClassOf disposition`.
- **realizable entity** (`obo:BFO_0000017`). It inheres in an independent continuant and
  is "of a type some instances of which are realized in processes of a correlated type".
- **Information Content Entity** (`cco:ont00000958`). A generically dependent continuant
  that is about something.
- **Directive ICE** (`cco:ont00000965`). An ICE that prescribes some entity.
- **aggregate has capability** (`cco:ont00001898`). Relates a Group of Agents to an Agent
  Capability it bears member by member.

Four consequences follow from the axioms themselves, not from their labels:

1. **The axioms classify by bearer alone.** Skill and Organization Capability are defined
   by an existential restriction on the bearer. "Intentional Acts of a certain type"
   appears only in the text. No axiom ties any capability to the kind of act it is
   realized in.
2. **Asserting an Agent Capability makes the bearer an Agent.** Agent is *equivalent to*
   material entity that bears an Agent Capability. Say that a machine bears one, and a
   reasoner infers that the machine is an Agent. The range of *capability of* infers the
   same.
3. **Any Agent Capability borne by a person is a Skill.** It follows from the equivalence
   axiom, whatever the ability is and however it was acquired.
4. **Agent Capability and function are not disjoint.** Function sits under disposition,
   and Agent Capability sits directly under realizable entity. Nothing forbids one entity
   from being both.

## 2. Two questions, not one

The architect's point holds: *what kind of activity* and *what kind of bearer* are
separate questions. They are answered from different places.

| Question | What answers it | Where it lives |
|---|---|---|
| **A. What does the ability do?** (its activity kind) | The type of process it is realized in: mail sorting | BFO: every realizable entity has a "correlated" process type. BCO already records this type-level link as the Realization Index (CM-01 P2), for business capabilities as annotations listing BPO act types |
| **B. What sort of ability is it?** (its bearer-specific classification) | What bears it, and in virtue of what | CCO: Skill (a person), Organization Capability (an organization), Agent Capability (any agent), Artifact Function (a designed artifact) |

A mail-sorting ability is therefore a pair: one shared answer to A, and a different answer
to B for each bearer. The activity kind is never redefined per bearer. Only the
classification of the individual capacity changes.

The shared answer to A is not automatically a BPO act type. BFO's Process
(`obo:BFO_0000015`) is the bearer-neutral class every activity kind falls under. CCO's Act,
and Planned Act within it, are narrower: an Act needs an Agent playing a causative role,
and a Planned Act also needs a directive.

- **Where an organization deploys a machine,** the sorting is the organization's act, and
  BPO's act type covers it (case 4 below).
- **A sorting process with no agent in it** is a process, not an act. Not every
  machine-executed process is a BPO Planned Act.

What is missing is narrower: a verified, specific mail-sorting process type usable across
human and artificial implementations (section 5, gap G2).

Sharing an activity kind does not make two capacities the same capacity. Nor does it give
them the same realization conditions. Joe, the post office and a machine sort mail under
different conditions, and each capacity is classified and evidenced on its own.

## 3. The worked example: mail sorting

*Act of mail sorting* below stands for whatever act type the index would name. It is
illustrative. This note does not assert that BPO or CCO declares such a type.

| # | Entity | Its individual capacity is classified as | Justified when | Not justified by |
|---|---|---|---|---|
| 1 | **Joe**, a person | **Skill.** The equivalence axiom makes it one as soon as it is an Agent Capability that is *capability of* Joe | Joe can sort mail as his own planned act, under a sorting scheme he follows (a Directive ICE he holds). Evidence: observed performance, training or test records | Joe's job title or position. That is role and permission, CM-01's "permitted / responsible", not ability |
| 2 | **The post office**, an organization | **Organization Capability**, and a Business Capability if the type is admitted under G1-T and attributed under G1-I | The organization can sort mail through its members *as organized*, its arrangements included (DP-1). Joe's skill is evidence for this (G1-I question 2), never the capability itself | The sum of its staff's skills. Several staff each able to sort is member-wise (case 3) |
| 3 | **A sorting team** with no organization rules | **No capability of its own.** Each member's Skill, attributed to the group with *aggregate has capability* | The members each bear the skill. Whether such a team can bear a capability of its own is C-2, still open | Treating the attribution as an Organization Capability (CD10) |
| 4 | **A deployed sorting machine** with a machine-learning address reader, run in the post office's process | **Artifact Function** of the material system (the hardware running the model), not an Agent Capability. The organization's act realizes the organization's capability, and the machine is an enabling condition of it (DP-1) | The system was designed to sort mail, and its make-up grounds the ability: the trained model, concretized in its memory, is part of that make-up. Here the organization is the agent, and the machine is used (CCO *uses*) | Its behaviour looking autonomous. Apparent autonomy alone does not establish agency (scope note §1) |
| 5 | **An autonomous sorting system** that takes, interprets and carries out sorting work with no operator in the act | **Artifact Function by default. Agent Capability only if a review finds the C-1 evidence criteria met (section 8, R2).** If they are met, CCO then *infers* that the system is an Agent | All four R2 criteria are established for the deployed system in its actual configuration, by design, configuration, deployment or operational evidence. No prior successful exercise is required | Being classified as a **Skill**: that would need the system to be a Person. Asserting it, as with any other conclusion here, without the recorded test |
| 6 | **An AI skill package** (for example a `SKILL.md` with code), an **A2A Agent Card** entry "mail-sorting", or an **agent manifest** | **No capacity at all.** An Information Content Entity. The package is a Directive ICE (it prescribes how to sort). The card and the manifest are descriptive ICEs about a claimed ability (CD13) | Always: an ICE is a generically dependent continuant, and in BFO only an independent continuant can bear a realizable entity | Anything. An advertisement is a claim to be tested, at most evidence. Installing the package can change a machine's make-up, and so ground case 4 or 5, but then the machine bears the ability, not the package |

Read down the "classified as" column, and the activity kind never changes: in every row
the ability is one realized in mail sorting. Only the classification changes, and each
change has a stated condition.

## 4. Possession versus advertisement

Possession and advertisement differ in what does the bearing, and in what counts as
evidence.

- **Possession.** A material entity bears a realizable entity, grounded in its own make-up
  (a function or disposition) or, for an agent, in its capacity to act. It is established
  by evidence about the bearer: performance, tests, design records. A capability need not
  have been exercised (CD8).
- **Advertisement.** An ICE says, or prescribes, that something can be done. A card, a
  manifest or a package is about the ability and bears nothing. It can be true, false or
  stale, and the same card can be served by different deployments.
- **The bridge between them.** An advertisement may *cite* evidence or *be* evidence. It
  never constitutes possession. This is CM-01's rule that a skill is evidence and never the
  capability (G1-I), applied one level down.

## 5. Do existing BFO and CCO constructs suffice?

**What they already provide, with no new term:**

- Every bearer-specific classification: Skill, Organization Capability, Agent Capability,
  Artifact Function, and BFO function and disposition.
- Bearing: *bearer of*, *inheres in*, *capability of*, *has capability*, *aggregate has
  capability*.
- Realization: BFO *realizes* and *has realization*.
- Participation and agency in acts: *has agent*, *agent in*, *uses*, *participates in*.
- What an advertisement is: ICE, Directive ICE, *is about*, *prescribes*.
- The type-level link from a capability to its activity kind: BCO's existing Realization
  Index pattern, annotations already in use, with no object property.

So the common treatment needs no new class or property *as a conceptual model*: the
example in section 3 is stated entirely in existing terms.

**Where they stop.** These are genuine gaps, not to be papered over:

- **G1. No type-level "realizable in" relation.** BFO's *has realization* holds between
  instances and needs an actual realization. The class expression *realizable entity and
  (has realization some Act of mail sorting)* would therefore exclude every unexercised
  capability, contradicting CD8. Today the shared activity kind can be *recorded*, as an
  annotation index. It cannot be *reasoned over*. Making it reasoned would need a new
  property or a modal pattern, which is a Stage 05 decision. This note does not propose
  one.
- **G2. No specific mail-sorting process type.** The bearer-neutral class exists: BFO's
  Process (`obo:BFO_0000015`). What the verified source terminology lacks is a specific
  mail-sorting process type that can be used consistently across human and artificial
  implementations.
  - BPO's act types are Planned Acts, so they require an agent.
  - In the deployed case (case 4) a BPO act type is enough, because the act is the
    organization's.
  - For a process with no agent in it, nothing in BPO or the pinned CCO names the kind.
  - This analysis introduces no such class.
- **G3. No named common class.** "Mail-sorting capability" as one class over every bearer
  would have to sit under realizable entity, not under Agent Capability. Under Agent
  Capability, the Agent equivalence would make every bearer an Agent. Realizable entity
  also includes roles, so a real common class would need its own definition and admission
  test. It can be written as an unnamed OWL class expression. Naming it is new
  vocabulary.

## 6. Genuine limitations of CCO's Skill

They are stated here so that CM-02 works around them in the open, without redefining
anything.

- **L1. Skill is "person capability", not skill.**
  - The definition says nothing of learning, practice or proficiency. An innate ability
    of a person is a Skill by the equivalence axiom.
  - The everyday and HR sense of skill, as in O*NET and ESCO, is narrower in one way and
    wider in another: those catalogues mix skills with knowledge and abilities.
  - Catalogue "skills" will therefore not map one-to-one onto `cco:ont00000089`. That is a
    rule for C-4, not a reason to change CCO.
- **L2. It is indexed by bearer only.** The "certain type" of act is in the text and in no
  axiom. CCO alone cannot say that two Skills are the same skill, or that Joe's skill and
  the post office's capability are of one activity kind. This is the gap the architect
  identified. G1 is its formal form.
- **L3. Only humans.** Person means Homo sapiens. A trained detection dog, or an artificial
  system that passed C-1, would bear an individual Agent Capability with no Skill-like
  class. CCO has no class for "an individual, non-collective agent's capability".
  Agent Capability itself is the only home, and that is acceptable.
- **L4. Agency is circular, and "held by" is undefined.**
  - Agent is defined through Agent Capability. Agent Capability is defined through Planned
    Act. Planned Act is defined through Agent, and through a directive "held by" an agent,
    a relation CCO never formalizes.
  - Planned Act asks that the directive be held by *at least one* of the agents. It does
    not ask that every causative participant hold it.
  - CCO therefore gives no independent test of agency. Any test for an artificial system
    has to be stated by BCO, as an evidence criterion (section 8, R2). It cannot be read
    off CCO, and it must not presuppose that the system is already an Agent.
- **L5. Attribution commits you to agency.** Because of the Agent equivalence, attributing
  an Agent Capability to a material entity entails that it is a CCO Agent. CCO cannot say
  "this system has an agent-like capability, its agency undetermined". Case 5 stays an
  Artifact Function until the evidence is reviewed and passes.
- **L6. Agent Capability is not a disposition by CCO's axioms.** It sits under realizable
  entity, not under BFO disposition. Whether a given capability is a disposition is a
  separate claim. For business capabilities, BCO makes it only after G1-T (DP-2).
- **L7. Agent Capability and Artifact Function are not disjoint.** CCO declares no
  disjointness between them, and this analysis assumes none.
- **L8. Realization relations do not express capacity.** BFO's *realizes* and *has
  realization* relate actual processes to realizable entities. They must not be used in a
  way that makes past exercise a condition of having a capability (G1; CD8).
- **L9. Capable members do not make a capable group.** A group whose members are each
  capable does not thereby bear a capability of its own, and certainly not an
  organizational one (CD10; case 3). CCO's *aggregate has capability* records member-wise
  attribution only.

These limitations are part of the analysis. They are not defects to repair by extending
the ontology without authorization.

## 7. Options for C-1

| Option | What it is | Assessment |
|---|---|---|
| **A. Activity-anchored, bearer-orthogonal** | The activity kind is fixed once, by its realization type (the Realization Index pattern). Each individual capacity takes the CCO or BFO class its bearer and grounds justify (section 3). Artificial systems default to Artifact Function, with Agent Capability only on a recorded test | **Recommended.** It meets the direction: no artificial distinction between activity kinds, no presumption of agency, no CCO change, no new term now. It leaves G1 to G3 visible, for decision at Stage 05 |
| **B. A named, bearer-neutral capability class per activity** | "Mail Sorting Capability" under realizable entity, with each bearer's capacity also classified under it | It gives the common concept a name, but mints a class family before C-1 is settled. It also needs a definition and an admission test that exclude roles. Better kept as a later Stage 05 option, built on A |
| **C. Everything under Agent Capability** | Treat capable artificial systems as Agents | Rejected. The Agent equivalence makes agency a side effect of classification, against the direction and the scope note |
| **D. Bearer-specific parallel vocabularies** | Separate "mail-sorting skill", "mail-sorting organization capability" and "mail-sorting function" types with no shared anchor | Rejected. It creates exactly the artificial distinction between activity kinds that the direction rules out |

## 8. Recommendation, as decided

The architect adopted R1 to R4 on 2026-11-18, R2 in a refined form
(`docs/decisions/2026-11-18-cm02-c1-decided.md`). They are stated here as adopted.

- **R1. Option A.** An activity kind is described once, through the process type its
  capacities are realized in. Each particular capacity is classified by its bearer, using
  the applicable CCO class. Information artifacts that describe or advertise it are kept
  apart. Sharing an activity kind does not equate two capacities, and does not give them
  the same realization conditions.
- **R2. C-1: the functional interpretation, as evidence criteria.** Whether an artificial
  material system bears an Agent Capability is assessed case by case. The assessment must
  establish all four of these:
  1. **The bearer.** A deployed material system is the proposed bearer, not a software
     package, a model file or a descriptive information artifact.
  2. **A causative role.** The system has a capacity to play a causative role in the
     relevant objective-directed activity, and is not merely a passive instrument.
  3. **Operational control of a directive.** The system can operationally represent and
     use a directive or plan, select relevant actions toward its objective, and respond
     appropriately to relevant changes in circumstances.
  4. **The system's own capacity.** The capacity belongs to the deployed system in its
     actual configuration. It is not attributed solely from human operators,
     organizational arrangements, documentation or vendor claims.

  How the criteria are to be read:

  - **They are evidence criteria, not an axiom.** They are BCO's criteria for review. They
    are not an OWL definition of Agent Capability, and they introduce no "holds directive"
    relation.
  - **They go beyond CCO's own requirement.** CCO's Planned Act requires that at least one
    involved Agent hold the directive. Criterion 3 asks more of an artificial system whose
    own capability is in question (L4).
  - **No circularity.** They do not presuppose that the system is already an Agent.
  - **No prior exercise is required.** Design, configuration, deployment and operational
    evidence can establish an unexercised capacity (CD8).
  - **What does not count.** A thermostat's stored setpoint, a simple fixed automation, an
    advertised AI skill, or a human operator's instructions do not establish agency merely
    by existing.
  - **Being nonhuman does not exclude a system.** Where the evidence establishes the
    capacity, CCO permits an Agent Capability, and the system's classification as an Agent
    follows from CCO's unchanged equivalence axiom. The review must say so.
  - **Failing a criterion.** A system that fails any criterion has its ability classified
    as an Artifact Function, or a BFO function, of the material system. It is never a
    Skill unless the bearer is a Person.
- **R3. Information artifacts never bear.** AI skill packages, agent cards and manifests
  are information artifacts: directive when they prescribe, descriptive when they
  advertise. They are evidence at most. The deployed material system is evaluated on its
  own.
- **R4. The limitations are recorded.** L1 to L9 stand as stated in section 6, and gaps G1
  to G3 are carried to Stage 05 as questions. None is answered by redefining CCO.

## 9. What the decision settles and leaves open

**Settled.** C-1 is resolved conceptually, through Option A and the qualified functional
interpretation. This analysis is the C-1 baseline for CM-02.

**Not authorized.** The decision authorizes:

- no OWL formalization;
- no class, object property, IRI or axiom;
- no ingestion of external skill catalogues;
- no change to any CCO definition.

**Still needed.** CM-02 needs its own model, competency questions, practitioner review and
approval under the Stage 02 standard.

## Sources

- CCO v2.0 merged, commit `510dad76be0ef710b65a421075af912af25342b7`, SHA-256
  `e609db27478a2c8b52b9bb5eb5ac979ac323510e851c368e4d9ec7d1c153fe5b`; BFO 2020 core,
  SHA-256 `6944e2c96a0d8709dc15ae5364792019e208061eda3f32311af4f3b8d8443a3b`; pins in
  `config/upstream-sources.yaml`.
- The CM-02 scope note, approved (`docs/proposals/2026-10-31-cm02-scope-note.md`): §1,
  §2, §4 (C-1, C-2, C-4), §5.
- CM-01, approved (`src/02_conceptual_models/CM-01-business-capability.md`): P2, Skill,
  Realization Index, Agent Manifest; DP-1, DP-2; specification CD8, CD10, CD13, §8 G1-I.
