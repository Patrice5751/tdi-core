from tdi.journal.trade_outcome_service import TradeOutcomeService
from tdi.models.trade_outcome import TradeOutcome


class DummyTradeRecord:

    def __init__(self):
        self.outcome = None


def test_attach_trade_outcome():
    record = DummyTradeRecord()

    outcome = TradeOutcome(
        executed=True,
        winner=True,
        result_r=2.0,
        profit=150.0,
        notes="Excellent pullback",
    )

    TradeOutcomeService.attach(
        record,
        outcome,
    )

    assert record.outcome == outcome