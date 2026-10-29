# SPDX-License-Identifier: MIT
"""The Capability Term Inventory's check refuses what it says it refuses.

tools/inventory/harvest_bpo.py has two halves: a harvest that needs the
network, and an offline check that runs everywhere. The check is tested
against the committed outputs, and then against copies in tmp_path broken
one rule at a time -- each mutation asserted to have changed something
before the check runs, each failure required to be the finding for that
rule (docs/process/PROCESS.md section 2). The harvest's own rules (what is
a capability class, what is withheld, Q-12, Q-13) and E7's release of the
withheld text are tested on a small synthetic BPO built here in memory, so
they run without the network; the real harvest is held to its pins by
--confirm in the weekly CI job.

No tracked fixture: every broken case is built at run time, because a
`test-fixture` component is loaded as Turtle by the validation ladder.
"""

from __future__ import annotations

import hashlib
import json
import re

import pytest
import yaml

from conftest import ROOT, load_tool

TOOL = "tools/inventory/harvest_bpo.py"
DIRECTORY = "docs/sources/inventory"
ENTRIES = DIRECTORY + "/bpo-entries.yaml"
FINDINGS = DIRECTORY + "/bpo-findings.yaml"
NOTICE = DIRECTORY + "/NOTICE.md"
RECORD = DIRECTORY + "/e7-release.md"
APPROVAL = "docs/decisions/2026-10-27-inventory-i1-approved.md"
RELEASED = "apqc-pcf-7.4"
WITHHELD = "apqc-terms-unverified"
RELEASE_COMMIT = "2e55edd9e86a0bc20fa88a21595cc61402faa5dc"
COPIED = ("config/inventory-sources.yaml", "config/upstream-sources.yaml",
          "config/inventory-pcf-sources.yaml",
          "tools/ontology/validate.py", ENTRIES, FINDINGS, NOTICE,
          DIRECTORY + "/README.md",
          "docs/decisions/2026-10-28-i2-and-bpo-repin-decided.md")


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
    assert 0 < counts["released"] < counts["entries"]


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


def test_every_withholding_is_released_with_the_notice(harvest):
    """E7 over the real data, read directly rather than through the
    tool's own check: nothing is still withheld, every released
    declaration carries text read at the release commit, and the file
    carries APQC's notice as pinned."""
    document = load(ROOT, ENTRIES)
    text = (ROOT / ENTRIES).read_bytes().decode("utf-8")
    assert WITHHELD + "}" not in text and "withheld: " + WITHHELD not in text
    released = [e for e in document["entries"]
                if e["rights_status"] == RELEASED]
    assert released and all(e["apqc_evidence"] or e["pcf_code"]
                            for e in released)
    for entry in released:
        for d in entry.get("declarations", []):
            assert isinstance(d["label"], list) and d["label"], entry["id"]
            assert isinstance(d["definition"], list), entry["id"]
            assert d["text_from"].startswith(
                "https://github.com/Skreen5hot/BusinessProcessOntology/blob/"
                + RELEASE_COMMIT + "/" + d["module"] + "#L"), entry["id"]
    pins = load(ROOT, "config/inventory-pcf-sources.yaml")["sources"][0]
    assert hashlib.sha256(document["apqc_notice"].encode("utf-8")) \
        .hexdigest() == pins["apqc_notice_sha256"]
    assert document["release"]["commit"] == pins["commit"] == RELEASE_COMMIT


def test_only_released_entries_name_a_release_line(harvest):
    """E7 adds a field only to what I-1 withheld, and keeps I-1's counts.
    (That every other entry is byte-identical to the approved file was
    measured when E7 was prepared and is recorded in e7-release.md; the
    approved file is in git, at ba8df1a, not in the tree.)"""
    document = load(ROOT, ENTRIES)
    for entry in document["entries"]:
        if entry["rights_status"] == "bpo-mit":
            for d in entry.get("declarations", []):
                assert "text_from" not in d, entry["id"]
    assert document["counts"]["entries"] == 186
    assert document["counts"]["released"] == 59


# --------------------------------------------- E7: traceability of I-1


