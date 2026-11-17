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
    record that exists (`record`, and, where a later decision replaced
    it, `superseded_by`);
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

PRESENTATION DRIFT (decision of 2026-11-17)

Strict byte matching is always the first check. A mismatch is classified
only for evidence the source's `presentation_drift` block names, by one of
two bounded rules, and only when the rule recovers bytes whose sha256 is
the pin itself: the FIBF pages' asset build number restored (the pin
reproduced exactly), or the GSA website policies page compared with its
Internet Archive baseline (verified against the pin, fetched from
web.archive.org only) outside the header navigation, the Drupal settings
script and asset versions. Every mismatch is printed with one of three
statuses: exact pinned-byte match, verified presentation-only drift, or
substantive or unexplained drift, which fails. Nothing classified becomes
a pin, and any other document stays byte-strict.
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
               "open_questions", "decision_points", "architect_decision",
               "presentation_drift"}
DRIFT_KEYS = {"decision", "disposition", "finding", "asset_build_number",
              "archived_baseline", "observations"}
BUILD_KEYS = {"baseline", "unchanged", "observed_2026_11_17", "rule",
              "evidence"}
ARCHIVED_KEYS = {"evidence", "archive", "also_archived", "comparison"}
DRIFT_OBSERVATION_KEYS = {"evidence", "retrieved", "observed_sha256", "bytes",
                          "classification"}
#: The comparisons --confirm knows. Each is bounded to the one documented
#: case it was approved for (decision of 2026-11-17); a new name is a new
#: decision, not a configuration.
COMPARISONS = ("gsa-drupal-page", "none")
BUILD_HOST = "ussm.gsa.gov"
GSA_HOST = "www.gsa.gov"
ARCHIVE = re.compile(r"^https://web\.archive\.org/web/(\d{14})id_/(https://.+)$")
BUILD_NUMBER = re.compile(r"^\d{19}$")
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
ARCHITECT_KEYS = {"record", "superseded_by"}
ARCHITECT_REQUIRED = {"record"}
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

    drift = source.get("presentation_drift")
    if drift is not None:
        _drift(drift, where + "/presentation_drift", source, base, out)

    decision = source.get("architect_decision")
    if decision is not None:
        dw = where + "/architect_decision"
        if _keys(decision, ARCHITECT_KEYS, ARCHITECT_REQUIRED, dw, out):
            for key in sorted(set(decision) & ARCHITECT_KEYS):
                record = str(decision.get(key, ""))
                if not (record.startswith(DECISIONS) and record.endswith(".md")
                        and (base / record).is_file()):
                    out.append("%s/%s points at %r, which is not a decision "
                               "record in %s. The decision is the architect's "
                               "act, recorded there" % (dw, key, record,
                                                        DECISIONS))


def _drift(drift, where, source, base, out) -> None:
    """The presentation-drift addendum (decision of 2026-11-17): the
    observed digests are observations, and every rule is bounded to the
    evidence it names, on the host it was approved for."""
    if not _keys(drift, DRIFT_KEYS, DRIFT_KEYS, where, out):
        return
    evidence = {e.get("id"): e for e in source.get("evidence") or []
                if isinstance(e, dict)}
    for key in ("decision", "disposition"):
        if not (base / str(drift.get(key, ""))).is_file():
            out.append("%s/%s names %r, which does not exist"
                       % (where, key, drift.get(key)))
    if not str(drift.get("decision", "")).startswith(DECISIONS):
        out.append("%s/decision is not a record in %s" % (where, DECISIONS))
    if not _text(drift.get("finding")):
        out.append("%s has no finding" % where)
    build = drift.get("asset_build_number")
    bw = where + "/asset_build_number"
    if _keys(build, BUILD_KEYS, BUILD_KEYS, bw, out):
        tokens = [build.get("baseline"), build.get("observed_2026_11_17")] + \
            list(build.get("unchanged") or [])
        if not all(BUILD_NUMBER.match(str(t)) for t in tokens):
            out.append("%s has a build number that is not 19 digits" % bw)
        for ref in build.get("evidence") or []:
            item = evidence.get(ref)
            if item is None:
                out.append("%s names %r, which this source's evidence does "
                           "not list" % (bw, ref))
            elif item.get("kind") != "url" or _host(item.get("url", "")) \
                    != BUILD_HOST or not item["url"].endswith("/"):
                out.append("%s names %r, which is not an HTML page on %s; "
                           "the build-number rule is bounded to those"
                           % (bw, ref, BUILD_HOST))
    for n, entry in enumerate(drift.get("archived_baseline") or []):
        aw = "%s/archived_baseline/%d" % (where, n)
        if not _keys(entry, ARCHIVED_KEYS, ARCHIVED_KEYS, aw, out):
            continue
        item = evidence.get(entry.get("evidence"))
        match = ARCHIVE.match(str(entry.get("archive", "")))
        if item is None:
            out.append("%s names evidence %r, which this source does not "
                       "list" % (aw, entry.get("evidence")))
        elif not match or match.group(2) != item.get("url"):
            out.append("%s archive is not an Internet Archive id_ capture "
                       "of the evidence's own URL" % aw)
        if entry.get("comparison") not in COMPARISONS:
            out.append("%s has comparison %r; expected one of %s"
                       % (aw, entry.get("comparison"), ", ".join(COMPARISONS)))
        if entry.get("comparison") == "gsa-drupal-page" and item is not None \
                and _host(item.get("url", "")) != GSA_HOST:
            out.append("%s applies gsa-drupal-page to a page not on %s"
                       % (aw, GSA_HOST))
    for n, obs in enumerate(drift.get("observations") or []):
        ow = "%s/observations/%d" % (where, n)
        if not _keys(obs, DRIFT_OBSERVATION_KEYS, DRIFT_OBSERVATION_KEYS, ow,
                     out):
            continue
        item = evidence.get(obs.get("evidence"))
        if item is None:
            out.append("%s names evidence %r, which this source does not "
                       "list" % (ow, obs.get("evidence")))
        if not HEX64.match(str(obs.get("observed_sha256", ""))):
            out.append("%s has no observed sha256 of 64 hex digits" % ow)
        elif item is not None and obs["observed_sha256"] == item.get("sha256"):
            out.append("%s observes the pinned digest; an observation records "
                       "drift" % ow)
        if not DATE.match(str(obs.get("retrieved", ""))):
            out.append("%s has no retrieval date" % ow)


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


