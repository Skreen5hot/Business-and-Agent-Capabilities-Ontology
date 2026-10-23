# SPDX-License-Identifier: MIT
"""Build the citation register's Markdown from its data, and check both.

    python tools/sources/build_register.py            # check; exit 1 on a finding
    python tools/sources/build_register.py --write    # regenerate the Markdown
    python tools/sources/build_register.py --claims SRC-OMG-03 --at-least P

`docs/sources/register.yaml` is the source of truth for every register
entry (ADR-003 D6, proposed). The Markdown register is generated from it
and from a hand-authored companion, `docs/sources/register-companion.md`,
which holds the analysis prose -- consensus, fault lines, the conflict
matrix, the SF findings, the access gaps -- and marks with one directive
line where the entry tables go. The companion is copied verbatim; only the
directive line is replaced.

What a check here refuses, each as a finding that names the entry:

- a claim whose status is missing, or anything other than exactly one of
  V, P, S, K, L (a qualifier belongs in the claim's `scope` or `note`,
  never in its status);
- a quote of more than 15 words; a quote with a missing, malformed or
  duplicate key (`SRC-<family>-<nn>-Q<n>`, numbered from the entry that
  holds it); more than one quote in an entry; a quote placed nowhere, or
  placed twice; a placeholder naming a quote that does not exist;
- a quotation mark typed into entry prose. Quotation marks come from a
  registered quote (`{Q1}`) or from a declared mention -- a title or a
  term's name -- (`{mention:...}`), so that every verbatim quotation is
  in the `quotes` list and nowhere else;
- an SRC identifier, anywhere in the register, the companion or any
  tracked file, that names no entry -- including the shorthand forms the
  analysis uses (`SRC-FO-01, -02`; `SRC-OG-01/02`);
- a register with other than EXPECTED_ENTRY_COUNT entries;
- an unknown field, an authority outside A1 to A9, a duplicate or
  malformed id, a family no section lists;
- a committed Markdown register that differs from a fresh generation.

Exit codes: 0 no findings; 1 findings (each printed); 2 bad usage.
"""

from __future__ import annotations

import argparse
import random
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import layout  # noqa: E402

#: Layout-contract ids, so the paths are the contract's rather than ours.
REGISTER_ID = "sources.register"
COMPANION_ID = "sources.register-companion"
OUTPUT_ID = "generated.sources-register"

#: The register's verification taxonomy, strongest first. The order of V
#: and P above the rest is what ADR-003 D6 relies on (a departure must
#: cite V or P). Placing S above K above L is this tool's choice: L marks
#: a primary that could not be read at all, so a claim resting on it is
#: no better than prior knowledge.
STATUSES = ("V", "P", "S", "K", "L")

AUTHORITIES = tuple("A%d" % n for n in range(1, 10))

#: ADR-003 D6: "More than 15 words ... fails the build". The register's
#: own prose says "under 15 words"; the two disagree only at exactly 15,
#: and no quote in the register is longer than 14.
MAX_QUOTE_WORDS = 15

#: The register's own rule: at most one verbatim quotation per entry.
#: ADR-003's Qn keys would allow more; raising this is the architect's
#: call, not an edit to make quietly.
MAX_QUOTES_PER_ENTRY = 1

#: The round-trip guard. The register had 63 entries when it became data
#: (commit 8f5c4a1); a conversion that dropped or doubled one would still
#: render. Change this in the same commit that adds or retires an entry.
EXPECTED_ENTRY_COUNT = 63

ENTRY_ID = re.compile(r"^SRC-([A-Z]+)-(\d{2})$")
QUOTE_KEY = re.compile(r"^(SRC-[A-Z]+-\d{2})-Q([1-9][0-9]*)$")
#: An SRC reference in running text, with the shorthand continuations the
#: analysis prose uses: `SRC-FO-01, -02, -03` and `SRC-OG-01/02`.
REFERENCE = re.compile(r"SRC-([A-Z]+)-(\d{2})((?:(?:/|,\s*-)\d{2})*)")
CONTINUATION = re.compile(r"\d{2}")
PLACEHOLDER = re.compile(r"\{([^{}]*)\}")
QUOTE_PLACEHOLDER = re.compile(r"^Q([1-9][0-9]*)$")
MENTION_PREFIX = "mention:"

