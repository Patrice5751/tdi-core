from tdi.analysis.trend_analysis import Trend
from tdi.models.trade import Side


class TrendAlignmentSpecification:
    """Checks whether the market trend matches the trade direction."""

    def is_satisfied_by(
        self,
        trend: Trend,
        side: Side,
    ) -> bool:
        expected_trend = (
            Trend.BULLISH
            if side == Side.BUY
            else Trend.BEARISH
        )

        return trend == expected_trend