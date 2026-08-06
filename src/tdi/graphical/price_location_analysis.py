from dataclasses import dataclass

from tdi.graphical.decision_zone import DecisionZone
from tdi.graphical.location_type import LocationType


@dataclass(frozen=True)
class PriceLocationAnalysis:
    location_type: LocationType

    decision_zone: DecisionZone

    quality_score: int

    extension_atr: float

    distance_ma20: float

    distance_support: float

    distance_resistance: float

    reason: str