# SPDX-License-Identifier: MIT
"""The communications record follows its protocol, and the checks can fail.

The live record is checked first. Then every rule in
communications/README.md that a tool can hold is broken, one at a time,
against a header that otherwise passes -- because a checker that accepts
the record and would also accept each of these is checking nothing.
"""

from __future__ import annotations

import copy
import hashlib
import shutil
import subprocess

import pytest

from conftest import load_tool

GOOD = {
    "id": "BCO-BPO-2026-10-23-vendoring-pin",
    "from": "BCO",
    "to": "BPO",
    "date": "2026-10-23",
    "type": "request",
    "subject": "A subject",
    "in_reply_to": None,
    "refs": [{"repo": "Skreen5hot/BusinessProcessOntology",
              "commit": "66131945b525c54f44e4962f32bb1f52dfa0cd12",
              "path": "ontology/apqc-ext.ttl",
              "sha256": "1b9a9375cb7303003556004effd712b63913d6aa4935"
                        "dbf604a653aec65cab4b"}],
    "author": "Aaron Damiano",
    "requires_act": False,
}
FILENAME = "2026-10-23-vendoring-pin.md"


@pytest.fixture(scope="module")
def comms():
    return load_tool("bco_communications", "tools/communications.py")


def header(**changes):
    out = copy.deepcopy(GOOD)
    for key, value in changes.items():
        if value is KeyError:
            out.pop(key)
        else:
            out[key] = value
    return out


# ---------------------------------------------------------- the record


def test_the_record_follows_the_protocol(comms):
    record = comms.check()
    assert record["ok"], record["findings"]


def test_the_record_is_not_empty(comms):
    """Guards the test above: a record with no messages passes every
    check."""
    record = comms.check()
    assert "BCO-BPO-2026-10-23-vendoring-pin" in record["messages"]


def test_the_first_request_to_bpo_is_open_until_answered(comms):
    """Status is derived: nothing has replied to it, so it is open."""
    assert "BCO-BPO-2026-10-23-vendoring-pin" in comms.check()["open"]


def test_the_good_header_passes(comms):
    """The baseline every falsification below departs from. If it failed,
    every refusal below would be passing for the wrong reason."""
    assert comms.check_header(GOOD, "BPO", "outgoing", FILENAME, b"") == []


# ------------------------------------------------- each rule can fail


@pytest.mark.parametrize("changes, expect", [
    ({"subject": KeyError}, "header lacks subject"),
    ({"date": "2026-10-24"}, "does not match the filename"),
    ({"date": "23 Oct 2026"}, "is not YYYY-MM-DD"),
    ({"from": "BPO", "to": "BCO"}, "from/to are BPO -> BCO"),
    ({"id": "BCO-BPO-2026-10-23-other"}, "its path makes it"),
    ({"type": "memo"}, "is not one of"),
    ({"type": "answer"}, "in_reply_to is null"),
    ({"requires_act": "no"}, "must be true or false"),
    ({"refs": [{"repo": "x", "commit": "6613194", "path": "p",
                "sha256": "0" * 64}]}, "not a full 40-hex SHA"),
    ({"refs": [{"repo": "x", "commit": "a" * 40, "path": "p"}]},
     "lacks sha256"),
    ({"refs": "ontology/apqc-ext.ttl"}, "refs must be a list"),
    ({"source": GOOD["refs"][0]}, "an outgoing message has a source"),
])
def test_each_header_rule_refuses(comms, changes, expect):
    problems = comms.check_header(header(**changes), "BPO", "outgoing",
                                  FILENAME, b"")
    assert any(expect in p for p in problems), problems


def test_a_bad_filename_is_refused(comms):
    problems = comms.check_header(GOOD, "BPO", "outgoing",
                                  "Vendoring Pin.md", b"")
    assert problems == ["filename is not YYYY-MM-DD-<slug>.md"]


def test_an_incoming_copy_must_be_the_original_bytes(comms):
    """Rule: an incoming body is the original, byte for byte. A tidied
    copy -- one changed character -- is refused."""
    original = b"# Reply from BPO\n\nAcknowledged.\n"
    incoming = header(**{"from": "BPO", "to": "BCO",
                         "id": "BPO-BCO-2026-10-23-vendoring-pin",
                         "type": "acknowledgment",
                         "in_reply_to": "BCO-BPO-2026-10-23-vendoring-pin"})
    incoming["source"] = {"repo": "Skreen5hot/BusinessProcessOntology",
                          "commit": "b" * 40, "path": "comms/x.md",
                          "sha256": hashlib.sha256(original).hexdigest()}
    assert comms.check_header(incoming, "BPO", "incoming", FILENAME,
                              original) == []

    tidied = original.replace(b"Acknowledged.", b"Acknowledged!")
    assert tidied != original
    problems = comms.check_header(incoming, "BPO", "incoming", FILENAME,
                                  tidied)
    assert any("the body is not the original" in p for p in problems)

    del incoming["source"]
    problems = comms.check_header(incoming, "BPO", "incoming", FILENAME,
                                  original)
    assert any("has no source" in p for p in problems), problems


