# SPDX-License-Identifier: MIT
"""The public site: built deterministically, checked, and able to fail.

The site is what an external validator sees instead of the repository, so
the questions are the repository's own, asked of the artifact: is every
figure derived rather than typed, does every link resolve on a subpath,
does ontology text stay text, and is what was built what gets deployed.
The Pages workflow builds twice and compares; this suite does the same,
and then breaks the checker's inputs one at a time to show it notices.
"""

from __future__ import annotations

import json
import re
import shutil
import zipfile
from pathlib import Path

import pytest

from conftest import load_tool


@pytest.fixture(scope="module")
def builder():
    return load_tool("bco_build_site", "tools/site/build_site.py")


@pytest.fixture(scope="module")
def checker():
    return load_tool("bco_check_site", "tools/site/check_site.py")


@pytest.fixture(scope="module")
def built(builder, tmp_path_factory):
    """One build, shared. Never the working `_site/`: a test that read the
    developer's last build would pass or fail on whether they had built."""
    out = tmp_path_factory.mktemp("site") / "_site"
    written = builder.build(out)
    return out, written


@pytest.fixture
def copy(built, tmp_path):
    """A disposable copy for tests that damage the artifact."""
    out, _ = built
    target = tmp_path / "_site"
    shutil.copytree(out, target)
    return target


def terms(out):
    return json.loads((out / "data/terms.json").read_text(encoding="utf-8"))


# ------------------------------------------------------------ the build


def test_two_builds_of_one_commit_are_identical(builder, built, tmp_path):
    """The only way to tell a deployment matches its commit is to rebuild
    and compare, and that only works if the build is deterministic."""
    _, first = built
    second = builder.build(tmp_path / "again")
    assert first == second
    assert builder.tree_digest(first) == builder.tree_digest(second)


def test_the_built_site_passes_its_own_check(checker, built):
    out, _ = built
    assert checker.check(out) == []


def test_every_navigation_entry_is_a_page(built, repo):
    out, _ = built
    site = json.loads((repo / "site/content/site.json")
                      .read_text(encoding="utf-8"))
    for item in site["navigation"]:
        assert (out / (item["path"] + "index.html")).is_file(), item


def test_downloads_are_the_repository_bytes(built, repo):
    """Copied, never re-serialised: a re-serialised file says the same
    thing and hashes differently, and its checksum would describe the
    serialiser."""
    out, _ = built
    manifest = json.loads((out / "data/downloads.json")
                          .read_text(encoding="utf-8"))
    for row in manifest["authored"] + manifest["upstream"]:
        sub = "downloads/" if row["origin"] == "authored" \
            else "downloads/upstream/"
        assert (out / sub / row["file"]).read_bytes() == \
            (repo / row["path"]).read_bytes(), row["file"]
    assert len(manifest["upstream"]) == 3


def test_the_bundle_holds_authored_files_only(built):
    """Upstream extracts are somebody else's and are offered separately,
    under their own licences -- not packed into an archive that carries
    this repository's LICENSE."""
    out, _ = built
    with zipfile.ZipFile(out / "downloads/bco-ontology.zip") as archive:
        names = archive.namelist()
    assert "bco/LICENSE" in names and "bco/SHA256SUMS" in names
    assert not [n for n in names if "extract" in n], names
    assert "bco/apqc-cap.ttl" in names


def test_a_crlf_source_file_stops_the_build(builder, tmp_path):
    """The guard behind cross-machine determinism. CRLF in the working tree
    -- from core.autocrlf=true, or from Python's write_text on Windows --
    made a local build publish six files that differed from CI's under the
    same commit."""
    lf = tmp_path / "lf.css"
    crlf = tmp_path / "crlf.css"
    lf.write_bytes(b"a {}\nb {}\n")
    crlf.write_bytes(b"a {}\r\nb {}\r\n")
    assert lf.read_bytes() != crlf.read_bytes()
    assert builder.source_bytes(lf) == b"a {}\nb {}\n"
    with pytest.raises(SystemExit) as error:
        builder.source_bytes(crlf)
    assert "CRLF" in str(error.value)


# ------------------------------------------------------- the term index


def test_the_index_holds_every_upstream_term_and_marks_it(built):
    out, _ = built
    index = terms(out)
    upstream = [r for r in index["classes"] if r["origin"] == "upstream"]
    assert len(upstream) >= 70, len(upstream)
    assert {r["module"] for r in upstream} == {"bfo", "cco", "bpo"}
    assert index["counts"]["authored"] == len(
        [r for r in index["classes"] if r["origin"] == "authored"])


def test_category_comes_from_the_hierarchy(built):
    """Act of Acquisition is a process because BPO puts it under a CCO act
    that CCO puts under BFO process -- not because of its name."""
    out, _ = built
    by_id = {r["id"]: r for r in terms(out)["classes"]}
    assert by_id["ex:ActOfAcquisition"]["category"] == "process"
    assert by_id["cco:ont00001180"]["category"] == "material entity"
    assert by_id["cco:ont00000568"]["category"] == "realizable entity", (
        "Organization Capability reaches realizable entity, not "
        "disposition, in CCO v2.0; the site must say what the extract says")


