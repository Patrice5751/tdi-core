from datetime import datetime

from tdi.graphical.candle import Candle


def test_create_candle():

    candle = Candle(
        index=15,
        timestamp=datetime(2026, 8, 7),
        open=100,
        high=105,
        low=99,
        close=103,
    )

    assert candle.index == 15

    assert candle.high == 105

    assert candle.low == 99
    