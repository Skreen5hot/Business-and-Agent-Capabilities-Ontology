# SPDX-License-Identifier: MIT
"""The I-2a rights review's check refuses what it says it refuses.

tools/inventory/rights.py checks docs/sources/inventory/rights.yaml
offline, and with --confirm refetches every pinned document. The offline
check is tested against the committed record, and then against copies in
tmp_path broken one rule at a time: each mutation is asserted to have
changed the bytes before the check runs, and each failure is required to
be the finding for that rule (docs/process/PROCESS.md section 2). The
network half is tested with the fetch replaced, so it runs offline; the
real refetch is the weekly CI job's.
"""

from __future__ import annotations

import pytest
import yaml

from conftest import ROOT, load_tool

TOOL = "tools/inventory/rights.py"
RIGHTS = "docs/sources/inventory/rights.yaml"
AUTHORITY = "docs/decisions/2026-10-28-i2-and-bpo-repin-decided.md"
COPIED = (RIGHTS, "docs/sources/register.yaml", "tools/ontology/validate.py",
          "tools/inventory/harvest_bpo.py", AUTHORITY,
          "docs/proposals/2026-10-28-inventory-i2-public-catalogs.md")


@pytest.fixture(scope="module")
def rights():
    return load_tool("bco_inventory_rights", TOOL)


@pytest.fixture
def copy(tmp_path):
    for relative in COPIED:
        target = tmp_path / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes((ROOT / relative).read_bytes())
    return tmp_path


def load(base):
    return yaml.safe_load((base / RIGHTS).read_bytes().decode("utf-8"))


def rewrite(base, data):
    """Write `data` back as YAML, and prove the bytes moved."""
    before = (base / RIGHTS).read_bytes()
    after = yaml.safe_dump(data, sort_keys=False,
                           allow_unicode=True).encode("utf-8")
    assert after != before
    (base / RIGHTS).write_bytes(after)


def findings(rights, base):
    problems, _ = rights.check(base)
    return problems


def source(data, sid):
    for item in data["sources"]:
        if item["id"] == sid:
            return item
    raise AssertionError("no source %s" % sid)


def refused(rights, base, needle):
    problems = findings(rights, base)
    assert any(needle in p for p in problems), problems
    return problems


# ------------------------------------------------------- the real record


def test_the_committed_record_passes(rights):
    problems, counts = rights.check(ROOT)
    assert problems == [], problems
    # Guard the guard: a check over an empty record would pass too.
    assert counts["sources"] >= 4 and counts["evidence"] > 40
    assert set(counts["status"].values()) <= set(rights.STATUSES)


def test_every_source_ends_undecided(rights):
    """I-2a decides nothing: the architect's act fills these, elsewhere."""
    for item in load(ROOT)["sources"]:
        assert item["architect_decision"] is None, item["id"]
        assert item["decision_points"], item["id"]


def test_every_evidence_item_is_pinned_by_digest(rights):
    """Read directly, not through the tool's own check."""
    for item in load(ROOT)["sources"]:
        for evidence in item["evidence"]:
            assert rights.HEX64.match(evidence["sha256"]), evidence["id"]


def test_the_copy_is_clean_before_anything_is_broken(rights, copy):
    assert findings(rights, copy) == []


def test_the_record_is_dispositioned_as_this_repositorys_content(
        disposition):
    rows = {r.path: r for r in disposition.classify()}
    assert rows[RIGHTS].disposition == disposition.CONTENT
    assert rows[TOOL].disposition == disposition.SOFTWARE


def test_the_inventory_admission_guard_still_holds_with_the_record(repo):
    harvest = load_tool("bco_harvest_bpo_for_rights_test",
                        "tools/inventory/harvest_bpo.py")
    assert harvest.admission_findings(repo, "docs/sources/inventory",
                                      {}) == []


