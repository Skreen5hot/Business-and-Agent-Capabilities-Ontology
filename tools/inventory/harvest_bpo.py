# SPDX-License-Identifier: MIT
"""Harvest the Business Process Ontology into the Capability Term Inventory.

    python tools/inventory/harvest_bpo.py             # offline check
    python tools/inventory/harvest_bpo.py --rebuild   # fetch, harvest, rewrite
    python tools/inventory/harvest_bpo.py --confirm   # fetch, harvest, compare

Phase I-1 of the inventory the architect scoped on 2026-10-27. The pins
are config/inventory-sources.yaml; its header says why the selected commit
and the baseline are pinned separately and why every file has a digest.

WHAT THE INVENTORY IS, AND IS NOT

Source evidence (D6). Every entry says what BPO, at one commit, says about
one item, with where it says it. Nothing here is vocabulary, nothing is
admitted, and nothing is grouped: two BPO items that look like the same
capability are two entries, and a class BPO declares in three modules
keeps three declarations side by side (Amendment 2). Crosswalk and
grouping are Phase I-4's; doing any of it here would bury the evidence a
later reviewer needs to disagree with it.

WHAT IS AN ENTRY

  capability-class   every class in BPO's namespace whose rdfs:subClassOf
                     closure, over all harvested modules plus the full
                     pinned CCO and BFO, reaches CCO Organization Capability
                     (cco:ont00000568). CCO is loaded whole because BPO's
                     own chains stop at CCO terms, and without CCO's
                     structure "reaches" would be answered "no" for every
                     class whose path runs through it -- the same false
                     negative docs/process/PROCESS.md section 1 describes.

  scope-entry        every key of capabilities/capability_scope.json (BPO's
                     judgment table: capability -> the processes it
                     enables), except `_doc`. A different kind from the
                     class even when it names the same IRI, because it is a
                     different statement in a different file, and the
                     processes it lists are kept in the table's own order.

  standing-function  catalog nodes BPO itself marks as standing functions.
                     There are none: ADR-001 R5 says a standing-function
                     node is catalog-only, and R6 says it SHOULD get an
                     Organization Capability bridged by
                     bpo:designatesProcessType, but no rule, annotation,
                     class or scheme records the standing-function judgement
                     on the node. The bridge is not that marker -- R4 bridges
                     to process universals and capabilities alike, and R6 is
                     a SHOULD -- so treating it as one would be inferring the
                     judgement, which the approval forbids along with
                     inferring it from labels or hierarchy level. The
                     bridges are recorded instead, on the capability-class
                     entry they reach (`designated_by`), as evidence.

Entry ids are `<entry_prefix>-<local name>-<kind>`, so an id is stable for
as long as BPO's IRI is.

THE RIGHTS RULE (Amendment 3)

BPO is MIT, and its own text travels under that licence with the
attribution in docs/sources/inventory/NOTICE.md. Much of BPO is derived
from the APQC PCF, whose terms BPO's licence cannot waive and which are
Phase I-2's to verify. So every literal the harvest can tie to the PCF is
withheld: the field is present, holding `{withheld: apqc-terms-unverified}`,
and the IRI and PCF code stay. An entry is tied to the PCF, and its labels
and definitions withheld, when BPO itself says so in any of these ways:

  iri-scheme       its local name is `P<digits>` or `PCF_<digits>`: BPO's D7
                   IRI scheme, stated in every slice header, for a reality-
                   layer class minted from a PCF node and for a catalog node.
  annotation       it carries bpo:pcfID, bpo:hierarchyID or
                   bpo:apqcSourceText, the provenance annotations the
                   catalog layer declares for PCF material.
  text-matches-pcf one of its labels or definitions equals, ignoring case and
                   whitespace, a PCF node's skos:prefLabel or
                   bpo:apqcSourceText in the catalog layer -- PCF text that
                   reached a class without its annotations.
  text-contains-pcf
                   one of its labels or definitions contains such a PCF
                   name of two or more words as a whole run of words
                   (punctuation and case ignored): a definition that
                   reproduces a PCF element's name inside BPO's own wording.
  text-shared-with-withheld
                   one of its labels or definitions equals, as above, text
                   withheld on another class by any rule: the same words
                   withheld in one entry are not published in the next.

The evidence is recorded on the entry (`apqc_evidence`), so the reason for
each withholding can be checked. A scope entry carries no literal, so the
rule decides only its status. What the rule cannot see: PCF text BPO
paraphrased closely enough to be APQC's but not equal to it. That is the
residue Phase I-2 has to judge with APQC's terms in hand, and it is why
the status is "unverified" rather than "clear".

THE OFFLINE CHECK

What runs before every commit and in CI, with no network: the pins are
well formed; the outputs parse, keep their schema, and record exactly the
pinned input digests; every withheld entry carries no label or definition
text and every entry with APQC evidence is withheld; the counts in the
findings agree with the entries; NOTICE.md is a fresh generation; and the
admission guard (Amendment 4) holds -- no file in the inventory directory
is anything but YAML or Markdown, none is an RDF serialization, none names
an IRI in this repository's AUTHORED_NAMESPACES (read from
tools/ontology/validate.py, not restated), and no entry carries a
ratification key. The inventory mints nothing and generates no class,
property, axiom or act; the guard is what makes that a fact rather than
an intention. --rebuild runs the same check on what it built before it
writes anything.

THE NETWORK

--rebuild and --confirm fetch each pinned file from raw.githubusercontent.com
at its pinned commit, and from nowhere else; a pin naming another host, or a
URL not naming its commit, is refused. Downloads are cached in
.upstream-cache/ (gitignored): BPO files under bpo-<commit>/<sha256>, CCO and BFO
under the names tools/ontology/vendor_upstream.py uses, so the two tools
share one digest-checked cache.

DETERMINISM

Every list is sorted, or kept in the source's own order where that order
is evidence (a scope entry's processes). YAML is emitted by PyYAML with a
fixed key order and written as bytes, so LF on every platform. Two
rebuilds produce identical bytes; the test suite and the weekly CI job
hold it to that.
"""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import re
import sys
import urllib.parse
import urllib.request
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import layout  # noqa: E402

FORMAT = 1
GENERATOR = "tools/inventory/harvest_bpo.py"
PINS = "config/inventory-sources.yaml"
UPSTREAM_PINS = "config/upstream-sources.yaml"
VALIDATOR = "tools/ontology/validate.py"
CACHE = ".upstream-cache"
SOURCE_ID = "bpo"
#: The only host --rebuild may reach. A pin naming another is refused, so a
#: copied-in URL cannot widen what this tool downloads from.
ALLOWED_PREFIX = "https://raw.githubusercontent.com/"
GITHUB = "https://github.com/"

RDF = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
RDFS = "http://www.w3.org/2000/01/rdf-schema#"
OWL = "http://www.w3.org/2002/07/owl#"
SKOS = "http://www.w3.org/2004/02/skos/core#"
OBO = "http://purl.obolibrary.org/obo/"
CCO = "https://www.commoncoreontologies.org/"

#: The CCO anchors the harvest reasons with, each with the label the full
#: CCO must give it. Checked at rebuild against the pinned file, because an
#: IRI asserted from memory is the error CLAUDE.md names first.
ORGANIZATION_CAPABILITY = CCO + "ont00000568"
AGENT_CAPABILITY = CCO + "ont00001379"
PLANNED_ACT = CCO + "ont00000228"
ANCHOR_LABELS = {
    ORGANIZATION_CAPABILITY: "Organization Capability",
    AGENT_CAPABILITY: "Agent Capability",
    PLANNED_ACT: "Planned Act",
}

#: Literal properties an entry reports, with the short form written in the
#: output. Full IRIs would be no less ambiguous to a reader and much longer.
LABEL_PROPERTIES = ((RDFS + "label", "rdfs:label"),
                    (SKOS + "prefLabel", "skos:prefLabel"),
                    (SKOS + "altLabel", "skos:altLabel"))
DEFINITION_PROPERTIES = ((OBO + "IAO_0000115", "obo:IAO_0000115"),
                         (SKOS + "definition", "skos:definition"))

#: BPO's provenance annotations for PCF material, by local name in BPO's
#: namespace (declared in ontology/apqc-catalog.ttl).
APQC_ANNOTATIONS = ("pcfID", "hierarchyID", "apqcSourceText")
#: BPO's D7 IRI scheme for PCF-derived names.
PCF_LOCAL = re.compile(r"^(?:P|PCF_)(\d+)$")
LOCAL = re.compile(r"^[A-Za-z0-9_]+$")
HEX40 = re.compile(r"^[0-9a-f]{40}$")
HEX64 = re.compile(r"^[0-9a-f]{64}$")

