# Decision record — Inventory I-2 (E1–E7) and the BPO re-pin (R1–R5), 2026-10-28

Recorded verbatim by Claude Code (`claude-opus-5-5`) on 2026-10-28, at the statement the
product owner and architect, Aaron Damiano, made in session. The act is his.

**What it is about:** the two proposals in pull request #14, as committed at
`0a763b15003d78172ef611d29ef630f62b4c4d0f`:

| Proposal | SHA-256 (LF bytes at `0a763b1`) | Decisions |
|---|---|---|
| `docs/proposals/2026-10-28-bpo-repin.md` | `8856203c75185883b16ed342b5f8fdd78def3e5e8ff411060216c54b99e543be` | R1–R5 (part A below) |
| `docs/proposals/2026-10-28-inventory-i2-public-catalogs.md` | `839707f48c500b96f54b24c1e41561686012323a931eab9f8571359266f0c747` | E1–E7 (part B below) |

This record is committed to the same pull request, so the decision and the proposals it
decides travel together.

---

````text
# Architect Decision — Inventory I-2 and BPO Re-pin Proposals

**Reference:** PR #14, proposals dated October 28, 2026.

I approve the direction of both proposals, subject to the conditions below.

## A. BPO Re-pin — R1–R5

**R1 — Approved: Option B.**

Re-pin the vendored BPO extract to commit `bc64e91839378e1926189c01bf184d6a22d5c1b7`, using the namespace `https://fandaws.com/ontology/bpo#`.

**R2 — Approved with a governance qualification.**

The namespace migration changes the full IRIs of the referenced BPO entities. This is a substantive identifier migration, but not a change to CM-01's accepted conceptual categories or relationships, provided the reported definitions and relevant axioms remain unchanged.

A new CM-01 version is not required solely for this controlled re-pin. However, the implementation PR must include an explicit old-to-new IRI mapping for all six vendored act genera, document the semantic comparison, and reference the migration in the decision register.

Do not silently change the interpretation of approved references or automatically generate OWL equivalence assertions.

**R3 — Approved.**

Retain `ex:` as a temporary prefix binding for the vendored BPO genera. Replace it with `bpo:` in a reviewed CM-01 update coordinated with specification v0.5.

The current specification's double use of `ex:` for BPO and proposed BCO terms must be corrected. The temporary binding must not attribute BCO classes to the BPO namespace.

**R4 — Approved for drafting.**

Prepare an acknowledgment to BPO after the re-pin is completed and validated. Sending the communication remains a separate action requiring my authorization.

**R5 — Approved.**

Preserve Inventory I-1's historical baseline commit `66131945b525c54f44e4962f32bb1f52dfa0cd12` and all approved inventory outputs unchanged.

Modify the cross-check to distinguish the original reviewed baseline from the current vendored BPO pin. Demonstrate unchanged I-1 output hashes and successful validation in the re-pin PR.

## B. Inventory I-2 — E1–E7

**E1 — Approved.**

Divide I-2 into independently reviewed PRs: I-2a Rights, I-2b APQC PCF, and I-2c Federal Catalogs.

**E2 — Approved with conditions.**

I-2a must evaluate the actual APQC terms and attribution requirements for each edition. No additional source names, descriptions, or substantial catalog structures may be publicly redistributed before the relevant rights are established and approved.

If the terms are ambiguous, prepare a request for written clarification from APQC for separate authorization.

**E3 — Approved.**

I will obtain the PCF 8.0 source under an appropriate APQC registration if needed. Its absence must not block I-2a or the independently executable parts of I-2b. Do not commit the downloaded source unless its terms permit redistribution.

**E4 — Approved: Option A.**

Evaluate each proposed level-3 standing function against CM-01's accepted definition. Record the reason, independent evidence and source locator. Submit the candidate list for my explicit approval.

No candidate is automatically admitted as a BCO Capability Type.

**E5 — Approved with qualification.**

Include FIBF functions, activities and source-defined Business Capability entries in separate inventory files. Enumerate and pin the exact source documents and editions included in the harvest snapshot.

Retain the distinction between FIBF's outcome-based business needs and BCO's organization-borne dispositions. Do not automatically equate or exclude individual entries without review.

**E6 — Approved with updated source evidence.**

Require primary-source material for FEAF-II BRM. An official OMB archive lists BRM version 3.1 and its taxonomy, both dated May 15, 2013.

