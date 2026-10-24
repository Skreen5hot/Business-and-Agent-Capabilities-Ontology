# SPDX-License-Identifier: MIT
"""Build the controlled vocabulary: authored YAML to Turtle (ADR-003).

    python tools/vocab/build.py                 # check: findings, then freshness
    python tools/vocab/build.py --write         # regenerate vocab/generated/
    python tools/vocab/build.py --out DIR       # write the build into DIR
    python tools/vocab/build.py --digest bcoc:X # print a concept record digest

INPUTS (paths from config/repository-layout.yaml)

    vocab/metamodel.yaml   metamodel concept records (bcom:), one per spec
                           section 4 row. P3 ships the file with an empty
                           `concepts` list; P5 fills it.
    vocab/catalog.yaml     catalog concept records (bcoc:). Empty in P3.
    vocab/agents.yaml      declared agents (bcoa:), D8.
    the specification in force (layout role `specification`), section 4
    docs/sources/register.yaml, the source register (D6, D8)
    vendor/**              the vendored extracts, to resolve upstream IRIs

The three vocab files must exist. An absent file is a finding, not an
empty list: the layout contract declares them, and "absent means empty"
would let a deleted file pass as a vocabulary with no terms.

OUTPUTS (generated artifacts; never edit them)

    vocab/generated/bco-vocabulary.ttl  the bco: annotation properties and
                                        the bco:PCFCode datatype (D1, D7)
    vocab/generated/bco-metamodel.ttl   bcom:MetamodelScheme and its concepts
    vocab/generated/bco-catalog.ttl     bcoc:CapabilityCatalogScheme and its
                                        concepts
    vocab/generated/bco-sources.ttl     one bcos: record per register entry
    vocab/generated/bco-agents.ttl      the declared bcoa: agents

Written by the serialiser in tools/ontology/vendor_upstream.py (D9): sorted
triples, one per line, no blank nodes, its own escaping, reparsed and
compared on every build.

THE CONCEPT RECORD DIGEST -- what a ratification act cites

    record = the authored YAML mapping of one concept, minus `ratified_by`
    for a metamodel concept, plus the key "spec_row_content" holding the
        section 4 row it wraps: {"label", "iri", "definition", "parents",
        "does_not_imply"}, each cell's text verbatim
    bytes  = json.dumps(record, sort_keys=True, ensure_ascii=False,
                        separators=(",", ":"), allow_nan=False)
             encoded as UTF-8 (no trailing newline; JSON escapes any
             newline inside a string, so the bytes are LF-only)
    digest = SHA-256 of those bytes, lowercase hex

`ratified_by` is left out because it is the one field written after the
act, pointing back at it; including it would make every act cite a digest
its own citation changes. The section 4 row is put in because D4 makes the
specification the metamodel definition's only source, so a change to the
row is a change to the concept's definition and must break a ratification
(D3) exactly as an edit to a catalog definition does. `--digest` prints it.

STATUS (D5) -- derived, never written. In this order:

  1. Deprecated: `is_replaced_by` names a concept that exists and is not
     itself replaced. `owl:deprecated true` is emitted. A replacement
     that does not exist, or is itself replaced (a chain or a cycle), is a
     finding rather than a fall-through.
  2. Ratified: `ratified_by` cites an act (D2) whose bco-ratification
     block lists this concept's IRI with the SHA-256 of its current
     record. A listed digest that differs is D3: the record changed after
     ratification.
  3. Otherwise the authored `authored_status`, Draft or Candidate.

THE METAMODEL STAGING RULE (D4)

Every section 4 row must have a metamodel record, and every record must
name a row -- once `vocab/metamodel.yaml` lists at least one concept. With
an empty list the coverage half is not applied, because P3 ships no terms
and P5 adds them. The section 4 parse runs regardless: a spec whose Terms
tables cannot be read is a finding on every build.

Exit codes: 0 no findings; 1 findings (each printed); 2 bad usage.
"""

from __future__ import annotations

import argparse
import functools
import hashlib
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(HERE.parent / "ontology"))
sys.path.insert(0, str(HERE.parent / "sources"))
sys.path.insert(0, str(HERE))

import layout  # noqa: E402
import build_register  # noqa: E402
import vendor_upstream  # noqa: E402
import citations  # noqa: E402
import spec_terms  # noqa: E402

GENERATOR = "tools/vocab/build.py"

#: ADR-003 D1, exactly. Siblings: no namespace is a prefix of another.
BCO = "https://fandaws.com/ontology/bco#"
BCOM = "https://fandaws.com/ontology/bco-metamodel#"
BCOC = "https://fandaws.com/ontology/bco-catalog#"
BCOS = "https://fandaws.com/ontology/bco-sources#"
BCOA = "https://fandaws.com/ontology/bco-agents#"
NAMESPACES = (("bco", BCO), ("bcom", BCOM), ("bcoc", BCOC), ("bcos", BCOS),
              ("bcoa", BCOA))

RDF = vendor_upstream.RDF
RDFS = vendor_upstream.RDFS
OWL = vendor_upstream.OWL
SKOS = vendor_upstream.SKOS
DCTERMS = vendor_upstream.DCTERMS
XSD = "http://www.w3.org/2001/XMLSchema#"
PROV = "http://www.w3.org/ns/prov#"

METAMODEL_SCHEME = BCOM + "MetamodelScheme"
CATALOG_SCHEME = BCOC + "CapabilityCatalogScheme"

