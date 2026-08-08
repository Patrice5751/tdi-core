from dataclasses import dataclass

from tdi.graphical.market_bias import MarketBias


@dataclass(frozen=True)
class MarketBiasAnalysis:
    bias: MarketBias
    confidence: int
    preferred_side: str | None
    reason: str
    