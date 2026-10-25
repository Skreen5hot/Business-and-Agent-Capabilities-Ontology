# SPDX-License-Identifier: MIT
"""Build the public site into _site/, deterministically.

    python tools/site/build_site.py              # into _site/
    python tools/site/build_site.py -o DIR       # somewhere else

The site exists for external validators: people who will read the
specification, look terms up, and download the files, without cloning the
repository or running anything. So it has to be easy to read and it has
to be right, and the second is the harder one: every title, count,
version, digest and licence on it is read from the repository at build
time, never typed into a page. site/content/site.json holds only the
words a person has to choose.

The method is BFO-Aligned ValueNet's (tools/site/build_site.py there),
rewritten for this repository rather than copied, because ValueNet's
builders depend on its own package for layout and parsing. What carries
over:

DETERMINISM

The site is deployed from an Actions artifact, not a committed tree, so
the only way to tell a deployment matches a commit is to rebuild it and
compare. So every input is enumerated in sorted order; the only
timestamp is the source commit's (or SOURCE_DATE_EPOCH), never now();
the output directory is emptied and rewritten, so a deleted source file
cannot survive into the artifact; and downloadable files are copied as
bytes, never re-serialised. The Pages workflow builds twice and requires
the two trees to be identical.

RELATIVE PATHS

The site is served from a project subpath
(/Business-and-Agent-Capabilities-Ontology/). A root-absolute
/assets/... works in local preview and 404s in production, so every
internal URL is relative, and tools/site/check_site.py resolves every one
against the built tree.

ONTOLOGY TEXT IS NEVER MARKUP

Every value read from a Turtle file or a pin reaches a page through
html.escape here, or through textContent in the explorer. The Markdown
documents -- the specification and every file under reviews/ -- are
rendered with raw-HTML passthrough removed, so a `<script>` in a
specification is shown as text, not run.

REFUSALS

An authored term with no label or no definition, or with two in one
language, stops the build: which one is published would otherwise be
decided by traversal order. Upstream terms are held to less -- a stub
is declared and labelled only -- but never more than one label. A
placeholder in a page that nothing fills, and an asset with a suffix no
rule covers, also stop it.
"""

from __future__ import annotations

import argparse
import hashlib
import html
import importlib.util
import io
import json
import os
import re
import subprocess
import sys
import zipfile
from pathlib import Path

_here = Path(__file__).resolve()
_root = next(p for p in (_here, *_here.parents)
             if (p / "config/repository-layout.yaml").is_file())
sys.path.insert(0, str(_root / "tools"))

import layout  # noqa: E402

OUTPUT = "_site"
PAGES = "site/pages"
ASSETS = "site/src"
CONTENT = "site/content/site.json"
PINS = "config/upstream-sources.yaml"
EXTRACTS = "config/upstream-extracts.json"
BASELINE = "config/validation-baseline.json"
BUNDLE_ROOT = "bco"
BUNDLE_NAME = "bco-ontology.zip"

#: Assets copied verbatim. Anything else under site/src/ is refused rather
#: than shipped or skipped: an artifact that deploys whatever it finds
#: cannot say what it deployed.
ALLOWED_ASSET_SUFFIXES = {".css", ".js"}

RDFS = "http://www.w3.org/2000/01/rdf-schema#"
OWL = "http://www.w3.org/2002/07/owl#"
SKOS = "http://www.w3.org/2004/02/skos/core#"
DCTERMS = "http://purl.org/dc/terms/"
RDF_TYPE = "http://www.w3.org/1999/02/22-rdf-syntax-ns#type"
OBO = "http://purl.obolibrary.org/obo/"
CCO = "https://www.commoncoreontologies.org/"

TERM_TYPES = {
    OWL + "Class": "class",
    OWL + "ObjectProperty": "property",
    OWL + "DatatypeProperty": "property",
    OWL + "AnnotationProperty": "property",
}

#: The category a class is shown under, decided by subClassOf closure to
#: these roots and nothing else -- never by a name ending in "Capability".
#: A class reaching two roots keeps the more specific (a disposition is
#: also a realizable entity); one reaching two unrelated roots is refused.
CATEGORY_ROOTS = {
    OBO + "BFO_0000016": "disposition",
    OBO + "BFO_0000023": "role",
    OBO + "BFO_0000017": "realizable entity",
    OBO + "BFO_0000015": "process",
    OBO + "BFO_0000040": "material entity",
    CCO + "ont00000958": "information content entity",
}

esc = html.escape


class Refused(SystemExit):
    """A question for whoever wrote the input, not for this build."""


# ------------------------------------------------------------- inputs


def git(*args: str) -> str:
    result = subprocess.run(["git", *args], cwd=str(_root),
                            capture_output=True)
    if result.returncode:
        raise Refused("git %s failed: %s" % (
            " ".join(args),
            result.stderr.decode("utf-8", "replace").strip()[-300:]))
    # Decoded explicitly: text=True would use cp1252 on Windows.
    return result.stdout.decode("utf-8").strip()


def stamp() -> tuple[str, int]:
    """The commit, and its own timestamp. Never now()."""
    commit = git("rev-parse", "HEAD")
    epoch = os.environ.get("SOURCE_DATE_EPOCH") or git(
        "log", "-1", "--format=%ct", commit)
    return commit, int(epoch)


def load_tool(name: str, relative: str):
    spec = importlib.util.spec_from_file_location(name, _root / relative)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def read_json(relative: str) -> dict:
    return json.loads((_root / relative).read_text(encoding="utf-8"))


def pins() -> list[dict]:
    import yaml

    raw = yaml.safe_load((_root / PINS).read_text(encoding="utf-8")) or {}
    return raw.get("sources") or []


def source_bytes(path: Path) -> bytes:
    """A file's bytes, refused if they carry CRLF.

    Every download is these bytes, so they have to be the bytes git
    publishes. .gitattributes pins LF in the index, but a checkout made
    with core.autocrlf=true -- the Windows default -- writes CRLF into the
    working tree, and a build there would publish different files from
    CI's under the same commit. That happened: the first deployment
    (9d89781) matched a Windows build of the same commit in 15 of 21
    files, and the other 6 were the CRLF stylesheet, scripts and LICENSE
    and the bundle and manifest built from them. Refusing here makes a
    local build either identical to CI's or a failure that names the file.
    """
    data = path.read_bytes()
    if b"\r\n" in data:
        try:
            name = relative(path)
        except ValueError:
            name = str(path)
        raise Refused(
            "%s has CRLF line endings in the working tree, so this build "
            "would publish different bytes from CI's. Rewrite it from the "
            "index (with no uncommitted change to it): delete it, then "
            "git checkout -- %s" % (name, name))
    return data


