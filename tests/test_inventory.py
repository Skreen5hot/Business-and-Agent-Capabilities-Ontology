# SPDX-License-Identifier: MIT
"""The Capability Term Inventory's check refuses what it says it refuses.

tools/inventory/harvest_bpo.py has two halves: a harvest that needs the
network, and an offline check that runs everywhere. The check is tested
against the committed outputs, and then against copies in tmp_path broken
one rule at a time -- each mutation asserted to have changed something
before the check runs, each failure required to be the finding for that
rule (docs/process/PROCESS.md section 2). The harvest's own rules (what is
a capability class, what is withheld, Q-12, Q-13) are tested on a small
synthetic BPO built here in memory, so they run without the network; the
real harvest is held to its pins by --confirm in the weekly CI job.

No tracked fixture: every broken case is built at run time, because a
`test-fixture` component is loaded as Turtle by the validation ladder.
"""

from __future__ import annotations

import json

import pytest
import yaml

from conftest import ROOT, load_tool

TOOL = "tools/inventory/harvest_bpo.py"
DIRECTORY = "docs/sources/inventory"
ENTRIES = DIRECTORY + "/bpo-entries.yaml"
FINDINGS = DIRECTORY + "/bpo-findings.yaml"
NOTICE = DIRECTORY + "/NOTICE.md"
COPIED = ("config/inventory-sources.yaml", "config/upstream-sources.yaml",
          "tools/ontology/validate.py", ENTRIES, FINDINGS, NOTICE,
          DIRECTORY + "/README.md")


@pytest.fixture(scope="module")
def harvest():
    return load_tool("bco_harvest_bpo", TOOL)


@pytest.fixture
def copy(tmp_path):
    """The check's inputs, copied byte for byte into tmp_path."""
    for relative in COPIED:
        target = tmp_path / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes((ROOT / relative).read_bytes())
    return tmp_path


def load(base, relative):
    loader = getattr(yaml, "CSafeLoader", yaml.SafeLoader)
    return yaml.load((base / relative).read_bytes().decode("utf-8"),
                     Loader=loader)


def rewrite(base, relative, data):
    """Write `data` back as YAML, and prove the bytes moved."""
    before = (base / relative).read_bytes()
    dumper = getattr(yaml, "CSafeDumper", yaml.SafeDumper)
    after = yaml.dump(data, Dumper=dumper, sort_keys=False,
                      allow_unicode=True).encode("utf-8")
    assert after != before
    (base / relative).write_bytes(after)


def findings(harvest, base):
    problems, _ = harvest.check(base)
    return problems


def first(entries, kind, rights=None):
    for entry in entries:
        if entry["kind"] == kind and (rights is None
                                      or entry["rights_status"] == rights):
            return entry
    raise AssertionError("no %s entry with rights %s" % (kind, rights))


# ------------------------------------------------------- the real outputs


def test_the_committed_outputs_pass(harvest):
    problems, counts = harvest.check(ROOT)
    assert problems == [], problems
    # Guard the guard: a check over an empty inventory would pass too.
    assert counts["capability-class"] > 0 and counts["scope-entry"] > 0
    assert 0 < counts["withheld"] < counts["entries"]


def test_the_copy_is_clean_before_anything_is_broken(harvest, copy):
    """Every negative test below starts from this state, so a finding in
    one of them is the mutation's and not the copy's."""
    assert findings(harvest, copy) == []


def test_the_findings_agree_with_the_entries(harvest):
    entries = load(ROOT, ENTRIES)["entries"]
    report = load(ROOT, FINDINGS)
    classes = [e for e in entries if e["kind"] == "capability-class"]
    assert report["selected"]["capability_classes"]["count"] == len(classes)
    q12 = report["selected"]["q12"]
    assert q12["count"] == len(q12["violations"])
    by_id = {e["id"]: e for e in entries}
    for row in q12["violations"]:
        listed = [t["target"] for t in by_id[row["entry"]]["enables_process"]]
        assert row["target"] in listed


