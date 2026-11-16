# SPDX-License-Identifier: MIT
"""Gate M and CD15's bounded absence answers (decision of 2026-11-15, B-2).

    python tools/ontology/manifests.py     # Gate M; exit 1 on a finding

GATE M

Every completeness manifest must match config/completeness-manifest.schema.json
(JSON Schema 2020-12), name only resolvable IRIs, and have start <= end. No
production evidence manifest exists: evidence graphs are Stage 06's. So the
gate checks the schema itself, every fixture manifest built to pass, and
every fixture manifest built to fail (tests/fixtures/cd15/manifests.json), and
says that it checked fixtures only.

THE ANSWERS (CD15, CAP-18)

The manifest is never RDF and changes nothing about OWL's open-world reading.
It bounds one named graph. A question about authorization evidence gets one of
three answers, per date:

  recorded       an applicable Authorization Record exists. Reported as the
                 records found, never as "authorized": validity in fact is not
                 established, and revocation and supersession are not
                 represented in v0.5 (OI-21)
  none recorded  no applicable record, and the question lies inside the scope
                 of a manifest whose graph is established complete
  unknown        anything else: no manifest covers the question, or the
                 manifest fails Gate M, or completeness is not established

"none recorded" is never "not authorized". No deontic reasoning is done: no
authority is weighed against another, and nothing is inferred about the law.

Applicability, CD15's table:

  act type   a record applies to acts of its class and of every class under
             it in the asserted hierarchy
  agent      a record applies to the agent it is about, by identity: a member
             is not the organization, nor the reverse
  period     from schema:validFrom to schema:validThrough, inclusive
  overlap    any one applicable record suffices; overlap is not an error
  authority  each record is judged alone. A record that cites no authority
             (dct:source) is not evidence (CAP-24), and a graph holding one is
             not established complete
  scope      outside a manifest's graph, organization, agents, act classes or
             dates: unknown

The same bounds answer CQ-4's realization question over a realization log:
an act realizing the capability, dated in the period, is recorded; otherwise
"none recorded" only where a manifest declares the log complete for the
organization, every member agent it has, every index member of the
capability's class and the whole period.
"""

from __future__ import annotations

import datetime as dt
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))

import layout  # noqa: E402

SCHEMA = "config/completeness-manifest.schema.json"
FIXTURES = "tests/fixtures/cd15/manifests.json"

PREFIXES = {
    "bco": "https://fandaws.com/ontology/bco#",
    "ex": "https://fandaws.com/ontology/bpo#",
    "cco": "https://www.commoncoreontologies.org/",
    "obo": "http://purl.obolibrary.org/obo/",
}
BCO = PREFIXES["bco"]
BPO = PREFIXES["ex"]
CCO = PREFIXES["cco"]
OBO = PREFIXES["obo"]
SCHEMA_ORG = "https://schema.org/"
DCT = "http://purl.org/dc/terms/"

LIMITATION = ("recorded evidence only: not a finding that the act is "
              "authorized in fact; revocation and supersession are not "
              "represented (OI-21)")

RECORDED, NONE, UNKNOWN = "recorded", "none recorded", "unknown"


# ------------------------------------------------------------------ Gate M


def schema() -> dict:
    path = layout.repository_root() / SCHEMA
    return json.loads(path.read_bytes().decode("utf-8"))


def expand(name: str) -> str | None:
    if re.match(r"^https?://", name):
        return name
    prefix, _, local = name.partition(":")
    return PREFIXES[prefix] + local if prefix in PREFIXES else None


def check(manifest, the_schema: dict | None = None) -> list:
    """Gate M's findings for one manifest; empty when it passes."""
    from jsonschema import Draft202012Validator

    validator = Draft202012Validator(the_schema or schema())
    findings = ["schema: %s at %s" % (e.message, "/".join(map(str, e.path))
                                       or "(root)")
                for e in sorted(validator.iter_errors(manifest),
                                key=lambda e: list(e.path))]
    if findings:
        return findings
    names = [manifest["graph"], manifest["organization"],
             *manifest["acting_agents"], *manifest["act_classes"],
             *manifest["authority_sources"]]
    findings += ["unresolvable name %r (known prefixes: %s)"
                 % (n, ", ".join(sorted(PREFIXES)))
                 for n in names if expand(n) is None]
    try:
        start = dt.date.fromisoformat(manifest["start"])
        end = dt.date.fromisoformat(manifest["end"])
    except ValueError as exc:
        return findings + ["not a calendar date: %s" % exc]
    if start > end:
        findings.append("start %s is after end %s" % (start, end))
    return findings


