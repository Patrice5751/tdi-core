from tdi.analysis.analysis_result import AnalysisResult
from tdi.analysis.decision_result import DecisionResult
from tdi.analysis.recommendation import Recommendation
from tdi.analysis.risk_result import RiskResult
from tdi.analysis.validation_result import ValidationResult

from config.trading_rules import (
    DECISION_ACCEPTABLE,
    DECISION_EXCELLENT,
    DECISION_GOOD,
    DECISION_RR_BONUS,
    DECISION_TREND_BONUS,
    DECISION_WAIT,
)


class DecisionEngine:

    def decide(
        self,
        analysis: AnalysisResult,
        validation: ValidationResult,
        risk: RiskResult,
    ) -> DecisionResult:

        score = self._compute_score(
            analysis,
            validation,
            risk,
        )

        confidence = score / 10

        recommendation = self._recommendation(score)

        strengths = self._strengths(validation, risk)

        weaknesses = self._weaknesses(validation)

        return DecisionResult(
            score=score,
            confidence=confidence,
            accepted=validation.valid,
            recommendation=recommendation,
            strengths=strengths,
            weaknesses=weaknesses,
        )

    def _compute_score(
        self,
        analysis: AnalysisResult,
        validation: ValidationResult,
        risk: RiskResult,
    ) -> int:

        score = validation.score

        if risk.rr >= 3:
            score += DECISION_RR_BONUS

        if analysis.trend.confidence >= 90:
            score += DECISION_TREND_BONUS

        return min(score, 100)

    def _recommendation(
        self,
        score: int,
    ) -> Recommendation:

        if score >= DECISION_EXCELLENT:
            return Recommendation.EXCELLENT

        if score >= DECISION_GOOD:
            return Recommendation.TAKE

        if score >= DECISION_ACCEPTABLE:
            return Recommendation.ACCEPTABLE

        if score >= DECISION_WAIT:
            return Recommendation.WAIT

        return Recommendation.REJECT

    def _strengths(
        self,
        validation: ValidationResult,
        risk: RiskResult,
    ) -> list[str]:

        strengths = []

        if validation.trend_ok:
            strengths.append("Tendance alignée")

        if validation.momentum_ok:
            strengths.append("Momentum confirmé")

        if validation.structure_ok:
            strengths.append("Structure favorable")

        if validation.rr_ok:
            strengths.append(f"Risk/Reward = {risk.rr:.2f}")

        return strengths

    def _weaknesses(
        self,
        validation: ValidationResult,
    ) -> list[str]:

        weaknesses = []

        if not validation.trend_ok:
            weaknesses.append("Tendance non alignée")

        if not validation.momentum_ok:
            weaknesses.append("Momentum insuffisant")

        if not validation.structure_ok:
            weaknesses.append("Structure défavorable")

        if not validation.rr_ok:
            weaknesses.append("Risk/Reward insuffisant")

        if not weaknesses:
            weaknesses.append("Aucune faiblesse majeure")

        return weaknesses