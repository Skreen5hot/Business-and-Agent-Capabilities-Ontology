# Decision record — G1-T tranche 1 signed: T1-01, T1-02 and T1-03 PASS, 2026-11-05

Recorded verbatim by Claude Code (`claude-opus-5-5`) on 2026-11-05, from the confirmation
the named approving reviewer for tranche 1, Aaron Damiano, gave in session. The finding and
the signature are his.

**What it is about:** the three G1-T type admission records on PR #38, as committed at
`7515f44`, with their confirmation tables blank:

| Record | SHA-256 at `7515f44` |
|---|---|
| `docs/catalog/admission/G1T-T1-01-customer-complaint-management.md` | `7950cce7d363088045f2c8484c1d0ee901b0d4867f3c5e3ac554cd0280665b81` |
| `docs/catalog/admission/G1T-T1-02-payroll-processing.md` | `f41e29cc40df6ed4ef84064bb40677cedc7aff7f4003c2977f7150164a87cee4` |
| `docs/catalog/admission/G1T-T1-03-accounts-payable-processing.md` | `b49935b79b4046d34d84080f46b5e1bff17f5e277d3aab5b607a343c20594c2d` |

They test the classes of `docs/catalog/tranche-1.md` revision 4 (SHA-256 `dfafb555…c045`)
against G1-T, specification v0.5.0-draft.3 §8, under the D4 decision of 2026-11-04 (act 9:
the reviewer's own confirmation, not an automated draft, is the signature). The
independent AI review of the same day (`docs/catalog/admission/G1T-T1-review-2026-11-05.md`)
is evidence for it, and is not the signature.

## The confirmation

````text
Finding: PASS | Reviewer: Aaron Damiano | Date: 11/5/2026 | Notes:

Record	Proposed finding	Confirmation notes
T1-01 Customer Complaint Management	PASS	Confirm all five G1-T answers and worked cases. Accept the four-act index and exclusion of P19072. BPO's broader type is distinct; no equivalence or subclass relationship is asserted.
T1-02 Payroll Processing	PASS	Confirm all five answers and worked cases. Accept the eleven-act index, including P10865. Preserve CD2 escalation, the distinction from Time Reporting, and CAP-34 outsourcing treatment.
T1-03 Accounts Payable Processing	PASS	Confirm all five answers and worked cases. Accept the seven-act index, including P10877; retain the exclusion of payment authorization. Accept non-purchase-order invoices and single-member organizational arrangements.
````

## The acts it contains

1. **T1-01 Customer complaint management: PASS.** All five answers and the worked cases are
   confirmed. The four-act index and the exclusion of `P19072` are accepted. BPO's broader
   type is distinct: no equivalence or subclass relation is asserted.
2. **T1-02 Payroll processing: PASS.** All five answers and the worked cases are confirmed.
   The eleven-act index, `P10865` included, is accepted. The CD2 escalation, the
   distinction from Time Reporting, and CAP-34's treatment of outsourcing are kept.
3. **T1-03 Accounts payable processing: PASS.** All five answers and the worked cases are
   confirmed. The seven-act index, `P10877` included, is accepted, and payment
   authorization stays excluded. Invoices with no purchase order and arrangements of a
   single member are accepted.

## How it was carried out

- Each record's confirmation table holds the finding, the reviewer, the date (2026-11-05,
  given as 11/5/2026) and his note for that record, verbatim. Each record's status reads
  signed, and its review date is set.
- No other content of the records changed.

## What it does not do

A PASS licenses asserting each class under `obo:BFO_0000016`, and so under
`bco:BusinessCapability`, for that class only (CAP-04). It asserts nothing yet. Under
Option B, no class is minted or asserted in OWL before all of CP-0 and D5. It licenses no
organization's claim to bear any of these capabilities (G1-I). It does not declare CP-0
complete. It adds no candidate, act or object property. The specification, CM-01 and
tranche-1 are unchanged.
