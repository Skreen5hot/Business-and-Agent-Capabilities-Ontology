# SPDX-License-Identifier: MIT
"""Read the Terms tables of specification section 4 (ADR-003 D4).

    python tools/vocab/spec_terms.py        # list the rows it finds

ADR-003 D4: a metamodel concept's definition comes from the Terms tables
of the specification in force, and nowhere else. This module finds those
tables and classifies every row, so that the build never has to guess
which rows are terms.

WHAT A TERM TABLE IS

A Markdown table inside `## 4. Terms` (up to the next `## ` heading)
whose header cells are exactly `Term | Definition | Parents | Does not
imply` (or `Parent`). The section's other table, the annotation
properties (`Term | Use | Value`), has a different header and is not a
term table: it is reported as skipped, by name, not silently dropped.

HOW A ROW IS CLASSIFIED -- the rule the tests pin

A row is CONCRETE when its Term cell is exactly

    <Label> `<p>:<LocalName>`           optionally followed by *(...)*

where the label is plain words (no backtick, bracket or angle bracket),
the code span holds one name with no placeholder, <p> is `ex:` (the
prefix v0.4 writes for BCO terms) or `bco:` (v0.5's correction), and the label
with every non-alphanumeric character removed equals the local name
("Capability Target-State Specification" -> CapabilityTargetStateSpecification).
A row that has that shape but whose label and local name disagree is a
FAILURE, not an exclusion: the spec has a typo or the rule is wrong, and
either way a person must look.

A row is a TEMPLATE, excluded with its reason, when its Term cell

  - names a placeholder pattern: the code span holds `<...>`
    (`ex:<Name>Realization`, `bco:<Name>Realization`);
  - names a family by one example, in a parenthetical that says "and the
    rest": an IRI (v0.4, `(`ex:StrategicPlanningCapability` and the
    rest)`) or plain words (v0.5, `(strategic planning capability and
    the rest)`); or
  - names no IRI because its representation is open: a plain label and a
    note that says "representation open" (v0.5, `Functional Adequacy
    Assessment *(new, R9; representation open)*`, whose parent is "To be
    chosen at Stage 05 (CD17)"). Nothing can wrap a row with no IRI.

Any other row is a FAILURE. A new row in a shape nobody anticipated is
reported rather than classified by a guess in either direction.

For a concrete row the Parents cell must be one or more code spans of
`prefix:local`, separated by commas, optionally followed by a full stop
and prose (v0.5's parent row: "... `obo:BFO_0000016`. Admitted by the
architect's ratification ..."). The prose is kept verbatim as the row's
parents note, and the record digest covers it. A row without one has no
`parents_note` key, so the digest of every v0.4 row is unchanged.

Cell text is kept verbatim (stripped of surrounding whitespace),
Markdown and all: D4 requires the built definition to equal the row's
text, and the row's text includes its backticks.
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

SECTION = re.compile(r"^## 4\.\s+Terms\s*$")
NEXT_SECTION = re.compile(r"^## ")
LAYER = re.compile(r"^\*\*([^*]+)\*\*")
TERM_HEADERS = (
    ("Term", "Definition", "Parents", "Does not imply"),
    ("Term", "Definition", "Parent", "Does not imply"),
)
CONCRETE = re.compile(
    r"^(?P<label>[A-Za-z][^`()<>*]*?)\s+"
    r"`(?P<prefix>ex|bco):(?P<local>[A-Za-z][A-Za-z0-9]*)`"
    r"(?:\s+\*\((?P<note>[^)]*)\)\*)?$")
PLACEHOLDER_IRI = re.compile(r"`(?:ex|bco):[^`]*<[^`>]+>[^`]*`")
FAMILY_EXAMPLE = re.compile(
    r"\(\s*(?:`(?:ex|bco):[A-Za-z0-9]+`|[a-z][a-z ]*[a-z])"
    r"\s+and the rest\s*\)")
REPRESENTATION_OPEN = re.compile(
    r"^[A-Za-z][^`()<>*]*?\s+\*\((?:[^)]*;\s*)?representation open\)\*$")
PARENT = re.compile(r"`([a-z]+):([A-Za-z_][A-Za-z0-9_]*)`")
PARENTS_CELL = re.compile(
    r"^(?P<spans>`[a-z]+:[A-Za-z_][A-Za-z0-9_]*`"
    r"(?:\s*,\s*`[a-z]+:[A-Za-z_][A-Za-z0-9_]*`)*)"
    r"(?:\.\s+(?P<note>\S.*))?$")


@dataclass(frozen=True)
class Row:
    """One concrete Terms row."""

    layer: str
    label: str
    local: str
    note: str
    definition: str
    parents: tuple  # of (prefix, local)
    does_not_imply: str
    line: int
    prefix: str = "ex"
    parents_note: str = ""

    @property
    def spec_iri(self) -> str:
        return "%s:%s" % (self.prefix, self.local)

    def content(self) -> dict:
        """What the row says, as the record digest includes it."""
        out = {
            "label": self.label,
            "iri": self.spec_iri,
            "definition": self.definition,
            "parents": ["%s:%s" % p for p in self.parents],
            "does_not_imply": self.does_not_imply,
        }
        if self.parents_note:
            out["parents_note"] = self.parents_note
        return out


@dataclass
class Parsed:
    rows: list = field(default_factory=list)
    excluded: list = field(default_factory=list)  # (line, term cell, reason)
    skipped_tables: list = field(default_factory=list)  # (line, layer, header)
    failures: list = field(default_factory=list)  # (line, message)


def cells(line: str) -> list:
    text = line.strip()
    if text.startswith("|"):
        text = text[1:]
    if text.endswith("|"):
        text = text[:-1]
    return [cell.strip() for cell in text.split("|")]


def squash(label: str) -> str:
    return re.sub(r"[^A-Za-z0-9]", "", label)


def classify(term: str):
    """('concrete', match) | ('template', reason) | ('unknown', reason)."""
    match = CONCRETE.fullmatch(term)
    if match:
        return "concrete", match
    if PLACEHOLDER_IRI.search(term):
        return "template", "names a placeholder pattern, not an IRI"
    if FAMILY_EXAMPLE.search(term):
        return "template", ("names one example standing for a family "
                            "('and the rest'), not one term")
    if REPRESENTATION_OPEN.fullmatch(term):
        return "template", ("names no IRI: its representation is open, to "
                            "be chosen at Stage 05")
    return "unknown", "neither a concrete term nor a recognised template"


def parse_text(text: str) -> Parsed:
    out = Parsed()
    lines = text.split("\n")
    start = next((n for n, line in enumerate(lines) if SECTION.match(line)),
                 None)
    if start is None:
        out.failures.append((0, "no '## 4. Terms' section"))
        return out
    end = next((n for n in range(start + 1, len(lines))
                if NEXT_SECTION.match(lines[n])), len(lines))

    layer = ""
    n = start + 1
    tables = 0
    while n < end:
        line = lines[n]
        heading = LAYER.match(line)
        if heading:
            layer = heading.group(1).strip()
        if line.lstrip().startswith("|") and n + 1 < end \
                and re.match(r"^\s*\|[\s:|-]+\|\s*$", lines[n + 1]):
            header = tuple(cells(line))
            body_start = n + 2
            body_end = body_start
            while body_end < end and lines[body_end].lstrip().startswith("|"):
                body_end += 1
            if header not in TERM_HEADERS:
                out.skipped_tables.append((n + 1, layer, " | ".join(header)))
                n = body_end
                continue
            tables += 1
            for m in range(body_start, body_end):
                _row(out, layer, cells(lines[m]), m + 1)
            n = body_end
            continue
        n += 1
    if not tables:
        out.failures.append((start + 1, "section 4 has no Terms table"))
    elif not out.rows:
        out.failures.append((start + 1, "section 4's Terms tables have no "
                                        "concrete row"))
    locals_seen = {}
    for row in out.rows:
        if row.local in locals_seen:
            out.failures.append((row.line, "%s is named by two rows "
                                           "(lines %d and %d)"
                                 % (row.spec_iri, locals_seen[row.local],
                                    row.line)))
        locals_seen.setdefault(row.local, row.line)
    return out


def _row(out: Parsed, layer: str, row: list, line: int) -> None:
    if len(row) != 4:
        out.failures.append((line, "a Terms row has %d cells, not 4"
                             % len(row)))
        return
    term, definition, parents, does_not_imply = row
    kind, detail = classify(term)
    if kind == "template":
        out.excluded.append((line, term, detail))
        return
    if kind == "unknown":
        out.failures.append((line, "Terms row %r is %s" % (term, detail)))
        return
    label, local = detail.group("label").strip(), detail.group("local")
    if squash(label) != local:
        out.failures.append((line, "Terms row label %r does not spell its "
                                   "IRI ex:%s" % (label, local)))
        return
    prefix = detail.group("prefix")
    cell = PARENTS_CELL.fullmatch(parents)
    if not cell:
        out.failures.append((line, "%s:%s: the Parents cell %r is not a "
                                   "comma-separated list of code-span names"
                             % (prefix, local, parents)))
        return
    if not definition or not does_not_imply:
        out.failures.append((line, "%s:%s has an empty Definition or Does "
                                   "not imply cell" % (prefix, local)))
        return
    out.rows.append(Row(layer=layer, label=label, local=local,
                        note=(detail.group("note") or "").strip(),
                        definition=definition,
                        parents=tuple(PARENT.findall(cell.group("spans"))),
                        does_not_imply=does_not_imply, line=line,
                        prefix=prefix,
                        parents_note=(cell.group("note") or "").strip()))


def parse(path: Path) -> Parsed:
    return parse_text(path.read_bytes().decode("utf-8"))


def main(argv=None) -> int:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    import layout

    specs = layout.components("specification")
    if len(specs) != 1:
        print("expected one specification in force, found %d" % len(specs))
        return 1
    parsed = parse(specs[0].resolve())
    for row in parsed.rows:
        print("concrete  line %-4d %-12s %s  (%s)"
              % (row.line, row.layer[:12], row.spec_iri, row.label))
    for line, term, reason in parsed.excluded:
        print("excluded  line %-4d %s -- %s" % (line, term, reason))
    for line, layer, header in parsed.skipped_tables:
        print("skipped   line %-4d table under %r: %s" % (line, layer, header))
    for line, message in parsed.failures:
        print("FAILURE   line %-4d %s" % (line, message))
    print("%d concrete row(s), %d excluded, %d failure(s)"
          % (len(parsed.rows), len(parsed.excluded), len(parsed.failures)))
    return 1 if parsed.failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
