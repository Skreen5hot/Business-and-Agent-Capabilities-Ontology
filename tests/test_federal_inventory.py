# SPDX-License-Identifier: MIT
"""Phase I-2c, the federal catalogs: the check refuses what it says it does.

tools/inventory/harvest_federal.py has a harvest that needs the pinned
documents (in the gitignored cache, or fetched) and an offline check that
runs everywhere. As in tests/test_inventory.py, the check is tested on the
committed outputs and then on copies in tmp_path broken one rule at a time
-- each mutation asserted to have changed the bytes before the check runs,
each failure required to be the finding for that rule. The rules that need
a workbook (what counts as a notice, the withholding rules, the reader)
are tested on small workbooks built here in memory. The harvest of the
real documents runs when the cache holds them and is skipped otherwise;
CI holds it to its pins weekly with --confirm.

No tracked fixture: every broken case is built at run time, because a
`test-fixture` component is loaded as Turtle by the validation ladder.
"""

from __future__ import annotations

import io
import zipfile

import pytest
import yaml

from conftest import ROOT, load_tool

TOOL = "tools/inventory/harvest_federal.py"
DIRECTORY = "docs/sources/inventory"
BRM = DIRECTORY + "/feaf-brm-entries.yaml"
FA = DIRECTORY + "/fibf-entries.yaml"
CAPS = DIRECTORY + "/fibf-business-capabilities.yaml"
SNAPSHOT = DIRECTORY + "/fibf-snapshot.yaml"
NOTICE = DIRECTORY + "/NOTICE-federal.md"
PINS = "config/inventory-federal-sources.yaml"
RIGHTS = DIRECTORY + "/rights.yaml"
COPIED = (PINS, RIGHTS, BRM, FA, CAPS, SNAPSHOT, NOTICE,
          "tools/inventory/harvest_bpo.py", "tools/ontology/validate.py",
          "docs/decisions/2026-10-28-i2a-decided.md",
          "docs/decisions/2026-10-28-i2-and-bpo-repin-decided.md")


@pytest.fixture(scope="module")
def harvest():
    return load_tool("bco_harvest_federal", TOOL)


@pytest.fixture(scope="module")
def committed():
    """The committed outputs, parsed once: they are megabytes of YAML."""
    loader = getattr(yaml, "CSafeLoader", yaml.SafeLoader)
    return {path: yaml.load((ROOT / path).read_bytes().decode("utf-8"),
                            Loader=loader)
            for path in (BRM, FA, CAPS, SNAPSHOT)}


@pytest.fixture
def copy(tmp_path):
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


def assert_finding(problems, *needles):
    assert problems, "the check passed a broken copy"
    assert any(all(n in p for n in needles) for p in problems), problems


def first(entries, **match):
    for entry in entries:
        if all(entry.get(k) == v for k, v in match.items()):
            return entry
    raise AssertionError("no entry matching %r" % match)


# ------------------------------------------------------- the real outputs


def test_the_committed_outputs_pass(harvest):
    problems, summary = harvest.check(ROOT)
    assert problems == [], problems
    # Guard the guard: a check over an empty inventory would pass too.
    brm, fa, caps, snap = (summary["brm"], summary["functions"],
                           summary["capabilities"], summary["snapshot"])
    assert brm["brm-mission-sector"] and brm["brm-business-function"]
    assert brm["brm-service"] and fa["fibf-function"] and fa["fibf-activity"]
    assert caps["fibf-business-capability"] > 0
    assert snap["documents"] == snap["harvested"] + snap["withheld-mitre"] \
        + snap["withheld-ambiguous"]
    assert snap["harvested"] > 0 and snap["withheld-mitre"] > 0


def test_the_copy_is_clean_before_anything_is_broken(harvest, copy):
    """Every negative test below starts from this state, so a finding in
    one of them is the mutation's and not the copy's."""
    assert findings(harvest, copy) == []


def test_both_brm_documents_are_harvested_separately(committed):
    """BRM-2 c: two documents, two id prefixes, never merged."""
    doc = committed[BRM]
    assert [d["evidence"] for d in doc["documents"]] == [
        "brm-3.1-service-codes-and-definitions", "brm-3.1-taxonomy"]
    prefixes = {e["document"]: e["id"].split("-")[3]
                for e in doc["entries"]}
    assert prefixes == {"brm-3.1-service-codes-and-definitions": "SCD",
                        "brm-3.1-taxonomy": "TAX"}
    levels = {e["level"] for e in doc["entries"]}
    assert levels == {"Mission Sector", "Business Function", "Service"}


