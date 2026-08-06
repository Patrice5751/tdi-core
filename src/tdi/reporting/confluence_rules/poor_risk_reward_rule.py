from tdi.reporting.confluence_observation import ConfluenceObservation
from tdi.reporting.severity import Severity


class PoorRiskRewardRule:

    @staticmethod
    def build(results):
        trend_passed = False
        momentum_passed = False
        structure_passed = False
        risk_reward_failed = False

        for result in results:
            if result.rule == "Trend":
                trend_passed = result.passed

            elif result.rule == "Momentum":
                momentum_passed = result.passed

            elif result.rule == "Structure":
                structure_passed = result.passed

            elif result.rule == "RiskReward":
                risk_reward_failed = not result.passed

        if (
            trend_passed
            and momentum_passed
            and structure_passed
            and risk_reward_failed
        ):
            return ConfluenceObservation(
                severity=Severity.CRITICAL,
                title="Poor Risk/Reward",
                message=(
                    "Technically valid setup, but not tradable "
                    "due to poor risk/reward."
                ),
            )

        return None