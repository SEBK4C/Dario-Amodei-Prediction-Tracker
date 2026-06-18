# Changelog

Append-only log of the recursive-improvement loop. Newest entries are inserted
directly below the marker by `Scripts/research.py`.

<!-- LOOP-ENTRIES -->

## Iteration 5 — 2026-06-18T14:06:15+00:00

- Deterministic refresh: 23 predictions (achieved: 1, in_window: 17, partially: 2, pending: 3).
- Backlog: 0 to resolve, 0 deadlines within 180d, 0 to strengthen.
- **Research (agent):** Resolved `one_person_billion_dollar_company_2026`
  `in_window → partially` (resolved_date 2026-04-02). Medvi, an AI-operated
  GLP-1 telehealth company, hit $401M first-year revenue and is tracking ~$1.8B
  in 2026 — the closest real-world instantiation of Amodei's 2026 one-person-$1B
  prediction. Scored **partially** (not achieved): Medvi has two people (founder
  Matthew Gallagher + brother Elliot), the figure is revenue not valuation, and
  the milestone is contested (FDA warning, lawsuits). Added 3 reputable evidence
  links (PYMNTS/NYT, NewsNation, Techdirt). Lifts H1 credit-weighted hit-rate to
  0.75; adds a +273-day lead/lag data point.
- Surveyed recent statements (G7 US-led AI coalition call 2026-06-17; Bloomberg
  one-direct-report profile 2026-06-10/11) — no NEW dated, scoreable forecasts
  to log beyond the already-tracked *Policy on the AI Exponential* essay.


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
