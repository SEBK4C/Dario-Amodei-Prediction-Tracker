"""Shared data access + schema for the Dario Amodei Prediction Tracker.

This module is the single authority for the on-disk schema of
``Mem/predictions.yaml`` (the single source of truth). Every other script
loads predictions through :func:`load_predictions` so validation rules live in
exactly one place.
"""
from __future__ import annotations

import dataclasses
import datetime as _dt
import pathlib
from typing import Any, Iterable

import yaml

# --------------------------------------------------------------------------
# Paths
# --------------------------------------------------------------------------
REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
MEM_DIR = REPO_ROOT / "Mem"
DOC_DIR = REPO_ROOT / "Doc"
FIG_DIR = DOC_DIR / "figures"
PREDICTIONS_FILE = MEM_DIR / "predictions.yaml"
METRICS_FILE = MEM_DIR / "metrics.json"
LOOP_STATE_FILE = MEM_DIR / "loop-state.json"

# --------------------------------------------------------------------------
# Controlled vocabularies
# --------------------------------------------------------------------------
# Status of a prediction relative to its predicted resolution date.
STATUSES = {
    "achieved",    # the predicted thing has demonstrably happened
    "partially",   # meaningfully but not fully realized
    "in_window",   # we are inside the predicted window; not yet resolved
    "pending",     # predicted window has not opened yet
    "missed",      # predicted window elapsed without the thing happening
    "unverifiable",  # cannot be objectively checked
}

# A status counts as "resolved" once we can score it true/false-ish.
RESOLVED_STATUSES = {"achieved", "partially", "missed"}

# Numeric credit assigned to each resolved status for calibration scoring.
STATUS_CREDIT = {"achieved": 1.0, "partially": 0.5, "missed": 0.0}

THEMES = {
    "agi_timeline",
    "coding",
    "science_bio_health",
    "economy_jobs",
    "safety_scaling",
    "anthropic_milestone",
}

CONFIDENCE = {"high", "medium", "low"}

REQUIRED_FIELDS = (
    "id",
    "theme",
    "quote",
    "speaker",
    "date_said",
    "venue",
    "primary_url",
    "predicted_date",
    "status",
    "confidence",
)


@dataclasses.dataclass
class Prediction:
    """One cited, dated prediction and its current public status."""

    id: str
    theme: str
    quote: str
    speaker: str
    date_said: _dt.date
    venue: str
    primary_url: str
    predicted_date: _dt.date
    status: str
    confidence: str
    predicted_horizon_verbatim: str = ""
    archive_url: str = ""
    resolved_date: _dt.date | None = None
    evidence: list[dict[str, Any]] = dataclasses.field(default_factory=list)
    tags: list[str] = dataclasses.field(default_factory=list)
    notes: str = ""

    # -- derived helpers -------------------------------------------------
    @property
    def horizon_days(self) -> int:
        """Days from when it was said to its predicted resolution date."""
        return (self.predicted_date - self.date_said).days

    @property
    def horizon_years(self) -> float:
        return self.horizon_days / 365.25

    def lead_days(self) -> int | None:
        """Signed slack for resolved predictions: + = arrived early.

        ``predicted_date - resolved_date``. Positive means the milestone was
        reached before the predicted deadline (ahead of schedule).
        """
        if self.resolved_date is None:
            return None
        return (self.predicted_date - self.resolved_date).days

    def is_resolved(self) -> bool:
        return self.status in RESOLVED_STATUSES

    def window_elapsed(self, today: _dt.date) -> bool:
        return self.predicted_date <= today


def _as_date(value: Any, field: str, pid: str) -> _dt.date:
    if isinstance(value, _dt.datetime):
        return value.date()
    if isinstance(value, _dt.date):
        return value
    if isinstance(value, str):
        try:
            return _dt.date.fromisoformat(value.strip())
        except ValueError as exc:  # pragma: no cover - surfaced via validate
            raise ValueError(
                f"prediction '{pid}': field '{field}' is not an ISO date: {value!r}"
            ) from exc
    raise ValueError(
        f"prediction '{pid}': field '{field}' must be a YYYY-MM-DD date, got {value!r}"
    )


def _coerce(raw: dict[str, Any]) -> Prediction:
    pid = str(raw.get("id", "<missing id>"))
    missing = [f for f in REQUIRED_FIELDS if raw.get(f) in (None, "")]
    if missing:
        raise ValueError(f"prediction '{pid}': missing required field(s): {', '.join(missing)}")

    resolved_raw = raw.get("resolved_date")
    resolved = _as_date(resolved_raw, "resolved_date", pid) if resolved_raw else None

    return Prediction(
        id=pid,
        theme=str(raw["theme"]),
        quote=str(raw["quote"]).strip(),
        speaker=str(raw["speaker"]),
        date_said=_as_date(raw["date_said"], "date_said", pid),
        venue=str(raw["venue"]),
        primary_url=str(raw["primary_url"]),
        predicted_date=_as_date(raw["predicted_date"], "predicted_date", pid),
        status=str(raw["status"]),
        confidence=str(raw["confidence"]),
        predicted_horizon_verbatim=str(raw.get("predicted_horizon_verbatim", "")),
        archive_url=str(raw.get("archive_url", "") or ""),
        resolved_date=resolved,
        evidence=list(raw.get("evidence", []) or []),
        tags=list(raw.get("tags", []) or []),
        notes=str(raw.get("notes", "") or ""),
    )


def load_raw(path: pathlib.Path | None = None) -> dict[str, Any]:
    path = path or PREDICTIONS_FILE
    with open(path, "r", encoding="utf-8") as fh:
        data = yaml.safe_load(fh)
    if not isinstance(data, dict) or "predictions" not in data:
        raise ValueError(f"{path} must be a mapping with a top-level 'predictions' list")
    return data


def load_predictions(path: pathlib.Path | None = None) -> list[Prediction]:
    """Load + coerce all predictions, sorted by the date they were said."""
    data = load_raw(path)
    preds = [_coerce(item) for item in data["predictions"]]
    preds.sort(key=lambda p: p.date_said)
    return preds


def load_meta(path: pathlib.Path | None = None) -> dict[str, Any]:
    return load_raw(path).get("meta", {})


def validate(preds: Iterable[Prediction]) -> list[str]:
    """Return a list of human-readable problems (empty list == valid)."""
    problems: list[str] = []
    seen_ids: set[str] = set()
    for p in preds:
        if p.id in seen_ids:
            problems.append(f"duplicate id: {p.id}")
        seen_ids.add(p.id)
        if p.theme not in THEMES:
            problems.append(f"{p.id}: unknown theme '{p.theme}' (allowed: {sorted(THEMES)})")
        if p.status not in STATUSES:
            problems.append(f"{p.id}: unknown status '{p.status}' (allowed: {sorted(STATUSES)})")
        if p.confidence not in CONFIDENCE:
            problems.append(f"{p.id}: unknown confidence '{p.confidence}'")
        if not p.primary_url.startswith(("http://", "https://")):
            problems.append(f"{p.id}: primary_url should be an http(s) URL")
        if p.predicted_date < p.date_said:
            problems.append(f"{p.id}: predicted_date precedes date_said")
        if p.status == "achieved" and p.resolved_date is None:
            problems.append(f"{p.id}: status 'achieved' requires a resolved_date")
        if p.status in {"achieved", "partially"} and not p.evidence:
            problems.append(f"{p.id}: status '{p.status}' should cite at least one evidence link")
    return problems
