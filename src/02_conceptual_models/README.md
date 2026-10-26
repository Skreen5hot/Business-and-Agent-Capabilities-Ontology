# Stage 02 — Conceptual Modeling

**Status:** in progress. CM-01, the Business Capability Conceptual Domain Model
(`CM-01-business-capability.md`, 0.1.0-draft.2), is drafted and awaits the architect:
its decision points DP-1 (RP-1) and DP-2 (RP-10) must be decided before it can be approved.

Standard: `docs/standards/stage-02-conceptual-modeling.md`. The architect's choices for
this stage are in `docs/decisions/2026-10-25-stage-02-choices.md`: one domain model
organized as patterns, Mermaid diagrams each with a textual description beside it, and
RP-1 and RP-10 decided through CM-01.

No conceptual model is approved.

Every `CM-<nn>-<words>.md` here is checked by `python tools/conceptual/check_models.py`
(in the before-committing list and in CI): its sections, diagrams, concept and
relationship descriptions, traceability, decision points and approval state, against the
format its module docstring states. Nothing else belongs in this directory.
