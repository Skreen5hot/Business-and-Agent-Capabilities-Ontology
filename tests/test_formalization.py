"""Stage 05, first tranche (D6): the module, its tranche record, its shapes
and its reasoners.

Each check has its positive case (the real module passes) and its negative
one (a case built to break it fails), as D5-2 requires. The standard's ids
are in the test names: S05-T1, C1 to C9, D, D2 and B
(docs/standards/stage-05-ontology.md, section 5).
"""

from __future__ import annotations

import copy

import pytest

from conftest import load_tool

BCO = "https://fandaws.com/ontology/bco#"
BPO = "https://fandaws.com/ontology/bpo#"
CCO = "https://www.commoncoreontologies.org/"
OBO = "http://purl.obolibrary.org/obo/"
RDF = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
RDFS = "http://www.w3.org/2000/01/rdf-schema#"
OWL = "http://www.w3.org/2002/07/owl#"
SKOS = "http://www.w3.org/2004/02/skos/core#"

#: Every Stage 05 SHACL message, with the fixture case it must fire on.
STAGE05_CONSTRAINTS = {
    "S05-C1: a BCO class with a realization index is not under "
    "bco:BusinessCapability (CAP-01).": BCO + "FixtureIndexOutsideParent",
    "S05-C1: a BCO class under Organization Capability is not under "
    "bco:BusinessCapability; an admitted class is never staged (standard "
    "S4).": BCO + "FixtureStagedCapability",
    "S05-C2: a capability class has a some restriction on has realization "
    "(obo:BFO_0000054), which would say every bearer has been realized "
    "(CAP-02).": BCO + "FixtureSomeRealization",
    "S05-C3: a specific capability class has no realization index; every "
    "K1 class except the parent carries one or more ex:enablesProcess "
    "(CAP-03).": BCO + "FixtureNoIndex",
    "S05-C3: a realization-index member is not declared as a class in the "
    "vendored extracts (Gate B).": BCO + "FixtureUndeclaredMember",
    "S05-C3: a realization-index member does not reach Planned Act "
    "(cco:ont00000228) through rdfs:subClassOf (CAP-03).":
        BCO + "FixtureNonActMember",
    "S05-C3: a realization-index member is capability-typed: it is under "
    "Organization Capability (cco:ont00000568), not an act (CAP-03).":
        BCO + "FixtureCapabilityMember",
    "S05-C5: a capability class's definition uses a deontic term "
    "(authoriz-, licen-, mandat-, responsib-, assign-, permit-; CAP-07).":
        BCO + "FixtureDeonticDefinition",
    "S05-C6: a capability class is placed under Function (obo:BFO_0000034) "
    "with no CD6 justification record (CAP-09).":
        BCO + "FixtureFunctionCapability",
    "S05-C6: a capability class is declared disjoint from Function "
    "(obo:BFO_0000034), which CAP-09 forbids.":
        BCO + "FixtureDisjointFromFunction",
    "S05-C7: a capability class has an only restriction with no CAP-30 "
    "exhaustiveness review record.": BCO + "FixtureOnlyRestriction",
}

#: Built to conform. None may be the focus of a Stage 05 violation.
STAGE05_POSITIVE_CONTROLS = [
    BCO + "BusinessCapability", BCO + "FixtureGoodCapability",
    BCO + "FixtureGoodNarrower", BCO + "FixtureDescriptionClass",
]


@pytest.fixture(scope="module")
def formalize():
    return load_tool("bco_formalize", "tools/ontology/formalize.py")


@pytest.fixture(scope="module")
def reason():
    return load_tool("bco_reason", "tools/ontology/reason.py")


@pytest.fixture(scope="module")
def vocab(formalize):
    """The vocabulary build, once: it takes most of a minute."""
    return formalize.vocabulary()


@pytest.fixture(scope="module")
def register(formalize):
    return formalize.act_register()


@pytest.fixture(scope="module")
def tranche(formalize):
    return formalize.load_tranche()


@pytest.fixture(scope="module")
def verified(formalize, tranche, vocab, register):
    return formalize.verify(tranche, vocab, register)


@pytest.fixture(scope="module")
def module_graph(repo):
    import rdflib

    return rdflib.Graph().parse(repo / "src/05_ontology/apqc-cap.ttl",
                                format="turtle")


