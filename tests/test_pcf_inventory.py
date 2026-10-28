# SPDX-License-Identifier: MIT
"""Phase I-2b: the PCF reader, the delta, the internal-only writer, and
the public status record's guard.

Every workbook here is SYNTHETIC, built in the test from made-up element
ids (six digits, 9xxxxx), hierarchy ids in categories 41 to 43 and names
such as "Synthetic alpha". No APQC content is in this file: whether APQC's
terms allow its content to be processed or republished is open
(APQC-1 c), and a test has no need of it. The committed status record is
tested as committed; the real workbook is used only when it is cached
locally, and the test that needs it is skipped otherwise (the weekly
--confirm job is CI's reproduction).

Refusals are tested by the words of their finding, one rule at a time,
with a positive control beside each guard (docs/process/PROCESS.md
section 2).
"""

from __future__ import annotations

import io
import subprocess
import zipfile
from xml.sax.saxutils import escape

import pytest
import yaml

from conftest import ROOT, load_tool

TOOL = "tools/inventory/harvest_pcf.py"
STATUS = "docs/sources/inventory/pcf-status.yaml"
HEADER = ("PCF ID", "Hierarchy ID", "Name", "Difference Index",
          "Change details", "Metrics available?", "Element Description")

#: (element id, hierarchy id, name, description) -- all made up.
ROWS_A = [
    ("900001", "41.0", "Synthetic alpha", "Made-up text one"),
    ("900002", "41.3", "Synthetic beta", "Made-up text two"),
    ("900003", "41.3.7", "Synthetic gamma", "Made-up text three"),
    ("900004", "41.3.7.2", "Synthetic delta", "Made-up text four"),
    ("900005", "41.3.8", "Synthetic epsilon", "Made-up text five"),
    ("900006", "42.0", "Synthetic zeta", "Made-up text six"),
    ("900007", "42.1", "Synthetic eta", "Made-up text seven"),
    ("900008", "42.1.4", "Synthetic theta", "Made-up text eight"),
]


@pytest.fixture(scope="module")
def pcf():
    return load_tool("bco_inventory_harvest_pcf", TOOL)


def xlsx(rows, sheet="Combined", header=HEADER, numeric_hid=False,
         content_type=True) -> bytes:
    """A minimal xlsx: one sheet, inline strings, numbers as numbers."""
    def cell(ref, value, number=False):
        if value is None:
            return ""
        if number:
            return '<c r="%s"><v>%s</v></c>' % (ref, value)
        return ('<c r="%s" t="inlineStr"><is><t>%s</t></is></c>'
                % (ref, escape(value)))

    lines = ["<row r=\"1\">%s</row>" % "".join(
        cell("%s1" % chr(65 + n), title) for n, title in enumerate(header))]
    for n, (eid, hid, name, description) in enumerate(rows, start=2):
        lines.append('<row r="%d">%s%s%s%s</row>' % (
            n, cell("A%d" % n, eid, number=True),
            cell("B%d" % n, hid, number=numeric_hid),
            cell("C%d" % n, name), cell("G%d" % n, description)))
    main = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
    rel = ("http://schemas.openxmlformats.org/officeDocument/2006/"
           "relationships")
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as archive:
        archive.writestr("[Content_Types].xml", (
            '<Types xmlns="http://schemas.openxmlformats.org/package/2006/'
            'content-types"><Override PartName="/xl/workbook.xml" '
            'ContentType="application/vnd.openxmlformats-officedocument.%s'
            '+xml"/></Types>' % ("spreadsheetml.sheet.main" if content_type
                                 else "wordprocessingml.document.main")))
        archive.writestr("xl/workbook.xml", (
            '<workbook xmlns="%s" xmlns:r="%s"><sheets><sheet name="Notes" '
            'sheetId="1" r:id="rId1"/><sheet name="%s" sheetId="2" '
            'r:id="rId2"/></sheets></workbook>' % (main, rel, sheet)))
        archive.writestr("xl/_rels/workbook.xml.rels", (
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/'
            '2006/relationships"><Relationship Id="rId1" Type="%s/worksheet" '
            'Target="worksheets/sheet1.xml"/><Relationship Id="rId2" '
            'Type="%s/worksheet" Target="/xl/worksheets/sheet2.xml"/>'
            '</Relationships>' % (rel, rel)))
        archive.writestr("xl/worksheets/sheet1.xml",
                         '<worksheet xmlns="%s"><sheetData/></worksheet>'
                         % main)
        archive.writestr("xl/worksheets/sheet2.xml", (
            '<worksheet xmlns="%s"><sheetData>%s</sheetData></worksheet>'
            % (main, "".join(lines))))
    return buffer.getvalue()


