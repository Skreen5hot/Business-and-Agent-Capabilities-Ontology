# SPDX-License-Identifier: MIT
"""The bounded presentation-drift check of rights.py --confirm.

The decision of 2026-11-17 (docs/decisions/2026-11-17-fibf-drift-
disposition-accepted.md, section 5) requires positive and negative tests
for each behaviour. They run offline, on small synthetic pages built here
with the same structure as the documented ones: a FIBF page whose
stylesheet and script references carry a 19-digit build number, and a GSA
Drupal page with a header navigation region, a Drupal settings script and
versioned assets. Nothing is fetched.
"""

from __future__ import annotations

import copy as copylib
import hashlib

import pytest
import yaml

from conftest import ROOT, load_tool

TOOL = "tools/inventory/rights.py"
RIGHTS = "docs/sources/inventory/rights.yaml"
BASELINE, UNCHANGED, NEW = ("1790778396531677562", "1617716038051754794",
                            "1794604162961183849")
QUOTE = "free of copyright and may be copied and distributed without permission"


@pytest.fixture(scope="module")
def rights():
    return load_tool("bco_inventory_rights_drift", TOOL)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def fibf_page(build=BASELINE, text="Travel and expense management") -> bytes:
    return ("""<!doctype html><html><head>
<link rel="stylesheet" href="/assets/css/index.css?%(b)s">
<link rel="stylesheet" href="/assets/css/main-page.css?%(b)s">
</head><body><main><h1>%(t)s</h1>
<a href="/assets/files/downloads/Travel_2024/Excel/business_capabilities.xlsx">Business capabilities</a>
</main>
<script src="/assets/js/slick.js?%(u)s"></script>
<script src="/assets/js/app.js?%(b)s"></script>
</body></html>
""" % {"b": build, "u": UNCHANGED, "t": text}).encode("utf-8")


def gsa_page(nav="Plan a trip", settings='{"v":1}', token="tnc3er",
             aggregate="js_gfM_sJi9NY2PDxRUezydBTSxtaekJ", quote=QUOTE,
             body="Most GSA material is", privacy="/website-information/privacy",
             extra_script="", space=" ") -> bytes:
    return ("""<!doctype html><html><head>
<script type="application/json" data-drupal-selector="drupal-settings-json">%(settings)s</script>
<script src="/sites/gsa.gov/files/js/%(agg)s.js?scope=header&amp;include=x"></script>
<script src="/modules/contrib/google_tag/js/gtag.js?%(token)s"></script>
</head><body>
<header class="usa-header usa-header--extended">
<div class="usa-navbar"><a class="logo-img" href="/">GSA</a></div>
<div class="usa-nav"><div class="usa-nav__inner"><nav><ul>
<li><a href="/travel/%(slug)s">%(nav)s</a></li></ul></nav></div></div>
<div class="grid-container"><a href="/website-information">Website information</a></div>
</header>
<main><h2>Reuse and copyright</h2>
<p>%(body)s%(space)s%(quote)s.</p>
<p><a href="%(privacy)s">Privacy and security</a></p></main>
<footer><a href="/website-information/website-policies">Website policies</a></footer>
%(extra)s</body></html>
""" % {"settings": settings, "agg": aggregate, "token": token, "nav": nav,
       "slug": nav.lower().replace(" ", "-"), "quote": quote, "body": body,
       "privacy": privacy, "extra": extra_script, "space": space}
            ).encode("utf-8")


def fibf_item(pinned: bytes, ident="fibf-page-travel") -> dict:
    return {"id": ident, "kind": "url", "url": "https://ussm.gsa.gov/fibf-travel/",
            "sha256": sha(pinned)}


def gsa_item(pinned: bytes) -> dict:
    return {"id": "gsa-website-policies", "kind": "url",
            "url": "https://www.gsa.gov/website-information/website-policies",
            "sha256": sha(pinned)}


ARCHIVE = ("https://web.archive.org/web/20261028084510id_/"
           "https://www.gsa.gov/website-information/website-policies")


def rules(rights):
    return {
        "fibf-page-travel": ("build-number", {
            "baseline": BASELINE, "unchanged": [UNCHANGED]}, []),
        "gsa-website-policies": ("gsa-drupal-page", {
            "evidence": "gsa-website-policies", "archive": ARCHIVE,
            "comparison": "gsa-drupal-page"}, [QUOTE]),
    }


def gsa_verdict(rights, tmp_path, served, baseline=None):
    baseline = baseline or gsa_page()
    return rights.classify(gsa_item(baseline), served, rules(rights),
                           tmp_path / "cache", fetch=lambda url: baseline)


# ---------------------------------------------------- 1. exact bytes pass

def test_exact_pinned_bytes_pass(rights, tmp_path):
    page = fibf_page()
    verdict = rights.classify(fibf_item(page), page, rules(rights), tmp_path)
    assert verdict.status == rights.EXACT
    gsa = gsa_page()
    assert gsa_verdict(rights, tmp_path, gsa).status == rights.EXACT


