# Decision record — I-5 proceeds: PR #35 merged, BRM Payroll confirmed as a designation, the AP hold lifted, 2026-11-04

Recorded verbatim by Claude Code (`claude-opus-5-5`) on 2026-11-04, from the decision the
architect, Aaron Damiano, gave in session. The acts are the architect's.

**What it is about:** pull request #35 (the Candidate Capability Catalog, head `9854052`),
and the tranche 1 readiness record, `docs/catalog/tranche-1.md` revision 2 (SHA-256
`f6fc550aa90d736aa8b372a07f1959c386dd0884404d8d2986e055a8f42ec6da`), committed as `b7930e7`
and, after the rebase this decision directs, as `35c85ea`, with the same content. It
answers the two questions that record left open: BRM Payroll's equivalence, and T1-03's
hold.

## The decision

````text
I-5 Decision: Proceed
1. PR #35 — MERGE AUTHORIZED
Merge PR #35 into main.
The catalog's checks are green, the generator defects have been corrected, and the outstanding admission decisions are appropriately separated from catalog generation.
After merging:

* Rebase PR #36 onto main.
* Preserve the approved I-5 tranche decisions and evidence exclusions.
* Run the required checks again.
* Keep all three candidates unadmitted until the admission test is ratified.

No additional harvesting or catalog expansion is authorized.
2. BRM Payroll equivalence — CONFIRMED
Treat BRM Payroll (BCC-b7c46718) and Payroll Processing (BCC-d95f68fd) as designations of the same candidate capability.
The shorter BRM definition does not establish a conflicting boundary. Administering employee compensation reasonably includes determining pay, applying deductions, disbursing compensation, and handling associated payroll taxes. These functions are also reflected in federal payroll process documentation.
CiteSeerX

Authorize the following:

* Retain BCC-d95f68fd as the canonical candidate.
* Retire BCC-b7c46718 as a separate active candidate, preserving both BRM source records and their provenance.
* Record BRM Payroll as an alternative designation, not a new capability type.
* Preserve the distinction between payroll tax operations and broader tax planning or general business tax preparation.
* Do not assert `owl:equivalentClass` or create new object properties.

This is a candidate identity decision, not admission into OWL.
3. Accounts Payable Processing — HOLD LIFTED
I accept the revised seven-act realization index for evaluation.
The exclusions are justified, the remaining acts represent operational payables work, and the approval/authorization distinction is preserved. The revised readiness record documents the evidence.
GitHub

T1-03 may now proceed alongside T1-01 and T1-02.
Next milestone
With these decisions resolved, all three candidates can advance to the ratified admission test.
Priority: D4 — ratify G1-T.
Do not expand the tranche, generate OWL classes, or introduce new object properties.
Merge PR #35, update PR #36 with these decisions, rerun the required checks, and advance to admission-test ratification.
````

The words "CiteSeerX" and "GitHub" stand in the decision as given, where it cited sources.
The federal payroll documentation behind "CiteSeerX" is not named and is not in this
repository's register; the equivalence rests on the architect's act, not on that source.

## The acts it contains

1. **PR #35 is merged** into main, and PR #36 is rebased onto main. The tranche decisions
   and evidence exclusions of 2026-11-04 are preserved, and the required checks are run again.
2. **BRM Payroll and Payroll Processing are designations of one candidate capability.**
   BCC-d95f68fd is canonical. BCC-b7c46718 is retired as a separate active candidate, and
   both BRM source records (INV-FEAF-BRM-SCD-624-brm-service,
   INV-FEAF-BRM-TAX-B10.805.624-brm-service) keep their provenance. BRM Payroll is an
   alternative designation, not a new type.
3. **Payroll tax operations stay distinct** from tax planning and from general business
   tax preparation.
4. **No `owl:equivalentClass`** and no new object property. This is a candidate identity
   decision, not admission into OWL.
5. **T1-03's hold is lifted.** The seven-act realization index is accepted for evaluation,
   and T1-03 proceeds with T1-01 and T1-02.
6. **Next milestone: D4, ratifying G1-T.** All three candidates stay unadmitted until then.
7. **Excluded:** further harvesting, catalog expansion, expanding the tranche, OWL classes,
   new object properties.

## How it was carried out

- PR #35 was merged with a merge commit, `36b9d6c`, whose tree is `9854052`'s.
- PR #36 was rebased onto it and retargeted to main. The rebase rewrote its two commits:
  `f320a67` is now `1948237` and `b7930e7` is now `35c85ea`, with the same content. The
  records that named the old commits name both.
- `docs/catalog/tranche-1.md` revision 3 records acts 2, 3 and 5. The generated catalog is
  not edited: it still lists BCC-b7c46718, because it is regenerated from the inventories.
  The retirement is recorded in the tranche record, against the pinned catalog digest.

## What it does not do

It admits, ratifies or mints nothing, and it does not ratify G1-T. CM-01, DP-1, DP-2 and the
specification are unchanged.