def test_an_authored_term_without_a_definition_stops_the_build(builder):
    """No fallback and no allowlist: a BCO term with no definition is a
    question for whoever wrote it, not something the site papers over."""
    import rdflib

    ns = "https://fandaws.com/ontology/bco#"
    graph = rdflib.Graph()
    graph.parse(data=("@prefix owl: <http://www.w3.org/2002/07/owl#> .\n"
                      "@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\n"
                      "<%sX> a owl:Class ; rdfs:label \"X\" .\n" % ns),
                format="turtle")
    source = {"key": "m", "path": "m.ttl", "graph": graph,
              "origin": "authored"}
    with pytest.raises(SystemExit) as error:
        builder.term_records([source], graph, (ns,), [("bco", ns)])
    assert "no skos:definition" in str(error.value)


def test_two_labels_in_one_language_stop_the_build(builder):
    import rdflib

    ns = "https://fandaws.com/ontology/bco#"
    graph = rdflib.Graph()
    graph.parse(data=("@prefix owl: <http://www.w3.org/2002/07/owl#> .\n"
                      "@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\n"
                      "@prefix skos: <http://www.w3.org/2004/02/skos/core#> .\n"
                      "<%sX> a owl:Class ; rdfs:label \"A\"@en, \"B\"@en ;\n"
                      "  skos:definition \"d\" .\n" % ns), format="turtle")
    source = {"key": "m", "path": "m.ttl", "graph": graph,
              "origin": "authored"}
    with pytest.raises(SystemExit) as error:
        builder.term_records([source], graph, (ns,), [("bco", ns)])
    assert "rdfs:label values tagged en" in str(error.value)


# ------------------------------------------------------- the vocabulary


VOCAB_PREFIXES = """\
@prefix rdf:     <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs:    <http://www.w3.org/2000/01/rdf-schema#> .
@prefix skos:    <http://www.w3.org/2004/02/skos/core#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix prov:    <http://www.w3.org/ns/prov#> .
@prefix xsd:     <http://www.w3.org/2001/XMLSchema#> .
@prefix bco:     <https://fandaws.com/ontology/bco#> .
@prefix bcom:    <https://fandaws.com/ontology/bco-metamodel#> .
@prefix bcoc:    <https://fandaws.com/ontology/bco-catalog#> .
@prefix bcos:    <https://fandaws.com/ontology/bco-sources#> .
@prefix bcoa:    <https://fandaws.com/ontology/bco-agents#> .
"""

#: Two schemes, two agents and two register records, as the generated
#: Turtle has them -- and no concept.
VOCAB_BASE = VOCAB_PREFIXES + """\
bcom:MetamodelScheme a skos:ConceptScheme ;
    skos:prefLabel "BCO metamodel scheme"@en ;
    skos:definition "The terms specification section 4 defines."@en .
bcoc:CapabilityCatalogScheme a skos:ConceptScheme ;
    skos:prefLabel "BCO capability catalog scheme"@en ;
    skos:definition "The business capabilities the BCO catalogues."@en .
bcoa:person a prov:Agent , prov:Person ; rdfs:label "A <em>Person</em>"@en .
bcoa:software a prov:Agent , prov:SoftwareAgent ;
    rdfs:label "Software"@en ; bco:modelIdentifier "model-x" ;
    prov:actedOnBehalfOf bcoa:person .
bcos:SRC-OMG-03 a dcterms:BibliographicResource ;
    dcterms:identifier "SRC-OMG-03" ;
    dcterms:bibliographicCitation "Cited <i>work</i> & co" ;
    bco:hasClaim bcos:SRC-OMG-03-claim-1 .
bcos:SRC-OMG-03-claim-1 bco:claimIndex "1"^^xsd:integer ;
    bco:claimStatus "<b>V</b>" .
bcos:SRC-OMG-04 a dcterms:BibliographicResource ;
    dcterms:identifier "SRC-OMG-04" ;
    dcterms:bibliographicCitation "UNCITED-REGISTER-ENTRY" ;
    bco:hasClaim bcos:SRC-OMG-04-claim-1 .
bcos:SRC-OMG-04-claim-1 bco:claimIndex "1"^^xsd:integer ;
    bco:claimStatus "V" .
"""

#: One catalog concept whose every displayed field carries markup.
VOCAB_CONCEPT = """\
bcoc:Treasury a skos:Concept ;
    skos:inScheme bcoc:CapabilityCatalogScheme ;
    skos:prefLabel "<b>Treasury</b> & Co"@en , "Tresorerie"@fr ;
    skos:definition "Manages <script>alert(1)</script> cash."@en ;
    skos:notation "10002"^^bco:PCFCode ;
    bco:lifecycleStatus "Draft" ;
    bco:designatesClass bco:TreasuryCapability ;
    bco:definitionGenus bco:BusinessCapability ;
    bco:foundationalAncestor bco:SomeAncestor ;
    prov:wasAttributedTo bcoa:software ;
    bco:sourceReference bcoc:source-1 , bcoc:source-2 .
bcoc:source-2 bco:citesSource bcos:SRC-OMG-03 ;
    bco:locator "section 9" ;
    bco:relation "consistent-with" ;
    bco:support "<i>contextual</i>" .
bcoc:source-1 bco:citesSource bcos:SRC-OMG-03 ;
    bco:locator "section \\"7\\" <b>2</b>" ;
    bco:relation "departs-from" ;
    bco:departureNote "Organization <u>only</u>."@en ;
    bco:citesClaim bcos:SRC-OMG-03-claim-1 .
"""


