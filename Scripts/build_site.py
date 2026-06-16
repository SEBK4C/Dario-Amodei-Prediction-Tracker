#!/usr/bin/env python3
"""
build_site.py
=============
Generate the static GitHub Pages site into ./docs from the single source of
truth (Mem/predictions_db.json) and the thesis output (Mem/thesis_results.json).

The TIMELINE is the visual centrepiece, per project mandate: every prediction is
plotted on a horizontal time axis from when it was *made* to its *target date*,
colour-coded by status, so the accelerating cadence is immediately legible.

Pure standard library. Run AFTER thesis_acceleration.py.
Usage:  python3 Scripts/build_site.py
"""
from __future__ import annotations

import html
import json
from datetime import date, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "Mem" / "predictions_db.json"
THESIS = ROOT / "Mem" / "thesis_results.json"
DOCS = ROOT / "docs"

STATUS_COLOR = {
    "Pending": "#d29922",
    "Achieved": "#2ea043",
    "Partial": "#58a6ff",
    "Failed": "#f85149",
    "Walked Back": "#a371f7",
}


def _d(s: str) -> date:
    return datetime.strptime(s, "%Y-%m-%d").date()


def timeline_svg(preds: list[dict]) -> str:
    """Horizontal timeline: one lane per prediction, made-date -> target-date."""
    W = 960
    row_h, top, left, right = 46, 70, 230, 40
    H = top + row_h * len(preds) + 60
    pw = W - left - right

    all_dates = [_d(p["date_made"]) for p in preds] + [_d(p["target_date"]) for p in preds]
    dmin, dmax = min(all_dates).toordinal(), max(all_dates).toordinal()
    span = (dmax - dmin) or 1

    def x(o: int) -> float:
        return left + (o - dmin) / span * pw

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
        f'font-family="system-ui,Segoe UI,Arial,sans-serif" font-size="13">',
        f'<rect width="{W}" height="{H}" fill="#0d1117"/>',
    ]
    # year gridlines
    y0, y1 = min(all_dates).year, max(all_dates).year + 1
    for yr in range(y0, y1 + 1):
        gx = x(date(yr, 1, 1).toordinal())
        parts.append(f'<line x1="{gx:.1f}" y1="{top-18}" x2="{gx:.1f}" y2="{H-30}" stroke="#21262d"/>')
        parts.append(
            f'<text x="{gx:.1f}" y="{top-24}" fill="#8b949e" text-anchor="middle" font-size="12">{yr}</text>'
        )
    # "today" marker
    today = date.today()
    if dmin <= today.toordinal() <= dmax:
        tx = x(today.toordinal())
        parts.append(
            f'<line x1="{tx:.1f}" y1="{top-18}" x2="{tx:.1f}" y2="{H-30}" '
            f'stroke="#f78166" stroke-width="2" stroke-dasharray="4 4"/>'
        )
        parts.append(
            f'<text x="{tx:.1f}" y="{H-14}" fill="#f78166" text-anchor="middle" font-size="11">today</text>'
        )

    for i, p in enumerate(preds):
        cy = top + i * row_h + row_h / 2
        x1, x2 = x(_d(p["date_made"]).toordinal()), x(_d(p["target_date"]).toordinal())
        color = STATUS_COLOR.get(p["status"], "#8b949e")
        label = html.escape(f'{p["id"]}  {p["category"].split(" / ")[0]}')
        parts.append(
            f'<text x="{left-12}" y="{cy+4:.1f}" fill="#e6edf3" text-anchor="end" font-size="12">{label}</text>'
        )
        # made -> target bar
        parts.append(
            f'<line x1="{x1:.1f}" y1="{cy:.1f}" x2="{x2:.1f}" y2="{cy:.1f}" '
            f'stroke="{color}" stroke-width="3" opacity="0.55"/>'
        )
        parts.append(f'<circle cx="{x1:.1f}" cy="{cy:.1f}" r="5" fill="#58a6ff"/>')
        parts.append(
            f'<rect x="{x2-5:.1f}" y="{cy-5:.1f}" width="10" height="10" fill="{color}" '
            f'transform="rotate(45 {x2:.1f} {cy:.1f})"/>'
        )
    parts.append("</svg>")
    return "\n".join(parts)


def card(p: dict) -> str:
    s = p["source"]
    color = STATUS_COLOR.get(p["status"], "#8b949e")
    return f"""
    <article class="card" id="{p['id']}">
      <div class="card-head">
        <span class="id">{p['id']}</span>
        <span class="badge" style="background:{color}22;color:{color};border:1px solid {color}">{html.escape(p['status'])}</span>
      </div>
      <p class="cat">{html.escape(p['category'])}</p>
      <p class="pred">{html.escape(p['prediction'])}</p>
      <blockquote>&ldquo;{html.escape(p['quote'])}&rdquo;</blockquote>
      <p class="meta">Made <b>{p['date_made']}</b> &middot; target <b>{p['target_date']}</b></p>
      <p class="src">Source: <a href="{html.escape(s['url'])}" target="_blank" rel="noopener">{html.escape(s['title'])}</a> ({html.escape(s['type'])})</p>
      <p class="notes">{html.escape(p['notes'])}</p>
    </article>"""


