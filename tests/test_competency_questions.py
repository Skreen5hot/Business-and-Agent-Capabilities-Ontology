"""CP-2: the competency questions over controlled fixture organizations
(docs/decisions/2026-11-15-d6-class-increment-accepted.md, D).

Each answerable question is a SPARQL query, run over the real module, the
vendored extracts and tests/fixtures/cq_organizations.ttl, and each must
return the expected answer from that data. Each question that cannot be
answered -- a missing relation, an unminted term, an unsupported query --
is a test that SKIPS with the reason. A skip is never a pass: the CP-2
record counts them as not demonstrated.

The questions are specification v0.5.0-draft.3, section 7.
"""

from __future__ import annotations

import pytest

BCO = "https://fandaws.com/ontology/bco#"
BPO = "https://fandaws.com/ontology/bpo#"

PREFIXES = """
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl:  <http://www.w3.org/2002/07/owl#>
PREFIX obo:  <http://purl.obolibrary.org/obo/>
PREFIX cco:  <https://www.commoncoreontologies.org/>
PREFIX ex:   <https://fandaws.com/ontology/bpo#>
PREFIX bco:  <https://fandaws.com/ontology/bco#>
"""

#: CQ-1. Business Capabilities O bears, bearing normalized to has capability.
CQ1 = PREFIXES + """
SELECT DISTINCT ?capability WHERE {
  { ?org cco:ont00001954 ?capability } UNION { ?capability cco:ont00001889 ?org }
  ?capability a ?class .
  ?class rdfs:subClassOf* bco:BusinessCapability .
}"""

#: CQ-1, reported apart: claims on staged classes (CD2).
CQ1_STAGED = PREFIXES + """
SELECT DISTINCT ?claim WHERE {
  { ?org cco:ont00001954 ?claim } UNION { ?claim cco:ont00001889 ?org }
  ?claim a ?class .
  ?class rdfs:subClassOf+ cco:ont00000568 .
  FILTER NOT EXISTS { ?class rdfs:subClassOf* bco:BusinessCapability }
}"""

#: CQ-2. The admissible realizations of capability type C: its index.
CQ2 = PREFIXES + """
SELECT ?act WHERE { ?type ex:enablesProcess ?act . }"""

#: CQ-3. The capabilities an act realized, filtered by CAP-21 (the act's
#: asserted type under an index member of the capability's class) and
#: CAP-34 (a member agent of the bearer performs it).
CQ3 = PREFIXES + """
SELECT DISTINCT ?capability WHERE {
  { ?act obo:BFO_0000055 ?capability } UNION { ?capability obo:BFO_0000054 ?act }
  ?capability a ?class .
  ?class rdfs:subClassOf* bco:BusinessCapability .
  ?class ex:enablesProcess ?member .
  ?act a ?asserted . ?asserted rdfs:subClassOf* ?member .
  { ?bearer cco:ont00001954 ?capability } UNION { ?capability cco:ont00001889 ?bearer }
  { ?act cco:ont00001833 ?agent } UNION { ?agent cco:ont00001787 ?act }
  { ?bearer obo:BFO_0000115 ?agent } UNION { ?agent obo:BFO_0000129 ?bearer }
}"""

#: CQ-10. Capability classes that have not passed G1-T: under Organization
#: Capability and not under bco:BusinessCapability. Standard S4 writes a
#: class under the parent only after its PASS, so the asserted hierarchy
#: answers it.
CQ10 = PREFIXES + """
SELECT DISTINCT ?class WHERE {
  ?class a owl:Class ; rdfs:subClassOf+ cco:ont00000568 .
  FILTER(STRSTARTS(STR(?class), "https://fandaws.com/ontology/bco#"))
  FILTER NOT EXISTS { ?class rdfs:subClassOf* bco:BusinessCapability }
}"""

#: Not demonstrable over this tranche, with the reason each is reported.
BLOCKED = {
    "CQ-4": "absence over a realization log needs a completeness manifest "
            "(CD15); no manifest encoding or schema exists (Gate M)",
    "CQ-5": "needs bco:AuthorizationRecord and bco:concernsType, which are "
            "not minted, and a completeness manifest (Gate M)",
    "CQ-6": "needs bco:CapabilityMap, bco:CapabilityAssessment, "
            "bco:CapabilityTarget, bco:concernsType and "
            "bco:assessedPresence, which are not minted",
    "CQ-7": "needs bco:CapabilitySourcingStatement and bco:concernsType, "
            "which are not minted",
    "CQ-8": "needs bco:CapabilityTarget and bco:concernsType, which are not "
            "minted",
    "CQ-9": "needs ex:designatesProcessType from APQC catalog nodes, which "
            "the BPO import boundary keeps out of the graph (Stage 05 "
            "standard section 4), and the coverage register (CD16), which "
            "is Stage 06's",
    "CQ-11": "no ontology relation records development (OI-4, as the "
             "specification says); the answer exists only in the tranche "
             "record's development_members, which is empty for this "
             "tranche, so no SPARQL query answers it",
    "CQ-12": "needs the coverage register's standing functions (CD16), "
             "which are Stage 06's",
    "CQ-13": "needs bco:CapabilityAssessment and bco:assessedPresence "
             "(CAP-26), which are not minted",
    "CQ-14": "needs bco:CapabilitySourcingStatement and "
             "bco:CapabilitySourcingAssessment, which are not minted",
    "CAP-18": "absence queries returning unknown outside a manifest's scope "
              "need the CD15 manifest and bco:AuthorizationRecord; neither "
              "exists",
}


