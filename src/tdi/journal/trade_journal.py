from tdi.journal.trade_record import TradeRecord


class TradeJournal:
    """Collection de TradeRecord."""

    def __init__(self):
        self._records: list[TradeRecord] = []

    def add(self, record: TradeRecord):
        self._records.append(record)

    @property
    def records(self):
        return tuple(self._records)

    def count(self):
        return len(self._records)

    def find_by_trade_id(self, trade_id: str):
        for record in self._records:
            if record.trade_id == trade_id:
                return record

        return None