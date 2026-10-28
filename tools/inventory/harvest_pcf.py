# SPDX-License-Identifier: MIT
"""Harvest the APQC PCF into internal evidence; publish only its status.

    python tools/inventory/harvest_pcf.py                  # offline check
    python tools/inventory/harvest_pcf.py --write          # write internal outputs and the status record
    python tools/inventory/harvest_pcf.py --confirm        # fetch the workbook from GitHub, require the status record
    python tools/inventory/harvest_pcf.py --write --pcf80 PATH   # also the 7.4 -> 8.0 delta

Phase I-2b of the Capability Term Inventory, under the architect's
decisions of 2026-10-28: E2-E4 (docs/decisions/2026-10-28-i2-and-bpo-
repin-decided.md) and APQC-1 c, APQC80-1 a (docs/decisions/2026-10-28-
i2a-decided.md).

THE POSTURE, AND WHY TWO KINDS OF OUTPUT

APQC-1 c makes the public posture citation only, pending APQC's written
clarification: no PCF-derived entry -- name, description, code or
hierarchy -- is published in this repository or on the site, and (E2) no
substantial catalog structure. The same decision says to keep the
permitted internal evidence and locators, so that the work can continue
without harvesting the source again. So this tool writes two things:

  internal   .inventory-internal/i2b/ (gitignored, and declared
             `tracked: false` in the layout contract): the entries, with
             names, descriptions, hierarchy ids and locators as the
             workbook gives them; the E4 worksheet; and, once the
             architect supplies PCF 8.0, the delta. Never committed. The
             writer refuses any path outside the internal directory, and
             any path inside the repository that git tracks or does not
             ignore.

  public     docs/sources/inventory/pcf-status.yaml: the citation (work,
             edition, rights holder, BPO locator and workbook digest), the
             posture, aggregate counts per level, the sha256 of every
             internal output -- so the internal evidence is provably the
             one reviewed -- and the state of 8.0 and of E4. No name, no
             description, no element or hierarchy id, no parent. A guard
             refuses the record if any of those reaches it (below).

THE SOURCE

The PCF 7.4 Cross-Industry Excel workbook as committed in BPO, pinned in
config/inventory-sources.yaml (the `apqc.evidence` item that is an .xlsx)
by commit, path and sha256 -- read from there, not restated. It is read
from the cache only: .upstream-cache/bpo-<commit>/<sha256> (where
harvest_bpo.py --rebuild/--confirm put it) or .upstream-cache/i2a/<sha256>
(where rights.py --confirm puts it). --write and --confirm fetch it, when
it is not cached, from raw.githubusercontent.com at the pinned commit with
harvest_bpo.py's fetch, which requires the digest. Nothing is ever fetched
from apqc.org: its Terms forbid automated access.

The reader is the standard library's zipfile and ElementTree. It reads
the sheet named `Combined` (every element, one row each), finds its
columns by the header row, and refuses rather than guesses: a missing
column, an element id that is not an integer, a hierarchy id that is not
dotted digits or is held as a number (1.10 and 1.1 are then the same
number), a repeated element or hierarchy id, a parent that is not in the
sheet. Level 1 is `N.0`; level 2 is `N.M`; below that the level is the
number of components.

WHAT AN INTERNAL ENTRY IS

  pcf-category            level 1
  pcf-process-group       level 2
  pcf-level-3-unjudged    level 3. Not a standing-function candidate: E4
                          makes that a written judgement against CM-01's
                          Standing Function, with a reason, independent
                          evidence and a locator, approved by the
                          architect. It needs a reader of the node's name,
                          and whether APQC's Terms let an AI tool read PCF
                          content is question 6 of the clarification
                          request. So no judgement is made here; the E4
                          worksheet holds one empty row per level-3 node.

Ids are INV-PCF74-<element id>-<kind>; the element id is the PCF ID column,
which APQC keeps across editions. Level-3 entries carry BPO's bridge, as
evidence and not proof (ADR-001 R4/R6; I-1 found the bridge is not a
standing-function marker): the capability-class entries of the committed
docs/sources/inventory/bpo-entries.yaml whose `designated_by` names a
catalog node with that PCF code, and those whose own `pcf_code` is it. The
bridge is derived mechanically from that file, whose digest is recorded.

THE 8.0 DELTA

--pcf80 PATH reads a PCF 8.0 workbook the architect supplies (APQC80-1 a;
it is never committed unless its terms permit, E3). The tool records its
sha256 and size, requires it to be an xlsx, reads it with the same reader,
and writes the delta at levels 1-3, keyed by element id: added, retired,
renamed, re-coded (hierarchy id changed) and moved (parent changed); an
element can carry several. Internal only; the status record gets the
digests and the counts. Without the file, 8.0 is reported as a gap and the
run succeeds. Pinning 8.0's in-file notice in rights.yaml is a separate
I-2a amendment, not this tool's.

THE OFFLINE CHECK (default; CI)

The status record must be in the generator's form (re-rendering its data
gives its bytes), keep its closed schema, agree with the pins and the
rights record, keep its counts consistent, and pass the public guard: no
key that would hold catalog content, no string matching a PCF hierarchy id
or holding a run of five or more digits outside the fields whose values
are checked against the pins, the admission guard (no authored-namespace
IRI, no RDF, no ratification key; harvest_bpo.py's constants). When the
workbook is cached, the record must also be byte-identical to a fresh
build, no name or description or element id from the build may appear in
it, and internal outputs that exist must have the recorded digests. CI
has no cache, so it checks the shape and the guard; the weekly job runs
--confirm, which fetches the public workbook from GitHub and requires
byte identity.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import re
import subprocess
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import layout  # noqa: E402

FORMAT = 1
GENERATOR = "tools/inventory/harvest_pcf.py"
HARVEST = "tools/inventory/harvest_bpo.py"
RIGHTS_TOOL = "tools/inventory/rights.py"
RIGHTS = "docs/sources/inventory/rights.yaml"
BPO_ENTRIES = "docs/sources/inventory/bpo-entries.yaml"
STATUS = "docs/sources/inventory/pcf-status.yaml"
INTERNAL = ".inventory-internal/i2b"
DECISION = "docs/decisions/2026-10-28-i2a-decided.md"
AUTHORITY = "docs/decisions/2026-10-28-i2-and-bpo-repin-decided.md"
CM01 = "src/02_conceptual_models/CM-01-business-capability.md"
CACHE = ".upstream-cache"
RIGHTS_74 = "apqc-pcf-7.4"
RIGHTS_80 = "apqc-pcf-8.0"

ENTRIES_FILE = "pcf-7.4-entries.yaml"
WORKSHEET_FILE = "pcf-7.4-e4-worksheet.yaml"
DELTA_FILE = "pcf-7.4-to-8.0-delta.yaml"

ENTRY_PREFIX = "INV-PCF74"
KIND_BY_LEVEL = {1: "pcf-category", 2: "pcf-process-group",
                 3: "pcf-level-3-unjudged"}
INTERNAL_RIGHTS = "apqc-1c-internal-only"
CHANGES = ("added", "retired", "renamed", "recoded", "moved")

SHEET = "Combined"
#: The columns read, by header text (case and spacing ignored). The
#: other columns (the 7.3 difference index and change details, the metrics
#: flag) are not read.
COLUMNS = {"element_id": "PCF ID", "hierarchy_id": "Hierarchy ID",
           "name": "Name", "description": "Element Description"}

MAIN = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
REL = ("{http://schemas.openxmlformats.org/officeDocument/2006/"
       "relationships}id")
XLSX_TYPE = b"spreadsheetml.sheet.main"

ELEMENT_ID = re.compile(r"^\d+$")
HIERARCHY_ID = re.compile(r"^\d+(?:\.\d+)+$")
HEX64 = re.compile(r"^[0-9a-f]{64}$")
#: A PCF hierarchy id, at any level including N.0 and N.M; wider than
#: rights.py's pattern (three components), because here levels 1 and 2
#: are what the record must not carry.
PCF_HIERARCHY = re.compile(r"(?<![\d.])\d{1,2}\.\d{1,2}(?:\.\d{1,2})*(?![\d])")
#: A run of digits as long as a PCF element id.
DIGIT_RUN = re.compile(r"\d{5,}")
#: Keys whose values hold hex digests or commits, not prose.
HEX_KEYS = ("sha256", "commit")


class Refused(SystemExit):
    """A question for whoever supplied the input, not for this tool."""


def root() -> Path:
    return layout.repository_root()


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


_MODULES: dict = {}


def _module(base: Path, relative: str, name: str):
    """A sibling tool, imported by path once per file and content."""
    path = base / relative
    key = (str(path.resolve()), sha256(path.read_bytes()))
    if key not in _MODULES:
        spec = importlib.util.spec_from_file_location(name, path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        _MODULES[key] = module
    return _MODULES[key]


_NAMESPACES: dict = {}


def authored_namespaces(base: Path) -> tuple:
    """harvest_bpo.py's reading of AUTHORED_NAMESPACES, once per validator."""
    path = base / "tools/ontology/validate.py"
    key = (str(path.resolve()), sha256(path.read_bytes()))
    if key not in _NAMESPACES:
        _NAMESPACES[key] = harvest_module(base).authored_namespaces(base)
    return _NAMESPACES[key]


