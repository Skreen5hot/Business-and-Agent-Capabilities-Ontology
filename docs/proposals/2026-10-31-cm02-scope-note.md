# Proposal — CM-02 scope and integration-boundary note (D2)

| Field | Value |
|---|---|
| Status | Proposal for the architect's approval under D2. **Not a decision.** |
| Date | 2026-10-31 |
| Prepared by | Claude Code (`claude-opus-5-5`), for the BCO team |
| Arises from | The architect's direction authorizing D2 (`docs/decisions/2026-10-31-d2-d3-authorized.md`); roadmap row D2 (`docs/ROADMAP.md` §4) |
| Governed by | The Stage 02 standard (`docs/standards/stage-02-conceptual-modeling.md`), §4.1 (establish scope) |
| Constrained by | CM-01 is approved and is not changed by this note; DP-1 and DP-2 are not reopened; no class, property, axiom or IRI is proposed |

This note sets the scope of CM-02, the future Agent Capability conceptual model, and its
boundary with CM-01. It is not CM-02. Approving it completes D2; it does not stand in for
CM-02's own practitioner review and approval, which come before any Agent Capability
formalization.

## 1. Purpose and scope

**What the module will represent.** The abilities of agents other than an organization
taken as a whole. CM-01 places three of these outside its scope and relies on them
without modeling them (`src/02_conceptual_models/README.md`):

1. **A person's abilities**: CCO's Skill, and whatever else a person can do that bears on
   organizational work.
2. **Member-wise abilities of a group**: several agents each able to do something, which
   CM-01 keeps apart from an organization's ability (CD10).
3. **What acting artificial systems bear**: software agents and the computing artifacts
   they run on, which CM-01 treats only as enabling conditions and as subjects of agent
   manifests (CD13).

**Intended uses.**

- Supplying the person-level evidence that CM-01's instance attribution cites: a
  position holder's skill supports, and never replaces, a claim that the organization
  bears a capability (G1-I question 2).
- Relating the skills an organization's members have to the capability types the
  organization bears or targets, for staffing and capability-gap analysis.
- Saying what an artificial system can do, in terms that keep it distinct from what an
  organization can do, so that agent manifests and routing (CD13) rest on a stated
  model.

**Outside its scope.**

- Organization capabilities. They are CM-01's, and nothing in CM-02 redefines them.
- Competency scoring, assessment methods and HR records. Ratings and assessments are
  represented, as in CM-01, not prescribed.
- Role, position, permission and responsibility, except as boundaries. They are CM-01's
  "able / permitted / responsible" distinction, and CM-02 inherits it.
- A new act hierarchy. Acts come from BPO (CM-01 A-01).
- Deontic reasoning and temporal qualification of bearing (CM-01 Q-06).

**One scope choice for the architect (S-1): artificial systems.** CCO defines an Agent as
"A Material Entity that bears an Agent Capability", so CCO itself does not rule out an
artificial system as a bearer. UAF lets any capable element, including resources,
exhibit a capability (SRC-OMG-04, V), and IOF lets any independent continuant bear one
(SRC-FO-02, V). CM-01 says software is information and bears nothing, and that any
function belongs to the computing artifact that runs it.

- **Option S-1a.** Include artificial systems as subject matter. CM-02 must then answer
  what such a system bears, an artifact's function or an Agent Capability, without the
  answer being presumed here.
- **Option S-1b.** Exclude them. CM-02 covers persons and member-wise abilities only.
  Software agents stay where CM-01 puts them, and the question is recorded as deferred.

**Recommendation: S-1a.** The repository's name and CM-01's routing use both point at
software agents, and the question will be asked whether or not the model answers it.
Under either option, CM-01's treatment stands for the Business Capability module:

- a system is never a member agent;
- a system is an enabling condition;
- a software agent bears no Organization Capability.

## 2. CCO alignment

From the vendored extract (`vendor/cco/cco-bco-extract.ttl`, CCO v2.0, SRC-FO-01, V):

| Term | CCO definition | Parent |
|---|---|---|
| Agent Capability `cco:ont00001379` | "A Realizable Entity that inheres in a Material Entity in virtue of that Material Entity's capacity to realize it in some Planned Act." | realizable entity `obo:BFO_0000017` |
| Organization Capability `cco:ont00000568` | "An Agent Capability that inheres in an Organization to the extent of that Organization's capacity to realize it in Intentional Acts of a certain type." | Agent Capability |
| Skill `cco:ont00000089` | "An Agent Capability that inheres in a Person to the extent of that Person's capacity to realize it in Intentional Acts of a certain type." | Agent Capability |

