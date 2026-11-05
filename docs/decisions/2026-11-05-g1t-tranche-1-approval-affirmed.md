# Decision record — G1-T tranche 1 approval affirmed by the reviewer, 2026-11-05

Recorded verbatim by Claude Code (`claude-opus-5-5`) on 2026-11-05, from what the
architect and named reviewer, Aaron Damiano, wrote in session. The act is his.

**What it is about:** the confirmation recorded at `15ac666`
(`docs/decisions/2026-11-05-g1t-tranche-1-signed.md`), which the provenance correction of
the same day (`docs/decisions/2026-11-05-g1t-approval-provenance-corrected.md`) withdrew as
an AI recommendation, pending "explicit, independently attributable approval from Aaron".
That confirmation was given against the three G1-T records as committed at `7515f44`, the
version presented for review:

| Record | SHA-256 at `7515f44` |
|---|---|
| `docs/catalog/admission/G1T-T1-01-customer-complaint-management.md` | `7950cce7d363088045f2c8484c1d0ee901b0d4867f3c5e3ac554cd0280665b81` |
| `docs/catalog/admission/G1T-T1-02-payroll-processing.md` | `f41e29cc40df6ed4ef84064bb40677cedc7aff7f4003c2977f7150164a87cee4` |
| `docs/catalog/admission/G1T-T1-03-accounts-payable-processing.md` | `b49935b79b4046d34d84080f46b5e1bff17f5e277d3aab5b607a343c20594c2d` |

## The affirmation

After being asked for a new approval that named each record, its finding and its version,
the reviewer wrote, in his own words:

````text
I already appoved these
````

## The act it contains

The confirmation of 2026-11-05 recorded at `15ac666` is the reviewer's own approval:
**T1-01, T1-02 and T1-03, PASS**, each with the note recorded there. This is the
"explicit, independently attributable approval from Aaron" that the provenance correction
names as the condition for restoring the signature. Its date is 2026-11-05.

## How it was carried out

- **Reviewed version.** The affirmation names no digest. It is bound to the records at
  `7515f44`, the version the confirmation was given against. Between `7515f44` and the
  current head, the records' status rows, confirmation tables and withdrawn-row notes
  changed. Their class, index, five answers and worked cases did not. If the reviewer
  meant another version, the correction is a new record.
- **The records.** Each status is "Signed: PASS". Each confirmation table holds the row
  `15ac666` wrote, reinstated. Each withdrawn-row note is replaced by a pointer to this
  record.
- **Notices.** The supersession notice on the `15ac666` record now also says the signature
  is reinstated. The provenance correction is kept unchanged, as history.

## What it does not do

A PASS licenses asserting each class under `obo:BFO_0000016`, and so under
`bco:BusinessCapability`, for that class only (CAP-04). It asserts nothing yet: no class is
minted or asserted in OWL before all of CP-0 and D5. It licenses no organization's claim to
bear any of these capabilities (G1-I). It declares no part of CP-0 complete, and adds no
candidate, act or object property.
