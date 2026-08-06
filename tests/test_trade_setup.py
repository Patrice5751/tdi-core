from tdi.advisor.trade_setup import TradeSetup


def test_create_trade_setup():
    setup = TradeSetup(
        symbol="XAUUSD",
        direction="SELL",
        entry=4050,
        stop_loss=4090,
        take_profit=3970,
        atr_h4=23,
        capital=5000,
        risk_percent=1.5,
    )

    assert setup.symbol == "XAUUSD"
    assert setup.direction == "SELL"
    assert setup.atr_h4 == 23
    assert setup.capital == 5000