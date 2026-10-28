# Draft — request to APQC for written clarification of the PCF terms

| Field | Value |
|---|---|
| Status | **Draft for the architect's separate authorization. Not sent, and not to be sent without that act.** |
| Date | 2026-10-28 |
| Prepared by | Claude Code (`claude-opus-5-5`), under decision E2 (`docs/decisions/2026-10-28-i2-and-bpo-repin-decided.md`) |
| Why | The I-2a rights review (`docs/sources/inventory/rights.yaml`, source `apqc-pcf-7.4`) found APQC's terms ambiguous for this repository's use; decision point APQC-2 |
| Addressee | APQC. The PCF workbook's About page gives `pcf_feedback@apqc.org` for questions about the PCF; whether that is the right desk for licensing, or a legal or permissions contact is, is the architect's call |
| Sender | The architect, in his own name |

## Why a request, and why now

The notice inside APQC's PCF 7.4 workbook grants a broad licence (use, copy, publish,
modify, create derivative works) on the condition that the notice travels with every copy
and derivative work. APQC's website Terms of Service, revised July 2026, bar publishing or
distributing any part of APQC's online resources unless an APQC licence agreement permits
it, give such an agreement precedence, and bar using the resources to create, train or
test AI systems. The Terms do not say whether the PCF's own notice is such an agreement.
Until APQC answers, the review recommends that PCF names and descriptions stay withheld,
as they are in Inventory I-1.

The questions are written so that each can be answered yes or no. Nothing in the draft
commits the project to anything; it describes what the project would do and asks whether
that is within APQC's terms.

## Draft message

> **Subject:** Permission question: APQC PCF in an open-source ontology repository
>
> Dear APQC,
>
> I maintain the Business Capability Ontology, an open-source, non-commercial ontology of
> business capabilities published on GitHub and as a public website. A related project I
> also maintain, the Business Process Ontology, is built on the Cross-Industry Process
> Classification Framework (PCF), version 7.4, and includes your Excel release of it with
> its notice intact.
>
> We would like to record PCF elements as cited source evidence: for selected elements,
> the PCF element ID, hierarchy ID, name and description, each attributed to the PCF, with
> your copyright and attribution notice reproduced in full in a notice file beside the data
> and on every web page that shows PCF text. We would not redistribute your workbook
> itself, sell anything, or suggest that APQC endorses the project. We would also compare
> PCF 7.4 with PCF 8.0 by element ID, under the same conditions.
>
> The notice in the PCF 7.4 workbook grants a licence to use, copy, publish, modify and
> create derivative works of the PCF, provided the notice is included in all copies and
> derivative works. APQC's Terms of Service (last modified July 2026) restrict public
> distribution of APQC's online resources unless an APQC licence agreement permits it. We
> want to be sure we read these correctly together. Could you confirm:
>
> 1. That the licence in the PCF's copyright and attribution notice is the agreement that
>    governs use of the PCF itself, so that the Terms of Service do not restrict what that
>    notice permits?
> 2. That the use described above (element IDs, hierarchy IDs, names and descriptions,
>    published openly with the full notice) is within that licence?
> 3. That reproducing the notice once in a notice file published with the data, and on each
>    web page showing PCF text, satisfies the requirement that copies and derivative works
>    contain it?
> 4. That people who obtain PCF-derived material from our public repository, without
>    registering with APQC, may use it under the same notice?
> 5. That the PCF 8.0 Cross-Industry release carries the same licence and notice as 7.4?
> 6. That the Terms of Service's clause on artificial intelligence does not apply to an
>    ontology that is developed with the help of AI software tools and that describes, among
>    other things, the capabilities of software agents? If it does apply, we would like to
>    know how.
>
> If any of this is outside what APQC permits, we will keep to citations and element IDs
> only. Thank you for the PCF, and for any guidance.
>
> Kind regards,
>
> Aaron Damiano

## What the architect decides

- Whether to send it at all (APQC-2), and to which address.
- Whether to keep, cut or reword question 6. It is the question most likely to draw a
  cautious answer; it is included because the review could not tell whether the Terms'
  AI clause reaches this project, and an unasked question is still an open one.
- Whether the description of BPO (a related project, same maintainer) should be there.
  It is accurate, and BPO's own redistribution of the workbook is part of what the answer
  would cover; it also tells APQC that its workbook is already in a public repository.

## After an answer

An answer would be recorded verbatim, as an incoming message with its digest, and would
amend the `apqc-pcf-7.4` and `apqc-pcf-8.0` records in `docs/sources/inventory/rights.yaml`
(evidence, findings, terms). The architect's posture decision (APQC-1) would then be
recorded in `docs/decisions/`, and only after that could I-2b, or a separate PR under E7,
publish PCF text.