def relative(path: Path) -> str:
    return path.resolve().relative_to(_root.resolve()).as_posix()


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def parse(path: Path):
    """One Turtle file under a stable base.

    Never the filesystem path as base: a relative IRI would resolve
    against the checkout's location and the index would describe the
    machine that built it.
    """
    import rdflib

    graph = rdflib.Graph()
    graph.parse(data=path.read_text(encoding="utf-8"), format="turtle",
                publicID="https://fandaws.com/ontology/bco/base/"
                + path.name)
    return graph


# --------------------------------------------------------- term index


def literal(graph, subject, predicate: str, what: str, required: bool) -> str:
    """At most one value per language, preferring English then untagged.

    Two values in the language that would be published is a refusal: the
    choice would otherwise fall to whichever the graph yielded first.
    """
    import rdflib

    values = list(graph.objects(subject, rdflib.URIRef(predicate)))
    wrong = [v for v in values if not isinstance(v, rdflib.Literal)]
    if wrong:
        raise Refused("%s has a %s that is not a literal: %r"
                      % (subject, what, [str(w)[:60] for w in wrong]))
    for lang in ("en", None):
        chosen = sorted({str(v) for v in values if v.language == lang})
        if len(chosen) > 1:
            raise Refused(
                "%s has %d %s values tagged %s: %s. Which is published "
                "would depend on traversal order; this is a question for "
                "the ontology." % (subject, len(chosen), what,
                                   lang or "untagged",
                                   [c[:40] for c in chosen]))
        if chosen:
            return chosen[0]
    if required:
        raise Refused("%s has no %s. The site publishes what the ontology "
                      "asserts, with no fallback." % (subject, what))
    return ""


def prefixes(authored: list[tuple[str, str]]) -> list[tuple[str, str]]:
    """Pinned upstream prefixes plus the authored (prefix, namespace)
    pairs, longest namespace first so the most specific one wins."""
    found = [(entry["prefix"], entry["namespace"]) for entry in pins()]
    found.extend(authored)
    return sorted(found, key=lambda pair: (-len(pair[1]), pair[0]))


def authored_prefixes(namespaces, graphs) -> list[tuple[str, str]]:
    """(prefix, namespace) for each authored namespace, read from the
    @prefix bindings of the generated vocabulary Turtle -- which declares
    all five -- rather than typed here. A namespace the vocabulary binds
    to no prefix, or to two, is refused: the short ids on every page
    depend on it."""
    out = []
    for namespace in namespaces:
        bound = sorted({prefix for graph in graphs
                        for prefix, iri in graph.namespaces()
                        if str(iri) == namespace})
        if len(bound) != 1:
            raise Refused(
                "the generated vocabulary binds %s to %s; expected exactly "
                "one prefix" % (namespace, bound or "no prefix"))
        out.append((bound[0], namespace))
    return out


def short_id(iri: str, known: list[tuple[str, str]]) -> str:
    for prefix, namespace in known:
        if iri.startswith(namespace):
            return prefix + ":" + iri[len(namespace):]
    return iri


def category_of(iri: str, kind: str, merged) -> str:
    import rdflib

    if kind == "property":
        return "property"
    sub = rdflib.URIRef(RDFS + "subClassOf")
    ancestors = {str(a) for a in merged.transitive_objects(
        rdflib.URIRef(iri), sub)}
    reached = [root for root in CATEGORY_ROOTS if root in ancestors]
    # Keep only the most specific: drop a root that another reached root
    # is itself a subclass of.
    specific = [root for root in reached
                if not any(other != root and root in {
                    str(a) for a in merged.transitive_objects(
                        rdflib.URIRef(other), sub)}
                    for other in reached)]
    if len(specific) > 1:
        raise Refused(
            "%s reaches unrelated category roots %s. A class that is two "
            "kinds of thing is a question for the ontology."
            % (iri, [CATEGORY_ROOTS[r] for r in specific]))
    return CATEGORY_ROOTS[specific[0]] if specific else "other"


def term_records(sources: list[dict], merged, authored_namespaces: tuple,
                 known: list[tuple[str, str]]) -> list[dict]:
    """One record per term, authored and upstream.

    `sources` is [{key, path, graph, origin}]. Authored terms are those in
    an authored namespace declared in an authored module, and must carry
    a label and a definition. Upstream terms are those typed and labelled
    in a vendored extract; a stub has no definition and is published as
    having none.
    """
    import rdflib

    records, seen = [], {}
    for source in sources:
        graph = source["graph"]
        for type_iri, kind in sorted(TERM_TYPES.items()):
            for subject in graph.subjects(rdflib.URIRef(RDF_TYPE),
                                          rdflib.URIRef(type_iri)):
                if not isinstance(subject, rdflib.URIRef):
                    continue
                iri = str(subject)
                authored = source["origin"] == "authored"
                if authored and not iri.startswith(tuple(authored_namespaces)):
                    continue
                if not authored and not list(graph.objects(
                        subject, rdflib.URIRef(RDFS + "label"))):
                    continue
                if iri in seen:
                    if seen[iri] == source["key"]:
                        continue
                    raise Refused("%s is declared by both %s and %s"
                                  % (iri, seen[iri], source["key"]))
                seen[iri] = source["key"]
                parent_predicate = (RDFS + "subClassOf" if kind == "class"
                                    else RDFS + "subPropertyOf")
                records.append({
                    "id": short_id(iri, known),
                    "iri": iri,
                    "label": literal(graph, subject, RDFS + "label",
                                     "rdfs:label", required=True),
                    "definition": literal(graph, subject,
                                          SKOS + "definition",
                                          "skos:definition",
                                          required=authored),
                    "kind": kind,
                    "category": category_of(iri, kind, merged),
                    "module": source["key"],
                    "origin": source["origin"],
                    "source": source["path"],
                    "parents": sorted(
                        str(o) for o in merged.objects(
                            subject, rdflib.URIRef(parent_predicate))
                        if isinstance(o, rdflib.URIRef)),
                    "synonyms": sorted(
                        str(o) for o in graph.objects(
                            subject, rdflib.URIRef(SKOS + "altLabel"))),
                })
    records.sort(key=lambda r: (r["label"].lower(), r["iri"]))
    return records


def ontology_header(graph, source: str) -> dict:
    """The one owl:Ontology header, or a refusal."""
    import rdflib

    headers = sorted(str(s) for s in graph.subjects(
        rdflib.URIRef(RDF_TYPE), rdflib.URIRef(OWL + "Ontology")))
    if len(headers) != 1:
        raise Refused("%s has %d ontology headers: %s"
                      % (source, len(headers), headers))
    subject = rdflib.URIRef(headers[0])
    return {
        "iri": headers[0],
        "title": literal(graph, subject, DCTERMS + "title", "dcterms:title",
                         required=False),
        "version": literal(graph, subject, OWL + "versionInfo",
                           "owl:versionInfo", required=False),
        "comment": literal(graph, subject, RDFS + "comment", "rdfs:comment",
                           required=False),
    }


# ----------------------------------------------------------- markdown


