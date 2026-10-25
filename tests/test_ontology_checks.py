# SPDX-License-Identifier: Apache-2.0
"""The corpus measures, and the honesty of the validation ladder.

Carried from the Application Requirement Ontology. There, these tests
were written against 62,000 triples of APQC corpus and two shape sets
that had been reporting a missing vocabulary as 213 defects. Here they
start against two empty module headers and one shape set, which makes
the falsification half of every rung the only evidence that anything is
being checked at all: a corpus with no classes conforms to every shape
whether the shapes work or not.

So the assertions that matter today are the ones about the fixture, and
the corpus-size guards are set to what is actually authored -- two
modules, headers only -- rather than inherited from a corpus this
repository does not have. Raise them as the modules fill.
"""

from __future__ import annotations

import pytest

from conftest import load_tool


@pytest.fixture(scope="module")
def digest_tool():
    return load_tool("bco_digest", "tools/ontology/corpus_digest.py")


@pytest.fixture(scope="module")
def digest(digest_tool):
    return digest_tool.measure()


@pytest.fixture(scope="module")
def validator():
    return load_tool("bco_validate", "tools/ontology/validate.py")


@pytest.fixture(scope="module")
def validation(validator):
    """Measured once.

    Each call runs every shape set against the whole corpus and against
    the fixture. Cheap today; in ARO, three tests asking for it
    separately over 62,000 triples outran a ten-minute timeout, and this
    corpus is meant to grow.
    """
    return validator.measure()


# ------------------------------------------------------------- digests


def test_the_two_measures_cover_every_triple(digest):
    """Ground triples and blank-node-touching triples partition the
    graph. If they did not, a change could land in the gap between them
    and move neither number."""
    merged = digest["merged"]
    assert (merged["ground_triples"] + merged["blank_nodes"]["triples_touching"]
            == merged["triples"]), merged


def test_the_corpus_is_not_empty(digest):
    """Guards every digest below: a digest of nothing is stable, and
    means nothing. Two module headers, four triples each, is what is
    authored today."""
    assert digest["merged"]["triples"] >= 8, digest["merged"]["triples"]
    assert digest["scope"]["files"] >= 2, digest["scope"]


def test_the_scope_is_the_authored_ontology(digest):
    """Not a directory walk. A walk would include the reasoner's own
    output and the fixture built to be invalid."""
    paths = digest["scope"]["paths"]
    assert not [p for p in paths if p.startswith("drafts/")], paths
    assert not [p for p in paths if "bad_examples" in p], paths
    assert not [p for p in paths if "shapes" in p], paths


def test_the_ground_digest_moves_when_a_named_term_changes(digest_tool):
    """Falsifies the measure: a digest that ignored content would be
    perfectly stable and perfectly useless."""
    import rdflib

    graph = rdflib.Graph()
    graph.parse(data='<https://ex.invalid/a> <https://ex.invalid/p> "one" .',
                format="turtle")
    before = digest_tool.digest_of(digest_tool.ground(graph))
    graph.add((rdflib.URIRef("https://ex.invalid/a"),
               rdflib.URIRef("https://ex.invalid/p"),
               rdflib.Literal("two")))
    assert digest_tool.digest_of(digest_tool.ground(graph)) != before


def test_the_blank_node_shape_survives_reparsing(digest_tool):
    """The reason blank nodes get a shape rather than a digest.

    rdflib renames them on every parse, so a naive comparison reports
    every restriction as both added and removed -- which is exactly what
    the first namespace check in this repository did.
    """
    import rdflib

    turtle = ("@prefix ex: <https://ex.invalid/> ." + chr(10)
              + "@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> ."
              + chr(10)
              + "ex:A rdfs:subClassOf [ a ex:R ; ex:on ex:p ] ." + chr(10)
              + "ex:B rdfs:subClassOf [ a ex:R ; ex:on ex:q ] ." + chr(10))
    first, second = rdflib.Graph(), rdflib.Graph()
    first.parse(data=turtle, format="turtle")
    second.parse(data=turtle, format="turtle")

    raw_first = {(str(s), str(p), str(o)) for s, p, o in first}
    raw_second = {(str(s), str(p), str(o)) for s, p, o in second}
    assert raw_first != raw_second, (
        "blank node names were stable across parses, so the problem this "
        "measure exists for did not occur and it is not being tested")

    assert (digest_tool.bnode_shape(first)["shape_sha256"]
            == digest_tool.bnode_shape(second)["shape_sha256"])


# ------------------------------------------------------- the ladder


