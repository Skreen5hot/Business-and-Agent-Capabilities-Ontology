"""CP-2: the competency questions over controlled fixture organizations
(docs/decisions/2026-11-15-d6-class-increment-accepted.md, D; and the
decision of 2026-11-15, B-1 to B-4,
docs/decisions/2026-11-15-b1-b4-approved-cap34-confirmed.md).

Each question is answered over the real modules, the vendored extracts and
the test-only fixtures tests/fixtures/cq_organizations.ttl and
cq_description.ttl, by the method the decisions name:

  SPARQL            CQ-1, CQ-2, CQ-3, CQ-6, CQ-7, CQ-8, CQ-10, CQ-13, CQ-14
  SPARQL over a     CQ-9 and CQ-12, with the TEST-ONLY coverage register
  test register     tests/fixtures/coverage_register.yaml (B-3). Demonstrated
                    over fixture data only; the production register is
                    Stage 06's and is not implemented
  CD15 manifests    CQ-4 and CQ-5, answered recorded, none recorded or
                    unknown within a manifest's scope (B-2;
                    tools/ontology/manifests.py)
  review records    CQ-11, extracted from the signed G1-T records (B-4;
                    tools/ontology/review_records.py): a review-record
                    answer, not an OWL inference or a SPARQL answer

The questions are specification v0.5.0-draft.3, section 7.
"""

from __future__ import annotations

import pytest

from conftest import load_tool

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

#: CQ-6. Types O's map records as needed (a target entry) with no
#: assessment entry finding them present. Only completed assessments are
#: entries (CD14).
CQ6 = PREFIXES + """
SELECT DISTINCT ?type WHERE {
  ?map a bco:CapabilityMap ; cco:ont00001982 ?org ; obo:BFO_0000178 ?t .
  ?t a bco:CapabilityTarget ; bco:concernsType ?type .
  FILTER NOT EXISTS {
    ?map obo:BFO_0000178 ?a .
    ?a a bco:CapabilityAssessment ; bco:concernsType ?type ;
       bco:assessedPresence ?p .
    FILTER(STR(?p) = "present") }
}"""

#: CQ-7. O's two-party sourcing arrangements (CAP-23): the act class, the
#: provider, and whether O also bears a capability whose index has an act
#: under that class (hybrid work).
CQ7 = PREFIXES + """
SELECT ?act ?provider ?bears WHERE {
  ?s a bco:CapabilitySourcingStatement ; cco:ont00001982 ?org ;
     cco:ont00001808 ?provider ; bco:concernsType ?act .
  ?provider a cco:ont00001180 .
  BIND(EXISTS {
    { ?org cco:ont00001954 ?c } UNION { ?c cco:ont00001889 ?org }
    ?c a ?K . ?K rdfs:subClassOf* bco:BusinessCapability .
    ?K ex:enablesProcess ?m . ?m rdfs:subClassOf* ?act } AS ?bears)
}"""

#: CQ-8. O's targets, and whether each matches a capability O bears.
CQ8 = PREFIXES + """
SELECT ?type ?matched WHERE {
  ?t a bco:CapabilityTarget ; cco:ont00001808 ?org ; bco:concernsType ?type .
  BIND(EXISTS {
    { ?org cco:ont00001954 ?c } UNION { ?c cco:ont00001889 ?org }
    ?c a ?type } AS ?matched)
}"""

#: CQ-9. Catalog nodes that designate a whole-function capability class
#: (ex:designatesProcessType to a K1 class). Over fixture data only (B-3).
CQ9 = PREFIXES + """
SELECT ?node ?class WHERE {
  ?node ex:designatesProcessType ?class .
  ?class rdfs:subClassOf+ cco:ont00000568 .
}"""

#: CQ-13. O's capability-bearing claims with no supporting present-finding
#: assessment (CAP-26), including those whose only evaluation is incomplete.
CQ13 = PREFIXES + """
SELECT DISTINCT ?claim WHERE {
  { ?org cco:ont00001954 ?claim } UNION { ?claim cco:ont00001889 ?org }
  ?claim a ?K . ?K rdfs:subClassOf+ cco:ont00000568 .
  FILTER NOT EXISTS {
    ?a a bco:CapabilityAssessment ; cco:ont00001982 ?org ;
       cco:ont00001808 ?claim ; bco:concernsType ?type ;
       bco:assessedPresence ?p .
    ?claim a ?type .
    FILTER(STR(?p) = "present") }
}"""