def render_markdown(text: str, id_prefix: str = "",
                    baselevel: int = 2) -> tuple[str, str]:
    """(body, table of contents), with raw HTML shown rather than run.

    Python-Markdown passes raw HTML through by default. Deregistering the
    block and inline HTML handlers makes a tag in the source come out as
    escaped text -- which is what a specification quoting `<Filler>` in
    prose needs anyway.

    `id_prefix` goes in front of every heading id, so that several
    documents on one page -- the Reviews page -- cannot mint the same id
    from the same heading text ("Summary" in two reviews).
    """
    import markdown
    from markdown.extensions.toc import slugify

    # baselevel 2: the page already has its one <h1>, so the document's
    # own `#` title becomes an <h2> and everything below shifts with it.
    md = markdown.Markdown(
        extensions=["tables", "toc", "fenced_code", "sane_lists"],
        extension_configs={"toc": {
            "permalink": False, "baselevel": baselevel,
            "slugify": lambda value, sep: id_prefix + slugify(value, sep)}})
    md.preprocessors.deregister("html_block")
    md.inlinePatterns.deregister("html")
    body = md.convert(text)
    # Wide tables scroll inside their own box rather than the page.
    body = body.replace("<table>", '<div class="scroll-x"><table>')
    body = body.replace("</table>", "</table></div>")
    return body, md.toc


REVIEW_NAME = re.compile(r"^(R[0-9]+)-[A-Za-z0-9.-]+$")


def page_ids(body: str) -> list[str]:
    return re.findall(r'\sid="([^"]*)"', body)


DISPOSITION_STATUS = re.compile(
    r"^\| Status \| (Proposed|Accepted)\b[^|]*\|\s*$", re.M)


def disposition_status(text: str, path) -> str:
    """Return "proposed" or "accepted", read from the disposition's own
    Status row."""
    found = DISPOSITION_STATUS.findall(text)
    if len(found) != 1:
        raise Refused(
            "%s has %d Status rows reading Proposed or Accepted; a "
            "disposition says exactly once which it is, and the Reviews "
            "page reads it from there" % (relative(path), len(found)))
    return found[0].lower()


def reviews_values(ctx: dict, paths: list) -> dict:
    """The Reviews page: every file under reviews/, in sorted order, each
    under its own heading and with its own id prefix.

    A review is named R<n>-<words>.md. A file named R<n>-disposition.md is
    the project's disposition of review R<n>: it is rendered too,
    directly after the review it answers and labelled as a disposition,
    so a validator reading a review sees the response beside it rather
    than the reviewer's word alone. Refused: a name of neither form, two
    reviews with one number, a disposition with no review, and any id the
    page would carry twice.

    Whether a disposition is proposed or accepted is read from its own
    `| Status | Proposed ... |` or `| Status | Accepted ... |` table row,
    never typed here: the label said "(proposed)" for every disposition,
    and went on saying it after R6's was accepted. A disposition with no
    such row, or another word in it, is refused.
    """
    reviews, dispositions = {}, {}
    for path in sorted(paths, key=lambda p: p.name):
        match = REVIEW_NAME.match(path.stem)
        if not match:
            raise Refused("%s is not named R<n>-<words>.md, so the Reviews "
                          "page cannot say which review it is"
                          % relative(path))
        number = match.group(1)
        target = (dispositions if path.stem == number + "-disposition"
                  else reviews)
        if number in target:
            raise Refused("two files under reviews/ claim %s: %s and %s"
                          % (number, relative(target[number]),
                             relative(path)))
        target[number] = path
    orphans = sorted(set(dispositions) - set(reviews))
    if orphans:
        raise Refused("a disposition answers no review under reviews/: %s"
                      % orphans)
    if not reviews:
        raise Refused("reviews/ holds no review, so the Reviews page would "
                      "describe nothing")

    def order(number: str) -> int:
        return int(number[1:])

    sections, contents = [], []
    for number in sorted(reviews, key=order):
        for path, kind in ((reviews[number], "review"),
                           (dispositions.get(number), "disposition")):
            if path is None:
                continue
            raw = source_bytes(path)
            text = raw.decode("utf-8")
            first = next((line.lstrip("# ").strip()
                          for line in text.splitlines()
                          if line.startswith("# ")), path.stem)
            tag = number.lower() + ("" if kind == "review"
                                    else "-disposition")
            # Document headings sit under the section's own <h2>.
            body, _toc = render_markdown(text, id_prefix=tag + "-",
                                         baselevel=3)
            heading = ("Review %s" % number if kind == "review"
                       else "Disposition of %s (%s)"
                       % (number, disposition_status(text, path)))
            contents.append('<li><a href="#review-%s">%s</a> &mdash; %s</li>'
                            % (tag, esc(heading), esc(first)))
            sections.append(
                '<section class="review" id="review-%s">\n<h2>%s</h2>\n%s\n'
                '<article class="doc">\n%s\n</article>\n</section>' % (
                    tag, esc(heading), definition_list([
                        ("Source", source_link(ctx, relative(path))),
                        ("SHA-256", code(sha256(raw))),
                    ]), body))
    html_sections = "\n".join(sections)
    ids = page_ids(html_sections)
    repeated = sorted({i for i in ids if ids.count(i) > 1})
    if repeated:
        raise Refused("the Reviews page would carry these ids more than "
                      "once: %s" % repeated)
    return {
        "reviews_contents": '<ul class="term-list">\n%s\n</ul>'
                            % "\n".join(contents),
        "reviews_body": html_sections,
    }


def render_inline(text: str) -> str:
    body, _toc = render_markdown(text)
    body = body.strip()
    if body.startswith("<p>") and body.endswith("</p>"):
        body = body[3:-4]
    return body


# --------------------------------------------------------- downloads


def deterministic_zip(members: list[tuple[str, bytes]], epoch: int) -> bytes:
    """Same members, same bytes, on any machine.

    Member order sorted; one timestamp, truncated to the two-second step
    zip stores rather than left to round; fixed permissions; fixed
    creating system; fixed compression level.
    """
    import time

    stamp_tuple = time.gmtime(epoch - (epoch % 2))[:6]
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as archive:
        for name, data in sorted(members):
            info = zipfile.ZipInfo(name, date_time=stamp_tuple)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            archive.writestr(info, data, compresslevel=9)
    return buffer.getvalue()


# -------------------------------------------------------------- pages


def fill(fragment: str, values: dict, name: str) -> str:
    wanted = set(re.findall(r"\{\{([a-z_]+)\}\}", fragment))
    missing = sorted(wanted - set(values))
    if missing:
        raise Refused("page %s has placeholders nothing fills: %s"
                      % (name, missing))
    for key in sorted(wanted):
        fragment = fragment.replace("{{%s}}" % key, values[key])
    leftover = re.findall(r"\{\{[^}]*\}\}", fragment)
    if leftover:
        raise Refused("page %s has malformed placeholders: %s"
                      % (name, leftover))
    return fragment