def harvest_module(base: Path):
    return _module(base, HARVEST, "bco_harvest_bpo_for_pcf")


def rights_module(base: Path):
    return _module(base, RIGHTS_TOOL, "bco_rights_for_pcf")


def parse_yaml(text):
    import yaml

    loader = getattr(yaml, "CSafeLoader", yaml.SafeLoader)
    return yaml.load(text, Loader=loader)


def dump(data) -> str:
    import yaml

    return yaml.safe_dump(data, sort_keys=False, allow_unicode=True,
                          width=79, default_flow_style=False)


def header(lines) -> str:
    return "".join("# %s\n" % line if line else "#\n" for line in lines)


# ------------------------------------------------------------------ pins


def workbook_pin(base: Path) -> dict:
    """The 7.4 workbook as config/inventory-sources.yaml pins it."""
    harvest = harvest_module(base)
    source = harvest.pins(base)
    found = [i for i in source["apqc"]["evidence"]
             if str(i["path"]).endswith(".xlsx")]
    if len(found) != 1:
        raise Refused("config/inventory-sources.yaml pins %d .xlsx APQC "
                      "evidence item(s); which one is the PCF workbook?"
                      % len(found))
    return {"repository": source["repository"],
            "raw_base": source["raw_base"], "commit": source["commit"],
            "path": found[0]["path"], "sha256": found[0]["sha256"]}


def rights_citation(base: Path) -> dict:
    """Rights holder, work, edition and register id, from rights.yaml."""
    data = parse_yaml((base / RIGHTS).read_bytes().decode("utf-8"))
    out = {}
    for item in data.get("sources") or []:
        if item.get("id") in (RIGHTS_74, RIGHTS_80):
            out[item["id"]] = {k: item[k] for k in
                               ("rightsholder", "work", "edition",
                                "register", "status")}
    for sid in (RIGHTS_74, RIGHTS_80):
        if sid not in out:
            raise Refused("%s has no source %r; what is the citation?"
                          % (RIGHTS, sid))
    return out


def cached_workbook(base: Path, pin: dict, cache: Path) -> bytes | None:
    """The pinned bytes from either cache, or None. Never the network."""
    for path in (cache / ("bpo-" + pin["commit"]) / pin["sha256"],
                 cache / "i2a" / pin["sha256"]):
        if path.is_file():
            data = path.read_bytes()
            if sha256(data) == pin["sha256"]:
                return data
    return None


def fetched_workbook(base: Path, pin: dict, cache: Path) -> bytes:
    """The pinned bytes, from the cache or raw.githubusercontent.com."""
    cached = cached_workbook(base, pin, cache)
    if cached is not None:
        return cached
    harvest = harvest_module(base)
    source = {"raw_base": pin["raw_base"]}
    return harvest.fetch(harvest.raw_url(source, pin["commit"], pin["path"]),
                         pin["sha256"],
                         cache / ("bpo-" + pin["commit"]) / pin["sha256"],
                         pin["commit"])


# ---------------------------------------------------------------- reader


def require_xlsx(data: bytes, what: str) -> zipfile.ZipFile:
    import io

    try:
        archive = zipfile.ZipFile(io.BytesIO(data))
    except zipfile.BadZipFile:
        raise Refused("%s is not a zip archive, so not an xlsx workbook"
                      % what) from None
    names = set(archive.namelist())
    if "[Content_Types].xml" not in names or "xl/workbook.xml" not in names:
        raise Refused("%s is a zip archive without [Content_Types].xml and "
                      "xl/workbook.xml; it is not an xlsx workbook" % what)
    if XLSX_TYPE not in archive.read("[Content_Types].xml"):
        raise Refused("%s declares no spreadsheetml workbook part; is it an "
                      "xlsx (and not, say, a macro-enabled or strict "
                      "workbook)?" % what)
    return archive


def _cell_text(cell, shared):
    kind = cell.get("t")
    value = cell.find(MAIN + "v")
    if kind == "s":
        return shared[int(value.text)], True
    if kind == "inlineStr":
        return "".join(t.text or "" for t in cell.iter(MAIN + "t")), True
    if kind == "str":
        return (value.text if value is not None else None), True
    return (value.text if value is not None else None), False