#: CQ-14. O's sourcing arrangements with no sourcing assessment.
CQ14 = PREFIXES + """
SELECT ?s WHERE {
  ?s a bco:CapabilitySourcingStatement ; cco:ont00001982 ?org .
  FILTER NOT EXISTS {
    ?sa a bco:CapabilitySourcingAssessment ; cco:ont00001808 ?s }
}"""


@pytest.fixture(scope="module")
def graph(repo, layout):
    import rdflib

    g = rdflib.Graph()
    for path in layout.ontology_files() + layout.vendored_files():
        g.parse(path, format="turtle")
    g.parse(repo / "tests/fixtures/cq_organizations.ttl", format="turtle")
    g.parse(repo / "tests/fixtures/cq_description.ttl", format="turtle")
    return g


def answer(graph, query, **bindings) -> set:
    import rdflib

    init = {k: rdflib.URIRef(v) for k, v in bindings.items()}
    return {str(row[0]) for row in graph.query(query, initBindings=init)}


# -------------------------------------------------------------------- CQ-1


def test_cq1_the_capabilities_an_organization_bears(graph):
    assert answer(graph, CQ1, org=BCO + "fixture_cq_org") == {
        BCO + "fixture_cq_payroll", BCO + "fixture_cq_cash",
        BCO + "fixture_cq_paytax"}
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


# ---------------------------------------------- CQ-4 and CQ-5 (CD15, Gate M)


@pytest.fixture(scope="module")
def cd15(repo):
    import json

    import rdflib

    tool = load_tool("bco_manifests_cq", "tools/ontology/manifests.py")
    data = json.loads((repo / "tests/fixtures/cd15/manifests.json")
                      .read_bytes().decode("utf-8"))
    manifests = [tool.Manifest.read(e["manifest"])
                 for e in data["valid"] + data["invalid"]
                 if isinstance(e["manifest"].get("graph"), str)]
    dataset = rdflib.Dataset()
    dataset.parse(repo / "tests/fixtures/cd15/evidence.trig", format="trig")
    return tool, manifests, dataset


def test_cq4_capabilities_with_no_recorded_realization(graph, cd15):
    """Over October 2026, within the realization log's manifest: payroll
    has a recorded realization; cash management has none recorded. In
    November, outside the manifest, both are unknown. An empty answer says
    nothing about whether O bears them (CD8)."""
    import datetime as dt

    tool, manifests, dataset = cd15
    org = BCO + "fixture_cq_org"
    borne = answer(graph, CQ1, org=org)

    def cq4(start, end):
        return {c: tool.realization(dataset, graph, manifests, org, c,
                                    start, end).status for c in borne}

    october = cq4(dt.date(2026, 10, 1), dt.date(2026, 10, 31))
    assert october[BCO + "fixture_cq_payroll"] == "recorded"
    assert october[BCO + "fixture_cq_cash"] == "none recorded"
    assert october[BCO + "fixture_cq_paytax"] == "none recorded"
    november = cq4(dt.date(2026, 11, 1), dt.date(2026, 11, 30))
    assert set(november.values()) == {"unknown"}


def test_cq5_index_acts_lacking_an_applicable_authorization(graph, cd15):
    """For O's capabilities (CQ-1), each index act (CQ-2), the clerk, and
    25 June to 5 July 2026: every index act under Act of Reporting is
    recorded throughout (two overlapping records); the remuneration act has
    none recorded in
    scope (the organization's own record does not apply to its member);
    every act class the manifest does not cover is unknown."""
    import datetime as dt

    tool, manifests, dataset = cd15
    org = BCO + "fixture_cq_org"
    acts = set()
    for cap in answer(graph, CQ1, org=org):
        for cls in graph.objects(__import__("rdflib").URIRef(cap),
                                 __import__("rdflib").RDF.type):
            acts |= answer(graph, CQ2, type=str(cls))
    result = {}
    for act in acts:
        segments = tool.authorization_period(
            dataset, graph, manifests, org, BCO + "fixture_cq_clerk", act,
            dt.date(2026, 6, 25), dt.date(2026, 7, 5))
        result[act] = {s[2].status for s in segments}
    import rdflib

    def under(genus):
        return {a for a in acts if rdflib.URIRef(BPO + genus) in
                graph.transitive_objects(rdflib.URIRef(a),
                                         rdflib.RDFS.subClassOf)}

    reporting, remuneration = under("ActOfReporting"), under("ActOfRemuneration")
    assert {BPO + "P10867", BPO + "P10868", BPO + "P10898"} <= reporting
    assert remuneration == {BPO + "P10862"}
    assert {a for a, s in result.items() if s == {"recorded"}} == reporting
    assert {a for a, s in result.items() if s == {"none recorded"}} ==         remuneration
    assert {a for a, s in result.items() if s == {"unknown"}} ==         acts - reporting - remuneration


