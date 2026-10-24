# SPDX-License-Identifier: MIT
"""The controlled-vocabulary build, tools/vocab/ (ADR-003, P3).

Every refusal the build makes is broken here on a fixture, and the test
requires THAT finding's code -- not merely a failure -- so a mutation that
trips some other check does not count (docs/process/PROCESS.md section 2).
Positive controls sit beside them: a fixture that must build clean, so a
refusal that fires on everything is caught too.

Fixtures are built at run time in tmp_path, never committed: the inputs
are YAML dicts written as LF bytes, the specification and the register
are the real ones unless a test copies and edits them, and ratification
acts live in a throwaway git repository the test creates, so D2's checks
run against real commits without touching this repository's history.

An SRC id that must NOT be a register entry is assembled at run time,
because tools/sources/build_register.py scans every tracked file for SRC
ids and would report a literal one here.
"""

from __future__ import annotations

import copy
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

from conftest import ROOT

AGENT = "bcoa:claude-opus-5-5"
PERSON_IRI = "https://fandaws.com/ontology/bco-agents#aaron-damiano"
SOFTWARE_IRI = "https://fandaws.com/ontology/bco-agents#claude-opus-5-5"
SPEC_ROWS = ["BusinessCapability", "CapabilityMap", "CapabilityAssessment",
             "CapabilityMaturityRating", "CapabilitySourcingStatement",
             "CapabilitySourcingAssessment", "CapabilityTarget",
             "CapabilityTargetStateSpecification", "AuthorizationRecord"]
TEMPLATE_TERMS = [
    "Specific capability classes (`ex:StrategicPlanningCapability` and the rest)",
    "Realization union `ex:<Name>Realization`",
]


def load_registered(name: str, relative: str):
    """conftest.load_tool, plus registering the module before it runs:
    a dataclass under `from __future__ import annotations` looks its own
    module up in sys.modules while it is being defined."""
    import importlib.util

    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def vb():
    return load_registered("bco_vocab_build", "tools/vocab/build.py")


@pytest.fixture(scope="module")
def st(vb):
    """The section 4 parser the build itself imported, not a second copy."""
    return vb.spec_terms


@pytest.fixture(scope="module")
def cit(vb):
    return vb.citations


@pytest.fixture(scope="module")
def register(vb):
    return vb.build_register.load(ROOT / "docs/sources/register.yaml")


@pytest.fixture(scope="module")
def spec_path(layout):
    specs = layout.components("specification")
    assert len(specs) == 1
    return specs[0].resolve()


def dump(path: Path, data) -> None:
    path.write_bytes(yaml.safe_dump(data, sort_keys=False,
                                    allow_unicode=True).encode("utf-8"))


AGENTS = [
    {"id": "aaron-damiano", "type": "Person", "name": "Aaron Damiano"},
    {"id": "claude-opus-5-5", "type": "SoftwareAgent", "name": "Claude Code",
     "model": "claude-opus-5-5", "acted_on_behalf_of": "aaron-damiano"},
]


def make(tmp_path, vb, layout, spec_path, metamodel=(), catalog=(),
         agents=None, spec=None, repo=None):
    tmp_path.mkdir(parents=True, exist_ok=True)
    dump(tmp_path / "metamodel.yaml", {"version": 1,
                                       "concepts": list(metamodel)})
    dump(tmp_path / "catalog.yaml", {"version": 1, "concepts": list(catalog)})
    dump(tmp_path / "agents.yaml", {"version": 1, "agents": list(
        AGENTS if agents is None else agents)})
    return vb.Inputs(metamodel=tmp_path / "metamodel.yaml",
                     catalog=tmp_path / "catalog.yaml",
                     agents=tmp_path / "agents.yaml",
                     spec=spec or spec_path,
                     register=ROOT / "docs/sources/register.yaml",
                     vendor=layout.vendored_files(), repo=repo or ROOT)


def source(**kw):
    ref = {"source": "SRC-GOV-04", "locator": "NAF v4.1, Capability",
           "relation": "consistent-with"}
    ref.update(kw)
    return ref


def meta(local="CapabilityMap", **kw):
    record = {"id": "bcom:" + local, "spec_row": "ex:" + local,
              "sources": [source()], "drafted_by": AGENT,
              "created": "2026-10-24T00:00:00Z", "authored_status": "Draft"}
    record.update(kw)
    return record


def cat(local="TreasuryManagement", **kw):
    record = {"id": "bcoc:" + local,
              "pref_label": [{"value": "Treasury Management",
                              "language": "en"}],
              "definition": ("A business capability whose realization "
                             "manages the cash and liquidity of an "
                             "organization."),
              "genus": "cco:ont00000568",
              "sources": [source()], "drafted_by": AGENT,
              "created": "2026-10-24T00:00:00Z", "authored_status": "Draft"}
    record.update(kw)
    return record


def codes(result):
    return {f.code for f in result.findings}


def built(vb, inputs):
    result = vb.build(inputs)
    assert not result.findings, [str(f) for f in result.findings]
    return result


def graph_of(result, name):
    import rdflib

    return rdflib.Graph().parse(data=result.files[name].decode("utf-8"),
                                format="turtle")


def refused(vb, inputs, code):
    """Build, and require the specific finding `code`."""
    result = vb.build(inputs)
    assert code in codes(result), (code, [str(f) for f in result.findings])
    assert not result.files, "a build with findings wrote output"
    return result


# ================================================================ D4: section 4


def test_the_spec_parser_finds_the_nine_concrete_rows(st, spec_path):
    parsed = st.parse(spec_path)
    assert not parsed.failures, parsed.failures
    assert [row.local for row in parsed.rows] == SPEC_ROWS
    assert len(parsed.rows) == 9


