# ADR-003 — Canonically Controlled Vocabulary: namespaces, citation, revision and sources

| Field | Value |
| --- | --- |
| Status | **PROPOSED** — awaiting the architect's ratification. Nothing below is in force until a ratification act is recorded in `docs/decisions/` citing this file's path, full commit and SHA-256. |
| Date | 2026-10-23 |
| Drafted by | Claude Code (`claude-opus-5-5`), a software agent, at the direction of Aaron Damiano |
| Ratifies | The architect, Aaron Damiano |
| Rests on | `docs/decisions/2026-10-23-ccv-plan-approved.md` (the direction and P0–P5 plan, approved verbatim); `docs/decisions/2026-10-23-adr-003-questions-answered.md` (the architect's answers to this ADR's three open questions, folded in below) |
| Numbering | ADR-001 is BPO's (category and upper-level modelling). ADR-002 is reserved for specification v0.4 ("Organizational Capabilities and Their Realization"). This is the BCO's next number. |

## Context

The BCO needs a controlled vocabulary with two SKOS concept schemes:
- **Metamodel scheme:** the terms the specification uses, such as Business Capability and
  Capability Assessment.
- **Catalog scheme:** the capabilities themselves, such as Treasury Management and Strategic
  Planning.

Every term needs provenance tied to the source register, and a status no one can set by hand.
The approved plan (P0–P5) needs these decisions fixed first, because every tool in P1–P4
encodes them:
- where the IRIs live;
- how a decision is cited;
- what a revision is;
- where the metamodel's definitions come from;
- what the register must hold.

Every decision below keeps a rule this repository already enforces:
- the wellformedness shapes filter on an exact namespace string;
- generated artifacts are byte-reproducible and contain no blank nodes;
- a record cites a digest bound to a commit;
- a decision is the architect's, and only the architect's.

## Decisions

### D1 — Namespaces are siblings, not nested

| Prefix | Namespace | Holds | In the wellformedness population |
| --- | --- | --- | --- |
| `bco:` | `https://fandaws.com/ontology/bco#` | The ontology itself (TBox): classes, properties, `bco:designatesClass`, the vocabulary's annotation properties, the `bco:PCFCode` datatype | yes, as today (`owl:Class`) |
| `bcom:` | `https://fandaws.com/ontology/bco-metamodel#` | Metamodel concepts and `bcom:MetamodelScheme` | yes (`skos:Concept`) |
| `bcoc:` | `https://fandaws.com/ontology/bco-catalog#` | Catalog concepts and `bcoc:CapabilityCatalogScheme` | yes (`skos:Concept`) |
| `bcos:` | `https://fandaws.com/ontology/bco-sources#` | One record per register entry (`bcos:SRC-OMG-03`), generated from `docs/sources/register.yaml` | **no**: its own graph and its own shape |
| `bcoa:` | `https://fandaws.com/ontology/bco-agents#` | Declared agents: people and software agents | **no**: its own graph and its own shape |

Why siblings: no namespace is a prefix of another, so a `STRSTARTS` filter on one can never
select another's terms. `AUTHORED_NAMESPACE` in `tools/ontology/validate.py` becomes
`AUTHORED_NAMESPACES`, a list. The wellformedness targets name each SKOS-bearing namespace
explicitly, and `tests/test_namespace.py` requires the list and the shapes to agree.

