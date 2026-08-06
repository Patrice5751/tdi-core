from dataclasses import dataclass


@dataclass(frozen=True)
class StatisticsResult:
    trades: int
    winners: int
    losers: int
    win_rate: float
    expectancy: float

    average_win: float
    average_loss: float

    profit_factor: float