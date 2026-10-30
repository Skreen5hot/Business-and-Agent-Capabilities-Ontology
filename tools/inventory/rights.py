# SPDX-License-Identifier: MIT
"""Check the rights review of the Capability Term Inventory's public catalogs.

    python tools/inventory/rights.py             # offline check
    python tools/inventory/rights.py --confirm   # refetch every pin, require its digest

Phase I-2a, under the architect's decision of 2026-10-28
(docs/decisions/2026-10-28-i2-and-bpo-repin-decided.md, E1-E3, E5, E6 and
part C). I-2a establishes, for each source and edition, what the rights
holder's terms permit, from primary evidence pinned by digest. It writes
no catalog content, and it decides nothing: every source ends in decision
points, and its `architect_decision` only points at the architect's act in
docs/decisions/ (2026-10-28-i2a-decided.md).

WHY THE RECORD IS HAND-WRITTEN AND THIS TOOL ONLY CHECKS IT

docs/sources/inventory/rights.yaml is judgement: what a licence notice
grants, where two documents conflict, what is left open. A generator
would only move that prose into Python strings, where it is harder to
review. What a tool can hold is the shape of the record and the facts
that are mechanical -- every piece of evidence pinned by digest, and the
digests still true -- so that is what this tool does. (The FIBF document
list was produced once by a script over the downloaded files; the
script is not kept, because the pins and --confirm are what make the
list checkable, not the script that typed it.)

THE OFFLINE CHECK

Refuses a rights record that:

  - is not the closed schema below (an unknown key anywhere is refused,
    because an unknown key is where catalog content would go);
  - names a source twice, a register id the citation register does not
    hold, a status other than evidence-complete, gap or deferred, or a
    terms assessment other than unambiguous, ambiguous or not-established;
  - marks a source gap or deferred without a gap reason, or complete with
    one; calls terms ambiguous with no open question;
  - has an evidence item without a sha256, a retrieval date or a statement
    of what was checked; a URL on a host the review may not cite as
    primary; BPO evidence without a 40-hex commit; browser-read text
    without its normalisation and the reason it cannot be refetched;
  - carries catalog content: a key such as label, name, definition,
    description, functions, activities or capabilities anywhere outside
    the findings block; a source code in a catalog's own pattern (a PCF
    hierarchy id, a FIBF function or activity code, a BRM code);
  - quotes more than 15 words, quotes outside a `quote` field (a
    quotation mark typed into any other string), or attributes a quote to
    evidence the source does not list;
  - fills `architect_decision` with anything but a pointer to a decision
    record that exists;
  - fails the admission guard (Amendment 4): an IRI in this repository's
    AUTHORED_NAMESPACES, text that reads as an RDF serialization, or a
    ratification or vocabulary key. The guard's constants are
    tools/inventory/harvest_bpo.py's, imported, so the two never drift.

THE NETWORK (--confirm)

Refetches every `url` evidence item from its pinned URL -- never from the
cache, which it only writes -- and requires the pinned sha256 (and, for
an archive, each pinned member's). Only
obamawhitehouse.archives.gov, ussm.gsa.gov and www.gsa.gov are fetched.
BPO evidence is read from a local BPO clone's git objects when one is at
BCO_BPO_CLONE or beside this repository, and otherwise from
raw.githubusercontent.com at the pinned commit. Browser-read text
(apqc.org) is never fetched: the site serves a bot challenge to scripted
clients and its terms forbid automated access, so it is reported as
manual. A digest that moved means the publisher changed the document;
that is a finding for the record, not something to re-pin silently.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import io
import os
import re
import subprocess
import sys
import urllib.parse
import urllib.request
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import layout  # noqa: E402

RIGHTS = "docs/sources/inventory/rights.yaml"
REGISTER = "docs/sources/register.yaml"
HARVEST = "tools/inventory/harvest_bpo.py"
DECISIONS = "docs/decisions/"
CACHE = ".upstream-cache/i2a"
FORMAT = 1

#: Hosts whose documents the review may pin as primary evidence and
#: --confirm may fetch. apqc.org is cited, never fetched (see docstring).
FETCH_HOSTS = ("obamawhitehouse.archives.gov", "ussm.gsa.gov", "www.gsa.gov")
BROWSER_HOSTS = ("www.apqc.org",)
RAW_GITHUB = "https://raw.githubusercontent.com/"
GITHUB = "https://github.com/"

STATUSES = ("evidence-complete", "gap", "deferred")
TERMS = ("unambiguous", "ambiguous", "not-established")
KINDS = ("url", "bpo-git-blob", "browser-text")
SNAPSHOT = ("candidate", "context", "excluded")
COMPONENTS = ("functions-activities", "business-capabilities")
FINDING_TOPICS = ("names", "descriptions", "codes_and_hierarchy",
                  "derivative_works", "attribution", "restrictions")
MAX_QUOTE_WORDS = 15

TOP_KEYS = {"format", "review", "authority", "proposal", "prepared",
            "scope_note", "sources", "summary_for_the_architect"}
TOP_REQUIRED = TOP_KEYS
SOURCE_KEYS = {"id", "register", "rightsholder", "work", "edition", "status",
               "terms", "gap_reason", "evidence", "unpinned_observations",
               "excluded_from_snapshot", "findings", "quotes",
               "open_questions", "decision_points", "architect_decision"}
SOURCE_REQUIRED = {"id", "register", "rightsholder", "work", "edition",
                   "status", "terms", "gap_reason", "evidence", "findings",
                   "open_questions", "decision_points", "architect_decision"}
EVIDENCE_KEYS = {"id", "kind", "url", "repository", "commit", "path",
                 "sha256", "bytes", "retrieved", "members", "normalisation",
                 "why_not_refetched", "checked", "domain", "components",
                 "snapshot", "notices", "third_party_references",
                 "macro_enabled"}
EVIDENCE_REQUIRED = {"id", "kind", "sha256", "retrieved", "checked"}
MEMBER_KEYS = {"member", "sha256"}
OBSERVATION_KEYS = {"url", "retrieved", "observed", "why_unpinned"}
EXCLUDED_KEYS = {"what", "why"}
FINDINGS_KEYS = set(FINDING_TOPICS)
ATTRIBUTION_KEYS = {"required", "summary", "locators"}
QUOTE_KEYS = {"evidence", "locator", "quote"}
DECISION_POINT_KEYS = {"id", "question", "options", "recommendation"}
OPTION_KEYS = {"key", "option"}
ARCHITECT_KEYS = {"record"}
PREPARED_KEYS = {"by", "date"}

#: Keys that would hold a catalog's own content. Refused anywhere except
#: directly under `findings`, where `names` and `descriptions` are the
#: topics a finding is about, holding prose about rights.
CATALOG_KEYS = ("label", "labels", "prefLabel", "altLabel", "name", "names",
                "definition", "definitions", "description", "descriptions",
                "title", "entries", "elements", "nodes", "processes",
                "functions", "activities", "capabilities", "children",
                "parent", "hierarchy", "code", "codes", "pcf_code", "pcf_id",
                "hierarchy_id", "element_id")
#: A catalog's own identifiers. I-2a needs none of them (they are I-2b's
#: and I-2c's), so their appearance is the sign that content leaked in.
CODE_PATTERNS = (
    ("a PCF hierarchy id", re.compile(r"\b\d{1,2}\.\d{1,2}\.\d{1,2}(?:\.\d{1,2})*\b")),
    ("a FIBF function or activity code", re.compile(r"\b[A-Z]{2,4}\.\d{3}(?:\.\d{3})*\b")),
    ("a BRM code", re.compile(r"\b[A-Z]\d{2}\.\d{3}(?:\.\d{3})?\b")),
)
QUOTE_MARKS = ('"', "“", "”")
HEX40 = re.compile(r"^[0-9a-f]{40}$")
HEX64 = re.compile(r"^[0-9a-f]{64}$")
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
SOURCE_ID = re.compile(r"^[a-z0-9]+(?:-[a-z0-9.]+)+$")
EVIDENCE_ID = re.compile(r"^[a-z0-9]+(?:-[a-z0-9.]+)+$")


class Refused(SystemExit):
    """A question for whoever wrote the record, not for this tool."""


def root() -> Path:
    return layout.repository_root()


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def harvest_module(base: Path):
    """tools/inventory/harvest_bpo.py, imported by path for its guard."""
    spec = importlib.util.spec_from_file_location(
        "bco_harvest_bpo_for_rights", base / HARVEST)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def parse_yaml(data: str):
    import yaml

    loader = getattr(yaml, "CSafeLoader", yaml.SafeLoader)
    return yaml.load(data, Loader=loader)


def load(base: Path):
    path = base / RIGHTS
    if not path.is_file():
        raise Refused("%s is missing. What records the rights review?"
                      % RIGHTS)
    raw = path.read_bytes()
    if b"\r\n" in raw:
        raise Refused("%s has CRLF line endings; digests here are over LF "
                      "bytes" % RIGHTS)
    import yaml

    text = raw.decode("utf-8")
    try:
        return text, parse_yaml(text)
    except yaml.YAMLError as error:
        raise Refused("%s does not parse as YAML: %s" % (RIGHTS, error)) \
            from None


def register_ids(base: Path) -> set[str]:
    path = base / REGISTER
    if not path.is_file():
        raise Refused("%s is missing, so no register id can be checked"
                      % REGISTER)
    data = parse_yaml(path.read_bytes().decode("utf-8"))
    entries = data.get("entries", data) if isinstance(data, dict) else data
    return {e["id"] for e in entries if isinstance(e, dict) and "id" in e}


# ----------------------------------------------------------------- check


def _keys(mapping, allowed, required, where, out) -> bool:
    if not isinstance(mapping, dict):
        out.append("%s is not a mapping; was it indented as intended?"
                   % where)
        return False
    for key in sorted(set(mapping) - set(allowed)):
        out.append("%s carries %r, which the rights record does not "
                   "define. Is it catalog content, or a field this tool "
                   "should know?" % (where, key))
    for key in sorted(set(required) - set(mapping)):
        out.append("%s declares no %r" % (where, key))
    return True


def _text(value) -> bool:
    return isinstance(value, str) and value.strip() != ""


def _walk(data, path=""):
    """(key or None, value, path, parent path) for every node."""
    if isinstance(data, dict):
        for key, value in data.items():
            here = "%s/%s" % (path, key)
            yield key, value, here, path
            yield from _walk(value, here)
    elif isinstance(data, list):
        for n, value in enumerate(data):
            here = "%s/%d" % (path, n)
            yield None, value, here, path
            yield from _walk(value, here)


def _host(url: str) -> str:
    return urllib.parse.urlsplit(url).hostname or ""


def _evidence(item, where, out) -> None:
    if not _keys(item, EVIDENCE_KEYS, EVIDENCE_REQUIRED, where, out):
        return
    if not EVIDENCE_ID.match(str(item.get("id", ""))):
        out.append("%s has id %r; expected lower-case words joined by "
                   "hyphens" % (where, item.get("id")))
    if not HEX64.match(str(item.get("sha256", ""))):
        out.append("%s has no sha256 of 64 hex digits. Evidence that is "
                   "not pinned by digest is a claim, not evidence" % where)
    if not DATE.match(str(item.get("retrieved", ""))):
        out.append("%s has no retrieval date (YYYY-MM-DD)" % where)
    if not _text(item.get("checked")):
        out.append("%s does not say what was checked in it" % where)
    kind = item.get("kind")
    if kind not in KINDS:
        out.append("%s has kind %r; expected one of %s"
                   % (where, kind, ", ".join(KINDS)))
        return
    url = item.get("url") or ""
    if kind == "url":
        if not url.startswith("https://") or _host(url) not in FETCH_HOSTS:
            out.append("%s cites %r, which is not https on %s. Primary "
                       "evidence comes from the rights holder's host"
                       % (where, url, ", ".join(FETCH_HOSTS)))
    elif kind == "browser-text":
        if not url.startswith("https://") or _host(url) not in BROWSER_HOSTS:
            out.append("%s cites %r as browser-read text, which is only "
                       "accepted from %s" % (where, url,
                                             ", ".join(BROWSER_HOSTS)))
        for key in ("normalisation", "why_not_refetched"):
            if not _text(item.get(key)):
                out.append("%s is browser-read text with no %r; how would "
                           "anyone reproduce the digest?" % (where, key))
    elif kind == "bpo-git-blob":
        if not HEX40.match(str(item.get("commit", ""))):
            out.append("%s names no 40-hex BPO commit" % where)
        if not _text(item.get("path")):
            out.append("%s names no path in BPO" % where)
        if not str(item.get("repository", "")).startswith(GITHUB):
            out.append("%s names no GitHub repository for its commit"
                       % where)
    for n, member in enumerate(item.get("members") or []):
        mw = "%s/members/%d" % (where, n)
        if _keys(member, MEMBER_KEYS, MEMBER_KEYS, mw, out):
            if not HEX64.match(str(member.get("sha256", ""))):
                out.append("%s has no sha256 of 64 hex digits" % mw)
    if "snapshot" in item and item["snapshot"] not in SNAPSHOT:
        out.append("%s has snapshot %r; expected one of %s"
                   % (where, item["snapshot"], ", ".join(SNAPSHOT)))
    for comp in item.get("components") or []:
        if comp not in COMPONENTS:
            out.append("%s lists component %r; expected one of %s"
                       % (where, comp, ", ".join(COMPONENTS)))


def _source(source, where, known_register, base, out) -> None:
    if not _keys(source, SOURCE_KEYS, SOURCE_REQUIRED, where, out):
        return
    if not SOURCE_ID.match(str(source.get("id", ""))):
        out.append("%s has id %r; expected e.g. apqc-pcf-7.4"
                   % (where, source.get("id")))
    if source.get("register") not in known_register:
        out.append("%s names register id %r, which %s does not hold"
                   % (where, source.get("register"), REGISTER))
    status, terms = source.get("status"), source.get("terms")
    if status not in STATUSES:
        out.append("%s has status %r; expected one of %s"
                   % (where, status, ", ".join(STATUSES)))
    if terms not in TERMS:
        out.append("%s has terms %r; expected one of %s"
                   % (where, terms, ", ".join(TERMS)))
    if status in ("gap", "deferred") and not _text(source.get("gap_reason")):
        out.append("%s is %s with no gap_reason. What is missing, and what "
                   "would close it?" % (where, status))
    if status == "evidence-complete" and source.get("gap_reason"):
        out.append("%s is evidence-complete but states a gap_reason; which "
                   "is it?" % where)
    if terms == "ambiguous" and not source.get("open_questions"):
        out.append("%s calls its terms ambiguous and asks no open question"
                   % where)
    for key in ("rightsholder", "work", "edition"):
        if not _text(source.get(key)):
            out.append("%s declares no %r" % (where, key))

    evidence = source.get("evidence")
    ids = set()
    if not isinstance(evidence, list) or not evidence:
        out.append("%s lists no evidence. A rights finding rests on a "
                   "document, pinned" % where)
        evidence = []
    for n, item in enumerate(evidence):
        _evidence(item, "%s/evidence/%d" % (where, n), out)
        if isinstance(item, dict):
            if item.get("id") in ids:
                out.append("%s/evidence/%d repeats id %r"
                           % (where, n, item.get("id")))
            ids.add(item.get("id"))

    for n, obs in enumerate(source.get("unpinned_observations") or []):
        ow = "%s/unpinned_observations/%d" % (where, n)
        if _keys(obs, OBSERVATION_KEYS, OBSERVATION_KEYS, ow, out):
            if not _text(obs.get("why_unpinned")):
                out.append("%s does not say why it is not pinned" % ow)
    for n, ex in enumerate(source.get("excluded_from_snapshot") or []):
        ew = "%s/excluded_from_snapshot/%d" % (where, n)
        if _keys(ex, EXCLUDED_KEYS, EXCLUDED_KEYS, ew, out):
            if not _text(ex.get("why")):
                out.append("%s does not say why it is excluded" % ew)

    findings = source.get("findings")
    if _keys(findings, FINDINGS_KEYS, FINDINGS_KEYS, where + "/findings",
             out):
        for topic in ("names", "descriptions", "codes_and_hierarchy",
                      "derivative_works"):
            if not _text(findings.get(topic)):
                out.append("%s/findings has no finding on %s"
                           % (where, topic))
        attribution = findings.get("attribution")
        aw = where + "/findings/attribution"
        if _keys(attribution, ATTRIBUTION_KEYS, ATTRIBUTION_KEYS, aw, out):
            if not isinstance(attribution.get("required"), bool):
                out.append("%s/required is not true or false" % aw)
            if not _text(attribution.get("summary")):
                out.append("%s has no summary" % aw)
            if not attribution.get("locators"):
                out.append("%s gives no locator: where does the "
                           "requirement come from?" % aw)
        if not isinstance(findings.get("restrictions"), list):
            out.append("%s/findings/restrictions is not a list" % where)

    for n, quote in enumerate(source.get("quotes") or []):
        qw = "%s/quotes/%d" % (where, n)
        if not _keys(quote, QUOTE_KEYS, QUOTE_KEYS, qw, out):
            continue
        if quote.get("evidence") not in ids:
            out.append("%s attributes its quote to %r, which this source's "
                       "evidence does not list" % (qw, quote.get("evidence")))
        text = quote.get("quote")
        if not _text(text):
            out.append("%s quotes nothing" % qw)
        elif len(text.split()) > MAX_QUOTE_WORDS:
            out.append("%s quotes %d words; the limit is %d. Paraphrase, "
                       "and quote only the operative words"
                       % (qw, len(text.split()), MAX_QUOTE_WORDS))
        if not _text(quote.get("locator")):
            out.append("%s gives no locator" % qw)

    points = source.get("decision_points")
    if not isinstance(points, list) or not points:
        out.append("%s offers the architect no decision point" % where)
        points = []
    seen = set()
    for n, point in enumerate(points):
        pw = "%s/decision_points/%d" % (where, n)
        if not _keys(point, DECISION_POINT_KEYS,
                     {"id", "question", "options"}, pw, out):
            continue
        if point.get("id") in seen:
            out.append("%s repeats decision point id %r"
                       % (pw, point.get("id")))
        seen.add(point.get("id"))
        options = point.get("options") or []
        if len(options) < 2:
            out.append("%s offers %d option(s); a decision needs at least "
                       "two" % (pw, len(options)))
        for m, option in enumerate(options):
            _keys(option, OPTION_KEYS, OPTION_KEYS,
                  "%s/options/%d" % (pw, m), out)

    decision = source.get("architect_decision")
    if decision is not None:
        dw = where + "/architect_decision"
        if _keys(decision, ARCHITECT_KEYS, ARCHITECT_KEYS, dw, out):
            record = str(decision.get("record", ""))
            if not (record.startswith(DECISIONS) and record.endswith(".md")
                    and (base / record).is_file()):
                out.append("%s points at %r, which is not a decision record "
                           "in %s. The decision is the architect's act, "
                           "recorded there" % (dw, record, DECISIONS))


def _content_findings(data, out) -> None:
    """No catalog content, no long or stray quotation."""
    for key, value, path, parent in _walk(data):
        if key in CATALOG_KEYS and not parent.endswith("/findings"):
            out.append("%s is a %r field. I-2a writes no catalog content; "
                       "what is it holding?" % (path, key))
        if not isinstance(value, str):
            continue
        if key == "quote":
            continue
        if any(mark in value for mark in QUOTE_MARKS):
            out.append("%s contains a quotation mark. Quotations go in a "
                       "quotes entry, where their length is checked; "
                       "paraphrase here" % path)
        for what, pattern in CODE_PATTERNS:
            hit = pattern.search(value)
            if hit:
                out.append("%s contains %r, %s. I-2a needs no catalog "
                           "codes; is catalog content in the record?"
                           % (path, hit.group(0), what))


def check(base: Path | None = None) -> tuple[list[str], dict]:
    """(findings, counts), offline."""
    base = base or root()
    text, data = load(base)
    out: list[str] = []
    harvest = harvest_module(base)

    if _keys(data, TOP_KEYS, TOP_REQUIRED, RIGHTS, out):
        if data.get("format") != FORMAT:
            out.append("%s is format %r; this tool reads format %d"
                       % (RIGHTS, data.get("format"), FORMAT))
        if data.get("review") != "I-2a":
            out.append("%s says it is review %r, not I-2a"
                       % (RIGHTS, data.get("review")))
        for key in ("authority", "proposal"):
            if not (base / str(data.get(key, ""))).is_file():
                out.append("%s names %s %r, which does not exist"
                           % (RIGHTS, key, data.get(key)))
        _keys(data.get("prepared"), PREPARED_KEYS, PREPARED_KEYS,
              RIGHTS + "/prepared", out)
        if not _text(data.get("summary_for_the_architect")):
            out.append("%s has no summary for the architect" % RIGHTS)
        sources = data.get("sources")
        if not isinstance(sources, list) or not sources:
            out.append("%s lists no sources" % RIGHTS)
            sources = []
        known = register_ids(base)
        seen = set()
        for n, source in enumerate(sources):
            where = "%s/sources/%d" % (RIGHTS, n)
            _source(source, where, known, base, out)
            if isinstance(source, dict):
                if source.get("id") in seen:
                    out.append("%s repeats source id %r"
                               % (where, source.get("id")))
                seen.add(source.get("id"))
        _content_findings(data, out)

    # The admission guard, with harvest_bpo's own constants.
    for namespace in harvest.authored_namespaces(base):
        if namespace in text:
            out.append("%s names %s, one of this repository's authored "
                       "namespaces. The inventory mints nothing"
                       % (RIGHTS, namespace))
    for marker in harvest.RDF_MARKERS:
        if marker.search(text):
            out.append("%s reads as an RDF serialization (%s)"
                       % (RIGHTS, marker.pattern))
    if isinstance(data, (dict, list)):
        for key, _value, path, _parent in _walk(data):
            if key in harvest.FORBIDDEN_KEYS:
                out.append("%s carries %r at %s. A ratification or "
                           "vocabulary field in source evidence would make "
                           "it a decision" % (RIGHTS, key, path))

    counts = {}
    if not out:
        sources = data["sources"]
        counts = {
            "sources": len(sources),
            "evidence": sum(len(s["evidence"]) for s in sources),
            "status": {s["id"]: s["status"] for s in sources},
            "terms": {s["id"]: s["terms"] for s in sources},
        }
    return out, counts


# --------------------------------------------------------------- confirm


def _get(url: str) -> bytes:
    host = _host(url)
    if not url.startswith("https://") or host not in FETCH_HOSTS + (
            "raw.githubusercontent.com",):
        raise Refused("refusing to fetch %s: not https on %s" % (
            url, ", ".join(FETCH_HOSTS + ("raw.githubusercontent.com",))))
    request = urllib.request.Request(url, headers={
        "User-Agent": "bco-inventory-rights (+tools/inventory/rights.py)"})
    with urllib.request.urlopen(request, timeout=180) as response:
        return response.read()


def bpo_clone(base: Path) -> Path | None:
    env = os.environ.get("BCO_BPO_CLONE")
    candidates = [Path(env)] if env else []
    candidates.append(base.parent / "BusinessProcessOntology")
    for path in candidates:
        if (path / ".git").exists():
            return path
    return None


def _bpo_bytes(item: dict, base: Path, cache: Path) -> tuple[bytes, str]:
    clone = bpo_clone(base)
    if clone is not None:
        result = subprocess.run(
            ["git", "-C", str(clone), "cat-file", "blob",
             "%s:%s" % (item["commit"], item["path"])],
            capture_output=True)
        if result.returncode == 0:
            return result.stdout, "git objects of %s" % clone
    cached = cache / item["sha256"]
    if cached.is_file() and sha256(cached.read_bytes()) == item["sha256"]:
        return cached.read_bytes(), "cache"
    repo = item["repository"][len(GITHUB):].rstrip("/")
    url = "%s%s/%s/%s" % (RAW_GITHUB, repo, item["commit"],
                          urllib.parse.quote(item["path"]))
    return _get(url), url


def confirm(base: Path, cache: Path) -> list[str]:
    _text_, data = load(base)
    out = []
    for source in data["sources"]:
        for item in source["evidence"]:
            where = "%s/%s" % (source["id"], item["id"])
            if item["kind"] == "browser-text":
                print("  manual  %s: %s" % (where, item["why_not_refetched"]
                                             .split(".")[0]))
                continue
            if item["kind"] == "bpo-git-blob":
                data_bytes, origin = _bpo_bytes(item, base, cache)
            else:
                # Always the network: a government page or file can change
                # at the same URL, and a cached copy would hide exactly the
                # drift this run exists to see. (BPO's bytes are named by
                # commit, so its cache can be trusted.)
                data_bytes, origin = _get(item["url"]), item["url"]
            got = sha256(data_bytes)
            if got != item["sha256"]:
                out.append("%s: %s served %d bytes digesting to %s; the pin "
                           "says %s. The publisher changed the document, or "
                           "something between us did -- either way the "
                           "record describes bytes that are no longer "
                           "served" % (where, origin, len(data_bytes), got,
                                       item["sha256"]))
                continue
            cache.mkdir(parents=True, exist_ok=True)
            (cache / got).write_bytes(data_bytes)
            for member in item.get("members") or []:
                try:
                    with zipfile.ZipFile(io.BytesIO(data_bytes)) as archive:
                        inner = archive.read(member["member"])
                except (KeyError, zipfile.BadZipFile):
                    out.append("%s holds no member %s"
                               % (where, member["member"]))
                    continue
                if sha256(inner) != member["sha256"]:
                    out.append("%s member %s digests to %s; the pin says %s"
                               % (where, member["member"], sha256(inner),
                                  member["sha256"]))
            print("  ok      %s (%s)" % (where, origin))
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--confirm", action="store_true",
                    help="refetch every pinned document and require its "
                         "digest")
    ap.add_argument("--cache", default=None,
                    help="download cache (default .upstream-cache/i2a/)")
    args = ap.parse_args(argv)
    base = root()
    problems, counts = check(base)
    if problems:
        for problem in problems:
            print("  FINDING: %s" % problem)
        return 1
    if args.confirm:
        cache = Path(args.cache) if args.cache else base / CACHE
        drifted = confirm(base, cache)
        if drifted:
            for problem in drifted:
                print("  FINDING: %s" % problem)
            return 1
    statuses = ", ".join("%s %s/%s" % (k, v, counts["terms"][k])
                         for k, v in counts["status"].items())
    print("  ok: %d sources, %d evidence items pinned by digest%s; no "
          "catalog content, quotes within %d words, admission guard holds "
          "(%s)" % (counts["sources"], counts["evidence"],
                    " and re-confirmed" if args.confirm else "",
                    MAX_QUOTE_WORDS, statuses))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
