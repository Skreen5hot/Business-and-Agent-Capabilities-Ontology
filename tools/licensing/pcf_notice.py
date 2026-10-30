# SPDX-License-Identifier: MIT
"""Every tracked file that carries APQC PCF material carries APQC's notice.

    python tools/licensing/pcf_notice.py      # exit 1 on a finding

The gate the architect's decision of 2026-10-29 asks for
(docs/decisions/2026-10-29-apqc-pcf-sourcing-decided.md, section 4: "a
check that fails when a PCF-bearing artifact lacks the notice"). It reads
the tracked files (`git ls-files`), never a list of filenames, so a new
PCF-bearing file is found the day it is committed.

WHAT MAKES A FILE PCF-BEARING

Structure, not prose. A file is PCF-bearing when it holds PCF element IDs,
hierarchy IDs, names or descriptions as data:

  YAML or JSON  any mapping key, at any depth, in PCF_KEYS: the fields
                this repository's tools use for a PCF element id or
                hierarchy id (`pcf_code`, `pcf_element_id`, ...), or BPO's
                annotations spelled as keys.
  RDF (Turtle and the other serializations rdflib reads by suffix)
                any triple whose predicate's local name is bpo:pcfID,
                bpo:hierarchyID or bpo:apqcSourceText (in any namespace,
                so a renamed BPO namespace is still caught), or any
                skos:inScheme of BPO's PCF scheme.

Markdown, HTML and other prose are not read: a citation of a PCF element
in an argument is not a copy of the catalog, and this rule cannot tell a
quoted PCF name from the same words in a sentence. That residue is stated
in docs/sources/inventory/README.md.

WHAT CARRYING THE NOTICE MEANS

The notice is APQC's, as tools/inventory/harvest_pcf.py copied it from
BPO's NOTICE.md into the repository-root NOTICE.md. This gate takes it
from there and requires its sha256 to be the one
config/inventory-pcf-sources.yaml pins (apqc_notice_sha256), so a notice
altered anywhere -- in NOTICE.md or in an artifact -- is refused, and
nothing here retypes it.

  YAML or JSON  a top-level `apqc_notice` whose value is the notice,
                exactly.
  RDF           exactly one owl:Ontology header, carrying exactly one
                dct:rights, whose value contains the notice exactly.

NOTICE.md must list exactly the PCF-bearing files, and must be what
harvest_pcf.py generates from the pins. A PCF-bearing file without the
notice is a finding unless config/inventory-pcf-sources.yaml lists it in
`exceptions` with a reason; an exception for a file that no longer needs
one (untracked, not PCF-bearing, or carrying the notice) is a finding too,
so the list cannot outlive its reason. Today it holds Phase I-1's
bpo-entries.yaml, which only the E7 pull request may change.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

TOOL_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(TOOL_ROOT / "tools"))

import layout  # noqa: E402

HARVEST_PCF = "tools/inventory/harvest_pcf.py"

#: Keys whose value is a PCF element id, hierarchy id or description.
PCF_KEYS = frozenset({"pcf_code", "pcf_id", "pcf_element_id",
                      "pcf_hierarchy_id", "parent_pcf_element_id",
                      "element_id", "hierarchy_id", "pcfID", "hierarchyID",
                      "apqcSourceText", "apqc_source_text"})
#: BPO's provenance annotations for PCF material, by local name.
PCF_PREDICATES = frozenset({"pcfID", "hierarchyID", "apqcSourceText"})
DATA_SUFFIXES = (".yaml", ".yml", ".json")
RDF_SUFFIXES = {".ttl": "turtle", ".nt": "nt", ".n3": "n3",
                ".owl": "xml", ".rdf": "xml", ".jsonld": "json-ld",
                ".trig": "trig", ".nq": "nquads"}

RDF_TYPE = "http://www.w3.org/1999/02/22-rdf-syntax-ns#type"
OWL_ONTOLOGY = "http://www.w3.org/2002/07/owl#Ontology"
DCT_RIGHTS = "http://purl.org/dc/terms/rights"
SKOS_IN_SCHEME = "http://www.w3.org/2004/02/skos/core#inScheme"

#: Every finding this gate can report, by the words it is reported in.
#: tests/test_pcf_notice.py fires each one on a negative fixture and pins
#: this tuple, so a new refusal arrives with its test.
NO_ROOT_NOTICE = "NOTICE.md does not reproduce APQC's notice"
STALE_NOTICE = "NOTICE.md is not a fresh generation"
UNREADABLE = "cannot be parsed, so whether it carries PCF material is unknown"
LACKS = "is PCF-bearing and carries no APQC notice"
ALTERED = "carries a notice that is not APQC's notice as copied from BPO"
RIGHTS_SHAPE = ("must carry the notice in exactly one dct:rights on exactly "
                "one ontology header")
UNLISTED = "is PCF-bearing and NOTICE.md does not list it"
OVERLISTED = "is listed in NOTICE.md as PCF-bearing but"
STALE_EXCEPTION = "has an exception in config/inventory-pcf-sources.yaml but"
MESSAGES = (NO_ROOT_NOTICE, STALE_NOTICE, UNREADABLE, LACKS, ALTERED,
            RIGHTS_SHAPE, UNLISTED, OVERLISTED, STALE_EXCEPTION)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


_HARVEST: dict = {}


def harvest_pcf():
    """tools/inventory/harvest_pcf.py, from this tool's own repository."""
    if "module" not in _HARVEST:
        spec = importlib.util.spec_from_file_location(
            "bco_harvest_pcf_for_gate", TOOL_ROOT / HARVEST_PCF)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        _HARVEST["module"] = module
    return _HARVEST["module"]


