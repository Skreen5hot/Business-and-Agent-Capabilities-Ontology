# Decision record — P5 pilot vocabulary: delivery accepted, nothing ratified, 2026-10-24

Recorded verbatim by the setup agent (Claude Code, `claude-opus-5-5`) on 2026-10-24, at the
statement the product owner and architect, Aaron Damiano, made in session. The act is his.

---

````text
Merge PR #6 with a merge commit so the 14 Draft terms are live on the site for my review. Record that I accepted P5's delivery, not any ratification.
````

---

## What this accepts

The **delivery** of P5: PR #6, head `76b47fce225021b2ce3692e88725cca2656312ff` on branch
`ccv/p5-pilot-terms`. It contains:
- 9 metamodel concepts (definitions from specification §4);
- 5 catalog concepts (authored genus–differentia definitions);
- all 14 Draft, each with sources from the register.

PR #6 merges to `main` with a merge commit so that the Draft terms are published on the site
for the architect's review.

## What this does not do

- **It ratifies nothing.** No concept's status changes. Every one of the 14 stays **Draft**,
  because no ratification act names it (ADR-003 D5).
- **It does not approve any definition, source citation or departure note.** Reviewing those
  on the site is the purpose of publishing them.
- **It does not settle the open points the PR raised:**
  - no PCF notations, because no BPO catalog node designates the five capability classes;
  - BPO slice 1.0 contradicts the specification's OI-9 on Business Model Governance;
  - whether Competitive Analysis belongs in the catalog;
  - the `genus` field set to `cco:ont00000568` while `bco:BusinessCapability` is unminted;
  - the Status page's stale "0 authored terms" wording;
  - the locators that fall short of a section or page.

## How a ratification will happen

By a separate act of the architect, recorded in `docs/decisions/`, that lists explicitly:
- each concept IRI it ratifies;
- that concept's current `record_sha256` (ADR-003 D5, confirmed 2026-10-23).

The digests listed in PR #6's body are valid at `76b47fce`. Any edit to a concept record, or
to its specification §4 row, before the act changes that concept's digest.
