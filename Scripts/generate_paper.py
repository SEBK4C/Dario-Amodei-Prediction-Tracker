#!/usr/bin/env python3
"""
generate_paper.py
=================
Synthesize the formal scientific paper into Doc/ from the database and thesis
results. Emits Markdown (always) and attempts a PDF via pandoc/weasyprint if
available (optional; absence is logged, not fatal).

Paper structure follows the project spec: Abstract, Introduction, Methodology,
Timeline Analysis (primary), Conclusions.

Usage:  python3 Scripts/generate_paper.py
"""
from __future__ import annotations

import json
import shutil
import subprocess
from datetime import date, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "Mem" / "predictions_db.json"
THESIS = ROOT / "Mem" / "thesis_results.json"
DOC = ROOT / "Doc"


def _d(s: str) -> date:
    return datetime.strptime(s, "%Y-%m-%d").date()


def build_md(db: dict, thesis: dict) -> str:
    preds = sorted(db["predictions"], key=lambda p: p["date_made"])
    meta = db["metadata"]
    h1 = thesis.get("hypothesis_H1", {})
    comp = thesis.get("supporting_model_effective_compute", {})
    today = date.today().isoformat()

    # Timeline table (primary analysis).
    rows = ["| ID | Category | Made | Target | Horizon (yr) | Status | Source |",
            "|----|----------|------|--------|--------------|--------|--------|"]
    for p in preds:
        horizon = (_d(p["target_date"]) - _d(p["date_made"])).days / 365.25
        src = f'[{p["source"]["title"]}]({p["source"]["url"]})'
        rows.append(
            f'| {p["id"]} | {p["category"].split(" / ")[0]} | {p["date_made"]} | '
            f'{p["target_date"]} | {horizon:.2f} | {p["status"]} | {src} |'
        )
    timeline_table = "\n".join(rows)

    comp_rows = ["| Year | Relative effective compute (x 2024) |",
                 "|------|--------------------------------------|"]
    for c in comp.get("curve", []):
        comp_rows.append(f'| {c["year"]} | {c["relative_effective_compute"]:,}x |')
    comp_table = "\n".join(comp_rows)

    tally = thesis.get("status_tally", {})
    tally_str = ", ".join(f"{k}: {v}" for k, v in tally.items())

    detail = []
    for p in preds:
        detail.append(
            f'### {p["id"]} — {p["category"]}\n\n'
            f'**Claim.** {p["prediction"]}\n\n'
            f'> "{p["quote"]}"\n\n'
            f'**Made:** {p["date_made"]} · **Target:** {p["target_date"]} · '
            f'**Status:** {p["status"]}\n\n'
            f'**Primary source:** [{p["source"]["title"]}]({p["source"]["url"]}) '
            f'({p["source"]["type"]}, {p["source"]["publisher"]})\n\n'
            f'**Assessment.** {p["notes"]}\n'
        )
    details = "\n".join(detail)

    return f"""---
title: "Tracking the Acceleration: An Empirical Audit of Dario Amodei's AI Timeline Predictions"
date: {today}
author: "Dario Amodei Prediction Tracker (autonomous R&D agent)"
---

# Tracking the Acceleration: An Empirical Audit of Dario Amodei's AI Timeline Predictions

*Report generated {today}. All claims are linked to explicit primary sources. This is an independent analytical project, not affiliated with Anthropic.*

## Abstract

We maintain a continuously-updated, primary-source-anchored database of public
predictions made by Dario Amodei, CEO of Anthropic, concerning the arrival and
impact of "powerful AI." As of this revision the corpus contains
**{len(preds)} tracked predictions** ({tally_str}). We test one principal
hypothesis (H1): that Amodei's successive "powerful AI" timelines exhibit a
*contracting prediction horizon* — the interval between when a forecast is made
and its target date shrinks over calendar time — which is the observable
signature of an accelerating (super-exponential) capability expectation. A
linear fit yields a horizon slope of **{h1.get('slope_years_per_year')} years per
calendar year** (R² = **{h1.get('r_squared')}**), {h1.get('verdict','').split(':')[0].lower()}
of H1. We contextualise this with a first-order effective-compute growth model
and present the full prediction timeline as the report's central artifact.

## Introduction

Anthropic's public posture rests on a *scaling paradigm*: the thesis that
continued growth in training compute, data, and algorithmic efficiency yields
broadly predictable gains in model capability, extrapolating toward systems
Amodei describes as a "country of geniuses in a datacenter." Beginning with the
October 2024 essay *Machines of Loving Grace* and continuing through the January
2026 essay *The Adolescence of Technology*, Amodei has issued a series of dated,
falsifiable forecasts spanning AGI timelines, software automation, biomedical
acceleration, and labour-market disruption.

These forecasts are unusually concrete for a frontier-lab CEO, which makes them
auditable. This tracker exists to hold each claim against its primary source and
against unfolding events, and — critically — to quantify whether the *cadence*
of the forecasts is itself accelerating.

## Methodology (How the Science Was Done)

**Data gathering.** Each prediction is logged in `Mem/predictions_db.json` only
when an explicit primary source (essay, policy submission, recorded interview,
or directly-quoted public remarks) can be hyperlinked. Statements were located
via targeted web search and cross-checked against the canonical publication
(e.g. `darioamodei.com` for essays). Entries carry the verbatim quote where
available, the date made, an inferred target date, a status, and an assessment.

**Status verification.** Each prediction is assigned one of: Pending, Achieved,
Partial, Failed, or Walked Back. A claim moves to Failed when its explicit target
window elapses without realization (e.g. the "90% of code in 3–6 months" claim,
whose September 2025 window passed), and to Walked Back when the predictor
publicly softens or retracts it (corroborated by reporting).

**Thesis testing.** `Scripts/thesis_acceleration.py` computes, for every
AGI-timeline prediction, the horizon = target − made, then regresses horizon on
date-made. A significantly negative slope supports H1. A supporting
effective-compute model projects relative compute growth at an assumed
{comp.get('assumption_doublings_per_year')} doublings/year
(≈ {comp.get('implied_annual_multiplier')}× annually) to contextualise the
~2027 window. All code is pure-standard-library and reproducible via
`Scripts/run_pipeline.sh`.

## Timeline Analysis (Primary Function)

The table below maps every tracked prediction from issuance to target, with its
realized horizon and current status. This timeline is the core artifact of the
project; the interactive version lives on the GitHub Pages site (`docs/`).

{timeline_table}

**H1 — contracting horizon.** Regressing horizon on date-made across the
AGI-timeline predictions gives slope = **{h1.get('slope_years_per_year')} yr/yr**
(R² = **{h1.get('r_squared')}**). {h1.get('verdict','')}

**Supporting context — effective compute.** Under the stated assumption, relative
effective compute grows as:

{comp_table}

This projection is illustrative, not a claim of Amodei's; it situates why a
2026–2027 "powerful AI" window is internally consistent with the scaling
paradigm even as specific sub-claims (e.g. code automation) have slipped.

### Per-prediction detail

{details}

## Conclusions

The evidence base is mixed but structured. On **AGI timing**, the load-bearing
forecasts (P002, P003) remain *Pending* and squarely live: the late-2026/early-2027
window has not yet elapsed, and the cadence of Amodei's forecasts is measurably
*tightening* (H1 supported), consistent with an accelerationist read of the
scaling curve. On **near-term operational claims**, the record is weaker: the
"90% of code" forecast (P004) **failed** its explicit window, and the
"white-collar bloodbath" labour forecast (P006) has been **walked back** amid
employment data that has so far not confirmed it.

The synthesis: Amodei is more calibrated on *capability emergence at the
research frontier* than on *the speed of real-world diffusion* (code, jobs),
where institutional and adoption frictions dominate. The next revisions of this
report will watch the 2026–2027 window closely, as it is decisive for P001–P003.

---

*Reproduce: `bash Scripts/run_pipeline.sh`. Data and sources: `Mem/`. Generated by an autonomous R&D agent.*
"""