#: Layout-contract ids.
INPUT_IDS = {"metamodel": "vocab.metamodel", "catalog": "vocab.catalog",
             "agents": "vocab.agents"}
REGISTER_ID = "sources.register"
OUTPUT_IDS = {
    "bco-vocabulary.ttl": "generated.vocab-terms",
    "bco-metamodel.ttl": "generated.vocab-metamodel",
    "bco-catalog.ttl": "generated.vocab-catalog",
    "bco-sources.ttl": "generated.vocab-sources",
    "bco-agents.ttl": "generated.vocab-agents",
}

AUTHORED_STATUSES = ("Draft", "Candidate")
RELATIONS = ("adapted-from", "consistent-with", "departs-from")
#: ADR-003 D7. The lexical form of a PCF 7.4 Cross-Industry element ID is
#: assumed to be five digits (as in the P2 trial). It has not been checked
#: against the PCF 7.4 workbook, which is licensed and not in this
#: repository; P5's first notation is where that is confirmed.
PCF_CODE = re.compile(r"^[0-9]{5}$")
CREATED = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
LANGUAGE = re.compile(r"^[a-z]{2,3}(-[A-Za-z0-9]{2,8})*$")
LOCAL = re.compile(r"^[A-Z][A-Za-z0-9]*$")
AGENT_LOCAL = re.compile(r"^[a-z0-9][a-z0-9-]*$")
SRC_ID = re.compile(r"^SRC-[A-Z]+-[0-9]{2}$")
SHA256 = re.compile(r"^[0-9a-f]{64}$")
#: D6: the quote tripwire's window.
TRIPWIRE_WORDS = 6

COMMON_REQUIRED = ("id", "sources", "drafted_by", "created",
                   "authored_status")
COMMON_OPTIONAL = ("ratified_by", "is_replaced_by", "revises", "change_note")
METAMODEL_FIELDS = set(COMMON_REQUIRED) | set(COMMON_OPTIONAL) | {"spec_row"}
CATALOG_REQUIRED = ("pref_label", "definition", "genus")
CATALOG_FIELDS = (set(COMMON_REQUIRED) | set(COMMON_OPTIONAL)
                  | set(CATALOG_REQUIRED)
                  | {"broader", "notation", "designates_class"})
SOURCE_FIELDS = {"source", "locator", "relation", "departure_note", "claim"}
AGENT_FIELDS = {"id", "type", "name", "model", "acted_on_behalf_of"}
#: Fields that are never authored, each refused with its own code so the
#: message says which decision forbids it rather than "unknown field".
STATUS_FIELDS = ("lifecycle_status", "lifecycleStatus", "deprecated",
                 "owl:deprecated")

#: The bco: terms the vocabulary graph uses, declared in bco-vocabulary.ttl.
#: Annotation properties and one datatype, which is what ADR-003 D1 puts in
#: bco: for the vocabulary. No class is minted here.
PROPERTIES = {
    "designatesClass": ("designates class",
                        "Relates a concept to the OWL class it names."),
    "lifecycleStatus": ("lifecycle status",
                        "The concept's status, derived by tools/vocab/build.py "
                        "(ADR-003 D5): Draft, Candidate, Ratified or "
                        "Deprecated. Never authored."),
    "doesNotImply": ("does not imply",
                     "What the specification section 4 row says the term "
                     "does not imply, verbatim."),
    "specParent": ("specification parent",
                   "A parent class the specification section 4 row names "
                   "for the class this concept designates."),
    "definitionGenus": ("definition genus",
                        "The BFO or CCO class a catalog definition takes as "
                        "its genus (ADR-003 D4)."),
    "sourceReference": ("source reference",
                        "Relates a concept to a reference to a register "
                        "entry (ADR-003 D6)."),
    "citesSource": ("cites source",
                    "Relates a source reference to the register record it "
                    "cites."),
    "locator": ("locator", "Where in the source the reference points."),
    "relation": ("relation",
                 "How the concept stands to the source: adapted-from, "
                 "consistent-with or departs-from."),
    "departureNote": ("departure note",
                      "Why a concept departs from the source it cites."),
    "citesClaim": ("cites claim",
                   "The 1-based index of the register entry claim a "
                   "departure rests on."),
    "claimStatus": ("claim status",
                    "A verification status of a register entry's claim: "
                    "V, P, S, K or L."),
    "currentRecord": ("current record",
                      "Relates a concept to the version of its record this "
                      "build was made from."),
    "recordSha256": ("record SHA-256",
                     "The concept record digest defined in "
                     "tools/vocab/build.py."),
    "ratifiedBy": ("ratified by",
                   "Relates a concept to the citation of the act that "
                   "ratified it (ADR-003 D2, D5)."),
    "actPath": ("act path", "The cited decision record's path."),
    "actCommit": ("act commit",
                  "The full commit the decision record is cited at."),
    "actSha256": ("act SHA-256",
                  "The SHA-256 of the decision record at that commit."),
    "modelIdentifier": ("model identifier",
                        "A software agent's exact model identifier."),
}
PCF_DATATYPE = ("PCF code",
                "An APQC Process Classification Framework 7.4 "
                "Cross-Industry element ID (ADR-003 D7). The edition is part "
                "of this datatype's definition; adopting another edition "
                "is a new datatype.")


@dataclass(frozen=True)
class Finding:
    code: str
    message: str

    def __str__(self) -> str:
        return "[%s] %s" % (self.code, self.message)


