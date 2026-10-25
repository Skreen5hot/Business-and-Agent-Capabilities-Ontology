# SPDX-License-Identifier: MIT
"""Check the Stage 02 conceptual models against the format they are written in.

    python tools/conceptual/check_models.py            # every model
    python tools/conceptual/check_models.py PATH ...   # these files only
    python tools/conceptual/check_models.py --json     # the same, as JSON

WHAT THIS IS ALLOWED TO DECIDE

The Stage 02 standard (docs/standards/stage-02-conceptual-modeling.md)
section 7 is explicit about the split: "Automated checks MAY verify
documentation completeness, internal references, and artifact
consistency. Conceptual adequacy and stakeholder agreement require human
review." So this checks that a model says everything the standard
requires it to say, in the places a reader will look for it, and that
what it says agrees with itself and with the repository. Whether the
concepts are the right concepts is never a finding here.

THE CONTRACT

A model is `src/02_conceptual_models/CM-<nn>-<words>.md`:

  * line 1 is `# CM-NN — <Title>`, and a `| Field | Value |` table before
    section 1 carries at least Model identifier (equal to the file's and
    the title's CM-NN), Title, Version and Status;
  * the ten headings of the standard's section 5 deliverables, in order:
    `## 1. Scope and purpose` to `## 10. Review status` (other `##`
    headings may sit between them);
  * section 3 holds `### P<n> — <name>` patterns, each with a Mermaid
    diagram, and every Mermaid block anywhere is followed by a paragraph
    beginning `**Reading the diagram.**` -- standard section 2.5:
    "Diagrams MUST be accompanied by textual explanations";
  * diagrams are flowcharts in a deliberately small Mermaid subset, so
    that every node label can be held to a concept heading in section 4
    and every edge label to a Relationship in the section 5 table -- and
    every concept and relationship to some diagram. That is the standard's
    "Diagrams and textual descriptions are consistent", made checkable;
  * each concept carries the section 4.2 bullets; the section 5 table has
    a fixed header, unique RL ids, and From/To naming concepts;
  * section 7 decision points each say `**Decision:** pending` or cite a
    record under docs/decisions/ that exists, with at least two options;
  * section 8 traces exactly the competency questions of the
    specification in force -- read from the specification's own section 7
    table, never listed here -- to patterns, concepts and relationships
    that exist;
  * section 9 numbers assumptions A-NN and open questions Q-NN, and every
    open question says whether it is carried forward or blocks approval;
  * section 10 says Approved: `no`, or cites an approval record -- and
    approval is refused while any decision is pending or any open question
    blocks it (standard section 4.6: material ambiguities "MUST be
    resolved before approval");
  * every `cco:`, `obo:` and `ex:` token outside a diagram names a term in
    the vendored extracts, and every `bcom:`/`bcoc:` token a concept or
    scheme in the generated vocabulary. CLAUDE.md: never assert an
    upstream IRI from memory. Diagram text is exempt because diagrams hold
    concept names, not IRIs.

Exit codes: 0 no findings (including "no model yet"); 1 findings, each on
its own line and naming the file and line.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import layout  # noqa: E402

COMPONENT = "conceptual-models"
ROLE = "conceptual-model"

MODEL_NAME = re.compile(r"^(CM-\d{2})-[a-z0-9]+(?:-[a-z0-9]+)*\.md$")
TITLE = re.compile(r"^# (CM-\d{2}) \u2014 (\S.*?)\s*$")
FIELD_HEADER = "| Field | Value |"
REQUIRED_FIELDS = ("Model identifier", "Title", "Version", "Status")

SECTIONS = (
    "1. Scope and purpose",
    "2. Conceptual diagram",
    "3. Patterns",
    "4. Concept descriptions",
    "5. Relationship descriptions",
    "6. Conceptual boundaries",
    "7. Decision points",
    "8. Requirements traceability",
    "9. Assumptions and open questions",
    "10. Review status",
)

PATTERN = re.compile(r"^(P\d+) \u2014 (\S.*)$")
CONCEPT_BULLETS = ("- **Description.**", "- **Distinguishing characteristics.**",
                   "- **Examples.**", "- **Boundaries.**",
                   "- **Related concepts.**")
RELATIONSHIP_HEADER = ("| ID | Relationship | From | To | Direction | Meaning "
                       "| Qualifications |")
RL_ID = re.compile(r"^RL-\d{2,}$")
DP = re.compile(r"^(DP-\d+) \u2014 (\S.*)$")
DECISION = re.compile(r"^\*\*Decision:\*\* (.+?)\s*$")
OPTION = re.compile(r"^\*\*Option [A-Z]\b")
CQ_ID = re.compile(r"^(CQ-\d+)\b")
ASSUMPTION = re.compile(r"^(?:[-*]|\d+\.)\s+\**(A-\d{2,})\b")
QUESTION = re.compile(r"^(?:[-*]|\d+\.)\s+\**(Q-\d{2,})\b")
LIST_ITEM = re.compile(r"^(?:[-*]|\d+\.)\s+")
CARRIED = "*Carried forward.*"
BLOCKS = "*Blocks approval.*"
READING = "**Reading the diagram.**"
DECISIONS_DIR = "docs/decisions/"

#: The prefixes whose tokens must resolve, and where. Upstream prefixes
#: are those the vendoring pins declare; these two are the vocabulary's.
UPSTREAM_PREFIXES = ("cco", "obo", "ex")
VOCABULARY_PREFIXES = ("bcom", "bcoc")
TOKEN = re.compile(r"(?<![\w:/#.-])(%s):([A-Za-z_]\w*)"
                   % "|".join(UPSTREAM_PREFIXES + VOCABULARY_PREFIXES))

# ---- the Mermaid subset

_ID = r"[A-Za-z_][A-Za-z0-9_]*"
_SHAPE = (r'(?:\(\["[^"]*"\]\)|\[\("[^"]*"\)\]|\(\("[^"]*"\)\)'
          r'|\{\{"[^"]*"\}\}|\["[^"]*"\])')
_NODE = r"(%s)(%s)?" % (_ID, _SHAPE)
_ARROW = r"(-\.->|-->|==>|-\.-|---)"
EDGE_LINE = re.compile(r"^%s\s*%s\|([^|]*)\|\s*%s\s*;?$"
                       % (_NODE, _ARROW, _NODE))
NODE_LINE = re.compile(r"^%s\s*;?$" % _NODE)
FLOWCHART = re.compile(r"^flowchart (LR|TB|TD)\s*$")
IGNORED = re.compile(r"^(?:%%.*|end|direction (?:LR|RL|TB|TD|BT)"
                     r"|(?:classDef|class|style|linkStyle)\s.*"
                     r'|subgraph %s(?:\s*\["[^"]*"\])?)\s*$' % _ID)


class Refused(SystemExit):
    """A question for whoever wrote the input, not for this tool."""


def collapse(text: str) -> str:
    return " ".join(text.split())


# ------------------------------------------------------------- parsing


class Model:
    """One model file, split into what the checks ask about.

    `masked` is the file's lines with every fenced block blanked, so a
    `#` comment or a `|` inside a code block is never read as a heading
    or a table row.
    """

    def __init__(self, path: Path, text: str):
        self.path = path
        self.lines = text.split("\n")
        self.problems: list[str] = []
        self.masked = list(self.lines)
        self.mermaid: list[tuple[int, int, list[str]]] = []
        self._fences()
        self.headings = [(i, len(m.group(1)), m.group(2).strip())
                         for i, line in enumerate(self.masked)
                         for m in [re.match(r"^(#{1,6}) (.+?)\s*$", line)]
                         if m]

    def finding(self, line: int | None, message: str) -> None:
        where = self.path.name if line is None else "%s:%d" % (
            self.path.name, line + 1)
        self.problems.append("%s: %s" % (where, message))

    def _fences(self) -> None:
        opener = None
        for i, line in enumerate(self.lines):
            if opener is None:
                match = re.match(r"^(```|~~~)\s*([\w-]*)\s*$", line)
                if match:
                    opener = (i, match.group(1), match.group(2))
                continue
            if line.strip() == opener[1]:
                start, _fence, info = opener
                if info == "mermaid":
                    self.mermaid.append((start, i, self.lines[start + 1:i]))
                for j in range(start, i + 1):
                    self.masked[j] = ""
                opener = None
        if opener is not None:
            self.finding(opener[0], "this fenced block is never closed; is "
                         "the rest of the file meant to be code?")
            for j in range(opener[0], len(self.lines)):
                self.masked[j] = ""

    # ---- structure

    def section(self, title: str) -> tuple[int, int] | None:
        """(first line, end) of the `## title` section, if present once."""
        found = [i for i, level, text in self.headings
                 if level == 2 and text == title]
        if len(found) != 1:
            return None
        start = found[0]
        end = next((i for i, level, _ in self.headings
                    if level <= 2 and i > start), len(self.lines))
        return start + 1, end

    def subsections(self, span, level: int = 3) -> list[tuple[int, str, int]]:
        """[(heading line, text, end)] of the headings at `level` in span."""
        if span is None:
            return []
        start, end = span
        heads = [(i, text) for i, lv, text in self.headings
                 if start <= i < end and lv == level]
        out = []
        for i, text in heads:
            stop = next((j for j, lv, _ in self.headings
                         if i < j < end and lv <= level), end)
            out.append((i, text, stop))
        return out

    def table(self, header_line: int) -> list[tuple[int, list[str]]]:
        """[(line, cells)] for the rows under a table header."""
        rows = []
        for i in range(header_line + 1, len(self.masked)):
            line = self.masked[i].strip()
            if not line.startswith("|"):
                break
            if re.match(r"^\|[\s:|-]+\|$", line):
                continue
            rows.append((i, cells(line)))
        return rows

    def find_line(self, span, exact: str = None, prefix: str = None):
        if span is None:
            return None
        for i in range(*span):
            line = self.masked[i].strip()
            if (exact is not None and line == exact) or (
                    prefix is not None and line.startswith(prefix)):
                return i
        return None

    def mermaid_in(self, span) -> list[tuple[int, int, list[str]]]:
        if span is None:
            return []
        return [m for m in self.mermaid if span[0] <= m[0] < span[1]]


def cells(line: str) -> list[str]:
    parts = re.split(r"(?<!\\)\|", line.strip())[1:-1]
    return [p.strip().replace("\\|", "|") for p in parts]


def plain(value: str) -> str:
    """A cell value without the backticks a path is often written in."""
    return value.strip().strip("`").strip()


def listed(cell: str) -> list[str]:
    """Comma-separated values; an empty cell or a dash means none."""
    value = cell.strip()
    if value in ("", "-", "\u2013", "\u2014"):
        return []
    return [collapse(part) for part in value.split(",") if part.strip()]


# ------------------------------------------------------------- context


def specification_cqs(spec: Path | None = None) -> list[str]:
    """The CQ ids in section 7 of the specification in force, in order."""
    if spec is None:
        specs = layout.components("specification")
        if len(specs) != 1:
            raise Refused("the layout contract declares %d specifications; "
                          "which one's competency questions are in force?"
                          % len(specs))
        spec = specs[0].resolve()
    lines = spec.read_text(encoding="utf-8").split("\n")
    try:
        start = next(i for i, line in enumerate(lines)
                     if re.match(r"^## 7\. Competency questions\s*$", line))
    except StopIteration:
        raise Refused("%s has no `## 7. Competency questions` section; "
                      "where are the competency questions?" % spec.name)
    found = []
    for line in lines[start + 1:]:
        if line.startswith("## "):
            break
        match = re.match(r"^\| (CQ-\d+)\b", line)
        if match:
            found.append(match.group(1))
    if not found:
        raise Refused("%s section 7 lists no CQ-n row; was the table moved?"
                      % spec.name)
    if len(found) != len(set(found)):
        raise Refused("%s section 7 lists a CQ twice: %s"
                      % (spec.name, sorted({c for c in found
                                            if found.count(c) > 1})))
    return found


def _prefixes(text: str) -> dict[str, str]:
    return dict(re.findall(r"^@prefix\s+(\w+):\s*<([^>]+)>\s*\.", text,
                           flags=re.M))


def known_terms() -> set[str]:
    """`prefix:local` for every term a token may name.

    Upstream: every subject typed in a vendored extract, under the prefix
    and namespace its pin declares. Vocabulary: every skos:Concept or
    skos:ConceptScheme in the generated vocabulary Turtle, under the
    prefixes that Turtle binds. Read with rdflib, so the answer does not
    depend on how a generator happens to lay out its lines.
    """
    import rdflib
    import yaml

    root = layout.repository_root()
    rdf_type = rdflib.RDF.type
    out: set[str] = set()

    pins = yaml.safe_load((root / "config/upstream-sources.yaml").read_text(
        encoding="utf-8")) or {}
    for pin in pins.get("sources") or []:
        if pin.get("prefix") not in UPSTREAM_PREFIXES:
            continue
        graph = rdflib.Graph()
        graph.parse(root / pin["extract"], format="turtle")
        namespace = pin["namespace"]
        for subject in set(graph.subjects(rdf_type, None)):
            iri = str(subject)
            if isinstance(subject, rdflib.URIRef) and iri.startswith(
                    namespace):
                out.add("%s:%s" % (pin["prefix"], iri[len(namespace):]))

    skos = rdflib.Namespace("http://www.w3.org/2004/02/skos/core#")
    for path in layout.vocabulary_files():
        text = path.read_text(encoding="utf-8")
        bound = {p: ns for p, ns in _prefixes(text).items()
                 if p in VOCABULARY_PREFIXES}
        if not bound:
            continue
        graph = rdflib.Graph()
        graph.parse(data=text, format="turtle")
        for kind in (skos.Concept, skos.ConceptScheme):
            for subject in graph.subjects(rdf_type, kind):
                iri = str(subject)
                for prefix, namespace in bound.items():
                    if iri.startswith(namespace):
                        out.add("%s:%s" % (prefix, iri[len(namespace):]))
    return out


# -------------------------------------------------------------- checks


def check_header(model: Model) -> dict:
    first = model.lines[0] if model.lines else ""
    title = TITLE.match(first)
    named = MODEL_NAME.match(model.path.name)
    if not named:
        model.finding(None, "the file is not named CM-<nn>-<words>.md; "
                      "which model is it?")
    if not title:
        model.finding(0, "line 1 is not `# CM-NN \u2014 <Title>`; what is "
                      "this model's identifier and title?")
    fields: dict[str, str] = {}
    scope = model.section(SECTIONS[0])
    limit = scope[0] - 1 if scope else len(model.lines)
    header = next((i for i in range(limit)
                   if model.masked[i].strip() == FIELD_HEADER), None)
    if header is None:
        model.finding(None, "no `%s` table before section 1; where are "
                      "the model identifier, title, version and status?"
                      % FIELD_HEADER)
    else:
        for line, row in model.table(header):
            if len(row) != 2:
                model.finding(line, "a Field/Value row with %d cells"
                              % len(row))
                continue
            if row[0] in fields:
                model.finding(line, "the field %r is stated twice; which "
                              "value is meant?" % row[0])
            fields[row[0]] = row[1]
        for name in REQUIRED_FIELDS:
            if not fields.get(name):
                model.finding(header, "the Field/Value table has no %r row"
                              % name)
    identifier = fields.get("Model identifier")
    ids = {"file": named.group(1) if named else None,
           "title": title.group(1) if title else None,
           "table": identifier}
    stated = {v for v in ids.values() if v}
    if len(stated) > 1:
        model.finding(header, "the model identifier disagrees with itself "
                      "(file %s, title %s, table %s); which is it?"
                      % (ids["file"], ids["title"], ids["table"]))
    return {"identifier": identifier or ids["title"] or ids["file"],
            "title": fields.get("Title") or (title.group(2) if title
                                             else ""),
            "version": fields.get("Version", ""),
            "status": fields.get("Status", ""),
            "fields": fields}


def check_sections(model: Model) -> None:
    positions = []
    for title in SECTIONS:
        found = [i for i, level, text in model.headings
                 if level == 2 and text == title]
        if not found:
            model.finding(None, "no `## %s` heading; the standard's section "
                          "5 requires this deliverable" % title)
        elif len(found) > 1:
            model.finding(found[1], "`## %s` appears %d times; which one is "
                          "the section?" % (title, len(found)))
        else:
            positions.append((found[0], title))
    for (a, first), (b, second) in zip(positions, positions[1:]):
        if b < a:
            model.finding(b, "`## %s` comes before `## %s`; the ten "
                          "sections are read in order" % (second, first))


def check_patterns(model: Model) -> list[str]:
    span = model.section(SECTIONS[2])
    ids = []
    for line, text, end in model.subsections(span):
        match = PATTERN.match(text)
        if not match:
            continue
        if match.group(1) in ids:
            model.finding(line, "pattern %s is declared twice"
                          % match.group(1))
        ids.append(match.group(1))
        if not model.mermaid_in((line, end)):
            model.finding(line, "pattern %s has no ```mermaid diagram; "
                          "what does it show?" % match.group(1))
    if span is not None and not ids:
        model.finding(span[0] - 1, "section 3 holds no `### P<n> \u2014 "
                      "<name>` pattern")
    return ids


def check_readings(model: Model) -> None:
    for start, end, _body in model.mermaid:
        following = end + 1
        while following < len(model.lines) and \
                not model.lines[following].strip():
            following += 1
        if following >= len(model.lines) or \
                not model.lines[following].startswith(READING):
            model.finding(start, "this diagram is not followed by a "
                          "paragraph beginning `%s`; standard section 2.5 "
                          "requires a textual explanation beside every "
                          "diagram" % READING)


def parse_diagram(model: Model, start: int, body: list[str]):
    """(node labels, edge labels), each [(line, label)], for one block."""
    labels: dict[str, tuple[int, str]] = {}
    used: dict[str, int] = {}
    edges: list[tuple[int, str]] = []
    seen_header = False

    def node(line: int, ident: str, shape: str | None) -> None:
        used.setdefault(ident, line)
        if not shape:
            return
        label = collapse(re.search(r'"([^"]*)"', shape).group(1))
        if ident in labels and labels[ident][1] != label:
            model.finding(line, "node %s is labelled %r here and %r on line "
                          "%d; which is it?" % (ident, label,
                                                labels[ident][1],
                                                labels[ident][0] + 1))
            return
        labels.setdefault(ident, (line, label))

    for offset, raw in enumerate(body):
        line = start + 1 + offset
        text = raw.strip()
        if not text or text.startswith("%%"):
            continue
        if not seen_header:
            if not FLOWCHART.match(text):
                model.finding(line, "a diagram begins %r; the contract is "
                              "`flowchart LR`, `flowchart TB` or "
                              "`flowchart TD`" % text[:40])
                return [], []
            seen_header = True
            continue
        if IGNORED.match(text):
            continue
        edge = EDGE_LINE.match(text)
        if edge:
            node(line, edge.group(1), edge.group(2))
            edges.append((line, collapse(edge.group(4))))
            node(line, edge.group(5), edge.group(6))
            continue
        alone = NODE_LINE.match(text)
        if alone and alone.group(2):
            node(line, alone.group(1), alone.group(2))
            continue
        model.finding(line, "diagram line %r is outside the Mermaid subset "
                      "the checker reads: a node `Id[\"Label\"]` (or one of "
                      "the four other quoted shapes), or one edge "
                      "`A -->|label| B` per line" % text[:60])
    for ident, line in sorted(used.items(), key=lambda kv: kv[1]):
        if ident not in labels:
            model.finding(line, "node %s is never given a quoted label; "
                          "which concept is it?" % ident)
    return [labels[i] for i in sorted(labels, key=lambda k: labels[k][0])], \
        edges


def check_concepts(model: Model) -> list[str]:
    span = model.section(SECTIONS[3])
    names = []
    for line, text, end in model.subsections(span):
        name = collapse(text)
        if name in names:
            model.finding(line, "concept %r is described twice" % name)
        names.append(name)
        body = [model.masked[i].strip() for i in range(line + 1, end)]
        for bullet in CONCEPT_BULLETS:
            if not any(b.startswith(bullet) for b in body):
                model.finding(line, "concept %r has no `%s` bullet "
                              "(standard section 4.2)" % (name, bullet))
    if span is not None and not names:
        model.finding(span[0] - 1, "section 4 describes no concept")
    return names


def check_relationships(model: Model, concepts: list[str]):
    span = model.section(SECTIONS[4])
    header = model.find_line(span, exact=RELATIONSHIP_HEADER)
    ids, relationships = [], set()
    if span is None:
        return ids, relationships
    if header is None:
        model.finding(span[0] - 1, "section 5 has no table headed `%s`"
                      % RELATIONSHIP_HEADER)
        return ids, relationships
    for line, row in model.table(header):
        if len(row) != 7:
            model.finding(line, "a relationship row with %d cells; the "
                          "header has 7" % len(row))
            continue
        rid, name, origin, target = row[0], collapse(row[1]), row[2], row[3]
        if not RL_ID.match(rid):
            model.finding(line, "relationship id %r is not RL-NN" % rid)
        elif rid in ids:
            model.finding(line, "relationship id %s is used twice" % rid)
        ids.append(rid)
        if not name:
            model.finding(line, "%s names no relationship" % rid)
        relationships.add(name)
        for column, cell in (("From", origin), ("To", target)):
            for concept in (collapse(c) for c in cell.split(" or ")):
                if concept not in concepts:
                    model.finding(line, "%s %s names %r, which is not a "
                                  "concept described in section 4"
                                  % (rid, column, concept))
    if not ids:
        model.finding(header, "the relationship table has no rows")
    return ids, relationships


def check_diagrams(model: Model, concepts: list[str],
                   relationships: set[str]) -> None:
    drawn, linked = set(), set()
    for start, _end, body in model.mermaid:
        nodes, edges = parse_diagram(model, start, body)
        for line, label in nodes:
            drawn.add(label)
            if label not in concepts:
                model.finding(line, "diagram node %r is not a concept "
                              "heading in section 4" % label)
        for line, label in edges:
            linked.add(label)
            if label not in relationships:
                model.finding(line, "diagram edge %r is not a Relationship "
                              "in the section 5 table" % label)
    for concept in concepts:
        if concept not in drawn:
            model.finding(None, "concept %r appears in no diagram" % concept)
    for name in sorted(relationships):
        if name and name not in linked:
            model.finding(None, "relationship %r appears in no diagram"
                          % name)


def decision_value(model: Model, line: int, value: str, root: Path,
                   what: str) -> str:
    value = plain(value)
    if value in ("pending", "no"):
        return value
    if not value.startswith(DECISIONS_DIR):
        model.finding(line, "%s is %r; it is `pending` or a path under %s"
                      % (what, value, DECISIONS_DIR))
    elif not (root / value).is_file():
        model.finding(line, "%s cites %s, which does not exist" % (what,
                                                                   value))
    return value


def check_decisions(model: Model, root: Path) -> list[tuple[str, str]]:
    span = model.section(SECTIONS[6])
    found = []
    for line, text, end in model.subsections(span):
        match = DP.match(text)
        if not match:
            continue
        dp = match.group(1)
        if dp in [d for d, _ in found]:
            model.finding(line, "decision point %s is declared twice" % dp)
        decisions = [(i, DECISION.match(model.masked[i].strip()))
                     for i in range(line + 1, end)]
        decisions = [(i, m) for i, m in decisions if m]
        if len(decisions) != 1:
            model.finding(line, "%s has %d `**Decision:**` lines; it says "
                          "exactly once what was decided" % (dp,
                                                             len(decisions)))
            value = "pending"
        else:
            value = decision_value(model, decisions[0][0],
                                   decisions[0][1].group(1), root,
                                   "%s's decision" % dp)
            if value == "no":
                model.finding(decisions[0][0], "%s's decision is `no`; it "
                              "is `pending` or a decision record" % dp)
        options = next((i for i in range(line + 1, end)
                        if model.masked[i].strip() == "#### Options"), None)
        if options is None:
            model.finding(line, "%s has no `#### Options` heading" % dp)
        else:
            count = sum(1 for i in range(options + 1, end)
                        if OPTION.match(model.masked[i].strip()))
            if count < 2:
                model.finding(options, "%s lists %d `**Option <Letter>` "
                              "paragraph(s); a decision needs at least two"
                              % (dp, count))
        found.append((dp, value))
    return found


def check_traceability(model: Model, cqs: list[str], patterns: list[str],
                       concepts: list[str], relationship_ids: list[str]):
    span = model.section(SECTIONS[7])
    header = model.find_line(span, prefix="| CQ | Question |")
    traced = []
    if span is None:
        return traced
    if header is None:
        model.finding(span[0] - 1, "section 8 has no table headed "
                      "`| CQ | Question | ...`")
        return traced
    columns = cells(model.masked[header])
    where = {}
    for name in ("Patterns", "Concepts", "Relationships"):
        if name not in columns:
            model.finding(header, "the traceability table has no %r column"
                          % name)
        else:
            where[name] = columns.index(name)
    for line, row in model.table(header):
        if len(row) != len(columns):
            model.finding(line, "a traceability row with %d cells; the "
                          "header has %d" % (len(row), len(columns)))
            continue
        # The id, then whatever marks the specification puts beside it
        # (`CQ-4 ‡`, `CQ-2 *(rev. v0.4)*`) -- read as the
        # specification's own table is read.
        match = CQ_ID.match(row[0])
        if not match:
            model.finding(line, "%r is not a CQ id" % row[0])
            continue
        cq = match.group(1)
        if cq in traced:
            model.finding(line, "%s is traced twice" % cq)
        traced.append(cq)
        for name, known in (("Patterns", patterns), ("Concepts", concepts),
                            ("Relationships", relationship_ids)):
            if name not in where:
                continue
            for value in listed(row[where[name]]):
                if value not in known:
                    model.finding(line, "%s's %s names %r, which the model "
                                  "does not define" % (cq, name, value))
    missing = [c for c in cqs if c not in traced]
    extra = [c for c in traced if c not in cqs]
    if missing:
        model.finding(header, "the specification's competency questions %s "
                      "are not traced" % ", ".join(missing))
    if extra:
        model.finding(header, "%s are traced but are not competency "
                      "questions of the specification in force"
                      % ", ".join(extra))
    return traced


def check_questions(model: Model) -> list[str]:
    """Returns the open questions that block approval."""
    span = model.section(SECTIONS[8])
    blocking = []
    if span is None:
        return blocking
    subs = {text: (line, end) for line, text, end in model.subsections(span)}
    for title in ("Assumptions", "Open questions"):
        if title not in subs:
            model.finding(span[0] - 1, "section 9 has no `### %s`" % title)
    for title, pattern, prefix in (("Assumptions", ASSUMPTION, "A"),
                                   ("Open questions", QUESTION, "Q")):
        if title not in subs:
            continue
        line, end = subs[title]
        items = []
        for i in range(line + 1, end):
            text = model.masked[i]
            if not LIST_ITEM.match(text):
                continue
            match = pattern.match(text)
            if not match:
                model.finding(i, "an item under %s does not begin with its "
                              "%s-NN id" % (title, prefix))
                continue
            items.append((i, match.group(1)))
        seen = []
        for index, (i, ident) in enumerate(items):
            if ident in seen:
                model.finding(i, "%s is numbered twice" % ident)
            seen.append(ident)
            if prefix != "Q":
                continue
            stop = items[index + 1][0] if index + 1 < len(items) else end
            block = "\n".join(model.masked[i:stop])
            marks = block.count(CARRIED) + block.count(BLOCKS)
            if marks != 1:
                model.finding(i, "%s carries %d of the markers `%s` and "
                              "`%s`; it says exactly once whether it can "
                              "wait" % (ident, marks, CARRIED, BLOCKS))
            elif BLOCKS in block:
                blocking.append(ident)
    return blocking


def check_review(model: Model, root: Path, pending: list[str],
                 blocking: list[str]) -> str:
    span = model.section(SECTIONS[9])
    if span is None:
        return "no"
    header = model.find_line(span, exact="| Item | State |")
    if header is None:
        model.finding(span[0] - 1, "section 10 has no `| Item | State |` "
                      "table")
        return "no"
    rows = {row[0]: (line, row[1]) for line, row in model.table(header)
            if len(row) == 2}
    if "Approved" not in rows:
        model.finding(header, "the review status table has no `Approved` "
                      "row; is the model approved or not?")
        return "no"
    line, value = rows["Approved"]
    approved = decision_value(model, line, value, root, "Approved")
    if approved == "pending":
        model.finding(line, "Approved is `pending`; it is `no` or an "
                      "approval record")
        approved = "no"
    if approved != "no" and (pending or blocking):
        model.finding(line, "the model is marked approved while %s; "
                      "standard section 4.6 requires material ambiguities "
                      "to be resolved before approval" % "; ".join(filter(
                          None, ["decision point(s) %s are pending"
                                 % ", ".join(pending) if pending else "",
                                 "open question(s) %s block approval"
                                 % ", ".join(blocking) if blocking
                                 else ""])))
    return approved


def check_tokens(model: Model, known: set[str]) -> int:
    exempt = set()
    for start, end, _body in model.mermaid:
        exempt.update(range(start, end + 1))
    count = 0
    for i, line in enumerate(model.lines):
        if i in exempt:
            continue
        for match in TOKEN.finditer(line):
            count += 1
            token = "%s:%s" % (match.group(1), match.group(2))
            if token in known:
                continue
            if match.group(1) in VOCABULARY_PREFIXES:
                model.finding(i, "%s is not a concept in the generated "
                              "vocabulary (src/01_controlled_vocabulary/"
                              "generated/)" % token)
            else:
                model.finding(i, "%s is not in the vendored extracts. Is "
                              "the IRI right? Verify it upstream and "
                              "re-vendor before citing it" % token)
    return count


def check_model(path: Path, cqs: list[str], known: set[str],
                root: Path) -> tuple[list[str], dict]:
    """(findings, record) for one model file."""
    data = path.read_bytes()
    if b"\r\n" in data:
        return (["%s: has CRLF line endings; the repository is LF "
                 "(.gitattributes)" % path.name], {})
    model = Model(path, data.decode("utf-8"))
    header = check_header(model)
    check_sections(model)
    patterns = check_patterns(model)
    check_readings(model)
    concepts = check_concepts(model)
    relationship_ids, relationships = check_relationships(model, concepts)
    check_diagrams(model, concepts, relationships)
    decisions = check_decisions(model, root)
    traced = check_traceability(model, cqs, patterns, concepts,
                                relationship_ids)
    blocking = check_questions(model)
    pending = [dp for dp, value in decisions if value == "pending"]
    approved = check_review(model, root, pending, blocking)
    tokens = check_tokens(model, known)
    record = {
        "path": path.name,
        "identifier": header["identifier"],
        "title": header["title"],
        "version": header["version"],
        "status": header["status"],
        "approved": approved,
        "patterns": len(patterns),
        "diagrams": len(model.mermaid),
        "concepts": len(concepts),
        "relationships": len(relationship_ids),
        "cqs_traced": len(traced),
        "decision_points": len(decisions),
        "decision_points_pending": len(pending),
        "open_questions_blocking": len(blocking),
        "tokens_checked": tokens,
    }
    return model.problems, record


def read_model(path: Path) -> dict:
    """Identifier, title, version, status and approval state, as the
    model states them -- what the site's Models page shows. No other
    check is made; the site build runs check() for that."""
    model = Model(path, path.read_bytes().decode("utf-8"))
    header = check_header(model)
    approved = "no"
    span = model.section(SECTIONS[9])
    header_line = model.find_line(span, exact="| Item | State |")
    if header_line is not None:
        for _line, row in model.table(header_line):
            if len(row) == 2 and row[0] == "Approved":
                approved = plain(row[1])
    return {"identifier": header["identifier"], "title": header["title"],
            "version": header["version"], "status": header["status"],
            "approved": approved}


# --------------------------------------------------------------- runner


def model_paths() -> tuple[list[Path], list[str]]:
    """(models, findings about other files in the models directory)."""
    entry = layout.component(COMPONENT)
    if entry.role != ROLE:
        raise Refused("%s is declared with role %s; the checker reads the "
                      "%s role" % (COMPONENT, entry.role, ROLE))
    directory = entry.resolve()
    models, problems = [], []
    readme = layout.component("stage.02-conceptual-models.readme").path
    for path in sorted(directory.iterdir(), key=lambda p: p.name):
        rel = path.relative_to(layout.repository_root()).as_posix()
        if rel == readme:
            continue
        if path.is_file() and MODEL_NAME.match(path.name):
            models.append(path)
        else:
            problems.append("%s: only CM-<nn>-<words>.md models and the "
                            "README belong in %s; what is this?"
                            % (rel, entry.path))
    ids = [MODEL_NAME.match(p.name).group(1) for p in models]
    for ident in sorted({i for i in ids if ids.count(i) > 1}):
        problems.append("%s: two files claim this identifier; which is the "
                        "model?" % ident)
    return models, problems


def check(paths: list[Path] | None = None, spec: Path | None = None,
          known: set[str] | None = None) -> tuple[list[str], list[dict]]:
    """(findings, one record per model). `paths` defaults to every model
    in the conceptual-models component."""
    root = layout.repository_root()
    problems: list[str] = []
    if paths is None:
        paths, problems = model_paths()
    if not paths:
        return problems, []
    cqs = specification_cqs(spec)
    known = known_terms() if known is None else known
    records = []
    for path in paths:
        found, record = check_model(Path(path), cqs, known, root)
        problems.extend(found)
        if record:
            records.append(record)
    return problems, records


def summary(records: list[dict]) -> str:
    if not records:
        return ("ok: no conceptual model yet (src/02_conceptual_models/"
                "CM-*.md); nothing to check")
    total = {key: sum(r[key] for r in records) for key in (
        "patterns", "diagrams", "concepts", "relationships", "cqs_traced",
        "decision_points_pending")}
    return ("ok: %d model(s), %d pattern(s), %d diagram(s), %d concept(s), "
            "%d relationship(s), %d CQ(s) traced, %d decision point(s) "
            "pending" % (len(records), total["patterns"], total["diagrams"],
                         total["concepts"], total["relationships"],
                         total["cqs_traced"],
                         total["decision_points_pending"]))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("paths", nargs="*", type=Path)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)

    problems, records = check(args.paths or None)
    if args.json:
        print(json.dumps({"findings": problems, "models": records},
                         indent=2, sort_keys=True))
        return 1 if problems else 0
    if problems:
        for problem in problems:
            print("  FINDING: %s" % problem)
        print("  %d finding(s) across %d model(s)" % (len(problems),
                                                     len(records)))
        return 1
    print("  " + summary(records))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