def test_ci_runs_the_check_and_the_weekly_confirmation(repo):
    workflow = yaml.safe_load((repo / ".github/workflows/checks.yml")
                              .read_bytes().decode("utf-8"))
    jobs = workflow["jobs"]
    main_runs = [s.get("run", "").strip() for s in jobs["checks"]["steps"]]
    assert "python tools/inventory/rights.py" in main_runs
    weekly = [s.get("run", "").strip() for s in jobs["vendored"]["steps"]]
    assert "python tools/inventory/rights.py --confirm" in weekly


# --------------------------------------------------------- evidence rules


def test_evidence_without_a_digest_is_refused(rights, copy):
    data = load(copy)
    del source(data, "feaf-brm-3.1")["evidence"][1]["sha256"]
    rewrite(copy, data)
    refused(rights, copy, "has no sha256")


def test_a_malformed_digest_is_refused(rights, copy):
    data = load(copy)
    source(data, "feaf-brm-3.1")["evidence"][1]["sha256"] = "0e6e24b6"
    rewrite(copy, data)
    refused(rights, copy, "has no sha256")


def test_evidence_without_a_retrieval_date_is_refused(rights, copy):
    data = load(copy)
    source(data, "feaf-brm-3.1")["evidence"][0]["retrieved"] = "October"
    rewrite(copy, data)
    refused(rights, copy, "no retrieval date")


def test_evidence_without_what_was_checked_is_refused(rights, copy):
    data = load(copy)
    source(data, "feaf-brm-3.1")["evidence"][0]["checked"] = ""
    rewrite(copy, data)
    refused(rights, copy, "does not say what was checked")


def test_a_secondary_source_is_refused(rights, copy):
    """E6: never a transcription on Wikipedia or CIO-Wiki."""
    data = load(copy)
    source(data, "feaf-brm-3.1")["evidence"][1]["url"] = (
        "https://en.wikipedia.org/wiki/Federal_enterprise_architecture")
    rewrite(copy, data)
    refused(rights, copy, "Primary evidence comes from")


def test_browser_text_without_its_normalisation_is_refused(rights, copy):
    data = load(copy)
    del source(data, "apqc-pcf-7.4")["evidence"][1]["normalisation"]
    rewrite(copy, data)
    refused(rights, copy, "no 'normalisation'")


def test_bpo_evidence_without_a_full_commit_is_refused(rights, copy):
    data = load(copy)
    source(data, "apqc-pcf-7.4")["evidence"][0]["commit"] = "bc64e91"
    rewrite(copy, data)
    refused(rights, copy, "no 40-hex BPO commit")


def test_a_member_without_a_digest_is_refused(rights, copy):
    data = load(copy)
    source(data, "apqc-pcf-7.4")["evidence"][0]["members"][0]["sha256"] = ""
    rewrite(copy, data)
    refused(rights, copy, "members/0 has no sha256")


# ------------------------------------------------------ status and schema


def test_an_unknown_status_is_refused(rights, copy):
    data = load(copy)
    source(data, "feaf-brm-3.1")["status"] = "approved"
    rewrite(copy, data)
    refused(rights, copy, "has status 'approved'")


def test_a_gap_without_a_reason_is_refused(rights, copy):
    data = load(copy)
    source(data, "apqc-pcf-8.0")["gap_reason"] = None
    rewrite(copy, data)
    refused(rights, copy, "is gap with no gap_reason")


def test_a_deferred_source_without_a_reason_is_refused(rights, copy):
    data = load(copy)
    item = source(data, "feaf-brm-3.1")
    item["status"] = "deferred"
    rewrite(copy, data)
    refused(rights, copy, "is deferred with no gap_reason")


def test_a_complete_source_with_a_gap_reason_is_refused(rights, copy):
    data = load(copy)
    source(data, "feaf-brm-3.1")["gap_reason"] = "something is missing"
    rewrite(copy, data)
    refused(rights, copy, "evidence-complete but states a gap_reason")


def test_ambiguous_terms_without_a_question_are_refused(rights, copy):
    data = load(copy)
    source(data, "apqc-pcf-7.4")["open_questions"] = []
    rewrite(copy, data)
    refused(rights, copy, "calls its terms ambiguous")