def test_every_row_has_a_locator(committed):
    for path in (BRM, FA, CAPS):
        for entry in committed[path]["entries"]:
            locator = entry["locator"]
            assert ("sheet" in locator and isinstance(locator["row"], int)) \
                or isinstance(locator.get("page"), int) \
                or isinstance(locator.get("pages"), list) \
                or isinstance(locator.get("html_line"), int), entry["id"]


def test_every_capability_carries_the_homonym_flag(committed):
    entries = committed[CAPS]["entries"]
    assert entries
    assert all(e["homonym_flag"] is True for e in entries)
    assert all(e["kind"] == "fibf-business-capability" for e in entries)
    assert "homonym" in committed[CAPS]["homonym_note"]


def test_no_entry_comes_from_a_mitre_marked_document(harvest, committed):
    """FIBF-1 c, read straight from rights.yaml rather than through the
    tool: no entry names a document rights.yaml marks, and every marked
    document is listed as withheld."""
    rights = load(ROOT, RIGHTS)
    fibf = next(s for s in rights["sources"] if s["id"] == "fibf-2026-10-28")
    marked = {e["id"] for e in fibf["evidence"]
              if "MITRE" in (e.get("notices") or "")}
    assert len(marked) == 21
    for path in (FA, CAPS):
        used = {e["document"] for e in committed[path]["entries"]}
        assert not used & marked
    status = {d["evidence"]: d["status"]
              for d in committed[SNAPSHOT]["documents"]}
    assert all(status[m] != "harvested" for m in marked)


def test_a_withheld_document_is_listed_by_locator_and_digest_only(
        harvest, committed):
    allowed = harvest.WITHHELD_SNAPSHOT_KEYS
    withheld = [d for d in committed[SNAPSHOT]["documents"]
                if d["status"] != "harvested"]
    assert withheld
    for d in withheld:
        assert set(d) <= allowed, (d["evidence"], set(d) - allowed)
        assert set(d["rights_validation"]) <= \
            harvest.WITHHELD_VALIDATION_KEYS


def test_no_third_party_mapping_text_in_any_output(harvest, committed):
    """FIBF-2 a, as a negative check over every data value, independent
    of the tool's own walk."""
    def walk(value):
        if isinstance(value, dict):
            for v in value.values():
                yield from walk(v)
        elif isinstance(value, list):
            for v in value:
                yield from walk(v)
        elif isinstance(value, str):
            yield value

    for path, doc in committed.items():
        for text in walk(doc):
            assert not harvest.THIRD_PARTY.search(text), (path, text[:80])


def test_withheld_fields_carry_no_text(committed):
    for path in (FA, CAPS):
        for e in committed[path]["entries"]:
            for field in ("name", "description"):
                if isinstance(e[field], dict):
                    assert set(e[field]) == {"withheld"}, e["id"]
                    assert e["rights_status"] == \
                        "us-government-work-text-withheld"


def test_the_snapshot_is_rights_yamls_candidates(committed):
    rights = load(ROOT, RIGHTS)
    fibf = next(s for s in rights["sources"] if s["id"] == "fibf-2026-10-28")
    candidates = [(e["id"], e["sha256"]) for e in fibf["evidence"]
                  if e.get("snapshot") == "candidate"]
    listed = [(d["evidence"], d["sha256"])
              for d in committed[SNAPSHOT]["documents"]]
    assert listed == candidates
    assert len(listed) == 40


def test_duplicates_are_recorded_not_merged(committed):
    """FIBF-3 a: the two contract-writing workbooks are identical; both are
    kept, each naming the other, and both sets of entries are present."""
    docs = {d["evidence"]: d for d in committed[SNAPSHOT]["documents"]}
    assert docs["fibf-doc-cw-1"]["duplicate_of"] == ["fibf-doc-cw-2"]
    assert docs["fibf-doc-cw-2"]["duplicate_of"] == ["fibf-doc-cw-1"]
    for path in (FA, CAPS):
        used = {e["document"] for e in committed[path]["entries"]}
        assert {"fibf-doc-cw-1", "fibf-doc-cw-2"} <= used


