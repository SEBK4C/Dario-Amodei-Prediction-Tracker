# Dario Amodei Prediction Tracker

A single source of truth that tracks **Dario Amodei's** (CEO, Anthropic) public
predictions about powerful AI, validates them against primary sources and
unfolding events, and quantifies whether the *cadence* of his forecasts is
itself accelerating.

> Independent analytical project. Not affiliated with Anthropic or Dario Amodei.
> Every logged prediction carries an explicit, hyperlinked primary source.

## What it shows

- **Timeline (core view):** every prediction plotted from the date it was *made*
  to its *target date*, colour-coded by status.
- **Acceleration thesis (H1):** Amodei's successive "powerful AI" timelines show
  a **contracting prediction horizon** (slope ≈ −0.20 yr/yr, R² ≈ 0.97) — the
  signature of an accelerating capability expectation.
- **Status ledger:** Pending / Achieved / Partial / Failed / Walked Back, each
  with the verbatim quote, source, and an assessment.

## Repository layout

```
Mem/      data backend — single source of truth
  predictions_db.json   the tracked predictions (edit this; everything else derives from it)
  sources.md            primary-source registry + verification TODOs
  thesis_results.json   machine-readable thesis output (generated)
  loop_log.md           append-only log of each research loop
Scripts/  automation
  thesis_acceleration.py  tests H1; emits thesis_results.json + Doc/figure_horizon.svg
  generate_paper.py       renders the scientific paper (Markdown + PDF)
  build_site.py           builds the GitHub Pages site into docs/
  minipdf.py              zero-dependency PDF writer (fallback when pandoc absent)
  run_pipeline.sh         runs all three stages in order
Doc/      generated scientific papers (Markdown + PDF) and figures
docs/     generated static site for GitHub Pages
```

## Reproduce locally

```bash
bash Scripts/run_pipeline.sh      # thesis -> paper -> site
open docs/index.html              # view the site
```

Pure Python standard library — no third-party dependencies required.

## Deployment

`.github/workflows/deploy.yml` rebuilds the pipeline and publishes `docs/` to
GitHub Pages on every push to the working branch and on a daily cron (06:00 UTC).
To enable: repo **Settings → Pages → Source: GitHub Actions**.

## Adding / updating a prediction

1. Add an entry to `Mem/predictions_db.json` **with a hyperlinked primary source**
   (this is a hard constraint — no source, no entry).
2. Record the source in `Mem/sources.md`.
3. Run `bash Scripts/run_pipeline.sh` to regenerate the paper and site.
4. Append a note to `Mem/loop_log.md`.

## Methodology

See the generated paper, [`Doc/acceleration_audit.md`](Doc/acceleration_audit.md),
for the full methodology, the per-prediction assessment, and the effective-compute
context model.
