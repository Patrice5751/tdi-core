from tdi.journal.statistics_engine import StatisticsEngine
from tdi.models.trade_outcome import TradeOutcome


class DummyRecord:

    def __init__(self, outcome):
        self.outcome = outcome


def test_compute_win_rate():

    records = [
        DummyRecord(
            TradeOutcome(
                executed=True,
                winner=True,
                result_r=2.0,
                profit=150,
            )
        ),
        DummyRecord(
            TradeOutcome(
                executed=True,
                winner=False,
                result_r=-1.0,
                profit=-75,
            )
        ),
        DummyRecord(
            TradeOutcome(
                executed=True,
                winner=True,
                result_r=1.5,
                profit=110,
            )
        ),
    ]

    stats = StatisticsEngine.compute(records)

    assert stats.trades == 3
    assert stats.winners == 2
    assert stats.losers == 1
    assert round(stats.win_rate, 1) == 66.7

def test_compute_expectancy():

    records = [
        DummyRecord(
            TradeOutcome(
                executed=True,
                winner=True,
                result_r=2.0,
                profit=150,
            )
        ),
        DummyRecord(
            TradeOutcome(
                executed=True,
                winner=False,
                result_r=-1.0,
                profit=-75,
            )
        ),
        DummyRecord(
            TradeOutcome(
                executed=True,
                winner=True,
                result_r=1.5,
                profit=110,
            )
        ),
    ]

    stats = StatisticsEngine.compute(records)

    assert round(stats.expectancy, 3) == 0.833

def test_compute_expectancy():
    records = [
        DummyRecord(
            TradeOutcome(
                executed=True,
                winner=True,
                result_r=2.0,
                profit=150,
            )
        ),
        DummyRecord(
            TradeOutcome(
                executed=True,
                winner=False,
                result_r=-1.0,
                profit=-75,
            )
        ),
        DummyRecord(
            TradeOutcome(
                executed=True,
                winner=True,
                result_r=1.5,
                profit=110,
            )
        ),
    ]

    stats = StatisticsEngine.compute(records)

    assert round(stats.expectancy, 3) == 0.833

def test_compute_average_win_loss():

    records = [
        DummyRecord(
            TradeOutcome(
                executed=True,
               winner=True,
                result_r=2.0,
                profit=150,
            )
        ),
        DummyRecord(
            TradeOutcome(
                executed=True,
                winner=False,
                result_r=-1.0,
                profit=-75,
            )
        ),
        DummyRecord(
            TradeOutcome(
                executed=True,
                winner=True,
                result_r=1.5,
                profit=110,
            )
        ),
    ]

    stats = StatisticsEngine.compute(records)

    assert round(stats.average_win, 2) == 1.75
    assert round(stats.average_loss, 2) == -1.00

def test_compute_profit_factor():

    records = [
        DummyRecord(
            TradeOutcome(
                executed=True,
                winner=True,
                result_r=2.0,
                profit=150,
            )
        ),
        DummyRecord(
            TradeOutcome(
                executed=True,
                winner=False,
                result_r=-1.0,
                profit=-75,
            )
        ),
        DummyRecord(
            TradeOutcome(
                executed=True,
                winner=True,
                result_r=1.5,
                profit=110,
            )
        ),
    ]

    stats = StatisticsEngine.compute(records)

    assert round(stats.profit_factor, 2) == 3.50
    