def test_no_withheld_entry_carries_text(harvest):
    """The rights rule over the real data, read directly rather than
    through the tool's own check."""
    marker = {"withheld": "apqc-terms-unverified"}
    withheld = [e for e in load(ROOT, ENTRIES)["entries"]
                if e["rights_status"] == "apqc-terms-unverified"]
    assert withheld
    for entry in withheld:
        for d in entry.get("declarations", []):
            assert d["label"] == marker and d["definition"] == marker, \
                entry["id"]


def test_the_entries_are_dispositioned_as_third_party_text(disposition):
    rows = {r.path: r for r in disposition.classify()}
    row = rows[ENTRIES]
    assert row.disposition == disposition.VENDORED
    assert row.licence == "MIT"
    assert rows[FINDINGS].disposition == disposition.CONTENT
    assert disposition.attribution_findings(list(rows.values())) == []


def test_ci_runs_the_check_and_the_weekly_confirmation(repo):
    workflow = yaml.safe_load((repo / ".github/workflows/checks.yml")
                              .read_bytes().decode("utf-8"))
    jobs = workflow["jobs"]
    main_runs = [s.get("run", "").strip() for s in jobs["checks"]["steps"]]
    assert "python tools/inventory/harvest_bpo.py" in main_runs
    weekly = [s.get("run", "").strip() for s in jobs["vendored"]["steps"]]
    assert "python tools/inventory/harvest_bpo.py --confirm" in weekly


# ------------------------------------------------------ digests and pins


def test_outputs_built_from_other_bytes_are_refused(harvest, copy):
    data = load(copy, ENTRIES)
    data["source"]["inputs"][0]["sha256"] = "0" * 64
    rewrite(copy, ENTRIES, data)
    assert any("records input digests that are not the pins" in p
               for p in findings(harvest, copy))


def test_a_pin_changed_without_a_rebuild_is_refused(harvest, copy):
    path = copy / "config/inventory-sources.yaml"
    text = path.read_bytes().decode("utf-8")
    old = "593b438ab44d14445a92917b6fb357eaa2ef542845b0bf7ccc30ab3fa0888602"
    assert old in text
    path.write_bytes(text.replace(old, "1" * 64).encode("utf-8"))
    problems = findings(harvest, copy)
    assert any("records input digests that are not the pins" in p
               for p in problems)
    assert any("selected commit or input digests are not the pins" in p
               for p in problems)


def test_a_baseline_other_than_the_vendored_pin_is_refused(harvest, copy):
    path = copy / "config/upstream-sources.yaml"
    text = path.read_bytes().decode("utf-8")
    old = "66131945b525c54f44e4962f32bb1f52dfa0cd12"
    assert text.count(old) >= 2
    path.write_bytes(text.replace(old, "a" * 40).encode("utf-8"))
    with pytest.raises(harvest.Refused) as refused:
        harvest.check(copy)
    assert "Was the extract re-pinned without the inventory?" in str(
        refused.value)


def test_a_pin_on_another_host_is_refused(harvest, copy):
    path = copy / "config/inventory-sources.yaml"
    text = path.read_bytes().decode("utf-8")
    old = "raw_base: https://raw.githubusercontent.com/"
    assert old in text
    path.write_bytes(text.replace(old, "raw_base: https://example.com/")
                     .encode("utf-8"))
    with pytest.raises(harvest.Refused) as refused:
        harvest.check(copy)
    assert "Should the allowed host really grow?" in str(refused.value)


def test_fetch_refuses_another_host_or_an_unpinned_url(harvest, tmp_path):
    """Refused before any network use: neither URL is ever requested."""
    commit = "b" * 40
    with pytest.raises(harvest.Refused, match="not on"):
        harvest.fetch("https://example.com/%s/x" % commit, "0" * 64,
                      tmp_path / "x", commit)
    with pytest.raises(harvest.Refused, match="does not name the pinned"):
        harvest.fetch("https://raw.githubusercontent.com/o/r/main/x",
                      "0" * 64, tmp_path / "x", commit)


# ----------------------------------------------------------------- schema


