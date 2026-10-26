# SPDX-License-Identifier: MIT
"""The conceptual-model checker: passes a conforming model, and refuses
each way of breaking the contract.

Every rule is falsified on a copy of one small valid model, written here
as a string rather than committed as a fixture: a tracked `test-fixture`
is loaded as Turtle by validate.py, and a Markdown model is not Turtle.
The model is synthetic so that these tests say what the checker does
whatever state CM-01 is in; one test at the end runs the checker over the
real repository.

The competency-question rows are generated from the specification in
force at test time, so the model traces exactly what the checker will
require without a CQ list typed here.
"""

from __future__ import annotations

import pytest

from conftest import load_tool


@pytest.fixture(scope="module")
def checker():
    return load_tool("bco_check_models", "tools/conceptual/check_models.py")


@pytest.fixture(scope="module")
def known(checker):
    return checker.known_terms()


@pytest.fixture(scope="module")
def cqs(checker):
    found = checker.specification_cqs()
    assert len(found) >= 10, found
    return found


VALID = """\
# CM-99 — Synthetic Test Model

| Field | Value |
| --- | --- |
| Model identifier | CM-99 |
| Title | Synthetic Test Model |
| Version | 0.0.1 |
| Status | Draft |

## 0. Document control

Built by tests/test_conceptual_models.py; never committed.

## 1. Scope and purpose

Makers, the widgets they make, and the know-how they hold. A maker's
ability is a disposition (obo:BFO_0000016), designated by the vocabulary
concept bcom:BusinessCapability.

## 2. Conceptual diagram

```mermaid
flowchart LR
  M["Maker"] -->|makes| W(["Widget"])
  M -.->|holds| K[("Know-how")]
```

**Reading the diagram.** A Maker makes Widgets and holds Know-how.

## 3. Patterns

### P1 — Making

```mermaid
flowchart TB
  M["Maker"] -->|makes| W(["Widget"])
```

**Reading the diagram.** A Maker makes a Widget.

### P2 — Knowing

```mermaid
flowchart TD
  %% the maker sits in a box of its own
  subgraph S ["Inside"]
    M["Maker"]
  end
  K{{"Know-how"}}
  M -.->|holds| K
  classDef plain fill:#fff
```

**Reading the diagram.** The Maker holds Know-how.

## 4. Concept descriptions

### Maker

- **Description.** Something that makes widgets.
- **Distinguishing characteristics.** It makes.
- **Examples.** A workshop.
- **Boundaries.** Not a widget.
- **Related concepts.** Widget, Know-how.

### Widget

- **Description.** A made thing.
- **Distinguishing characteristics.** It is made.
- **Examples.** A sprocket.
- **Boundaries.** Not a maker.
- **Related concepts.** Maker.
- **Vocabulary.** None yet.

### Know-how

- **Description.** What a maker knows.
- **Distinguishing characteristics.** It is held.
- **Examples.** A technique.
- **Boundaries.** Not a widget.
- **Related concepts.** Maker.

## 5. Relationship descriptions

| ID | Relationship | From | To | Direction | Meaning | Qualifications |
| --- | --- | --- | --- | --- | --- | --- |
| RL-01 | makes | Maker | Widget | Maker to Widget | Brings into being. | None. |
| RL-02 | holds | Maker | Know-how or Widget | Maker to held thing | Has. | None. |

## 6. Conceptual boundaries

A widget is not a maker.

## 7. Decision points

### DP-1 — Whether know-how is shared

**Decision:** pending

#### Options

**Option A — Shared.** Know-how is held by several makers.

**Option B — Private.** Know-how is held by one maker.

## 8. Requirements traceability

| CQ | Question | Patterns | Concepts | Relationships |
| --- | --- | --- | --- | --- |
{cq_rows}

## 9. Assumptions and open questions

### Assumptions

- **A-01.** Makers exist.
- **A-02.** Widgets are made.

### Open questions

- **Q-01.** Is know-how shared? *Carried forward.*

## 10. Review status

| Item | State |
| --- | --- |
| Stakeholder review | not yet |
| Approved | no |
"""


