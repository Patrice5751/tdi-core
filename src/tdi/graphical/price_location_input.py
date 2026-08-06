from dataclasses import dataclass

from tdi.graphical.market_direction import MarketDirection


@dataclass(frozen=True)
class PriceLocationInput:
    current_price: float

    market_direction: MarketDirection

    ma20: float

    atr: float

    nearest_support: float

    nearest_resistance: float

    breakout_level: float | None = None