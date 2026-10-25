# Decision record — Staged development adopted; Stage 02 (Conceptual Modeling) choices, 2026-10-25

Recorded verbatim by the setup agent (Claude Code, `claude-opus-5-5`) on 2026-10-25, at the
architect's statements in session. The choices are his.

---

## What the architect stated

````text
Great work so far. The goal is to follow an incremental process to build out a compressive Capabilities Ontology that complements the Process Ontology. Next is the Conceptual Modeling Stage

src/
├── 01_controlled_vocabulary/
├── 02_conceptual_models│
├── 03_taxonomy/ (Comprehensive collection of terms)
├── 04_thesaurus/
├── 05_ontology/
└── 06_knowledge_graph/
````

He supplied the governing standard with that statement. It is filed verbatim at
`docs/standards/stage-02-conceptual-modeling.md`.

The agent then asked four questions. The architect selected one option for each. The
questions and selected options are quoted verbatim below, each with the option's description
as it was shown:

**1.** *"How should the repo adopt the src/01–06 stage layout?"* — **"Move now, first PR (Recommended)"**

> A mechanical PR before any modeling: vocab/ → src/01_controlled_vocabulary/, ontology/ →
> src/05_ontology/, each stage dir gets a README stating its status. Tools find files by layout
> id, so content and digests don't change; CI, docs and paths are updated and verified
> byte-identical.

**2.** *"Which diagram notation for the conceptual model?"* — **"Mermaid, rendered locally (Recommended)"**

> Mermaid source in the model files is the truth: text, diffable, rendered natively on GitHub.
> The public site renders it with a pinned, vendored mermaid.js served from the site itself
> (no CDN, so check_site stays clean). Each diagram has its required textual description
> beside it.

**3.** *"How should the conceptual model be split?"* — **"One domain model, several patterns (Recommended)"**

> CM-01 Business Capability Conceptual Domain Model: one scope, one approval, with patterns
> inside it (capability and bearer; realization by BPO acts; description layer:
> maps/assessments/ratings/targets; sourcing and authorization; catalog and coverage). Traced
> to CQ-1..CQ-14.

**4.** *"The Stage 02 standard says ambiguities that materially affect meaning must be
resolved before approval. RP-1 (material basis: member agents only vs including artifacts)
and RP-10 (when a capability type is a genuine disposition) are exactly that. How should
CM-01 handle them?"* — **"Decide them in CM-01 (Recommended)"**

> CM-01 presents RP-1 and RP-10 as explicit decision points with the options, the R6/R7
> critiques and register evidence. Approving CM-01 requires your decision on each, recorded
> as acts; the spec follows in v0.5.

---

## Effect

1. **The repository follows six stages**, `src/01_controlled_vocabulary/` to
   `src/06_knowledge_graph/`. The governing standard for Stage 02 is
   `docs/standards/stage-02-conceptual-modeling.md`.
2. **The layout moves first, in a PR of its own.** That PR is mechanical: it moves files,
   adds stage READMEs and updates paths. It changes no content, and its generated outputs are
   verified byte-identical apart from the paths they record.
3. **Stage 02 delivers CM-01**, the Business Capability Conceptual Domain Model:
   - one model, organized as patterns;
   - Mermaid diagrams, rendered on the site from a pinned, vendored copy;
   - a textual description beside each diagram.
4. **RP-1 and RP-10 are decided through CM-01.** Approving CM-01 requires the architect's
   decision on each, recorded as acts. Specification v0.5 follows those decisions.

## What this does not do

It approves no conceptual model, decides neither RP-1 nor RP-10, and ratifies no vocabulary
concept. It does not change ADR-003, whose path references (`vocab/`) describe the
repository as it was when ratified.
