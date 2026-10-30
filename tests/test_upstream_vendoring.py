# SPDX-License-Identifier: Apache-2.0
"""The vendored BFO, CCO and BPO extracts, and whether they earn their place.

Two questions, and the second is the one worth asking.

  Is the vendoring correct?   Every upstream term this repository or its
                              specification names is described, nothing
                              dangles, the digests match, and every triple
                              sits in the extract of the file it came from.

  Is it load-bearing?         The BCO's realizing act types come from BPO,
                              which anchors them under CCO, which anchors
                              under BFO. A BPO act genus reaches
                              obo:BFO_0000015 (process) only when all
                              three are present. If that ever stops being
                              true the extracts are decoration.

None of these tests need the network. Rebuilding from upstream does, and
that is a separate mode of the tool -- see `--confirm`, which is what
shows these files are derived from the pins rather than hand-edited.

Carried from the Application Requirement Ontology and rewritten where the
measurements differ: ARO's load-bearing test was 116 capability classes
reaching cco:ont00001379, and the BCO has no authored class yet.
"""

from __future__ import annotations

import json

import pytest

from conftest import load_tool

#: BPO's namespace since v0.4.0; vendored at it since the 2026-10-28 re-pin.
BPO = "https://fandaws.com/ontology/bpo#"
PROCESS = "http://purl.obolibrary.org/obo/BFO_0000015"
DISPOSITION = "http://purl.obolibrary.org/obo/BFO_0000016"
REALIZABLE = "http://purl.obolibrary.org/obo/BFO_0000017"
MATERIAL_ENTITY = "http://purl.obolibrary.org/obo/BFO_0000040"
ORGANIZATION = "https://www.commoncoreontologies.org/ont00001180"
ORGANIZATION_CAPABILITY = "https://www.commoncoreontologies.org/ont00000568"


@pytest.fixture(scope="module")
def vendoring():
    return load_tool("bco_vendor", "tools/ontology/vendor_upstream.py")


@pytest.fixture(scope="module")
def report(vendoring):
    return vendoring.verify()