@pytest.fixture(scope="module")
def data_graph(layout):
    """What the ladder validates: modules, vocabulary, extracts."""
    import rdflib

    graph = rdflib.Graph()
    for path in (layout.ontology_files() + layout.vocabulary_files()
                 + layout.vendored_files()):
        graph.parse(path, format="turtle")
    return graph


@pytest.fixture(scope="module")
def validation():
    return load_tool("bco_validate_s05",
                     "tools/ontology/validate.py").measure()


def findings_for(formalize, tranche, vocab, register):
    return formalize.verify(tranche, vocab, register)[0]


# ================================================= S05-T1: the tranche record


def test_s05_t1_the_record_verifies_and_the_module_is_its_build(
        formalize, verified, repo):
    findings, classes = verified
    assert findings == [], findings
    data = formalize.render(classes)
    assert (repo / "src/05_ontology/apqc-cap.ttl").read_bytes() == data, (
        "apqc-cap.ttl is not what the tranche record produces; run "
        "tools/ontology/formalize.py --write")


def test_s05_t1_the_tranche_is_the_parent_and_39(verified):
    """The counts D5-3 approved: the parent and 39 ready types, 160 index
    slots, 147 distinct acts (156 over all 42 admitted types; the 9 others
    belong only to the three held back)."""
    _, classes = verified
    assert classes[0]["iri"] == BCO + "BusinessCapability"
    assert classes[0]["index"] == []
    assert len(classes) == 40
    assert sum(len(c["index"]) for c in classes) == 160
    assert len({m for c in classes for m in c["index"]}) == 147
    held = {"CorporateCardManagement", "CostDriverAndCriticalActivityAnalysis",
            "CustomerCreditManagement"}
    assert not held & {c["iri"][len(BCO):] for c in classes}


@pytest.mark.parametrize("mutate, needle", [
    # an index member swapped for another act
    (lambda t: t["classes"][3]["index"].__setitem__(0, "P10037"),
     "differs from the signed index"),
    # a member dropped
    (lambda t: t["classes"][3]["index"].pop(), "differs from the signed index"),
    # the concept digest moved
    (lambda t: t["classes"][0].__setitem__("concept_record_sha256", "0" * 64),
     "concept_record_sha256"),
    # a held type smuggled in
    (lambda t: t["classes"].append(dict(copy.deepcopy(t["classes"][3]),
                                        g1t="T2-02")),
     "not a ready row"),
    # a held type no longer held
    (lambda t: t["excluded"].pop("T2-24"), "holds back"),
    # a signed record's digest that is not the signed one
    (lambda t: t["classes"][0]["signed_record"].__setitem__("sha256", "1" * 64),
     "not the digest the T1 signature names"),
    # a commit that does not exist
    (lambda t: t["classes"][0]["signed_record"].__setitem__(
        "commit", "0" * 40), "git cannot show"),
    # a class whose label is not the readiness package's
    (lambda t: t["classes"][5].__setitem__("label", "Something Else"),
     "readiness package says"),
    # a type listed twice
    (lambda t: t["classes"].append(copy.deepcopy(t["classes"][4])),
     "listed twice"),
])
def test_s05_t1_a_record_that_drifts_from_its_sources_is_refused(
        formalize, tranche, vocab, register, mutate, needle):
    broken = copy.deepcopy(tranche)
    mutate(broken)
    try:
        found = findings_for(formalize, broken, vocab, register)
    except SystemExit as refused:
        found = [str(refused)]
    assert any(needle in f for f in found), found


def test_s05_t1_bytes_moved_after_signing_are_refused(
        formalize, tranche, vocab, register, repo):
    """T1-02's record gained status rows after it was signed. Its bytes at a
    later commit exist and parse, and must still be refused: the index is
    read only from the bytes that were signed."""
    import subprocess

    later = subprocess.run(["git", "rev-parse", "d7839dc"], cwd=str(repo),
                           capture_output=True, text=True).stdout.strip()
    broken = copy.deepcopy(tranche)
    broken["classes"][0]["signed_record"]["commit"] = later
    found = findings_for(formalize, broken, vocab, register)
    assert any("digests to" in f for f in found), found


def test_s05_t1_a_vocabulary_definition_that_is_not_the_signed_one(
        formalize, tranche, vocab, register):
    labels, definitions, digests, expand = vocab
    concept = expand(tranche["classes"][2]["concept"])
    changed = dict(definitions)
    changed[concept] = [definitions[concept][0].replace("organization",
                                                        "enterprise", 1)]
    found = findings_for(formalize, tranche,
                         (labels, changed, digests, expand), register)
    assert any("not the signed one" in f for f in found), found


