from dataclasses import dataclass

from tdi.graphical.market_direction import MarketDirection


@dataclass(frozen=True)
class MarketDirectionAnalysis:

    direction: MarketDirection

    structure_confidence: int

    ma_confirmation: int

    timeframe_alignment: int

    confidence: int

    reason: str