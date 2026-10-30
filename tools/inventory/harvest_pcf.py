# SPDX-License-Identifier: MIT
"""Publish the APQC PCF 7.4 from BPO's catalog, with APQC's notice.

    python tools/inventory/harvest_pcf.py             # offline check
    python tools/inventory/harvest_pcf.py --write     # fetch (cache, else GitHub), write the outputs
    python tools/inventory/harvest_pcf.py --confirm   # fetch (cache, else GitHub), require byte identity

Phase I-2b of the Capability Term Inventory, under the architect's
decision of 2026-10-29 (docs/decisions/2026-10-29-apqc-pcf-sourcing-
decided.md), which replaced APQC-1 (citation only), withdrew APQC-2 and
deferred APQC80-1. It writes two files:

  docs/sources/inventory/pcf-7.4-entries.yaml
      one entry per PCF 7.4 element: element ID, hierarchy ID, level,
      parent (by element ID), name, description, BPO's IRI and a locator
      (the line of the node in BPO's catalog at the pinned commit), and,
      where Phase I-1 found one, BPO's bridge to a capability class. Its
      header carries the citation, APQC's notice verbatim (`apqc_notice`),
      the statement that the material is APQC's and not under this
      repository's MIT licence, that APQC does not endorse this work, and
      that APQC's marks are used only to identify the source.

  NOTICE.md (repository root)
      separates this repository's MIT work from the PCF material, lists
      every PCF-bearing file (config/inventory-pcf-sources.yaml,
      `pcf_bearing`), reproduces APQC's notice and records the digest of
      the BPO file it was copied from.

THE SOURCE

BPO only, at the commit config/inventory-pcf-sources.yaml pins: its
ontology/apqc-catalog.ttl and NOTICE.md, each by sha256, fetched from
raw.githubusercontent.com at that commit (harvest_bpo.py's fetch, which
refuses any other host, a URL not naming the commit, and a digest other
than the pin) and cached under .upstream-cache/bpo-<commit>/<sha256>.
Nothing is fetched from apqc.org, by this tool or any other: the decision
names BPO's catalog as the only source, and APQC's Terms forbid automated
access. The PCF workbook is no longer read.

THE NOTICE, COPIED AND NOT RETYPED

APQC's notice is the blockquote under "## APQC's notice" in BPO's
NOTICE.md; its `> ` lines are unwrapped into one paragraph (each line's
text stripped, joined by single spaces). The tool refuses unless that
section holds exactly one blockquote of one paragraph, the result digests
to the `apqc_notice_sha256` the pin records, and it equals the APQC part
of the catalog's dct:rights at the same commit -- the text after BPO's
framing sentence and the first blank line, on the one owl:Ontology
header, which must carry exactly one dct:rights. So the two places BPO
states the notice must agree, and the copy here is the bytes BPO
published. The outputs record NOTICE.md's sha256 wherever the notice is
used.

THE CATALOG, READ STRICTLY

Every skos:Concept in the PCF scheme must carry exactly one bpo:pcfID
(digits), bpo:hierarchyID (dotted digits), skos:prefLabel and at most one
bpo:apqcSourceText; its IRI must be BPO's `PCF_<element id>`; element and
hierarchy ids must be unique. The level is read from the hierarchy id
(`N.0` is 1, `N.M` is 2, otherwise the number of components) and must
agree with BPO's "APQC level: ..." comment where there is one. A level-1
node has no skos:broader; every other has exactly one, and it must be the
node whose hierarchy id is the dotted parent. Refusals name the element
id, never a name or description.

BPO'S BRIDGE, AS EVIDENCE

From the committed docs/sources/inventory/bpo-entries.yaml (Phase I-1,
read and never written): the capability-class entries whose
`designated_by` names a catalog node with an element's id, and those
whose own `pcf_code` is that id. Recorded on every element that has one,
at any level, with the input's sha256. It is evidence, not proof: I-1
found that the bridge is not a standing-function marker. A code the
bridge names that the catalog lacks is listed in the header.

WHAT THIS DOES NOT DO

No E4 judgement: whether a PCF element is a standing function, a
capability or anything else is not decided here, and the header records
E4 as open. No PCF 8.0 (APQC80-1 is deferred with the 7.4-to-8.0
comparison). No vocabulary concept, ontology class, property, IRI or
type-admission result: the entries are source evidence (Amendment 4), and
harvest_bpo.py's admission guard holds over this directory. No I-1 output
is changed.

THE OFFLINE CHECK (default; CI)

The entries file must be the generator's rendering of its own data; its
header must be what the pins, rights.yaml and the decision give; its
`apqc_notice` must digest to the pin; its entries must be well formed,
unique, sorted, with parents one level up and hierarchy ids that extend
their parent's, and counts that add up; its bridges must be what the
committed bpo-entries.yaml gives now; NOTICE.md must be a fresh
generation. With both pinned files cached, a fresh build must reproduce
both outputs byte for byte. tools/licensing/pcf_notice.py is the
repository-wide gate; this tool checks only its own outputs.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import layout  # noqa: E402

FORMAT = 1
GENERATOR = "tools/inventory/harvest_pcf.py"
GATE = "tools/licensing/pcf_notice.py"
HARVEST = "tools/inventory/harvest_bpo.py"
PINS = "config/inventory-pcf-sources.yaml"
SOURCE_ID = "apqc-pcf-7.4-via-bpo"
BPO_ENTRIES = "docs/sources/inventory/bpo-entries.yaml"
CACHE = ".upstream-cache"
ROOT_NOTICE = "NOTICE.md"
NOTICE_SECTION = "APQC's notice"
PCF_SECTION = "Files that carry PCF material"

RDF = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
RDFS = "http://www.w3.org/2000/01/rdf-schema#"
OWL = "http://www.w3.org/2002/07/owl#"
SKOS = "http://www.w3.org/2004/02/skos/core#"
DCT = "http://purl.org/dc/terms/"

#: BPO's level names, in its catalog's rdfs:comment "APQC level: <name>".
LEVEL_NAMES = {"Category": 1, "ProcessGroup": 2, "Process": 3,
               "Activity": 4, "Task": 5}

ELEMENT_ID = re.compile(r"^\d+$")
HIERARCHY_ID = re.compile(r"^\d+(?:\.\d+)+$")
HEX64 = re.compile(r"^[0-9a-f]{64}$")
HEX40 = re.compile(r"^[0-9a-f]{40}$")

#: The statements every PCF-bearing YAML output carries, in this
#: repository's words (the notice itself is APQC's, and copied).
NOT_MIT = ("The PCF material in this file -- element IDs, hierarchy IDs, "
           "names and descriptions -- is APQC's, used under APQC's licence, "
           "whose notice is `apqc_notice`. It is not covered by this "
           "repository's MIT licence (LICENSE); NOTICE.md at the repository "
           "root says which files carry it.")
NO_ENDORSEMENT = ("APQC does not produce, review or endorse the Business "
                  "Capability Ontology or this inventory.")
MARKS = ("Process Classification Framework® and PCF are APQC's marks. "
         "They are used here only to identify the source.")
STATUS = ("source evidence (scope approval D6); not vocabulary and not an "
          "admission to the ontology (Amendment 4). No element is judged a "
          "standing function or a capability here (E4 is open)")
E4 = {"state": "open",
      "judged": 0,
      "record": "docs/decisions/2026-10-28-i2-and-bpo-repin-decided.md",
      "note": ("E4 (Option A) asks for a written judgement of each level-3 "
               "element against CM-01's Standing Function, with a reason, "
               "independent evidence and a locator, for the architect's "
               "approval. Not performed in I-2b; no element is a candidate")}
PCF_8_0 = {"state": "deferred",
           "record": "docs/decisions/2026-10-29-apqc-pcf-sourcing-decided.md",
           "note": ("APQC80-1 deferred, with the 7.4-to-8.0 comparison, "
                    "until a version upgrade is planned")}
BRIDGE_NOTE = ("BPO's bridge (ADR-001 R4/R6), from Phase I-1's entries: "
               "evidence, not proof. I-1 found it is not a standing-function "
               "marker")

TOP_KEYS = ("format", "generator", "phase", "status", "decision",
            "citation", "apqc_notice", "apqc_notice_source", "licence",
            "endorsement", "marks", "source", "bridge_input", "e4",
            "pcf_8_0", "counts", "entries")
ENTRY_KEYS = ("id", "pcf_element_id", "pcf_hierarchy_id", "level",
              "parent_pcf_element_id", "name", "description", "bpo_iri",
              "locator", "bpo_bridge")
BRIDGE_KEYS = ("designated_by_catalog_node", "capability_class_with_this_code")


class Refused(SystemExit):
    """A question for whoever supplied the input, not for this tool."""


def root() -> Path:
    return layout.repository_root()


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


_MODULES: dict = {}


def harvest_module(base: Path):
    """harvest_bpo.py, imported by path once per file and content."""
    path = base / HARVEST
    key = (str(path.resolve()), sha256(path.read_bytes()))
    if key not in _MODULES:
        spec = importlib.util.spec_from_file_location(
            "bco_harvest_bpo_for_pcf", path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        _MODULES[key] = module
    return _MODULES[key]


def parse_yaml(text):
    import yaml

    loader = getattr(yaml, "CSafeLoader", yaml.SafeLoader)
    return yaml.load(text, Loader=loader)


def dump(data) -> str:
    """YAML as harvest_bpo.py writes it. libyaml's emitter when present:
    the entries are 1.2 MB and the pure-Python emitter takes seconds per
    rendering. tests/test_pcf_inventory.py requires the two emitters to
    give the same bytes for the committed file, so the output does not
    depend on which one a machine has."""
    import yaml

    dumper = getattr(yaml, "CSafeDumper", yaml.SafeDumper)
    return yaml.dump(data, Dumper=dumper, sort_keys=False,
                     allow_unicode=True, width=79, default_flow_style=False)


def header(lines) -> str:
    return "".join("# %s\n" % line if line else "#\n" for line in lines)


# ------------------------------------------------------------------ pins


def _hex(value, pattern) -> bool:
    return isinstance(value, str) and bool(pattern.match(value))


def pins(base: Path) -> dict:
    """config/inventory-pcf-sources.yaml, checked; the one source, with
    the file's shared keys attached."""
    path = base / PINS
    if not path.is_file():
        raise Refused(PINS + " is missing. Which BPO commit is the PCF "
                      "taken from?")
    raw = parse_yaml(path.read_bytes().decode("utf-8")) or {}
    found = [s for s in raw.get("sources") or [] if s.get("id") == SOURCE_ID]
    if len(found) != 1:
        raise Refused("%s pins %d source(s) with id %r; this tool reads "
                      "exactly one" % (PINS, len(found), SOURCE_ID))
    source = dict(found[0])
    for key in ("directory", "rights", "rights_source", "decision"):
        if not raw.get(key):
            raise Refused("%s declares no %r" % (PINS, key))
        source[key] = raw[key]
    for key in ("repository", "raw_base", "commit", "namespace", "scheme",
                "entry_prefix", "inputs", "apqc_notice_sha256", "outputs",
                "licence"):
        if not source.get(key):
            raise Refused("%s declares no %s for %s" % (PINS, key, SOURCE_ID))
    if not _hex(source["commit"], HEX40):
        raise Refused("%s: commit %r is not a full commit hash; a branch or "
                      "a short hash could move" % (PINS, source["commit"]))
    if not source["raw_base"].startswith(
            "https://raw.githubusercontent.com/"):
        raise Refused("%s: raw_base is not on raw.githubusercontent.com"
                      % PINS)
    for name in ("catalog", "notice"):
        item = source["inputs"].get(name) or {}
        if not item.get("path") or not _hex(item.get("sha256"), HEX64):
            raise Refused("%s: inputs.%s needs a path and a sha256"
                          % (PINS, name))
    if not source["inputs"]["notice"].get("section"):
        raise Refused("%s: inputs.notice names no section" % PINS)
    if not _hex(source["apqc_notice_sha256"], HEX64):
        raise Refused("%s: apqc_notice_sha256 is not a sha256" % PINS)
    outputs = source["outputs"]
    if outputs.get("notice") != ROOT_NOTICE:
        raise Refused("%s: outputs.notice must be %s, the repository-root "
                      "notice the decision asks for" % (PINS, ROOT_NOTICE))
    if not str(outputs.get("entries", "")).startswith(
            source["directory"] + "/"):
        raise Refused("%s: outputs.entries is outside %s"
                      % (PINS, source["directory"]))
    bearing = raw.get("pcf_bearing") or []
    exceptions = raw.get("exceptions") or []
    for n, item in enumerate(bearing):
        if not isinstance(item, dict) or set(item) != {"path", "carries"} \
                or not item["path"] or not item["carries"]:
            raise Refused("%s: pcf_bearing item %d needs exactly a path and "
                          "what it carries" % (PINS, n))
    for n, item in enumerate(exceptions):
        if not isinstance(item, dict) or set(item) != {"path", "reason"} \
                or not item["path"] or not item["reason"]:
            raise Refused("%s: exception %d needs exactly a path and a "
                          "reason" % (PINS, n))
    paths = [i["path"] for i in bearing]
    if len(paths) != len(set(paths)):
        raise Refused("%s lists a PCF-bearing file twice" % PINS)
    if outputs["entries"] not in paths:
        raise Refused("%s: pcf_bearing does not list %s, which this tool "
                      "writes" % (PINS, outputs["entries"]))
    for item in exceptions:
        if item["path"] not in paths:
            raise Refused("%s: the exception for %s names a file pcf_bearing "
                          "does not list" % (PINS, item["path"]))
        if item["path"] == outputs["entries"]:
            raise Refused("%s: %s is this tool's output and always carries "
                          "the notice; it cannot be an exception"
                          % (PINS, item["path"]))
    source["pcf_bearing"] = bearing
    source["exceptions"] = exceptions
    return source


