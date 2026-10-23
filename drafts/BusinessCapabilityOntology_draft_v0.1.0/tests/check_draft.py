#!/usr/bin/env python3
"""Offline structural guards for BCO draft v0.1.0.

Requirements: rdflib.
Not a substitute for importing the pinned BFO/CCO OWL closure, SHACL, or
full OWL DL reasoning. This file never fetches external ontology documents.
"""
from pathlib import Path
from rdflib import Graph, URIRef, Namespace
from rdflib.namespace import RDF, RDFS, OWL, SKOS

ROOT = Path(__file__).resolve().parents[1]
BC = Namespace("https://example.org/BusinessCapabilityOntology#")
CCO = Namespace("https://www.commoncoreontologies.org/")
BFO = Namespace("http://purl.obolibrary.org/obo/")
EX = Namespace("http://example.org/apqc#")
SH = Namespace("http://www.w3.org/ns/shacl#")

def main():
    paths = sorted(ROOT.rglob("*.ttl"))
    assert len(paths) == 5, (len(paths), paths)
    allg = Graph()
    per = {}
    for path in paths:
        g = Graph().parse(path, format="turtle")
        per[path.relative_to(ROOT).as_posix()] = g
        allg += g
        print("PARSE OK", path.relative_to(ROOT), f"({len(g)} triples)")

    core = per["ontology/business-capability-core.ttl"]
    info = per["ontology/business-capability-information.ttl"]
    align = per["alignment/bpo-review-links.ttl"]
    example = per["examples/synthetic-illustration.ttl"]
    sh = per["shapes/capability-data-shapes.ttl"]

    assert (BC.BusinessCapability, RDFS.subClassOf, CCO.ont00000568) in core
    assert (BC.BusinessCapability, RDFS.subClassOf, BFO.BFO_0000016) in core
    assert not list(allg.triples((None, RDF.type, OWL.ObjectProperty))), "A new object property was introduced."
    assert not list(allg.triples((BC.BusinessCapability, OWL.equivalentClass, None)))
    assert not list(allg.triples((BC.BusinessCapability, OWL.disjointWith, BFO.BFO_0000034)))
    assert not list(allg.triples((BFO.BFO_0000034, OWL.disjointWith, BC.BusinessCapability)))
    assert not list(allg.triples((None, OWL.onProperty, BFO.BFO_0000054))), "Potential realization may not be encoded as a has-realization restriction."
    assert not list(allg.triples((None, OWL.onProperty, BFO.BFO_0000055)))
    assert not list(allg.triples((None, RDFS.subClassOf, BC.BusinessCapability))), "Existing classes must not be auto-promoted in v0.1.0."
    assert not list(allg.triples((None, OWL.sameAs, None)))

    new_classes = {s for s in allg.subjects(RDF.type, OWL.Class)}
    expected = {
        BC.BusinessCapability,
        BC.BusinessCapabilityDescription, BC.BusinessCapabilityMap,
        BC.BusinessCapabilityAssessment, BC.BusinessCapabilityMaturityAssessment,
        BC.BusinessCapabilitySourcingAssessment,
        BC.BusinessCapabilityTargetStateSpecification
    }
    assert new_classes == expected, f"Unexpected new ontology classes: {new_classes ^ expected}"
    for cls in new_classes:
        for prop in (RDFS.label, SKOS.definition, RDFS.comment, SKOS.example):
            assert (cls, prop, None) in allg, (cls, prop)
    assert (BC.BusinessCapabilityMaturityAssessment, RDFS.subClassOf, CCO.ont00001010) in info
    assert (BC.BusinessCapabilityTargetStateSpecification, RDFS.subClassOf, CCO.ont00000965) in info
    assert (BC.BusinessCapabilityDescription, RDFS.subClassOf, CCO.ont00000853) in info
    for term in (EX.StrategicPlanningCapability, EX.BusinessModelGovernanceCapability,
                 EX.CustomerExperienceManagementCapability, EX.CompetitiveAnalysisCapability):
        assert (term, RDFS.seeAlso, BC.BusinessCapability) in align
        assert (term, RDF.type, OWL.Class) not in allg, "No redefinition of BPO class in this draft"
        assert not list(align.triples((term, RDFS.subClassOf, None)))
    assert (EX.CompetitiveAnalysisCapability, RDFS.seeAlso, EX.P19945) in align

    assert (URIRef("https://example.org/BusinessCapabilityOntology/example#UnexercisedPlanningCapability"),
            RDF.type, BC.BusinessCapability) in example
    assert not list(example.triples((None, BFO.BFO_0000054, None)))
    assert not list(example.triples((None, BFO.BFO_0000055, None)))
    assert not list(example.triples((None, CCO.ont00001898, None)))
    assert (BC.BusinessCapabilityBearerShape, RDF.type, SH.NodeShape) in sh

    object_preds = {p for (_, p, _) in allg if str(p).startswith(str(CCO)) or str(p).startswith(str(BFO))}
    allowed_preds = {CCO.ont00001954, CCO.ont00001889, CCO.ont00001808, CCO.ont00001811}
    assert object_preds == allowed_preds, ("An unreviewed BFO/CCO assertion predicate was used", object_preds - allowed_preds)
    print("\nPASS: 7 new classes (1 realist, 6 ICE), 0 new object properties, "
          "0 inferred or existential realizations, no BPO class redefinitions.")
    print("LIMIT: RDF syntax and draft-specific structural guards only. "
          "Full closure, SHACL execution, and OWL reasoner tests NOT RUN.")

if __name__ == "__main__":
    main()
