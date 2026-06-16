# `Mem/` — the single source of truth

Everything the site and paper say is derived from files in this directory. Edit
data here; never hand-edit generated pages in `Doc/`.

## `predictions.yaml`

```yaml
meta:
  title: Dario Amodei Prediction Tracker
  maintained_by: <name/handle>
predictions:
  - id: powerful_ai_2026            # unique snake_case key
    theme: agi_timeline             # see THEMES below
    quote: "verbatim quote (<=240 chars)"
    speaker: Dario Amodei
    date_said: 2024-10-11           # ISO date the statement was made/published
    venue: "Machines of Loving Grace (essay)"
    primary_url: "https://..."      # primary or near-primary source
    archive_url: "https://web.archive.org/..."   # optional
    predicted_horizon_verbatim: "as early as 2026"
    predicted_date: 2026-12-31      # normalized resolve-by date; range -> END of range
    status: in_window               # see STATUSES below
    resolved_date: null             # ISO date achieved/missed; required if achieved
    confidence: high                # high | medium | low (sourcing/normalization confidence)
    tags: [agi, scaling]
    evidence:
      - url: "https://..."
        date: 2026-05-01
        note: "what this shows"
    notes: "normalization assumptions, caveats"
```

### THEMES
`agi_timeline`, `coding`, `science_bio_health`, `economy_jobs`, `safety_scaling`,
`anthropic_milestone`.

### STATUSES
| status | meaning |
|---|---|
| `pending` | predicted window has not opened yet |
| `in_window` | we are inside the predicted window; not yet resolved |
| `achieved` | the predicted thing has demonstrably happened (needs `resolved_date` + evidence) |
| `partially` | meaningfully but not fully realized (needs evidence) |
| `missed` | window elapsed without the thing happening |
| `unverifiable` | cannot be objectively scored |

For calibration scoring, resolved statuses get credit `achieved=1.0`,
`partially=0.5`, `missed=0.0`.

## `metrics.json` (generated)
Written by `Scripts/mathematics.py`. Consumed by `Scripts/build_paper.py`. Not
committed (rebuilt every run).

## `loop-state.json`
The recursive-improvement loop's state: iteration counter, last run, status
counts, and the current research agenda. Updated by `Scripts/research.py`.

## `CHANGELOG.md`
Human-readable, append-only log of each loop iteration.

## Editorial rules
1. **No source, no entry.** Every prediction needs a working `primary_url`.
2. **Quote verbatim.** Paraphrases go in `notes`, not `quote`.
3. **Normalize transparently.** Record how a verbal horizon became a date in `notes`.
4. **Score with evidence.** `achieved`/`partially` require at least one evidence link.