def test_an_unknown_register_id_is_refused(rights, copy):
    data = load(copy)
    source(data, "feaf-brm-3.1")["register"] = "SRC-GOV-%d" % 99  # built, so the register scan sees no id
    rewrite(copy, data)
    refused(rights, copy, "which docs/sources/register.yaml does not hold")


def test_a_repeated_source_is_refused(rights, copy):
    data = load(copy)
    data["sources"].append(dict(source(data, "feaf-brm-3.1")))
    rewrite(copy, data)
    refused(rights, copy, "repeats source id 'feaf-brm-3.1'")


def test_a_decision_point_with_one_option_is_refused(rights, copy):
    data = load(copy)
    point = source(data, "feaf-brm-3.1")["decision_points"][0]
    point["options"] = point["options"][:1]
    rewrite(copy, data)
    refused(rights, copy, "a decision needs at least two")


def test_an_architect_decision_must_point_at_a_record(rights, copy):
    data = load(copy)
    source(data, "feaf-brm-3.1")["architect_decision"] = {
        "record": "docs/decisions/2099-01-01-not-made.md"}
    rewrite(copy, data)
    refused(rights, copy, "which is not a decision record")


def test_an_architect_decision_pointing_at_a_record_is_accepted(rights,
                                                                copy):
    """The positive control for the refusal above: the field is for the
    architect's act, and a pointer to a real record is what it holds."""
    data = load(copy)
    source(data, "feaf-brm-3.1")["architect_decision"] = {"record": AUTHORITY}
    rewrite(copy, data)
    assert findings(rights, copy) == []


# --------------------------------------------------------- catalog content


def test_an_unknown_key_is_refused(rights, copy):
    data = load(copy)
    source(data, "feaf-brm-3.1")["sectors"] = ["a sector"]
    rewrite(copy, data)
    refused(rights, copy, "which the rights record does not define")


def test_a_catalog_field_is_refused_wherever_it_is(rights, copy):
    data = load(copy)
    source(data, "fibf-2026-10-28")["evidence"][0]["activities"] = ["x"]
    rewrite(copy, data)
    refused(rights, copy, "I-2a writes no catalog content")


def test_findings_topics_are_not_mistaken_for_catalog_fields(rights):
    """`names` under findings is the topic of a finding; elsewhere it is a
    catalog field. The committed record uses the first, and passes."""
    assert "names" in rights.CATALOG_KEYS
    assert "names" in load(ROOT)["sources"][0]["findings"]


@pytest.mark.parametrize("code", ["10.2.3", "FFM.090", "B10.808.034"])
def test_a_catalog_code_in_prose_is_refused(rights, copy, code):
    data = load(copy)
    item = source(data, "feaf-brm-3.1")
    item["open_questions"].append("What does %s mean?" % code)
    rewrite(copy, data)
    refused(rights, copy, "needs no catalog codes")


def test_a_quote_over_fifteen_words_is_refused(rights, copy):
    data = load(copy)
    source(data, "feaf-brm-3.1")["quotes"][0]["quote"] = " ".join(
        ["word"] * 16)
    rewrite(copy, data)
    refused(rights, copy, "quotes 16 words")


def test_a_quote_of_fifteen_words_is_accepted(rights, copy):
    data = load(copy)
    source(data, "feaf-brm-3.1")["quotes"][0]["quote"] = " ".join(
        ["word"] * 15)
    rewrite(copy, data)
    assert findings(rights, copy) == []


@pytest.mark.parametrize("mark", ['"', "“"])
def test_a_quotation_outside_a_quote_field_is_refused(rights, copy, mark):
    data = load(copy)
    item = source(data, "feaf-brm-3.1")
    item["findings"]["names"] += " The page says %sfree%s." % (mark, mark)
    rewrite(copy, data)
    refused(rights, copy, "contains a quotation mark")