def model_text(cqs: list[str]) -> str:
    rows = []
    for index, cq in enumerate(cqs):
        # Vary the cells: a dash means none, and a marked id is read as
        # the specification's own table is read.
        mark = " ‡" if index == 1 else ""
        relationships = "—" if index == 2 else "RL-01, RL-02"
        rows.append("| %s%s | A question. | P1, P2 | Maker, Widget | %s |"
                    % (cq, mark, relationships))
    return VALID.replace("{cq_rows}", "\n".join(rows))


@pytest.fixture
def write(tmp_path, cqs):
    """Write a (possibly mutated) copy of the valid model as bytes, LF."""
    def _write(text: str | None = None,
               name: str = "CM-99-synthetic-test.md"):
        path = tmp_path / name
        path.write_bytes((text if text is not None
                          else model_text(cqs)).encode("utf-8"))
        return path
    return _write


def run(checker, known, paths):
    return checker.check(paths=paths, known=known)


def mutated(cqs, old: str, new: str, count: int = 1) -> str:
    text = model_text(cqs)
    assert text.count(old) >= count, old
    changed = text.replace(old, new, count)
    assert changed != text
    return changed


# ------------------------------------------------------- the valid model


def test_the_synthetic_model_passes(checker, known, write):
    """The positive control. Every negative test below is this model with
    one thing broken, so a checker that refused this would make them all
    pass for the wrong reason."""
    problems, records = run(checker, known, [write()])
    assert problems == []
    record = records[0]
    assert record["identifier"] == "CM-99"
    assert record["patterns"] == 2 and record["diagrams"] == 3
    assert record["concepts"] == 3 and record["relationships"] == 2
    assert record["decision_points_pending"] == 1
    assert record["approved"] == "no"
    assert record["tokens_checked"] == 2


def test_the_summary_line_counts_what_was_checked(checker, known, write,
                                                  cqs):
    _problems, records = run(checker, known, [write()])
    line = checker.summary(records)
    assert line.startswith("ok: 1 model(s), 2 pattern(s), 3 diagram(s), "
                           "3 concept(s), 2 relationship(s), %d CQ(s) traced"
                           % len(cqs)), line
    assert "1 decision point(s) pending" in line


def test_no_model_is_reported_cleanly(checker):
    assert checker.check(paths=[])[0] == []
    assert checker.summary([]).startswith("ok: no conceptual model yet")


def test_main_exits_nonzero_on_a_finding(checker, write, cqs, capsys):
    good = write()
    assert checker.main([str(good)]) == 0
    assert "ok: 1 model(s)" in capsys.readouterr().out
    bad = write(mutated(cqs, "| Version | 0.0.1 |\n", ""),
                name="CM-98-broken.md")
    bad.write_bytes(bad.read_bytes().replace(b"CM-99", b"CM-98"))
    assert checker.main([str(bad)]) == 1
    assert "FINDING" in capsys.readouterr().out


# ----------------------------------------------- the negative cases, by rule


