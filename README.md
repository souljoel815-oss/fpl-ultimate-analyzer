# FPL Ultimate Analyzer

A **machine-learning analytics engine for Fantasy Premier League** that scores every player with a model ensemble and uses **mathematical optimization** to build the best possible squad, transfers, and multi-week plan — from the public FPL data feed alone.

> 🎥 **Demo:** _add your Loom link here_ · 🖼️ Screenshots in [`docs/screenshots/`](./docs/screenshots/)
>
> 🔒 This is a **showcase repo**. Full source available on request.

---

## The problem

FPL managers drown in stats but lack a principled way to convert them into decisions: *who to captain, who to transfer, and which 15 players give the best expected points under a £100m budget and squad rules?* This turns that into an optimization problem with an ML-driven objective.

## The solution

A clean Python package behind both a **CLI** and a **Streamlit** UI:

1. **Ingest** — pulls the public FPL bulk endpoints (polite client: User-Agent + retry/backoff, ≤10 requests per cold run). No login required.
2. **Feature engineering** — per-player features from form, fixtures, and history.
3. **ML ensemble** — XGBoost + LightGBM + CatBoost mean predictor, plus a **quantile head** (ceiling) and a **Poisson goal-rate head** (captaincy) for richer projections.
4. **Optimization** —
   - **PuLP linear programming** for from-scratch 15-man squad construction (budget + position + club constraints),
   - **ranked enumeration** for single-week transfer suggestions,
   - **beam search** across the planning horizon for multi-week plans.
5. **Diagnostics panel** — unified Run Status / Diagnostics in both CLI and web.

## Architecture

See [`docs/architecture.md`](./docs/architecture.md).

## Tech stack

| Area | Tools |
|---|---|
| ML | `scikit-learn`, `xgboost`, `lightgbm`, `catboost` |
| Optimization | `PuLP` (linear programming), beam search |
| Data | `pandas`, `numpy`, `scipy`, Parquet caching |
| HTTP | `requests` + `urllib3` retry adapter (polite client) |
| UI | `streamlit`, `plotly`; cross-platform paths via `platformdirs` |
| Quality | `pytest`, `responses` (API mocking), `freezegun` (time-pinned cache tests) |

## Engineering highlights

- **Disk cache** under the OS-standard user cache dir, 1-hour TTL, survives restarts (cold run ≤120s, cached ≤5s).
- **Measurable targets**: designed against explicit success criteria (cache hit rate ≥95%, ≤10 outbound requests per cold run).
- **Decoupled design**: a domain library (`fpl/`) with two thin entry points (CLI + web).

## Illustrative code

A representative, non-proprietary excerpt is in
[`samples/illustrative_interface.py`](./samples/illustrative_interface.py).

---

> Built against the **public** FPL feed only — no account credentials used.
