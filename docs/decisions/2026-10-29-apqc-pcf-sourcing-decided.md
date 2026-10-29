# Decision record — APQC PCF sourcing: rights position, superseded decisions, BPO as the only source, 2026-10-29

Claude Code (`claude-opus-5-5`) recorded this verbatim on 2026-10-29, from the statement the
product owner and architect, Aaron Damiano, made in session. The act is the architect's,
and so is the acceptance of the residual risk it states.

**What it is about:** the I-2a rights review and the APQC decisions recorded on it, as
committed at `b120b48289f36e88c249e5f9e5201755dc5d5a48` (the head of pull request #16), and
the BPO commit that first carries BPO's `NOTICE.md`:

| Item | SHA-256 (LF bytes at the commit named) |
|---|---|
| `docs/sources/inventory/rights.yaml` at `b120b48` | `2ac667ee29ae853f1c55d1f8cb3a04fc298bdaab881ef00e3fa80ec6b0930cf6` |
| `docs/decisions/2026-10-28-i2a-decided.md` at `b120b48` | `605f53bc50868e651354b59bd39be2e89afa5ddadc1f1c77d45b66dd64951854` |
| `docs/proposals/2026-10-28-apqc-clarification-request.md` at `b120b48` | `1c5459a266391a800eee761e51b536f85bb92c548596081f61569c91b08f60f9` |
| BPO `NOTICE.md` at `2e55edd9e86a0bc20fa88a21595cc61402faa5dc` | `ab7d5122a2d6384b9f380f13b76bb94c31295c69aeaa56f7b1ccdf25b79953e3` |
| BPO `ontology/apqc-catalog.ttl` at `2e55edd` | `598faf6efa81ef6545cac04000c3d3834a9e8478f7619a3b8eed848a5b8d1547` |

**Two notes on the text as received.**

- **It was pasted three times over.** Two full copies were followed by a third from
  section 3's second bullet onward. The copies are identical, so the text is recorded once.
- **It leaves `<BPO-COMMIT>` as a placeholder.** The rule it states is "a pinned commit that
  includes BPO's NOTICE.md … or later". On 2026-10-29 the first BPO commit with `NOTICE.md`
  was `2e55edd`, which was also BPO's head ("Carry APQC's PCF notice on every PCF-bearing
  artifact (NOTICE.md)"). That is the earliest commit the rule admits. The placeholder is
  left as written below. The commit BCO actually pins is named by the change that pins it.

---

````text
Change of direction on APQC PCF sourcing.

I have reviewed the I-2a rights findings and the APQC clarification draft. I am changing direction so the work does not wait on APQC.

### 1. Rights position (supersedes the open question in I-2a)

As architect, I take the following position and accept its residual risk:

- The licence in the PCF's own Copyright and attribution notice governs use of the PCF. It is a perpetual, worldwide, royalty-free licence to use, copy, publish, modify and create derivative works, on the condition that the notice accompanies every copy and derivative work. APQC's website Terms of Service do not restrict what that notice permits.
- Developing an ontology with an AI coding assistant, or modelling the capabilities of software agents, is not creating, training or testing an AI system within the Terms' AI clause.

Record this as my decision and my acceptance of the risk. Do not alter the rights evidence: `rights.yaml` may continue to record the terms as ambiguous, with this decision cited as the resolution of the publication posture.

### 2. Decisions superseded

| Decision | Change |
|---|---|
| APQC-2 (A, send the clarification request) | **Withdrawn.** Do not send the request. Mark the draft as not sent and superseded by this decision. Do not add APQC as a communications team. |
| APQC-1 (C, citation only pending clarification) | **Replaced.** PCF 7.4 material may be published, sourced from BPO, under the conditions in sections 3 and 4. |
| APQC80-1 (A, I obtain PCF 8.0) | **Deferred.** No PCF 8.0 work until a version upgrade is planned. The 7.4-to-8.0 comparison is deferred with it. |

### 3. Source: BPO only

- Take all PCF 7.4 material (element IDs, hierarchy IDs, names, descriptions) from BPO's repository at a pinned commit that includes BPO's NOTICE.md: `<BPO-COMMIT>` or later. `ontology/apqc-catalog.ttl` carries all 1,921 elements. Vendor further BPO files only as needed, each pinned by commit and digest under the existing re-pin discipline.
- Do not access apqc.org for PCF material. Never fetch from it by script; its Terms forbid automated access.

### 4. Notice obligations in BCO

Everything BCO publishes that carries PCF-derived material must carry APQC's notice verbatim, as BPO now does:

- a NOTICE file that separates BCO's MIT work from the PCF material, lists the files concerned, and reproduces the notice;
- the notice on each PCF-bearing artifact (for Turtle, `dct:rights` on the ontology header), and in the footer of every site page that shows PCF text;
- a check that fails when a PCF-bearing artifact lacks the notice;
- no suggestion that APQC endorses BCO, and APQC's marks used only to identify the source.

Copy the notice text from BPO's NOTICE.md at the pinned commit, not by retyping it, and record its digest.

### 5. Governance that still applies

- Lifting I-1's APQC withholding still requires its own reviewed PR (E7), with the I-1 approval and historical outputs kept traceable. I authorize preparing that PR under this decision.
- I-2b proceeds on the BPO source.
- No new vocabulary concepts, ontology classes, properties, IRIs or type-admission results are authorized by this decision. I-3 through I-5 remain separately governed.
- The MITRE and ITIL/TBM restrictions (FIBF-1, FIBF-2) are unchanged.

### 6. Communications

BPO will send a notice pointing to its NOTICE.md and the pinning commit. File it under the protocol. Acknowledge it once the new pin is in place.
````

---

## Effect

**The publication posture for PCF 7.4.** It now rests on the architect's rights position
(section 1), with the residual risk accepted by the architect.

- **The rights evidence is unchanged.** `rights.yaml` still records APQC's terms as
  ambiguous. Its APQC sources point here, as the decision that resolves the publication
  posture.
- **What may be published.** Element IDs, hierarchy IDs, names and descriptions, under
  three conditions:
  - they are taken from BPO at a pinned commit that carries BPO's `NOTICE.md`;
  - APQC's notice, copied from that file, travels with every PCF-bearing artifact;
  - a check refuses an artifact that lacks it.

**The I-2a decisions on APQC:**

| Decision | Before | Now |
|---|---|---|
| APQC-1 | c, citation only pending APQC | Replaced: PCF 7.4 published from BPO, with the notice |
| APQC-2 | a, send the request | Withdrawn: the request is not sent, and APQC is not added as a team |
| APQC80-1 | a, the architect obtains 8.0 | Deferred, with the 7.4-to-8.0 comparison, until a version upgrade is planned |

The BRM and FIBF decisions (BRM-1, BRM-2, FIBF-1, FIBF-2, FIBF-3) are unchanged.

**The work that follows,** each part under its own reviewed PR:

- I-2b, on the BPO source.
- BCO's notice file and its check.
- Under E7, a PR that lifts I-1's withholding and keeps the I-1 approval and its outputs
  traceable.

**Communications.** BPO's notice is filed when it arrives. It is acknowledged once BCO's new
pin is in place.

## What this does not do

- It does not change the rights evidence in `rights.yaml`.
- It does not itself lift I-1's withholding or change any I-1 output.
- It does not authorize any vocabulary concept, ontology class, property, IRI or
  type-admission result, or any of I-3 to I-5.
- It does not touch apqc.org. Nothing is fetched from it, by script or otherwise.