@dataclass
class Inputs:
    metamodel: Path
    catalog: Path
    agents: Path
    spec: Path
    register: Path
    vendor: list
    repo: Path


@dataclass
class Result:
    files: dict = field(default_factory=dict)  # name -> bytes
    findings: list = field(default_factory=list)
    statuses: dict = field(default_factory=dict)  # concept IRI -> status
    digests: dict = field(default_factory=dict)  # concept IRI -> record digest
    spec: object = None


def default_inputs() -> Inputs:
    root = layout.repository_root()
    specs = layout.components("specification")
    if len(specs) != 1:
        raise SystemExit("expected one specification in force, found %d"
                         % len(specs))
    return Inputs(
        metamodel=root / layout.component(INPUT_IDS["metamodel"]).path,
        catalog=root / layout.component(INPUT_IDS["catalog"]).path,
        agents=root / layout.component(INPUT_IDS["agents"]).path,
        spec=specs[0].resolve(),
        register=layout.component(REGISTER_ID).resolve(),
        vendor=layout.vendored_files(),
        repo=root,
    )


def prefix_table() -> tuple:
    """The serialiser's prefixes: the W3C ones and the pinned upstreams
    (from the pins, as the extracts use), then PROV and ADR-003 D1's."""
    return vendor_upstream.prefixes() + (("prov", PROV),) + NAMESPACES


def expand(curie: str) -> str | None:
    for prefix, namespace in prefix_table():
        if curie.startswith(prefix + ":"):
            return namespace + curie[len(prefix) + 1:]
    return None


# ------------------------------------------------------------- digests


def canonical(value) -> bytes:
    return json.dumps(value, sort_keys=True, ensure_ascii=False,
                      separators=(",", ":"), allow_nan=False).encode("utf-8")


def record_digest(record: dict, row=None) -> str:
    """The concept record digest; see the module docstring."""
    body = {k: v for k, v in record.items() if k != "ratified_by"}
    if row is not None:
        body["spec_row_content"] = row.content()
    return hashlib.sha256(canonical(body)).hexdigest()


def minted(namespace: str, kind: str, content) -> str:
    """A provenance node's IRI: the namespace of the concept it belongs to,
    the kind, and the SHA-256 of its canonical JSON (D9: no blank nodes)."""
    return "%s%s-%s" % (namespace, kind,
                        hashlib.sha256(canonical(content)).hexdigest())


# ------------------------------------------------------------- loading


def load_file(path: Path, key: str, findings: list) -> list:
    import yaml

    if not path.is_file():
        findings.append(Finding("input-missing", "%s does not exist; it is "
                                "declared, and an absent file is not an "
                                "empty one" % path.name))
        return []
    raw = path.read_bytes()
    if b"\r" in raw:
        findings.append(Finding("input-shape", "%s contains CR; authored "
                                               "files are LF" % path.name))
    data = yaml.safe_load(raw.decode("utf-8"))
    if not isinstance(data, dict) or set(data) != {"version", key} \
            or data.get("version") != 1 or not isinstance(data.get(key), list):
        findings.append(Finding("input-shape", "%s must be exactly "
                                "{version: 1, %s: [...]}" % (path.name, key)))
        return []
    items = []
    for n, item in enumerate(data[key], 1):
        if not isinstance(item, dict):
            findings.append(Finding("input-shape", "%s %s[%d] is not a "
                                    "mapping" % (path.name, key, n)))
            continue
        items.append(item)
    return items


def described_upstream(vendor: list) -> set:
    """Every IRI a vendored extract describes (has as a subject)."""
    return set(_described(tuple(str(p) for p in vendor)))


@functools.lru_cache(maxsize=4)
def _described(vendor: tuple) -> frozenset:
    import rdflib

    graph = rdflib.Graph()
    for path in vendor:
        graph.parse(path, format="turtle")
    return frozenset(str(s) for s in graph.subjects()
                     if isinstance(s, rdflib.URIRef))


def tokens(text: str) -> list:
    """Words for the tripwire: lowercase, split on anything that is not a
    letter or a digit, so case and punctuation never decide a match."""
    import unicodedata

    text = unicodedata.normalize("NFKC", text).lower()
    return re.findall(r"[^\W_]+", text)


def ngrams(words: list, n: int = TRIPWIRE_WORDS) -> set:
    return {tuple(words[i:i + n]) for i in range(len(words) - n + 1)}


# ------------------------------------------------------------- checks


def check_fields(record: dict, allowed: set, required: tuple, where: str,
                 kind: str, findings: list) -> None:
    for name in sorted(map(str, record)):
        if name in allowed:
            continue
        if name == "definition" and kind == "metamodel":
            findings.append(Finding(
                "D4-definition-authored",
                "%s authors a definition; a metamodel definition comes from "
                "specification section 4 and nowhere else" % where))
        elif name in STATUS_FIELDS:
            findings.append(Finding(
                "D5-status-authored",
                "%s authors %s; status and owl:deprecated are derived, "
                "never written" % (where, name)))
        elif name == "narrower" and kind == "catalog":
            findings.append(Finding(
                "catalog-narrower",
                "%s authors narrower; the catalog states broader only" % where))
        else:
            findings.append(Finding("record-unknown-field",
                                    "%s has unknown field %r" % (where, name)))
    for name in required:
        if name not in record:
            findings.append(Finding("record-missing-field",
                                    "%s has no %r" % (where, name)))


