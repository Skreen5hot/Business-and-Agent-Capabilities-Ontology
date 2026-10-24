# Decision record — ADR-003 batch-act digest confirmed; ratification timing set, 2026-10-23

Recorded verbatim by the setup agent (Claude Code, `claude-opus-5-5`) on 2026-10-23, at the
statement the product owner and architect, Aaron Damiano, made in session. The act is his.

**What this decides:**
- Each concept IRI listed in a batch ratification act must carry the SHA-256 of that
  concept's record (ADR-003 D5).
- ADR-003 stays PROPOSED on PR #1 until the P2 trial findings are signed off, and is then
  ratified and merged.

**What it does not do:** it does not ratify ADR-003.

---

````text
1. Batch Act Digest Confirmed The requirement that each IRI in a batch ratification act must include the SHA-256 digest of its concept record is approved and locked. This provides a bidirectional cryptographic lock: the decision pins the exact state of each concept, and the concept pins the decision commit and file hash.

2. ADR-003 on PR #1 Acknowledged. Leaving ADR-003 as `PROPOSED` on PR #1 while P1 and P2 run is the correct posture. We will formally ratify and merge ADR-003 once the P2 trial findings are signed off.

3. Expectations for P1 & P2 Reviews When each session reports back with its PR:

* For P1 (Source Register as Data):

   * Verification that all 63 register entries round-trip cleanly from `docs/sources/register.yaml` to `register.md`.

   * Hard CI failures for quotes exceeding 15 words and any missing/malformed V/P/S/K/L claim codes.

* For P2 (LinkML Trial):

   * Pinned release details in the trial environment.

   * Byte-for-byte diff report across consecutive builds.

   * Explicit go/no-go recommendation on `gen-shacl` versus handwritten SHACL shapes.

Worktrees and parallel execution are approved. Awaiting the PR links and test outputs for P1 and P2.
````

---

## Effect

- **ADR-003 D5:** the record digest per listed IRI is no longer an open detail. It is
  confirmed, and ADR-003's last section says so.
- **Order:** P2 sign-off comes first, then ADR-003 is ratified and merged.
- **P1 review criteria:**
  - all 63 entries round-trip from `register.yaml` to the Markdown register;
  - hard failures for quotes over 15 words and for missing or malformed V/P/S/K/L codes.
- **P2 review criteria:**
  - the pinned release;
  - a byte-for-byte diff report across consecutive builds;
  - an explicit go/no-go on `gen-shacl` versus hand-written SHACL.
