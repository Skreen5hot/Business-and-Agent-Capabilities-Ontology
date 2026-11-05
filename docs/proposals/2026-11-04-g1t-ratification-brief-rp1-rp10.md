# Ratification brief — G1-T: RP-1 and RP-10 (D4)

| Field | Value |
|---|---|
| Status | **Decided 2026-11-04** (`docs/decisions/2026-11-04-d4-rp1-rp10-ratified-option-b.md`): P1 to P3 accepted, RP-1 and RP-10 ratified, sequencing Option B, Aaron Damiano named G1-T reviewer for tranche 1. The text decided on is this brief at `7bd032d`; this status line is the only change since |
| Date | 2026-11-04 |
| Prepared by | Claude Code (`claude-opus-5-5`), for the BCO team |
| Arises from | The architect's I-5 decision of 2026-11-04: "Priority: D4 — ratify G1-T" (`docs/decisions/2026-11-04-i5-proceed-payroll-synonym-ap-hold-lifted.md`, on PR #36) |
| Text to be ratified | `specifications/Business-Capability-Ontology-v0.5.0-draft.3.md` at `c3f1ba2` (PR #34), SHA-256 `2224f869b0ec7a1e31b0afc1c2b403ad222ea290c334bff48a93ebbb6516c574` |
| Decisions it carries | DP-1, RP-1 (`docs/decisions/2026-10-25-dp1-rp1-grounding-boundary.md`); DP-2, RP-10 (`docs/decisions/2026-10-26-dp2-rp10-admission-attribution.md`) |
| Constrained by | DP-1 and DP-2 are not reopened. CM-01 is not changed. No class, property, axiom or IRI is proposed |

G1-T is the type-admission test of specification §8. RP-1 and RP-10 are the specification's
first two ratification items, because "they decide what every G1-T record argues" (§9):
RP-1 fixes the bearer and the basis G1-T questions 1 and 2 ask about, and RP-10 fixes the
test itself. This brief checks that draft.3 carries what the architect decided under DP-1
and DP-2, lists what draft.3 adds beyond them, and sets out what has to be decided, in
order.

## 1. What ratifying RP-1 and RP-10 does, and does not do

**Does.** Under §10, ratifying an item that DP-1 or DP-2 already decided "confirms that this
text carries those decisions faithfully, not that it reopens them". Ratifying RP-1 and RP-10
together also:

- **makes G1-T's five questions and three review rules normative** for type admission (§8);
- **is the admission record of the parent `bco:BusinessCapability`** under
  `obo:BFO_0000016` (disposition) and `cco:ont00000568` (Organization Capability) (CD3,
  R10-04). The parent is minted only in a formalization tranche after it, and no specific
  class may cite this record as its own admission (CAP-04).

**Does not.**

- **Complete CP-0 or D4.** CP-0 also needs RP-2 to RP-9, ADR-002, the permanent namespace
  (RP-5), and the source-adequacy exceptions approved or closed (§10, roadmap D4).
- **Admit any specific class.** Each needs its own PASS G1-T record, with reviewer, date
  and the worked constant-membership cases (CAP-04, b3).
- **Assert anything in OWL.** `src/05_ontology/` stays empty until a formalization tranche
  (D5, CP-1).

## 2. Preconditions

| # | Precondition | State | Why it comes first |
|---|---|---|---|
| P1 | **D3's exit**: the architect accepts v0.5 for ratification (roadmap D3) | **Open.** draft.3 is on PR #34, stacked on PR #33; neither is merged. The R11 acceptance of 2026-11-03 says it does not accept draft.3 for ratification | Ratification is of a text. It has to be the accepted text |
| P2 | **The R5 disposition** (draft.3 §0.2) accepted | **Open.** No acceptance record exists | R5-01, R5-09 and R5-14 are in the RP-1 and RP-10 text (§3, §4 below). CP-0 lists this disposition |
| P3 | **The R10 disposition** (`reviews/R10-disposition.md`; draft.3 §0.4) accepted | **Open.** Proposed, not accepted | R10-01 is in RP-1 and R10-04 is in RP-10. CP-0 lists this disposition |
| P4 | The R11 practitioner-review dispositions accepted and carried into §0.3 | **Done**, 2026-11-03 | Several G1-I clauses come from R11 |
| P5 | CM-02's approved scope carried | **Done** (D2; §1, CD1, CD13) | G1-T question 1 sends what fails it to CM-02 |
| P6 | Source-adequacy exceptions SE-1 and SE-2 | **Open**, "before CP-0" | **Not a precondition here.** Both only add sources to departures that V and P sources already establish (CD1, SF-06). Excluding them leaves the decisions unchanged. They stay CP-0 items |

P1 to P3 can be decided in one act. The recommendation is to do so: they are reviews of the
same text.

## 3. RP-1: does draft.3 carry DP-1?

### DP-1, element by element

| DP-1 (2026-10-25) | Where draft.3 carries it | Faithful |
|---|---|---|
| Option A: the Organization alone bears a business capability | CD1; §4 Business Capability; G1-T question 1 | Yes |
| Basis: its member agent or agents; artifacts, owned or not, are enabling conditions | CD2 items 1 and 3; G1-T question 2 | Yes |
| a1: the relevant member agent or agents, one can suffice; the arrangement is the reason, not the basis; never an abstract set | CD2 item 1 and "One member suffices"; G1-I question 1 | Yes, word for word in substance |
| a2: a basis is asserted only for a type that has passed type admission | CD2 "A basis only for an admitted type"; CAP-25 | Yes |
| a3: constitution, configuration, enabling conditions and temporary constraints kept apart | CD2 items 1 to 4 | Yes |
| a4: OI-14 open where evidence shows socio-technical grounding is needed, citing NAF and UAF; G1-T question 2 sends a type there | CD2 (R5-09 bullet); G1-T question 2; OI-14 | Yes |
| The commitment: losing an essential platform does not by itself end the capability; it persists, latent, unavailable until replaced; it ends only when its basis or arrangement goes | CD2 "The commitment, as decided"; §10 known limits | Yes, with "by itself" kept |
| Limitations acknowledged: the commitment; the SF-06 departure; the organization-only narrowing listed (Q-08) | CD2 (SF-06 sources named); CD1 departures table (SF-05) | Yes. Q-08's list is now in the text |

**No discrepancy found.**

### What draft.3 adds to RP-1 beyond DP-1

Ratifying RP-1 as written accepts each of these too. None reverses DP-1, but the first two
add obligations or framing that DP-1 did not state.

| Addition | Source | Effect | Already accepted? |
|---|---|---|---|
| **A grounding witness for every bearing claim** (CAP-35): every asserted Business Capability instance has at least one asserted basis to a named member | R10-01 | A new obligation on instance data. It also settles that an unadmitted class's instance is never reported as a Business Capability | No: P3 |
| **"A modeling policy, not a CCO entailment"**: the member-only basis is BCO's choice, not something CCO forces | R5-01 | States the status of a1 honestly. Changes no rule | No: P2 |
| Enabling conditions are those **relevant to the capability's realization** | R9 | Narrows item 3 | Yes, 2026-10-26 |
| **When a platform's loss reaches the basis**, G1-I is asked again; a type with a constitutive artifact goes to OI-14 | R5-09 | Applies the commitment's "by itself" | No: P2 |
| **Escalation**: an irreversible loss with no feasible alternative sends the type back to G1-T question 2 | R11 P-01 | The text says it "applies a4 as decided; it does not extend it" | Yes, 2026-11-03 |
| **Possession and availability reported together** | R11 P-01 | Assessment content (RP-6 territory) | Yes, 2026-11-03 |
| **A written procedure is information about the arrangement**, not the arrangement (`cco:ont00001808` *is about*) | R11 P-10 | Clarifies item 2 | Yes, 2026-11-03 |
| **The provider's work is the provider's** (CAP-34) | R10-02 | Sits in CD2's text, but the register files it under RP-2 | No: P3. Ratified with RP-2, and recommended to be read so |
| A person's ability is CCO Skill (`cco:ont00000089`); member-wise and artificial-system abilities are CM-02's | D2 | Moves the boundary into CM-02's approved scope | Yes, 2026-10-31 |

## 4. RP-10: does draft.3 carry DP-2?

### DP-2, element by element

| DP-2 (2026-10-26) | Where draft.3 carries it | Faithful |
|---|---|---|
| Option A: two tests, G1-T once per type with no organization in view, G1-I per bearing claim, recorded as the supporting assessment | CD3; §8 G1-T and G1-I; CAP-04, CAP-26 | Yes |
| A type not yet admitted is staged under Organization Capability, transitionally | CD3 "Staging is transitional"; OI-7 | Yes |
| b1: G1-T question 3 asks about the organization's arrangements, which may involve one member | G1-T question 3 | Yes |
| b3: the constant-membership cases (the DP-1 table) worked in every type review | §8 review rule "Worked cases" | Yes |
| b4: a failing type is reclassified or removed, never left staged | CD3; §8 "No permanent staging"; CAP-32 | Yes |
| b5: G1-I separates capacity from exercise; a realization supports but is never required; who *would* perform; a finding on past exercise shows basis and arrangement still in place | G1-I questions 2 and 3 | Yes |
| b2 rejected: no interest condition, for the reason given | CD3 "No interest condition"; §8 "No sixth question" | Yes, with the reason and the SF-04 departure |
| Limitations: staging outside BFO's split (OI-7); two kinds of record; the SF-04 departure | OI-7; CD3 | Yes |

**No discrepancy found.**

### What draft.3 adds to RP-10 beyond DP-2

| Addition | Source | Effect | Already accepted? |
|---|---|---|---|
| **The parent is admitted by this ratification, not by G1-T** | R10-04 | **The most consequential addition.** Ratifying RP-10 becomes the parent's admission record. The reason: G1-T tests a type against the parent's definition, and the parent has no index (R5-14), so G1-T cannot be asked of it | No: P3 (and R5-14 under P2) |
| G1-T questions 4 (non-deontic) and 5 (exercise, not development) | v0.4, R4-02 | Older than DP-2, which did not touch them. Ratifying RP-10 makes them normative. Tranche 1's evidence exclusions rest on them | Ratified by this act only |
| G1-T question 1 sends a failing ability to Skill or CM-02 | D2 | Boundary wording | Yes, 2026-10-31 |
| G1-I question 2's further clauses: dated criteria and threshold (P-02), arrangement evidence (P-04), the remaining ability after a platform loss (P-01), procedures as evidence (P-10) | R11 | Tightens what counts as evidence | Yes, 2026-11-03 |
| G1-I question 3 is about performing, not taking part (CM-01 RL-14) | R10-02 | Ties to CAP-34 (RP-2) | No: P3 |
| G1-I questions 4 (enabling conditions) and 5 (fragility); "no finding" when evidence cannot settle questions 1 or 2 | R11 P-01, P-04; CD14 | Assessment content | Yes, 2026-11-03 (R11); CD14 under RP-6 |

## 5. Sequencing: may tranche 1 be reviewed on RP-1 and RP-10 alone?

The roadmap makes T7, the first tranche, depend on **D4**, all of CP-0. Under that reading,
no G1-T record can be completed until RP-2 to RP-9, RP-5, ADR-002 and SE-1 and SE-2 are
also settled.

What G1-T asks depends only on RP-1 and RP-10. Two other things also bear on a G1-T record:

- the **realization index**, which question 4 and question 5 examine, is CD4 (RP-2);
- what a **PASS** licenses, a subclass assertion, is not acted on before a formalization
  tranche (D5, CP-1) in any case.

| Option | What happens | Cost |
|---|---|---|
| **A. Keep the roadmap as written** | G1-T records wait for all of CP-0 | Tranche 1 waits on RP-5 (the namespace) and ADR-002, which have nothing to do with admission |
| **B. Allow G1-T records once RP-1, RP-2 and RP-10 are ratified** (recommended). A PASS is recorded, and licenses nothing in OWL until CP-0 and D5 | The three tranche 1 candidates can be reviewed now. A roadmap amendment is needed: T7's dependency becomes "RP-1, RP-2 and RP-10 ratified" for the review, and D4 for formalization | RP-2 joins the first ratification. It is "Revised (R5-05, R10-02)", and its text needs the same check as this brief gives RP-1 and RP-10 |
| C. Allow G1-T records on RP-1 and RP-10 alone | As B, with the index rules unratified | A record's question 4 and 5 answers would rest on an unratified CD4 |

## 6. Before a G1-T record can be a PASS, whichever option

- **A named reviewer.** CAP-04 requires a reviewer and a date on every PASS record. Who
  reviews, and whether the recorder may draft for the reviewer, is the architect's to say.
- **The worked cases.** b3 requires each review to work R6's constant-membership cases (the
  DP-1 table in CM-01). Tranche 1's §6 drafts answers to the five questions but does not
  yet work those cases. That is drafting work, done after ratification.
