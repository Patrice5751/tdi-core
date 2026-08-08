from dataclasses import dataclass

from tdi.adapters.mt5_market_data_adapter import (
    MT5MarketDataAdapter,
)
from tdi.graphical.graphical_context import GraphicalContext
from tdi.graphical.graphical_context_engine import (
    GraphicalContextEngine,
)
from tdi.graphical.market_direction_engine import (
    MarketDirectionEngine,
)
from tdi.graphical.pivot_detector import PivotDetector
from tdi.graphical.swing_classifier import SwingClassifier
from tdi.indicators.indicator_engine import IndicatorEngine


@dataclass(frozen=True)
class MT5AnalysisPipeline:
    adapter: MT5MarketDataAdapter

    def analyze(
        self,
        symbol: str,
        timeframe: str = "H4",
        count: int = 250,
        breakout_level: float | None = None,
    ) -> GraphicalContext:
        candles = self.adapter.get_candles(
            symbol=symbol,
            timeframe=timeframe,
            count=count,
        )

        if not candles:
            raise ValueError(
                "Aucune bougie disponible pour l'analyse."
            )

        indicators = IndicatorEngine().calculate(
            candles
        )

        if indicators.atr is None:
            raise ValueError(
                "ATR indisponible : historique insuffisant."
            )

        if indicators.ma20 is None:
            raise ValueError(
                "MA20 indisponible : historique insuffisant."
            )

        pivots = PivotDetector().detect(
            candles=candles,
            atr=indicators.atr,
        )

        swings = SwingClassifier().classify(
            pivots
        )

        direction_analysis = (
            MarketDirectionEngine().detect(
                swings
            )
        )

        current_price = (
            self.adapter.get_current_price(
                symbol
            )
        )

        return GraphicalContextEngine().analyze(
            candles=candles,
            current_price=current_price,
            atr=indicators.atr,
            ma20=indicators.ma20,
            market_direction=(
                direction_analysis.direction
            ),
            direction_confidence=(
                direction_analysis.confidence
            ),
            breakout_level=breakout_level,
        )
    