def _column(ref: str) -> str:
    return re.sub(r"\d+$", "", ref)


def _norm(text: str) -> str:
    return " ".join(str(text).split()).casefold()


def read_workbook(data: bytes, what: str = "the workbook") -> dict:
    """{nodes: [...], rows_by_level: {...}, sheet, rows} from xlsx bytes.

    Structural refusals name the row and column, never a cell's value, so
    a refusal does not copy catalog content into a log.
    """
    archive = require_xlsx(data, what)
    shared = []
    if "xl/sharedStrings.xml" in archive.namelist():
        for item in ElementTree.fromstring(
                archive.read("xl/sharedStrings.xml")).findall(MAIN + "si"):
            shared.append("".join(t.text or "" for t in item.iter(MAIN + "t")))
    workbook = ElementTree.fromstring(archive.read("xl/workbook.xml"))
    rels = ElementTree.fromstring(archive.read("xl/_rels/workbook.xml.rels"))
    targets = {r.get("Id"): r.get("Target") for r in rels}
    sheets = []
    for sheet in workbook.find(MAIN + "sheets"):
        target = targets.get(sheet.get(REL), "")
        target = target.lstrip("/")
        if not target.startswith("xl/"):
            target = "xl/" + target
        sheets.append((sheet.get("name"), target))
    chosen = [s for s in sheets if s[0] == SHEET]
    if len(chosen) != 1:
        raise Refused("%s has %d sheet(s) named %r; the reader takes every "
                      "element from that one sheet. Has the layout changed?"
                      % (what, len(chosen), SHEET))
    sheet_name, target = chosen[0]
    rows = ElementTree.fromstring(archive.read(target)).findall(
        ".//" + MAIN + "row")
    if not rows:
        raise Refused("%s sheet %r has no rows" % (what, sheet_name))
    head = {}
    for cell in rows[0].findall(MAIN + "c"):
        text, _ = _cell_text(cell, shared)
        if text is not None:
            head[_norm(text)] = _column(cell.get("r"))
    columns = {}
    for key, title in COLUMNS.items():
        if _norm(title) not in head:
            raise Refused("%s sheet %r has no %r column in its header row "
                          "(row %s)" % (what, sheet_name, title,
                                        rows[0].get("r")))
        columns[key] = head[_norm(title)]

    nodes = []
    for row in rows[1:]:
        number = int(row.get("r"))
        values = {}
        for cell in row.findall(MAIN + "c"):
            values[_column(cell.get("r"))] = _cell_text(cell, shared)
        if all(v[0] in (None, "") for v in values.values()):
            continue
        where = "%s sheet %r row %d" % (what, sheet_name, number)
        eid, _ = values.get(columns["element_id"], (None, False))
        eid = (eid or "").strip()
        if re.fullmatch(r"\d+\.0+", eid):
            eid = eid.split(".")[0]
        if not ELEMENT_ID.match(eid):
            raise Refused("%s: the %r cell is not an integer element id"
                          % (where, COLUMNS["element_id"]))
        hid, is_text = values.get(columns["hierarchy_id"], (None, False))
        hid = (hid or "").strip()
        if not is_text:
            raise Refused("%s: the %r cell is a number, not text; 1.10 and "
                          "1.1 cannot be told apart once it is a number"
                          % (where, COLUMNS["hierarchy_id"]))
        if not HIERARCHY_ID.match(hid):
            raise Refused("%s: the %r cell is not dotted digits"
                          % (where, COLUMNS["hierarchy_id"]))
        name, _ = values.get(columns["name"], (None, False))
        if not name or not name.strip():
            raise Refused("%s: the %r cell is empty" % (where,
                                                        COLUMNS["name"]))
        description, _ = values.get(columns["description"], (None, False))
        parts = hid.split(".")
        level = 1 if len(parts) == 2 and int(parts[1]) == 0 else len(parts)
        if level == 1:
            parent = None
        elif level == 2:
            parent = parts[0] + ".0"
        else:
            parent = ".".join(parts[:-1])
        nodes.append({"element_id": eid, "hierarchy_id": hid,
                      "level": level, "parent_hierarchy_id": parent,
                      "name": name,
                      "description": description if description else None,
                      "sheet": sheet_name, "row": number})

    by_element, by_hierarchy = {}, {}
    for node in nodes:
        where = "%s sheet %r row %d" % (what, node["sheet"], node["row"])
        if node["element_id"] in by_element:
            raise Refused("%s repeats the element id of row %d"
                          % (where, by_element[node["element_id"]]["row"]))
        if node["hierarchy_id"] in by_hierarchy:
            raise Refused("%s repeats the hierarchy id of row %d"
                          % (where, by_hierarchy[node["hierarchy_id"]]["row"]))
        by_element[node["element_id"]] = node
        by_hierarchy[node["hierarchy_id"]] = node
    for node in nodes:
        parent = node.pop("parent_hierarchy_id")
        if parent is None:
            node["parent"] = None
            continue
        if parent not in by_hierarchy:
            raise Refused("%s sheet %r row %d: its parent is not in the sheet"
                          % (what, node["sheet"], node["row"]))
        node["parent"] = {"element_id": by_hierarchy[parent]["element_id"],
                          "hierarchy_id": parent}
    levels = {}
    for node in nodes:
        levels[node["level"]] = levels.get(node["level"], 0) + 1
    if not levels.get(1):
        raise Refused("%s has no level-1 element; is it the PCF?" % what)
    return {"sheet": sheet_name, "rows": len(nodes), "nodes": nodes,
            "rows_by_level": {"level_%d" % k: levels[k]
                              for k in sorted(levels)}}


# ---------------------------------------------------------------- bridge


def bpo_bridges(entries_document: dict) -> dict:
    """{pcf code: {bridges: [...], coded: [...]}} from I-1's entries."""
    out: dict = {}
    for entry in entries_document.get("entries") or []:
        if entry.get("kind") != "capability-class":
            continue
        for bridge in entry.get("designated_by") or []:
            code = bridge.get("pcf_code")
            if code is None:
                continue
            out.setdefault(str(code), {"bridges": [], "coded": []})[
                "bridges"].append({"capability_class_entry": entry["id"],
                                   "capability_class_iri": entry["iri"],
                                   "catalog_node": bridge["node"],
                                   "module": bridge["module"]})
        if entry.get("pcf_code") is not None:
            out.setdefault(str(entry["pcf_code"]),
                           {"bridges": [], "coded": []})["coded"].append(
                {"capability_class_entry": entry["id"],
                 "capability_class_iri": entry["iri"]})
    for value in out.values():
        value["bridges"].sort(key=lambda b: (b["capability_class_entry"],
                                             b["catalog_node"], b["module"]))
        value["coded"].sort(key=lambda b: b["capability_class_entry"])
    return out