def test_a_local_ref_is_recomputed_from_its_commit(comms, repo):
    ref = {"repo": comms.THIS_REPO,
           "commit": "3d43724170db5199dde6243e2a6beae306083ec7",
           "path": "config/upstream-sources.yaml",
           "sha256": "e9c00d8e123a6619ae4bc07429684ed254983da00a314648a8b4"
                     "d17be458000d"}
    assert comms.check_local_ref(repo, ref) == []
    wrong = dict(ref, sha256="0" * 64)
    assert any("digests to" in p for p in comms.check_local_ref(repo, wrong))
    missing = dict(ref, path="config/no-such-file.yaml")
    assert any("does not exist" in p
               for p in comms.check_local_ref(repo, missing))


# ------------------------------------------- rules about the whole tree


def message(path, fields):
    import yaml

    text = "---\n" + yaml.safe_dump(fields, sort_keys=False) + "---\n\nBody.\n"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(text.encode("utf-8"))


@pytest.fixture
def tree(tmp_path, repo):
    """A throwaway repository holding the protocol and one good message,
    so tree-level rules can be broken without touching the real record."""
    root = tmp_path / "r"
    (root / "config").mkdir(parents=True)
    (root / "config/repository-layout.yaml").write_bytes(b"version: 1\n")
    (root / "communications/bpo").mkdir(parents=True)
    shutil.copy(repo / "communications/README.md",
                root / "communications/README.md")
    shutil.copy(repo / "communications/bpo/README.md",
                root / "communications/bpo/README.md")
    message(root / "communications/bpo/outgoing" / FILENAME, GOOD)
    for args in (["init", "-q"], ["config", "user.email", "t@invalid"],
                 ["config", "user.name", "t"], ["add", "-A"],
                 ["commit", "-q", "-m", "one"]):
        subprocess.run(["git", *args], cwd=str(root), check=True,
                       capture_output=True)
    return root


def test_the_throwaway_tree_starts_clean(comms, tree):
    record = comms.check(tree)
    assert record["ok"], record["findings"]
    assert record["open"] == [GOOD["id"]]


def test_an_answer_closes_the_thread_it_replies_to(comms, tree):
    reply = header(**{"from": "BPO", "to": "BCO",
                      "id": "BPO-BCO-2026-10-24-ack", "date": "2026-10-24",
                      "type": "acknowledgment", "in_reply_to": GOOD["id"]})
    body = b"\nBody.\n"
    reply["source"] = {"repo": "Skreen5hot/BusinessProcessOntology",
                       "commit": "c" * 40, "path": "x.md",
                       "sha256": hashlib.sha256(body).hexdigest()}
    message(tree / "communications/bpo/incoming/2026-10-24-ack.md", reply)
    record = comms.check(tree)
    assert record["ok"], record["findings"]
    assert record["open"] == []


def test_a_reply_to_nothing_is_refused(comms, tree):
    stray = header(id="BCO-BPO-2026-10-23-stray", type="answer",
                   in_reply_to="BCO-BPO-2026-01-01-never-sent")
    message(tree / "communications/bpo/outgoing/2026-10-23-stray.md", stray)
    findings = comms.check(tree)["findings"]
    assert any("names no message" in f for f in findings), findings


def test_an_unknown_team_folder_is_refused(comms, tree):
    (tree / "communications/bpp/outgoing").mkdir(parents=True)
    findings = comms.check(tree)["findings"]
    assert any("not a known team folder" in f for f in findings), findings


def test_a_committed_message_that_is_edited_is_refused(comms, tree):
    """Rule 1. The edit is committed, because the rule is about history:
    an uncommitted edit is still a draft."""
    path = tree / "communications/bpo/outgoing" / FILENAME
    before = path.read_bytes()
    path.write_bytes(before.replace(b"Body.", b"Body, revised."))
    assert path.read_bytes() != before
    subprocess.run(["git", "commit", "-qam", "edit"], cwd=str(tree),
                   check=True, capture_output=True)
    findings = comms.check(tree)["findings"]
    assert any("never edited" in f for f in findings), findings
