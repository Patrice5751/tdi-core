from tdi.models.trade_outcome import TradeOutcome


class TradeOutcomeService:
    @staticmethod
    def attach(
        trade_record,
        outcome: TradeOutcome,
    ):
        trade_record.outcome = outcome