KIND_CLASS = "capability-class"
KIND_SCOPE = "scope-entry"
KINDS = (KIND_CLASS, KIND_SCOPE)
RIGHTS_BPO = "bpo-mit"
TARGET_KINDS = ("act", "capability", "act-and-capability", "unresolved")

#: Keys that would make an inventory file a vocabulary or ratification
#: record. Amendment 4: no inventory operation produces either.
FORBIDDEN_KEYS = ("ratified_by", "ratification", "lifecycle_status",
                  "designates_class", "bco-ratification")
#: What an inventory file may be. Anything else in the directory -- Turtle,
#: RDF/XML, JSON-LD, N-Triples -- is a serialization the inventory must
#: never produce.
ALLOWED_SUFFIXES = (".yaml", ".md")
#: Text that marks a file as RDF whatever its name says.
RDF_MARKERS = (re.compile(r"(?m)^\s*@prefix\s"), re.compile(r"(?m)^\s*PREFIX\s+\w*:"),
               re.compile(r"<rdf:RDF\b"), re.compile(r'"@context"\s*:'))


class Refused(SystemExit):
    """A question for whoever wrote the pin or the output, not for this tool."""


def root() -> Path:
    return layout.repository_root()


def parse_yaml(data):
    """yaml.safe_load, with libyaml's loader where PyYAML has it.

    The same safe subset either way; libyaml is about eight times faster
    on a 250 KB entries file, which is the difference between a check
    that runs before every commit and one people skip.
    """
    import yaml

    loader = getattr(yaml, "CSafeLoader", yaml.SafeLoader)
    return yaml.load(data, Loader=loader)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


# ------------------------------------------------------------------ pins


def _load_yaml(path: Path, name: str):
    if not path.is_file():
        raise Refused("%s is missing. What would say which bytes the "
                      "inventory was built from?" % name)
    return parse_yaml(path.read_bytes().decode("utf-8")) or {}


def _require(mapping, keys, where):
    if not isinstance(mapping, dict):
        raise Refused("%s is not a mapping; was it indented as intended?"
                      % where)
    for key in keys:
        if mapping.get(key) in (None, "", []):
            raise Refused("%s declares no %r -- which value was meant?"
                          % (where, key))


def _inputs(block, where) -> list[dict]:
    _require(block, ("ontology", "scope"), where)
    out = []
    for item in list(block["ontology"]) + [block["scope"]]:
        _require(item, ("path", "sha256"), where)
        if not HEX64.match(str(item["sha256"])):
            raise Refused("%s: %s has sha256 %r, which is not 64 lowercase "
                          "hex characters" % (where, item["path"],
                                              item["sha256"]))
        out.append({"path": item["path"], "sha256": item["sha256"]})
    paths = [i["path"] for i in out]
    if len(paths) != len(set(paths)):
        raise Refused("%s pins a path twice; which digest is meant?" % where)
    return out


def upstream_pins(base: Path) -> dict:
    """config/upstream-sources.yaml, by id: where CCO, BFO and the vendored
    BPO commit are pinned. Read, never restated here."""
    raw = _load_yaml(base / UPSTREAM_PINS, UPSTREAM_PINS)
    return {entry["id"]: entry for entry in raw.get("sources") or []}


def pins(base: Path | None = None) -> dict:
    """The BPO source from config/inventory-sources.yaml, checked.

    Returns the source mapping with `inputs` and `baseline_inputs`
    flattened to [{path, sha256}] and the shared `directory` attached.
    """
    base = base or root()
    raw = _load_yaml(base / PINS, PINS)
    directory = raw.get("directory")
    if not directory:
        raise Refused(PINS + " names no inventory directory. Where should "
                      "the admission guard look?")
    found = [s for s in raw.get("sources") or [] if s.get("id") == SOURCE_ID]
    if len(found) != 1:
        raise Refused("%s pins %d source(s) with id %r; this tool harvests "
                      "exactly one" % (PINS, len(found), SOURCE_ID))
    source = dict(found[0])
    where = "%s source %s" % (PINS, SOURCE_ID)
    _require(source, ("repository", "raw_base", "commit", "namespace",
                      "entry_prefix", "inputs", "baseline", "licence",
                      "apqc", "outputs", "standing_functions"), where)
    if not HEX40.match(source["commit"]):
        raise Refused("%s: commit %r is not a full 40-hex SHA. A short SHA "
                      "or a branch name is not a pin." % (where,
                                                         source["commit"]))
    if not (source["raw_base"] + "/").startswith(ALLOWED_PREFIX):
        raise Refused("%s: raw_base %s is not on %s. Should the allowed host "
                      "really grow?" % (where, source["raw_base"],
                                        ALLOWED_PREFIX))
    if not source["repository"].startswith(GITHUB):
        raise Refused("%s: repository %s is not on GitHub, so what would the "
                      "locators link to?" % (where, source["repository"]))
    source["inputs_flat"] = _inputs(source["inputs"], where + " inputs")
    baseline = source["baseline"]
    _require(baseline, ("commit", "namespace", "namespace_mapping",
                        "inputs"), where + " baseline")
    if not HEX40.match(baseline["commit"]):
        raise Refused("%s: baseline commit %r is not a full 40-hex SHA"
                      % (where, baseline["commit"]))
    source["baseline_flat"] = _inputs(baseline["inputs"],
                                      where + " baseline inputs")
    mapping = baseline["namespace_mapping"]
    _require(mapping, ("from", "to", "evidence"), where + " namespace_mapping")
    if not source["namespace"].startswith(mapping["to"]):
        raise Refused("%s: the namespace %s is not under the mapping's target "
                      "%s; is the mapping the right way round?"
                      % (where, source["namespace"], mapping["to"]))
    if not baseline["namespace"].startswith(mapping["from"]):
        raise Refused("%s: the baseline namespace %s is not under the "
                      "mapping's source %s" % (where, baseline["namespace"],
                                               mapping["from"]))
    if remap(baseline["namespace"], mapping) != source["namespace"]:
        raise Refused("%s: mapping %s -> %s takes the baseline namespace to "
                      "%s, not %s" % (where, mapping["from"], mapping["to"],
                                      remap(baseline["namespace"], mapping),
                                      source["namespace"]))

    # The baseline is "the existing pinned baseline" only if it is the commit
    # and the bytes config/upstream-sources.yaml vendors.
    vendored = upstream_pins(base).get(SOURCE_ID)
    if not vendored:
        raise Refused("%s pins no %r, so what baseline is this compared "
                      "with?" % (UPSTREAM_PINS, SOURCE_ID))
    if vendored["commit"] != baseline["commit"]:
        raise Refused("%s: the baseline is %s, but %s vendors BPO at %s. "
                      "Was the extract re-pinned without the inventory?"
                      % (where, baseline["commit"], UPSTREAM_PINS,
                         vendored["commit"]))
    if vendored["namespace"] != baseline["namespace"]:
        raise Refused("%s: the baseline namespace %s is not the vendored "
                      "pin's %s" % (where, baseline["namespace"],
                                    vendored["namespace"]))
    vendored_path = vendored["url"].split(vendored["commit"] + "/", 1)[-1]
    pinned = {i["path"]: i["sha256"] for i in source["baseline_flat"]}
    if pinned.get(vendored_path) != vendored["sha256"]:
        raise Refused("%s: the baseline pins %s at %s, but %s pins the same "
                      "file at %s. Which bytes are the baseline?"
                      % (where, vendored_path, pinned.get(vendored_path),
                         UPSTREAM_PINS, vendored["sha256"]))

    licence = source["licence"]
    _require(licence, ("spdx", "path", "sha256", "licence_statement_contains",
                       "attribution"), where + " licence")
    apqc = source["apqc"]
    _require(apqc, ("rightsholder", "work", "edition", "rights_status",
                    "withheld_marker", "evidence"), where + " apqc")
    for item in apqc["evidence"]:
        _require(item, ("path", "sha256", "what"), where + " apqc evidence")
    for item in source["standing_functions"].get("evidence") or []:
        _require(item, ("path", "sha256", "what"),
                 where + " standing_functions evidence")
    _require(mapping["evidence"], ("path", "sha256"),
             where + " namespace_mapping evidence")
    _require(source["outputs"], ("entries", "findings", "notice"),
             where + " outputs")
    for key, path in source["outputs"].items():
        if not path.startswith(directory + "/"):
            raise Refused("%s: output %s (%s) is outside %s, where the "
                          "admission guard would not see it"
                          % (where, key, path, directory))
    source["directory"] = directory
    return source


