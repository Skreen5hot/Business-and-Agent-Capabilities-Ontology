# SPDX-License-Identifier: MIT
"""Phase I-2b: the PCF 7.4 entries and NOTICE.md, from BPO's catalog.

Under the architect's decision of 2026-10-29
(docs/decisions/2026-10-29-apqc-pcf-sourcing-decided.md) the PCF 7.4 is
published from BPO's ontology/apqc-catalog.ttl at a pinned commit, with
APQC's notice copied from BPO's NOTICE.md. The reader, the notice
extraction and the checks are tested on SYNTHETIC catalogs: made-up
element ids (9xxxxx), hierarchy ids in categories 41 to 43, names such as
"Synthetic alpha". APQC's notice itself is never typed here: the tests
take it from the committed NOTICE.md by the tool's own extraction, and
its digest is the pin.

Refusals are tested by the words of their finding, one rule at a time,
with a positive control beside each (docs/process/PROCESS.md section 2).
"""

from __future__ import annotations

import subprocess

import pytest
import yaml

from conftest import ROOT, load_tool

TOOL = "tools/inventory/harvest_pcf.py"
ENTRIES = "docs/sources/inventory/pcf-7.4-entries.yaml"
BPO_ENTRIES = "docs/sources/inventory/bpo-entries.yaml"
PINS = "config/inventory-pcf-sources.yaml"
NS = "https://fandaws.com/ontology/bpo#"
FRAMING = "Synthetic framing sentence, standing in for BPO's."

#: (element id, hierarchy id, name, description, BPO level name)
NODES = [
    ("900001", "41.0", "Synthetic alpha", "Made-up text one", "Category"),
    ("900002", "41.3", "Synthetic beta", "Made-up text two", "ProcessGroup"),
    ("900003", "41.3.7", "Synthetic gamma", "Made-up text three", "Process"),
    ("900004", "41.3.7.2", "Synthetic delta", "Made-up text four",
     "Activity"),
    ("900005", "41.3.7.2.1", "Synthetic epsilon", None, "Task"),
    ("900006", "42.0", "Synthetic zeta", "Made-up text six", "Category"),
    ("900007", "42.10", "Synthetic eta", "Made-up text seven",
     "ProcessGroup"),
    ("900008", "42.2", "Synthetic theta", "Made-up text eight",
     "ProcessGroup"),
]


@pytest.fixture(scope="module")
def pcf():
    return load_tool("bco_inventory_harvest_pcf", TOOL)


@pytest.fixture(scope="module")
def notice(pcf):
    """APQC's notice, by the tool's extraction from the committed copy."""
    text = (ROOT / "NOTICE.md").read_bytes().decode("utf-8")
    return pcf.extract_notice(text)


@pytest.fixture(scope="module")
def source(pcf):
    return pcf.pins(ROOT)


def esc(text: str) -> str:
    return text.replace("\\", "\\\\").replace('"', '\\"')


def catalog(notice, nodes=NODES, rights=None, extra="", broader=None,
            iri=None) -> bytes:
    """A catalog in the shape of BPO's, built from `nodes`."""
    if rights is None:
        rights = ['%s\\n\\n%s' % (esc(FRAMING), esc(notice))]
    lines = [
        "@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .",
        "@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .",
        "@prefix owl: <http://www.w3.org/2002/07/owl#> .",
        "@prefix skos: <http://www.w3.org/2004/02/skos/core#> .",
        "@prefix dct: <http://purl.org/dc/terms/> .",
        "@prefix bpo: <%s> ." % NS,
        "@prefix apqc: <https://fandaws.com/ontology/bpo/scheme#> .",
        "",
        "<https://fandaws.com/ontology/bpo/scheme> a owl:Ontology%s ."
        % "".join(' ;\n    dct:rights "%s"' % r for r in rights),
        "",
    ]
    by_hid = {n[1]: n for n in nodes}
    for eid, hid, name, description, level in nodes:
        parts = hid.split(".")
        parent = None
        if not (len(parts) == 2 and parts[1] == "0"):
            parent = parts[0] + ".0" if len(parts) == 2 \
                else ".".join(parts[:-1])
        subject = (iri or {}).get(eid, "bpo:PCF_%s" % eid)
        body = [
            "%s a owl:NamedIndividual, skos:Concept ;" % subject,
            "    skos:inScheme apqc:PCF ;",
            '    skos:prefLabel "%s" ;' % esc(name),
            '    bpo:pcfID "%s" ;' % eid,
            '    bpo:hierarchyID "%s" ;' % hid,
            '    rdfs:comment "APQC level: %s"' % level,
        ]
        if description is not None:
            body[-1] += " ;"
            body.append('    bpo:apqcSourceText "%s"' % esc(description))
        target = (broader or {}).get(eid)
        if target is None and parent in by_hid:
            target = by_hid[parent][0]
        if target is not None:
            body[-1] += " ;"
            body.append("    skos:broader bpo:PCF_%s" % target)
        lines += body
        lines[-1] += " ."
        lines.append("")
    return ("\n".join(lines) + extra).encode("utf-8")


