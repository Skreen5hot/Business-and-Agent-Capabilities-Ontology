# Decision record — D6 class-only increment accepted for integration; CP-1 and CP-2 kept open, 2026-11-15

Recorded verbatim by Claude Code (`claude-opus-5-5`) on 2026-11-15, from the decision the
architect, Aaron Damiano, Product Owner and Ontology Architect, gave in session on local
commit `3564d2b`. The acts are the architect's. This record makes none.

## What it is about

Branch `d6/tranche-1`, commit `3564d2bb2431c2f2ccbe95d848904f6d1c42d165`:

| Record | SHA-256 at `3564d2b` |
| --- | --- |
| `src/05_ontology/apqc-cap.ttl` (the 40 classes, A) | `3b2f8a50e204a2a2ce45039e3ef69966a873f999c4036ac2d0b54f619baa979b` |
| `src/05_ontology/tranche-1.yaml` (the tranche record) | `a433ded84078b638b033d6651c31306347d0db035fe9c0877d5715c6b31ea0b6` |
| `vendor/bpo/bpo-ext-bco-extract.ttl` (the APQC-derived labels, F) | `e4db134f3f7dfc67b4ba24c53b47c16f5b876f4e18ff5003f855de7cb94443ef` |
| `site/content/site.json` (the notice, E) | `f7a74ec9b62aa3084c8590a726daec3d88ca4e50a04e5cc2ed0a4e2ce84b961b` |
| `tools/ontology/formalize.py` | `8353966c7878aaf31e918b6d6924217cd3245300150a470b76f3ef1d0e467f6d` |
| `tools/ontology/reason.py` | `cdd3cac85861e91ab71e38c58377cbf740fdbe493dd671f5c78615dfc428737e` |
| `shapes/stage05_shapes.ttl` | `3aeeda48faa49961743300a112ba4b94996721408e24f97eca25c550bbf63e72` |

## The decision

