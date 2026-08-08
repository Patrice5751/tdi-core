from dataclasses import dataclass

from tdi.graphical.location_type import LocationType
from tdi.graphical.market_direction import MarketDirection


@dataclass(frozen=True)
class GraphicalContext:
    direction: MarketDirection
    direction_confidence: int

    location_type: LocationType

    support: float | None
    resistance: float | None

    support_touches: int
    resistance_touches: int

    ma20: float | None = None
    ma50: float | None = None
    ma200: float | None = None

    ma_confirmation_score: int = 0
    ma_bullish: bool = False
    ma_bearish: bool = False
    