# SPDX-License-Identifier: MIT
"""The vocabulary schema's LinkML checks. Needs requirements-vocab.txt.

    .venv-vocab/Scripts/python tools/vocab/schema_check.py          # check
    .venv-vocab/Scripts/python tools/vocab/schema_check.py --write  # regenerate the JSON Schema

LinkML is adopted go-limited (docs/decisions/2026-10-24-p2-linkml-signoff.md):
one schema, gen-json-schema the only generator, linkml validate in CI.
This is that, and it runs only in the vocab CI job, because the main
suite does not install LinkML (requirements-vocab.txt is separate). It is
not a pytest test on purpose: a test that skips without LinkML would be a
pass in disguise in the main job (docs/process/PROCESS.md section 9), so
the check lives where its environment exists.

What it checks, in order:

  1. gen-json-schema is deterministic here: run from the repository root,
     run again, and run on a copy of the schema at another path and
     depth. Every output, CRLF normalised to LF, must be byte-identical.
  2. The committed config/vocab-schema.json equals that output (LF).
  3. `linkml validate` accepts the three authored files.
  4. `linkml validate` accepts a base document of each kind that
     exercises every slot, and rejects every case built from it to break
     one rule. Each case is named for its rule, and its mutation is
     asserted to have changed the document before it is run.

Printed: the raw and LF SHA-256 of the generator's output and its CR
count, so a run on Linux can be compared with the P2 trial's Windows
digests.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

import layout  # noqa: E402

SCHEMA_ID = "config.vocab-schema"
OUTPUT_ID = "generated.vocab-json-schema"
AUTHORED = (("vocab.metamodel", "MetamodelFile"),
            ("vocab.catalog", "CatalogFile"),
            ("vocab.agents", "AgentsFile"))

SOURCE = {"source": "SRC-OMG-03", "locator": "BACM 1.1, clause 7.2",
          "relation": "departs-from",
          "departure_note": "The BCO bearer is an organization only.",
          "claim": 1}
COMMON = {"sources": [SOURCE,
                      {"source": "SRC-GOV-04", "locator": "NAF v4.1",
                       "relation": "consistent-with"}],
          "drafted_by": "bcoa:claude-opus-5-5",
          "created": "2026-10-24T00:00:00Z",
          "authored_status": "Draft",
          "ratified_by": {
              "path": "docs/adr/ADR-003-controlled-vocabulary.md",
              "commit": "838573f1a22a12ebbc7e5933eecd6cdd1a6c52de",
              "sha256": "899ddc9c96fee90f2088f42693a37e8d8335e4ec9a2140a437f51e024cd02421"},
          "revises": "a" * 64,
          "change_note": ["Wording tightened."]}
BASES = {
    "MetamodelFile": {"version": 1, "concepts": [dict(
        COMMON, id="bcom:CapabilityMap", spec_row="ex:CapabilityMap",
        is_replaced_by="bcom:CapabilityAssessment")]},
    "CatalogFile": {"version": 1, "concepts": [dict(
        COMMON, id="bcoc:TreasuryManagement",
        pref_label=[{"value": "Treasury Management", "language": "en"}],
        definition="A business capability whose realization manages cash.",
        genus="cco:ont00000568", broader=["bcoc:FinancialManagement"],
        notation="10759", designates_class="bco:TreasuryManagement")]},
    "AgentsFile": {"version": 1, "agents": [
        {"id": "aaron-damiano", "type": "Person", "name": "Aaron Damiano"},
        {"id": "claude-opus-5-5", "type": "SoftwareAgent", "name": "Claude",
         "model": "claude-opus-5-5", "acted_on_behalf_of": "aaron-damiano"}]},
}


def first(doc):
    return doc["concepts"][0]


def m_set(cls, path, value):
    def apply(doc):
        target = doc
        for key in path[:-1]:
            target = target[key]
        target[path[-1]] = value
    return cls, apply


def m_del(cls, path):
    def apply(doc):
        target = doc
        for key in path[:-1]:
            target = target[key]
        del target[path[-1]]
    return cls, apply


C0 = ("concepts", 0)
#: name -> (root class, mutation). Each must be REJECTED.
CASES = {
    "metamodel-definition-authored": m_set("MetamodelFile", C0 + ("definition",), "A thing."),
    "metamodel-lifecycle-status-authored": m_set("MetamodelFile", C0 + ("lifecycle_status",), "Ratified"),
    "metamodel-owl-deprecated-authored": m_set("MetamodelFile", C0 + ("deprecated",), True),
    "metamodel-pref-label-authored": m_set("MetamodelFile", C0 + ("pref_label",), [{"value": "x", "language": "en"}]),
    "metamodel-without-spec-row": m_del("MetamodelFile", C0 + ("spec_row",)),
    "metamodel-spec-row-not-ex": m_set("MetamodelFile", C0 + ("spec_row",), "bco:CapabilityMap"),
    "metamodel-id-in-catalog": m_set("MetamodelFile", C0 + ("id",), "bcoc:CapabilityMap"),
    "authored-status-ratified": m_set("MetamodelFile", C0 + ("authored_status",), "Ratified"),
    "created-not-a-utc-timestamp": m_set("MetamodelFile", C0 + ("created",), "yesterday"),
    "drafted-by-not-an-agent-curie": m_set("MetamodelFile", C0 + ("drafted_by",), "Claude"),
    "sources-missing": m_del("MetamodelFile", C0 + ("sources",)),
    "sources-empty": m_set("MetamodelFile", C0 + ("sources",), []),
    "source-id-malformed": m_set("MetamodelFile", C0 + ("sources", 0, "source"), "SRC-OMG-3"),
    "source-without-locator": m_del("MetamodelFile", C0 + ("sources", 1, "locator")),
    "source-relation-unknown": m_set("MetamodelFile", C0 + ("sources", 1, "relation"), "inspired-by"),
    "departs-from-without-departure-note": m_del("MetamodelFile", C0 + ("sources", 0, "departure_note")),
    "departs-from-without-claim": m_del("MetamodelFile", C0 + ("sources", 0, "claim")),
    "ratification-short-commit": m_set("MetamodelFile", C0 + ("ratified_by", "commit"), "838573f"),
    "ratification-empty-file-digest": m_set("MetamodelFile", C0 + ("ratified_by", "sha256"), "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"),
    "ratification-path-outside-decisions": m_set("MetamodelFile", C0 + ("ratified_by", "path"), "notes/approval.md"),
    "ratification-record-digest-in-citation": m_set("MetamodelFile", C0 + ("ratified_by", "record_digest"), "b" * 64),
    "revises-not-a-digest": m_set("MetamodelFile", C0 + ("revises",), "previous"),
    "catalog-narrower-authored": m_set("CatalogFile", C0 + ("narrower",), ["bcoc:CashManagement"]),
    "catalog-without-definition": m_del("CatalogFile", C0 + ("definition",)),
    "catalog-without-genus": m_del("CatalogFile", C0 + ("genus",)),
    "catalog-notation-not-pcf-code": m_set("CatalogFile", C0 + ("notation",), "1.1.2"),
    "catalog-pref-label-without-language": m_del("CatalogFile", C0 + ("pref_label", 0, "language")),
    "catalog-broader-not-catalog": m_set("CatalogFile", C0 + ("broader",), ["bcom:CapabilityMap"]),
    "catalog-lifecycle-status-authored": m_set("CatalogFile", C0 + ("lifecycle_status",), "Draft"),
    "file-version-not-1": m_set("CatalogFile", ("version",), 2),
    "agent-type-unknown": m_set("AgentsFile", ("agents", 0, "type"), "Organization"),
    "software-agent-without-model": m_del("AgentsFile", ("agents", 1, "model")),
    "software-agent-without-principal": m_del("AgentsFile", ("agents", 1, "acted_on_behalf_of")),
}


def executable(name: str) -> str:
    scripts = Path(sys.executable).parent
    for candidate in (scripts / (name + ".exe"), scripts / name):
        if candidate.exists():
            return str(candidate)
    raise SystemExit("%s is not installed beside %s; install "
                     "requirements-vocab.txt" % (name, sys.executable))


def run(cmd, cwd) -> tuple[int, bytes]:
    proc = subprocess.run(cmd, cwd=str(cwd), capture_output=True)
    return proc.returncode, proc.stdout + proc.stderr


def generate(schema: Path, cwd: Path) -> bytes:
    proc = subprocess.run([executable("gen-json-schema"), str(schema)],
                          cwd=str(cwd), capture_output=True)
    if proc.returncode:
        raise SystemExit("gen-json-schema failed:\n"
                         + proc.stderr.decode("utf-8", "replace")[-3000:])
    return proc.stdout


def lf(data: bytes) -> bytes:
    return data.replace(b"\r\n", b"\n")


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def validate(schema: Path, cls: str, data: Path) -> tuple[int, str]:
    code, out = run([executable("linkml"), "validate", "-s", str(schema),
                     "-C", cls, str(data)], ROOT)
    return code, out.decode("utf-8", "replace").strip()


def main(argv=None) -> int:
    import yaml

    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args(argv)

    schema = layout.component(SCHEMA_ID).resolve()
    output = ROOT / layout.component(OUTPUT_ID).path
    failures = []

    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        raw = generate(schema, ROOT)
        print("gen-json-schema: %d bytes, %d CR, sha256 %s, LF sha256 %s"
              % (len(raw), raw.count(b"\r"), sha(raw), sha(lf(raw))))
        elsewhere = tmp / "a" / "deeper" / "checkout" / "config"
        elsewhere.mkdir(parents=True)
        shutil.copy2(schema, elsewhere / schema.name)
        runs = {"root": lf(raw), "root-again": lf(generate(schema, ROOT)),
                "copy-elsewhere": lf(generate(elsewhere / schema.name,
                                              elsewhere))}
        if len(set(runs.values())) != 1:
            failures.append("gen-json-schema is not deterministic: %s"
                            % {k: sha(v)[:16] for k, v in runs.items()})
        fresh = runs["root"]
        if args.write:
            output.write_bytes(fresh)
            print("wrote %s" % output)
        elif not output.is_file() or output.read_bytes() != fresh:
            failures.append("%s is not a fresh gen-json-schema output (LF); "
                            "run with --write" % output.name)

        for cid, cls in AUTHORED:
            code, text = validate(schema, cls, layout.component(cid).resolve())
            if code:
                failures.append("linkml validate rejects %s as %s: %s"
                                % (layout.component(cid).path, cls,
                                   text[-400:]))
            else:
                print("accepted  %s" % layout.component(cid).path)

        for cls, base in sorted(BASES.items()):
            path = tmp / ("base-%s.yaml" % cls)
            path.write_bytes(yaml.safe_dump(base, sort_keys=True).encode())
            code, text = validate(schema, cls, path)
            if code:
                failures.append("the base %s is rejected, so every case "
                                "built from it means nothing: %s"
                                % (cls, text[-400:]))
            else:
                print("accepted  base %s" % cls)

        for name, (cls, mutate) in sorted(CASES.items()):
            doc = copy.deepcopy(BASES[cls])
            mutate(doc)
            assert doc != BASES[cls], "mutation %s did not apply" % name
            path = tmp / ("case-%s.yaml" % name)
            path.write_bytes(yaml.safe_dump(doc, sort_keys=True).encode())
            code, text = validate(schema, cls, path)
            if code == 0:
                failures.append("case %s was accepted; the schema does not "
                                "carry that rule" % name)
            else:
                last = [line for line in text.splitlines() if line.strip()]
                print("rejected  %-42s %s" % (name, (last[-1] if last else "")[:110]))

    for failure in failures:
        print("FAILURE  " + failure)
    print("%d case(s) rejected of %d; %d failure(s)"
          % (len(CASES) - sum(f.startswith("case ") for f in failures),
             len(CASES), len(failures)))
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