def test_s05_t1_a_vocabulary_label_that_moved(formalize, tranche, vocab,
                                              register):
    labels, definitions, digests, expand = vocab
    concept = expand(tranche["classes"][2]["concept"])
    changed = dict(labels, **{concept: ["Renamed"]})
    found = findings_for(formalize, tranche,
                         (changed, definitions, digests, expand), register)
    assert any("is not the readiness package's" in f for f in found), found


def test_the_batch_parenthetical_is_not_part_of_the_definition(formalize):
    match = formalize.definition_matches
    assert match("A b c. (revision 3, as in the vocabulary)", "A b c.")
    assert match("A  b\nc.", "A b c.")
    assert not match("A b c d.", "A b c.")
    assert not match("A b c. and more", "A b c.")


# =============================================== S05-C4 and C9: BPO and PASS


def test_s05_c4_a_development_genus_member_needs_its_reason(
        formalize, tranche, vocab, register):
    """None of the 160 members is under a CD5 development genus, so the
    real record lists none. Mark one member's genus as a development genus,
    and the record must be refused until it carries the signed reason."""
    genus, development = register
    member = tranche["classes"][1]["index"][0]
    found = findings_for(formalize, tranche, vocab,
                         (genus, development | set(genus[member])))
    assert any("CAP-06" in f for f in found), found


def test_s05_c4_a_listed_reason_must_be_the_signed_one(
        formalize, tranche, vocab, register):
    genus, development = register
    broken = copy.deepcopy(tranche)
    member = broken["classes"][1]["index"][0]
    broken["classes"][1]["development_members"] = {
        member: "a reason no signed record gives"}
    found = findings_for(formalize, broken, vocab,
                         (genus, development | set(genus[member])))
    assert any("not the signed one" in f for f in found), found


def test_s05_c3_a_capability_typed_member_is_refused_before_writing(
        formalize, tranche, vocab, register):
    genus, development = register
    member = tranche["classes"][1]["index"][0]
    changed = dict(genus, **{member: genus[member] + [CCO + "ont00000568"]})
    found = findings_for(formalize, tranche, vocab, (changed, development))
    assert any("capability-typed" in f for f in found), found


def test_s05_c9_every_class_has_a_signed_pass(verified, tranche):
    """Each written class is a ready row and has a signed record; the
    falsification is the T2-02 case above ("not a ready row")."""
    findings, classes = verified
    assert not findings
    ids = {c["g1t"] for c in classes if c["g1t"]}
    assert ids == {c["g1t"] for c in tranche["classes"]}
    assert all(c["signed_record"]["sha256"] for c in tranche["classes"])


# ======================================== S3, C1's module half, C3's property


ALLOWED = {RDF + "type", RDFS + "label", SKOS + "definition",
           RDFS + "subClassOf", BPO + "enablesProcess"}


def module_defects(graph) -> list:
    """S3 and S05-C1 over the module alone: every class is the parent or
    directly under it; each carries only the allowed predicates; nothing is
    a blank node; the parent's parents are the two S2 names."""
    import rdflib

    out = []
    parent = rdflib.URIRef(BCO + "BusinessCapability")
    for s in set(graph.subjects(rdflib.RDF.type, rdflib.OWL.Class)):
        supers = set(graph.objects(s, rdflib.RDFS.subClassOf))
        if s == parent:
            if supers != {rdflib.URIRef(CCO + "ont00000568"),
                          rdflib.URIRef(OBO + "BFO_0000016")}:
                out.append("the parent's parents are %s" % supers)
        elif supers != {parent}:
            out.append("%s is not directly and only under the parent" % s)
        for p, o in graph.predicate_objects(s):
            if str(p) not in ALLOWED:
                out.append("%s carries %s" % (s, p))
    for triple in graph:
        if any(isinstance(term, rdflib.BNode) for term in triple):
            out.append("a blank node: %r" % (triple,))
    return out


def test_s3_the_module_carries_only_what_the_standard_allows(module_graph):
    assert module_defects(module_graph) == []


