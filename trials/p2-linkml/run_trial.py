"""P2 LinkML trial: measure, don't assume.

    .venv-linkml/Scripts/python trials/p2-linkml/run_trial.py --out <dir>

Run with the trial venv's interpreter (requirements-linkml-trial.txt). It
writes every generated file and a results.json under --out, which must be
OUTSIDE the repository: nothing generated here is committed, and the
report (docs/trials/2026-10-p2-linkml.md) records digests instead.

What it measures:

  determinism   gen-json-schema, gen-shacl and gen-owl, each run in five
                configurations: twice from this checkout (hash seed
                unset), once from a copy of the trial directory at a
                different path and depth, and twice with a fixed
                PYTHONHASHSEED (0 and 4242). SHA-256 of every output; a
                byte-diff summary for any pair that differs.
  blank nodes   distinct blank nodes in each RDF output, and in the RDF
                linkml-convert makes of the sample terms.
  validation    `linkml validate` over the samples (must accept) and
                every fixture (must reject), with the message it gives.
  gen-shacl     the generated shapes run with pyshacl over the RDF of the
                same samples and fixtures: which defects the generated
                SHACL catches at all.
"""

from __future__ import annotations

import argparse
import difflib
import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCHEMA_NAME = "bco_vocab_trial.yaml"
ROOT_CLASS = "ConceptCollection"
SCRIPTS = Path(sys.executable).parent

#: name -> (executable, extra args, output suffix). Output is taken from
#: stdout as raw bytes: that is what a build step redirecting the command
#: would publish.
GENERATORS = {
    "gen-json-schema": ("gen-json-schema", [], ".schema.json"),
    "gen-shacl": ("gen-shacl", [], ".shacl.ttl"),
    "gen-owl": ("gen-owl", [], ".owl.ttl"),
}
RDF_OUTPUTS = ("gen-shacl", "gen-owl")


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def env_with(seed):
    env = dict(os.environ)
    env.pop("PYTHONHASHSEED", None)
    if seed is not None:
        env["PYTHONHASHSEED"] = str(seed)
    return env


def tool(name: str) -> str:
    for candidate in (SCRIPTS / (name + ".exe"), SCRIPTS / name):
        if candidate.exists():
            return str(candidate)
    raise SystemExit("not installed in this venv: " + name)


def run(cmd, cwd, env):
    proc = subprocess.run(cmd, cwd=cwd, env=env, capture_output=True)
    return proc.returncode, proc.stdout, proc.stderr


def generate(schema_dir: Path, out: Path, seed) -> dict:
    out.mkdir(parents=True, exist_ok=True)
    found = {}
    for name, (exe, extra, suffix) in GENERATORS.items():
        cmd = [tool(exe), *extra, SCHEMA_NAME]
        code, stdout, stderr = run(cmd, schema_dir, env_with(seed))
        if code != 0:
            raise SystemExit("%s failed (%d):\n%s" % (name, code,
                                                       stderr.decode()[-3000:]))
        (out / (name + suffix)).write_bytes(stdout)
        found[name] = {
            "sha256": sha256(stdout),
            "bytes": len(stdout),
            "cr_bytes": stdout.count(b"\r"),
            "sha256_lf": sha256(stdout.replace(b"\r\n", b"\n")),
            "file": str(out / (name + suffix)),
        }
    return found


def diff_summary(a: bytes, b: bytes, limit=12) -> list[str]:
    la = a.decode("utf-8", "replace").splitlines()
    lb = b.decode("utf-8", "replace").splitlines()
    lines = [line for line in difflib.unified_diff(la, lb, lineterm="", n=0)
             if not line.startswith(("---", "+++", "@@"))]
    return ["%d changed lines" % len(lines)] + lines[:limit]


def blank_nodes(path: Path, fmt="turtle") -> int:
    import rdflib

    graph = rdflib.Graph()
    graph.parse(path, format=fmt)
    nodes = set()
    for triple in graph:
        nodes.update(t for t in triple if isinstance(t, rdflib.BNode))
    return len(nodes)


def rule_of(path: Path) -> str:
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("# rule: "):
            return line[len("# rule: "):]
    return ""