# ----------------------------------------------------------------- build


def entry_id(node: dict) -> str:
    return "%s-%s-%s" % (ENTRY_PREFIX, node["element_id"],
                         KIND_BY_LEVEL[node["level"]])


def entries(read: dict, bridges: dict) -> list[dict]:
    out = []
    for node in read["nodes"]:
        if node["level"] not in KIND_BY_LEVEL:
            continue
        entry = {
            "id": entry_id(node),
            "kind": KIND_BY_LEVEL[node["level"]],
            "element_id": node["element_id"],
            "hierarchy_id": node["hierarchy_id"],
            "level": node["level"],
            "parent": node["parent"],
            "locator": {"sheet": node["sheet"], "row": node["row"]},
            "rights_status": INTERNAL_RIGHTS,
            "name": node["name"],
            "description": node["description"],
        }
        if node["level"] == 3:
            found = bridges.get(node["element_id"],
                                {"bridges": [], "coded": []})
            entry["bpo_bridge_evidence"] = {
                "bridged": bool(found["bridges"]),
                "designated_by_catalog_node": found["bridges"],
                "capability_class_with_this_code": found["coded"],
            }
        out.append(entry)
    out.sort(key=lambda e: (e["level"], int(e["element_id"])))
    return out


INTERNAL_HEADER = [
    "INTERNAL. Never commit this file (APQC-1 c,",
    "docs/decisions/2026-10-28-i2a-decided.md). It holds APQC PCF content",
    "as the workbook gives it, kept so the work can continue without",
    "harvesting the source again. GENERATED by tools/inventory/harvest_pcf.py",
    "--write; its sha256 is recorded in docs/sources/inventory/pcf-status.yaml.",
]


def entries_document(pin: dict, citation: dict, read: dict,
                     bridge_digest: str, items: list[dict]) -> dict:
    return {
        "format": FORMAT,
        "generator": GENERATOR,
        "internal": True,
        "status": ("internal source evidence (APQC-1 c); not vocabulary, not "
                   "an admission (Amendment 4), and no level-3 node is a "
                   "standing-function candidate (E4 is not performed)"),
        "source": {
            "rightsholder": citation["rightsholder"],
            "work": citation["work"],
            "edition": citation["edition"],
            "bpo": {k: pin[k] for k in ("repository", "commit", "path",
                                        "sha256")},
            "sheet": read["sheet"],
        },
        "bridge_input": {"path": BPO_ENTRIES, "sha256": bridge_digest,
                         "note": ("BPO's bridge (ADR-001 R4/R6) is evidence, "
                                  "not proof: I-1 found it is not a "
                                  "standing-function marker")},
        "counts": entry_counts(items),
        "entries": items,
    }


def entry_counts(items: list[dict]) -> dict:
    counts = {kind: 0 for kind in KIND_BY_LEVEL.values()}
    for item in items:
        counts[item["kind"]] += 1
    return counts


def worksheet_document(items: list[dict]) -> dict:
    rows = []
    for item in items:
        if item["level"] != 3:
            continue
        rows.append({
            "entry": item["id"],
            "element_id": item["element_id"],
            "node_locator": dict(item["locator"]),
            "bpo_bridged": item["bpo_bridge_evidence"]["bridged"],
            "judgement": None,
            "reason": None,
            "independent_evidence": [],
            "judged_by": None,
            "judged_on": None,
        })
    return {
        "format": FORMAT,
        "generator": GENERATOR,
        "internal": True,
        "method": {
            "decision": "E4 Option A",
            "record": AUTHORITY,
            "test": ("CM-01's Standing Function (%s): does the node name an "
                     "ongoing function rather than a bounded process?"
                     % CM01),
            "judgement_values": ["standing-function-candidate",
                                 "not-a-candidate", "undecided"],
            "independent_evidence_item": {
                "kind": ("fibf-function | brm-function | children-recur | "
                         "bpo-bridge | other"),
                "locator": "where the evidence is (document, page, row)",
                "summary": "what it shows, in the judge's words",
            },
            "rule": ("a judgement cites at least one piece of evidence other "
                     "than the node's name or level; a bpo-bridge counts as "
                     "evidence, not proof; the list goes to the architect, "
                     "and no candidate is admitted as a Capability Type"),
        },
        "state": ("deferred: not performed pending APQC's answer to question "
                  "6 of the clarification request (whether its Terms reach "
                  "AI-assisted development) or an explicit architect "
                  "decision; every row is empty"),
        "rows": rows,
    }


def node_summary(node: dict) -> dict:
    return {"hierarchy_id": node["hierarchy_id"], "level": node["level"],
            "parent_element_id": (node["parent"] or {}).get("element_id"),
            "name": node["name"],
            "locator": {"sheet": node["sheet"], "row": node["row"]}}


def delta(old: dict, new: dict) -> list[dict]:
    """7.4 -> 8.0 at levels 1-3, keyed by element id."""
    before = {n["element_id"]: n for n in old["nodes"]}
    after = {n["element_id"]: n for n in new["nodes"]}
    out = []
    for eid in sorted(set(before) | set(after), key=int):
        a, b = before.get(eid), after.get(eid)
        if not ((a and a["level"] <= 3) or (b and b["level"] <= 3)):
            continue
        if a is None:
            changes = ["added"]
        elif b is None:
            changes = ["retired"]
        else:
            changes = []
            if " ".join(a["name"].split()) != " ".join(b["name"].split()):
                changes.append("renamed")
            if a["hierarchy_id"] != b["hierarchy_id"]:
                changes.append("recoded")
            if ((a["parent"] or {}).get("element_id")
                    != (b["parent"] or {}).get("element_id")):
                changes.append("moved")
        if changes:
            out.append({"element_id": eid, "kind": "pcf-delta",
                        "changes": changes,
                        "pcf_7_4": node_summary(a) if a else None,
                        "pcf_8_0": node_summary(b) if b else None})
    return out


def delta_counts(items: list[dict]) -> dict:
    return {c: sum(1 for i in items if c in i["changes"]) for c in CHANGES}


def delta_document(pin: dict, digest80: str, size80: int,
                   items: list[dict]) -> dict:
    return {
        "format": FORMAT,
        "generator": GENERATOR,
        "internal": True,
        "from": {"edition": "7.4", "sha256": pin["sha256"]},
        "to": {"edition": "8.0", "sha256": digest80, "bytes": size80},
        "levels": [1, 2, 3],
        "counts": delta_counts(items),
        "changes": items,
    }


def internal_bytes(data: dict) -> bytes:
    return (header(INTERNAL_HEADER) + "\n" + dump(data)).encode("utf-8")


# ---------------------------------------------------------------- status


