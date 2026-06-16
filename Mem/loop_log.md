# Research Loop Log

Append-only log of each daily research/self-improvement loop iteration.

---

## 2026-06-16 — Iteration 0 (bootstrap)

**Research & Fetch.** Seeded the corpus from web search across Amodei's essays
(*Machines of Loving Grace*, *The Adolescence of Technology*), the OSTP policy
submission, Davos 2025 remarks, the CFR "90% of code" remarks, and the Axios
labour interview.

**Database.** Created `predictions_db.json` with 6 anchored predictions
(P001–P006); 4 Pending, 1 Failed (P004, 90%-of-code window elapsed), 1 Walked
Back (P006, labour forecast tempered by May 2026).

**Thesis.** H1 (contracting prediction horizon → accelerating expectation):
**SUPPORTED**. Linear fit slope = −0.197 yr/yr, R² = 0.966 across AGI-timeline
predictions (P001–P003).

**Docs.** Generated `Doc/acceleration_audit.md` and a zero-dependency
`Doc/acceleration_audit.pdf` (6 pages, validated xref). Built the GitHub Pages
site at `docs/` with the timeline as the centerpiece.

**Deploy.** Added `.github/workflows/deploy.yml` (push + daily cron → Pages).

**Self-improvement notes for next loop:**
- Upgrade P004/P005 anchors from secondhand reporting to primary transcripts.
- Add Wayback `archived_url` per source (link-rot guard).
- Add automated status re-evaluation: flag any Pending prediction whose
  `target_date` has elapsed for manual review (candidate for Failed/Achieved).
- Consider a `confidence` field where Amodei attached probabilities.
