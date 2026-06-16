# Primary Source Registry

Every prediction in `predictions_db.json` must cite an explicit, hyperlinked
primary source. This registry is the canonical list of sources consulted, so
future loop iterations can re-verify and de-duplicate.

| Pred IDs | Source | URL | Type | Verified |
|----------|--------|-----|------|----------|
| P001 | Machines of Loving Grace (Oct 24, 2024) | https://darioamodei.com/essay/machines-of-loving-grace | Essay (canonical) | URL canonical |
| P002 | Anthropic recommendations to OSTP for the U.S. AI Action Plan (Mar 2025) | https://www.anthropic.com/news/anthropic-s-recommendations-ostp-u-s-ai-action-plan | Policy submission | Page 403s to bots; widely cited primary |
| P003 | The Adolescence of Technology (Jan 27, 2026) | https://darioamodei.com/essay/the-adolescence-of-technology | Essay (canonical) | URL canonical |
| P004 | Council on Foreign Relations remarks (Mar 10, 2025), reported | https://finance.yahoo.com/news/anthropic-ceo-says-ai-could-193020957.html | Public remarks | Reported; seek CFR transcript |
| P005 | World Economic Forum / Davos 2025 remarks, reported | https://www.pymnts.com/artificial-intelligence-2/2025/anthropic-ceo-sees-ai-powered-advances-doubling-human-lifespans/ | Interview | Reported; seek WEF video |
| P006 | Axios "Behind the Curtain: A white-collar bloodbath" (May 28, 2025) | https://www.axios.com/2025/05/28/ai-jobs-white-collar-unemployment-anthropic | Interview | URL verified |

## Corroborating / context sources (not prediction anchors)

- Fortune (May 26, 2026) — Altman & Amodei walking back jobs-apocalypse forecasts: https://fortune.com/2026/05/26/sam-altman-dario-amodei-walking-back-ai-jobs-apocalypse-prophecies-ipo/
- Redwood Research — "Is 90% of code at Anthropic being written by AIs?": https://blog.redwoodresearch.org/p/is-90-of-code-at-anthropic-being
- Fortune (Jan 27, 2026) — coverage of "The Adolescence of Technology": https://fortune.com/2026/01/27/anthropic-ceo-dario-amodei-essay-warning-ai-adolescence-test-humanity-risks-remedies/

## TODO for future loops (improve source accuracy — per CRITICAL CONSTRAINTS)

- [ ] Replace reported-secondhand anchors (P004, P005) with primary transcripts/video where available.
- [ ] Add direct Anthropic/darioamodei.com permalink for the OSTP submission text (P002).
- [ ] Add an `archived_url` field (Wayback) per source to guard against link rot.