def test_an_entry_missing_a_field_is_refused(harvest, copy):
    data = load(copy, ENTRIES)
    del data["entries"][0]["iri"]
    rewrite(copy, ENTRIES, data)
    assert any("has no 'iri' field" in p for p in findings(harvest, copy))


def test_an_unknown_kind_is_refused(harvest, copy):
    data = load(copy, ENTRIES)
    data["entries"][0]["kind"] = "standing-function-guess"
    rewrite(copy, ENTRIES, data)
    assert any("has kind 'standing-function-guess'" in p
               for p in findings(harvest, copy))


def test_an_id_not_derived_from_the_iri_is_refused(harvest, copy):
    data = load(copy, ENTRIES)
    entry = data["entries"][0]
    entry["id"] = entry["id"].replace("INV-BPO-", "INV-BPO-X")
    rewrite(copy, ENTRIES, data)
    problems = findings(harvest, copy)
    assert any("should be INV-BPO-" in p for p in problems), problems


def test_unsorted_entries_are_refused(harvest, copy):
    data = load(copy, ENTRIES)
    data["entries"].reverse()
    rewrite(copy, ENTRIES, data)
    assert any("is not sorted by id" in p for p in findings(harvest, copy))


def test_counts_that_disagree_with_the_entries_are_refused(harvest, copy):
    data = load(copy, FINDINGS)
    data["selected"]["capability_classes"]["count"] += 1
    rewrite(copy, FINDINGS, data)
    assert any("capability classes;" in p for p in findings(harvest, copy))
    data = load(copy, ENTRIES)
    data["counts"]["withheld"] -= 1
    rewrite(copy, ENTRIES, data)
    assert any("states counts" in p for p in findings(harvest, copy))


# ------------------------------------------------------------ rights rule


def test_a_withheld_entry_carrying_a_label_is_refused(harvest, copy):
    data = load(copy, ENTRIES)
    entry = first(data["entries"], "capability-class",
                  "apqc-terms-unverified")
    entry["declarations"][0]["label"] = [
        {"property": "rdfs:label", "text": "Some PCF wording"}]
    rewrite(copy, ENTRIES, data)
    assert any("is withheld (apqc-terms-unverified) but its declaration 0 "
               "label carries" in p for p in findings(harvest, copy))


def test_a_withheld_entry_carrying_a_definition_is_refused(harvest, copy):
    data = load(copy, ENTRIES)
    entry = first(data["entries"], "capability-class",
                  "apqc-terms-unverified")
    entry["declarations"][0]["definition"] = [
        {"property": "skos:definition", "text": "Some PCF wording"}]
    rewrite(copy, ENTRIES, data)
    assert any("declaration 0 definition carries" in p
               for p in findings(harvest, copy))


def test_apqc_evidence_on_an_unwithheld_entry_is_refused(harvest, copy):
    """Releasing an entry by flipping its status, with the evidence still
    on it, is exactly the act Phase I-2 has not authorized."""
    data = load(copy, ENTRIES)
    entry = first(data["entries"], "capability-class",
                  "apqc-terms-unverified")
    entry["rights_status"] = "bpo-mit"
    rewrite(copy, ENTRIES, data)
    assert any("Who verified APQC's terms?" in p
               for p in findings(harvest, copy))


def test_a_withholding_with_no_evidence_is_refused(harvest, copy):
    data = load(copy, ENTRIES)
    entry = first(data["entries"], "capability-class", "bpo-mit")
    entry["rights_status"] = "apqc-terms-unverified"
    rewrite(copy, ENTRIES, data)
    assert any("withheld with no APQC evidence recorded" in p
               for p in findings(harvest, copy))


def test_an_edited_notice_is_refused(harvest, copy):
    notice = copy / NOTICE
    notice.write_bytes(notice.read_bytes() + b"edited\n")
    assert any("NOTICE.md is not what" in p for p in findings(harvest, copy))


# ------------------------------------------------------- admission guard


def test_an_rdf_file_in_the_inventory_is_refused(harvest, copy):
    (copy / DIRECTORY / "bpo-classes.ttl").write_bytes(b"# nothing\n")
    assert any("bpo-classes.ttl is not YAML or Markdown" in p
               for p in findings(harvest, copy))