# ------------------------------------------------- presentation drift
#
# The decision of 2026-11-17 (docs/decisions/2026-11-17-fibf-drift-
# disposition-accepted.md) lets --confirm classify a byte mismatch on two
# documented kinds of page, and nothing else. Strict byte matching stays the
# first check; a mismatch is always reported; a classified mismatch never
# becomes a pin. Each rule recovers bytes whose sha256 IS the pin, so what a
# rule accepts is the approved evidence itself, not something like it.

EXACT, PRESENTATION, FAILURE = ("exact pinned-byte match",
                                "verified presentation-only drift",
                                "substantive or unexplained drift")
#: A stylesheet or script reference carrying a 19-digit build number.
_BUILD_REF = re.compile(rb'(\.(?:css|js)\?)(\d{19})(?=")')
#: A Drupal aggregate's content-hash file name.
_AGGREGATE = re.compile(r"/(js|css)_[A-Za-z0-9_-]{20,}\.(js|css)$")
_VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link",
         "meta", "param", "source", "track", "wbr"}


class Drift:
    def __init__(self, status: str, detail: str, pinned: bytes | None = None):
        self.status, self.detail, self.pinned = status, detail, pinned

    def __repr__(self):
        return "Drift(%r, %r)" % (self.status, self.detail)


def drift_rules(data) -> dict:
    """evidence id -> (rule, its block, the source's quotes for it)."""
    rules = {}
    for source in data.get("sources") or []:
        drift = source.get("presentation_drift")
        if not drift:
            continue
        build = drift.get("asset_build_number") or {}
        for ref in build.get("evidence") or []:
            rules[ref] = ("build-number", build, [])
        for entry in drift.get("archived_baseline") or []:
            if entry.get("comparison") == "gsa-drupal-page":
                quotes = [q["quote"] for q in source.get("quotes") or []
                          if q.get("evidence") == entry["evidence"]]
                rules[entry["evidence"]] = ("gsa-drupal-page", entry, quotes)
    return rules


def restore_build_number(item: dict, served: bytes, build: dict) -> Drift:
    """A FIBF page whose one difference is a new build number: put the
    baseline number back and require the pinned sha256 exactly."""
    if _host(item.get("url", "")) != BUILD_HOST:
        return Drift(FAILURE, "the build-number rule does not apply off %s"
                     % BUILD_HOST)
    baseline = str(build["baseline"])
    known = {baseline} | {str(t) for t in build.get("unchanged") or []}
    found = [m.group(2).decode() for m in _BUILD_REF.finditer(served)]
    if not found:
        return Drift(FAILURE, "no asset build number in the served page, so "
                     "the difference is not the documented one")
    new = sorted(set(found) - known)
    if not new:
        return Drift(FAILURE, "the build numbers are the baseline's, so the "
                     "difference is something else")
    if len(new) > 1:
        return Drift(FAILURE, "%d new build numbers (%s); which one replaced "
                     "the baseline is ambiguous" % (len(new), ", ".join(new)))
    restored = _BUILD_REF.sub(
        lambda m: m.group(1) + (baseline.encode() if m.group(2).decode()
                                == new[0] else m.group(2)), served)
    if sha256(restored) != item["sha256"]:
        return Drift(FAILURE, "restoring build number %s to %s leaves bytes "
                     "digesting to %s, not the pin: an unexplained difference "
                     "remains" % (new[0], baseline, sha256(restored)))
    return Drift(PRESENTATION, "asset build number %s in place of %s (%d "
                 "reference(s)); restoring it reproduces the pin exactly"
                 % (new[0], baseline, found.count(new[0])), restored)


