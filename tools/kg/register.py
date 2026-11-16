# SPDX-License-Identifier: MIT
"""Stage 06 register data: the CP-3 scope audit, the coverage register and
the bc: migration manifest (docs/standards/stage-06-knowledge-graph.md).

    python tools/kg/register.py           # check; exit 1 on a finding
    python tools/kg/register.py --write   # regenerate the audit and register

The audit (src/06_knowledge_graph/scope-audit.yaml) and the register
(src/06_knowledge_graph/coverage-register.json) are generated from reviewed
records, never typed. The check requires each committed file to be what this
tool writes, the register to match config/coverage-register.schema.json, and
the hand-authored migration manifest (src/06_knowledge_graph/bc-migration.yaml)
to keep S06-MG's rules.

THE SCOPE AUDIT (S06-A1, K10)

One row per entry of BPO's capabilities/capability_scope.json at the pin, as
harvested in docs/sources/inventory/bpo-entries.yaml. Each row keeps two
things apart:

  bpo   what BPO declares: the key, whether BPO declares it as a capability
        class, and how many of its index entries name acts and how many name
        capability classes.
  bco   what the BCO has independently accepted: a written class (its tranche
        and G1-T records), a vocabulary concept that is not admitted, or
        nothing. Taken only from reviewed BCO records: an accepted candidate
        in the tranche 2 review, or a specification section 9 row. A
        synthesized crosswalk candidate is recorded as provenance and never
        counted as an acceptance.

Each row has a staging status, as CP-3 requires, and the next step the
specification names. The audit admits nothing, reclassifies nothing and
asserts no subclass.

THE COVERAGE REGISTER, BATCH 1 (S06-R1, S06-R2, K8)

The source is the Stage 03 review's retained part-of links
(docs/catalog/tranche-2-review.yaml): the Stage 03 standard says that where
CD16 applies, a part-of link is recorded in the coverage register. A broader
candidate is a standing function in batch 1 only if all of these hold:

  - its concept cites exactly one PCF 7.4 element, and that element's BPO
    catalog node is in the PCF inventory (the key);
  - every retained part-of link to it was kept as reviewed (none merged,
    retargeted or kept outside), and none is a narrowing, which leaves the
    rest of the grouping unlisted;
  - every component is a class written in a Stage 05 module;
  - it has no retained kind-of link: whether possessing a subtype bears on
    the function's coverage is not decided;
  - no unresolved link points to it.

Anything else is listed under `waiting`, with its reasons. A component is a
class IRI only (OI-13 for version 1). If the grouping's own concept is a
written class, it is recorded as the whole-function class, never as a
component (CAP-22).

Only identifiers enter: the catalog node's IRI and its PCF element id, under
the rights basis recorded in the file. No PCF name, description or hierarchy
id is written. The file carries APQC's notice, because a PCF element id is
PCF material (tools/licensing/pcf_notice.py).
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))

import layout  # noqa: E402

AUDIT = "src/06_knowledge_graph/scope-audit.yaml"
REGISTER = "src/06_knowledge_graph/coverage-register.json"
MIGRATION = "src/06_knowledge_graph/bc-migration.yaml"
SCHEMA = "config/coverage-register.schema.json"
STANDARD = "docs/standards/stage-06-knowledge-graph.md"
DECISION = "docs/decisions/2026-11-16-stage06-standard-and-first-increment.md"
RIGHTS_DECISION = "docs/decisions/2026-10-29-apqc-pcf-sourcing-decided.md"

BPO_ENTRIES = "docs/sources/inventory/bpo-entries.yaml"
PCF_ENTRIES = "docs/sources/inventory/pcf-7.4-entries.yaml"
CROSSWALK = "docs/catalog/crosswalk.yaml"
REVIEW = "docs/catalog/tranche-2-review.yaml"
CATALOG = "src/01_controlled_vocabulary/catalog.yaml"
TRANCHE = "src/05_ontology/tranche-1.yaml"
SPEC = "specifications/Business-Capability-Ontology-v0.5.0-draft.3.md"
DRAFT = "drafts/BusinessCapabilityOntology_draft_v0.1.0"

BCO = "https://fandaws.com/ontology/bco#"
BPO = "https://fandaws.com/ontology/bpo#"
BC = "https://example.org/BusinessCapabilityOntology#"

#: Specification section 9 rows that name a BCO position on a BPO scope key,
#: and the pilot vocabulary concept each corresponds to. Only rows whose BPO
#: class is a capability_scope.json key are listed.
SECTION_9 = {
    BPO + "StrategicPlanningCapability": {
        "concept": "bcoc:StrategicPlanning",
        "row": "ex:StrategicPlanningCapability: a candidate for "
               "bco:StrategicPlanningCapability; its index from the scope "
               "file once OI-20 clears; G1-T; no only without a CAP-30 review",
    },
    BPO + "CustomerExperienceManagementCapability": {
        "concept": "bcoc:CustomerExperienceManagement",
        "row": "ex:CustomerExperienceManagementCapability: each index member "
               "reviewed under CD5 before G1-T",
    },
}

STAGING = {
    "written": "admitted and written: a G1-T PASS and a Stage 05 class",
    "concept-not-admitted": "staged: a BCO vocabulary concept (Draft) with no "
                            "G1-T PASS; nothing is written",
    "none": "staged: no BCO concept accepts it; nothing is written",
}

PCF_LOCATOR = re.compile(r"PCF 7\.4 element (\d+) \(hierarchy [\d.]+\)")


class Refused(SystemExit):
    pass


def load_yaml(rel: str):
    import yaml
    return yaml.safe_load((layout.repository_root() / rel).read_bytes()
                          .decode("utf-8"))


def written_classes() -> dict:
    """concept -> {class, g1t, signed_record}, from the tranche record, each
    class confirmed declared in a Stage 05 module."""
    import rdflib
    graph = rdflib.Graph()
    for module in layout.components("ontology-module"):
        graph.parse(module.resolve(), format="turtle")
    declared = {str(s) for s in graph.subjects(
        rdflib.RDF.type, rdflib.OWL.Class)}
    out = {}
    for row in load_yaml(TRANCHE)["classes"]:
        iri = BCO + row["class"].split(":", 1)[1]
        if iri not in declared:
            raise Refused("%s names %s, which no module declares"
                          % (TRANCHE, row["class"]))
        out[row["concept"]] = {"class": iri, "g1t": row["g1t"],
                               "signed_record": row["signed_record"]["path"]}
    return out


def concepts() -> dict:
    return {c["id"]: c for c in load_yaml(CATALOG)["concepts"]}


def pcf_element(concept: dict) -> str | None:
    """The single PCF 7.4 element a concept's sources cite, or None."""
    found = set()
    for source in concept.get("sources") or []:
        found.update(PCF_LOCATOR.findall(source.get("locator", "")))
    return found.pop() if len(found) == 1 else None


