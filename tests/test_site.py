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
        builder.term_records([source], graph, ns, [("bco", ns)])
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
        builder.term_records([source], graph, ns, [("bco", ns)])
    assert "rdfs:label values tagged en" in str(error.value)


# --------------------------------------------------- text is not markup


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
