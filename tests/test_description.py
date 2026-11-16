"""CP-1's checks on the description layer and the evidence register
(decision of 2026-11-15, B-1 and B-2): shapes/description_shapes.ttl against
its fixture of test-only individuals, and the description module against its
tranche record.

Each constraint fires on its own case; the positive controls survive under
every shape set; the module holds exactly the authorized terms. What SHACL
cannot decide is listed in GATE_F and is not counted as covered.
"""

from __future__ import annotations

import pytest

from conftest import load_tool

BCO = "https://fandaws.com/ontology/bco#"
CCO = "https://www.commoncoreontologies.org/"

#: Every description-shape message, with the fixture individual it must fire
#: on.
DESCRIPTION_CONSTRAINTS = {
    'CAP-17: a Capability Assessment or Capability Target concerns a '
    'type that is not a capability class (under cco:ont00000568).':
        BCO + "fixture_d_target_act_type",
    'CAP-17: a Capability Assessment, Capability Target, Capability '
    'Sourcing Statement or Authorization Record does not carry exactly '
    'one bco:concernsType.':
        BCO + "fixture_d_assess_two_types",
    'CAP-17: a Capability Map has an entry that is not a Capability '
    'Assessment or Capability Target; a Functional Adequacy Assessment '
    'is never an entry.':
        BCO + "fixture_d_map_faa_entry",
    'CAP-17: a Capability Map has no Capability Assessment or '
    'Capability Target entry (obo:BFO_0000178).':
        BCO + "fixture_d_map_empty",
    'CAP-17: a Capability Map, Capability Sourcing Assessment or '
    'Functional Adequacy Assessment carries bco:concernsType.':
        BCO + "fixture_d_map_typed",
    'CAP-17: a Capability Sourcing Statement or Authorization Record '
    'concerns a type that is not an act class (under cco:ont00000228).':
        BCO + "fixture_d_auth_cap_type",
    'CAP-20: a Capability Maturity Rating carries the ordinal '
    'measurement annotation (cco:ont00001739), which is reserved for '
    'the measured entity.':
        BCO + "fixture_d_rating_annotation",
    'CAP-20: a Capability Maturity Rating cites no Capability '
    'Assessment as its source (dct:source).':
        BCO + "fixture_d_rating_no_assessment",
    'CAP-20: a Capability Maturity Rating does not conform to exactly '
    'one scale (dct:conformsTo).':
        BCO + "fixture_d_rating_no_scale",
    'CAP-20: a Capability Maturity Rating does not have exactly one '
    'ordinal value (schema:ratingValue, the Stage 05 encoding).':
        BCO + "fixture_d_rating_no_value",
    'CAP-20: a Capability Maturity Rating is not an ordinal measurement '
    '(cco:ont00001811) of exactly one existing capability instance.':
        BCO + "fixture_d_rating_no_target",
    "CAP-20: a Capability Maturity Rating's value is given by a "
    'property whose domain is Information Bearing Entity '
    '(cco:ont00000253), which a rating is not.':
        BCO + "fixture_d_rating_ibe",
    'CAP-23: a Capability Sourcing Statement does not describe exactly '
    'one Organization (the consumer).':
        BCO + "fixture_d_sourcing_two_consumers",
    'CAP-23: a Capability Sourcing Statement is not about exactly one '
    'Organization other than the one it describes (the provider).':
        BCO + "fixture_d_sourcing_two_providers",
    'CAP-24: an Authorization Record cites no authority (dct:source).':
        BCO + "fixture_d_auth_no_authority",
    'CAP-24: an Authorization Record does not have exactly one '
    'schema:validFrom and one schema:validThrough, each typed xsd:date.':
        BCO + "fixture_d_auth_string_date",
    'CAP-24: an Authorization Record is not about exactly one agent.':
        BCO + "fixture_d_auth_two_agents",
    'CAP-26: a capability instance does not have exactly one '
    'Organization bearer, whichever direction the bearing is asserted '
    'in.':
        BCO + "fixture_d_cap_two_bearers",
    'CAP-26: a capability instance has no supporting Capability '
    'Assessment that describes its bearer, is about it, concerns its '
    'class and finds it present.':
        BCO + "fixture_d_cap_unsupported",
    'CAP-26: no supporting assessment of a capability instance cites '
    'evidence other than an Authorization Record or a past realization '
    'of the capability.':
        BCO + "fixture_d_cap_auth_only",
    'CAP-27: a Capability Assessment cites no evidence (dct:source).':
        BCO + "fixture_d_assess_no_source",
    'CAP-27: a Capability Assessment does not have exactly one '
    'bco:assessedPresence, valued present, absent or partial.':
        BCO + "fixture_d_assess_no_finding",
    'CAP-27: a Capability Assessment does not have exactly one dct:date '
    'typed xsd:date.':
        BCO + "fixture_d_assess_no_date",
    'CAP-27: a Capability Assessment names no criteria '
    '(dct:conformsTo).':
        BCO + "fixture_d_assess_no_criteria",
    "CAP-27: a Capability Assessment's criteria carry no dct:identifier "
    'that can be reported.':
        BCO + "fixture_d_assess_criteria_no_id",
    'CAP-28: an Action Permission (cco:ont00000751) permits no asserted '
    'act instance; a prospective authorization is an Authorization '
    'Record.':
        BCO + "fixture_d_prospective_license",
    'CAP-28: an Authorization Record is typed Action Permission '
    '(cco:ont00000751).':
        BCO + "fixture_d_auth_as_permission",
    'CAP-31: a Capability Target-State Specification has no named '
    'Capability Target as a continuant part (obo:BFO_0000178).':
        BCO + "fixture_d_tss_empty",
    'CAP-33: a Capability Assessment states an integration, '
    'availability or adequacy finding.':
        BCO + "fixture_d_assess_integration",
    'CAP-33: a Functional Adequacy Assessment carries '
    'bco:assessedPresence; it states no presence finding (CD17).':
        BCO + "fixture_d_faa_presence",
    'CAP-33: a Functional Adequacy Assessment does not describe exactly '
    'one Organization.':
        BCO + "fixture_d_faa_no_org",
    'CAP-33: a Functional Adequacy Assessment does not state exactly '
    'three findings, one each for integration and coordination, '
    'operational availability, and adequacy for the function.':
        BCO + "fixture_d_faa_two_findings",
    'CAP-33: a Functional Adequacy Assessment is not about exactly one '
    'Standing Function (its APQC catalog concept, a skos:Concept).':
        BCO + "fixture_d_faa_no_function",
    'CAP-33: an adequacy finding cites no evidence that establishes it '
    '(dct:source).':
        BCO + "fixture_d_finding_no_source",
    'CAP-33: an adequacy finding does not have exactly one dct:date '
    'typed xsd:date.':
        BCO + "fixture_d_finding_no_criteria",
    'CAP-33: an adequacy finding is not exactly one of met, partly met '
    'or not met (schema:ratingValue).':
        BCO + "fixture_d_finding_bad_value",
    'CAP-33: an adequacy finding names no criteria (dct:conformsTo).':
        BCO + "fixture_d_finding_no_criteria",
    'CAP-33: an individual is both a Functional Adequacy Assessment and '
    'a Capability Assessment; it is a sibling of Capability Assessment, '
    'never a kind of it (CD17).':
        BCO + "fixture_d_faa_as_assessment",
    'CD14: an absent Capability Assessment is about a capability '
    'instance; an absent finding links none.':
        BCO + "fixture_d_assess_absent_linked",
    'CD17: a Capability Sourcing Assessment is not about exactly one '
    'Capability Sourcing Statement.':
        BCO + "fixture_d_sa_no_statement",
    'CD17: a Capability Sourcing Assessment states no criteria '
    '(dct:conformsTo) or cites no evidence (dct:source).':
        BCO + "fixture_d_sa_no_criteria",
    'CD17: a present-finding Capability Assessment cites a Functional '
    'Adequacy Assessment as its evidence; adequacy is never evidence '
    'that a capability is possessed.':
        BCO + "fixture_d_assess_cites_faa",
}