def test_the_spec_parser_excludes_the_template_rows_by_rule(st, spec_path):
    parsed = st.parse(spec_path)
    assert [term for _, term, _ in parsed.excluded] == TEMPLATE_TERMS
    reasons = [reason for _, _, reason in parsed.excluded]
    assert "and the rest" in reasons[0] and "placeholder" in reasons[1]
    # The annotation-properties table is skipped by header, by name.
    assert [layer for _, layer, _ in parsed.skipped_tables] == [
        "Annotation properties"]


def test_the_spec_parser_keeps_cells_verbatim(st, spec_path):
    rows = {r.local: r for r in st.parse(spec_path).rows}
    text = spec_path.read_bytes().decode("utf-8")
    for row in rows.values():
        assert "| %s |" % row.definition in text
        assert "| %s |" % row.does_not_imply in text
    assert rows["CapabilityAssessment"].does_not_imply.endswith(
        "That `partial` is a fraction of a disposition.")
    assert rows["BusinessCapability"].parents == (
        ("cco", "ont00000568"), ("obo", "BFO_0000016"))
    assert rows["CapabilityTargetStateSpecification"].label == \
        "Capability Target-State Specification"


SECTION = ("## 4. Terms\n\n**Reality layer**\n\n"
           "| Term | Definition | Parents | Does not imply |\n"
           "| --- | --- | --- | --- |\n%s\n\n## 5. Next\n")
GOOD_ROW = "| Capability Map `ex:CapabilityMap` | A thing. | `cco:ont00000853` | Nothing. |"


@pytest.mark.parametrize("row, needle", [
    ("| Capability Mop `ex:CapabilityMap` | A thing. | `cco:ont00000853` | Nothing. |",
     "does not spell its IRI"),
    ("| Capability Map, see `ex:CapabilityMap` and `ex:Other` | A. | `cco:x` | N. |",
     "neither a concrete term nor a recognised template"),
    ("| Capability Map `ex:CapabilityMap` | A thing. | cco:ont00000853 | Nothing. |",
     "Parents cell"),
    ("| Capability Map `ex:CapabilityMap` | A thing. | `cco:ont00000853` |",
     "cells, not 4"),
    (GOOD_ROW + "\n" + GOOD_ROW, "named by two rows"),
])
def test_the_spec_parser_refuses_a_row_it_cannot_classify(st, row, needle):
    parsed = st.parse_text(SECTION % row)
    assert any(needle in message for _, message in parsed.failures), \
        parsed.failures


def test_the_spec_parser_positive_control(st):
    parsed = st.parse_text(SECTION % GOOD_ROW)
    assert not parsed.failures and [r.local for r in parsed.rows] == [
        "CapabilityMap"]


def test_a_spec_without_section_4_is_a_failure(st):
    assert st.parse_text("# Nothing here\n").failures


def test_an_unreadable_spec_fails_the_build(vb, layout, spec_path, tmp_path):
    bad = tmp_path / "spec.md"
    text = spec_path.read_bytes().decode("utf-8")
    mutated = text.replace("Capability Map `ex:CapabilityMap`",
                           "Capability Mop `ex:CapabilityMap`")
    assert mutated != text
    bad.write_bytes(mutated.encode("utf-8"))
    refused(vb, make(tmp_path, vb, layout, spec_path, spec=bad),
            "D4-spec-parse")


def test_a_spec_parent_no_extract_describes_fails(vb, layout, spec_path,
                                                  tmp_path):
    bad = tmp_path / "spec.md"
    text = spec_path.read_bytes().decode("utf-8")
    old = "| A Descriptive ICE that describes an organization and has"
    assert text.count(old) == 1
    row = next(line for line in text.split("\n") if old in line)
    mutated = text.replace(row, row.replace("`cco:ont00000853`",
                                            "`cco:ont99999999`"))
    assert mutated != text
    bad.write_bytes(mutated.encode("utf-8"))
    refused(vb, make(tmp_path, vb, layout, spec_path, spec=bad),
            "D4-parent-unresolved")


def test_a_metamodel_definition_is_refused(vb, layout, spec_path, tmp_path):
    refused(vb, make(tmp_path, vb, layout, spec_path,
                     metamodel=[meta(definition="A map.")]),
            "D4-definition-authored")


def test_a_record_must_name_its_own_row(vb, layout, spec_path, tmp_path):
    refused(vb, make(tmp_path, vb, layout, spec_path,
                     metamodel=[meta(spec_row="ex:CapabilityTarget")]),
            "D4-spec-row-mismatch")


def test_a_record_naming_a_template_row_names_no_row(vb, layout, spec_path,
                                                     tmp_path):
    """The excluded rows have consequences: a record wrapping the
    'and the rest' example is refused, because that row is no term."""
    refused(vb, make(tmp_path, vb, layout, spec_path,
                     metamodel=[meta("StrategicPlanningCapability")]),
            "D4-no-row")


def test_staging_one_record_requires_every_row(vb, layout, spec_path,
                                               tmp_path):
    result = refused(vb, make(tmp_path, vb, layout, spec_path,
                              metamodel=[meta()]), "D4-row-uncovered")
    uncovered = sorted(f.message.split()[3] for f in result.findings
                       if f.code == "D4-row-uncovered")
    assert uncovered == sorted("ex:" + r for r in SPEC_ROWS
                               if r != "CapabilityMap")


def test_staging_an_empty_metamodel_requires_no_row(vb, layout, spec_path,
                                                    tmp_path):
    result = built(vb, make(tmp_path, vb, layout, spec_path))
    assert result.statuses == {} and len(result.spec.rows) == 9


def test_full_metamodel_builds_and_definitions_are_the_rows(
        vb, st, layout, spec_path, tmp_path):
    result = built(vb, make(tmp_path, vb, layout, spec_path,
                            metamodel=[meta(r) for r in SPEC_ROWS]))
    import rdflib

    g = graph_of(result, "bco-metamodel.ttl")
    skos = rdflib.Namespace(vb.SKOS)
    rows = {r.local: r for r in st.parse(spec_path).rows}
    for local in SPEC_ROWS:
        s = rdflib.URIRef(vb.BCOM + local)
        assert [str(o) for o in g.objects(s, skos.definition)] == [
            rows[local].definition]
        assert [str(o) for o in g.objects(s, skos.prefLabel)] == [
            rows[local].label]
        assert list(g.objects(s, rdflib.URIRef(vb.BCO + "designatesClass"))) \
            == [rdflib.URIRef(vb.BCO + local)]
    assert set(result.statuses.values()) == {"Draft"}