#: The line in the companion that the entry tables replace.
DIRECTIVE = ("<!-- The entry tables are generated here from register.yaml "
             "by tools/sources/build_register.py. -->")

#: The companion states the entry count in prose; it must be the real one.
STATED_COUNT = re.compile(r"\brecords (\d+) sources\b")

TOP_FIELDS = {"version", "sections", "entries"}
SECTION_FIELDS = {"heading", "families"}
ENTRY_REQUIRED = ("id", "authority", "citation", "urls", "access_terms",
                  "definition", "claims")
ENTRY_FIELDS = set(ENTRY_REQUIRED) | {"quotes"}
URL_FIELDS = {"label", "url", "prefix", "suffix"}
CLAIM_FIELDS = {"status", "scope", "note"}
QUOTE_FIELDS = {"key", "text"}

TABLE_HEADER = ("| ID | Source (publisher; version; date) | URL | "
                "Licence / access | Definition, paraphrased | Status | "
                "Auth. |\n|---|---|---|---|---|---|---|")
NO_URL = "none retrieved"


class Refused(RuntimeError):
    """Raised instead of rendering data that has findings."""


# ------------------------------------------------------------- loading


def default_paths() -> tuple[Path, Path, Path]:
    """Register, companion and output, as the layout contract places them.
    The output is not required to exist: --write is how it comes to."""
    root = layout.repository_root()
    return tuple(root / layout.component(cid).path
                 for cid in (REGISTER_ID, COMPANION_ID, OUTPUT_ID))


def read_text(path: Path) -> str:
    """UTF-8, decoded explicitly; CR is reported, not normalised away."""
    return path.read_bytes().decode("utf-8")


def load(path: Path) -> dict:
    import yaml

    data = yaml.safe_load(read_text(path))
    return data if isinstance(data, dict) else {}


def entries(data: dict) -> list[dict]:
    raw = data.get("entries")
    return [e for e in raw if isinstance(e, dict)] if isinstance(raw, list) else []


def known_ids(data: dict) -> set[str]:
    return {e["id"] for e in entries(data) if isinstance(e.get("id"), str)}


# ------------------------------------------------------------- checks


def quote_words(text: str) -> int:
    """Words in a quote: whitespace-separated tokens holding a letter or a
    digit, so an ellipsis standing alone is not a word."""
    return sum(1 for token in text.split() if re.search(r"\w", token))


def entry_text_fields(entry: dict) -> list[tuple[str, object]]:
    """(where, value) for every prose field of an entry that renders."""
    out: list[tuple[str, object]] = [
        ("citation", entry.get("citation")),
        ("access_terms", entry.get("access_terms")),
        ("definition", entry.get("definition")),
    ]
    for n, url in enumerate(entry.get("urls") or [], 1):
        if isinstance(url, dict):
            for key in ("label", "prefix", "suffix"):
                if key in url:
                    out.append(("urls[%d].%s" % (n, key), url[key]))
    for n, claim in enumerate(entry.get("claims") or [], 1):
        if isinstance(claim, dict):
            for key in ("scope", "note"):
                if key in claim:
                    out.append(("claims[%d].%s" % (n, key), claim[key]))
    return out


def references(text: str) -> list[str]:
    """Every entry id a piece of text names, shorthand expanded."""
    found: list[str] = []
    for match in REFERENCE.finditer(text):
        family, first, rest = match.groups()
        found.append("SRC-%s-%s" % (family, first))
        found.extend("SRC-%s-%s" % (family, nn)
                     for nn in CONTINUATION.findall(rest))
    return found


def _cell_problems(where: str, value: object) -> list[str]:
    if not isinstance(value, str) or not value.strip():
        return ["%s is missing or not text" % where]
    problems = []
    if "\n" in value or "\r" in value:
        problems.append("%s spans lines; a table cell cannot" % where)
    if "|" in value:
        problems.append("%s contains '|', which would split the table cell"
                        % where)
    return problems


