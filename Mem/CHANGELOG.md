# Changelog

Append-only log of the recursive-improvement loop. Newest entries are inserted
directly below the marker by `Scripts/research.py`.

<!-- LOOP-ENTRIES -->

## Iteration 6 — 2026-06-19T17:06:06+00:00

- Deterministic refresh: 23 predictions (achieved: 1, in_window: 18, partially: 1, pending: 3).
- Backlog: 0 to resolve, 0 deadlines within 180d, 0 to strengthen.
- **Research (web):** strengthened two records with newly-found dated sources.
  - `entry_level_white_collar_jobs`: documented the May 2026 *walk-back* —
    Amodei reframed automation as a productivity multiplier rather than mass
    unemployment (Fortune 2026-05-26), corroborated by the Yale Budget Lab
    finding no measurable labor dislocation ~1yr into the window. Resolves the
    standing "to be tracked" note; status kept `in_window` (deadline 2030) but
    flagged as trending toward `missed`/`partially` on the 10-20% reading.
  - `ai_90pct_code_3to6_months`: added Amodei's 2026-01-13 declaration that the
    90% threshold is "already true at Anthropic," plus an independent 12-month
    "claim chowder" (Daring Fireball 2026-03-13) showing the industry-wide
    "essentially all code" reading did not materialize. Confirms `partially`.
  - No clean NEW dated forecast found since last research (recent June 2026
    appearances — ABC7 regulation interview 06-11, India summit remarks 06-18 —
    were advocacy/commentary, not dated capability predictions).


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