def check_sources(refs, where: str, register: dict, findings: list) -> list:
    """The valid references, as dicts; findings for the rest (D6)."""
    if not isinstance(refs, list) or not refs:
        findings.append(Finding("D6-no-sources", "%s cites no source; every "
                                "concept is tied to the register" % where))
        return []
    known = build_register.known_ids(register)
    good = []
    for n, ref in enumerate(refs, 1):
        at = "%s sources[%d]" % (where, n)
        if not isinstance(ref, dict):
            findings.append(Finding("D6-reference-shape", "%s is not a "
                                                          "mapping" % at))
            continue
        bad = False
        for name in sorted(set(map(str, ref)) - SOURCE_FIELDS):
            findings.append(Finding("D6-reference-shape",
                                    "%s has unknown field %r" % (at, name)))
            bad = True
        src = ref.get("source")
        if not isinstance(src, str) or not SRC_ID.fullmatch(src) \
                or src not in known:
            findings.append(Finding("D6-unknown-source",
                                    "%s cites %r, which is not an entry in "
                                    "register.yaml" % (at, src)))
            bad = True
        locator = ref.get("locator")
        if not isinstance(locator, str) or not locator.strip():
            findings.append(Finding("D6-locator-missing",
                                    "%s has no locator" % at))
            bad = True
        relation = ref.get("relation")
        if relation not in RELATIONS:
            findings.append(Finding("D6-relation",
                                    "%s relation %r is not one of %s"
                                    % (at, relation, ", ".join(RELATIONS))))
            bad = True
        if relation == "departs-from":
            note = ref.get("departure_note")
            if not isinstance(note, str) or not note.strip():
                findings.append(Finding("D6-departure-note",
                                        "%s departs-from with no "
                                        "departure_note" % at))
                bad = True
            claim = ref.get("claim")
            if src in known:
                strong = build_register.claims_at_or_above(register, src, "P")
                entry = next(e for e in build_register.entries(register)
                             if e.get("id") == src)
                claims = entry.get("claims") or []
                if (not isinstance(claim, int) or isinstance(claim, bool)
                        or not 1 <= claim <= len(claims)
                        or dict(claims[claim - 1]) not in strong):
                    findings.append(Finding(
                        "D6-departure-claim",
                        "%s departs-from %s citing claim %r, which is not a "
                        "claim of that entry at V or P" % (at, src, claim)))
                    bad = True
        elif "departure_note" in ref or "claim" in ref:
            findings.append(Finding("D6-reference-shape",
                                    "%s carries departure_note or claim "
                                    "without departs-from" % at))
            bad = True
        if not bad:
            good.append(ref)
    return good


def check_labels(labels, where: str, findings: list) -> list:
    if not isinstance(labels, list) or not labels:
        findings.append(Finding("catalog-label", "%s has no pref_label"
                                % where))
        return []
    seen, good = set(), []
    for label in labels:
        if (not isinstance(label, dict) or set(label) != {"value", "language"}
                or not isinstance(label.get("value"), str)
                or not label["value"].strip()
                or not isinstance(label.get("language"), str)
                or not LANGUAGE.fullmatch(label["language"])):
            findings.append(Finding("catalog-label",
                                    "%s pref_label %r is not {value, "
                                    "language}" % (where, label)))
            continue
        if label["language"] in seen:
            findings.append(Finding("catalog-label",
                                    "%s has two pref_labels in %r"
                                    % (where, label["language"])))
            continue
        seen.add(label["language"])
        good.append(label)
    if good and "en" not in seen:
        findings.append(Finding("catalog-label",
                                "%s has no English pref_label" % where))
    return good


def check_common(record: dict, where: str, agents: dict, findings: list):
    if record.get("authored_status") not in AUTHORED_STATUSES:
        findings.append(Finding(
            "D5-authored-status",
            "%s authored_status %r; an author writes Draft or Candidate "
            "and nothing else" % (where, record.get("authored_status"))))
    drafted = record.get("drafted_by")
    if not isinstance(drafted, str) or not drafted.startswith("bcoa:") \
            or drafted[len("bcoa:"):] not in agents:
        findings.append(Finding("D8-undeclared-agent",
                                "%s drafted_by %r is not a declared agent"
                                % (where, drafted)))
    created = record.get("created")
    if not isinstance(created, str) or not CREATED.fullmatch(created):
        findings.append(Finding("record-created",
                                "%s created %r is not a quoted UTC "
                                "timestamp YYYY-MM-DDTHH:MM:SSZ"
                                % (where, created)))
    if "change_note" in record:
        notes = record["change_note"]
        if not isinstance(notes, list) or not notes or not all(
                isinstance(x, str) and x.strip() for x in notes):
            findings.append(Finding("D3-change-note",
                                    "%s change_note is not a list of text"
                                    % where))
    if "revises" in record:
        if not isinstance(record["revises"], str) \
                or not SHA256.fullmatch(record["revises"]):
            findings.append(Finding("D3-revises",
                                    "%s revises %r is not a record digest"
                                    % (where, record.get("revises"))))
        if "change_note" not in record:
            findings.append(Finding("D3-revises",
                                    "%s revises an earlier record with no "
                                    "change_note" % where))