# ================================================================ D5: status


@pytest.mark.parametrize("field", ["lifecycle_status", "lifecycleStatus",
                                   "deprecated", "owl:deprecated"])
def test_an_authored_status_field_is_refused(vb, layout, spec_path, tmp_path,
                                             field):
    refused(vb, make(tmp_path, vb, layout, spec_path,
                     catalog=[cat(**{field: "Ratified"})]),
            "D5-status-authored")


def test_an_authored_status_other_than_draft_or_candidate(vb, layout,
                                                         spec_path, tmp_path):
    refused(vb, make(tmp_path, vb, layout, spec_path,
                     catalog=[cat(authored_status="Ratified")]),
            "D5-authored-status")


def test_candidate_is_kept(vb, layout, spec_path, tmp_path):
    result = built(vb, make(tmp_path, vb, layout, spec_path,
                            catalog=[cat(authored_status="Candidate")]))
    assert set(result.statuses.values()) == {"Candidate"}


def test_replacement_by_a_live_concept_deprecates(vb, layout, spec_path,
                                                  tmp_path):
    result = built(vb, make(tmp_path, vb, layout, spec_path, catalog=[
        cat("CashManagement", is_replaced_by="bcoc:TreasuryManagement"),
        cat()]))
    assert result.statuses[vb.BCOC + "CashManagement"] == "Deprecated"
    assert result.statuses[vb.BCOC + "TreasuryManagement"] == "Draft"
    text = result.files["bco-catalog.ttl"].decode("utf-8")
    assert ('bcoc:CashManagement owl:deprecated "true"^^xsd:boolean .'
            in text)
    assert "bcoc:CashManagement dcterms:isReplacedBy bcoc:TreasuryManagement ." \
        in text
    assert "bcoc:TreasuryManagement owl:deprecated" not in text


@pytest.mark.parametrize("catalog", [
    [cat("CashManagement", is_replaced_by="bcoc:Nowhere")],
    [cat("CashManagement", is_replaced_by="bcoc:CashManagement")],
    [cat("A1", is_replaced_by="bcoc:B1"), cat("B1", is_replaced_by="bcoc:C1"),
     cat("C1")],
    [cat("A1", is_replaced_by="bcoc:B1"), cat("B1", is_replaced_by="bcoc:A1")],
], ids=["unknown", "self", "chain", "cycle"])
def test_a_replacement_that_is_not_a_live_concept_is_refused(
        vb, layout, spec_path, tmp_path, catalog):
    refused(vb, make(tmp_path, vb, layout, spec_path, catalog=catalog),
            "D5-replaced-by")


# ================================================================ D2, D3, D5: acts


def git(repo: Path, *args: str) -> str:
    proc = subprocess.run(["git", "-c", "user.name=Fixture",
                           "-c", "user.email=fixture@example.invalid",
                           *args], cwd=str(repo), capture_output=True)
    assert proc.returncode == 0, proc.stderr.decode("utf-8", "replace")
    return proc.stdout.decode("utf-8").strip()


@pytest.fixture
def actrepo(tmp_path):
    repo = tmp_path / "actrepo"
    repo.mkdir()
    git(repo, "init", "-q")
    git(repo, "symbolic-ref", "HEAD", "refs/heads/main")
    (repo / "docs" / "decisions").mkdir(parents=True)
    (repo / "README").write_bytes(b"fixture\n")
    git(repo, "add", "-A")
    git(repo, "commit", "-q", "-m", "root")
    return repo


def act_text(concepts, agent=PERSON_IRI, extra=None, blocks=1):
    body = {"agent": agent, "concepts": concepts}
    if extra:
        body.update(extra)
    block = "```bco-ratification\n%s```\n" % yaml.safe_dump(body,
                                                           sort_keys=False)
    return ("# Ratification act (fixture)\n\n" + block * blocks).encode()


def commit_act(repo: Path, data: bytes, name="2026-11-01-act.md",
               branch=None) -> dict:
    if branch:
        git(repo, "checkout", "-q", "-b", branch)
    path = "docs/decisions/" + name
    (repo / path).write_bytes(data)
    git(repo, "add", "-A")
    git(repo, "commit", "-q", "-m", "act")
    commit = git(repo, "rev-parse", "HEAD")
    if branch:
        git(repo, "checkout", "-q", "main")
    return {"path": path, "commit": commit,
            "sha256": hashlib.sha256(data).hexdigest()}


def ratified_fixture(vb, layout, spec_path, tmp_path, repo, record=None,
                     act=None, **act_kw):
    """Build once to learn the digest, commit an act naming it, cite it."""
    record = record or cat()
    first = built(vb, make(tmp_path / "a", vb, layout, spec_path,
                           catalog=[record], repo=repo))
    iri = vb.BCOC + record["id"].split(":")[1]
    digest = first.digests[iri]
    concepts = act if act is not None else [{"iri": iri,
                                             "record_sha256": digest}]
    cite = commit_act(repo, act_text(concepts, **act_kw))
    return dict(record, ratified_by=cite), iri, digest


def test_a_cited_act_naming_the_current_record_ratifies(
        vb, layout, spec_path, tmp_path, actrepo):
    record, iri, digest = ratified_fixture(vb, layout, spec_path, tmp_path,
                                           actrepo)
    result = built(vb, make(tmp_path / "b", vb, layout, spec_path,
                            catalog=[record], repo=actrepo))
    assert result.statuses[iri] == "Ratified"
    assert result.digests[iri] == digest, "ratified_by moved the digest"
    text = result.files["bco-catalog.ttl"].decode("utf-8")
    assert 'bco:lifecycleStatus "Ratified"' in text
    assert record["ratified_by"]["commit"] in text


