# SPDX-License-Identifier: MIT
"""The citation register is data, and its rules are hard failures.

ADR-003 D6 (proposed): `docs/sources/register.yaml` is the source of
truth, the Markdown register is generated from it, and a claim status
outside V/P/S/K/L, a quote over 15 words, a bad quote key or an unknown
SRC id fails the build.

Every refusal below is falsified the same way (PROCESS.md section 2): the
committed register is copied, one thing is broken, the test asserts the
copy really differs from the original, and then requires the specific
finding -- not just any finding -- while the unbroken register has none.
"""

from __future__ import annotations

import copy

import pytest

from conftest import load_tool


@pytest.fixture(scope="module")
def reg():
    return load_tool("bco_build_register", "tools/sources/build_register.py")


@pytest.fixture(scope="module")
def paths(reg):
    return reg.default_paths()


@pytest.fixture(scope="module")
def data(reg, paths):
    return reg.load(paths[0])


@pytest.fixture(scope="module")
def companion(reg, paths):
    return reg.read_text(paths[1])


def entry(data, entry_id):
    return next(e for e in data["entries"] if e["id"] == entry_id)


def broken(data, entry_id, mutate):
    """A deep copy with one entry mutated, asserted to differ."""
    changed = copy.deepcopy(data)
    mutate(entry(changed, entry_id))
    assert changed != data, "the mutation changed nothing"
    return changed


def require(reg, data, companion, expected):
    """The specific finding is reported for the broken copy. That the
    unbroken register has no findings at all is
    test_the_committed_register_has_no_findings."""
    problems = reg.findings(data, companion)
    assert any(expected in p for p in problems), (
        "expected a finding containing %r; got %s" % (expected, problems))
    return problems


# ------------------------------------------------------------- the register


def test_the_committed_register_has_no_findings(reg, data, companion):
    assert reg.findings(data, companion) == []


def test_the_register_is_not_empty_by_accident(reg, data):
    """Guards the test above: an empty register has no findings either --
    except the count guard, which this pins independently."""
    entries = data["entries"]
    assert len(entries) == reg.EXPECTED_ENTRY_COUNT == 63
    assert sum(len(e["claims"]) for e in entries) >= 63
    assert sum(len(e.get("quotes") or []) for e in entries) >= 20
    families = {e["id"].split("-")[1] for e in entries}
    assert families == {"ISO", "OMG", "OG", "GOV", "IND", "FO", "MS", "BA"}


def test_no_tracked_file_names_an_unknown_src_id(reg, data, repo):
    texts = reg.tracked_texts(repo)
    assert any(path == "docs/sources/register-companion.md"
               for path, _ in texts), "the scan did not reach the companion"
    assert reg.unknown_references(reg.known_ids(data), texts) == []


def test_the_committed_markdown_is_a_fresh_generation(reg, data, companion,
                                                      paths):
    fresh = reg.render(data, companion)
    assert paths[2].read_bytes() == fresh, (
        "docs/sources/business-capability-definition-sources.md differs from "
        "a fresh generation; edit register.yaml or the companion and run "
        "tools/sources/build_register.py --write")


def test_generation_is_deterministic_and_lf(reg, data, companion):
    first = reg.render(data, companion)
    assert reg.render(copy.deepcopy(data), companion) == first
    for seed in (1, 2, 3):
        assert reg.render(reg.shuffled(data, seed), companion) == first, (
            "entry order in the YAML changed the output; inputs must be sorted")
    assert reg.shuffled(data, 1)["entries"] != data["entries"], (
        "the shuffle was a no-op, so the order test tested nothing")
    assert b"\r" not in first
    assert first.endswith(b"\n")


