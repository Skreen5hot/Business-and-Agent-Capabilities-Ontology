# Decision record — Stage 05 completion record accepted; CP-1 and CP-2 closed; CAP-20 and CAP-33 encodings confirmed, 2026-11-16

Recorded verbatim by Claude Code (`claude-opus-5-5`) on 2026-11-16, from the decision the
architect, Aaron Damiano, Product Owner and Ontology Architect, gave in session after PR
#56 merged into `main` as `2a9c6b1`. The acts are the architect's. This record makes none.

## What it is about

`main` at `2a9c6b1fcb0ee7a3c494615ec65dcd534443d8ce` (PR #56 merged):

| Record | SHA-256 at `2a9c6b1` |
| --- | --- |
| `docs/proposals/2026-11-15-stage05-tranche1-completion-record.md` (the completion record accepted) | `95c65a47b67e3b6911d269cf9b77d2fd6cc358e56da8e8b36a4d81eaef0719c5` |
| `src/05_ontology/fidelity-trace-tranche-1.md` (the conceptual-fidelity trace) | `b7bb4ae1080d2e37839911c7b1cdcad9155ca06b96d99c76a4702d7eb0424295` |
| `src/05_ontology/apqc-cap.ttl` (the parent and 39 capability classes) | `3b2f8a50e204a2a2ce45039e3ef69966a873f999c4036ac2d0b54f619baa979b` |
| `src/05_ontology/apqc-cap-desc.ttl` (nine description classes, two annotation properties) | `be9fea20dece2f41a5637ae19352eea05d15606e36602652c9435e74759e7048` |
| `shapes/description_shapes.ttl` (the CAP-20 and CAP-33 encodings) | `b71aaff40e3ebec66faa277239370c8598d6376d249f1a45bb9f941f73c11f82` |
| `shapes/instance_shapes.ttl` | `c7ca715907be47446e471174f0a27bc224c5015fb163d1cd0f071c6fe5fd646b` |
| `config/completeness-manifest.schema.json` (Gate M) | `02ea3fc8b215dbc1ad8664e81f34abcd97fed50ea94d1db791fc9be968e502e2` |
| `docs/proposals/2026-11-15-stage05-description-tranche-readiness.md` | `675793811e50b5fc176dcc3c87ef2b65456c1cf44462da217249a129321bc75f` |
| `docs/standards/stage-05-ontology.md` (§7, under which the tranches are complete) | `d3eef7428a97fd05345c9710773cdad38f74962ff5958faf05b9a228e779b15f` |
| `specifications/Business-Capability-Ontology-v0.5.0-draft.3.md` (the specification in force) | `2224f869b0ec7a1e31b0afc1c2b403ad222ea290c334bff48a93ebbb6516c574` |

## The decision

> Subject: Architect Decision — Stage 05 Completion Record Accepted, CP-1 and CP-2 Closed
> I have reviewed the Stage 05 completion record merged through PR #56 at `2a9c6b1`, including its implementation evidence, tests, conceptual-fidelity trace, and stated limitations.
> DECISION: ACCEPT THE STAGE 05 COMPLETION RECORD. CP-1 AND CP-2 ARE SATISFIED FOR THE APPROVED FIRST CAPABILITY AND DESCRIPTION TRANCHES.
> The defined Stage 05 tranches are formally complete under §7 of the approved Stage 05 standard.
> 1. Formalization and Validation — ACCEPTED
> I accept the recorded implementation and validation evidence for:
>
> * The Business Capability parent and 39 admitted specific capability classes.
> * The nine description-layer information classes.
> * The two approved annotation properties.
> * The signed realization-index verification.
> * The SHACL, Gate M, ELK and HermiT checks.
> * CQ-1 through CQ-14 under their previously approved methods.
> * The conceptual-fidelity trace.
>
> The reported 834 passing tests, two pre-existing skips, and absence of skipped CAP or CQ tests are accepted as the recorded validation results.
> This acceptance applies to the exact reviewed artifacts and source baselines. It does not imply that every possible BCO capability has been formalized.
> 2. CAP-20 Encoding — CONFIRMED
> I approve `schema:ratingValue` as the Stage 05 representation of the ordinal value carried by a Capability Maturity Rating.
> The rating remains a CCO Ordinal Measurement Information Content Entity. The encoding must preserve exactly one value, an identified ordinal scale, and the Capability Assessment serving as its source.
> The use of this Schema.org property does not reclassify the information content entity as a `schema:Rating` or assert an OWL equivalence.
> No new property or class is authorized.
> 3. CAP-33 Encoding — CONFIRMED
> I approve the existing representation of the Functional Adequacy Assessment's three findings as continuant parts of the assessment, using the verified BFO parthood relation.
> Each finding remains a Descriptive Information Content Entity. Use `schema:reviewAspect` for its assessed dimension and `schema:ratingValue` for its finding of "met", "partly met" or "not met", with the required criteria, evidence and date.
> The three dimensions remain integration and coordination, operational availability, and adequacy for the function.
> This is an approved RDF/SHACL encoding convention, not an assertion that the findings are Schema.org Reviews or Ratings. Preserve that distinction in the documentation.
> No new object property, assessment subclass relationship or capability-bearing inference is authorized.
> 4. CP-1 and CP-2 — CLOSED WITH EXPLICIT SCOPE
> I accept CP-1 as satisfied using the implemented classes, constraints, reasoners and test fixtures.
> I accept CP-2 as satisfied using its approved fixture-query and review-record methods.
> The qualifications remain binding:
>
> * CAP-13 was not exercised because the current index-generation workflow does not consume `capability_scope.json`. Record it as not applicable to this tranche, not as a passing test.
> * CAP-05's union restriction check is vacuous because the tranche contains no K2 union.
> * CQ-9 and CQ-12 use the test-only coverage register.
> * CQ-11 uses the approved CAP-06 review-record method; OI-4 remains unresolved.
> * CQ-4, CQ-5 and Gate M operate on fixture evidence and manifests.
> * Gate F has not established sufficiency of real-world evidence.
> * ELK and HermiT results apply to pinned partial BFO, CCO and BPO extracts, not their complete published ontologies.
>
> These limitations do not prevent completion of the approved Stage 05 tranches. They must remain explicit in the stage-completion record and future release documentation.
> CP-3 and any broader source-coverage, migration or production-register obligations remain separately open where applicable.
> 5. Remaining Issues — NONBLOCKING
> Retain N-1 through N-9 with their recorded scopes and dependencies.
> Do not reopen the 42 G1-T admissions or alter their signed definitions and realization indexes.
> The three admitted types awaiting source checks, the Q-12 dependencies, production evidence graphs, complete upstream conformance, and any future Agent Capability formalization remain outside this acceptance.
> The upstream extract-refetch check was not exercised in CI. Preserve the verified local pin evidence and require the appropriate reproducibility check before any release or claim of full upstream conformance.
> 6. Recording and Next Stage
> Record this decision verbatim, including the two confirmed encodings and the defined limitations. Update the completion record from prepared to accepted, with its exact reviewed SHA-256 and decision reference.
> Update the roadmap, HANDOFF, development status and public site to state accurately that the first capability and description tranches of Stage 05 are complete and validated against test fixtures.
> Administrative integration is authorized after the required repository checks.
> This decision does not authorize an ontology release, production G1-I assertions, or Stage 06 knowledge-graph implementation.
> The next architectural submission should be a concise Stage 06 standard and a bounded implementation proposal that identifies the first production-data scope, evidence-quality gates, coverage-register responsibilities and upstream-conformance requirements. Do not turn that submission into another review of the already completed Stage 05 work.
> FINAL DECISION: STAGE 05 COMPLETION RECORD ACCEPTED FOR THE APPROVED TRANCHES. CP-1 AND CP-2 SATISFIED WITH RECORDED QUALIFICATIONS. CAP-20 AND CAP-33 ENCODINGS CONFIRMED. STAGE 06 IMPLEMENTATION NOT YET AUTHORIZED.

## What it authorizes, and what it does not

- **Accepts:** the completion record above. The first capability tranche and the description
  tranche of Stage 05 are complete under §7 of the Stage 05 standard, validated against
  test fixtures. CP-1 and CP-2 are satisfied with the recorded qualifications, which stay
  binding (CAP-13 not applicable to this tranche, CAP-05's union check vacuous, CQ-9 and
  CQ-12 over the test-only register, CQ-11 by review records, CQ-4, CQ-5 and Gate M over
  fixtures, Gate F not established, reasoners over partial extracts).
- **Confirms:** CAP-20's value as `schema:ratingValue`, and CAP-33's findings as BFO
  continuant parts with `schema:reviewAspect` and `schema:ratingValue`. Both are RDF/SHACL
  encoding conventions: neither types anything as a Schema.org Rating or Review nor asserts
  an equivalence.
- **Authorizes:** administrative integration of this record and the status updates after
  the repository checks.
- **Does not authorize:** an ontology release; production G1-I assertions; Stage 06
  knowledge-graph implementation; any new property or class; reopening the 42 G1-T
  admissions or their signed definitions and indexes. N-1 to N-9 stay open as recorded;
  CP-3 and the source-coverage, migration and production-register obligations stay open
  where applicable. The upstream refetch check must run before any release or claim of
  full upstream conformance.
- **Next submission:** a concise Stage 06 standard and a bounded implementation proposal
  (first production-data scope, evidence-quality gates, coverage-register
  responsibilities, upstream-conformance requirements).
