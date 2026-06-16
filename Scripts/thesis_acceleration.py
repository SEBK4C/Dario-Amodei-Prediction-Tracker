#!/usr/bin/env python3
"""
thesis_acceleration.py
======================
Thesis-testing harness for the Dario Amodei Prediction Tracker.

THESIS (H1): Amodei's successive public timelines for "powerful AI" imply a
*shrinking prediction horizon* -- i.e., as calendar time advances, the gap
between the date a forecast is made and its target date contracts. A shrinking
horizon is the observable signature of a forecaster pricing in super-exponential
("accelerating") capability growth driven by compounding effective-compute gains.

We test H1 directly against the logged predictions and, as a supporting model,
fit a simple effective-compute growth curve to contextualise the timelines.

Pure standard library (no third-party deps) so it runs in any cron environment.
Outputs:
  - Mem/thesis_results.json   (machine-readable results, consumed by site build)
  - Doc/figure_horizon.svg    (prediction-horizon scatter, self-contained SVG)

Usage:  python3 Scripts/thesis_acceleration.py
"""
from __future__ import annotations

import json
import math
from datetime import date, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "Mem" / "predictions_db.json"
RESULTS = ROOT / "Mem" / "thesis_results.json"
FIGURE = ROOT / "Doc" / "figure_horizon.svg"

# AGI-timeline predictions are the ones whose horizon we track for acceleration.
TIMELINE_CATEGORY = "Powerful AI / AGI Timeline"


def _parse(d: str) -> date:
    return datetime.strptime(d, "%Y-%m-%d").date()


def load_db() -> dict:
    with DB.open() as fh:
        return json.load(fh)


def horizon_analysis(predictions: list[dict]) -> dict:
    """For each timeline prediction, horizon = target_date - date_made (years)."""
    rows = []
    for p in predictions:
        if p["category"] != TIMELINE_CATEGORY:
            continue
        made = _parse(p["date_made"])
        target = _parse(p["target_date"])
        horizon_yrs = (target - made).days / 365.25
        rows.append(
            {
                "id": p["id"],
                "date_made": p["date_made"],
                "target_date": p["target_date"],
                "made_ordinal": made.toordinal(),
                "horizon_years": round(horizon_yrs, 3),
            }
        )
    rows.sort(key=lambda r: r["made_ordinal"])

    # Linear regression of horizon (y) on date-made (x, in years from first).
    slope = intercept = r2 = None
    if len(rows) >= 2:
        x0 = rows[0]["made_ordinal"]
        xs = [(r["made_ordinal"] - x0) / 365.25 for r in rows]
        ys = [r["horizon_years"] for r in rows]
        n = len(xs)
        mx, my = sum(xs) / n, sum(ys) / n
        sxx = sum((x - mx) ** 2 for x in xs)
        sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
        if sxx > 0:
            slope = sxy / sxx
            intercept = my - slope * mx
            ss_tot = sum((y - my) ** 2 for y in ys)
            ss_res = sum((y - (intercept + slope * x)) ** 2 for x, y in zip(xs, ys))
            r2 = 1 - ss_res / ss_tot if ss_tot > 0 else 1.0

    return {
        "rows": rows,
        "slope_years_per_year": round(slope, 4) if slope is not None else None,
        "intercept_years": round(intercept, 4) if intercept is not None else None,
        "r_squared": round(r2, 4) if r2 is not None else None,
        "verdict": _verdict(slope),
    }


def _verdict(slope):
    if slope is None:
        return "Insufficient data (need >= 2 timeline predictions)."
    if slope < -0.05:
        return (
            "SUPPORTED: prediction horizon is contracting over time "
            f"({slope:+.2f} yr of horizon per calendar yr), the signature of an "
            "accelerating (super-exponential) capability expectation."
        )
    if slope > 0.05:
        return (
            "NOT SUPPORTED: prediction horizon is expanding over time "
            f"({slope:+.2f} yr/yr); forecasts are being pushed further out."
        )
    return "INCONCLUSIVE: horizon is roughly stable over time."


def effective_compute_model(
    doublings_per_year: float = 2.5, years: int = 6, start_year: int = 2024
) -> dict:
    """
    Supporting context model. Industry estimates put the growth of *effective
    training compute* (raw FLOP x algorithmic efficiency) at roughly 4-5x/year,
    i.e. ~2.0-2.5 doublings/year. We project the relative effective-compute
    multiplier from the start year to contextualise a ~2027 'powerful AI' window.
    """
    curve = []
    for i in range(years + 1):
        yr = start_year + i
        multiplier = 2 ** (doublings_per_year * i)
        curve.append({"year": yr, "relative_effective_compute": round(multiplier, 1)})
    return {
        "assumption_doublings_per_year": doublings_per_year,
        "implied_annual_multiplier": round(2 ** doublings_per_year, 2),
        "curve": curve,
    }


