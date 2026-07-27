from dataclasses import dataclass
from enum import Enum


class Momentum(Enum):
    BULLISH = "Bullish"
    BEARISH = "Bearish"
    NEUTRAL = "Neutral"


@dataclass(frozen=True)
class MomentumAnalysis:
    momentum: Momentum
    confidence: int
    reason: list[str]