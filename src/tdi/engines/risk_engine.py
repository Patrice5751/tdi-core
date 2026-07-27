
from tdi.analysis.risk_result import RiskResult
from tdi.models.trade import Trade

from config.trading_rules import MIN_RR


class RiskEngine:

    def analyze(self, trade: Trade) -> RiskResult:

        reasons = []

        risk_amount = trade.capital * trade.risk_percent / 100

        stop_distance = abs(trade.entry - trade.stop_loss)

        target_distance = abs(trade.take_profit - trade.entry)

        rr = (
            target_distance / stop_distance
            if stop_distance > 0
            else 0.0
        )

        if stop_distance == 0:
            reasons.append("Le Stop Loss doit être différent du prix d'entrée")

        if rr < MIN_RR:
            valid = False
            reasons.append(
                f"Risk/Reward insuffisant ({rr:.2f} < {MIN_RR:.2f})"
            )

        valid = stop_distance > 0 and rr >= MIN_RR    

        return RiskResult(
            risk_amount=risk_amount,
            stop_distance=stop_distance,
            target_distance=target_distance,
            rr=rr,
            position_size=0.0,      # calculé dans la V2
            valid=valid,
            reasons=reasons,
        )