def test_rdf_inside_an_allowed_suffix_is_refused(harvest, copy):
    (copy / DIRECTORY / "classes.md").write_bytes(
        b"@prefix owl: <http://www.w3.org/2002/07/owl#> .\n")
    assert any("classes.md reads as an RDF serialization" in p
               for p in findings(harvest, copy))


def test_an_authored_namespace_iri_is_refused(harvest, copy, repo):
    validator = load_tool("bco_validate_for_inventory_test",
                          "tools/ontology/validate.py")
    for namespace in validator.AUTHORED_NAMESPACES:
        data = load(copy, ENTRIES)
        entry = first(data["entries"], "scope-entry", "bpo-mit")
        entry["enables_process"][0]["target"] = namespace + "Minted"
        rewrite(copy, ENTRIES, data)
        assert any("names %s, one of this repository's authored "
                   "namespaces" % namespace in p
                   for p in findings(harvest, copy)), namespace
        (copy / ENTRIES).write_bytes((repo / ENTRIES).read_bytes())


def test_the_guard_reads_the_validators_namespaces(harvest, copy):
    """Not a copy of the list: emptying it in the validator the check
    imports leaves the guard with nothing to refuse, and it says so."""
    path = copy / "tools/ontology/validate.py"
    text = path.read_bytes().decode("utf-8")
    start = text.index("AUTHORED_NAMESPACES = (")
    end = text.index(")", start) + 1
    path.write_bytes((text[:start] + "AUTHORED_NAMESPACES = ()"
                      + text[end:]).encode("utf-8"))
    with pytest.raises(harvest.Refused, match="lists no AUTHORED_NAMESPACES"):
        harvest.check(copy)


def test_a_ratification_key_is_refused(harvest, copy):
    data = load(copy, ENTRIES)
    data["entries"][0]["ratified_by"] = {"path": "docs/decisions/x.md"}
    rewrite(copy, ENTRIES, data)
    assert any("carries 'ratified_by'" in p for p in findings(harvest, copy))


# ----------------------------------------- the harvest, on a synthetic BPO

CCO = "https://www.commoncoreontologies.org/"
NS = "https://fandaws.com/ontology/bpo#"

MINI_CCO = """
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix cco: <https://www.commoncoreontologies.org/> .
cco:ont00001379 a owl:Class ; rdfs:label "Agent Capability"@en .
cco:ont00000568 a owl:Class ; rdfs:label "Organization Capability"@en ;
    rdfs:subClassOf cco:ont00001379 .
cco:ont00000228 a owl:Class ; rdfs:label "Planned Act"@en .
"""

PREFIXES = """@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix cco: <https://www.commoncoreontologies.org/> .
@prefix bpo: <https://fandaws.com/ontology/bpo#> .
"""

SLICE = PREFIXES + """
<https://fandaws.com/ontology/bpo/slice/1.0> a owl:Ontology ;
    owl:versionInfo "0.4.1" .
bpo:CapA a owl:Class ; rdfs:subClassOf cco:ont00000568 ;
    rdfs:label "Cap A" ; skos:definition "Defined in the slice." .
bpo:P10001 a owl:Class ; rdfs:subClassOf cco:ont00000568 ;
    rdfs:label "Manage things" ; skos:definition "A PCF-named capability." .
bpo:CapB a owl:Class ; rdfs:subClassOf bpo:CapA ;
    rdfs:label "Do stuff" ; skos:definition "Copied label." .
bpo:CapC a owl:Class ; rdfs:subClassOf cco:ont00000568 ;
    rdfs:label "Cap C" ; skos:definition "Annotated." ;
    bpo:hierarchyID "1.2" .
bpo:P10003 a owl:Class ; rdfs:subClassOf cco:ont00000228 ;
    rdfs:label "An act" .
bpo:Helper a owl:Class ; rdfs:subClassOf cco:ont00001379 .
bpo:PCF_10002 bpo:pcfID "10002" ; skos:prefLabel "Do stuff" ;
    bpo:designatesProcessType bpo:CapB .
"""

