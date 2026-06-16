#!/usr/bin/env python3
"""Generate the scientific-paper Markdown pages from data + metrics.

Reads ``Mem/predictions.yaml`` and ``Mem/metrics.json`` and writes the
data-driven site pages into ``Doc/``:

* ``index.md``        -- the paper (abstract / intro / methods / results / conclusions)
* ``timeline.md``     -- the timeline table, the tracker's primary artifact
* ``predictions.md``  -- the full cited catalogue with evidence
* ``changelog.md``    -- mirror of Mem/CHANGELOG.md for the site

Run ``Scripts/mathematics.py`` first so ``metrics.json`` and the figures exist.
"""
from __future__ import annotations

import datetime as _dt
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import dataio  # noqa: E402

STATUS_BADGE = {
    "achieved": "✅ achieved",
    "partially": "🟡 partially",
    "in_window": "🔵 in window",
    "pending": "🟣 pending",
    "missed": "🔴 missed",
    "unverifiable": "⚪ unverifiable",
}


def _fmt(n, nd=1, pct=False, suffix=""):
    if n is None:
        return "n/a"
    if pct:
        return f"{100 * n:.{nd}f}%"
    return f"{n:.{nd}f}{suffix}"


def _load_metrics() -> dict:
    if dataio.METRICS_FILE.exists():
        return json.loads(dataio.METRICS_FILE.read_text(encoding="utf-8"))
    return {}


def _references(preds: list[dataio.Prediction]) -> tuple[str, dict[str, int]]:
    """Build a numbered reference list keyed by primary_url."""
    order: list[tuple[str, dataio.Prediction]] = []
    seen: dict[str, int] = {}
    for p in sorted(preds, key=lambda p: p.date_said):
        if p.primary_url not in seen:
            seen[p.primary_url] = len(order) + 1
            order.append((p.primary_url, p))
    lines = []
    for url, p in order:
        n = seen[url]
        archive = f" ([archived]({p.archive_url}))" if p.archive_url else ""
        lines.append(f"{n}. {p.speaker}, *{p.venue}*, {p.date_said.isoformat()}. "
                     f"<{url}>{archive}")
    return "\n".join(lines), seen


