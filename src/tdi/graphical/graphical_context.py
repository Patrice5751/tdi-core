from dataclasses import dataclass

from tdi.graphical.market_direction import MarketDirection
from tdi.graphical.location_type import LocationType


@dataclass(frozen=True)
class GraphicalContext:
    direction: MarketDirection
    direction_confidence: int

    location_type: LocationType

    support: float | None
    resistance: float | None

    support_touches: int
    resistance_touches: int