# Changelog

Append-only log of the recursive-improvement loop. Newest entries are inserted
directly below the marker by `Scripts/research.py`.

<!-- LOOP-ENTRIES -->

## Iteration 3 — 2026-06-17T02:07:26+00:00

- Deterministic refresh: 24 predictions (achieved: 1, in_window: 18, partially: 1, pending: 4).
- Backlog: 0 to resolve, 0 deadlines within 180d, 0 to strengthen.
- Research sweep (2026-06-17): searched recent Dario Amodei / Anthropic statements.
  No brand-new dated capability/timeline forecast in the last 24h; the most recent
  essay ("Policy on the AI Exponential", 2026-06-10) was already captured. EXPAND:
  added one distinct, previously-missing prediction from that essay — AI in-silico
  simulation replacing slow/expensive clinical experiments
  (`ai_simulation_replaces_clinical_experiments`, science_bio_health, pending).
- Non-prediction context noted (not logged as forecasts): Anthropic reported ~$47B
  ARR by May 2026; Amodei announced a $200M AI-impact research investment and gave
  an ABC News interview backing pre-deployment testing/certification.
- Environment note: all primary/secondary fetches returned HTTP 403 (darioamodei.com,
  archive.org, reader proxies), so verbatim quotes could not be re-verified against
  primaries this run. Verbatim verification of the new entry is deferred to the next
  run with working fetch access.


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
