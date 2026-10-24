# Decision record — Response to review R6 accepted, 2026-10-24

Recorded verbatim by the setup agent (Claude Code, `claude-opus-5-5`) on 2026-10-24, at the
statement the product owner and architect, Aaron Damiano, made in session. The act is his.

---

````text
I accept the R6 response as proposed, including treating the catalog revisions as editorial (same IRIs) and publishing R6. Record the acceptance and merge PR #7 with a merge commit.
````

---

## What it rests on

PR #7, head `c7264cf623b1ccf46eefd8d7d09a68d7d19eeec4` on branch `ccv/r6-review-response`.
All CI jobs passed at that head.

## Effect

1. **R6 is published.** The external review is filed verbatim at
   `reviews/R6-vocabulary-review.md`, as received, and rendered on the site's Reviews page.
   The architect has decided it may be public.
2. **The disposition in `reviews/R6-disposition.md` is accepted.** Its 39 rows stand:
   - 20 answered by spec v0.4;
   - 8 accepted and done in PR #7;
   - 6 deferred to spec v0.5;
   - 2 deferred to RP-1 (F2, material basis);
   - 1 deferred to RP-10 (F1, admissibility);
   - 2 deferred to CP-n.

   The rows deferred to RP-1, RP-10 and spec v0.5 are **not decided here**. They are inputs
   to those decisions.
3. **The catalog revisions are editorial** under ADR-003 D3. The five catalog concepts keep
   their IRIs. Their definitions were generalised per R6 §3 (Competitive Analysis aligned
   with CD2), and each record links its P5 version through `revises`.
4. **Source references state their support.** Every `consistent-with` citation now carries
   `support: definitional | contextual`: 5 definitional, 36 contextual, and none of the
   catalog citations definitional.
5. **Ratification acts record their basis.** A `bco-ratification` block now requires:
   - editorial and ontological approvals, each a declared `prov:Person`;
   - a validation commit with the list of gates that passed.

   This is additive to the P3-accepted format. ADR-003 D5 (explicit IRIs plus record
   digests) is unchanged.
6. **The site has a Reviews page** rendering every review, with prefixed, unique ids, at
   the existing `review/` URL.
7. **PR #7 merges to `main` with a merge commit.**

## What this does not do

- **It ratifies no concept.** All 14 remain Draft. Their record digests changed in PR #7;
  the PR body lists the current ones.
- **It does not decide RP-1, RP-10, or any spec v0.5 change.**
- **It does not change the specification or `ontology/`.**

## Carried forward

- A ratification act's gates are recorded but not re-run.
- The Status page's "Authored terms checked: 0" wording is stale.
- LinkML does not refuse `support` on adapted-from or departs-from; the build and the
  shapes do.
- R6 §4.2's temporal-context point has no row of its own; the spec's known limits cover it.