def _get_archive(url: str) -> bytes:
    if not ARCHIVE.match(url):
        raise Refused("refusing to fetch %s: not an Internet Archive id_ "
                      "capture" % url)
    request = urllib.request.Request(url, headers={
        "User-Agent": "bco-inventory-rights (+tools/inventory/rights.py)",
        "Accept-Encoding": "identity"})
    last = None
    for _attempt in range(3):
        try:
            with urllib.request.urlopen(request, timeout=180) as response:
                data = response.read()
            if data[:2] == b"\x1f\x8b":
                import gzip
                data = gzip.decompress(data)
            return data
        except OSError as error:
            last = error
    raise OSError("the archive did not answer: %s" % last)


def archived_baseline(item: dict, entry: dict, cache: Path,
                      fetch=None) -> tuple[bytes | None, str]:
    """The approved bytes from the independent archive, or why not."""
    cached = cache / item["sha256"]
    if cached.is_file() and sha256(cached.read_bytes()) == item["sha256"]:
        return cached.read_bytes(), "cache"
    try:
        data = (fetch or _get_archive)(entry["archive"])
    except Exception as error:  # fail closed on any retrieval failure
        return None, "the approved baseline could not be retrieved (%s)" \
            % error
    if sha256(data) != item["sha256"]:
        return None, ("the archived baseline digests to %s, not the pin, so "
                      "the approved baseline cannot be verified"
                      % sha256(data))
    cache.mkdir(parents=True, exist_ok=True)
    cached.write_bytes(data)
    return data, entry["archive"]


class _GsaEvents:
    """The comparable events of a GSA Drupal page: every tag with its
    attributes and every text run, except the three documented regions --
    the header navigation subtree (div.usa-nav__inner inside
    header.usa-header), the Drupal settings script's body, and the version
    part of stylesheet and script URLs. Whitespace is collapsed."""

    def __init__(self, document: bytes):
        from html.parser import HTMLParser

        events, stack = [], []
        state = {"nav": 0, "settings": 0, "skip": 0, "in_settings": False}
        owner = self

        class Parser(HTMLParser):
            def handle_starttag(self, tag, attrs):
                owner._start(tag, attrs, events, stack, state)

            def handle_startendtag(self, tag, attrs):
                owner._start(tag, attrs, events, stack, state, void=True)

            def handle_endtag(self, tag):
                owner._end(tag, events, stack, state)

            def handle_data(self, data):
                if state["skip"] or state["in_settings"]:
                    return
                text = " ".join(data.split())
                if text:
                    events.append(("text", text))

            def handle_comment(self, data):
                if not state["skip"]:
                    events.append(("comment", " ".join(data.split())))

        parser = Parser(convert_charrefs=True)
        parser.feed(document.decode("utf-8"))
        parser.close()
        if state["skip"]:
            raise ValueError("the navigation region never closes")
        self.events, self.nav, self.settings = (events, state["nav"],
                                                state["settings"])

    @staticmethod
    def _asset(tag, attrs):
        out = []
        for key, value in attrs:
            value = value or ""
            if (tag, key) in (("script", "src"), ("link", "href")) and \
                    value.startswith("/"):
                path = value.split("?", 1)[0]
                value = _AGGREGATE.sub(r"/\1_*.\2", path)
            out.append((key, value))
        return tuple(sorted(out))

    def _start(self, tag, attrs, events, stack, state, void=False):
        classes = (dict(attrs).get("class") or "").split()
        if state["skip"]:
            if tag not in _VOID and not void:
                state["skip"] += 1
            return
        if tag == "div" and "usa-nav__inner" in classes and any(
                t == "header" and "usa-header" in c for t, c in stack):
            state["nav"] += 1
            state["skip"] = 1
            events.append(("navigation",))
            return
        if tag == "script" and dict(attrs).get("data-drupal-selector") == \
                "drupal-settings-json":
            state["settings"] += 1
            state["in_settings"] = True
        events.append(("start", tag, self._asset(tag, attrs)))
        if tag not in _VOID and not void:
            stack.append((tag, classes))

    def _end(self, tag, events, stack, state):
        if state["skip"]:
            state["skip"] -= 1
            return
        if tag == "script":
            state["in_settings"] = False
        events.append(("end", tag))
        for i in range(len(stack) - 1, -1, -1):
            if stack[i][0] == tag:
                del stack[i:]
                break


