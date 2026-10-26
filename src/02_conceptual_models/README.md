# Stage 02 — Conceptual Modeling

**Status:** in progress. CM-01, the Business Capability Conceptual Domain Model
(`CM-01-business-capability.md`, 0.1.0-draft.5), is drafted and awaits the architect's
review and approval. Both decision points are decided: DP-1 (RP-1,
`docs/decisions/2026-10-25-dp1-rp1-grounding-boundary.md`) and DP-2 (RP-10,
`docs/decisions/2026-10-26-dp2-rp10-admission-attribution.md`).

Standard: `docs/standards/stage-02-conceptual-modeling.md`. The architect's choices for
this stage are in `docs/decisions/2026-10-25-stage-02-choices.md`: one domain model
organized as patterns, Mermaid diagrams each with a textual description beside it, and
RP-1 and RP-10 decided through CM-01.

No conceptual model is approved.

## Planned models

| Model | Status | Why it is needed |
| --- | --- | --- |
| CM-01 Business Capability | Drafted (0.1.0-draft.5), not approved | The capabilities an organization bears, their grounding, realization, description, sourcing and coverage |
| CM-02 Agent Capability (working title) | Planned, not started; scope not yet set | A complementary model for capabilities borne by agents other than an organization as a whole, which CM-01 deliberately places outside its scope: a person's Skill and Agent Capability (CD1), member-wise abilities of an aggregate (CD10), and the functions of the computing artifacts that software agents run on (CD13). CM-01 relies on these as evidence and enabling conditions without modeling them. Recorded at review R9's request as a broader scope dependency, not a reason to redesign CM-01. The repository's name already reaches this far |

Starting CM-02, and setting its scope, is the architect's decision.

Every `CM-<nn>-<words>.md` here is checked by `python tools/conceptual/check_models.py`
(in the before-committing list and in CI): its sections, diagrams, concept and
relationship descriptions, traceability, decision points and approval state, against the
format its module docstring states. Nothing else belongs in this directory.