def tracked_files(base: Path) -> dict[str, bytes]:
    result = subprocess.run(["git", "-C", str(base), "ls-files", "-z"],
                            capture_output=True)
    if result.returncode:
        raise SystemExit("git ls-files failed, so the tracked files are "
                         "unknown: %s" % result.stderr.decode(
                             "utf-8", "replace").strip()[-300:])
    out = {}
    for name in result.stdout.decode("utf-8").split("\0"):
        if name and (base / name).is_file():
            out[name] = (base / name).read_bytes()
    return out


# ------------------------------------------------------------ detection


def _keys(data):
    if isinstance(data, dict):
        for key, value in data.items():
            yield key
            yield from _keys(value)
    elif isinstance(data, list):
        for value in data:
            yield from _keys(value)


def _local(iri: str) -> str:
    return iri.rsplit("#", 1)[-1].rsplit("/", 1)[-1]


def read(path: str, data: bytes, scheme: str):
    """(kind, parsed, bearing) -- kind "data", "rdf" or None (not read).

    Raises ValueError when a file of a read kind does not parse."""
    lower = path.lower()
    if lower.endswith(DATA_SUFFIXES):
        text = data.decode("utf-8")
        if lower.endswith(".json"):
            parsed = json.loads(text)
        else:
            import yaml

            loader = getattr(yaml, "CSafeLoader", yaml.SafeLoader)
            try:
                parsed = yaml.load(text, Loader=loader)
            except yaml.YAMLError as error:
                raise ValueError(str(error)) from None
        bearing = any(isinstance(k, str) and k in PCF_KEYS
                      for k in _keys(parsed))
        return "data", parsed, bearing
    suffix = Path(lower).suffix
    if suffix in RDF_SUFFIXES:
        from rdflib import Graph

        graph = Graph()
        try:
            graph.parse(data=data, format=RDF_SUFFIXES[suffix])
        except Exception as error:  # rdflib raises many types
            raise ValueError("%s: %s" % (type(error).__name__,
                                         str(error)[:200])) from None
        bearing = False
        for _s, p, o in graph:
            if _local(str(p)) in PCF_PREDICATES or (
                    str(p) == SKOS_IN_SCHEME and str(o) == scheme):
                bearing = True
                break
        return "rdf", graph, bearing
    return None, None, False