def test_every_entry_and_quote_reaches_the_markdown(reg, data, companion):
    """Guards the freshness test: a renderer that dropped rows would still
    be compared against its own output."""
    text = reg.render(data, companion).decode("utf-8")
    # Entry rows have seven cells; the conflict matrix's rows have eight.
    rows = [line for line in text.split("\n")
            if line.startswith("| SRC-") and line.count(" | ") == 6]
    assert len(rows) == 63
    for e in data["entries"]:
        assert any(row.startswith("| %s |" % e["id"]) for row in rows), e["id"]
        for q in e.get("quotes") or []:
            assert '"%s"' % q["text"] in text, q["key"]
    assert reg.DIRECTIVE not in text


# ------------------------------------------------------------- claim status


@pytest.mark.parametrize("bad", ["", None, "X", "v", "V (OWL)", "V/L", True,
                                 "Verified"])
def test_a_claim_status_outside_vpskl_is_refused(reg, data, companion, bad):
    def mutate(e):
        e["claims"][0]["status"] = bad
    changed = broken(data, "SRC-OMG-01", mutate)
    if bad in ("", None):
        require(reg, changed, companion, "SRC-OMG-01 claim 1 has no status")
    else:
        require(reg, changed, companion,
                "SRC-OMG-01 claim 1 has status %r; a status is exactly one "
                "of V, P, S, K, L" % (bad,))


def test_a_claim_without_a_status_field_is_refused(reg, data, companion):
    def mutate(e):
        del e["claims"][0]["status"]
    require(reg, broken(data, "SRC-ISO-01", mutate), companion,
            "SRC-ISO-01 claim 1 has no status")


def test_an_entry_without_claims_is_refused(reg, data, companion):
    def mutate(e):
        e["claims"] = []
    require(reg, broken(data, "SRC-ISO-01", mutate), companion,
            "SRC-ISO-01 has no claims")


# ------------------------------------------------------------- quotes


def test_a_quote_over_15_words_is_refused(reg, data, companion):
    def mutate(e):
        e["quotes"][0]["text"] = " ".join(["word"] * 16)
    require(reg, broken(data, "SRC-OMG-01", mutate), companion,
            "SRC-OMG-01 quote 1 is 16 words; a quote may be at most 15")


def test_a_quote_of_exactly_15_words_passes(reg, data, companion):
    """The boundary, so the limit is shown to be 15 and not 14 or 16."""
    def mutate(e):
        e["quotes"][0]["text"] = " ".join(["word"] * 15)
    assert not any("words" in p for p in
                   reg.findings(broken(data, "SRC-OMG-01", mutate), companion))


def test_an_ellipsis_is_not_counted_as_a_word(reg):
    assert reg.quote_words("an ability that an active structure element "
                           "… possesses") == 8


@pytest.mark.parametrize("key, expected", [
    (None, "has no key"),
    ("", "has no key"),
    ("SRC-OMG-01-Q0", "has malformed key"),
    ("SRC-OMG-01-q1", "has malformed key"),
    ("SRC-OMG-01-Q01", "has malformed key"),
    ("SRC-OMG-01", "has malformed key"),
    ("SRC-OMG-03-Q1", "belongs to another entry"),
])
def test_a_missing_or_malformed_quote_key_is_refused(reg, data, companion,
                                                     key, expected):
    def mutate(e):
        if key is None:
            del e["quotes"][0]["key"]
        else:
            e["quotes"][0]["key"] = key
    require(reg, broken(data, "SRC-OMG-01", mutate), companion, expected)


def test_a_duplicate_quote_key_is_refused(reg, data, companion):
    def mutate(e):
        e["quotes"].append(dict(e["quotes"][0]))
    require(reg, broken(data, "SRC-OMG-01", mutate), companion,
            "SRC-OMG-01 quote 2 duplicates key SRC-OMG-01-Q1")


def test_more_than_one_quote_in_an_entry_is_refused(reg, data, companion):
    def mutate(e):
        e["quotes"].append({"key": "SRC-OMG-01-Q2", "text": "deliver value"})
        e["definition"] += " {Q2}"
    require(reg, broken(data, "SRC-OMG-01", mutate), companion,
            "SRC-OMG-01 has 2 quotes; the register allows at most 1")