def vocabulary_page(builder, validator, turtle, notice="EMPTY-NOTICE"):
    import rdflib

    graph = rdflib.Graph()
    graph.parse(data=turtle, format="turtle")
    namespaces = validator.AUTHORED_NAMESPACES
    known = builder.prefixes(builder.authored_prefixes(namespaces, [graph]))
    values = builder.vocabulary_values(graph, namespaces, known, notice)
    return "\n".join(values[key] for key in sorted(values))


@pytest.fixture(scope="module")
def validator():
    return load_tool("bco_validate_site", "tools/ontology/validate.py")


def test_the_vocabulary_page_is_built_and_in_the_navigation(built, repo):
    """A page no navigation entry reaches is refused by the build; this is
    the other direction -- the entry exists and every page links to it."""
    out, _ = built
    site = json.loads((repo / "site/content/site.json")
                      .read_text(encoding="utf-8"))
    entries = [i for i in site["navigation"] if i["key"] == "vocabulary"]
    assert entries == [{"key": "vocabulary", "label": "Vocabulary",
                        "path": "vocabulary/"}], entries
    page = (out / "vocabulary/index.html").read_text(encoding="utf-8")
    assert "<h1>Vocabulary</h1>" in page
    assert 'href="../vocabulary/" aria-current="page"' in page
    for other in ("index.html", "modules/index.html", "status/index.html"):
        text = (out / other).read_text(encoding="utf-8")
        assert re.search(r'href="(\.\./)?vocabulary/"', text), other


def test_the_real_vocabulary_page_matches_the_real_vocabulary(built, repo,
                                                              layout):
    """Read from the generated Turtle: both schemes and both declared
    agents appear, and the empty-state notice shows exactly while no
    concept exists. Since P5 there are concepts, so the notice is gone,
    and every concept's English label and every register entry a concept
    cites is on the page."""
    import html
    import rdflib

    out, _ = built
    page = (out / "vocabulary/index.html").read_text(encoding="utf-8")
    graph = rdflib.Graph()
    for path in layout.vocabulary_files():
        graph.parse(path, format="turtle")
    skos = "http://www.w3.org/2004/02/skos/core#"
    bco = "https://fandaws.com/ontology/bco#"
    concepts = set(graph.subjects(rdflib.RDF.type,
                                  rdflib.URIRef(skos + "Concept")))
    notice = json.loads((repo / "site/content/site.json").read_text(
        encoding="utf-8"))["notices"]["vocabulary_empty"]["text"]
    for needle in ("BCO metamodel scheme", "BCO capability catalog scheme",
                   "bcoa:aaron-damiano", "bcoa:claude-opus-5-5",
                   "https://fandaws.com/ontology/bco-sources#"):
        assert needle in page, needle
    assert (notice in page) == (not concepts), (len(concepts), notice)

    assert len(concepts) == 14, len(concepts)
    for concept in concepts:
        labels = [str(o) for o in graph.objects(
            concept, rdflib.URIRef(skos + "prefLabel"))
            if getattr(o, "language", None) == "en"]
        assert len(labels) == 1, (concept, labels)
        assert html.escape(labels[0], quote=True) in page, labels[0]
    cited = {str(o).rsplit("#", 1)[1] for o in graph.objects(
        None, rdflib.URIRef(bco + "citesSource"))}
    assert cited, "no concept cites a source"
    for src in cited:
        assert "<code>%s</code>" % src in page, src
    # Review R7, A: every cited claim appears with its index and status.
    claims = set(graph.objects(None, rdflib.URIRef(bco + "citesClaim")))
    assert claims, "no departs-from cites a claim"
    for claim in claims:
        index = graph.value(claim, rdflib.URIRef(bco + "claimIndex"))
        status = graph.value(claim, rdflib.URIRef(bco + "claimStatus"))
        assert "claim %s, status %s" % (index, status) in page, claim
    # Review R7, E: the genus and the ancestor of each catalog concept.
    assert page.count("<dt>Genus</dt>") == 5, page.count("<dt>Genus</dt>")
    assert page.count("<dt>Foundational ancestor</dt>") == 5


def test_the_empty_state_shows_when_there_are_no_concepts(builder,
                                                          validator):
    page = vocabulary_page(builder, validator, VOCAB_BASE)
    assert "EMPTY-NOTICE" in page
    assert "No concept cites a source yet" in page
    # The register is not published: an uncited record stays off the page.
    assert "UNCITED-REGISTER-ENTRY" not in page