# ------------------------------------------------------------------ audit

def audit() -> dict:
    written = written_classes()
    catalog = concepts()
    entries = load_yaml(BPO_ENTRIES)["entries"]
    scope = [e for e in entries if e["kind"] == "scope-entry"]
    crosswalk = {r["inventory_id"]: r for r in load_yaml(CROSSWALK)["records"]}
    review = {c["id"]: c for c in load_yaml(REVIEW)["candidates"]}
    rows = []
    for entry in scope:
        ids = [entry["id"]] + ([entry["capability_class_entry"]]
                               if entry.get("capability_class_entry") else [])
        candidates = sorted({i["candidate"] for rid in ids
                             for i in (crosswalk.get(rid) or {})
                             .get("interpretations", [])
                             if i.get("relation") == "designates"})
        kinds = [p["target_kind"] for p in entry["enables_process"]]
        bpo = {
            "key": entry["iri"],
            "entry": entry["id"],
            "locator": entry["locator"],
            "declared_as_capability_class":
                entry.get("capability_class_entry") is not None,
            "index_entries": {"acts": kinds.count("act"),
                              "capability_classes": kinds.count("capability")},
        }
        accepted, via = None, None
        for bcc in candidates:
            c = review.get(bcc)
            if c and c.get("disposition") == "accepted" and c.get("concept"):
                accepted, via = c["concept"], {
                    "record": REVIEW, "candidate": bcc,
                    "g1t": c.get("g1t")}
        if accepted is None and entry["iri"] in SECTION_9:
            row9 = SECTION_9[entry["iri"]]
            accepted, via = row9["concept"], {
                "record": SPEC + ", section 9", "row": row9["row"]}
        if accepted in written:
            status = "written"
        elif accepted is not None:
            status = "concept-not-admitted"
        else:
            status = "none"
        bco = {"accepted": status, "staging_status": STAGING[status]}
        if accepted is not None:
            if accepted not in catalog:
                raise Refused("%s: %s is not a vocabulary concept"
                              % (entry["id"], accepted))
            bco["concept"] = accepted
            bco["concept_status"] = catalog[accepted]["authored_status"]
            bco["accepted_by"] = via
        if status == "written":
            bco.update(written[accepted])
        next_steps = []
        if not bpo["declared_as_capability_class"]:
            next_steps.append("BPO-side: the key is not declared as a "
                              "capability class (CAP-13 cannot resolve it)")
        if bpo["index_entries"]["capability_classes"]:
            next_steps.append("BPO-side: re-index the entries that name "
                              "capability classes to acts (section 9; OI-20)")
        if status != "written":
            next_steps.append("BCO: a candidate for a later tranche only "
                              "through G1-T; nothing is admitted from BPO's "
                              "declaration")
        rows.append({"bpo": bpo, "bco": bco,
                     "crosswalk_candidates": candidates,
                     "next": next_steps})
    rows.sort(key=lambda r: r["bpo"]["key"])
    return {
        "format": 1,
        "check": "S06-A1 (%s, section 4)" % STANDARD,
        "generator": "tools/kg/register.py --write",
        "decision": DECISION,
        "source": {
            "file": "capabilities/capability_scope.json",
            "commit": scope[0]["version"]["commit"],
            "harvested_in": BPO_ENTRIES,
        },
        "rule": ("bpo is what BPO declares; bco is what the BCO has "
                 "independently accepted, from reviewed records only. A "
                 "crosswalk candidate is provenance, never an acceptance. "
                 "Nothing here admits a type, changes a classification or "
                 "asserts a subclass (K10)."),
        "summary": {
            "entries": len(rows),
            "bco_written": sum(r["bco"]["accepted"] == "written" for r in rows),
            "bco_concept_not_admitted": sum(
                r["bco"]["accepted"] == "concept-not-admitted" for r in rows),
            "bco_none": sum(r["bco"]["accepted"] == "none" for r in rows),
            "bpo_keys_not_capability_classes": sum(
                not r["bpo"]["declared_as_capability_class"] for r in rows),
            "bpo_keys_indexing_capability_classes": sum(
                bool(r["bpo"]["index_entries"]["capability_classes"])
                for r in rows),
        },
        "entries": rows,
    }


