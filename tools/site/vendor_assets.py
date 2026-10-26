# SPDX-License-Identifier: MIT
"""Vendor the third-party files the public site serves, and verify them.

    python tools/site/vendor_assets.py            # offline verify
    python tools/site/vendor_assets.py --fetch    # fetch, verify, rewrite

The pins are config/site-vendor.yaml; its header says why the site
vendors Mermaid rather than loading it from a CDN. This is the tool that
holds the repository to those pins.

THE DEFAULT RUN IS OFFLINE

It reads each pinned member's file from vendor/site/ and compares its
sha256 with the pin, checks the licence statement against the extracted
LICENSE, and checks that vendor/site/NOTICE.md is what this tool would
write. No network, no tarball: it is the check that runs before every
commit and in CI, and a check that needed a registry to be up would be
re-run rather than read when it failed.

--fetch IS THE ONLY WRITER

It downloads the pinned tarball, and nothing else, from the registry URL
in the pin, and refuses it unless its sha512 equals the pinned npm
`integrity` and its sha1 the pinned `shasum`. It then extracts exactly
the pinned members -- a member that is not a regular file, or a name the
pin does not list, is never written -- verifies each one's sha256, and
writes them as bytes, so no newline translation stands between the
registry's bytes and the committed ones. The notice is regenerated from
the pins in the same run.

Network use is limited to the tarball URL in each pin. The registry
metadata URL is recorded in the pin as where the integrity was read from,
and is not fetched here: a tool that re-read the expected digest from the
same host that serves the file would be checking the host against itself.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import io
import sys
import tarfile
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import layout  # noqa: E402

PINS = "config/site-vendor.yaml"
NOTICE = "vendor/site/NOTICE.md"
GENERATOR = "tools/site/vendor_assets.py"
#: The only hosts --fetch may reach. A pin naming another is refused, so a
#: copied-in URL cannot widen what this tool downloads from.
ALLOWED_PREFIXES = ("https://registry.npmjs.org/",)
#: Where every pinned member must land. Anything else would be a vendored
#: file outside the directory the layout contract and the licensing tool
#: know to look in.
VENDOR_ROOT = "vendor/site/"


class Refused(SystemExit):
    """A question for whoever wrote the pin, not for this tool."""


def root() -> Path:
    return layout.repository_root()


def assets(base: Path | None = None) -> list[dict]:
    """The pins, each checked for the fields the rest of this tool uses."""
    import yaml

    base = base or root()
    path = base / PINS
    if not path.is_file():
        raise Refused(PINS + " is missing. Without it, what would say which "
                      "bytes the site is allowed to serve?")
    raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    found = raw.get("assets") or []
    if not found:
        raise Refused(PINS + " pins no asset. Was the list emptied on "
                      "purpose? The site's Models page needs Mermaid.")
    ids = set()
    for entry in found:
        for required in ("id", "project", "version", "tarball", "integrity",
                         "shasum", "members", "licence"):
            if not entry.get(required):
                raise Refused("%s: asset %r declares no %r -- which value "
                              "was meant?" % (PINS, entry.get("id"),
                                              required))
        if entry["id"] in ids:
            raise Refused("%s pins %r twice; which one is meant?"
                          % (PINS, entry["id"]))
        ids.add(entry["id"])
        if not str(entry["integrity"]).startswith("sha512-"):
            raise Refused("%s: %s integrity is not sha512-...; was it copied "
                          "from dist.integrity?" % (PINS, entry["id"]))
        if not entry["tarball"].startswith(ALLOWED_PREFIXES):
            raise Refused("%s: %s tarball %s is not on %s. Should the "
                          "allowed hosts really grow?"
                          % (PINS, entry["id"], entry["tarball"],
                             ALLOWED_PREFIXES))
        for required in ("spdx", "attribution", "file",
                         "licence_statement_contains"):
            if not entry["licence"].get(required):
                raise Refused("%s: %s declares no licence.%s"
                              % (PINS, entry["id"], required))
        for member in entry["members"]:
            for required in ("member", "path", "site_path", "sha256"):
                if not member.get(required):
                    raise Refused("%s: a member of %s declares no %r"
                                  % (PINS, entry["id"], required))
            if not member["path"].startswith(VENDOR_ROOT):
                raise Refused("%s: %s writes %s, outside %s. Is that where "
                              "the layout contract expects it?"
                              % (PINS, entry["id"], member["path"],
                                 VENDOR_ROOT))
        if entry["licence"]["file"] not in {m["path"]
                                             for m in entry["members"]}:
            raise Refused("%s: %s names licence file %s, which is not one "
                          "of its members. Where would the licence text "
                          "come from?" % (PINS, entry["id"],
                                          entry["licence"]["file"]))
    return found


def by_path(base: Path | None = None) -> dict[str, dict]:
    """Every pinned file, indexed by repository path, with its asset.

    What the licensing tool and the site build ask: which asset produced
    this file, and under what licence.
    """
    out = {}
    for entry in assets(base):
        for member in entry["members"]:
            out[member["path"]] = {"asset": entry, "member": member}
    return out


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def notice_text(pinned: list[dict]) -> bytes:
    """vendor/site/NOTICE.md, from the pins alone."""
    lines = [
        "# Third-party notices: site assets",
        "",
        "The public site serves the files below, which this repository",
        "redistributes unmodified. Each licence requires attribution, and",
        "this file is that attribution. It is generated by",
        "`%s` from `%s`; the licensing check reads the" % (GENERATOR, PINS),
        "same pins and fails if an attribution declared there is missing",
        "here.",
        "",
        "These are not part of the ontology. They are software the site",
        "runs in the reader's browser, and nothing in this repository's",
        "validation loads them.",
    ]
    for entry in sorted(pinned, key=lambda e: e["id"]):
        lines += [
            "",
            "## %s %s" % (entry["project"], entry["version"]),
            "",
            " ".join(entry["licence"]["attribution"].split()),
            "",
            "- tarball: %s" % entry["tarball"],
            "- integrity: `%s`" % entry["integrity"],
            "- licence: %s -- `%s`" % (entry["licence"]["spdx"],
                                       entry["licence"]["file"]),
        ]
        for member in entry["members"]:
            lines.append("- `%s` from `%s`, sha256 `%s`"
                         % (member["path"], member["member"],
                            member["sha256"]))
    return ("\n".join(lines) + "\n").encode("utf-8")


def verify(base: Path | None = None) -> tuple[list[str], int]:
    """(findings, files checked), offline."""
    base = base or root()
    pinned = assets(base)
    problems, checked = [], 0
    for entry in pinned:
        for member in entry["members"]:
            path = base / member["path"]
            if not path.is_file():
                problems.append(
                    "%s is missing. Run `python %s --fetch` to restore it "
                    "from the pin." % (member["path"], GENERATOR))
                continue
            checked += 1
            got = sha256(path.read_bytes())
            if got != member["sha256"]:
                problems.append(
                    "%s has sha256 %s; the pin says %s. Was it edited, or "
                    "rewritten with CRLF? Restore it with --fetch, or "
                    "change the pin on purpose." % (member["path"], got,
                                                    member["sha256"]))
        licence = base / entry["licence"]["file"]
        if licence.is_file():
            needle = entry["licence"]["licence_statement_contains"]
            if needle not in licence.read_text(encoding="utf-8"):
                problems.append(
                    "%s does not contain %r, so what supports the SPDX "
                    "identifier %s the pin declares?"
                    % (entry["licence"]["file"], needle,
                       entry["licence"]["spdx"]))
    notice = base / NOTICE
    if not notice.is_file():
        problems.append("%s is missing; the vendored site assets are "
                        "redistributed without their attribution. Run "
                        "--fetch, which writes it." % NOTICE)
    elif notice.read_bytes() != notice_text(pinned):
        problems.append("%s is not what %s writes from %s. Was it edited "
                        "by hand, or a pin changed without --fetch?"
                        % (NOTICE, GENERATOR, PINS))
    return problems, checked


def integrity_of(data: bytes) -> str:
    return "sha512-" + base64.b64encode(hashlib.sha512(data).digest()).decode()


def extract(entry: dict, tarball: bytes) -> dict[str, bytes]:
    """{repository path: bytes} for the pinned members, verified.

    The tarball is opened in memory and only the named members are read;
    nothing is extracted to disk by name, so a hostile member path cannot
    place a file anywhere.
    """
    got = integrity_of(tarball)
    if got != entry["integrity"]:
        raise Refused("the %s tarball has integrity %s; the pin says %s. "
                      "Was it served by something other than the registry?"
                      % (entry["id"], got, entry["integrity"]))
    sha1 = hashlib.sha1(tarball).hexdigest()
    if sha1 != entry["shasum"]:
        raise Refused("the %s tarball has shasum %s; the pin says %s"
                      % (entry["id"], sha1, entry["shasum"]))
    wanted = {m["member"]: m for m in entry["members"]}
    out = {}
    with tarfile.open(fileobj=io.BytesIO(tarball), mode="r:gz") as archive:
        for info in archive.getmembers():
            if info.name not in wanted:
                continue
            if not info.isfile():
                raise Refused("%s in the %s tarball is not a regular file; "
                              "is the pin naming the right member?"
                              % (info.name, entry["id"]))
            member = wanted[info.name]
            if member["path"] in out:
                raise Refused("the %s tarball holds %s twice; which copy "
                              "would be the pinned one?"
                              % (entry["id"], info.name))
            data = archive.extractfile(info).read()
            digest = sha256(data)
            if digest != member["sha256"]:
                raise Refused("%s from the %s tarball has sha256 %s; the pin "
                              "says %s" % (info.name, entry["id"], digest,
                                           member["sha256"]))
            out[member["path"]] = data
    missing = sorted(m["member"] for m in entry["members"]
                     if m["path"] not in out)
    if missing:
        raise Refused("the %s tarball holds none of %s. Was the member "
                      "renamed in this version?" % (entry["id"], missing))
    return out


def download(url: str) -> bytes:
    if not url.startswith(ALLOWED_PREFIXES):
        raise Refused("refusing to fetch %s: not on %s"
                      % (url, ALLOWED_PREFIXES))
    request = urllib.request.Request(url, headers={
        "User-Agent": "bco-vendor-assets (+%s)" % GENERATOR})
    with urllib.request.urlopen(request, timeout=120) as response:
        return response.read()


def fetch(base: Path | None = None) -> list[str]:
    base = base or root()
    pinned = assets(base)
    written = []
    for entry in pinned:
        files = extract(entry, download(entry["tarball"]))
        needle = entry["licence"]["licence_statement_contains"]
        licence_text = files[entry["licence"]["file"]].decode("utf-8")
        if needle not in licence_text:
            raise Refused("the %s LICENSE does not contain %r; is %s the "
                          "right SPDX identifier?"
                          % (entry["id"], needle, entry["licence"]["spdx"]))
        for path, data in sorted(files.items()):
            target = base / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
            written.append(path)
    notice = base / NOTICE
    notice.parent.mkdir(parents=True, exist_ok=True)
    notice.write_bytes(notice_text(pinned))
    written.append(NOTICE)
    return written


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--fetch", action="store_true",
                    help="download the pinned tarballs and rewrite the files")
    args = ap.parse_args(argv)

    if args.fetch:
        for path in fetch():
            print("  wrote %s" % path)
    problems, checked = verify()
    if problems:
        for problem in problems:
            print("  FINDING: %s" % problem)
        return 1
    pinned = assets()
    print("  ok: %d asset(s) pinned (%s), %d file(s) match their sha256, "
          "%s is fresh" % (len(pinned), ", ".join(
              "%s %s" % (e["project"], e["version"]) for e in pinned),
              checked, NOTICE))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
