from dataclasses import dataclass
from enum import Enum

from tdi.analysis.trend_analysis import Trend


class IntermarketState(Enum):
    CONFIRMED = "Confirmed"
    MIXED = "Mixed"
    DIVERGENT = "Divergent"


@dataclass(frozen=True)
class IntermarketAnalysis:
    state: IntermarketState
    score: int
    primary_trend: Trend
    confirmation_trend: Trend
    reason: str