# --------------------------------------------------------------- register

def pcf_inventory() -> tuple[dict, str]:
    data = load_yaml(PCF_ENTRIES)
    nodes = {e["pcf_element_id"]: e["bpo_iri"] for e in data["entries"]}
    return nodes, data["apqc_notice"]


def pcf_ancestors() -> dict:
    """element id -> the set of its ancestors' element ids, itself included."""
    parent = {e["pcf_element_id"]: e.get("parent_pcf_element_id")
              for e in load_yaml(PCF_ENTRIES)["entries"]}
    out = {}
    for element in parent:
        seen, here = set(), element
        while here and here not in seen:
            seen.add(here)
            here = parent.get(here)
        out[element] = seen
    return out


def add_notes(functions: list, catalog: dict) -> None:
    """The notes batch 1's synthetic domain review asked for, derived from
    the data so that each one holds wherever its condition does
    (src/06_knowledge_graph/register-batch-1-review.md, findings 2, 3 to 5)."""
    ancestors = pcf_ancestors()
    users = {}
    for f in functions:
        for c in f["components"]:
            users.setdefault(c["class"], []).append(f["key"])
    for f in functions:
        notes = []
        if f["whole_function_class"]:
            notes.append(
                "Not a complete breakdown: the function's work outside the "
                "listed components belongs to the whole-function class "
                "itself, whose own realization index holds it.")
        for c in f["components"]:
            element = pcf_element(catalog[c["concept"]])
            if element and f["pcf_element_id"] not in ancestors.get(element,
                                                                    {element}):
                notes.append(
                    "%s is a component by a reviewed part-of link, though its "
                    "own PCF element is outside this key's subtree; a join on "
                    "the PCF hierarchy alone would not find it."
                    % c["class"][len(BCO):])
            others = [k for k in users[c["class"]] if k != f["key"]]
            if others:
                notes.append(
                    "%s is also a component of %s. A shared capability type "
                    "says nothing about whether one arrangement serves both "
                    "functions." % (c["class"][len(BCO):],
                                    ", ".join(k[len(BPO):] for k in others)))
        f["notes"] = notes


