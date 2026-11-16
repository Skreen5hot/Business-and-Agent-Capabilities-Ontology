# SPDX-License-Identifier: MIT
"""Write the Stage 05 capability module from its tranche record (D6).

    python tools/ontology/formalize.py           # verify; exit 1 on a finding
    python tools/ontology/formalize.py --write   # regenerate apqc-cap.ttl

THE TRANCHE RECORD IS THE ONLY INPUT THAT NAMES A CLASS

`src/05_ontology/tranche-1.yaml` lists the parent and the 39 classes the
architect approved (D5-3) and authorized (D6, E). Nothing else adds a class:
not the vocabulary's broader links, not the PCF or any source hierarchy, not
the catalog. Every field in it is checked against the record it came from,
and the module is written from what those records say, never from the
tranche record's own copy of it:

  readiness     the readiness package at the commit the architect approved,
                by SHA-256. Each class's concept, class IRI, label, index
                size and concept-digest prefix must equal its row there,
                and the row must say "ready". The rows it holds back, and
                nothing else, are the tranche record's `excluded`.
  signed G1-T   each class's signed record, read from git at the commit
                whose bytes were signed and checked against the SHA-256 the
                signature names. Its realization index, member by member and
                in order, must equal `index`; its definition must equal the
                vocabulary's.
  vocabulary    each concept's preferred label and definition, read from the
                vocabulary build (tools/vocab/build.py), and its record
                digest, which must equal `concept_record_sha256` and, for
                tranche 2, the signature record's.
  BPO           each index member must be an act type the I-1 register
                records (docs/catalog/bpo-act-types.yaml), under no capability
                genus. A member under a CD5 development genus needs a
                `development_members` entry with its signed reason (CAP-06).

WHAT IT WRITES (Stage 05 standard, S1 to S8)

  bco:BusinessCapability  owl:Class; rdfs:subClassOf cco:ont00000568 and
                          obo:BFO_0000016; the label and definition of
                          bcom:BusinessCapability (specification v0.5 §4).
  each specific class     owl:Class; rdfs:subClassOf bco:BusinessCapability,
                          its only named parent (no kind-of link is in this
                          tranche); rdfs:label and skos:definition, @en, the
                          concept's; one ex:enablesProcess per index member.

Nothing else: no object property, no restriction, no equivalence, no
disjointness, no individual. The module's IRI and title are kept. The
Turtle is written by the vendoring serialiser (sorted, one triple per line),
so a rebuild is byte-identical and `--write` is the only way the file moves.
"""

from __future__ import annotations

import argparse
import hashlib
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(HERE.parent / "vocab"))
sys.path.insert(0, str(HERE))

import layout  # noqa: E402
import vendor_upstream  # noqa: E402

GENERATOR = "tools/ontology/formalize.py"
TRANCHE = "src/05_ontology/tranche-1.yaml"
MODULE_ID = "ontology.cap"
ACT_TYPES = "docs/catalog/bpo-act-types.yaml"
MODULE_IRI = "https://fandaws.com/ontology/bco/apqc-cap"

RDF = vendor_upstream.RDF
RDFS = vendor_upstream.RDFS
OWL = vendor_upstream.OWL
SKOS = vendor_upstream.SKOS
DCTERMS = vendor_upstream.DCTERMS
BCO = "https://fandaws.com/ontology/bco#"
BPO = "https://fandaws.com/ontology/bpo#"
CCO = "https://www.commoncoreontologies.org/"
OBO = "http://purl.obolibrary.org/obo/"
ENABLES = BPO + "enablesProcess"
ORGANIZATION_CAPABILITY = CCO + "ont00000568"

ACT = re.compile(r"^P\d+$")
SHA = re.compile(r"^[0-9a-f]{64}$")
COMMIT = re.compile(r"^[0-9a-f]{40}$")
#: A readiness-package row (section 2), as the approved text writes it.
READINESS_ROW = re.compile(
    r"^\| (T\d-\d\d) \| `(bcoc:\w+)` \| `(bco:\w+)` \| ([^|]+?) \| (\d+) \| "
    r"`([0-9a-f]{12})…` \| ([^|]+?) \|$", re.M)
