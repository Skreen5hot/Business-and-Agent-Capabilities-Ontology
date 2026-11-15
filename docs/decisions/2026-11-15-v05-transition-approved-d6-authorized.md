# Decision record — v0.5 transition approved, publication notice corrected, D6 first tranche authorized, 2026-11-15

Recorded verbatim by Claude Code (`claude-opus-5-5`) on 2026-11-15, from the direction the
architect, Aaron Damiano, Product Owner and Ontology Architect, gave in session on commit
`48be208`. The acts are the architect's. This record makes none.

## What it is about

Branch `vocab/spec-v0.5-in-force`, commit `48be208fc4ce5ec5601cac6c4eb3febea280585b`:

| Record | SHA-256 at `48be208` |
| --- | --- |
| `docs/decisions/2026-11-15-spec-v0.5-in-force.md` (the transition, A) | `ebcf755fe4d88937744dfc44ce9edd6b5f636b3f0253d2228b728db64c84d255` |
| `src/01_controlled_vocabulary/metamodel.yaml` (the nine revisions, A) | `7c4649324568cc274e134441aea18fc4b14191c8707690109a54d2e2f09f1e53` |
| `src/01_controlled_vocabulary/generated/bco-metamodel.ttl` | `babe3491ae2f8b39af642b0714da110fefca294dc233c71420c4efdaf0279ad1` |
| `site/content/site.json` (the notice corrected in B) | `05224a22922533706f28a2eeee181952a57eaebdc39b26397dc4923e8caccc57` |
| `config/upstream-extracts.json` (C) | `983527284a3d85d12e4641ff2b705c517228e473fee24e5803b108ecb2f159b1` |
| `vendor/bfo/bfo-core-bco-extract.ttl` (C) | `86c83303a4427f5939db0a3ce780d3b87ca4916262bae5a827b17cfd1a08783d` |
| `vendor/cco/cco-bco-extract.ttl` (C) | `8e82210bed0293582eda523c1d479366b920ac1b45f2acb07691e1b7d64884ad` |
| `docs/standards/stage-05-ontology.md` (the D5 standard D6 implements against) | `7faf9e2fc3ee60d868e11a626999475c0a5caf80286524a74386c9bbb6d98f1f` |
| `docs/proposals/2026-11-15-d5-readiness-package.md` (the tranche, E) | `f6f579975ad7a01c0589f86e43b9b9ca9b62968afe96cfb3a9a395331ba379e9` |

## The decision

