# RP-3 faithfulness check — enablement relations (CD12), with the OI-6 lookup

| Field | Value |
|---|---|
| Status | **Decided 2026-11-06**: RP-3 ratified, with a clarification on `requiresCapability`, and OI-6's lookup closed (`docs/decisions/2026-11-06-rp3-ratified.md`). The text decided on is this check at `a4ba28a`; this status line is the only change since |
| Date | 2026-11-06 |
| Prepared by | Claude Code (`claude-opus-5-5`), for the BCO team |
| Closes, if decided | CP-0 closure matrix item 7, decision 2 (`docs/proposals/2026-11-05-cp0-closure-matrix.md`); the lookup answers OI-6 |
| Text checked | `specifications/Business-Capability-Ontology-v0.5.0-draft.3.md` at `c3f1ba2`, SHA-256 `2224f869b0ec7a1e31b0afc1c2b403ad222ea290c334bff48a93ebbb6516c574`: CD12, CAP-03, CAP-13, CAP-14, §9's migration row, OI-6 |
| Checked against | CM-01, approved (SHA-256 `292c8f36d64075b9663e159985a15b448aa933c3b5ed4baff3b2a556ca861ccc`): Realization Index, RL-10, RL-11, Q-12. R5-08 (`reviews/R5-v0.4-artifact-review.md`), accepted. BPO at the inventory pin `bc64e91` (`config/inventory-sources.yaml`), each file digest-checked |

## 1. What RP-3 is

The register (§10) states RP-3 as: "`ex:enablesProcess` an annotation meaning admissible
realization; `requiresCapability` withdrawn". Its status is "Revised wording (R5-08)".
Like RP-2, it has no decision point of its own, so its faithfulness is checked against
CM-01 and the accepted review.

CD12 says four things:

1. BPO's `capability_scope.json` generates `ex:enablesProcess`, the mandatory realization
   index of CD4.
2. It is an `owl:AnnotationProperty` with no causal or modal entailment. Its label is
   historical: it means *admissible realization*, not actual enablement.
3. `requiresCapability` stays withdrawn. Read as stated, it would say every act of a type
   needs an organization bearing the capability. That is false whenever a contractor or a
   single person performs the act.
4. Each scope entry is checked against CD5 before it enters the index. Generation is
   tested on its output, and the legacy generator stays until its consumers are audited.

## 2. CD12 against CM-01

| CD12 (draft.3) | CM-01 (approved) | Faithful |
|---|---|---|
| `ex:enablesProcess` carries the realization index | RL-10 *has realization index*, mandatory for every specific type; RL-11 *lists as admissible*, Realization Index to BPO Act Type | Yes. CM-01 names the relation; CD12 names its carrier |
| An annotation, with no causal or modal entailment | RL-11 "Not exhaustive, not modal"; the Realization Index claims neither that the list is complete nor that every act of a listed type needs a capability | Yes. An annotation carries no OWL entailment, which is the formal form of "not modal" |
| `requiresCapability` withdrawn | The same sentence of the Realization Index: no claim that every act of a listed type needs a capability | Yes. `requiresCapability` states exactly the claim CM-01 rules out |
| Scope entries checked against CD5 | The Realization Index lists acts that exercise the capability, not acts that develop it (CD5, ratified with RP-2) | Yes |
| Generation tested; the legacy generator kept until consumers are audited | Not in CM-01; an implementation rule | Consistent. It adds a process rule, not a commitment |

**No discrepancy between CD12 and CM-01.** R5-08 asked for three things, and draft.3 has
each: a declaration check (CAP-03's last sentence, gate B), a generation test (CAP-13 and
CAP-14), and the wording "admissible realization index, not actual enablement" (CD12).

## 3. The OI-6 lookup: where BPO declares the two properties

OI-6 asks where BPO declares `enablesProcess` and `requiresCapability`. The vendored
extract holds neither. It is drawn from `ontology/apqc-ext.ttl` alone, and
`config/upstream-extracts.json` lists both among the 61 names the specification uses that
no pinned file describes. The lookup therefore read BPO's own modules at the inventory pin
`bc64e91` (BPO v0.4.1): all 20 pinned ontology files, each checked against its pinned SHA-256.