def remap(iri: str, mapping: dict) -> str:
    """BPO ADR-002's one base substitution, applied to one IRI."""
    old, new = mapping["from"], mapping["to"]
    if iri == old or iri.startswith(old + "#") or iri.startswith(old + "/"):
        return new + iri[len(old):]
    return iri


def raw_url(source: dict, commit: str, path: str) -> str:
    return "%s/%s/%s" % (source["raw_base"], commit,
                         urllib.parse.quote(path))


def blob_url(source: dict, commit: str, path: str, line=None) -> str:
    url = "%s/blob/%s/%s" % (source["repository"], commit,
                             urllib.parse.quote(path))
    return url + ("#L%d" % line if line else "")


# ----------------------------------------------------------------- fetch


def fetch(url: str, expected: str, cache_file: Path, commit: str) -> bytes:
    """Pinned bytes, from the cache or the network, digest checked.

    The URL must be on raw.githubusercontent.com and name the pinned
    commit. A cached file with the wrong digest is discarded rather than
    trusted: a cache is a copy, and a copy is only as good as its check.
    """
    if not url.startswith(ALLOWED_PREFIX):
        raise Refused("refusing to fetch %s: not on %s" % (url,
                                                          ALLOWED_PREFIX))
    if "/%s/" % commit not in url:
        raise Refused("refusing to fetch %s: it does not name the pinned "
                      "commit %s, so what it serves could change" % (url,
                                                                     commit))
    if cache_file.is_file():
        data = cache_file.read_bytes()
        if sha256(data) == expected:
            return data
        cache_file.unlink()
    request = urllib.request.Request(url, headers={
        "User-Agent": "bco-inventory-harvest (+%s)" % GENERATOR})
    with urllib.request.urlopen(request, timeout=180) as response:
        data = response.read()
    got = sha256(data)
    if got != expected:
        raise Refused("%s served %d bytes digesting to %s; the pin says %s. "
                      "Was it served by something other than GitHub, or is "
                      "the pin wrong?" % (url, len(data), got, expected))
    cache_file.parent.mkdir(parents=True, exist_ok=True)
    cache_file.write_bytes(data)
    return data


def fetch_commit(source: dict, commit: str, items: list[dict],
                 cache: Path) -> dict[str, bytes]:
    """Each file cached under its pinned digest, not its path.

    Content-addressed because BPO's PCF workbook has a 95-character name
    that, under a deep cache directory, passes Windows' 260-character path
    limit; and a digest-named file cannot be mistaken for another pin's.
    """
    out = {}
    for item in items:
        out[item["path"]] = fetch(
            raw_url(source, commit, item["path"]), item["sha256"],
            cache / ("bpo-" + commit) / item["sha256"], commit)
    return out


def fetch_upstream(base: Path, cache: Path) -> dict[str, bytes]:
    """The full pinned CCO and BFO, from config/upstream-sources.yaml."""
    found = upstream_pins(base)
    out = {}
    for key in ("cco", "bfo"):
        entry = found.get(key)
        if not entry:
            raise Refused("%s pins no %r; the harvest cannot tell what "
                          "reaches Organization Capability without it"
                          % (UPSTREAM_PINS, key))
        out[key] = fetch(entry["url"], entry["sha256"],
                         cache / (key + ".ttl"), entry["commit"])
    return out


def verify_evidence(source: dict, cache: Path) -> None:
    """The licence and evidence files, fetched and held to their digests.

    Nothing from them reaches the outputs; they are fetched so the pins
    in the config are checked against the bytes they describe rather than
    taken on trust. The LICENSE must say MIT, and the PCF workbook must
    hold the member the config cites with the digest it records.
    """
    commit = source["commit"]
    licence = source["licence"]
    items = [{"path": licence["path"], "sha256": licence["sha256"]}]
    items += [{"path": i["path"], "sha256": i["sha256"]}
              for i in source["apqc"]["evidence"]]
    items += [{"path": i["path"], "sha256": i["sha256"]}
              for i in source["standing_functions"].get("evidence") or []]
    evidence = source["baseline"]["namespace_mapping"]["evidence"]
    items.append({"path": evidence["path"], "sha256": evidence["sha256"]})
    unique = {i["path"]: i for i in items}
    got = fetch_commit(source, commit, list(unique.values()), cache)
    text = got[licence["path"]].decode("utf-8")
    if licence["licence_statement_contains"] not in text:
        raise Refused("%s at %s does not contain %r; is %s the right SPDX "
                      "identifier?" % (licence["path"], commit,
                                       licence["licence_statement_contains"],
                                       licence["spdx"]))
    for item in source["apqc"]["evidence"]:
        if not item.get("member"):
            continue
        with zipfile.ZipFile(io.BytesIO(got[item["path"]])) as archive:
            try:
                member = archive.read(item["member"])
            except KeyError:
                raise Refused("%s holds no %s; was the evidence re-exported?"
                              % (item["path"], item["member"])) from None
        if sha256(member) != item.get("member_sha256"):
            raise Refused("%s in %s has sha256 %s; the pin says %s"
                          % (item["member"], item["path"], sha256(member),
                             item.get("member_sha256")))
        if item.get("member_contains", "").encode() not in member:
            raise Refused("%s in %s does not contain %r; is it the notice "
                          "the config describes?" % (item["member"],
                                                     item["path"],
                                                     item["member_contains"]))


# --------------------------------------------------------------- harvest


def prefixes_of(text: str) -> dict[str, str]:
    """A Turtle file's own prefix declarations, {label: namespace}."""
    found = {}
    for match in re.finditer(
            r"(?m)^\s*(?:@prefix|PREFIX)\s+([A-Za-z][\w.-]*|):\s*<([^>]*)>",
            text):
        found[match.group(1)] = match.group(2)
    return found


class LineIndex:
    """Where each subject first begins a line in one Turtle file.

    Matched as the file writes it -- `bpo:X`, `ex:X` at the baseline, or
    `<iri>` -- at the start of a line, because that is where BPO declares a
    subject. Built once per file: the harvest asks for thousands of
    subjects, and rescanning a 3,000-line slice for each would make the
    locator the slowest part of the build.
    """

    def __init__(self, text: str):
        self.prefixes = prefixes_of(text)
        self.first = {}
        for number, line in enumerate(text.split("\n"), start=1):
            token = re.match(r"[^\s;,]+", line)
            if token:
                self.first.setdefault(token.group(0), number)

    def line_of(self, iri: str) -> int | None:
        """1-based, or None when no line begins with the IRI; the caller
        decides whether that is a refusal."""
        tokens = ["<%s>" % iri]
        for label, namespace in sorted(self.prefixes.items()):
            if iri.startswith(namespace) and LOCAL.match(iri[len(namespace):]):
                tokens.append("%s:%s" % (label, iri[len(namespace):]))
        found = [self.first[t] for t in tokens if t in self.first]
        return min(found) if found else None


def normalise(text: str) -> str:
    return " ".join(str(text).split()).casefold()


def words(text: str) -> tuple[str, ...]:
    """The text's words, casefolded, punctuation dropped: what a PCF name
    contained in a longer label or definition is compared on."""
    return tuple(re.findall(r"[^\W_]+(?:['-][^\W_]+)*",
                            str(text).casefold()))