def test_the_upstream_vocabulary_the_shapes_walk_is_in_scope(validation):
    """The inverse of what this test used to assert.

    Shapes requiring a class to reach a CCO anchor via subClassOf+ have
    no chain to walk when CCO is absent. They report every subject as
    violating, and that report is indistinguishable from a real defect
    unless the tool separates the two. It did separate them, and then the
    vocabulary was vendored, so now every referenced term resolves.
    """
    record = validation
    assert record["unresolved"] == [], (
        "%s is referenced and not described, so any rung that walks "
        "through it is reporting the scope again" % record["unresolved"])
    for name, info in record["upstream_vocabularies"].items():
        assert info["resolvable"], (name, info)

    for name, rung in record["rungs"].items():
        assert rung["evaluable"], (
            "%s is blocked on %s" % (name,
                                     rung["blocked_by_missing_vocabulary"]))


def test_a_resolvable_vocabulary_is_not_a_complete_one(validation):
    """What "resolvable" does and does not mean.

    Every referenced term is described. That is true of a partial extract
    by construction -- the extract was built from the references -- and
    it is not the same claim as "BFO and CCO are present". The report has
    to carry the difference, or a reader takes the first for the second.
    """
    vendoring = validation["vendoring"]
    assert vendoring["available"], vendoring
    assert vendoring["partial_extracts"] is True
    assert vendoring["not_covered"]
    assert sum(entry["axioms_dropped"]
               for entry in vendoring["sources"].values()) > 0


def test_the_violations_are_attributed_to_whose_terms_they_are(validation):
    """Loading somebody else ontology into the data graph creates the
    mirror of the problem it solved: a defect in the extract reported as
    a defect here."""
    for name, rung in validation["rungs"].items():
        corpus = rung["corpus"]
        assert (corpus["against_authored_terms"]
                + corpus["against_vendored_terms"]
                == corpus["violations"]), (name, corpus)
        assert corpus["against_vendored_terms"] == 0, (
            "%d violation(s) are against vendored upstream terms, which "
            "are findings about the extract" % corpus["against_vendored_terms"])


def test_the_baseline_describes_reality(validation, validator):
    """The gate, run as a test.

    The count of open findings used to be written into this file as
    `== 10`. It now lives in config/validation-baseline.json, so the team
    inheriting this can see what is owed without reading test code, and
    so there is one source of truth rather than a number here and another
    in a report.
    """
    problems = validator.compare(validation, validator.baseline())
    assert problems == [], problems


def test_every_rung_is_recorded(validation, validator):
    """Both directions. A rung with no baseline entry would be adopted
    silently; an entry for a rung that no longer exists is coverage for
    nothing."""
    recorded = set((validator.baseline().get("rungs") or {}))
    assert recorded == set(validation["rungs"]), (
        "recorded but gone: %s; present but unrecorded: %s"
        % (sorted(recorded - set(validation["rungs"])),
           sorted(set(validation["rungs"]) - recorded)))



# ------------------------------------------------------- the gate


def rung(findings=0, evaluable=True, exercised=True, vendored=0):
    return {"evaluable": evaluable, "can_still_fail": exercised,
            "blocked_by_missing_vocabulary": [] if evaluable else ["CCO"],
            "corpus": {"against_authored_terms": findings,
                       "against_vendored_terms": vendored}}


def test_the_gate_accepts_only_a_baseline_that_matches(validator):
    """Falsifies the gate, one disagreement at a time.

    Run against constructed records rather than the live ladder, because
    several of these states -- a rung that has vanished, a vocabulary
    that has gone missing, a finding at all -- cannot be reached from
    this repository today. A branch that cannot be reached is a branch
    nobody has executed.
    """
    baseline = {"rungs": {"a": {"authored_findings": 10}}}

    assert validator.compare({"rungs": {"a": rung(10)}}, baseline) == []

    got = validator.compare({"rungs": {"a": rung(11)}}, baseline)
    assert got and "1 new finding." in got[0], got

    got = validator.compare({"rungs": {"a": rung(13)}}, baseline)
    assert got and "3 new findings." in got[0], got

    got = validator.compare({"rungs": {"a": rung(9)}}, baseline)
    assert got and "re-record" in got[0], got

    got = validator.compare({"rungs": {"a": rung(10), "b": rung(0)}}, baseline)
    assert got and "no entry" in got[0], got

    got = validator.compare({"rungs": {}}, baseline)
    assert got and "no longer exists" in got[0], got

    got = validator.compare({"rungs": {"a": rung(10, evaluable=False)}},
                            baseline)
    assert got and "cannot be evaluated" in got[0], got

    got = validator.compare({"rungs": {"a": rung(10, exercised=False)}},
                            baseline)
    assert got and "did not fire on the fixture" in got[0], got

    got = validator.compare({"rungs": {"a": rung(10, vendored=3)}}, baseline)
    assert got and "vendored upstream terms" in got[0], got


