# Changelog

Append-only log of the recursive-improvement loop. Newest entries are inserted
directly below the marker by `Scripts/research.py`.

<!-- LOOP-ENTRIES -->

## Iteration 5 — 2026-06-18T21:05:54+00:00

- Deterministic refresh: 24 predictions (achieved: 1, in_window: 19, partially: 1, pending: 3).
- Backlog: 0 to resolve, 0 deadlines within 180d, 0 to strengthen.
- **Research (NEW prediction +1 → 24):** Added `ai_industry_trillions_revenue_before_2030`
  — Amodei on the Feb 2026 Dwarkesh podcast: "It is hard for me to see that there
  won't be trillions of dollars in revenue before 2030," tied to a ~2028 'low
  hundreds of billions' milestone and his 10x/yr growth model ("off by a year ...
  you go bankrupt"). theme=economy_jobs, medium confidence; primary=Dwarkesh,
  corroborated by Fortune (2026-02-14) and DCD (2026-02-16).
- Reviewed but did NOT log (no new dated, scoreable prediction): Bloomberg *The
  Circuit with Emily Chang* (2026-06-17, OpenAI/Pentagon retrospective) and the
  Pentagon "supply-chain risk" dispute coverage (an event, not a forecast).


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