def render_svg(rows: list[dict], reg: dict) -> str:
    """Self-contained SVG scatter of prediction horizon vs. date made."""
    W, H = 720, 420
    ml, mr, mt, mb = 70, 30, 40, 60
    pw, ph = W - ml - mr, H - mt - mb
    if not rows:
        return f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}"></svg>'

    xs = [r["made_ordinal"] for r in rows]
    ys = [r["horizon_years"] for r in rows]
    xmin, xmax = min(xs), max(xs)
    ymin, ymax = 0, max(ys) * 1.15 + 0.1
    xspan = (xmax - xmin) or 1

    def px(o):
        return ml + (o - xmin) / xspan * pw

    def py(v):
        return mt + (1 - (v - ymin) / (ymax - ymin)) * ph

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
        f'font-family="system-ui,Arial,sans-serif" font-size="13">',
        f'<rect width="{W}" height="{H}" fill="#0d1117"/>',
        f'<text x="{W/2}" y="22" fill="#e6edf3" font-size="16" font-weight="700" '
        f'text-anchor="middle">Prediction Horizon vs. Date Made (AGI timeline)</text>',
    ]
    # axes
    parts.append(
        f'<line x1="{ml}" y1="{mt}" x2="{ml}" y2="{mt+ph}" stroke="#30363d"/>'
        f'<line x1="{ml}" y1="{mt+ph}" x2="{ml+pw}" y2="{mt+ph}" stroke="#30363d"/>'
    )
    # y gridlines/labels
    for k in range(0, int(ymax) + 1):
        y = py(k)
        parts.append(f'<line x1="{ml}" y1="{y:.1f}" x2="{ml+pw}" y2="{y:.1f}" stroke="#161b22"/>')
        parts.append(f'<text x="{ml-8}" y="{y+4:.1f}" fill="#8b949e" text-anchor="end">{k}</text>')
    parts.append(
        f'<text x="20" y="{mt+ph/2}" fill="#8b949e" text-anchor="middle" '
        f'transform="rotate(-90 20 {mt+ph/2})">Horizon (years)</text>'
    )
    # regression line
    if reg.get("slope_years_per_year") is not None:
        x0 = rows[0]["made_ordinal"]
        s = reg["slope_years_per_year"]
        b = reg["intercept_years"]
        y_at = lambda o: b + s * ((o - x0) / 365.25)
        parts.append(
            f'<line x1="{px(xmin):.1f}" y1="{py(y_at(xmin)):.1f}" '
            f'x2="{px(xmax):.1f}" y2="{py(y_at(xmax)):.1f}" '
            f'stroke="#f78166" stroke-width="2" stroke-dasharray="6 4"/>'
        )
    # points + date labels
    for r in rows:
        cx, cy = px(r["made_ordinal"]), py(r["horizon_years"])
        parts.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="6" fill="#58a6ff"/>')
        parts.append(
            f'<text x="{cx:.1f}" y="{cy-12:.1f}" fill="#e6edf3" text-anchor="middle" '
            f'font-size="11">{r["id"]}</text>'
        )
        parts.append(
            f'<text x="{cx:.1f}" y="{mt+ph+18:.1f}" fill="#8b949e" text-anchor="middle" '
            f'font-size="10">{r["date_made"]}</text>'
        )
    parts.append(
        f'<text x="{ml+pw}" y="{H-12}" fill="#8b949e" text-anchor="end" font-size="11">'
        f'slope = {reg.get("slope_years_per_year")} yr/yr  (R^2 = {reg.get("r_squared")})</text>'
    )
    parts.append("</svg>")
    return "\n".join(parts)


def main() -> None:
    db = load_db()
    preds = db["predictions"]
    reg = horizon_analysis(preds)
    compute = effective_compute_model()

    # Status tally across all predictions.
    tally: dict[str, int] = {}
    for p in preds:
        tally[p["status"]] = tally.get(p["status"], 0) + 1

    results = {
        "generated": date.today().isoformat(),
        "n_predictions": len(preds),
        "status_tally": tally,
        "hypothesis_H1": {
            "statement": "Successive 'powerful AI' timelines imply a shrinking prediction horizon (accelerating expectation).",
            **reg,
        },
        "supporting_model_effective_compute": compute,
    }
    RESULTS.write_text(json.dumps(results, indent=2))
    FIGURE.write_text(render_svg(reg["rows"], reg))

    print(f"[thesis] {len(preds)} predictions | status {tally}")
    print(f"[thesis] H1 slope = {reg['slope_years_per_year']} yr/yr, R^2 = {reg['r_squared']}")
    print(f"[thesis] {reg['verdict']}")
    print(f"[thesis] wrote {RESULTS.relative_to(ROOT)} and {FIGURE.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