class Harvest:
    """One commit of BPO, parsed, with the questions the inventory asks.

    `modules` keeps each file's graph apart, because a statement's module
    is part of the evidence; `graph` is all of them plus the full CCO and
    BFO, for reachability only.
    """

    def __init__(self, commit: str, namespace: str, files: dict[str, bytes],
                 scope_path: str, upstream: dict[str, bytes]):
        import rdflib

        self.commit = commit
        self.ns = namespace
        self.texts = {}
        self.lines = {}
        self.modules = {}
        self._declarations = {}
        self.graph = rdflib.Graph()
        for path in sorted(files):
            if path == scope_path:
                continue
            text = files[path].decode("utf-8")
            graph = rdflib.Graph()
            graph.parse(data=text, format="turtle")
            self.texts[path] = text
            self.lines[path] = LineIndex(text)
            self.modules[path] = graph
            self.graph += graph
        for key in ("cco", "bfo"):
            self.graph.parse(data=upstream[key].decode("utf-8"),
                             format="turtle")
        for iri, label in ANCHOR_LABELS.items():
            labels = {str(o) for o in self.graph.objects(
                rdflib.URIRef(iri), rdflib.URIRef(RDFS + "label"))}
            if label not in labels:
                raise Refused("the pinned CCO labels %s %s, not %r. Is the "
                              "anchor this tool reasons with the right IRI?"
                              % (iri, sorted(labels), label))
        self.scope_path = scope_path
        self.scope_text = files[scope_path].decode("utf-8")
        self._ancestors = {}
        self.capabilities = sorted(
            c for c in self._local_subjects()
            if ORGANIZATION_CAPABILITY in self.ancestors(c))
        self.agent_only = sorted(
            c for c in self._local_subjects()
            if AGENT_CAPABILITY in self.ancestors(c)
            and ORGANIZATION_CAPABILITY not in self.ancestors(c))
        self._pcf_text = self._pcf_literals()
        # A PCF name of one word ("Plan") is ordinary English; two or more
        # is a name a definition can only contain by reproducing it.
        self._pcf_phrases = {}
        for text, node in self._pcf_text.items():
            phrase = words(text)
            if len(phrase) >= 2:
                self._pcf_phrases.setdefault(phrase, node)
        self._pcf_longest = max(map(len, self._pcf_phrases), default=0)

    # -- graph questions ------------------------------------------------

    def term(self, local: str):
        import rdflib

        return rdflib.URIRef(self.ns + local)

    def _local_subjects(self) -> set[str]:
        import rdflib

        sub = rdflib.URIRef(RDFS + "subClassOf")
        return {str(s) for s in self.graph.subjects(sub, None)
                if isinstance(s, rdflib.URIRef) and str(s).startswith(self.ns)}

    def ancestors(self, iri: str) -> set[str]:
        """Named rdfs:subClassOf ancestors, transitively, over everything."""
        import rdflib

        if iri in self._ancestors:
            return self._ancestors[iri]
        sub = rdflib.URIRef(RDFS + "subClassOf")
        seen, stack = set(), [rdflib.URIRef(iri)]
        while stack:
            for parent in self.graph.objects(stack.pop(), sub):
                if isinstance(parent, rdflib.URIRef) and str(parent) not in seen:
                    seen.add(str(parent))
                    stack.append(parent)
        self._ancestors[iri] = seen
        return seen

    def target_kind(self, iri: str) -> str:
        up = self.ancestors(iri)
        act = PLANNED_ACT in up or iri == PLANNED_ACT
        cap = ORGANIZATION_CAPABILITY in up or iri == ORGANIZATION_CAPABILITY
        if act and cap:
            return "act-and-capability"
        return "act" if act else ("capability" if cap else "unresolved")

    def version_info(self, path: str) -> str | None:
        import rdflib

        graph = self.modules[path]
        found = sorted(
            str(v) for o in graph.subjects(rdflib.URIRef(RDF + "type"),
                                           rdflib.URIRef(OWL + "Ontology"))
            for v in graph.objects(o, rdflib.URIRef(OWL + "versionInfo")))
        if len(found) > 1:
            raise Refused("%s at %s states %d owl:versionInfo values %s; which "
                          "one versions it?" % (path, self.commit, len(found),
                                                found))
        return found[0] if found else None

    def literals(self, graph, iri: str, properties) -> list[dict]:
        import rdflib

        out = []
        for prop, short in properties:
            for value in graph.objects(rdflib.URIRef(iri),
                                       rdflib.URIRef(prop)):
                if isinstance(value, rdflib.Literal):
                    item = {"property": short, "text": str(value)}
                    if value.language:
                        item["lang"] = value.language
                    out.append(item)
        return sorted(out, key=lambda i: (i["property"], i.get("lang") or "",
                                          i["text"]))

    def declarations(self, iri: str) -> list[dict]:
        """One record per module that types `iri` owl:Class, never merged."""
        import rdflib

        if iri in self._declarations:
            return self._declarations[iri]
        out = []
        for path in sorted(self.modules):
            graph = self.modules[path]
            if (rdflib.URIRef(iri), rdflib.URIRef(RDF + "type"),
                    rdflib.URIRef(OWL + "Class")) not in graph:
                continue
            line = self.lines[path].line_of(iri)
            if line is None:
                raise Refused("%s types %s owl:Class at %s, but no line "
                              "begins with it. Where is it declared?"
                              % (path, iri, self.commit))
            parents = sorted(
                str(p) for p in graph.objects(rdflib.URIRef(iri),
                                              rdflib.URIRef(RDFS + "subClassOf"))
                if isinstance(p, rdflib.URIRef))
            out.append({
                "module": path,
                "line": line,
                "version_info": self.version_info(path),
                "subclass_of": parents,
                "label": self.literals(graph, iri, LABEL_PROPERTIES),
                "definition": self.literals(graph, iri,
                                            DEFINITION_PROPERTIES),
            })
        self._declarations[iri] = out
        return out

    def enables(self) -> list[tuple[str, str, str]]:
        """Every enablesProcess triple, with the module asserting it.

        Per module, so a triple two modules assert is two rows: the
        statement and where it was made are kept together.
        """
        import rdflib

        prop = self.term("enablesProcess")
        out = []
        for path, graph in self.modules.items():
            for s, o in graph.subject_objects(prop):
                out.append((str(s), str(o), path))
        return sorted(out)

    def designated_by(self, iri: str) -> list[dict]:
        import rdflib

        prop = self.term("designatesProcessType")
        out = set()
        for path, graph in self.modules.items():
            for node in graph.subjects(prop, rdflib.URIRef(iri)):
                out.add((str(node), path))
        return [{"node": node, "pcf_code": self.pcf_code(node),
                 "module": path} for node, path in sorted(out)]

    def pcf_code(self, iri: str) -> str | None:
        """The PCF code BPO records: bpo:pcfID, else the D7 local name."""
        values = sorted({str(v) for v in self.graph.objects(
            self.term_iri(iri), self.term("pcfID"))})
        local = iri[len(self.ns):] if iri.startswith(self.ns) else ""
        match = PCF_LOCAL.match(local)
        if match and values and values != [match.group(1)]:
            raise Refused("%s is named for PCF %s but carries bpo:pcfID %s at "
                          "%s. Which code is it?" % (iri, match.group(1),
                                                     values, self.commit))
        if len(values) > 1:
            raise Refused("%s carries bpo:pcfID %s at %s. Which code is it?"
                          % (iri, values, self.commit))
        if values:
            return values[0]
        return match.group(1) if match else None

    @staticmethod
    def term_iri(iri: str):
        import rdflib

        return rdflib.URIRef(iri)

    def _pcf_literals(self) -> dict[str, str]:
        """Normalised PCF text -> the catalog node it belongs to.

        A node is PCF material when it carries bpo:pcfID; its prefLabel
        and apqcSourceText are the text the rights rule compares with.
        """
        found = {}
        for node in sorted({str(s) for s in self.graph.subjects(
                self.term("pcfID"), None)}):
            local = node[len(self.ns):] if node.startswith(self.ns) else ""
            if not (local.startswith("PCF_") and PCF_LOCAL.match(local)):
                continue
            for prop in (self.term_iri(SKOS + "prefLabel"),
                         self.term("apqcSourceText")):
                for value in self.graph.objects(self.term_iri(node), prop):
                    found.setdefault(normalise(value), node)
        return found

    def apqc_evidence(self, iri: str, declarations: list[dict]) -> list[str]:
        """Why an entry is tied to the PCF, or [] when nothing ties it."""
        out = []
        local = iri[len(self.ns):]
        if PCF_LOCAL.match(local):
            out.append("iri-scheme: %s (BPO D7)" % local)
        for name in APQC_ANNOTATIONS:
            if any(True for _ in self.graph.objects(self.term_iri(iri),
                                                    self.term(name))):
                out.append("annotation: bpo:%s" % name)
        for declaration in declarations:
            for item in declaration["label"] + declaration["definition"]:
                node = self._pcf_text.get(normalise(item["text"]))
                if node:
                    out.append("text-matches-pcf: %s %s of %s"
                               % (declaration["module"], item["property"],
                                  node))
                    continue
                for node in self._contained_pcf(item["text"]):
                    out.append("text-contains-pcf: %s %s contains the "
                               "name of %s" % (declaration["module"],
                                               item["property"], node))
        return sorted(set(out))

    def _contained_pcf(self, text: str) -> list[str]:
        """The catalog nodes whose name (two or more words) the text
        contains as a whole run of words."""
        w = words(text)
        found = set()
        for n in range(2, min(len(w), self._pcf_longest) + 1):
            for i in range(len(w) - n + 1):
                node = self._pcf_phrases.get(w[i:i + n])
                if node:
                    found.add(node)
        return sorted(found)

    # -- the scope table -------------------------------------------------

    def scope(self) -> list[dict]:
        """capability_scope.json's entries, in file order, CURIEs expanded.

        CURIEs are expanded with the prefixes of capabilities_wiring.ttl at
        the same commit -- the Turtle BPO's own generator writes from this
        table -- so the expansion is BPO's, not one typed here.
        """
        def no_duplicates(pairs):
            keys = [k for k, _ in pairs]
            if len(keys) != len(set(keys)):
                raise Refused("%s at %s repeats a key; json would keep only "
                              "the last. Which one is meant?"
                              % (self.scope_path, self.commit))
            return dict(pairs)

        data = json.loads(self.scope_text, object_pairs_hook=no_duplicates)
        wiring = [p for p in self.texts if p.endswith("capabilities_wiring.ttl")]
        if len(wiring) != 1:
            raise Refused("found %d capabilities_wiring.ttl at %s; whose "
                          "prefixes expand the scope table?" % (len(wiring),
                                                                self.commit))
        prefixes = prefixes_of(self.texts[wiring[0]])

        def expand(curie: str) -> str:
            label, _, local = curie.partition(":")
            if label not in prefixes or not LOCAL.match(local):
                raise Refused("%s at %s names %r, which %s's prefixes do not "
                              "expand. What does it mean?"
                              % (self.scope_path, self.commit, curie,
                                 wiring[0]))
            return prefixes[label] + local

        lines = self.scope_text.split("\n")
        out = []
        for key, processes in data.items():
            if key == "_doc":
                continue
            if not isinstance(processes, list):
                raise Refused("%s at %s maps %s to %r, not a list of process "
                              "IRIs" % (self.scope_path, self.commit, key,
                                        processes))
            needle = json.dumps(key) + ":"
            line = next((n for n, text in enumerate(lines, start=1)
                         if text.strip().startswith(needle)), None)
            if line is None:
                raise Refused("%s at %s has key %s on no line of its own"
                              % (self.scope_path, self.commit, key))
            out.append({"key": key, "iri": expand(key), "line": line,
                        "processes": [expand(p) for p in processes]})
        return out