def rights_citation(base: Path, source: dict) -> dict:
    """Rights holder, work, edition and register id, from rights.yaml."""
    data = parse_yaml((base / source["rights"]).read_bytes().decode("utf-8"))
    for item in data.get("sources") or []:
        if item.get("id") == source["rights_source"]:
            return {k: item[k] for k in ("rightsholder", "work", "edition",
                                         "register")}
    raise Refused("%s has no source %r; what is the citation?"
                  % (source["rights"], source["rights_source"]))


def fetched(base: Path, source: dict, cache: Path,
            network: bool) -> dict | None:
    """{catalog: bytes, notice: bytes} from the cache, or (network=True)
    from raw.githubusercontent.com at the pinned commit. None when offline
    and not cached."""
    harvest = harvest_module(base)
    out = {}
    for name in ("catalog", "notice"):
        item = source["inputs"][name]
        cache_file = cache / ("bpo-" + source["commit"]) / item["sha256"]
        if not network:
            if not cache_file.is_file() or \
                    sha256(cache_file.read_bytes()) != item["sha256"]:
                return None
            out[name] = cache_file.read_bytes()
            continue
        out[name] = harvest.fetch(
            harvest.raw_url(source, source["commit"], item["path"]),
            item["sha256"], cache_file, source["commit"])
    return out


