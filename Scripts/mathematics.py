#!/usr/bin/env python3
"""The "science": quantitative tests of the tracker's thesis.

This script turns the cited predictions in ``Mem/predictions.yaml`` into
falsifiable statistics and figures. It writes ``Mem/metrics.json`` (consumed by
the paper generator) and renders figures into ``Doc/figures/``.

Hypotheses under test
---------------------
H1 (Trajectory / calibration): When his dated predictions resolve, Dario
   Amodei's milestones arrive on or ahead of the stated deadline more often
   than behind -- consistent with an accelerating trajectory.

H2 (Horizon compression): Across successive predictions, the *horizon* (time
   from utterance to predicted resolution) shortens over calendar time -- i.e.
   he expects transformative AI sooner as time passes.

H3 (Realized acceleration): The cumulative count of resolved-true milestones
   grows super-linearly (better fit by an exponential than a line) over time.

Each hypothesis is operationalized below and scored against the data. With few
resolved data points some tests will honestly report "insufficient data" rather
than over-claim -- the loop is designed to strengthen them as evidence grows.
"""
from __future__ import annotations

import datetime as _dt
import json
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import dataio  # noqa: E402

import numpy as np  # noqa: E402

# Headless rendering for CI.
import matplotlib  # noqa: E402

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import matplotlib.dates as mdates  # noqa: E402

# Colour map shared by every figure so status reads consistently.
STATUS_COLORS = {
    "achieved": "#2e7d32",
    "partially": "#9e9d24",
    "in_window": "#1565c0",
    "pending": "#6a1b9a",
    "missed": "#c62828",
    "unverifiable": "#616161",
}
STATUS_ORDER = ["achieved", "partially", "in_window", "pending", "missed", "unverifiable"]


# --------------------------------------------------------------------------
# Small statistics helpers (kept dependency-light: numpy only)
# --------------------------------------------------------------------------
def ols(x: np.ndarray, y: np.ndarray) -> dict:
    """Ordinary least squares for y ~ a + b*x with goodness-of-fit stats."""
    n = len(x)
    if n < 2 or np.allclose(x, x[0]):
        return {"n": int(n), "slope": None, "intercept": None, "r": None,
                "r2": None, "t_stat": None, "sufficient": False}
    b, a = np.polyfit(x, y, 1)
    y_hat = a + b * x
    ss_res = float(np.sum((y - y_hat) ** 2))
    ss_tot = float(np.sum((y - np.mean(y)) ** 2))
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else None
    # Pearson r
    sx, sy = np.std(x), np.std(y)
    r = float(np.mean((x - x.mean()) * (y - y.mean())) / (sx * sy)) if sx > 0 and sy > 0 else None
    # two-sided t statistic for the slope (no scipy: report stat, not p)
    t_stat = None
    if r is not None and n > 2 and abs(r) < 1.0:
        t_stat = float(r * math.sqrt((n - 2) / (1 - r * r)))
    return {"n": int(n), "slope": float(b), "intercept": float(a), "r": r,
            "r2": r2, "t_stat": t_stat, "sufficient": True}


def year_frac(d: _dt.date) -> float:
    """Calendar date as a fractional year (for regressions/plots)."""
    start = _dt.date(d.year, 1, 1)
    end = _dt.date(d.year + 1, 1, 1)
    return d.year + (d - start).days / (end - start).days


def arrival_subset(preds: list[dataio.Prediction]) -> list[dataio.Prediction]:
    """The 'when does powerful AI arrive' forecasts used for H2.

    Horizon-compression is only meaningful across comparable forecasts, so we
    restrict it to predictions tagged ``powerful_ai_arrival`` (falling back to
    the ``agi_timeline`` theme). Mixing month-scale coding claims with
    decade-scale biology claims would measure theme composition, not horizons.
    """
    tagged = [p for p in preds if "powerful_ai_arrival" in p.tags]
    return tagged if tagged else [p for p in preds if p.theme == "agi_timeline"]


