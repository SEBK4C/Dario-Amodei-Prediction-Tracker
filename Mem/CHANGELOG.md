# Changelog

Append-only log of the recursive-improvement loop. Newest entries are inserted
directly below the marker by `Scripts/research.py`.

<!-- LOOP-ENTRIES -->

## Iteration 5 — 2026-06-19T00:05:24+00:00

- Deterministic refresh: 24 predictions (achieved: 1, in_window: 19, partially: 1, pending: 3).
- Backlog: 0 to resolve, 0 deadlines within 180d, 0 to strengthen.
- **EXPAND (new record):** Added `jevons_paradox_jobs_revision_2026`. In a
  May 5 2026 Anthropic briefing on AI in financial services (alongside JPMorgan's
  Jamie Dimon), Amodei materially *revised* his flagship May-2025 labor-market
  forecast ("~50% of entry-level white-collar jobs / 20% unemployment"). Instead
  of net job collapse he now invokes the **Jevons paradox**: "If you automate 90%
  of the job, then everyone does the 10% of the job, and the 10% expands to be
  100% of what people do and 10xs their productivity." Corroborated by Fortune
  (May 5 + May 26), Technology Magazine, and Yahoo Finance. Linked to the original
  record so calibration can track the thesis as it actually evolved — the first
  documented self-revision of a flagship prediction in this dataset.
- Notable but not logged (no new *dated* forecast): Nikhil Kamath "People by WTF"
  interview (Feb 24 2026) and the June 2026 "Policy on the AI Exponential" essay —
  both restate existing timelines already in the dataset.


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