STATUS_HEADER = [
    "GENERATED by tools/inventory/harvest_pcf.py --write. Do not edit: the",
    "offline check requires this file to be the generator's rendering of",
    "its data, and a fresh build to reproduce it byte for byte.",
    "",
    "Capability Term Inventory, Phase I-2b: the APQC PCF, citation only",
    "(APQC-1 c). This public record holds the citation, the posture,",
    "aggregate counts and the digests of the internal evidence. No PCF",
    "name, description, element id, hierarchy id or structure is here; the",
    "evidence itself is internal and never committed. Read",
    "docs/sources/inventory/README.md first.",
]

STATUS_KEYS = ("format", "generator", "phase", "what", "posture", "citation",
               "counts", "internal", "e4", "pcf_8_0")
POSTURE_KEYS = ("decision", "record", "rights_source", "public")
CITATION_KEYS = ("rightsholder", "work", "edition", "register", "bpo_locator")
LOCATOR_KEYS = ("repository", "commit", "path", "sha256")
COUNT_KEYS = ("workbook_rows", "rows_by_level", "entries_by_kind",
              "level_3_bpo_bridged", "level_3_bpo_coded")
INTERNAL_KEYS = ("directory", "committed", "bridge_input", "outputs")
BRIDGE_KEYS = ("path", "sha256")
OUTPUT_KEYS = ("file", "sha256", "bytes")
E4_KEYS = ("state", "why", "worksheet_rows", "judged")
PCF80_KEYS = ("state", "rights_source", "gap", "file", "delta")
FILE_KEYS = ("sha256", "bytes")
DELTA_KEYS = ("output", "counts")

POSTURE_PUBLIC = ("citation and aggregate counts only, pending APQC's "
                  "written clarification; no PCF name, description, code, "
                  "hierarchy or substantial structure (E2)")
WHAT = ("Phase I-2b status: the PCF 7.4 workbook read into internal evidence "
        "(levels 1-3, with locators and BPO bridge evidence) and an empty E4 "
        "worksheet; only this record is public")
E4_WHY = ("E4 requires a written judgement of each level-3 node against "
          "CM-01's Standing Function, which means reading PCF names; "
          "whether APQC's Terms let an AI tool do that is question 6 of the "
          "clarification request. Deferred until APQC answers or the "
          "architect decides explicitly")
GAP_80 = ("not supplied: the architect obtains PCF 8.0 under the architect's "
          "registration (APQC80-1 a); then run --write --pcf80 <path>, and "
          "pin its in-file notice in rights.yaml as an I-2a amendment")


def status_document(pin: dict, citations: dict, read: dict, items: list,
                    bridge_digest: str, outputs: dict, pcf80: dict) -> dict:
    level3 = [i for i in items if i["level"] == 3]
    return {
        "format": FORMAT,
        "generator": GENERATOR,
        "phase": "I-2b",
        "what": WHAT,
        "posture": {"decision": "APQC-1 c", "record": DECISION,
                    "rights_source": RIGHTS_74, "public": POSTURE_PUBLIC},
        "citation": {
            "rightsholder": citations[RIGHTS_74]["rightsholder"],
            "work": citations[RIGHTS_74]["work"],
            "edition": citations[RIGHTS_74]["edition"],
            "register": citations[RIGHTS_74]["register"],
            "bpo_locator": {k: pin[k] for k in LOCATOR_KEYS},
        },
        "counts": {
            "workbook_rows": read["rows"],
            "rows_by_level": dict(read["rows_by_level"]),
            "entries_by_kind": entry_counts(items),
            "level_3_bpo_bridged": sum(
                1 for i in level3 if i["bpo_bridge_evidence"]["bridged"]),
            "level_3_bpo_coded": sum(
                1 for i in level3
                if i["bpo_bridge_evidence"]["capability_class_with_this_code"]),
        },
        "internal": {
            "directory": INTERNAL,
            "committed": False,
            "bridge_input": {"path": BPO_ENTRIES, "sha256": bridge_digest},
            "outputs": [{"file": name, "sha256": sha256(data),
                         "bytes": len(data)}
                        for name, data in sorted(outputs.items())
                        if name != DELTA_FILE],
        },
        "e4": {"state": "deferred", "why": E4_WHY,
               "worksheet_rows": len(level3), "judged": 0},
        "pcf_8_0": pcf80,
    }


def pcf80_gap() -> dict:
    return {"state": "gap", "rights_source": RIGHTS_80, "gap": GAP_80,
            "file": None, "delta": None}


def pcf80_supplied(digest: str, size: int, delta_data: bytes,
                   counts: dict) -> dict:
    return {"state": "supplied", "rights_source": RIGHTS_80, "gap": None,
            "file": {"sha256": digest, "bytes": size},
            "delta": {"output": {"file": DELTA_FILE,
                                 "sha256": sha256(delta_data),
                                 "bytes": len(delta_data)},
                      "counts": counts}}


def status_bytes(document: dict) -> bytes:
    return (header(STATUS_HEADER) + "\n" + dump(document)).encode("utf-8")


# ----------------------------------------------------------- the guard


def _walk(data, path="", key=None):
    if isinstance(data, dict):
        for k, v in data.items():
            yield k, v, "%s/%s" % (path, k)
            yield from _walk(v, "%s/%s" % (path, k), k)
    elif isinstance(data, list):
        for n, v in enumerate(data):
            yield key, v, "%s/%d" % (path, n)
            yield from _walk(v, "%s/%d" % (path, n), key)


def _closed(mapping, keys, where, out) -> bool:
    if not isinstance(mapping, dict):
        out.append("%s is not a mapping" % where)
        return False
    extra = sorted(set(mapping) - set(keys))
    missing = sorted(set(keys) - set(mapping))
    for key in extra:
        out.append("%s carries %r, which the status record does not define. "
                   "Is it catalog content?" % (where, key))
    for key in missing:
        out.append("%s declares no %r" % (where, key))
    return not extra and not missing


def _count(value) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) \
        and value >= 0


