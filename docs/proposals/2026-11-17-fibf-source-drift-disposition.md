# FIBF source drift: disposition for the architect's approval

| Field | Value |
|---|---|
| Authority | The architect's confirmation of 2026-11-17, item 3 (a bounded investigation of the FIBF drift) |
| Source | `fibf-2026-10-28` in `docs/sources/inventory/rights.yaml` (rights review of 2026-10-28, `docs/decisions/2026-10-28-i2a-decided.md`) |
| Prepared by | Claude Code (`claude-opus-5-5`), 2026-11-17 |
| Status | Proposed. Nothing is re-pinned, and no licensing or redistribution status is changed |

## 1. What failed

The weekly CI job, "Rights documents are still served as pinned", runs `rights.py --confirm`. It has failed since 2026-11-02, most recently in run 44048548873 (2026-11-17, `main` at `ff49142`).

**27 evidence items** no longer match their pins:

- the FIBF index;
- the 25 FIBF domain pages;
- GSA's website policies page.

**Not affected:**

- all 39 FIBF workbooks;
- the FEAF/BRM items;
- the APQC item.

Those still match. So the drift is confined to HTML pages. Not one data file has changed.

## 2. The affected documents

| Evidence | Approved URL | Pinned SHA-256 (bytes) | Served 2026-11-17 SHA-256 (bytes) |
|---|---|---|---|
| `fibf-index-page` | https://ussm.gsa.gov/fibf/ | `9d32b82c297961d248592a13818069ddf857b05926caf3e1331cc00266e8f49a` (101877) | `4a8a1e24e8ab987344b7992bf68bc821df3dae2c93304dba5dbb38238efc0e1b` (101877) |
| `fibf-page-cw` | https://ussm.gsa.gov/fibf-cw/ | `3916f84364e71d06795966f12787a4b24114e77ad5ffef05ed68bc59052c83e9` (83227) | `d96ec28f8d7a1bd00d1bfb221f881c72312526b25033c62b853f6ff370e61c0a` (83227) |
| `fibf-page-cyb-cvd` | https://ussm.gsa.gov/fibf-cyb-cvd/ | `d6e986b9eb95ea507fbf7750ccc0662906750fa33e4d82d347ec673fb938def0` (79832) | `c6dc472fb95a1fcb21a9ee42c7b86a00b099b86e516046d3e5011afb1ce15530` (79832) |
| `fibf-page-cyb-soc` | https://ussm.gsa.gov/fibf-cyb-soc/ | `ddb536706e4a238ad063108252fc3f9f48bfcd745d5e2d3a0d7b3c2f98e86b2f` (87056) | `b6362ed871b0cc2d00947fc90405aa9ab27a9a58c58f84ccf2877e62525ffd3c` (87056) |
| `fibf-page-erm` | https://ussm.gsa.gov/fibf-ERM/ | `8e642c484b7b9748f78c7d447ca2147ff4e136032e89488dd0d770fcef848816` (83683) | `39d1d3d9621a6c9a742192092fde0e8219c38f335cd361b91e22286e585aae0f` (83683) |
| `fibf-page-fm` | https://ussm.gsa.gov/fibf-fm/ | `ebee75a98c6630ca23b3ba8755a54078b6e4d5eded669b708e1d693ed318b823` (95294) | `721f6537afe7ac24cad628ba3803048e238e2dd8c0cb8709883b3e08b06b4ead` (95294) |
| `fibf-page-gm` | https://ussm.gsa.gov/fibf-gm/ | `979994981d2b36fc36f699ce50ca355a86de101b6ac85a2bfa0fbd131afef81b` (86754) | `32e2820cb4c0af8be3cb4f490488f7d96fd3d994ed2e007313b3df0a7ecfca66` (86754) |
| `fibf-page-hr-hcm` | https://ussm.gsa.gov/fibf-hr-hcm/ | `7a2a29de46bade3ff99c8b3ecf6e2a0d36af9bd721be92d166bd371cffa995a3` (75915) | `5a1cde92a28499fad27d1637d999f5c9405b01420823dc1e8535ec240de1e9f4` (75915) |
| `fibf-page-hr-hcs` | https://ussm.gsa.gov/fibf-hr-hcs/ | `1a4286806ced4d63aaf011ad3171d2a013f7a02c02a93c09c9143137527e7b81` (89574) | `f83e14608430d24923a43904af1f5d027675e34d0acfb1fa8a76d0d08cab9733` (89574) |
| `fibf-page-hr-hce` | https://ussm.gsa.gov/fibf-hr-hce/ | `16a3fcbe0f555ac8094d5064fdac9053a0b13a2766d1e9bd03cd104ed1080510` (86267) | `babab167131bde1b7a50f2fbd16cf0c0cf15066573e71c6358fe20806cb2be15` (86267) |
| `fibf-page-hr-ac` | https://ussm.gsa.gov/fibf-hr-ac/ | `3b9d1888aadb0157a17d9f42906591f73b41d76a97a5139533715bdc3333bbb5` (90437) | `c186a7360095ccc1f7f1bd3072546a20ba729cf2fa59b4a38e4efb9072d46425` (90437) |
| `fibf-page-hr-td` | https://ussm.gsa.gov/fibf-hr-td/ | `e04acbbf6e47430e7482c5d0c7919f689466fe4cfd9f1228196d4db88d9222d5` (88002) | `106f693196b008fc23f137bb98e038909dfa153a79f10abf22e756d8af129558` (88002) |
| `fibf-page-hr-epm` | https://ussm.gsa.gov/fibf-hr-epm/ | `f07b3d6ce8a368e9ada9a9261bfdc7190f5721ab1f430227759e132c89d19ec1` (88362) | `819e6a9ecfcbef348b477b062dc8ab7a8e86c97224c8c554b7d3c679fca1f1d9` (88362) |
| `fibf-page-hr-cb` | https://ussm.gsa.gov/fibf-hr-cb/ | `6b0c5c319fb13b668deb6f75699c53c8b03cb13f87a174e46ccf44f977728517` (88688) | `c1b7cadec0f8212e104c16aa144d8f507c2b0173fae378f86ee45a38885a2474` (88688) |
| `fibf-page-hr-sep-ret` | https://ussm.gsa.gov/fibf-hr-sep-ret/ | `d6e4db246fc6baec49d079513cf8300dfb774e3287a09788947181d07d277b68` (86929) | `b84f101133a4897181e5f3ce4ecf1db05924491fd72e1ec481b50291e3efd579` (86929) |
| `fibf-page-hr-ea` | https://ussm.gsa.gov/fibf-hr-ea/ | `efd76b2ef97355fb61755cc659309c2ee25a9acc880119541a8727c568be0965` (87374) | `6c1b697915033809f4c38acb9eb6a7512523ef50aedb2ba095f607bf81876f28` (87374) |
| `fibf-page-hr-lr` | https://ussm.gsa.gov/fibf-hr-lr/ | `1b33db2b9f86a76f8590fb03ea22f422d8ce65aab1171fd7912a78f37efbc6b1` (87982) | `6627131dc1c60ebedfc91caf48002057678c036fa53ec2caab59b8f639add93d` (87982) |
| `fibf-page-hr-hca` | https://ussm.gsa.gov/fibf-hr-hca/ | `e96fe1f967416af750395676ddc7c6669199ecf41da68232a7171cd3ac64db16` (90250) | `054dc00a599294693d8a95ff14c5104ff5bc725ea134892e04c7c95bf103d7a8` (90250) |
| `fibf-page-hr-par` | https://ussm.gsa.gov/fibf-hr-par/ | `22e3f372e0901cc37f93098311126159c8432cfbec9fa0e75d126e869585ac4c` (86692) | `f943f8e81fc8775a005e6a31a42e19c876786a5a8a1e8418c9310c33597f90d6` (86692) |
| `fibf-page-mom` | https://ussm.gsa.gov/fibf-mom/ | `420e8c609ada4dfbbefffc7a58a5e936600dd35d65e34a2143bb8d2379e3de62` (84641) | `33f3f3b5311817c862ce9a10398537af8eb5684c4a7ee82d936a3de395fc1613` (84641) |
| `fibf-page-rpm` | https://ussm.gsa.gov/fibf-RPM/ | `bb6ac21dcd6ef7fd0ecef59bd2b7c8b6c5ddde2e59249e60b1abf55f970a1b97` (89690) | `a6aa3a7a87d4a0be5d7c13e25c201ab7674a71e0f62aed42a80e0eed6e227495` (89690) |
| `fibf-page-travel` | https://ussm.gsa.gov/fibf-travel/ | `c086cc7c629dc8305c1ae75255939f984792575a995effc74e84eec60806210b` (85560) | `a06bbf2963f1791a0c4bd71b5595ffe1310b86ca3197f7ad5638f6d49a3e9d61` (85560) |
| `fibf-page-eeo` | https://ussm.gsa.gov/fibf-eeo/ | `1d1edf3504e7c60866624aab8977672136cb6730485e99bec12f724bd6c7da54` (88557) | `6ab565522a47b825bad9268c0512735f7892920c024eb3a304dc99b2186f1252` (88557) |
| `fibf-page-foia` | https://ussm.gsa.gov/fibf-foia/ | `3332e8340f7b3de0f05a9c8e3223bbdafc4efd90b01a1b60cef65e9ca03a557c` (75617) | `566617860197916d408b32a7c23fb27371a2c31bbb2ad7b18a9bb450fb9fdf9c` (75617) |
| `fibf-page-its` | https://ussm.gsa.gov/fibf-its/ | `eea63678efd562436a5420aa6c9f6088114bc0f348e303dd9dff7b44a2df3292` (76544) | `6b46626096e7b0f694fab97f87c7b1a5108b54c6356fb2fecaf5f919ba54796c` (76544) |
| `fibf-page-rm` | https://ussm.gsa.gov/fibf-rm/ | `635f27e67211df3bc1dd31a3170925b2524d70c92a6b9e6cd1273ce4104052f4` (75387) | `d5908e922e809873a9c0f89af708b7f0fe2587a8abd135339d10ab9ab2f613d8` (75387) |
| `gsa-website-policies` | https://www.gsa.gov/website-information/website-policies | `58fb6f3eeb2788bbf691553894a1d88be2de8d6b94279e922c01cce91c04ac96` (188962) | `2d78cea2e4f4ca7dde5af08fa65855ede9e8a19c3e1a3511f9393218a10b0e56` (185387) |

