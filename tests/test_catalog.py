# SPDX-License-Identifier: MIT
"""Phase I-4: the Candidate Capability Catalog and its crosswalk.

Directed on 2026-11-03
(docs/decisions/2026-11-03-bulk-capability-synthesis-directed.md). The
normalizer is tested on made-up labels ("Synthetic widgets"), one rule at a
time. The synthesis is tested on the committed inventories: the committed
catalog must be the generator's output, its counts must be the catalog's
own, and every hard check must refuse a catalog broken in the way it names,
with the unbroken catalog beside it as the positive control
(docs/process/PROCESS.md section 2).
"""

from __future__ import annotations

import copy
import re

import pytest
import yaml

from conftest import ROOT, load_tool

TOOL = "tools/catalog/synthesize.py"
DISPOSITIONS = "docs/catalog/dispositions.yaml"
#: Where reviewers cite candidates by identifier: each one cited is pinned.
REVIEW_RECORDS = ("docs/catalog/tranche-1.md", "docs/catalog/admission", "docs/decisions")
CATALOG = "docs/catalog/candidates.yaml"
CROSSWALK = "docs/catalog/crosswalk.yaml"
REPORT = "docs/catalog/report.md"
INVENTORY_FILES = (
    "docs/sources/inventory/bpo-entries.yaml",
    "docs/sources/inventory/pcf-7.4-entries.yaml",
    "docs/sources/inventory/feaf-brm-entries.yaml",
    "docs/sources/inventory/fibf-entries.yaml",
    "docs/sources/inventory/fibf-business-capabilities.yaml",
)
CLASSES = {"capability", "process", "skill", "function", "role", "requirement",
           "unresolved"}


@pytest.fixture(scope="module")
def tool():
    return load_tool("catalog_synthesize", TOOL)


@pytest.fixture(scope="module")
def built(tool):
    """The pipeline run once on the committed inputs, its parts kept."""
    docs = {k: tool.load_yaml(ROOT, p) for k, p in tool.INPUTS.items()}
    acts = tool.load_yaml(ROOT, tool.ACTS)
    s = tool.synthesize(ROOT, docs, acts)
    tool.overlaps(s)
    tool.classify(s)
    catalog = tool.describe(s)
    xwalk = tool.crosswalk_rows(s, {c["key"]: c["id"] for c in catalog})
    return {"s": s, "catalog": catalog, "xwalk": xwalk, "docs": docs}


@pytest.fixture(scope="module")
def committed():
    load = lambda p: yaml.load((ROOT / p).read_text(encoding="utf-8"),
                               Loader=getattr(yaml, "CSafeLoader", yaml.SafeLoader))
    return load(CATALOG), load(CROSSWALK)


# ------------------------------------------------------------ normalizer


def test_imperative_label_gives_verbs_family_and_object(tool):
    f = tool.frame_label("Develop and manage synthetic widgets", "label")
    assert f.verbs == ("develop", "manage")
    assert f.family == "development"
    assert f.object == "synthetic widgets"
    assert f.key == "development|synthetic widget"


def test_a_planned_object_makes_develop_formulation(tool):
    assert tool.frame_label("Develop synthetic widget strategy", "label").family == \
        "formulation"
    assert tool.frame_label("Develop synthetic widgets", "label").family == "development"


def test_a_light_verb_yields_to_its_nominal(tool):
    f = tool.frame_label("Perform synthetic widget accounting", "label")
    assert (f.family, f.object) == ("accounting", "synthetic widget")


def test_noun_phrase_label_reads_its_trailing_nominal(tool):
    f = tool.frame_label("Synthetic Widget Disposal Approval", "label")
    assert f.family == "governance" and f.object == "synthetic widget disposal"
    assert f.bounded


def test_a_second_clause_ends_the_object(tool):
    f = tool.frame_label("Operate widgets and monitor synthetic gadgets", "label")
    assert f.object == "widgets"
    control = tool.frame_label("Operate widgets and test rigs", "label")
    assert control.object == "widgets and test rigs"   # "test" may be a noun


def test_an_artifact_label_is_marked_inferred(tool):
    f = tool.frame_label("Synthetic Widget Plan", "label")
    assert f.inferred and f.family == "formulation"
    assert not tool.frame_label("Synthetic Widget Planning", "label").inferred


def test_relations_with_name_the_party(tool):
    f = tool.frame_label("Manage relations with synthetic widget makers", "label")
    assert (f.family, f.object) == ("relationship", "synthetic widget makers")