def build_index(preds, metrics, meta) -> str:
    c = metrics.get("counts", {})
    h1 = metrics.get("H1_calibration", {})
    h2 = metrics.get("H2_horizon_compression", {})
    h3 = metrics.get("H3_realized_acceleration", {})
    ll = (h1 or {}).get("lead_lag") or {}
    refs, refmap = _references(preds)
    today = metrics.get("as_of_date", _dt.date.today().isoformat())

    n = c.get("total", 0)
    by_status = c.get("by_status", {})
    hit = h1.get("credit_weighted_hit_rate")

    # Prose that adapts to however much evidence currently exists.
    accel_line = (
        f"the cumulative count of realized milestones is best fit by an "
        f"**{h3.get('better_fit')}** model"
        + (f" (doubling time ≈ {_fmt(h3.get('doubling_time_years'))} years)"
           if h3.get("doubling_time_years") else "")
        if h3.get("sufficient") else
        f"there are not yet enough resolved-true milestones to fit a growth curve "
        f"({h3.get('reason', 'insufficient data')})"
    )

    md = f"""---
title: "{meta.get('title', 'Dario Amodei Prediction Tracker')}"
description: "A citation-grounded, continuously-updated timeline of Dario Amodei's public predictions about AI and Anthropic, scored against observed outcomes."
---

# {meta.get('title', 'Dario Amodei Prediction Tracker')}

*A living scientific report — automatically rebuilt from a cited dataset.*
**As of {today}.** {n} tracked predictions · primary sources only · [view the timeline](timeline.md) · [full catalogue](predictions.md)

## Abstract

Dario Amodei, CEO of Anthropic, makes frequent, specific, and dated public
predictions about the trajectory of artificial intelligence — when "powerful
AI" arrives, how quickly software, science, and the labor market will change,
and how capability scaling will proceed. This report assembles those statements
into a single, citation-grounded dataset and places each on a timeline from the
date it was said to the date it is predicted to come true. We then test, in
code, whether the corpus describes an *accelerating* path and whether resolved
milestones land on or ahead of schedule. Across **{n}** tracked predictions
(**{by_status.get('achieved', 0)}** achieved, **{by_status.get('partially', 0)}**
partially, **{by_status.get('in_window', 0)}** currently in their predicted
window, **{by_status.get('pending', 0)}** pending, **{by_status.get('missed', 0)}**
missed), the credit-weighted hit-rate among predictions whose window has elapsed
is **{_fmt(hit, pct=True) if hit is not None else 'n/a'}**, and {accel_line}. The
dataset, code, and this document are regenerated automatically; every claim
links back to a primary source. This page is the machine-written summary — the
**[timeline](timeline.md)** is the primary artifact.

## 1. Introduction

Public AI discourse is saturated with bold timelines, but those claims are
rarely tracked. When a leader says transformative capability is "two years
away," is that borne out? Amodei is an unusually concrete forecaster: his essay
*Machines of Loving Grace* and his interviews give datable horizons for coding
automation, scientific progress, the labor market, and the arrival of what he
calls *powerful AI*. That concreteness makes his forecasts testable.

This project treats those forecasts as a falsifiable dataset. Our goals are:

1. **Provenance.** Every tracked prediction links to a primary source — the
   essay, the official talk, or a reputable outlet quoting him directly.
2. **Timeline.** Each prediction is placed on a line from *date said* to
   *predicted deadline*, and marked when (and whether) it was realized.
3. **Measurement.** We compute calibration, lead/lag, and acceleration
   statistics, and test three hypotheses about the trajectory.
4. **Self-improvement.** A scheduled research loop adds new statements, updates
   statuses against fresh evidence, and rebuilds this report.

### Hypotheses

* **H1 — Trajectory / calibration.** When his dated predictions resolve, the
  milestones arrive on or ahead of the stated deadline more often than behind.
* **H2 — Horizon compression.** Across successive predictions, the *horizon*
  (time from utterance to predicted resolution) shortens over calendar time.
* **H3 — Realized acceleration.** The cumulative count of realized milestones
  grows super-linearly over time.

## 2. Data and Methods

**Dataset.** The source of truth is [`Mem/predictions.yaml`](https://github.com/sebk4c/dario-amodei-prediction-tracker/blob/main/Mem/predictions.yaml).
Each record carries the verbatim quote, speaker, the date it was said, the
venue, a primary-source URL (plus an archive link where available), the
verbatim predicted horizon, a normalized `predicted_date` (range ends are
normalized to the end of the range), a `status`, optional `resolved_date`, and
the evidence used to score it. Records are schema-validated on every build by
[`Scripts/validate.py`](https://github.com/sebk4c/dario-amodei-prediction-tracker/blob/main/Scripts/validate.py).

**Status vocabulary.** `pending` (window not yet open), `in_window` (inside the
predicted window, unresolved), `achieved`, `partially`, `missed`, and
`unverifiable`. For calibration, resolved statuses receive credit
`achieved = 1.0`, `partially = 0.5`, `missed = 0.0`.

**Statistics.** All metrics are computed by
[`Scripts/mathematics.py`](https://github.com/sebk4c/dario-amodei-prediction-tracker/blob/main/Scripts/mathematics.py)
using ordinary least squares (numpy). For each resolved-true prediction we
compute *lead days* = `predicted_date − resolved_date` (positive = ahead of
schedule). H2 regresses stated horizon (years) on the year the statement was
made, **restricted to the "powerful-AI-arrival" forecasts** so the comparison is
like-for-like. H3 compares a linear and a log-linear (exponential) fit to the cumulative
count of achieved milestones, reporting R² for each and a doubling time when the
exponential dominates. Where data are too sparse for a stable fit, the script
reports *insufficient data* rather than over-claiming.

**Reproducibility.** `python Scripts/build_all.sh` regenerates every number and
figure in this document from the dataset. Builds are deterministic given the
dataset and the current date.

## 3. Results

### 3.1 The timeline

The primary artifact of this project is the timeline. The full, sortable
version lives on the **[Timeline page](timeline.md)**; the figure below shows
each prediction as a line from when it was said (○) to its predicted deadline
(|), with ★ marking realized milestones.

![Prediction timeline](figures/timeline.png)

### 3.2 Status distribution

Of **{n}** tracked predictions, the current breakdown is:
{_status_table(by_status)}

![Status distribution](figures/status_breakdown.png)

### 3.3 H1 — calibration and lead/lag

Among the **{h1.get('elapsed_resolved_n', 0)}** prediction(s) whose window has
already elapsed and that are scoreable, the credit-weighted hit-rate is
**{_fmt(hit, pct=True) if hit is not None else 'n/a'}**.
{_lead_lag_prose(ll)}

### 3.4 H2 — horizon compression

Restricting to the **{h2.get('n_subset', '?')}** "powerful-AI-arrival" forecasts
(so we compare like with like) and regressing each one's stated horizon (in
years) on the calendar year it was made yields: {h2.get('interpretation', 'insufficient data')}.
A negative slope is evidence for H2 (he expects powerful AI *sooner* as time
passes). {('**Slope ' + _fmt(h2.get('slope'), 2, suffix=' yr/yr') + '**, R² = ' + _fmt(h2.get('r2'), 2) + '.') if h2.get('sufficient') else ''}

![Horizon compression](figures/horizon_compression.png)

### 3.5 H3 — realized acceleration

For realized milestones, {accel_line}.
{('Linear R² = ' + _fmt(h3.get('linear_r2'), 2) + ', exponential R² = ' + _fmt(h3.get('exponential_r2'), 2) + '.') if h3.get('sufficient') else ''}

![Cumulative achievements](figures/cumulative_achievements.png)

## 4. Discussion

These statistics are deliberately conservative. Normalizing verbal horizons
("a few years", "as early as 2026") into single dates introduces judgment,
recorded per-record in the `notes` field and the `confidence` rating. Scoring a
qualitative claim ("AI writes most code") as achieved/partial is itself a
judgment backed by cited evidence. The corpus is also **survivorship-prone**:
memorable, bold predictions are easier to find than quiet, hedged ones. We
mitigate this by requiring a primary source for inclusion and by tracking
`missed` and `in_window` items rather than only successes.

The headline tension in the data is between **vision claims** (decade-scale
biology and economic transformation) and **near-term operational claims**
(coding automation within months). The latter resolve quickly and dominate the
calibration statistics today; the former dominate the long tail of the timeline
and will determine whether the "accelerating path" thesis ultimately holds.

## 5. Conclusions

1. The corpus of {n} cited predictions is concrete enough to score, and most
   near-term claims have either resolved or entered their predicted window.
2. On currently-resolvable predictions, the credit-weighted hit-rate is
   {_fmt(hit, pct=True) if hit is not None else 'n/a'}; {('lead/lag analysis indicates milestones have arrived ' + ('ahead of' if (ll.get('median_days') or 0) >= 0 else 'behind') + ' schedule on balance' ) if ll else 'lead/lag analysis awaits more resolved milestones'}.
3. The acceleration thesis (H3) {('is currently best supported by an ' + str(h3.get('better_fit')) + ' fit') if h3.get('sufficient') else 'cannot yet be confirmed or refuted with the available resolved milestones'}.

This document is regenerated on every data change and on a daily schedule. As
the research loop adds statements and resolves open windows, these conclusions
will update — and, being code-driven, they remain falsifiable.

## References

{refs}

---
<small>Generated by <code>Scripts/build_paper.py</code> on {metrics.get('generated_at', '')}.
Single source of truth: <code>Mem/predictions.yaml</code>. This is a community
research project and is not affiliated with or endorsed by Anthropic or Dario Amodei.</small>
"""
    return md