def refusal(pcf, call) -> str:
    with pytest.raises(pcf.Refused) as error:
        call()
    return str(error.value)


# ------------------------------------------------------------- the reader


def test_the_reader_takes_levels_parents_and_locators(pcf):
    read = pcf.read_workbook(xlsx(ROWS_A))
    assert read["sheet"] == "Combined" and read["rows"] == 8
    assert read["rows_by_level"] == {"level_1": 2, "level_2": 2,
                                     "level_3": 3, "level_4": 1}
    by = {n["element_id"]: n for n in read["nodes"]}
    assert by["900001"]["level"] == 1 and by["900001"]["parent"] is None
    assert by["900002"]["level"] == 2
    assert by["900002"]["parent"] == {"element_id": "900001",
                                      "hierarchy_id": "41.0"}
    assert by["900003"]["parent"]["element_id"] == "900002"
    assert by["900004"]["level"] == 4
    assert (by["900003"]["sheet"], by["900003"]["row"]) == ("Combined", 4)
    assert by["900003"]["name"] == "Synthetic gamma"
    assert by["900003"]["description"] == "Made-up text three"


def test_a_missing_column_is_refused(pcf):
    header = tuple(h for h in HEADER if h != "Element Description")
    message = refusal(pcf, lambda: pcf.read_workbook(xlsx(ROWS_A,
                                                          header=header)))
    assert "has no 'Element Description' column" in message


def test_a_workbook_without_the_combined_sheet_is_refused(pcf):
    message = refusal(pcf, lambda: pcf.read_workbook(xlsx(ROWS_A,
                                                          sheet="Other")))
    assert "sheet(s) named 'Combined'" in message


def test_an_element_id_that_is_not_an_integer_is_refused(pcf):
    rows = [("90000x",) + ROWS_A[0][1:]] + ROWS_A[1:]
    message = refusal(pcf, lambda: pcf.read_workbook(xlsx(rows)))
    assert "is not an integer element id" in message
    # The refusal names the row, never the cell's value.
    assert "90000x" not in message


def test_a_hierarchy_id_held_as_a_number_is_refused(pcf):
    message = refusal(pcf, lambda: pcf.read_workbook(
        xlsx(ROWS_A, numeric_hid=True)))
    assert "cannot be told apart" in message


def test_a_hierarchy_id_that_is_not_dotted_digits_is_refused(pcf):
    rows = [ROWS_A[0][:1] + ("41-0",) + ROWS_A[0][2:]] + ROWS_A[1:]
    message = refusal(pcf, lambda: pcf.read_workbook(xlsx(rows)))
    assert "is not dotted digits" in message


def test_a_repeated_element_id_is_refused(pcf):
    rows = ROWS_A + [("900001", "43.0", "Synthetic iota", "x")]
    assert "repeats the element id" in refusal(
        pcf, lambda: pcf.read_workbook(xlsx(rows)))


def test_a_repeated_hierarchy_id_is_refused(pcf):
    rows = ROWS_A + [("900099", "41.3.8", "Synthetic iota", "x")]
    assert "repeats the hierarchy id" in refusal(
        pcf, lambda: pcf.read_workbook(xlsx(rows)))


def test_an_orphan_is_refused(pcf):
    rows = ROWS_A + [("900099", "43.2.1", "Synthetic iota", "x")]
    assert "its parent is not in the sheet" in refusal(
        pcf, lambda: pcf.read_workbook(xlsx(rows)))


def test_a_file_that_is_not_an_xlsx_is_refused(pcf):
    assert "not a zip archive" in refusal(
        pcf, lambda: pcf.read_workbook(b"plain text", "the 8.0 file"))
    assert "declares no spreadsheetml workbook part" in refusal(
        pcf, lambda: pcf.read_workbook(xlsx(ROWS_A, content_type=False)))
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as archive:
        archive.writestr("readme.txt", "x")
    assert "it is not an xlsx workbook" in refusal(
        pcf, lambda: pcf.read_workbook(buffer.getvalue()))


# ------------------------------------------------------------- the entries


