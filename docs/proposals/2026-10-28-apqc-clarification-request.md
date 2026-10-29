# Request to APQC for written clarification of the PCF terms — not sent, superseded

> **Not sent. Superseded on 2026-10-29** by the architect's decision
> `docs/decisions/2026-10-29-apqc-pcf-sourcing-decided.md`. That decision withdraws APQC-2,
> so the request is not sent and APQC is not added as a communications team. It replaces
> APQC-1 with the architect's own rights position: PCF 7.4 is published, sourced from BPO
> and with APQC's notice. It defers APQC80-1. The text below is kept as it stood when the
> decision was taken (`b120b48`), as the record of what was considered.

| Field | Value |
|---|---|
| Status | **Not sent; superseded** by `docs/decisions/2026-10-29-apqc-pcf-sourcing-decided.md`, which withdrew APQC-2. Before that: authorized in principle (APQC-2 a, `docs/decisions/2026-10-28-i2a-decided.md`, section 3). This revision makes the two disclosures that decision requires, and records the check of the contact. The draft the decision was taken on is this file at `4143880` (SHA-256 `f6818a9b…f63f`) |
| Date | 2026-10-28 |
| Prepared by | Claude Code (`claude-opus-5-5`), under decisions E2 and APQC-2 |
| Why | The I-2a rights review (`docs/sources/inventory/rights.yaml`, source `apqc-pcf-7.4`) found APQC's terms ambiguous for this repository's use |
| Addressee | `pcf_feedback@apqc.org` (see "The contact" below) |
| Sender | The architect, by email from the architect's own account. The message is signed in the architect's name, so only the architect can send it |
| After sending | Not applicable: the request is not sent (see the status above) |

## The contact

The decision asks for the appropriate permissions contact to be verified before the
request is sent.

- **What the evidence shows.**
  - The only contact APQC gives in the PCF itself is `pcf_feedback@apqc.org`, with the
    telephone number +1-713-681-4020. It appears on the About sheet of the pinned 7.4
    workbook (`xl/drawings/drawing2.xml`, workbook SHA-256 `0e6e24b6…7d24`), which tells
    readers with further questions to contact APQC there.
  - The PCF 7.2.1 edition gives the same address.
  - Older PCF editions, from 2010 to 2014, name `apqcinfo@apqc.org` instead.
- **What could not be checked.**
  - No separate permissions or legal contact for the PCF turned up in that evidence or
    in a web search.
  - apqc.org itself could not be read for one, because its Terms forbid automated access.
- **What to do when sending.** Address the request to `pcf_feedback@apqc.org`, the
  contact APQC names in the licensed file. If the architect, reading apqc.org by hand,
  finds that its Terms or contact page name a legal or permissions address, copy that
  address too.

## Facts the message states, as verified on 2026-10-28

| Statement | Evidence |
|---|---|
| The BCO is open source under the MIT licence, and is published on GitHub and as a website | `LICENSE`; repository `Skreen5hot/Business-and-Agent-Capabilities-Ontology` is public; the site is `https://skreen5hot.github.io/Business-and-Agent-Capabilities-Ontology/` |
| BPO is a public GitHub repository under the MIT licence, with a website | `gh repo view Skreen5hot/BusinessProcessOntology`: public, MIT; the site is `https://skreen5hot.github.io/BusinessProcessOntology/` |
| BPO includes APQC's PCF 7.4 Cross-Industry Excel file, with its notice sheet, and has done so since June 2026 | The file is at the BPO repository root at `bc64e91`, SHA-256 `0e6e24b6…7d24`. It was first committed in `225f2a9` (2026-06-02). Its Copyright and attribution sheet is present (rights.yaml, `apqc74-workbook`) |
| BPO's published ontology is built on PCF 7.4. Its classes carry PCF element IDs, and its files reproduce PCF element names | For example, `ontology/slices/apqc_13_0.ttl` at `bc64e91` has classes keyed by PCF element ID (`bpo:PCF_20959`), and comments that quote PCF element names |
| The BCO repository already contains PCF element IDs, taken from BPO, but no PCF names or descriptions | Inventory I-1 (`docs/sources/inventory/bpo-entries.yaml`) records `pcf_code` values and withholds PCF text (59 entries) |
| Both projects are developed with AI assistance | The BCO's tooling, inventory and documents are written with Claude Code, an AI coding agent, which reads the source files, including BPO's PCF-derived files and the notices in the PCF workbook. Of BPO's last 100 commits, 57 are co-authored by Claude. The BCO also models the capabilities of software agents |

## Message