def gate() -> tuple[list, dict]:
    """(findings, counts) for the schema and the fixture manifests."""
    from jsonschema import Draft202012Validator
    from jsonschema.exceptions import SchemaError

    findings: list = []
    the_schema = schema()
    try:
        Draft202012Validator.check_schema(the_schema)
    except SchemaError as exc:
        return ["the schema is not a valid JSON Schema: %s" % exc.message], {}
    path = layout.repository_root() / FIXTURES
    data = json.loads(path.read_bytes().decode("utf-8"))
    for n, entry in enumerate(data["valid"]):
        for f in check(entry["manifest"], the_schema):
            findings.append("valid[%d] (%s) fails: %s" % (n, entry["case"], f))
    for n, entry in enumerate(data["invalid"]):
        if not check(entry["manifest"], the_schema):
            findings.append("invalid[%d] (%s) passes; it was built to fail"
                            % (n, entry["case"]))
    return findings, {"valid": len(data["valid"]),
                      "invalid": len(data["invalid"])}


# ---------------------------------------------------------------- answers


class Answer:
    """One answer: its status, the records it rests on, and why."""

    def __init__(self, status: str, records=None, reason: str = ""):
        self.status, self.records, self.reason = status, records or [], reason

    def __repr__(self):
        return "Answer(%r, %r, %r)" % (self.status, self.records, self.reason)


class Manifest:
    """A manifest, read: names expanded, dates parsed, and whether it passes
    Gate M. One that fails bounds nothing."""

    def __init__(self, **fields):
        self.__dict__.update(fields)

    @classmethod
    def read(cls, data: dict) -> "Manifest":
        ok = not check(data)
        get = (lambda k: data.get(k) or [])
        x = lambda n: expand(n) or n  # noqa: E731
        date = (lambda k: dt.date.fromisoformat(data[k])
                if ok else dt.date.min)
        return cls(graph=x(data.get("graph", "")),
                   organization=x(data.get("organization", "")),
                   agents={x(n) for n in get("acting_agents")},
                   act_classes={x(n) for n in get("act_classes")},
                   start=date("start"), end=date("end"),
                   authorities={x(n) for n in get("authority_sources")},
                   valid=ok)


def _uri(s: str):
    import rdflib
    return rdflib.URIRef(s)


def under(context, sub: str, sup: str) -> bool:
    """`sub` is `sup` or under it in the asserted rdfs:subClassOf hierarchy."""
    import rdflib

    return sub == sup or _uri(sup) in context.transitive_objects(
        _uri(sub), rdflib.RDFS.subClassOf)


def _dates(graph, subject, predicate) -> list:
    import rdflib

    out = []
    for o in graph.objects(subject, _uri(predicate)):
        if isinstance(o, rdflib.Literal) and o.datatype == rdflib.XSD.date:
            out.append(o.toPython())
    return out


def records(graph) -> list:
    """Every Authorization Record in `graph`, read: (iri, agents, classes,
    from, through, authorities, well_formed)."""
    import rdflib

    out = []
    for r in set(graph.subjects(rdflib.RDF.type, _uri(BCO + "AuthorizationRecord"))):
        agents = {str(o) for o in graph.objects(r, _uri(CCO + "ont00001808"))}
        classes = {str(o) for o in graph.objects(r, _uri(BCO + "concernsType"))}
        froms = _dates(graph, r, SCHEMA_ORG + "validFrom")
        throughs = _dates(graph, r, SCHEMA_ORG + "validThrough")
        authorities = {str(o) for o in graph.objects(r, _uri(DCT + "source"))}
        ok = (len(agents) == 1 and len(classes) == 1 and len(froms) == 1
              and len(throughs) == 1 and bool(authorities))
        out.append({"iri": str(r), "agents": agents, "classes": classes,
                    "from": froms[0] if froms else None,
                    "through": throughs[0] if throughs else None,
                    "authorities": authorities, "well_formed": ok})
    return out


def applies(record: dict, context, agent: str, act_class: str,
            on: dt.date) -> bool:
    return (record["well_formed"] and record["agents"] == {agent}
            and any(under(context, act_class, c) for c in record["classes"])
            and record["from"] <= on <= record["through"])