OTHER = PREFIXES + """
<https://fandaws.com/ontology/bpo/slice/2.0> a owl:Ontology ;
    owl:versionInfo "0.4.1" .
bpo:CapA a owl:Class ; rdfs:subClassOf cco:ont00000568 ;
    rdfs:label "Cap A" ; skos:definition "Defined differently here." .
"""

WIRING = PREFIXES + """
<https://fandaws.com/ontology/bpo/capabilities/wiring> a owl:Ontology .
bpo:CapA bpo:enablesProcess bpo:P10003 .
bpo:CapA bpo:enablesProcess bpo:P10001 .
"""

SCOPE = json.dumps({"_doc": "table", "bpo:CapA": ["bpo:P10003", "bpo:P10001"],
                    "bpo:Helper": ["bpo:P10003"]}, indent=2)

SOURCE = {
    "id": "bpo",
    "repository": "https://github.com/Skreen5hot/BusinessProcessOntology",
    "commit": "c" * 40,
    "entry_prefix": "INV-BPO",
    "apqc": {"withheld_marker": "apqc-terms-unverified"},
}


def synthetic(harvest, slice_text=SLICE):
    files = {"ontology/slices/a.ttl": slice_text.encode(),
             "ontology/slices/b.ttl": OTHER.encode(),
             "ontology/capabilities_wiring.ttl": WIRING.encode(),
             "capabilities/capability_scope.json": SCOPE.encode()}
    upstream = {"cco": MINI_CCO.encode(), "bfo": b""}
    return harvest.Harvest("c" * 40, NS, files,
                           "capabilities/capability_scope.json", upstream)


def test_capability_classes_are_the_closure_under_organization_capability(
        harvest):
    h = synthetic(harvest)
    assert h.capabilities == [NS + "CapA", NS + "CapB", NS + "CapC",
                              NS + "P10001"]
    assert h.agent_only == [NS + "Helper"]


def test_the_rights_rule_withholds_on_each_kind_of_evidence(harvest):
    h = synthetic(harvest)
    entries = {e["iri"][len(NS):]: e
               for e in harvest.class_entries(h, SOURCE)}
    marker = {"withheld": "apqc-terms-unverified"}
    assert entries["CapA"]["rights_status"] == "bpo-mit"
    assert entries["CapA"]["declarations"][0]["label"][0]["text"] == "Cap A"
    assert entries["P10001"]["apqc_evidence"] == [
        "iri-scheme: P10001 (BPO D7)"]
    assert entries["P10001"]["pcf_code"] == "10001"
    assert entries["CapC"]["apqc_evidence"] == ["annotation: bpo:hierarchyID"]
    assert entries["CapB"]["apqc_evidence"] == [
        "text-matches-pcf: ontology/slices/a.ttl rdfs:label of "
        + NS + "PCF_10002"]
    for name in ("P10001", "CapB", "CapC"):
        assert entries[name]["rights_status"] == "apqc-terms-unverified"
        for d in entries[name]["declarations"]:
            assert d["label"] == marker and d["definition"] == marker
    assert entries["CapB"]["designated_by"] == [
        {"node": NS + "PCF_10002", "pcf_code": "10002",
         "module": "ontology/slices/a.ttl"}]


def test_the_text_match_rule_discriminates(harvest):
    """Falsifies the third rule: the same class with a label that is not
    PCF text is not withheld."""
    changed = SLICE.replace('rdfs:label "Do stuff"', 'rdfs:label "Own words"')
    assert changed != SLICE
    entries = {e["iri"][len(NS):]: e
               for e in harvest.class_entries(synthetic(harvest, changed),
                                              SOURCE)}
    assert entries["CapB"]["rights_status"] == "bpo-mit"
    assert entries["CapB"]["apqc_evidence"] == []