def record_rows():
    """{path: (approved digest, digest at E7)} from e7-release.md."""
    rows = {}
    text = (ROOT / RECORD).read_bytes().decode("utf-8")
    for match in re.finditer(r"(?m)^\| `([^`]+)` \| `([0-9a-f]{64})` \| "
                             r"`([0-9a-f]{64})` \| (changed|unchanged)",
                             text):
        rows[match.group(1)] = (match.group(2), match.group(3),
                                match.group(4))
    return rows


def test_the_record_cites_every_digest_the_approval_recorded():
    """The approval is the architect's and is never edited; the record
    must carry each digest it recorded, so the approved versions stay
    findable (git show ba8df1a:<path>)."""
    approval = (ROOT / APPROVAL).read_bytes().decode("utf-8")
    recorded = dict(re.findall(r"(?m)^\| `([^`]+)` \| `([0-9a-f]{64})` \|$",
                               approval))
    assert len(recorded) == 6
    rows = record_rows()
    assert set(rows) == set(recorded)
    for path, digest in recorded.items():
        assert rows[path][0] == digest, path


def test_the_record_pins_the_i1_outputs_as_they_now_are():
    """The I-1 outputs and pins, held to the record: an output changed
    after E7 without a new record is refused here. Those E7 did not
    change are still the approved bytes."""
    rows = record_rows()
    for path in (ENTRIES, FINDINGS, NOTICE, "config/inventory-sources.yaml"):
        approved, now, state = rows[path]
        digest = hashlib.sha256((ROOT / path).read_bytes()).hexdigest()
        assert digest == now, path
        assert (state == "unchanged") == (approved == now), path
    assert rows[FINDINGS][2] == "unchanged"
    assert rows["config/inventory-sources.yaml"][2] == "unchanged"
    assert rows[ENTRIES][2] == rows[NOTICE][2] == "changed"


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


BASELINE = "66131945b525c54f44e4962f32bb1f52dfa0cd12"
SELECTED = "bc64e91839378e1926189c01bf184d6a22d5c1b7"


def test_the_reviewed_baseline_needs_the_architects_record(harvest, copy):
    """After the re-pin the vendored pin is the inventory's own commit and
    the baseline is I-1's historical one. That is accepted only because
    R5's record names the baseline by full commit: without it, a moved
    pin and a kept baseline would look like a re-pin nobody reviewed."""
    harvest.check(copy)
    record = copy / harvest.REVIEWED_BASELINE_RECORD
    text = record.read_bytes().decode("utf-8")
    assert BASELINE in text
    record.write_bytes(text.replace(BASELINE, "b" * 40).encode("utf-8"))
    with pytest.raises(harvest.Refused,
                       match="re-pinned without the inventory"):
        harvest.check(copy)


def test_the_pre_repin_state_still_holds_the_old_rule(harvest, copy):
    """Positive control for the other branch: with the extract vendored at
    the baseline (as at I-1's review), the baseline must be its commit,
    namespace and bytes, and is accepted as such."""
    path = copy / "config/upstream-sources.yaml"
    text = path.read_bytes().decode("utf-8")
    old = load(copy, "config/inventory-sources.yaml")["sources"][0][
        "baseline"]
    text = (text.replace(SELECTED, BASELINE)
            .replace("namespace: https://fandaws.com/ontology/bpo#",
                     "namespace: " + old["namespace"])
            .replace("a8119728796872a1814aace8130a32cc8e42961b0bd5feaa28b736"
                     "d60a0cc6fd",
                     "1b9a9375cb7303003556004effd712b63913d6aa4935dbf604a653"
                     "aec65cab4b"))
    path.write_bytes(text.encode("utf-8"))
    harvest.check(copy)
    path.write_bytes(text.replace("namespace: " + old["namespace"],
                                  "namespace: http://example.org/x#")
                     .encode("utf-8"))
    with pytest.raises(harvest.Refused, match="not the vendored pin's"):
        harvest.check(copy)