def covers(manifest: Manifest, context, organization: str, agents: set,
           act_classes: set, start: dt.date, end: dt.date) -> bool:
    return (manifest.valid and manifest.organization == organization
            and agents <= manifest.agents
            and all(any(under(context, a, c) for c in manifest.act_classes)
                    for a in act_classes)
            and manifest.start <= start and end <= manifest.end)


def authorization(dataset, context, manifests: list, organization: str,
                  agent: str, act_class: str, on: dt.date) -> Answer:
    """CQ-5's unit question: is there an applicable Authorization Record for
    `agent` to perform acts of `act_class` on `on`?"""
    found, graphs = [], {}
    for g in dataset.graphs():
        rs = records(g)
        graphs[str(g.identifier)] = rs
        found += [r["iri"] for r in rs if applies(r, context, agent,
                                                  act_class, on)]
    if found:
        return Answer(RECORDED, sorted(set(found)), LIMITATION)
    reasons = []
    for m in manifests:
        if not covers(m, context, organization, {agent}, {act_class}, on, on):
            continue
        if m.graph not in graphs:
            reasons.append("the manifest's graph %s is not present" % m.graph)
            continue
        bad = [r["iri"] for r in graphs[m.graph] if not r["well_formed"]]
        if bad:
            reasons.append("completeness not established: %s holds a record "
                           "without the fields CAP-24 requires, such as its "
                           "authority (%s)" % (m.graph, ", ".join(sorted(bad))))
            continue
        return Answer(NONE, [], "no applicable record within the declared "
                      "scope of %s; not a finding that the agent is "
                      "unauthorized" % m.graph)
    return Answer(UNKNOWN, [], "; ".join(reasons) or
                  "no valid manifest covers this organization, agent, act "
                  "class and date")


def over(start: dt.date, end: dt.date):
    day = start
    while day <= end:
        yield day
        day += dt.timedelta(days=1)


def authorization_period(dataset, context, manifests, organization, agent,
                         act_class, start: dt.date, end: dt.date) -> list:
    """[(first, last, Answer)]: the per-date answers over the period, each
    run of equal answers collapsed into one segment."""
    out: list = []
    for day in over(start, end):
        a = authorization(dataset, context, manifests, organization, agent,
                          act_class, day)
        key = (a.status, tuple(a.records))
        if out and (out[-1][2].status, tuple(out[-1][2].records)) == key \
                and out[-1][1] + dt.timedelta(days=1) == day:
            out[-1] = (out[-1][0], day, out[-1][2])
        else:
            out.append((day, day, a))
    return out


def realization(dataset, context, manifests: list, organization: str,
                capability: str, start: dt.date, end: dt.date) -> Answer:
    """CQ-4's unit question: is a realization of `capability` recorded in
    the period? Acts are dated with dct:date in the realization log."""
    import rdflib

    cap = _uri(capability)
    found = []
    for g in dataset.graphs():
        acts = set(g.subjects(_uri(OBO + "BFO_0000055"), cap)) | \
            set(g.objects(cap, _uri(OBO + "BFO_0000054")))
        for act in acts:
            if any(start <= d <= end for d in _dates(g, act, DCT + "date")):
                found.append(str(act))
    if found:
        return Answer(RECORDED, sorted(found), "")
    classes = {str(c) for c in context.objects(cap, rdflib.RDF.type)}
    index = {str(m) for c in classes
             for m in context.objects(_uri(c), _uri(BPO + "enablesProcess"))}
    members = {str(m) for m in context.objects(_uri(organization),
                                               _uri(OBO + "BFO_0000115"))}
    graphs = {str(g.identifier) for g in dataset.graphs()}
    for m in manifests:
        if index and covers(m, context, organization, members, index,
                            start, end) and m.graph in graphs:
            return Answer(NONE, [], "no realization recorded within the "
                          "declared scope of %s; says nothing about whether "
                          "the organization bears the capability (CD8)"
                          % m.graph)
    return Answer(UNKNOWN, [], "no valid manifest declares the realization "
                  "log complete for this organization, its members, the "
                  "capability's index and the period")


def main(argv=None) -> int:
    findings, counts = gate()
    if findings:
        for f in findings:
            print("FINDING  %s" % f)
        return 1
    print("Gate M: the schema is valid JSON Schema 2020-12; %d fixture "
          "manifest(s) built to pass pass, %d built to fail fail. No "
          "production evidence manifest exists (evidence graphs are Stage "
          "06's), so this gate has checked fixtures only."
          % (counts["valid"], counts["invalid"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