> Subject: Architect Direction — v0.5 Specification Transition and D6 Implementation
> I have reviewed your report on commit `48be208`.
> Decision: APPROVE THE SPECIFICATION TRANSITION, WITH ONE PUBLICATION CORRECTION, AND AUTHORIZE THE FIRST D6 FORMALIZATION TRANCHE.
> A. Specification v0.5 — Approved
> I approve making `Business-Capability-Ontology-v0.5.0-draft.3.md` the current specification reference under its established CP-0 ratification decisions.
> Preserve v0.4 and earlier versions as historical artifacts.
> I accept the nine metamodel vocabulary-record revisions and the parser changes supporting both specification formats.
> The reported successful verification of all 46 historical record digests is appropriate evidence that the previous records remain reproducible.
> Do not reopen the previously ratified architectural decisions.
> B. Public-Site Notice — Correct Before Publishing
> Replace the proposed notice with:
> "The Business Capability Ontology is under development and has not been released. Its v0.5 specification commitments have been ratified under CP-0. Forty-two Business Capability types have passed G1-T admission, but their OWL classes have not yet been implemented. Controlled-vocabulary ratification and ontology formalization are separate activities, and the remaining vocabulary records retain their applicable review statuses."
> Ensure the specification's ratification status is visibly linked to the controlling CP-0 decision records.
> The historical draft.3 filename and document digest may be preserved. Do not imply that every requirement has already passed executable validation merely because the specification was ratified.
> C. Vendored Extracts — Approved With Verification
> I accept regenerating the pinned BFO and CCO extracts against the current specification.
> Before merging, verify that removing Contractor Role and Directive ICE does not break any approved requirement, ontology dependency, validation shape, conceptual pattern or required provenance check.
> Do not retain terms solely because v0.4 mentioned them, but do not remove terms that remain necessary to the actual ontology dependency graph.
> Preserve the upstream pins and extract provenance.
> D. Repository Integration — Authorized
> You may push `48be208`, open the PR, perform the required checks, and merge after successful CI and confirmation that the final diff contains only approved changes.
> Record the final commit and generated artifact digests.
> Coordinate the integration with PR #52 so the approved D5 standard, readiness decision and specification-in-force baseline are all represented consistently on `main`.
> E. D6 — Stage 05 Ontology Formalization AUTHORIZED
> I now authorize D6 implementation for the first Business Capability formalization tranche previously approved under D5.
> Scope:
>
> * The generic `bco:BusinessCapability` parent.
> * The 39 specifically identified G1-T-admitted capability types eligible for the first tranche.
>
> The three admitted types held for additional source checks remain excluded. The Q-12-blocked candidates also remain excluded.
> Required implementation work:
>
> 1. Complete the approved pinned BPO extract expansion for the 156 distinct realization-index act classes and the necessary existing ancestry.
> 2. Complete the approved ROBOT, ELK and HermiT dependency pinning and validation configuration.
> 3. Implement the parent and 39 eligible capability types as OWL classes, using their admitted definitions and approved IRIs.
> 4. Reuse existing BFO/CCO superclass and relation patterns. Consult the Extended Relation Ontology first when selecting formal relations.
> 5. Generate the existing BPO `enablesProcess` annotations from the signed G1-T indexes, with exact-record verification.
> 6. Implement the applicable OWL and SHACL checks and the required positive and negative fixtures.
> 7. Execute the approved reasoner and validation checkpoints before claiming the formalization tranche has passed.
>
> Restrictions:
>
> * No new object properties.
> * No automatic subclass axioms from SKOS broader links or source-framework hierarchies.
> * No invented BPO act classes.
> * No `requiresCapability` assertions.
> * No changes to signed G1-T definitions or realization indexes without the applicable change control.
> * No automatic G1-I assertions about particular organizations.
> * No claim of release or complete BFO/CCO conformance before the prescribed validation evidence exists.
>
> You may perform the approved dependency and validation preparation immediately. Implement the substantive OWL tranche against the integrated D5 standard and current specification baseline.
> F. Next Deliverable
> I do not want another general readiness proposal.
> The next major deliverable should be an executable Stage 05 ontology implementation containing the approved parent and 39 eligible types, together with validation results and a clear account of any genuine blockers.
> Report the number of OWL classes implemented, indexes verified, validation constraints tested, reasoner results and unresolved defects.
> Final direction: Approve the specification transition, correct the publication notice, integrate the branch after CI, and proceed with the authorized D6 first-tranche implementation.

## Acts it contains

| Act | What it settles |
| --- | --- |
| A | v0.5.0-draft.3 is the current specification reference; the nine revisions and the parser changes are accepted; v0.4 and earlier stay as historical artifacts |
| B | The site's notice is the text above, and the ratification status links to the CP-0 records |
| C | The regenerated extracts are accepted once the removal of Contractor Role and Directive ICE is verified harmless |
| D | Push, PR, CI and merge of `48be208` are authorized |
| E | D6 is authorized for the first tranche: `bco:BusinessCapability` and the 39 types of D5-3 |

## A note on the notice's count

The notice says forty-two types have passed G1-T admission. That is the D5 record's
reading: 42 catalog concepts with a signed PASS. G1-T has signed 43 types PASS; the 43rd,
T1-01, has no catalog concept (`docs/decisions/2026-11-15-bpo-inquiry-and-d5-approved.md`,
"Reconciling 42 with T1-01"). The notice is published as directed.