def test_a_baseline_other_than_the_vendored_pin_is_refused(harvest, copy):
    path = copy / "config/upstream-sources.yaml"
    text = path.read_bytes().decode("utf-8")
    assert text.count(SELECTED) >= 2
    path.write_bytes(text.replace(SELECTED, "a" * 40).encode("utf-8"))
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
    data["counts"]["released"] -= 1
    rewrite(copy, ENTRIES, data)
    assert any("states counts" in p for p in findings(harvest, copy))


# ------------------------------------------------------------ rights rule


def test_an_entry_still_withheld_is_refused(harvest, copy):
    """The rule's output without E7's release is no longer what the tool
    writes."""
    data = load(copy, ENTRIES)
    entry = first(data["entries"], "capability-class", RELEASED)
    entry["rights_status"] = WITHHELD
    for d in entry["declarations"]:
        d["label"] = d["definition"] = {"withheld": WITHHELD}
        del d["text_from"]
    rewrite(copy, ENTRIES, data)
    problems = findings(harvest, copy)
    assert any("is still withheld (apqc-terms-unverified); E7 released "
               "every withheld entry" in p for p in problems), problems
    assert any("label is still withheld" in p for p in problems)


def test_a_withheld_field_on_a_released_entry_is_refused(harvest, copy):
    data = load(copy, ENTRIES)
    entry = first(data["entries"], "capability-class", RELEASED)
    entry["declarations"][0]["definition"] = {"withheld": WITHHELD}
    rewrite(copy, ENTRIES, data)
    problems = findings(harvest, copy)
    assert any("declaration 0 definition is still withheld" in p
               for p in problems), problems
    assert any("carries no label or definition list" in p for p in problems)


def test_released_text_without_its_source_line_is_refused(harvest, copy):
    data = load(copy, ENTRIES)
    entry = first(data["entries"], "capability-class", RELEASED)
    declaration = entry["declarations"][0]
    declaration["text_from"] = declaration["locator"]
    rewrite(copy, ENTRIES, data)
    assert any("is not a line of" in p and "at the release commit" in p
               for p in findings(harvest, copy))


def test_text_from_on_bpo_text_is_refused(harvest, copy):
    data = load(copy, ENTRIES)
    entry = first(data["entries"], "capability-class", "bpo-mit")
    entry["declarations"][0]["text_from"] = "https://example.org/x"
    rewrite(copy, ENTRIES, data)
    assert any("names text_from but is not released text" in p
               for p in findings(harvest, copy))


def test_apqc_evidence_on_a_bpo_mit_entry_is_refused(harvest, copy):
    """Recording PCF text as BPO's MIT text, with the evidence still on
    it, would drop APQC's notice from text that needs it."""
    data = load(copy, ENTRIES)
    entry = first(data["entries"], "capability-class", RELEASED)
    entry["rights_status"] = "bpo-mit"
    rewrite(copy, ENTRIES, data)
    assert any("not BPO's MIT text" in p for p in findings(harvest, copy))


def test_a_release_with_no_evidence_is_refused(harvest, copy):
    data = load(copy, ENTRIES)
    entry = first(data["entries"], "capability-class", "bpo-mit")
    entry["rights_status"] = RELEASED
    rewrite(copy, ENTRIES, data)
    assert any("released as PCF material with no APQC evidence" in p
               for p in findings(harvest, copy))


def test_an_altered_or_missing_apqc_notice_is_refused(harvest, copy):
    data = load(copy, ENTRIES)
    data["apqc_notice"] = data["apqc_notice"].replace("APQC", "ACME", 1)
    rewrite(copy, ENTRIES, data)
    assert any("not APQC's notice as" in p for p in findings(harvest, copy))
    del data["apqc_notice"]
    rewrite(copy, ENTRIES, data)
    assert any("carries no apqc_notice" in p for p in findings(harvest, copy))


def test_a_release_other_than_the_pins_is_refused(harvest, copy):
    data = load(copy, ENTRIES)
    data["release"]["inputs"][1]["sha256"] = "0" * 64
    rewrite(copy, ENTRIES, data)
    assert any("records a release that is not what" in p
               for p in findings(harvest, copy))