> Subject: Architect Decision — D6 Class Formalization, CP-1/CP-2, and Repository Integration
> I have reviewed your report on the first Stage 05 formalization tranche, local commit `3564d2b`.
> Decision: ACCEPT THE CLASS-ONLY IMPLEMENTATION AS A D6 DEVELOPMENT INCREMENT. AUTHORIZE ITS PR AND CONTINUE THE REQUIRED VALIDATION.
> This is the substantive ontology implementation we have been working toward. I want to preserve the progress without prematurely declaring the remaining checkpoints complete.
> A. D6 Implementation — Accepted for Integration
> I accept the reported implementation scope:
>
> * 40 OWL classes: the generic `bco:BusinessCapability` parent and 39 signed G1-T-admitted specific types.
> * 39 realization indexes containing 160 `bpo:enablesProcess` annotation assertions across 147 distinct indexed BPO act types.
> * Validation against signed admission records and source digests.
> * Eleven exercised SHACL constraints with negative fixtures.
> * Successful ELK and HermiT checks against the pinned partial extracts.
>
> The validation evidence supports advancing the implementation, but it does not establish full consistency with the published BFO, CCO and BPO ontologies.
> Preserve that qualification in the formalization report.
> B. Repository Integration — Authorized
> You may push `d6/tranche-1`, open a PR and integrate it after:
>
> 1. All required CI checks pass on the final reviewed changes.
> 2. The public-site notice is corrected.
> 3. APQC-derived label attribution and publication permissions are verified.
> 4. The PR clearly identifies CP-1 and CP-2 as incomplete.
> 5. The final diff contains no unauthorized ontology classes, object properties or changes to signed G1-T definitions and indexes.
>
> The PR may be merged as a class-only Stage 05 implementation increment. Its merge does not constitute final Stage 05 completion or ontology release.
> No additional approval is needed for faithful implementation of these conditions.
> C. CP-1 — Keep Open; Complete the Missing Evidence
> Do not waive or redefine CP-1.
> The class-formalization portion has been implemented and tested. Complete the remaining requirements using a bounded synthetic validation dataset.
> I authorize creating test-only individuals for the required positive and negative fixtures, including:
>
> * Organizations and their member agents.
> * Capability-bearing and material-basis assertions.
> * Planned Acts, their performers and realization assertions.
> * Capability Assessments and supporting evidence.
> * Authorization, sourcing and functional-adequacy examples where required.
>
> Exercise the applicable CAP-21 and CAP-25–35 rules and Gates C-A, G and M.
> Use existing verified BFO/CCO relations. Consult the Extended Relation Ontology first when selecting relations.
> If a missing encoding genuinely requires a new ontology term or changes approved conceptual meaning, isolate that issue for my decision rather than silently adding a term.
> These test fixtures are not production capability claims and do not constitute Stage 06 implementation.
> D. CP-2 — Keep Open; Complete the Competency Questions
> The reported ELK and HermiT results are accepted as partial CP-2 evidence.
> Complete the remaining checkpoint by demonstrating CQ-1 through CQ-14 over one or more controlled fixture organizations, including CAP-18's positive and negative authorization-evidence cases.
> Every competency question must produce the expected answer from actual test data.
> A missing relation, unavailable encoding or unsupported query must be reported explicitly, not counted as passing.
> Do not create a new production knowledge-graph framework to accomplish this.
> E. Public-Site Notice — Replacement Approved
> Replace the outdated notice with:
> "The Business Capability Ontology is under development and has not been released. Its v0.5 specification commitments were ratified under CP-0. Forty-two specific Business Capability types have passed G1-T admission. Thirty-nine of those types, together with the generic Business Capability parent, are implemented as OWL classes in the first Stage 05 tranche. The implementation has passed its reported class-level validation against pinned partial ontology extracts. Instance-level validation, CP-1/CP-2 completion, and full upstream ontology conformance remain outstanding. No production knowledge graph or ontology release has been approved."
> Ensure this status becomes public when the implementation PR merges.
> F. APQC-Derived Labels — Attribution Required
> The BPO extract contains act labels derived from APQC PCF element names.
> Do not rely solely on the fact that the existing PCF notice gate passes.
> Ensure the generated extract and applicable repository notices clearly identify the APQC-derived material, its source and the governing attribution.
> Verify that existing rights approvals permit publication of those labels in the extract. A notice does not itself establish redistribution rights.
> If the labels cannot be published under the approved rights conditions, omit the affected labels from the distributed extract while preserving permissible act identifiers and validation functionality.
> Do not unnecessarily expand the extract or import APQC source descriptions.
> G. Ontological Conformance — Preserve the Limits of Evidence
> The current reasoner results concern the vendored partial BFO, CCO and BPO extracts.
> Because those extracts omit anonymous class expressions, these results do not prove consistency with the complete published ontologies.
> Before claiming full upstream conformance, perform a separate check against the complete pinned dependencies or provide an approved, accurately scoped conformance assessment.
> This does not prevent integration of the class-only increment. It limits the claims that may be made about it.
> H. Remaining Formalization Deliverables
> Complete the conceptual-fidelity trace for the 40 classes, connecting their formal definitions, parentage and realization indexes to the approved CM-01 and signed G1-T baselines.
> After the remaining applicable CP-1 and CP-2 validation evidence is complete, prepare the Stage Completion Record with the precise pass/fail results, unresolved issues, source pins and artifact digests.
> Do not mark Stage 05 complete merely because the class-only PR merges.
> I. Immediate Next Actions
> Proceed in this order:
>
> 1. Correct the site notice and APQC attribution.
> 2. Push and integrate the D6 class-only implementation after CI.
> 3. Build the minimal synthetic instance fixtures.
> 4. Complete CP-1 and CP-2 validation.
> 5. Complete the conceptual-fidelity trace.
> 6. Return the Stage Completion Record for final acceptance.
>
> Do not reopen CP-0, D5, or the 42 signed G1-T admissions. Do not begin Stage 06 or expand the tooling into another development project.
> Our immediate objective is to finish validating the ontology classes that now exist, not to create another planning or governance cycle.
> Final disposition: First D6 class-formalization increment accepted for integration; CP-1 and CP-2 remain open; test-fixture development authorized; final Stage 05 acceptance reserved.

## Verification under F: may the labels be published?

The governing approval is the APQC decision of 2026-10-29
(`docs/decisions/2026-10-29-apqc-pcf-sourcing-decided.md`), sections 3 and 4, and its
"Effect":

- PCF element IDs, hierarchy IDs, names and descriptions may be published if they are
  "taken from BPO at a pinned commit that carries BPO's `NOTICE.md`";
- APQC's notice travels with them;
- a check refuses an artifact that lacks it.

The BPO pin the extract is built from is `bc64e91` (v0.4.1). The approval names `2e55edd`
"or later". Measured on 2026-11-15 with the GitHub API:

- `bc64e91` is **3 commits behind** `2e55edd`;
- `NOTICE.md` **does not exist** at `bc64e91`.

The first condition therefore fails for anything taken from `bc64e91`.

The inventory's rights rule says what counts as PCF material on an act
(`docs/sources/inventory/README.md`, "The rights rule"): every literal of a class whose
local name is `P<digits>`. That covers its label, definition, comment and example. The
same README treats BPO IRIs that embed PCF element IDs as identifiers, not catalog data.

**Result: the labels cannot be published from this pin.** As F directs, the extract
omits them. From the two slice files it takes only each act class's `rdf:type` and
`rdfs:subClassOf`. This keeps the act identifiers and everything validation walks: the
declaration and the ancestry to Planned Act. The extract's header and
`vendor/NOTICE.md` say that the act IRIs embed APQC PCF element IDs, where they come
from, why the act names and descriptions are absent, and where APQC's notice is
(`NOTICE.md`). Re-pinning BPO to a commit that carries its `NOTICE.md` would make the
names publishable; that is a repin, which is its own reviewed change and is not done
here.