**Sources and agents are per project** (the architect's answer, 2026-10-23). A bare
`https://fandaws.com/ontology/sources#` would be shared by every project under that domain,
so ARO's or BPO's registers could mint the same `SRC-` identifiers for different works.
`bco-sources#` and `bco-agents#` prevent those collisions. Federating sources across projects,
if it is ever needed, is a future cross-project alignment ADR. It does not happen by
widening these namespaces.

Whether these are `#` or `/` namespaces stays with RP-5. Changing it means changing every row
of this table in one commit.

### D2 — A decision is cited by path, full commit and SHA-256

Every citation of a decision has three parts:
- `path`: a file under `docs/decisions/` (ratification acts), or `docs/adr/` when the ADR
  itself is cited;
- `commit`: the full 40-character hexadecimal SHA of a commit reachable from `main`;
- `sha256`: the SHA-256 of `git show <commit>:<path>`.

CI recomputes the digest at that commit and fails the build if the three do not agree. A short
commit, a commit not reachable from `main`, or a digest of anything other than those exact
bytes is refused. The empty-file digest, `e3b0c442…b855`, is refused by name.

This is the binding `communications/` already uses for refs into this repository.

### D3 — A concept's IRI is fixed to its meaning

- **An editorial change** (wording, labels, notes, sources) keeps the concept IRI. The change
  is a new version of the concept's *record*. Git keeps the history; the generated graph links
  consecutive record versions with `prov:wasRevisionOf`, using IRIs minted from the record's
  content; the change carries a `skos:changeNote`.
- **A change of meaning** mints a new concept IRI. The old concept gains
  `dcterms:isReplacedBy` pointing at the new one, and from that alone it becomes Deprecated
  (D5).
- **A Ratified concept's definition does not change in place.** CI refuses an edit to the
  definition of a concept whose ratification act cites an earlier record digest. Either a new
  act ratifies the new record, or the change is a change of meaning and gets a new IRI.

`prov:wasRevisionOf` relates record versions only. `dcterms:isReplacedBy` relates concepts
only. Neither is used for the other's job.

### D4 — Metamodel definitions come from specification §4, and nowhere else

- The vocabulary build reads the **Terms** tables of the specification in force (layout role
  `specification`, today v0.4.0-draft.1, §4). From each row it takes: term, IRI, definition,
  parent(s), "Does not imply".
- A metamodel concept's YAML **may not** carry a `definition`. It supplies the provenance
  wrapper (sources, drafting agent, notes, status inputs) and names the §4 row it wraps.
- CI fails if a §4 row has no metamodel concept, if a metamodel concept names no §4 row, or if
  the built definition differs from the row's text.
- The spec writes these terms as `ex:` names. The concept is `bcom:<LocalName>` and its
  `bco:designatesClass` is `bco:<LocalName>`, with the local name unchanged from the spec.
- When the specification changes, the vocabulary follows it at the next build. If that changes
  a Ratified concept's definition, D3 applies: CI fails until a new act or a new IRI resolves
  it.

Catalog concepts are not in §4. Their definitions are authored in YAML, in genus–differentia
form with a BFO/CCO genus, and are subject to D6's quote tripwire.

### D5 — Status is derived, never written

Authors write `Draft` or `Candidate` and nothing else. The build derives the published status,
along with `owl:deprecated`, in this order:

1. **Deprecated** if the concept has `dcterms:isReplacedBy` pointing at a concept that exists
   and is not itself Deprecated. `owl:deprecated true` is emitted.
2. **Ratified** if a ratification act, cited per D2, names this concept's IRI and the SHA-256
   of its current record (confirmed 2026-10-23). One act may ratify a **batch** of concepts, but only by listing
   every ratified concept IRI explicitly. An act that admits concepts by scheme ("all of
   `bcom:MetamodelScheme`"), by pattern, or by any rule other than an explicit list is
   refused. Every concept in the batch has its own `ratified_by` citing the shared act's
   path, commit and SHA-256. (The architect's answer, 2026-10-23.)
3. **Otherwise**, the authored `Draft` or `Candidate`.

`lifecycleStatus` and `owl:deprecated` in authored YAML are build failures. All P5 pilot terms
enter as Draft.

### D6 — The source register is data, and its rules are hard failures

- `docs/sources/register.yaml` is the source of truth. The Markdown register is generated from
  it, and a test requires the two to agree.
- **Claims carry a status** of `V`, `P`, `S`, `K` or `L` (the register's existing taxonomy),
  never a boolean.
- **Quotes** are keyed `SRC-<family>-<nn>-Q<n>`. More than 15 words, a missing key, or a
  duplicate key fails the build.
- **`departs-from`** must cite a claim at `V` or `P`, with a locator and a `departure_note`.
  Anything less fails the build.
- **The quote tripwire** flags any authored definition sharing a 6-word run, after
  normalising case and punctuation, with any registered quote. It is a tripwire, not a
  copyright guarantee: the register holds short quotes, not the works.

As of the register at `8f5c4a1b04e0d5249d0f5b4225998bbef5ec9a76`, these claims about broader
bearers are at `V`, so a `departs-from` for the BCO's organization-only bearer can cite them
today:
- SRC-OMG-01 (VDML 1.1, actors and positions provide capabilities);
- SRC-OMG-03 (BACM 1.1, OrgUnit includes individuals);
- SRC-OMG-04 (UAF 1.3, any CapableElement exhibits capability);
- SRC-GOV-04 (NAF v4.1, the expected ability of resources).

The ArchiMate claim (SRC-OG-03) is `S` and cannot be cited for a departure until it is read.

### D7 — `skos:notation` is typed, and the PCF edition is 7.4 (confirmed)

APQC PCF element identifiers are typed with the datatype `bco:PCFCode`, declared in `bco:`
with the lexical form of a PCF 7.4 Cross-Industry element ID. The edition is part of the
datatype's definition, not of each literal. Adopting PCF 8.0 (published March 2026) would mean
a new datatype and a decision, not a quiet change. The architect confirmed 7.4 for all
catalog notations on 2026-10-23. Moving the catalog to 8.0 is its own evaluation and decision
record, taken once the pilot is stable. 7.4 matches BPO, whose `CLAUDE.md` at
`66131945b525c54f44e4962f32bb1f52dfa0cd12` names it. An untyped `skos:notation` fails the
build.

### D8 — Sources and agents are declared, in graphs of their own

- **Sources.** `bcos:` records are generated from `register.yaml`. They are not SKOS concepts.
  They live in their own generated file and are checked by their own shape: every record has
  an id, citation and status.
- **Agents.** `bcoa:` declares each agent once:
  - a person is a `prov:Person` with a name;
  - a software agent is a `prov:SoftwareAgent` with its exact model identifier (for example
    `claude-opus-5-5`, never a guessed one) and `prov:actedOnBehalfOf` the person who directed
    it.
- An attribution to an undeclared agent IRI fails the build.
- An approval, and anything else that sets status, can only be attributed to a `prov:Person`.

### D9 — The toolchain is Python only, and every artifact is reproducible

- **No Java tools:** no ROBOT and no riot.
- **No blank nodes:** provenance nodes (source references, ratification references, record
  versions) get IRIs minted from their content.
- **Serialization** reuses the deterministic serializer in `tools/ontology/vendor_upstream.py`.
- **Generated files** are declared in the layout contract with their generator, and CI
  rebuilds and compares them.
- **LinkML** is adopted only on a "go" from P2, which builds twice, compares the output byte
  for byte, and weighs `gen-shacl` against hand-written shapes.

## Out of scope, locked

- `#` versus `/` for every namespace above: RP-5.
- `skos:closeMatch` and other alignments to BPO catalog concepts, until BPO's namespace move
  lands (BPO's acknowledgment of 2026-10-23).
- Any `Ratified` term in the P5 pilot.
- Adopting APQC PCF 8.0.

## Consequences

- P1 can start: `register.yaml`, its generator, and the V/P/S/K/L, 15-word and key checks.
- P2 can start: the LinkML trial.
- P3–P4 code against these decisions:
  - `tools/vocab/`;
  - `AUTHORED_NAMESPACES`;
  - the shapes for concepts, sources and agents;
  - the §4 extraction;
  - D2 digest checks;
  - D5 derivation.
- `tools/ontology/validate.py`, `shapes/wellformedness_shapes.ttl` and
  `tests/test_namespace.py` change in P4 to take a list of namespaces. Until then, the single
  `bco#` namespace stays authoritative and the gate is unchanged.

## Questions for the architect: answered

The three questions this ADR raised were answered on 2026-10-23, and the answers are recorded
verbatim in `docs/decisions/2026-10-23-adr-003-questions-answered.md`:

1. **D1:** `bco-sources#` and `bco-agents#`, per project. Cross-project federation is a
   future alignment ADR.
2. **D5:** batch ratification is allowed, by an explicit list of concept IRIs. Wildcard and
   scheme-level acts are refused.
3. **D7:** PCF 7.4 is confirmed. Moving to 8.0 is a separate decision after the pilot.

**The record digest in a batch act is confirmed** (`docs/decisions/2026-10-23-adr-003-batch-digest-confirmed.md`).
Each IRI a batch act lists carries the SHA-256 of the concept record it ratifies (D5 item 2).
The act pins each concept's state, and each concept's `ratified_by` pins the act's commit and
digest, so an edit on either side breaks the lock and fails CI (D3).

**Ratification timing:** this ADR is ratified and merged once the P2 LinkML trial's findings
are signed off.

## How this becomes ratified

The architect states the ratification, with any amendments, in session. The act is recorded
verbatim in `docs/decisions/`, citing this file's path, the full commit it is merged at, and
its SHA-256, per D2. This file's Status line then changes to `RATIFIED`, citing that act, in
the same commit. That edit is the one change made to this file after ratification. Any later
change to a decision here needs a new ADR that supersedes it.
