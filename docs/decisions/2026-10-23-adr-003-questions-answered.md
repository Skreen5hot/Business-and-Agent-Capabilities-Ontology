# Decision record — ADR-003 open questions answered, 2026-10-23

Recorded verbatim by the setup agent (Claude Code, `claude-opus-5-5`) on 2026-10-23, at the
statement the product owner and architect, Aaron Damiano, made in session. The act is his.

**What this decides:** the three questions ADR-003 left for the architect: the sources and
agents namespaces, the unit of ratification, and the PCF edition.

**What it does not do:** it does not ratify ADR-003. The answers are folded into ADR-003, which
stays PROPOSED until a separate ratification act cites it.

---

````text
Great work getting branch `ccv/p0-decisions` clean, compliant, and verified across all 121 checks.

Here are the PO decisions on the three open questions for ADR-003:

1. Sources and Agents Namespaces: Project-Scoped (`bco-sources#` and `bco-agents#`)
Adopt the project-scoped namespaces: `bco-sources#` and `bco-agents#`. Isolating them per project prevents ID and agent collisions with BPO, ARO, or future upstream siblings. If multi-project source federation becomes necessary later, we can address that via a cross-project alignment ADR, but we will not bleed namespaces now.

2. Unit of Ratification: Batch-Allowed by Explicit IRI List
We will support an act ratifying a defined batch of concepts, provided every ratified concept IRI is explicitly enumerated in the decision record.

* A single decision document (e.g., `docs/decisions/YYYY-MM-DD-ratify-metamodel-pilot.md`) can ratify multiple concepts.

* Each concept’s `ratified_by` block points to that shared decision path, commit, and file digest.

* No blanket or wildcard ratifications: An act cannot say "all concepts in scheme X are ratified." It must explicitly name the concept IRIs being admitted. This keeps the ceremony manageable for the P5 pilot while preserving deterministic, inspectable provenance per concept.

3. PCF Edition: Confirmed at 7.4
Confirm PCF 7.4 for all catalog notations. The register and working models are pegged to 7.4. Upgrading the catalog to PCF 8.0 will be handled as its own dedicated evaluation and decision record once the pilot is stable.

Direction & Next Steps

1. Update ADR-003: Fold these three answers into the record so it is complete and ready for formal ratification.

2. Execute P1 & P2 in Parallel: You are cleared to proceed with P1 (`docs/sources/register.yaml` and the Markdown generator) and P2 (the LinkML reproducibility trial) immediately on their respective branches.
````

---

## What it rests on

ADR-003 as proposed at commit `4251b872245567ff7c2a9d093da6134d0ca224c2` on branch
`ccv/p0-decisions`, "Questions for the architect before ratifying" (questions 1–3).

## Effect

- **ADR-003 D1:** `bco-sources#` and `bco-agents#` are adopted, per project. Federation
  across projects is left to a future alignment ADR.
- **ADR-003 D3/D5:** one act may ratify a batch of concepts, but only by listing each concept
  IRI explicitly. A wildcard or scheme-level ratification is refused.
- **ADR-003 D7:** PCF 7.4 is confirmed for all catalog notations. Moving to PCF 8.0 is a
  separate evaluation and decision, after the pilot is stable.
- **P1 and P2 are cleared to start**, each on its own branch.

## Note the record must carry

The act lists the concept IRIs. ADR-003 D3 also has each listed IRI carry the SHA-256 of the
concept record being ratified, because that digest is how CI detects an edit to a Ratified
definition after the act. ADR-003 records this as part of the batch format, for the
architect to confirm or strike when ratifying.