#: A signature-record row: id, candidate, class, concept, ..., index, ..., digest.
SIGNATURE_ROW = re.compile(
    r"^\| (T2-\d\d) \| BCC-\w+ \| ([^|]+?) \| `(bcoc:\w+)` \| [^|]+ \| (\d+) \| "
    r"[^|]+ \| `([0-9a-f]{64})` \|$", re.M)
INDEX_MEMBER = re.compile(r"^\| `bpo:(P\d+)` \|", re.M)


class Refused(SystemExit):
    """An input that cannot be read at all, as opposed to a finding."""


def repo_root() -> Path:
    return layout.repository_root()


def git_bytes(commit: str, path: str) -> bytes:
    out = subprocess.run(["git", "show", "%s:%s" % (commit, path)],
                         cwd=str(repo_root()), capture_output=True)
    if out.returncode:
        raise Refused("git cannot show %s at %s: %s"
                      % (path, commit, out.stderr.decode("utf-8", "replace")))
    return out.stdout


def signed_text(commit: str, path: str, sha256: str, findings: list,
                what: str) -> str:
    """The bytes at `commit`, refused as a finding unless they digest to the
    SHA-256 the signature (or approval) names."""
    data = git_bytes(commit, path)
    got = hashlib.sha256(data).hexdigest()
    if got != sha256:
        findings.append("%s: %s at %s digests to %s, not the %s the record "
                        "names" % (what, path, commit[:12], got[:16],
                                   sha256[:16]))
    return data.decode("utf-8")


def squash(text: str) -> str:
    return " ".join(text.split())


# ---------------------------------------------------------------- inputs


def load_tranche(path: Path | None = None) -> dict:
    import yaml

    path = path or (repo_root() / TRANCHE)
    data = yaml.safe_load(path.read_bytes().decode("utf-8"))
    if not isinstance(data, dict) or not isinstance(data.get("classes"), list):
        raise Refused("%s has no `classes` list" % TRANCHE)
    return data


def vocabulary():
    """(labels, definitions, digests) from the vocabulary build, by IRI."""
    import rdflib
    import build as vocab

    result = vocab.build(vocab.default_inputs())
    if result.findings:
        raise Refused("the vocabulary build has findings; run "
                      "tools/vocab/build.py first: %s" % result.findings[0])
    graph = rdflib.Graph()
    for name in ("bco-metamodel.ttl", "bco-catalog.ttl"):
        graph.parse(data=result.files[name].decode("utf-8"), format="turtle")
    labels, definitions = {}, {}
    for s, o in graph.subject_objects(rdflib.URIRef(SKOS + "prefLabel")):
        if getattr(o, "language", None) == "en":
            labels.setdefault(str(s), []).append(str(o))
    for s, o in graph.subject_objects(rdflib.URIRef(SKOS + "definition")):
        if getattr(o, "language", None) == "en":
            definitions.setdefault(str(s), []).append(str(o))
    return labels, definitions, dict(result.digests), vocab.expand


def act_register() -> tuple[dict, set]:
    """{act local name: [genus IRI, ...]} and the development genera."""
    import yaml

    data = yaml.safe_load((repo_root() / ACT_TYPES).read_bytes()
                          .decode("utf-8"))
    genus = {}
    for entry in data["act_types"]:
        genus[entry["act_type"].split("#")[-1]] = list(entry["genus"])
    development = {g["iri"] for g in data["genera"] if g.get("development_act")}
    return genus, development


def t2_section(batch: str, tid: str) -> str | None:
    body = batch.split("\n## 6.")[0]
    for section in re.split(r"(?m)^(?=### T2-\d\d — )", body)[1:]:
        if section.startswith("### %s — " % tid):
            return section
    return None


