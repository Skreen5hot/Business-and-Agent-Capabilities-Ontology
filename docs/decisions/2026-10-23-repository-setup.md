# Decision record — repository setup choices, 2026-10-23

Recorded by the setup agent (Claude Code) on 2026-10-23, at the architect's answers in session.
The choices are the architect's. They were made by selecting among options the agent proposed;
the question and the selected option are quoted verbatim below, and the option's description as
it was shown is given beneath each, because the label alone does not say what was chosen.

These are **setup choices, not ratifications.** Nothing here ratifies the specification, any RP-n,
or ADR-002. Choice 5 in particular is a provisional working assumption that RP-5 will replace.

---

## The choices

**1.** *"How much of ARO's machinery should BCO start with?"* — **"Full core (Recommended)"**

> Port the generic pieces as-is: layout contract, licensing dispositions, vendored BFO/CCO
> extracts, SHACL wellformedness + baseline gate, corpus digest, the matching tests, pinned CI,
> .gitattributes, PROCESS/DEVELOPMENT/HANDOFF docs. Leave out ARO-only parts (spike/, WS-3,
> fx-seam, APQC corpus index).

**2.** *"BCO takes its act types from BPO (apqc-ext.ttl etc.). How should this repo get them?"* —
**"Vendor a pinned extract (Recommended)"**

> Add BPO as a third upstream in config/upstream-sources.yaml, pinned to a commit + sha256,
> extracted like BFO/CCO, with MIT attribution in vendor/NOTICE.md. Validation never hits the
> network.

**3.** *"How should ratification acts be recorded?"* — **"docs/decisions only (Recommended)"**

> Dated verbatim decision records like ARO's, citing the SHA-256 of what was ratified. Add the act
> tool + queue later if the volume of RP/CD items warrants it.

**4.** *"Where should BCO ontology files live and what should they be named?"* —
**"Spec §2 layout (Recommended)"**

> Follow v0.4's proposed layout: ontology/apqc-cap.ttl, ontology/apqc-cap-desc.ttl, shapes beside
> them, capabilities/*.json, docs/migration/, docs/adr/. Existing v0.1 draft stays frozen under
> drafts/ with its own non-ontology role so its defects never count as corpus defects.

**5.** *"BCO terms need a namespace before the tools can tell authored terms from vendored BPO
terms. The spec puts BCO in BPO's ex: (http://example.org/apqc#), and RP-5 says to mint a
permanent one. What should the tooling assume for now?"* — **"Provisional bco namespace
(Recommended)"**

> Use https://fandaws.com/ontology/bco# (ARO's fandaws.com pattern), recorded as provisional
> pending RP-5. Authored and vendored terms stay separable by IRI, so ARO's validate and
> vendoring logic carry over unchanged.

**6.** *"Which CCO release should BCO pin?"* — **"v2.0 (2024-11-06) (Recommended)"**

> Matches BPO's pin and the spec's dependency table (CCO 2.0), so BPO act genera anchor to the
> same CCO IRIs this repo vendors. Closes part of OI-1.

**7.** *"With no BCO terms written yet, the vendored extracts would be almost empty. Should
vendoring also take its seed terms from the v0.4 spec's cco:/obo:/ex: references?"* —
**"Yes, seed from the spec (Recommended)"**

> Vendor the 27 BFO/CCO terms the spec cites, plus the BPO terms it cites, now. Spec ex: terms
> that BPO does not define (the ones BCO will mint) are listed in the manifest instead of
> refused.

Earlier in the same session the architect also directed: *"Commit the import to main and remove
BACO_spec_v0.4.md since it duplicates specifications/…v0.4.0-draft.1.md. Don't push yet."*
(commit `b4d4493`), and chose to keep the setup on the checked-out branch, `main`, rather than a
new branch.

---

## What they rest on

| item | where | digest / commit |
|---|---|---|
| BCO spec v0.4.0-draft.1 | `specifications/Business-Capability-Ontology-v0.4.0-draft.1.md` | `c55fb36c…8f9f` (as imported, `b4d4493`) |
| ARO, the setup carried from | github.com/Skreen5hot/ApplicationRequirementOntology | `733538a` |
| BPO, the vendored upstream | github.com/Skreen5hot/BusinessProcessOntology | `66131945b525c54f44e4962f32bb1f52dfa0cd12` |
| CCO v2.0-2024-11-06 | CommonCoreOntologies, `src/cco-merged/CommonCoreOntologiesMerged.ttl` | commit `510dad76be0ef710b65a421075af912af25342b7`; file `e609db27…fe5b` |

The CCO commit is the target of the `v2.0-2024-11-06` tag, resolved through the GitHub API. The
pins in `config/upstream-sources.yaml` are the authority; this table only points at them.

## Measured when they were applied

- Every `cco:` (21) and `obo:` (6) term the spec names is described by the pinned CCO v2.0 and BFO
  files. None is unresolved.
- 6 `ex:` terms the spec names are BPO act genera in `apqc-ext.ttl` and are vendored. 61 are not
  described by any pinned file; they are listed in `config/upstream-extracts.json`.
- CCO v2.0 places Organization Capability (`cco:ont00000568`) under realizable entity
  (`obo:BFO_0000017`), not under disposition (`obo:BFO_0000016`). CD3's explicit
  `rdfs:subClassOf obo:BFO_0000016` is therefore the BCO's own assertion, not one CCO supplies.
  `tests/test_upstream_vendoring.py` pins this.

## Effect

The repository is set up on ARO's method, with the BCO-specific changes described in
`docs/DEVELOPMENT.md`. No ontology term exists yet. The next decisions in the spec's own order
are RP-1, then RP-2 and RP-3 (spec §9, §10), then ADR-002; RP-5 replaces choice 5.