def test_a_quotation_mark_typed_into_prose_is_refused(reg, data, companion):
    """Quotes move out of prose: a verbatim quotation typed into a field
    would escape the word limit and the key."""
    def mutate(e):
        e["definition"] += ' It says "an unregistered quotation".'
    require(reg, broken(data, "SRC-ISO-01", mutate), companion,
            "SRC-ISO-01 definition has a quotation mark typed into prose")


def test_a_quote_placed_nowhere_or_twice_is_refused(reg, data, companion):
    def nowhere(e):
        e["definition"] = e["definition"].replace("{Q1}", "it")
    require(reg, broken(data, "SRC-OMG-01", nowhere), companion,
            "SRC-OMG-01-Q1 is placed 0 times")

    def twice(e):
        e["definition"] += " {Q1}"
    require(reg, broken(data, "SRC-OMG-01", twice), companion,
            "SRC-OMG-01-Q1 is placed 2 times")


def test_a_placeholder_naming_no_quote_is_refused(reg, data, companion):
    def mutate(e):
        e["definition"] += " {Q1}"
    require(reg, broken(data, "SRC-ISO-01", mutate), companion,
            "but SRC-ISO-01 has no quote SRC-ISO-01-Q1")


# ------------------------------------------------------------- references


def planted(family, nn):
    """Built at run time, so this file does not itself name an unknown id
    and trip the tracked-file scan it is testing."""
    return "SRC-" + family + "-" + nn


def test_an_unknown_src_id_in_an_entry_is_refused(reg, data, companion):
    ghost = planted("ISO", "99")

    def mutate(e):
        e["definition"] += " Compare " + ghost + "."
    require(reg, broken(data, "SRC-ISO-01", mutate), companion,
            "names %s, which is not a register entry" % ghost)


def test_an_unknown_src_id_in_the_companion_is_refused(reg, data, companion):
    ghost = planted("XYZ", "01")
    changed = companion + "\nSee " + ghost + ".\n"
    assert changed != companion
    require(reg, data, changed, "companion names %s" % ghost)


def test_shorthand_references_are_expanded_and_checked(reg, data, companion):
    """`SRC-FO-01, -02, -03` and `SRC-OG-01/02` name three and two ids;
    a scan reading only the first would miss a dangling continuation."""
    assert reg.references(planted("FO", "01") + ", -02, -03") == [
        planted("FO", "01"), planted("FO", "02"), planted("FO", "03")]
    assert reg.references(planted("OG", "01") + "/02") == [
        planted("OG", "01"), planted("OG", "02")]
    changed = companion + "\n" + planted("FO", "01") + ", -99\n"
    require(reg, data, changed, "names %s" % planted("FO", "99"))


def test_an_unknown_src_id_in_a_tracked_file_is_reported(reg, data):
    ghost = planted("BA", "42")
    problems = reg.unknown_references(
        reg.known_ids(data), [("docs/elsewhere.md", "As " + ghost + " says.")])
    assert problems == ["docs/elsewhere.md names %s, which is not a register "
                        "entry" % ghost]


# ------------------------------------------------------------- round trip


def test_fewer_or_more_entries_than_recorded_is_refused(reg, data, companion):
    fewer = copy.deepcopy(data)
    fewer["entries"] = fewer["entries"][:-1]
    assert len(fewer["entries"]) == 62
    require(reg, fewer, companion, "the register has 62 entries; it had 63")

    more = copy.deepcopy(data)
    extra = copy.deepcopy(entry(data, "SRC-BA-09"))
    extra["id"] = planted("BA", "10")
    more["entries"].append(extra)
    assert len(more["entries"]) == 64
    require(reg, more, companion, "the register has 64 entries; it had 63")


