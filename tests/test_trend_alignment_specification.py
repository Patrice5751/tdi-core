from tdi.analysis.trend_analysis import Trend
from tdi.models.trade import Side
from tdi.specifications.trend_alignment import (
    TrendAlignmentSpecification,
)


def test_buy_with_bullish_trend():
    specification = TrendAlignmentSpecification()

    assert specification.is_satisfied_by(
        trend=Trend.BULLISH,
        side=Side.BUY,
    )


def test_sell_with_bearish_trend():
    specification = TrendAlignmentSpecification()

    assert specification.is_satisfied_by(
        trend=Trend.BEARISH,
        side=Side.SELL,
    )


def test_buy_with_bearish_trend_is_rejected():
    specification = TrendAlignmentSpecification()

    assert not specification.is_satisfied_by(
        trend=Trend.BEARISH,
        side=Side.BUY,
    )


def test_neutral_trend_is_not_aligned():
    specification = TrendAlignmentSpecification()

    assert not specification.is_satisfied_by(
        trend=Trend.NEUTRAL,
        side=Side.BUY,
    )