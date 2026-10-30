# SPDX-License-Identifier: MIT
"""The PCF notice gate: every PCF-bearing file carries APQC's notice.

docs/decisions/2026-10-29-apqc-pcf-sourcing-decided.md, section 4: "a
check that fails when a PCF-bearing artifact lacks the notice", plus a
NOTICE file that lists the files concerned. Each finding the gate can
report (pcf_notice.MESSAGES) is fired here on a negative fixture, beside a
positive control, and the tuple is pinned so a new refusal arrives with
its test. The fixtures are SYNTHETIC (made-up element ids, 9xxxxx); APQC's
notice is never typed here, but taken from the committed NOTICE.md by the
tool's own extraction.
"""

from __future__ import annotations

import json

import pytest
import yaml

from conftest import ROOT, load_tool

GATE = "tools/licensing/pcf_notice.py"
PINS = "config/inventory-pcf-sources.yaml"
RIGHTS = "docs/sources/inventory/rights.yaml"
ENTRIES = "docs/sources/inventory/pcf-7.4-entries.yaml"
BPO_ENTRIES = "docs/sources/inventory/bpo-entries.yaml"
SCHEME = "https://fandaws.com/ontology/bpo/scheme#PCF"


@pytest.fixture(scope="module")
def gate():
    return load_tool("bco_pcf_notice", GATE)


@pytest.fixture(scope="module")
def h(gate):
    return gate.harvest_pcf()


@pytest.fixture(scope="module")
def notice(h):
    return h.extract_notice((ROOT / "NOTICE.md").read_bytes()
                            .decode("utf-8"))


def ttl(notice=None, rights=None, headers=1, pcf=True,
        predicate="https://fandaws.com/ontology/bpo#hierarchyID") -> bytes:
    """A Turtle file; `rights` is a list of dct:rights values (default:
    framing plus the notice when `notice` is given)."""
    if rights is None:
        rights = [] if notice is None else \
            ["Framing.\\n\\n" + notice.replace('"', '\\"')]
    lines = ["@prefix owl: <http://www.w3.org/2002/07/owl#> .",
             "@prefix dct: <http://purl.org/dc/terms/> ."]
    for n in range(headers):
        lines.append("<https://example.org/onto%d> a owl:Ontology%s ." % (
            n, "".join(' ;\n    dct:rights "%s"' % r for r in rights)
            if n == 0 else ""))
    if pcf:
        lines.append('<https://example.org/n900001> <%s> "41.3" .'
                     % predicate)
    lines.append("# bpo:pcfID in a comment is not an assertion")
    return ("\n".join(lines) + "\n").encode("utf-8")


def data(notice=None, key="pcf_code", nested=False) -> bytes:
    body = {"format": 1}
    if notice is not None:
        body["apqc_notice"] = notice
    item = {key: "900001", "name": "Synthetic alpha"}
    body["entries"] = [{"wrapper": item}] if nested else [item]
    return yaml.safe_dump(body, sort_keys=False,
                          allow_unicode=True).encode("utf-8")


@pytest.fixture
def scenario(tmp_path, gate, h, notice):
    """make(files, bearing, exceptions) -> (findings, report).

    The pins name `bearing` (paths) as PCF-bearing and `exceptions`
    ({path: reason}); NOTICE.md is rendered fresh from them unless
    `files` supplies one. `files` maps paths to bytes, as git would."""
    for relative in (PINS, RIGHTS):
        target = tmp_path / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes((ROOT / relative).read_bytes())
    pin_data = yaml.safe_load((ROOT / PINS).read_bytes().decode("utf-8"))
    entries_path = pin_data["sources"][0]["outputs"]["entries"]

    def make(files, bearing=(), exceptions=None, notice_md=None):
        exceptions = exceptions or {}
        pins = dict(pin_data)
        pins["pcf_bearing"] = [{"path": entries_path, "carries": "entries"}]
        pins["pcf_bearing"] += [{"path": p, "carries": "synthetic"}
                                for p in bearing]
        pins["exceptions"] = [{"path": p, "reason": r}
                              for p, r in exceptions.items()]
        (tmp_path / PINS).write_bytes(yaml.safe_dump(
            pins, sort_keys=False).encode("utf-8"))
        source = h.pins(tmp_path)
        files = dict(files)
        files.setdefault(entries_path, data(notice))
        if notice_md is None:
            notice_md = h.notice_bytes(source, h.rights_citation(
                tmp_path, source), notice)
        if notice_md is not False:
            files["NOTICE.md"] = notice_md
        return gate.findings(tmp_path, files)

    return make


def fired(problems, message):
    return [p for p in problems if message in p]


# ----------------------------------------------------- positive controls