def check_agents(items: list, findings: list) -> dict:
    agents: dict = {}
    for n, agent in enumerate(items, 1):
        at = "agents.yaml agents[%d]" % n
        extra = set(map(str, agent)) - AGENT_FIELDS
        aid = agent.get("id")
        kind = agent.get("type")
        if extra or not isinstance(aid, str) or not AGENT_LOCAL.fullmatch(aid) \
                or kind not in ("Person", "SoftwareAgent") \
                or not isinstance(agent.get("name"), str) \
                or not agent["name"].strip():
            findings.append(Finding("D8-agent-shape",
                                    "%s must be {id, type: Person | "
                                    "SoftwareAgent, name, ...}" % at))
            continue
        if aid in agents:
            findings.append(Finding("D8-agent-shape",
                                    "%s declares %s twice" % (at, aid)))
            continue
        if kind == "Person" and ("model" in agent
                                 or "acted_on_behalf_of" in agent):
            findings.append(Finding("D8-agent-shape",
                                    "%s: a Person has no model or "
                                    "acted_on_behalf_of" % at))
            continue
        agents[aid] = agent
    for aid, agent in sorted(agents.items()):
        if agent["type"] != "SoftwareAgent":
            continue
        model = agent.get("model")
        boss = agent.get("acted_on_behalf_of")
        if not isinstance(model, str) or not model.strip():
            findings.append(Finding("D8-agent-shape",
                                    "software agent %s has no exact model "
                                    "identifier" % aid))
        if not isinstance(boss, str) or boss not in agents \
                or agents[boss]["type"] != "Person":
            findings.append(Finding("D8-agent-shape",
                                    "software agent %s acted_on_behalf_of %r, "
                                    "which is not a declared Person"
                                    % (aid, boss)))
    return agents


# ------------------------------------------------------------- the build


def L(text: str, language: str | None = None, datatype: str | None = None):
    import rdflib

    if datatype:
        return rdflib.Literal(text, datatype=rdflib.URIRef(datatype))
    return rdflib.Literal(text, lang=language)


def U(iri: str):
    import rdflib

    return rdflib.URIRef(iri)