# --------------------------------------------------------------------------
# Metric computation
# --------------------------------------------------------------------------
def compute_metrics(preds: list[dataio.Prediction], today: _dt.date) -> dict:
    n = len(preds)
    by_status = {s: 0 for s in STATUS_ORDER}
    by_theme: dict[str, int] = {}
    for p in preds:
        by_status[p.status] = by_status.get(p.status, 0) + 1
        by_theme[p.theme] = by_theme.get(p.theme, 0) + 1

    resolved = [p for p in preds if p.is_resolved()]
    achieved = [p for p in preds if p.status == "achieved"]

    # H1 — calibration on predictions whose window has elapsed.
    elapsed = [p for p in preds if p.window_elapsed(today) and p.is_resolved()]
    credit = [dataio.STATUS_CREDIT[p.status] for p in elapsed]
    hit_rate = float(np.mean(credit)) if credit else None

    # Lead/lag (days early) for resolved-true predictions.
    leads = [p.lead_days() for p in resolved if p.lead_days() is not None]
    lead_stats = None
    if leads:
        arr = np.array(leads, dtype=float)
        lead_stats = {
            "n": int(len(arr)),
            "mean_days": float(arr.mean()),
            "median_days": float(np.median(arr)),
            "min_days": float(arr.min()),
            "max_days": float(arr.max()),
            "share_on_or_ahead": float(np.mean(arr >= 0)),
        }

    # H2 — horizon compression on the "powerful AI arrival" forecasts only.
    arrival = arrival_subset(preds)
    xs = np.array([year_frac(p.date_said) for p in arrival], dtype=float)
    ys = np.array([p.horizon_years for p in arrival], dtype=float)
    horizon_reg = ols(xs, ys)
    horizon_reg["subset"] = "powerful_ai_arrival"
    horizon_reg["n_subset"] = len(arrival)
    horizon_reg["interpretation"] = _interpret_horizon(horizon_reg)

    # H3 — realized acceleration: cumulative achieved vs time, linear vs exp.
    accel = _acceleration_fit(achieved)

    metrics = {
        "generated_at": _dt.datetime.now(_dt.timezone.utc).isoformat(timespec="seconds"),
        "as_of_date": today.isoformat(),
        "counts": {
            "total": n,
            "by_status": by_status,
            "by_theme": dict(sorted(by_theme.items())),
            "resolved": len(resolved),
            "achieved": len(achieved),
            "window_elapsed": sum(1 for p in preds if p.window_elapsed(today)),
            "with_archive": sum(1 for p in preds if p.archive_url),
            "high_confidence": sum(1 for p in preds if p.confidence == "high"),
        },
        "date_range": {
            "first_said": min((p.date_said for p in preds), default=None).isoformat()
            if preds else None,
            "last_said": max((p.date_said for p in preds), default=None).isoformat()
            if preds else None,
            "earliest_deadline": min((p.predicted_date for p in preds), default=None).isoformat()
            if preds else None,
            "latest_deadline": max((p.predicted_date for p in preds), default=None).isoformat()
            if preds else None,
        },
        "H1_calibration": {
            "elapsed_resolved_n": len(elapsed),
            "credit_weighted_hit_rate": hit_rate,
            "lead_lag": lead_stats,
        },
        "H2_horizon_compression": horizon_reg,
        "H3_realized_acceleration": accel,
    }
    return metrics


def _interpret_horizon(reg: dict) -> str:
    if not reg.get("sufficient"):
        return "insufficient data (need >= 2 predictions spanning different dates)"
    slope = reg["slope"]
    if slope is None:
        return "insufficient variance to estimate"
    direction = "shortening" if slope < 0 else "lengthening"
    return (f"stated horizon is {direction} by ~{abs(slope):.2f} years per calendar year "
            f"(r={reg['r']:.2f}, n={reg['n']})")


def _acceleration_fit(achieved: list[dataio.Prediction]) -> dict:
    pts = sorted([p for p in achieved if p.resolved_date], key=lambda p: p.resolved_date)
    if len(pts) < 3:
        return {"sufficient": False,
                "reason": f"need >= 3 resolved-true milestones, have {len(pts)}"}
    t0 = pts[0].resolved_date
    t = np.array([(p.resolved_date - t0).days / 365.25 for p in pts], dtype=float)
    c = np.arange(1, len(pts) + 1, dtype=float)  # cumulative count
    lin = ols(t, c)
    exp = ols(t, np.log(c))  # log-linear => exponential in original space
    doubling_years = None
    if exp.get("slope") and exp["slope"] > 0:
        doubling_years = math.log(2) / exp["slope"]
    better = None
    if lin.get("r2") is not None and exp.get("r2") is not None:
        better = "exponential" if exp["r2"] > lin["r2"] else "linear"
    return {
        "sufficient": True,
        "n": len(pts),
        "linear_r2": lin.get("r2"),
        "exponential_r2": exp.get("r2"),
        "better_fit": better,
        "doubling_time_years": doubling_years,
    }


# --------------------------------------------------------------------------
# Figures
# --------------------------------------------------------------------------
def _save(fig, name: str) -> None:
    dataio.FIG_DIR.mkdir(parents=True, exist_ok=True)
    for ext in ("png", "svg"):
        fig.savefig(dataio.FIG_DIR / f"{name}.{ext}", bbox_inches="tight", dpi=150)
    plt.close(fig)