def definition_list(rows: list[tuple[str, str]]) -> str:
    """Rows of (term, already-escaped html)."""
    out = ['<dl class="facts">']
    for term, value in rows:
        out.append("  <dt>%s</dt><dd>%s</dd>" % (esc(term), value))
    out.append("</dl>")
    return "\n".join(out)


def code(text: str) -> str:
    return "<code>%s</code>" % esc(text)


def source_link(ctx: dict, path: str, label: str | None = None) -> str:
    url = "%s/blob/%s/%s" % (ctx["repository"], ctx["commit"], path)
    return '<a href="%s">%s</a>' % (esc(url, quote=True),
                                    esc(label or path))


def shell(ctx: dict, key: str, title: str, body: str, depth: int) -> str:
    site, notices = ctx["site"], ctx["site"]["notices"]
    prefix = "../" * depth
    nav = []
    for item in site["navigation"]:
        href = (prefix + item["path"]) or "./"
        current = ' aria-current="page"' if item["key"] == key else ""
        nav.append('      <a href="%s"%s>%s</a>'
                   % (esc(href, quote=True), current, esc(item["label"])))
    scripts = ""
    if key == "explore":
        scripts = ('\n  <script src="%sassets/js/ranking.js"></script>'
                   '\n  <script src="%sassets/js/explorer.js"></script>'
                   % (prefix, prefix))
    page_title = (esc(site["site"]["name"]) if key == "home"
                  else "%s &middot; %s" % (esc(title),
                                           esc(site["site"]["name"])))
    return """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%(title)s</title>
<link rel="stylesheet" href="%(prefix)sassets/css/site.css">
</head>
<body>
  <a class="skip" href="#main">Skip to content</a>
  <header class="masthead">
    <p class="wordmark"><a href="%(home)s">%(name)s</a></p>
    <nav aria-label="Primary">
%(nav)s
    </nav>
  </header>
  <main id="main" tabindex="-1" class="page-%(key)s">
%(body)s
  </main>
  <footer class="footer">
    <p class="notice"><strong>%(draft)s</strong></p>
    <p class="notice">%(iri)s</p>
    <p class="notice">%(licence)s</p>
    <p class="credit">%(credit)s</p>
    <p class="build">Built from commit %(commit_link)s &middot;
      <span data-build="label">%(label)s</span> &middot;
      <a href="%(issues)s">Report an issue</a></p>
  </footer>%(scripts)s
</body>
</html>
""" % {
        "title": page_title,
        "prefix": prefix,
        "home": prefix or "./",
        "name": esc(site["site"]["name"]),
        "nav": "\n".join(nav),
        "key": esc(key),
        "body": body,
        "draft": esc(notices["draft"]["text"]),
        "iri": esc(notices["iri_resolution"]["text"]),
        "licence": esc(notices["license"]["text"]),
        "credit": esc(notices["acknowledgment"]["text"]),
        "commit_link": '<a href="%s/tree/%s"><code data-build="commit">%s'
                       '</code></a>' % (esc(ctx["repository"], quote=True),
                                        ctx["commit"], ctx["commit"][:12]),
        "label": esc(notices["build_label"]["text"]),
        "issues": esc(ctx["repository"] + "/issues", quote=True),
        "scripts": scripts,
    }


def notice_block(text: str) -> str:
    return ('<section class="notice-block" aria-label="Status">\n'
            "  <p><strong>%s</strong></p>\n</section>" % esc(text))


# --------------------------------------------------------- vocabulary


PROV = "http://www.w3.org/ns/prov#"


def vocabulary_concept_count(graph, namespaces) -> int:
    """SKOS concepts the vocabulary graph declares in an authored
    namespace: the population the vocabulary and wellformedness rungs
    validate."""
    import rdflib

    return sum(1 for s in set(graph.subjects(
        rdflib.URIRef(RDF_TYPE), rdflib.URIRef(SKOS + "Concept")))
        if isinstance(s, rdflib.URIRef) and str(s).startswith(
            tuple(namespaces)))


