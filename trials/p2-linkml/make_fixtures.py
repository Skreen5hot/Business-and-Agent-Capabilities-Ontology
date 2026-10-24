"""Write the P2 negative fixtures, one defect each, as LF bytes.

    python trials/p2-linkml/make_fixtures.py trials/p2-linkml/fixtures

Each fixture is the minimal valid base with exactly one mutation; the
mutation is asserted to have changed the document before it is written.
"""
import copy, sys
from pathlib import Path
import yaml

OUT = Path(sys.argv[1])
OUT.mkdir(parents=True, exist_ok=True)

MM = {
    "id": "bcom:BusinessCapability",
    "pref_label": [{"value": "Business Capability", "language": "en"}],
    "in_scheme": "bcom:MetamodelScheme",
    "designates_class": "bco:BusinessCapability",
    "spec_row": "Business Capability",
    "sources": [{"source": "SRC-OMG-03", "locator": "BACM 1.1, clause 7.2",
                 "relation": "departs-from",
                 "departure_note": "Organization-only bearer."}],
    "drafted_by": "bcoa:claude-opus-5-5",
    "created": "2026-10-23T00:00:00Z",
    "authored_status": "Draft",
}
CAT = {
    "id": "bcoc:TreasuryManagement",
    "pref_label": [{"value": "Treasury Management", "language": "en"}],
    "definition": "A business capability that manages cash and liquidity.",
    "in_scheme": "bcoc:CapabilityCatalogScheme",
    "broader": ["bcoc:FinancialManagement"],
    "notation": "10759",
    "sources": [{"source": "SRC-OMG-01", "relation": "adapted-from"}],
    "drafted_by": "bcoa:claude-opus-5-5",
    "created": "2026-10-23T00:00:00Z",
    "authored_status": "Candidate",
    "ratified_by": {
        "path": "docs/decisions/2026-11-01-catalog-batch-1.md",
        "commit": "8f5c4a1b04e0d5249d0f5b4225998bbef5ec9a76",
        "sha256": "0123456789abcdef" * 4,
        "record_digest": "fedcba9876543210" * 4,
    },
}
BUILT = {"id": "bcoc:CashManagement", "lifecycle_status": "Deprecated",
         "deprecated": True, "is_replaced_by": "bcoc:TreasuryManagement"}


def mutate(key, base, f):
    d = copy.deepcopy(base)
    f(d)
    assert d != base, "mutation did not apply"
    return {key: [d]}, base


def mm(f):
    return mutate("metamodel_concepts", MM, f)


def cat(f):
    return mutate("catalog_concepts", CAT, f)


def built(f):
    return mutate("built_statuses", BUILT, f)


def drop(key):
    return lambda d: d.pop(key)


def setk(key, value):
    return lambda d: d.__setitem__(key, value)


CASES = [
    # name, ADR rule, (doc, base)
    ("departs-from-without-departure-note", "D6 departs-from requires a departure_note",
     mm(lambda d: d["sources"][0].pop("departure_note"))),
    ("departs-from-without-locator", "D6 departs-from requires a locator",
     mm(lambda d: d["sources"][0].pop("locator"))),
    ("lifecycle-status-authored", "D5 lifecycleStatus is never authored",
     cat(setk("lifecycle_status", "Ratified"))),
    ("owl-deprecated-authored", "D5 owl:deprecated is never authored",
     cat(setk("deprecated", True))),
    ("authored-status-ratified", "D5 authors write Draft or Candidate only",
     cat(setk("authored_status", "Ratified"))),
    ("deprecated-without-replacement", "D5 Deprecated requires a replacement",
     built(drop("is_replaced_by"))),
    ("catalog-narrower-authored", "catalog concepts carry broader only, never narrower",
     cat(setk("narrower", ["bcoc:CashManagement"]))),
    ("metamodel-definition-authored", "D4 a metamodel concept may not carry a definition",
     mm(setk("definition", "Authored text that should come from spec section 4."))),
    ("metamodel-without-designates-class", "MetamodelConcept requires designatesClass",
     mm(drop("designates_class"))),
    ("metamodel-in-catalog-scheme", "a metamodel concept is in bcom:MetamodelScheme",
     mm(setk("in_scheme", "bcoc:CapabilityCatalogScheme"))),
    ("source-id-malformed", "SRC id matches ^SRC-[A-Z]+-[0-9]{2}$",
     cat(lambda d: d["sources"][0].__setitem__("source", "SRC-OMG-3"))),
    ("source-relation-unknown", "relation is one of the three enum values",
     cat(lambda d: d["sources"][0].__setitem__("relation", "inspired-by"))),
    ("sources-missing", "every concept cites at least one source",
     cat(drop("sources"))),
    ("ratification-short-commit", "D2 commit is the full 40-hex SHA",
     cat(lambda d: d["ratified_by"].__setitem__("commit", "8f5c4a1"))),
    ("ratification-empty-file-digest", "D2 the empty-file SHA-256 is refused by name",
     cat(lambda d: d["ratified_by"].__setitem__(
         "sha256", "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"))),
    ("ratification-without-record-digest", "D5 the act pins the record digest",
     cat(lambda d: d["ratified_by"].pop("record_digest"))),
    ("ratification-path-outside-decisions", "D2 path is under docs/decisions/ or docs/adr/",
     cat(lambda d: d["ratified_by"].__setitem__("path", "notes/approval.md"))),
    ("notation-not-pcf-code", "D7 notation is a PCF 7.4 element ID",
     cat(setk("notation", "1.1.2"))),
    ("pref-label-without-language", "prefLabel carries a language",
     cat(lambda d: d["pref_label"][0].pop("language"))),
    ("drafted-by-not-an-agent-iri", "drafted_by is a bcoa: agent IRI",
     cat(setk("drafted_by", "Claude"))),
    ("created-not-a-datetime", "created is an xsd:dateTime",
     cat(setk("created", "yesterday"))),
]

for name, rule, (doc, base) in CASES:
    body = yaml.safe_dump(doc, sort_keys=True, allow_unicode=False, width=79)
    text = ("# P2 negative fixture: %s\n# rule: %s\n# expect: reject\n%s"
            % (name, rule, body))
    (OUT / (name + ".yaml")).write_bytes(text.encode("utf-8"))
#: The positive control: the three bases every fixture mutates, in one
#: document that must be ACCEPTED. A fixture rejected while this is also
#: rejected proves nothing about the rule it names.
BASES = {"metamodel_concepts": [MM], "catalog_concepts": [CAT],
         "built_statuses": [BUILT]}
text = ("# P2 positive control: the unmutated bases of every fixture.\n"
        "# expect: accept\n"
        + yaml.safe_dump(BASES, sort_keys=True, allow_unicode=False, width=79))
(OUT.parent / "samples" / "fixture_bases.yaml").write_bytes(text.encode("utf-8"))
print(len(CASES), "fixtures written, plus samples/fixture_bases.yaml")
