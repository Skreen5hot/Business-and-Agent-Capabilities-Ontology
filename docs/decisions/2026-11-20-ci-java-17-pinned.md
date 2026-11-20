# Decision record — CI pins Java 17 for the reasoners, 2026-11-20

Recorded verbatim by Claude Code (`claude-opus-5-5`) on 2026-11-20, from the answer the
product owner and architect, Aaron Damiano, gave in session. The act is the architect's.

## What it is about

| Field | Value |
| --- | --- |
| Finding | On 2026-11-20 the Checks run for pull request #67 (run 44733125350) failed at "The reasoners classify the module (ELK and HermiT)". The runner reported `openjdk version "25.0.5" 2026-10-20 LTS`. Real input passed, but none of the falsification cases was rejected (ELK: unsatisfiable, CAP-16; HermiT: unsatisfiable, CAP-16, inconsistent), so `reason.py` refused the run as evidence. The same step passed on `main` at `c35d373` on 2026-11-18 under `openjdk version "17.0.21"`, and passes locally under Java 23. Pull request #67 changes only two Markdown files |
| `.github/workflows/checks.yml` before the change | SHA-256 `5bd5f219aadb793cea54bca57753cdfd4fc244829e506f8e489a35f1dc147f2b`, at `main` `c35d373` |
| `config/reasoner-pins.yaml` before the change | SHA-256 `930ce2cf0e8d23ab6c71e4de834c5bdc73855bf9e4cde0b05619989de09f6b84`. It left Java to the machine ("Java is the machine's"), under D5-7 |

## The act

Asked "Pin Java 17 in the CI workflow so the reasoner check works again?", the architect
answered:

````text
Yes, pin Java 17
````

## What it does

- **Java is pinned in CI.** Both workflow jobs that run the reasoners, the checkpoint (S05-D,
  S05-D2) and S06-U2, set up Temurin 17 with `actions/setup-java`. The action is pinned by
  commit, `d1374f8ac74474200d16ef8ecee22c7ae7a51880` (v6.3.0, its latest release, read from
  GitHub on 2026-11-20).
- **The pin is noted in `config/reasoner-pins.yaml`.** Its comment now says CI pins Temurin
  17. Locally, Java is still the machine's. ROBOT, ELK and HermiT keep their pins.

## What it does not do

- It does not explain why the falsification cases pass under Java 25. That is not
  investigated here, and a result under Java 25 is not evidence until it is.
- It changes no reasoner, ROBOT pin, module or check.
