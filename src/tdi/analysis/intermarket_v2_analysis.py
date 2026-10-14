from dataclasses import dataclass
from enum import Enum

from tdi.analysis.trend_analysis import Trend


class IntermarketV2State(Enum):
    CONFIRMED = "Confirmed"
    MIXED = "Mixed"
    DIVERGENT = "Divergent"
    UNAVAILABLE = "Unavailable"


@dataclass(frozen=True)
class IntermarketV2Analysis:
    state: IntermarketV2State
    score: int | None
    primary_trend: Trend
    silver_trend: Trend | None
    dollar_trend: Trend | None
    silver_score: int | None
    dollar_score: int | None
    coverage: int
    reason: str