def test_s3_a_class_outside_the_standard_is_found(module_graph):
    import rdflib

    broken = rdflib.Graph()
    for triple in module_graph:
        broken.add(triple)
    some = rdflib.URIRef(BCO + "PaymentProcessing")
    broken.add((some, rdflib.OWL.equivalentClass,
                rdflib.URIRef(BCO + "CashManagement")))
    broken.add((some, rdflib.RDFS.subClassOf,
                rdflib.URIRef(BCO + "CashManagement")))
    defects = module_defects(broken)
    assert any("equivalentClass" in d for d in defects), defects
    assert any("not directly and only" in d for d in defects), defects


def enables_declared(graph) -> bool:
    import rdflib

    return (rdflib.URIRef(BPO + "enablesProcess"), rdflib.RDF.type,
            rdflib.OWL.AnnotationProperty) in graph


def test_s05_c3_enables_process_is_an_annotation_property(data_graph):
    """CAP-03: declared an owl:AnnotationProperty, from BPO's own module,
    and declared nothing else."""
    import rdflib

    assert enables_declared(data_graph)
    kinds = set(data_graph.objects(rdflib.URIRef(BPO + "enablesProcess"),
                                   rdflib.RDF.type))
    assert kinds == {rdflib.OWL.AnnotationProperty}, kinds
    assert not enables_declared(rdflib.Graph())


# ============================================ S05-C8: the BPO import boundary


EXCLUDED_MODULES = ("capabilities_wiring.ttl", "delivery_processes.ttl")


def boundary_defects(graph) -> list:
    import rdflib

    out = []
    requires = rdflib.URIRef(BPO + "requiresCapability")
    if any(True for _ in graph.triples((None, requires, None))):
        out.append("bpo:requiresCapability is asserted")
    capability = rdflib.URIRef(CCO + "ont00000568")
    for s in graph.subjects(rdflib.RDFS.subClassOf, capability):
        if str(s).startswith(BPO):
            out.append("BPO class %s is under Organization Capability" % s)
    return out


def test_s05_c8_no_requires_capability_and_no_bpo_capability_class(
        data_graph):
    assert boundary_defects(data_graph) == []


def test_s05_c8_the_boundary_check_can_fail():
    import rdflib

    graph = rdflib.Graph()
    graph.add((rdflib.URIRef(BPO + "P10000"),
               rdflib.URIRef(BPO + "requiresCapability"),
               rdflib.URIRef(BPO + "SomeCapability")))
    graph.add((rdflib.URIRef(BPO + "SomeCapability"), rdflib.RDFS.subClassOf,
               rdflib.URIRef(CCO + "ont00000568")))
    assert len(boundary_defects(graph)) == 2


def test_s05_c8_no_excluded_bpo_module_is_pinned(repo):
    """RP-3: the modules that assert bpo:requiresCapability are never a
    source, and an additional file takes act classes or the one annotation
    property, nothing wider."""
    import yaml

    pins = yaml.safe_load((repo / "config/upstream-sources.yaml")
                          .read_bytes().decode("utf-8"))
    bpo = next(s for s in pins["sources"] if s["id"] == "bpo")
    named = [bpo["url"]] + [f["url"] for f in bpo["additional_files"]]
    assert not [u for u in named if u.endswith(EXCLUDED_MODULES)], named
    patterns = {f["subjects"] for f in bpo["additional_files"]}
    assert patterns == {"^https://fandaws\\.com/ontology/bpo#P[0-9]+$",
                        "^https://fandaws\\.com/ontology/bpo#enablesProcess$"}


def test_q13_each_genus_has_one_declaration(data_graph):
    """The slices redeclare the genera with different text; taking only
    their act classes leaves each genus the registry's one definition."""
    import rdflib

    for genus in set(data_graph.subjects(rdflib.RDF.type, rdflib.OWL.Class)):
        if str(genus).startswith(BPO + "ActOf"):
            defs = list(data_graph.objects(genus, rdflib.URIRef(
                SKOS + "definition")))
            assert len(defs) <= 1, (genus, defs)


