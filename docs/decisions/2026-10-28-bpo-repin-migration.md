# Migration record — vendored BPO extract re-pinned to v0.4.1, 2026-10-28

**This records work done under a decision. It is not a decision.** The act is the architect's
R1–R5 of 2026-10-28 (`docs/decisions/2026-10-28-i2-and-bpo-repin-decided.md`). R2 requires the
re-pin to give an explicit old-to-new IRI mapping for all six vendored act genera, to document
the semantic comparison, and to reference the migration in the decision register. This
record does those three things; the register reference is its place here, in
`docs/decisions/`.

Prepared by Claude Code (`claude-opus-5-5`) in the re-pin pull request, on branch
`stage/bpo-repin`.

## The pin

| | Before | After |
|---|---|---|
| BPO commit | `66131945b525c54f44e4962f32bb1f52dfa0cd12` | `bc64e91839378e1926189c01bf184d6a22d5c1b7` (v0.4.1) |
| `ontology/apqc-ext.ttl` SHA-256 | `1b9a9375cb7303003556004effd712b63913d6aa4935dbf604a653aec65cab4b` | `a8119728796872a1814aace8130a32cc8e42961b0bd5feaa28b736d60a0cc6fd` |
| Namespace | `http://example.org/apqc#` | `https://fandaws.com/ontology/bpo#` |
| Prefix in this repository | `ex` | `ex`, a temporary binding for BPO's genera only (R3) |
| BPO `LICENSE` SHA-256 | `2154e0221f7e5119b2d45842fcd4be421c11c5d64a459601f2c35f53710c487a` | the same |
| `vendor/bpo/bpo-ext-bco-extract.ttl` SHA-256 | `bc2f0b861bd5dd1ded34ed7cc6e725018637178a9428c5a70e5b15d7a85995f7` | `059f01139ff5c02dcf070d8472c56854177e538015249102d353ea45ea25c4bd` |

## The IRI mapping (R2)

BPO's ADR-002 makes the move one base substitution with local names unchanged. For the six
vendored genera:

| Genus | Old IRI | New IRI |
|---|---|---|
| Act of Acquisition | `http://example.org/apqc#ActOfAcquisition` | `https://fandaws.com/ontology/bpo#ActOfAcquisition` |
| Act of Development | `http://example.org/apqc#ActOfDevelopment` | `https://fandaws.com/ontology/bpo#ActOfDevelopment` |
| Act of Improvement | `http://example.org/apqc#ActOfImprovement` | `https://fandaws.com/ontology/bpo#ActOfImprovement` |
| Act of Organizational Establishment | `http://example.org/apqc#ActOfOrganizationalEstablishment` | `https://fandaws.com/ontology/bpo#ActOfOrganizationalEstablishment` |
| Act of Remuneration | `http://example.org/apqc#ActOfRemuneration` | `https://fandaws.com/ontology/bpo#ActOfRemuneration` |
| Act of Reporting | `http://example.org/apqc#ActOfReporting` | `https://fandaws.com/ontology/bpo#ActOfReporting` |

The mapping is recorded here as documentation only. **No OWL equivalence is asserted**
between old and new IRIs: no `owl:equivalentClass`, `owl:sameAs` or similar axiom appears
anywhere in the change (counted: 0), as R2 requires.

## The semantic comparison (R2)

**Method.** The old extract (as committed before the re-pin) was parsed, its BPO IRIs were
rewritten by the base substitution, and its triples were compared with the new extract's for
each genus. The upstream source files were compared the same way: `apqc-ext.ttl` at the old
pin, with the base rewritten, against the file at `bc64e91`.

**Per genus, in the vendored extract:**

| Genus | Triples old / new | Identical | Differs |
|---|---|---|---|
| Acquisition | 5 / 5 | type, label, definition, superclass, comment | — |
| Development | 5 / 5 | type, label, definition, superclass, comment | — |
| Improvement | 5 / 5 | type, label, definition, superclass | comment |
| Organizational Establishment | 5 / 5 | type, label, definition, superclass | comment |
| Remuneration | 6 / 6 | type, label, definition, both superclasses | comment |
| Reporting | 6 / 6 | type, label, definition, both superclasses, comment | — |

- Every `rdfs:label`, `skos:definition`, `rdfs:subClassOf` and `rdf:type` triple of the six
  genera is identical under the mapping. The relevant axioms and the definitions are
  unchanged, which is R2's condition for needing no new CM-01 version.
- The three comments that differ are identical once `bpo:` is read back as `ex:`. Each changes
  one cross-reference in BPO's own prose, where v0.4.1 renamed its prefix label:
  - Improvement: `ex:ActOfImplementation` became `bpo:ActOfImplementation`;
  - Organizational Establishment: `ex:ActOfFormulation` became `bpo:ActOfFormulation`;
  - Remuneration: `ex:ActOfFinancialTransaction` became `bpo:ActOfFinancialTransaction`.
