# Changelog

Append-only log of the recursive-improvement loop. Newest entries are inserted
directly below the marker by `Scripts/research.py`.

<!-- LOOP-ENTRIES -->

## Iteration 5 — 2026-06-18T18:06:42+00:00

- Deterministic refresh: 24 predictions (achieved: 1, in_window: 19, partially: 1, pending: 3).
- Backlog: 0 to resolve, 0 deadlines within 180d, 0 to strengthen.
- **EXPAND (+1 prediction):** Added `dwarkesh_90pct_country_of_geniuses_10yr` —
  Amodei's "I'm at 90% on that" / within-ten-years statement (Dwarkesh, 2026-02-13).
  The dataset previously captured only the aggressive near-term "hunch" from that
  same episode; this adds his high-confidence OUTER bound (→ 2036-02-13).
  Tagged `calibration_anchor` and deliberately excluded from the H2
  horizon-compression subset (it is a distribution tail, not a central estimate),
  so the H2 slope is unchanged (shortening ~0.15 yr/yr, r=-0.13, n=8).
- **Methodological note:** the tracker now distinguishes *central/earliest* arrival
  estimates (which compress over time) from *confidence bounds* (the stable
  90%/10-year tail) — the two move differently and should not share one regression.
- **Context, not logged as predictions** (no dated capability forecast): G7 summit
  (Évian, 2026-06-17) — Amodei urged leaders to "resist the temptation to splinter"
  on AI; and the Anthropic–Pentagon standoff — Trump administration ordered agencies
  to stop using Anthropic models and Defense Sec. Hegseth designated the firm a
  "supply chain risk"; Amodei called it "retaliatory and punitive" and reaffirmed
  Anthropic's two red lines (no mass surveillance of Americans; no autonomous weapons).


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
