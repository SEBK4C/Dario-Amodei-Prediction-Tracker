# Changelog

Append-only log of the recursive-improvement loop. Newest entries are inserted
directly below the marker by `Scripts/research.py`.

<!-- LOOP-ENTRIES -->

## Iteration 4 — 2026-06-17T08:07:57+00:00

- Deterministic refresh: 24 predictions (achieved: 1, in_window: 18, partially: 1, pending: 3, unverifiable: 1).
- Backlog: 0 to resolve, 0 deadlines within 180d, 0 to strengthen.
- **Research find (+1 record):** added `jevons_automation_expands_work_2026` —
  on 2026-05-05, onstage with JPMorgan CEO Jamie Dimon at Anthropic's "Briefing:
  Financial Services" (NYC), Amodei partly **walked back** his 2025 "~50% of
  entry-level white-collar jobs / 10–20% unemployment" warning, reframing
  automation as a Jevons-paradox productivity multiplier ("automate 90% of the
  job… the 10% expands… 10xs their productivity"). Cross-linked to the original
  `entry_level_white_collar_jobs` record; classified `unverifiable` (qualitative,
  no falsifiable horizon) so it does not distort calibration.
  Sources: Fortune 2026-05-05 & 2026-05-26, CNBC 2026-05-05.


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
