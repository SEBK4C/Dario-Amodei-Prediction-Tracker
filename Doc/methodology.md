# Methodology

This page documents how the tracker is built and how each statistic is computed.
It is the detailed companion to the Methods section of [the paper](index.md). The
whole pipeline is reproducible: `bash Scripts/build_all.sh` regenerates every
number and figure from the dataset.

## 1. The dataset

The single source of truth is
[`Mem/predictions.yaml`](https://github.com/sebk4c/dario-amodei-prediction-tracker/blob/main/Mem/predictions.yaml).
The schema is specified in
[`Mem/SCHEMA.md`](https://github.com/sebk4c/dario-amodei-prediction-tracker/blob/main/Mem/SCHEMA.md)
and enforced on every build by `Scripts/validate.py`. Each record stores the
verbatim quote, speaker, the date it was said, the venue, a primary-source URL
(plus an archive link where available), the verbatim predicted horizon, a
normalized `predicted_date`, a `status`, an optional `resolved_date`, a
`confidence` rating, and the `evidence` used to score it.

### Inclusion criteria

1. **Primary source required.** A record is only included if it links to a
   primary or near-primary source (the essay, the official talk/podcast, an
   official Anthropic post, or a reputable outlet quoting Amodei directly).
2. **Verbatim quotes.** The `quote` field is verbatim; paraphrase and context
   go in `notes`. Where a quote condenses adjacent sentences, that is flagged.
3. **Datable.** The statement must carry an explicit or reconstructable horizon.

### Confidence ratings

`high` / `medium` / `low` reflect the strength of *sourcing and normalization*,
not how likely the prediction is to come true. A snippet-sourced 2026 quote
whose primary page was unreachable at research time is marked `medium` until the
primary is directly verified.

## 2. Normalizing horizons into dates

Predictions are often verbal ("a few years", "as early as 2026", "1–2 years").
We normalize each to a single `predicted_date` so it can be placed on a timeline
and scored:

- **Ranges → the END of the range.** "2026 or 2027" → `2027-12-31`. This is the
  conservative choice (gives the prediction the most time to resolve).
- **"As early as Y"** → end of year Y.
- **Conditional horizons** (e.g. biology claims that begin "5–10 years *after*
  powerful AI") are normalized assuming the optimistic powerful-AI date he
  himself gives (~2026), then adding the stated offset.

Every normalization assumption is recorded in the record's `notes`. Because this
introduces judgment, the [Discussion](index.md#4-discussion) treats the results
as sensitive to it.

## 3. Status vocabulary

| status | meaning | counts as resolved? |
|---|---|---|
| `pending` | predicted window has not opened yet | no |
| `in_window` | inside the predicted window, not yet resolved | no |
| `achieved` | demonstrably happened (needs `resolved_date` + evidence) | yes |
| `partially` | meaningfully but not fully realized | yes |
| `missed` | window elapsed without it happening | yes |
| `unverifiable` | cannot be objectively scored | no |

For calibration, resolved statuses receive credit `achieved = 1.0`,
`partially = 0.5`, `missed = 0.0`.

## 4. The hypotheses and how they are tested

All statistics are computed by `Scripts/mathematics.py` (ordinary least squares
via numpy; no p-values are claimed — we report effect sizes, $r$, $R^2$, and a
slope $t$-statistic).

### H1 — Trajectory / calibration

Among predictions whose window has **elapsed** (`predicted_date ≤ today`) and
that are resolved, we report the credit-weighted hit-rate

$$\text{hit-rate} = \frac{1}{N}\sum_i c_i,\quad c_i \in \{0,\,0.5,\,1\}.$$

For each resolved-true prediction we also compute the **lead** (days early):

$$\text{lead}_i = \text{predicted\_date}_i - \text{resolved\_date}_i,$$

so a positive lead means the milestone arrived ahead of the deadline. We report
the mean, median, range, and the share with lead $\geq 0$.

### H2 — Horizon compression

Restricted to the **"powerful-AI-arrival"** forecasts (records tagged
`powerful_ai_arrival`) so the comparison is like-for-like, we regress the stated
horizon $h_i$ (years from utterance to predicted date) on the calendar year
$y_i$ the statement was made:

$$h_i = a + b\,y_i + \varepsilon_i.$$

A negative slope $b$ is evidence that Amodei expects powerful AI *sooner* as time
passes (the deadline stays roughly fixed while the clock advances). We report
$b$ (years of horizon per calendar year), Pearson $r$, and $R^2$.

### H3 — Realized acceleration

For the milestones scored `achieved`, we order them by `resolved_date` and fit
the cumulative count $C(t)$ both linearly and log-linearly (i.e. exponential,
$\log C = a + b t$). We compare $R^2$ and, when the exponential dominates and
$b > 0$, report a doubling time $\ln 2 / b$. This test requires at least three
achieved milestones; below that it reports *insufficient data* rather than
fitting noise.

## 5. Figures

`Scripts/mathematics.py` renders four figures (PNG + SVG) into `Doc/figures/`:
the timeline, the status distribution, the H2 horizon-compression scatter with
its fit, and the H3 cumulative-achievements curve.

## 6. Reproducibility & build

```bash
pip install -r requirements.txt
bash Scripts/build_all.sh   # validate → math → paper → exports → site
```

The build is deterministic given the dataset and the current date (the "as of"
date can be pinned for testing via the `DA_TODAY` environment variable). CI runs
the same pipeline and deploys the `site/` directory to GitHub Pages.

## 7. Limitations

- **Survivorship bias.** Bold, memorable predictions are easier to find than
  quiet, hedged ones. We mitigate this by requiring a primary source and by
  tracking `missed`, `pending`, and `in_window` items, not only successes.
- **Normalization sensitivity.** Turning verbal horizons into dates is a
  judgment call; results can shift with different normalization rules.
- **Scoring qualitative claims.** "AI writes most code" or "most cancer
  eliminated" require interpretation; we anchor each judgment to cited evidence.
- **Small N.** Few predictions have resolved, so H1/H3 rest on a handful of
  points today. The loop is designed to strengthen them over time.