- **IRIs before encoding.** OI-8: BFO's *has member part* is not yet in the vendored
  extracts, and the *is performed by* relation for CAP-34 is unverified. This blocks the
  Stage 05 encoding of CAP-25, CAP-34 and CAP-35, not ratification or a G1-T record. The
  IRIs this brief cites were checked against the vendored extracts: `obo:BFO_0000016`
  disposition, `obo:BFO_0000218` has material basis, `cco:ont00000568` Organization
  Capability, `cco:ont00001180` Organization, `cco:ont00000089` Skill, `cco:ont00001808`
  is about.

## 7. Decisions asked of the architect, in order

1. **P1 to P3, together:** accept v0.5.0-draft.3 (SHA-256 `2224f869…c574`) for ratification,
   and accept the R5 and R10 dispositions. Or name the changes wanted first.
2. **RP-1:** ratify as carried in draft.3 CD1 and CD2, accepting the additions in §3. The
   provider's-work bullet is read as part of RP-2.
3. **RP-10:** ratify as carried in draft.3 CD3 and §8, accepting the additions in §4. This
   includes the parent's admission by this ratification, and G1-T questions 4 and 5.
4. **Sequencing (§5):** option A, B or C. If B, authorize a matching check of RP-2.
5. **Reviewer (§6):** who signs G1-T records.

Each act is recorded verbatim in `docs/decisions/`, with the digest of the text it is about.
The specification's register (§10) is updated only in a reviewed version, never silently.

## 8. What remains for CP-0 after these acts

RP-2 to RP-9, RP-5 (the permanent namespace), ADR-002, and SE-1 and SE-2. Then D4 closes
with a stage-completion record (roadmap D4).
