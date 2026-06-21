# Architecture — FPL Ultimate Analyzer

```mermaid
flowchart TD
    API[Public FPL bulk API\npolite client: UA + retry/backoff] --> CACHE[(Parquet cache\n1h TTL · platformdirs)]
    CACHE --> FE[Feature engineering\nform · fixtures · history]
    FE --> ENS
    subgraph ENS["ML ensemble"]
        MEAN[XGBoost + LightGBM + CatBoost\nmean predictor]
        Q[Quantile head\nceiling]
        P[Poisson goal-rate head\ncaptaincy]
    end
    ENS --> PROJ[Per-player projections]
    PROJ --> OPT
    subgraph OPT["Optimizers"]
        LP[PuLP linear programming\n15-man squad · budget + rules]
        ENUM[Ranked enumeration\nsingle-week transfers]
        BEAM[Beam search\nmulti-week plan]
    end
    OPT --> CLI[CLI: fpl_main.py]
    OPT --> WEB[Streamlit: fpl_gui.py]
    PROJ --> DIAG[Run Status / Diagnostics panel]
```

## Notes
- **One model, three decisions**: the same projections drive squad build, transfers, and multi-week planning.
- **Constraints as math**: budget, position quotas, and max-3-per-club are encoded as LP constraints, not heuristics.
- **Reproducible**: Parquet cache + time-pinned tests make runs deterministic within the TTL window.