def _structure_findings(data: dict) -> tuple[list[str], dict[str, tuple[int, int]]]:
    """Top level and sections. Returns findings and family -> sort key."""
    problems: list[str] = []
    for key in sorted(set(data) - TOP_FIELDS):
        problems.append("unknown top-level field %r" % key)
    if data.get("version") != 1:
        problems.append("version is %r; this tool reads version 1"
                        % data.get("version"))
    order: dict[str, tuple[int, int]] = {}
    sections = data.get("sections")
    if not isinstance(sections, list) or not sections:
        return problems + ["no sections are declared"], order
    for s, section in enumerate(sections):
        if not isinstance(section, dict):
            problems.append("section %d is not a mapping" % (s + 1))
            continue
        for key in sorted(set(section) - SECTION_FIELDS):
            problems.append("section %d has unknown field %r" % (s + 1, key))
        problems += _cell_problems("section %d heading" % (s + 1),
                                   section.get("heading"))
        families = section.get("families")
        if not isinstance(families, list) or not families:
            problems.append("section %d lists no families" % (s + 1))
            continue
        for f, family in enumerate(families):
            if not isinstance(family, str) or not re.fullmatch(r"[A-Z]+", family):
                problems.append("section %d family %r is not an upper-case code"
                                % (s + 1, family))
            elif family in order:
                problems.append("family %s is listed in two sections" % family)
            else:
                order[family] = (s, f)
    return problems, order


def _quote_findings(entry_id: str, entry: dict) -> tuple[list[str], dict[str, str]]:
    problems: list[str] = []
    quotes = entry.get("quotes", [])
    by_number: dict[str, str] = {}
    if quotes is None or not isinstance(quotes, list):
        return ["%s: quotes is not a list" % entry_id], by_number
    if len(quotes) > MAX_QUOTES_PER_ENTRY:
        problems.append("%s has %d quotes; the register allows at most %d per "
                        "entry" % (entry_id, len(quotes), MAX_QUOTES_PER_ENTRY))
    seen: set[str] = set()
    for n, quote in enumerate(quotes, 1):
        where = "%s quote %d" % (entry_id, n)
        if not isinstance(quote, dict):
            problems.append("%s is not a mapping" % where)
            continue
        for key in sorted(set(quote) - QUOTE_FIELDS):
            problems.append("%s has unknown field %r" % (where, key))
        key = quote.get("key")
        if key is None or key == "":
            problems.append("%s has no key" % where)
        elif not isinstance(key, str) or not QUOTE_KEY.fullmatch(key):
            problems.append("%s has malformed key %r; expected %s-Q<n>"
                            % (where, key, entry_id))
        elif QUOTE_KEY.fullmatch(key).group(1) != entry_id:
            problems.append("%s has key %r, which belongs to another entry"
                            % (where, key))
        elif key in seen:
            problems.append("%s duplicates key %s" % (where, key))
        else:
            seen.add(key)
            by_number[QUOTE_KEY.fullmatch(key).group(2)] = key
        text = quote.get("text")
        problems += _cell_problems("%s text" % where, text)
        if isinstance(text, str):
            if '"' in text:
                problems.append("%s text contains a quotation mark" % where)
            words = quote_words(text)
            if words > MAX_QUOTE_WORDS:
                problems.append("%s is %d words; a quote may be at most %d"
                                % (where, words, MAX_QUOTE_WORDS))
    return problems, by_number