def status_findings(document, base: Path, *, pin: dict | None = None,
                    citations: dict | None = None,
                    content: dict | None = None,
                    raw: bytes | None = None) -> list[str]:
    """The public guard and the closed schema. `content`, when the build
    is at hand, holds the names, descriptions and element ids that must
    not appear: {"texts": set, "element_ids": set}."""
    out: list[str] = []
    where = STATUS
    if not _closed(document, STATUS_KEYS, where, out):
        return out
    rights = rights_module(base)
    harvest = harvest_module(base)

    # Keys that would hold catalog content, anywhere.
    for key, _value, path in _walk(document):
        if isinstance(key, str) and key in rights.CATALOG_KEYS:
            out.append("%s%s is a %r field. The public record holds no PCF "
                       "content; what is it holding?" % (where, path, key))
        if isinstance(key, str) and key in harvest.FORBIDDEN_KEYS:
            out.append("%s carries %r at %s. A ratification or vocabulary "
                       "field in source evidence would make it a decision"
                       % (where, key, path))

    if document["format"] != FORMAT:
        out.append("%s is format %r; this tool writes %d"
                   % (where, document["format"], FORMAT))
    if document["generator"] != GENERATOR or document["phase"] != "I-2b" \
            or document["what"] != WHAT:
        out.append("%s does not name this generator and phase in its own "
                   "words; was it written by hand?" % where)

    posture = document["posture"]
    if _closed(posture, POSTURE_KEYS, where + "/posture", out):
        if posture != {"decision": "APQC-1 c", "record": DECISION,
                       "rights_source": RIGHTS_74, "public": POSTURE_PUBLIC}:
            out.append("%s/posture is not APQC-1 c as decided in %s"
                       % (where, DECISION))
        if not (base / DECISION).is_file():
            out.append("%s/posture points at %s, which does not exist"
                       % (where, DECISION))

    citation = document["citation"]
    exempt = set()
    if _closed(citation, CITATION_KEYS, where + "/citation", out):
        locator = citation["bpo_locator"]
        if _closed(locator, LOCATOR_KEYS, where + "/citation/bpo_locator",
                   out):
            if pin and {k: pin[k] for k in LOCATOR_KEYS} != locator:
                out.append("%s/citation/bpo_locator is not the workbook "
                           "config/inventory-sources.yaml pins" % where)
            exempt.add(("path", locator["path"]))
        if citations:
            expected = citations[RIGHTS_74]
            for key in ("rightsholder", "work", "edition", "register"):
                if citation[key] != expected[key]:
                    out.append("%s/citation/%s is not what %s records for "
                               "%s" % (where, key, RIGHTS, RIGHTS_74))
        exempt.add(("edition", citation["edition"]))

    counts = document["counts"]
    if _closed(counts, COUNT_KEYS, where + "/counts", out):
        levels = counts["rows_by_level"]
        kinds = counts["entries_by_kind"]
        good = isinstance(levels, dict) and isinstance(kinds, dict)
        if good:
            for key, value in list(levels.items()) + list(kinds.items()):
                if not _count(value):
                    out.append("%s/counts holds %r for %s; counts are "
                               "non-negative integers" % (where, value, key))
                    good = False
            for key in levels:
                if not re.fullmatch(r"level_[1-9]", str(key)):
                    out.append("%s/counts/rows_by_level has key %r; expected "
                               "level_<n>" % (where, key))
                    good = False
            if set(kinds) != set(KIND_BY_LEVEL.values()):
                out.append("%s/counts/entries_by_kind is not exactly %s"
                           % (where, ", ".join(KIND_BY_LEVEL.values())))
                good = False
        if good:
            if sum(levels.values()) != counts["workbook_rows"]:
                out.append("%s/counts: the rows per level do not add up to "
                           "the workbook rows" % where)
            for level, kind in KIND_BY_LEVEL.items():
                if kinds[kind] != levels.get("level_%d" % level, 0):
                    out.append("%s/counts: %s is not the level-%d row count"
                               % (where, kind, level))
            for key in ("level_3_bpo_bridged", "level_3_bpo_coded"):
                if not _count(counts[key]) \
                        or counts[key] > kinds["pcf-level-3-unjudged"]:
                    out.append("%s/counts/%s is not a count of level-3 "
                               "entries" % (where, key))

    internal = document["internal"]
    if _closed(internal, INTERNAL_KEYS, where + "/internal", out):
        if internal["directory"] != INTERNAL or internal["committed"] \
                is not False:
            out.append("%s/internal must name %s and committed: false"
                       % (where, INTERNAL))
        if _closed(internal["bridge_input"], BRIDGE_KEYS,
                   where + "/internal/bridge_input", out):
            if internal["bridge_input"]["path"] != BPO_ENTRIES:
                out.append("%s/internal/bridge_input is not %s"
                           % (where, BPO_ENTRIES))
        files = []
        for n, item in enumerate(internal["outputs"] or []):
            ow = "%s/internal/outputs/%d" % (where, n)
            if _closed(item, OUTPUT_KEYS, ow, out):
                files.append(item["file"])
                exempt.add(("file", item["file"]))
                if not _count(item["bytes"]):
                    out.append("%s/bytes is not a size" % ow)
        if sorted(files) != sorted([ENTRIES_FILE, WORKSHEET_FILE]):
            out.append("%s/internal/outputs lists %s; expected %s and %s"
                       % (where, files, ENTRIES_FILE, WORKSHEET_FILE))

    e4 = document["e4"]
    if _closed(e4, E4_KEYS, where + "/e4", out):
        if e4["state"] != "deferred" or e4["why"] != E4_WHY \
                or e4["judged"] != 0:
            out.append("%s/e4 records judgements. E4 is deferred pending "
                       "APQC's answer to question 6 or an architect "
                       "decision; this tool makes none" % where)
        if isinstance(counts, dict) and isinstance(
                counts.get("entries_by_kind"), dict) and \
                e4["worksheet_rows"] != counts["entries_by_kind"].get(
                    "pcf-level-3-unjudged"):
            out.append("%s/e4/worksheet_rows is not the level-3 count"
                       % where)

    pcf80 = document["pcf_8_0"]
    if _closed(pcf80, PCF80_KEYS, where + "/pcf_8_0", out):
        if pcf80["rights_source"] != RIGHTS_80:
            out.append("%s/pcf_8_0/rights_source is not %s"
                       % (where, RIGHTS_80))
        exempt.add(("rights_source", RIGHTS_80))
        if pcf80["state"] == "gap":
            if pcf80 != pcf80_gap():
                out.append("%s/pcf_8_0 is a gap but carries a file or a "
                           "delta, or its own words" % where)
        elif pcf80["state"] == "supplied":
            if pcf80["gap"] is not None:
                out.append("%s/pcf_8_0 is supplied and still states a gap"
                           % where)
            if _closed(pcf80["file"], FILE_KEYS, where + "/pcf_8_0/file",
                       out):
                if not _count(pcf80["file"]["bytes"]):
                    out.append("%s/pcf_8_0/file/bytes is not a size" % where)
            if _closed(pcf80["delta"], DELTA_KEYS, where + "/pcf_8_0/delta",
                       out):
                d = pcf80["delta"]
                if _closed(d["output"], OUTPUT_KEYS,
                           where + "/pcf_8_0/delta/output", out):
                    if d["output"]["file"] != DELTA_FILE:
                        out.append("%s/pcf_8_0/delta/output is not %s"
                                   % (where, DELTA_FILE))
                    exempt.add(("file", DELTA_FILE))
                if not isinstance(d["counts"], dict) \
                        or set(d["counts"]) != set(CHANGES) \
                        or not all(_count(v) for v in d["counts"].values()):
                    out.append("%s/pcf_8_0/delta/counts is not a count per "
                               "change type (%s)" % (where,
                                                     ", ".join(CHANGES)))
        else:
            out.append("%s/pcf_8_0/state is %r; expected gap or supplied"
                       % (where, pcf80["state"]))
    exempt.add(("rights_source", RIGHTS_74))
    # The tool's own fixed prose, already required equal to its constants.
    exempt.update({("what", WHAT), ("public", POSTURE_PUBLIC),
                   ("why", E4_WHY), ("gap", GAP_80)})

    # Every digest is a digest.
    for key, value, path in _walk(document):
        if key == "sha256" and not HEX64.match(str(value)):
            out.append("%s%s is not a sha256" % (where, path))

    # No PCF code or element id in any string a pin does not fix.
    for key, value, path in _walk(document):
        if not isinstance(value, str) or key in HEX_KEYS:
            continue
        if (key, value) in exempt:
            continue
        hit = PCF_HIERARCHY.search(value)
        if hit:
            out.append("%s%s holds %r, which reads as a PCF hierarchy id. "
                       "The public record carries no PCF code"
                       % (where, path, hit.group(0)))
        hit = DIGIT_RUN.search(value)
        if hit:
            out.append("%s%s holds a run of %d digits, as long as a PCF "
                       "element id. The public record carries no PCF code"
                       % (where, path, len(hit.group(0))))

    # With the build at hand: none of its names, descriptions or ids.
    if content:
        strings = [(path, value) for key, value, path in _walk(document)
                   if isinstance(value, str) and key not in HEX_KEYS]
        for path, value in strings:
            folded = _norm(value)
            for text in content["texts"]:
                if text in folded and re.search(
                        r"(?<!\w)%s(?!\w)" % re.escape(text), folded):
                    out.append("%s%s contains the text of a PCF name or "
                               "description" % (where, path))
                    break
            tokens = set(re.findall(r"\d+", value))
            if (key_hit := tokens & content["element_ids"]) and \
                    ("path", value) not in exempt:
                out.append("%s%s contains %d PCF element id(s)"
                           % (where, path, len(key_hit)))

    # The admission guard, with harvest_bpo's constants, over the file's
    # own text when it is at hand (a Turtle line is RDF text whatever YAML
    # scalar holds it) and over the rendering of the data.
    text = dump(document)
    if raw is not None:
        text = raw.decode("utf-8", errors="replace") + "\n" + text
    for namespace in authored_namespaces(base):
        if namespace in text:
            out.append("%s names %s, one of this repository's authored "
                       "namespaces. The inventory mints nothing"
                       % (where, namespace))
    for marker in harvest.RDF_MARKERS:
        if marker.search(text):
            out.append("%s reads as an RDF serialization (%s)"
                       % (where, marker.pattern))
    return out


