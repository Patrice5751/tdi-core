from tdi.engines.trend_engine import TrendEngine
from tdi.analysis.trend_analysis import Trend
from tdi.models.market_snapshot import MarketSnapshot


def test_bearish_trend():

    snapshot = MarketSnapshot(
        price=4000,
        ema20=4010,
        ema50=4030,
        ema200=4050,
        rsi=40,
        macd=-5,
        macd_signal=-2,
        macd_histogram=-3,
    )

    result = TrendEngine().analyze(snapshot)

    assert result.trend == Trend.BEARISH
    assert result.confidence == 90