def _entry_findings(entry: dict, order: dict[str, tuple[int, int]]) -> list[str]:
    entry_id = entry.get("id")
    if not isinstance(entry_id, str) or not ENTRY_ID.fullmatch(entry_id):
        return ["an entry has malformed id %r" % (entry_id,)]
    problems: list[str] = []
    for key in sorted(set(entry) - ENTRY_FIELDS):
        problems.append("%s has unknown field %r" % (entry_id, key))
    for key in ENTRY_REQUIRED:
        if key not in entry:
            problems.append("%s has no %s" % (entry_id, key))
    family = ENTRY_ID.fullmatch(entry_id).group(1)
    if family not in order:
        problems.append("%s is in family %s, which no section lists"
                        % (entry_id, family))
    if entry.get("authority") not in AUTHORITIES:
        problems.append("%s has authority %r; expected one of A1 to A9"
                        % (entry_id, entry.get("authority")))

    urls = entry.get("urls")
    if not isinstance(urls, list):
        problems.append("%s: urls is not a list" % entry_id)
    else:
        for n, url in enumerate(urls, 1):
            if not isinstance(url, dict):
                problems.append("%s urls[%d] is not a mapping" % (entry_id, n))
                continue
            for key in sorted(set(url) - URL_FIELDS):
                problems.append("%s urls[%d] has unknown field %r"
                                % (entry_id, n, key))
            target = url.get("url")
            if not isinstance(target, str) or not re.fullmatch(r"https?://\S+",
                                                               target):
                problems.append("%s urls[%d] has no http(s) url" % (entry_id, n))

    claims = entry.get("claims")
    if not isinstance(claims, list) or not claims:
        problems.append("%s has no claims" % entry_id)
    else:
        for n, claim in enumerate(claims, 1):
            if not isinstance(claim, dict):
                problems.append("%s claim %d is not a mapping" % (entry_id, n))
                continue
            for key in sorted(set(claim) - CLAIM_FIELDS):
                problems.append("%s claim %d has unknown field %r"
                                % (entry_id, n, key))
            if "status" not in claim or claim["status"] in (None, ""):
                problems.append("%s claim %d has no status" % (entry_id, n))
            elif claim["status"] not in STATUSES:
                problems.append(
                    "%s claim %d has status %r; a status is exactly one of "
                    "V, P, S, K, L, and a qualifier goes in scope or note"
                    % (entry_id, n, claim["status"]))

    quote_problems, by_number = _quote_findings(entry_id, entry)
    problems += quote_problems

    placed: dict[str, int] = {}
    for where, value in entry_text_fields(entry):
        label = "%s %s" % (entry_id, where)
        problems += _cell_problems(label, value)
        if not isinstance(value, str):
            continue
        outside = PLACEHOLDER.sub("", value)
        if '"' in outside:
            problems.append(
                "%s has a quotation mark typed into prose; use {Qn} for a "
                "registered quote or {mention:...} for a title or a name"
                % label)
        if "{" in outside or "}" in outside:
            problems.append("%s has an unbalanced brace" % label)
        for token in PLACEHOLDER.findall(value):
            q = QUOTE_PLACEHOLDER.fullmatch(token)
            if q:
                if q.group(1) not in by_number:
                    problems.append("%s places {%s}, but %s has no quote %s-Q%s"
                                    % (label, token, entry_id, entry_id,
                                       q.group(1)))
                else:
                    placed[q.group(1)] = placed.get(q.group(1), 0) + 1
            elif token.startswith(MENTION_PREFIX):
                mention = token[len(MENTION_PREFIX):]
                if not mention.strip() or '"' in mention:
                    problems.append("%s has an empty or quoted mention" % label)
            else:
                problems.append("%s has unknown placeholder {%s}"
                                % (label, token))
    for number, key in sorted(by_number.items()):
        count = placed.get(number, 0)
        if count != 1:
            problems.append("%s is placed %d times; a quote is placed exactly "
                            "once" % (key, count))
    return problems


def findings(data: dict, companion: str) -> list[str]:
    """Every finding about the register data and the companion, without
    touching the rest of the repository."""
    problems, order = _structure_findings(data)
    raw = data.get("entries")
    if not isinstance(raw, list):
        return problems + ["entries is not a list"]
    ids: list[str] = []
    for entry in raw:
        if not isinstance(entry, dict):
            problems.append("an entry is not a mapping")
            continue
        problems += _entry_findings(entry, order)
        if isinstance(entry.get("id"), str):
            ids.append(entry["id"])
    for duplicate in sorted({i for i in ids if ids.count(i) > 1}):
        problems.append("%s is declared %d times" % (duplicate,
                                                     ids.count(duplicate)))
    if len(raw) != EXPECTED_ENTRY_COUNT:
        problems.append(
            "the register has %d entries; it had %d when it became data. "
            "If an entry was added or retired on purpose, change "
            "EXPECTED_ENTRY_COUNT in the same commit" % (len(raw),
                                                        EXPECTED_ENTRY_COUNT))
    covered = {ENTRY_ID.fullmatch(i).group(1) for i in ids
               if ENTRY_ID.fullmatch(i)}
    for family in sorted(set(order) - covered):
        problems.append("family %s is listed in a section but has no entry"
                        % family)

    if "\r" in companion:
        problems.append("the companion contains CR; the register is LF")
    lines = companion.split("\n")
    if lines.count(DIRECTIVE) != 1:
        problems.append("the companion must hold the directive line exactly "
                        "once; it holds it %d times" % lines.count(DIRECTIVE))
    stated = STATED_COUNT.findall(companion)
    if [int(n) for n in stated] != [len(raw)]:
        problems.append("the companion states %s as the entry count; the "
                        "register has %d" % (stated or "nothing", len(raw)))

    problems += unknown_references(
        set(ids), [("register.yaml " + where, value)
                   for entry in entries(data)
                   for where, value in entry_text_fields(entry)
                   if isinstance(value, str)]
        + [("register.yaml %s quote" % e.get("id"), q.get("text"))
           for e in entries(data) for q in (e.get("quotes") or [])
           if isinstance(q, dict) and isinstance(q.get("text"), str)]
        + [("companion", companion)])
    return problems