CASES = [
    # 1. title line, Field/Value table, identifier agreement
    ("1-title", "# CM-99 — Synthetic", "# Synthetic", "line 1 is not"),
    ("1-version", "| Version | 0.0.1 |\n", "", "no 'Version' row"),
    ("1-identifier", "| Model identifier | CM-99 |",
     "| Model identifier | CM-98 |", "disagrees with itself"),
    ("1-table", "| Field | Value |", "| Key | Value |", "no `| Field"),
    # 2. the ten sections, present and ordered
    ("2-missing", "## 6. Conceptual boundaries\n", "## 6. Boundaries\n",
     "no `## 6. Conceptual boundaries`"),
    ("2-renamed", "## 2. Conceptual diagram", "## 11. Overview",
     "no `## 2. Conceptual diagram`"),
    # 3. patterns, each with a diagram
    ("3-no-diagram", "### P2 — Knowing\n\n```mermaid",
     "### P2 — Knowing\n\nText.\n\n```text", "has no ```mermaid"),
    ("3-duplicate", "### P2 — Knowing", "### P1 — Knowing",
     "pattern P1 is declared twice"),
    # 4. a reading after every diagram
    ("4-reading", "**Reading the diagram.** A Maker makes a Widget.",
     "A Maker makes a Widget.", "Reading the diagram"),
    # 5. the Mermaid subset, and diagram-to-text consistency
    ("5-header", "flowchart TB", "graph TB", "flowchart LR"),
    ("5-node", 'W(["Widget"])\n```\n\n**Reading the diagram.** A Maker '
     "makes a Widget.", 'W(["Gadget"])\n```\n\n**Reading the diagram.** A '
     "Maker makes a Widget.", "'Gadget' is not a concept"),
    ("5-edge", "M -.->|holds| K\n  classDef", "M -.->|keeps| K\n  classDef",
     "'keeps' is not a Relationship"),
    ("5-unquoted", 'K{{"Know-how"}}', "K{{Know-how}}",
     "outside the Mermaid subset"),
    ("5-unlabelled", '  K{{"Know-how"}}\n', "", "never given a quoted label"),
    ("5-chain", "M -.->|holds| K\n  classDef",
     "M -.->|holds| K -->|makes| W\n  classDef", "outside the Mermaid"),
    ("5-relabelled", '    M["Maker"]\n  end', '    M["Maker"]\n  end\n'
     '  M["Widget"]', "labelled"),
    # 6. the section 4.2 bullets
    ("6-bullet", "- **Examples.** A sprocket.\n", "",
     "no `- **Examples.**` bullet"),
    # 7. the relationship table
    ("7-header", "| ID | Relationship | From | To |",
     "| ID | Name | From | To |", "no table headed"),
    ("7-duplicate", "| RL-02 | holds |", "| RL-01 | holds |",
     "RL-01 is used twice"),
    ("7-from", "| RL-01 | makes | Maker |", "| RL-01 | makes | Smith |",
     "names 'Smith'"),
    ("7-format", "| RL-02 | holds |", "| R2 | holds |", "is not RL-NN"),
    # 8. decision points
    ("8-path", "**Decision:** pending",
     "**Decision:** docs/decisions/no-such-record.md", "does not exist"),
    ("8-value", "**Decision:** pending", "**Decision:** maybe",
     "is `pending` or a path"),
    ("8-twice", "**Decision:** pending",
     "**Decision:** pending\n\n**Decision:** pending", "2 `**Decision:**`"),
    ("8-options", "**Option B — Private.**", "Private.",
     "1 `**Option <Letter>`"),
    ("8-no-options", "#### Options", "#### Choices", "no `#### Options`"),
    # 10. assumptions and open questions
    ("10-marker", "shared? *Carried forward.*", "shared?",
     "carries 0 of the markers"),
    ("10-both", "*Carried forward.*", "*Carried forward.* *Blocks "
     "approval.*", "carries 2 of the markers"),
    ("10-unnumbered", "- **A-02.** Widgets", "- Widgets",
     "does not begin with its A-NN id"),
    ("10-heading", "### Open questions", "### Questions",
     "no `### Open questions`"),
    # 11. review status
    ("11-row", "| Approved | no |", "| Signed off | no |",
     "no `Approved` row"),
    ("11-path", "| Approved | no |",
     "| Approved | docs/decisions/no-such-approval.md |", "does not exist"),
    ("11-blocked", "| Approved | no |",
     "| Approved | `docs/decisions/2026-10-25-stage-02-choices.md` |",
     "DP-1 are pending"),
    # 12. upstream and vocabulary tokens outside diagrams
    ("12-upstream", "(obo:BFO_0000016)", "(obo:BFO_9999999)",
     "obo:BFO_9999999 is not in the vendored extracts"),
    ("12-cco", "(obo:BFO_0000016)", "(cco:ont99999999)",
     "cco:ont99999999 is not in the vendored extracts"),
    ("12-bpo", "(obo:BFO_0000016)", "(ex:ActOfInventing)",
     "ex:ActOfInventing is not in the vendored"),
    ("12-vocabulary", "bcom:BusinessCapability", "bcom:BusinessCapabilty",
     "not a concept in the generated vocabulary"),
]


