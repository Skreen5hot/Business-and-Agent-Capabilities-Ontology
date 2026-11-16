# Decision record — Stage 06 standard and register-first increment approved with binding directions, 2026-11-16

Recorded verbatim by Claude Code (`claude-opus-5-5`) on 2026-11-16, from the decision the
architect, Aaron Damiano, Product Owner and Ontology Architect, gave in session on the
local branch `stage06/proposal` at `ed5780a`. The acts are the architect's. This record
makes none.

## What it is about

`stage06/proposal` at `ed5780afc2fe9b99bceb5768ddcdecbf044c5f66`, branched from `main` at
`2a9c6b1` (before PR #57 merged; the branch is rebased onto `6d47055` for its PR, which
changes no reviewed file):

| Record | SHA-256 at `ed5780a` |
| --- | --- |
| `docs/proposals/2026-11-16-stage-06-knowledge-graph-standard.md` (the proposed standard) | `2a26eed2d371a919f1fed5e5674fcdc601513b43d2c3fcb02f44f97b50be1e43` |
| `docs/proposals/2026-11-16-stage06-first-increment-proposal.md` (the first-increment proposal, K-1 to K-6) | `509a25c7eeb1b5b40d7ecb701279282653f9875e4f83b24cbc2f35128fe6687f` |
| `specifications/Business-Capability-Ontology-v0.5.0-draft.3.md` (the specification in force) | `2224f869b0ec7a1e31b0afc1c2b403ad222ea290c334bff48a93ebbb6516c574` |

## The decision