def test_acronyms_expand_once(tool):
    assert tool.tokens("Manage IT assets") == ["manage", "information", "technology",
                                               "assets"]
    assert tool.tokens("human resources information systems HRIS")[-1] == "systems"


def test_sentences_stop_at_a_clause(tool):
    f = tool.frame_sentence("Determine if the synthetic widget is ready.")
    assert f is None
    f = tool.frame_sentence("Validate synthetic widgets against the register.")
    assert f.object == "synthetic widgets"


def test_a_label_naming_only_its_ability_is_circular(tool):
    # "Synthetic procurement" would read "obtain ... procurement": the
    # object is the ability itself (found by the product owner on
    # BCC-cc2de1a5, 2026-11-03).
    assert tool.circular("procurement", "acquisition")
    assert tool.circular("certification and accreditation", "verification")
    assert not tool.circular("synthetic widgets", "acquisition")
    assert not tool.circular("payments", "governance")   # approving payments


def test_an_adjective_left_alone_keeps_its_ability_noun(tool):
    # "National Defense" read "protect national" (I-4 assessment, defect 3).
    f = tool.frame_label("Synthetic National Defense", "label")
    assert f.qualified and f.object == "synthetic national defense"
    assert f.as_dict()["qualified"] is True
    control = tool.frame_label("Synthetic Widget Defense", "label")
    assert not control.qualified and control.object == "synthetic widget"
    assert "qualified" not in control.as_dict()


def test_a_pinned_key_keeps_its_identifier(tool):
    key = "development|synthetic widget"
    assert tool.candidate_id(key) == "BCC-" + tool.sha256(key.encode())[:8]
    assert tool.candidate_id(key, {key: "BCC-00000001"}) == "BCC-00000001"
    assert tool.candidate_id("development|other", {key: "BCC-00000001"}) != "BCC-00000001"


def test_overlaps_beyond_the_limit_are_counted(tool):
    n = tool.OVERLAP_LIMIT + 2
    cands = {"f%d|synthetic widget" % i: {"broader": {}, "narrower": {}} for i in range(n)}
    tool.overlaps({"cands": cands})
    c = cands["f0|synthetic widget"]
    assert len(c["overlaps"]) == tool.OVERLAP_LIMIT and c["overlaps_found"] == n - 1


def test_no_unflagged_candidate_has_a_circular_differentia(committed):
    cat, _ = committed
    for x in cat["candidates"]:
        if x["review"]["status"] == "generated-draft":
            assert not any("circular" in f for f in x["review"]["flags"])
    procurement = next(x for x in cat["candidates"] if x["id"] == "BCC-cc2de1a5")
    assert procurement["review"]["status"] == "needs-review"
    assert "obtain procurement" not in procurement["definition"]["text"]


def test_an_approval_in_the_evidence_is_flagged_deontic(committed):
    cat, _ = committed
    by = {x["id"]: x for x in cat["candidates"]}
    # Payments Approval: both its acts approve or authorize (G1-T q4).
    assert any("deontic" in f for f in by["BCC-9ecf360b"]["review"]["flags"])
    assert by["BCC-9ecf360b"]["review"]["generated"]["status"] == "needs-review"
    # Positive control: complaint handling has no approval act.
    assert not any("deontic" in f for f in by["BCC-373b146e"]["review"]["flags"])


def test_recorded_dispositions_govern_and_keep_the_generated_status(committed):
    cat, _ = committed
    by = {x["id"]: x for x in cat["candidates"]}
    rejected = by["BCC-9ecf360b"]["review"]          # Payments Approval
    assert rejected["status"] == rejected["disposition"]["status"] == "rejected"
    assert rejected["disposition"]["record"].startswith(
        "docs/decisions/2026-11-04-i5-tranche-1-approved-for-evaluation.md")
    assert rejected["generated"]["status"] == "needs-review"
    retired = by["BCC-b7c46718"]["review"]           # BRM Payroll
    assert retired["status"] == "retired" and retired["disposition"]["into"] == "BCC-d95f68fd"
    assert by["BCC-d95f68fd"]["review"]["retired_into_it"] == ["BCC-b7c46718"]
    # Provenance: the retired candidate keeps both its BRM source records.
    assert len(by["BCC-b7c46718"]["sources"]) == 2
    # Positive control: an undisposed candidate has no disposition.
    assert "disposition" not in by["BCC-373b146e"]["review"]
    assert cat["counts"]["recorded_dispositions"] == 2


