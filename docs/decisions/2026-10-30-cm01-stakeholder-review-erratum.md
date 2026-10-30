# Erratum — CM-01 §10: which review met the stakeholder-review gate

**This corrects a record of work. It is not a new decision, and it changes no decision.**
CM-01's approval stands as made. The architect directed this erratum (below). CM-01 is
preserved unchanged.

## The architect's direction, verbatim

Recorded by Claude Code (`claude-opus-5-5`) on 2026-10-30, from the statements the product
owner and architect, Aaron Damiano, made in session.

The first statement:

````text
I would choose an erratum, provided your final review satisfies the project's stakeholder-review requirement.
````

Claude Code answered that no review by an agent can satisfy that requirement: the Stage 02
standard says "Conceptual adequacy and stakeholder agreement require human review". It
asked what the erratum should say met the gate, offering two answers. One was that the
gate was met by the architect's review of draft.5 as product owner, a domain stakeholder,
R8 and R9 being ontological reviews. The other was that the gate was not met, and a
domain-practitioner review is due before Stage 05. The architect chose the first:

````text
My review, as owner
````

## What was wrong

`src/02_conceptual_models/CM-01-business-capability.md` at `a60d53b` (SHA-256
`292c8f36d64075b9663e159985a15b448aa933c3b5ed4baff3b2a556ca861ccc`; approved as draft.5,
SHA-256 `a59e3cd4149693ce388deaa7c8953242a8c3355e4c7eef96d094c8e90a75b5a0`) records the
Stage 02 standard's gate "Domain stakeholders have reviewed the model" in two places in
§10:

- the **Stakeholder review** row lists R8 and R9 first, and then the architect's review
  of draft.5;
- the checklist ticks the gate on "R8 reviewed draft.1 and R9 draft.4".

Both rest the gate on R8 and R9. Those were ontological reviews of the model, not reviews
by domain stakeholders. The Stage 02 standard (`docs/standards/stage-02-conceptual-modeling.md`
§7) requires human review for stakeholder agreement, and a review's kind decides which
gate it can meet.

## What is true

- **The gate was met by the architect's review of draft.5, made as product owner.** The
  product owner is a domain stakeholder. That review is the one recorded in
  `docs/decisions/2026-10-26-cm01-approved-r8-r9-accepted.md`, whose statement begins "I
  have completed my review of CM-01 version 0.1.0-draft.5". The record names Aaron Damiano
  as "the product owner and architect".
- **R8 and R9 were ontological reviews.** They stand as what they were: reviews whose
  dispositions were accepted, and which shaped draft.2 and draft.5. They are not what met
  the stakeholder-review gate.
- **The gate's outcome is unchanged.** It was met before approval, by a different review
  from the one the checklist names.

## What follows

- CM-01 is not edited. When a later reviewed version of CM-01 is made for any other
  reason, its §10 states the gate as above, citing this erratum.
- The roadmap recommendation that a domain-practitioner review be a named gate before
  Stage 05 is not decided by this erratum. It remains a recommendation.