def test_carrying_files_pass(scenario, notice, gate):
    problems, report = scenario(
        {"a.yaml": data(notice), "b.json": json.dumps(
            {"apqc_notice": notice, "pcf_hierarchy_id": "41.3"}).encode(),
         "c.ttl": ttl(notice)}, bearing=["a.yaml", "b.json", "c.ttl"])
    assert problems == []
    assert set(report["bearing"]) == {ENTRIES, "a.yaml", "b.json", "c.ttl"}
    assert all(v is None for v in report["bearing"].values())


def test_files_without_pcf_material_need_no_notice(scenario):
    problems, report = scenario({
        "plain.yaml": b"name: Synthetic alpha\ndescription: x\n",
        "plain.ttl": ttl(pcf=False),
        "prose.md": b"pcf_code: 900001 and bpo:pcfID in prose\n",
        "tool.py": b"PCF_KEYS = {'pcf_code': 1}\n"})
    assert problems == []
    assert set(report["bearing"]) == {ENTRIES}


@pytest.mark.parametrize("name, content", [
    ("nested.yaml", lambda n: data(None, nested=True)),
    ("element.yaml", lambda n: data(None, key="pcf_element_id")),
    ("code.json", lambda n: json.dumps({"x": [{"pcf_code": "1"}]}).encode()),
    ("other-ns.ttl", lambda n: ttl(predicate="http://example.org/apqc#pcfID")),
    ("text.ttl", lambda n: ttl(
        predicate="https://fandaws.com/ontology/bpo#apqcSourceText")),
    ("scheme.ttl", lambda n: (
        "<https://example.org/n1> "
        "<http://www.w3.org/2004/02/skos/core#inScheme> <%s> .\n"
        % SCHEME).encode()),
])
def test_pcf_material_is_found_however_it_is_held(scenario, notice, gate,
                                                  name, content):
    problems, report = scenario({name: content(notice)})
    assert name in report["bearing"]
    assert fired(problems, gate.UNLISTED)


# ----------------------------------------------------- negative fixtures


def test_a_yaml_artifact_without_the_notice_is_refused(scenario, gate):
    problems, _ = scenario({"a.yaml": data(None)}, bearing=["a.yaml"])
    assert fired(problems, "a.yaml " + gate.LACKS), problems


def test_an_altered_notice_in_yaml_is_refused(scenario, notice, gate):
    altered = notice.replace("perpetual", "revocable")
    problems, _ = scenario({"a.yaml": data(altered)}, bearing=["a.yaml"])
    assert fired(problems, "a.yaml " + gate.ALTERED), problems


def test_a_whitespace_change_is_an_altered_notice(scenario, notice, gate):
    problems, _ = scenario({"a.yaml": data(notice.replace(". ", ".  ", 1))},
                           bearing=["a.yaml"])
    assert fired(problems, gate.ALTERED), problems


def test_turtle_without_dct_rights_is_refused(scenario, gate):
    problems, _ = scenario({"c.ttl": ttl()}, bearing=["c.ttl"])
    assert fired(problems, "c.ttl " + gate.LACKS), problems


def test_turtle_with_an_altered_notice_is_refused(scenario, notice, gate):
    problems, _ = scenario({"c.ttl": ttl(notice.replace("APQC.", "APQC"))},
                           bearing=["c.ttl"])
    assert fired(problems, "c.ttl " + gate.ALTERED), problems


def test_turtle_with_two_dct_rights_is_refused(scenario, notice, gate):
    problems, _ = scenario({"c.ttl": ttl(rights=[
        "Framing.\\n\\n" + notice.replace('"', '\\"'), "Another."])},
        bearing=["c.ttl"])
    assert fired(problems, gate.RIGHTS_SHAPE), problems


def test_turtle_with_two_ontology_headers_is_refused(scenario, notice, gate):
    problems, _ = scenario({"c.ttl": ttl(notice, headers=2)},
                           bearing=["c.ttl"])
    assert fired(problems, gate.RIGHTS_SHAPE), problems


def test_an_unlisted_pcf_bearing_file_is_refused(scenario, notice, gate):
    problems, _ = scenario({"a.yaml": data(notice)})
    assert fired(problems, "a.yaml " + gate.UNLISTED), problems


def test_a_listed_file_without_pcf_material_is_refused(scenario, gate):
    problems, _ = scenario({"plain.yaml": b"name: x\n"},
                           bearing=["plain.yaml"])
    assert fired(problems, "plain.yaml " + gate.OVERLISTED), problems


def test_a_listed_file_that_is_not_tracked_is_refused(scenario, gate):
    problems, _ = scenario({}, bearing=["gone.yaml"])
    assert fired(problems, "gone.yaml " + gate.OVERLISTED), problems


def test_a_stale_notice_is_refused(scenario, h, gate):
    base_problems, _ = scenario({})
    assert base_problems == []
    notice_md = (ROOT / "NOTICE.md").read_bytes() + b"\nAn added line.\n"
    problems, _ = scenario({}, notice_md=notice_md)
    assert fired(problems, gate.STALE_NOTICE), problems


