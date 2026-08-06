from config.trading_rules import MIN_RR
from tdi.analysis.risk_result import RiskResult


class MinimumRRSpecification:
    """Checks whether the Risk/Reward ratio satisfies the minimum requirement."""

    def is_satisfied_by(self, risk: RiskResult) -> bool:
        return risk.rr >= MIN_RR