def bpo_notice_md(notice, width=90, section="APQC's notice") -> bytes:
    """A NOTICE.md in the shape of BPO's, the notice wrapped at `width`."""
    lines, line = [], ""
    for word in notice.split(" "):
        if line and len(line) + 1 + len(word) > width:
            lines.append(line)
            line = word
        else:
            line = (line + " " + word) if line else word
    lines.append(line)
    return ("# Notice\n\nPreamble.\n\n## %s\n\nThe notice below.\n\n%s\n\n"
            "## Also\n\n- Something else.\n"
            % (section, "\n".join("> " + x for x in lines))).encode("utf-8")


def refusal(call) -> str:
    with pytest.raises(SystemExit) as caught:
        call()
    return str(caught.value)


# ------------------------------------------------------------ the notice


def test_the_notice_is_unwrapped_from_bpos_blockquote(pcf, notice):
    for width in (60, 90, 200):
        text = bpo_notice_md(notice, width).decode("utf-8")
        assert pcf.extract_notice(text) == notice


def test_the_notice_matches_its_pinned_digest(pcf, notice, source):
    assert pcf.sha256(notice.encode("utf-8")) == source["apqc_notice_sha256"]


def test_a_notice_md_without_the_section_is_refused(pcf, notice):
    text = bpo_notice_md(notice, section="Their notice").decode("utf-8")
    assert "0 '## APQC's notice' heading" in refusal(
        lambda: pcf.extract_notice(text))


def test_two_blockquotes_in_the_section_are_refused(pcf, notice):
    text = bpo_notice_md(notice).decode("utf-8").replace(
        "The notice below.", "> A second quote.\n\nThe notice below.")
    assert "2 blockquote(s)" in refusal(lambda: pcf.extract_notice(text))


def test_a_two_paragraph_blockquote_is_refused(pcf, notice):
    text = bpo_notice_md(notice, 60).decode("utf-8")
    first = text.index("\n> ") + 1
    second = text.index("\n> ", first) + 1
    text = text[:second] + ">\n" + text[second:]
    assert "more than one paragraph" in refusal(
        lambda: pcf.extract_notice(text))


def test_the_notice_must_agree_with_the_catalogs_rights(pcf, notice, source):
    graph = pcf.read_catalog(catalog(notice), source)["graph"]
    assert pcf.verified_notice(source, bpo_notice_md(notice), graph) \
        == notice
    altered = catalog(notice, rights=['%s\\n\\n%s' % (
        esc(FRAMING), esc(notice.replace("perpetual", "temporary")))])
    graph = pcf.read_catalog(altered, source)["graph"]
    assert "disagree" in refusal(lambda: pcf.verified_notice(
        source, bpo_notice_md(notice), graph))


def test_an_altered_notice_in_notice_md_is_refused_by_its_digest(
        pcf, notice, source):
    graph = pcf.read_catalog(catalog(notice), source)["graph"]
    changed = bpo_notice_md(notice.replace("royalty-free", "royalty"))
    assert "digests to" in refusal(lambda: pcf.verified_notice(
        source, changed, graph))


def test_two_dct_rights_are_refused(pcf, notice, source):
    two = catalog(notice, rights=['%s\\n\\n%s' % (esc(FRAMING), esc(notice)),
                                  "Another statement."])
    graph = pcf.read_catalog(two, source)["graph"]
    assert "2 dct:rights" in refusal(lambda: pcf.verified_notice(
        source, bpo_notice_md(notice), graph))


def test_rights_without_a_blank_line_are_refused(pcf, notice, source):
    flat = catalog(notice, rights=[esc(FRAMING + " " + notice)])
    graph = pcf.read_catalog(flat, source)["graph"]
    assert "no blank line" in refusal(lambda: pcf.verified_notice(
        source, bpo_notice_md(notice), graph))


# ---------------------------------------------------------------- reader