@pytest.fixture(scope="module")
def graph(repo, layout):
    import rdflib

    g = rdflib.Graph()
    for path in layout.ontology_files() + layout.vendored_files():
        g.parse(path, format="turtle")
    g.parse(repo / "tests/fixtures/cq_organizations.ttl", format="turtle")
    return g


def answer(graph, query, **bindings) -> set:
    import rdflib

    init = {k: rdflib.URIRef(v) for k, v in bindings.items()}
    return {str(row[0]) for row in graph.query(query, initBindings=init)}


# -------------------------------------------------------------------- CQ-1


def test_cq1_the_capabilities_an_organization_bears(graph):
    assert answer(graph, CQ1, org=BCO + "fixture_cq_org") == {
        BCO + "fixture_cq_payroll", BCO + "fixture_cq_cash"}
    assert answer(graph, CQ1, org=BCO + "fixture_cq_other") == {
        BCO + "fixture_cq_other_ap"}
    # The vendor bears none: its staff performing an act is not bearing.
    assert answer(graph, CQ1, org=BCO + "fixture_cq_vendor") == set()


def test_cq1_staged_claims_are_reported_apart(graph):
    org = BCO + "fixture_cq_org"
    assert answer(graph, CQ1_STAGED, org=org) == {BCO + "fixture_cq_staged"}
    assert BCO + "fixture_cq_staged" not in answer(graph, CQ1, org=org)


# -------------------------------------------------------------------- CQ-2


def test_cq2_admissible_realizations_are_the_index(graph):
    assert answer(graph, CQ2, type=BCO + "PayrollProcessing") == {
        BPO + "P108%d" % n for n in range(58, 69)}
    assert answer(graph, CQ2, type=BCO + "CashManagement") == {
        BPO + "P10893", BPO + "P10895", BPO + "P10898"}
    # The parent has no index (CAP-03 excepts it).
    assert answer(graph, CQ2, type=BCO + "BusinessCapability") == set()


# -------------------------------------------------------------------- CQ-3


def test_cq3_the_capabilities_an_act_realized(graph):
    assert answer(graph, CQ3, act=BCO + "fixture_cq_run_october") == {
        BCO + "fixture_cq_payroll"}
    # Written as has realization and agent in.
    assert answer(graph, CQ3, act=BCO + "fixture_cq_cash_position") == {
        BCO + "fixture_cq_cash"}


def test_cq3_excludes_the_vendor_case_and_the_misfiled_act(graph):
    """Both are asserted to realize payroll processing; neither counts.
    The vendor's staff perform one (CAP-34); the other is asserted outside
    the index (CAP-21)."""
    assert answer(graph, CQ3, act=BCO + "fixture_cq_run_vendor") == set()
    assert answer(graph, CQ3, act=BCO + "fixture_cq_misfiled") == set()


# ------------------------------------------------------------------- CQ-10


def test_cq10_classes_that_have_not_passed_g1t(graph):
    """Over the real module, none of the 40 written classes; the fixture's
    staged class is the one that has not passed."""
    assert answer(graph, CQ10) == {BCO + "FixtureCqStagedClass"}


# ------------------------------------------- the same data under the shapes


def test_the_fixture_organizations_under_the_instance_shapes(graph, layout):
    """The instance shapes over the real classes: the valid individuals
    conform, and the two acts CQ-3 excludes are exactly what CAP-34 and
    CAP-21 report."""
    import rdflib
    from pyshacl import validate as shacl

    shapes = rdflib.Graph().parse(layout.path("validation.instances"),
                                  format="turtle")
    _, results, _ = shacl(data_graph=graph, shacl_graph=shapes,
                          inference="none", advanced=True)
    SH = rdflib.Namespace("http://www.w3.org/ns/shacl#")
    found = {(str(results.value(r, SH.focusNode)),
              str(results.value(r, SH.resultMessage)).split(":")[0])
             for r in results.subjects(rdflib.RDF.type, SH.ValidationResult)}
    assert found == {(BCO + "fixture_cq_payroll", "CAP-34"),
                     (BCO + "fixture_cq_payroll", "CAP-21")}, found


# ------------------------------------------------------- not demonstrated


@pytest.mark.parametrize("question", sorted(BLOCKED))
def test_not_demonstrated(question):
    """Reported, never counted: each of these needs a term, relation or
    encoding that does not exist (src/05_ontology/README.md, CP-2)."""
    pytest.skip("%s not demonstrated: %s" % (question, BLOCKED[question]))
