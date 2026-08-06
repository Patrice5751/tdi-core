from tdi.reporting.confluence_observation import ConfluenceObservation
from tdi.reporting.severity import Severity

class HighConvictionRule:

    @staticmethod
    def build(results):
        trend = False
        momentum = False
        structure = False
        risk_reward = False

        for result in results:
            if result.rule == "Trend" and result.passed:
                trend = True

            elif result.rule == "Momentum" and result.passed:
                momentum = True

            elif result.rule == "Structure" and result.passed:
                structure = True

            elif result.rule == "RiskReward" and result.passed:
                risk_reward = True

        if (
            trend
            and momentum
            and structure
            and risk_reward
        ):
            return ConfluenceObservation(
                severity=Severity.INFO,
                title="High Conviction",
                message="Trend, momentum, structure and risk/reward are aligned.",
            )

        return None