def _plain(document: bytes) -> str:
    import html

    text = re.sub(r"<(script|style)\b.*?</\1>", " ",
                  document.decode("utf-8"), flags=re.S | re.I)
    return " ".join(html.unescape(re.sub(r"<[^>]+>", " ", text)).split())


def compare_gsa_page(baseline: bytes, served: bytes, quotes: list) -> Drift:
    """The GSA website policies page against its approved baseline."""
    text = _plain(served)
    for quote in quotes:
        if " ".join(quote.split()) not in text:
            return Drift(FAILURE, "the rights language quoted in the review "
                         "(%s ...) is no longer on the page"
                         % " ".join(quote.split()[:5]))
    try:
        old, new = _GsaEvents(baseline), _GsaEvents(served)
    except Exception as error:  # an unsupported page fails closed
        return Drift(FAILURE, "the page could not be compared: %s" % error)
    for name, a, b in (("header navigation region", old.nav, new.nav),
                       ("Drupal settings script", old.settings, new.settings)):
        if a != 1 or b != 1:
            return Drift(FAILURE, "the %s occurs %d time(s) in the baseline "
                         "and %d in the served page; the comparison needs "
                         "exactly one in each" % (name, a, b))
    if old.events != new.events:
        import difflib

        matcher = difflib.SequenceMatcher(None, old.events, new.events,
                                          autojunk=False)
        diffs = [op for op in matcher.get_opcodes() if op[0] != "equal"]
        tag, i1, i2, j1, j2 = diffs[0]
        shown = "; ".join(
            ["was %s" % (e,) for e in old.events[i1:i2][:2]] +
            ["now %s" % (e,) for e in new.events[j1:j2][:2]])
        return Drift(FAILURE, "%d unexplained difference(s) outside the "
                     "navigation, Drupal settings and asset versions; the "
                     "first: %s" % (len(diffs), shown[:600]))
    return Drift(PRESENTATION, "only the header navigation, the Drupal "
                 "settings and asset versions differ from the approved "
                 "baseline; all other tags, attributes, links and text, and "
                 "the quoted rights language, are unchanged", baseline)


def classify(item: dict, served: bytes, rules: dict, cache: Path,
             fetch=None) -> Drift:
    """Strict bytes first; then, only for evidence a rule names, the
    documented comparison; everything else fails."""
    if sha256(served) == item["sha256"]:
        return Drift(EXACT, "the pinned bytes", served)
    rule = rules.get(item["id"])
    if rule is None:
        return Drift(FAILURE, "no presentation-drift rule covers this "
                     "document, so its bytes must match exactly")
    name, block, quotes = rule
    if name == "build-number":
        return restore_build_number(item, served, block)
    if name == "gsa-drupal-page":
        if _host(item.get("url", "")) != GSA_HOST:
            return Drift(FAILURE, "gsa-drupal-page applies only on %s"
                         % GSA_HOST)
        baseline, origin = archived_baseline(item, block, cache, fetch)
        if baseline is None:
            return Drift(FAILURE, origin)
        return compare_gsa_page(baseline, served, quotes)
    return Drift(FAILURE, "unknown rule %r" % name)


def recover(base: Path, item: dict, served: bytes, cache: Path) -> Drift:
    """For the federal harvest: the classification of served bytes against
    this record's rules, with the approved bytes when they are recovered."""
    _text_, data = load(base)
    return classify(item, served, drift_rules(data), cache)


def confirm(base: Path, cache: Path, drifts: list | None = None) -> list[str]:
    _text_, data = load(base)
    rules = drift_rules(data)
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
                mismatch = ("%s: %s served %d bytes digesting to %s; the pin "
                            "says %s" % (where, origin, len(data_bytes), got,
                                         item["sha256"]))
                verdict = classify(item, data_bytes, rules, cache) \
                    if item["kind"] == "url" else \
                    Drift(FAILURE, "no presentation-drift rule covers this "
                          "document")
                if verdict.status == PRESENTATION:
                    line = "%s. %s: %s. The pin stands; the served bytes are " \
                           "not evidence" % (mismatch, verdict.status,
                                             verdict.detail)
                    print("  drift   " + line)
                    if drifts is not None:
                        drifts.append(line)
                    cache.mkdir(parents=True, exist_ok=True)
                    (cache / item["sha256"]).write_bytes(verdict.pinned)
                    continue
                out.append("%s. %s: %s. The publisher changed the document, "
                           "or something between us did -- either way the "
                           "record describes bytes that are no longer served"
                           % (mismatch, FAILURE, verdict.detail))
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
        drifts: list = []
        drifted = confirm(base, cache, drifts)
        if drifted:
            print("  %d byte mismatch(es) above classified as %s"
                  % (len(drifts), PRESENTATION))
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
    if args.confirm:
        print("  %d byte mismatch(es) classified as %s; every pin stands"
              % (len(drifts), PRESENTATION))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