def fig_timeline(preds: list[dataio.Prediction], today: _dt.date) -> None:
    preds = sorted(preds, key=lambda p: p.date_said)
    fig, ax = plt.subplots(figsize=(10, max(3, 0.55 * len(preds) + 1.5)))
    for i, p in enumerate(preds):
        color = STATUS_COLORS.get(p.status, "#000")
        ax.plot([p.date_said, p.predicted_date], [i, i], color=color, lw=2.4, alpha=0.85,
                solid_capstyle="round", zorder=2)
        ax.scatter([p.date_said], [i], color=color, s=28, zorder=3, marker="o")
        ax.scatter([p.predicted_date], [i], color=color, s=70, zorder=3, marker="|", linewidths=2.2)
        if p.resolved_date:
            mk = "*" if p.status == "achieved" else "x"
            kw = {"edgecolors": "black", "linewidths": 0.4} if mk == "*" else {}
            ax.scatter([p.resolved_date], [i], color=color, s=130, zorder=4, marker=mk, **kw)
        label = p.id.replace("_", " ")
        ax.text(p.date_said, i + 0.22, label[:42], fontsize=7.5, va="bottom")
    ax.axvline(today, color="#444", ls="--", lw=1.1, zorder=1)
    ax.text(today, len(preds) - 0.4, " today", fontsize=8, color="#444", rotation=90, va="top")
    ax.set_yticks([])
    ax.set_ylim(-0.8, len(preds) + 0.2)
    ax.set_title("Dario Amodei predictions: said → predicted deadline (○ said, | deadline, ★ achieved)")
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    ax.grid(axis="x", alpha=0.25)
    handles = [plt.Line2D([0], [0], color=STATUS_COLORS[s], lw=3, label=s)
               for s in STATUS_ORDER]
    ax.legend(handles=handles, loc="lower right", fontsize=7, ncol=2, framealpha=0.9)
    _save(fig, "timeline")


def fig_status(metrics: dict) -> None:
    counts = metrics["counts"]["by_status"]
    labels = [s for s in STATUS_ORDER if counts.get(s, 0) > 0]
    vals = [counts[s] for s in labels]
    fig, ax = plt.subplots(figsize=(7, 3.6))
    ax.bar(labels, vals, color=[STATUS_COLORS[s] for s in labels])
    for i, v in enumerate(vals):
        ax.text(i, v + 0.05, str(v), ha="center", fontsize=9)
    ax.set_ylabel("predictions")
    ax.set_title("Prediction status distribution")
    ax.margins(y=0.15)
    _save(fig, "status_breakdown")


def fig_horizon(preds: list[dataio.Prediction], reg: dict) -> None:
    if len(preds) < 2:
        return
    xs = np.array([year_frac(p.date_said) for p in preds])
    ys = np.array([p.horizon_years for p in preds])
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.scatter(xs, ys, c=[STATUS_COLORS.get(p.status, "#000") for p in preds], s=45, zorder=3)
    if reg.get("sufficient") and reg.get("slope") is not None:
        xr = np.linspace(xs.min(), xs.max(), 50)
        ax.plot(xr, reg["intercept"] + reg["slope"] * xr, color="#c62828", lw=1.8,
                label=f"OLS slope={reg['slope']:.2f} yr/yr, r={reg['r']:.2f}")
        ax.legend(fontsize=8)
    ax.set_xlabel("year prediction was made")
    ax.set_ylabel("stated horizon (years to deadline)")
    ax.set_title("H2: are stated horizons compressing over time?")
    ax.grid(alpha=0.25)
    _save(fig, "horizon_compression")


def fig_cumulative(preds: list[dataio.Prediction]) -> None:
    pts = sorted([p for p in preds if p.status == "achieved" and p.resolved_date],
                 key=lambda p: p.resolved_date)
    if not pts:
        return
    xs = [p.resolved_date for p in pts]
    ys = list(range(1, len(pts) + 1))
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.step(xs, ys, where="post", color=STATUS_COLORS["achieved"], lw=2)
    ax.scatter(xs, ys, color=STATUS_COLORS["achieved"], s=40, zorder=3)
    ax.set_ylabel("cumulative achieved milestones")
    ax.set_title("H3: realized milestones over time")
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
    fig.autofmt_xdate()
    ax.grid(alpha=0.25)
    _save(fig, "cumulative_achievements")


def main() -> int:
    today = _dt.date.today()
    env_today = os.environ.get("DA_TODAY")
    if env_today:
        today = _dt.date.fromisoformat(env_today)

    preds = dataio.load_predictions()
    problems = dataio.validate(preds)
    if problems:
        print("Refusing to compute metrics on invalid data:", file=sys.stderr)
        for p in problems:
            print(f"  - {p}", file=sys.stderr)
        return 1

    metrics = compute_metrics(preds, today)
    dataio.METRICS_FILE.write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    print(f"Wrote {dataio.METRICS_FILE.relative_to(dataio.REPO_ROOT)}")

    fig_timeline(preds, today)
    fig_status(metrics)
    fig_horizon(arrival_subset(preds), metrics["H2_horizon_compression"])
    fig_cumulative(preds)
    print(f"Wrote figures to {dataio.FIG_DIR.relative_to(dataio.REPO_ROOT)}/")

    c = metrics["counts"]
    print(f"\nSummary: {c['total']} predictions | "
          f"{c['achieved']} achieved, {c['by_status'].get('in_window', 0)} in-window, "
          f"{c['by_status'].get('pending', 0)} pending, {c['by_status'].get('missed', 0)} missed")
    print(f"H2 horizon: {metrics['H2_horizon_compression']['interpretation']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