def register() -> dict:
    written = written_classes()
    catalog = concepts()
    nodes, notice = pcf_inventory()
    review = load_yaml(REVIEW)
    cand = {c["id"]: c for c in review["candidates"]}
    links_to = {}
    for link in review["links"]:
        links_to.setdefault(link["broader"], []).append(link)
    narrowed = {c["id"]: c["narrowed_to"] for c in review["candidates"]
                if (c.get("narrowed_to") or {}).get("kind") == "part-of"}
    groups = sorted({l["broader"] for l in review["links"]
                     if l["disposition"] == "retained"
                     and l.get("kind") == "part-of"} | set(narrowed))
    functions, waiting = [], []
    for bcc in groups:
        concept = (cand.get(bcc) or {}).get("concept")
        links = links_to.get(bcc, [])
        part = [l for l in links if l["disposition"] == "retained"
                and l.get("kind") == "part-of"]
        reasons = []
        element = pcf_element(catalog[concept]) if concept in catalog else None
        if concept is None:
            reasons.append("no BCO concept for the grouping")
        elif element is None:
            reasons.append("its concept cites no single PCF 7.4 element")
        elif element not in nodes:
            reasons.append("PCF element %s is not in the PCF inventory"
                           % element)
        odd = sorted({l["action"] for l in part if l["action"] != "kept"})
        if odd:
            reasons.append("a part-of link was %s in review, so the component "
                           "list is not as reviewed" % " / ".join(odd))
        if bcc in narrowed:
            reasons.append("narrowed: the grouping keeps more than its "
                           "narrowed type, so its components are not all "
                           "listed")
        if any(l["disposition"] == "retained" and l.get("kind") == "kind-of"
               for l in links):
            reasons.append("it has kind-of subtypes; whether possessing a "
                           "subtype bears on coverage is not decided")
        if any(l["disposition"] == "unresolved" for l in links):
            reasons.append("an unresolved link points to it")
        components = []
        for l in part:
            if l["action"] != "kept":
                continue
            nc = (cand.get(l["narrower"]) or {}).get("concept")
            if nc not in written:
                reasons.append("component %s is not a written class"
                               % (nc or l["narrower"]))
                continue
            components.append({"class": written[nc]["class"],
                               "concept": nc,
                               "g1t": written[nc]["g1t"],
                               "link": {"record": REVIEW,
                                        "narrower": l["narrower"],
                                        "broader": bcc}})
        if bcc in narrowed and narrowed[bcc]["concept"] not in written:
            reasons.append("component %s is not a written class"
                           % narrowed[bcc]["concept"])
        if not components and not reasons:
            reasons.append("no component")
        if reasons:
            waiting.append({"grouping": bcc, "concept": concept,
                            "reasons": sorted(set(reasons))})
            continue
        whole = written.get(concept, {}).get("class")
        if whole in {c["class"] for c in components}:
            raise Refused("%s: the whole-function class is among its own "
                          "components (CAP-22)" % bcc)
        components.sort(key=lambda c: c["class"])
        functions.append({
            "key": nodes[element],
            "pcf_element_id": element,
            "grouping": bcc,
            "concept": concept,
            "whole_function_class": whole,
            "components": components,
            "rights": {
                "status": "established",
                "basis": RIGHTS_DECISION + ", sections 1 and 3",
                "source": "BPO ontology/apqc-catalog.ttl at "
                          "2e55edd9e86a0bc20fa88a21595cc61402faa5dc, as "
                          "harvested in " + PCF_ENTRIES,
                "content": "the catalog node's IRI and its element id only; "
                           "no PCF name, description or hierarchy id",
            },
        })
    functions.sort(key=lambda f: f["key"])
    add_notes(functions, catalog)
    return {
        "format": 1,
        "version": 1,
        "batch": 1,
        "status": "proposed for the architect's acceptance as one batch "
                  "(%s, D), after a separate synthetic domain review"
                  % DECISION,
        "check": "S06-R1, S06-R2, S06-R3 (%s, section 4)" % STANDARD,
        "generator": "tools/kg/register.py --write",
        "source": REVIEW,
        "rule": ("Components are capability types as written class IRIs "
                 "only (OI-13, version 1). A component list implies no "
                 "organization possesses them, and possessing them "
                 "establishes no integration, availability or adequacy. "
                 "No subclass link is generated (CAP-29)."),
        "apqc_notice": notice,
        "functions": functions,
        "waiting": waiting,
    }


# --------------------------------------------------------------- migration

