# Decision record — E4: the method for level-3 standing-function candidates (Option A), 2026-10-30

The act is the architect's. It is recorded verbatim, with the rest of the closure set, in
`docs/decisions/2026-10-30-closure-decided.md`, under "Smaller corrections — APPROVED".
Claude Code (`claude-opus-5-5`) wrote this record on 2026-10-30 so that E4 has a record
of its own. It quotes the act and adds nothing to it.

**What it is about:** E4 as first decided, in
`docs/decisions/2026-10-28-i2-and-bpo-repin-decided.md` (SHA-256
`0a8b10a308a697c300b747163ce84bd312aeaff864202ea95c034b3fd50a44a0` at `a8fb873`).
That record approved Option A: each proposed level-3 standing function is evaluated
against CM-01's accepted definition, with a reason, independent evidence and a source
locator, and the list is submitted for explicit approval. No candidate is admitted
automatically.

## The act

> E4: I approve Option A: independently justified, documented, architect-reviewed
> classification of level-3 standing-function candidates against CM-01.
> This closes E4's method decision only. No standing-function candidate is approved by
> this act. Present actual candidate judgments through their separate review process.

## Effect

- **E4's method is decided.** A level-3 element becomes a standing-function candidate only
  through a written classification against CM-01's definition. Each classification has:
  - its own justification;
  - evidence independent of the catalog that names it;
  - a source locator.
  The architect reviews the classifications.
- **No candidate exists yet.** No element is judged, and none is approved. The judgments
  are presented through their own review.
- **The I-2b entries are unchanged.** `docs/sources/inventory/pcf-7.4-entries.yaml` keeps
  its generated header `e4: {state: open, judged: 0, ...}`. There, `open` means that no
  element has been judged, which remains true. Changing what the generator writes is a
  change to an I-2b output, for a reviewed PR of its own if wanted.

## What this does not do

- It does not approve any standing-function candidate, or admit any Capability Type.
- It does not authorize ontology IRIs, OWL classes, object properties, subclass assertions
  or vocabulary admissions.
- It does not start I-3, I-4 or I-5.