def build(inputs: Inputs) -> Result:
    result = Result()
    findings = result.findings
    register = build_register.load(inputs.register)
    upstream = described_upstream(inputs.vendor)

    # -- section 4 ------------------------------------------------------
    parsed = spec_terms.parse(inputs.spec)
    result.spec = parsed
    for line, message in parsed.failures:
        findings.append(Finding("D4-spec-parse", "%s line %d: %s"
                                % (inputs.spec.name, line, message)))
    rows = {row.spec_iri: row for row in parsed.rows}
    for row in parsed.rows:
        for prefix, local in row.parents:
            iri = expand("%s:%s" % (prefix, local))
            if iri is None or iri not in upstream:
                findings.append(Finding(
                    "D4-parent-unresolved",
                    "section 4 row %s names parent %s:%s, which no vendored "
                    "extract describes" % (row.spec_iri, prefix, local)))

    # -- agents ----------------------------------------------------------
    agents = check_agents(load_file(inputs.agents, "agents", findings),
                          findings)

    # -- concepts --------------------------------------------------------
    metamodel = load_file(inputs.metamodel, "concepts", findings)
    catalog = load_file(inputs.catalog, "concepts", findings)
    concepts = []  # (kind, namespace, record, row)
    seen_ids: set = set()
    for kind, items, prefix, namespace in (
            ("metamodel", metamodel, "bcom", BCOM),
            ("catalog", catalog, "bcoc", BCOC)):
        for n, record in enumerate(items, 1):
            cid = record.get("id")
            where = "%s.yaml concepts[%d] (%s)" % (kind, n, cid)
            if not isinstance(cid, str) or not cid.startswith(prefix + ":") \
                    or not LOCAL.fullmatch(cid[len(prefix) + 1:]):
                findings.append(Finding("record-id",
                                        "%s id must be %s:<UpperCamelName>"
                                        % (where, prefix)))
                continue
            if cid in seen_ids:
                findings.append(Finding("record-id", "%s is declared twice"
                                        % cid))
                continue
            seen_ids.add(cid)
            if kind == "metamodel":
                check_fields(record, METAMODEL_FIELDS,
                             COMMON_REQUIRED + ("spec_row",), where, kind,
                             findings)
            else:
                check_fields(record, CATALOG_FIELDS,
                             COMMON_REQUIRED + CATALOG_REQUIRED, where, kind,
                             findings)
            check_common(record, where, agents, findings)
            row = None
            if kind == "metamodel":
                local = cid[len(prefix) + 1:]
                spec_row = record.get("spec_row")
                if spec_row != "ex:" + local:
                    findings.append(Finding(
                        "D4-spec-row-mismatch",
                        "%s spec_row %r; the concept bcom:%s wraps the row "
                        "ex:%s" % (where, spec_row, local, local)))
                elif spec_row not in rows:
                    findings.append(Finding(
                        "D4-no-row",
                        "%s names %s, which is no concrete section 4 row"
                        % (where, spec_row)))
                else:
                    row = rows[spec_row]
            concepts.append((kind, namespace, record, row, where))

    if metamodel:
        wrapped = {record.get("spec_row") for kind, _, record, _, _ in concepts
                   if kind == "metamodel"}
        for iri in sorted(set(rows) - wrapped):
            findings.append(Finding(
                "D4-row-uncovered",
                "section 4 row %s has no metamodel concept" % iri))

    # -- digests ---------------------------------------------------------
    full = {}
    for kind, namespace, record, row, where in concepts:
        iri = expand(record["id"])
        full[record["id"]] = iri
        try:
            result.digests[iri] = record_digest(record, row)
        except (TypeError, ValueError) as error:
            findings.append(Finding("record-digest",
                                    "%s cannot be written as canonical JSON "
                                    "(%s); quote timestamps" % (where, error)))

    # -- status (D5) -----------------------------------------------------
    replaced = {record["id"]: record.get("is_replaced_by")
                for _, _, record, _, _ in concepts
                if "is_replaced_by" in record}
    acts: dict = {}
    for kind, namespace, record, row, where in concepts:
        iri = full[record["id"]]
        status = record.get("authored_status")
        target = replaced.get(record["id"])
        if record["id"] in replaced:
            if target == record["id"]:
                findings.append(Finding("D5-replaced-by",
                                        "%s is_replaced_by itself" % where))
            elif target not in full:
                findings.append(Finding(
                    "D5-replaced-by",
                    "%s is_replaced_by %r, which is not a concept" % (where,
                                                                      target)))
            elif target in replaced:
                findings.append(Finding(
                    "D5-replaced-by",
                    "%s is_replaced_by %s, which is itself replaced; point at "
                    "the live successor" % (where, target)))
            else:
                status = "Deprecated"
        if "ratified_by" in record and iri in result.digests:
            ratified = ratification(inputs.repo, record["ratified_by"], iri,
                                    result.digests[iri], agents, acts, where,
                                    findings)
            if ratified and status != "Deprecated":
                status = "Ratified"
        result.statuses[iri] = status

    # -- sources (D6) and the quote tripwire -----------------------------
    quotes = []
    for entry in build_register.entries(register):
        for quote in entry.get("quotes") or []:
            if isinstance(quote, dict) and isinstance(quote.get("text"), str):
                quotes.append((quote.get("key"), ngrams(tokens(quote["text"]))))
    checked_refs = {}
    for kind, namespace, record, row, where in concepts:
        checked_refs[record["id"]] = check_sources(record.get("sources"),
                                                   where, register, findings)
        if kind == "catalog" and isinstance(record.get("definition"), str):
            grams = ngrams(tokens(record["definition"]))
            for key, quoted in quotes:
                if grams & quoted:
                    findings.append(Finding(
                        "D6-quote-tripwire",
                        "%s definition shares a %d-word run with registered "
                        "quote %s" % (where, TRIPWIRE_WORDS, key)))

    # -- catalog-only checks ----------------------------------------------
    for kind, namespace, record, row, where in concepts:
        if kind != "catalog":
            continue
        check_labels(record.get("pref_label"), where, findings)
        definition = record.get("definition")
        if not isinstance(definition, str) or not re.match(
                r"^An? [a-z]", definition.strip()):
            findings.append(Finding(
                "catalog-definition-form",
                "%s definition does not open genus-differentia style "
                "('A <genus> that ...')" % where))
        genus = record.get("genus")
        if not isinstance(genus, str) or not genus.startswith(
                ("cco:", "obo:")) or expand(genus) not in upstream:
            findings.append(Finding(
                "catalog-genus",
                "%s genus %r is not a BFO or CCO class a vendored extract "
                "describes" % (where, genus)))
        broader = record.get("broader", [])
        if not isinstance(broader, list) or any(
                not isinstance(b, str) or not b.startswith("bcoc:")
                or b not in full or b == record["id"] for b in broader):
            findings.append(Finding(
                "catalog-broader",
                "%s broader %r must list other catalog concepts" % (where,
                                                                   broader)))
        if "notation" in record and (not isinstance(record["notation"], str)
                                     or not PCF_CODE.fullmatch(
                                         record["notation"])):
            findings.append(Finding(
                "D7-notation",
                "%s notation %r is not a PCF 7.4 element ID (five digits, "
                "quoted)" % (where, record["notation"])))
        if "designates_class" in record and (
                not isinstance(record["designates_class"], str)
                or not re.fullmatch(r"bco:[A-Z][A-Za-z0-9]*",
                                    record["designates_class"])):
            findings.append(Finding(
                "catalog-designates-class",
                "%s designates_class %r is not bco:<UpperCamelName>"
                % (where, record["designates_class"])))

    if findings:
        return result

    # -- triples ------------------------------------------------------------
    graphs = {
        "bco-vocabulary.ttl": vocabulary_triples(),
        "bco-metamodel.ttl": scheme_triples(METAMODEL_SCHEME,
                                            "BCO metamodel scheme",
                                            "The terms specification "
                                            "section 4 defines."),
        "bco-catalog.ttl": scheme_triples(CATALOG_SCHEME,
                                          "BCO capability catalog scheme",
                                          "The business capabilities the "
                                          "BCO catalogues."),
        "bco-sources.ttl": source_triples(register),
        "bco-agents.ttl": agent_triples(agents),
    }
    for kind, namespace, record, row, where in concepts:
        iri = full[record["id"]]
        out = graphs["bco-%s.ttl" % kind]
        out.extend(concept_triples(kind, namespace, iri, record, row,
                                   result.statuses[iri], result.digests[iri],
                                   checked_refs[record["id"]], full))

    table = prefix_table()
    inputs_named = {
        "bco-vocabulary.ttl": [GENERATOR],
        "bco-metamodel.ttl": ["vocab/metamodel.yaml",
                              "specification section 4 (%s)"
                              % inputs.spec.name],
        "bco-catalog.ttl": ["vocab/catalog.yaml"],
        "bco-sources.ttl": ["docs/sources/register.yaml"],
        "bco-agents.ttl": ["vocab/agents.yaml"],
    }
    for name, triples in graphs.items():
        header = [
            "%s -- generated by %s. Do not edit." % (name, GENERATOR),
            "From: %s." % "; ".join(inputs_named[name]),
            "Regenerate with: python %s --write" % GENERATOR,
            "Namespaces are ADR-003 D1's; provenance nodes are IRIs minted "
            "from content (D9).",
        ]
        text = vendor_upstream.serialise(triples, header, table)
        try:
            vendor_upstream.round_trip(text, triples)
        except SystemExit as error:
            findings.append(Finding("serialise-round-trip",
                                    "%s: %s" % (name, error)))
        result.files[name] = text.encode("utf-8")

    # D4: the built definition equals the row's text, read back from the
    # bytes that will be published rather than from the triples that went in.
    if not findings:
        import rdflib

        graph = rdflib.Graph().parse(
            data=result.files["bco-metamodel.ttl"].decode("utf-8"),
            format="turtle")
        for kind, namespace, record, row, where in concepts:
            if kind != "metamodel":
                continue
            got = [str(o) for o in graph.objects(
                U(full[record["id"]]), U(SKOS + "definition"))]
            if got != [row.definition]:
                findings.append(Finding(
                    "D4-definition-differs",
                    "%s: the built definition %r is not the row's text"
                    % (where, got)))
    return result