def test_d3_an_edit_after_ratification_is_refused(vb, layout, spec_path,
                                                  tmp_path, actrepo):
    record, _, _ = ratified_fixture(vb, layout, spec_path, tmp_path, actrepo)
    edited = dict(record, definition=record["definition"].replace(
        "cash", "money"))
    assert edited["definition"] != record["definition"]
    refused(vb, make(tmp_path / "b", vb, layout, spec_path, catalog=[edited],
                     repo=actrepo), "D3-record-changed")


def test_d3_a_spec_change_breaks_a_ratified_metamodel_concept(
        vb, layout, spec_path, tmp_path, actrepo):
    """D4 + D3: the row is in the record digest, so changing the spec's
    definition un-ratifies the concept that wraps it."""
    records = [meta(r) for r in SPEC_ROWS]
    first = built(vb, make(tmp_path / "a", vb, layout, spec_path,
                           metamodel=records, repo=actrepo))
    iri = vb.BCOM + "CapabilityMap"
    cite = commit_act(actrepo, act_text([{"iri": iri, "record_sha256":
                                          first.digests[iri]}]))
    records = [dict(r, ratified_by=cite) if r["id"] == "bcom:CapabilityMap"
               else r for r in records]
    ok = built(vb, make(tmp_path / "b", vb, layout, spec_path,
                        metamodel=records, repo=actrepo))
    assert ok.statuses[iri] == "Ratified"

    bad = tmp_path / "spec.md"
    text = spec_path.read_bytes().decode("utf-8")
    old = "that are its entries."
    assert text.count(old) == 1
    bad.write_bytes(text.replace(old, "that are its listed entries.")
                    .encode("utf-8"))
    refused(vb, make(tmp_path / "c", vb, layout, spec_path,
                     metamodel=records, spec=bad, repo=actrepo),
            "D3-record-changed")


def test_an_act_that_omits_the_concept(vb, layout, spec_path, tmp_path,
                                       actrepo):
    record, _, digest = ratified_fixture(
        vb, layout, spec_path, tmp_path, actrepo,
        act=[{"iri": "https://fandaws.com/ontology/bco-catalog#Other",
              "record_sha256": "c" * 64}])
    refused(vb, make(tmp_path / "b", vb, layout, spec_path, catalog=[record],
                     repo=actrepo), "D5-act-omits-concept")


@pytest.mark.parametrize("act, extra", [
    ([{"iri": "https://fandaws.com/ontology/bco-catalog#*",
       "record_sha256": "c" * 64}], None),
    ([{"iri": "https://fandaws.com/ontology/bco-catalog#CapabilityCatalogScheme",
       "record_sha256": "c" * 64}], None),
    ([{"iri": "https://fandaws.com/ontology/bco-catalog#",
       "record_sha256": "c" * 64}], None),
    ([{"iri": "bcoc:TreasuryManagement", "record_sha256": "c" * 64}], None),
    (None, {"scheme": "https://fandaws.com/ontology/bco-catalog#CapabilityCatalogScheme"}),
], ids=["wildcard", "scheme-iri", "namespace", "curie", "scheme-key"])
def test_an_act_that_is_not_an_explicit_list_is_refused(
        vb, layout, spec_path, tmp_path, actrepo, act, extra):
    record = cat()
    first = built(vb, make(tmp_path / "a", vb, layout, spec_path,
                           catalog=[record], repo=actrepo))
    iri = vb.BCOC + "TreasuryManagement"
    listed = act if act is not None else [{"iri": iri, "record_sha256":
                                           first.digests[iri]}]
    cite = commit_act(actrepo, act_text(listed, extra=extra))
    refused(vb, make(tmp_path / "b", vb, layout, spec_path,
                     catalog=[dict(record, ratified_by=cite)], repo=actrepo),
            "D5-act-not-explicit")


def test_an_act_with_two_blocks_is_refused(vb, layout, spec_path, tmp_path,
                                           actrepo):
    record = cat()
    cite = commit_act(actrepo, act_text([{"iri": vb.BCOC + "TreasuryManagement",
                                          "record_sha256": "c" * 64}],
                                        blocks=2))
    refused(vb, make(tmp_path, vb, layout, spec_path,
                     catalog=[dict(record, ratified_by=cite)], repo=actrepo),
            "D5-act-block")


def test_d8_a_status_act_by_a_software_agent_is_refused(
        vb, layout, spec_path, tmp_path, actrepo):
    record, _, _ = ratified_fixture(vb, layout, spec_path, tmp_path, actrepo,
                                    agent=SOFTWARE_IRI)
    refused(vb, make(tmp_path / "b", vb, layout, spec_path, catalog=[record],
                     repo=actrepo), "D8-act-agent-not-person")


def test_deprecated_outranks_ratified(vb, layout, spec_path, tmp_path,
                                      actrepo):
    record, iri, _ = ratified_fixture(vb, layout, spec_path, tmp_path,
                                      actrepo)
    # Replacing changes the record, so the act must name the new record.
    replaced = dict(record, is_replaced_by="bcoc:Successor")
    replaced.pop("ratified_by")
    first = built(vb, make(tmp_path / "b", vb, layout, spec_path,
                           catalog=[replaced, cat("Successor")],
                           repo=actrepo))
    cite = commit_act(actrepo, act_text([{"iri": iri, "record_sha256":
                                          first.digests[iri]}]),
                      name="2026-11-02-act.md")
    result = built(vb, make(tmp_path / "c", vb, layout, spec_path,
                            catalog=[dict(replaced, ratified_by=cite),
                                     cat("Successor")], repo=actrepo))
    assert result.statuses[iri] == "Deprecated"


# ---- D2, against the throwaway repository


def good_cite(actrepo, vb):
    return commit_act(actrepo, act_text([{"iri": vb.BCOC + "TreasuryManagement",
                                          "record_sha256": "c" * 64}]))