# -------------------------------------------------------------- measures


def class_entries(h: Harvest, source: dict) -> list[dict]:
    marker = {"withheld": source["apqc"]["withheld_marker"]}
    enables = {}
    for s, o, path in h.enables():
        enables.setdefault(s, []).append(
            {"target": o, "target_kind": h.target_kind(o), "module": path})
    declared = {iri: h.declarations(iri) for iri in h.capabilities}
    evidence_of = {iri: h.apqc_evidence(iri, declared[iri])
                   for iri in h.capabilities}
    # Text withheld on one class is withheld wherever else it appears
    # word for word; repeated until no class is added, since a class
    # withheld this way withholds its own text in turn.
    changed = True
    while changed:
        changed = False
        withheld_text = {}
        for iri in h.capabilities:
            if evidence_of[iri]:
                for d in declared[iri]:
                    for item in d["label"] + d["definition"]:
                        withheld_text.setdefault(normalise(item["text"]), iri)
        for iri in h.capabilities:
            if evidence_of[iri]:
                continue
            shared = sorted({
                "text-shared-with-withheld: %s %s equals text of %s"
                % (d["module"], item["property"], source_iri)
                for d in declared[iri]
                for item in d["label"] + d["definition"]
                for source_iri in [withheld_text.get(normalise(item["text"]))]
                if source_iri and source_iri != iri})
            if shared:
                evidence_of[iri] = shared
                changed = True
    out = []
    for iri in h.capabilities:
        local = iri[len(h.ns):]
        if not LOCAL.match(local):
            raise Refused("%s has local name %r, which cannot make a stable "
                          "entry id" % (iri, local))
        declarations = declared[iri]
        evidence = evidence_of[iri]
        withheld = bool(evidence)
        rendered = []
        for d in declarations:
            rendered.append({
                "module": d["module"],
                "line": d["line"],
                "locator": blob_url(source, h.commit, d["module"], d["line"]),
                "version_info": d["version_info"],
                "hierarchy": {"subclass_of": d["subclass_of"]},
                "label": dict(marker) if withheld else d["label"],
                "definition": dict(marker) if withheld else d["definition"],
            })
        out.append({
            "id": "%s-%s-%s" % (source["entry_prefix"], local, KIND_CLASS),
            "kind": KIND_CLASS,
            "iri": iri,
            "version": {"commit": h.commit},
            "rights_status": (marker["withheld"] if withheld else RIGHTS_BPO),
            "apqc_evidence": evidence,
            "pcf_code": h.pcf_code(iri),
            "declarations": rendered,
            "designated_by": h.designated_by(iri),
            "enables_process": enables.get(iri, []),
        })
    return out


def scope_entries(h: Harvest, source: dict) -> list[dict]:
    marker = source["apqc"]["withheld_marker"]
    out = []
    capability_ids = set(h.capabilities)
    for item in h.scope():
        iri = item["iri"]
        if not iri.startswith(h.ns):
            raise Refused("%s at %s has key %s outside BPO's namespace %s"
                          % (h.scope_path, h.commit, item["key"], h.ns))
        local = iri[len(h.ns):]
        evidence = h.apqc_evidence(iri, [])
        out.append({
            "id": "%s-%s-%s" % (source["entry_prefix"], local, KIND_SCOPE),
            "kind": KIND_SCOPE,
            "iri": iri,
            "version": {"commit": h.commit},
            "rights_status": marker if evidence else RIGHTS_BPO,
            "apqc_evidence": evidence,
            "pcf_code": h.pcf_code(iri),
            "source_key": item["key"],
            "module": h.scope_path,
            "line": item["line"],
            "locator": blob_url(source, h.commit, h.scope_path, item["line"]),
            "label": None,
            "definition": None,
            "capability_class_entry": (
                "%s-%s-%s" % (source["entry_prefix"], local, KIND_CLASS)
                if iri in capability_ids else None),
            "enables_process": [
                {"position": n, "target": p, "target_kind": h.target_kind(p),
                 "pcf_code": h.pcf_code(p)}
                for n, p in enumerate(item["processes"], start=1)],
        })
    return out


def measure(h: Harvest, entry_prefix: str, mapping: dict | None) -> dict:
    """The counts and lists the findings report, for one commit.

    `mapping`, for the baseline, rewrites every IRI reported by BPO
    ADR-002's base substitution, so the two commits are comparable.
    """
    m = (lambda iri: remap(iri, mapping)) if mapping else (lambda iri: iri)

    def entry_id(iri, kind):
        return "%s-%s-%s" % (entry_prefix, m(iri)[len(m(h.ns)):], kind)

    by_module = {}
    undeclared = []
    for iri in h.capabilities:
        declared = h.declarations(iri)
        if not declared:
            undeclared.append(m(iri))
        for d in declared:
            by_module[d["module"]] = by_module.get(d["module"], 0) + 1

    enables = h.enables()
    targets = {}
    for _, o, _ in enables:
        targets[o] = h.target_kind(o)
    by_kind = {k: sum(1 for _, o, _ in enables if targets[o] == k)
               for k in TARGET_KINDS}
    enables_by_module = {}
    for _, _, path in enables:
        enables_by_module[path] = enables_by_module.get(path, 0) + 1
    q12 = [{"capability": m(s), "target": m(o), "module": path,
            "entry": (entry_id(s, KIND_CLASS) if s in set(h.capabilities)
                      else None)}
           for s, o, path in enables
           if targets[o] in ("capability", "act-and-capability")]

    scope = h.scope()
    listed = [p for item in scope for p in item["processes"]]
    scope_kinds = {k: sum(1 for p in listed if h.target_kind(p) == k)
                   for k in TARGET_KINDS}
    scope_q12 = [{"scope_key": m(item["iri"]), "target": m(p),
                  "position": n, "entry": entry_id(item["iri"], KIND_SCOPE)}
                 for item in scope
                 for n, p in enumerate(item["processes"], start=1)
                 if h.target_kind(p) in ("capability", "act-and-capability")]

    q13_all, q13_cap = [], []
    capability_set = set(h.capabilities)
    import rdflib

    for iri in sorted({str(s) for g in h.modules.values()
                       for s in g.subjects(rdflib.URIRef(RDF + "type"),
                                           rdflib.URIRef(OWL + "Class"))
                       if str(s).startswith(h.ns)}):
        declared = h.declarations(iri)
        if len(declared) < 2:
            continue
        definitions = {tuple(sorted(i["text"] for i in d["definition"]))
                       for d in declared}
        parents = {tuple(d["subclass_of"]) for d in declared}
        differs = (["definitions"] if len(definitions) > 1 else []) + (
            ["superclasses"] if len(parents) > 1 else [])
        row = {"iri": m(iri), "modules": [d["module"] for d in declared],
               "differs": differs}
        q13_all.append(row)
        if iri in capability_set:
            q13_cap.append(row)

    def q13_summary(rows):
        return {
            "declared_in_two_or_more_modules": len(rows),
            "differing_definitions": sum(1 for r in rows
                                         if "definitions" in r["differs"]),
            "differing_superclasses": sum(1 for r in rows
                                          if "superclasses" in r["differs"]),
            "inconsistent": sum(1 for r in rows if r["differs"]),
            "inconsistent_classes": [r for r in rows if r["differs"]],
        }

    return {
        "capability_classes": {
            "count": len(h.capabilities),
            "pcf_named": sum(1 for c in h.capabilities
                             if PCF_LOCAL.match(c[len(h.ns):])),
            "declarations_by_module": dict(sorted(by_module.items())),
            "with_no_owl_class_declaration": sorted(undeclared),
            "iris": [m(c) for c in h.capabilities],
        },
        "agent_capability_only": {
            "note": ("classes in BPO's namespace that reach CCO Agent "
                     "Capability but not Organization Capability; outside "
                     "the capability-class definition, so not entries"),
            "count": len(h.agent_only),
            "iris": [m(c) for c in h.agent_only],
        },
        "scope": {
            "entries": len(scope),
            "processes_listed": len(listed),
            "distinct_processes": len(set(listed)),
            "listed_by_target_kind": scope_kinds,
            "keys_that_are_not_capability_classes": sorted(
                m(item["iri"]) for item in scope
                if item["iri"] not in capability_set),
            "capability_valued": scope_q12,
        },
        "enables_process": {
            "triples": len(enables),
            "by_module": dict(sorted(enables_by_module.items())),
            "distinct_subjects": len({s for s, _, _ in enables}),
            "distinct_targets": len(targets),
            "triples_by_target_kind": by_kind,
        },
        "q12": {
            "count": len(q12),
            "distinct_targets": len({r["target"] for r in q12}),
            "violations": q12,
        },
        "q13": {
            "all_classes": q13_summary(q13_all),
            "capability_classes": q13_summary(q13_cap),
        },
    }