def ratification(repo: Path, citation, iri: str, digest: str, agents: dict,
                 acts: dict, where: str, findings: list) -> bool:
    key = repr(citation)
    try:
        if key not in acts:
            blob = citations.check_citation(repo, citation)
            acts[key] = citations.parse_act(blob, citation["path"])
        act = acts[key]
    except citations.CitationError as error:
        findings.append(Finding(error.code, "%s ratified_by: %s"
                                % (where, error)))
        return False
    agent = act["agent"]
    local = agent[len(BCOA):] if agent.startswith(BCOA) else None
    if local not in agents or agents[local]["type"] != "Person":
        findings.append(Finding(
            "D8-act-agent-not-person",
            "%s: the act %s is attributed to %s, which is not a declared "
            "prov:Person; only a person sets status"
            % (where, citation["path"], agent)))
        return False
    if iri not in act["concepts"]:
        findings.append(Finding(
            "D5-act-omits-concept",
            "%s: the act %s does not list %s" % (where, citation["path"],
                                                 iri)))
        return False
    if act["concepts"][iri] != digest:
        findings.append(Finding(
            "D3-record-changed",
            "%s: the act ratified record %s, and the current record is %s; "
            "a Ratified concept does not change in place -- a new act or a "
            "new IRI" % (where, act["concepts"][iri][:16], digest[:16])))
        return False
    return True


def vocabulary_triples() -> list:
    t = []
    for local, (label, definition) in sorted(PROPERTIES.items()):
        s = U(BCO + local)
        t += [(s, U(RDF + "type"), U(OWL + "AnnotationProperty")),
              (s, U(RDFS + "label"), L(label, "en")),
              (s, U(SKOS + "definition"), L(definition, "en"))]
    s = U(BCO + "PCFCode")
    t += [(s, U(RDF + "type"), U(RDFS + "Datatype")),
          (s, U(RDFS + "label"), L(PCF_DATATYPE[0], "en")),
          (s, U(SKOS + "definition"), L(PCF_DATATYPE[1], "en"))]
    return t


def scheme_triples(scheme: str, label: str, definition: str) -> list:
    s = U(scheme)
    return [(s, U(RDF + "type"), U(SKOS + "ConceptScheme")),
            (s, U(SKOS + "prefLabel"), L(label, "en")),
            (s, U(SKOS + "definition"), L(definition, "en"))]


def source_triples(register: dict) -> list:
    t = []
    for entry in build_register.entries(register):
        s = U(BCOS + entry["id"])
        t += [(s, U(RDF + "type"), U(DCTERMS + "BibliographicResource")),
              (s, U(DCTERMS + "identifier"), L(entry["id"])),
              (s, U(DCTERMS + "bibliographicCitation"),
               L(build_register.expand(entry["citation"], entry)))]
        for claim in entry.get("claims") or []:
            t.append((s, U(BCO + "claimStatus"), L(claim["status"])))
    return t


def agent_triples(agents: dict) -> list:
    t = []
    for aid, agent in sorted(agents.items()):
        s = U(BCOA + aid)
        t += [(s, U(RDF + "type"), U(PROV + "Agent")),
              (s, U(RDF + "type"), U(PROV + agent["type"])),
              (s, U(RDFS + "label"), L(agent["name"], "en"))]
        if agent["type"] == "SoftwareAgent":
            t += [(s, U(BCO + "modelIdentifier"), L(agent["model"])),
                  (s, U(PROV + "actedOnBehalfOf"),
                   U(BCOA + agent["acted_on_behalf_of"]))]
    return t


