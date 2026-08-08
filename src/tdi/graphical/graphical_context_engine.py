from tdi.graphical.candle import Candle
from tdi.graphical.graphical_context import GraphicalContext
from tdi.graphical.market_direction import MarketDirection
from tdi.graphical.pivot_detector import PivotDetector
from tdi.graphical.price_location_engine import PriceLocationEngine
from tdi.graphical.price_location_input import PriceLocationInput
from tdi.graphical.support_resistance_engine import (
    SupportResistanceEngine,
)


class GraphicalContextEngine:
    def analyze(
        self,
        candles: list[Candle],
        current_price: float,
        atr: float,
        ma20: float,
        market_direction: MarketDirection,
        direction_confidence: int,
        breakout_level: float | None = None,
    ) -> GraphicalContext:
        pivots = PivotDetector().detect(
            candles=candles,
            atr=atr,
        )

        support_resistance = (
            SupportResistanceEngine().analyze(
                pivots=pivots,
                current_price=current_price,
                atr=atr,
            )
        )

        price_location = PriceLocationEngine().analyze(
            PriceLocationInput(
                current_price=current_price,
                market_direction=market_direction,
                ma20=ma20,
                atr=atr,
                nearest_support=support_resistance.support,
                nearest_resistance=support_resistance.resistance,
                breakout_level=breakout_level,
            )
        )

        return GraphicalContext(
            direction=market_direction,
            direction_confidence=direction_confidence,
            location_type=price_location.location_type,
            support=support_resistance.support,
            resistance=support_resistance.resistance,
            support_touches=support_resistance.support_touches,
            resistance_touches=support_resistance.resistance_touches,
        )
    