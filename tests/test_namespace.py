# SPDX-License-Identifier: Apache-2.0
"""The authored namespaces, and the trap inside the shapes.

The BCO mints IRIs in exactly the five namespaces ADR-003 D1 names, all
provisional pending RP-5 (the ontology's own since the architect's choice
of 2026-10-23 in docs/decisions): bco# for the ontology, bco-metamodel#
and bco-catalog# for the vocabulary's two concept schemes, bco-sources#
for source records and bco-agents# for declared agents.
tools/ontology/validate.py lists them as AUTHORED_NAMESPACES. The spec
writes its terms as `ex:` in BPO's http://example.org/apqc#, and
`example.org` is IANA-reserved for documentation: IRIs under it can never
be dereferenced and must never be cited. BPO is upstream and pinned, so
references into its namespace are legitimate. Minting a term there is
not.

The trap is the second half of this file. The shapes carry SPARQL in
`sh:select` literals that test the namespace by string prefix. Text
inside a literal is not an IRI, so a namespace change that walked the
graph would leave it behind -- and the constraint would then match
nothing, report no violations, and look exactly like a passing shape.
Carried from ARO, where a namespace migration had exactly that construct
in it; widened in P4 from one namespace to five, each shown to matter.
"""

from __future__ import annotations

import importlib.util
import re
import sys

import pytest

from conftest import ROOT, load_tool

RESERVED = "example.org"
STALE = "https://stale.invalid/ns#"

#: `STRSTARTS(STR(?x), "<namespace>")`, as the shapes spell a namespace
#: filter. The namespace is group 2.
FILTER = re.compile(r'(STRSTARTS\(STR\([?$]\w+\),\s*")([^"]*)(")')


@pytest.fixture(scope="module")
def validator():
    return load_tool("bco_validate_ns", "tools/ontology/validate.py")


@pytest.fixture(scope="module")
def namespaces(validator):
    return validator.AUTHORED_NAMESPACES


@pytest.fixture(scope="module")
def upstream(validator):
    return tuple(validator.UPSTREAM)