def test_the_entries_are_dispositioned_as_third_party_text(disposition):
    rows = {r.path: r for r in disposition.classify()}
    for path in (BRM, FA, CAPS):
        assert rows[path].disposition == disposition.VENDORED, path
        assert rows[path].licence == "LicenseRef-US-Government-Work"
    assert rows[SNAPSHOT].disposition == disposition.CONTENT
    assert disposition.attribution_findings(list(rows.values())) == []


def test_i1_outputs_are_untouched(repo):
    """I-1's NOTICE.md is regenerated byte for byte by harvest_bpo.py and
    recorded in I-1's approval; this phase writes a notice of its own."""
    bpo = load_tool("bco_harvest_bpo_for_federal_test",
                    "tools/inventory/harvest_bpo.py")
    problems, _ = bpo.check(repo)
    assert problems == []


def test_ci_runs_the_check_and_the_weekly_confirmation(repo):
    workflow = yaml.safe_load((repo / ".github/workflows/checks.yml")
                              .read_bytes().decode("utf-8"))
    jobs = workflow["jobs"]
    main_runs = [s.get("run", "").strip() for s in jobs["checks"]["steps"]]
    assert "python tools/inventory/harvest_federal.py" in main_runs
    weekly = [s.get("run", "").strip() for s in jobs["vendored"]["steps"]]
    assert "python tools/inventory/harvest_federal.py --confirm" in weekly


# ------------------------------------------------------ broken copies


def test_a_snapshot_digest_other_than_rights_yamls_is_refused(harvest, copy):
    doc = load(copy, SNAPSHOT)
    doc["documents"][3]["sha256"] = "0" * 64
    rewrite(copy, SNAPSHOT, doc)
    assert_finding(findings(harvest, copy), "candidates")


def test_an_entry_digest_other_than_the_pin_is_refused(harvest, copy):
    doc = load(copy, FA)
    doc["entries"][0]["document_sha256"] = "f" * 64
    rewrite(copy, FA, doc)
    assert_finding(findings(harvest, copy), doc["entries"][0]["id"],
                   "rights.yaml pins")


def test_an_entry_without_a_locator_is_refused(harvest, copy):
    doc = load(copy, BRM)
    del doc["entries"][5]["locator"]
    rewrite(copy, BRM, doc)
    assert_finding(findings(harvest, copy), "has no 'locator'")


def test_an_empty_locator_is_refused(harvest, copy):
    doc = load(copy, FA)
    doc["entries"][0]["locator"] = {"sheet": "Somewhere"}
    rewrite(copy, FA, doc)
    assert_finding(findings(harvest, copy), "no usable locator")


def test_an_entry_from_a_withheld_document_is_refused(harvest, copy):
    """The negative fixture for FIBF-1 c: content attributed to a MITRE-
    marked workbook must never pass, whatever else is right about it."""
    rights = load(copy, RIGHTS)
    fibf = next(s for s in rights["sources"] if s["id"] == "fibf-2026-10-28")
    marked = next(e for e in fibf["evidence"] if e["id"] == "fibf-doc-hr-cb-2")
    doc = load(copy, FA)
    entry = doc["entries"][0]
    entry["document"] = marked["id"]
    entry["document_sha256"] = marked["sha256"]
    rewrite(copy, FA, doc)
    assert_finding(findings(harvest, copy), "fibf-doc-hr-cb-2",
                   "does not mark harvested")


def test_a_mitre_marked_document_marked_harvested_is_refused(harvest, copy):
    doc = load(copy, SNAPSHOT)
    record = first(doc["documents"], evidence="fibf-doc-mom-1")
    record["status"] = "harvested"
    doc["counts"]["harvested"] += 1
    doc["counts"]["withheld-mitre"] -= 1
    rewrite(copy, SNAPSHOT, doc)
    assert_finding(findings(harvest, copy), "fibf-doc-mom-1",
                   "records a MITRE notice")


def test_content_of_a_withheld_document_in_the_snapshot_is_refused(
        harvest, copy):
    doc = load(copy, SNAPSHOT)
    record = first(doc["documents"], evidence="fibf-doc-gm-1")
    record["entries"] = {"fibf-business-capability": 1}
    rewrite(copy, SNAPSHOT, doc)
    assert_finding(findings(harvest, copy), "fibf-doc-gm-1",
                   "locator, digest and status only")


def test_third_party_mapping_text_is_refused(harvest, copy):
    doc = load(copy, FA)
    doc["entries"][0]["description"] = "Mapped to an ITIL practice."
    rewrite(copy, FA, doc)
    assert_finding(findings(harvest, copy), "FIBF-2 a")