# ---------------------------------------------------------------- notice


def extract_notice(text: str, section: str = NOTICE_SECTION,
                   what: str = "NOTICE.md") -> str:
    """The blockquote under `## <section>`, unwrapped into one paragraph.

    Exactly one heading, exactly one blockquote of one paragraph in its
    section; each `> ` line's text stripped and joined by single spaces.
    """
    lines = text.split("\n")
    heads = [n for n, line in enumerate(lines)
             if line.rstrip() == "## " + section]
    if len(heads) != 1:
        raise Refused("%s has %d '## %s' heading(s); APQC's notice is the "
                      "blockquote under exactly one" % (what, len(heads),
                                                         section))
    body = []
    for line in lines[heads[0] + 1:]:
        if line.startswith("#") and re.match(r"^#{1,2} ", line):
            break
        body.append(line)
    blocks, current = [], None
    for line in body:
        if line.startswith(">"):
            if current is None:
                current = []
                blocks.append(current)
            current.append(line)
        else:
            current = None
    if len(blocks) != 1:
        raise Refused("%s section '%s' holds %d blockquote(s); expected "
                      "exactly one, APQC's notice" % (what, section,
                                                      len(blocks)))
    parts = []
    for line in blocks[0]:
        content = line[1:].strip()
        if not content:
            raise Refused("%s section '%s': the blockquote has more than one "
                          "paragraph; the notice is one" % (what, section))
        parts.append(content)
    return " ".join(parts)


def rights_notice(graph, what: str = "the catalog") -> tuple[str, str]:
    """(BPO's framing, APQC's notice) from the one ontology header's one
    dct:rights, split at the first blank line."""
    from rdflib import URIRef

    headers = sorted(set(graph.subjects(URIRef(RDF + "type"),
                                        URIRef(OWL + "Ontology"))))
    if len(headers) != 1:
        raise Refused("%s has %d owl:Ontology header(s); expected one"
                      % (what, len(headers)))
    values = list(graph.objects(headers[0], URIRef(DCT + "rights")))
    if len(values) != 1:
        raise Refused("%s's ontology header carries %d dct:rights; expected "
                      "exactly one" % (what, len(values)))
    framing, blank, notice = str(values[0]).partition("\n\n")
    if not blank or not notice.strip():
        raise Refused("%s's dct:rights has no blank line separating BPO's "
                      "framing from APQC's notice" % what)
    return framing, notice