def test_the_reader_takes_levels_parents_and_lines(pcf, notice, source):
    nodes = {n["element_id"]: n
             for n in pcf.read_catalog(catalog(notice), source)["nodes"]}
    assert nodes["900001"]["level"] == 1 and nodes["900001"]["parent"] is None
    assert nodes["900002"]["level"] == 2
    assert nodes["900002"]["parent"] == "900001"
    assert nodes["900003"]["parent"] == "900002"
    assert nodes["900005"]["level"] == 5
    assert nodes["900005"]["description"] is None
    assert nodes["900007"]["parent"] == "900006"
    text = catalog(notice).decode("utf-8").split("\n")
    for eid, node in nodes.items():
        assert text[node["line"] - 1].startswith("bpo:PCF_%s " % eid)


def test_entries_are_sorted_by_hierarchy_not_by_text(pcf, notice, source):
    read = pcf.read_catalog(catalog(notice), source)
    items = pcf.entries(read["nodes"], source, {})
    hids = [i["pcf_hierarchy_id"] for i in items]
    # 42.2 before 42.10: numeric, component by component.
    assert hids.index("42.2") < hids.index("42.10")
    assert items[0]["id"] == "INV-PCF74-900001"
    assert items[0]["locator"].startswith(
        "https://github.com/Skreen5hot/BusinessProcessOntology/blob/%s/"
        "ontology/apqc-catalog.ttl#L" % source["commit"])


@pytest.mark.parametrize("change, words", [
    (lambda n: [n[0], ("900002", "41.3", "Synthetic beta", "x",
                       "Category")] + n[2:], "BPO's comment says level"),
    (lambda n: n + [("900009", "43.4", "Synthetic orphan", "x",
                     "ProcessGroup")], "no element holds its parent"),
    (lambda n: n + [("900009", "41.3", "Synthetic twin", "x",
                     "ProcessGroup")], "repeats the hierarchy id"),
    (lambda n: n + [("900009", "41", "Synthetic flat", "x",
                     "Category")], "not dotted digits"),
    (lambda n: n + [("90A009", "43.0", "Synthetic letters", "x",
                     "Category")], "not digits"),
])
def test_a_malformed_catalog_is_refused(pcf, notice, source, change, words):
    data = catalog(notice, nodes=change(list(NODES)))
    assert words in refusal(lambda: pcf.read_catalog(data, source))


def test_a_broader_that_is_not_the_hierarchy_parent_is_refused(
        pcf, notice, source):
    data = catalog(notice, broader={"900003": "900006"})
    assert "skos:broader is not" in refusal(
        lambda: pcf.read_catalog(data, source))


def test_an_iri_other_than_bpos_scheme_is_refused(pcf, notice, source):
    data = catalog(notice, iri={"900003": "bpo:P900003"})
    assert "not BPO's PCF_<element id>" in refusal(
        lambda: pcf.read_catalog(data, source))


def test_two_names_are_refused(pcf, notice, source):
    data = catalog(notice, extra='bpo:PCF_900003 skos:prefLabel "Other" .\n')
    assert "exactly one" in refusal(lambda: pcf.read_catalog(data, source))


# ---------------------------------------------------------------- bridge


BRIDGES = {"entries": [
    {"kind": "capability-class", "id": "INV-BPO-SynthCap-capability-class",
     "iri": NS + "SynthCap", "pcf_code": "900004",
     "designated_by": [{"node": NS + "PCF_900003", "module": "m.ttl",
                        "pcf_code": "900003"}]},
    {"kind": "scope-entry", "id": "INV-BPO-SynthCap-scope-entry",
     "iri": NS + "SynthCap", "pcf_code": "900001"},
]}


def test_bridges_are_bpos_evidence_at_any_level(pcf, notice, source):
    bridges = pcf.bpo_bridges(BRIDGES)
    assert set(bridges) == {"900003", "900004"}
    read = pcf.read_catalog(catalog(notice), source)
    items = {i["pcf_element_id"]: i
             for i in pcf.entries(read["nodes"], source, bridges)}
    assert items["900003"]["bpo_bridge"]["designated_by_catalog_node"][0][
        "capability_class_entry"] == "INV-BPO-SynthCap-capability-class"
    assert items["900004"]["bpo_bridge"][
        "capability_class_with_this_code"][0]["capability_class_iri"] \
        == NS + "SynthCap"
    # A scope entry is not a capability class, so it bridges nothing.
    assert items["900001"]["bpo_bridge"] is None


# ----------------------------------------------------------------- build