def snapshot(h: Harvest, mapping: dict | None) -> dict:
    """What the diff compares: per capability class and per scope key."""
    m = (lambda iri: remap(iri, mapping)) if mapping else (lambda iri: iri)
    classes = {}
    for iri in h.capabilities:
        declared = h.declarations(iri)
        classes[m(iri)] = {
            "labels": sorted({(d["module"], i["text"]) for d in declared
                              for i in d["label"]}),
            "definitions": sorted({(d["module"], i["text"]) for d in declared
                                   for i in d["definition"]}),
            "parents": sorted({(d["module"], m(p)) for d in declared
                               for p in d["subclass_of"]}),
        }
    scope = {m(item["iri"]): [m(p) for p in item["processes"]]
             for item in h.scope()}
    return {"classes": classes, "scope": scope}


def diff(selected: dict, baseline: dict) -> dict:
    a, b = baseline["classes"], selected["classes"]
    common = sorted(set(a) & set(b))
    sa, sb = baseline["scope"], selected["scope"]
    return {
        "note": ("baseline IRIs rewritten by the namespace mapping before "
                 "comparison; labels and definitions compared per module "
                 "as literal text, so a change to an ex: mention inside a "
                 "definition counts as redefined"),
        "capability_classes": {
            "added": sorted(set(b) - set(a)),
            "removed": sorted(set(a) - set(b)),
            "relabelled": [i for i in common if a[i]["labels"] != b[i]["labels"]],
            "redefined": [i for i in common
                          if a[i]["definitions"] != b[i]["definitions"]],
            "re_parented": [i for i in common
                            if a[i]["parents"] != b[i]["parents"]],
        },
        "scope_entries": {
            "added": sorted(set(sb) - set(sa)),
            "removed": sorted(set(sa) - set(sb)),
            "processes_changed": sorted(k for k in set(sa) & set(sb)
                                        if sa[k] != sb[k]),
        },
    }


# --------------------------------------------------------------- outputs


def _dump(data) -> str:
    import yaml

    return yaml.safe_dump(data, sort_keys=False, allow_unicode=True,
                          width=79, default_flow_style=False)


def header(lines: list[str]) -> str:
    return "".join("# %s\n" % line if line else "#\n" for line in lines)


def entries_document(source: dict, entries: list[dict]) -> dict:
    apqc = source["apqc"]
    withheld = sum(1 for e in entries if e["rights_status"] != RIGHTS_BPO)
    return {
        "format": FORMAT,
        "generator": GENERATOR,
        "status": ("source evidence (scope approval D6); not vocabulary, "
                   "not an admission to the ontology (Amendment 4)"),
        "source": {
            "id": source["id"],
            "repository": source["repository"],
            "commit": source["commit"],
            "namespace": source["namespace"],
            "inputs": source["inputs_flat"],
            "licence": {"spdx": source["licence"]["spdx"],
                        "path": source["licence"]["path"],
                        "sha256": source["licence"]["sha256"]},
        },
        "rights": {
            RIGHTS_BPO: ("BPO-authored text, redistributed under BPO's MIT "
                         "licence with the attribution in %s"
                         % source["outputs"]["notice"]),
            apqc["withheld_marker"]: (
                "%s; every label and definition the rule ties to the %s %s "
                "is withheld, keeping the IRI and PCF code"
                % (apqc["rights_status"], apqc["work"], apqc["edition"])),
        },
        "standing_functions": {
            "marker_found": False,
            "entries": 0,
            "why": ("BPO records no standing-function marker on a catalog "
                    "node (ADR-001 R5/R6 define the judgement, not a "
                    "marker); catalog-node bridges to capability classes "
                    "are recorded on those entries as designated_by"),
        },
        "counts": {
            "entries": len(entries),
            KIND_CLASS: sum(1 for e in entries if e["kind"] == KIND_CLASS),
            KIND_SCOPE: sum(1 for e in entries if e["kind"] == KIND_SCOPE),
            "withheld": withheld,
        },
        "entries": entries,
    }


ENTRIES_HEADER = [
    "GENERATED by tools/inventory/harvest_bpo.py --rebuild. Do not edit:",
    "the offline check compares this file with what the tool would write",
    "only through its rules, and --confirm compares it byte for byte.",
    "",
    "Capability Term Inventory, Phase I-1: the Business Process Ontology",
    "(BPO) harvested at one pinned commit. Source evidence, not vocabulary,",
    "and not an admission to the ontology. One entry per source item, never",
    "merged. Read docs/sources/inventory/README.md first.",
    "",
    "Rights: BPO-authored text is BPO's, under the MIT License; see NOTICE.md",
    "in this directory. Text tied to the APQC PCF is withheld until APQC's",
    "terms are verified (Phase I-2).",
]

FINDINGS_HEADER = [
    "GENERATED by tools/inventory/harvest_bpo.py --rebuild. Do not edit.",
    "",
    "Counts recalculated from the pinned files at the selected commit and",
    "at the baseline, and the difference between them. Every number is",
    "derived by the tool; none is typed. IRIs only: no label or definition",
    "appears here, so nothing in this file is subject to the rights rule.",
]

DEFINITIONS = {
    "capability_class": (
        "a class in BPO's namespace whose rdfs:subClassOf closure over every "
        "harvested module plus the full pinned CCO and BFO reaches CCO "
        "Organization Capability (cco:ont00000568)"),
    "target_kind": (
        "act: the target's closure reaches CCO Planned Act "
        "(cco:ont00000228); capability: it reaches Organization Capability; "
        "act-and-capability: both; unresolved: neither"),
    "q12": ("a bpo:enablesProcess triple whose target is a capability or "
            "act-and-capability rather than an act (CM-01 Q-12)"),
    "q13": ("a class in BPO's namespace typed owl:Class in two or more "
            "modules whose per-module definition sets (obo:IAO_0000115, "
            "skos:definition) or named rdfs:subClassOf sets differ (CM-01 "
            "Q-13)"),
    "harvested_modules": (
        "every ontology/**/*.ttl at the commit except SHACL shapes and the "
        "bad-examples fixture"),
}


def findings_document(source: dict, selected: dict, baseline: dict,
                      changes: dict) -> dict:
    return {
        "format": FORMAT,
        "generator": GENERATOR,
        "definitions": DEFINITIONS,
        "selected": dict({"commit": source["commit"],
                          "inputs": source["inputs_flat"]}, **selected),
        "baseline": dict({
            "commit": source["baseline"]["commit"],
            "inputs": source["baseline_flat"],
            "namespace_mapping": {
                "from": source["baseline"]["namespace_mapping"]["from"],
                "to": source["baseline"]["namespace_mapping"]["to"],
                "applied_to": "every IRI reported in this section",
            },
        }, **baseline),
        "diff": changes,
    }