def verified_notice(source: dict, notice_md: bytes, graph) -> str:
    """APQC's notice, extracted from NOTICE.md and checked twice."""
    notice = extract_notice(notice_md.decode("utf-8"),
                            source["inputs"]["notice"]["section"],
                            "BPO's NOTICE.md at %s" % source["commit"][:7])
    if sha256(notice.encode("utf-8")) != source["apqc_notice_sha256"]:
        raise Refused("APQC's notice as extracted from BPO's NOTICE.md "
                      "digests to %s; %s pins %s. Did the notice change, or "
                      "the extraction?" % (sha256(notice.encode("utf-8")),
                                           PINS,
                                           source["apqc_notice_sha256"]))
    _framing, stated = rights_notice(graph, "BPO's %s at %s" % (
        source["inputs"]["catalog"]["path"], source["commit"][:7]))
    if stated != notice:
        raise Refused("APQC's notice in BPO's NOTICE.md is not the APQC "
                      "part of the catalog's dct:rights at the same commit; "
                      "the two statements of the notice disagree, and "
                      "neither is copied until they agree")
    return notice


# --------------------------------------------------------------- catalog


def level_of(hierarchy_id: str) -> int:
    parts = hierarchy_id.split(".")
    if len(parts) == 2 and int(parts[1]) == 0:
        return 1
    return len(parts)


def parent_hierarchy(hierarchy_id: str) -> str | None:
    parts = hierarchy_id.split(".")
    level = level_of(hierarchy_id)
    if level == 1:
        return None
    if level == 2:
        return parts[0] + ".0"
    return ".".join(parts[:-1])


def node_lines(text: str, namespace: str) -> dict:
    """{element id: line} where each catalog node's subject block starts."""
    harvest_prefixes = {}
    for match in re.finditer(
            r"(?m)^\s*(?:@prefix|PREFIX)\s+([A-Za-z][\w.-]*|):\s*<([^>]*)>",
            text):
        harvest_prefixes[match.group(1)] = match.group(2)
    labels = [re.escape(k) for k, v in harvest_prefixes.items()
              if v == namespace]
    forms = [r"<%sPCF_(\d+)>" % re.escape(namespace)]
    forms += [r"%s:PCF_(\d+)" % label for label in labels]
    pattern = re.compile(r"^(?:%s)\s" % "|".join(forms))
    found: dict = {}
    for number, line in enumerate(text.split("\n"), start=1):
        match = pattern.match(line)
        if match:
            eid = next(g for g in match.groups() if g)
            found.setdefault(eid, []).append(number)
    return found


def read_catalog(data: bytes, source: dict) -> dict:
    """{graph, nodes} from the catalog's bytes, refusing rather than
    guessing."""
    from rdflib import Graph, Literal, URIRef

    graph = Graph()
    graph.parse(data=data.decode("utf-8"), format="turtle")
    ns = source["namespace"]
    scheme = URIRef(source["scheme"])
    p_id, p_hid = URIRef(ns + "pcfID"), URIRef(ns + "hierarchyID")
    p_text = URIRef(ns + "apqcSourceText")
    p_label, p_broader = URIRef(SKOS + "prefLabel"), URIRef(SKOS + "broader")
    p_scheme, p_comment = URIRef(SKOS + "inScheme"), URIRef(RDFS + "comment")
    concepts = sorted(set(graph.subjects(URIRef(RDF + "type"),
                                         URIRef(SKOS + "Concept"))))
    if not concepts:
        raise Refused("the catalog has no skos:Concept; is it BPO's PCF "
                      "catalog?")
    lines = node_lines(data.decode("utf-8"), ns)

    def one(node, prop, where, optional=False):
        values = list(graph.objects(node, prop))
        if len(values) > 1 or (not values and not optional):
            raise Refused("%s carries %d %s; expected %s" % (
                where, len(values), prop, "at most one" if optional
                else "exactly one"))
        if values and not isinstance(values[0], Literal):
            raise Refused("%s: %s is not a literal" % (where, prop))
        return str(values[0]) if values else None

    nodes, by_iri, by_hid = [], {}, {}
    for concept in concepts:
        if set(graph.objects(concept, p_scheme)) != {scheme}:
            raise Refused("catalog concept %s is not in the PCF scheme alone"
                          % concept)
        where = "catalog concept %s" % concept
        eid = one(concept, p_id, where)
        if not ELEMENT_ID.match(eid):
            raise Refused("%s: bpo:pcfID is not digits" % where)
        where = "PCF element %s" % eid
        if str(concept) != ns + "PCF_" + eid:
            raise Refused("%s: its IRI is not BPO's PCF_<element id>"
                          % where)
        hid = one(concept, p_hid, where)
        if not HIERARCHY_ID.match(hid):
            raise Refused("%s: bpo:hierarchyID is not dotted digits" % where)
        name = one(concept, p_label, where)
        if not name.strip():
            raise Refused("%s: skos:prefLabel is empty" % where)
        description = one(concept, p_text, where, optional=True)
        level = level_of(hid)
        for comment in graph.objects(concept, p_comment):
            match = re.fullmatch(r"APQC level: (\w+)", str(comment))
            if match and LEVEL_NAMES.get(match.group(1)) != level:
                raise Refused("%s: BPO's comment says level %r, its "
                              "hierarchy id says %d" % (where,
                                                        match.group(1),
                                                        level))
        where_lines = lines.get(eid) or []
        if len(where_lines) != 1:
            raise Refused("%s: its subject block starts on %d line(s) of "
                          "the catalog; expected one" % (where,
                                                         len(where_lines)))
        node = {"element_id": eid, "hierarchy_id": hid, "level": level,
                "name": name, "description": description,
                "iri": str(concept), "line": where_lines[0],
                "broader": sorted(str(b) for b in
                                  graph.objects(concept, p_broader))}
        if str(concept) in by_iri:
            raise Refused("%s appears twice" % where)
        if hid in by_hid:
            raise Refused("%s repeats the hierarchy id of PCF element %s"
                          % (where, by_hid[hid]["element_id"]))
        by_iri[str(concept)] = by_hid[hid] = node
        nodes.append(node)
    ids = [n["element_id"] for n in nodes]
    if len(ids) != len(set(ids)):
        raise Refused("the catalog repeats a bpo:pcfID")
    for node in nodes:
        where = "PCF element %s" % node["element_id"]
        parent_hid = parent_hierarchy(node["hierarchy_id"])
        broader = node.pop("broader")
        if parent_hid is None:
            if broader:
                raise Refused("%s is level 1 and has a skos:broader" % where)
            node["parent"] = None
            continue
        if parent_hid not in by_hid:
            raise Refused("%s: no element holds its parent hierarchy id"
                          % where)
        parent = by_hid[parent_hid]
        if broader != [parent["iri"]]:
            raise Refused("%s: its skos:broader is not the element its "
                          "hierarchy id names as parent" % where)
        node["parent"] = parent["element_id"]
    if not any(n["level"] == 1 for n in nodes):
        raise Refused("the catalog has no level-1 element; is it the PCF?")
    return {"graph": graph, "nodes": nodes}