COPIED = (PINS, "docs/sources/inventory/rights.yaml",
          "docs/decisions/2026-10-29-apqc-pcf-sourcing-decided.md",
          "tools/ontology/validate.py", "tools/inventory/harvest_bpo.py",
          "tools/layout.py", "config/repository-layout.yaml")


@pytest.fixture
def synthetic(tmp_path, notice):
    """A repository with the pins and a synthetic bridge input, plus the
    synthetic BPO files at hand."""
    for relative in COPIED:
        target = tmp_path / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes((ROOT / relative).read_bytes())
    (tmp_path / BPO_ENTRIES).write_bytes(
        yaml.safe_dump(BRIDGES).encode("utf-8"))
    return tmp_path, {"catalog": catalog(notice),
                      "notice": bpo_notice_md(notice)}


def write(base, built):
    for name, data in built.items():
        (base / name).parent.mkdir(parents=True, exist_ok=True)
        (base / name).write_bytes(data)


def test_a_build_carries_the_notice_and_the_statements(pcf, synthetic,
                                                       notice):
    base, files = synthetic
    built = pcf.build(base, files)
    document = yaml.safe_load(built[ENTRIES].decode("utf-8"))
    assert document["apqc_notice"] == notice
    assert document["apqc_notice_source"]["sha256"] == \
        pcf.pins(base)["inputs"]["notice"]["sha256"]
    assert "not covered by this repository's MIT licence" in \
        document["licence"]
    assert "does not produce, review or endorse" in document["endorsement"]
    assert "only to identify the source" in document["marks"]
    assert document["e4"]["state"] == "open"
    assert document["e4"]["judged"] == 0
    assert document["pcf_8_0"]["state"] == "deferred"
    assert document["counts"]["elements"] == len(NODES)
    assert document["counts"]["by_level"] == {
        "level_1": 2, "level_2": 3, "level_3": 1, "level_4": 1, "level_5": 1}
    notice_md = built["NOTICE.md"].decode("utf-8")
    assert pcf.extract_notice(notice_md) == notice
    assert pcf.listed_files(notice_md) == [
        i["path"] for i in pcf.pins(base)["pcf_bearing"]]


def test_two_builds_are_byte_identical(pcf, synthetic):
    base, files = synthetic
    assert pcf.build(base, files) == pcf.build(base, files)


def test_the_offline_check_passes_on_a_fresh_build(pcf, synthetic):
    base, files = synthetic
    write(base, pcf.build(base, files))
    problems, notes = pcf.check(base, base / "no-cache")
    assert problems == []
    assert any("not cached" in n for n in notes)
    # And with the files at hand, byte identity too.
    assert pcf.check(base, base / "no-cache", files)[0] == []


def edited(pcf, base, change):
    path = base / ENTRIES
    document = yaml.safe_load(path.read_bytes().decode("utf-8"))
    change(document)
    path.write_bytes(pcf.entries_bytes(document))
    return pcf.check(base, base / "no-cache")[0]


def _unbridge(document):
    for entry in document["entries"]:
        entry["bpo_bridge"] = None


@pytest.mark.parametrize("change, words", [
    (lambda d: d.update(apqc_notice=d["apqc_notice"].replace(
        "APQC.", "APQC")), "apqc_notice is not APQC's notice"),
    (lambda d: d.update(licence="Covered by MIT."), "licence is not what"),
    (lambda d: d.update(endorsement="Endorsed."), "endorsement is not what"),
    (lambda d: d.update(marks="Ours."), "marks is not what"),
    (lambda d: d["e4"].update(judged=3), "e4 is not what"),
    (lambda d: d["entries"][2].update(parent_pcf_element_id="900006"),
     "parent's hierarchy id is not its own"),
    (lambda d: d["entries"].reverse(), "not sorted by hierarchy id"),
    (lambda d: d["counts"].update(elements=99), "states counts"),
    (_unbridge, "bpo_bridge is not what"),
    (lambda d: d["entries"][0].update(bpo_iri=NS + "P1"), "bpo_iri is not"),
    (lambda d: d["entries"][0].update(locator="https://example.org/x"),
     "locator is not a line"),
    (lambda d: d["entries"][1].update(level=4), "level is not its"),
    (lambda d: d["entries"][1].update(extra="x"), "does not define"),
    (lambda d: d.pop("apqc_notice"), "declares no 'apqc_notice'"),
])
def test_an_edited_entries_file_is_refused(pcf, synthetic, change, words):
    base, files = synthetic
    write(base, pcf.build(base, files))
    problems = edited(pcf, base, change)
    assert any(words in p for p in problems), problems


