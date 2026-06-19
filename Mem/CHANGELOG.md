# Changelog

Append-only log of the recursive-improvement loop. Newest entries are inserted
directly below the marker by `Scripts/research.py`.

<!-- LOOP-ENTRIES -->

## Qualitative research pass — 2026-06-19 (Claude /research)

- **Result: no dataset change.** Searched recent public statements for new dated
  Dario Amodei / Anthropic predictions since the last data update (2026-06-16).
  No genuinely new, verifiable dated prediction surfaced; the freshest essay
  ("Policy on the AI Exponential", 2026-06-10) is already tracked as
  `policy_exponential_year_or_two`.
- **No milestone resolved.** ASL-4 not reached; the interpretability-by-2027
  goal remains `in_window`; Claude Fable 5 (released 2026-06-09) is a model
  release, not a tracked prediction.
- **Watched signal (already logged):** Amodei continuing to soften the "~50% of
  entry-level white-collar jobs" claim (Fortune 2026-05-26; an ABC News
  interview). Leads noted but NOT added as citations — primaries were
  paywalled/bot-blocked at fetch time and the project requires a verified
  primary source before logging. To re-verify next pass.
- **Tooling note:** WebFetch succeeds for GitHub-raw essay mirrors but returns
  403 on darioamodei.com and major news/paywalled domains, so primary-source
  verification currently leans on archived/mirror URLs.

## Iteration 5 — 2026-06-19T06:47:50+00:00

- Deterministic refresh: 23 predictions (achieved: 1, in_window: 18, partially: 1, pending: 3).
- Backlog: 0 to resolve, 0 deadlines within 180d, 0 to strengthen.


## Iteration 4 — 2026-06-18T06:37:18+00:00

- Deterministic refresh: 23 predictions (achieved: 1, in_window: 18, partially: 1, pending: 3).
- Backlog: 0 to resolve, 0 deadlines within 180d, 0 to strengthen.


## Iteration 3 — 2026-06-17T06:45:52+00:00

- Deterministic refresh: 23 predictions (achieved: 1, in_window: 18, partially: 1, pending: 3).
- Backlog: 0 to resolve, 0 deadlines within 180d, 0 to strengthen.


## Iteration 2 — 2026-06-16T22:40:56+00:00

- Deterministic refresh: 23 predictions (achieved: 1, in_window: 18, partially: 1, pending: 3).
- Backlog: 0 to resolve, 0 deadlines within 180d, 0 to strengthen.


## Iteration 1 — 2026-06-16T21:58:24+00:00

- Deterministic refresh: 22 predictions (achieved: 1, in_window: 17, partially: 1, pending: 3).
- Backlog: 0 to resolve, 0 deadlines within 180d, 0 to strengthen.

## Bootstrap — 2026-06-16

- Project created: `Mem/` (data), `Scripts/` (build + science), `Doc/` (paper + site).
- Seeded the prediction dataset (22 predictions) from primary sources: essays
  (*Machines of Loving Grace*, *The Urgency of Interpretability*, *The
  Adolescence of Technology*, *Policy on the AI Exponential*), podcasts (Lex
  Fridman #452, Dwarkesh), official Anthropic posts (OSTP submission, ASL-3
  activation, RSP v3.0), and reputable interview coverage (CFR, Axios, Davos,
  Code with Claude).
- Implemented the math/thesis tests (calibration, lead/lag, horizon-compression
  regression, realized-acceleration fit) and figure generation.
- Wired GitHub Pages export and the daily research loop in CI.