# -------------------------------------------------------------------- CQ-6


def test_cq6_needed_types_with_no_present_assessment_entry(graph):
    """Cash management (a target, assessed nowhere in the map) and accounts
    payable (a target, assessed absent) are reported; payroll has a present
    assessment entry. The cash evaluation in progress is no entry."""
    assert answer(graph, CQ6, org=BCO + "fixture_cq_org") == {
        BCO + "CashManagement", BCO + "AccountsPayableProcessing"}


# -------------------------------------------------------------------- CQ-7


def rows(graph, query, **bindings) -> set:
    import rdflib

    init = {k: rdflib.URIRef(v) for k, v in bindings.items()}
    return {tuple(str(v) if not isinstance(v, rdflib.Literal) else
                  v.toPython() for v in row)
            for row in graph.query(query, initBindings=init)}


def test_cq7_sourcing_arrangements_and_hybrid_work(graph):
    assert rows(graph, CQ7, org=BCO + "fixture_cq_org") == {
        (BPO + "ActOfRemuneration", BCO + "fixture_cq_vendor", True),
        (BPO + "P10869", BCO + "fixture_cq_vendor", False)}


# -------------------------------------------------------------------- CQ-8


def test_cq8_targets_and_which_already_match(graph):
    assert rows(graph, CQ8, org=BCO + "fixture_cq_org") == {
        (BCO + "PayrollProcessing", True), (BCO + "CashManagement", True),
        (BCO + "AccountsPayableProcessing", False)}


# --------------------------------------------- CQ-9 and CQ-12 (fixture only)


@pytest.fixture(scope="module")
def register(repo):
    """The TEST-ONLY coverage register (B-3); not the production register,
    which is Stage 06's."""
    import yaml

    data = yaml.safe_load((repo / "tests/fixtures/coverage_register.yaml")
                          .read_bytes().decode("utf-8"))
    expand = lambda c: BCO + c.split(":", 1)[1]  # noqa: E731
    return {expand(k): [expand(c) for c in v["components"]]
            for k, v in data["standing_functions"].items()}


def test_cq9_standing_functions_with_a_whole_function_class(graph, register):
    """Demonstrated over fixture data only. One standing function designates
    a whole-function class; the treasury function designates none and is
    represented only by its register entry; a node designating an act class
    is not a standing function with a capability class."""
    payroll = BCO + "fixture_cq_node_payroll_function"
    treasury = BCO + "fixture_cq_node_treasury_function"
    found = rows(graph, CQ9)
    assert found == {(payroll, BCO + "FixtureCqWholePayrollFunction")}
    assert treasury in register and treasury not in {n for n, _ in found}


def test_cq9_designation_is_bpos_declared_annotation(repo):
    """B-3: ex:designatesProcessType is used only after verifying its
    declaration at the approved pin: the vendored extract carries it, from
    ontology/apqc-catalog.ttl at bc64e91, as an owl:AnnotationProperty."""
    import rdflib

    g = rdflib.Graph().parse(repo / "vendor/bpo/bpo-ext-bco-extract.ttl",
                             format="turtle")
    p = rdflib.URIRef(BPO + "designatesProcessType")
    assert (p, rdflib.RDF.type, rdflib.OWL.AnnotationProperty) in g
    text = (repo / "config/upstream-sources.yaml").read_text(encoding="utf-8")
    assert "bc64e91839378e1926189c01bf184d6a22d5c1b7/ontology/apqc-catalog.ttl" \
        in text


def cq12(graph, register, org, function):
    """CQ-12: the register entry for the function joined to CQ-1. Returns
    (every component borne?, the components not borne). Component
    possession only; it writes nothing."""
    import rdflib

    borne = set()
    for cap in answer(graph, CQ1, org=org):
        borne |= {str(c) for c in graph.objects(rdflib.URIRef(cap),
                                                rdflib.RDF.type)}
    missing = [c for c in register[function] if c not in borne]
    return not missing, missing