def test_a_constructed_concept_renders_every_field_escaped(builder,
                                                           validator):
    """One concept, every field carrying markup: each arrives as text, and
    none of it as markup. The cited source's citation is shown, the
    uncited one is not, and the empty-state notice is gone."""
    page = vocabulary_page(builder, validator, VOCAB_BASE + VOCAB_CONCEPT)
    assert "EMPTY-NOTICE" not in page
    for raw in ("<b>Treasury</b>", "<script>", "<i>work</i>", "<u>only</u>",
                "<b>V</b>",
                "<i>contextual</i>",
                "<em>Person</em>", "<b>2</b>"):
        assert raw not in page, raw
    for escaped in ("&lt;b&gt;Treasury&lt;/b&gt; &amp; Co",
                    "Manages &lt;script&gt;alert(1)&lt;/script&gt; cash.",
                    "Tresorerie (fr)", "<dd>Draft</dd>",
                    "<code>10002</code>",
                    "<code>bco:TreasuryCapability</code>",
                    "<code>SRC-OMG-03</code> &mdash; departs-from &mdash; "
                    "section &quot;7&quot; &lt;b&gt;2&lt;/b&gt; &mdash; "
                    "claim 1, status &lt;b&gt;V&lt;/b&gt; &mdash; "
                    "Organization &lt;u&gt;only&lt;/u&gt;.",
                    "<dt>Genus</dt>",
                    "<code>bco:BusinessCapability</code>",
                    "<dt>Foundational ancestor</dt>",
                    "<code>bco:SomeAncestor</code>",
                    "<code>SRC-OMG-03</code> &mdash; consistent-with "
                    "(&lt;i&gt;contextual&lt;/i&gt;) &mdash; section 9",
                    "Cited &lt;i&gt;work&lt;/i&gt; &amp; co",
                    "Software (<code>bcoa:software</code>)",
                    "A &lt;em&gt;Person&lt;/em&gt;"):
        assert escaped in page, escaped
    assert "UNCITED-REGISTER-ENTRY" not in page


def test_a_concept_in_no_scheme_stops_the_build(builder, validator):
    """Where it would be listed is a question for the vocabulary, not a
    choice the page makes by traversal order."""
    unplaced = VOCAB_CONCEPT.replace(
        "    skos:inScheme bcoc:CapabilityCatalogScheme ;\n", "")
    assert unplaced != VOCAB_CONCEPT
    with pytest.raises(SystemExit) as error:
        vocabulary_page(builder, validator, VOCAB_BASE + unplaced)
    assert "scheme" in str(error.value)


def test_the_site_build_reads_no_vocabulary_yaml(builder, repo, tmp_path,
                                                 monkeypatch):
    """The page is the generated Turtle's, never the authored YAML's.

    Every file the build opens is recorded. The generated Turtle must be
    among them -- otherwise this would pass for a build that read nothing
    -- and no YAML under src/01_controlled_vocabulary/, nor the register YAML the source records
    are generated from, may be.
    """
    import builtins
    import io

    opened = []
    real_open = io.open

    def recording(file, *args, **kwargs):
        try:
            opened.append(Path(file).resolve())
        except TypeError:
            pass
        return real_open(file, *args, **kwargs)

    monkeypatch.setattr(io, "open", recording)
    monkeypatch.setattr(builtins, "open", recording)
    builder.build(tmp_path / "_site")
    monkeypatch.undo()

    root = repo.resolve()
    relative = {p.relative_to(root).as_posix() for p in opened
                if p.is_relative_to(root)}
    generated = {r for r in relative if r.startswith("src/01_controlled_vocabulary/generated/")
                 and r.endswith(".ttl")}
    assert len(generated) == 5, sorted(relative)[:40]
    yaml_read = sorted(r for r in relative
                       if (r.startswith("src/01_controlled_vocabulary/") and r.endswith(".yaml"))
                       or r == "docs/sources/register.yaml")
    assert yaml_read == [], yaml_read


# --------------------------------------------------- text is not markup


# ------------------------------------------------------------ reviews


def test_every_review_is_on_the_reviews_page(built, repo):
    """Every reviews/*.md, each under its own section, in sorted order,
    with its own source digest -- and the navigation says Reviews."""
    import hashlib

    out, _ = built
    page = (out / "review/index.html").read_text(encoding="utf-8")
    site = json.loads((repo / "site/content/site.json")
                      .read_text(encoding="utf-8"))
    assert {"key": "review", "label": "Reviews",
            "path": "review/"} in site["navigation"]
    assert "<h1>Reviews</h1>" in page
    files = sorted((repo / "reviews").glob("*.md"))
    assert len(files) >= 2, files
    positions = []
    for path in files:
        number, _, rest = path.stem.partition("-")
        tag = number.lower() + ("-disposition" if rest == "disposition"
                                else "")
        marker = 'id="review-%s"' % tag
        assert page.count(marker) == 1, marker
        positions.append(page.index(marker))
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        assert "<code>%s</code>" % digest in page, path.name
    # Reviews in number order, each disposition right after its review.
    order = sorted(positions)
    assert page.index('id="review-r5"') < page.index('id="review-r6"') \
        < page.index('id="review-r6-disposition"'), order


def test_the_r6_disposition_is_rendered_as_accepted(built):
    """Rendered, not excluded, and labelled with the status its own Status
    row states. The label was a hard-coded "(proposed)" and went on saying
    so after the architect accepted R6's disposition on 2026-10-24."""
    out, _ = built
    page = (out / "review/index.html").read_text(encoding="utf-8")
    assert "Disposition of R6 (accepted)" in page
    assert "Disposition of R6 (proposed)" not in page
    assert "2026-10-24-r6-response-accepted.md" in page


def _review_pair(tmp_path, status_row):
    review = tmp_path / "R9-some-review.md"
    review.write_bytes(b"# A review\n\nText.\n")
    disposition = tmp_path / "R9-disposition.md"
    rows = "| Field | Value |\n| --- | --- |\n" + status_row
    disposition.write_bytes(("# Disposition\n\n" + rows).encode("utf-8"))
    return [review, disposition]


