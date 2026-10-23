# SPDX-License-Identifier: Apache-2.0
"""The ontology's namespace, and the trap inside the shapes.

The BCO authors in https://fandaws.com/ontology/bco#, provisionally
(RP-5; the architect's choice of 2026-10-23 in docs/decisions). The spec
writes its terms as `ex:` in BPO's http://example.org/apqc#, and
`example.org` is IANA-reserved for documentation: IRIs under it can never
be dereferenced and must never be cited. BPO is upstream and pinned, so
references into its namespace are legitimate. Minting a term there is
not.

The trap is the last pair of tests. The wellformedness shapes carry
SPARQL in `sh:select` literals that test the namespace by string prefix.
Text inside a literal is not an IRI, so a namespace change that walked
the graph would leave it behind -- and the constraint would then match
nothing, report no violations, and look exactly like a passing shape.
Carried from ARO, where a namespace migration had exactly that construct
in it.
"""

from __future__ import annotations

import pytest

from conftest import load_tool

RESERVED = "example.org"


@pytest.fixture(scope="module")
def validator():
    return load_tool("bco_validate_ns", "tools/ontology/validate.py")


@pytest.fixture(scope="module")
def namespace(validator):
    return validator.AUTHORED_NAMESPACE


@pytest.fixture(scope="module")
def upstream(validator):
    return tuple(validator.UPSTREAM)


@pytest.fixture(scope="module")
def turtle(layout):
    """Everything this repository authors in Turtle: the modules, the
    shapes and the fixtures. Not the vendored extracts, which are other
    people's, and not the v0.1 draft, which is preserved as it was."""
    paths = list(layout.ontology_files())
    for role in ("ontology-validation", "test-fixture"):
        for entry in layout.components(role):
            paths.extend(entry.members("*.ttl"))
    return sorted(paths)


def test_the_corpus_was_measured_not_assumed(turtle):
    """Guards every test below: an empty file list passes all of them."""
    assert len(turtle) >= 4, turtle


def test_the_authored_namespace_is_not_an_upstream_one(namespace, upstream):
    """If the BCO authored in BPO's namespace, as the spec writes it,
    nothing could tell a BCO term from a vendored BPO one, and every
    violation would be attributed by a guess."""
    assert namespace not in upstream
    assert "http://example.org/apqc#" in upstream, (
        "BPO's namespace is not treated as upstream, so a defect in the "
        "vendored BPO extract would be reported as a defect here")


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


def test_every_declared_prefix_is_authored_or_pinned(turtle, namespace,
                                                     upstream):
    """A prefix pointing somewhere else is either an upstream vocabulary
    nobody pinned or a mistake, and the two look identical in a diff."""
    import re

    standard = ("http://www.w3.org/", "http://purl.org/dc/")
    authored_root = namespace.rstrip("#")
    stray = []
    for path in turtle:
        for match in re.finditer(r"@prefix\s+\S*:\s+<([^>]+)>",
                                 path.read_text(encoding="utf-8")):
            iri = match.group(1)
            if (iri.startswith(authored_root) or iri.startswith(upstream)
                    or iri.startswith(standard)):
                continue
            stray.append((path.name, iri))
    assert not stray, stray[:8]


def test_the_sparql_inside_the_shapes_targets_the_current_namespace(
        layout, namespace):
    """The vacuous-pass trap.

    A constraint that filters on a namespace prefix string still runs
    when the string is stale. It simply selects nothing, reports no
    violation, and is indistinguishable from a shape that holds.
    """
    import rdflib

    citing = []
    for entry in layout.components("ontology-validation"):
        graph = rdflib.Graph()
        graph.parse(entry.resolve(), format="turtle")
        for _s, _p, obj in graph:
            if not isinstance(obj, rdflib.Literal) or "STRSTARTS" not in str(obj):
                continue
            if namespace in str(obj):
                citing.append(entry.id)
            else:
                pytest.fail(
                    "%s carries a SPARQL namespace filter that does not name "
                    "%s; it would run, match nothing, and report no "
                    "violations:\n%s" % (entry.id, namespace, obj))

    assert len(citing) >= 2, (
        "expected the wellformedness targets to name the namespace in their "
        "SPARQL; found %d such literals, so either the constraints changed "
        "or this test is no longer watching them" % len(citing))


def test_a_stale_namespace_filter_really_does_select_nothing(layout,
                                                             namespace):
    """Guards the test above by demonstrating the trap it exists for.

    The same shapes, with the filter string pointed at a namespace
    nothing uses, run against the fixture built to break them -- and
    find nothing wrong. If they still found violations, the filter would
    not be what selects the targets, and the test above would be
    guarding a string that does not matter.
    """
    import rdflib
    from pyshacl import validate as shacl

    shapes_path = layout.path("validation.wellformedness")
    text = shapes_path.read_text(encoding="utf-8")
    stale = text.replace(namespace, "https://stale.invalid/ns#")
    assert stale != text, "the filter string was not in the shapes at all"

    fixture = rdflib.Graph()
    for entry in layout.components("test-fixture"):
        for path in entry.members("*.ttl"):
            fixture.parse(path, format="turtle")

    def conforms(shape_text):
        shapes = rdflib.Graph()
        shapes.parse(data=shape_text, format="turtle")
        return shacl(data_graph=fixture, shacl_graph=shapes,
                     inference="none", advanced=True)[0]

    assert conforms(text) is False, "the real shapes did not fire"
    assert conforms(stale) is True, (
        "the shapes still fired with the namespace filter pointed nowhere")
