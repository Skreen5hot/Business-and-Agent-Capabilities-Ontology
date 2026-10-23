# SPDX-License-Identifier: Apache-2.0
"""The initial import, held to what it said it was.

docs/ARTIFACT-INVENTORY.md says the files in the 2026-10-22 import are
"preserved byte-for-byte", and the v0.1 draft package carries its own
SHA256SUMS.txt. Both are claims until something recomputes them. These
tests do, from the index rather than the working tree -- the index is
what is published, and a working-tree read would measure whatever
core.autocrlf did on this machine.

Two files were rewritten when the repository was set up, deliberately,
and are named below with the reason. Everything else in the import is
required to be exactly what the inventory recorded.
"""

from __future__ import annotations

import hashlib
import json
import re
import subprocess

import pytest

INVENTORY = "docs/ARTIFACT-INVENTORY.md"
MANIFEST = "docs/artifact-manifest.json"
DRAFT = "drafts/BusinessCapabilityOntology_draft_v0.1.0"

#: Files the import recorded that have since been rewritten on purpose.
#: Named rather than skipped by pattern, so the list can only grow by an
#: edit somebody can see.
REWRITTEN = {
    "README.md": "rewritten at repository setup (2026-10-23) to describe "
                 "the tooling; the import's text is in git history",
    ".gitignore": "rewritten at repository setup (2026-10-23) to carry "
                  "ARO's rules plus the reference-material exclusions",
}


def indexed_blob(repo, path: str) -> bytes:
    result = subprocess.run(["git", "cat-file", "blob", ":" + path],
                            cwd=str(repo), capture_output=True)
    assert result.returncode == 0, (
        "%s is not in the index: %s"
        % (path, result.stderr.decode("utf-8", "replace")[-200:]))
    return result.stdout


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


@pytest.fixture(scope="module")
def recorded(repo) -> dict:
    """The import's digests, from the JSON manifest -- and required to
    agree with the Markdown inventory, because two records of the same
    fact that disagree mean one of them is wrong and nothing says which.
    """
    manifest = json.loads((repo / MANIFEST).read_text(encoding="utf-8"))
    from_json = {entry["path"]: entry["sha256"]
                 for entry in manifest["files"]}

    table = (repo / INVENTORY).read_text(encoding="utf-8")
    from_markdown = dict(re.findall(
        r"^\| `([^`]+)` \| `([0-9a-f]{64})` \|$", table, flags=re.M))

    assert len(from_json) >= 15, len(from_json)
    assert from_json == from_markdown, (
        "the inventory and the manifest disagree: %s"
        % sorted(set(from_json.items()) ^ set(from_markdown.items()))[:4])
    return from_json


def test_every_imported_file_is_still_what_the_import_recorded(repo,
                                                               recorded):
    changed = []
    for path, digest in sorted(recorded.items()):
        if path in REWRITTEN:
            continue
        if sha256(indexed_blob(repo, path)) != digest:
            changed.append(path)
    assert not changed, (
        "%d imported file(s) no longer match the digest the import "
        "recorded: %s. If the change is deliberate, add the file to "
        "REWRITTEN with the reason." % (len(changed), changed))


def test_the_rewritten_files_were_in_fact_rewritten(repo, recorded):
    """An exemption for a file that still matches is an exemption for
    nothing, and would quietly cover a later accidental edit."""
    for path in REWRITTEN:
        assert path in recorded, path
        assert sha256(indexed_blob(repo, path)) != recorded[path], (
            "%s still matches its import digest; remove it from REWRITTEN"
            % path)


def test_the_draft_package_passes_its_own_checksums(repo):
    """SHA256SUMS.txt is the v0.1 package's own claim about itself.

    Every file it lists must digest to what it says, and every file in
    the package except SHA256SUMS.txt must be listed -- a checksum file
    that omits a file certifies the package minus that file.
    """
    sums = indexed_blob(repo, DRAFT + "/SHA256SUMS.txt").decode("utf-8")
    listed = {}
    for line in sums.splitlines():
        if not line.strip():
            continue
        digest, name = line.split(None, 1)
        listed[name.strip().lstrip("*")] = digest

    files = subprocess.run(["git", "ls-files", DRAFT], cwd=str(repo),
                           capture_output=True, text=True,
                           encoding="utf-8").stdout.split()
    in_package = {f[len(DRAFT) + 1:] for f in files} - {"SHA256SUMS.txt"}
    assert len(in_package) >= 10, in_package
    assert set(listed) == in_package, sorted(set(listed) ^ in_package)

    wrong = [name for name, digest in sorted(listed.items())
             if sha256(indexed_blob(repo, DRAFT + "/" + name)) != digest]
    assert not wrong, wrong


def test_the_checksum_comparison_can_fail(repo, recorded):
    """Falsifies the comparison: one byte appended to a real imported
    file must not match its recorded digest. Without this, a sha256 that
    returned a constant would pass every test above."""
    path = "specifications/Business-Capability-Ontology-v0.4.0-draft.1.md"
    data = indexed_blob(repo, path)
    assert sha256(data) == recorded[path]
    assert sha256(data + b" ") != recorded[path]
