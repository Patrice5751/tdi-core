from tdi.adapters.mt5_momentum_pipeline import (
    MT5MomentumPipeline,
)
from tdi.analysis.momentum_analysis import Momentum
from tdi.graphical.candle import Candle


class FakeAdapter:
    def __init__(
        self,
        candles,
        price=100.0,
    ):
        self._candles = candles
        self._price = price

    def get_candles(
        self,
        symbol,
        timeframe,
        count,
    ):
        return self._candles[:count]

    def get_current_price(
        self,
        symbol,
    ):
        return self._price


class FakeAnalysisPipeline:
    def __init__(
        self,
        adapter,
    ):
        self.adapter = adapter


def make_rising_candles(
    count: int,
) -> list[Candle]:
    candles = []

    for index in range(count):
        close = 100.0 + index

        candles.append(
            Candle(
                index=index,
                timestamp=None,
                open=close - 1,
                high=close + 2,
                low=close - 2,
                close=close,
            )
        )

    return candles


def test_momentum_pipeline_returns_analysis():
    adapter = FakeAdapter(
        make_rising_candles(250)
    )

    pipeline = MT5MomentumPipeline(
        analysis_pipeline=FakeAnalysisPipeline(
            adapter
        )
    )

    result = pipeline.analyze(
        symbol="XAUUSD",
        timeframe="H4",
    )

    assert result.momentum in {
        Momentum.BULLISH,
        Momentum.BEARISH,
        Momentum.NEUTRAL,
    }


def test_linear_rising_market_can_remain_neutral():
    adapter = FakeAdapter(
        make_rising_candles(250)
    )

    pipeline = MT5MomentumPipeline(
        analysis_pipeline=FakeAnalysisPipeline(
            adapter
        )
    )

    result = pipeline.analyze(
        symbol="XAUUSD",
        timeframe="H4",
    )

    assert result.momentum == Momentum.NEUTRAL
    assert result.confidence == 30

def test_empty_history_raises_error():
    adapter = FakeAdapter([])

    pipeline = MT5MomentumPipeline(
        analysis_pipeline=FakeAnalysisPipeline(
            adapter
        )
    )

    try:
        pipeline.analyze(
            symbol="XAUUSD",
            timeframe="H4",
        )
        raised = False
    except ValueError:
        raised = True

    assert raised is True

def make_accelerating_candles(
    count: int,
) -> list[Candle]:
    candles = []

    price = 100.0

    for index in range(count):
        increment = 0.05 + (
            index / count
        )

        price += increment

        candles.append(
            Candle(
                index=index,
                timestamp=None,
                open=price - 1,
                high=price + 2,
                low=price - 2,
                close=price,
            )
        )

    return candles

def test_accelerating_market_returns_bullish_momentum():
    adapter = FakeAdapter(
        make_accelerating_candles(250)
    )

    pipeline = MT5MomentumPipeline(
        analysis_pipeline=FakeAnalysisPipeline(
            adapter
        )
    )

    result = pipeline.analyze(
        symbol="XAUUSD",
        timeframe="H4",
    )

    assert result.momentum == Momentum.BULLISH
    assert result.confidence >= 50