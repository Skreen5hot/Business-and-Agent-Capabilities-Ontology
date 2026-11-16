"""Stage 06, the register-first increment (docs/standards/stage-06-knowledge-graph.md;
decision of 2026-11-16): the CP-3 scope audit (S06-A1), the coverage register
(S06-R1 to S06-R3), the bc: migration manifest (S06-MG), the S06-U2 record,
and the separation of production from test data (K2, S06-E3).

Every rule has its positive case, the committed data, and a negative case: a
broken copy built to fail for that rule alone.
"""

from __future__ import annotations

import copy
import hashlib
import json

import pytest
import yaml

from conftest import load_tool

BCO = "https://fandaws.com/ontology/bco#"
BPO = "https://fandaws.com/ontology/bpo#"
STAGE06 = "src/06_knowledge_graph"


@pytest.fixture(scope="module")
def tool():
    return load_tool("bco_kg_register", "tools/kg/register.py")


@pytest.fixture(scope="module")
def register(repo):
    return json.loads((repo / STAGE06 / "coverage-register.json")
                      .read_bytes().decode("utf-8"))


@pytest.fixture(scope="module")
def audit(repo):
    return yaml.safe_load((repo / STAGE06 / "scope-audit.yaml")
                          .read_bytes().decode("utf-8"))


@pytest.fixture(scope="module")
def migration(repo):
    return yaml.safe_load((repo / STAGE06 / "bc-migration.yaml")
                          .read_bytes().decode("utf-8"))


# ----------------------------------------------------------- generation

def test_the_audit_and_register_are_the_generators_output(tool, repo):
    assert (repo / tool.AUDIT).read_bytes() == tool.render_yaml(tool.audit())
    assert (repo / tool.REGISTER).read_bytes() == \
        tool.render_json(tool.register())


def test_the_check_passes_on_the_committed_data(tool):
    assert tool.main([]) == 0


# ----------------------------------------------------------- S06-R1, schema

def test_the_schema_accepts_the_register(tool, register):
    assert tool.check_schema(register) == []


@pytest.mark.parametrize("name, break_it", [
    ("an act type as a component",
     lambda r: r["functions"][0]["components"][0].update(
         {"class": BPO + "P10736"})),
    ("an APQC process node as a component",
     lambda r: r["functions"][0]["components"][0].update(
         {"class": BPO + "PCF_10736"})),
    ("an individual as a component",
     lambda r: r["functions"][0]["components"][0].update(
         {"class": BCO + "fixture_cq_org"})),
    ("an unknown field", lambda r: r.update({"hierarchy_id": "9.9"})),
    ("a missing version", lambda r: r.pop("version")),
    ("a key that is not a catalog node",
     lambda r: r["functions"][0].update({"key": BCO + "TaxManagement"})),
    ("a PCF name on a function",
     lambda r: r["functions"][0].update({"name": "a catalog name"})),
])
def test_the_schema_refuses(tool, register, name, break_it):
    broken = copy.deepcopy(register)
    break_it(broken)
    assert tool.check_schema(broken), name


# --------------------------------------------------- S06-R2, CAP-22 and K8

def test_the_register_keeps_cap22_and_k8(tool, register):
    assert tool.check_register(register) == []


def test_a_batch_1_function_has_written_components_and_a_pinned_key(
        tool, register):
    assert register["functions"], "batch 1 is empty"
    nodes, _ = tool.pcf_inventory()
    k1 = tool.k1_classes(tool.module_graph())
    for f in register["functions"]:
        assert nodes[f["pcf_element_id"]] == f["key"]
        assert {c["class"] for c in f["components"]} <= k1
        assert f["whole_function_class"] not in {
            c["class"] for c in f["components"]}