def test_recording_refuses_to_raise_a_count_without_a_reason(validator,
                                                             tmp_path,
                                                             monkeypatch):
    """Without this, a regression certifies itself on the one run that
    introduces it and the baseline becomes a transcript of whatever
    happened rather than a commitment."""
    import json

    monkeypatch.setattr(validator.layout, "repository_root",
                        lambda: tmp_path)
    (tmp_path / "config").mkdir()
    (tmp_path / "config" / "validation-baseline.json").write_text(
        json.dumps({"rungs": {"a": {"authored_findings": 10}}}),
        encoding="utf-8")

    raised = {"rungs": {"a": rung(11)}}
    assert validator.record_baseline(raised, None) == 1, (
        "recording accepted a raised count with no reason given")

    assert validator.record_baseline(raised, "deliberate, see ADR-9") == 0
    after = json.loads(
        (tmp_path / "config" / "validation-baseline.json").read_text(
            encoding="utf-8"))
    assert after["rungs"]["a"]["authored_findings"] == 11
    assert after["rungs"]["a"]["why"] == "deliberate, see ADR-9", (
        "the reason was not recorded beside the number it excuses")

    # Lowering never needs a reason.
    assert validator.record_baseline({"rungs": {"a": rung(4)}}, None) == 0


# --------------------------------------------- the wellformedness set


WELLFORMEDNESS_CONSTRAINTS = [
    "Class has no rdfs:label.",
    "Class has no skos:definition.",
    "Concept has no skos:prefLabel.",
]


def test_every_wellformedness_constraint_is_exercised(validation):
    """Named, not counted.

    None of these finds anything in the corpus today, because nothing is
    authored. A constraint that finds nothing and is never exercised is
    indistinguishable from one that selects nothing, and these exist for
    modules that are not written yet, so the fixture is the only evidence
    they work at all.
    """
    rung = validation["rungs"]["validation.wellformedness"]
    fired = sorted({v["message"] for v in rung["fixture"]["detail"]})
    missing = [m for m in WELLFORMEDNESS_CONSTRAINTS if m not in fired]
    assert not missing, (
        "%d presence constraint(s) did not fire against the fixture: %s"
        % (len(missing), missing))

    drift = [m for m in fired if "in the same language" in m]
    assert drift, (
        "no drift constraint fired against the fixture, so a zero against "
        "the corpus rests on nothing")


def test_the_wellformedness_fixture_does_not_flag_what_is_legitimate(
        validation):
    """The false positives sh:maxCount 1 would have produced.

    A multilingual label pair is correct and must not be reported, and a
    catalog concept carrying no rdfs:label is correct because a concept
    is labelled with skos:prefLabel. The second of those was the first
    draft of this shape set, and it reported 3,842 findings that were the
    catalog being told to look like a class.
    """
    rung = validation["rungs"]["validation.wellformedness"]
    flagged = {v["focus"] for v in rung["fixture"]["detail"]}
    for good in ("FixtureMultilingual", "FixtureWellFormed",
                 "FixtureRepeatedValue", "FixtureConceptWellFormed",
                 "FixtureNotInThePopulation",
                 "FixtureConceptOutsideThePopulation"):
        assert not [f for f in flagged if f and f.endswith("#" + good)], (
            "%s was built to conform and did not" % good)
    # FixtureConceptWellFormed exists in both concept namespaces; guard
    # that the loop above was looking at both.
    assert {"https://fandaws.com/ontology/bco-metamodel#",
            "https://fandaws.com/ontology/bco-catalog#"} <= {
        f.rsplit("#", 1)[0] + "#" for f in flagged if f}


def test_the_fixtures_come_from_the_contract(validator, layout):
    """In ARO, `measure` named one fixture component, and a second shape
    set then had nowhere to put its cases. The CAP shapes will each bring
    a fixture; this is what makes adding one a declaration rather than
    an edit to the tool."""
    declared = {c.path for c in layout.components("test-fixture")}
    found = {p.relative_to(layout.repository_root()).as_posix()
             for p in validator.fixtures()}
    assert found == declared, (declared, found)
    assert found, "no fixture is loaded, so no shape set can be falsified"


def test_a_ladder_that_evaluated_nothing_does_not_pass(validator):
    """`all()` over an empty sequence is True, so the first version of
    this tool reported success having evaluated no rung at all.

    That state cannot be reached from this repository any more, which is
    exactly why the guard is tested against a constructed record rather
    than against the live one -- otherwise it would be a branch nobody
    executes, sitting in a tool whose whole subject is checks that do not
    fire.
    """
    assert validator.passed_of({}) is False

    blocked = {"one": {"evaluable": False,
                       "corpus": {"conforms": True}, "can_still_fail": True}}
    assert validator.passed_of(blocked) is False

    evaluated = {"one": {"evaluable": True,
                         "corpus": {"conforms": True},
                         "can_still_fail": True}}
    assert validator.passed_of(evaluated) is True


