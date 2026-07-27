from dataclasses import dataclass


@dataclass(frozen=True)
class PriceStructure:
    current_price: float

    support: float
    resistance: float

    swing_high: float
    swing_low: float