@pytest.fixture(scope="module")
def vocab_build():
    """tools/vocab/build.py, registered before it runs (its dataclasses
    look their module up in sys.modules while being defined)."""
    name = "bco_vocab_build_ns"
    spec = importlib.util.spec_from_file_location(
        name, ROOT / "tools/vocab/build.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def turtle(layout):
    """Everything this repository authors in Turtle: the modules, the
    generated vocabulary, the shapes and the fixtures. Not the vendored
    extracts, which are other people's, and not the v0.1 draft, which is
    preserved as it was."""
    paths = list(layout.ontology_files()) + list(layout.vocabulary_files())
    for role in ("ontology-validation", "test-fixture"):
        for entry in layout.components(role):
            paths.extend(entry.members("*.ttl"))
    return sorted(paths)


def filters_in(path) -> list[str]:
    """Every namespace string a shape file's SPARQL filters on, read from
    the parsed literals rather than the file text, so a comment naming a
    namespace is not mistaken for a filter on it."""
    import rdflib

    graph = rdflib.Graph()
    graph.parse(path, format="turtle")
    found = []
    for _s, _p, obj in graph:
        if isinstance(obj, rdflib.Literal) and "STRSTARTS" in str(obj):
            found.extend(m.group(2) for m in FILTER.finditer(str(obj)))
    return found


def test_the_corpus_was_measured_not_assumed(turtle, layout):
    """Guards every test below: an empty file list passes all of them."""
    assert len(turtle) >= 11, turtle
    assert len(layout.vocabulary_files()) == 5, layout.vocabulary_files()


# ------------------------------------------------- the namespace list


def test_the_authored_namespaces_are_adr_003_d1_exactly(namespaces,
                                                        vocab_build):
    """The list in validate.py and the namespaces the vocabulary build
    mints in are one list. Two hand-kept copies that disagreed would
    leave a vocabulary namespace outside the ladder's attribution, or the
    ladder filtering on one nothing is minted in."""
    assert len(namespaces) == 5 and len(set(namespaces)) == 5, namespaces
    assert tuple(ns for _prefix, ns in vocab_build.NAMESPACES) == \
        tuple(namespaces), (vocab_build.NAMESPACES, namespaces)
    assert namespaces[0] == vocab_build.BCO, (
        "the first authored namespace is the ontology's own; the site and "
        "the class target rely on that order")


def test_the_authored_namespaces_are_siblings(namespaces):
    """No namespace is a prefix of another (D1), so a STRSTARTS filter on
    one cannot select another's terms. The stem the five share,
    https://fandaws.com/ontology/bco, is not itself a namespace."""
    for one in namespaces:
        for other in namespaces:
            if one != other:
                assert not other.startswith(one), (one, other)
    assert all(ns.endswith("#") for ns in namespaces), namespaces


def test_no_authored_namespace_is_an_upstream_one(namespaces, upstream):
    """If the BCO authored in BPO's namespace, as the spec writes it,
    nothing could tell a BCO term from a vendored BPO one, and every
    violation would be attributed by a guess. Attribution is by string
    prefix, so overlap in either direction is refused, not only
    equality."""
    for ns in namespaces:
        assert ns not in upstream
        assert not [u for u in upstream
                    if ns.startswith(u) or u.startswith(ns)], ns
    assert "http://example.org/apqc#" in upstream, (
        "BPO's namespace is not treated as upstream, so a defect in the "
        "vendored BPO extract would be reported as a defect here")


def test_the_overlap_guard_refuses_a_clash(validator, monkeypatch):
    """Falsifies the guard in validate._upstream: an authored namespace
    under an upstream one is refused rather than silently attributed."""
    monkeypatch.setattr(validator, "AUTHORED_NAMESPACES",
                        ("http://example.org/apqc#bco/",))
    with pytest.raises(SystemExit) as error:
        validator._upstream()
    assert "cannot be told apart" in str(error.value)


def test_the_old_single_namespace_name_is_gone(validator, repo):
    """P4 replaced AUTHORED_NAMESPACE with a list and deleted the name.
    An alias would let a consumer keep reading one namespace while the
    ladder checks five."""
    assert not hasattr(validator, "AUTHORED_NAMESPACE")
    for relative in ("tools/site/build_site.py", "tools/ontology",
                     "tools/vocab", "tools/layout.py"):
        target = repo / relative
        files = [target] if target.is_file() else sorted(
            target.glob("*.py"))
        assert files, relative
        for path in files:
            text = path.read_text(encoding="utf-8")
            assert not re.search(r"\bAUTHORED_NAMESPACE\b", text), path


# ----------------------------------------------- the reserved domain


def test_nothing_is_minted_in_the_reserved_domain(turtle, upstream):
    """Subjects, not references.

    A BCO module will point at BPO act types, which live under
    example.org, so a reference there is expected. Declaring a term
    there is not: it would be a BCO term in BPO's namespace, under a
    domain nobody can dereference.
    """
    import rdflib

    offenders = []
    for path in turtle:
        graph = rdflib.Graph()
        graph.parse(path, format="turtle")
        for subject in set(graph.subjects()):
            if (isinstance(subject, rdflib.URIRef)
                    and RESERVED in str(subject)):
                offenders.append((path.name, str(subject)[:70]))
    assert not offenders, (
        "%d term(s) are minted under %s: %s"
        % (len(offenders), RESERVED, offenders[:5]))


def test_every_reserved_domain_reference_is_to_a_pinned_upstream(turtle,
                                                                upstream):
    """The other half. A reference into example.org that is not BPO's
    pinned namespace is a typo or a leftover from the spec's `ex:`
    examples, and either way points at nothing."""
    import rdflib

    stray = []
    for path in turtle:
        graph = rdflib.Graph()
        graph.parse(path, format="turtle")
        for triple in graph:
            for term in triple:
                if (isinstance(term, rdflib.URIRef) and RESERVED in str(term)
                        and not str(term).startswith(upstream)):
                    stray.append((path.name, str(term)[:70]))
    assert not stray, stray[:8]


def test_every_declared_prefix_is_authored_or_pinned(turtle, namespaces,
                                                     upstream):
    """A prefix pointing somewhere else is either an upstream vocabulary
    nobody pinned or a mistake, and the two look identical in a diff."""
    standard = ("http://www.w3.org/", "http://purl.org/dc/")
    authored = tuple(ns.rstrip("#") for ns in namespaces)
    stray = []
    for path in turtle:
        for match in re.finditer(r"@prefix\s+\S*:\s+<([^>]+)>",
                                 path.read_text(encoding="utf-8")):
            iri = match.group(1)
            if (iri.startswith(authored) or iri.startswith(upstream)
                    or iri.startswith(standard)):
                continue
            stray.append((path.name, iri))
    assert not stray, stray[:8]


# ---------------------------------------------- the vacuous-pass trap


def test_the_sparql_inside_the_shapes_names_only_authored_namespaces(
        layout, namespaces):
    """The list and the shapes agree, both directions.

    Every namespace a filter names is in AUTHORED_NAMESPACES -- a filter
    on any other string runs, matches nothing, and reports no violation
    -- and every namespace in the list is named by some filter, so none
    is left unchecked.
    """
    named = {}
    for entry in layout.components("ontology-validation"):
        found = filters_in(entry.resolve())
        stray = sorted(set(found) - set(namespaces))
        assert not stray, (
            "%s filters on %s, which is not an authored namespace; it "
            "would run, match nothing, and report no violations"
            % (entry.id, stray))
        named[entry.id] = set(found)
    union = set().union(*named.values())
    assert union == set(namespaces), (
        "named by no shape: %s" % sorted(set(namespaces) - union))


def test_the_wellformedness_population_is_d1s(layout, namespaces):
    """ADR-003 D1's table: the ontology's classes and the two SKOS
    schemes' concepts are in the wellformedness population; source
    records and agents are not (D8), and have their own shapes."""
    found = filters_in(layout.path("validation.wellformedness"))
    assert set(found) == set(namespaces[:3]), found
    assert len(found) >= 3, (
        "expected one filter per namespace at least; found %d, so the "
        "targets changed or this test is no longer watching them"
        % len(found))


def fixture_graph(layout):
    import rdflib

    graph = rdflib.Graph()
    for entry in layout.components("test-fixture"):
        for path in entry.members("*.ttl"):
            graph.parse(path, format="turtle")
    return graph


_RUNS: dict = {}


def violations(fixture, shape_text) -> list[tuple[str, str]]:
    """(focus, message) of every violation the shapes report.

    Memoised on the shape text: the unmutated shapes are asked the same
    question by several tests, and a pyshacl run over the vocabulary
    shapes takes seconds even on the small fixture. The fixture is the
    same graph every time (the committed fixture files).
    """
    if shape_text not in _RUNS:
        _RUNS[shape_text] = _violations(fixture, shape_text)
    return _RUNS[shape_text]


def _violations(fixture, shape_text) -> list[tuple[str, str]]:
    import rdflib
    from pyshacl import validate as shacl

    shapes = rdflib.Graph()
    shapes.parse(data=shape_text, format="turtle")
    _conforms, results, _text = shacl(data_graph=fixture, shacl_graph=shapes,
                                      inference="none", advanced=True)
    SH = rdflib.Namespace("http://www.w3.org/ns/shacl#")
    return sorted((str(results.value(r, SH.focusNode)),
                   str(results.value(r, SH.resultMessage)))
                  for r in results.subjects(rdflib.RDF.type,
                                            SH.ValidationResult))


def stale(text: str, namespace: str) -> str:
    """The shapes with one namespace's filters pointed nowhere -- in the
    SPARQL only, never in a @prefix the constraints' paths depend on."""
    changed, count = FILTER.subn(
        lambda m: m.group(1) + (STALE if m.group(2) == namespace
                                else m.group(2)) + m.group(3), text)
    assert count and changed != text, (
        "no filter on %s to make stale" % namespace)
    return changed


def population(found, namespace) -> set:
    """Focus nodes in `namespace` that are what its filter selects --
    terms, concepts, records, agents -- and not the provenance nodes the
    vocabulary build mints in a concept's namespace (<ns>source-...,
    <ns>ratification-..., <ns>record-...), which the vocabulary shapes
    select structurally rather than by namespace."""
    return {focus for focus, _ in found
            if focus.startswith(namespace)
            and not re.match(r"(source|ratification|record)-",
                             focus[len(namespace):])}


#: (shape set, index into AUTHORED_NAMESPACES) for every filter that
#: selects a population. The test after this one requires the list to
#: cover every filter except the one negative use, which has its own.
TARGET_FILTERS = [
    ("validation.wellformedness", 0),
    ("validation.wellformedness", 1),
    ("validation.wellformedness", 2),
    ("validation.vocabulary", 1),
    ("validation.vocabulary", 2),
    ("validation.vocabulary", 3),
    ("validation.vocabulary", 4),
]
NEGATIVE_FILTERS = [("validation.vocabulary", 0)]


@pytest.mark.parametrize("shape_set, index", TARGET_FILTERS)
def test_a_stale_namespace_filter_really_does_select_nothing(
        layout, namespaces, shape_set, index):
    """Guards the agreement test by demonstrating the trap it exists
    for, once per namespace each shape set filters on.

    The same shapes, with that one namespace's filter strings pointed
    at a namespace nothing uses, run against the fixtures built to break
    them -- and find nothing wrong in that namespace, while it found
    something before. If they still found violations there, the filter
    would not be what selects the targets, and the agreement test would
    be guarding a string that does not matter.
    """
    namespace = namespaces[index]
    text = layout.path(shape_set).read_text(encoding="utf-8")
    fixture = fixture_graph(layout)

    before = population(violations(fixture, text), namespace)
    assert before, ("the real shapes found nothing in %s, so there is "
                    "nothing for a stale filter to lose" % namespace)
    after = population(violations(fixture, stale(text, namespace)),
                       namespace)
    assert after == set(), (
        "with the %s filter pointed nowhere the shapes still reported %s"
        % (namespace, sorted(after)[:5]))


def test_a_stale_negative_filter_fires_on_good_data(layout, namespaces):
    """The trap the other way round. "Designates a class outside bco#"
    is a NOT-STRSTARTS filter: stale, it does not select nothing -- it
    rejects every metamodel concept, the positive control included."""
    message = ("Metamodel concept designates a class outside the bco: "
               "namespace.")
    good = namespaces[1] + "GoodMetamodelConcept"
    text = layout.path("validation.vocabulary").read_text(encoding="utf-8")
    fixture = fixture_graph(layout)

    assert (good, message) not in violations(fixture, text)
    assert (good, message) in violations(fixture,
                                         stale(text, namespaces[0]))


def test_every_filter_has_a_demonstration(layout, namespaces):
    """A filter added without a stale-string demonstration is a filter
    whose vacuous pass nobody has seen."""
    named = set()
    for entry in layout.components("ontology-validation"):
        for ns in set(filters_in(entry.resolve())):
            named.add((entry.id, namespaces.index(ns)))
    assert named == set(TARGET_FILTERS) | set(NEGATIVE_FILTERS), (
        "undemonstrated: %s; demonstrated but gone: %s"
        % (sorted(named - set(TARGET_FILTERS) - set(NEGATIVE_FILTERS)),
           sorted(set(TARGET_FILTERS) | set(NEGATIVE_FILTERS) - named)))