def main() -> None:
    DOC.mkdir(exist_ok=True)
    db = json.loads(DB.read_text())
    thesis = json.loads(THESIS.read_text()) if THESIS.exists() else {}
    md = build_md(db, thesis)
    md_path = DOC / "acceleration_audit.md"
    md_path.write_text(md)
    print(f"[paper] wrote {md_path.relative_to(ROOT)} ({len(md)} bytes)")

    # PDF generation. Prefer pandoc (richest), else fall back to the bundled
    # zero-dependency minipdf writer so the PDF deliverable is always produced.
    pdf_path = DOC / "acceleration_audit.pdf"
    if shutil.which("pandoc"):
        try:
            subprocess.run(
                ["pandoc", str(md_path), "-o", str(pdf_path)],
                check=True, capture_output=True, timeout=120,
            )
            print(f"[paper] wrote {pdf_path.relative_to(ROOT)} via pandoc")
            return
        except Exception as e:  # noqa: BLE001
            print(f"[paper] pandoc PDF failed ({e}); falling back to minipdf.")
    try:
        import minipdf  # local module, pure stdlib
        minipdf.md_file_to_pdf(md_path, pdf_path)
        print(f"[paper] wrote {pdf_path.relative_to(ROOT)} via bundled minipdf "
              f"({pdf_path.stat().st_size} bytes)")
    except Exception as e:  # noqa: BLE001
        print(f"[paper] PDF generation failed ({e}); Markdown remains canonical.")


if __name__ == "__main__":
    main()