def test_the_shapes_are_still_wired_to_a_fixture(validation):
    """The bad-examples fixture must break at least one shape set.

    A fixture that breaks nothing is not a falsification, and a shape set
    with no fixture behind it has a green result that cannot be
    distinguished from a constraint selecting nothing.
    """
    record = validation
    exercised = [name for name, rung in record["rungs"].items()
                 if rung["fixture_exercises_these_shapes"]]
    assert exercised, (
        "the bad-examples fixture produced no violations against any shape "
        "set, so nothing is falsifying the shapes")

    unexercised = sorted(set(record["rungs"]) - set(exercised))
    assert unexercised == [], (
        "%s has no negative fixture behind it, so its result cannot be "
        "distinguished from a constraint that selects nothing" % unexercised)




# ------------------------------------------------- the vocabulary set


BCOM = "https://fandaws.com/ontology/bco-metamodel#"
BCOC = "https://fandaws.com/ontology/bco-catalog#"
BCOS = "https://fandaws.com/ontology/bco-sources#"
BCOA = "https://fandaws.com/ontology/bco-agents#"

#: Every constraint in shapes/vocabulary_shapes.ttl, by its message, with
#: the case in shapes/vocabulary_bad_examples.ttl named for it. Named, not
#: counted: any 75 violations would satisfy a count.
VOCABULARY_CONSTRAINTS = {
    # concepts
    "Concept is in no skos:inScheme.": BCOC + "VocabNoScheme",
    "Concept is in more than one skos:inScheme.": BCOC + "VocabTwoSchemes",
    "Concept has a skos:prefLabel with no language tag.":
        BCOC + "VocabUntaggedLabel",
    "Concept has two skos:prefLabel values in one language.":
        BCOC + "VocabTwoEnglishLabels",
    "Concept has no skos:definition.": BCOC + "VocabNoDefinition",
    "Concept stores skos:narrower; the hierarchy is stated with "
    "skos:broader only.": BCOC + "VocabStoresNarrower",
    "Concept has no bco:lifecycleStatus.": BCOC + "VocabNoStatus",
    "Concept has more than one bco:lifecycleStatus.":
        BCOC + "VocabTwoStatuses",
    "Concept has a bco:lifecycleStatus outside Draft, Candidate, Ratified "
    "and Deprecated.": BCOC + "VocabUnknownStatus",
    "Concept is owl:deprecated true with no dcterms:isReplacedBy.":
        BCOC + "VocabDeprecatedUnreplaced",
    "Concept has dcterms:isReplacedBy and is not owl:deprecated true.":
        BCOC + "VocabReplacedNotDeprecated",
    "Concept is replaced by something that is not a skos:Concept in scope.":
        BCOC + "VocabReplacedByNothing",
    "Concept's bco:lifecycleStatus and owl:deprecated disagree.":
        BCOC + "VocabStatusDisagrees",
    "Concept is Ratified with no bco:ratifiedBy.":
        BCOC + "VocabRatifiedUncited",
    "Concept has no prov:wasAttributedTo.": BCOC + "VocabUnattributed",
    "Concept is attributed to an agent not declared in bco-agents.":
        BCOC + "VocabUndeclaredAgent",
    # metamodel and catalog
    "Metamodel concept is not in bcom:MetamodelScheme.":
        BCOM + "VocabWrongScheme",
    "Metamodel concept has no bco:designatesClass.":
        BCOM + "VocabNoDesignatedClass",
    "Metamodel concept designates a class outside the bco: namespace.":
        BCOM + "VocabDesignatesElsewhere",
    "Catalog concept is not in bcoc:CapabilityCatalogScheme.":
        BCOC + "VocabCatalogWrongScheme",
    "Catalog skos:notation is not typed bco:PCFCode.":
        BCOC + "VocabUntypedNotation",
    # catalog genus and foundational ancestor (review R7, Finding E)
    "Catalog concept has no bco:definitionGenus.": BCOC + "VocabNoGenus",
    "Catalog concept has more than one bco:definitionGenus.":
        BCOC + "VocabTwoGenera",
    "Catalog concept's bco:definitionGenus is neither a BFO or CCO class "
    "nor the class a metamodel concept designates.":
        BCOC + "VocabGenusUndesignated",
    "Catalog concept has no bco:foundationalAncestor.":
        BCOC + "VocabNoAncestor",
    "Catalog concept has more than one bco:foundationalAncestor.":
        BCOC + "VocabTwoAncestors",
    "Catalog concept's bco:foundationalAncestor is not a BFO or CCO class.":
        BCOC + "VocabAncestorNotUpstream",
    # source references
    "Source reference cites no source.": BCOC + "source-no-source",
    "Source reference cites something that is not a bco-sources record.":
        BCOC + "source-not-a-record",
    "Source reference has no bco:locator.": BCOC + "source-no-locator",
    "Source reference has no bco:relation.": BCOC + "source-no-relation",
    "Source reference has a bco:relation other than adapted-from, "
    "consistent-with or departs-from.": BCOC + "source-bad-relation",
    "A departs-from source reference has no bco:departureNote.":
        BCOC + "source-departs-no-note",
    "A departs-from source reference cites no claim.":
        BCOC + "source-departs-no-claim",
    "A departs-from source reference cites a claim that is not a claim of "
    "the source it cites.": BCOC + "source-departs-foreign-claim",
    "A departs-from source reference cites a claim whose status is not V "
    "or P.": BCOC + "source-departs-weak-claim",
    "A consistent-with source reference has no bco:support.":
        BCOC + "source-consistent-no-support",
    "Source reference has more than one bco:support.":
        BCOC + "source-two-supports",
    "Source reference has a bco:support other than definitional or "
    "contextual.": BCOC + "source-bad-support",
    "Source reference carries bco:support with a relation other than "
    "consistent-with.": BCOC + "source-support-not-consistent",
    # source records
    "Source record is not a dcterms:BibliographicResource.":
        BCOS + "SRC-BA-01",
    "Source record has no dcterms:identifier.": BCOS + "SRC-BA-02",
    "Source record's dcterms:identifier is not its IRI's local name.":
        BCOS + "SRC-BA-03",
    "Source record has no dcterms:bibliographicCitation.":
        BCOS + "SRC-BA-04",
    # claims (review R7, Finding A)
    "Source record has no bco:hasClaim.": BCOS + "SRC-BA-05",
    "Source record carries a bco:claimStatus of its own; a status belongs "
    "on the claim it qualifies.": BCOS + "SRC-BA-06",
    "Source record has two claims with the same bco:claimIndex.":
        BCOS + "SRC-BA-07",
    "Source record links a claim that is not one of its own.":
        BCOS + "SRC-BA-08",
    "Claim has no bco:claimIndex.": BCOS + "SRC-MS-01-claim-1",
    "Claim has more than one bco:claimIndex.": BCOS + "SRC-MS-01-claim-2",
    "Claim's bco:claimIndex is not a positive xsd:integer.":
        BCOS + "SRC-MS-01-claim-3",
    "Claim's bco:claimIndex is not the number its IRI ends with.":
        BCOS + "SRC-MS-01-claim-4",
    "Claim has no bco:claimStatus.": BCOS + "SRC-MS-01-claim-5",
    "Claim has more than one bco:claimStatus.": BCOS + "SRC-MS-01-claim-6",
    "Claim has a bco:claimStatus other than V, P, S, K or L.":
        BCOS + "SRC-MS-01-claim-7",
    "Claim belongs to no source record.": BCOS + "SRC-MS-02-claim-1",
    # concept records, current and prior (review R7, Finding B)
    "Record is not a prov:Entity.": BCOC + "record-" + "a" * 64,
    "Record has no bco:recordSha256.": BCOC + "record-" + "b" * 64,
    "Record has more than one bco:recordSha256.": BCOC + "record-" + "c" * 64,
    "Record's bco:recordSha256 is not the digest its IRI names.":
        BCOC + "record-" + "d" * 64,
    "Record is a revision of a record the vocabulary graph does not "
    "describe.": BCOC + "record-" + "1" * 64,
    "Record's bco:recordCommit is not a full 40-hex commit.":
        BCOC + "record-" + "3" * 64,
    # agents
    "Declared agent is not a prov:Agent.": BCOA + "fixture-untyped-agent",
    "Declared agent is not exactly one of prov:Person and "
    "prov:SoftwareAgent.": BCOA + "fixture-no-kind",
    "Person has no name (rdfs:label).": BCOA + "fixture-nameless-person",
    "Software agent has no bco:modelIdentifier.":
        BCOA + "fixture-software-no-model",
    "Software agent has no prov:actedOnBehalfOf.":
        BCOA + "fixture-software-unaccountable",
    "Software agent acted on behalf of something that is not a declared "
    "prov:Person.": BCOA + "fixture-software-for-software",
    # ratification references
    "Ratification reference has no bco:actPath.":
        BCOC + "ratification-no-path",
    "Ratification reference's bco:actPath is not a file under "
    "docs/decisions/ or docs/adr/.": BCOC + "ratification-path-elsewhere",
    "Ratification reference has no bco:actCommit.":
        BCOC + "ratification-no-commit",
    "Ratification reference's bco:actCommit is not a full 40-hex commit.":
        BCOC + "ratification-short-commit",
    "Ratification reference has no bco:actSha256.":
        BCOC + "ratification-no-sha",
    "Ratification reference's bco:actSha256 is not a 64-hex SHA-256.":
        BCOC + "ratification-bad-sha",
    "Ratification reference cites the SHA-256 of the empty file.":
        BCOC + "ratification-empty-file",
}

