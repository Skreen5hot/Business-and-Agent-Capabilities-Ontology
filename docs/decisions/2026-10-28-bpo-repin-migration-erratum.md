# Erratum — BPO re-pin migration record: 13 changed comments, not 14

**This corrects a record of work. It is not a decision, and it changes no decision.** It
was found while the facts in the BPO acknowledgment were being checked before it was sent,
as `docs/decisions/2026-10-28-i2a-decided.md` section 1 requires.

## What was wrong

Three documents say that, across the whole upstream file, `bc64e91` differs from
`327ea2c` in "14 `rdfs:comment` literals":

- `docs/decisions/2026-10-28-bpo-repin-migration.md`, line 69, as merged at `6731f59`,
  SHA-256 `f7cafd49cf4589178efbc85c883dddc06bc6b7d876be6bb42bf914c5050fb349`;
- `docs/proposals/2026-10-28-bpo-repin.md`, section on the candidate pins;
- the acknowledgment draft, `docs/proposals/2026-10-28-bpo-repin-acknowledgment-draft.md`.

## What is true

- **13 comments plus one version triple.** 14 triples differ between `327ea2c` and
  `bc64e91`: 13 `rdfs:comment` literals and the ontology's `owl:versionInfo` (0.4.0 to
  0.4.1). So the count of 14 included the version triple.
- **Measured on 2026-10-28**, with rdflib, from the files fetched at each commit:
  - SHA-256 of `327ea2c` `21b18ac3…347d`;
  - SHA-256 of `bc64e91` `a8119728…c6fd`.
- **The 13 subjects:**
  - ActOfAccounting;
  - ActOfCardAdministration;
  - ActOfCommunication;
  - ActOfDeployment;
  - ActOfImplementation;
  - ActOfImprovement;
  - ActOfInvestigation;
  - ActOfMonitoring;
  - ActOfOrganizationalEstablishment;
  - ActOfProcessControl;
  - ActOfRemuneration;
  - ActOfScheduling;
  - ActOfTransportation.
- **The isomorphism claim stands, with a precision.** `327ea2c` is graph-isomorphic to
  `6613194` under BPO's base substitution, ignoring `owl:versionInfo`.
  - BPO's substitution replaces `http://example.org/apqc` with
    `https://fandaws.com/ontology/bpo`. It therefore also moves the ontology IRI, from
    `…/apqc/ext` to `…/bpo/ext`.
  - A substitution of the `#` namespace alone leaves 3 header triples unmatched.

## What this does not change

- **The vendored genera.** The per-genus table in the migration record is correct. There
  are three changed comments among the six vendored genera: Improvement, Organizational
  Establishment and Remuneration. No label, definition, superclass or type changed.
- **The facts the decisions relied on.** R2's conditions, namely the definitions and
  relevant axioms being unchanged, rest on that per-genus comparison. This correction
  does not touch it.
- **The approved documents.** They stay as merged, and their digests in
  `docs/decisions/2026-10-28-bpo-repin-approved.md` stay valid. This erratum stands beside
  them.
- **The acknowledgment as sent.** `communications/bpo/outgoing/2026-10-28-repin-acknowledgment.md`
  states the corrected count.