# ------------------------------- 2. a build-number-only change passes, visibly

def test_a_fibf_build_number_change_passes_and_recovers_the_pin(rights,
                                                                tmp_path):
    pinned = fibf_page()
    verdict = rights.classify(fibf_item(pinned), fibf_page(build=NEW),
                              rules(rights), tmp_path)
    assert verdict.status == rights.PRESENTATION
    assert verdict.pinned == pinned and NEW in verdict.detail


def test_confirm_reports_the_drift_and_keeps_the_pin(rights, tmp_path,
                                                     monkeypatch, capsys):
    pinned = fibf_page()
    item = dict(fibf_item(pinned), retrieved="2026-10-28")
    data = {"sources": [{"id": "fibf-2026-10-28", "evidence": [item],
                         "quotes": [], "presentation_drift": {
                             "asset_build_number": {
                                 "baseline": BASELINE, "unchanged": [UNCHANGED],
                                 "evidence": [item["id"]]},
                             "archived_baseline": []}}]}
    monkeypatch.setattr(rights, "load", lambda base: ("", data))
    monkeypatch.setattr(rights, "_get", lambda url: fibf_page(build=NEW))
    drifts = []
    assert rights.confirm(tmp_path, tmp_path / "cache", drifts) == []
    assert len(drifts) == 1
    assert rights.PRESENTATION in drifts[0] and sha(pinned) in drifts[0]
    assert "The pin stands" in drifts[0]
    assert "drift   " in capsys.readouterr().out
    assert item["sha256"] == sha(pinned)
    assert (tmp_path / "cache" / sha(pinned)).read_bytes() == pinned


# ----------------------------- 3. a FIBF text change fails, build numbers or not

def test_a_fibf_text_change_fails_even_with_a_new_build_number(rights,
                                                               tmp_path):
    verdict = rights.classify(
        fibf_item(fibf_page()), fibf_page(build=NEW, text="Something else"),
        rules(rights), tmp_path)
    assert verdict.status == rights.FAILURE
    assert "unexplained difference remains" in verdict.detail


@pytest.mark.parametrize("served, needle", [
    (fibf_page(text="Something else"), "baseline's"),
    (fibf_page(build=NEW).replace(
        b"main-page.css?" + NEW.encode(), b"main-page.css?1111111111111111111"),
     "ambiguous"),
    (b"<html><body>no assets</body></html>", "no asset build number"),
])
def test_a_fibf_page_outside_the_documented_case_fails(rights, tmp_path,
                                                       served, needle):
    verdict = rights.classify(fibf_item(fibf_page()), served, rules(rights),
                              tmp_path)
    assert verdict.status == rights.FAILURE and needle in verdict.detail


# ------------------------- 4. the verified GSA presentation changes pass

def test_gsa_navigation_settings_and_asset_changes_pass(rights, tmp_path):
    served = gsa_page(nav="City Pair airfare", settings='{"v":2,"x":[1]}',
                      token="tof2mb", aggregate="js_H1X_FPvK2NAIvBX3fq2w16bX",
                      space="\n    ")
    verdict = gsa_verdict(rights, tmp_path, served)
    assert verdict.status == rights.PRESENTATION, verdict.detail
    assert verdict.pinned == gsa_page()


# ---------------- 5. GSA rights language, content or a relevant link changing

@pytest.mark.parametrize("change, needle", [
    ({"quote": "subject to copyright and may not be copied"}, "rights language"),
    ({"body": "Some GSA material is"}, "unexplained"),
    ({"privacy": "/website-information/other"}, "unexplained"),
    ({"extra_script": '<script src="/core/assets/new.js?v=1"></script>'},
     "unexplained"),
])
def test_a_gsa_substantive_or_link_change_fails(rights, tmp_path, change,
                                                needle):
    verdict = gsa_verdict(rights, tmp_path, gsa_page(**change))
    assert verdict.status == rights.FAILURE and needle in verdict.detail


def test_a_changed_link_outside_the_navigation_region_fails(rights, tmp_path):
    served = gsa_page().replace(b'href="/website-information"',
                                b'href="/elsewhere"')
    verdict = gsa_verdict(rights, tmp_path, served)
    assert verdict.status == rights.FAILURE


def test_a_page_without_the_navigation_region_fails_closed(rights, tmp_path):
    served = gsa_page().replace(b"usa-nav__inner", b"usa-nav__other")
    verdict = gsa_verdict(rights, tmp_path, served)
    assert verdict.status == rights.FAILURE and "exactly one" in verdict.detail


# ------------------------------- 6. an unverifiable baseline fails closed