def vocabulary_values(graph, namespaces, known: list[tuple[str, str]],
                      empty_notice: str) -> dict:
    """The Vocabulary page's placeholders, from the generated Turtle.

    `graph` is vocab/generated/*.ttl merged -- never the YAML: what the
    site publishes is what tools/vocab/build.py published, after its
    checks, not a second reading of its inputs. `namespaces` is
    validate.AUTHORED_NAMESPACES, whose first entry is bco:, where the
    vocabulary's annotation properties live.

    Shown: the authored namespaces, each scheme with its concepts (label,
    definition, derived status, designated class, genus and foundational
    ancestor (review R7, E), notation, sources with their relation and,
    for consistent-with, their support, and for departs-from the cited
    claim's index and status (R7, A), drafting agent), the citations of
    the register entries concepts
    actually cite -- not the register, whose publication the architect
    has not decided -- and the declared agents. The same refusals as
    the term index: a concept with no label, definition or status, or
    two in the published language, stops the build, and so does a
    concept in no scheme or in two.
    """
    import rdflib

    bco = namespaces[0]
    U = rdflib.URIRef
    rdf_type = U(RDF_TYPE)

    def short(iri) -> str:
        return short_id(str(iri), known)

    def objects(subject, predicate: str) -> list:
        return sorted(graph.objects(subject, U(predicate)), key=str)

    def one(subject, predicate: str, what: str, required: bool) -> str:
        return literal(graph, subject, predicate, what, required)

    def agent_name(agent) -> str:
        name = one(agent, RDFS + "label", "rdfs:label", required=False)
        return ("%s (%s)" % (esc(name), code(short(agent))) if name
                else code(short(agent)) + " (not a declared agent)")

    schemes = sorted(s for s in graph.subjects(
        rdf_type, U(SKOS + "ConceptScheme")) if isinstance(s, rdflib.URIRef))
    concepts = sorted(s for s in graph.subjects(
        rdf_type, U(SKOS + "Concept")) if isinstance(s, rdflib.URIRef))
    by_scheme = {scheme: [] for scheme in schemes}
    for concept in concepts:
        homes = objects(concept, SKOS + "inScheme")
        if len(homes) != 1 or homes[0] not in by_scheme:
            raise Refused(
                "%s is in %d scheme(s) %s; the page places a concept under "
                "exactly one declared scheme" % (concept, len(homes),
                                                [str(h) for h in homes]))
        by_scheme[homes[0]].append(concept)

    cited = {}
    parts = []
    for scheme in schemes:
        members = by_scheme[scheme]
        title = one(scheme, SKOS + "prefLabel", "skos:prefLabel",
                    required=True)
        parts.append("<h3>%s</h3>\n%s" % (esc(title), definition_list([
            ("IRI", code(str(scheme))),
            ("Definition", esc(one(scheme, SKOS + "definition",
                                   "skos:definition", required=True))),
            ("Concepts", "%d" % len(members)),
        ])))
        for concept in members:
            labels = sorted(objects(concept, SKOS + "prefLabel"),
                            key=lambda v: (v.language or "", str(v)))
            rows = [
                ("IRI", code(str(concept))),
                ("Labels", "; ".join(
                    "%s%s" % (esc(str(v)), " (%s)" % esc(v.language)
                              if v.language else "") for v in labels)),
                ("Definition", esc(one(concept, SKOS + "definition",
                                       "skos:definition", required=True))),
                ("Status", esc(one(concept, bco + "lifecycleStatus",
                                   "bco:lifecycleStatus", required=True))),
            ]
            notation = one(concept, SKOS + "notation", "skos:notation",
                           required=False)
            if notation:
                rows.append(("Notation", code(notation)))
            # Review R7, Finding E: the immediate genus, and apart from it
            # the foundational BFO/CCO ancestor (annotations, not axioms).
            for predicate, name in ((bco + "designatesClass",
                                     "Designated class"),
                                    (bco + "definitionGenus", "Genus"),
                                    (bco + "foundationalAncestor",
                                     "Foundational ancestor"),
                                    (SKOS + "broader", "Broader"),
                                    (DCTERMS + "isReplacedBy",
                                     "Replaced by")):
                values = objects(concept, predicate)
                if values:
                    rows.append((name, ", ".join(code(short(v))
                                                 for v in values)))
            drafted = objects(concept, PROV + "wasAttributedTo")
            rows.append(("Drafted by", ", ".join(agent_name(a)
                                                 for a in drafted)
                         or "not stated"))
            references = []
            for node in objects(concept, bco + "sourceReference"):
                source = graph.value(node, U(bco + "citesSource"))
                src_id = (str(graph.value(source, U(DCTERMS + "identifier"))
                              or short(source)) if source else "no source")
                if source is not None:
                    cited[src_id] = source
                note = one(node, bco + "departureNote", "bco:departureNote",
                           required=False)
                # Review R6, 6.1: a consistent-with reference says whether
                # the source supports the definition or only its context.
                support = one(node, bco + "support", "bco:support",
                              required=False)
                relation = one(node, bco + "relation", "bco:relation",
                               required=False) or "no relation"
                # Review R7, Finding A: a cited claim is a resource with
                # its own index and status, shown with the reference.
                claims = []
                for claim in objects(node, bco + "citesClaim"):
                    index = one(claim, bco + "claimIndex", "bco:claimIndex",
                                required=False)
                    status = one(claim, bco + "claimStatus",
                                 "bco:claimStatus", required=False)
                    claims.append("claim %s, status %s" % (
                        index or short(claim), status or "not stated"))
                references.append((src_id, "<li>%s &mdash; %s &mdash; %s%s%s"
                                   "</li>" % (
                    code(src_id),
                    esc("%s (%s)" % (relation, support) if support
                        else relation),
                    esc(one(node, bco + "locator", "bco:locator",
                            required=False) or "no locator"),
                    "".join(" &mdash; %s" % esc(c) for c in claims),
                    " &mdash; %s" % esc(note) if note else "")))
            rows.append(("Sources", '<ul class="term-list">%s</ul>'
                         % "".join(item for _key, item in sorted(references))
                         if references else "none cited"))
            heading = one(concept, SKOS + "prefLabel", "skos:prefLabel",
                          required=True)
            parts.append("<h4>%s</h4>\n%s" % (esc(heading),
                                              definition_list(rows)))
    schemes_html = "\n".join(parts) or "<p>No concept scheme is declared.</p>"

    prefix_of = {ns: prefix for prefix, ns in known}
    namespaces_html = ('<div class="scroll-x"><table>\n<thead><tr><th>Prefix'
                       "</th><th>Namespace</th></tr></thead>\n<tbody>\n%s\n"
                       "</tbody></table></div>" % "\n".join(
                           "<tr><td>%s</td><td>%s</td></tr>" % (
                               code(prefix_of[ns] + ":"), code(ns))
                           for ns in namespaces))

    if cited:
        sources_html = ('<div class="scroll-x"><table>\n<thead><tr><th>'
                        "Source</th><th>Citation</th></tr></thead>\n<tbody>\n"
                        "%s\n</tbody></table></div>" % "\n".join(
                            "<tr><td>%s</td><td>%s</td></tr>" % (
                                code(src_id), esc(one(
                                    source, DCTERMS + "bibliographicCitation",
                                    "dcterms:bibliographicCitation",
                                    required=False) or "not in the register"))
                            for src_id, source in sorted(cited.items())))
    else:
        sources_html = ("<p>No concept cites a source yet, so no citation is "
                        "shown.</p>")

    agents = sorted(s for s in graph.subjects(rdf_type, U(PROV + "Agent"))
                    if isinstance(s, rdflib.URIRef))
    agent_rows = []
    for agent in agents:
        kinds = sorted(str(k).rsplit("#", 1)[-1] for k in objects(
            agent, RDF_TYPE) if str(k) in (PROV + "Person",
                                           PROV + "SoftwareAgent"))
        model = one(agent, bco + "modelIdentifier", "bco:modelIdentifier",
                    required=False)
        behalf = objects(agent, PROV + "actedOnBehalfOf")
        agent_rows.append("<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td>"
                          "<td>%s</td></tr>" % (
                              code(short(agent)),
                              esc(one(agent, RDFS + "label", "rdfs:label",
                                      required=True)),
                              esc(", ".join(kinds) or "undeclared kind"),
                              code(model) if model else "&mdash;",
                              ", ".join(agent_name(b) for b in behalf)
                              or "&mdash;"))
    agents_html = ('<div class="scroll-x"><table>\n<thead><tr><th>Agent</th>'
                   "<th>Name</th><th>Kind</th><th>Model identifier</th>"
                   "<th>On behalf of</th></tr></thead>\n<tbody>\n%s\n</tbody>"
                   "</table></div>" % "\n".join(agent_rows)
                   if agent_rows else "<p>No agent is declared.</p>")

    return {
        "vocabulary_notice": (notice_block(empty_notice) if not concepts
                              else ""),
        "vocabulary_counts": definition_list(
            [("Concepts", "%d" % len(concepts))]
            + [(one(s, SKOS + "prefLabel", "skos:prefLabel", required=True),
                "%d" % len(by_scheme[s])) for s in schemes]
            + [("Sources cited", "%d" % len(cited)),
               ("Declared agents", "%d" % len(agents))]),
        "vocabulary_namespaces": namespaces_html,
        "vocabulary_schemes": schemes_html,
        "vocabulary_sources": sources_html,
        "vocabulary_agents": agents_html,
    }


# ------------------------------------------------------------- build