def test_a_capability_without_its_homonym_flag_is_refused(harvest, copy):
    doc = load(copy, CAPS)
    del doc["entries"][0]["homonym_flag"]
    rewrite(copy, CAPS, doc)
    assert_finding(findings(harvest, copy), "homonym flag")


def test_a_withheld_field_with_text_is_refused(harvest, copy):
    doc = load(copy, FA)
    entry = next(e for e in doc["entries"] if isinstance(e["name"], dict))
    entry["name"]["text"] = "the words that were withheld"
    rewrite(copy, FA, doc)
    assert_finding(findings(harvest, copy), entry["id"],
                   "a withheld field holds only")


def test_an_id_its_fields_do_not_produce_is_refused(harvest, copy):
    doc = load(copy, BRM)
    doc["entries"][0]["code"] = "999"
    rewrite(copy, BRM, doc)
    assert_finding(findings(harvest, copy), "is not an id its fields produce")


def test_counts_that_disagree_with_the_entries_are_refused(harvest, copy):
    doc = load(copy, FA)
    doc["counts"]["fibf-activity"] += 1
    rewrite(copy, FA, doc)
    assert_finding(findings(harvest, copy), "states counts")


def test_a_single_brm_document_is_refused(harvest, copy):
    doc = load(copy, BRM)
    doc["documents"] = doc["documents"][:1]
    rewrite(copy, BRM, doc)
    assert_finding(findings(harvest, copy), "BRM-2 c")


def test_an_edited_notice_is_refused(harvest, copy):
    path = copy / NOTICE
    path.write_bytes(path.read_bytes() + b"\nAn added line.\n")
    assert_finding(findings(harvest, copy), "NOTICE-federal.md", "edited")


def test_an_authored_namespace_iri_is_refused(harvest, copy):
    """The admission guard: the inventory mints nothing."""
    namespace = harvest.harvest_bpo_module(copy).authored_namespaces(copy)[0]
    doc = load(copy, FA)
    doc["entries"][0]["description"] = "see %sSomething" % namespace
    rewrite(copy, FA, doc)
    assert_finding(findings(harvest, copy), namespace)


def test_an_rdf_file_in_the_inventory_is_refused(harvest, copy):
    (copy / DIRECTORY / "fibf.ttl").write_bytes(b"@prefix ex: <x#> .\n")
    assert_finding(findings(harvest, copy), "fibf.ttl", "not YAML or Markdown")


def test_a_ratification_key_is_refused(harvest, copy):
    doc = load(copy, BRM)
    doc["entries"][0]["ratified_by"] = "someone"
    rewrite(copy, BRM, doc)
    assert_finding(findings(harvest, copy), "ratified_by")


# ------------------------------------------ the rules, on built workbooks


def workbook(sheets, shared=(), extra=None) -> bytes:
    """A minimal .xlsx: `sheets` is [(name, sheet XML body, footer)]."""
    ns = 'xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"'
    rel = ('xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/'
           'relationships"')
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as z:
        z.writestr("xl/workbook.xml", '<workbook %s %s><sheets>%s</sheets>'
                   '</workbook>' % (ns, rel, "".join(
                       '<sheet name="%s" sheetId="%d" r:id="rId%d"/>'
                       % (name, n + 1, n + 1)
                       for n, (name, _, _) in enumerate(sheets))))
        z.writestr("xl/_rels/workbook.xml.rels", (
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/'
            '2006/relationships">%s</Relationships>' % "".join(
                '<Relationship Id="rId%d" Target="worksheets/sheet%d.xml"/>'
                % (n + 1, n + 1) for n in range(len(sheets)))))
        for n, (_, body, footer) in enumerate(sheets):
            hf = ("<headerFooter><oddFooter>%s</oddFooter></headerFooter>"
                  % footer) if footer else ""
            z.writestr("xl/worksheets/sheet%d.xml" % (n + 1),
                       "<worksheet %s><sheetData>%s</sheetData>%s"
                       "</worksheet>" % (ns, body, hf))
        if shared:
            z.writestr("xl/sharedStrings.xml", "<sst %s>%s</sst>" % (ns, "".join(
                "<si><t>%s</t></si>" % s for s in shared)))
        for name, data in (extra or {}).items():
            z.writestr(name, data)
    return buffer.getvalue()


