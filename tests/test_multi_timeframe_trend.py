from tdi.analysis.multi_timeframe_trend import MultiTimeframeTrend
from tdi.analysis.trend_analysis import Trend


def test_create_multi_timeframe_trend():
    result = MultiTimeframeTrend(
        h4_trend=Trend.BEARISH,
        h1_trend=Trend.BEARISH,
    )

    assert result.h4_trend is Trend.BEARISH
    assert result.h1_trend is Trend.BEARISH