def hierarchy_key(hierarchy_id: str) -> tuple:
    return tuple(int(p) for p in hierarchy_id.split("."))


# ---------------------------------------------------------------- bridge


def bpo_bridges(entries_document: dict) -> dict:
    """{pcf code: {designated_by_catalog_node, capability_class_with_this_code}}
    from I-1's entries."""
    out: dict = {}

    def slot(code):
        return out.setdefault(str(code), {BRIDGE_KEYS[0]: [],
                                          BRIDGE_KEYS[1]: []})

    for entry in entries_document.get("entries") or []:
        if entry.get("kind") != "capability-class":
            continue
        for bridge in entry.get("designated_by") or []:
            if bridge.get("pcf_code") is None:
                continue
            slot(bridge["pcf_code"])[BRIDGE_KEYS[0]].append(
                {"capability_class_entry": entry["id"],
                 "capability_class_iri": entry["iri"],
                 "catalog_node": bridge["node"],
                 "module": bridge["module"]})
        if entry.get("pcf_code") is not None:
            slot(entry["pcf_code"])[BRIDGE_KEYS[1]].append(
                {"capability_class_entry": entry["id"],
                 "capability_class_iri": entry["iri"]})
    for value in out.values():
        value[BRIDGE_KEYS[0]].sort(key=lambda b: (
            b["capability_class_entry"], b["catalog_node"], b["module"]))
        value[BRIDGE_KEYS[1]].sort(key=lambda b: b["capability_class_entry"])
    return out


# ----------------------------------------------------------------- build


def blob_url(source: dict, path: str, line: int | None = None) -> str:
    url = "%s/blob/%s/%s" % (source["repository"], source["commit"], path)
    return url + ("#L%d" % line if line else "")


def entries(nodes: list[dict], source: dict, bridges: dict) -> list[dict]:
    out = []
    path = source["inputs"]["catalog"]["path"]
    for node in nodes:
        out.append({
            "id": "%s-%s" % (source["entry_prefix"], node["element_id"]),
            "pcf_element_id": node["element_id"],
            "pcf_hierarchy_id": node["hierarchy_id"],
            "level": node["level"],
            "parent_pcf_element_id": node["parent"],
            "name": node["name"],
            "description": node["description"],
            "bpo_iri": node["iri"],
            "locator": blob_url(source, path, node["line"]),
            "bpo_bridge": bridges.get(node["element_id"]),
        })
    out.sort(key=lambda e: hierarchy_key(e["pcf_hierarchy_id"]))
    return out


def counts_of(items: list[dict]) -> dict:
    levels: dict = {}
    for item in items:
        levels[item["level"]] = levels.get(item["level"], 0) + 1
    return {
        "elements": len(items),
        "by_level": {"level_%d" % k: levels[k] for k in sorted(levels)},
        "with_description": sum(1 for i in items if i["description"]),
        "with_parent": sum(1 for i in items
                           if i["parent_pcf_element_id"] is not None),
        "bpo_bridged": sum(1 for i in items if i["bpo_bridge"]
                           and i["bpo_bridge"][BRIDGE_KEYS[0]]),
        "bpo_coded": sum(1 for i in items if i["bpo_bridge"]
                         and i["bpo_bridge"][BRIDGE_KEYS[1]]),
    }


def citation_text(source: dict, citation: dict) -> str:
    return ("%s, version %s, by %s (register %s); taken from the Business "
            "Process Ontology, %s at commit %s (%s)."
            % (citation["work"], citation["edition"],
               citation["rightsholder"], citation["register"],
               source["inputs"]["catalog"]["path"], source["commit"],
               source["repository"]))


def notice_source(source: dict) -> dict:
    item = source["inputs"]["notice"]
    return {"repository": source["repository"], "commit": source["commit"],
            "path": item["path"], "sha256": item["sha256"],
            "section": item["section"],
            "notice_sha256": source["apqc_notice_sha256"]}


