# Decision record — CM-02 started; the Agent Capability / Skill distinction (C-1) first, 2026-11-18

Recorded verbatim by Claude Code (`claude-opus-5-5`) on 2026-11-18, from two directions
the product owner and architect, Aaron Damiano, gave in session. The acts are the
architect's.

## What it is about

| Field | Value |
| --- | --- |
| Document | `docs/proposals/2026-10-31-cm02-scope-note.md`, the approved CM-02 scope and integration-boundary baseline (D2, `docs/decisions/2026-10-31-d2-cm02-scope-approved.md`) |
| SHA-256 at this record | `35036ef2d6d0111f851af043c72cd733e83bc9e05774b014734b1d7dbc573a77`, the administrative revision recorded by the D2 approval; unchanged since |
| Commit | `main` at `8e6f0c4` |

## The acts

The first, given in reply to a survey of what came next on the roadmap:

````text
Lets start CM-02 be clear what an Agent Capability is verse an agent skill (are they the same?) What open sources have archived Agent Capabilities?
````

The second, given after an answer to the first that distinguished CCO's Skill from AI
skill packages and surveyed candidate sources:

````text
Subject: CM-02 — Resolve the Agent Capability / Skill Conceptual Distinction First
I am not satisfied with treating the human-versus-artificial bearer distinction as an adequate explanation of Skill.
I understand that CCO formally defines Skill as an Agent Capability inhering in a Person. We must respect that existing class and its OWL axioms.
However, the type of activity an entity can perform and the type of entity bearing that capability are separate ontological questions.
Consider mail sorting:

* Joe can have a mail-sorting capability, classified as a CCO Skill.
* A deployed AI-controlled material system might have a corresponding capability or artifact function, depending on its actual ontological status.
* An organization can have an organizational mail-sorting capability.
* An AI skill package or manifest can describe mail-sorting functionality without bearing that capability.

I do not want CM-02 to create artificial distinctions between the underlying activity kinds simply because the bearers differ.
My direction is to make this the first substantive modeling issue in CM-02.
Prepare a concise conceptual analysis that:

1. States the exact CCO class axioms and definitions for Agent Capability, Skill, Organization Capability, Agent and Person.
2. Separates the type of activity from the bearer-specific capability classification.
3. Explains how one task-oriented capability concept can be considered across persons, organizations and artificial systems without assuming that all such systems bear Agent Capabilities.
4. Distinguishes genuine capability possession from an advertised AI skill, software package or agent manifest.
5. Evaluates whether existing BFO/CCO constructs support the required common conceptual treatment without introducing new classes or object properties.
6. Identifies any genuine limitations of CCO's person-based Skill definition rather than attempting to conceal or redefine them.

Use mail sorting as a worked example, showing the classification of the individual capacity in each case and the conditions under which that classification is justified.
Do not assume an AI system is a CCO Agent. Do not automatically classify an AI system's ability as a Skill. Do not change the definitions of existing CCO terms.
Do not turn this into a broad source-catalog ingestion exercise yet. O*NET, ESCO, OASF and other sources can inform subsequent terminology development after their rights and semantic suitability are established.
Return the conceptual modeling options with a recommendation for C-1. I want the ontological issue settled before scaling the Agent Capability vocabulary.
The goal is a coherent ontology of capabilities across different kinds of bearers—not a vocabulary in which human and artificial abilities appear fundamentally different simply because one is called a Skill.
````

## What it does

- Starts the full CM-02 under the Stage 02 standard, within the approved scope note.
- Makes C-1, with the activity-kind / bearer distinction, CM-02's first substantive
  modeling issue, to be settled before the Agent Capability vocabulary is scaled.
- Directs a concise conceptual analysis with options and a recommendation for C-1. It is
  `docs/proposals/2026-11-18-cm02-c1-capability-analysis.md`.

## What it does not do

- It does not approve CM-02, decide C-1, or authorize Agent Capability formalization.
- It introduces no class, object property, IRI or OWL axiom, and changes no CCO
  definition.
- It does not admit any source. O*NET, ESCO, OASF and the others are not ingested; each
  enters only after its rights and semantic suitability are established.
- It does not reopen CM-01, DP-1, DP-2 or the D2 approval.