ROWS = ('<row r="1"><c r="A1" t="s"><v>0</v></c>'
        '<c r="B1" t="inlineStr"><is><t>Inline &amp; text</t></is></c>'
        '<c r="C1"><v>42</v></c><c r="D1" s="3"/></row>'
        '<row r="3"><c r="B3" t="s"><v>1</v></c></row>')


def test_the_reader_takes_shared_inline_and_cached_values(harvest):
    book = harvest.Workbook(workbook([("Data", ROWS, None)],
                                     shared=("Shared one", "Shared two")))
    sheet = book.sheet("Data")
    assert sheet.cells == {1: {1: "Shared one", 2: "Inline & text",
                               3: "42"}, 3: {2: "Shared two"}}


def test_merged_ranges_carry_their_top_left_value(harvest):
    body = ('<row r="1"><c r="A1" t="inlineStr"><is><t>Group</t></is></c>'
            '</row>')
    data = workbook([("M", body, None)])
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        parts = {n: z.read(n) for n in z.namelist()}
    parts["xl/worksheets/sheet1.xml"] = parts[
        "xl/worksheets/sheet1.xml"].replace(
        b"</sheetData>", b'</sheetData><mergeCells count="1">'
        b'<mergeCell ref="A1:A3"/></mergeCells>')
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as z:
        for name, blob in parts.items():
            z.writestr(name, blob)
    cells = harvest.Workbook(buffer.getvalue()).sheet("M").cells
    assert [cells[r][1] for r in (1, 2, 3)] == ["Group"] * 3


def test_a_mitre_footer_is_a_notice(harvest):
    """The bytes test FIBF-1 c rests on, positive and negative."""
    marked = harvest.Workbook(workbook(
        [("S", ROWS, "&C(c) 2021 The MITRE Corporation")],
        shared=("a b", "c d")))
    clean = harvest.Workbook(workbook([("S", ROWS, "&CPage &P")],
                                      shared=("a b", "c d")))
    assert harvest.workbook_rights(marked)["mitre_parts"]
    assert harvest.workbook_rights(clean)["mitre_parts"] == []
    assert harvest.workbook_rights(clean)["other_notices"] == []


def test_a_copyright_line_without_mitre_is_still_a_notice(harvest):
    book = harvest.Workbook(workbook(
        [("S", ROWS, "&CCopyright 2020 Someone Else")], shared=("a", "b")))
    rights = harvest.workbook_rights(book)
    assert rights["mitre_parts"] == []
    assert rights["other_notices"] == ["copyright"]


def test_an_external_link_target_is_counted_not_read_as_a_notice(harvest):
    rels = ('<Relationships xmlns="http://schemas.openxmlformats.org/package/'
            '2006/relationships"><Relationship Id="rId1" Target="https://'
            'share.mitre.example/x.xlsx" TargetMode="External"/>'
            '</Relationships>')
    book = harvest.Workbook(workbook(
        [("S", ROWS, None)], shared=("a", "b"),
        extra={"xl/externalLinks/_rels/externalLink1.xml.rels": rels}))
    rights = harvest.workbook_rights(book)
    assert rights["mitre_parts"] == []
    assert rights["external_links_to_mitre_host"] == 1


def test_text_shared_with_a_mitre_workbook_is_withheld(harvest):
    withhold = harvest.Withholding({harvest.norm("Plan the Records Work")})
    counter = {}
    assert withhold.field("plan the records-work.", counter) == {
        "withheld": "text-in-mitre-marked-document"}
    # One word is not text anyone could own; it stays.
    one = harvest.Withholding({harvest.norm("Records")})
    assert one.field("Records", counter) == "Records"
    # And different words stay, of course.
    assert withhold.field("Plan the budget", counter) == "Plan the budget"
    assert counter == {"text-in-mitre-marked-document": 1}


def test_a_long_mitre_cell_inside_a_field_is_withheld(harvest):
    # A whole MITRE-marked cell of six words or more, inside a longer field.
    cell = "measure the impact of a finding uniformly"
    withhold = harvest.Withholding({harvest.norm(cell)})
    counter = {}
    assert withhold.field("Develop an approach to " + cell.upper() + ".",
                          counter) == {"withheld": "text-in-mitre-marked-document"}
    # Word by word: a cell inside a longer word does not count.
    assert withhold.field("Premeasure the impact of a finding uniformly",
                          counter) == \
        "Premeasure the impact of a finding uniformly"
    # Five words is a name, not text: it stays.
    name = harvest.Withholding(
        {harvest.norm("Work Schedule and Leave Management")})
    assert name.field("Maintain Work Schedule and Leave Management records",
                      counter) == \
        "Maintain Work Schedule and Leave Management records"
    assert counter == {"text-in-mitre-marked-document": 1}