def carries(kind: str, parsed, notice: str) -> str | None:
    """None when the file carries the notice, else the finding's words."""
    if kind == "data":
        if not isinstance(parsed, dict) or "apqc_notice" not in parsed:
            return LACKS
        return None if parsed["apqc_notice"] == notice else ALTERED
    from rdflib import URIRef

    headers = set(parsed.subjects(URIRef(RDF_TYPE), URIRef(OWL_ONTOLOGY)))
    rights = [o for h in headers for o in parsed.objects(h, URIRef(
        DCT_RIGHTS))]
    if not rights and len(headers) <= 1:
        return LACKS
    if len(headers) != 1 or len(rights) != 1:
        return "%s (it has %d header(s) and %d dct:rights)" % (
            RIGHTS_SHAPE, len(headers), len(rights))
    return None if notice in str(rights[0]) else ALTERED


# ----------------------------------------------------------------- gate


def findings(base: Path,
             files: dict[str, bytes] | None = None) -> tuple[list, dict]:
    """(findings, report) over `files` ({path: bytes}; default: tracked)."""
    h = harvest_pcf()
    source = h.pins(base)
    if files is None:
        files = tracked_files(base)
    out: list[str] = []
    report = {"scanned": 0, "bearing": {}, "excepted": []}

    root_notice = files.get(h.ROOT_NOTICE)
    if root_notice is None:
        return ["%s: %s is not tracked" % (NO_ROOT_NOTICE, h.ROOT_NOTICE)], \
            report
    text = root_notice.decode("utf-8")
    try:
        notice = h.extract_notice(text, h.NOTICE_SECTION, h.ROOT_NOTICE)
    except SystemExit as refusal:
        return ["%s: %s" % (NO_ROOT_NOTICE, refusal)], report
    if sha256(notice.encode("utf-8")) != source["apqc_notice_sha256"]:
        return ["%s: the blockquote under '## %s' digests to %s, and %s pins "
                "%s" % (NO_ROOT_NOTICE, h.NOTICE_SECTION,
                        sha256(notice.encode("utf-8")), h.PINS,
                        source["apqc_notice_sha256"])], report
    citation = h.rights_citation(base, source)
    if root_notice != h.notice_bytes(source, citation, notice):
        out.append("%s: it is not what %s writes from %s; run `python %s "
                   "--write`" % (STALE_NOTICE, h.GENERATOR, h.PINS,
                                 h.GENERATOR))

    exceptions = {e["path"]: e["reason"] for e in source["exceptions"]}
    bearing: dict[str, str | None] = {}
    for path in sorted(files):
        try:
            kind, parsed, is_bearing = read(path, files[path],
                                            source["scheme"])
        except (ValueError, UnicodeDecodeError) as error:
            out.append("%s %s (%s)" % (path, UNREADABLE, error))
            continue
        if kind is None:
            continue
        report["scanned"] += 1
        if not is_bearing:
            continue
        problem = carries(kind, parsed, notice)
        bearing[path] = problem
        if path in exceptions:
            if problem is None:
                out.append("%s %s it carries the notice; remove the "
                           "exception" % (path, STALE_EXCEPTION))
            else:
                report["excepted"].append(path)
            continue
        if problem is not None:
            out.append("%s %s" % (path, problem))
    report["bearing"] = bearing

    for path in sorted(exceptions):
        if path not in files:
            out.append("%s %s it is not tracked" % (path, STALE_EXCEPTION))
        elif path not in bearing:
            out.append("%s %s it carries no PCF material"
                       % (path, STALE_EXCEPTION))

    listed = h.listed_files(text)
    for path in sorted(set(bearing) - set(listed)):
        out.append("%s %s" % (path, UNLISTED))
    for path in sorted(set(listed) - set(bearing)):
        out.append("%s %s %s" % (path, OVERLISTED,
                                 "it is not tracked" if path not in files
                                 else "carries no PCF material"))
    return out, report


def main(argv=None) -> int:
    base = layout.repository_root()
    problems, report = findings(base)
    if problems:
        for problem in problems:
            print("  FINDING: %s" % problem)
        return 1
    carrying = sorted(p for p, v in report["bearing"].items() if v is None)
    print("  ok: %d tracked YAML, JSON and RDF file(s) read; %d PCF-bearing, "
          "all listed in NOTICE.md; %d carry APQC's notice (%s); %d lack it under "
          "a recorded exception (%s)"
          % (report["scanned"], len(report["bearing"]), len(carrying),
             ", ".join(carrying) or "none", len(report["excepted"]),
             ", ".join(report["excepted"]) or "none"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