def test_an_unavailable_baseline_fails_closed(rights, tmp_path):
    def down(url):
        raise OSError("connection refused")
    verdict = rights.classify(gsa_item(gsa_page()), gsa_page(nav="Other"),
                              rules(rights), tmp_path / "cache", fetch=down)
    assert verdict.status == rights.FAILURE
    assert "could not be retrieved" in verdict.detail


def test_a_baseline_that_is_not_the_pin_fails_closed(rights, tmp_path):
    verdict = rights.classify(
        gsa_item(gsa_page()), gsa_page(nav="Other"), rules(rights),
        tmp_path / "cache", fetch=lambda url: gsa_page(body="Altered"))
    assert verdict.status == rights.FAILURE
    assert "cannot be verified" in verdict.detail


def test_the_archive_fetch_takes_only_an_archive_capture(rights):
    with pytest.raises(rights.Refused):
        rights._get_archive("https://www.gsa.gov/website-information/x")


# ------------------------------------ 7. non-HTML evidence stays strict

def test_a_workbook_stays_byte_strict(rights, tmp_path):
    item = {"id": "fibf-doc-travel-1", "kind": "url",
            "url": "https://ussm.gsa.gov/assets/files/downloads/x.xlsx",
            "sha256": sha(b"PK workbook")}
    verdict = rights.classify(item, b"PK workbook, changed", rules(rights),
                              tmp_path)
    assert verdict.status == rights.FAILURE
    assert "must match exactly" in verdict.detail


def test_the_record_refuses_a_build_rule_on_a_workbook(rights, tmp_path):
    from test_rights import COPIED
    for relative in COPIED:
        target = tmp_path / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes((ROOT / relative).read_bytes())
    data = yaml.safe_load((tmp_path / RIGHTS).read_bytes().decode("utf-8"))
    fibf = next(s for s in data["sources"] if s["id"] == "fibf-2026-10-28")
    fibf["presentation_drift"]["asset_build_number"]["evidence"].append(
        "fibf-doc-travel-1")
    (tmp_path / RIGHTS).write_bytes(yaml.safe_dump(
        data, sort_keys=False, allow_unicode=True).encode("utf-8"))
    problems, _ = rights.check(tmp_path)
    assert any("not an HTML page on ussm.gsa.gov" in p for p in problems), \
        problems


# --------------------------------------------- the committed addendum

def test_the_addendum_keeps_every_pin_and_observes_without_pinning(rights):
    data = yaml.safe_load((ROOT / RIGHTS).read_bytes().decode("utf-8"))
    fibf = next(s for s in data["sources"] if s["id"] == "fibf-2026-10-28")
    drift = fibf["presentation_drift"]
    pins = {e["id"]: e["sha256"] for e in fibf["evidence"]}
    assert len(drift["asset_build_number"]["evidence"]) == 26
    assert len(drift["observations"]) == 27
    for obs in drift["observations"]:
        assert obs["observed_sha256"] != pins[obs["evidence"]]
    rule = rights.drift_rules(data)
    assert set(rule) == set(drift["asset_build_number"]["evidence"]) | {
        "gsa-website-policies"}
    assert all(not ref.startswith("fibf-doc-") for ref in rule)


def test_the_addendum_refuses_an_observation_that_is_the_pin(rights,
                                                             tmp_path):
    from test_rights import COPIED
    for relative in COPIED:
        target = tmp_path / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes((ROOT / relative).read_bytes())
    data = yaml.safe_load((tmp_path / RIGHTS).read_bytes().decode("utf-8"))
    fibf = next(s for s in data["sources"] if s["id"] == "fibf-2026-10-28")
    pins = {e["id"]: e["sha256"] for e in fibf["evidence"]}
    obs = copylib.deepcopy(fibf["presentation_drift"]["observations"][0])
    obs["observed_sha256"] = pins[obs["evidence"]]
    fibf["presentation_drift"]["observations"][0] = obs
    (tmp_path / RIGHTS).write_bytes(yaml.safe_dump(
        data, sort_keys=False, allow_unicode=True).encode("utf-8"))
    problems, _ = rights.check(tmp_path)
    assert any("observes the pinned digest" in p for p in problems), problems


# ------------------------------------- the federal harvest uses the same rule

def test_the_harvest_uses_only_recovered_pinned_bytes(tmp_path, monkeypatch):
    harvest = load_tool("bco_harvest_federal_drift",
                        "tools/inventory/harvest_federal.py")
    pinned = fibf_page()
    item = fibf_item(pinned)
    monkeypatch.setattr(harvest, "fetch", lambda url: fibf_page(build=NEW))
    assert harvest.Bytes(tmp_path / "a", refetch=True)(item) == pinned
    monkeypatch.setattr(harvest, "fetch",
                        lambda url: fibf_page(build=NEW, text="Changed"))
    with pytest.raises(harvest.Refused, match="not a re-pin"):
        harvest.Bytes(tmp_path / "b", refetch=True)(item)