def signed_class(record: dict, text: str, tid: str) -> tuple[str, list]:
    """(definition, index) as the signed record states them."""
    if tid.startswith("T2-"):
        section = t2_section(text, tid)
        if section is None:
            return "", []
        match = re.search(r"^\| Definition \| (.+?) \|$", section, re.M)
        definition = match.group(1) if match else ""
        index = section.split("**Excluded** (")[0]
        index = index.split("**Realization index** (")[1] \
            if "**Realization index** (" in index else ""
        return definition, INDEX_MEMBER.findall(index)
    # Tranche 1: a "**Definition** (...). text" paragraph, then the index.
    match = re.search(r"^\*\*Definition\*\* \([^)]*\)\. (.+?)\n\n", text,
                      re.M | re.S)
    definition = squash(match.group(1)) if match else ""
    index = text.split("**Realization index**")[1].split("\n\n**")[0] \
        if "**Realization index**" in text else ""
    return definition, INDEX_MEMBER.findall(index)


def definition_matches(signed: str, vocabulary_text: str) -> bool:
    """The signed cell is the vocabulary's definition, optionally followed by
    the batch's parenthetical provenance ("(revision 3, as in the
    vocabulary; ...)"), which is commentary on the definition, not part of
    it."""
    signed, vocabulary_text = squash(signed), squash(vocabulary_text)
    return (signed == vocabulary_text
            or signed.startswith(vocabulary_text + " ("))


# ---------------------------------------------------------------- verify