Intentional Act is Planned Act's alternative label (`cco:ont00000228`). Planned Act is
"An Act in which at least one Agent plays a causative role and which is prescribed by
some Directive Information Content Entity held by at least one of the Agents".

**What this gives CM-02.** Organization Capability and Skill are sibling kinds of Agent
Capability, distinguished by the kind of bearer. In CCO neither is a part, a sum or a
specialization of the other. Both sit under realizable entity, not disposition. CCO
declines the disposition placement that IOF and Beverley et al. adopt (SRC-FO-02,
SRC-FO-03, both V; register finding SF-01). Agent Capability itself is borne by any
material entity able to realize it in a Planned Act. That is where a capability that is
neither a person's nor an organization's would fall, and why S-1 matters.

**Person-borne and organization-borne capabilities.** A Skill inheres in a Person, and
its realizations are that person's acts. A business capability inheres in an
Organization, and its realizations are acts its members perform on its behalf, through
its arrangements (CM-01 P1, P2).

**Why an organization's capability is not an aggregation of its members' skills.** CM-01
already commits to the reasons, and CM-02 must keep them:

1. **The bearer differs.** The capability inheres in the organization, not in the
   members. CCO has a separate relation, `cco:ont00001898` aggregate has capability, for
   abilities a group has member by member. CM-01 never lets that relation stand for an
   organization's capability (CD10).
2. **The arrangement is part of the ground.** Under DP-1 the capability rests on its
   member agents *as organized*: positions, decision lines, routines and coordination
   (a1, a3). The same people, differently arranged, can give the organization a
   capability or take it away, with no change in anyone's skill.
3. **Plurality is not the criterion.** One indispensable member can be the whole basis,
   and the capability is still the organization's if it is realized through the
   organization's arrangements (R6-08's one-analyst firm; DP-1 a1; DP-2 b1). So "more than
   one skilled person" is neither necessary nor sufficient.
4. **Skills are evidence, not the capability.** A position holder's skill supports an
   attribution (G1-I question 2). It never constitutes one, and several members each
   having a skill is member-wise (CD10).

The management literature takes the same view. Winter treats a capability as routines
(SRC-MS-06), and Helfat and Peteraf as a team's coordinated performance (SRC-MS-05). But
the register's claims for both definitions rest on prior knowledge only (status K), so
CM-02 cites them as background, not evidence, until they are verified.

## 3. Integration with CM-01

CM-02 meets CM-01 at five points. At each, CM-01's approved meaning governs.

| Interface | CM-01 (approved) | What CM-02 adds | What CM-02 must not do |
|---|---|---|---|
| Member Agent | A person or member organization that is part of the organization; never a system | The person as bearer of Skills and other abilities | Make a system a member agent |
| Capability Basis (DP-1) | The member agent or agents themselves: material constitution (a1, a3) | What the members of a basis can each do | Make a skill the basis. The basis is the member, and the skill inheres in the member |
| Organizational Arrangement (DP-1) | The configuration that explains why the basis grounds the capability; not material (a3) | Nothing. Arrangement stays CM-01's | Recast arrangement as a sum of skills |
| Enabling Condition (DP-1) | Every artifact relevant to the capability's realization, owned or not; absence makes the capability unavailable, not ended | Under S-1a, what an artificial system bears | Move an artifact into the basis. A type whose review shows an artifact is constitutive goes to Q-15 (OI-14), by change control on CM-01 |
| Evidence and attribution (DP-2) | G1-I: evidence of capacity can suffice; a skill of a position holder is evidence | The representation of skills that an assessment cites | Let a skill, or skills together, assert bearing |

The distinction DP-1 keeps between an organization's *basis* (its member agents, as
organized) and the *enabling conditions* relevant to its realization (artifacts and
outside services) passes into CM-02 unchanged. A member's skill falls on neither side
on its own: it is borne by a part of the basis. An artificial system, whatever CM-02
finds it bears, remains an enabling condition of the organization's capabilities.

## 4. Module boundaries and dependencies