#: Built to conform. None may be the focus of a vocabulary violation.
VOCABULARY_POSITIVE_CONTROLS = [
    BCOA + "fixture-person", BCOA + "fixture-software",
    BCOS + "SRC-OMG-01", BCOS + "SRC-OMG-03",
    BCOM + "GoodMetamodelConcept", BCOC + "GoodCatalogConcept",
    BCOC + "source-good-adapted", BCOC + "source-good-definitional",
    BCOC + "source-good-contextual", BCOC + "GoodRatifiedConcept",
    BCOC + "ratification-good", BCOC + "GoodDeprecatedConcept",
    BCOC + "GoodDepartingConcept", BCOC + "source-good-departs",
    # Claims, one with a scope and a note; a current record revising a
    # described prior one (review R7, A and B).
    BCOS + "SRC-OMG-01-claim-1", BCOS + "SRC-OMG-03-claim-1",
    BCOS + "SRC-OMG-03-claim-2", BCOS + "SRC-MS-01",
    BCOC + "record-" + "4" * 64, BCOC + "record-" + "5" * 64,
    # Hosts: valid concepts that carry the broken references.
    BCOC + "VocabSourceHost", BCOC + "VocabRatificationHost",
    BCOC + "VocabRecordHost",
]


def shape_messages(path) -> tuple[list, list]:
    """(messages, constraint nodes with no message) of a shape file."""
    import rdflib

    SH = rdflib.Namespace("http://www.w3.org/ns/shacl#")
    graph = rdflib.Graph()
    graph.parse(path, format="turtle")
    constraints = (list(graph.objects(None, SH.property))
                   + list(graph.objects(None, SH.sparql)))
    messages = [str(graph.value(node, SH.message)) for node in constraints
                if graph.value(node, SH.message) is not None]
    silent = [node for node in constraints
              if graph.value(node, SH.message) is None]
    return messages, silent