- No triple in the new extract mentions the old namespace (counted: 0).
- Over the whole upstream file, the 189 triples differ only in 14 `rdfs:comment` literals of
  that kind and in `owl:versionInfo` (0.3.0 to 0.4.1). At BPO's own re-pin target `327ea2c`,
  the file is graph-isomorphic to the old pin under the mapping, ignoring `owl:versionInfo`.
  This confirms BPO's statement in its v0.4.0 notice.
- The BFO and CCO extracts change only in their `@prefix ex:` declaration line. So do the five
  generated vocabulary Turtle files. No triple in any of them uses `ex:`.

## CM-01 (R2, R3)

- CM-01's bytes are unchanged: SHA-256 `292c8f36…1ccc` before and after.
- Its six `ex:` tokens (lines 693, 696, 697, 861 and 888) name the six genera above. Line 94
  binds `ex:` to "BPO's `ex:` act genera" in the vendored extracts, not to an IRI.
- After the re-pin those tokens expand to the new IRIs in the table above. They are the same
  BPO terms, under BPO's own mapping, with definitions and axioms unchanged.
- This is the substantive identifier migration R2 names, recorded here so that the change is
  not silent. CM-01's next reviewed version, coordinated with specification v0.5, replaces
  `ex:` with `bpo:` (R3).
- The model checker still passes:
  `ok: 1 model(s), 5 pattern(s), 6 diagram(s), 33 concept(s), 39 relationship(s), 14 CQ(s) traced`.

## No BCO class attributed to BPO's namespace (R3)

- The draft specification writes `ex:` both for BPO's terms and for terms the BCO will mint.
  Until now, `config/upstream-extracts.json` recorded the 61 spec names that no pinned file
  describes as IRIs under BPO's namespace, and the site listed them as BPO terms.
- After the re-pin, the record would have put `ex:BusinessCapability` and the spec's example
  individuals under `https://fandaws.com/ontology/bpo#`.
- So the manifest (format 2) now lists them once, as the spec writes them, attributed to no
  namespace, and the site's status page shows them the same way.
- Two tests hold this:
  - no extract's record names any of them as an IRI;
  - a recorded name with an unknown prefix is refused.

## I-1 preserved (R5)

- I-1's historical baseline stays `66131945b525c54f44e4962f32bb1f52dfa0cd12`.
- `config/inventory-sources.yaml` and every I-1 output are byte-identical to the digests in
  `docs/decisions/2026-10-27-inventory-i1-approved.md`:

| File | SHA-256, unchanged |
|---|---|
| `config/inventory-sources.yaml` | `9b6043ccc49e97654571d6ade41d67a9fb49039dfe0ce7e785664d43ebfa9a52` |
| `docs/sources/inventory/bpo-entries.yaml` | `2fd975314aa3ac839aa70ede2ec4e1dd0e78e47628d18a4878689dd5a6f5fe7b` |
| `docs/sources/inventory/bpo-findings.yaml` | `2d0278739c088fe184947f9ee2896c0ad44885ba1c7169ad808136bd73b006e7` |
| `docs/sources/inventory/NOTICE.md` | `1c56161da6e0a95a9fff228920fed8e47ce0cdc021ffcf56c420623a6d6a29de` |
| `docs/sources/inventory/README.md` | `edd8d13b213d10dcb2a253d25a002eb156efc209ca5f6312dd59762744205273` |

- `tools/inventory/harvest_bpo.py --confirm`, a fresh network harvest of the pinned files,
  reports:
  `every inventory output is byte-identical to a fresh harvest of the pinned files`.
- **The cross-check changed as R5 directs.** It now accepts two states:
  - **Before a re-pin:** the baseline is the vendored commit, namespace and bytes, as before.
  - **After a re-pin:** the vendored pin must be the inventory's own commit, and R5's record
    must name the baseline by full commit.
  
  Anything else is refused as a re-pin the inventory does not know about. Tests cover both
  states, the refusal when the record no longer names the baseline, and the refusal of a
  vendored pin that is neither.
- The generator's own digest changes with this edit. The I-1 record's digest of
  `tools/inventory/harvest_bpo.py` (`3d7f4cd2…2609`) describes the generator as reviewed at
  `ba8df1a`.

## Not done here

- The acknowledgment to BPO is drafted in this PR as
  `docs/proposals/2026-10-28-bpo-repin-acknowledgment-draft.md`, not in
  `communications/bpo/outgoing/`, which holds only messages sent. Sending it needs the
  architect's separate authorization (R4).
- The `ex:` to `bpo:` rename, and the specification's corrected use of `ex:`, belong to spec
  v0.5 and CM-01's next reviewed version (R3).
- No other BPO module is vendored.
