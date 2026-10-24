# SPDX-License-Identifier: MIT
"""Decision citations (ADR-003 D2) and ratification acts (D5), checked
against git.

A citation is three parts:

    path     a file under docs/decisions/ or docs/adr/
    commit   the full 40-hex SHA of a commit reachable from origin/main
             or main
    sha256   the SHA-256 of the exact bytes `git show <commit>:<path>`

and every part is recomputed here, from the repository, never trusted.
Refused by name: a short commit, the empty-file digest e3b0c442...b855, a
path outside the two directories, a commit no main ref reaches, a digest
that is not the blob's.

A RATIFICATION ACT is a decision record whose text, at the cited commit,
holds exactly one fenced block with the info string `bco-ratification`:

    ```bco-ratification
    agent: https://fandaws.com/ontology/bco-agents#<person>
    approvals:
      editorial: https://fandaws.com/ontology/bco-agents#<person>
      ontological: https://fandaws.com/ontology/bco-agents#<person>
    validation:
      commit: <40 hex: a commit reachable from origin/main or main>
      gates:
        - python tools/ontology/validate.py --gate
        - python -m pytest tests/ -q -p no:randomly
    concepts:
      - iri: https://fandaws.com/ontology/bco-catalog#TreasuryManagement
        record_sha256: <64 hex: the concept record digest, see build.py>
    ```

Exactly these four keys, all required, and in each list item exactly
`iri` and `record_sha256`. Every IRI is written out in full; a CURIE, a
wildcard, a namespace or a scheme IRI is refused, and so is any other key
(`scheme`, `pattern`, `all`, ...): ADR-003 D5 admits a batch only as an
explicit list. The block is read from the cited commit's blob, not from
the working tree, so the act that counts is the one the digest pins.

`approvals` and `validation` were added on 2026-10-24 in answer to review
R6, section 6.3: a draft's provenance does not show that its definitions
passed review or the gates, so the act records both. `approvals` is
exactly `editorial` and `ontological`, each a person's IRI written in
full; the build requires each to be a declared prov:Person (ADR-003 D8),
the same rule as `agent`, and one person may give both. `validation` is
exactly `commit` -- the full 40-hex SHA at which the gates were run,
which must be reachable from origin/main or main (check_validation) --
and `gates`, the non-empty list of the gate commands that passed there,
each written once. The list is the act's statement; this module does not
re-run the gates. The addition is to the act's format only: what ADR-003
D5 requires an act to carry (explicit IRIs, each with its record digest)
is unchanged.
"""

from __future__ import annotations

import hashlib
import re
import subprocess
from pathlib import Path

EMPTY_SHA256 = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
FULL_COMMIT = re.compile(r"^[0-9a-f]{40}$")
SHA256 = re.compile(r"^[0-9a-f]{64}$")
CITED_PATH = re.compile(r"^docs/(decisions|adr)/[A-Za-z0-9._-]+\.md$")
MAIN_REFS = ("origin/main", "main")
BLOCK = re.compile(r"^```bco-ratification[ \t]*\n(.*?)^```[ \t]*$",
                   re.M | re.S)
ACT_KEYS = {"agent", "approvals", "validation", "concepts"}
APPROVAL_KEYS = {"editorial", "ontological"}
VALIDATION_KEYS = {"commit", "gates"}
ITEM_KEYS = {"iri", "record_sha256"}


class CitationError(ValueError):
    """A citation or act that does not hold. `code` names the rule."""

    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code = code


def _git(root: Path, *args: str) -> tuple[int, bytes, bytes]:
    proc = subprocess.run(["git", *args], cwd=str(root), capture_output=True)
    return proc.returncode, proc.stdout, proc.stderr


def _reachable(root: Path, commit: str, unknown: str, unreachable: str,
               what: str) -> None:
    """`commit` is a commit here and some main ref reaches it, or
    CitationError under the code given for each failure."""
    code, out, _ = _git(root, "cat-file", "-t", commit)
    if code or out.strip() != b"commit":
        raise CitationError(unknown, "%s %s is not a commit in this "
                                     "repository" % (what, commit))
    refs = [ref for ref in MAIN_REFS
            if _git(root, "rev-parse", "--verify", "--quiet",
                    ref + "^{commit}")[0] == 0]
    if not refs:
        raise CitationError(unreachable,
                            "neither origin/main nor main exists, so "
                            "reachability of %s cannot be established"
                            % commit)
    if not any(_git(root, "merge-base", "--is-ancestor", commit, ref)[0] == 0
               for ref in refs):
        raise CitationError(unreachable, "%s %s is not reachable from %s"
                            % (what, commit, " or ".join(refs)))


def check_validation(root: Path, act: dict) -> None:
    """The act's validation commit exists and a main ref reaches it (R6,
    section 6.3). Its form was checked by parse_act."""
    _reachable(root, act["validation"]["commit"],
               "D5-act-validation-unreachable",
               "D5-act-validation-unreachable", "validation commit")