def test_a_quote_from_unlisted_evidence_is_refused(rights, copy):
    data = load(copy)
    source(data, "feaf-brm-3.1")["quotes"][0]["evidence"] = "apqc74-workbook"
    rewrite(copy, data)
    refused(rights, copy, "which this source's evidence does not list")


# ------------------------------------------------------ admission guard


def test_an_authored_namespace_iri_is_refused(rights, copy):
    namespace = rights.harvest_module(copy).authored_namespaces(copy)[0]
    data = load(copy)
    source(data, "feaf-brm-3.1")["open_questions"].append(
        "Should it be %sBusinessFunction?" % namespace)
    rewrite(copy, data)
    refused(rights, copy, "authored namespaces")


def test_rdf_in_the_record_is_refused(rights, copy):
    """A Turtle line inside a folded scalar is still RDF text in the file,
    whatever the YAML around it says."""
    path = copy / RIGHTS
    before = path.read_bytes()
    after = before.replace(b"scope_note: >-\n",
                           b"scope_note: >-\n  @prefix owl: <x> .\n", 1)
    assert after != before
    path.write_bytes(after)
    refused(rights, copy, "reads as an RDF serialization")


def test_a_ratification_key_is_refused(rights, copy):
    data = load(copy)
    source(data, "feaf-brm-3.1")["findings"]["attribution"][
        "ratified_by"] = "someone"
    rewrite(copy, data)
    refused(rights, copy, "A ratification or vocabulary field")


def test_crlf_is_refused(rights, copy):
    path = copy / RIGHTS
    path.write_bytes(path.read_bytes().replace(b"\n", b"\r\n"))
    with pytest.raises(rights.Refused) as error:
        rights.check(copy)
    assert "CRLF" in str(error.value)


def test_unparseable_yaml_is_refused(rights, copy):
    path = copy / RIGHTS
    path.write_bytes(path.read_bytes() + b"sources: [\n")
    with pytest.raises(rights.Refused) as error:
        rights.check(copy)
    assert "does not parse as YAML" in str(error.value)


# ----------------------------------------------------------- the network


@pytest.mark.parametrize("url", [
    "https://www.apqc.org/terms-of-service",
    "http://ussm.gsa.gov/fibf/",
    "https://en.wikipedia.org/wiki/Federal_enterprise_architecture",
])
def test_fetch_refuses_hosts_it_may_not_reach(rights, url):
    with pytest.raises(rights.Refused):
        rights._get(url)


def test_confirm_reports_a_document_that_changed(rights, copy, tmp_path,
                                                 monkeypatch):
    """With the fetch replaced by one serving other bytes, every fetched
    pin is a finding, browser text is skipped, and nothing is trusted from
    the cache."""
    monkeypatch.setenv("BCO_BPO_CLONE", str(tmp_path / "no-clone"))
    monkeypatch.setattr(rights, "bpo_clone", lambda base: None)
    monkeypatch.setattr(rights, "_get", lambda url: b"not the document")
    cache = tmp_path / "cache"
    problems = rights.confirm(copy, cache)
    fetched = sum(1 for s in load(copy)["sources"] for e in s["evidence"]
                  if e["kind"] != "browser-text")
    assert len(problems) == fetched
    assert all("no longer served" in p for p in problems)
    assert not any("apqc-terms-of-service" in p for p in problems)


def test_confirm_ignores_a_cached_copy_of_a_live_document(rights, copy,
                                                          tmp_path,
                                                          monkeypatch):
    """A cached file with the pinned digest must not stand in for the
    network: the run exists to see the publisher's current bytes."""
    data = load(copy)
    item = source(data, "feaf-brm-3.1")["evidence"][0]
    cache = tmp_path / "cache"
    cache.mkdir()
    (cache / item["sha256"]).write_bytes(b"cached")
    seen = []
    monkeypatch.setattr(rights, "bpo_clone", lambda base: None)

    def fake(url):
        seen.append(url)
        return b"served now"

    monkeypatch.setattr(rights, "_get", fake)
    rights.confirm(copy, cache)
    assert item["url"] in seen