**Shared concepts** (defined in CM-01, used by CM-02 without redefinition): Organization,
Member Agent, Skill (CM-02 becomes its home; CM-01's boundaries for it stand), Act, BPO
Act Type, Enabling Condition, Evidence, Agent Manifest.

**Intended integration points.**

- Skill as G1-I evidence.
- Skill types related to capability types for gap analysis. This relation is not
  "requires", which CM-01 forbids for acts (CD12).
- Agent manifests resting on CM-02's account of artificial systems (under S-1a).
- BPO's `ex:CompetitiveAnalysisCapability`, an Agent Capability borne by an analyst,
  which the specification sends to Skill. Re-homing it is BPO's to decide.

**Exclusions.** Everything listed outside scope in section 1. Under S-1b, artificial
systems as well.

**Unresolved questions for the full CM-02.**

- **C-1.** Under S-1a: does an acting artificial system bear an artifact function, an
  Agent Capability, or either according to the case? What follows from CCO making
  whatever bears an Agent Capability an Agent?
- **C-2.** Are there person-borne abilities relevant here that are not Skills, and are
  there Agent Capabilities borne by groups that are not organizations (a team without
  organization rules)?
- **C-3.** How skill types relate to capability types, and to the acts both are realized
  in, without implying requirement.
- **C-4.** Whether skill catalogs (competency frameworks) enter as a catalog layer, as
  APQC did for CM-01. Any such source passes the rights gate first.
- **C-5.** Whether the interest condition (SF-04) applies to any CM-02 type. This is a
  CM-02 question only: b2's rejection for business capabilities stands.

**Deferred to the full CM-02.** Its concepts, patterns, relationships, competency
questions, practitioner review and approval.

**Dependencies.**

- The CCO pin (SRC-FO-01).
- BPO's acts, and Q-12 to Q-14, as for CM-01.
- The source register, which has no entry yet for skill or competency frameworks, or
  for artificial agency.

## 5. Implications for formalization

These are questions for Stage 05, raised now so CM-02 can be written with them in view.
None selects a property, introduces a class or states an axiom.

- **Placement.** CCO keeps Agent Capability, Skill and Organization Capability under
  realizable entity. CM-01 admits a business-capability type as a disposition only after
  G1-T (DP-2). Whether CM-02 types need an admission test of their own, and whether any
  is a disposition, is open. CM-01's answer is not to be assumed for persons.
- **Artificial systems (S-1a).** A designed artifact's ability fits BFO's function
  (`obo:BFO_0000034`), which is defined through intentional design. CCO's Agent
  Capability is defined through Planned Acts, which need an agent holding a directive
  information content entity. Which reading fits a given system, and whether both can,
  is the formal side of C-1.
- **Member-wise bearing.** CCO already has `cco:ont00001898` (aggregate has capability).
  CD10 restricts its use for business capabilities. CM-02 may use it for member-wise
  abilities, subject to formalization review.
- **Organization alignment.** CCO's Organization is a Group of Agents (`cco:ont00000300`),
  an object aggregate with only agents as parts. A member's skill is therefore borne by
  a part of the organization, which keeps it consistent with DP-1's basis without being
  the basis.
- **Namespaces.** No IRI is minted for CM-02 before its formalization tranche, and then
  only under ADR-003 D1.

## 6. Decisions requested

1. Approve this note as the CM-02 scope and integration boundary (D2's exit).
2. Decide S-1: include artificial systems (S-1a, recommended) or exclude them (S-1b).

Approval would authorize nothing beyond D2's completion: not the full CM-02, and no
Agent Capability class, property or axiom.

## Sources

- CM-01, approved: `src/02_conceptual_models/CM-01-business-capability.md` (P1, §4
  Member Agent, Capability Basis, Organizational Arrangement, Enabling Condition, Skill,
  Agent Manifest; §6; Q-15)
- DP-1: `docs/decisions/2026-10-25-dp1-rp1-grounding-boundary.md`; DP-2:
  `docs/decisions/2026-10-26-dp2-rp10-admission-attribution.md`
- Specification v0.4.0-draft.1: CD1, CD10, CD13, §8 G1-I
- Source register `docs/sources/register.yaml` and its companion: SRC-FO-01, SRC-FO-02,
  SRC-FO-03, SRC-OMG-04 (each V); SRC-MS-05, SRC-MS-06 (definitions K); findings SF-01,
  SF-04, SF-05
- CCO and BFO terms as declared in `vendor/cco/cco-bco-extract.ttl` and
  `vendor/bfo/bfo-core-bco-extract.ttl`
