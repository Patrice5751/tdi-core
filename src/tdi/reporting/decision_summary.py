from dataclasses import dataclass
from tdi.reporting.decision import Decision
from tdi.reporting.confidence import Confidence


@dataclass(frozen=True)
class DecisionSummary:
    decision: Decision
    confidence: Confidence

    @staticmethod
    def from_score(score: int):
        if score >= 90:
            return DecisionSummary(
                 decision=Decision.STRONG_BUY,
                 confidence=Confidence.HIGH,
            )

        if score >= 75:
            return DecisionSummary(
                decision=Decision.BUY,
                confidence=Confidence.MEDIUM,
            )

        if score >= 60:
            return DecisionSummary(
                decision=Decision.BUY_WITH_CAUTION,
                confidence=Confidence.LOW,
            )

        return DecisionSummary(
            decision=Decision.NO_TRADE,
            confidence=Confidence.VERY_LOW,
        )