@pytest.fixture(scope="module")
def manifest(vendoring):
    import json

    root = vendoring.layout.repository_root()
    return json.loads((root / vendoring.MANIFEST).read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def extracts(layout):
    """The vendored extracts as one graph."""
    import rdflib

    graph = rdflib.Graph()
    for path in layout.vendored_files():
        graph.parse(path, format="turtle")
    return graph


def extract(layout, component_id):
    import rdflib

    graph = rdflib.Graph()
    graph.parse(layout.path(component_id), format="turtle")
    return graph


# ------------------------------------------------------------- pinning


def test_every_url_names_the_commit_it_pins(vendoring):
    """A tag can be moved to a different commit; a commit cannot.

    Includes BPO's licence statement url, which is read for the licence
    and would otherwise be read from whatever that url serves today.
    """
    for entry in vendoring.sources():
        assert entry["commit"] in entry["url"], entry["id"]
        statement = entry["licence"].get("statement_url")
        if statement:
            assert entry["commit"] in statement, entry["id"]


def test_a_licence_statement_off_the_pinned_commit_is_refused(
        vendoring, monkeypatch):
    """Falsifies the check above in the tool rather than in this file."""
    real = vendoring.sources()
    tampered = [dict(entry, licence=dict(entry["licence"]))
                for entry in real]
    bpo = next(entry for entry in tampered if entry["id"] == "bpo")
    bpo["licence"]["statement_url"] = bpo["licence"]["statement_url"].replace(
        bpo["commit"], "main")
    assert bpo["licence"]["statement_url"] != next(
        e for e in real if e["id"] == "bpo")["licence"]["statement_url"]

    import yaml

    monkeypatch.setattr(yaml, "safe_load", lambda _text: {"sources": tampered})
    with pytest.raises(SystemExit) as error:
        vendoring.sources()
    assert "does not name the pinned commit" in str(error.value)


def test_the_recorded_digest_is_what_the_extract_digests_to(report):
    assert report["ok"], report["findings"]


def test_the_manifest_records_a_source_digest_for_every_extract(vendoring,
                                                                manifest):
    pinned = {entry["id"]: entry for entry in vendoring.sources()}
    assert set(manifest["extracts"]) == set(pinned) == {"bfo", "cco", "bpo"}
    for key, record in manifest["extracts"].items():
        assert record["source_sha256"] == pinned[key]["sha256"], key
        assert record["commit"] == pinned[key]["commit"], key


# ------------------------------------------------------- completeness


def test_every_upstream_term_named_here_is_described(report):
    """The check that catches the corpus or the spec growing past the
    extract. A new cco: reference lands as a term nothing describes, and
    a shape walking through it silently answers "no" for every subject."""
    assert report["unresolved_seeds"] == [], report["unresolved_seeds"]


def test_the_extracts_reference_nothing_they_do_not_describe(report):
    """Closure. An extract that mentions an upstream term it does not
    carry has the same defect as the corpus would, one level down."""
    assert report["dangling_references"] == [], report["dangling_references"]


def test_a_term_that_is_not_vendored_is_reported_rather_than_ignored(
        vendoring, monkeypatch):
    """Falsifies the completeness check.

    Both assertions above pass when nothing is missing and would also
    pass if the check looked at the wrong thing. Adding one term nobody
    vendored has to produce a finding.
    """
    real = vendoring.seed_terms
    invented = "https://www.commoncoreontologies.org/ont00000000"

    monkeypatch.setattr(vendoring, "seed_terms",
                        lambda namespaces: real(namespaces) | {invented})
    record = vendoring.verify()
    assert invented in record["unresolved_seeds"], record
    assert not record["ok"]


def test_a_new_spec_term_fails_until_the_extracts_are_rebuilt(
        vendoring, monkeypatch):
    """The spec is a seed source, so a spec revision naming a new CCO
    class must fail offline verification -- that failure is the moment
    somebody rebuilds and looks at what the new term is. Only the terms
    the last build recorded as unresolvable are excused."""
    real = vendoring.spec_terms
    invented = "https://www.commoncoreontologies.org/ont00000001"
    assert invented not in vendoring.recorded_unresolvable_spec_terms()

    monkeypatch.setattr(vendoring, "spec_terms",
                        lambda: real() | {invented})
    record = vendoring.verify()
    assert invented in record["unresolved_seeds"], record
    assert not record["ok"]


def test_the_spec_is_actually_read(vendoring, manifest):
    """Guards the two tests above and the excuse list: a spec reader that
    found nothing would excuse nothing and fail nothing.

    Every cco: and obo: term the v0.4 spec names is described by CCO v2.0
    or BFO, measured 2026-10-23. The only spec terms nothing describes
    are in the ex: namespace -- terms the BCO will mint, and BPO terms
    from files not vendored.
    """
    spec = vendoring.spec_terms()
    assert len(spec) > 80, len(spec)
    assert ORGANIZATION in spec

    for key in ("bfo", "cco"):
        assert len(manifest["extracts"][key]["seed_terms"]) >= 6, key

    unresolved = manifest[vendoring.UNRESOLVED_KEY]
    assert "ex:BusinessCapability" in unresolved
    assert "ex:ActOfAcquisition" not in unresolved
    assert not [n for n in unresolved
                if n.startswith(("cco:", "obo:"))], unresolved


def test_spec_names_nothing_describes_are_attributed_to_no_namespace(
        vendoring, manifest):
    """The spec writes `ex:` for BPO's terms and for terms the BCO will
    mint, so expanding ex:BusinessCapability would record a BCO class as
    a term of BPO's namespace -- what the architect's R3 (2026-10-28)
    forbids. The manifest lists such names once, as the spec writes them,
    and no extract's record names any of them as an IRI."""
    unresolved = manifest[vendoring.UNRESOLVED_KEY]
    assert unresolved, "the guard below would pass vacuously"
    assert not [n for n in unresolved if "://" in n], unresolved[:5]
    as_iris = {vendoring.expand_spec_name(n) for n in unresolved}
    recorded = json.dumps(manifest["extracts"])
    assert not [iri for iri in as_iris if '"%s"' % iri in recorded]


def test_a_recorded_name_with_an_unknown_prefix_is_refused(vendoring):
    """Falsifies the expansion the excuse list relies on: a name whose
    prefix no pin declares names nothing, so it cannot be excused."""
    assert vendoring.expand_spec_name("ex:Thing") == BPO + "Thing"
    with pytest.raises(vendoring.Refused):
        vendoring.expand_spec_name("zz:Thing")


def test_a_markdown_escaped_underscore_does_not_truncate_a_term(
        vendoring, layout, monkeypatch, tmp_path):
    """Markdown writes `ex:acme\\_map` for ex:acme_map. Read naively that
    is ex:acme, a different term -- and an invented one that would then
    be recorded as named by the spec."""
    spec = tmp_path / "spec.md"
    spec.write_text("The map " + "`ex:acme" + chr(92) + "_map`" + ".",
                    encoding="utf-8")

    class Spec:
        @staticmethod
        def resolve():
            return spec

    monkeypatch.setattr(vendoring.layout, "components",
                        lambda role=None: [Spec()])
    found = vendoring.spec_terms()
    assert BPO + "acme_map" in found, found
    assert BPO + "acme" not in found, found


def test_the_extracts_carry_no_blank_nodes(extracts):
    """By construction, and the reason the digest means anything.

    rdflib renames blank nodes on every parse. An extract containing one
    would digest differently every time it was rebuilt from identical
    upstream bytes, and `--confirm` would report a difference that is not
    there.
    """
    import rdflib

    blank = [t for triple in extracts for t in triple
             if isinstance(t, rdflib.BNode)]
    assert not blank, "%d blank node(s) in the extracts" % len(blank)


# ---------------------------------------------------------- attribution


def test_a_triple_is_vendored_under_the_file_it_came_from(
        vendoring, monkeypatch, tmp_path):
    """The defect fixed in this repository's copy of the tool.

    ARO partitioned selected triples by subject namespace alone. CCO's
    merged file carries its own annotations on BFO terms, so triples that
    exist only in CCO were written into the BFO extract under BFO's
    licence, with a header naming bfo-core.ttl as their source. Built
    here from two constructed upstreams so the case is exercised without
    the network: B annotates a term in A's namespace, and that triple has
    to land in B's extract.
    """
    import rdflib

    a_ns, b_ns = "https://a.invalid/", "https://b.invalid/"
    licence = "<http://purl.org/dc/terms/license>"
    a_ttl = ("<%sx> <http://www.w3.org/2000/01/rdf-schema#label> \"x\" .\n"
             "<%sonto> %s \"licence-A\" .\n" % (a_ns, a_ns, licence))
    b_ttl = ("<%sx> <http://www.w3.org/2004/02/skos/core#scopeNote> "
             "\"said by B\" .\n"
             "<%sy> <http://www.w3.org/2000/01/rdf-schema#subClassOf> "
             "<%sx> .\n"
             "<%sonto> %s \"licence-B\" .\n"
             % (a_ns, b_ns, a_ns, b_ns, licence))
    pins = []
    for key, namespace, text in (("a", a_ns, a_ttl), ("b", b_ns, b_ttl)):
        pins.append({
            "id": key, "project": key.upper(), "release": "r",
            "commit": "c0ffee", "url": "https://u.invalid/c0ffee/" + key,
            "sha256": key, "namespace": namespace, "prefix": key,
            "extract": "vendor/%s.ttl" % key, "_text": text,
            "licence": {"spdx": "MIT", "url": "https://l.invalid/",
                        "licence_statement_contains": "licence-" + key.upper(),
                        "attribution": key}})

    monkeypatch.setattr(vendoring, "sources", lambda: pins)
    monkeypatch.setattr(vendoring, "fetch",
                        lambda source, cache: source["_text"].encode("utf-8"))
    monkeypatch.setattr(vendoring, "seed_terms",
                        lambda namespaces: {b_ns + "y"})
    monkeypatch.setattr(vendoring, "spec_terms", lambda: set())

    built = vendoring.build(tmp_path)
    graph_a, graph_b = rdflib.Graph(), rdflib.Graph()
    graph_a.parse(data=built["a"]["text"], format="turtle")
    graph_b.parse(data=built["b"]["text"], format="turtle")

    note = (rdflib.URIRef(a_ns + "x"),
            rdflib.URIRef("http://www.w3.org/2004/02/skos/core#scopeNote"),
            rdflib.Literal("said by B"))
    assert note in graph_b, "B's annotation on A's term left B's extract"
    assert note not in graph_a, (
        "B's annotation on A's term was vendored under A's licence")
    assert (rdflib.URIRef(a_ns + "x"), rdflib.RDFS.label,
            rdflib.Literal("x")) in graph_a


# ------------------------------------------------------- load-bearing


def reaching(graph, anchor: str) -> set:
    query = """
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        SELECT DISTINCT ?c WHERE {
          ?c rdfs:subClassOf* <%s> .
          FILTER(STRSTARTS(STR(?c), "%s"))
        }""" % (anchor, BPO)
    return {str(row[0]) for row in graph.query(query)}


def test_bpo_act_genera_are_processes_only_with_cco_and_bfo(layout,
                                                           extracts):
    """The measurement this vendoring exists for.

    A capability is realized by acts of BPO types (spec section 2), and
    an act type that is not a process cannot realize anything. BPO
    anchors its genera under CCO acts; CCO anchors those under BFO. With
    BPO alone the chain stops at the first CCO parent and no genus is a
    process. With all three, every one is.
    """
    bpo_only = extract(layout, "vendor.bpo")
    genera = {str(s) for s in bpo_only.subjects()
              if str(s).startswith(BPO)}
    assert len(genera) >= 6, genera

    assert reaching(bpo_only, PROCESS) == set(), (
        "BPO genera reach BFO process without CCO and BFO, so those "
        "extracts are not what makes the realization question answerable")
    assert reaching(extracts, PROCESS) == genera, (
        "%s do not reach obo:BFO_0000015 even with every extract present"
        % sorted(genera - reaching(extracts, PROCESS)))


def test_the_extracts_say_what_cd1_and_cd3_assume(extracts):
    """Two facts the spec's design rests on, read from the upstream
    rather than restated.

    CD1: the bearer is a cco:Organization, which must be a material
    entity for a disposition to inhere in it. It is.

    CD3: a capability class is asserted under obo:BFO_0000016
    (disposition) explicitly, after G1-T. That assertion is the BCO's to
    make -- CCO v2.0 puts Organization Capability under realizable
    entity and not under disposition. If an upstream re-pin ever changed
    that, CD3's explicit co-parent would become redundant and this test
    is where it would show.
    """
    def reaches(sub, sup):
        return extracts.query(
            "ASK { <%s> <http://www.w3.org/2000/01/rdf-schema#subClassOf>* "
            "<%s> }" % (sub, sup)).askAnswer

    assert reaches(ORGANIZATION, MATERIAL_ENTITY)
    assert reaches(ORGANIZATION_CAPABILITY, REALIZABLE)
    assert not reaches(ORGANIZATION_CAPABILITY, DISPOSITION)


# ---------------------------------------------------------- licensing


def test_the_extracts_are_third_party_and_redistributable(disposition):
    """The three extracts, among the vendored rows. The site's vendored
    assets (config/site-vendor.yaml) and the inventory's entries files
    (config/inventory-sources.yaml) are third-party-redistributed too, and
    are held to their own pins in tests/test_site.py and
    tests/test_inventory.py; here every vendored row is only required to
    be accounted for by exactly one of the three pin files."""
    rows = {row.path: row for row in disposition.classify()}
    extracts = disposition.vendored_sources()
    site_assets = disposition.site_vendored_assets()
    inventory = disposition.inventory_sources()
    every = [row for row in rows.values()
             if row.disposition == disposition.VENDORED]
    assert {row.path for row in every} == (
        set(extracts) | set(site_assets) | set(inventory))
    vendored = [row for row in every if row.path in extracts]
    assert len(vendored) == 3, [row.path for row in vendored]
    assert {row.licence for row in vendored} == {
        "CC-BY-4.0", "BSD-3-Clause", "MIT"}
    for row in vendored:
        assert row.redistributable, row.path


def test_the_licence_comes_from_the_pins_not_from_this_repository(
        disposition, monkeypatch):
    """A vendored file does not carry this repository's licence.

    ARO asserted the two differ. Here they do not -- BPO is MIT, and so
    is this repository -- so equality proves nothing, and the classifier
    is asked instead with the project licence replaced by a sentinel. A
    vendored row that reported the sentinel took its licence from the
    wrong place.
    """
    monkeypatch.setattr(disposition, "project_licence",
                        lambda: "SENTINEL-PROJECT-LICENCE")
    pinned = {path: disposition.licence_expression(entry)
              for path, (entry, _notice)
              in disposition.redistributed_sources().items()}
    rows = [row for row in disposition.classify()
            if row.disposition == disposition.VENDORED]
    assert rows
    for row in rows:
        assert row.licence == pinned[row.path], row


def test_attribution_is_checked_rather_than_assumed(disposition,
                                                    monkeypatch):
    """Falsifies the attribution check.

    Every licence here permits redistribution on condition of
    attribution. Pointing the check at a file that does not contain the
    attribution has to produce a finding, or the condition is being
    reported as met by a check that never looks.
    """
    rows = disposition.classify()
    assert disposition.attribution_findings(rows) == []

    monkeypatch.setattr(disposition, "NOTICE", "LICENSE")
    problems = disposition.attribution_findings(rows)
    assert problems, (
        "the attribution check passed against a file containing no "
        "attribution")
    for extract_path in ("vendor/bfo/bfo-core-bco-extract.ttl",
                         "vendor/cco/cco-bco-extract.ttl",
                         "vendor/bpo/bpo-ext-bco-extract.ttl"):
        assert extract_path in problems[0], extract_path


# -------------------------------------------------- what was not done


def test_the_manifest_states_what_the_extracts_leave_out(manifest):
    """A partial extract that does not say it is partial is the defect
    this whole method is about."""
    assert manifest["not_covered"], manifest.keys()
    assert any("anonymous class expression" in line
               for line in manifest["not_covered"])
    assert any("consistent" in line for line in manifest["not_covered"])
    assert any("apqc-ext.ttl alone" in line
               for line in manifest["not_covered"])

    dropped = sum(entry["axioms_dropped_anonymous_object"]
                  for entry in manifest["extracts"].values())
    assert dropped > 0, (
        "no axioms were dropped, so either the upstream has no anonymous "
        "class expressions -- it does -- or the count is not being taken")


def test_each_extract_says_in_its_own_header_that_it_is_partial(layout):
    """The manifest is a file somebody has to go and read. The extract is
    the file they already have open."""
    paths = layout.vendored_files()
    assert len(paths) == 3, paths
    for path in paths:
        head = path.read_text(encoding="utf-8")[:3000]
        assert "partial extract" in head.lower(), path.name
        assert "cannot be" in head and "consistency" in head, path.name
        assert "axioms about the selected terms were dropped" in head, \
            path.name


# --------------------------------------------------------- serialising


def test_the_serialiser_round_trips_awkward_literals(vendoring):
    """Falsifies the escaping.

    Definitions in CCO run to several lines and contain quotation marks.
    A serialiser that got either wrong would emit a file that parses to a
    different graph, and the digest recorded for it would be a digest of
    the damage.
    """
    import rdflib

    subject = rdflib.URIRef("https://ex.invalid/a")
    awkward = ('line one' + chr(10) + 'line "two"' + chr(9) + 'tabbed'
               + chr(92) + ' backslash')
    triples = [
        (subject, rdflib.URIRef("https://ex.invalid/p"),
         rdflib.Literal(awkward, lang="en")),
        (subject, rdflib.URIRef("http://www.w3.org/2000/01/rdf-schema#label"),
         rdflib.Literal("plain")),
        (subject, rdflib.URIRef("https://ex.invalid/n"),
         rdflib.Literal("3", datatype=rdflib.URIRef(
             "http://www.w3.org/2001/XMLSchema#integer"))),
    ]
    text = vendoring.serialise(triples, ["a test"])
    assert chr(10) not in text.split('"')[1], (
        "the literal was emitted across lines, so a newline inside it is "
        "no longer distinguishable from formatting")

    back = rdflib.Graph()
    back.parse(data=text, format="turtle")
    assert set(back) == set(triples)


def test_the_same_inputs_serialise_to_the_same_bytes(vendoring):
    """Sorted, deduplicated, and independent of the order given."""
    import rdflib

    triples = [
        (rdflib.URIRef("https://ex.invalid/b"),
         rdflib.URIRef("https://ex.invalid/p"), rdflib.Literal("two")),
        (rdflib.URIRef("https://ex.invalid/a"),
         rdflib.URIRef("https://ex.invalid/p"), rdflib.Literal("one")),
    ]
    first = vendoring.serialise(triples, ["h"])
    second = vendoring.serialise(list(reversed(triples)) + triples, ["h"])
    assert first == second


def test_a_blank_node_reaching_the_serialiser_is_refused(vendoring):
    """It cannot happen by construction, which is exactly why the guard
    is here: the construction is what would change."""
    import rdflib

    with pytest.raises(SystemExit):
        vendoring.serialise(
            [(rdflib.URIRef("https://ex.invalid/a"),
              rdflib.URIRef("https://ex.invalid/p"), rdflib.BNode())], ["h"])


def test_the_serialiser_prefixes_come_from_the_pins(vendoring):
    """Every pinned namespace is abbreviated in the extracts. A prefix
    list kept by hand would have written BPO's IRIs out longhand the day
    it was added, and nothing would have said so."""
    declared = dict(vendoring.prefixes())
    for entry in vendoring.sources():
        assert declared[entry["prefix"]] == entry["namespace"], entry["id"]


# ------------------------------------------------------------- scope


def test_the_extracts_are_not_counted_as_this_repository_ontology(layout):
    """A vendored file in `ontology_files()` would put third-party triples
    into the corpus digest, and the digest would then move whenever an
    upstream pin changed."""
    authored = {p.as_posix() for p in layout.ontology_files()}
    vendored = {p.as_posix() for p in layout.vendored_files()}
    assert vendored
    assert not (authored & vendored)


def test_the_corpus_digest_does_not_measure_the_vendored_extracts():
    digest = load_tool("bco_digest_scope",
                       "tools/ontology/corpus_digest.py").measure()
    assert not [p for p in digest["scope"]["paths"] if p.startswith("vendor/")]