#: Further cases the specification names, each firing the message it starts
#: with.
SECOND_CASES = {
    BCO + "fixture_d_cap_past_only": "CAP-26: no supporting",
    BCO + "fixture_d_cap_inverse_unsupported": "CAP-26: a capability instance has no",
    BCO + "fixture_d_assess_two_findings":
        "CAP-27: a Capability Assessment does not have exactly one bco",
    BCO + "fixture_d_assess_two_dates":
        "CAP-27: a Capability Assessment does not have exactly one dct",
}

#: Built to conform under every shape set, including the instance fixture's
#: positive capabilities, which this fixture supplies with assessments.
POSITIVE_CONTROLS = [
    BCO + "fixture_good_cap", BCO + "fixture_inverse_cap",
    BCO + "fixture_staged_no_basis",
    BCO + "fixture_d_assess_good_cap", BCO + "fixture_d_assess_inverse_cap",
    BCO + "fixture_d_assess_staged", BCO + "fixture_d_assess_absent",
    BCO + "fixture_d_target_good", BCO + "fixture_d_map_good",
    BCO + "fixture_d_tss_good", BCO + "fixture_d_rating_good",
    BCO + "fixture_d_sourcing_good", BCO + "fixture_d_sa_good",
    BCO + "fixture_d_auth_good", BCO + "fixture_d_permission_good",
    BCO + "fixture_d_faa_good", BCO + "fixture_d_faa_good_f1",
    BCO + "fixture_d_faa_good_f2", BCO + "fixture_d_faa_good_f3",
]