def verify(tranche: dict, vocab=None, register=None) -> tuple[list, list]:
    """(findings, classes): every check above, and the class rows the
    module is written from, each built from the sources, not the record."""
    findings: list = []
    labels, definitions, digests, expand = vocab or vocabulary()
    genus, development = register or act_register()

    readiness = tranche.get("readiness") or {}
    approved = signed_text(readiness.get("commit", "HEAD"),
                           readiness.get("path", ""),
                           readiness.get("sha256", ""), findings,
                           "readiness package")
    rows = {m.group(1): m for m in READINESS_ROW.finditer(approved)}
    ready = {tid for tid, m in rows.items() if m.group(7) == "ready"}
    held = set(rows) - ready

    signatures = tranche.get("signatures") or {}
    t2 = signatures.get("G1T-T2") or {}
    sig_text = signed_text(t2.get("commit", "HEAD"), t2.get("path", ""),
                           t2.get("sha256", ""), findings, "signature record")
    if (t2.get("signs") or {}).get("sha256", "") not in sig_text:
        findings.append("the T2 signature record does not name the batch "
                        "digest the tranche record gives")
    signed_rows = {m.group(1): m for m in SIGNATURE_ROW.finditer(sig_text)}
    t1 = signatures.get("G1T-T1") or {}
    t1_decision = (repo_root() / t1.get("path", "")).read_bytes() \
        .decode("utf-8") if t1.get("path") else ""
    for path, sha in (t1.get("signs") or {}).items():
        if sha not in t1_decision:
            findings.append("the T1 signature record does not name %s for "
                            "%s" % (sha[:16], path))

    excluded = set((tranche.get("excluded") or {}))
    if excluded != held:
        findings.append("the tranche record excludes %s; the readiness "
                        "package holds back %s"
                        % (sorted(excluded), sorted(held)))

    seen, classes, texts = set(), [], {}
    for n, entry in enumerate(tranche["classes"]):
        tid = entry.get("g1t")
        where = "classes[%d] (%s)" % (n, tid)
        if tid in seen:
            findings.append("%s is listed twice" % where)
            continue
        seen.add(tid)
        if tid not in ready:
            findings.append("%s is not a ready row of the readiness package"
                            % where)
            continue
        row = rows[tid]
        for key, want in (("concept", row.group(2)), ("class", row.group(3)),
                          ("label", row.group(4).strip())):
            if entry.get(key) != want:
                findings.append("%s %s %r; the readiness package says %r"
                                % (where, key, entry.get(key), want))
        concept = expand(row.group(2))
        cls = BCO + row.group(3).split(":", 1)[1]
        if row.group(2).split(":", 1)[1] != row.group(3).split(":", 1)[1]:
            findings.append("%s: the class's local name is not the "
                            "concept's (S1)" % where)

        digest = digests.get(concept)
        if entry.get("concept_record_sha256") != digest:
            findings.append("%s concept_record_sha256 is %s; the vocabulary "
                            "build gives %s" % (
                                where, entry.get("concept_record_sha256"),
                                digest))
        if not (digest or "").startswith(row.group(6)):
            findings.append("%s: the concept's record digest has moved since "
                            "the readiness package (%s…)" % (where,
                                                             row.group(6)))
        if tid in signed_rows:
            srow = signed_rows[tid]
            if srow.group(5) != digest:
                findings.append("%s: the concept's record digest is not the "
                                "one the signature names" % where)
            if srow.group(3) != row.group(2):
                findings.append("%s: the signature names %s"
                                % (where, srow.group(3)))
        elif tid.startswith("T2-"):
            findings.append("%s has no row in the T2 signature record" % where)

        record = entry.get("signed_record") or {}
        commit, path = record.get("commit", ""), record.get("path", "")
        if not COMMIT.fullmatch(commit) or not SHA.fullmatch(
                record.get("sha256", "")):
            findings.append("%s signed_record needs a full commit and "
                            "SHA-256" % where)
            continue
        if tid.startswith("T2-"):
            if record.get("sha256") != (t2.get("signs") or {}).get("sha256"):
                findings.append("%s: not the batch digest the signature "
                                "names" % where)
        elif record.get("sha256") != (t1.get("signs") or {}).get(path):
            findings.append("%s: not the digest the T1 signature names"
                            % where)
        key = (commit, path)
        if key not in texts:
            texts[key] = signed_text(commit, path, record["sha256"],
                                     findings, where)
        definition, index = signed_class(record, texts[key], tid)
        if not index:
            findings.append("%s: no realization index in the signed record"
                            % where)
        if entry.get("index") != index:
            findings.append("%s index %s differs from the signed index %s"
                            % (where, entry.get("index"), index))
        if int(row.group(5)) != len(index):
            findings.append("%s: the signed index has %d members; the "
                            "readiness package says %s"
                            % (where, len(index), row.group(5)))

        label = labels.get(concept) or []
        text = definitions.get(concept) or []
        if len(label) != 1 or len(text) != 1:
            findings.append("%s: the vocabulary gives %d English labels and "
                            "%d definitions for %s"
                            % (where, len(label), len(text), row.group(2)))
            continue
        if label[0] != row.group(4).strip():
            findings.append("%s: the vocabulary's label %r is not the "
                            "readiness package's %r"
                            % (where, label[0], row.group(4).strip()))
        if not definition_matches(definition, text[0]):
            findings.append("%s: the vocabulary's definition is not the "
                            "signed one" % where)

        dev = {}
        for member in index:
            if not ACT.fullmatch(member) or member not in genus:
                findings.append("%s: %s is no act type in the BPO register"
                                % (where, member))
                continue
            if ORGANIZATION_CAPABILITY in genus[member]:
                findings.append("%s: %s is capability-typed (CAP-03)"
                                % (where, member))
            if set(genus[member]) & development:
                dev[member] = True
        listed = entry.get("development_members") or {}
        if set(listed) != set(dev):
            findings.append("%s: development-genus members %s; the tranche "
                            "record lists %s (CAP-06)"
                            % (where, sorted(dev), sorted(listed)))
        for member, reason in listed.items():
            if not str(reason).strip() or str(reason) not in texts[key]:
                findings.append("%s: %s's CAP-06 reason is not the signed "
                                "one" % (where, member))

        classes.append({"g1t": tid, "iri": cls, "label": label[0],
                        "definition": text[0], "index": index})

    missing = ready - seen
    if missing:
        findings.append("ready rows the tranche record omits: %s"
                        % sorted(missing))

    parent = tranche.get("parent") or {}
    pconcept = expand(parent.get("concept", ""))
    plabel = labels.get(pconcept) or []
    ptext = definitions.get(pconcept) or []
    if parent.get("class") != "bco:BusinessCapability" or len(plabel) != 1 \
            or len(ptext) != 1:
        findings.append("the parent must be bco:BusinessCapability, with one "
                        "label and one definition from %s"
                        % parent.get("concept"))
        return findings, classes
    if parent.get("parents") != ["cco:ont00000568", "obo:BFO_0000016"]:
        findings.append("the parent's parents are cco:ont00000568 and "
                        "obo:BFO_0000016 (S2)")
    if not (repo_root() / parent.get("admitted_by", "")).is_file():
        findings.append("the parent's admitting record is missing")
    classes.insert(0, {"g1t": None, "iri": BCO + "BusinessCapability",
                       "label": plabel[0], "definition": ptext[0],
                       "index": []})
    return findings, classes