def test_a_release_pin_changed_without_a_rebuild_is_refused(harvest, copy):
    path = copy / "config/inventory-pcf-sources.yaml"
    text = path.read_bytes().decode("utf-8")
    old = "04267a0766f7a8ea43735143471a2d019f40a67a3f539b5f7725cb3589fac2fc"
    assert old in text
    path.write_bytes(text.replace(old, "2" * 64).encode("utf-8"))
    problems = findings(harvest, copy)
    assert any("records a release that is not what" in p for p in problems)
    assert any("NOTICE.md is not what" in p for p in problems)


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


# ------------------------------------------ E7's release, synthetic

NOTICE_TEXT = "(c) Example. A notice that must travel with the text."
RP = {"repository": SOURCE["repository"], "commit": "d" * 40,
      "rights_status": RELEASED, "notice": {"path": "NOTICE.md"}}


def release_module(slice_text=SLICE, notice=NOTICE_TEXT):
    """The synthetic slice as BPO would serve it at the release commit:
    the same declarations, with APQC's notice on the ontology header."""
    header = ('<https://fandaws.com/ontology/bpo/slice/1.0> a owl:Ontology ;\n'
              '    <http://purl.org/dc/terms/rights> """Framing.\n\n%s""" ;\n'
              % notice)
    text = slice_text.replace(
        "<https://fandaws.com/ontology/bpo/slice/1.0> a owl:Ontology ;\n",
        header)
    assert text != slice_text
    return text.encode()


def released(harvest, module=None, h=None):
    h = h or synthetic(harvest)
    entries = harvest.class_entries(h, SOURCE)
    module = release_module() if module is None else module
    return {e["iri"][len(NS):]: e for e in harvest.release(
        entries, h, SOURCE, RP, NOTICE_TEXT,
        {"ontology/slices/a.ttl": module})}


def test_the_release_fills_withheld_text_and_leaves_the_rest(harvest):
    h = synthetic(harvest)
    before = {e["iri"][len(NS):]: e
              for e in harvest.class_entries(h, SOURCE)}
    entries = released(harvest, h=h)
    assert entries["CapA"] == before["CapA"]
    for name in ("P10001", "CapB", "CapC"):
        entry = entries[name]
        assert entry["rights_status"] == RELEASED
        assert entry["apqc_evidence"] == before[name]["apqc_evidence"]
        (d,) = entry["declarations"]
        assert d["label"] == h.declarations(NS + name)[0]["label"]
        assert d["definition"] == h.declarations(NS + name)[0]["definition"]
        assert d["text_from"].startswith(
            SOURCE["repository"] + "/blob/" + "d" * 40
            + "/ontology/slices/a.ttl#L")
    # The line is the release module's, not the harvest's: the header
    # grew by the lines of its dct:rights.
    grew = release_module().count(b"\n") - SLICE.count("\n")
    assert grew > 0
    assert entries["CapB"]["declarations"][0]["text_from"].endswith(
        "#L%d" % (before["CapB"]["declarations"][0]["line"] + grew))


def test_the_release_refuses_text_that_changed(harvest):
    """Falsifies the equality rule: one word of one withheld definition
    changed at the release commit, and nothing is released."""
    module = release_module(SLICE.replace('"Annotated."', '"Annotated anew."'))
    with pytest.raises(harvest.Refused,
                       match=r"1 declaration\(s\) differ: "
                             r"INV-BPO-CapC-capability-class"):
        released(harvest, module)
    # Positive control: the same module unchanged is released.
    assert released(harvest)["CapC"]["rights_status"] == RELEASED


def test_the_release_refuses_a_module_without_the_notice(harvest):
    module = release_module(notice="Some other words.")
    with pytest.raises(harvest.Refused, match="carries the notice"):
        released(harvest, module)


def test_the_release_refuses_an_unpinned_module(harvest):
    h = synthetic(harvest)
    entries = harvest.class_entries(h, SOURCE)
    with pytest.raises(harvest.Refused, match="does not pin for the release"):
        harvest.release(entries, h, SOURCE, RP, NOTICE_TEXT, {})


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