def entries_document(source: dict, citation: dict, notice: str,
                     items: list[dict], bridge_digest: str,
                     unmatched: list[str]) -> dict:
    catalog = source["inputs"]["catalog"]
    return {
        "format": FORMAT,
        "generator": GENERATOR,
        "phase": "I-2b",
        "status": STATUS,
        "decision": source["decision"],
        "citation": citation_text(source, citation),
        "apqc_notice": notice,
        "apqc_notice_source": notice_source(source),
        "licence": NOT_MIT,
        "endorsement": NO_ENDORSEMENT,
        "marks": MARKS,
        "source": {
            "rightsholder": citation["rightsholder"],
            "work": citation["work"],
            "edition": citation["edition"],
            "register": citation["register"],
            "repository": source["repository"],
            "commit": source["commit"],
            "path": catalog["path"],
            "sha256": catalog["sha256"],
            "scheme": source["scheme"],
        },
        "bridge_input": {"path": BPO_ENTRIES, "sha256": bridge_digest,
                         "note": BRIDGE_NOTE,
                         "codes_not_in_the_catalog": unmatched},
        "e4": dict(E4),
        "pcf_8_0": dict(PCF_8_0),
        "counts": counts_of(items),
        "entries": items,
    }


ENTRIES_HEADER = [
    "GENERATED by tools/inventory/harvest_pcf.py --write. Do not edit: the",
    "offline check requires this file to be the generator's rendering of",
    "its data, and --confirm a fresh build from BPO to reproduce it.",
    "",
    "Capability Term Inventory, Phase I-2b: the APQC Process Classification",
    "Framework (PCF), Cross-Industry, version 7.4, every element, as the",
    "Business Process Ontology's catalog states it at the pinned commit.",
    "Source evidence, not vocabulary, and not an admission to the ontology.",
    "",
    "This material is APQC's, used under APQC's licence; APQC's notice is the",
    "`apqc_notice` field below, copied from BPO's NOTICE.md. It is not",
    "covered by this repository's MIT licence. APQC does not endorse this",
    "work. Keep the notice with any copy or derivative of this file. See",
    "NOTICE.md at the repository root, and docs/sources/inventory/README.md.",
]


def entries_bytes(document: dict) -> bytes:
    return (header(ENTRIES_HEADER) + "\n" + dump(document)).encode("utf-8")


def notice_bytes(source: dict, citation: dict, notice: str) -> bytes:
    """The repository-root NOTICE.md, from the pins and the notice."""
    catalog = source["inputs"]["catalog"]
    item = source["inputs"]["notice"]
    exceptions = {e["path"]: e["reason"] for e in source["exceptions"]}
    lines = [
        "# Notice: APQC Process Classification Framework® material",
        "",
        "<!-- GENERATED by %s --write from %s. Do not edit; %s -->"
        % (GENERATOR, PINS, "the offline check requires a fresh generation"),
        "",
        "This repository holds two kinds of material, under different terms.",
        "",
        "| Material | Terms |",
        "|---|---|",
        "| The Business Capability Ontology's own work: the specification, "
        "the conceptual models, the vocabulary, the ontology modules and "
        "shapes, the tools, the tests, the site and the documentation | "
        "MIT, see [`LICENSE`](LICENSE) |",
        "| Material derived from the **%s, version %s**: element IDs, "
        "hierarchy IDs, element names and element descriptions, in the "
        "files listed below | APQC's licence, whose notice is reproduced "
        "below. **The MIT licence does not cover this material.** |"
        % (citation["work"].replace("Process Classification Framework",
                                    "Process Classification "
                                    "Framework®"),
           citation["edition"]),
        "",
        "Other third-party material is attributed where it lives: the "
        "vendored ontologies in `vendor/NOTICE.md`, the site's vendored "
        "assets in `vendor/site/NOTICE.md`, and the inventory's BPO text in "
        "`docs/sources/inventory/NOTICE.md`.",
        "",
        "## Source",
        "",
        " ".join(source["licence"]["attribution"].split()),
        "",
        "- repository: %s" % source["repository"],
        "- commit: `%s`" % source["commit"],
        "- catalog: `%s`, sha256 `%s`" % (catalog["path"], catalog["sha256"]),
        "- notice: `%s`, sha256 `%s`" % (item["path"], item["sha256"]),
        "- decision: `%s`" % source["decision"],
        "",
        "PCF material is taken only from BPO at a pinned commit that carries "
        "BPO's `NOTICE.md`; nothing is fetched from apqc.org.",
        "",
        "## %s" % PCF_SECTION,
        "",
    ]
    for entry in source["pcf_bearing"]:
        line = "- `%s`: %s." % (entry["path"],
                                " ".join(entry["carries"].split()))
        if entry["path"] in exceptions:
            line += (" **Does not yet carry the notice**: %s."
                     % " ".join(exceptions[entry["path"]].split()))
        else:
            line += " Carries the notice."
        lines.append(line)
    lines += [
        "",
        "`%s` fails when a tracked file carries PCF content and is not "
        "listed here, or lacks the notice without a recorded exception."
        % GATE,
        "",
        "## %s" % NOTICE_SECTION,
        "",
        "Copied by `%s` from the \"%s\" section of BPO's `%s` at commit "
        "`%s` (sha256 `%s`), which states that it reproduces the notice "
        "verbatim from the Copyright and attribution sheet of APQC's PCF "
        "7.4 workbook; the tool requires it to equal the APQC part of "
        "`dct:rights` in BPO's `%s` at the same commit. Its sha256 (UTF-8) "
        "is `%s`. APQC's licence requires a copy of it in every copy of the "
        "PCF and in every derivative work."
        % (GENERATOR, item["section"], item["path"], source["commit"],
           item["sha256"], catalog["path"], source["apqc_notice_sha256"]),
        "",
        "> %s" % notice,
        "",
        "## Also",
        "",
        "- **No endorsement.** %s" % NO_ENDORSEMENT,
        "- **Trademarks.** %s" % MARKS,
        "- **Redistributing.** If you copy or adapt a file listed above, "
        "keep this notice with it.",
    ]
    return ("\n".join(lines) + "\n").encode("utf-8")


