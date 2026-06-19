# Changelog

Append-only log of the recursive-improvement loop. Newest entries are inserted
directly below the marker by `Scripts/research.py`.

<!-- LOOP-ENTRIES -->

## Iteration 5 — 2026-06-19T04:06:17+00:00

- Deterministic refresh: 25 predictions (achieved: 1, in_window: 20, partially: 1, pending: 3).
- Backlog: 0 to resolve, 0 deadlines within 180d, 2 to strengthen.
- RESEARCH (EXPAND): +2 dated predictions from the Feb 13 2026 Dwarkesh
  podcast ("end of the exponential"), both resolving by end of 2026 and
  feeding the compute/economics thesis:
  - `anthropic_revenue_10x_levels_off_2026` — revenue ~10x/yr ($100M→$1B→~$10B)
    "starts to level off sometime in 2026".
  - `anthropic_profitable_2026` — Anthropic "could be profitable in 2026 if the
    revenue grows fast enough" (conditional).
  Both logged at LOW confidence: quotes reconstructed from consistent secondary
  coverage (Zvi, MindStudio, AlphaTarget); the primary dwarkesh.com audio was
  not fetchable in this environment, so they enter the STRENGTHEN backlog for
  verbatim verification against the transcript on the next run.


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