def _status_table(by_status: dict) -> str:
    rows = ["| status | count |", "|---|---|"]
    for s, badge in STATUS_BADGE.items():
        if by_status.get(s, 0):
            rows.append(f"| {badge} | {by_status[s]} |")
    return "\n".join(rows)


def _lead_lag_prose(ll: dict) -> str:
    if not ll:
        return ("No resolved-true predictions yet carry both a deadline and a "
                "resolution date, so lead/lag cannot be computed.")
    return (f"Across **{ll['n']}** resolved-true prediction(s), the median lead "
            f"is **{_fmt(ll['median_days'], 0)} days** "
            f"({'ahead of' if ll['median_days'] >= 0 else 'behind'} schedule); "
            f"**{_fmt(ll['share_on_or_ahead'], pct=True)}** arrived on or ahead of "
            f"the predicted deadline (range {_fmt(ll['min_days'],0)} to "
            f"{_fmt(ll['max_days'],0)} days).")


def build_timeline(preds, metrics) -> str:
    rows = ["| # | Prediction | Theme | Said | Predicted by | Status | Resolved | Source |",
            "|---|---|---|---|---|---|---|---|"]
    for i, p in enumerate(sorted(preds, key=lambda p: p.predicted_date), 1):
        resolved = p.resolved_date.isoformat() if p.resolved_date else "—"
        short = (p.quote[:80] + "…") if len(p.quote) > 80 else p.quote
        rows.append(
            f"| {i} | {short} | {p.theme} | {p.date_said.isoformat()} | "
            f"{p.predicted_date.isoformat()} | {STATUS_BADGE.get(p.status, p.status)} | "
            f"{resolved} | [link]({p.primary_url}) |"
        )
    table = "\n".join(rows)
    today = metrics.get("as_of_date", "")
    return f"""# Timeline

The primary artifact of this tracker: every cited Dario Amodei prediction
ordered by the date it is predicted to come true, with current status. **As of
{today}.**

![Prediction timeline](figures/timeline.png)

{table}

> Status legend: ✅ achieved · 🟡 partially · 🔵 in window · 🟣 pending · 🔴 missed · ⚪ unverifiable.
> Full quotes, evidence, and citations are on the [Predictions catalogue](predictions.md).
"""