def draft_classes() -> list[str]:
    """The v0.1 class IRIs, read as text from the checksummed draft (never
    loaded as ontology)."""
    import hashlib
    root = layout.repository_root() / DRAFT
    sums = {}
    for line in (root / "SHA256SUMS.txt").read_bytes().decode().splitlines():
        if line.strip():
            digest, name = line.split(None, 1)
            sums[name.strip().lstrip("*").lstrip("./")] = digest
    found = []
    for name in ("ontology/business-capability-core.ttl",
                 "ontology/business-capability-information.ttl"):
        data = (root / name).read_bytes()
        if sums.get(name) != hashlib.sha256(data).hexdigest():
            raise Refused("%s/%s does not match its SHA256SUMS" % (DRAFT, name))
        text = data.decode("utf-8")
        found += [BC + m for m in re.findall(
            r"^bc:(\w+)\s*\n\s*a owl:Class", text, re.M)]
    return sorted(found)


def module_graph():
    import rdflib
    graph = rdflib.Graph()
    for module in layout.components("ontology-module"):
        graph.parse(module.resolve(), format="turtle")
    return graph


def k1_classes(graph) -> set:
    """Every class written under bco:BusinessCapability, the parent excluded."""
    import rdflib
    parent = rdflib.URIRef(BCO + "BusinessCapability")
    return {str(s) for s in graph.subjects(rdflib.RDFS.subClassOf, parent)}


def check_register(data: dict) -> list[str]:
    """S06-R2 and K8 over a register: keys are catalog nodes in the PCF
    inventory, components are written K1 classes only, no whole-function
    class is among its own components, and every entry has a rights status."""
    findings = []
    nodes, notice = pcf_inventory()
    k1 = k1_classes(module_graph())
    if data.get("apqc_notice") != notice:
        findings.append("%s: apqc_notice is not APQC's notice" % REGISTER)
    for f in data.get("functions") or []:
        key = f.get("key")
        if nodes.get(f.get("pcf_element_id")) != key:
            findings.append("%s: %s is not the catalog node of PCF element %s"
                            % (REGISTER, key, f.get("pcf_element_id")))
        classes = [c.get("class") for c in f.get("components") or []]
        for c in classes:
            if c not in k1:
                findings.append("%s: component %s of %s is not a written "
                                "capability class (K8)" % (REGISTER, c, key))
        whole = f.get("whole_function_class")
        if whole is not None and whole not in k1:
            findings.append("%s: whole-function class %s of %s is not written"
                            % (REGISTER, whole, key))
        if whole is not None and whole in classes:
            findings.append("%s: %s is among its own function's components "
                            "(CAP-22)" % (REGISTER, whole))
        if len(set(classes)) != len(classes):
            findings.append("%s: %s lists a component twice" % (REGISTER, key))
        if (f.get("rights") or {}).get("status") != "established":
            findings.append("%s: %s has no established rights basis; withhold "
                            "it rather than commit it (E)" % (REGISTER, key))
    return findings


def check_audit(data: dict) -> list[str]:
    """S06-A1: one row per scope entry at the pin, BPO's declaration and the
    BCO's acceptance kept apart, the staging status from the closed list,
    and every acceptance citing its record."""
    findings = []
    scope = sorted(e["iri"] for e in load_yaml(BPO_ENTRIES)["entries"]
                   if e["kind"] == "scope-entry")
    rows = data.get("entries") or []
    keys = sorted(r.get("bpo", {}).get("key") for r in rows)
    if keys != scope:
        findings.append("%s: the rows are not exactly the %d scope entries"
                        % (AUDIT, len(scope)))
    written = written_classes()
    for r in rows:
        bco, key = r.get("bco") or {}, (r.get("bpo") or {}).get("key")
        status = bco.get("accepted")
        if status not in STAGING or bco.get("staging_status") != STAGING.get(
                status):
            findings.append("%s: %s has no closed-list staging status"
                            % (AUDIT, key))
        if status in ("written", "concept-not-admitted") and                 not (bco.get("accepted_by") or {}).get("record"):
            findings.append("%s: %s claims an acceptance with no record"
                            % (AUDIT, key))
        if status == "written" and bco.get("concept") not in written:
            findings.append("%s: %s is marked written, but its concept is not "
                            "a written class" % (AUDIT, key))
        if status != "written" and "class" in bco:
            findings.append("%s: %s names a class without being written"
                            % (AUDIT, key))
        if set(r.get("bpo") or {}) & {"accepted", "concept", "staging_status"}:
            findings.append("%s: %s mixes the BCO's acceptance into BPO's "
                            "declaration" % (AUDIT, key))
    return findings