@pytest.mark.parametrize("name, break_it, expect", [
    ("whole-function class among its components",
     lambda f: f["components"].append(
         dict(f["components"][0], **{"class": f["whole_function_class"]})),
     "CAP-22"),
    ("a component that is not written",
     lambda f: f["components"][0].update({"class": BCO + "TreasuryManagement"}),
     "not a written capability class"),
    ("the parent as a component",
     lambda f: f["components"][0].update({"class": BCO + "BusinessCapability"}),
     "not a written capability class"),
    ("a key for another element",
     lambda f: f.update({"key": BPO + "PCF_17058"}),
     "is not the catalog node"),
    ("a withheld rights status committed",
     lambda f: f["rights"].update({"status": "withheld"}),
     "no established rights basis"),
])
def test_the_register_check_refuses(tool, register, name, break_it, expect):
    broken = copy.deepcopy(register)
    target = next(f for f in broken["functions"]
                  if f["whole_function_class"]) if "whole" in name \
        else broken["functions"][0]
    break_it(target)
    findings = tool.check_register(broken)
    assert any(expect in f for f in findings), (name, findings)


def test_the_register_refuses_a_changed_notice(tool, register):
    broken = dict(register, apqc_notice=register["apqc_notice"] + " ")
    assert any("apqc_notice" in f for f in tool.check_register(broken))


def test_no_pcf_name_description_or_hierarchy_id_enters_the_register(
        repo, register):
    entries = yaml.safe_load((repo / "docs/sources/inventory/pcf-7.4-entries.yaml")
                             .read_bytes().decode("utf-8"))["entries"]
    by_id = {e["pcf_element_id"]: e for e in entries}
    text = json.dumps({k: v for k, v in register.items()
                       if k != "apqc_notice"})
    for f in register["functions"]:
        element = by_id[f["pcf_element_id"]]
        assert element["name"] not in text
        assert element["pcf_hierarchy_id"] not in text.replace(
            f["pcf_element_id"], "")
        assert element["description"][:40] not in text


def test_waiting_groupings_each_give_a_reason(register):
    for w in register["waiting"]:
        assert w["reasons"]
    listed = {f["grouping"] for f in register["functions"]}
    assert not listed & {w["grouping"] for w in register["waiting"]}


# ------------------------------------------------------ S06-R3, Gate G