def test_every_vocabulary_constraint_has_a_message_and_is_listed(layout):
    """Both directions. A constraint with no sh:message reports nothing a
    reader can act on (gen-shacl's failing, and why it was no-go); one
    missing from the list above has no named case; a listed message the
    shapes no longer carry is a test for nothing."""
    messages, silent = shape_messages(layout.path("validation.vocabulary"))
    assert not silent, "%d constraint(s) carry no sh:message" % len(silent)
    assert len(messages) == len(set(messages)), (
        "two constraints share a message, so the fixture cannot tell "
        "which one fired")
    assert set(messages) == set(VOCABULARY_CONSTRAINTS), (
        "unlisted: %s; listed but absent: %s"
        % (sorted(set(messages) - set(VOCABULARY_CONSTRAINTS)),
           sorted(set(VOCABULARY_CONSTRAINTS) - set(messages))))


def test_every_vocabulary_constraint_fires_on_its_own_case(validation):
    """Each message, on the focus node named for it -- not merely
    somewhere. A constraint firing only on some other case's incidental
    defect would pass a message-only check while its own case slipped
    through."""
    rung = validation["rungs"]["validation.vocabulary"]
    fired = {(v["focus"], v["message"]) for v in rung["fixture"]["detail"]}
    missing = sorted(message for message, focus
                     in VOCABULARY_CONSTRAINTS.items()
                     if (focus, message) not in fired)
    assert not missing, (
        "%d vocabulary constraint(s) did not fire on their own case: %s"
        % (len(missing), missing))


def test_the_vocabulary_fixture_does_not_flag_what_is_legitimate(validation):
    """The positive controls: a ratified, a deprecated, a departing and a
    multilingual concept, a typed notation, the agents and the records the
    cases rely on. The bug this caught on the day it was written: the
    "exactly one kind" rule, written as a COUNT in a sub-select, reported
    every agent there was."""
    rung = validation["rungs"]["validation.vocabulary"]
    flagged = {v["focus"]: v["message"] for v in rung["fixture"]["detail"]}
    wrong = {good: flagged[good] for good in VOCABULARY_POSITIVE_CONTROLS
             if good in flagged}
    assert not wrong, wrong