def test_the_extract_carries_no_pcf_literal(repo):
    """F (docs/decisions/2026-11-15-d6-class-increment-accepted.md): the BPO
    pin predates BPO's NOTICE.md, so no PCF-derived literal on an act class
    is published -- no name, description, comment, example or PCF
    annotation. Only each act's type and parents, which validation walks.
    The header says why, and names APQC's notice."""
    import re

    import rdflib

    path = repo / "vendor/bpo/bpo-ext-bco-extract.ttl"
    graph = rdflib.Graph().parse(path, format="turtle")
    act = re.compile("^" + re.escape(BPO) + r"P\d+$")
    acts = {s for s in graph.subjects() if act.match(str(s))}
    assert len(acts) >= 147, len(acts)
    for s in acts:
        for p, o in graph.predicate_objects(s):
            assert p in (rdflib.RDF.type, rdflib.RDFS.subClassOf), (s, p)
            assert not isinstance(o, rdflib.Literal), (s, p, o)
    for local in ("pcfID", "hierarchyID", "apqcSourceText"):
        assert not list(graph.triples((None, rdflib.URIRef(BPO + local),
                                       None))), local
    head = path.read_text(encoding="utf-8")[:4000]
    assert "embed PCF 7.4" in head and "NOTICE.md" in head, head[:500]
    notice = (repo / "vendor/NOTICE.md").read_text(encoding="utf-8")
    assert "embed PCF 7.4" in notice and "APQC does not" in notice


def test_an_additional_file_must_be_pinned_to_the_source_commit(
        monkeypatch, tmp_path):
    vendoring = load_tool("bco_vendor_s05", "tools/ontology/vendor_upstream.py")
    import yaml

    real = vendoring.layout.repository_root()
    pins = yaml.safe_load((real / "config/upstream-sources.yaml")
                          .read_bytes().decode("utf-8"))
    bpo = next(s for s in pins["sources"] if s["id"] == "bpo")
    bpo["additional_files"][0]["url"] = bpo["additional_files"][0]["url"] \
        .replace(bpo["commit"], "main")
    (tmp_path / "config").mkdir()
    (tmp_path / "config/upstream-sources.yaml").write_bytes(
        yaml.safe_dump(pins).encode("utf-8"))
    monkeypatch.setattr(vendoring.layout, "repository_root", lambda: tmp_path)
    with pytest.raises(SystemExit, match="is not pinned to"):
        vendoring.sources()


# ============================================================ the shape set


def test_every_stage05_constraint_has_a_message_and_is_listed(layout):
    from test_ontology_checks import shape_messages

    messages, silent = shape_messages(layout.path("validation.stage05"))
    assert not silent
    assert len(messages) == len(set(messages))
    assert set(messages) == set(STAGE05_CONSTRAINTS), (
        sorted(set(messages) ^ set(STAGE05_CONSTRAINTS)))


def test_every_stage05_constraint_fires_on_its_own_case(validation):
    rung = validation["rungs"]["validation.stage05"]
    fired = {(v["focus"], v["message"]) for v in rung["fixture"]["detail"]}
    missing = sorted(m for m, focus in STAGE05_CONSTRAINTS.items()
                     if (focus, m) not in fired)
    assert not missing, missing


def test_the_stage05_fixture_does_not_flag_what_is_legitimate(validation):
    rung = validation["rungs"]["validation.stage05"]
    flagged = {v["focus"] for v in rung["fixture"]["detail"]}
    assert not flagged & set(STAGE05_POSITIVE_CONTROLS), (
        flagged & set(STAGE05_POSITIVE_CONTROLS))


def test_the_real_module_conforms_to_stage05(validation):
    """And the conformance is not vacuous: the K1 target selects the 40
    written classes (measured by the fixture's own K1 cases firing above,
    and here by the corpus having them at all)."""
    rung = validation["rungs"]["validation.stage05"]
    assert rung["corpus"]["conforms"], rung["corpus"]


def test_the_stage05_targets_select_the_real_classes(data_graph):
    """The K1 target's query, run on the real graph, selects the 40."""
    q = """SELECT ?this WHERE {
      ?this a <http://www.w3.org/2002/07/owl#Class> .
      FILTER(STRSTARTS(STR(?this), "https://fandaws.com/ontology/bco#"))
      ?this <http://www.w3.org/2000/01/rdf-schema#subClassOf>*
            <https://fandaws.com/ontology/bco#BusinessCapability> . }"""
    assert len(list(data_graph.query(q))) == 40


# ================================================ S05-D and S05-D2: reasoners


def reasoner_available(reason) -> bool:
    try:
        return bool(reason.java()) and reason.jar_ok(reason.pins())
    except SystemExit:
        return False