def test_a_renamed_element_is_caught_only_with_the_source(pcf, synthetic):
    """Offline, a consistent edit of a name cannot be told from BPO's
    text; with BPO's files at hand (--confirm, weekly) it is refused."""
    base, files = synthetic
    write(base, pcf.build(base, files))
    edited(pcf, base, lambda d: d["entries"][0].update(name="Renamed"))
    assert pcf.check(base, base / "no-cache")[0] == []
    problems = pcf.check(base, base / "no-cache", files)[0]
    assert any("not what building from the pinned BPO files" in p
               for p in problems)


def test_a_hand_formatted_entries_file_is_refused(pcf, synthetic):
    base, files = synthetic
    write(base, pcf.build(base, files))
    path = base / ENTRIES
    document = yaml.safe_load(path.read_bytes().decode("utf-8"))
    path.write_bytes(yaml.safe_dump(document, sort_keys=False,
                                    width=200).encode("utf-8"))
    problems = pcf.check(base, base / "no-cache")[0]
    assert any("not the generator's rendering" in p for p in problems)


def test_a_stale_notice_is_refused(pcf, synthetic):
    base, files = synthetic
    write(base, pcf.build(base, files))
    path = base / "NOTICE.md"
    path.write_bytes(path.read_bytes() + b"\nAn added line.\n")
    problems = pcf.check(base, base / "no-cache")[0]
    assert any("NOTICE.md is not what" in p for p in problems)


def test_a_moved_bridge_input_is_refused(pcf, synthetic):
    base, files = synthetic
    write(base, pcf.build(base, files))
    path = base / BPO_ENTRIES
    path.write_bytes(path.read_bytes() + b"# moved\n")
    problems = pcf.check(base, base / "no-cache")[0]
    assert any("other than the committed one" in p for p in problems)


def test_crlf_is_refused(pcf, synthetic):
    base, files = synthetic
    write(base, pcf.build(base, files))
    path = base / ENTRIES
    path.write_bytes(path.read_bytes().replace(b"\n", b"\r\n"))
    problems = pcf.check(base, base / "no-cache")[0]
    assert any("CRLF" in p for p in problems)


def _repin(base, change):
    path = base / PINS
    data = yaml.safe_load(path.read_bytes().decode("utf-8"))
    change(data)
    path.write_bytes(yaml.safe_dump(data, sort_keys=False).encode("utf-8"))


def test_an_entries_output_cannot_be_an_exception(pcf, synthetic):
    base, _ = synthetic
    _repin(base, lambda d: d["exceptions"].append(
        {"path": ENTRIES, "reason": "convenience"}))
    assert "cannot be an exception" in refusal(lambda: pcf.pins(base))


def test_an_exception_must_name_a_listed_file(pcf, synthetic):
    base, _ = synthetic
    _repin(base, lambda d: d["exceptions"].append(
        {"path": "docs/elsewhere.yaml", "reason": "unlisted"}))
    assert "pcf_bearing does not list" in refusal(lambda: pcf.pins(base))


def test_a_short_commit_is_refused(pcf, synthetic):
    base, _ = synthetic
    _repin(base, lambda d: d["sources"][0].update(commit="2e55edd"))
    assert "not a full commit hash" in refusal(lambda: pcf.pins(base))


# ---------------------------------------------- the committed outputs


def committed() -> dict:
    return yaml.safe_load((ROOT / ENTRIES).read_bytes().decode("utf-8"))


def test_the_committed_outputs_pass_the_offline_check(pcf, tmp_path):
    problems, _ = pcf.check(ROOT, tmp_path / "no-cache")
    assert problems == []


def test_the_committed_entries_are_every_pcf_7_4_element(pcf):
    counts = committed()["counts"]
    assert counts["elements"] == 1921
    assert counts["by_level"] == {"level_1": 13, "level_2": 72,
                                  "level_3": 350, "level_4": 1297,
                                  "level_5": 189}
    assert counts["with_parent"] == 1908


def test_the_committed_entries_carry_the_pinned_notice(pcf, source):
    document = committed()
    assert pcf.sha256(document["apqc_notice"].encode("utf-8")) == \
        source["apqc_notice_sha256"]
    assert document["apqc_notice_source"]["sha256"] == \
        source["inputs"]["notice"]["sha256"] == \
        "ab7d5122a2d6384b9f380f13b76bb94c31295c69aeaa56f7b1ccdf25b79953e3"
    assert document["source"]["sha256"] == source["inputs"]["catalog"][
        "sha256"] == \
        "598faf6efa81ef6545cac04000c3d3834a9e8478f7619a3b8eed848a5b8d1547"
    assert source["commit"] == "2e55edd9e86a0bc20fa88a21595cc61402faa5dc"