def check_migration(data: dict | None = None,
                    text: str | None = None) -> list[str]:
    import rdflib
    findings = []
    if data is None:
        data = load_yaml(MIGRATION)
    if text is None:
        text = (layout.repository_root() / MIGRATION).read_bytes().decode()
    rows = data.get("classes") or []
    declared = {str(s) for s in module_graph().subjects(rdflib.RDF.type,
                                                        rdflib.OWL.Class)}
    old = sorted(r.get("old_iri") for r in rows)
    if old != draft_classes():
        findings.append("%s: the rows are not exactly the v0.1 classes"
                        % MIGRATION)
    for r in rows:
        mig = r.get("identifier_migration") or {}
        sem = r.get("semantic_relation") or {}
        if mig.get("kind") not in ("rename", "split", "not-carried"):
            findings.append("%s: %s has no identifier migration kind"
                            % (MIGRATION, r.get("old_iri")))
        targets = mig.get("to") or []
        if mig.get("kind") == "not-carried" and targets:
            findings.append("%s: %s is not carried but names a target"
                            % (MIGRATION, r.get("old_iri")))
        if mig.get("kind") in ("rename", "split") and not targets:
            findings.append("%s: %s names no target" % (MIGRATION,
                                                       r.get("old_iri")))
        for target in targets:
            if target not in declared:
                findings.append("%s: %s is not a class written in a module"
                                % (MIGRATION, target))
        if sem.get("equivalence_asserted") is not False:
            findings.append("%s: %s must state equivalence_asserted: false"
                            % (MIGRATION, r.get("old_iri")))
        if not sem.get("relation") or not r.get("decision") \
                or "definition_change" not in r:
            findings.append("%s: %s lacks its semantic relation, decision or "
                            "definition change" % (MIGRATION, r.get("old_iri")))
    for banned in ("owl:sameAs", "owl:equivalentClass"):
        if banned in text.replace("no " + banned, ""):
            findings.append("%s mentions %s outside a negation"
                            % (MIGRATION, banned))
    return findings


# ------------------------------------------------------------------- main

def render_yaml(data) -> bytes:
    import yaml
    head = ("# GENERATED by tools/kg/register.py --write. Do not edit: the "
            "check requires\n# this file to be the generator's rendering of "
            "its reviewed inputs.\n")
    return (head + yaml.safe_dump(data, sort_keys=False, allow_unicode=True,
                                  width=88)).encode("utf-8")


def render_json(data) -> bytes:
    return (json.dumps(data, indent=2, ensure_ascii=False) + "\n").encode()


def check_schema(data) -> list[str]:
    import jsonschema
    schema = json.loads((layout.repository_root() / SCHEMA).read_bytes())
    jsonschema.Draft202012Validator.check_schema(schema)
    validator = jsonschema.Draft202012Validator(
        schema, format_checker=jsonschema.FormatChecker())
    return ["%s: %s at %s" % (REGISTER, e.message, "/".join(map(str, e.path)))
            for e in validator.iter_errors(data)]


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--write", action="store_true",
                    help="regenerate the audit and the register")
    args = ap.parse_args(argv)
    root = layout.repository_root()
    built = {AUDIT: render_yaml(audit()), REGISTER: render_json(register())}
    findings = []
    for rel, data in built.items():
        path = root / rel
        if args.write:
            path.write_bytes(data)
            print("  wrote %s" % rel)
        elif not path.is_file() or path.read_bytes() != data:
            findings.append("%s is not what tools/kg/register.py writes "
                            "(run --write)" % rel)
    reg = json.loads(built[REGISTER])
    findings += check_schema(reg)
    findings += check_register(reg)
    findings += check_audit(load_yaml(AUDIT))
    findings += check_migration()
    summary = load_yaml(AUDIT)["summary"]
    print("  scope audit: %(entries)d entries; BCO written %(bco_written)d, "
          "concept not admitted %(bco_concept_not_admitted)d, none "
          "%(bco_none)d" % summary)
    print("  coverage register batch 1: %d function(s), %d waiting"
          % (len(reg["functions"]), len(reg["waiting"])))
    print("  bc: migration manifest: %d class(es)"
          % len(load_yaml(MIGRATION).get("classes") or []))
    for f in findings:
        print("  FINDING: " + f)
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
