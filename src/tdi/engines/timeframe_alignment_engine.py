from tdi.analysis.timeframe_alignment import TimeframeAlignment
from tdi.analysis.trend_analysis import Trend
from tdi.models.trade import Side


class TimeframeAlignmentEngine:
    @staticmethod
    def evaluate(
        h4_trend: Trend,
        h1_trend: Trend,
        side: Side,
    ) -> TimeframeAlignment:
        expected_trend = (
            Trend.BULLISH
            if side == Side.BUY
            else Trend.BEARISH
        )

        aligned = (
            h4_trend == expected_trend
            and h1_trend == expected_trend
        )

        score = 10 if aligned else 0

        return TimeframeAlignment(
            aligned=aligned,
            score=score,
        )
        