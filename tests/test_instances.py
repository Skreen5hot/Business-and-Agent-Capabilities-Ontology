"""CP-1's instance-level checks (docs/decisions/2026-11-15-d6-class-
increment-accepted.md, C): shapes/instance_shapes.ttl against its fixture of
test-only individuals.

Each constraint fires on its own case; the positive controls survive; the
encoding choices are the ones the shape file records. The CP-1 rules that
need description-layer terms, which are not minted, are listed in
BLOCKED and asserted absent from the shapes, so that none is counted as
covered by accident.
"""

from __future__ import annotations

import pytest

from conftest import load_tool

BCO = "https://fandaws.com/ontology/bco#"

#: Every instance-shape message, with the fixture individual it must fire on.
INSTANCE_CONSTRAINTS = {
    "CAP-08: the bearer of a Business Capability instance, in either "
    "direction of has capability, is not an Organization.":
        BCO + "fixture_cap_person_bearer",
    "CAP-12: aggregate has capability (cco:ont00001898) has a Business "
    "Capability instance as its object.": BCO + "fixture_cap_aggregate",
    "CAP-35: a Business Capability instance has no material basis "
    "(obo:BFO_0000218); every instance needs at least one member agent of "
    "its bearer as its grounding witness.": BCO + "fixture_cap_no_basis",
    "CAP-25: a material-basis object is not a member part of the "
    "capability's bearer (obo:BFO_0000115 / obo:BFO_0000129).":
        BCO + "fixture_cap_outsider_basis",
    "CAP-25: a material-basis object is an artifact (cco:ont00000995); an "
    "artifact is an enabling condition, never the basis.":
        BCO + "fixture_cap_artifact_basis",
    "CAP-25: a material-basis object is not a named agent (under Agent, "
    "Person or Group of Agents).": BCO + "fixture_cap_artifact_basis",
    "CAP-21: an act realizing a Business Capability instance is not "
    "asserted under any member of the capability class's index (Gate C-A, "
    "asserted graph).": BCO + "fixture_cap_misfiled",
    "CAP-34: no member agent of the bearer performs an act realizing this "
    "capability (has agent, cco:ont00001833); taking part, or naming only "
    "the organization, does not count.": BCO + "fixture_cap_vendor_run",
    "CAP-25: has material basis is asserted on an instance of a class that "
    "has not passed G1-T (a staged Organization Capability class).":
        BCO + "fixture_staged_with_basis",
    "CAP-11: an information content entity has a capability, realizes "
    "something or has a realization.": BCO + "fixture_bad_map",
    "CAP-19: an information content entity is the bearer of a realizable "
    "entity.": BCO + "fixture_software_ice",
}

#: A second case for CAP-34: only the organization is named as performer.
SECOND_CASES = {
    BCO + "fixture_cap_org_performer": "CAP-34:",
}

#: Built to conform.
POSITIVE_CONTROLS = [
    BCO + "fixture_good_cap", BCO + "fixture_inverse_cap",
    BCO + "fixture_staged_no_basis", BCO + "fixture_good_map",
    BCO + "fixture_good_act", BCO + "fixture_joint_act",
]

#: CP-1 rules that cannot be encoded without an unminted term (the
#: description layer: Capability Assessment, Map, Target, Maturity Rating,
#: Sourcing Statement and Assessment, Target-State Specification,
#: Authorization Record, Functional Adequacy Assessment; the annotations
#: bco:concernsType and bco:assessedPresence), or without a completeness
#: manifest schema (Gate M). Reported, never counted.
BLOCKED = ("CAP-17", "CAP-18", "CAP-20", "CAP-23", "CAP-24", "CAP-26",
           "CAP-27", "CAP-28", "CAP-31", "CAP-33")


@pytest.fixture(scope="module")
def validation():
    return load_tool("bco_validate_instances",
                     "tools/ontology/validate.py").measure()


def test_every_instance_constraint_has_a_message_and_is_listed(layout):
    from test_ontology_checks import shape_messages

    messages, silent = shape_messages(layout.path("validation.instances"))
    assert not silent
    assert len(messages) == len(set(messages))
    assert set(messages) == set(INSTANCE_CONSTRAINTS), (
        sorted(set(messages) ^ set(INSTANCE_CONSTRAINTS)))


def test_every_instance_constraint_fires_on_its_own_case(validation):
    rung = validation["rungs"]["validation.instances"]
    fired = {(v["focus"], v["message"]) for v in rung["fixture"]["detail"]}
    missing = sorted(m for m, focus in INSTANCE_CONSTRAINTS.items()
                     if (focus, m) not in fired)
    assert not missing, missing
    for focus, prefix in SECOND_CASES.items():
        assert any(f == focus and m.startswith(prefix) for f, m in fired), (
            focus, prefix)


def test_the_instance_fixture_does_not_flag_what_is_legitimate(validation):
    """A capability with one member as basis, bearing written as capability
    of, an act performed jointly by a member and vendor staff, a staged
    instance with no basis (not a Business Capability instance, a2), and a
    description with a creator."""
    flagged = {v["focus"] for rung in validation["rungs"].values()
               for v in rung["fixture"]["detail"]}
    assert not flagged & set(POSITIVE_CONTROLS), (
        flagged & set(POSITIVE_CONTROLS))


def test_the_real_corpus_has_no_instance_and_conforms(validation, layout):
    """The ontology holds no individual (the module is class-only), so the
    corpus half of this rung is vacuous by construction; the fixture half
    is the evidence. Stated so it is not mistaken for coverage."""
    import rdflib

    graph = rdflib.Graph()
    for path in layout.ontology_files():
        graph.parse(path, format="turtle")
    assert not set(graph.subjects(rdflib.RDF.type, rdflib.OWL.NamedIndividual))
    assert validation["rungs"]["validation.instances"]["corpus"]["conforms"]


def test_the_vendor_case_is_participation_not_performance(repo):
    """CAP-34's encoding: has agent (cco:ont00001833) is a sub-property of
    has participant (obo:BFO_0000057) at the CCO pin, so performing is a
    kind of taking part, and taking part alone is not performing."""
    import rdflib

    cco = rdflib.Graph().parse(repo / "vendor/cco/cco-bco-extract.ttl",
                               format="turtle")
    has_agent = rdflib.URIRef("https://www.commoncoreontologies.org/ont00001833")
    assert (has_agent, rdflib.RDFS.subPropertyOf,
            rdflib.URIRef("http://purl.obolibrary.org/obo/BFO_0000057")) in cco


def test_no_blocked_rule_is_claimed_by_a_shape(layout):
    """The rules that need unminted terms are not in any shape file, so a
    green ladder cannot be read as covering them."""
    from test_ontology_checks import shape_messages

    for entry in layout.components("ontology-validation"):
        messages, _ = shape_messages(entry.resolve())
        claimed = [m for m in messages if m.startswith(BLOCKED)]
        assert not claimed, (entry.id, claimed)