def content_of(items: list[dict]) -> dict:
    """What the status record must not contain, from a build."""
    texts = set()
    for item in items:
        for key in ("name", "description"):
            if item.get(key):
                folded = _norm(item[key])
                # A one- or two-letter name could occur by accident in any
                # prose; three characters and more is a real collision.
                if len(folded) >= 3:
                    texts.add(folded)
    return {"texts": texts,
            "element_ids": {item["element_id"] for item in items}}


# ---------------------------------------------------------------- writes


def _git(base: Path, *args) -> subprocess.CompletedProcess | None:
    try:
        return subprocess.run(["git", "-C", str(base), *args],
                              capture_output=True, text=True)
    except OSError:
        return None


def internal_target(base: Path, internal: Path, name: str) -> Path:
    """Where an internal output may be written, or a refusal.

    The path must be inside the internal directory. If that directory is
    inside the repository, git must ignore the path and track nothing at
    it, and both must be provable: without git the answer is no.
    """
    internal = internal.resolve()
    target = (internal / name).resolve()
    try:
        target.relative_to(internal)
    except ValueError:
        raise Refused("refusing to write %s: it is outside the internal "
                      "directory %s. PCF content goes nowhere else "
                      "(APQC-1 c)" % (target, internal)) from None
    base = base.resolve()
    try:
        rel = target.relative_to(base).as_posix()
    except ValueError:
        return target                       # outside the repository
    tracked = _git(base, "ls-files", "--", rel)
    ignored = _git(base, "check-ignore", "-q", "--no-index", rel)
    if tracked is None or ignored is None or tracked.returncode != 0:
        raise Refused("refusing to write %s: git cannot say whether it is "
                      "tracked, and PCF content is written only where it "
                      "provably is not" % rel)
    if tracked.stdout.strip():
        raise Refused("refusing to write %s: git tracks it. PCF content is "
                      "never committed (APQC-1 c)" % rel)
    if ignored.returncode != 0:
        raise Refused("refusing to write %s: git does not ignore it, so the "
                      "next `git add` would commit PCF content. Is %s in "
                      ".gitignore?" % (rel, INTERNAL))
    return target


def write_internal(base: Path, internal: Path, outputs: dict) -> None:
    targets = {name: internal_target(base, internal, name)
               for name in outputs}
    for name, data in sorted(outputs.items()):
        targets[name].parent.mkdir(parents=True, exist_ok=True)
        targets[name].write_bytes(data)
        print("  wrote %s (internal, %d bytes, sha256 %s)"
              % (targets[name], len(data), sha256(data)))


def write_status(base: Path, data: bytes, document: dict, content: dict,
                 pin: dict, citations: dict) -> None:
    """The one public write: only the status record, only once guarded."""
    problems = status_findings(document, base, pin=pin, citations=citations,
                               content=content)
    if problems:
        raise Refused("the status record failed its own guard; nothing "
                      "public was written:\n  " + "\n  ".join(problems))
    (base / STATUS).write_bytes(data)
    print("  wrote %s" % STATUS)


# ----------------------------------------------------------------- build