def gather() -> dict:
    """Everything the pages are made from, read once."""
    import rdflib

    validate = load_tool("bco_site_validate", "tools/ontology/validate.py")
    authored_namespaces = validate.AUTHORED_NAMESPACES

    # The generated vocabulary Turtle, from the layout contract
    # (`vocabulary: true`). Never vocab/*.yaml: the page publishes what
    # tools/vocab/build.py built, and tests/test_site.py checks that no
    # YAML under vocab/ is opened by this build.
    vocabulary_graphs = [parse(path) for path in layout.vocabulary_files()]
    if not vocabulary_graphs:
        raise Refused("the layout contract marks no file vocabulary: true, "
                      "so the Vocabulary page would describe nothing")
    vocabulary = rdflib.Graph()
    for graph in vocabulary_graphs:
        for triple in graph:
            vocabulary.add(triple)
    known = prefixes(authored_prefixes(authored_namespaces,
                                       vocabulary_graphs))

    authored, upstream = [], []
    for entry in layout.components("ontology-module"):
        path = entry.resolve()
        authored.append({"key": path.stem, "component": entry.id,
                         "path": relative(path), "graph": parse(path),
                         "origin": "authored", "file": path})
    pinned = {entry["extract"]: entry for entry in pins()}
    for entry in layout.components("vendored-ontology"):
        path = entry.resolve()
        pin = pinned.get(relative(path))
        if pin is None:
            raise Refused("%s is vendored and no pin produces it"
                          % relative(path))
        upstream.append({"key": pin["id"], "component": entry.id,
                         "path": relative(path), "graph": parse(path),
                         "origin": "upstream", "file": path, "pin": pin})

    merged = rdflib.Graph()
    for source in authored + upstream:
        for triple in source["graph"]:
            merged.add(triple)

    records = term_records(authored + upstream, merged, authored_namespaces,
                           known)

    specs = layout.components("specification")
    if len(specs) != 1:
        raise Refused("expected one specification in force, found %d"
                      % len(specs))
    spec_path = specs[0].resolve()
    reviews = layout.component("reviews").members("*.md")

    return {
        "authored_namespaces": authored_namespaces,
        "known": known,
        "vocabulary": vocabulary,
        "authored": authored,
        "upstream": upstream,
        "records": records,
        "spec_path": spec_path,
        "reviews": reviews,
        "shapes": [e.resolve() for e in layout.components(
            "ontology-validation")],
        "extracts": read_json(EXTRACTS),
        "baseline": read_json(BASELINE),
        "decisions": sorted(layout.component("docs.decisions")
                            .members("*.md"), key=lambda p: p.name),
    }


def spec_version(text: str) -> str:
    match = re.search(r"^\| Version \| ([^|]+?) \|", text, flags=re.M)
    if not match:
        raise Refused("the specification states no Version row")
    return match.group(1).strip()


def ratification_rows(text: str) -> list[list[str]]:
    rows = re.findall(r"^\| (RP-\d+) \| ([^|]*) \| ([^|]*) \| ([^|]*) \| "
                      r"([^|]*) \|$", text, flags=re.M)
    if not rows:
        raise Refused("the specification's RP table was not found")
    return [list(cell.strip() for cell in row) for row in rows]


def checklist(text: str) -> list[tuple[bool, str]]:
    return [(mark.lower() == "x", item.strip()) for mark, item in
            re.findall(r"^- \[([ xX])\] (.+)$", text, flags=re.M)]