# ---------------------------------------------------------------- write


def triples(classes: list, version: str) -> list:
    import rdflib

    U, L = rdflib.URIRef, rdflib.Literal
    module = U(MODULE_IRI)
    out = [
        (module, U(RDF + "type"), U(OWL + "Ontology")),
        (module, U(DCTERMS + "title"),
         L("Business Capability Ontology: capability module")),
        (module, U(OWL + "versionInfo"), L(version)),
        (module, U(RDFS + "comment"), L(
            "The Business Capability parent and the specific capability "
            "classes of the first Stage 05 tranche, written by %s from %s. "
            "Each specific class's index is its signed G1-T realization "
            "index, one bpo:enablesProcess annotation per member. No class "
            "here asserts that any organization bears it (G1-I)."
            % (GENERATOR, TRANCHE))),
    ]
    parent = U(BCO + "BusinessCapability")
    for row in classes:
        s = U(row["iri"])
        out += [(s, U(RDF + "type"), U(OWL + "Class")),
                (s, U(RDFS + "label"), L(row["label"], lang="en")),
                (s, U(SKOS + "definition"), L(row["definition"], lang="en"))]
        if row["g1t"] is None:
            out += [(s, U(RDFS + "subClassOf"), U(ORGANIZATION_CAPABILITY)),
                    (s, U(RDFS + "subClassOf"), U(OBO + "BFO_0000016"))]
        else:
            out.append((s, U(RDFS + "subClassOf"), parent))
            out += [(s, U(ENABLES), U(BPO + m)) for m in row["index"]]
    return out


def render(classes: list) -> bytes:
    n = len(classes) - 1
    members = sum(len(r["index"]) for r in classes)
    version = ("0.1.0 -- first Stage 05 tranche: bco:BusinessCapability and "
               "%d specific classes; specification v0.5.0-draft.3" % n)
    header = [
        "Generated by %s from %s -- do not edit." % (GENERATOR, TRANCHE),
        "",
        "Business Capability Ontology: capability module, first tranche.",
        "",
        "  classes     bco:BusinessCapability and %d specific classes" % n,
        "  index       %d bpo:enablesProcess annotations, %d distinct acts"
        % (members, len({m for r in classes for m in r["index"]})),
        "  decisions   D5-3, docs/decisions/2026-11-15-bpo-inquiry-and-d5-approved.md",
        "              D6 E, docs/decisions/2026-11-15-v05-transition-approved-d6-authorized.md",
        "",
        "Under the Stage 05 standard (docs/standards/stage-05-ontology.md):",
        "each class carries only its type, its one named parent, its label,",
        "its definition and its index. No object property, restriction,",
        "equivalence, disjointness or individual is written. BPO's act",
        "classes are referenced through ex: and never redeclared; their",
        "declarations are in vendor/bpo/bpo-ext-bco-extract.ttl.",
        "",
        "Labels and definitions are the controlled vocabulary's",
        "(src/01_controlled_vocabulary/). Index members embed APQC PCF element",
        "IDs in their IRIs (APQC's notice: NOTICE.md).",
    ]
    table = vendor_upstream.prefixes() + (("bco", BCO),)
    rows = triples(classes, version)
    text = vendor_upstream.serialise(rows, header, table)
    vendor_upstream.round_trip(text, rows)
    return text.encode("utf-8")


def module_path() -> Path:
    return layout.component(MODULE_ID).resolve()


# ------------------------------------------------- the description tranche
#
# The description layer (decision of 2026-11-15, B-1): information classes
# (K3) and two annotation properties, written into apqc-cap-desc.ttl from
# src/05_ontology/tranche-2-description.yaml. G1-T does not apply to them.
# Each class carries only its type, its one named parent, its label and its
# definition; each property its type, its label and, as its definition,
# section 4's "Use" cell, the only definition the specification gives. No object
# property, restriction, equivalence, disjointness or individual.

