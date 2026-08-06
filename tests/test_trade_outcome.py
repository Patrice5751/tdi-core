from tdi.models.trade_outcome import TradeOutcome


def test_create_trade_outcome():
    outcome = TradeOutcome(
        executed=True,
        winner=True,
        result_r=2.4,
        profit=180.0,
        notes="Breakout after pullback",
    )

    assert outcome.executed is True
    assert outcome.winner is True
    assert outcome.result_r == 2.4
    assert outcome.profit == 180.0
    assert outcome.notes == "Breakout after pullback"
    