def listed_files(text: str) -> list[str]:
    """The paths NOTICE.md lists under its PCF-bearing section."""
    out, inside = [], False
    for line in text.split("\n"):
        if line.startswith("## "):
            inside = line.rstrip() == "## " + PCF_SECTION
            continue
        if inside:
            match = re.match(r"^- `([^`]+)`", line)
            if match:
                out.append(match.group(1))
    return out


def build(base: Path, fetched_files: dict) -> dict:
    """Both outputs, as bytes, keyed by repository path. Writes nothing."""
    source = pins(base)
    citation = rights_citation(base, source)
    read = read_catalog(fetched_files["catalog"], source)
    notice = verified_notice(source, fetched_files["notice"], read["graph"])
    bridge_raw = (base / BPO_ENTRIES).read_bytes()
    bridges = bpo_bridges(parse_yaml(bridge_raw.decode("utf-8")))
    known = {n["element_id"] for n in read["nodes"]}
    unmatched = sorted((c for c in bridges if c not in known), key=int)
    items = entries(read["nodes"], source, bridges)
    document = entries_document(source, citation, notice, items,
                                sha256(bridge_raw), unmatched)
    return {source["outputs"]["entries"]: entries_bytes(document),
            ROOT_NOTICE: notice_bytes(source, citation, notice)}


# ----------------------------------------------------------------- check


def _closed(mapping, keys, where, out) -> bool:
    if not isinstance(mapping, dict):
        out.append("%s is not a mapping" % where)
        return False
    extra = sorted(set(mapping) - set(keys), key=str)
    missing = sorted(set(keys) - set(mapping))
    for key in extra:
        out.append("%s carries %r, which this file does not define"
                   % (where, key))
    for key in missing:
        out.append("%s declares no %r" % (where, key))
    if not extra and list(mapping) != list(keys):
        out.append("%s's keys are not in the generator's order" % where)
    return not extra and not missing


def entries_findings(document, base: Path, source: dict,
                     citation: dict) -> list[str]:
    """Every rule the offline check holds the entries file to."""
    out: list[str] = []
    where = source["outputs"]["entries"]
    if not _closed(document, TOP_KEYS, where, out):
        return out
    if document["format"] != FORMAT or document["generator"] != GENERATOR \
            or document["phase"] != "I-2b":
        out.append("%s is not format %d of %s, phase I-2b"
                   % (where, FORMAT, GENERATOR))
    notice = document["apqc_notice"]
    if not isinstance(notice, str) or sha256(notice.encode("utf-8")) \
            != source["apqc_notice_sha256"]:
        out.append("%s: apqc_notice is not APQC's notice as copied from "
                   "BPO's NOTICE.md (its sha256 is not the pin in %s)"
                   % (where, PINS))
    expected = entries_document(source, citation, notice, [], "", [])
    for key in ("status", "decision", "citation", "apqc_notice_source",
                "licence", "endorsement", "marks", "source", "e4",
                "pcf_8_0"):
        if document[key] != expected[key]:
            out.append("%s: %s is not what the pins, %s and the decision "
                       "give" % (where, key, source["rights"]))
    if not (base / source["decision"]).is_file():
        out.append("%s: the decision %s does not exist"
                   % (where, source["decision"]))

    items = document["entries"]
    if not isinstance(items, list) or not items:
        out.append("%s holds no entries" % where)
        return out
    by_id, seen_hids = {}, set()
    for n, item in enumerate(items):
        ew = "%s entry %d" % (where, n)
        if not _closed(item, ENTRY_KEYS, ew, out):
            continue
        eid = item["pcf_element_id"]
        if not isinstance(eid, str) or not ELEMENT_ID.match(eid):
            out.append("%s: pcf_element_id is not a string of digits" % ew)
            continue
        ew = "%s, PCF element %s" % (where, eid)
        if item["id"] != "%s-%s" % (source["entry_prefix"], eid):
            out.append("%s: its id is not %s-<element id>"
                       % (ew, source["entry_prefix"]))
        hid = item["pcf_hierarchy_id"]
        if not isinstance(hid, str) or not HIERARCHY_ID.match(hid):
            out.append("%s: pcf_hierarchy_id is not dotted digits" % ew)
            continue
        if item["level"] != level_of(hid):
            out.append("%s: its level is not its hierarchy id's" % ew)
        if not isinstance(item["name"], str) or not item["name"].strip():
            out.append("%s has no name" % ew)
        if item["description"] is not None and \
                not isinstance(item["description"], str):
            out.append("%s: description is not text" % ew)
        if item["bpo_iri"] != source["namespace"] + "PCF_" + eid:
            out.append("%s: bpo_iri is not BPO's PCF_<element id>" % ew)
        if not re.fullmatch(re.escape(blob_url(
                source, source["inputs"]["catalog"]["path"])) + r"#L\d+",
                str(item["locator"])):
            out.append("%s: its locator is not a line of the pinned catalog"
                       % ew)
        if eid in by_id or hid in seen_hids:
            out.append("%s repeats an element or hierarchy id" % ew)
        by_id[eid] = item
        seen_hids.add(hid)
    if out:
        return out
    hids = [i["pcf_hierarchy_id"] for i in items]
    if hids != sorted(hids, key=hierarchy_key):
        out.append("%s is not sorted by hierarchy id, so it is not what the "
                   "tool writes" % where)
    for item in items:
        ew = "%s, PCF element %s" % (where, item["pcf_element_id"])
        parent = item["parent_pcf_element_id"]
        if item["level"] == 1:
            if parent is not None:
                out.append("%s is level 1 and names a parent" % ew)
            continue
        if parent not in by_id:
            out.append("%s names a parent that is not an entry" % ew)
            continue
        if by_id[parent]["pcf_hierarchy_id"] != parent_hierarchy(
                item["pcf_hierarchy_id"]):
            out.append("%s: its parent's hierarchy id is not its own, one "
                       "level up" % ew)

    bridge_raw = (base / BPO_ENTRIES).read_bytes()
    bridges = bpo_bridges(parse_yaml(bridge_raw.decode("utf-8")))
    recorded = document["bridge_input"]
    if not isinstance(recorded, dict) or recorded.get("path") != BPO_ENTRIES \
            or recorded.get("sha256") != sha256(bridge_raw) \
            or recorded.get("note") != BRIDGE_NOTE:
        out.append("%s was built from a %s other than the committed one; "
                   "run --write" % (where, BPO_ENTRIES))
    else:
        unmatched = sorted((c for c in bridges if c not in by_id), key=int)
        if recorded.get("codes_not_in_the_catalog") != unmatched \
                or set(recorded) != {"path", "sha256", "note",
                                     "codes_not_in_the_catalog"}:
            out.append("%s: bridge_input does not list the bridge's codes "
                       "the catalog lacks" % where)
        for item in items:
            if item["bpo_bridge"] != bridges.get(item["pcf_element_id"]):
                out.append("%s, PCF element %s: bpo_bridge is not what %s "
                           "gives" % (where, item["pcf_element_id"],
                                      BPO_ENTRIES))
    if document["counts"] != counts_of(items):
        out.append("%s states counts %r; its entries give %r"
                   % (where, document["counts"], counts_of(items)))
    return out


