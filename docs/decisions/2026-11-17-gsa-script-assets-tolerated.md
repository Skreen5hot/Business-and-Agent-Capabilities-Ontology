# Decision record — GSA website policies page: added or removed script assets tolerated, 2026-11-17

Recorded verbatim by Claude Code (`claude-opus-5-5`) on 2026-11-17, from the decision the
architect, Aaron Damiano, Product Owner and Ontology Architect, gave in session after PR
#61 merged into `main` as `f4046e6`. The act is the architect's. This record makes none.

## What it is about

`main` at `f4046e6e8f0dab84746d045b7b8d548bca565d8f` (PR #61 merged):

| Record | SHA-256 at `f4046e6` |
| --- | --- |
| `tools/inventory/rights.py` (the bounded check whose GSA rule this widens) | `8b8419843628ef807adc455e627fa630f1f331a4a22ac6384b2c441a3257dd78` |
| `docs/decisions/2026-11-17-fibf-drift-disposition-accepted.md` (the decision it extends) | `4de239b9107fc516589f96d58693bfee753fe194b71dd64db3bfe7d03d8f4b0b` |
| `docs/sources/inventory/rights.yaml` (the pins, all retained) | `0d3eca02f6156506a62a6e15e676d640c83623e846abc69d5c4116c34effebfe` |

The finding it answers: the networked check (CI run 44067548004) failed the GSA website
policies page on one difference the disposition had not identified, an added
`<script src="/core/assets/vendor/ckeditor5/ckeditor5-dll/ckeditor5-dll.js?v=47.6.3-drupal.1">`
in the page footer. No text, link or rights language changed.

## The question put

> How should the added ckeditor5 script on GSA's policies page be treated?

The options offered: extend the GSA rule so that added or removed script elements count as
asset changes (a wider tolerance, needing approval), or keep the rule and let the job fail.

## The decision

> Tolerate script assets

## How it is applied

- **The scope of the change.** In `tools/inventory/rights.py`, the `gsa-drupal-page`
  comparison, and only that one, no longer compares external script elements: a `<script>`
  with a same-site `src` (a path beginning `/`, not `//`) and no body. Such elements may be
  added, removed or reordered.
- **What still fails:**
  - an inline script;
  - a script with a body;
  - a script loaded from another host;
  - any other tag, attribute, link or text outside the three regions already tolerated.
- **Visible changes.** The presentation-drift report names the added and removed script
  paths.
- **What is unchanged:**
  - the FIBF build-number rule;
  - the strictness of every other document;
  - every pin;
  - the licensing disposition.

## Closure of the FIBF source-drift issue

The decision of 2026-11-17 (`docs/decisions/2026-11-17-fibf-drift-disposition-accepted.md`,
section 7) closes the issue once the corrected check passes against the documented
evidence. It did, in CI run 44072906624, dispatched on `sources/gsa-script-assets` at
`8377273` and merged into `main` as `26d477f` (PR #62):

- **`rights.py --confirm`:** 73 evidence items re-confirmed. 27 byte mismatches, each
  classified as verified presentation-only drift, and every pin stands:
  - 26 FIBF pages: the asset build number;
  - the GSA policies page: navigation, Drupal settings, asset versions and the added
    same-site script `ckeditor5-dll.js`.
- **`harvest_federal.py --confirm`:** it ran again, after being blocked since 2026-11-02.
  Every federal inventory output is byte-identical to a fresh harvest of the refetched
  documents.

**The FIBF source-drift issue is closed.** CP-3, the accepted register batch and the
licensing decisions were not reopened.