DESC_TRANCHE = "src/05_ontology/tranche-2-description.yaml"
DESC_MODULE_ID = "ontology.cap-desc"
DESC_MODULE_IRI = "https://fandaws.com/ontology/bco/apqc-cap-desc"
DESIGNATES = BCO + "designatesClass"
#: The adequacy assessment's section 4 row, which has no IRI.
FAA_ROW = re.compile(r"^\| Functional Adequacy Assessment \*\(new, R9; "
                     r"representation open\)\* \| (.+?) \| (.+?) \| (.+?) \|$",
                     re.M)
#: The decision that chose the adequacy assessment's representation.
FAA_DECISION = ("`bco:FunctionalAdequacyAssessment`, under CCO Descriptive "
                "Information Content Entity (`cco:ont00000853`)")


def load_description(path: Path | None = None) -> dict:
    import yaml

    path = path or (repo_root() / DESC_TRANCHE)
    data = yaml.safe_load(path.read_bytes().decode("utf-8"))
    if not isinstance(data, dict) or not isinstance(data.get("classes"), list):
        raise Refused("%s has no `classes` list" % DESC_TRANCHE)
    return data


def designations() -> dict:
    """{concept IRI: [designated class IRI, ...]} from the vocabulary build."""
    import rdflib
    import build as vocab

    result = vocab.build(vocab.default_inputs())
    graph = rdflib.Graph().parse(
        data=result.files["bco-metamodel.ttl"].decode("utf-8"),
        format="turtle")
    out: dict = {}
    for s, o in graph.subject_objects(rdflib.URIRef(DESIGNATES)):
        out.setdefault(str(s), []).append(str(o))
    return out


def declared_classes() -> set:
    """Every class the vendored CCO and BFO extracts declare."""
    import rdflib

    graph = rdflib.Graph()
    for path in layout.vendored_files():
        graph.parse(path, format="turtle")
    return {str(s) for s in graph.subjects(rdflib.RDF.type, rdflib.OWL.Class)}


def spec_rows(text: str) -> dict:
    """{`bco:X`: (definition, parent cell)} for section 4's term rows, and
    {`bco:p`: use} for its annotation-property rows."""
    section = text.split("\n## 4. Terms")[1].split("\n## 5.")[0]
    rows, uses = {}, {}
    for line in section.splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if not line.startswith("| ") or len(cells) < 3:
            continue
        match = re.search(r"`(bco:\w+)`", cells[0])
        if not match:
            continue
        if cells[0] == "`%s`" % match.group(1):
            uses[match.group(1)] = cells[1]
        else:
            rows[match.group(1)] = (cells[1], cells[2])
    return {"terms": rows, "uses": uses}


def relation_labels(text: str) -> dict:
    """{`bco:p`: label} from section 5's relation table."""
    section = text.split("\n## 5. Relations")[1].split("\n**Class pattern")[0]
    out = {}
    for match in re.finditer(r"^\| ([a-z ]+) \| `(bco:\w+)` \(annotation\) \|",
                             section, re.M):
        out[match.group(2)] = match.group(1)
    return out


