#!/usr/bin/env python3
"""Daily self-improvement bookkeeping for the prediction tracker loop.

This is the deterministic half of the recursive-improvement loop — it runs in
CI every day with no API key required. It:

* re-validates the dataset,
* computes a *review backlog* (predictions whose window is opening, elapsed, or
  resolving soon and therefore need fresh evidence),
* updates ``Mem/loop-state.json`` (iteration counter, timestamps, backlog),
* appends a dated entry to ``Mem/CHANGELOG.md``,
* prints a RESEARCH AGENDA that the Claude-powered ``/research`` step consumes
  to go find new statements and update statuses.

Run with ``--agenda-only`` to just print the agenda (used by the research
workflow to brief the model) without mutating state.
"""
from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import dataio  # noqa: E402

SOON_DAYS = 180


def build_agenda(preds, today):
    elapsed_unresolved, opening_soon, low_conf = [], [], []
    for p in preds:
        if p.status == "in_window" and p.window_elapsed(today):
            elapsed_unresolved.append(p)
        if p.status == "pending" and 0 <= (p.predicted_date - today).days <= SOON_DAYS:
            opening_soon.append(p)
        if p.status == "in_window" and 0 <= (p.predicted_date - today).days <= SOON_DAYS:
            opening_soon.append(p)
        if p.confidence == "low":
            low_conf.append(p)
    return {
        "resolve_now": [p.id for p in elapsed_unresolved],
        "deadline_within_180d": sorted({p.id for p in opening_soon}),
        "low_confidence_needs_better_source": [p.id for p in low_conf],
    }


def print_agenda(preds, today):
    agenda = build_agenda(preds, today)
    print("=" * 64)
    print(f"RESEARCH AGENDA  (as of {today.isoformat()}, {len(preds)} predictions)")
    print("=" * 64)
    print("\n1. RESOLVE — windows elapsed but still 'in_window' (need a verdict):")
    print("   " + (", ".join(agenda["resolve_now"]) or "(none)"))
    print("\n2. WATCH — deadlines within 180 days (refresh evidence):")
    print("   " + (", ".join(agenda["deadline_within_180d"]) or "(none)"))
    print("\n3. STRENGTHEN — low-confidence records needing a better primary source:")
    print("   " + (", ".join(agenda["low_confidence_needs_better_source"]) or "(none)"))
    print("\n4. EXPAND — search for NEW dated Dario Amodei / Anthropic predictions")
    print("   since the last run and add them to Mem/predictions.yaml with citations.")
    print("=" * 64)
    return agenda


def update_state(preds, today, agenda):
    state = {}
    if dataio.LOOP_STATE_FILE.exists():
        try:
            state = json.loads(dataio.LOOP_STATE_FILE.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            state = {}
    iteration = int(state.get("iteration", 0)) + 1
    now = _dt.datetime.now(_dt.timezone.utc).isoformat(timespec="seconds")
    new_state = {
        "iteration": iteration,
        "last_run_utc": now,
        "as_of_date": today.isoformat(),
        "prediction_count": len(preds),
        "status_counts": _status_counts(preds),
        "agenda": agenda,
        "history": (state.get("history", []) + [{"iteration": iteration, "at": now,
                                                  "count": len(preds)}])[-50:],
    }
    dataio.LOOP_STATE_FILE.write_text(json.dumps(new_state, indent=2), encoding="utf-8")
    return new_state


def _status_counts(preds):
    out = {}
    for p in preds:
        out[p.status] = out.get(p.status, 0) + 1
    return out


MARKER = "<!-- LOOP-ENTRIES -->"


def append_changelog(state):
    path = dataio.MEM_DIR / "CHANGELOG.md"
    text = path.read_text(encoding="utf-8") if path.exists() else f"# Changelog\n\n{MARKER}\n"
    counts = ", ".join(f"{k}: {v}" for k, v in sorted(state["status_counts"].items()))
    entry = (f"\n## Iteration {state['iteration']} — {state['last_run_utc']}\n\n"
             f"- Deterministic refresh: {state['prediction_count']} predictions ({counts}).\n"
             f"- Backlog: {len(state['agenda']['resolve_now'])} to resolve, "
             f"{len(state['agenda']['deadline_within_180d'])} deadlines within 180d, "
             f"{len(state['agenda']['low_confidence_needs_better_source'])} to strengthen.\n")
    # Newest entry goes directly below the marker (newest-first).
    if MARKER in text:
        text = text.replace(MARKER, MARKER + "\n" + entry, 1)
    else:
        text = text.rstrip() + "\n" + entry
    path.write_text(text, encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--agenda-only", action="store_true",
                    help="print the research agenda without mutating loop state")
    args = ap.parse_args()

    today = _dt.date.today()
    env_today = os.environ.get("DA_TODAY")
    if env_today:
        today = _dt.date.fromisoformat(env_today)

    preds = dataio.load_predictions()
    problems = dataio.validate(preds)
    if problems:
        print("Dataset invalid; fix before running the loop:", file=sys.stderr)
        for p in problems:
            print(f"  - {p}", file=sys.stderr)
        return 1

    agenda = print_agenda(preds, today)
    if args.agenda_only:
        return 0
    state = update_state(preds, today, agenda)
    append_changelog(state)
    print(f"\nLoop iteration {state['iteration']} recorded → Mem/loop-state.json + CHANGELOG.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
