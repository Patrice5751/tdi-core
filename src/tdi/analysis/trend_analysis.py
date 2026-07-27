from dataclasses import dataclass
from enum import Enum


class Trend(Enum):
    BULLISH = "Bullish"
    BEARISH = "Bearish"
    NEUTRAL = "Neutral"


@dataclass(frozen=True)
class TrendAnalysis:
    trend: Trend
    confidence: int
    reason: str