def verify_description(record: dict, vocab=None, designated=None,
                       declared=None) -> tuple[list, dict]:
    """(findings, {"classes": [...], "properties": [...]}): each row built
    from the sources it names, never from the record's own copy."""
    findings: list = []
    labels, definitions, digests, expand = vocab or vocabulary()
    designated = designations() if designated is None else designated
    declared = declared_classes() if declared is None else declared

    spec = record.get("specification") or {}
    path = repo_root() / spec.get("path", "")
    text = path.read_bytes().decode("utf-8") if path.is_file() else ""
    got = hashlib.sha256(text.encode("utf-8")).hexdigest()
    if got != spec.get("sha256"):
        findings.append("the specification digests to %s, not the %s the "
                        "record names" % (got[:16], str(spec.get("sha256"))[:16]))
    rows = spec_rows(text) if text else {"terms": {}, "uses": {}}
    relabels = relation_labels(text) if text else {}
    decision_path = repo_root() / (record.get("authorized_by") or {}).get(
        "path", "")
    decision = decision_path.read_bytes().decode("utf-8") \
        if decision_path.is_file() else ""
    if "B-1 — Description Layer: APPROVED" not in decision:
        findings.append("the authorizing decision record is missing or does "
                        "not approve B-1")

    out = {"classes": [], "properties": []}
    seen = set()
    for n, entry in enumerate(record["classes"]):
        cls = entry.get("class", "")
        where = "classes[%d] (%s)" % (n, cls)
        if not re.fullmatch(r"bco:[A-Z]\w+", cls) or cls in seen:
            findings.append("%s: not a bco: class IRI, or listed twice" % where)
            continue
        seen.add(cls)
        iri = BCO + cls[4:]
        parent = entry.get("parent", "")
        if not parent.startswith("cco:") or \
                CCO + parent[4:] not in declared:
            findings.append("%s: parent %s is not a class the vendored CCO "
                            "extract declares" % (where, parent))
        if parent == "cco:ont00000568":
            findings.append("%s: an information class is never under "
                            "Organization Capability" % where)
        concept = entry.get("concept")
        if concept is None:
            match = FAA_ROW.search(text)
            if cls != "bco:FunctionalAdequacyAssessment" or not match:
                findings.append("%s has no concept, and is not the adequacy "
                                "assessment whose row has no IRI" % where)
                continue
            if FAA_DECISION not in decision or parent != "cco:ont00000853":
                findings.append("%s: the parent is not the one the decision "
                                "chose" % where)
            label, definition = entry.get("label"), match.group(1)
            if label != "Functional Adequacy Assessment":
                findings.append("%s: the label is not section 4's" % where)
        else:
            curie = "bco:" + concept.split(":", 1)[1]
            cexp = expand(concept)
            if curie != cls:
                findings.append("%s: the class's local name is not the "
                                "concept's (S1)" % where)
            if digests.get(cexp) != entry.get("concept_record_sha256"):
                findings.append("%s concept_record_sha256 is %s; the "
                                "vocabulary build gives %s"
                                % (where, entry.get("concept_record_sha256"),
                                   digests.get(cexp)))
            if designated.get(cexp) != [iri]:
                findings.append("%s: the concept designates %s"
                                % (where, designated.get(cexp)))
            label = (labels.get(cexp) or [None])[0]
            definition = (definitions.get(cexp) or [None])[0]
            if len(labels.get(cexp) or []) != 1 or \
                    len(definitions.get(cexp) or []) != 1:
                findings.append("%s: the vocabulary gives no single English "
                                "label and definition" % where)
                continue
            row = rows["terms"].get(cls)
            if row is None:
                findings.append("%s: no section 4 row names it" % where)
                continue
            if squash(row[0]) != squash(definition):
                findings.append("%s: the vocabulary's definition is not "
                                "section 4's" % where)
            if row[1] != "`%s`" % parent:
                findings.append("%s: section 4 gives the parent %s, the "
                                "record %s" % (where, row[1], parent))
        out["classes"].append({"iri": iri, "label": label,
                               "definition": definition,
                               "parent": CCO + parent[4:]})

    for n, entry in enumerate(record.get("annotation_properties") or []):
        prop = entry.get("property", "")
        where = "annotation_properties[%d] (%s)" % (n, prop)
        if rows["uses"].get(prop) != entry.get("use"):
            findings.append("%s: the use is not section 4's" % where)
        if relabels.get(prop) != entry.get("label"):
            findings.append("%s: the label is not section 5's (%s)"
                            % (where, relabels.get(prop)))
        out["properties"].append({"iri": BCO + prop[4:],
                                  "label": entry.get("label"),
                                  "use": entry.get("use")})
    if set(rows["uses"]) != {p["iri"].replace(BCO, "bco:")
                             for p in out["properties"]}:
        findings.append("the record's annotation properties are not section "
                        "4's: %s" % sorted(rows["uses"]))
    return findings, out