def test_the_register_generates_nothing_into_the_ontology(tool, repo):
    """Running the register tool writes no triple: every module, and the
    corpus digest, is unchanged by it."""
    paths = [c.resolve() for c in tool.layout.components("ontology-module")]
    before = {p: hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
    tool.register()
    tool.audit()
    after = {p: hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
    assert before == after
    for path in (repo / STAGE06).iterdir():
        assert path.suffix not in (".ttl", ".owl", ".rdf", ".nt", ".trig"), path


# ----------------------------------------------------------- S06-A1, K10

def test_the_audit_covers_the_41_scope_entries(tool, audit):
    assert audit["summary"]["entries"] == len(audit["entries"]) == 41
    assert tool.check_audit(audit) == []


def test_the_audit_admits_nothing(audit):
    for row in audit["entries"]:
        assert row["bco"]["accepted"] != "written" or row["bco"].get("g1t")
        assert "subclass" not in json.dumps(row).lower().replace(
            "asserts no subclass", "")


@pytest.mark.parametrize("name, break_it, expect", [
    ("a missing entry", lambda a: a["entries"].pop(),
     "not exactly the"),
    ("an acceptance with no record",
     lambda a: next(r for r in a["entries"]
                    if r["bco"]["accepted"] == "concept-not-admitted")["bco"]
     .pop("accepted_by"), "no record"),
    ("a status outside the closed list",
     lambda a: a["entries"][0]["bco"].update({"accepted": "admitted"}),
     "closed-list"),
    ("a type marked written that is not",
     lambda a: next(r for r in a["entries"]
                    if r["bco"]["accepted"] == "concept-not-admitted")["bco"]
     .update({"accepted": "written",
              "staging_status": "admitted and written: a G1-T PASS and a "
                                "Stage 05 class"}), "not a written class"),
    ("BCO acceptance mixed into BPO's declaration",
     lambda a: a["entries"][0]["bpo"].update({"accepted": "written"}),
     "mixes"),
])
def test_the_audit_check_refuses(tool, audit, name, break_it, expect):
    broken = copy.deepcopy(audit)
    break_it(broken)
    findings = tool.check_audit(broken)
    assert any(expect in f for f in findings), (name, findings)


# ---------------------------------------------------------- S06-MG, K10

def test_the_migration_manifest_keeps_its_rules(tool, migration):
    assert tool.check_migration() == []
    assert len(migration["classes"]) == 7
    for row in migration["classes"]:
        assert row["semantic_relation"]["equivalence_asserted"] is False


@pytest.mark.parametrize("name, break_it, expect", [
    ("an asserted equivalence",
     lambda m: m["classes"][0]["semantic_relation"].update(
         {"equivalence_asserted": True}), "equivalence_asserted"),
    ("a target that is not written",
     lambda m: m["classes"][0]["identifier_migration"].update(
         {"to": [BCO + "BusinessCapabilityDescription"]}),
     "not a class written"),
    ("a missing v0.1 class", lambda m: m["classes"].pop(),
     "not exactly the v0.1"),
    ("a not-carried row naming a target",
     lambda m: next(r for r in m["classes"]
                    if r["identifier_migration"]["kind"] == "not-carried")
     ["identifier_migration"].update({"to": [BCO + "BusinessCapability"]}),
     "not carried but names"),
    ("no semantic relation",
     lambda m: m["classes"][0]["semantic_relation"].pop("relation"),
     "lacks its semantic relation"),
])
def test_the_migration_check_refuses(tool, migration, name, break_it, expect):
    broken = copy.deepcopy(migration)
    break_it(broken)
    findings = tool.check_migration(broken, "")
    assert any(expect in f for f in findings), (name, findings)


def test_the_migration_check_refuses_an_owl_equivalence_in_the_text(
        tool, migration):
    findings = tool.check_migration(
        migration, "old owl:sameAs new")
    assert any("owl:sameAs" in f for f in findings)


# ------------------------------------------------------------ S06-U2 record

def test_the_upstream_record_names_the_complete_closure(repo, tool):
    record = json.loads((repo / STAGE06 / "upstream-conformance.json")
                        .read_bytes().decode("utf-8"))
    pins = {s["id"]: s for s in yaml.safe_load(
        (repo / "config/upstream-sources.yaml").read_bytes()
        .decode("utf-8"))["sources"]}
    roles = {item["role"]: item for item in record["closure"]}
    assert roles["complete BFO at its pin"]["sha256"] == pins["bfo"]["sha256"]
    assert roles["complete CCO (merged) at its pin"]["sha256"] == \
        pins["cco"]["sha256"]
    modules = {item["path"]: item["sha256"] for item in record["closure"]
               if item["role"] == "BCO module"}
    for path, digest in modules.items():
        assert hashlib.sha256((repo / path).read_bytes()).hexdigest() == \
            digest, "%s changed since S06-U2 ran: rerun it" % path
    assert len(modules) == len(tool.layout.components("ontology-module"))
    assert "not claimed" in record["not_claimed"]
    results = {r["reasoner"]: r for r in record["results"]}
    assert set(results) == {"ELK", "HermiT"}
    for r in results.values():
        assert r["result"] == "PASS" and r["real_input"] == "PASS"
        assert all(v in ("rejected", "detected") for v in r["cases"].values())
    assert results["HermiT"]["cases"]["inconsistent"] == "rejected"


# ----------------------------------------------------- K2, S06-E3 (part)

def test_no_fixture_iri_in_production_data_and_no_instance_data(repo):
    for path in sorted((repo / STAGE06).iterdir()):
        text = path.read_bytes().decode("utf-8")
        assert "fixture_" not in text, path
    register_text = (repo / STAGE06 / "coverage-register.json").read_bytes()
    assert b"NamedIndividual" not in register_text
