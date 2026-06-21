"""
Illustrative interface excerpt — FPL Ultimate Analyzer.

Representative structure/style only. The trained models, feature engineering,
and optimizer internals are private and NOT included here.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PlayerProjection:
    player_id: int
    name: str
    position: str          # GK | DEF | MID | FWD
    club: str
    price: float           # in £m
    mean_points: float     # ensemble mean
    ceiling: float         # quantile head
    captain_score: float   # Poisson goal-rate head


# Squad rules expressed declaratively — the optimizer (PuLP) consumes these.
SQUAD_RULES = {
    "budget": 100.0,
    "size": 15,
    "by_position": {"GK": 2, "DEF": 5, "MID": 5, "FWD": 3},
    "max_per_club": 3,
}


def best_captain(squad: list[PlayerProjection]) -> PlayerProjection:
    """Captaincy uses the Poisson goal-rate head, not raw mean points."""
    return max(squad, key=lambda p: p.captain_score)


def value_score(p: PlayerProjection) -> float:
    """A simple points-per-million heuristic used for quick ranking/inspection.
    The real optimizer solves a constrained LP rather than ranking on value alone.
    """
    return p.mean_points / p.price if p.price else 0.0