@pytest.mark.parametrize("change, code", [
    (lambda c: dict(c, commit=c["commit"][:7]), "D2-short-commit"),
    (lambda c: dict(c, sha256="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"),
     "D2-empty-digest"),
    (lambda c: dict(c, path="notes/2026-11-01-act.md"), "D2-path"),
    (lambda c: dict(c, path="docs/decisions/2026-11-09-absent.md"),
     "D2-path-not-in-commit"),
    (lambda c: dict(c, sha256="d" * 64), "D2-digest-mismatch"),
    (lambda c: dict(c, commit="1" * 40), "D2-unknown-commit"),
    (lambda c: dict(c, extra="x"), "D2-citation-shape"),
], ids=["short-commit", "empty-digest", "path-outside", "path-absent",
        "digest-mismatch", "unknown-commit", "shape"])
def test_d2_a_broken_citation_is_refused(vb, cit, layout, spec_path, tmp_path,
                                         actrepo, change, code):
    cite = good_cite(actrepo, vb)
    cit.check_citation(actrepo, cite)  # positive control: the citation holds
    broken = change(cite)
    assert broken != cite
    with pytest.raises(cit.CitationError) as error:
        cit.check_citation(actrepo, broken)
    assert error.value.code == code, (code, str(error.value))
    # and through the build, by the same code
    refused(vb, make(tmp_path, vb, layout, spec_path,
                     catalog=[cat(ratified_by=broken)], repo=actrepo), code)


def test_d2_a_commit_main_does_not_reach_is_refused(vb, cit, actrepo):
    cite = commit_act(actrepo, act_text([{"iri": vb.BCOC + "X",
                                          "record_sha256": "c" * 64}]),
                      branch="side")
    with pytest.raises(cit.CitationError) as error:
        cit.check_citation(actrepo, cite)
    assert error.value.code == "D2-unreachable"
    git(actrepo, "merge", "-q", "--no-ff", "side", "-m", "merge side")
    cit.check_citation(actrepo, cite)  # reachable once merged


def test_d2_the_real_adr_003_citation_holds(cit, repo):
    """Positive control against this repository: the citation the
    ratification act of 2026-10-24 records."""
    blob = cit.check_citation(repo, {
        "path": "docs/adr/ADR-003-controlled-vocabulary.md",
        "commit": "838573f1a22a12ebbc7e5933eecd6cdd1a6c52de",
        "sha256": "899ddc9c96fee90f2088f42693a37e8d8335e4ec9a2140a437f51e024cd02421"})
    assert b"ADR-003" in blob


# ================================================================ D6: sources


def other_id():
    return "SRC-%s-%02d" % ("ZZZ", 99)


def strong_claim(register, vb, src):
    claims = vb.build_register.entries(register)
    entry = next(e for e in claims if e["id"] == src)
    strong = vb.build_register.claims_at_or_above(register, src, "P")
    return next(n for n, c in enumerate(entry["claims"], 1)
                if dict(c) in strong)


def weak_claim(register, vb):
    for entry in vb.build_register.entries(register):
        strong = vb.build_register.claims_at_or_above(register, entry["id"],
                                                      "P")
        for n, claim in enumerate(entry["claims"], 1):
            if dict(claim) not in strong:
                return entry["id"], n
    raise AssertionError("the register has no claim below P")


def test_departs_from_a_v_claim_builds(vb, register, layout, spec_path,
                                       tmp_path):
    n = strong_claim(register, vb, "SRC-OMG-03")
    ref = source(source="SRC-OMG-03", relation="departs-from", claim=n,
                 locator="BACM 1.1, clause 7.2",
                 departure_note="The BCO bearer is an organization only.")
    result = built(vb, make(tmp_path, vb, layout, spec_path,
                            catalog=[cat(sources=[ref])]))
    text = result.files["bco-catalog.ttl"].decode("utf-8")
    assert "bco:citesSource bcos:SRC-OMG-03 ." in text
    assert '"departs-from"' in text


@pytest.mark.parametrize("ref, code", [
    (lambda r, v: source(source=other_id()), "D6-unknown-source"),
    (lambda r, v: source(locator=""), "D6-locator-missing"),
    (lambda r, v: {k: x for k, x in source().items() if k != "locator"},
     "D6-locator-missing"),
    (lambda r, v: source(relation="inspired-by"), "D6-relation"),
    (lambda r, v: source(source="SRC-OMG-03", relation="departs-from",
                         claim=strong_claim(r, v, "SRC-OMG-03")),
     "D6-departure-note"),
    (lambda r, v: source(source=weak_claim(r, v)[0], relation="departs-from",
                         claim=weak_claim(r, v)[1], departure_note="Why."),
     "D6-departure-claim"),
    (lambda r, v: source(source="SRC-OMG-03", relation="departs-from",
                         claim=99, departure_note="Why."),
     "D6-departure-claim"),
    (lambda r, v: source(source="SRC-OMG-03", relation="departs-from",
                         departure_note="Why."), "D6-departure-claim"),
    (lambda r, v: source(departure_note="Why."), "D6-reference-shape"),
], ids=["unknown-id", "empty-locator", "no-locator", "relation",
        "no-departure-note", "claim-below-P", "claim-out-of-range",
        "no-claim", "note-without-departure"])
def test_a_bad_source_reference_is_refused(vb, register, layout, spec_path,
                                           tmp_path, ref, code):
    refused(vb, make(tmp_path, vb, layout, spec_path,
                     catalog=[cat(sources=[ref(register, vb)])]), code)


def test_a_concept_without_sources_is_refused(vb, layout, spec_path, tmp_path):
    refused(vb, make(tmp_path, vb, layout, spec_path,
                     catalog=[cat(sources=[])]), "D6-no-sources")