def build(base: Path, workbook: bytes, pcf80_path: Path | None,
          committed80: dict | None) -> dict:
    """Everything, in memory: internal outputs, status bytes, content."""
    pin = workbook_pin(base)
    citations = rights_citation(base)
    if sha256(workbook) != pin["sha256"]:
        raise Refused("the workbook digests to %s; the pin says %s"
                      % (sha256(workbook), pin["sha256"]))
    read = read_workbook(workbook, "the PCF 7.4 workbook")
    bridge_raw = (base / BPO_ENTRIES).read_bytes()
    bridge_digest = sha256(bridge_raw)
    bridges = bpo_bridges(parse_yaml(bridge_raw.decode("utf-8")))
    items = entries(read, bridges)
    outputs = {
        ENTRIES_FILE: internal_bytes(entries_document(
            pin, citations[RIGHTS_74], read, bridge_digest, items)),
        WORKSHEET_FILE: internal_bytes(worksheet_document(items)),
    }
    note = None
    if pcf80_path is not None:
        if not pcf80_path.is_file():
            raise Refused("--pcf80 %s: no such file" % pcf80_path)
        raw80 = pcf80_path.read_bytes()
        read80 = read_workbook(raw80, "the PCF 8.0 workbook")
        changes = delta(read, read80)
        delta_data = internal_bytes(delta_document(
            pin, sha256(raw80), len(raw80), changes))
        outputs[DELTA_FILE] = delta_data
        pcf80 = pcf80_supplied(sha256(raw80), len(raw80), delta_data,
                               delta_counts(changes))
    elif committed80 and committed80.get("state") == "supplied":
        pcf80 = committed80
        note = ("PCF 8.0 is recorded as supplied; its block was carried "
                "over, not re-derived. Pass --pcf80 <path> to re-derive it")
    else:
        pcf80 = pcf80_gap()
    document = status_document(pin, citations, read, items, bridge_digest,
                               outputs, pcf80)
    return {"pin": pin, "citations": citations, "outputs": outputs,
            "document": document, "status": status_bytes(document),
            "content": content_of(items), "items": items, "note": note}


# ----------------------------------------------------------------- check


def load_status(base: Path):
    path = base / STATUS
    if not path.is_file():
        raise Refused("%s is missing. Run --write with the workbook cached"
                      % STATUS)
    raw = path.read_bytes()
    if b"\r\n" in raw:
        raise Refused("%s has CRLF line endings; digests here are over LF "
                      "bytes" % STATUS)
    return raw, parse_yaml(raw.decode("utf-8"))


def check(base: Path, cache: Path, internal: Path,
          pcf80_path: Path | None = None,
          workbook: bytes | None = None) -> tuple[list[str], list[str]]:
    """(findings, notes), offline unless `workbook` was fetched."""
    raw, document = load_status(base)
    pin = workbook_pin(base)
    citations = rights_citation(base)
    notes: list[str] = []
    out = status_findings(document, base, pin=pin, citations=citations,
                          raw=raw)
    if out:
        return out, notes
    if status_bytes(document) != raw:
        out.append("%s is not the generator's rendering of its own data; "
                   "was it edited by hand?" % STATUS)
    if document["internal"]["bridge_input"]["sha256"] != sha256(
            (base / BPO_ENTRIES).read_bytes()):
        out.append("%s was built from a %s other than the committed one; "
                   "run --write" % (STATUS, BPO_ENTRIES))
    if workbook is None:
        workbook = cached_workbook(base, pin, cache)
    if workbook is None:
        notes.append("the PCF 7.4 workbook is not cached, so the record "
                      "was checked for shape, pins and the public guard "
                      "only; --confirm reproduces it from GitHub")
        return out, notes
    built = build(base, workbook, pcf80_path, document["pcf_8_0"])
    if built["note"]:
        notes.append(built["note"])
    out += status_findings(built["document"], base, pin=pin,
                           citations=citations, content=built["content"])
    out += status_findings(document, base, pin=pin, citations=citations,
                           content=built["content"])
    if built["status"] != raw:
        out.append("%s is not what building from the pinned workbook "
                   "produces; run --write" % STATUS)
    expected = {o["file"]: o["sha256"] for o in
                built["document"]["internal"]["outputs"]}
    if built["document"]["pcf_8_0"].get("delta"):
        d = built["document"]["pcf_8_0"]["delta"]["output"]
        expected[d["file"]] = d["sha256"]
    present = 0
    for name, digest in sorted(expected.items()):
        path = internal / name
        if not path.is_file():
            continue
        present += 1
        if sha256(path.read_bytes()) != digest:
            out.append("internal %s does not have the digest %s records; "
                       "the internal evidence is not the one reviewed. Run "
                       "--write" % (name, STATUS))
    if not present:
        notes.append("no internal output is present in %s; --write "
                     "regenerates them" % internal)
    return out, notes


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    mode = ap.add_mutually_exclusive_group()
    mode.add_argument("--write", action="store_true",
                      help="read the pinned workbook (cache, else GitHub) "
                           "and write the internal outputs and the status "
                           "record")
    mode.add_argument("--confirm", action="store_true",
                      help="read the pinned workbook (cache, else GitHub) "
                           "and require the status record byte for byte")
    ap.add_argument("--pcf80", default=None,
                    help="a PCF 8.0 xlsx the architect supplied (any local "
                         "path; never commit it)")
    ap.add_argument("--internal-dir", default=None,
                    help="internal output directory (default %s)" % INTERNAL)
    ap.add_argument("--cache", default=None,
                    help="download cache (default %s/)" % CACHE)
    args = ap.parse_args(argv)
    base = root()
    cache = Path(args.cache) if args.cache else base / CACHE
    internal = Path(args.internal_dir) if args.internal_dir \
        else base / INTERNAL
    pcf80 = Path(args.pcf80) if args.pcf80 else None

    if args.write:
        pin = workbook_pin(base)
        workbook = fetched_workbook(base, pin, cache)
        committed80 = None
        if (base / STATUS).is_file():
            committed80 = load_status(base)[1].get("pcf_8_0")
        built = build(base, workbook, pcf80, committed80)
        if built["note"]:
            print("  note: %s" % built["note"])
        write_internal(base, internal, built["outputs"])
        write_status(base, built["status"], built["document"],
                     built["content"], built["pin"], built["citations"])

    workbook = None
    if args.confirm:
        workbook = fetched_workbook(base, workbook_pin(base), cache)
    problems, notes = check(base, cache, internal, pcf80, workbook)
    for note in notes:
        print("  note: %s" % note)
    if problems:
        for problem in problems:
            print("  FINDING: %s" % problem)
        return 1
    _raw, document = load_status(base)
    counts = document["counts"]
    reproduced = workbook is not None or cached_workbook(
        base, workbook_pin(base), cache) is not None
    print("  ok: %s is citation and counts only (%d workbook rows; %s); the "
          "public and admission guards hold%s; E4 deferred (%d level-3 rows "
          "unjudged); PCF 8.0 %s"
          % (STATUS, counts["workbook_rows"],
             ", ".join("%s %d" % (k, v) for k, v in
                       counts["entries_by_kind"].items()),
             ", and a fresh build reproduces it" if reproduced else "",
             document["e4"]["worksheet_rows"],
             "supplied" if document["pcf_8_0"]["state"] == "supplied"
             else "is a gap: not supplied (APQC80-1 a; pass --pcf80)"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