#: The parts of CAP-26, CAP-27 and CAP-33 that need a person's judgment
#: (Gate F): whether cited evidence establishes a negative finding, whether
#: evidence is sufficient against the stated threshold, and whether a source
#: is an organization chart, charter or responsibility assignment. No shape
#: claims them.
GATE_F = (
    "an absent finding whose only source records that no evidence of "
    "presence was found (CAP-27, F)",
    "a present finding whose only evidence is an organization chart "
    "(CAP-27, F; CAP-26)",
    "a not met finding whose only source records that the dimension could "
    "not be assessed (CAP-33, F)",
)


@pytest.fixture(scope="module")
def validation():
    return load_tool("bco_validate_description",
                     "tools/ontology/validate.py").measure()


def test_every_description_constraint_has_a_message_and_is_listed(layout):
    from test_ontology_checks import shape_messages

    messages, silent = shape_messages(layout.path("validation.description"))
    assert not silent
    assert len(messages) == len(set(messages))
    assert set(messages) == set(DESCRIPTION_CONSTRAINTS), (
        sorted(set(messages) ^ set(DESCRIPTION_CONSTRAINTS)))


def test_every_description_constraint_fires_on_its_own_case(validation):
    rung = validation["rungs"]["validation.description"]
    fired = {(v["focus"], v["message"]) for v in rung["fixture"]["detail"]}
    missing = sorted(m for m, focus in DESCRIPTION_CONSTRAINTS.items()
                     if (focus, m) not in fired)
    assert not missing, missing
    for focus, prefix in SECOND_CASES.items():
        assert any(f == focus and m.startswith(prefix) for f, m in fired), (
            focus, prefix)


def test_the_positive_controls_survive_every_shape_set(validation):
    flagged = {v["focus"] for rung in validation["rungs"].values()
               for v in rung["fixture"]["detail"]}
    assert not flagged & set(POSITIVE_CONTROLS), (
        sorted(flagged & set(POSITIVE_CONTROLS)))


def test_the_real_corpus_has_no_individual_and_conforms(validation):
    """The modules hold classes only, so the corpus half of this rung is
    vacuous; the fixture half is the evidence."""
    assert validation["rungs"]["validation.description"]["corpus"][
        "conforms"]


# --------------------------------------------------- the description module


@pytest.fixture(scope="module")
def formalize():
    return load_tool("bco_formalize_description",
                     "tools/ontology/formalize.py")


@pytest.fixture(scope="module")
def desc(repo):
    import rdflib

    return rdflib.Graph().parse(repo / "src/05_ontology/apqc-cap-desc.ttl",
                                format="turtle")