def test_every_reviewed_candidate_is_pinned(committed):
    cat, _ = committed
    doc = yaml.safe_load((ROOT / DISPOSITIONS).read_text(encoding="utf-8"))
    pins = {p["id"]: p["key"] for p in doc["pins"]}
    cited = set()
    for rel in REVIEW_RECORDS:
        path = ROOT / rel
        for f in ([path] if path.is_file() else sorted(path.glob("*.md"))):
            cited |= set(re.findall(r"BCC-[0-9a-f]{8}", f.read_text(encoding="utf-8")))
    assert {"BCC-373b146e", "BCC-d95f68fd", "BCC-62e789bf"} <= cited
    assert cited <= set(pins), sorted(cited - set(pins))
    by = {x["id"]: x for x in cat["candidates"]}
    for pid, key in pins.items():
        assert by[pid]["key"] == key
    assert {d["id"] for d in doc["dispositions"]} <= set(pins)


def test_no_ability_phrase_ends_in_a_bare_adjective(tool, committed):
    cat, _ = committed
    flagged = 0
    for x in cat["candidates"]:
        ability = x["distinctive_ability"]["ability"]
        assert not ability.startswith("carry out other ")
        assert ability.split()[-1] not in tool.ADJECTIVES, (x["id"], ability)
        if tool.QUALIFIED in x["review"]["flags"]:
            flagged += 1
            assert ability.startswith("carry out ")
            assert x["review"]["status"] != "generated-draft"
    assert flagged
    by = {x["name"]: x for x in cat["candidates"]}
    assert by["National Defense Capability"]["distinctive_ability"]["ability"] == \
        "carry out national defense"
    assert by["Public Relationship Management Capability"]["distinctive_ability"][
        "ability"] == "build and sustain public relationships"


def test_a_truncated_overlap_list_says_so(committed):
    cat, _ = committed
    cut = [x for x in cat["candidates"] if "overlaps_truncated" in x]
    assert cut and cat["counts"]["overlap_lists_truncated"] == len(cut)
    for x in cat["candidates"]:
        t = x.get("overlaps_truncated")
        if t:
            assert t["shown"] == len(x["overlaps"]) and t["found"] > t["shown"]
    report = (ROOT / REPORT).read_text(encoding="utf-8")
    assert "overlap list is cut at 6" in report and "| %d |" % len(cut) in report


def test_fibf_codes_are_padded_for_matching(tool):
    assert tool.norm_code("TRT.010.70") == tool.norm_code("TRT.010.070")


# ------------------------------------------------------------ the catalog


def test_committed_catalog_is_the_generators_output(tool):
    assert tool.check(ROOT) == []


def test_every_source_record_is_in_the_crosswalk_once(committed):
    _, xw = committed
    want = []
    for path in INVENTORY_FILES:
        want += [e["id"] for e in yaml.safe_load(
            (ROOT / path).read_text(encoding="utf-8"))["entries"]]
    got = [r["inventory_id"] for r in xw["records"]]
    assert sorted(got) == sorted(want)
    for r in xw["records"]:
        assert r["interpretations"] or r["no_interpretation"]


def test_counts_are_the_catalogs_own(committed):
    cat, xw = committed
    c, cands = cat["counts"], cat["candidates"]
    assert c["unique_candidates"] == len(cands)
    assert c["candidates_generated"] == sum(len(x["sources"]) for x in cands)
    assert c["likely_bfo_cco_capabilities"] == sum(
        1 for x in cands if x["bfo_cco_compatibility"] == "likely")
    assert c["rejected_or_deferred"] == sum(
        1 for x in cands if x["review"]["status"] in ("rejected", "deferred"))
    assert c["records_lacking_interpretation"] == sum(
        1 for r in xw["records"] if not r["interpretations"])
    assert c["source_records_processed"]["total"] == len(xw["records"])
    report = (ROOT / REPORT).read_text(encoding="utf-8")
    assert "| Unique candidates after deduplication | %d |" % len(cands) in report


def test_every_candidate_has_the_directed_fields(committed):
    cat, _ = committed
    for x in cat["candidates"]:
        assert re.fullmatch(r"BCC-[0-9a-f]{8}", x["id"])
        assert x["name"] and x["definition"]["genus"] and x["definition"]["differentia"]
        assert x["bearer"]["proposed"] and x["distinctive_ability"]["ability"]
        assert x["sources"] and "realization_evidence" in x
        assert "broader" in x and "narrower" in x and "overlaps" in x and "synonyms" in x
        assert x["classification"] in CLASSES and x["classification_reason"]
        assert x["review"]["status"] and x["review"]["justification"]
        if x["bfo_cco_compatibility"] == "likely":
            assert x["realization_evidence"]["act_types"] or any(
                "narrower" in f for f in x["review"]["flags"])