BPO = {"entries": [
    {"id": "INV-BPO-SyntheticCapability-capability-class",
     "kind": "capability-class",
     "iri": "https://example.invalid/bpo#SyntheticCapability",
     "pcf_code": None,
     "designated_by": [{"node": "https://example.invalid/bpo#PCF_900003",
                        "pcf_code": "900003", "module": "x.ttl"}]},
    {"id": "INV-BPO-P900005-capability-class", "kind": "capability-class",
     "iri": "https://example.invalid/bpo#P900005", "pcf_code": "900005",
     "designated_by": []},
    {"id": "INV-BPO-Scope-scope-entry", "kind": "scope-entry",
     "iri": "https://example.invalid/bpo#Scope", "pcf_code": "900008"},
]}


def test_entries_are_levels_one_to_three_with_stable_ids(pcf):
    items = pcf.entries(pcf.read_workbook(xlsx(ROWS_A)), {})
    assert [i["id"] for i in items] == [
        "INV-PCF74-900001-pcf-category", "INV-PCF74-900006-pcf-category",
        "INV-PCF74-900002-pcf-process-group",
        "INV-PCF74-900007-pcf-process-group",
        "INV-PCF74-900003-pcf-level-3-unjudged",
        "INV-PCF74-900005-pcf-level-3-unjudged",
        "INV-PCF74-900008-pcf-level-3-unjudged"]
    assert all(i["rights_status"] == pcf.INTERNAL_RIGHTS for i in items)
    # No judgement is made: nothing is called a candidate.
    assert not any("candidate" in i["kind"] for i in items)


def test_level_three_carries_bpos_bridge_as_evidence(pcf):
    items = pcf.entries(pcf.read_workbook(xlsx(ROWS_A)),
                        pcf.bpo_bridges(BPO))
    by = {i["element_id"]: i for i in items}
    bridged = by["900003"]["bpo_bridge_evidence"]
    assert bridged["bridged"] is True
    assert bridged["designated_by_catalog_node"][0][
        "capability_class_entry"] == (
        "INV-BPO-SyntheticCapability-capability-class")
    coded = by["900005"]["bpo_bridge_evidence"]
    assert coded["bridged"] is False
    assert coded["capability_class_with_this_code"][0][
        "capability_class_entry"] == "INV-BPO-P900005-capability-class"
    # A scope entry is not a capability class, and so not a bridge.
    assert by["900008"]["bpo_bridge_evidence"]["bridged"] is False
    assert "bpo_bridge_evidence" not in by["900002"]


def test_the_e4_worksheet_is_one_empty_row_per_level_three_node(pcf):
    items = pcf.entries(pcf.read_workbook(xlsx(ROWS_A)),
                        pcf.bpo_bridges(BPO))
    sheet = pcf.worksheet_document(items)
    assert [r["element_id"] for r in sheet["rows"]] == [
        "900003", "900005", "900008"]
    for row in sheet["rows"]:
        assert row["judgement"] is None and row["reason"] is None
        assert row["independent_evidence"] == []
        assert row["judged_by"] is None and row["judged_on"] is None
        assert row["node_locator"]["sheet"] == "Combined"
    assert sheet["state"].startswith("deferred")


def test_two_builds_are_byte_identical(pcf):
    read = pcf.read_workbook(xlsx(ROWS_A))
    first = pcf.internal_bytes(pcf.worksheet_document(
        pcf.entries(read, pcf.bpo_bridges(BPO))))
    second = pcf.internal_bytes(pcf.worksheet_document(
        pcf.entries(pcf.read_workbook(xlsx(ROWS_A)), pcf.bpo_bridges(BPO))))
    assert first == second and b"\r\n" not in first


# --------------------------------------------------------------- the delta


