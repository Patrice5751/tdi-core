from tdi.engines.timeframe_alignment_engine import (
    TimeframeAlignmentEngine,
)

from tdi.analysis.trend_analysis import Trend
from tdi.models.trade import Side


def test_buy_alignment():

    result = TimeframeAlignmentEngine.evaluate(
        h4_trend=Trend.BULLISH,
        h1_trend=Trend.BULLISH,
        side=Side.BUY,
    )

    assert result.aligned is True


def test_buy_not_aligned():

    result = TimeframeAlignmentEngine.evaluate(
        h4_trend=Trend.BULLISH,
        h1_trend=Trend.BEARISH,
        side=Side.BUY,
    )

    assert result.aligned is False


def test_sell_alignment():

    result = TimeframeAlignmentEngine.evaluate(
        h4_trend=Trend.BEARISH,
        h1_trend=Trend.BEARISH,
        side=Side.SELL,
    )

    assert result.aligned is True


def test_sell_not_aligned():

    result = TimeframeAlignmentEngine.evaluate(
        h4_trend=Trend.BEARISH,
        h1_trend=Trend.BULLISH,
        side=Side.SELL,
    )

    assert result.aligned is False