## 3. What the difference is

**The 26 FIBF pages (the index and 25 domain pages): document metadata only.**

- **Where it is:** each page links its CSS and JavaScript with a 19-digit cache-busting build number. It was `1790778396531677562` on 2026-10-28 and is `1794604162961183849` now. Each page carries it 9 times.
- **The proof:** I put the old build number back into the bytes served today. For **all 26 pages**, that gives exactly the pinned SHA-256.
- **What that rules out:** nothing else in any page changed. No text, link or line moved, and every byte count is identical.
- **Independent copy:** the Internet Archive holds a snapshot of the index (`20261107030843`) that is byte-identical to its pin.
- **Cause:** a rebuild of the USSM site, not a change in what the pages say.

**GSA website policies page: page furniture changed; the content did not.**

- **The original is preserved independently.** The Internet Archive holds the pinned bytes exactly, at snapshots `20261023063449` and `20261028084510`, as `https://web.archive.org/web/20261028084510id_/https://www.gsa.gov/website-information/website-policies`.
- **The page changes often.** Archived copies show it changing every few days, and today's bytes equal the snapshot of `20261113042134`.
- **What differs, original against today:**
  - the site navigation menu, which was restructured;
  - Drupal's settings script;
  - asset version tokens.
- **The `<main>` region:** its extracted text is identical. Its bytes differ only by one blank line that moved.
- **Delivery and access:** no transport problem. Repeated fetches return the same bytes, with HTTP 200.