def linkml_validate(data: Path) -> dict:
    cmd = [tool("linkml"), "validate", "-s", str(HERE / SCHEMA_NAME),
           "-C", ROOT_CLASS, str(data)]
    code, stdout, stderr = run(cmd, HERE, env_with(0))
    text = (stdout + stderr).decode("utf-8", "replace")
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return {"exit": code, "messages": lines[:8]}


def to_rdf(data: Path, out: Path, schema: Path) -> tuple[int, str]:
    # --no-validate: the point is to hand defective data to the generated
    # SHACL, so the converter must not refuse it first.
    cmd = [tool("linkml-convert"), "--no-validate", "-s", str(schema), "-C",
           ROOT_CLASS, "-t", "ttl", "-o", str(out), str(data)]
    code, stdout, stderr = run(cmd, HERE, env_with(0))
    return code, (stdout + stderr).decode("utf-8", "replace")[-600:]


def generated_shacl(data_ttl: Path, shapes: Path) -> dict:
    import rdflib
    from pyshacl import validate

    try:
        conforms, results, _ = validate(
            data_graph=rdflib.Graph().parse(data_ttl, format="turtle"),
            shacl_graph=rdflib.Graph().parse(shapes, format="turtle"),
            inference="none", advanced=True)
    except Exception as exc:  # the generated shapes may not load at all
        return {"conforms": None, "error": "%s: %s" % (
            type(exc).__name__, str(exc).splitlines()[0][:200])}
    SH = rdflib.Namespace("http://www.w3.org/ns/shacl#")
    found = []
    for result in results.subjects(rdflib.RDF.type, SH.ValidationResult):
        path = results.value(result, SH.resultPath)
        comp = results.value(result, SH.sourceConstraintComponent)
        msg = results.value(result, SH.resultMessage)
        found.append("%s %s: %s" % (
            str(comp).rsplit("#", 1)[-1] if comp else "?",
            str(path).rsplit("#", 1)[-1].rsplit("/", 1)[-1] if path else "-",
            (str(msg) if msg else "")[:120]))
    return {"conforms": bool(conforms), "results": sorted(set(found))[:6],
            "count": len(found)}


