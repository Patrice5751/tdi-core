from tdi.journal.statistics_result import StatisticsResult


class StatisticsEngine:

    @staticmethod
    def compute(records):

        executed = [
            r for r in records
            if r.outcome and r.outcome.executed
        ]

        trades = len(executed)

        winners = sum(
            1
            for r in executed
            if r.outcome.winner
        )

        losers = trades - winners

        win_rate = (
            winners / trades * 100
            if trades
            else 0.0
        )

        total_r = sum(
            r.outcome.result_r
            for r in executed
        )

        expectancy = (
            total_r / trades
            if trades
            else 0.0
        )

        winning_r = [
            r.outcome.result_r
            for r in executed
            if r.outcome.winner
        ]

        losing_r = [
            r.outcome.result_r
            for r in executed
            if not r.outcome.winner
        ]

        average_win = (
            sum(winning_r) / len(winning_r)
            if winning_r
            else 0.0
        )

        average_loss = (
            sum(losing_r) / len(losing_r)
            if losing_r
            else 0.0
        )        

        profit_factor = (
            sum(winning_r) / abs(sum(losing_r))
            if losing_r
            else 0.0
        )

        return StatisticsResult(
            trades=trades,
            winners=winners,
            losers=losers,
            win_rate=win_rate,
            expectancy=expectancy,
            average_win=average_win,
            average_loss=average_loss,
            profit_factor=profit_factor
        )

        