@pytest.mark.parametrize("row, label", [
    ("| Status | Proposed by the agent, 2026-11-01 |\n", "(proposed)"),
    ("| Status | Accepted 2026-11-02 by the architect |\n", "(accepted)"),
])
def test_the_disposition_label_is_read_from_its_status_row(builder, tmp_path,
                                                            monkeypatch, row,
                                                            label):
    monkeypatch.setattr(builder, "relative", lambda path: path.name)
    ctx = {"repository": "https://example.invalid/repo", "commit": "0" * 40}
    values = builder.reviews_values(ctx, _review_pair(tmp_path, row))
    page = "".join(values.values())
    assert "Disposition of R9 %s" % label in page


@pytest.mark.parametrize("row", [
    "",                                        # no Status row
    "| Status | Pending review |\n",           # neither word
    "| Status | Proposedly |\n",               # not the word itself
    "| Status | Proposed |\n| Status | Accepted |\n",   # says both
])
def test_a_disposition_without_one_clear_status_is_refused(builder, tmp_path,
                                                            monkeypatch, row):
    monkeypatch.setattr(builder, "relative", lambda path: path.name)
    ctx = {"repository": "https://example.invalid/repo", "commit": "0" * 40}
    with pytest.raises(SystemExit) as error:
        builder.reviews_values(ctx, _review_pair(tmp_path, row))
    assert "Status rows" in str(error.value)


def test_the_status_page_counts_the_vocabulary_it_validates(built, repo):
    """The count is the SKOS concepts in the generated vocabulary, read from
    the Turtle -- the population the vocabulary and wellformedness rungs
    check. It said "Authored terms checked: 0" for a day after 14 concepts
    entered the validation scope, because it counted ontology terms only."""
    import rdflib

    graph = rdflib.Graph()
    for path in sorted((repo / "src/01_controlled_vocabulary/generated").glob("*.ttl")):
        graph.parse(path, format="turtle")
    concept = rdflib.URIRef("http://www.w3.org/2004/02/skos/core#Concept")
    expected = len(set(graph.subjects(rdflib.RDF.type, concept)))
    assert expected >= 14, expected

    out, _ = built
    page = (out / "status/index.html").read_text(encoding="utf-8")
    assert ("<dt>Vocabulary concepts checked</dt><dd>%d</dd>" % expected
            in page), "the Status page does not show the vocabulary count"
    assert "<dt>Ontology terms checked</dt>" in page
    assert "Authored terms checked" not in page
    assert "every shape set conforms vacuously" not in page
    assert "check the %d vocabulary concept(s)" % expected in page


def test_ids_on_the_reviews_page_are_unique_and_prefixed(built):
    """Every id once, and every heading id inside a section carries that
    section's prefix -- so "Summary" in two reviews cannot collide."""
    out, _ = built
    page = (out / "review/index.html").read_text(encoding="utf-8")
    ids = re.findall(r'\sid="([^"]*)"', page)
    assert len(ids) == len(set(ids)), sorted(
        i for i in set(ids) if ids.count(i) > 1)
    sections = re.findall(r'<section class="review" id="review-([^"]+)">'
                          r"(.*?)</section>", page, flags=re.S)
    assert len(sections) >= 3, len(sections)
    for tag, body in sections:
        headings = re.findall(r'<h[3-6] id="([^"]+)"', body)
        assert headings, tag
        for heading in headings:
            assert heading.startswith(tag + "-"), (tag, heading)
            # and no other section's prefix is a longer match
            others = [t for t, _ in sections
                      if t != tag and heading.startswith(t + "-")
                      and len(t) > len(tag)]
            assert not others, (tag, heading, others)


def write_reviews(tmp_path, files):
    paths = []
    for name, text in files.items():
        path = tmp_path / name
        path.write_bytes(text.encode("utf-8"))
        paths.append(path)
    return paths


@pytest.fixture
def review_ctx(builder, monkeypatch):
    """reviews_values on files outside the repository: source links need
    a repository-relative path, so the name stands in for it."""
    monkeypatch.setattr(builder, "relative", lambda path: path.name)
    return {"repository": "https://example.invalid/repo", "commit": "0" * 40}


def test_two_reviews_with_the_same_headings_get_distinct_ids(
        builder, review_ctx, tmp_path):
    same = "# A review\n\n## Summary\n\nText.\n"
    values = builder.reviews_values(review_ctx, write_reviews(tmp_path, {
        "R1-first.md": same, "R2-second.md": same}))
    body = values["reviews_body"]
    for expected in ('id="r1-summary"', 'id="r2-summary"',
                     'id="review-r1"', 'id="review-r2"'):
        assert body.count(expected) == 1, expected
    # Without the prefix, both would have been "summary".
    plain, _ = builder.render_markdown(same)
    assert 'id="summary"' in plain


