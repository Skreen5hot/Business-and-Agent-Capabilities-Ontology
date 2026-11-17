# SPDX-License-Identifier: MIT
"""Run the pinned reasoners over the ontology (Stage 05 gates S05-D, S05-D2).

    python tools/ontology/reason.py               # S05-D: ELK; SKIP if absent
    python tools/ontology/reason.py --hermit      # also HermiT (S05-D2)
    python tools/ontology/reason.py --checkpoint  # both; absence is a FAIL
    python tools/ontology/reason.py --fetch       # download the pinned jar
    python tools/ontology/reason.py --complete    # S06-U2: complete BFO and CCO
    python tools/ontology/reason.py --complete --record src/06_knowledge_graph/upstream-conformance.json

WHAT IS REASONED OVER

The ontology modules (layout role `ontology-module`) merged with the
vendored extracts, through ROBOT's `merge` and `reason`. Not the vocabulary,
which is SKOS and asserts no OWL class axioms. ROBOT fails a `reason` that
finds the input inconsistent or a class unsatisfiable; that failure is this
tool's FAIL.

THE COMPLETE CLOSURE (S06-U2)

With --complete, the BFO and CCO extracts are replaced by the complete
files at their pins (config/upstream-sources.yaml), fetched through
vendor_upstream.py's digest-checked fetch into its cache. BPO stays its
extract: the Stage 05 import boundary (standard section 4; RP-3) excludes
the BPO modules whose capability assertions the BCO does not admit, so no
complete-BPO conformance is claimed, and the record says so. Both reasoners
run, falsified as below, and an absent one is a FAIL. --record writes what
was loaded (each file, its role and SHA-256), the versions that ran and the
results, with no timestamp, so the same inputs write the same bytes.

EVERY RUN IS FALSIFIED

A reasoner that never fails proves nothing (D5-2: positive and negative
evidence for each rule). So each reasoner also runs on the same input plus,
in turn:

  unsatisfiable  one class under bco:BusinessCapability, and so under
                 disposition, and under role, which the BFO extract declares
                 disjoint from disposition;
  CAP-16         the specification's fixture: a real index member declared
                 disjoint from its own parent;
  inconsistent   (HermiT) an individual of the unsatisfiable class;
  CAP-10         (HermiT) a class defined as the intersection of two written
                 capability classes, which must come back as a candidate.

Each must be rejected, or detected, for the reason built in, as ROBOT
reports it. If one is not, the run is not evidence, and the result is a FAIL
whatever the real input did.

CAP-10 CANDIDATES

HermiT's classification is compared with what is asserted: any
rdfs:subClassOf between two BCO classes that is inferred and not asserted is
reported as a CAP-10 candidate for review. None is asserted from it.

RESULTS

PASS, FAIL or SKIP per reasoner, with the ROBOT and Java versions that ran.
Exit 1 on a FAIL; exit 0 on PASS or SKIP. At a checkpoint (--checkpoint) a
SKIP is a FAIL: a skipped or unavailable reasoner is not a passing
checkpoint result (D5-2).
"""

from __future__ import annotations

import argparse
import hashlib
import shutil
import subprocess
import sys
import tempfile
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))

import layout  # noqa: E402

PINS = "config/reasoner-pins.yaml"
BCO = "https://fandaws.com/ontology/bco#"
OBO = "http://purl.obolibrary.org/obo/"
RDFS_SUBCLASS = "http://www.w3.org/2000/01/rdf-schema#subClassOf"

#: Appended to the real input to make one class unsatisfiable.
UNSATISFIABLE = """
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix owl:  <http://www.w3.org/2002/07/owl#> .
@prefix obo:  <http://purl.obolibrary.org/obo/> .
@prefix bco:  <https://fandaws.com/ontology/bco#> .
bco:ReasonerFalsificationCase a owl:Class ;
    rdfs:subClassOf bco:BusinessCapability , obo:BFO_0000023 .
"""
#: ... and, for HermiT, an instance of it, making the whole input inconsistent.
INCONSISTENT = UNSATISFIABLE + """
bco:reasoner_falsification_instance a owl:NamedIndividual ,
    bco:ReasonerFalsificationCase .
"""


class Refused(SystemExit):
    pass


def pins() -> dict:
    import yaml

    root = layout.repository_root()
    data = yaml.safe_load((root / PINS).read_bytes().decode("utf-8"))
    robot = data.get("robot") or {}
    for key in ("url", "sha256", "bytes", "cache", "commit",
                "reports_version"):
        if not robot.get(key):
            raise Refused("%s declares no robot.%s" % (PINS, key))
    if robot["commit"] not in robot["licence"]["url"]:
        raise Refused("ROBOT's licence url does not name the pinned commit")
    return data


