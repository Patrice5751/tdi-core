from tdi.analysis.intermarket_analysis import (
    IntermarketAnalysis,
    IntermarketState,
)
from tdi.analysis.trend_analysis import Trend, TrendAnalysis


class IntermarketEngine:

    def analyze(
        self,
        primary: TrendAnalysis,
        confirmation: TrendAnalysis,
    ) -> IntermarketAnalysis:

        if (
            primary.trend == confirmation.trend
            and primary.trend != Trend.NEUTRAL
        ):
            return IntermarketAnalysis(
                state=IntermarketState.CONFIRMED,
                score=100,
                primary_trend=primary.trend,
                confirmation_trend=confirmation.trend,
                reason="Directional trends aligned",
            )

        if (
            primary.trend != Trend.NEUTRAL
            and confirmation.trend != Trend.NEUTRAL
            and primary.trend != confirmation.trend
        ):
            return IntermarketAnalysis(
                state=IntermarketState.DIVERGENT,
                score=0,
                primary_trend=primary.trend,
                confirmation_trend=confirmation.trend,
                reason="Directional trends opposed",
            )

        return IntermarketAnalysis(
            state=IntermarketState.MIXED,
            score=50,
            primary_trend=primary.trend,
            confirmation_trend=confirmation.trend,
            reason="At least one trend is neutral",
        )