def test_cq12_component_possession(graph, register):
    org = BCO + "fixture_cq_org"
    assert cq12(graph, register, org,
                BCO + "fixture_cq_node_payroll_function") == (True, [])
    assert cq12(graph, register, org,
                BCO + "fixture_cq_node_treasury_function") == (
        False, [BCO + "InHouseBankAccountManagement"])


def test_cq12_component_possession_is_not_whole_function_possession(
        graph, register):
    """O bears every component of the payroll function and does not bear
    the whole-function class the function designates."""
    org = BCO + "fixture_cq_org"
    assert cq12(graph, register, org,
                BCO + "fixture_cq_node_payroll_function")[0]
    borne_types = rows(graph, PREFIXES + """
        SELECT ?t WHERE { { ?org cco:ont00001954 ?c } UNION
                          { ?c cco:ont00001889 ?org } ?c a ?t }""", org=org)
    assert (BCO + "FixtureCqWholePayrollFunction",) not in borne_types


def test_cq12_establishes_no_integration_availability_or_adequacy(
        graph, register):
    """The adequacy assessment of the same function finds adequacy not met,
    while CQ-12 says every component is borne. Running CQ-12 adds no triple:
    no finding or assessment is generated from it (CAP-29)."""
    before = len(graph)
    assert cq12(graph, register, BCO + "fixture_cq_org",
                BCO + "fixture_cq_node_payroll_function")[0]
    assert len(graph) == before
    adequacy = rows(graph, PREFIXES + """
        PREFIX schema: <https://schema.org/>
        SELECT ?v WHERE { ?faa obo:BFO_0000178 ?f .
          ?f schema:reviewAspect "adequacy for the function" ;
             schema:ratingValue ?v }""")
    assert adequacy == {("not met",)}


def test_cq12_generates_no_subclass_axiom(graph, register):
    """Listing a component creates no subclass link (CD16, CAP-22), and the
    whole-function class is not among its own function's components."""
    import rdflib

    whole = rdflib.URIRef(BCO + "FixtureCqWholePayrollFunction")
    for function, components in register.items():
        assert str(whole) not in components
        for c in components:
            c = rdflib.URIRef(c)
            assert (c, rdflib.RDFS.subClassOf, whole) not in graph
            assert (whole, rdflib.RDFS.subClassOf, c) not in graph
    assert set(graph.objects(whole, rdflib.RDFS.subClassOf)) == {
        rdflib.URIRef(BCO + "BusinessCapability")}


def register_findings(graph, register) -> list:
    """CAP-22 over a coverage register: every key is a catalog concept (a
    skos:Concept here, standing in for an APQC one) and not a capability
    class; every component is a written K1 class; a function's designated
    whole-function class is never among its own components."""
    import rdflib

    out = []
    k1 = rdflib.URIRef("https://www.commoncoreontologies.org/ont00000568")
    designates = rdflib.URIRef(BPO + "designatesProcessType")
    for key, components in register.items():
        node = rdflib.URIRef(key)
        if (node, rdflib.RDF.type, rdflib.SKOS.Concept) not in graph or                 k1 in set(graph.transitive_objects(node,
                                                   rdflib.RDFS.subClassOf)):
            out.append(("key", key))
        whole = {str(o) for o in graph.objects(node, designates)}
        for c in components:
            if k1 not in set(graph.transitive_objects(rdflib.URIRef(c),
                                                      rdflib.RDFS.subClassOf)):
                out.append(("component", c))
            if c in whole:
                out.append(("designated", c))
    return out


def test_cap22_the_test_register_passes_and_each_case_fails(graph, register):
    """CAP-22's fixture cases, over the test-only register: a key that is a
    K1 class, an unresolved component, and a function listing its designated
    whole-function class as a component."""
    assert register_findings(graph, register) == []
    payroll = BCO + "fixture_cq_node_payroll_function"
    bad = dict(register)
    bad[BCO + "PayrollProcessing"] = [BCO + "CashManagement"]
    assert ("key", BCO + "PayrollProcessing") in register_findings(graph, bad)
    bad = dict(register)
    bad[payroll] = register[payroll] + [BCO + "NoSuchCapability"]
    assert ("component", BCO + "NoSuchCapability") in register_findings(
        graph, bad)
    bad = dict(register)
    bad[payroll] = register[payroll] + [BCO + "FixtureCqWholePayrollFunction"]
    assert ("designated", BCO + "FixtureCqWholePayrollFunction") in         register_findings(graph, bad)


# ------------------------------------- CQ-11 (review-record method, B-4)


@pytest.fixture(scope="module")
def cq11():
    return load_tool("bco_review_records", "tools/ontology/review_records.py")