def jar_path(data: dict) -> Path:
    return layout.repository_root() / data["robot"]["cache"]


def jar_ok(data: dict) -> bool:
    path = jar_path(data)
    if not path.is_file():
        return False
    got = hashlib.sha256(path.read_bytes()).hexdigest()
    if got != data["robot"]["sha256"]:
        raise Refused("%s digests to %s, not the pinned %s; delete it and "
                      "run --fetch" % (path, got[:16],
                                       data["robot"]["sha256"][:16]))
    return True


def fetch(data: dict) -> Path:
    robot, path = data["robot"], jar_path(data)
    if jar_ok(data):
        return path
    path.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(robot["url"], timeout=600) as response:
        payload = response.read()
    if len(payload) != robot["bytes"] or \
            hashlib.sha256(payload).hexdigest() != robot["sha256"]:
        raise Refused("%s served %d bytes that are not the pinned jar"
                      % (robot["url"], len(payload)))
    path.write_bytes(payload)
    return path


def java() -> str | None:
    return shutil.which("java")


def versions(data: dict) -> dict:
    out = {"java": None, "robot": None}
    exe = java()
    if exe:
        run = subprocess.run([exe, "-version"], capture_output=True)
        out["java"] = (run.stderr or run.stdout).decode("utf-8", "replace") \
            .splitlines()[0].strip()
        run = subprocess.run([exe, "-jar", str(jar_path(data)), "--version"],
                             capture_output=True)
        out["robot"] = run.stdout.decode("utf-8", "replace").strip()
    return out


def inputs() -> list[Path]:
    modules = [c.resolve() for c in layout.components("ontology-module")]
    return modules + list(layout.vendored_files())


#: The complete files S06-U2 loads in place of the extracts.
COMPLETE_ROLES = {"bfo": "complete BFO at its pin",
                  "cco": "complete CCO (merged) at its pin"}
BOUNDARY = ("BPO is loaded as its extract only. The Stage 05 import boundary "
            "(docs/standards/stage-05-ontology.md, section 4; RP-3) excludes "
            "the BPO modules whose capability assertions the BCO does not "
            "admit, so conformance with the complete BPO is not claimed.")


def vendor_upstream():
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "vendor_upstream_for_reason", HERE / "vendor_upstream.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def complete_closure() -> list[dict]:
    """S06-U2's input: the BCO modules, the complete pinned BFO and CCO,
    and the BPO extract. Each item has its path, role and SHA-256."""
    root = layout.repository_root()
    vu = vendor_upstream()
    cache = root / vu.CACHE
    items = []
    for module in layout.components("ontology-module"):
        path = module.resolve()
        items.append({"path": path.relative_to(root).as_posix(),
                      "role": "BCO module",
                      "sha256": hashlib.sha256(path.read_bytes()).hexdigest()})
    by_id = {s["id"]: s for s in vu.sources()}
    for source_id, role in COMPLETE_ROLES.items():
        source = by_id[source_id]
        vu.fetch(source, cache)            # digest-checked; refuses others
        path = cache / (source_id + ".ttl")
        items.append({"path": path.relative_to(root).as_posix(),
                      "role": role, "url": source["url"],
                      "commit": source["commit"], "sha256": source["sha256"]})
    for path in layout.vendored_files():
        resolved = path.resolve()
        if "/vendor/bpo/" in resolved.as_posix():
            items.append({"path": resolved.relative_to(root).as_posix(),
                          "role": "BPO extract (import boundary)",
                          "sha256": hashlib.sha256(
                              resolved.read_bytes()).hexdigest()})
    return items


def robot_reason(data: dict, reasoner: str, files: list[Path],
                 extra: str | None, out: Path) -> tuple[bool, str]:
    """(passed, ROBOT's last lines). `extra` is appended Turtle."""
    command = [java(), "-jar", str(jar_path(data)), "merge"]
    paths = list(files)
    if extra is not None:
        case = out.parent / ("falsification-%s.ttl" % reasoner)
        case.write_bytes(extra.encode("utf-8"))
        paths.append(case)
    for path in paths:
        command += ["--input", str(path)]
    command += ["reason", "--reasoner", reasoner, "--output", str(out)]
    run = subprocess.run(command, capture_output=True)
    text = (run.stdout + run.stderr).decode("utf-8", "replace").strip()
    return run.returncode == 0, "\n".join(text.splitlines()[-4:])