@pytest.mark.parametrize("files, needle", [
    # The disposition states its status, so the collision is what is
    # refused -- without the row it would be refused for that instead and
    # this case would stop testing ids.
    ({"R1-review.md": "# A\n\n## Disposition x\n",
      "R1-disposition.md": "# B\n\n| Status | Proposed |\n\n## x\n"},
     "more than once"),
    ({"R1-review.md": "# A\n", "R2-disposition.md": "# B\n"},
     "answers no review"),
    ({"notes.md": "# A\n"}, "not named R<n>"),
    ({"R1-review.md": "# A\n", "R1-other.md": "# B\n"}, "claim R1"),
], ids=["colliding-ids", "orphan-disposition", "misnamed", "same-number"])
def test_the_reviews_page_refuses_what_it_cannot_place(
        builder, review_ctx, tmp_path, files, needle):
    with pytest.raises(SystemExit) as error:
        builder.reviews_values(review_ctx, write_reviews(tmp_path, files))
    assert needle in str(error.value), str(error.value)


def test_raw_html_in_a_document_is_shown_not_run(builder):
    body, _ = builder.render_markdown(
        "Text <script>alert(1)</script> and `<Filler>`.\n\n<div>raw</div>")
    assert "<script>" not in body and "<div>" not in body
    assert "&lt;script&gt;" in body and "&lt;Filler&gt;" in body


def test_the_explorer_never_writes_markup(repo):
    """Ontology text reaches the page through textContent only. Looked for
    as an assignment, not as a word: the file's own comment says "never
    innerHTML", and a scan for the bare word would fail on the rule's
    explanation."""
    for name in ("explorer.js", "ranking.js"):
        text = (repo / "site/src/assets/js" / name).read_text(
            encoding="utf-8")
        assert not re.search(r"\.(innerHTML|outerHTML)\s*[+]?=", text), name
        assert "insertAdjacentHTML" not in text, name
        assert "document.write" not in text, name


def test_the_specification_is_rendered_whole(built, repo):
    """Every heading in the Markdown arrives on the page, as a heading one
    level down -- the page owns the only <h1>."""
    out, _ = built
    source = (repo / "specifications/"
              "Business-Capability-Ontology-v0.4.0-draft.1.md").read_text(
        encoding="utf-8")
    page = (out / "specification/index.html").read_text(encoding="utf-8")
    # Fenced code first: the spec's Turtle examples carry `# ...` comment
    # lines, and counting those as headings is the scan-finds-the-comment
    # trap. The first version of this test fell into it (21 against 18).
    prose = re.sub(r"^```.*?^```", "", source, flags=re.M | re.S)
    headings = re.findall(r"^#{1,4} ", prose, flags=re.M)
    assert len(headings) >= 15, len(headings)
    assert page.count("<h1") == 1
    assert len(re.findall(r"<h[2-5] id=", page)) >= len(headings)
    assert "nothing in it is normative" in page


# ------------------------------------------------ the checker can fail


def damage(path, old, new):
    text = path.read_text(encoding="utf-8")
    assert old in text, (path.name, old[:60])
    changed = text.replace(old, new, 1)
    assert changed != text
    path.write_text(changed, encoding="utf-8")


@pytest.mark.parametrize("page, old, new, expect", [
    ("modules/index.html", 'href="../assets/css/site.css"',
     'href="https://cdn.invalid/site.css"', "from another origin"),
    ("modules/index.html", 'href="../downloads/"',
     'href="../downloadz/"', "resolves to nothing"),
    ("modules/index.html", 'href="../downloads/"',
     'href="/downloads/"', "root-absolute"),
    ("modules/index.html", "</main>",
     "<script>alert(1)</script></main>", "inline script"),
    ("modules/index.html", "<h2>", "<h1>x</h1><h2>", "<h1> elements"),
    ("modules/index.html", '<main id="main"',
     '<main onclick="x()" id="main"', "event handler"),
    ("specification/index.html", 'href="#', 'href="#no-such-', "fragment"),
    ("review/index.html", 'id="review-r5"', 'id="review-r6"',
     "id used more than once"),
])
def test_the_checker_refuses_each_kind_of_damage(checker, copy, page, old,
                                                 new, expect):
    """Each refusal, falsified on a real artifact. A checker that passed
    the clean build and also passed these would be checking nothing."""
    damage(copy / page, old, new)
    problems = checker.check(copy)
    assert any(expect in p for p in problems), problems


def test_the_checker_notices_a_tampered_download(checker, copy):
    target = copy / "downloads/apqc-cap.ttl"
    original = target.read_bytes()
    target.write_bytes(original + b"\n# tampered\n")
    assert target.read_bytes() != original
    problems = checker.check(copy)
    assert any("apqc-cap.ttl does not match" in p for p in problems), problems


# ------------------------------------------------------- conceptual models


@pytest.fixture(scope="module")
def models_checker():
    return load_tool("bco_site_test_check_models",
                     "tools/conceptual/check_models.py")


@pytest.fixture(scope="module")
def vendor_tool():
    return load_tool("bco_site_test_vendor_assets",
                     "tools/site/vendor_assets.py")


MERMAID_SOURCE = ('flowchart LR\n  A["Maker <b>&</b>"] -->|makes| B(["Widget"])'
                  '\n  C{{"Know-how"}}\n  A -.->|holds| C')


def test_the_models_page_is_built_after_vocabulary(built, repo):
    out, _ = built
    site = json.loads((repo / "site/content/site.json")
                      .read_text(encoding="utf-8"))
    keys = [i["key"] for i in site["navigation"]]
    assert {"key": "models", "label": "Models",
            "path": "models/"} in site["navigation"]
    assert keys.index("models") == keys.index("vocabulary") + 1, keys
    page = (out / "models/index.html").read_text(encoding="utf-8")
    assert "<h1>Conceptual models</h1>" in page
    assert 'href="../models/" aria-current="page"' in page
    # The curated note: words in site.json, not counts.
    assert esc_in(site["notices"]["models"]["text"], page)