@pytest.mark.parametrize("old, new, expect",
                         [case[1:] for case in CASES],
                         ids=[case[0] for case in CASES])
def test_each_rule_refuses_its_breakage(checker, known, write, cqs, old, new,
                                        expect):
    problems, _ = run(checker, known, [write(mutated(cqs, old, new))])
    assert any(expect in p for p in problems), problems


def test_a_patterns_section_with_no_pattern_is_refused(checker, known,
                                                       write, cqs):
    """Rule 3: section 3 holds at least one `### P<n> —` pattern."""
    text = mutated(cqs, "### P1 — Making", "### Making")
    text = text.replace("### P2 — Knowing", "### Knowing")
    problems, _ = run(checker, known, [write(text)])
    assert any("section 3 holds no" in p for p in problems), problems


def test_sections_out_of_order_are_refused(checker, known, write, cqs):
    """Rule 2's ordering half: both headings present, in the wrong order."""
    text = model_text(cqs)
    six = text.index("## 6. Conceptual boundaries")
    seven = text.index("## 7. Decision points")
    block6, rest = text[six:seven], text[seven:]
    eight = rest.index("## 8. Requirements traceability")
    block7 = rest[:eight]
    swapped = text[:six] + block7 + block6 + rest[eight:]
    problems, _ = run(checker, known, [write(swapped)])
    assert any("comes before" in p for p in problems), problems


def test_an_orphan_concept_is_refused(checker, known, write, cqs):
    """Rule 5's converse: a described concept no diagram shows."""
    text = mutated(cqs, "### Know-how\n", "### Gadget\n\n- **Description.** "
                   "x\n- **Distinguishing characteristics.** x\n- "
                   "**Examples.** x\n- **Boundaries.** x\n- **Related "
                   "concepts.** x\n\n### Know-how\n")
    problems, _ = run(checker, known, [write(text)])
    assert any("concept 'Gadget' appears in no diagram" in p
               for p in problems), problems


def test_an_orphan_relationship_is_refused(checker, known, write, cqs):
    text = mutated(cqs, "| RL-02 | holds |",
                   "| RL-03 | sells | Maker | Widget | x | x | x |\n"
                   "| RL-02 | holds |")
    problems, _ = run(checker, known, [write(text)])
    assert any("relationship 'sells' appears in no diagram" in p
               for p in problems), problems


@pytest.mark.parametrize("old, new, expect", [
    ("| P1, P2 | Maker, Widget |", "| P1, P9 | Maker, Widget |",
     "names 'P9'"),
    ("| P1, P2 | Maker, Widget |", "| P1, P2 | Maker, Smith |",
     "names 'Smith'"),
    ("| P1, P2 | Maker, Widget | RL-01, RL-02 |",
     "| P1, P2 | Maker, Widget | RL-01, RL-07 |", "names 'RL-07'"),
], ids=["pattern", "concept", "relationship"])
def test_traceability_names_only_what_the_model_defines(checker, known,
                                                        write, cqs, old,
                                                        new, expect):
    """Rule 9: every pattern, concept and RL a row names exists."""
    problems, _ = run(checker, known, [write(mutated(cqs, old, new))])
    assert any(expect in p for p in problems), problems