## 4. Rights and redistribution language

**None changed.**

- **FIBF pages:** their text is unchanged byte for byte, apart from the build number. The pages still carry no copyright or licence notice, as the review recorded.
- **GSA website policies:** the "Reuse and copyright" section is identical. The review's quotation still appears as quoted.
- **Workbooks:** they are unchanged, so the MITRE notices the review recorded are unchanged too.

## 5. What is affected in the repository

**Affected: only the byte pins and the CI check.**

- **`docs/sources/inventory/rights.yaml`:** the 27 `sha256` values (and, for the policies page, `bytes`). The checked statements and the quotation remain true of the content served.
- **`docs/sources/inventory/fibf-entries.yaml` and `fibf-snapshot.yaml`:** they cite `fibf-page-eeo` as a catalog document, with its `document_sha256` and `html_line` locators. They also cite `fibf-page-its` in a draft basis.
  - The build number is replaced in place, so every line and element they locate is unchanged.
  - What was extracted from those pages is still what the pages say.
- **`config/inventory-federal-sources.yaml`:** it lists the index and the policies page as context evidence. Its licence (`LicenseRef-US-Government-Work`) rests on the policies text, which is unchanged.
- **The weekly harvest step:** `harvest_federal.py --confirm` is skipped while `rights.py --confirm` fails. It has therefore not run against fresh downloads since 2026-11-02, though its offline check passes on every commit.

**Not affected:**

- the vocabulary;
- the catalog's dispositions;
- the licensing disposition;
- NOTICE files;
- anything published.

## 6. Recommendation

**Retain the original pins.** The approved evidence is still exactly what the review assessed:

- the byte pins stay as they are;
- for the FIBF pages, the pinned bytes can be rebuilt reproducibly from today's pages;
- for the policies page, the pinned bytes are in an independent archive.

Neither updating the pins nor replacing the locators is warranted, since the source identity and content are unchanged. Suspending reliance is not warranted either, since no rights language moved.

**With it, two bounded follow-ups, each needing your approval:**

1. **Record this disposition** against `fibf-2026-10-28`. It would sit as an addendum in `rights.yaml`'s evidence notes, beside the original pins, not replacing them. It would give:
   - the build-number explanation;
   - the archive snapshots that hold the original bytes;
   - today's digests, as observed copies, not as pins.
2. **Make the weekly check say what it found.** Today it cannot tell a rebuilt site from a changed document.
   - **Proposed change:** keep the byte check. When the bytes differ, have `--confirm` also test whether the difference is the asset build number only (FIBF pages) or furniture outside `<main>` (the policies page).
   - **Effect on the job:** it would still report every byte mismatch, but classify it, and fail only on a change in content.
   - **Why it needs your approval:** it changes a check's pass condition. I won't make that change without it. Until then, the job stays red and visible.

## 7. What this does not do

- It doesn't change the licensing disposition or public redistribution status.
- It doesn't accept changed terms. None were found.
- It doesn't replace any source.
- It doesn't review the wider rights policy.
- It keeps the pinned evidence and the 2026-10-28 review exactly as they are.