def test_the_delta_classifies_each_change(pcf):
    rows_b = [
        ("900001", "41.0", "Synthetic alpha", "Made-up text one"),
        ("900002", "41.3", "Synthetic beta renamed", "Made-up text two"),
        # 900003 re-coded and moved under 900007
        ("900003", "42.1.9", "Synthetic gamma", "Made-up text three"),
        # level-4 change only: not in the delta
        ("900004", "41.3.8.5", "Synthetic delta changed", "x"),
        ("900005", "41.3.8", "Synthetic   epsilon", "whitespace only"),
        ("900006", "42.0", "Synthetic zeta", "Made-up text six"),
        ("900007", "42.1", "Synthetic eta", "Made-up text seven"),
        # 900008 retired; 900010 added at level 3; 900011 added at level 4
        ("900010", "42.1.5", "Synthetic kappa", "new"),
        ("900011", "42.1.5.1", "Synthetic lambda", "new, level 4"),
    ]
    changes = pcf.delta(pcf.read_workbook(xlsx(ROWS_A)),
                        pcf.read_workbook(xlsx(rows_b)))
    by = {c["element_id"]: c["changes"] for c in changes}
    assert by == {"900002": ["renamed"], "900003": ["recoded", "moved"],
                  "900008": ["retired"], "900010": ["added"]}
    assert pcf.delta_counts(changes) == {"added": 1, "retired": 1,
                                         "renamed": 1, "recoded": 1,
                                         "moved": 1}
    retired = [c for c in changes if c["element_id"] == "900008"][0]
    assert retired["pcf_8_0"] is None
    assert retired["pcf_7_4"]["locator"] == {"sheet": "Combined", "row": 9}


def test_a_node_leaving_level_three_is_re_coded(pcf):
    rows_b = [r if r[0] != "900008" else
              ("900008", "42.1.4.1", r[2], r[3]) for r in ROWS_A]
    rows_b.append(("900012", "42.1.4", "Synthetic mu", "x"))
    changes = pcf.delta(pcf.read_workbook(xlsx(ROWS_A)),
                        pcf.read_workbook(xlsx(rows_b)))
    by = {c["element_id"]: c["changes"] for c in changes}
    assert by["900008"] == ["recoded", "moved"]
    assert by["900012"] == ["added"]


# ---------------------------------------------------- the internal writer


def git(path, *args):
    subprocess.run(["git", "-C", str(path), *args], check=True,
                   capture_output=True)


@pytest.fixture
def gitrepo(tmp_path):
    base = tmp_path / "repo"
    base.mkdir()
    git(base, "init", "-q")
    (base / ".gitignore").write_bytes(b".inventory-internal/\n")
    (base / "tracked.yaml").write_bytes(b"x: 1\n")
    git(base, "add", ".gitignore", "tracked.yaml")
    return base


def test_an_ignored_internal_path_is_accepted(pcf, gitrepo):
    internal = gitrepo / ".inventory-internal" / "i2b"
    target = pcf.internal_target(gitrepo, internal, "pcf-7.4-entries.yaml")
    assert target == (internal / "pcf-7.4-entries.yaml").resolve()
    pcf.write_internal(gitrepo, internal, {"a.yaml": b"a: 1\n"})
    assert (internal / "a.yaml").read_bytes() == b"a: 1\n"


def test_a_tracked_path_is_refused(pcf, gitrepo):
    assert "git tracks it" in refusal(
        pcf, lambda: pcf.internal_target(gitrepo, gitrepo, "tracked.yaml"))


def test_a_path_git_does_not_ignore_is_refused(pcf, gitrepo):
    assert "git does not ignore it" in refusal(
        pcf, lambda: pcf.internal_target(gitrepo, gitrepo / "docs",
                                         "pcf.yaml"))


def test_a_path_outside_the_internal_directory_is_refused(pcf, gitrepo):
    internal = gitrepo / ".inventory-internal" / "i2b"
    assert "outside the internal directory" in refusal(
        pcf, lambda: pcf.internal_target(gitrepo, internal,
                                         "../../docs/pcf.yaml"))


def test_without_git_nothing_inside_the_repository_is_written(pcf,
                                                              tmp_path):
    base = tmp_path / "not-a-repo"
    base.mkdir()
    assert "git cannot say whether it is tracked" in refusal(
        pcf, lambda: pcf.internal_target(base, base / ".inventory-internal",
                                         "x.yaml"))


def test_a_directory_outside_the_repository_is_accepted(pcf, gitrepo,
                                                        tmp_path):
    outside = tmp_path / "elsewhere"
    assert pcf.internal_target(gitrepo, outside, "x.yaml") == (
        outside / "x.yaml").resolve()


def test_the_real_internal_directory_is_ignored_and_untracked(repo):
    ignored = subprocess.run(
        ["git", "-C", str(repo), "check-ignore", "-q", "--no-index",
         ".inventory-internal/i2b/pcf-7.4-entries.yaml"])
    assert ignored.returncode == 0
    tracked = subprocess.run(["git", "-C", str(repo), "ls-files", "--",
                              ".inventory-internal"],
                             capture_output=True, text=True)
    assert tracked.stdout.strip() == ""


