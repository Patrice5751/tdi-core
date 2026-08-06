from tdi.analysis.momentum_analysis import Momentum
from tdi.models.trade import Side
from tdi.specifications.momentum_valid import (
    MomentumValidSpecification,
)


def test_buy_with_bullish_momentum():
    specification = MomentumValidSpecification()

    assert specification.is_satisfied_by(
        momentum=Momentum.BULLISH,
        side=Side.BUY,
    )


def test_sell_with_bearish_momentum():
    specification = MomentumValidSpecification()

    assert specification.is_satisfied_by(
        momentum=Momentum.BEARISH,
        side=Side.SELL,
    )


def test_buy_with_bearish_momentum_is_rejected():
    specification = MomentumValidSpecification()

    assert not specification.is_satisfied_by(
        momentum=Momentum.BEARISH,
        side=Side.BUY,
    )


def test_neutral_momentum_is_not_valid():
    specification = MomentumValidSpecification()

    assert not specification.is_satisfied_by(
        momentum=Momentum.NEUTRAL,
        side=Side.BUY,
    )