def notice_text(source: dict) -> bytes:
    """docs/sources/inventory/NOTICE.md, from the pins alone."""
    licence = source["licence"]
    apqc = source["apqc"]
    lines = [
        "# Third-party notices: Capability Term Inventory",
        "",
        "The inventory files in this directory redistribute text from the",
        "projects below. Each licence requires attribution, and this file is",
        "that attribution. It is generated by `%s` from" % GENERATOR,
        "`%s`; the licensing check reads the same pins and" % PINS,
        "fails if an attribution declared there is missing here.",
        "",
        "## %s" % source["project"],
        "",
        " ".join(licence["attribution"].split()),
        "",
        "- repository: %s" % source["repository"],
        "- commit: `%s`" % source["commit"],
        "- licence: %s -- `%s`, sha256 `%s`" % (licence["spdx"],
                                                 licence["path"],
                                                 licence["sha256"]),
        "- redistributed in: `%s`" % source["outputs"]["entries"],
        "",
        "## %s, %s" % (apqc["work"], apqc["edition"]),
        "",
        "Rightsholder: %s. Status: %s." % (apqc["rightsholder"],
                                           apqc["rights_status"]),
        "",
        "Every label and definition the harvest ties to the PCF is withheld",
        "(`withheld: %s`); the rule, and the paraphrase it" % apqc[
            "withheld_marker"],
        "cannot detect, are in `README.md` in this directory. Entries keep",
        "BPO's IRIs and the PCF codes, which are APQC's identifiers for its",
        "process elements. BPO's MIT licence does not speak for APQC's",
        "material. Whether APQC's terms cover what is kept, and what",
        "attribution they would require, is Phase I-2's question. The",
        "evidence of APQC's terms that BPO carries, pinned in",
        "`%s`:" % PINS,
        "",
    ]
    for item in apqc["evidence"]:
        line = "- `%s`, sha256 `%s`" % (item["path"], item["sha256"])
        if item.get("member"):
            line += "; member `%s`, sha256 `%s`" % (item["member"],
                                                     item["member_sha256"])
        lines.append(line)
    return ("\n".join(lines) + "\n").encode("utf-8")


def build(cache: Path, base: Path | None = None) -> dict[str, bytes]:
    """Every output, as bytes, keyed by repository path. Writes nothing."""
    base = base or root()
    source = pins(base)
    verify_evidence(source, cache)
    upstream = fetch_upstream(base, cache)
    scope_path = source["inputs"]["scope"]["path"]

    selected_files = fetch_commit(source, source["commit"],
                                  source["inputs_flat"], cache)
    selected = Harvest(source["commit"], source["namespace"], selected_files,
                       scope_path, upstream)
    baseline_files = fetch_commit(source, source["baseline"]["commit"],
                                  source["baseline_flat"], cache)
    baseline = Harvest(source["baseline"]["commit"],
                       source["baseline"]["namespace"], baseline_files,
                       source["baseline"]["inputs"]["scope"]["path"],
                       upstream)
    mapping = source["baseline"]["namespace_mapping"]

    entries = sorted(class_entries(selected, source)
                     + scope_entries(selected, source),
                     key=lambda e: e["id"])
    ids = [e["id"] for e in entries]
    if len(ids) != len(set(ids)):
        raise Refused("two entries share an id: %s"
                      % sorted({i for i in ids if ids.count(i) > 1}))

    outputs = source["outputs"]
    entries_bytes = (header(ENTRIES_HEADER) + "\n" + _dump(
        entries_document(source, entries))).encode("utf-8")
    findings_bytes = (header(FINDINGS_HEADER) + "\n" + _dump(
        findings_document(
            source,
            measure(selected, source["entry_prefix"], None),
            measure(baseline, source["entry_prefix"], mapping),
            diff(snapshot(selected, None), snapshot(baseline, mapping)))
    )).encode("utf-8")
    built = {outputs["entries"]: entries_bytes,
             outputs["findings"]: findings_bytes,
             outputs["notice"]: notice_text(source)}
    problems = check_documents(source, built, base)
    if problems:
        raise Refused("the harvest built outputs its own check refuses:\n  "
                      + "\n  ".join(problems))
    return built


# ----------------------------------------------------------------- check


def authored_namespaces(base: Path) -> tuple:
    """AUTHORED_NAMESPACES, read from tools/ontology/validate.py.

    Imported by path rather than restated, so a namespace change there
    (RP-5) moves this guard with it.
    """
    import importlib.util

    spec = importlib.util.spec_from_file_location(
        "bco_validate_for_inventory", base / VALIDATOR)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    found = tuple(module.AUTHORED_NAMESPACES)
    if not found:
        raise Refused(VALIDATOR + " lists no AUTHORED_NAMESPACES, so the "
                      "admission guard would refuse nothing")
    return found


def _walk_keys(data, path=""):
    if isinstance(data, dict):
        for key, value in data.items():
            yield key, path
            yield from _walk_keys(value, "%s/%s" % (path, key))
    elif isinstance(data, list):
        for n, value in enumerate(data):
            yield from _walk_keys(value, "%s/%d" % (path, n))


def admission_findings(base: Path, directory: str,
                       contents: dict[str, bytes]) -> list[str]:
    """Amendment 4, over every file in the inventory directory.

    `contents` holds files about to be written, which take the place of
    what is on disk under the same path.
    """
    namespaces = authored_namespaces(base)
    files = dict(contents)
    folder = base / directory
    if folder.is_dir():
        for path in sorted(folder.rglob("*")):
            if path.is_file():
                rel = path.relative_to(base).as_posix()
                files.setdefault(rel, path.read_bytes())
    out = []
    for rel in sorted(files):
        if not rel.startswith(directory + "/"):
            continue
        data = files[rel]
        if not rel.endswith(ALLOWED_SUFFIXES):
            out.append("%s is not YAML or Markdown. The inventory produces "
                       "no RDF or OWL serialization; what is this file?"
                       % rel)
            continue
        text = data.decode("utf-8", errors="replace")
        for marker in RDF_MARKERS:
            if marker.search(text):
                out.append("%s reads as an RDF serialization (%s). Did an "
                           "inventory operation emit ontology?"
                           % (rel, marker.pattern))
                break
        for namespace in namespaces:
            if namespace in text:
                out.append("%s names %s, one of this repository's authored "
                           "namespaces. The inventory mints nothing; which "
                           "operation put it there?" % (rel, namespace))
        if rel.endswith(".yaml"):
            import yaml

            try:
                parsed = parse_yaml(text)
            except yaml.YAMLError as error:
                out.append("%s does not parse as YAML: %s" % (rel, error))
                continue
            for key, where in _walk_keys(parsed):
                if key in FORBIDDEN_KEYS:
                    out.append("%s carries %r at %s. A ratification or "
                               "vocabulary field in source evidence would "
                               "make it a decision; who made it?"
                               % (rel, key, where or "/"))
    return out