# ------------------------------------------------------- the public guard


def committed():
    return yaml.safe_load((ROOT / STATUS).read_bytes().decode("utf-8"))


def guard(pcf, document, **kw):
    return pcf.status_findings(document, ROOT, **kw)


def refused(pcf, document, needle, **kw):
    problems = guard(pcf, document, **kw)
    assert any(needle in p for p in problems), problems
    return problems


def test_the_committed_record_passes_the_guard(pcf):
    """The positive control for every guard test below."""
    pin = pcf.workbook_pin(ROOT)
    citations = pcf.rights_citation(ROOT)
    raw = (ROOT / STATUS).read_bytes()
    assert guard(pcf, committed(), pin=pin, citations=citations,
                 raw=raw) == []
    assert pcf.status_bytes(committed()) == raw


def test_the_committed_record_carries_no_pcf_code_or_content_key(pcf):
    """Read directly, not through the tool's guard."""
    rights = load_tool("bco_rights_for_pcf_test",
                       "tools/inventory/rights.py")
    text = (ROOT / STATUS).read_bytes().decode("utf-8")
    pcf_pattern = rights.CODE_PATTERNS[0][1]
    assert not pcf_pattern.search(text)
    keys = set()

    def walk(node):
        if isinstance(node, dict):
            for key, value in node.items():
                keys.add(key)
                walk(value)
        elif isinstance(node, list):
            for value in node:
                walk(value)
    walk(committed())
    assert not keys & set(rights.CATALOG_KEYS)
    assert not keys & {"name", "description", "element_id",
                       "hierarchy_id", "parent", "label", "definition"}


def test_counts_are_the_only_numbers_about_the_catalog(pcf):
    counts = committed()["counts"]
    assert set(counts) == set(pcf.COUNT_KEYS)
    assert all(isinstance(v, int) for v in counts["rows_by_level"].values())


@pytest.mark.parametrize("code", ["41.0", "41.3", "41.3.7", "41.3.7.2"])
def test_a_hierarchy_id_in_prose_is_refused(pcf, code):
    document = committed()
    document["e4"]["why"] = "see %s" % code
    refused(pcf, document, "reads as a PCF hierarchy id")


def test_an_element_id_in_prose_is_refused(pcf):
    document = committed()
    document["posture"]["public"] = "except element 900003"
    refused(pcf, document, "as long as a PCF element id")


@pytest.mark.parametrize("key", ["name", "description", "hierarchy_id",
                                 "element_id", "parent", "codes"])
def test_a_content_key_is_refused_wherever_it_is(pcf, key):
    document = committed()
    document["counts"][key] = "x"
    refused(pcf, document, "The public record holds no PCF content")
    document = committed()
    document["internal"]["outputs"][0][key] = "x"
    refused(pcf, document, "The public record holds no PCF content")


def test_an_unknown_key_is_refused(pcf):
    document = committed()
    document["citation"]["levels"] = ["x"]
    refused(pcf, document, "which the status record does not define")


def test_a_name_from_the_build_is_refused(pcf):
    content = pcf.content_of(pcf.entries(pcf.read_workbook(xlsx(ROWS_A)),
                                         {}))
    document = committed()
    assert guard(pcf, document, content=content) == []      # control
    document["e4"]["why"] = "about Synthetic gamma, deferred"
    refused(pcf, document, "contains the text of a PCF name or description",
            content=content)


def test_a_description_from_the_build_is_refused(pcf):
    content = pcf.content_of(pcf.entries(pcf.read_workbook(xlsx(ROWS_A)),
                                         {}))
    document = committed()
    document["what"] = "made-up TEXT   two"
    refused(pcf, document, "contains the text of a PCF name or description",
            content=content)


def test_counts_that_do_not_add_up_are_refused(pcf):
    document = committed()
    document["counts"]["rows_by_level"]["level_1"] += 1
    refused(pcf, document, "do not add up to the workbook rows")


def test_a_kind_count_not_matching_its_level_is_refused(pcf):
    document = committed()
    document["counts"]["entries_by_kind"]["pcf-process-group"] += 1
    refused(pcf, document, "is not the level-2 row count")


