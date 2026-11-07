# RP-4 faithfulness check — the agent manifest (CD13), with the OI-10 consumer check

| Field | Value |
|---|---|
| Status | **Decided 2026-11-06**: RP-4 ratified, and OI-10 closed for CP-0 with its release check kept (`docs/decisions/2026-11-06-rp4-ratified.md`). The text decided on is this check at `e1da561`; this status line is the only change since |
| Date | 2026-11-06 |
| Prepared by | Claude Code (`claude-opus-5-5`), for the BCO team |
| Closes, if decided | CP-0 closure matrix item 8, decision 3 (`docs/proposals/2026-11-05-cp0-closure-matrix.md`); the consumer check answers OI-10 for CP-0 |
| Text checked | `specifications/Business-Capability-Ontology-v0.5.0-draft.3.md` at `c3f1ba2`, SHA-256 `2224f869b0ec7a1e31b0afc1c2b403ad222ea290c334bff48a93ebbb6516c574`: CD13, CAP-08, CAP-19, §9's `agents.json` row, OI-10 |
| Checked against | CM-01, approved (SHA-256 `292c8f36d64075b9663e159985a15b448aa933c3b5ed4baff3b2a556ca861ccc`): Agent Manifest, RL-18. The D2 decisions of 2026-10-31 (`docs/decisions/2026-10-31-cm02-scope-s1-decided.md`, S-1a; `docs/decisions/2026-10-31-d2-cm02-scope-approved.md`). BPO at the pin `bc64e91`, and its main at `14a1e2c` |

## 1. What RP-4 is

The register (§10) states RP-4 as: "Description-layer manifest; the computing artifact an
enabling condition only where relevant; what systems bear is CM-02's". Its status is
"Consumers to be checked (OI-10)". The closure matrix asked the architect to decide whether
that consumer check must come before ratification. It has now been done (§3), so the
question no longer needs deciding.

CD13 says five things:

1. BPO's `capabilities/agents.json` lists software agents against capability classes. No
   software agent bears an Organization Capability (CD1).
2. Software is information content, not a material entity, so it bears no BFO realizable.
   Any artifact function belongs to the deployed computing artifact that runs it.
3. The manifest is an ICE that designates the capability types an agent serves (CD14). It
   keeps its routing use.
4. Under CD2, the computing artifact is outside the basis of every business capability. It
   is an enabling condition only of those whose realization actually depends on it.
5. What an artificial system bears is CM-02's question. Nothing in this module presumes the
   answer, and nothing CM-02 finds changes this module's treatment.

## 2. CD13 against CM-01 and D2

| CD13 (draft.3) | CM-01 (approved) and D2 | Faithful |
|---|---|---|
| The manifest is an ICE that designates capability types; it keeps its routing use | Agent Manifest: "A record listing the capability types a software agent serves, used to route work to it"; "Concerns types; describes"; RL-18 *concerns type*, exactly one per record | Yes. One difference: RL-18 says a manifest concerns exactly one type, while an `agents.json` entry lists one or two. Each listed type would be its own manifest record. That is a formalization matter, not a conflict |
| Software bears no realizable; any function is the computing artifact's | Agent Manifest: "Software is information, so it bears no capability; any function belongs to the computing artifact that runs it" | Yes, word for word in substance |
| No software agent bears an Organization Capability (CD1) | Agent Manifest, Boundaries: "Never a bearer, never a basis" | Yes |
| The computing artifact is an enabling condition, only where realization depends on it | Agent Manifest: the artifact "is an Enabling Condition of the organization's capabilities". CM-01 does not add "only where relevant" | Yes, and narrower. CD13 limits the enabling condition to capabilities whose realization depends on the artifact; CM-01 states it without the limit. Narrowing a general statement does not contradict it |
| What artificial systems bear is CM-02's; nothing here presumes it | D2, S-1a: artificial systems are in CM-02's investigative scope; CM-02's integration boundary leaves CM-01's organizational grounding (DP-1) untouched | Yes |

**No discrepancy found.** Two requirements already carry CD13 into the gates:

- **CAP-08.** A K1 instance's bearer is an Organization. Its negative fixture is BPO's own
  `agent.strategy_lead.v1` having a capability.
