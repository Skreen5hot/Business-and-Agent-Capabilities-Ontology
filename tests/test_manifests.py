"""Gate M and CAP-18 (decision of 2026-11-15, B-2): the CD15 completeness
manifest's schema, and absence answers bounded by it.

Each applicability rule of CD15 has a positive and a negative case, over
test-only evidence graphs (tests/fixtures/cd15/evidence.trig) and the real
module, extracts and fixture organizations. Every answer is one of
"recorded", "none recorded" or "unknown"; none is "not authorized".
"""

from __future__ import annotations

import datetime as dt
import json

import pytest

from conftest import load_tool

BCO = "https://fandaws.com/ontology/bco#"
BPO = "https://fandaws.com/ontology/bpo#"
CCO = "https://www.commoncoreontologies.org/"

CLERK = BCO + "fixture_cq_clerk"
TREASURER = BCO + "fixture_cq_treasurer"
ORG = BCO + "fixture_cq_org"


@pytest.fixture(scope="module")
def tool():
    return load_tool("bco_manifests", "tools/ontology/manifests.py")


@pytest.fixture(scope="module")
def fixtures(repo):
    return json.loads((repo / "tests/fixtures/cd15/manifests.json")
                      .read_bytes().decode("utf-8"))


@pytest.fixture(scope="module")
def context(repo, layout):
    import rdflib

    g = rdflib.Graph()
    for path in layout.ontology_files() + layout.vendored_files():
        g.parse(path, format="turtle")
    g.parse(repo / "tests/fixtures/cq_organizations.ttl", format="turtle")
    return g


@pytest.fixture(scope="module")
def dataset(repo):
    import rdflib

    d = rdflib.Dataset()
    d.parse(repo / "tests/fixtures/cd15/evidence.trig", format="trig")
    return d


@pytest.fixture(scope="module")
def manifests(tool, fixtures):
    """Every fixture manifest, read; the invalid ones too, so that a
    manifest failing Gate M is shown to bound nothing."""
    return [tool.Manifest.read(e["manifest"])
            for e in fixtures["valid"] + fixtures["invalid"]
            if isinstance(e["manifest"].get("graph"), str)]


def ask(tool, dataset, context, manifests, agent, act, day,
        organization=ORG):
    return tool.authorization(dataset, context, manifests, organization,
                              agent, BPO + act if ":" not in act else act,
                              dt.date.fromisoformat(day))


# --------------------------------------------------------------- Gate M


def test_gate_m_passes_and_can_fail(tool):
    findings, counts = tool.gate()
    assert not findings, findings
    assert counts["valid"] >= 4 and counts["invalid"] >= 9


@pytest.mark.parametrize("case", [
    "M4 start after end", "no authority sources", "a field CD15 does not have",
    "a month that does not exist", "a day that does not exist",
    "no acting agents", "a prefix the tool does not know",
    "an act class listed twice", "a graph that is not a name"])
def test_each_invalid_manifest_fails_for_its_reason(tool, fixtures, case):
    entry = next(e for e in fixtures["invalid"] if e["case"].startswith(case))
    assert tool.check(entry["manifest"]), case


def test_the_schema_has_exactly_cd15s_fields(tool):
    """CD15: graph IRI, organization, acting agents, covered act classes,
    start and end dates, authority sources. Nothing else: revocation and
    supersession are not representable (OI-21)."""
    schema = tool.schema()
    assert set(schema["required"]) == set(schema["properties"]) == {
        "graph", "organization", "acting_agents", "act_classes", "start",
        "end", "authority_sources"}
    assert schema["additionalProperties"] is False


def test_the_gate_cli(tool, capsys):
    assert tool.main([]) == 0
    assert "fixtures only" in capsys.readouterr().out


# ----------------------------------------------------- CAP-18 and CD15


def test_cap18_outside_the_manifest_is_unknown_never_empty(
        tool, dataset, context, manifests):
    """The specification's failing fixture: a date outside the manifest. The
    only manifest naming 2027 fails Gate M (start after end), so it bounds
    nothing."""
    a = ask(tool, dataset, context, manifests, CLERK, "P10867", "2027-03-01")
    assert a.status == "unknown" and a.records == []


def test_cap18_in_scope_with_no_record_is_none_recorded(
        tool, dataset, context, manifests):
    a = ask(tool, dataset, context, manifests, CLERK, "P10867", "2026-10-01")
    assert a.status == "none recorded"
    assert "not a finding that the agent is unauthorized" in a.reason