def test_a_judgement_in_the_record_is_refused(pcf):
    document = committed()
    document["e4"]["judged"] = 3
    refused(pcf, document, "E4 is deferred")


def test_a_changed_posture_is_refused(pcf):
    document = committed()
    document["posture"]["decision"] = "APQC-1 a"
    refused(pcf, document, "is not APQC-1 c")


def test_a_committed_internal_directory_is_refused(pcf):
    document = committed()
    document["internal"]["committed"] = True
    refused(pcf, document, "committed: false")


def test_a_citation_other_than_the_pin_is_refused(pcf):
    document = committed()
    document["citation"]["bpo_locator"]["commit"] = "0" * 40
    refused(pcf, document, "is not the workbook",
            pin=pcf.workbook_pin(ROOT))


def test_a_citation_other_than_the_rights_record_is_refused(pcf):
    document = committed()
    document["citation"]["edition"] = "7.3"
    refused(pcf, document, "is not what docs/sources/inventory/rights.yaml",
            citations=pcf.rights_citation(ROOT))


def test_an_authored_namespace_iri_is_refused(pcf):
    namespace = pcf.harvest_module(ROOT).authored_namespaces(ROOT)[0]
    document = committed()
    document["what"] = "mints %sX" % namespace
    refused(pcf, document, "authored namespaces")


def test_rdf_in_the_record_is_refused(pcf):
    raw = (ROOT / STATUS).read_bytes() + b"@prefix owl: <x> .\n"
    refused(pcf, committed(), "reads as an RDF serialization", raw=raw)


def test_a_ratification_key_is_refused(pcf):
    document = committed()
    document["e4"]["ratified_by"] = "someone"
    refused(pcf, document, "A ratification or vocabulary field")


def test_a_supplied_8_0_needs_its_digests_and_counts(pcf):
    document = committed()
    document["pcf_8_0"] = pcf.pcf80_supplied("a" * 64, 10, b"x",
                                             {c: 0 for c in pcf.CHANGES})
    assert guard(pcf, document) == []                        # control
    document["pcf_8_0"]["delta"]["counts"].pop("moved")
    refused(pcf, document, "is not a count per change type")
    document = committed()
    document["pcf_8_0"]["file"] = {"sha256": "a" * 64, "bytes": 1}
    refused(pcf, document, "is a gap but carries a file")


def test_the_status_is_not_written_when_its_guard_fails(pcf):
    document = committed()
    document["e4"]["why"] = "see 41.3.7"
    before = (ROOT / STATUS).read_bytes()
    with pytest.raises(pcf.Refused) as error:
        pcf.write_status(ROOT, b"never", document, None,
                         pcf.workbook_pin(ROOT), pcf.rights_citation(ROOT))
    assert "nothing public was written" in str(error.value)
    assert (ROOT / STATUS).read_bytes() == before


def test_a_status_built_from_a_synthetic_workbook_carries_none_of_it(pcf):
    read = pcf.read_workbook(xlsx(ROWS_A))
    items = pcf.entries(read, pcf.bpo_bridges(BPO))
    outputs = {pcf.ENTRIES_FILE: b"a", pcf.WORKSHEET_FILE: b"b"}
    pin = pcf.workbook_pin(ROOT)
    document = pcf.status_document(pin, pcf.rights_citation(ROOT), read,
                                   items, "c" * 64, outputs,
                                   pcf.pcf80_gap())
    data = pcf.status_bytes(document)
    assert guard(pcf, document, content=pcf.content_of(items)) == []
    text = data.decode("utf-8")
    for eid, hid, name, description in ROWS_A:
        assert eid not in text and name not in text
        assert description not in text and hid not in text
    assert document["counts"]["level_3_bpo_bridged"] == 1
    assert document["counts"]["level_3_bpo_coded"] == 1


# ------------------------------------------------------- the offline check


COPIED = ("config/inventory-sources.yaml", "config/upstream-sources.yaml",
          "docs/decisions/2026-10-28-i2-and-bpo-repin-decided.md",
          "docs/decisions/2026-10-28-i2a-decided.md",
          "docs/sources/inventory/rights.yaml",
          "docs/sources/inventory/bpo-entries.yaml", STATUS,
          "tools/ontology/validate.py", "tools/inventory/harvest_bpo.py",
          "tools/inventory/rights.py", "tools/layout.py")