- **CAP-19.** No ICE bears a realizable entity. Its negative fixture is a software ICE
  bearing an artifact function.

## 3. The OI-10 consumer check

OI-10 asks what consumes `agents.json` for routing, so that changing it breaks nothing
unseen. BPO was cloned and every file searched, at the pin `bc64e91` and again at main
`14a1e2c`. Neither `agents.json` nor its consumer differs between the two.

**What the file is.** `capabilities/agents.json` lists 12 agents (`agent.market_analysis.v1`
to `agent.risk.v1`). Each has a `capabilities` list of BPO capability classes and a `roles`
list of BPO role classes. BPO's own CLAUDE.md calls it "a representative demo fleet, not a
real roster".

**Its consumers.**

| Where | What it does with `agents.json` | Effect of RP-4 |
|---|---|---|
| BPO `scripts/matchability.py` | The only code that reads it. For each process carrying `bpo:requiresCapability`, `requiresRole` or `requiresPermission`, it asks whether one agent's listed classes, or their subclasses, meet them all. Its output is a coverage-gap report, which its docstring calls "a deliverable, not a failure". It is run by hand: BPO's one workflow, `static.yml`, publishes the docs site and does not run it | None, unless BPO changes the file. RP-4 changes how BCO **reads** the manifest. It does not change the file |
| BPO `PHASE1.md`, `CLAUDE.md`, `docs/patterns/layer-architecture.mmd` | Describe the fleet and the matchability check | Documentation only |
| BCO | Nothing reads `agents.json`. The inventory harvest takes the scope file and the ontology modules, not the manifest. The only BCO mentions are the spec, the roadmap and the closure matrix | None |
| A runtime dispatcher | BPO's PHASE1.md speaks of "the agents the dispatcher actually has". No dispatcher code is in BPO or BCO | **Not checkable from here.** If one exists, it lives in another repository |

**OI-10 is answered for CP-0.** One consumer exists and it is BPO's own script, so
ratifying RP-4 breaks nothing.

The roadmap also lists OI-10 at D8, release, as a consumer-impact assessment. That stays
open until release, when any outside dispatcher would matter.

## 4. What the check means for RP-4

**Ratifying RP-4 needs nothing from BPO.** As with RP-3, CD13 governs how BCO treats BPO's
artifact, not BPO's artifact itself.

Two points bear on carrying it out:

1. **BPO's script reads the manifest as bearing.** `matchability.py` says an agent
   "bear[s] a satisfying capability", which is the reading CD13 rejects. The routing
   arithmetic is the same under CD13's reading: "serves a type at or below the required
   one". So the disagreement is about words, not results. It also runs on
   `requiresCapability`, which RP-3 withdrew from BCO, not from BPO. Whether to raise
   either with BPO is the architect's call, and neither is a condition of RP-4.
2. **§9's migration row is BPO-side work, best left to BPO.** The row says to retype
   `agents.json` as a description-layer manifest using `bco:concernsType`, after checking
   consumers. That would mean BPO renaming a field or adopting a BCO annotation, and
   `matchability.py` would need the same change. Nothing in BCO depends on it.
   - If BCO ever needs manifest records in its own graph, it can generate them from the
     JSON as ICEs with one `bco:concernsType` each (RL-18).
   - `bco:concernsType` is not minted yet; minting it is Stage 05 work under CD14, not
     RP-4.

## 5. Recommended disposition

**Ratify RP-4 as carried in draft.3:** CD13, with CAP-08 and CAP-19 as its checks.

Make three points explicit in the ratification:

1. The manifest is read in BCO as a description that concerns types. No entry in it is
   evidence that a software agent bears any capability, or that any organization does.
2. OI-10 is closed for CP-0 by §3. The consumer-impact assessment at release (D8) stays
   open, including any dispatcher outside BPO.
3. BPO's file, its script and §9's retyping are BPO's. RP-4 makes none of them a
   condition, and no message to BPO is implied.

## 6. What this check does not do

It ratifies nothing and changes no text. It sends no message to BPO, mints no
`bco:concernsType`, and adds no candidate, object property or OWL. It does not touch
CM-02's question. RP-5, RP-6 to RP-9, ADR-002 and the stage-completion record remain CP-0
obligations.
