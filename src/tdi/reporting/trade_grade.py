from dataclasses import dataclass


@dataclass(frozen=True)
class TradeGrade:
    value: float

    @staticmethod
    def from_score(score: int):
        """
        Convertit un score TDI (0-100)
        en note sur 10.
        """
        return TradeGrade(round(score / 10, 1))