def unknown_references(known: set[str],
                       texts: list[tuple[str, str]]) -> list[str]:
    problems = []
    for where, text in texts:
        for ref in sorted(set(references(text)) - known):
            problems.append("%s names %s, which is not a register entry"
                            % (where, ref))
    return problems


def tracked_texts(root: Path) -> list[tuple[str, str]]:
    """Every tracked file that decodes as UTF-8, as (path, text)."""
    result = subprocess.run(["git", "ls-files", "-z"], cwd=str(root),
                            capture_output=True)
    if result.returncode:
        raise Refused("git ls-files failed: "
                      + result.stderr.decode("utf-8", "replace")[-300:])
    out = []
    for name in sorted(n for n in result.stdout.decode("utf-8").split("\0") if n):
        path = root / name
        if not path.is_file():
            continue
        try:
            out.append((name, path.read_bytes().decode("utf-8")))
        except UnicodeDecodeError:
            continue
    return out


# ------------------------------------------------------------- rendering


def expand(value: str, entry: dict) -> str:
    """Placeholders replaced: {Qn} by the quote in quotation marks,
    {mention:x} by x in quotation marks."""
    quotes = {QUOTE_KEY.fullmatch(q["key"]).group(2): q["text"]
              for q in entry.get("quotes") or []}

    def one(match: re.Match) -> str:
        token = match.group(1)
        q = QUOTE_PLACEHOLDER.fullmatch(token)
        if q:
            return '"%s"' % quotes[q.group(1)]
        return '"%s"' % token[len(MENTION_PREFIX):]

    return PLACEHOLDER.sub(one, value)


def render_urls(entry: dict) -> str:
    parts = []
    for url in entry["urls"]:
        text = "[%s](%s)" % (expand(url["label"], entry), url["url"])
        if url.get("prefix"):
            text = expand(url["prefix"], entry) + " " + text
        if url.get("suffix"):
            text = text + " " + expand(url["suffix"], entry)
        parts.append(text)
    return "; ".join(parts) if parts else NO_URL


def render_claims(entry: dict) -> str:
    """Each claim as `S`, `S (scope)` and then `; note`, joined by `; `."""
    parts = []
    for claim in entry["claims"]:
        text = claim["status"]
        if claim.get("scope"):
            text += " (%s)" % expand(claim["scope"], entry)
        if claim.get("note"):
            text += "; " + expand(claim["note"], entry)
        parts.append(text)
    return "; ".join(parts)


def sort_key(entry: dict, order: dict[str, tuple[int, int]]):
    family, nn = ENTRY_ID.fullmatch(entry["id"]).groups()
    return order[family] + (int(nn),)


def render(data: dict, companion: str) -> bytes:
    """The Markdown register, as LF bytes. Refuses data with findings."""
    problems = findings(data, companion)
    if problems:
        raise Refused("the register has %d finding(s); first: %s"
                      % (len(problems), problems[0]))
    _, order = _structure_findings(data)
    rows: dict[int, list[str]] = {}
    for entry in sorted(entries(data), key=lambda e: sort_key(e, order)):
        row = "| %s |" % " | ".join([
            entry["id"], expand(entry["citation"], entry), render_urls(entry),
            expand(entry["access_terms"], entry),
            expand(entry["definition"], entry), render_claims(entry),
            entry["authority"]])
        rows.setdefault(order[ENTRY_ID.fullmatch(entry["id"]).group(1)][0],
                        []).append(row)
    blocks = []
    for s, section in enumerate(data["sections"]):
        blocks.append("### %s\n\n%s\n%s" % (section["heading"], TABLE_HEADER,
                                            "\n".join(rows[s])))
    body = companion.replace(DIRECTIVE, "\n\n".join(blocks), 1)
    header = header_line()
    text = header + "\n" + body
    if not text.endswith("\n"):
        text += "\n"
    return text.encode("utf-8")


