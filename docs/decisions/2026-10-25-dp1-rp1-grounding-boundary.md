# Decision record — DP-1 (RP-1), the grounding boundary: Option A with amendments a1–a4, 2026-10-25

Recorded verbatim by Claude Code (`claude-opus-5-5`) on 2026-10-25, at the statement the
product owner and architect, Aaron Damiano, made in session. The act is his.

---

````text
DP-1 (RP-1): I choose Option A, and I accept amendments a1, a2, a3 and a4, as written in CM-01 0.1.0-draft.2 (SHA-256 6cbc3822e50b61550144b30ca8ed1c8bd37db505abc6efcdbce604e65d928313). I accept the commitment that permanently removing an essential platform does not by itself end the capability. Reco
````

---

**On the text as received.** The statement arrived cut off after "Reco". It was sent from a
reply button the agent had offered, whose full text ended "Record the decision."; the app
truncates a button's message at 300 characters. The choice itself (the option, the four
amendments, the commitment, and the digest of the text decided on) is complete before the
cut, and the record quotes only what arrived.

## What it is about

| Field | Value |
| --- | --- |
| Decision point | DP-1, which is specification RP-1 (the grounding boundary, CD1 and CD2) |
| Text decided on | `src/02_conceptual_models/CM-01-business-capability.md`, 0.1.0-draft.2 |
| At commit | `5db0bfc634c803db3b56f1002db91d78337fa6fa` (PR #11, branch `stage/cm-01`) |
| SHA-256 of that text | `6cbc3822e50b61550144b30ca8ed1c8bd37db505abc6efcdbce604e65d928313`, checked against `git show 5db0bfc:src/02_conceptual_models/CM-01-business-capability.md` before this record was written |
| Option chosen | **A** — the Organization alone bears a business capability; its basis is its constituent member agent or agents; artifacts, owned or not, are enabling conditions |
| Amendments | **a1 accepted** (the basis is the relevant member agent or agents, one can suffice; the arrangement is the reason, not the basis; never an abstract set). **a2 accepted** (a basis is asserted only for a capability whose type has passed type admission). **a3 accepted** (material constitution, organizational configuration, enabling conditions and temporary realization constraints are distinguished explicitly). **a4 accepted** (OI-14 stays open for cases where evidence shows socio-technical grounding is needed, citing NAF and UAF; G1-T question 2 is where a type is sent there; the rationale and consequences of this boundary are recorded) |
| Commitment accepted | Permanently removing an essential platform does not by itself end the capability. It persists, latent, and is assessed as unavailable until the artifact is replaced; it ends only when its basis or arrangement goes |

## Rationale, as the decided text states it

From CM-01 draft.2 §7 DP-1, the drafter's recommendation the architect adopted, which R8
reached independently: A keeps CCO's Organization Capability reusable as is, which R7 asks
for; it satisfies BFO's material-basis condition for every basis it asserts (members are
parts of the organization), which is R6's and R7's formal point; a3 answers R6 Finding 2's
request for four distinctions; a4 keeps option C available for the first type whose review
shows an artifact is constitutive, without building a second bearer pattern before a case
needs one.

## Limitations acknowledged

- The commitment above, which R6 Finding 2 objects to.
- The departure from the defence and enterprise-architecture mainstream that counts
  technology inside the capability: NAF and UAF Capability Configurations, APQC, G211 and
  DM2 (register SF-06).
- The organization-only bearer is a narrowing every source family exceeds (SF-05); the
  departures are to be listed in specification v0.5 (CM-01 Q-08).

## Effect

- CM-01 is revised to apply the decision (0.1.0-draft.3): the grounding relationships in P1
  and the overview become commitments rather than conditional; the "as the specification
  proposes it" hedges go; a1–a4 are written into §4, §5 and §6; Q-01 is closed; DP-1's
  decision line cites this record. Nothing in P2–P5 changes.
- Specification v0.5 is to carry the decision into CD1 and CD2, G1-T question 2 and G1-I
  question 1, CAP-25, and OI-14.

## What this does not do

- It does not decide DP-2 (RP-10), which remains pending, nor amendment b5 or any other
  DP-2 amendment.
- It does not approve CM-01; approval needs DP-2, the architect's review of draft.3, and an
  approval act.
- It does not ratify RP-1 in the specification or any vocabulary concept; all 14 concepts
  remain Draft. It does not accept the R8 disposition, which remains proposed.
- It asserts no OWL: `src/05_ontology/` stays empty, and no material-basis assertion exists
  anywhere.
