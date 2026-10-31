# CM-01 Domain-Practitioner Review Package — cover note for the architect

| Field | Value |
| --- | --- |
| Status | **Proposed. Not approved for distribution.** Prepared at the architect's direction of 2026-10-31 for the architect's review |
| Purpose | To support the domain-practitioner review of CM-01 that roadmap AD-2 and §6 require before CP-0 (D4) |
| Drafted by | Claude Code (claude-opus-5-5), at the architect's direction, 2026-10-31 |
| Model reviewed | `src/02_conceptual_models/CM-01-business-capability.md`, version 0.1.0, approved 2026-10-26. SHA-256 `292c8f36d64075b9663e159985a15b448aa933c3b5ed4baff3b2a556ca861ccc` |
| Specification referenced | `specifications/Business-Capability-Ontology-v0.5.0-draft.2.md`, under review on PR #33 (commit `be8a732`). SHA-256 `7b0911b8eeb51201396e228b98c588dade7d616a3ba154a752b4d227ee3e956b`. For context only |
| Effect | None. This package is not a review and records no finding. It does not complete the practitioner review, close O-3, or authorize ratification. CM-01 and the specification are unchanged |

This note is for the architect. The reviewer receives files 01 to 06.

## Contents

| File | For the reviewer | What it is |
| --- | --- | --- |
| `01-reviewer-brief.md` | Yes | One page: purpose, scope, the reviewer's role, what feedback is expected, and what happens to it |
| `02-cm01-in-plain-language.md` | Yes | CM-01's principal concepts and its five patterns, in plain language, with section references |
| `03-scenarios.md` | Yes | Five business scenarios: dormant capability, single-member grounding, outsourcing, platform dependency, functional adequacy |
| `04-questionnaire.md` | Yes | Open questions in five areas, plus one on the approved decisions |
| `05-findings-template.md` | Yes | The form the reviewer completes and returns |
| `06-references.md` | Yes | The documents, versions and digests, separating what is approved from what is proposed |

The reviewer also receives copies of the documents named in `06-references.md`:

- CM-01;
- the DP-1 and DP-2 decision records;
- the CM-01 stakeholder-review erratum;
- specification draft.2.

CM-01 is also on the public site's Models page. Draft.2 is not on the site, because it is not the specification in force.

## How the package keeps out of the reviewer's way

- **It gives no answers.** Each scenario says what CM-01 does with the case, cites the section, and asks what the reviewer would expect. It does not argue for the model's treatment.
- **It invites objections to approved decisions.** DP-1, DP-2 and CM-01 itself are open to comment. File 01 says how such a finding is handled: by a new, reviewed version of CM-01, never by a silent edit.
- **It asks for no formal work.** The reviewer is not asked to judge OWL axioms, choose object properties, or ratify anything.
- **It keeps approved and proposed apart.** Files 02 and 06 label every source as approved, proposed, or superseded but in force.

## How completed findings are recorded (proposed)

1. The completed template is filed verbatim as received, under the next review number. For example: `reviews/R11-cm01-practitioner-review.md`. It names the reviewer and the capacity they acted in, as roadmap §6 requires. It also records the SHA-256 digests of the package and documents the reviewer was given.
2. A proposed disposition is then drafted separately, for example `reviews/R11-disposition.md`. It gives each finding a disposition and lists the artifacts each finding affects. It decides nothing.
3. All findings go to the architect for disposition before CP-0.
   - Accepted dispositions are carried into v0.5.
   - A finding that requires a change to CM-01 goes through change control, as a new, reviewed version.
4. A completed review does not close O-3. Only the architect does that.

## Points for the architect to settle before distribution

None of these is decided by this package.

- **The reviewer (O-3).** Their identity and the capacity they act in. Roadmap §6 names three capacities: business architect, capability-planning practitioner, or FIBF standards-lead-agency analyst.
- **Publication and consent.**
  - Every file under `reviews/` is rendered on the public site's Reviews page, so filing the findings there publishes them.
  - The reviewer should agree in advance to their name, capacity and findings being published. Otherwise the architect should choose another place to file them.
  - File 01 tells the reviewer that findings are published, so this point needs settling before distribution.
- **Which specification draft to send.**
  - Draft.2 is still under review, so it may change before or during the practitioner review.
  - If it is revised, file 06's specification row and this note's digest change with it. CM-01's row does not change.
  - The review is of CM-01, so the specification is context, not the subject.
- **Delivery format.** The package is Markdown in the repository. It can be sent as Markdown, or rendered to PDF or a shared document without changing the text.
- **Return date and channel.** Files 01 and 05 leave both as placeholders, `[to be set by the architect]`.
- **Compensation and confidentiality terms**, if any. These are outside the repository.

Approving the package for distribution is the architect's act. If approved, it would be recorded in `docs/decisions/` with this directory's file digests.