def header_line() -> str:
    register = layout.component(REGISTER_ID).path
    companion = layout.component(COMPANION_ID).path
    return ("<!-- Generated by tools/sources/build_register.py from %s and "
            "%s. Do not edit this file: edit those, then run the tool with "
            "--write. -->" % (register, companion))


def freshness_findings(committed: bytes | None, fresh: bytes,
                       where: str) -> list[str]:
    if committed is None:
        return ["%s does not exist; run with --write" % where]
    if committed != fresh:
        committed_lines = committed.decode("utf-8", "replace").split("\n")
        fresh_lines = fresh.decode("utf-8", "replace").split("\n")
        line = next((n for n, (a, b) in
                     enumerate(zip(committed_lines, fresh_lines), 1)
                     if a != b),
                    min(len(committed_lines), len(fresh_lines)) + 1)
        return ["%s differs from a fresh generation (first difference at "
                "line %d); edit the register or the companion and run with "
                "--write, never the Markdown" % (where, line)]
    return []


def shuffled(data: dict, seed: int) -> dict:
    """The same register with its entries in another order: rendering it
    must give the same bytes, because the inputs are sorted."""
    copy = dict(data)
    items = list(entries(data))
    random.Random(seed).shuffle(items)
    copy["entries"] = items
    return copy


# ------------------------------------------------------------- queries


def claims_at_or_above(data: dict, src_id: str, minimum: str) -> list[dict]:
    """The claims of one entry whose status is `minimum` or stronger.

    For P3: a `departs-from` must cite a claim at V or P, so it asks for
    `claims_at_or_above(data, id, "P")` and requires a non-empty answer.
    Unknown ids and statuses raise rather than return an empty list,
    because an empty list is also what a real but unverified entry
    returns.
    """
    if minimum not in STATUSES:
        raise ValueError("%r is not a status; expected one of %s"
                         % (minimum, ", ".join(STATUSES)))
    match = [e for e in entries(data) if e.get("id") == src_id]
    if len(match) != 1:
        raise KeyError("%s is not a register entry" % src_id)
    cut = STATUSES.index(minimum)
    return [dict(claim) for claim in match[0].get("claims") or []
            if claim.get("status") in STATUSES
            and STATUSES.index(claim["status"]) <= cut]


# ------------------------------------------------------------- command line


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--write", action="store_true",
                    help="regenerate the Markdown register")
    ap.add_argument("--register", type=Path, default=None)
    ap.add_argument("--companion", type=Path, default=None)
    ap.add_argument("--output", type=Path, default=None)
    ap.add_argument("--no-tracked", action="store_true",
                    help="skip scanning tracked files for SRC references")
    ap.add_argument("--claims", metavar="SRC-ID", default=None)
    ap.add_argument("--at-least", metavar="STATUS", default="L")
    args = ap.parse_args(argv)

    register_path, companion_path, output_path = default_paths()
    register_path = args.register or register_path
    companion_path = args.companion or companion_path
    output_path = args.output or output_path

    data = load(register_path)
    if args.claims:
        try:
            for claim in claims_at_or_above(data, args.claims, args.at_least):
                print(render_claims({"claims": [claim], "quotes": []}))
        except (KeyError, ValueError) as error:
            print(error.args[0], file=sys.stderr)
            return 2
        return 0

    companion = read_text(companion_path)
    problems = []
    if "\r" in read_text(register_path):
        problems.append("%s contains CR; the register is LF" % register_path)
    problems += findings(data, companion)
    if not args.no_tracked:
        problems += unknown_references(
            known_ids(data), tracked_texts(layout.repository_root()))
    if not problems:
        fresh = render(data, companion)
        if args.write:
            output_path.write_bytes(fresh)
            print("wrote %s (%d entries, %d bytes)"
                  % (output_path, len(entries(data)), len(fresh)))
        else:
            committed = output_path.read_bytes() if output_path.is_file() else None
            problems += freshness_findings(committed, fresh, str(output_path))
    for problem in problems:
        print("FINDING  " + problem)
    if problems:
        print("%d finding(s)" % len(problems))
        return 1
    if not args.write:
        print("ok: %d entries, %d claims, %d quotes; the Markdown is a fresh "
              "generation" % (len(entries(data)),
                              sum(len(e["claims"]) for e in entries(data)),
                              sum(len(e.get("quotes") or [])
                                  for e in entries(data))))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
