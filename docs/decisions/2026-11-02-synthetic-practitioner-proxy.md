# Decision record — a synthetic practitioner as proxy for the AD-2 practitioner review, 2026-11-02

Recorded verbatim by Claude Code (`claude-opus-5-5`) on 2026-11-02, from the direction the product owner and architect, Aaron Damiano, gave in session. The act is the architect's.

**What it is about:**

- *The review.* `CM-01_Enterprise_Architecture_Practitioner_Desk_Review_2026-11-02.md`, an analytical desk review of CM-01, submitted with the direction. Its author is ChatGPT (GPT-6), acting in "an enterprise-architect / ontology-aware analytical role".
  - It is filed verbatim as `reviews/R11-cm01-practitioner-desk-review.md`.
  - SHA-256 `a7d774e6235383f30e85c42b3a15a7f162c8506111d4648b59a9f633ff6fa7cc`, identical to the file received.
- *The requirement it bears on.* The domain-practitioner review of `docs/ROADMAP.md`, revision 2: AD-2, section 6, and open item O-3, "Practitioner reviewer(s) identified and engaged".
  - Act 3 of the D2/D3 authorization (`docs/decisions/2026-10-31-d2-d3-authorized.md`) kept O-3 open.
  - The same act required a qualified practitioner to be nominated, with documented qualifications and capacity, before the review counts under AD-2.
- *The model reviewed.* CM-01 0.1.0, `src/02_conceptual_models/CM-01-business-capability.md`, SHA-256 `292c8f36d64075b9663e159985a15b448aa933c3b5ed4baff3b2a556ca861ccc`.

**The act it contains:** for this project, a synthetic practitioner stands as proxy for the human domain practitioner that AD-2 requires.

**How this record reads the direction.** This is the recorder's reading, not part of the act:

- **R11 stands as the domain-practitioner review of CM-01 under AD-2.** Its reviewer and capacity are as R11's section 1 states them.
- **O-3 is answered.** The reviewer is identified and engaged by the architect's designation.
- **Its findings go to the architect for disposition before CP-0.** This is the same route roadmap §6 sets for any practitioner's findings. The proposed disposition is `reviews/R11-disposition.md`, and it is not accepted.

**What the direction departs from, recorded so that a later reader sees it.** The direction leaves the following text unchanged and takes precedence over it for this project:

- **Roadmap §6 and specification draft.2 §0.3** name the reviewer's capacity as "a business architect, a capability-planning practitioner, or a FIBF standards-lead-agency analyst".
- **R11 limits its own standing.** It says it is "**not** an independent human practitioner attestation". It also says it "must **not** be filed or described as closing O-3, completing a human stakeholder gate, authorizing distribution of PR #34, or supporting ratification by itself".
  - The direction is the architect's answer to that limit. R11 does not close O-3 by itself; the architect's designation does.
  - R11's own text is not edited.
- **The CM-01 stakeholder-review gate is not affected.** It was met by the architect's review as product owner (`docs/decisions/2026-10-30-cm01-stakeholder-review-erratum.md`). R11 does not stand in for it.
- **R11 grants no consent to named publication** (its section 9). Filing it under `reviews/` publishes it on the public site's Reviews page.
  - It is published under the project owner's editorial responsibility, which R11's section 9 allows.
  - Its status line labels it as AI-generated analysis.
- **The review package was not formally approved for distribution.** The package on PR #34 was proposed for distribution and never approved. The architect gave it to the reviewer, and that is recorded here as the architect's own act.

**What it does not do:**

- It accepts no finding or disposition.
- It changes neither CM-01 nor any specification.
- It authorizes neither ratification nor CP-0.
- It does not edit the roadmap.

Whether to amend roadmap §6 and specification §0.3 to name the proxy is left for the architect to decide.

---

````text
The synthetic practitioner will be a proxy for the human practitioner for the purpose of this project. - Aaron Damiano, human project manager and architect
````