def concept_triples(kind, namespace, iri, record, row, status, digest, refs,
                    full) -> list:
    s = U(iri)
    t = [(s, U(RDF + "type"), U(SKOS + "Concept")),
         (s, U(BCO + "lifecycleStatus"), L(status)),
         (s, U(PROV + "wasAttributedTo"), U(expand(record["drafted_by"]))),
         (s, U(DCTERMS + "created"), L(record["created"],
                                       datatype=XSD + "dateTime"))]
    if kind == "metamodel":
        t += [(s, U(SKOS + "inScheme"), U(METAMODEL_SCHEME)),
              (s, U(SKOS + "prefLabel"), L(row.label, "en")),
              (s, U(SKOS + "definition"), L(row.definition, "en")),
              (s, U(BCO + "doesNotImply"), L(row.does_not_imply, "en")),
              (s, U(BCO + "designatesClass"), U(BCO + row.local))]
        for prefix, local in row.parents:
            t.append((s, U(BCO + "specParent"),
                      U(expand("%s:%s" % (prefix, local)))))
    else:
        t += [(s, U(SKOS + "inScheme"), U(CATALOG_SCHEME)),
              (s, U(SKOS + "definition"), L(record["definition"], "en")),
              (s, U(BCO + "definitionGenus"), U(expand(record["genus"])))]
        for label in record["pref_label"]:
            t.append((s, U(SKOS + "prefLabel"),
                      L(label["value"], label["language"])))
        for broader in record.get("broader", []):
            t.append((s, U(SKOS + "broader"), U(full[broader])))
        if "notation" in record:
            t.append((s, U(SKOS + "notation"),
                      L(record["notation"], datatype=BCO + "PCFCode")))
        if "designates_class" in record:
            t.append((s, U(BCO + "designatesClass"),
                      U(expand(record["designates_class"]))))
    if status == "Deprecated":
        t += [(s, U(OWL + "deprecated"), L("true", datatype=XSD + "boolean")),
              (s, U(DCTERMS + "isReplacedBy"),
               U(full[record["is_replaced_by"]]))]
    for note in record.get("change_note", []):
        t.append((s, U(SKOS + "changeNote"), L(note, "en")))

    rec = U("%srecord-%s" % (namespace, digest))
    t += [(s, U(BCO + "currentRecord"), rec),
          (rec, U(RDF + "type"), U(PROV + "Entity")),
          (rec, U(BCO + "recordSha256"), L(digest))]
    if "revises" in record:
        t.append((rec, U(PROV + "wasRevisionOf"),
                  U("%srecord-%s" % (namespace, record["revises"]))))

    for ref in refs:
        node = U(minted(namespace, "source", ref))
        t += [(s, U(BCO + "sourceReference"), node),
              (node, U(BCO + "citesSource"), U(BCOS + ref["source"])),
              (node, U(BCO + "locator"), L(ref["locator"])),
              (node, U(BCO + "relation"), L(ref["relation"]))]
        if "departure_note" in ref:
            t.append((node, U(BCO + "departureNote"),
                      L(ref["departure_note"], "en")))
        if "claim" in ref:
            t.append((node, U(BCO + "citesClaim"),
                      L(str(ref["claim"]), datatype=XSD + "integer")))

    if status == "Ratified" or ("ratified_by" in record
                                and status == "Deprecated"):
        cite = record["ratified_by"]
        node = U(minted(namespace, "ratification", cite))
        t += [(s, U(BCO + "ratifiedBy"), node),
              (node, U(BCO + "actPath"), L(cite["path"])),
              (node, U(BCO + "actCommit"), L(cite["commit"])),
              (node, U(BCO + "actSha256"), L(cite["sha256"]))]
    return t


# ------------------------------------------------------------- command line


def output_paths() -> dict:
    root = layout.repository_root()
    return {name: root / layout.component(cid).path
            for name, cid in OUTPUT_IDS.items()}


def freshness(result: Result, paths: dict) -> list:
    out = []
    for name, data in sorted(result.files.items()):
        path = paths[name]
        committed = path.read_bytes() if path.is_file() else None
        if committed != data:
            out.append(Finding("generated-stale",
                               "%s is %s a fresh build; run python %s --write"
                               % (path.name, "missing, not" if committed
                                  is None else "not", GENERATOR)))
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    group = ap.add_mutually_exclusive_group()
    group.add_argument("--write", action="store_true",
                       help="regenerate the committed Turtle")
    group.add_argument("--out", type=Path, default=None,
                       help="write the build into this directory instead")
    group.add_argument("--digest", metavar="CURIE", default=None,
                       help="print one concept's record digest")
    args = ap.parse_args(argv)

    inputs = default_inputs()
    result = build(inputs)
    problems = list(result.findings)
    if args.digest and not problems:
        iri = expand(args.digest)
        if iri not in result.digests:
            print("%s is not a concept" % args.digest, file=sys.stderr)
            return 2
        print(result.digests[iri])
        return 0
    if not problems:
        if args.write or args.out:
            target = args.out
            for name, data in sorted(result.files.items()):
                path = (target / name) if target else output_paths()[name]
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(data)
                print("wrote %s (%d bytes)" % (path, len(data)))
        else:
            problems += freshness(result, output_paths())
    for problem in problems:
        print("FINDING  %s" % problem)
    if problems:
        print("%d finding(s)" % len(problems))
        return 1
    if not (args.write or args.out):
        counts = {}
        for status in result.statuses.values():
            counts[status] = counts.get(status, 0) + 1
        print("ok: section 4 has %d concrete row(s) (%d template row(s) "
              "excluded); %d concept(s) %s; the Turtle is a fresh build"
              % (len(result.spec.rows), len(result.spec.excluded),
                 len(result.statuses),
                 json.dumps(dict(sorted(counts.items())))))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
