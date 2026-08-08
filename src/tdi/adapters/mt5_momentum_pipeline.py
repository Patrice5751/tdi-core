from dataclasses import dataclass

from tdi.adapters.mt5_analysis_pipeline import (
    MT5AnalysisPipeline,
)
from tdi.analysis.momentum_analysis import MomentumAnalysis
from tdi.engines.momentum_engine import MomentumEngine
from tdi.indicators.indicator_engine import IndicatorEngine
from tdi.models.market_snapshot import MarketSnapshot


@dataclass(frozen=True)
class MT5MomentumPipeline:
    analysis_pipeline: MT5AnalysisPipeline

    def analyze(
        self,
        symbol: str,
        timeframe: str,
        count: int = 250,
    ) -> MomentumAnalysis:
        adapter = self.analysis_pipeline.adapter

        resolved_symbol = symbol

        if hasattr(
            adapter,
            "resolve_symbol",
        ):
            resolved_symbol = adapter.resolve_symbol(
                symbol
            )

        candles = adapter.get_candles(
            symbol=resolved_symbol,
            timeframe=timeframe,
            count=count,
        )

        if not candles:
            raise ValueError(
                "Aucune bougie disponible pour le momentum."
            )

        indicators = IndicatorEngine().calculate(
            candles
        )

        if (
            indicators.ma20 is None
            or indicators.ma50 is None
            or indicators.ma200 is None
            or indicators.rsi is None
            or indicators.macd is None
            or indicators.macd_signal is None
            or indicators.macd_histogram is None
        ):
            raise ValueError(
                "Indicateurs insuffisants pour le momentum."
            )

        current_price = adapter.get_current_price(
            resolved_symbol
        )

        snapshot = MarketSnapshot(
            price=current_price,
            ema20=indicators.ma20,
            ema50=indicators.ma50,
            ema200=indicators.ma200,
            rsi=indicators.rsi,
            macd=indicators.macd,
            macd_signal=indicators.macd_signal,
            macd_histogram=indicators.macd_histogram,
        )

        return MomentumEngine().analyze(
            snapshot
        )