def test_the_vocabulary_is_in_the_data_graph_and_not_the_digest(
        validation, digest, layout, repo):
    """The vocabulary enters the ladder by declaration (`vocabulary:
    true`, layout.vocabulary_files), and stays out of the corpus digest:
    it is generated, and compared byte for byte by tools/vocab/build.py,
    so it is its own measurement -- and bco-sources.ttl is built from the
    register, which would move the ontology's digest on a citation
    edit."""
    vocabulary = sorted(p.relative_to(repo).as_posix()
                        for p in layout.vocabulary_files())
    assert vocabulary == sorted(
        "src/01_controlled_vocabulary/generated/%s.ttl" % name for name in (
            "bco-vocabulary", "bco-metamodel", "bco-catalog", "bco-sources",
            "bco-agents")), vocabulary
    assert sorted(validation["scope"]["vocabulary_files"]) == vocabulary
    assert not set(vocabulary) & set(digest["scope"]["paths"]), (
        digest["scope"]["paths"])

    # Listed is not loaded: the graph the shapes ran over holds exactly
    # the ontology, the vocabulary and the extracts.
    import rdflib

    expected = rdflib.Graph()
    for path in (layout.ontology_files() + layout.vocabulary_files()
                 + layout.vendored_files()):
        expected.parse(path, format="turtle")
    without = rdflib.Graph()
    for path in layout.ontology_files() + layout.vendored_files():
        without.parse(path, format="turtle")
    assert len(expected) > len(without), "the vocabulary adds no triple"
    assert validation["scope"]["data_triples"] == len(expected), (
        validation["scope"]["data_triples"], len(expected), len(without))


def test_the_layout_refuses_vocabulary_on_anything_but_generated(layout,
                                                                 tmp_path):
    """Only a generated artifact can be vocabulary Turtle: the vocabulary
    is authored as YAML and built, never written as Turtle by hand."""
    with pytest.raises(layout.LayoutError) as error:
        layout.Component({"id": "x", "path": "x.ttl",
                          "role": "ontology-module", "vocabulary": True},
                         tmp_path)
    assert "only a generated-artifact" in str(error.value)
    with pytest.raises(layout.LayoutError):
        layout.Component({"id": "x", "path": "x.ttl",
                          "role": "generated-artifact", "generator": "t",
                          "vocabulary": "yes"}, tmp_path)


def real_vocabulary(layout):
    import rdflib

    graph = rdflib.Graph()
    for path in layout.vocabulary_files():
        graph.parse(path, format="turtle")
    return graph


def vocabulary_violations(layout, graph) -> list[tuple[str, str]]:
    import rdflib
    from pyshacl import validate as shacl

    shapes = rdflib.Graph()
    shapes.parse(layout.path("validation.vocabulary"), format="turtle")
    _c, results, _t = shacl(data_graph=graph, shacl_graph=shapes,
                            inference="none", advanced=True)
    SH = rdflib.Namespace("http://www.w3.org/ns/shacl#")
    return sorted((str(results.value(r, SH.focusNode)),
                   str(results.value(r, SH.resultMessage)))
                  for r in results.subjects(rdflib.RDF.type,
                                            SH.ValidationResult))


def test_the_real_records_and_agents_are_selected(layout):
    """The zero the source-record and agent shapes report against the
    real vocabulary is not a constraint selecting nothing: strip every
    record's citation and the architect's name, in memory, and every one
    of the 63 records and the one person is reported. The concept shapes
    have their own guard on real data since P5, in the next test."""
    import rdflib

    graph = real_vocabulary(layout)
    assert vocabulary_violations(layout, graph) == []

    citation = rdflib.URIRef("http://purl.org/dc/terms/bibliographicCitation")
    records = set(graph.subjects(citation, None))
    assert len(records) == 63, len(records)
    graph.remove((None, citation, None))
    person = rdflib.URIRef(BCOA + "aaron-damiano")
    label = rdflib.URIRef("http://www.w3.org/2000/01/rdf-schema#label")
    assert (person, label, None) in graph
    graph.remove((person, label, None))

    found = vocabulary_violations(layout, graph)
    uncited = {f for f, m in found
               if m == "Source record has no dcterms:bibliographicCitation."}
    assert uncited == {str(r) for r in records}, len(uncited)
    assert (str(person), "Person has no name (rdfs:label).") in found
    assert len(found) == 64, found[:5]