def test_a_duplicate_entry_id_is_refused(reg, data, companion):
    def mutate(e):
        e["id"] = "SRC-BA-08"
    require(reg, broken(data, "SRC-BA-09", mutate), companion,
            "SRC-BA-08 is declared 2 times")


def test_the_companion_must_state_the_real_count(reg, data, companion):
    changed = companion.replace("records 63 sources", "records 64 sources")
    assert changed != companion
    require(reg, data, changed, "the companion states ['64']")


def test_a_markdown_edited_by_hand_is_refused(reg, data, companion, paths):
    committed = paths[2].read_bytes()
    edited = committed.replace(b"| SRC-OMG-03 |", b"| SRC-OMG-03  |", 1)
    assert edited != committed
    problems = reg.freshness_findings(edited, reg.render(data, companion),
                                      "register.md")
    assert problems and "differs from a fresh generation" in problems[0]
    assert reg.freshness_findings(committed, reg.render(data, companion),
                                  "register.md") == []


def test_render_refuses_data_with_findings(reg, data, companion):
    def mutate(e):
        e["claims"][0]["status"] = "Q"
    with pytest.raises(reg.Refused):
        reg.render(broken(data, "SRC-OMG-01", mutate), companion)


# ------------------------------------------------------------- schema


@pytest.mark.parametrize("mutate, expected", [
    (lambda e: e.update(staus="V"), "has unknown field 'staus'"),
    (lambda e: e["claims"][0].update(locus="x"), "claim 1 has unknown field"),
    (lambda e: e.update(authority="A10"), "has authority 'A10'"),
    (lambda e: e.pop("citation"), "has no citation"),
    (lambda e: e.update(definition="a | b"), "contains '|'"),
    (lambda e: e.update(definition="{quote:x}"), "unknown placeholder"),
    (lambda e: e["urls"][0].update(url="www.example.org"), "no http(s) url"),
])
def test_schema_refusals(reg, data, companion, mutate, expected):
    require(reg, broken(data, "SRC-OMG-01", mutate), companion, expected)


# ------------------------------------------------------------- queries


def test_claims_at_or_above(reg, data):
    """For P3: a departs-from must cite V or P (ADR-003 D6)."""
    for src in ("SRC-OMG-01", "SRC-OMG-03", "SRC-OMG-04", "SRC-GOV-04"):
        found = reg.claims_at_or_above(data, src, "P")
        assert found and all(c["status"] == "V" for c in found), src
    assert reg.claims_at_or_above(data, "SRC-OG-03", "P") == []
    assert [c["status"] for c in
            reg.claims_at_or_above(data, "SRC-OG-03", "L")] == ["S", "L"]
    assert [c["scope"] for c in
            reg.claims_at_or_above(data, "SRC-MS-04", "V")] == ["citation"]
    assert [c["status"] for c in
            reg.claims_at_or_above(data, "SRC-MS-04", "K")] == ["V", "K"]


def test_claims_at_or_above_refuses_what_it_cannot_answer(reg, data):
    with pytest.raises(KeyError):
        reg.claims_at_or_above(data, planted("ISO", "99"), "P")
    with pytest.raises(ValueError):
        reg.claims_at_or_above(data, "SRC-OMG-01", "A")


def test_claims_at_or_above_returns_copies(reg, data):
    found = reg.claims_at_or_above(data, "SRC-OMG-01", "V")
    found[0]["status"] = "L"
    assert entry(data, "SRC-OMG-01")["claims"][0]["status"] == "V"


# ------------------------------------------------------------- command line


def test_the_command_line_check_passes_and_fails(reg, paths, tmp_path, capsys):
    assert reg.main([]) == 0
    stale = tmp_path / "register.md"
    stale.write_bytes(paths[2].read_bytes() + b"\nhand edit\n")
    assert reg.main(["--output", str(stale), "--no-tracked"]) == 1
    assert "differs from a fresh generation" in capsys.readouterr().out