def test_third_party_names_and_mapping_cells_are_withheld(harvest):
    withhold = harvest.Withholding(set())
    withhold.third = {harvest.norm("Enterprise Data Center")}
    counter = {}
    assert withhold.field("Enterprise Data Center ", counter) == {
        "withheld": "third-party-mapping-text"}
    assert withhold.field("Aligned to the TBM taxonomy", counter) == {
        "withheld": "third-party-mapping-text"}
    assert withhold.field("Secure the data center", counter) == \
        "Secure the data center"
    assert counter == {"third-party-mapping-text": 2}


def test_a_mapping_column_is_found_and_a_mention_is_not(harvest):
    body = ('<row r="1"><c r="A1" t="inlineStr"><is><t>Activity</t></is></c>'
            '<c r="B1" t="inlineStr"><is><t>Reference</t></is></c></row>'
            + "".join(
                '<row r="%d"><c r="A%d" t="inlineStr"><is><t>%s</t></is></c>'
                '<c r="B%d" t="inlineStr"><is><t>ITIL practice %d</t></is>'
                '</c></row>' % (r, r, "Technology Business Management"
                                if r == 5 else "Activity %d" % r, r, r)
                for r in range(4, 10)))
    book = harvest.Workbook(workbook([("FA", body, None)]))
    found, texts = harvest.third_party_columns(book, "doc", {("FA", 1)})
    by_column = {f["column"]: f for f in found}
    assert by_column["B"]["mapping"] is True
    assert by_column["A"] == {"sheet": "FA", "column": "A", "mapping": False,
                              "harvested": True}
    assert harvest.norm("ITIL practice 4") in texts
    assert harvest.norm("Activity 4") not in texts


def test_the_mitre_check_fires_on_shared_text(harvest, committed):
    """The rebuild-time negative check, with a positive control."""
    names = {"functions": FA, "capabilities": CAPS}
    contents = {FA: (ROOT / FA).read_bytes(), CAPS: (ROOT / CAPS).read_bytes()}
    assert harvest.mitre_findings(contents, names, set()) == []
    entry = next(e for e in committed[CAPS]["entries"]
                 if isinstance(e["description"], str))
    texts = {harvest.norm(entry["description"])}
    found = harvest.mitre_findings(contents, names, texts)
    assert any(entry["id"] in f and "FIBF-1 c" in f for f in found), found


def test_fetch_refuses_another_host(harvest):
    with pytest.raises(SystemExit):
        harvest.fetch("https://www.apqc.org/anything")
    with pytest.raises(SystemExit):
        harvest.fetch("http://ussm.gsa.gov/fibf/")


def test_codes_are_split_from_names_as_published(harvest):
    assert harvest.split_code("HCM.A5-1.010 Compensation Strategy") == (
        "HCM.A5-1.010", "Compensation Strategy")
    assert harvest.split_code("ERM.010.010 - Records Creation") == (
        "ERM.010.010", "Records Creation")
    assert harvest.split_code("Throughout process") == (
        None, "Throughout process")


# ------------------------------------- the real harvest, when cached


def _cache_ready(harvest):
    try:
        import pypdf  # noqa: F401
    except ImportError:
        return False
    pinned = harvest.pins(ROOT)
    cache = ROOT / harvest.CACHE
    items = pinned["brm"]["items"] + pinned["fibf"]["items"] + list(
        pinned["fibf"]["pages"].values())
    for source in (pinned["brm"], pinned["fibf"]):
        items += [source["evidence"][ref] for ref in source["context"]]
    return all((cache / i["sha256"]).is_file() for i in items)


def test_a_rebuild_from_the_pinned_bytes_is_byte_identical(harvest):
    """Reproducibility, and the MITRE negative check over the real bytes
    (build() refuses outputs that publish a MITRE-marked workbook's text).
    Needs the gitignored cache; CI's weekly --confirm fetches instead."""
    if not _cache_ready(harvest):
        pytest.skip("the pinned documents are not in .upstream-cache/i2a/")
    built, evidence = harvest.build(ROOT / harvest.CACHE, ROOT)
    for path, data in built.items():
        assert data == (ROOT / path).read_bytes(), path
    assert evidence["findings"] == []