def cap10_candidates(asserted: list[Path], reasoned: Path) -> list:
    import rdflib

    def bco_subclass(graph):
        return {(str(s), str(o)) for s, o in graph.subject_objects(
                    rdflib.URIRef(RDFS_SUBCLASS))
                if isinstance(o, rdflib.URIRef)
                and str(s).startswith(BCO) and str(o).startswith(BCO)}

    before = rdflib.Graph()
    for path in asserted:
        before.parse(path, format="turtle")
    after = rdflib.Graph().parse(reasoned, format="turtle")
    return sorted(bco_subclass(after) - bco_subclass(before)
                  - {(s, s) for s, _ in bco_subclass(after)})


def index_member_and_parent(files: list[Path]) -> tuple[str, str]:
    """A real index member and one of its named parents, for the CAP-16
    case. The first in sorted order, so the case is the same every run."""
    import rdflib

    graph = rdflib.Graph()
    for path in files:
        graph.parse(path, format="turtle")
    enables = rdflib.URIRef("https://fandaws.com/ontology/bpo#enablesProcess")
    members = sorted({str(o) for o in graph.objects(None, enables)})
    for member in members:
        parents = sorted(str(o) for o in graph.objects(
            rdflib.URIRef(member), rdflib.URIRef(RDFS_SUBCLASS))
            if isinstance(o, rdflib.URIRef))
        if parents:
            return member, parents[0]
    raise Refused("no index member with a named parent to build CAP-16 on")


def cap16_case(member: str, parent: str) -> str:
    """CAP-16's fixture, as the specification states it: an index member
    declared disjoint from its own parent."""
    return ("<%s> <http://www.w3.org/2002/07/owl#disjointWith> <%s> .\n"
            % (member, parent))


#: CAP-10's fixture: a class defined as the intersection of two written
#: capability classes is under each of them, and that must come back as an
#: inferred, unasserted subsumption between BCO classes. (An equivalence
#: would not do: equivalent classes share a node, and the reasoner reports
#: no subclass link between them.)
CAP10_CASE = """
@prefix owl:  <http://www.w3.org/2002/07/owl#> .
@prefix bco:  <https://fandaws.com/ontology/bco#> .
bco:ReasonerCap10Case a owl:Class ;
    owl:equivalentClass [ a owl:Class ;
        owl:intersectionOf ( bco:CashManagement bco:PaymentProcessing ) ] .
"""


