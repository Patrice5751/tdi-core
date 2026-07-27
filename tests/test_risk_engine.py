import pytest

from tdi.engines.risk_engine import RiskEngine
from tdi.models.trade import Side, Trade


def make_trade(
    entry: float = 4050.0,
    stop_loss: float = 4090.0,
    take_profit: float = 3970.0,
) -> Trade:
    return Trade(
        instrument="XAUUSD",
        side=Side.SELL,
        entry=entry,
        stop_loss=stop_loss,
        take_profit=take_profit,
        capital=5000.0,
        risk_percent=1.0,
        timeframe="H4",
        atr=30.0,
        created_at=None,
    )


def test_risk_engine_calculates_valid_trade() -> None:
    engine = RiskEngine()
    trade = make_trade()

    result = engine.analyze(trade)

    assert result.risk_amount == pytest.approx(50.0)
    assert result.stop_distance == pytest.approx(40.0)
    assert result.target_distance == pytest.approx(80.0)
    assert result.rr == pytest.approx(2.0)
    assert result.position_size == pytest.approx(0.0)
    assert result.valid is True


def test_risk_engine_rejects_low_rr() -> None:
    engine = RiskEngine()

    trade = make_trade(
        entry=4050.0,
        stop_loss=4090.0,
        take_profit=4010.0,
    )

    result = engine.analyze(trade)

    assert result.rr == pytest.approx(1.0)
    assert result.valid is False
    assert result.reasons


def test_risk_engine_handles_zero_stop_distance() -> None:
    engine = RiskEngine()

    trade = make_trade(
        entry=4050.0,
        stop_loss=4050.0,
        take_profit=3970.0,
    )

    result = engine.analyze(trade)

    assert result.stop_distance == pytest.approx(0.0)
    assert result.rr == pytest.approx(0.0)
    assert result.valid is False