def test_an_altered_root_notice_is_refused(scenario, notice, gate):
    text = (ROOT / "NOTICE.md").read_bytes().decode("utf-8")
    altered = text.replace(notice, notice.replace("royalty-free", "paid"))
    assert altered != text
    problems, _ = scenario({}, notice_md=altered.encode("utf-8"))
    assert fired(problems, gate.NO_ROOT_NOTICE), problems


def test_a_missing_root_notice_is_refused(scenario, gate):
    problems, _ = scenario({}, notice_md=False)
    assert fired(problems, gate.NO_ROOT_NOTICE), problems


@pytest.mark.parametrize("name, content", [
    ("broken.yaml", b"a: [unclosed\n"),
    ("broken.json", b"{not json"),
    ("broken.ttl", b"<a> <b> .\n"),
])
def test_an_unreadable_file_is_refused(scenario, gate, name, content):
    problems, _ = scenario({name: content})
    assert fired(problems, name + " " + gate.UNREADABLE), problems


def test_an_exception_holds_off_only_the_notice(scenario, gate):
    problems, report = scenario({"old.yaml": data(None)},
                                bearing=["old.yaml"],
                                exceptions={"old.yaml": "awaits E7"})
    assert problems == []
    assert report["excepted"] == ["old.yaml"]


@pytest.mark.parametrize("files, why", [
    ({"old.yaml": b"__notice__"}, "carries the notice"),
    ({"old.yaml": b"name: x\n"}, "carries no PCF material"),
])
def test_an_exception_that_is_no_longer_needed_is_refused(
        scenario, notice, gate, files, why):
    files = {k: (data(notice) if v == b"__notice__" else v)
             for k, v in files.items()}
    problems, _ = scenario(files, bearing=["old.yaml"],
                           exceptions={"old.yaml": "awaits E7"})
    assert fired(problems, "old.yaml " + gate.STALE_EXCEPTION), problems
    assert fired(problems, why), problems


def test_an_exception_for_an_untracked_file_is_refused(scenario, gate):
    problems, _ = scenario({}, bearing=["old.yaml"],
                           exceptions={"old.yaml": "awaits E7"})
    assert fired(problems, "old.yaml " + gate.STALE_EXCEPTION), problems


#: Which test above fires each message.
FIRED_BY = {
    "NO_ROOT_NOTICE": test_an_altered_root_notice_is_refused,
    "STALE_NOTICE": test_a_stale_notice_is_refused,
    "UNREADABLE": test_an_unreadable_file_is_refused,
    "LACKS": test_a_yaml_artifact_without_the_notice_is_refused,
    "ALTERED": test_an_altered_notice_in_yaml_is_refused,
    "RIGHTS_SHAPE": test_turtle_with_two_dct_rights_is_refused,
    "UNLISTED": test_an_unlisted_pcf_bearing_file_is_refused,
    "OVERLISTED": test_a_listed_file_without_pcf_material_is_refused,
    "STALE_EXCEPTION": test_an_exception_that_is_no_longer_needed_is_refused,
}


def test_every_finding_has_a_negative_fixture(gate):
    assert gate.MESSAGES == tuple(getattr(gate, name) for name in FIRED_BY)
    assert len(set(gate.MESSAGES)) == len(gate.MESSAGES)


# ------------------------------------------------------ the repository


def test_the_repository_passes_the_gate(gate):
    problems, report = gate.findings(ROOT)
    assert problems == []
    assert report["bearing"] == {ENTRIES: None, BPO_ENTRIES: None}
    assert report["excepted"] == []


def test_the_exception_list_is_empty_since_e7(h):
    """It held I-1's entries, "awaits E7", until E7 gave them the notice.
    Pinned empty, so nothing joins it unnoticed: a new exception is a new
    decision."""
    assert h.pins(ROOT)["exceptions"] == []
    text = (ROOT / "NOTICE.md").read_bytes().decode("utf-8")
    assert "Does not yet carry the notice" not in text


def test_root_notice_lists_every_pcf_bearing_file(h):
    text = (ROOT / "NOTICE.md").read_bytes().decode("utf-8")
    assert h.listed_files(text) == [ENTRIES, BPO_ENTRIES]


def test_the_vendored_bpo_extract_carries_no_pcf_material(gate):
    path = "vendor/bpo/bpo-ext-bco-extract.ttl"
    kind, _parsed, bearing = gate.read(path, (ROOT / path).read_bytes(),
                                       SCHEME)
    assert kind == "rdf" and bearing is False


def test_the_gate_runs_before_committing(repo):
    text = (repo / "CLAUDE.md").read_bytes().decode("utf-8")
    assert ".venv/Scripts/python tools/licensing/pcf_notice.py" in text
    assert ".venv/Scripts/python tools/inventory/harvest_pcf.py" in text