def test_identifiers_are_not_iris_and_nothing_is_minted(committed):
    text = (ROOT / CATALOG).read_text(encoding="utf-8")
    assert "fandaws.com/ontology/bco" not in text
    assert not re.search(r"(?m)^\s*@prefix", text)
    assert "subClassOf" not in text and "owl:Class" not in text


def test_the_catalog_carries_apqcs_notice(committed):
    cat, xw = committed
    pcf = yaml.safe_load((ROOT / INVENTORY_FILES[1]).read_text(encoding="utf-8"))
    assert cat["apqc_notice"] == xw["apqc_notice"] == pcf["apqc_notice"]


# ------------------------------------------------------------ hard checks


def hard(tool, built, catalog=None, xwalk=None):
    return tool.checks(built["s"], catalog or built["catalog"], xwalk or built["xwalk"],
                       built["docs"])[0]


def test_positive_control_passes_every_hard_check(tool, built):
    assert hard(tool, built) == []


def test_a_dropped_crosswalk_row_is_refused(tool, built):
    assert any("crosswalk has" in f for f in hard(tool, built, xwalk=built["xwalk"][1:]))


def test_a_dangling_broader_link_is_refused(tool, built):
    cat = copy.deepcopy(built["catalog"])
    victim = next(c for c in cat if c["broader"])
    victim["broader"][0]["id"] = "BCC-00000000"
    found = hard(tool, built, catalog=cat)
    assert any("broader link to BCC-00000000" in f for f in found)


def test_a_broken_inverse_is_refused(tool, built):
    cat = copy.deepcopy(built["catalog"])
    next(c for c in cat if c["narrower"])["narrower"].pop()
    assert any("not inverse" in f for f in hard(tool, built, catalog=cat))


def test_an_iri_for_an_identifier_is_refused(tool, built):
    cat = copy.deepcopy(built["catalog"])
    cat[0]["id"] = "https://fandaws.com/ontology/bco#Widget"
    assert any("not a provisional inventory identifier" in f
               for f in hard(tool, built, catalog=cat))


def test_a_definition_without_its_genus_is_refused(tool, built):
    cat = copy.deepcopy(built["catalog"])
    cat[0]["definition"]["text"] = "Widgets."
    assert any("does not state the genus" in f for f in hard(tool, built, catalog=cat))


def test_a_row_without_interpretation_or_reason_is_refused(tool, built):
    xw = copy.deepcopy(built["xwalk"])
    row = next(r for r in xw if not r["interpretations"])
    del row["no_interpretation"]
    assert any("neither an interpretation nor a reason" in f
               for f in hard(tool, built, xwalk=xw))


def with_review(built, pins=None, dispositions=None):
    s = dict(built["s"])
    if pins is not None:
        s["pins"] = pins
    if dispositions is not None:
        s["dispositions"] = dispositions
    return dict(built, s=s)


def test_a_pinned_candidate_that_vanishes_is_refused(tool, built):
    pins = dict(built["s"]["pins"])
    pins["development|no such synthetic widget"] = "BCC-0000000f"
    found = hard(tool, with_review(built, pins=pins))
    assert any("BCC-0000000f" in f and "no longer generated" in f for f in found)


def test_a_disposition_not_in_effect_is_refused(tool, built):
    cat = copy.deepcopy(built["catalog"])
    victim = next(c for c in cat if c["id"] == "BCC-9ecf360b")
    victim["review"] = victim["review"]["generated"]
    found = hard(tool, built, catalog=cat)
    assert any("BCC-9ecf360b: its recorded disposition is not in effect" in f for f in found)


def test_a_disposition_without_a_pin_is_refused(tool, built):
    disp = dict(built["s"]["dispositions"])
    some = next(c for c in built["catalog"] if c["id"] not in built["s"]["pins"].values())
    disp[some["id"]] = {"id": some["id"], "status": "rejected", "date": "2026-11-07",
                        "record": "x", "reason": "x"}
    found = hard(tool, with_review(built, dispositions=disp))
    assert any("%s has a disposition but no pinned identifier" % some["id"] in f
               for f in found)


def test_retirement_into_a_non_candidate_is_refused(tool, built):
    disp = copy.deepcopy(built["s"]["dispositions"])
    disp["BCC-b7c46718"]["into"] = "BCC-00000000"
    found = hard(tool, with_review(built, dispositions=disp))
    assert any("retired into BCC-00000000, which is not an active candidate" in f
               for f in found)