def test_the_two_yaml_emitters_agree_on_the_committed_file(pcf):
    """dump() prefers libyaml; the bytes must not depend on it."""
    if not hasattr(yaml, "CSafeDumper"):
        pytest.skip("libyaml is not available here")
    document = committed()
    options = dict(sort_keys=False, allow_unicode=True, width=79,
                   default_flow_style=False)
    assert yaml.dump(document, Dumper=yaml.CSafeDumper, **options) == \
        yaml.dump(document, Dumper=yaml.SafeDumper, **options)


def test_with_bpos_files_cached_a_fresh_build_reproduces_both(pcf, source):
    """Local only: CI has no cache, and reproduces them weekly instead."""
    files = pcf.fetched(ROOT, source, ROOT / pcf.CACHE, network=False)
    if files is None:
        pytest.skip("BPO's catalog and NOTICE.md are not cached here")
    built = pcf.build(ROOT, files)
    for name, data in built.items():
        assert (ROOT / name).read_bytes() == data, name


# ------------------------------------------------------- wiring and layout


def test_the_entries_are_apqcs_text_written_by_this_tool(layout):
    component = layout.component("inventory.pcf-entries")
    assert component.path == ENTRIES
    assert component.role == "source-evidence"
    assert component.generator == "tool.inventory-harvest-pcf"
    assert layout.component("notice.pcf").path == "NOTICE.md"
    assert layout.component("notice.pcf").generator == \
        "tool.inventory-harvest-pcf"
    assert layout.component("tool.inventory-harvest-pcf").path == TOOL


def test_the_entries_are_dispositioned_under_apqcs_licence(disposition):
    rows = {r.path: r for r in disposition.classify()}
    row = rows[ENTRIES]
    assert row.disposition == disposition.VENDORED
    assert row.licence == "LicenseRef-APQC-PCF"
    assert disposition.redistributed_sources()[ENTRIES][1] == "NOTICE.md"
    assert disposition.attribution_findings(list(rows.values())) == []


def test_the_withdrawn_status_record_and_internal_directory_are_gone(
        layout, repo):
    ids = {c.id for c in layout.components()}
    assert "inventory.pcf-status" not in ids
    assert "inventory.internal" not in ids
    assert not (repo / "docs/sources/inventory/pcf-status.yaml").exists()
    # Still ignored: a stale local copy holds PCF text without the notice.
    text = (repo / ".gitignore").read_bytes().decode("utf-8")
    assert ".inventory-internal/" in text.splitlines()
    tracked = subprocess.run(["git", "-C", str(repo), "ls-files"],
                             capture_output=True, text=True).stdout
    assert ".inventory-internal/" not in tracked


def test_the_admission_guard_holds_with_the_entries(repo):
    harvest = load_tool("bco_harvest_bpo_for_pcf_test",
                        "tools/inventory/harvest_bpo.py")
    assert harvest.admission_findings(repo, "docs/sources/inventory",
                                      {}) == []


def test_ci_runs_the_check_the_gate_and_the_weekly_confirmation(repo):
    workflow = yaml.safe_load((repo / ".github/workflows/checks.yml")
                              .read_bytes().decode("utf-8"))
    jobs = workflow["jobs"]
    main_runs = [s.get("run", "").strip() for s in jobs["checks"]["steps"]]
    assert "python tools/inventory/harvest_pcf.py" in main_runs
    assert "python tools/licensing/pcf_notice.py" in main_runs
    weekly = [s.get("run", "").strip() for s in jobs["vendored"]["steps"]]
    assert "python tools/inventory/harvest_pcf.py --confirm" in weekly


def test_the_tools_never_name_apqc_org_as_a_host_to_fetch():
    for relative in (TOOL, "tools/licensing/pcf_notice.py"):
        text = (ROOT / relative).read_bytes().decode("utf-8")
        assert "https://www.apqc.org" not in text
        assert "urlopen" not in text


def test_the_workbook_and_pcf_8_0_are_no_longer_read():
    text = (ROOT / TOOL).read_bytes().decode("utf-8")
    assert "zipfile" not in text and ".xlsx" not in text
    assert "--pcf80" not in text