def run_reasoner(data: dict, reasoner: str, work: Path,
                 files: list[Path] | None = None) -> dict:
    files = inputs() if files is None else files
    out = work / ("reasoned-%s.ttl" % reasoner)
    passed, tail = robot_reason(data, reasoner, files, None, out)
    result = {"reasoner": reasoner, "input_files": len(files),
              "real_input": "PASS" if passed else "FAIL",
              "detail": tail if not passed else "", "cases": {}}
    ok = passed

    def falsify(name: str, extra: str, expect: str) -> None:
        """The case must be rejected, and for the reason built in: a
        rejection for any other cause (a parse error in the case, say) is
        not evidence."""
        nonlocal ok
        case_dir = work / ("%s-%s" % (reasoner, name))
        case_dir.mkdir()
        accepted, why = robot_reason(data, reasoner, files, extra,
                                     case_dir / "out.ttl")
        rejected = not accepted and expect in why
        result["cases"][name] = "rejected" if rejected else "NOT REJECTED"
        if not rejected:
            ok = False
            result["detail"] += ("the %s case was not rejected as expected, "
                                 "so this run is not evidence: %s\n"
                                 % (name, why))

    falsify("unsatisfiable", UNSATISFIABLE,
            "unsatisfiable: %sReasonerFalsificationCase" % BCO)
    member, parent = index_member_and_parent(files)
    falsify("CAP-16", cap16_case(member, parent), "unsatisfiable: %s" % member)
    if reasoner == "HermiT":
        falsify("inconsistent", INCONSISTENT, "ontology is inconsistent")
        if passed:
            result["cap10_candidates"] = cap10_candidates(files, out)
        # CAP-10's own fixture: the comparison must see an inferred link.
        case_dir = work / "HermiT-CAP-10"
        case_dir.mkdir()
        accepted, _ = robot_reason(data, reasoner, files, CAP10_CASE,
                                   case_dir / "out.ttl")
        seen = accepted and (BCO + "ReasonerCap10Case",
                             BCO + "CashManagement") in cap10_candidates(
            files, case_dir / "out.ttl")
        result["cases"]["CAP-10"] = "detected" if seen else "NOT DETECTED"
        ok = ok and seen
    result["result"] = "PASS" if ok else "FAIL"
    return result


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--fetch", action="store_true",
                    help="download the pinned ROBOT jar, then run")
    ap.add_argument("--hermit", action="store_true",
                    help="also run HermiT (S05-D2)")
    ap.add_argument("--checkpoint", action="store_true",
                    help="run ELK and HermiT; an absent reasoner is a FAIL")
    ap.add_argument("--complete", action="store_true",
                    help="S06-U2: ELK and HermiT over the modules with the "
                    "complete pinned BFO and CCO; an absent reasoner is a FAIL")
    ap.add_argument("--record", metavar="PATH",
                    help="with --complete, write the closure and the results")
    args = ap.parse_args(argv)
    if args.record and not args.complete:
        ap.error("--record needs --complete")
    if args.complete:
        args.checkpoint = True
    data = pins()
    if args.fetch:
        fetch(data)
    wanted = ["ELK"] + (["HermiT"] if args.hermit or args.checkpoint else [])

    if not java() or not jar_ok(data):
        why = "no java on PATH" if not java() else \
            "the pinned ROBOT jar is not at %s (run --fetch)" % \
            data["robot"]["cache"]
        verdict = "FAIL" if args.checkpoint else "SKIP"
        for name in wanted:
            print("  %-7s %s: %s" % (name, verdict, why))
        if args.checkpoint:
            print("  checkpoint: a skipped or unavailable reasoner is not a "
                  "passing result")
            return 1
        return 0

    seen = versions(data)
    if seen["robot"] != data["robot"]["reports_version"]:
        raise Refused("the jar reports %r, not %r"
                      % (seen["robot"], data["robot"]["reports_version"]))
    print("  %s; %s" % (seen["robot"], seen["java"]))
    closure = complete_closure() if args.complete else None
    files = None
    if closure is not None:
        root = layout.repository_root()
        files = [root / item["path"] for item in closure]
        print("  complete closure, %d file(s):" % len(files))
        for item in closure:
            print("    %-33s %s  %s" % (item["role"], item["sha256"][:16],
                                       item["path"]))
        print("  " + BOUNDARY)
    results = []
    failed = False
    with tempfile.TemporaryDirectory(prefix="bco-reason-") as tmp:
        for name in wanted:
            result = run_reasoner(data, name, Path(tmp), files)
            results.append(result)
            failed = failed or result["result"] != "PASS"
            print("  %-7s %s  real input %s over %d file(s); falsification: %s"
                  % (name, result["result"], result["real_input"],
                     result["input_files"],
                     ", ".join("%s %s" % kv for kv in result["cases"].items())))
            if "cap10_candidates" in result:
                found = result["cap10_candidates"]
                print("          CAP-10 candidates (inferred, not asserted, "
                      "between BCO classes): %d" % len(found))
                for sub, sup in found:
                    print("            %s  <  %s" % (sub[len(BCO):],
                                                     sup[len(BCO):]))
            if result["detail"]:
                print("          " + result["detail"].replace(
                    "\n", "\n          "))
    if args.record:
        write_record(Path(args.record), seen, closure, results)
    return 1 if failed else 0


def write_record(path: Path, seen: dict, closure: list, results: list) -> None:
    """S06-U2's record: what was loaded and what each reasoner found."""
    import json
    record = {
        "format": 1,
        "check": "S06-U2 (docs/standards/stage-06-knowledge-graph.md, section 4)",
        "generator": "tools/ontology/reason.py --complete --record",
        "robot": seen["robot"],
        "java": seen["java"],
        "claim": ("The BCO modules are consistent, and every class satisfiable, "
                  "together with the complete BFO and CCO at their pins."),
        "not_claimed": BOUNDARY,
        "closure": closure,
        "results": [],
    }
    for r in results:
        entry = {k: r[k] for k in ("reasoner", "result", "real_input", "cases")}
        if "cap10_candidates" in r:
            entry["cap10_candidates"] = r["cap10_candidates"]
        record["results"].append(entry)
    path.write_bytes((json.dumps(record, indent=2, ensure_ascii=False) + "\n")
                     .encode("utf-8"))
    print("  recorded %s" % path.as_posix())


if __name__ == "__main__":
    raise SystemExit(main())
