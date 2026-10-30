# Decision record — the Ontology Template is not adopted; the BCO follows the recommended plan, starting with a roadmap, 2026-10-30

Recorded verbatim by Claude Code (`claude-opus-5-5`) on 2026-10-30, from the statements
the product owner and architect, Aaron Damiano, made in session. The acts are the
architect's. They are about the exchange with the Ontology Template team
(`communications/example/`, at `d7a3619`): the template's request
`EXAMPLE-BCO-2026-10-30-process-proposals`, BCO's answer and BCO's correction.

## Act 1 — the template is not adopted

````text
Regarding our communication with the Ontology Template team. Thank you for your inputs. We will not be adopting the template as we progress. BUT the conversation and templates principles should inform our future work. What in our roadmap should be adjust based on our conversations, that will improve the final quality and process flow.
````

Claude Code answered with nine recommendations. The architect directed that they be
followed.

## Act 2 — follow the recommended plan, starting with a roadmap

````text
Let now follow the recommended plan and start with a Roadmap
````

The architect pasted the recommendations with that statement. They are reproduced here
exactly as pasted:

````text
1. Write a current roadmap. HANDOFF §7 “Suggested next steps” dates from setup day: it still says nothing is pushed and CI has never run. BCO has no roadmap beyond the spec’s checkpoints. One roadmap record should name each step, its entry gate and its standard, and replace §7. Record your decision not to adopt the template in it too.
2. Spec v0.5 is the next item on the critical path, ahead of ratification and any formal work. v0.4 still predates CM-01, and HANDOFF’s “write the CAP shapes first” step predates it too. v0.5 should do four things:

* Carry the decisions forward: DP-1, DP-2, the R9 corrections, and the erratum. Add a short table mapping each decision to the sections it changes, so nothing is left uncarried.
* Check its sources: every source v0.5 relies on should be primary-verified (V or P) or explicitly excused. The register already shows weak spots, such as Helfat & Peteraf resting on prior knowledge only.
* Raise the known risks as decision points now:
   * BFO’s `has material basis` for DP-1’s “basis” commits to Disposition, which CM-01 deliberately did not.
   * Conditional standing-function designation can’t be an OWL class.
   * “Never exercised” questions need closed-world checking.
These are the formalization surprises still ahead. Deciding them in v0.5 is cheaper than discovering them in OWL.
* Only then CP-0: ratify RP-1 to RP-10, accept ADR-002, and fix the permanent namespace (RP-5).

3. Scope CM-02 before CP-0. Agent Capability is planned but unstarted, and CM-01’s basis is member agents. Ratifying RP-1 (who bears a capability) without at least CM-02’s scope and its boundary with CM-01 risks rerunning the mistake of drafting the spec before the conceptual model. A full CM-02 isn’t needed first; its scope and boundary are.
4. Make “standard supplied” an entry gate for every stage.

* Stages 03, 04 and 05 each need a standard before they start.
* Stage 01 has 14 concepts and no standard. Write it before any of them is ratified.

5. Re-check the five catalog concepts before ratifying any of them. They were written before the admission criteria existed. Run each one against the admission test (G1-T, from DP-2) and the R6 rewrite before ratification.
6. Add domain-practitioner review as a named gate. Place it at CM-02 approval, after any substantive CM-01 change, and before Stage 05 begins. Every review record should state the capacity the reviewer acted in. For BCO, a practitioner is a business architect or capability-planning lead, or a FIBF standards-lead-agency analyst.
7. Treat the inventory and terminology as a parallel lane.

* What may run now: I-3 (restricted catalogs, citation only) and I-4 (crosswalk and deduplication), each when authorized.
* What waits: I-5 (first-tranche recommendation) waits for CP-0, because it applies the admission test.
* Start a homonym register now. The inventory has already found ISO/CMMI “capability” and FIBF “business capability”. Stage 04 can begin from it.
* Keep rights as a gate on every new source before any harvest, as I-3 will need.

8. At Stage 05, check conceptual fidelity. Each authored term, and each axiom, cites the CM-01 element or decision it formalizes. That catches meaning drift, such as inferring adequacy from components, which CM-01 forbids.
9. Keep what worked:

* a closure gate before each new phase;
* decisions recorded verbatim with digests;
* errata as new records;
* one reviewed PR per phase.
````

## What this record does and does not do

- It records that the BCO will not adopt the Ontology Template, and that the exchange's
  principles inform its work.
- It records the direction to follow the plan above, starting with a roadmap. The roadmap
  is `docs/ROADMAP.md`, proposed for the architect's approval.
- It authorizes no step of the plan by itself. Each step starts when the architect
  authorizes it. It mints no IRI, ratifies nothing, and authorizes no inventory phase.