def build(out: Path) -> list[tuple[str, str]]:
    ctx_site = read_json(CONTENT)
    commit, epoch = stamp()
    data = gather()
    ctx = {"site": ctx_site, "commit": commit,
           "repository": ctx_site["site"]["repository"].rstrip("/")}
    files: dict[str, bytes] = {}

    authored_terms = [r for r in data["records"] if r["origin"] == "authored"]
    upstream_terms = [r for r in data["records"] if r["origin"] == "upstream"]
    spec_text = data["spec_path"].read_text(encoding="utf-8")
    spec_bytes = source_bytes(data["spec_path"])
    version = spec_version(spec_text)
    findings = sum(r.get("authored_findings", 0)
                   for r in data["baseline"]["rungs"].values())
    draft = notice_block(ctx_site["notices"]["draft"]["text"])

    # ---- data
    modules = ([{"key": s["key"], "title": ontology_header(
                    s["graph"], s["path"])["title"] or s["key"],
                 "origin": "authored"} for s in data["authored"]]
               + [{"key": s["key"], "title": "%s %s" % (
                    s["pin"]["project"], s["pin"]["release"]),
                   "origin": "upstream"} for s in data["upstream"]])
    terms = {
        "format_version": 1,
        "generated_by": "tools/site/build_site.py",
        "source_commit": commit,
        "authored_namespaces": list(data["authored_namespaces"]),
        "modules": modules,
        "counts": {"authored": len(authored_terms),
                   "upstream": len(upstream_terms)},
        "classes": data["records"],
        "note": "`classes` holds every term, properties included; the name "
                "is the explorer's. Upstream terms are vendored, not "
                "authored here; `origin` says which.",
    }
    files["data/terms.json"] = (json.dumps(terms, indent=2, sort_keys=True,
                                           ensure_ascii=False)
                                .encode("utf-8") + b"\n")

    # ---- downloads
    authored_files = ([s["file"] for s in data["authored"]]
                      + data["shapes"])
    download_rows = []
    bundle_members = []
    sums = []
    for path in authored_files:
        raw = source_bytes(path)
        files["downloads/" + path.name] = raw
        download_rows.append({"file": path.name, "path": relative(path),
                              "bytes": len(raw), "sha256": sha256(raw),
                              "origin": "authored"})
        bundle_members.append((BUNDLE_ROOT + "/" + path.name, raw))
        sums.append("%s  %s" % (sha256(raw), path.name))
    licence = source_bytes(_root / "LICENSE")
    bundle_members.append((BUNDLE_ROOT + "/LICENSE", licence))
    sums.append("%s  %s" % (sha256(licence), "LICENSE"))
    sums_bytes = ("\n".join(sorted(sums, key=lambda s: s[66:])) + "\n"
                  ).encode("utf-8")
    bundle_members.append((BUNDLE_ROOT + "/SHA256SUMS", sums_bytes))
    bundle = deterministic_zip(bundle_members, epoch)
    files["downloads/" + BUNDLE_NAME] = bundle

    spec_name = data["spec_path"].name
    files["downloads/" + spec_name] = spec_bytes
    upstream_rows = []
    for source in data["upstream"]:
        raw = source_bytes(source["file"])
        files["downloads/upstream/" + source["file"].name] = raw
        upstream_rows.append({"file": source["file"].name,
                              "path": source["path"], "bytes": len(raw),
                              "sha256": sha256(raw), "origin": "upstream",
                              "licence": source["pin"]["licence"]["spdx"]})
    notice = source_bytes(_root / "vendor/NOTICE.md")
    files["downloads/upstream/NOTICE.md"] = notice

    manifest = {
        "format_version": 1,
        "generated_by": "tools/site/build_site.py",
        "source_commit": commit,
        "bundle": {"filename": BUNDLE_NAME, "bytes": len(bundle),
                   "sha256": sha256(bundle), "root": BUNDLE_ROOT + "/",
                   "members": sorted(name for name, _ in bundle_members)},
        "authored": download_rows,
        "specification": {"file": spec_name,
                          "path": relative(data["spec_path"]),
                          "bytes": len(spec_bytes),
                          "sha256": sha256(spec_bytes)},
        "upstream": upstream_rows,
    }
    files["data/downloads.json"] = (json.dumps(manifest, indent=2,
                                               sort_keys=True)
                                    .encode("utf-8") + b"\n")

    # ---- page values
    status_summary = definition_list([
        ("Specification", "%s &mdash; %s" % (
            esc(version), '<a href="specification/">read it</a>')),
        ("Ratified", "nothing yet &mdash; see "
                     '<a href="status/">Status</a>'
         if not any(done for done, _ in checklist(spec_text)
                    if _.startswith("CP-0")) else "CP-0 complete"),
        ("BCO terms written", "%d" % len(authored_terms)),
        ("Upstream terms in use", "%d, from %d pinned extracts" % (
            len(upstream_terms), len(data["upstream"]))),
        ("Open validation findings", "%d" % findings),
    ])
    for_validators = "<ol>\n%s\n</ol>" % "\n".join(
        "  <li>%s</li>" % esc(item)
        for item in ctx_site["home"]["for_validators"])

    spec_body, spec_toc = render_markdown(spec_text)
    spec_facts = definition_list([
        ("Version", esc(version)),
        ("Source", source_link(ctx, relative(data["spec_path"]))),
        ("SHA-256", code(sha256(spec_bytes))),
        ("Download", '<a href="../downloads/%s">%s</a> (%s bytes)' % (
            esc(spec_name, quote=True), esc(spec_name),
            "{:,}".format(len(spec_bytes)))),
    ])

    authored_modules = []
    for source in data["authored"]:
        header = ontology_header(source["graph"], source["path"])
        count = sum(1 for r in authored_terms if r["module"] == source["key"])
        authored_modules.append(
            "<h3>%s</h3>\n%s\n%s" % (
                esc(header["title"] or source["key"]),
                "<p>%s</p>" % esc(header["comment"]) if header["comment"]
                else "",
                definition_list([
                    ("Terms", "%d%s" % (count, " &mdash; specified, not yet "
                                        "written" if not count else "")),
                    ("Version", esc(header["version"] or "none stated")),
                    ("Ontology IRI", code(header["iri"])),
                    # The ontology's own namespace: the first of
                    # AUTHORED_NAMESPACES, as ADR-003 D1 orders them
                    # (tests/test_namespace.py pins the order).
                    ("Namespace", code(data["authored_namespaces"][0])
                     + " (provisional)"),
                    ("Source", source_link(ctx, source["path"])),
                    ("Download", '<a href="../downloads/%s">%s</a>' % (
                        esc(source["file"].name, quote=True),
                        esc(source["file"].name))),
                ])))
    shape_rows = []
    for path in data["shapes"]:
        rung = None
        for name, entry in data["baseline"]["rungs"].items():
            if layout.component(name).resolve() == path:
                rung = entry
        shape_rows.append("<li>%s &mdash; %s recorded finding(s)</li>" % (
            source_link(ctx, relative(path)),
            esc(str(rung["authored_findings"])) if rung else "no baseline"))
    shape_sets = "<ul>\n%s\n</ul>" % "\n".join(shape_rows)

    upstream_sources = []
    for source in data["upstream"]:
        pin = source["pin"]
        record = data["extracts"]["extracts"][pin["id"]]
        upstream_sources.append("<h3>%s %s</h3>\n%s" % (
            esc(pin["project"]), esc(pin["release"]), definition_list([
                ("Commit", code(pin["commit"])),
                ("Taken from", '<a href="%s">%s</a>' % (
                    esc(pin["url"], quote=True), esc(pin["url"]))),
                ("Licence", '<a href="%s">%s</a>' % (
                    esc(pin["licence"]["url"], quote=True),
                    esc(pin["licence"]["spdx"]))),
                ("Attribution", esc(" ".join(
                    pin["licence"]["attribution"].split()))),
                ("Terms", "%d in full, %d declared as stubs" % (
                    record["terms_described_in_full"],
                    record["terms_declared_as_stubs"])),
                ("Axioms dropped", "%d (anonymous class expressions)"
                 % record["axioms_dropped_anonymous_object"]),
                ("Extract", source_link(ctx, source["path"])),
            ])))

    rp_rows = ratification_rows(spec_text)
    ratification = (
        "<p>The specification lists ten decisions that need ratification "
        "before any requirement is promoted. This is its own table, "
        "rendered as it stands in the specification at this commit; a "
        "ratification is recorded in the decision record below.</p>\n"
        '<div class="scroll-x"><table class="rp">\n<thead><tr><th>ID</th>'
        "<th>Decision</th><th>Proposal</th><th>Status</th></tr></thead>\n"
        "<tbody>\n%s\n</tbody></table></div>\n"
        "<h3>Acceptance checklist</h3>\n<ul class=\"checklist\">\n%s\n</ul>"
        % ("\n".join("<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>"
                     % (esc(row[0]), render_inline(row[1]),
                        render_inline(row[2]), render_inline(row[4]))
                     for row in rp_rows),
           "\n".join("  <li>%s %s</li>" % (
               "&#9745;" if done else "&#9744;", render_inline(item))
               for done, item in checklist(spec_text))))

    decision_rows = []
    for path in data["decisions"]:
        first = path.read_text(encoding="utf-8").splitlines()[0]
        decision_rows.append("<li>%s</li>" % source_link(
            ctx, relative(path), first.lstrip("# ").strip()))
    decisions = ("<ul>\n%s\n</ul>" % "\n".join(decision_rows)
                 if decision_rows else "<p>None recorded.</p>")

    # Counted from the generated vocabulary the ladder validates, not
    # typed: this line said "Authored terms checked: 0" for a day after
    # 14 vocabulary concepts entered the validation scope, because it
    # counted ontology terms only.
    concepts_checked = vocabulary_concept_count(data["vocabulary"],
                                                data["authored_namespaces"])
    if not authored_terms and not concepts_checked:
        vacuity = ("<p>With no BCO term or vocabulary concept written, "
                   "every shape set conforms vacuously. What shows the "
                   "shapes work today is the fixture built to break them, "
                   "which they reject.</p>")
    elif not authored_terms:
        vacuity = ("<p>No BCO ontology term is written yet, so the shapes "
                   "over ontology classes conform vacuously; the "
                   "vocabulary and wellformedness rungs check the %d "
                   "vocabulary concept(s) counted above. Each shape set is "
                   "also run against a fixture built to break it, which it "
                   "rejects.</p>" % concepts_checked)
    else:
        vacuity = ""
    validation = definition_list(
        [("Ontology terms checked", "%d" % len(authored_terms)),
         ("Vocabulary concepts checked", "%d" % concepts_checked)]
        + [("%s" % name, "%d recorded finding(s)" % entry["authored_findings"])
           for name, entry in sorted(data["baseline"]["rungs"].items())]) \
        + vacuity

    unresolved_parts = []
    for key, record in sorted(data["extracts"]["extracts"].items()):
        names = record["named_by_specification_described_by_no_pinned_file"]
        if not names:
            continue
        unresolved_parts.append(
            "<h3>%s namespace (%d)</h3>\n<ul class=\"term-list\">\n%s\n</ul>"
            % (esc(key.upper()), len(names), "\n".join(
                "  <li>%s</li>" % code(short_id(iri, data["known"]))
                for iri in names)))
    unresolved = "\n".join(unresolved_parts) or "<p>None.</p>"

    def file_table(rows: list[dict], href_prefix: str, licence: bool) -> str:
        head = "<th>File</th><th>Bytes</th><th>SHA-256</th>" + (
            "<th>Licence</th>" if licence else "")
        body = "\n".join(
            "<tr><td><a href=\"%s%s\">%s</a></td><td>%s</td><td>%s</td>%s"
            "</tr>" % (href_prefix, esc(r["file"], quote=True),
                       esc(r["file"]), "{:,}".format(r["bytes"]),
                       code(r["sha256"]),
                       "<td>%s</td>" % esc(r["licence"]) if licence else "")
            for r in rows)
        return ('<div class="scroll-x"><table>\n<thead><tr>%s</tr></thead>'
                "\n<tbody>\n%s\n</tbody></table></div>" % (head, body))

    bundle_html = (
        "<p>Every authored module and shape set, the licence, and a "
        "SHA256SUMS file, in one archive. Upstream extracts are not "
        "included.</p>\n<p><a href=\"%s\">Download %s</a> (%s bytes)</p>\n%s"
        "\n<p>The archive is byte-reproducible: member order, timestamps, "
        "permissions and creating system are fixed, so two builds of one "
        "commit produce the same bytes.</p>"
        % (esc(BUNDLE_NAME, quote=True), esc(BUNDLE_NAME),
           "{:,}".format(len(bundle)), definition_list([
               ("SHA-256", code(sha256(bundle))),
               ("Members", "%d" % len(bundle_members)),
           ])))

    explore_notice = notice_block(
        "No BCO term has been written yet. Everything listed below is "
        "upstream: the BFO, CCO and BPO terms the specification builds on. "
        "BCO terms will appear beside them, marked as authored, once "
        "ADR-002 is ratified.") if not authored_terms else ""

    values = {
        "site_name": esc(ctx_site["site"]["name"]),
        "tagline": esc(ctx_site["site"]["tagline"]),
        "summary": esc(ctx_site["home"]["summary"]),
        "draft_notice": draft,
        "status_summary": status_summary,
        "for_validators": for_validators,
        "companion_link": '<a href="%s">%s</a>' % (
            esc(ctx_site["site"]["companion"]["url"], quote=True),
            esc(ctx_site["site"]["companion"]["label"])),
        "spec_facts": spec_facts,
        "spec_toc": spec_toc,
        "spec_body": spec_body,
        "authored_modules": "\n".join(authored_modules),
        "shape_sets": shape_sets,
        "upstream_sources": "\n".join(upstream_sources),
        "ratification": ratification,
        "decisions": decisions,
        "validation": validation,
        "unresolved": unresolved,
        "bundle": bundle_html,
        "authored_files": file_table(download_rows, "", False),
        "upstream_files": file_table(upstream_rows, "upstream/", True)
        + '\n<p>Attribution for all three: <a href="upstream/NOTICE.md">'
          "NOTICE.md</a>.</p>",
        "explore_notice": explore_notice,
    }
    values.update(reviews_values(ctx, data["reviews"]))
    values.update(vocabulary_values(
        data["vocabulary"], data["authored_namespaces"], data["known"],
        ctx_site["notices"]["vocabulary_empty"]["text"]))

    labels = {item["key"]: item["label"]
              for item in ctx_site["navigation"]}
    for item in ctx_site["navigation"]:
        key = item["key"]
        fragment_path = _root / PAGES / (key + ".html")
        if not fragment_path.is_file():
            raise Refused("navigation names %s and %s does not exist"
                          % (key, relative(fragment_path)))
        body = fill(fragment_path.read_text(encoding="utf-8"), values, key)
        depth = 0 if not item["path"] else item["path"].count("/")
        target = (item["path"] or "") + "index.html"
        files[target] = shell(ctx, key, labels[key], body,
                              depth).encode("utf-8")
    unused = sorted(p.stem for p in (_root / PAGES).glob("*.html")
                    if p.stem not in labels)
    if unused:
        raise Refused("page fragments no navigation entry reaches: %s"
                      % unused)

    # ---- assets
    assets = _root / ASSETS
    refused = []
    for path in sorted(assets.rglob("*"), key=lambda p: p.as_posix()):
        if path.is_dir():
            continue
        if path.name.startswith(".") or path.suffix not in \
                ALLOWED_ASSET_SUFFIXES:
            refused.append(path.relative_to(assets).as_posix())
            continue
        files[path.relative_to(assets).as_posix()] = source_bytes(path)
    if refused:
        raise Refused("%s holds files this build has no rule for: %s"
                      % (ASSETS, refused))

    # ---- write
    clear_output(out)
    written = []
    for name in sorted(files):
        dest = out / name
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(files[name])
        os.utime(dest, (epoch, epoch))
        written.append((name, sha256(files[name])))
    return written


def clear_output(out: Path) -> None:
    """Empty the artifact so no file from a previous build survives.

    ValueNet's version, kept for the reason it gives: on a synchronised
    filesystem a directory may refuse removal while its files do not, and
    only a surviving *file* would be deployed.
    """
    if not out.exists():
        out.mkdir(parents=True)
        return
    for path in sorted(out.rglob("*"), key=lambda q: len(q.parts),
                       reverse=True):
        try:
            path.rmdir() if path.is_dir() else path.unlink()
        except OSError as exc:
            if not path.is_dir():
                raise Refused("cannot remove %s from the previous build: %s"
                              % (path, exc))


def tree_digest(written: list[tuple[str, str]]) -> str:
    return sha256("\n".join("%s %s" % row for row in written)
                  .encode("utf-8"))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("-o", "--out", default=OUTPUT)
    args = ap.parse_args(argv)
    out = Path(args.out)
    out = out if out.is_absolute() else _root / out

    written = build(out)
    for name, digest in written:
        print("    %-52s %s" % (name, digest[:16]))
    print()
    print("  %d file(s) -> %s" % (len(written), args.out))
    print("  tree digest %s" % tree_digest(written))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