def test_act_type_positive_a_record_covers_the_classes_under_it(
        tool, dataset, context, manifests):
    a = ask(tool, dataset, context, manifests, CLERK, "P10867", "2026-03-01")
    assert a.status == "recorded"
    assert a.records == [BCO + "fixture_cd15_r_reporting_clerk"]


def test_act_type_negative_not_a_sibling_nor_the_genus(
        tool, dataset, context, manifests):
    assert ask(tool, dataset, context, manifests, TREASURER, "P10867",
               "2026-03-01").status == "recorded"
    assert ask(tool, dataset, context, manifests, TREASURER, "P10868",
               "2026-03-01").status == "none recorded"
    assert ask(tool, dataset, context, manifests, TREASURER,
               "ActOfReporting", "2026-03-01").status == "none recorded"


def test_agent_positive_and_negative(tool, dataset, context, manifests):
    """A record about the organization applies to it, and not to its
    member; the organization is not an agent the manifest covers."""
    assert ask(tool, dataset, context, manifests, ORG, "P10862",
               "2026-03-01").status == "recorded"
    assert ask(tool, dataset, context, manifests, CLERK, "P10862",
               "2026-03-01").status == "none recorded"
    assert ask(tool, dataset, context, manifests, ORG, "P10867",
               "2026-03-01").status == "unknown"


def test_period_inclusive_positive_and_negative(
        tool, dataset, context, manifests):
    a = ask(tool, dataset, context, manifests, CLERK, "P10868", "2026-09-30")
    assert a.status == "recorded"
    assert a.records == [BCO + "fixture_cd15_r_reporting_clerk_h2"]
    assert ask(tool, dataset, context, manifests, CLERK, "P10868",
               "2026-10-01").status == "none recorded"


def test_overlap_any_one_suffices_and_is_not_an_error(
        tool, dataset, context, manifests):
    a = ask(tool, dataset, context, manifests, CLERK, "P10867", "2026-06-20")
    assert a.status == "recorded"
    assert a.records == [BCO + "fixture_cd15_r_reporting_clerk",
                         BCO + "fixture_cd15_r_reporting_clerk_h2"]


def test_several_authorities_each_record_judged_alone(
        tool, dataset, context, manifests):
    """On 1 July the regulator's record has ended; the internal register's
    record alone answers. No authority is weighed against the other."""
    a = ask(tool, dataset, context, manifests, CLERK, "P10867", "2026-07-01")
    assert a.records == [BCO + "fixture_cd15_r_reporting_clerk_h2"]


def test_scope_negative_cases_are_unknown(tool, dataset, context, manifests):
    other = BCO + "fixture_cq_other"
    assert ask(tool, dataset, context, manifests, BCO + "fixture_cq_other_clerk",
               "P10867", "2026-03-01", organization=other).status == "unknown"
    # An act class no manifest covers (P10893, under Act of Accounting).
    assert ask(tool, dataset, context, manifests, CLERK, "P10893",
               "2026-03-01").status == "unknown"
    # A valid manifest whose graph is not in the dataset (M5).
    m5 = "https://example.org/fixture/"
    a = tool.authorization(dataset, context, manifests, m5 + "org", m5 + "org",
                           BPO + "P10867", dt.date(2026, 3, 1))
    assert a.status == "unknown" and "not present" in a.reason


def test_missing_authority_evidence_is_not_evidence_and_blocks_completeness(
        tool, dataset, context, manifests):
    a = ask(tool, dataset, context, manifests, CLERK, "P10862", "2025-03-01")
    assert a.status == "unknown"
    assert "fixture_cd15_r_no_authority" in a.reason
    assert a.records == []


def test_revocation_is_a_stated_limit_not_a_field(
        tool, dataset, context, manifests, fixtures):
    a = ask(tool, dataset, context, manifests, CLERK, "P10867", "2026-03-01")
    assert "OI-21" in a.reason and "not a finding" in a.reason
    revoked = next(e for e in fixtures["invalid"]
                   if "revocation" in e["case"])
    assert any("revoked_records" in f for f in tool.check(revoked["manifest"]))


def test_no_answer_says_not_authorized(tool, dataset, context, manifests):
    for agent in (CLERK, TREASURER, ORG):
        for act in ("P10862", "P10867", "P10868", "P10893"):
            for day in ("2025-03-01", "2026-03-01", "2026-10-01", "2027-03-01"):
                a = ask(tool, dataset, context, manifests, agent, act, day)
                assert a.status in ("recorded", "none recorded", "unknown")
                assert "not authorized" not in a.reason