def check(base: Path, cache: Path,
          fetched_files: dict | None = None) -> tuple[list[str], list[str]]:
    """(findings, notes): offline, plus byte identity when the pinned
    files are at hand."""
    source = pins(base)
    citation = rights_citation(base, source)
    notes: list[str] = []
    path = base / source["outputs"]["entries"]
    notice_path = base / ROOT_NOTICE
    out = []
    for p in (path, notice_path):
        if not p.is_file():
            out.append("%s is missing. Run `python %s --write`"
                       % (p.relative_to(base).as_posix(), GENERATOR))
    if out:
        return out, notes
    raw = path.read_bytes()
    for p, data in ((path, raw), (notice_path, notice_path.read_bytes())):
        if b"\r\n" in data:
            out.append("%s has CRLF line endings; digests here are over LF "
                       "bytes" % p.relative_to(base).as_posix())
    if out:
        return out, notes
    document = parse_yaml(raw.decode("utf-8"))
    out = entries_findings(document, base, source, citation)
    if out:
        return out, notes
    if entries_bytes(document) != raw:
        out.append("%s is not the generator's rendering of its own data; "
                   "was it edited by hand?" % source["outputs"]["entries"])
    fresh = notice_bytes(source, citation, document["apqc_notice"])
    if notice_path.read_bytes() != fresh:
        out.append("%s is not what %s writes from %s; was it edited by hand, "
                   "or the pins changed without --write?"
                   % (ROOT_NOTICE, GENERATOR, PINS))
    harvest = harvest_module(base)
    out += harvest.admission_findings(base, source["directory"], {})
    if fetched_files is None:
        fetched_files = fetched(base, source, cache, network=False)
    if fetched_files is None:
        notes.append("BPO's catalog and NOTICE.md at %s are not cached, so "
                     "the outputs were checked offline only; --confirm "
                     "rebuilds them from GitHub" % source["commit"][:7])
        return out, notes
    built = build(base, fetched_files)
    for name, data in sorted(built.items()):
        if (base / name).read_bytes() != data:
            out.append("%s is not what building from the pinned BPO files "
                       "produces; run --write" % name)
    return out, notes


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    mode = ap.add_mutually_exclusive_group()
    mode.add_argument("--write", action="store_true",
                      help="read the pinned BPO files (cache, else GitHub) "
                           "and write the entries and NOTICE.md")
    mode.add_argument("--confirm", action="store_true",
                      help="read the pinned BPO files (cache, else GitHub) "
                           "and require both outputs byte for byte")
    ap.add_argument("--cache", default=None,
                    help="download cache (default %s/)" % CACHE)
    args = ap.parse_args(argv)
    base = root()
    cache = Path(args.cache) if args.cache else base / CACHE
    source = pins(base)

    files = None
    if args.write or args.confirm:
        files = fetched(base, source, cache, network=True)
        built = build(base, files)
        differing = sorted(name for name, data in built.items()
                           if not (base / name).is_file()
                           or (base / name).read_bytes() != data)
        if args.confirm and differing:
            print("  FINDING: %d output(s) are not what building from BPO "
                  "at the pinned commit produces: %s"
                  % (len(differing), ", ".join(differing)))
            return 1
        if args.write:
            for name, data in sorted(built.items()):
                (base / name).write_bytes(data)
                print("  wrote %s%s" % (name, "" if name in differing
                                        else " (unchanged)"))
    problems, notes = check(base, cache, files)
    for note in notes:
        print("  note: %s" % note)
    if problems:
        for problem in problems:
            print("  FINDING: %s" % problem)
        return 1
    document = parse_yaml((base / source["outputs"]["entries"]).read_bytes()
                          .decode("utf-8"))
    counts = document["counts"]
    print("  ok: %s holds %d PCF 7.4 elements (%s) from BPO %s, with APQC's "
          "notice (sha256 %s); %d bridged by BPO; %s is fresh%s; E4 open; "
          "PCF 8.0 deferred"
          % (source["outputs"]["entries"], counts["elements"],
             ", ".join("%s %d" % (k, v) for k, v in
                       counts["by_level"].items()),
             source["commit"][:7], source["apqc_notice_sha256"][:12],
             counts["bpo_bridged"], ROOT_NOTICE,
             "; a fresh build from BPO reproduces both" if files is not None
             or fetched(base, source, cache, network=False) is not None
             else ""))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