def check_citation(root: Path, citation: object) -> bytes:
    """The cited blob's bytes, or CitationError naming the broken rule."""
    if not isinstance(citation, dict) or set(citation) != {"path", "commit",
                                                           "sha256"}:
        raise CitationError("D2-citation-shape",
                            "a citation is exactly path, commit and sha256; "
                            "got %r" % (citation,))
    path, commit, digest = (citation["path"], citation["commit"],
                            citation["sha256"])
    if not isinstance(path, str) or not CITED_PATH.fullmatch(path):
        raise CitationError("D2-path", "cited path %r is not a file under "
                                       "docs/decisions/ or docs/adr/" % (path,))
    if not isinstance(commit, str) or not FULL_COMMIT.fullmatch(commit):
        raise CitationError("D2-short-commit",
                            "cited commit %r is not a full 40-character "
                            "lowercase hexadecimal SHA" % (commit,))
    if digest == EMPTY_SHA256:
        raise CitationError("D2-empty-digest",
                            "cited sha256 is e3b0c442...b855, the digest of "
                            "the empty file; it is refused by name")
    if not isinstance(digest, str) or not SHA256.fullmatch(digest):
        raise CitationError("D2-digest-form", "cited sha256 %r is not 64 "
                                              "lowercase hex" % (digest,))
    _reachable(root, commit, "D2-unknown-commit", "D2-unreachable",
               "cited commit")
    code, blob, _ = _git(root, "show", "%s:%s" % (commit, path))
    if code:
        raise CitationError("D2-path-not-in-commit",
                            "%s does not exist at commit %s" % (path, commit))
    actual = hashlib.sha256(blob).hexdigest()
    if actual != digest:
        raise CitationError("D2-digest-mismatch",
                            "the SHA-256 of git show %s:%s is %s, not the "
                            "cited %s" % (commit[:12], path, actual, digest))
    return blob


def parse_act(blob: bytes, where: str) -> dict:
    """{'agent': iri, 'approvals': {'editorial': iri, 'ontological': iri},
    'validation': {'commit': sha, 'gates': [str]},
    'concepts': {iri: record_sha256}} or CitationError."""
    import yaml

    text = blob.decode("utf-8")
    blocks = BLOCK.findall(text)
    if len(blocks) != 1:
        raise CitationError("D5-act-block",
                            "%s holds %d bco-ratification blocks; a "
                            "ratification act holds exactly one"
                            % (where, len(blocks)))
    data = yaml.safe_load(blocks[0])
    if not isinstance(data, dict):
        raise CitationError("D5-act-block", "%s: the bco-ratification block "
                                            "is not a mapping" % where)
    extra = set(data) - ACT_KEYS
    if extra:
        raise CitationError("D5-act-not-explicit",
                            "%s admits concepts by %s; ADR-003 D5 admits a "
                            "batch only as an explicit list of IRIs"
                            % (where, ", ".join(sorted(map(str, extra)))))
    agent = data.get("agent")
    if not isinstance(agent, str) or not agent.startswith("https://"):
        raise CitationError("D5-act-agent", "%s names no agent IRI written "
                                            "in full" % where)
    approvals = data.get("approvals")
    if not isinstance(approvals, dict) or not APPROVAL_KEYS <= set(approvals):
        raise CitationError(
            "D5-act-approval-missing",
            "%s does not record both approvals; an act states who gave the "
            "editorial and who gave the ontological approval (review R6, "
            "section 6.3): got %r" % (where, approvals))
    if set(approvals) != APPROVAL_KEYS or not all(
            isinstance(approvals[k], str) and approvals[k].startswith(
                "https://") for k in APPROVAL_KEYS):
        raise CitationError(
            "D5-act-approval-shape",
            "%s: approvals is exactly editorial and ontological, each a "
            "person IRI written in full; got %r" % (where, approvals))
    validation = data.get("validation")
    if not isinstance(validation, dict) \
            or set(validation) != VALIDATION_KEYS:
        raise CitationError(
            "D5-act-validation-shape",
            "%s: validation is exactly commit and gates, the commit the "
            "gates ran at and the commands that passed; got %r"
            % (where, validation))
    if not isinstance(validation["commit"], str) \
            or not FULL_COMMIT.fullmatch(validation["commit"]):
        raise CitationError(
            "D5-act-validation-commit",
            "%s: validation commit %r is not a full 40-character lowercase "
            "hexadecimal SHA" % (where, validation["commit"]))
    gates = validation["gates"]
    if not isinstance(gates, list) or not gates:
        raise CitationError(
            "D5-act-validation-gates",
            "%s lists no gate that passed; an act names the gates run at "
            "its validation commit" % where)
    if not all(isinstance(g, str) and g.strip() for g in gates) \
            or len(set(gates)) != len(gates):
        raise CitationError(
            "D5-act-validation-gates",
            "%s: each gate is a command, written once; got %r"
            % (where, gates))
    items = data.get("concepts")
    if not isinstance(items, list) or not items:
        raise CitationError("D5-act-not-explicit",
                            "%s lists no concepts; an act ratifies an "
                            "explicit, non-empty list" % where)
    found: dict = {}
    for item in items:
        if not isinstance(item, dict) or set(item) != ITEM_KEYS:
            raise CitationError("D5-act-not-explicit",
                                "%s: each listed concept is exactly iri and "
                                "record_sha256; got %r" % (where, item))
        iri, digest = item["iri"], item["record_sha256"]
        if (not isinstance(iri, str) or not iri.startswith("https://")
                or any(ch in iri for ch in "*?[]{}") or iri.endswith(("#", "/"))
                or iri.endswith("Scheme")):
            raise CitationError("D5-act-not-explicit",
                                "%s lists %r, which is not one concept IRI "
                                "written in full (a wildcard, namespace, "
                                "scheme or CURIE is refused)" % (where, iri))
        if not isinstance(digest, str) or not SHA256.fullmatch(digest) \
                or digest == EMPTY_SHA256:
            raise CitationError("D5-act-record-digest",
                                "%s lists %s with record_sha256 %r, which is "
                                "not a usable SHA-256" % (where, iri, digest))
        if iri in found:
            raise CitationError("D5-act-not-explicit",
                                "%s lists %s twice" % (where, iri))
        found[iri] = digest
    return {"agent": agent, "approvals": dict(approvals),
            "validation": {"commit": validation["commit"],
                           "gates": list(gates)},
            "concepts": found}
