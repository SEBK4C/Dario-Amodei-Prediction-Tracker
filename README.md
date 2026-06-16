# Dario Amodei Prediction Tracker

A **citation-grounded, continuously-updated timeline** of the public predictions
made by Dario Amodei (CEO of Anthropic) about AI and Anthropic — placed on a
timeline from when they were said to when they are predicted to come true, and
scored against observed outcomes as those dates arrive.

The output is a **static, scientific-paper-style site** (GitHub Pages) plus
downloadable **PDF / DOCX / HTML**, all regenerated from a single dataset so the
numbers are reproducible and falsifiable. Every tracked claim links to a
**primary source**.

> **The timeline is the point.** This project exists to show, with citations,
> whether the predicted *accelerating path* of AI capability, adoption, and
> software automation is actually showing up in observed events.

This is an independent community project — **not affiliated with or endorsed by
Anthropic or Dario Amodei**.

## The thesis (tested in code)

The repository states three hypotheses and tests each one in
[`Scripts/mathematics.py`](Scripts/mathematics.py):

- **H1 — Trajectory / calibration:** when his dated predictions resolve, the
  milestones arrive on or ahead of the stated deadline more often than behind.
- **H2 — Horizon compression:** across successive "powerful-AI-arrival"
  forecasts, the horizon (time from utterance to predicted date) shortens.
- **H3 — Realized acceleration:** the cumulative count of realized milestones
  grows super-linearly over time.

The current results (with honest "insufficient data" where N is small) are
written into the paper on every build. See the published site.

## Repository layout

The three top-level working directories are mandated by the project brief:

| Directory | Role |
|---|---|
| **`Mem/`** | **Memory / single source of truth.** `predictions.yaml` (the cited dataset), `SCHEMA.md`, generated `metrics.json`, `loop-state.json`, and the append-only `CHANGELOG.md`. |
| **`Scripts/`** | **Build + science.** `validate.py` (schema), `mathematics.py` (the thesis tests + figures), `build_paper.py` (generates the paper/site pages), `export_docs.py` (PDF/DOCX/HTML via pandoc), `research.py` (daily loop bookkeeping), `build_all.sh` (orchestrator). |
| **`Doc/`** | **The documents.** Static pages (`about.md`, `methodology.md`) plus the generated paper (`index.md`), `timeline.md`, `predictions.md`, figures, and document exports. |

```
Mem/predictions.yaml ──► Scripts/validate.py ──► Scripts/mathematics.py ──► Mem/metrics.json + Doc/figures/
                                                          │
                                                          ▼
                                        Scripts/build_paper.py ──► Doc/index.md, timeline.md, predictions.md
                                                          │
                                          ┌───────────────┴───────────────┐
                                          ▼                               ▼
                              Scripts/export_docs.py            mkdocs build  ──►  site/  ──►  GitHub Pages
                              (PDF / DOCX / HTML)
```

## Quickstart

```bash
pip install -r requirements.txt
bash Scripts/build_all.sh        # validate → math → paper → exports → site
mkdocs serve                     # preview at http://127.0.0.1:8000
```

`pandoc` (and a LaTeX engine for PDF) are optional locally — the export step
skips gracefully if they are missing. CI installs them.

## The self-improvement loop

The recursive `/research` loop has two halves:

1. **Deterministic** ([`Scripts/research.py`](Scripts/research.py), workflow
   [`research.yml`](.github/workflows/research.yml)) — runs daily with no API
   key: re-validates the data, recomputes a *research agenda* (which predictions
   need resolving, watching, or stronger sources), bumps the loop counter, and
   appends to the changelog.
2. **Claude-powered** (workflow [`research-claude.yml`](.github/workflows/research-claude.yml),
   **opt-in**) — runs Claude Code daily to act on the agenda: find new dated
   predictions, refresh statuses against fresh evidence, and open a pull request.

## Deploying to GitHub Pages

1. In the repo: **Settings → Pages → Build and deployment → Source = "GitHub Actions"**.
2. Push to the default branch (or run the **Build & deploy site** workflow
   manually). The site builds and deploys automatically.
3. **Daily export:** the scheduled `cron` in `pages.yml` re-exports the site
   each day. ⚠️ GitHub only runs scheduled workflows from the **default
   branch**, so merge these workflows to `main` for the cron to fire.

### Enabling the Claude-powered daily research (optional)

1. Add repository secret **`ANTHROPIC_API_KEY`**.
2. Add repository variable **`ENABLE_CLAUDE_RESEARCH = true`**.
3. Verify the `anthropics/claude-code-action` version/inputs against the
   [docs](https://docs.claude.com/en/docs/claude-code/github-actions).

## Contributing / corrections

Found a misattributed quote, a wrong date, a better primary source, or a status
that should change? Edit [`Mem/predictions.yaml`](Mem/predictions.yaml)
(see [`Mem/SCHEMA.md`](Mem/SCHEMA.md)) and open a PR. Never hand-edit the
generated files in `Doc/` — they are rebuilt from the data.

## License

See [LICENSE](LICENSE). Quotes are reproduced for analysis and commentary with
attribution to their primary sources.