#: The expected answer: what the signed G1-T records exclude as governing or
#: developing each class rather than exercising it (Q5; T1 question 5).
CQ11_EXPECTED = {
    "bco:AccountsReceivableProcessing": {"P10799"},
    "bco:CapitalInvestmentAppraisal": {"P10844"},
    "bco:CollectionsManagement": {"P10804"},
    "bco:ControlEnvironmentAndRiskObjectiveFormulation": {"P10914"},
    "bco:CustomerDeductionManagement": {"P10809"},
    "bco:ExpenseReimbursementProcessing": {"P10880"},
    "bco:FinancialPerformanceAnalysis": {"P10785", "P10786"},
    "bco:FinancialPlanningBudgetingAndForecasting": {"P10771"},
    "bco:FixedAssetAccounting": {"P10828"},
    "bco:InternalControlEffectivenessMonitoring": {"P10919"},
    "bco:PayrollProcessing": {"P10853", "P14075"},
    "bco:TimeReporting": {"P10853"},
}


def test_cq11_review_record_answer(cq11):
    """A review-record answer, not an OWL or SPARQL answer (the CQ-11
    exception): read from the signed records at their signed commits."""
    result = cq11.answer()
    assert len(result) == 39
    assert {c: set(r["acts"]) for c, r in result.items() if r["acts"]} == \
        CQ11_EXPECTED


def test_cq11_development_evidence_is_never_a_realization_index_member(cq11):
    """Positive and negative together: every act the records name as
    developing or governing a class is outside that class's realization
    index, and no index member is named."""
    for cls, row in cq11.answer().items():
        assert not set(row["acts"]) & set(row["index"]), cls


def test_cq11_an_act_can_develop_one_capability_and_not_another(cq11):
    """P10853 (setting policies) is recorded as development for payroll
    processing and for time reporting, and is in no written class's index:
    the records say what it does for those two classes only."""
    result = cq11.answer()
    named = {c for c, r in result.items() if "P10853" in r["acts"]}
    assert named == {"bco:PayrollProcessing", "bco:TimeReporting"}
    assert not any("P10853" in r["index"] for r in result.values())


def test_cq11_absence_of_a_record_is_not_proof(cq11, capsys):
    """Accounts payable's record names no act under question 5 (it calls
    the summary act out without its identifier), so none is recorded; the
    answer says that is not a finding that none exists."""
    result = cq11.answer()
    assert result["bco:AccountsPayableProcessing"]["acts"] == {}
    assert cq11.main([]) == 0
    out = capsys.readouterr().out
    assert ("bco:AccountsPayableProcessing  no development or governance act "
            "recorded in the CAP-06 review records; not a finding that none "
            "exists") in out
    assert "not an OWL or SPARQL answer" in out


# ------------------------------------------------------------------- CQ-13


def test_cq13_claims_without_a_supporting_assessment(graph):
    """Cash management, whose only evaluation is incomplete, and the staged
    claim; payroll and payroll tax are supported."""
    assert answer(graph, CQ13, org=BCO + "fixture_cq_org") == {
        BCO + "fixture_cq_cash", BCO + "fixture_cq_staged"}


# ------------------------------------------------------------------- CQ-14


def test_cq14_sourcing_without_a_sourcing_assessment(graph):
    assert answer(graph, CQ14, org=BCO + "fixture_cq_org") == {
        BCO + "fixture_cq_sourcing_ap"}


def test_the_fixture_organizations_under_the_description_shapes(graph,
                                                                layout):
    """The description layer of the fixture organizations is well formed;
    the only reports are the CAP-26 gaps CQ-13 finds, the other
    organization's unassessed claim, and the staged claim's."""
    import rdflib
    from pyshacl import validate as shacl

    shapes = rdflib.Graph().parse(layout.path("validation.description"),
                                  format="turtle")
    _, results, _ = shacl(data_graph=graph, shacl_graph=shapes,
                          inference="none", advanced=True)
    SH = rdflib.Namespace("http://www.w3.org/ns/shacl#")
    found = {(str(results.value(r, SH.focusNode)),
              str(results.value(r, SH.resultMessage)).split(":")[0])
             for r in results.subjects(rdflib.RDF.type, SH.ValidationResult)}
    assert found == {(BCO + "fixture_cq_cash", "CAP-26"),
                     (BCO + "fixture_cq_staged", "CAP-26"),
                     (BCO + "fixture_cq_other_ap", "CAP-26")}, found