def _entry_findings(entry: dict, source: dict) -> list[str]:
    marker_value = source["apqc"]["withheld_marker"]
    marker = {"withheld": marker_value}
    eid = entry.get("id", "<no id>")
    out = []
    for key in ("id", "kind", "iri", "version", "rights_status",
                "apqc_evidence", "pcf_code", "enables_process"):
        if key not in entry:
            out.append("%s has no %r field" % (eid, key))
    if out:
        return out
    if entry["kind"] not in KINDS:
        out.append("%s has kind %r; the kinds are %s" % (eid, entry["kind"],
                                                         KINDS))
        return out
    local = entry["iri"][len(source["namespace"]):]
    if not entry["iri"].startswith(source["namespace"]):
        out.append("%s has IRI %s outside BPO's namespace %s"
                   % (eid, entry["iri"], source["namespace"]))
    expected = "%s-%s-%s" % (source["entry_prefix"], local, entry["kind"])
    if eid != expected:
        out.append("%s should be %s for IRI %s and kind %s"
                   % (eid, expected, entry["iri"], entry["kind"]))
    if entry["version"] != {"commit": source["commit"]}:
        out.append("%s records version %r, not the pinned commit %s"
                   % (eid, entry["version"], source["commit"]))
    status = entry["rights_status"]
    if status not in (RIGHTS_BPO, marker_value):
        out.append("%s has rights_status %r; it is %s or %s"
                   % (eid, status, RIGHTS_BPO, marker_value))
    tied = bool(entry["apqc_evidence"]) or entry["pcf_code"] is not None
    if tied and status != marker_value:
        out.append("%s has APQC evidence %s (PCF code %r) and rights_status "
                   "%r. Who verified APQC's terms?" % (
                       eid, entry["apqc_evidence"], entry["pcf_code"],
                       status))
    if status == marker_value and not tied:
        out.append("%s is withheld with no APQC evidence recorded; what "
                   "ties it to the PCF?" % eid)

    def texts(holder, where):
        for field in ("label", "definition"):
            if field not in holder:
                out.append("%s %s has no %r field" % (eid, where, field))
                continue
            value = holder[field]
            if status == marker_value:
                if value is not None and value != marker:
                    out.append("%s is withheld (%s) but its %s %s carries %r. "
                               "Withheld means the text is absent; where did "
                               "it come from?" % (eid, marker_value, where,
                                                  field, value))
            elif value == marker:
                out.append("%s is %s but its %s %s is withheld; which is it?"
                           % (eid, status, where, field))

    if entry["kind"] == KIND_CLASS:
        for key in ("declarations", "designated_by"):
            if key not in entry:
                out.append("%s has no %r field" % (eid, key))
        for n, declaration in enumerate(entry.get("declarations") or []):
            for key in ("module", "line", "locator", "version_info",
                        "hierarchy"):
                if key not in declaration:
                    out.append("%s declaration %d has no %r" % (eid, n, key))
            texts(declaration, "declaration %d" % n)
    else:
        for key in ("source_key", "module", "line", "locator",
                    "capability_class_entry"):
            if key not in entry:
                out.append("%s has no %r field" % (eid, key))
        texts(entry, "entry")
    for target in entry["enables_process"]:
        if target.get("target_kind") not in TARGET_KINDS:
            out.append("%s lists target %s with kind %r"
                       % (eid, target.get("target"),
                          target.get("target_kind")))
    return out


def check_documents(source: dict, contents: dict[str, bytes],
                    base: Path) -> list[str]:
    """Every rule the offline check enforces, over the given bytes."""
    import yaml

    outputs = source["outputs"]
    problems = []
    for key in ("entries", "findings", "notice"):
        if outputs[key] not in contents:
            problems.append("%s is missing. Run `python %s --rebuild`."
                            % (outputs[key], GENERATOR))
    if problems:
        return problems
    try:
        entries_doc = parse_yaml(contents[outputs["entries"]])
        findings_doc = parse_yaml(contents[outputs["findings"]])
    except yaml.YAMLError as error:
        return ["an inventory output does not parse as YAML: %s" % error]
    for name, doc in ((outputs["entries"], entries_doc),
                      (outputs["findings"], findings_doc)):
        if not isinstance(doc, dict) or doc.get("format") != FORMAT \
                or doc.get("generator") != GENERATOR:
            problems.append("%s is not format %d from %s"
                            % (name, FORMAT, GENERATOR))
    if problems:
        return problems

    recorded = entries_doc.get("source") or {}
    if recorded.get("commit") != source["commit"]:
        problems.append("%s was built from commit %r; the pin is %s"
                        % (outputs["entries"], recorded.get("commit"),
                           source["commit"]))
    if recorded.get("inputs") != source["inputs_flat"]:
        problems.append("%s records input digests that are not the pins in "
                        "%s. Was it built from other bytes, or the pins "
                        "changed without --rebuild?" % (outputs["entries"],
                                                        PINS))
    selected = findings_doc.get("selected") or {}
    baseline = findings_doc.get("baseline") or {}
    if (selected.get("commit"), selected.get("inputs")) != (
            source["commit"], source["inputs_flat"]):
        problems.append("%s's selected commit or input digests are not the "
                        "pins" % outputs["findings"])
    if (baseline.get("commit"), baseline.get("inputs")) != (
            source["baseline"]["commit"], source["baseline_flat"]):
        problems.append("%s's baseline commit or input digests are not the "
                        "pins" % outputs["findings"])

    entries = entries_doc.get("entries")
    if not isinstance(entries, list) or not entries:
        problems.append("%s holds no entries. Was the harvest empty, or the "
                        "list removed?" % outputs["entries"])
        return problems
    ids = [e.get("id") for e in entries if isinstance(e, dict)]
    if len(ids) != len(entries):
        problems.append("%s has an entry that is not a mapping"
                        % outputs["entries"])
        return problems
    if len(ids) != len(set(ids)):
        problems.append("%s repeats an id: %s" % (
            outputs["entries"], sorted({i for i in ids if ids.count(i) > 1})))
    if ids != sorted(ids):
        problems.append("%s is not sorted by id, so it is not what the tool "
                        "writes" % outputs["entries"])
    for entry in entries:
        problems.extend(_entry_findings(entry, source))

    counts = entries_doc.get("counts") or {}
    by_kind = {k: sum(1 for e in entries if e.get("kind") == k)
               for k in KINDS}
    withheld = sum(1 for e in entries
                   if e.get("rights_status") != RIGHTS_BPO)
    expected = dict({"entries": len(entries), "withheld": withheld},
                    **by_kind)
    if counts != expected:
        problems.append("%s states counts %r; its entries give %r"
                        % (outputs["entries"], counts, expected))
    caps = (selected.get("capability_classes") or {})
    if caps.get("count") != by_kind[KIND_CLASS] or sorted(
            caps.get("iris") or []) != sorted(
            e["iri"] for e in entries if e.get("kind") == KIND_CLASS):
        problems.append("%s reports %r capability classes; %s has %d "
                        "entries of that kind, for other IRIs or another "
                        "number" % (outputs["findings"], caps.get("count"),
                                    outputs["entries"], by_kind[KIND_CLASS]))
    if (selected.get("scope") or {}).get("entries") != by_kind[KIND_SCOPE]:
        problems.append("%s reports %r scope entries; %s has %d"
                        % (outputs["findings"],
                           (selected.get("scope") or {}).get("entries"),
                           outputs["entries"], by_kind[KIND_SCOPE]))
    known = set(ids)
    for row in (selected.get("q12") or {}).get("violations") or []:
        if row.get("entry") is not None and row["entry"] not in known:
            problems.append("%s lists Q-12 entry %s, which %s does not hold"
                            % (outputs["findings"], row["entry"],
                               outputs["entries"]))

    if contents[outputs["notice"]] != notice_text(source):
        problems.append("%s is not what %s writes from %s. Was it edited by "
                        "hand, or a pin changed without --rebuild?"
                        % (outputs["notice"], GENERATOR, PINS))
    problems.extend(admission_findings(base, source["directory"], contents))
    return problems


def check(base: Path | None = None) -> tuple[list[str], dict]:
    """(findings, the entries document's counts), offline."""
    base = base or root()
    source = pins(base)
    contents = {}
    for key in ("entries", "findings", "notice"):
        path = base / source["outputs"][key]
        if path.is_file():
            contents[source["outputs"][key]] = path.read_bytes()
    problems = check_documents(source, contents, base)
    counts = {}
    if not problems:
        counts = parse_yaml(contents[source["outputs"]["entries"]])[
            "counts"]
    return problems, counts


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--rebuild", action="store_true",
                    help="fetch the pinned files and rewrite the outputs")
    ap.add_argument("--confirm", action="store_true",
                    help="fetch and harvest in memory, then require the "
                         "committed outputs to be byte-identical")
    ap.add_argument("--cache", default=None,
                    help="download cache (default .upstream-cache/)")
    args = ap.parse_args(argv)
    base = root()
    cache = Path(args.cache) if args.cache else base / CACHE

    if args.rebuild or args.confirm:
        built = build(cache, base)
        differing = sorted(path for path, data in built.items()
                           if not (base / path).is_file()
                           or (base / path).read_bytes() != data)
        if args.confirm:
            if differing:
                print("  FINDING: %d inventory output(s) are not what "
                      "harvesting the pinned files produces: %s"
                      % (len(differing), ", ".join(differing)))
                return 1
            print("  every inventory output is byte-identical to a fresh "
                  "harvest of the pinned files")
            return 0
        for path, data in sorted(built.items()):
            target = base / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
            print("  wrote %s%s" % (path, "" if path in differing
                                    else " (unchanged)"))

    problems, counts = check(base)
    if problems:
        for problem in problems:
            print("  FINDING: %s" % problem)
        return 1
    print("  ok: %d entries (%d capability-class, %d scope-entry, %d "
          "withheld), digests match the pins, rights and admission rules "
          "hold, NOTICE.md is fresh"
          % (counts["entries"], counts[KIND_CLASS], counts[KIND_SCOPE],
             counts["withheld"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