@pytest.fixture
def copy(tmp_path):
    for relative in COPIED:
        target = tmp_path / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes((ROOT / relative).read_bytes())
    return tmp_path


def offline(pcf, base):
    return pcf.check(base, base / "no-cache", base / "no-internal")


def test_the_offline_check_without_the_workbook_passes(pcf, copy):
    problems, notes = offline(pcf, copy)
    assert problems == []
    assert any("not cached" in n for n in notes)


def test_a_hand_edited_record_is_refused(pcf, copy):
    path = copy / STATUS
    before = path.read_bytes()
    after = yaml.safe_dump(committed(), sort_keys=True).encode("utf-8")
    assert after != before
    path.write_bytes(after)
    problems, _ = offline(pcf, copy)
    assert any("not the generator's rendering" in p for p in problems), \
        problems


def test_a_moved_bridge_input_is_refused(pcf, copy):
    path = copy / "docs/sources/inventory/bpo-entries.yaml"
    path.write_bytes(path.read_bytes() + b"# moved\n")
    problems, _ = offline(pcf, copy)
    assert any("other than the committed one" in p for p in problems)


def test_crlf_is_refused(pcf, copy):
    path = copy / STATUS
    path.write_bytes(path.read_bytes().replace(b"\n", b"\r\n"))
    assert "CRLF" in refusal(pcf, lambda: offline(pcf, copy))


def test_with_the_cached_workbook_a_fresh_build_reproduces_the_record(
        pcf):
    """Local only: CI has no cache, and reproduces it weekly instead."""
    pin = pcf.workbook_pin(ROOT)
    if pcf.cached_workbook(ROOT, pin, ROOT / pcf.CACHE) is None:
        pytest.skip("the PCF 7.4 workbook is not cached here")
    problems, _ = pcf.check(ROOT, ROOT / pcf.CACHE, ROOT / pcf.INTERNAL)
    assert problems == []


# ------------------------------------------------------- wiring and layout


def test_the_record_is_a_generated_artifact_of_this_tool(layout):
    component = layout.component("inventory.pcf-status")
    assert component.path == STATUS
    assert component.role == "generated-artifact"
    assert component.generator == "tool.inventory-harvest-pcf"
    assert layout.component("tool.inventory-harvest-pcf").path == TOOL


def test_the_internal_directory_is_declared_never_tracked(layout, repo):
    component = layout.component("inventory.internal")
    assert component.path == ".inventory-internal"
    assert component.tracked is False
    assert component.redistributable is False
    text = (repo / ".gitignore").read_bytes().decode("utf-8")
    assert ".inventory-internal/" in text.splitlines()


def test_the_admission_guard_holds_with_the_record(repo):
    harvest = load_tool("bco_harvest_bpo_for_pcf_test",
                        "tools/inventory/harvest_bpo.py")
    assert harvest.admission_findings(repo, "docs/sources/inventory",
                                      {}) == []


def test_ci_runs_the_check_and_the_weekly_confirmation(repo):
    workflow = yaml.safe_load((repo / ".github/workflows/checks.yml")
                              .read_bytes().decode("utf-8"))
    jobs = workflow["jobs"]
    main_runs = [s.get("run", "").strip() for s in jobs["checks"]["steps"]]
    assert "python tools/inventory/harvest_pcf.py" in main_runs
    weekly = [s.get("run", "").strip() for s in jobs["vendored"]["steps"]]
    assert "python tools/inventory/harvest_pcf.py --confirm" in weekly
    # The weekly confirmation follows harvest_bpo --confirm, which fetches
    # the workbook into the shared cache as part of its evidence check.
    assert weekly.index("python tools/inventory/harvest_pcf.py --confirm") \
        > weekly.index("python tools/inventory/harvest_bpo.py --confirm")


def test_the_tool_never_names_apqc_org_as_a_host_to_fetch(pcf):
    source = (ROOT / TOOL).read_bytes().decode("utf-8")
    assert "https://www.apqc.org" not in source
    assert "urlopen" not in source


def test_no_internal_output_name_is_tracked(repo):
    tracked = subprocess.run(["git", "-C", str(repo), "ls-files"],
                             capture_output=True, text=True).stdout
    for name in ("pcf-7.4-entries.yaml", "pcf-7.4-e4-worksheet.yaml",
                 "pcf-7.4-to-8.0-delta.yaml"):
        assert name not in tracked