def shacl_features(path: Path) -> dict:
    import rdflib

    SH = rdflib.Namespace("http://www.w3.org/ns/shacl#")
    g = rdflib.Graph().parse(path, format="turtle")
    property_shapes = set(g.objects(None, SH.property))
    return {
        "node_shapes": len(set(g.subjects(rdflib.RDF.type, SH.NodeShape))),
        "property_shapes": len(property_shapes),
        "sh_message": len(set(g.subject_objects(SH.message))),
        "property_shapes_with_message": sum(
            1 for p in property_shapes if (p, SH.message, None) in g),
        "sparql_targets": len(set(g.subjects(rdflib.RDF.type, SH.SPARQLTarget))),
        "sparql_constraints": len(set(g.objects(None, SH.sparql))),
        "target_class": len(set(g.subject_objects(SH.targetClass))),
        "severity_declared": len(set(g.subject_objects(SH.severity))),
        "closed": len(set(g.subject_objects(SH.closed))),
        "triples": len(g),
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args(argv)
    out = args.out.resolve()
    repo = HERE.parents[1]
    if repo in out.parents or out == repo:
        raise SystemExit("--out must be outside the repository")
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)

    import linkml
    from importlib.metadata import version

    results = {"versions": {p: version(p) for p in (
        "linkml", "linkml-runtime", "rdflib", "pyshacl", "PyYAML",
        "pydantic", "jsonschema")},
        "python": sys.version.split()[0],
        "schema_sha256": sha256((HERE / SCHEMA_NAME).read_bytes())}

    # --- determinism ---------------------------------------------------
    copy_dir = out / "elsewhere" / "a" / "deeper" / "checkout" / "p2-linkml"
    shutil.copytree(HERE, copy_dir,
                    ignore=shutil.ignore_patterns("__pycache__"))
    configs = [
        ("run1-checkout-seed-unset", HERE, None),
        ("run2-checkout-seed-unset", HERE, None),
        ("run3-copy-elsewhere-seed-unset", copy_dir, None),
        ("run4-checkout-seed-0", HERE, 0),
        ("run5-checkout-seed-4242", HERE, 4242),
        ("run6-checkout-seed-0-again", HERE, 0),
    ]
    runs = {}
    for label, where, seed in configs:
        runs[label] = generate(where, out / "gen" / label, seed)
    results["determinism"] = runs

    diffs = {}
    first = configs[0][0]
    for name in GENERATORS:
        base = Path(runs[first][name]["file"]).read_bytes()
        for label, _, _ in configs[1:]:
            other = Path(runs[label][name]["file"]).read_bytes()
            if other != base:
                diffs["%s: %s vs %s" % (name, first, label)] = diff_summary(
                    base, other)
    results["differences"] = diffs

    # Same graph, different bytes? Isomorphism says whether a difference
    # is serialisation order (blank-node labels) or content.
    from rdflib import Graph
    from rdflib.compare import isomorphic

    iso = {}
    for name in RDF_OUTPUTS:
        base_graph = Graph().parse(runs[first][name]["file"], format="turtle")
        iso[name] = {label: isomorphic(base_graph, Graph().parse(
            runs[label][name]["file"], format="turtle"))
            for label, _, _ in configs[1:]}
    results["isomorphic_to_run1"] = iso
    # Does a fixed hash seed at least fix the graph? Runs 4 and 6 share
    # seed 0; run 1 and 2 share an unset (random) seed.
    pairs = {}
    for a, b in ((configs[3][0], configs[5][0]), (configs[0][0], configs[1][0])):
        for name in RDF_OUTPUTS:
            pairs["%s: %s vs %s" % (name, a, b)] = isomorphic(
                Graph().parse(runs[a][name]["file"], format="turtle"),
                Graph().parse(runs[b][name]["file"], format="turtle"))
    results["isomorphic_pairs"] = pairs

    # --- blank nodes in generated RDF ----------------------------------
    results["blank_nodes"] = {
        name: blank_nodes(Path(runs[first][name]["file"]))
        for name in RDF_OUTPUTS}

    # --- a variant with distinct class URIs ----------------------------
    # ADR-003 types both concept kinds skos:Concept. gen-shacl keys a node
    # shape by class_uri, so the two kinds (and the abstract base) merge
    # into one shape. The variant drops those class_uri lines so that each
    # class gets its own shape, to measure what gen-shacl catches when the
    # merge is out of the way. It is derived here, never committed.
    variant_dir = out / "variant"
    variant_dir.mkdir()
    text = (HERE / SCHEMA_NAME).read_bytes()
    line = b"    class_uri: skos:Concept\n"
    assert text.count(line) == 3, "variant mutation would not apply"
    variant = text.replace(line, b"")
    assert variant != text
    (variant_dir / SCHEMA_NAME).write_bytes(variant)
    code, stdout, stderr = run([tool("gen-shacl"), SCHEMA_NAME], variant_dir,
                               env_with(0))
    assert code == 0, stderr.decode()[-2000:]
    variant_shapes = variant_dir / "gen-shacl.variant.shacl.ttl"
    variant_shapes.write_bytes(stdout)
    results["variant_gen_shacl_sha256"] = sha256(stdout)
    results["blank_nodes"]["gen-shacl (variant)"] = blank_nodes(variant_shapes)

    # --- validation ----------------------------------------------------
    shapes = Path(runs[first]["gen-shacl"]["file"])
    cases = ([("accept", p) for p in sorted((HERE / "samples").glob("*.yaml"))]
             + [("reject", p) for p in sorted((HERE / "fixtures").glob("*.yaml"))])
    validation = []
    for expect, path in cases:
        row = {"case": path.relative_to(HERE).as_posix(), "expect": expect,
               "rule": rule_of(path)}
        row["linkml_validate"] = linkml_validate(path)
        ttl = out / "rdf" / (path.stem + ".ttl")
        ttl.parent.mkdir(parents=True, exist_ok=True)
        code, text = to_rdf(path, ttl, HERE / SCHEMA_NAME)
        row["convert_exit"] = code
        if code == 0 and ttl.exists():
            row["data_blank_nodes"] = blank_nodes(ttl)
            row["gen_shacl"] = generated_shacl(ttl, shapes)
        else:
            row["convert_error"] = text
        vttl = out / "rdf-variant" / (path.stem + ".ttl")
        vttl.parent.mkdir(parents=True, exist_ok=True)
        code, text = to_rdf(path, vttl, variant_dir / SCHEMA_NAME)
        if code == 0 and vttl.exists():
            row["gen_shacl_variant"] = generated_shacl(vttl, variant_shapes)
        else:
            row["variant_convert_error"] = text
        validation.append(row)
    results["validation"] = validation

    # --- probes --------------------------------------------------------
    probe = HERE / "probes" / "probe_value_presence.yaml"
    results["probe_value_presence"] = {}
    for data in sorted((HERE / "probes").glob("probe_value_presence_*.yaml")):
        cmd = [tool("linkml"), "validate", "-s", str(probe), "-C",
               "Container", str(data)]
        code, stdout, stderr = run(cmd, HERE, env_with(0))
        text = (stdout + stderr).decode("utf-8", "replace").strip()
        results["probe_value_presence"][data.name] = {
            "exit": code, "output": text.rsplit("] ", 1)[-1][:300]}

    conditions = HERE / "probes" / "probe_conditions.yaml"
    code, stdout, stderr = run(
        [tool("linkml"), "validate", "-s", str(conditions), "-C", "Container",
         str(HERE / "probes" / "probe_conditions_data.yaml")], HERE, env_with(0))
    text = (stdout + stderr).decode("utf-8", "replace").strip()
    results["probe_conditions"] = {"validate_exit": code,
                                   "validate_output": text.rsplit("] ", 1)[-1][:300]}
    code, stdout, stderr = run([tool("gen-shacl"), conditions.name],
                               conditions.parent, env_with(0))
    lines = stderr.decode("utf-8", "replace").strip().splitlines()
    results["probe_conditions"].update({
        "gen_shacl_exit": code,
        "gen_shacl_error": lines[-1][:300] if (code and lines) else None})

    # gen-owl with the schema's own slot_uri / class_uri mappings: does
    # it write axioms about other people's terms (SKOS, PROV, DC, OWL)?
    code, stdout, stderr = run([tool("gen-owl"), "--no-use-native-uris",
                                SCHEMA_NAME], HERE, env_with(0))
    foreign = {}
    if code == 0:
        import rdflib
        g = rdflib.Graph().parse(data=stdout.decode("utf-8"), format="turtle")
        for subject in set(g.subjects()):
            text = str(subject)
            for ns in ("http://www.w3.org/2004/02/skos/core#",
                       "http://www.w3.org/ns/prov#", "http://purl.org/dc/terms/",
                       "http://www.w3.org/2002/07/owl#"):
                if text.startswith(ns):
                    foreign[text] = sorted(
                        "%s %s" % (str(p).rsplit("#", 1)[-1].rsplit("/", 1)[-1],
                                   str(o).rsplit("#", 1)[-1][:40])
                        for p, o in g.predicate_objects(subject)
                        if not isinstance(o, rdflib.BNode))[:4]
    results["gen_owl_mapped_uris"] = {"exit": code,
                                      "foreign_subjects": foreign}

    # --- generated SHACL versus the hand-written shapes ----------------
    results["shacl_features"] = {
        "generated": shacl_features(shapes),
        "generated_variant": shacl_features(variant_shapes),
        "hand_written_wellformedness": shacl_features(
            repo / "shapes" / "wellformedness_shapes.ttl"),
    }

    (out / "results.json").write_bytes(
        json.dumps(results, indent=2, sort_keys=True).encode("utf-8") + b"\n")
    print(json.dumps({k: results[k] for k in (
        "versions", "blank_nodes", "shacl_features")}, indent=2))
    for name in GENERATORS:
        digests = {label: runs[label][name]["sha256"][:16] for label in runs}
        print(name, "identical" if len(set(digests.values())) == 1
              else "DIFFERS", digests)
    for row in validation:
        lv = row["linkml_validate"]["exit"]
        gs = row.get("gen_shacl", {}).get("conforms")
        gv = row.get("gen_shacl_variant", {}).get("conforms")
        print("%-50s %-6s validate=%s gen-shacl=%s variant=%s"
              % (row["case"], row["expect"], lv, gs, gv))
    return 0


if __name__ == "__main__":
    sys.exit(main())