def build_catalogue(preds) -> str:
    out = ["# Prediction catalogue",
           "",
           "Every tracked prediction with its verbatim quote, primary source, "
           "normalization notes, and the evidence used to score its status. "
           "This is the human-readable view of "
           "[`Mem/predictions.yaml`](https://github.com/sebk4c/dario-amodei-prediction-tracker/blob/main/Mem/predictions.yaml).",
           ""]
    for p in sorted(preds, key=lambda p: p.date_said):
        out.append(f"## {p.id.replace('_', ' ').title()}  ·  {STATUS_BADGE.get(p.status, p.status)}")
        out.append("")
        out.append(f"> \"{p.quote}\"")
        out.append("")
        out.append(f"- **Speaker / venue:** {p.speaker} — *{p.venue}*")
        out.append(f"- **Said:** {p.date_said.isoformat()}  ·  **Theme:** {p.theme}  ·  **Confidence:** {p.confidence}")
        out.append(f"- **Predicted horizon:** {p.predicted_horizon_verbatim or '—'} "
                   f"→ normalized **{p.predicted_date.isoformat()}**")
        if p.resolved_date:
            out.append(f"- **Resolved:** {p.resolved_date.isoformat()} "
                       f"(lead {p.lead_days()} days)")
        src = f"[primary source]({p.primary_url})"
        if p.archive_url:
            src += f" · [archived]({p.archive_url})"
        out.append(f"- **Source:** {src}")
        if p.evidence:
            out.append("- **Evidence:**")
            for e in p.evidence:
                if isinstance(e, dict):
                    url = e.get("url", "")
                    note = e.get("note", "")
                    date = e.get("date", "")
                    out.append(f"    - [{date}]({url}) — {note}" if url else f"    - {note}")
                else:
                    out.append(f"    - {e}")
        if p.notes:
            out.append(f"- **Notes:** {p.notes}")
        out.append("")
    return "\n".join(out)


def main() -> int:
    preds = dataio.load_predictions()
    meta = dataio.load_meta()
    metrics = _load_metrics()
    if not metrics:
        print("WARNING: Mem/metrics.json missing — run Scripts/mathematics.py first.",
              file=sys.stderr)

    (dataio.DOC_DIR / "index.md").write_text(build_index(preds, metrics, meta), encoding="utf-8")
    (dataio.DOC_DIR / "timeline.md").write_text(build_timeline(preds, metrics), encoding="utf-8")
    (dataio.DOC_DIR / "predictions.md").write_text(build_catalogue(preds), encoding="utf-8")

    changelog = dataio.MEM_DIR / "CHANGELOG.md"
    if changelog.exists():
        (dataio.DOC_DIR / "changelog.md").write_text(changelog.read_text(encoding="utf-8"),
                                                      encoding="utf-8")
    print("Wrote Doc/index.md, Doc/timeline.md, Doc/predictions.md, Doc/changelog.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
