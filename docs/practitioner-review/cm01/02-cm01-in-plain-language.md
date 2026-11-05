# CM-01 in plain language

This is a summary of the approved model, CM-01 version 0.1.0. Where it and CM-01 differ, CM-01 governs. References such as "§4 Capability Basis" point into CM-01. Nothing here is from the draft specification unless it says so.

## The core idea

An organization can do things. What it can do is a **business capability**: something the organization *has*, which exists whether or not it is being used, and which shows itself when the organization's members carry out business acts of certain kinds. The model keeps three things apart that business-architecture practice often bundles:

- being **able** (the capability);
- being **permitted** (authorization);
- being **in a position** to act now (the systems, services and conditions the capability depends on, and whether they are available).

It also keeps everything people *write about* capabilities (maps, assessments, ratings, targets) separate from the capabilities themselves. Putting a capability on a map does not claim the organization has it.

## Principal concepts

| Concept | In plain words | CM-01 |
| --- | --- | --- |
| Organization | The bearer of business capabilities: a group whose parts are its members | §4 Organization |
| Business Capability | A particular organization's ability to perform a kind of work. It may never yet have been exercised | §4 Business Capability |
| Capability Type | A kind of capability, such as strategic planning. One organization's capability may fall under several types | §4 Capability Type |
| Member Agent | A person, or a member organization, that belongs to the organization | §4 Member Agent |
| Capability Basis | The members in whom the capability is grounded. One member can be enough | §4 Capability Basis |
| Organizational Arrangement | The positions, reporting lines, routines and coordination that explain why those members, so organized, give the organization the capability | §4 Organizational Arrangement |
| Enabling Condition | What the capability depends on but does not consist of: systems, equipment, facilities, outside services | §4 Enabling Condition |
| Skill | A person's own ability. Not a business capability | §4 Skill |
| Act; BPO Act Type | A business act that happened, and its kind. Act kinds come from a companion Business Process Ontology (BPO) | §4 Act, BPO Act Type |
| Realization Index | For each capability type, the kinds of act that may exercise it. It says what may, not what must | §4 Realization Index |
| Type Admission Record | A once-per-type check that capabilities of this kind can genuinely belong to an organization, with no particular organization in view | §4 Type Admission Record |
| Capability Map | A description of one organization, whose entries are assessments and targets | §4 Capability Map |
| Capability Assessment | A statement about one capability type at one organization, with one finding (present, absent or partial), the criteria used and the evidence | §4 Capability Assessment |
| Capability Maturity Rating | A rating of a capability the organization has, on a stated scale. There is no rating of an absent capability | §4 Capability Maturity Rating |
| Capability Target; Target-State Specification | A capability the organization is to come to have; and the plan that contains targets and the acts that will reach them | §4 Capability Target, Capability Target-State Specification |
| Capability Sourcing Statement; Sourcing Assessment | A record that another organization provides certain work; and an assessment of the dependence it creates | §4 Capability Sourcing Statement, Capability Sourcing Assessment |
| Authorization Record; Evidence Scope | A record that an authority permitted an agent to perform a kind of act in a period; and the bounds within which "none recorded" means none | §4 Authorization Record, Evidence Scope |
| Standing Function; Coverage Register Entry | An ongoing business function ("Manage X") from the APQC process framework; and the list of capability types it requires | §4 Standing Function, Coverage Register Entry |
| Functional Adequacy Assessment | A judgment about whether an organization can actually perform a standing function, with separate findings for integration, availability and adequacy | §4 Functional Adequacy Assessment |

## The five patterns

**P1 — Capability and bearer (CM-01 §3 P1).** An organization bears a capability. The capability rests on a basis of one or more members, organized by an arrangement. Systems, equipment, facilities and outside services are enabling conditions. If one is lost, even permanently, the capability becomes unavailable rather than ceasing; it ends only when its basis or arrangement goes. A person's own ability is a skill, not a business capability. Roles, responsibilities, charters and authorizations show that an organization is responsible or permitted, not that it is able, so they do not appear here.

**P2 — Realization by business acts (§3 P2).** Business acts, of kinds the process ontology defines, exercise ("realize") a capability. They are performed by the organization's members. Each capability type lists the kinds of act that may realize it; that list does not claim that every such act needs a capability. Building or improving a capability ("developing" it) is different from exercising it. A capability that has never been exercised is still a capability.

**P3 — The description layer (§3 P3).** Maps, assessments, ratings, targets and plans are statements about an organization. There are three ways a statement can refer:

- to a *kind* of capability, with no claim that one exists — a target, for example;
- to a *particular* capability that exists — a rating, for example;
- as *evidence that the organization has one* — an assessment with a present finding.

**P4 — Sourcing and authorization (§3 P4).** If a provider's staff do certain work for the organization, the organization depends on that provider. It does not thereby have the capability itself. It may also have its own capability for the same work, and the two can coexist. A separate assessment records the risk of the dependence. Authorization is recorded but does not say that any permitted act happened. "No record found" counts as an answer only within a declared evidence scope; outside one, the answer is "unknown".

**P5 — Catalog, specialization and coverage (§3 P5).** APQC catalog entries and the project's vocabulary point at capability types; they are not the types. A standing function has a list of component capability types it requires. It points at a whole-function capability type only where one has been defined. Answering whether an organization can perform a function takes four questions, each answered separately:

- does it have every component capability;
- do they work together;
- are the systems and services available now;
- is it adequate to stated criteria such as volume, quality and timeliness?

None of the four is inferred from another (§6, "Functional coverage and adequacy").

## The two approved decisions

- **DP-1, the grounding boundary (§7 DP-1).** A capability rests on members in an arrangement. Artifacts and outside services are enabling conditions, not part of what it rests on. One member can be enough. Losing an essential platform for good does not by itself end the capability. CM-01 records this last point as the project's own commitment, and notes that defence and enterprise-architecture frameworks such as NAF and UAF count technology inside the capability. A capability type whose review shows a technology really is part of the ability is held for a separate, still-open question (§9 Q-15).
- **DP-2, admission and attribution (§7 DP-2).** Two separate checks.
  - *Type admission* asks once, per kind of capability, whether capabilities of that kind can genuinely belong to an organization.
  - *Attribution* asks, for each claim, whether this organization has one. Evidence of capacity can be enough. A record of past exercise supports the claim but is never required, and on its own must be backed by evidence that the people and arrangement are still in place.

## Approved and proposed

Everything above is in approved CM-01. The draft specification v0.5 proposes how these ideas become formal rules, such as validation requirements numbered CAP-nn. Those proposals are under review and not approved. File 06 lists the sources and their status.