def test_the_real_concepts_and_departures_are_selected(layout):
    """Since P5 the concept shapes run on real concepts: 9 metamodel and 5
    catalog, all Draft. Their zero is not a target selecting nothing:
    strip every concept's definition and every departs-from reference's
    departure note, in memory, and each of the 14 concepts and each
    departs-from reference is reported -- and nothing else."""
    import rdflib

    graph = real_vocabulary(layout)
    assert vocabulary_violations(layout, graph) == []

    bco = "https://fandaws.com/ontology/bco#"
    skos = "http://www.w3.org/2004/02/skos/core#"
    concepts = set(graph.subjects(rdflib.RDF.type,
                                  rdflib.URIRef(skos + "Concept")))
    metamodel = {c for c in concepts if str(c).startswith(BCOM)}
    catalog = {c for c in concepts if str(c).startswith(BCOC)}
    assert (len(metamodel), len(catalog)) == (9, 5), (metamodel, catalog)
    assert metamodel | catalog == concepts
    status = rdflib.URIRef(bco + "lifecycleStatus")
    assert {str(graph.value(c, status)) for c in concepts} == {"Draft"}

    relation = rdflib.URIRef(bco + "relation")
    departures = set(graph.subjects(relation, rdflib.Literal("departs-from")))
    assert departures, "the real vocabulary records no departs-from"
    graph.remove((None, rdflib.URIRef(skos + "definition"), None))
    graph.remove((None, rdflib.URIRef(bco + "departureNote"), None))

    found = vocabulary_violations(layout, graph)
    undefined = {f for f, m in found if m == "Concept has no skos:definition."}
    unnoted = {f for f, m in found if m == ("A departs-from source reference "
                                            "has no bco:departureNote.")}
    assert undefined == {str(c) for c in concepts}, len(undefined)
    assert unnoted == {str(d) for d in departures}, len(unnoted)
    assert len(found) == len(concepts) + len(departures), found[:5]


def test_the_real_claims_and_records_are_selected(layout):
    """Review R7, Findings A and B, on real data: the claim shape runs over
    every register claim and the record shape over every current and
    prior record. Their zero is not a target selecting nothing: strip the
    claims' statuses, in memory, and every claim is reported, and so is
    every departs-from reference, whose cited claim no longer has a status
    at V or P; strip the records' digests, and every record is reported,
    and so is every record that revises one."""
    import rdflib

    bco = "https://fandaws.com/ontology/bco#"
    prov = "http://www.w3.org/ns/prov#"
    graph = real_vocabulary(layout)
    assert vocabulary_violations(layout, graph) == []

    claims = set(graph.objects(None, rdflib.URIRef(bco + "hasClaim")))
    assert len(claims) == 83, len(claims)
    departures = set(graph.subjects(rdflib.URIRef(bco + "relation"),
                                    rdflib.Literal("departs-from")))
    assert departures
    stripped = real_vocabulary(layout)
    stripped.remove((None, rdflib.URIRef(bco + "claimStatus"), None))
    found = vocabulary_violations(layout, stripped)
    assert {f for f, m in found if m == "Claim has no bco:claimStatus."} \
        == {str(c) for c in claims}
    assert {f for f, m in found if m == (
        "A departs-from source reference cites a claim whose status is not "
        "V or P.")} == {str(d) for d in departures}
    assert len(found) == len(claims) + len(departures), found[:5]

    digest = rdflib.URIRef(bco + "recordSha256")
    current = set(graph.objects(None, rdflib.URIRef(bco + "currentRecord")))
    records = current | set(graph.subjects(digest, None))
    revising = set(graph.subjects(rdflib.URIRef(prov + "wasRevisionOf"),
                                  None))
    # 14 current records; 19 prior: 9 + 5 of the P5 pilot, 5 of R6. 19
    # records revise another: the 14 current and the 5 R6 catalog records.
    assert (len(current), len(records), len(revising)) == (14, 33, 19), (
        len(current), len(records), len(revising))
    stripped = real_vocabulary(layout)
    stripped.remove((None, digest, None))
    found = vocabulary_violations(layout, stripped)
    # With its digest gone, a prior record that revises nothing is selected
    # by nothing; every record that is current or revises is reported.
    selected = current | revising
    assert {f for f, m in found if m == "Record has no bco:recordSha256."} \
        == {str(r) for r in selected}
    assert {f for f, m in found if m == (
        "Record is a revision of a record the vocabulary graph does not "
        "describe.")} == {str(r) for r in revising}
    assert len(found) == len(selected) + len(revising), found[:5]


# ------------------------------------------- the committed measurement


def test_the_committed_digest_is_the_one_the_tool_produces(digest, repo):
    """An artifact in the tree that nothing compares is a claim, not a
    measurement. This is the comparison."""
    import json

    recorded = json.loads(
        (repo / "config/corpus-digest.json").read_text(encoding="utf-8"))
    assert (recorded["merged"]["ground_sha256"]
            == digest["merged"]["ground_sha256"]), (
        "config/corpus-digest.json describes a different corpus; "
        "regenerate it in the commit that changed the ontology")
    assert (recorded["merged"]["blank_nodes"]["shape_sha256"]
            == digest["merged"]["blank_nodes"]["shape_sha256"])
    assert recorded["scope"]["paths"] == digest["scope"]["paths"]
