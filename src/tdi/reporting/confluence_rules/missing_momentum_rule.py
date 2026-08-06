from tdi.reporting.confluence_observation import ConfluenceObservation
from tdi.reporting.severity import Severity

class MissingMomentumRule:

    @staticmethod
    def build(results):
        trend_passed = False
        momentum_passed = False

        for result in results:
            if result.rule == "Trend":
                trend_passed = result.passed

            elif result.rule == "Momentum":
                momentum_passed = result.passed

        if trend_passed and not momentum_passed:
            return ConfluenceObservation(
                severity=Severity.WARNING,
                title="Missing Momentum",
                message="Trend is valid but momentum confirmation is missing.",
            )

        return None