def test_the_quote_tripwire_names_the_quote(vb, register, layout, spec_path,
                                            tmp_path):
    entry = next(e for e in vb.build_register.entries(register)
                 if e["id"] == "SRC-GOV-04")
    quote = entry["quotes"][0]
    # Case and punctuation differ from the quote; the words do not.
    words = quote["text"].split()
    lifted = " ".join(words[:7]).upper().replace(" ", ", ", 1)
    definition = "A business capability that is the %s, roughly." % lifted
    result = refused(vb, make(tmp_path, vb, layout, spec_path,
                              catalog=[cat(definition=definition)]),
                     "D6-quote-tripwire")
    assert any(quote["key"] in f.message for f in result.findings
               if f.code == "D6-quote-tripwire")


def test_the_quote_tripwire_allows_five_words(vb, register, layout, spec_path,
                                              tmp_path):
    entry = next(e for e in vb.build_register.entries(register)
                 if e["id"] == "SRC-GOV-04")
    words = entry["quotes"][0]["text"].split()
    definition = ("A business capability whose bearer has the %s, and "
                  "nothing more." % " ".join(words[:5]))
    built(vb, make(tmp_path, vb, layout, spec_path,
                   catalog=[cat(definition=definition)]))


# ================================================================ catalog, D7


def test_a_typed_notation_is_emitted(vb, layout, spec_path, tmp_path):
    result = built(vb, make(tmp_path, vb, layout, spec_path,
                            catalog=[cat(notation="10759")]))
    assert ('skos:notation "10759"^^bco:PCFCode .'
            in result.files["bco-catalog.ttl"].decode("utf-8"))
    vocab = result.files["bco-vocabulary.ttl"].decode("utf-8")
    assert "bco:PCFCode rdf:type rdfs:Datatype ." in vocab


@pytest.mark.parametrize("record, code", [
    (cat(notation="1.1.2"), "D7-notation"),
    (cat(notation=10759), "D7-notation"),
    (cat(narrower=["bcoc:CashManagement"]), "catalog-narrower"),
    (cat(broader=["bcoc:Nowhere"]), "catalog-broader"),
    (cat(genus="cco:ont99999999"), "catalog-genus"),
    (cat(genus="bco:BusinessCapability"), "catalog-genus"),
    (cat(definition="Manages cash."), "catalog-definition-form"),
    (cat(pref_label=[{"value": "Tresorerie", "language": "fr"}]),
     "catalog-label"),
    (cat(pref_label=[{"value": "A", "language": "en"},
                     {"value": "B", "language": "en"}]), "catalog-label"),
    (cat(designates_class="ex:TreasuryManagement"),
     "catalog-designates-class"),
    (cat(colour="blue"), "record-unknown-field"),
    ({k: v for k, v in cat().items() if k != "genus"}, "record-missing-field"),
], ids=["notation-form", "notation-untyped-int", "narrower", "broader",
        "genus-unknown", "genus-not-upstream", "definition-form", "no-english",
        "two-english", "designates-class", "unknown-field", "missing-field"])
def test_a_bad_catalog_record_is_refused(vb, layout, spec_path, tmp_path,
                                         record, code):
    refused(vb, make(tmp_path, vb, layout, spec_path, catalog=[record]), code)


def test_broader_between_catalog_concepts_builds(vb, layout, spec_path,
                                                 tmp_path):
    result = built(vb, make(tmp_path, vb, layout, spec_path, catalog=[
        cat("FinancialManagement"),
        cat(broader=["bcoc:FinancialManagement"])]))
    assert ("bcoc:TreasuryManagement skos:broader bcoc:FinancialManagement ."
            in result.files["bco-catalog.ttl"].decode("utf-8"))


# ================================================================ D8: agents


def test_an_undeclared_drafting_agent_is_refused(vb, layout, spec_path,
                                                 tmp_path):
    refused(vb, make(tmp_path, vb, layout, spec_path,
                     catalog=[cat(drafted_by="bcoa:somebody-else")]),
            "D8-undeclared-agent")


@pytest.mark.parametrize("agents", [
    [AGENTS[0], dict(AGENTS[1], acted_on_behalf_of="nobody")],
    [AGENTS[0], {k: v for k, v in AGENTS[1].items() if k != "model"}],
    [AGENTS[0], dict(AGENTS[1], acted_on_behalf_of="claude-opus-5-5")],
    [dict(AGENTS[0], type="Organization"), AGENTS[1]],
    [dict(AGENTS[0], model="x"), AGENTS[1]],
    [AGENTS[0], AGENTS[0], AGENTS[1]],
], ids=["principal-undeclared", "no-model", "principal-not-a-person",
        "unknown-type", "person-with-model", "duplicate"])
def test_a_bad_agent_declaration_is_refused(vb, layout, spec_path, tmp_path,
                                            agents):
    refused(vb, make(tmp_path, vb, layout, spec_path, agents=agents),
            "D8-agent-shape")


def test_the_real_agents_are_declared_as_d8_says(vb, layout):
    result = built(vb, vb.default_inputs())
    text = result.files["bco-agents.ttl"].decode("utf-8")
    assert "bcoa:aaron-damiano rdf:type prov:Person ." in text
    assert "bcoa:claude-opus-5-5 rdf:type prov:SoftwareAgent ." in text
    assert 'bcoa:claude-opus-5-5 bco:modelIdentifier "claude-opus-5-5" .' in text
    assert ("bcoa:claude-opus-5-5 prov:actedOnBehalfOf bcoa:aaron-damiano ."
            in text)


# ================================================================ D3 history


def test_revises_needs_a_change_note(vb, layout, spec_path, tmp_path):
    refused(vb, make(tmp_path, vb, layout, spec_path,
                     catalog=[cat(revises="a" * 64)]), "D3-revises")


def test_revises_links_record_versions(vb, layout, spec_path, tmp_path):
    result = built(vb, make(tmp_path, vb, layout, spec_path, catalog=[
        cat(revises="a" * 64, change_note=["Wording tightened."])]))
    text = result.files["bco-catalog.ttl"].decode("utf-8")
    assert "prov:wasRevisionOf bcoc:record-%s ." % ("a" * 64) in text
    assert 'skos:changeNote "Wording tightened."@en' in text