def render_description(rows: dict) -> bytes:
    import rdflib

    U, L = rdflib.URIRef, rdflib.Literal
    n, p = len(rows["classes"]), len(rows["properties"])
    version = ("0.1.0 -- Stage 05 description tranche: %d information classes "
               "and %d annotation properties; specification v0.5.0-draft.3"
               % (n, p))
    module = U(DESC_MODULE_IRI)
    out = [
        (module, U(RDF + "type"), U(OWL + "Ontology")),
        (module, U(DCTERMS + "title"),
         L("Business Capability Ontology: description module")),
        (module, U(OWL + "versionInfo"), L(version)),
        (module, U(RDFS + "comment"), L(
            "The description layer and the evidence register (specification "
            "v0.5 section 4; CD14, CD15, CD17): information content entity "
            "classes about organizations and their capabilities, and the two "
            "annotation properties bco:concernsType and bco:assessedPresence, "
            "written by %s from %s. No class here is a capability type, and "
            "none asserts that any organization bears a capability."
            % (GENERATOR, DESC_TRANCHE))),
    ]
    for row in rows["classes"]:
        s = U(row["iri"])
        out += [(s, U(RDF + "type"), U(OWL + "Class")),
                (s, U(RDFS + "subClassOf"), U(row["parent"])),
                (s, U(RDFS + "label"), L(row["label"], lang="en")),
                (s, U(SKOS + "definition"), L(row["definition"], lang="en"))]
    for row in rows["properties"]:
        s = U(row["iri"])
        out += [(s, U(RDF + "type"), U(OWL + "AnnotationProperty")),
                (s, U(RDFS + "label"), L(row["label"], lang="en")),
                (s, U(SKOS + "definition"), L(row["use"], lang="en"))]
    header = [
        "Generated by %s from %s -- do not edit." % (GENERATOR, DESC_TRANCHE),
        "",
        "Business Capability Ontology: description module.",
        "",
        "  classes     %d information classes (K3), each under one CCO" % n,
        "              information class; none under cco:ont00000568",
        "  properties  %d annotation properties; no object property" % p,
        "  decision    B-1, docs/decisions/2026-11-15-b1-b4-approved-cap34-confirmed.md",
        "",
        "Labels and definitions are the controlled vocabulary's, which are",
        "specification section 4's; the Functional Adequacy Assessment's are",
        "its section 4 row's, and its parent is the one the decision chose.",
        "The constraints on individuals are shapes/description_shapes.ttl.",
    ]
    table = vendor_upstream.prefixes() + (("bco", BCO),)
    text = vendor_upstream.serialise(out, header, table)
    vendor_upstream.round_trip(text, out)
    return text.encode("utf-8")


def desc_module_path() -> Path:
    return layout.component(DESC_MODULE_ID).resolve()


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--write", action="store_true",
                    help="regenerate src/05_ontology/apqc-cap.ttl and "
                         "apqc-cap-desc.ttl")
    args = ap.parse_args(argv)
    vocab = vocabulary()
    findings, classes = verify(load_tranche(), vocab=vocab)
    dfindings, drows = verify_description(load_description(), vocab=vocab)
    findings += ["description tranche: %s" % f for f in dfindings]
    if findings:
        for finding in findings:
            print("FINDING  %s" % finding)
        print("%d finding(s); nothing written" % len(findings))
        return 1
    stale = False
    for path, data in ((module_path(), render(classes)),
                       (desc_module_path(), render_description(drows))):
        if args.write:
            path.write_bytes(data)
            print("wrote %s (%d bytes)" % (path, len(data)))
        elif not path.is_file() or path.read_bytes() != data:
            print("FINDING  %s is not what its tranche record produces; run "
                  "%s --write" % (path.name, GENERATOR))
            stale = True
    if stale:
        return 1
    members = sum(len(r["index"]) for r in classes)
    print("ok: %d classes (the parent and %d specific), %d index members "
          "verified against their signed records, %d distinct acts; the "
          "module is a fresh build"
          % (len(classes), len(classes) - 1, members,
             len({m for r in classes for m in r["index"]})))
    print("ok: description module, %d information classes and %d annotation "
          "properties verified against the vocabulary and section 4; a "
          "fresh build" % (len(drows["classes"]), len(drows["properties"])))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