def test_a_pcf_name_inside_a_definition_is_withheld(harvest):
    """The containment rule withholds a definition that reproduces a PCF
    name of two or more words, and only a whole run of words."""
    contained = SLICE.replace(
        'skos:definition "Copied label."',
        'skos:definition "A capacity to do, stuff and more."').replace(
        'rdfs:label "Do stuff"', 'rdfs:label "Own words"')
    entries = {e["iri"][len(NS):]: e
               for e in harvest.class_entries(synthetic(harvest, contained),
                                              SOURCE)}
    assert entries["CapB"]["apqc_evidence"] == [
        "text-contains-pcf: ontology/slices/a.ttl skos:definition contains "
        "the name of " + NS + "PCF_10002"]
    assert entries["CapB"]["rights_status"] == "apqc-terms-unverified"
    split = contained.replace("to do, stuff", "to do the stuff")
    entries = {e["iri"][len(NS):]: e
               for e in harvest.class_entries(synthetic(harvest, split),
                                              SOURCE)}
    assert entries["CapB"]["apqc_evidence"] == []


def test_text_withheld_on_one_class_is_withheld_on_another(harvest):
    """CapA's definition in module b equals P10001's withheld definition,
    so CapA is withheld too; changing one word falsifies it."""
    shared = OTHER.replace('"Defined differently here."',
                           '"A PCF-named capability."')

    def entries_with(other):
        h = harvest.Harvest(
            "c" * 40, NS,
            {"ontology/slices/a.ttl": SLICE.encode(),
             "ontology/slices/b.ttl": other,
             "ontology/capabilities_wiring.ttl": WIRING.encode(),
             "capabilities/capability_scope.json": SCOPE.encode()},
            "capabilities/capability_scope.json",
            {"cco": MINI_CCO.encode(), "bfo": b""})
        return {e["iri"][len(NS):]: e
                for e in harvest.class_entries(h, SOURCE)}

    entries = entries_with(shared.encode())
    assert entries["CapA"]["apqc_evidence"] == [
        "text-shared-with-withheld: ontology/slices/b.ttl skos:definition "
        "equals text of " + NS + "P10001"]
    assert entries["CapA"]["rights_status"] == "apqc-terms-unverified"
    entries = entries_with(OTHER.encode())
    assert entries["CapA"]["rights_status"] == "bpo-mit"


def test_declarations_are_kept_apart_and_q12_q13_are_counted(harvest):
    h = synthetic(harvest)
    entries = {e["iri"][len(NS):]: e
               for e in harvest.class_entries(h, SOURCE)}
    modules = [d["module"] for d in entries["CapA"]["declarations"]]
    assert modules == ["ontology/slices/a.ttl", "ontology/slices/b.ttl"]
    report = harvest.measure(h, "INV-BPO", None)
    assert report["enables_process"]["triples"] == 2
    assert report["q12"]["count"] == 1
    assert report["q12"]["violations"][0]["target"] == NS + "P10001"
    q13 = report["q13"]["capability_classes"]
    assert q13["declared_in_two_or_more_modules"] == 1
    assert q13["differing_definitions"] == 1
    assert q13["differing_superclasses"] == 0


def test_scope_entries_keep_order_and_are_not_merged(harvest):
    h = synthetic(harvest)
    scope = {e["iri"][len(NS):]: e for e in harvest.scope_entries(h, SOURCE)}
    assert [t["target"] for t in scope["CapA"]["enables_process"]] == [
        NS + "P10003", NS + "P10001"]
    assert [t["target_kind"] for t in scope["CapA"]["enables_process"]] == [
        "act", "capability"]
    assert scope["CapA"]["capability_class_entry"] == \
        "INV-BPO-CapA-capability-class"
    assert scope["Helper"]["capability_class_entry"] is None


def test_the_baseline_mapping_is_one_base_substitution(harvest):
    mapping = {"from": "http://example.org/apqc",
               "to": "https://fandaws.com/ontology/bpo"}
    assert harvest.remap("http://example.org/apqc#P10020", mapping) == \
        NS + "P10020"
    assert harvest.remap("http://example.org/apqc/scheme#PCF", mapping) == \
        "https://fandaws.com/ontology/bpo/scheme#PCF"
    assert harvest.remap("http://example.org/apqcX", mapping) == \
        "http://example.org/apqcX"
    assert harvest.remap(CCO + "ont00000568", mapping) == CCO + "ont00000568"