# ================================================================ record digest


def test_the_record_digest_is_the_documented_bytes(vb, st, spec_path):
    record = cat()
    expected = hashlib.sha256(json.dumps(
        record, sort_keys=True, ensure_ascii=False,
        separators=(",", ":")).encode("utf-8")).hexdigest()
    assert vb.record_digest(record) == expected
    # ratified_by is not part of the record
    cited = dict(record, ratified_by={"path": "docs/decisions/x.md",
                                      "commit": "1" * 40, "sha256": "2" * 64})
    assert vb.record_digest(cited) == expected
    # a metamodel record includes its section 4 row
    row = st.parse(spec_path).rows[1]
    body = dict(meta(), spec_row_content=row.content())
    assert vb.record_digest(meta(), row) == hashlib.sha256(json.dumps(
        body, sort_keys=True, ensure_ascii=False,
        separators=(",", ":")).encode("utf-8")).hexdigest()
    assert vb.record_digest(meta(), row) != vb.record_digest(meta())


def test_an_unquoted_timestamp_is_refused(vb, layout, spec_path, tmp_path):
    inputs = make(tmp_path, vb, layout, spec_path, catalog=[cat()])
    text = inputs.catalog.read_bytes().decode("utf-8")
    mutated = text.replace("'2026-10-24T00:00:00Z'", "2026-10-24T00:00:00Z")
    assert mutated != text
    inputs.catalog.write_bytes(mutated.encode("utf-8"))
    result = refused(vb, inputs, "record-created")
    assert "record-digest" in codes(result)


# ================================================================ D9: IRIs


def test_namespaces_are_exactly_adr_003_d1s(vb, repo):
    """Read from the ratified ADR's D1 table, not typed here."""
    text = (repo / "docs/adr/ADR-003-controlled-vocabulary.md").read_bytes() \
        .decode("utf-8")
    d1 = text.split("### D1")[1].split("### D2")[0]
    table = dict(re.findall(r"^\| `(\w+):` \| `([^`]+)` \|", d1, flags=re.M))
    assert table == dict(vb.NAMESPACES)
    assert len(table) == 5


def test_no_blank_nodes_and_provenance_iris_are_content_minted(
        vb, register, layout, spec_path, tmp_path):
    import rdflib

    n = strong_claim(register, vb, "SRC-OMG-03")
    ref = source(source="SRC-OMG-03", relation="departs-from", claim=n,
                 departure_note="Organization only.")
    result = built(vb, make(tmp_path / "a", vb, layout, spec_path,
                            metamodel=[meta(r, sources=[ref])
                                       for r in SPEC_ROWS],
                            catalog=[cat(sources=[ref])]))
    for name in result.files:
        g = graph_of(result, name)
        assert not any(isinstance(t, rdflib.BNode) for triple in g
                       for t in triple), name
    text = result.files["bco-catalog.ttl"].decode("utf-8")
    minted = vb.minted(vb.BCOC, "source", ref)
    assert re.fullmatch(re.escape(vb.BCOC) + r"source-[0-9a-f]{64}", minted)
    assert "bcoc:source-%s" % minted.rsplit("-", 1)[1] in text
    assert "bcom:source-%s" % minted.rsplit("-", 1)[1] in \
        result.files["bco-metamodel.ttl"].decode("utf-8")
    # the IRI is a function of the content: change the locator, it moves
    moved = vb.minted(vb.BCOC, "source", dict(ref, locator="elsewhere"))
    assert moved != minted


def test_sources_graph_has_one_record_per_register_entry(vb, register):
    import rdflib

    result = built(vb, vb.default_inputs())
    g = graph_of(result, "bco-sources.ttl")
    ids = {str(o) for o in g.objects(None, rdflib.URIRef(
        vb.DCTERMS + "identifier"))}
    assert ids == vb.build_register.known_ids(register)
    assert len(ids) == vb.build_register.EXPECTED_ENTRY_COUNT
    for src in ids:
        s = rdflib.URIRef(vb.BCOS + src)
        assert g.value(s, rdflib.URIRef(vb.DCTERMS + "bibliographicCitation"))
        assert g.value(s, rdflib.URIRef(vb.BCO + "claimStatus"))


# ================================================================ inputs


def test_an_absent_input_file_is_not_an_empty_one(vb, layout, spec_path,
                                                  tmp_path):
    inputs = make(tmp_path, vb, layout, spec_path)
    inputs.catalog.unlink()
    refused(vb, inputs, "input-missing")


def test_a_cr_in_an_input_is_refused(vb, layout, spec_path, tmp_path):
    inputs = make(tmp_path, vb, layout, spec_path)
    inputs.agents.write_bytes(inputs.agents.read_bytes().replace(b"\n",
                                                                 b"\r\n"))
    refused(vb, inputs, "input-shape")


def test_a_duplicate_concept_is_refused(vb, layout, spec_path, tmp_path):
    refused(vb, make(tmp_path, vb, layout, spec_path, catalog=[cat(), cat()]),
            "record-id")


# ================================================================ determinism


def rich(vb, register, layout, spec_path, tmp_path):
    n = strong_claim(register, vb, "SRC-OMG-03")
    ref = source(source="SRC-OMG-03", relation="departs-from", claim=n,
                 departure_note="Organization only.")
    return make(tmp_path, vb, layout, spec_path,
                metamodel=[meta(r, sources=[ref, source()])
                           for r in SPEC_ROWS],
                catalog=[cat("FinancialManagement"),
                         cat(broader=["bcoc:FinancialManagement"],
                             notation="10759", change_note=["x"],
                             revises="b" * 64),
                         cat("CashManagement",
                             is_replaced_by="bcoc:TreasuryManagement")])