def test_traceability_covers_exactly_the_specifications_cqs(checker, known,
                                                            write, cqs):
    """Rule 9: the CQ set is the specification's, read from its section 7
    -- one missing and one invented are both refused."""
    last = cqs[-1]
    text = model_text(cqs)
    lines = text.split("\n")
    dropped = "\n".join(l for l in lines
                        if not l.startswith("| %s |" % last))
    problems, _ = run(checker, known, [write(dropped)])
    assert any("%s are not traced" % last in p for p in problems), problems

    row = next(l for l in lines if l.startswith("| %s |" % last))
    invented = text.replace(row, row + "\n| CQ-999 | x | P1 | Maker | "
                            "RL-01 |", 1)
    problems, _ = run(checker, known, [write(invented)])
    assert any("CQ-999 are traced but" in p for p in problems), problems


def test_approval_is_accepted_once_nothing_blocks_it(checker, known, write,
                                                     cqs):
    """Rule 11's positive half: with the decision recorded and the open
    question carried forward, an approval record that exists is accepted.
    Without this, the refusal above could be a checker that refuses every
    approval."""
    record = "docs/decisions/2026-10-25-stage-02-choices.md"
    text = mutated(cqs, "**Decision:** pending", "**Decision:** " + record)
    text = text.replace("| Approved | no |", "| Approved | `%s` |" % record)
    problems, records = run(checker, known, [write(text)])
    assert problems == [], problems
    assert records[0]["approved"] == record


def test_a_blocking_open_question_prevents_approval(checker, known, write,
                                                    cqs):
    record = "docs/decisions/2026-10-25-stage-02-choices.md"
    text = mutated(cqs, "**Decision:** pending", "**Decision:** " + record)
    text = text.replace("*Carried forward.*", "*Blocks approval.*")
    text = text.replace("| Approved | no |", "| Approved | %s |" % record)
    problems, _ = run(checker, known, [write(text)])
    assert any("Q-01 block approval" in p for p in problems), problems


def test_tokens_inside_a_diagram_are_exempt(checker, known, write, cqs):
    """Rule 12: diagrams hold concept names, so a token-shaped string in a
    Mermaid comment is not held to the extracts."""
    text = mutated(cqs, "%% the maker sits in a box of its own",
                   "%% cco:ont99999999 is not a real term")
    problems, _ = run(checker, known, [write(text)])
    assert problems == [], problems


def test_the_cq_list_is_read_from_the_specification(checker, tmp_path):
    """Never typed into the checker: a specification with three questions
    yields three."""
    spec = tmp_path / "spec.md"
    spec.write_bytes(b"# S\n\n## 7. Competency questions\n\n| ID | Q | A |\n"
                     b"| --- | --- | --- |\n| CQ-1 | a | b |\n"
                     b"| CQ-2 *(rev.)* | a | b |\n| CQ-3 \xe2\x80\xa1 | a | b"
                     b" |\n\n## 8. Next\n\n| CQ-4 | not here | x |\n")
    assert checker.specification_cqs(spec) == ["CQ-1", "CQ-2", "CQ-3"]


def test_a_crlf_model_is_refused(checker, known, write, cqs):
    path = write()
    path.write_bytes(path.read_bytes().replace(b"\n", b"\r\n"))
    problems, _ = run(checker, known, [path])
    assert any("CRLF" in p for p in problems), problems


# --------------------------------------------------- the real repository


def test_the_repository_models_pass(checker, repo):
    """Every CM-*.md in the repository, through the same entry point the
    command line and CI use."""
    models = sorted((repo / "src/02_conceptual_models").glob("CM-*.md"))
    if not models:
        pytest.skip("no conceptual model exists yet under "
                    "src/02_conceptual_models/; the checker reports zero "
                    "models cleanly (test_no_model_is_reported_cleanly)")
    problems, records = checker.check()
    assert problems == [], problems
    assert len(records) == len(models)