def build() -> str:
    db = json.loads(DB.read_text())
    thesis = json.loads(THESIS.read_text()) if THESIS.exists() else {}
    preds = sorted(db["predictions"], key=lambda p: p["date_made"])
    meta = db["metadata"]

    tally = thesis.get("status_tally", {})
    tally_html = " ".join(
        f'<span class="pill" style="border-color:{STATUS_COLOR.get(k,"#8b949e")}">{html.escape(k)}: {v}</span>'
        for k, v in tally.items()
    )
    h1 = thesis.get("hypothesis_H1", {})
    fig = (ROOT / "Doc" / "figure_horizon.svg")
    fig_svg = fig.read_text() if fig.exists() else ""
    legend = " ".join(
        f'<span class="pill" style="border-color:{c}">{html.escape(k)}</span>'
        for k, c in STATUS_COLOR.items()
    )

    return f"""<!DOCTYPE html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(meta['title'])}</title>
<meta name="description" content="{html.escape(meta['description'])}">
<style>
  :root{{color-scheme:dark}}
  body{{margin:0;background:#010409;color:#e6edf3;font-family:system-ui,Segoe UI,Arial,sans-serif;line-height:1.55}}
  .wrap{{max-width:1000px;margin:0 auto;padding:24px}}
  header h1{{margin:0 0 6px;font-size:28px}}
  header p.sub{{color:#8b949e;margin:0 0 16px}}
  .pills{{display:flex;flex-wrap:wrap;gap:8px;margin:12px 0}}
  .pill{{font-size:12px;padding:3px 10px;border:1px solid #30363d;border-radius:999px;color:#e6edf3;background:#0d1117}}
  section{{background:#0d1117;border:1px solid #21262d;border-radius:12px;padding:18px;margin:18px 0}}
  section h2{{margin-top:0;font-size:20px}}
  svg{{max-width:100%;height:auto;display:block}}
  .verdict{{background:#161b22;border-left:3px solid #f78166;padding:10px 14px;border-radius:6px;color:#e6edf3}}
  .grid{{display:grid;gap:14px}}
  .card{{background:#0d1117;border:1px solid #21262d;border-radius:10px;padding:16px}}
  .card-head{{display:flex;justify-content:space-between;align-items:center}}
  .id{{font-weight:700;color:#58a6ff}}
  .badge{{font-size:12px;padding:2px 10px;border-radius:999px;font-weight:600}}
  .cat{{color:#8b949e;font-size:12px;text-transform:uppercase;letter-spacing:.04em;margin:8px 0 4px}}
  .pred{{font-weight:600;margin:4px 0}}
  blockquote{{margin:8px 0;padding:8px 12px;border-left:3px solid #30363d;color:#c9d1d9;font-style:italic}}
  .meta,.src,.notes{{font-size:13px;color:#8b949e;margin:6px 0}}
  a{{color:#58a6ff}}
  footer{{color:#6e7681;font-size:12px;text-align:center;padding:24px}}
</style></head>
<body><div class="wrap">
<header>
  <h1>{html.escape(meta['title'])}</h1>
  <p class="sub">{html.escape(meta['description'])}</p>
  <div class="pills">{tally_html}</div>
  <p class="sub">Last updated {meta['last_updated']} &middot; {len(preds)} tracked predictions &middot; every entry carries a hyperlinked primary source.</p>
</header>

<section>
  <h2>&#128336; Prediction Timeline <span style="font-size:13px;color:#8b949e">(the core view)</span></h2>
  <p class="sub">Circle = date the prediction was made; diamond = target date. Bar colour encodes status.</p>
  <div class="pills">{legend}</div>
  {timeline_svg(preds)}
</section>

<section>
  <h2>&#128202; Acceleration Thesis (H1)</h2>
  <p>{html.escape(h1.get('statement',''))}</p>
  <p class="verdict">{html.escape(h1.get('verdict',''))}</p>
  <p class="sub">Linear fit of prediction horizon on date-made: slope = <b>{h1.get('slope_years_per_year')}</b> yr/yr, R&sup2; = <b>{h1.get('r_squared')}</b>.</p>
  {fig_svg}
</section>

<section>
  <h2>&#128203; Tracked Predictions</h2>
  <div class="grid">
    {''.join(card(p) for p in preds)}
  </div>
</section>

<footer>
  Generated by Scripts/build_site.py &middot; data: Mem/predictions_db.json &middot;
  This tracker logs publicly reported statements with primary-source links; it is an independent analytical project and is not affiliated with Anthropic or Dario Amodei.
</footer>
</div></body></html>"""


def main() -> None:
    DOCS.mkdir(exist_ok=True)
    (DOCS / "index.html").write_text(build())
    (DOCS / ".nojekyll").write_text("")
    # publish the raw data alongside the site for transparency / reuse
    (DOCS / "predictions_db.json").write_text(DB.read_text())
    print(f"[site] wrote {DOCS/'index.html'} ({(DOCS/'index.html').stat().st_size} bytes)")


if __name__ == "__main__":
    main()