def test_the_description_tranche_verifies_and_the_module_is_fresh(formalize):
    findings, rows = formalize.verify_description(formalize.load_description())
    assert not findings, findings
    assert formalize.desc_module_path().read_bytes() == \
        formalize.render_description(rows)


def test_the_module_holds_exactly_the_authorized_terms(desc):
    """B-1: seven description-layer classes, the Authorization Record, the
    Functional Adequacy Assessment, and two annotation properties. No object
    property, restriction, equivalence, disjointness or individual."""
    import rdflib

    R, O = rdflib.RDF, rdflib.OWL
    classes = {str(s) for s in desc.subjects(R.type, O.Class)}
    assert classes == {BCO + n for n in (
        "CapabilityMap", "CapabilityAssessment", "CapabilityMaturityRating",
        "CapabilitySourcingStatement", "CapabilitySourcingAssessment",
        "CapabilityTarget", "CapabilityTargetStateSpecification",
        "AuthorizationRecord", "FunctionalAdequacyAssessment")}
    assert {str(s) for s in desc.subjects(R.type, O.AnnotationProperty)} == {
        BCO + "concernsType", BCO + "assessedPresence"}
    for kind in (O.ObjectProperty, O.DatatypeProperty, O.Restriction,
                 O.NamedIndividual):
        assert not set(desc.subjects(R.type, kind)), kind
    for p in (O.equivalentClass, O.disjointWith, O.unionOf):
        assert not set(desc.subject_objects(p)), p


def test_the_parents_are_the_specifications_and_no_class_is_a_capability(
        desc):
    import rdflib

    parents = {str(s).split("#")[1]: {str(o) for o in desc.objects(
        s, rdflib.RDFS.subClassOf)} for s in desc.subjects(
            rdflib.RDF.type, rdflib.OWL.Class)}
    assert parents == {
        "CapabilityMap": {CCO + "ont00000853"},
        "CapabilityAssessment": {CCO + "ont00000853"},
        "CapabilityMaturityRating": {CCO + "ont00001010"},
        "CapabilitySourcingStatement": {CCO + "ont00000853"},
        "CapabilitySourcingAssessment": {CCO + "ont00000853"},
        "CapabilityTarget": {CCO + "ont00000476"},
        "CapabilityTargetStateSpecification": {CCO + "ont00000974"},
        "AuthorizationRecord": {CCO + "ont00000853"},
        "FunctionalAdequacyAssessment": {CCO + "ont00000853"},
    }


def test_the_adequacy_assessment_is_never_a_capability_assessment(desc):
    """B-1: not a subclass of bco:CapabilityAssessment, directly or not."""
    import rdflib

    faa = rdflib.URIRef(BCO + "FunctionalAdequacyAssessment")
    assert rdflib.URIRef(BCO + "CapabilityAssessment") not in set(
        desc.transitive_objects(faa, rdflib.RDFS.subClassOf))


def test_a_drifted_record_is_a_finding(formalize):
    """S05-T1 for the description tranche: a drifted concept digest, a
    capability parent, a changed use, an unauthorized class with no concept,
    and a parent the decision did not choose are each caught."""
    import copy

    record = formalize.load_description()
    vocab = formalize.vocabulary()
    edits = [
        lambda r: r["classes"][0].update(concept_record_sha256="0" * 64),
        lambda r: r["classes"][1].update(parent="cco:ont00000568"),
        lambda r: r["annotation_properties"][0].update(use="Something else"),
        lambda r: r["classes"].append({"class": "bco:CapabilityPortfolio",
                                       "parent": "cco:ont00000853"}),
        lambda r: r["classes"][-1].update(parent="cco:ont00000958"),
    ]
    for n, edit in enumerate(edits):
        case = copy.deepcopy(record)
        edit(case)
        findings, _ = formalize.verify_description(case, vocab=vocab)
        assert findings, n


def test_no_gate_f_judgment_is_claimed_by_a_shape(layout):
    """The judgments in GATE_F are review work. No shape message claims to
    decide sufficiency or what a source establishes."""
    from test_ontology_checks import shape_messages

    messages, _ = shape_messages(layout.path("validation.description"))
    for m in messages:
        assert "sufficien" not in m and "organization chart" not in m, m
    assert len(GATE_F) == 3