def test_the_build_is_independent_of_input_order(vb, register, layout,
                                                 spec_path, tmp_path):
    one = built(vb, rich(vb, register, layout, spec_path, tmp_path / "a"))
    inputs = rich(vb, register, layout, spec_path, tmp_path / "b")
    for path in (inputs.metamodel, inputs.catalog):
        data = yaml.safe_load(path.read_bytes().decode("utf-8"))
        data["concepts"].reverse()
        dump(path, data)
    two = built(vb, inputs)
    assert one.files == two.files
    assert len(one.files) == 5 and all(one.files.values())


def run_build(*args, cwd=ROOT, seed=None):
    env = dict(os.environ)
    env.pop("PYTHONHASHSEED", None)
    if seed is not None:
        env["PYTHONHASHSEED"] = str(seed)
    proc = subprocess.run([sys.executable, str(ROOT / "tools/vocab/build.py"),
                           *args], cwd=str(cwd), env=env, capture_output=True)
    return proc.returncode, (proc.stdout + proc.stderr).decode("utf-8",
                                                             "replace")


def test_two_builds_into_different_paths_are_byte_identical(tmp_path):
    a = tmp_path / "one"
    b = tmp_path / "x" / "y" / "z" / "two"
    assert run_build("--out", str(a), seed=0)[0] == 0
    assert run_build("--out", str(b), cwd=tmp_path, seed=4242)[0] == 0
    names = sorted(p.name for p in a.iterdir())
    assert names == sorted(p.name for p in b.iterdir())
    assert len(names) == 5
    for name in names:
        assert (a / name).read_bytes() == (b / name).read_bytes(), name
        assert b"\r" not in (a / name).read_bytes()


def test_the_committed_turtle_is_a_fresh_build(vb, layout):
    result = built(vb, vb.default_inputs())
    paths = vb.output_paths()
    assert sorted(paths) == sorted(result.files)
    assert not vb.freshness(result, paths)
    code, out = run_build()
    assert code == 0, out


def test_a_stale_committed_file_is_caught(vb, tmp_path):
    result = built(vb, vb.default_inputs())
    paths = {}
    for name, data in result.files.items():
        paths[name] = tmp_path / name
        paths[name].write_bytes(data)
    assert not vb.freshness(result, paths)
    tampered = paths["bco-agents.ttl"].read_bytes() + b"# edited\n"
    paths["bco-agents.ttl"].write_bytes(tampered)
    found = vb.freshness(result, paths)
    assert [f.code for f in found] == ["generated-stale"]
    assert "bco-agents.ttl" in found[0].message


def test_every_generated_file_names_the_build_as_its_generator(vb, layout):
    for name, cid in vb.OUTPUT_IDS.items():
        component = layout.component(cid)
        assert component.role == "generated-artifact"
        assert component.generator == "tool.vocab-build"
        assert component.path.endswith("/" + name)
    assert layout.component("tool.vocab-build").path == "tools/vocab/build.py"


# ================================================================ LinkML boundary


def test_the_main_suite_does_not_import_linkml(vb):
    assert not any(name == "linkml" or name.startswith("linkml")
                   for name in sys.modules), "LinkML was imported"
    dev = (ROOT / "requirements-dev.txt").read_text(encoding="utf-8")
    assert "linkml" not in dev.lower()


def pins(path: Path) -> dict:
    out = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            name, version = line.split("==")
            out[name.lower().replace("_", "-")] = version
    return out


def test_the_vocab_pin_is_whole_and_agrees_with_the_dev_pins():
    vocab = pins(ROOT / "requirements-vocab.txt")
    dev = pins(ROOT / "requirements-dev.txt")
    assert len(vocab) == 91
    assert vocab["linkml"] == "1.11.1" and vocab["linkml-runtime"] == "1.11.1"
    shared = sorted(set(vocab) & set(dev))
    assert shared, "no shared pins, so the comparison below compares nothing"
    assert {n: vocab[n] for n in shared} == {n: dev[n] for n in shared}


def test_the_json_schema_and_the_build_describe_the_same_records(vb, layout):
    """The committed gen-json-schema output, read without LinkML: its
    closed property sets must be the build's, so the two cannot drift."""
    component = layout.component("generated.vocab-json-schema")
    assert component.generator == "tool.vocab-schema-check"
    raw = component.resolve().read_bytes()
    assert b"\r" not in raw
    defs = json.loads(raw)["$defs"]
    assert set(defs["MetamodelConcept"]["properties"]) == vb.METAMODEL_FIELDS
    assert set(defs["CatalogConcept"]["properties"]) == vb.CATALOG_FIELDS
    assert set(defs["SourceReference"]["properties"]) == vb.SOURCE_FIELDS
    assert set(defs["Agent"]["properties"]) == vb.AGENT_FIELDS
    for name in ("MetamodelConcept", "CatalogConcept", "SourceReference",
                 "Agent"):
        assert defs[name]["additionalProperties"] is False, name
    assert defs["AuthoredStatus"]["enum"] == list(vb.AUTHORED_STATUSES)
    assert defs["SourceRelation"]["enum"] == list(vb.RELATIONS)


def test_ci_runs_the_build_and_keeps_linkml_in_its_own_job(repo):
    """Read the workflow as YAML, so a step named in a comment does not
    count (docs/process/PROCESS.md section 1, the fetch-depth row)."""
    workflow = yaml.safe_load((repo / ".github/workflows/checks.yml")
                              .read_bytes().decode("utf-8"))
    jobs = workflow["jobs"]
    main_runs = [step.get("run", "") for step in jobs["checks"]["steps"]]
    assert "python tools/vocab/build.py" in [r.strip() for r in main_runs]
    assert not any("requirements-vocab" in r or "linkml" in r.lower()
                   for r in main_runs)
    checkout = jobs["checks"]["steps"][0]
    assert checkout["with"]["fetch-depth"] == 0, \
        "D2 reachability needs origin/main in the checkout"
    vocab_runs = "\n".join(step.get("run", "")
                           for step in jobs["vocab-schema"]["steps"])
    assert "pip install -r requirements-vocab.txt" in vocab_runs
    assert "python tools/vocab/schema_check.py" in vocab_runs