Retrieve and validate the primary documents, pin their digests, and confirm the applicable redistribution rights before harvesting. If retrieval or verification fails, record the gap and defer that source rather than using secondary transcriptions.

**E7 — Conditionally approved.**

After I-2a establishes the applicable rights, lifting APQC-related withholding in I-1 requires a separate reviewed PR. The original I-1 approval and historical outputs must remain traceable.

## C. Authorization and boundaries

These decisions authorize the two proposed workstreams, but execution remains subject to the established PR review sequence.

Proceed first with the BPO re-pin PR and I-2a rights review. Neither is permission to publish additional restricted catalog material.

No inventory process may mint vocabulary concepts, OWL classes, object properties, subclass axioms or type-admission results.

CM-01 remains the approved conceptual baseline. Its future version must incorporate the explicit BPO prefix correction through the normal review procedure.

Record the decisions above in `docs/decisions/`, preserving their relation to the two proposals in PR #14.

I-3, I-4 and I-5 are not authorized by these decisions.
````

---

## Effect

**BPO re-pin (part A):**

- **Authorized:** a re-pin PR to BPO `bc64e91`, namespace `https://fandaws.com/ontology/bpo#`.
  That PR must:
  - give the old-to-new IRI mapping for all six vendored act genera;
  - document the semantic comparison (definitions and relevant axioms unchanged);
  - reference this migration in the decision register.
- **No OWL equivalence assertions** are generated between old and new IRIs.
- **`ex:` stays a temporary binding**, for the vendored BPO genera only.
  - `bpo:` replaces it in a reviewed CM-01 update coordinated with specification v0.5.
  - That update also corrects the specification's use of `ex:` for proposed BCO terms.
  - Until then, the binding must not attribute BCO classes to BPO's namespace.
- **CM-01 needs no new version** solely for this re-pin, and stays the approved baseline.
- **I-1 stays as reviewed.**
  - The historical baseline `66131945` and every approved I-1 output stay unchanged.
  - The cross-check distinguishes the reviewed baseline from the current vendored pin.
  - The re-pin PR shows the I-1 output hashes unchanged.
- **A BPO acknowledgment** is drafted once the re-pin is validated. Sending it needs a
  separate authorization.

**Inventory I-2 (part B):**

- **Split into three PRs**, each reviewed: I-2a rights, I-2b APQC PCF, I-2c federal
  catalogs. I-2a comes first; I-2b and I-2c follow after review.
- **APQC (E2):**
  - I-2a evaluates the actual terms and attribution requirements per edition.
  - Nothing further is redistributed before the rights are established and approved.
  - If the terms are ambiguous, a request to APQC is prepared for separate authorization.
- **PCF 8.0 (E3):** the architect obtains it if needed. Its absence does not block I-2a or
  the parts of I-2b that can run without it, and it is not committed unless its terms
  permit.
- **Level-3 standing functions (E4):**
  - Each candidate is evaluated against CM-01's definition, with a reason, independent
    evidence and a source locator.
  - The list goes to the architect for explicit approval.
  - No candidate is admitted as a Capability Type.
- **FIBF (E5):**
  - Functions, activities and Business Capability entries go in separate files, from
    enumerated, pinned documents and editions.
  - FIBF's outcome-based needs stay distinct from BCO's organization-borne dispositions.
  - No entry is equated or excluded without review.
- **FEAF-II BRM (E6):**
  - Primary documents only: BRM 3.1 and its taxonomy, both dated 15 May 2013, per the OMB
    archive the architect cites.
  - They are retrieved, validated, pinned by digest, and their rights confirmed before any
    harvest.
  - If that fails, the gap is recorded and the source deferred.
- **Lifting I-1's APQC withholding (E7):** only after I-2a, in a separate reviewed PR, with
  the I-1 approval and historical outputs kept traceable.

**Boundaries (part C):**

- The re-pin PR and the I-2a rights review come first.
- Neither permits publishing further restricted catalog material.
- No inventory process mints vocabulary concepts, OWL classes, object properties, subclass
  axioms or type-admission results.
- I-3, I-4 and I-5 are not authorized.

## What this does not do

- It performs neither workstream; each arrives as its own pull request for review.
- It sends nothing to BPO or to APQC.
- It changes no CM-01 text and no I-1 output.