> **To:** pcf_feedback@apqc.org
>
> **Subject:** Permission question: APQC PCF in two open-source ontology projects
>
> Dear APQC,
>
> I maintain two related open-source ontology projects. Both are MIT-licensed and published
> on GitHub and as public websites, and neither is sold. I would like to confirm that our
> use of the Process Classification Framework (PCF) is within your terms, and to adjust it
> if it is not.
>
> **What already exists.** The Business Process Ontology
> (https://github.com/Skreen5hot/BusinessProcessOntology) is built on the PCF
> Cross-Industry version 7.4. Since June 2026 its repository has included your Excel
> release of PCF 7.4, with its copyright and attribution notice intact. Its published
> ontology files use PCF element IDs to identify its classes, and reproduce PCF element
> names. The second project, the Business Capability Ontology
> (https://github.com/Skreen5hot/Business-and-Agent-Capabilities-Ontology), records PCF
> element IDs taken from the first project. Pending your answer, it withholds PCF names
> and descriptions.
>
> **How the projects are developed.** Both projects are developed with the help of an AI
> coding assistant (Anthropic's Claude Code). The assistant writes software and documents,
> and in doing so reads the projects' source files, which include PCF-derived content and
> the notice in your workbook. The Business Capability Ontology also describes, among other
> things, the capabilities of software agents.
>
> **What we would like to do.** We would like to record selected PCF elements as cited
> source evidence: element ID, hierarchy ID, name and description, each attributed to the
> PCF. Your copyright and attribution notice would be reproduced in full in a notice file
> beside the data, and on every web page that shows PCF text. We would not suggest that
> APQC endorses either project. We would also compare PCF 7.4 with PCF 8.0 by element ID,
> under the same conditions.
>
> **Why we are asking.** The notice in the PCF 7.4 workbook grants a licence to use, copy,
> publish, modify and create derivative works of the PCF, provided the notice is included
> in all copies and derivative works. APQC's Terms of Service (last modified July 2026)
> restrict public distribution of APQC's online resources unless an APQC licence agreement
> permits it, and restrict using them to create, train or test AI systems. We want to be
> sure we read these correctly together. Could you confirm:
>
> 1. That the licence in the PCF's copyright and attribution notice is the agreement that
>    governs use of the PCF itself, so that the Terms of Service do not restrict what that
>    notice permits?
> 2. That the uses described above, both existing and intended, are within that licence?
>    These are publishing element IDs, hierarchy IDs, names and descriptions openly with
>    the full notice, and including the PCF 7.4 Excel file, with its notice, in a public
>    repository.
> 3. That reproducing the notice once in a notice file published with the data, and on
>    each web page showing PCF text, satisfies the requirement that copies and derivative
>    works contain it?
> 4. That people who obtain PCF-derived material from our public repositories, without
>    registering with APQC, may use it under the same notice?
> 5. That the PCF 8.0 Cross-Industry release carries the same licence and notice as 7.4?
> 6. That the Terms of Service's clause on artificial intelligence does not apply to
>    ontologies that are developed with an AI coding assistant, as described above, and
>    that describe the capabilities of software agents? If it does apply, could you tell us
>    how?
>
> Until we hear from you, the Business Capability Ontology will publish nothing more from
> the PCF than citations. If any of this is outside what APQC permits, we will change what
> we publish accordingly. Thank you for the PCF, and for any guidance.
>
> Kind regards,
>
> Aaron Damiano

## What changed from the draft at `4143880`

- **The BPO disclosure is now explicit and accurate.**
  - It gives the BPO repository's address.
  - It states that the PCF 7.4 Excel file has been in that public repository since June
    2026.
  - It states that BPO's published files use PCF element IDs and reproduce element names.
  - Question 2 now asks about that existing use as well as the intended one.
- **The AI disclosure now has a paragraph of its own.** It names the assistant, says what
  the assistant does, and says that the assistant reads PCF-derived content. Before, it
  appeared only inside question 6.
- **The BCO's current state is stated:** it holds PCF element IDs, and withholds PCF names
  and descriptions.
- **"Non-commercial" was replaced** by "MIT-licensed … neither is sold". The MIT licence
  lets others use the work commercially, so "non-commercial" was not accurate.
- **The closing line follows APQC-1 c:** the BCO publishes nothing more from the PCF than
  citations until APQC answers.

## After an answer

1. The answer is recorded verbatim, with its digest, as an incoming message.
2. It amends the `apqc-pcf-7.4` and `apqc-pcf-8.0` records in
   `docs/sources/inventory/rights.yaml`.
3. Public redistribution expands only after a later decision of the architect is recorded
   in `docs/decisions/`.