def test_s05_d_and_d2_both_reasoners_pass_and_are_falsified(reason, capsys):
    """ELK and HermiT over the modules and extracts, each run also
    rejecting a class built to be unsatisfiable and CAP-16's fixture (an
    index member disjoint from its own parent); HermiT also rejects an
    inconsistent case and detects CAP-10's fixture. Skipped where Java or the pinned jar is absent: per
    commit that is a SKIP, and a checkpoint (below) refuses it."""
    if not reasoner_available(reason):
        pytest.skip("Java or the pinned ROBOT jar is absent (reason.py "
                    "--fetch)")
    assert reason.main(["--checkpoint"]) == 0
    out = capsys.readouterr().out
    assert "ELK     PASS" in out and "HermiT  PASS" in out, out
    assert out.count("unsatisfiable rejected") == 2, out
    assert out.count("CAP-16 rejected") == 2, out
    assert "inconsistent rejected" in out and "CAP-10 detected" in out, out
    assert "CAP-10 candidates (inferred, not asserted, between BCO " \
           "classes): 0" in out, out


def test_a_checkpoint_without_a_reasoner_fails(reason, monkeypatch, capsys):
    """D5-2: a skipped or unavailable reasoner is not a passing checkpoint
    result; on an ordinary commit it is a SKIP."""
    monkeypatch.setattr(reason, "java", lambda: None)
    assert reason.main(["--checkpoint"]) == 1
    assert "FAIL" in capsys.readouterr().out
    assert reason.main([]) == 0
    assert "SKIP" in capsys.readouterr().out


def test_a_jar_with_other_bytes_is_refused(reason, monkeypatch, tmp_path):
    data = reason.pins()
    fake = tmp_path / "robot.jar"
    fake.write_bytes(b"not robot")
    monkeypatch.setattr(reason, "jar_path", lambda d: fake)
    with pytest.raises(SystemExit, match="not the pinned"):
        reason.jar_ok(data)


def test_the_reasoner_pins_name_versions_digests_and_licences(reason):
    data = reason.pins()
    assert data["robot"]["release"] == "v1.9.11"
    assert len(data["robot"]["sha256"]) == 64
    assert {r["name"]: r["licence"] for r in data["reasoners"]} == {
        "ELK": "Apache-2.0", "HermiT": "LGPL-3.0-or-later"}


def test_the_fidelity_trace_matches_the_module(repo, tranche, module_graph):
    """The conceptual-fidelity trace's class table (section 2) has one row
    per written class, in the tranche record's order, each naming the
    class, its signed record's commit and digest, its concept digest, the
    parent the module asserts and the index size the module carries; and
    CM-01 is the approved version the trace cites."""
    import hashlib

    import rdflib

    text = (repo / "src/05_ontology/fidelity-trace-tranche-1.md").read_text(
        encoding="utf-8")
    table = text.split("## 2. The 40 classes")[1].split("## 3.")[0]
    rows = [r for r in table.splitlines()
            if r.startswith("| ") and "`bco:" in r]
    assert len(rows) == 40, len(rows)
    assert "`bco:BusinessCapability` | Business Capability |" in rows[0]
    enables = rdflib.URIRef(BPO + "enablesProcess")
    for row, entry in zip(rows[1:], tranche["classes"]):
        cells = [c.strip() for c in row.strip().strip("|").split("|")]
        assert cells[0] == entry["g1t"], (cells[0], entry["g1t"])
        assert cells[1] == "`%s`" % entry["class"]
        record = entry["signed_record"]
        assert record["commit"][:7] in cells[3], cells[3]
        assert record["sha256"][:12] in cells[3], cells[3]
        assert entry["concept_record_sha256"][:12] in cells[4]
        cls = rdflib.URIRef(BCO + entry["class"][4:])
        supers = {str(o) for o in module_graph.objects(
            cls, rdflib.RDFS.subClassOf)}
        assert supers == {BCO + "BusinessCapability"}
        assert cells[5] == "`bco:BusinessCapability`"
        assert int(cells[6]) == len(list(module_graph.objects(
            cls, enables))) == len(entry["index"])
    cm01 = repo / "src/02_conceptual_models/CM-01-business-capability.md"
    digest = hashlib.sha256(cm01.read_bytes()).hexdigest()
    assert digest == ("292c8f36d64075b9663e159985a15b448aa933c3b5ed4baff3b2a"
                      "556ca861ccc")
    assert digest in text