> Subject: Architect Decision — Stage 06 Standard and First Knowledge-Graph Increment
> I have reviewed the reported Stage 06 proposal at local commit `ed5780a`.
> Decision: APPROVE THE REGISTER-FIRST ARCHITECTURE AND ITS BOUNDED INITIAL SCOPE, WITH THE FOLLOWING BINDING DIRECTIONS.
> These directions resolve the architectural questions in your report. Because the branch is still local, final ratification of the exact standard text is conditional on its published PR matching these decisions.
> A. Stage 06 Standard
> Approve the reported separation among:
>
> 1. Register and migration data.
> 2. Organization-specific evidence.
> 3. Derived query answers, which must not be written back as source assertions.
>
> Retain K1–K9 and the proposed executable checks, subject to the clarifications below.
> A signed G1-I assessment is required before asserting organizational capability possession. G1-T admission alone does not establish possession.
> Every assessment must retain its criteria, source evidence, date, reviewer and finding. Missing data cannot be interpreted automatically as an adverse finding.
> Test and production evidence must remain isolated.
> B. First Increment — APPROVED
> Authorize implementation of the bounded register-first increment:
>
> * Audit the 41 BPO capability-scope entries at the approved source pin.
> * Build the initial coverage register for standing functions whose proposed component types are among the 39 implemented specific capability classes.
> * Prepare the `bc:` migration manifest.
> * Implement and execute the upstream refetch and complete-pinned-BFO/CCO reasoning checks.
>
> The scope audit must distinguish what BPO actually declares from what BCO independently accepts. Do not automatically admit a BPO capability type, change its classification or create an OWL subclass assertion from the audit.
> The migration manifest must distinguish exact identifier migration from semantic equivalence. Do not create `owl:sameAs`, `owl:equivalentClass` or replacement IRIs without justified and separately approved semantics.
> C. OI-13 — DECIDED
> For coverage-register version 1, component requirements will reference capability types represented by approved class IRIs.
> Do not mix capability individuals, functional units, act types or APQC process nodes into that component field.
> A standing function's component list does not imply that an organization possesses those capabilities, nor that possession establishes integration, availability or whole-function adequacy.
> Any future extension of the component model requires its own semantic justification.
> D. Coverage Register Approval — BATCH APPROVAL
> Do not require me to approve every register entry separately.
> Prepare one coherent register batch with source evidence, reviewed component relationships, proposed function identifiers, rights status and test results.
> Use a separate synthetic domain review for the batch under the project's accepted process.
> Submit only substantive semantic disputes and the consolidated batch for architectural acceptance.
> This preserves accountability without creating a new governance cycle for every function.
> E. APQC Rights — CONSERVATIVE APPROACH APPROVED
> The first increment may use validated, permitted identifiers and mappings needed for the register.
> Do not publish APQC names, definitions, proprietary hierarchy descriptions or reconstructed catalog content merely because their identifiers are available.
> Verify the rights basis for the specific identifiers and relationships before distributing them. If their public redistribution is not established, keep the relevant register material private or withheld.
> An attribution notice does not substitute for permission.
> Do not block the independent upstream conformance checks while resolving a particular register entry's rights status.
> F. Namespace Decision
> Do not mint real organization or individual IRIs in any of the existing ontology term namespaces merely to avoid a new namespace decision.
> A separate instance-data namespace will be required before the first real organization evidence graph is created. Reserve that decision for the second increment, when the organization and publication rights are known.
> The standard must clearly distinguish ontology-term IRIs, externally reused IRIs and new instance-data IRIs.
> The first register increment must use only identifiers whose creation or reuse is already authorized. Escalate a genuine register-identifier namespace requirement before minting new terms.
> G. Upstream Conformance — APPROVED WITH A PRECISE CLAIM
> Require the upstream refetch job to execute successfully in an auditable workflow, verifying the pinned files and digests.
> Require HermiT consistency checking with the BCO module and the complete pinned BFO and CCO dependencies needed for that check.
> Record the actual ontology closure loaded and the reasoner results.
> Do not claim full BPO conformance because the ratified import boundary excludes BPO modules with incompatible capability assertions.
> Report any such limitation explicitly rather than weakening the boundary or disabling a failing check.
> H. K-6 — STAGE 06 COMPLETION RULE
> CP-3 is necessary but not sufficient for overall Stage 06 completion.
> CP-3 may close once the coverage register, audit, migration responsibilities and required checks satisfy their acceptance criteria.
> However, final Stage 06 completion additionally requires at least one real organization evidence graph with:
>
> * An identified organization and approved instance namespace.
> * Evidence whose use and disclosure are authorized.
> * Any required consent or privacy safeguards.
> * A named assessor and reviewer.
> * At least one signed G1-I decision supported by dated, sourced evidence.
> * Successful applicable validation and competency-query execution.
>
> A negative or partial finding is permissible if genuinely supported; do not manufacture a PASS merely to satisfy the stage.
> If no suitable evidence can lawfully be obtained, Stage 06 remains partially complete. A fictional organization or synthetic fixture cannot substitute for production evidence.
> Amend the proposed completion rule accordingly.
> I. Second Increment — NOT YET AUTHORIZED
> Do not begin real organization evidence collection or G1-I assertion until its scope is specifically approved.
> The following must be decided for that increment: organization, data rights, consent/privacy requirements, instance namespace, assessor and reviewer.
> Do not invent these details or use confidential information in the public repository by default.
> J. Integration and Next Deliverable
> You may push `stage06/proposal` and open a PR containing the standard and the bounded implementation proposal.
> Align the actual K-1 through K-6 decision entries with this direction, and identify any wording that conflicts with it.
> Once the corrected standard and implementation scope are confirmed in the PR, the register-first implementation is authorized. Do not start the real evidence increment.
> After required CI, integrate the accepted standard and proceed with the bounded register work without another broad planning exercise.
> Return the first completed coverage-register batch, the 41-entry audit, the migration manifest and the actual upstream-check results.
> Final direction: Proceed toward CP-3 through real register implementation, but do not close Stage 06 until an actual, authorized organizational evidence graph has been validated.

## What it authorizes, and what it does not

- **Approves:** the register-first architecture, with directions A to J binding. Ratifying
  the exact standard text depends on the published PR matching them. The standard and the
  proposal are amended to do so, and each place where the reviewed text conflicted with them
  is listed in the proposal's section 8.
- **Authorizes, once the PR matches:** integrating the standard, then the register-first
  increment:
  - the audit of the 41 scope entries;
  - a first coverage-register batch, accepted as one batch after a synthetic domain review;
  - the `bc:` migration manifest;
  - the upstream refetch and the complete-BFO/CCO HermiT checks, both run.
- **Decides:**
  - OI-13 for register version 1 (D-C): components are approved capability class IRIs only.
  - K-6 (D-H): CP-3 is necessary but not sufficient. Final Stage 06 completion needs one
    real, authorized organization evidence graph. No synthetic substitute counts.
- **Does not authorize:**
  - the second increment, meaning real evidence collection or G1-I assertions;
  - an instance namespace;
  - publishing APQC names, definitions or hierarchy;
  - any `owl:sameAs`, `owl:equivalentClass` or replacement IRI without separately
    approved semantics;
  - a claim of full BPO conformance;
  - a release.
