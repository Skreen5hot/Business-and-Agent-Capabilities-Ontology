# SPDX-License-Identifier: MIT
"""CQ-11 by the review-record method (decision of 2026-11-15, B-4).

    python tools/ontology/review_records.py   # print the answer per class

"Which acts develop capability C, as distinct from realizing it?" No
ontology relation records development (OI-4, open), and no property is
authorized. The specification names the CAP-06 review records as the interim
source. For the written classes those records are the signed G1-T records,
read here from git at the commit whose bytes were signed, and checked
against the SHA-256 the signature names (the tranche record's
`signed_record`), never from the working tree:

  tranche 2   each class's **Excluded** table: the rows coded Q5, "It governs
              or develops the capability rather than exercising it", with
              their reasons (G1-T question 5, CD5, CAP-06)
  tranche 1   each record's G1-T question 5 row ("Exercise, not
              development"): the acts its evidence names as out

This is a review-record answer, not an OWL inference and not a SPARQL answer
from the capability module (the CQ-11 exception the decision approves). It
reports what the records say, and only that:

  - An act it names is development or governance evidence for C, recorded
    when C's index was reviewed. It is not in C's realization index.
  - A class with no such row has none recorded. That is never a finding
    that no act can develop the capability.
  - Q5 joins "governs" and "develops", and so does this answer; the records
    do not separate them.

Act names, which derive from APQC PCF element names, are not printed; the
act IRIs and the review reasons are.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(HERE))

import formalize  # noqa: E402

#: A tranche 2 exclusion row: act, via, code, reason.
EXCLUDED_ROW = re.compile(
    r"^\| `bpo:(P\d+)` \| [^|]+ \| (\w+) \| (.+?) \|$", re.M)
#: A tranche 1 question 5 row: its evidence cell.
QUESTION_5 = re.compile(
    r"^\| 5 \| \*\*Exercise, not development\.\*\*[^|]*\| [^|]+ \| (.+?) \|$",
    re.M)
ACT = re.compile(r"`(P\d+)`")

NONE_RECORDED = ("no development or governance act recorded in the CAP-06 "
                 "review records; not a finding that none exists")


def answer(tranche: dict | None = None) -> dict:
    """{class CURIE: {"acts": {act: reason}, "record": "path@commit",
    "index": [...]}} for every written specific class."""
    tranche = tranche or formalize.load_tranche()
    findings: list = []
    texts: dict = {}
    out = {}
    for entry in tranche["classes"]:
        record = entry["signed_record"]
        key = (record["commit"], record["path"])
        if key not in texts:
            texts[key] = formalize.signed_text(record["commit"],
                                               record["path"],
                                               record["sha256"], findings,
                                               entry["g1t"])
        text = texts[key]
        acts = {}
        if entry["g1t"].startswith("T2-"):
            section = formalize.t2_section(text, entry["g1t"]) or ""
            excluded = section.split("**Excluded** (")[1] \
                if "**Excluded** (" in section else ""
            excluded = excluded.split("\n\n**")[0]
            for act, code, reason in EXCLUDED_ROW.findall(excluded):
                if code == "Q5":
                    acts[act] = reason.strip()
        else:
            match = QUESTION_5.search(text)
            if match:
                for act in ACT.findall(match.group(1)):
                    acts[act] = match.group(1).strip()
        out[entry["class"]] = {
            "acts": acts, "index": list(entry["index"]),
            "record": "%s@%s" % (record["path"], record["commit"][:7])}
    if findings:
        raise formalize.Refused("; ".join(findings))
    return out


def main(argv=None) -> int:
    result = answer()
    for cls in sorted(result):
        row = result[cls]
        if row["acts"]:
            print("%s  (%s)" % (cls, row["record"]))
            for act, reason in sorted(row["acts"].items()):
                print("    bpo:%s  %s" % (act, reason))
        else:
            print("%s  %s" % (cls, NONE_RECORDED))
    named = sum(len(r["acts"]) for r in result.values())
    print("%d act(s) recorded over %d of %d classes; a review-record answer "
          "(CQ-11 exception, decision of 2026-11-15, B-4), not an OWL or "
          "SPARQL answer" % (named, sum(1 for r in result.values()
                                        if r["acts"]), len(result)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