def esc_in(text, page):
    import html
    return html.escape(text) in page


def test_a_mermaid_block_renders_as_escaped_pre(builder):
    """The diagram's source stays text: escaped inside pre.mermaid, so with
    JavaScript off the reader sees the Mermaid source, and markup in a
    label is never markup."""
    import html

    text = "Before.\n\n```mermaid\n%s\n```\n\nAfter.\n" % MERMAID_SOURCE
    body, _ = builder.render_markdown(text, mermaid=True)
    blocks = re.findall(r'<pre class="mermaid">(.*?)</pre>', body, re.S)
    assert len(blocks) == 1, body
    assert "<b>" not in blocks[0] and "&lt;b&gt;" in blocks[0]
    assert "language-mermaid" not in body
    assert html.unescape(blocks[0]).strip() == MERMAID_SOURCE
    # Off by default: no other page gets an element it has no script for.
    plain, _ = builder.render_markdown(text)
    assert 'class="mermaid"' not in plain
    assert 'class="language-mermaid"' in plain


def write_model(tmp_path, approved: str, name="CM-77-test-model.md"):
    text = ("# CM-77 — A Test Model\n\n| Field | Value |\n| --- | --- |\n"
            "| Model identifier | CM-77 |\n| Title | A Test Model |\n"
            "| Version | 9.9.9 |\n| Status | Draft |\n\n"
            "## 1. Scope and purpose\n\nText.\n\n## 3. Patterns\n\n"
            "### P1 — One\n\n```mermaid\n%s\n```\n\n"
            "**Reading the diagram.** Text.\n\n## 10. Review status\n\n"
            "| Item | State |\n| --- | --- |\n| Approved | %s |\n"
            % (MERMAID_SOURCE, approved))
    path = tmp_path / name
    path.write_bytes(text.encode("utf-8"))
    return path


@pytest.mark.parametrize("approved, shown, absent", [
    ("no", "Not approved", "Approved &mdash; record"),
    ("`docs/decisions/2026-10-25-stage-02-choices.md`",
     "Approved &mdash; record", "Not approved"),
], ids=["not-approved", "approved"])
def test_the_approval_state_is_read_from_the_model(builder, models_checker,
                                                   review_ctx, tmp_path,
                                                   approved, shown, absent):
    """Read from the model's own section 10 Review status table, through
    the checker's reader -- never typed into site/."""
    values = builder.models_values(
        review_ctx, [write_model(tmp_path, approved)], models_checker,
        "a notice", "no models")
    page = "".join(values.values())
    assert shown in page and absent not in page
    assert "CM-77 &mdash; A Test Model" in page
    assert "<dd>9.9.9</dd>" in page
    if approved != "no":
        assert "2026-10-25-stage-02-choices.md" in page
    # The hexagon's braces survive as character references, so fill()
    # cannot mistake them for a placeholder.
    assert "{{" not in page and "&#123;&#123;" in page
    assert 'id="model-cm-77"' in page and 'id="cm-77-' in page


def test_no_model_says_so(builder, models_checker, review_ctx):
    values = builder.models_values(review_ctx, [], models_checker,
                                   "a notice", "No model yet, on purpose.")
    page = "".join(values.values())
    assert "No model yet, on purpose." in page
    assert "a notice" not in page


def test_the_real_models_page_reads_each_model(built, repo, models_checker):
    out, _ = built
    page = (out / "models/index.html").read_text(encoding="utf-8")
    models = sorted((repo / "src/02_conceptual_models").glob("CM-*.md"))
    if not models:
        site = json.loads((repo / "site/content/site.json")
                          .read_text(encoding="utf-8"))
        assert esc_in(site["notices"]["models_empty"]["text"], page)
        return
    for path in models:
        record = models_checker.read_model(path)
        tag = record["identifier"].lower()
        assert page.count('id="model-%s"' % tag) == 1
        assert ("<dd>%s</dd>" % builder_esc(record["version"])) in page
        expected = ("Not approved" if record["approved"] == "no"
                    else "Approved &mdash; record")
        section = page[page.index('id="model-%s"' % tag):]
        assert expected in section[:4000], record
    assert page.count('<pre class="mermaid">') >= len(models)


def builder_esc(text):
    import html
    return html.escape(text)


def test_mermaid_loads_on_the_models_page_and_no_other(built):
    """2.5 MB of script on the one page with diagrams, and nowhere else;
    the bundle before the script that runs it."""
    out, _ = built
    for path in sorted(out.rglob("*.html")):
        page = path.read_text(encoding="utf-8")
        scripts = re.findall(r'<script src="([^"]+)"', page)
        rel = path.relative_to(out).as_posix()
        if rel == "models/index.html":
            assert scripts == ["../assets/vendor/mermaid/mermaid.min.js",
                               "../assets/js/models.js"], scripts
        else:
            assert not [s for s in scripts if "mermaid" in s
                        or "models.js" in s], (rel, scripts)