## Verification under C

Done before the merge, against the regenerated extracts at the pins (BFO `044490fc`,
CCO `510dad76`, BPO `bc64e91`, unchanged):

| Term | What the regeneration did | What still names it | Verdict |
| --- | --- | --- | --- |
| `cco:ont00000506` Contractor Role | Left the CCO extract (6 triples). v0.5 does not name it; v0.4 named it only in OI-8 | No shape, ontology module, vocabulary record, CM-01 or CM-02 pattern, standard or test names it. v0.3's worked example did, and v0.3 is documentation | Safe to remove |
| `cco:ont00000965` Directive ICE | Stopped being a seed (v0.4 named it only in a change table). **It is still described in full**: it is the named ancestor of Plan (`ont00000974`), Objective (`ont00000476`) and `ont00001324`, which section 4's parents reach, so the closure keeps it | The extract's own subclass, domain, range and disjointness triples | Not removed. The commit message of `48be208` and HANDOFF said it was; that was wrong, and both are corrected |
| `obo:BFO_0000023` role | From full to stub: its identifier, parent, alt label, definition and example left; its type and label stay | `obo:BFO_0000016 owl:disjointWith obo:BFO_0000023` (kept); the site's label map; one negative vocabulary fixture (`catalog-ancestor-unrelated`), which still fails as intended | Safe. Role is not a dependency of any BCO term; the disjointness the D5 package cites (§5) is kept |

Provenance: the pins, their file digests and each extract's header are unchanged in
form; `config/upstream-extracts.json` records the new seeds and digests. The validation
gate, the vendoring check and the full suite pass on the regenerated extracts.

## Integration under D

PR #53 (branch `vocab/spec-v0.5-in-force`, commits `48be208` and `32176e2`) passed CI (Build
and check; Contract, licensing, tests; Vocabulary schema) and its diff held only A, B and C:
the specification transition, the site notice and CP-0 links, the regenerated extracts,
and the records. It was merged on 2026-11-15 as
`97f047b79ebcfab1848f94c8216f1d5f3904f9c5`. PR #52 had merged before it (`b0ffdd5`), so
`main` at `97f047b` carries the D5 standard (`docs/standards/stage-05-ontology.md`), the D5
decision and the v0.5 baseline together.

Generated artifacts at `97f047b`, by SHA-256:

| File | SHA-256 |
| --- | --- |
| `config/upstream-extracts.json` | `983527284a3d85d12e4641ff2b705c517228e473fee24e5803b108ecb2f159b1` |
| `vendor/bfo/bfo-core-bco-extract.ttl` | `86c83303a4427f5939db0a3ce780d3b87ca4916262bae5a827b17cfd1a08783d` |
| `vendor/cco/cco-bco-extract.ttl` | `8e82210bed0293582eda523c1d479366b920ac1b45f2acb07691e1b7d64884ad` |
| `vendor/bpo/bpo-ext-bco-extract.ttl` | `059f01139ff5c02dcf070d8472c56854177e538015249102d353ea45ea25c4bd` |
| `vendor/NOTICE.md` | `51e728d62667bf24a4e6801f5071861f853f575dd70a4bd9b36675daea56a1ba` |
| `src/01_controlled_vocabulary/generated/bco-metamodel.ttl` | `babe3491ae2f8b39af642b0714da110fefca294dc233c71420c4efdaf0279ad1` |
| `config/vocab-schema.json` | `81c4220aa94792e50281f73f5149abfec87bf6ffc4ec52350b597160c470fa66` |
| `config/validation-baseline.json` | `ffb9a584beb62e3b3dfc53f198a7cfc50052c8f0516852681c86da686ce24d9d` |
| `config/corpus-digest.json` | `9d9977676bf0a9f31d78d1e6aaeca1c48bc44914797921d937d2bc300ba4bbc1` |
