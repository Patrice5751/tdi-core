from tdi.advisor.atr_rule import ATRRule
from tdi.advisor.momentum_rule import MomentumRule
from tdi.advisor.risk_rule import RiskRule
from tdi.advisor.rr_rule import RRRule
from tdi.advisor.structure_rule import StructureRule
from tdi.advisor.trend_rule import TrendRule


class RuleEngine:

    @staticmethod
    def evaluate(
        trade,
        analysis,
        validation,
        risk,
    ):

        return [
            TrendRule.evaluate(
                confidence=analysis.trend.confidence,
            ),
            MomentumRule.evaluate(
                confidence=analysis.momentum.confidence,
            ),
            StructureRule.evaluate(
                side=trade.side,
                entry=trade.entry,
                support=analysis.structure.support,
                resistance=analysis.structure.resistance,
                atr=trade.atr,
            ),
            RRRule.evaluate(
                rr=risk.rr,
            ),
            RiskRule.evaluate(
                risk_ok=validation.risk_ok,
            ),
            ATRRule.evaluate(
                atr_ok=validation.atr_ok,
            ),
        ]