| | `bpo:enablesProcess` | `bpo:requiresCapability` |
|---|---|---|
| Declared in | `ontology/capabilities_roles.ttl` | `ontology/capabilities_roles.ttl` |
| Declared as | **`owl:AnnotationProperty`**, as CD12 requires | **`owl:ObjectProperty`** |
| BPO's label | enables process | requires capability |
| BPO's comment, in short | Capability to the process class whose execution it enables. The operational inverse of `requiresCapability`; its BFO grounding is *has realization*. Used for authoring scope and wiring checks | Process class to the capability an agent must bear to perform it. **Derived** from `enablesProcess`, generated as its inverse so the two never drift. Range enforced by BPO's SHACL |
| Triples | 361: 356 in `capabilities_wiring.ttl`, 5 in `capabilities_roles.ttl` | 361: 356 in `capabilities_wiring.ttl`, 5 in `delivery_processes.ttl` |

The 361 `enablesProcess` entries match CM-01 Q-12's count at BPO `66131945`.

**BPO's current main** (`14a1e2c`, 2026-11-05) was also checked. It still declares
`enablesProcess` an annotation property and `requiresCapability` an object property, and
still generates `requiresCapability`. This is a check, not a re-pin: the pin is unchanged.

**OI-6 is answered.** Both properties are declared in `capabilities_roles.ttl`.

## 4. What the lookup means for RP-3

**The property kind is faithful.** BPO already declares `enablesProcess` an
`owl:AnnotationProperty`. CAP-03's declaration check would pass at the pin, and nothing
needs to change in BPO for CD12's second point.

Three gaps remain. None makes CD12's text wrong; each bears on carrying it out.

1. **BPO's comment on `enablesProcess` reads the opposite way to CD12.** It says the
   capability *enables* the process's execution, and grounds it in *has realization*. CD12
   says the label is historical and the property carries no causal claim. If BCO ever
   loads BPO's declaration, BPO's comment comes with it. The options are to ask BPO to
   reword the comment, or to have BCO's own documentation state the reading and leave
   BPO's text alone. CD12 already does the second.
2. **BPO still generates `requiresCapability`: 361 triples.** CD12's "withdrawn" and §9's
   "stop generating the second" are not yet true in BPO. They bind BCO's own build at
   once: CAP-14 fails any `requiresCapability` triple there, and BCO generates none today.
   BPO's generator is BPO's to change, and CD12 itself keeps the legacy generator until its
   consumers are audited. Two consequences:
   - BCO must not take `capabilities_wiring.ttl` or `delivery_processes.ttl` into its
     imports closure while they carry `requiresCapability`, or CAP-14 fails.
   - BPO's comment on `requiresCapability` states the reading CD12 rejects: that every act
     of the type needs a bearer.
3. **CAP-03's declaration check has nothing to check yet.** The vendored extract does not
   carry `ex:enablesProcess`, so gate B cannot see its declaration. Adding it means
   vendoring `capabilities_roles.ttl`, or the one declaration from it, with a re-pin. That
   is formalization work: D5, not CP-0.

## 5. Recommended disposition

**Ratify RP-3 as carried in draft.3:** CD12, CAP-03's declaration clause, CAP-13, CAP-14
and §9's migration row, on the evidence of the OI-6 lookup above.

Make three points explicit in the ratification:

1. `requiresCapability` is withdrawn **for BCO**: BCO generates, asserts and imports none.
   Whether BPO stops generating it is BPO's decision, after its consumer audit.
2. The meaning of `ex:enablesProcess` in BCO is CD12's, whatever BPO's comment says.
   Whether to ask BPO to change the comment is the architect's call; it would be a message
   under `communications/`.
3. Vendoring BPO's declaration so gate B can check it is formalization work, for D5.

**OI-6 can be recorded as answered** by §3, in the same act or on its own.

## 6. What this check does not do

It ratifies nothing and changes no text. It sends no message to BPO, and adds no vendored
term, candidate, object property or OWL. RP-4 (OI-10), RP-5, RP-6 to RP-9, ADR-002 and the
stage-completion record remain CP-0 obligations.