def test_the_served_bundle_is_the_pinned_bytes(built, repo, vendor_tool):
    """Copied from vendor/site/, not site/src/, and byte-identical to the
    pin -- with the licence beside it."""
    import hashlib

    out, _ = built
    for path, entry in vendor_tool.by_path(repo).items():
        served = out / entry["member"]["site_path"]
        assert served.read_bytes() == (repo / path).read_bytes(), path
        assert hashlib.sha256(served.read_bytes()).hexdigest() == \
            entry["member"]["sha256"]
    assert (out / "assets/vendor/mermaid/LICENSE").is_file()
    assert not (repo / "site/src/assets/vendor").exists()


def test_the_build_refuses_a_missing_or_altered_bundle(builder, repo,
                                                       tmp_path):
    """No Models page whose diagrams cannot render, and no unpinned bytes
    served under a pinned name."""
    (tmp_path / "config").mkdir()
    (tmp_path / "config/site-vendor.yaml").write_bytes(
        (repo / "config/site-vendor.yaml").read_bytes())
    with pytest.raises(SystemExit) as error:
        builder.vendored_site_files(tmp_path)
    assert "mermaid.min.js is missing" in str(error.value)
    assert "--fetch" in str(error.value)

    for name in ("mermaid.min.js", "LICENSE"):
        target = tmp_path / "vendor/site/mermaid" / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes((repo / "vendor/site/mermaid" / name).read_bytes())
    assert len(builder.vendored_site_files(tmp_path)) == 2
    bundle = tmp_path / "vendor/site/mermaid/mermaid.min.js"
    bundle.write_bytes(bundle.read_bytes() + b"\n// altered\n")
    with pytest.raises(SystemExit) as error:
        builder.vendored_site_files(tmp_path)
    assert "pinned sha256" in str(error.value)


def test_the_site_licence_notice_names_mermaid(built, repo):
    out, _ = built
    site = json.loads((repo / "site/content/site.json")
                      .read_text(encoding="utf-8"))
    assert "Mermaid (MIT)" in site["notices"]["license"]["text"]
    downloads = (out / "downloads/index.html").read_text(encoding="utf-8")
    assert "<h3>Mermaid 11.4.1</h3>" in downloads
    assert 'href="../assets/vendor/mermaid/LICENSE"' in downloads


# ---------------------------------------------------- vendored site assets


def test_the_vendored_assets_match_their_pins(vendor_tool, repo):
    problems, checked = vendor_tool.verify(repo)
    assert problems == [] and checked == 2, problems


def test_an_edited_vendored_asset_is_a_finding(vendor_tool, repo, tmp_path):
    for relative in ("config/site-vendor.yaml", "vendor/site/NOTICE.md",
                     "vendor/site/mermaid/LICENSE",
                     "vendor/site/mermaid/mermaid.min.js"):
        target = tmp_path / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes((repo / relative).read_bytes())
    assert vendor_tool.verify(tmp_path)[0] == []
    licence = tmp_path / "vendor/site/mermaid/LICENSE"
    licence.write_bytes(licence.read_bytes().replace(b"\n", b"\r\n"))
    notice = tmp_path / "vendor/site/NOTICE.md"
    notice.write_bytes(notice.read_bytes() + b"edited\n")
    problems, _ = vendor_tool.verify(tmp_path)
    assert any("LICENSE has sha256" in p for p in problems), problems
    assert any("NOTICE.md is not what" in p for p in problems), problems


def fake_tarball(members: dict) -> bytes:
    import io
    import tarfile

    buffer = io.BytesIO()
    with tarfile.open(fileobj=buffer, mode="w:gz") as archive:
        for name, data in members.items():
            info = tarfile.TarInfo(name)
            info.size = len(data)
            archive.addfile(info, io.BytesIO(data))
    return buffer.getvalue()


def test_extract_takes_only_pinned_members_and_checks_every_digest(
        vendor_tool):
    """Offline: a tarball built here, a pin computed for it. The pinned
    member is extracted; an unlisted member, even one aimed outside the
    vendor directory, is never written; and a wrong integrity or member
    digest is refused."""
    import hashlib

    tarball = fake_tarball({"package/dist/x.js": b"x();\n",
                            "../../escape.js": b"bad\n",
                            "package/other.js": b"other\n"})
    entry = {
        "id": "x", "integrity": vendor_tool.integrity_of(tarball),
        "shasum": hashlib.sha1(tarball).hexdigest(),
        "members": [{"member": "package/dist/x.js",
                     "path": "vendor/site/x/x.js",
                     "site_path": "assets/vendor/x/x.js",
                     "sha256": hashlib.sha256(b"x();\n").hexdigest()}]}
    assert vendor_tool.extract(entry, tarball) == {
        "vendor/site/x/x.js": b"x();\n"}

    wrong = dict(entry, integrity="sha512-AAAA")
    with pytest.raises(SystemExit) as error:
        vendor_tool.extract(wrong, tarball)
    assert "integrity" in str(error.value)

    member = dict(entry["members"][0], sha256="0" * 64)
    with pytest.raises(SystemExit) as error:
        vendor_tool.extract(dict(entry, members=[member]), tarball)
    assert "sha256" in str(error.value)


def test_fetch_refuses_any_host_but_the_registry(vendor_tool):
    with pytest.raises(SystemExit) as error:
        vendor_tool.download("https://cdn.invalid/mermaid.tgz")
    assert "refusing to fetch" in str(error.value)
