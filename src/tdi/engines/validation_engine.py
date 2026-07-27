from tdi.analysis.analysis_result import AnalysisResult
from tdi.analysis.momentum_analysis import Momentum
from tdi.analysis.risk_result import RiskResult
from tdi.analysis.structure_analysis import Structure
from tdi.analysis.trend_analysis import Trend
from tdi.analysis.validation_result import ValidationResult
from tdi.models.trade import Side

from config.trading_rules import (
    MIN_RR,
    VALIDATION_MIN_SCORE,
    VALIDATION_MOMENTUM_SCORE,
    VALIDATION_STRUCTURE_SCORE,
    VALIDATION_TREND_SCORE,
)


class ValidationEngine:
    """Vérifie l'alignement technique et la validité du risque."""

    def validate(
        self,
        analysis: AnalysisResult,
        risk: RiskResult,
        side: Side,
    ) -> ValidationResult:

        score = 0
        reasons: list[str] = []

        trend_ok = self._check_trend(
            trend=analysis.trend.trend,
            side=side,
            reasons=reasons,
        )

        momentum_ok = self._check_momentum(
            momentum=analysis.momentum.momentum,
            side=side,
            reasons=reasons,
        )

        structure_ok = self._check_structure(
            structure=analysis.structure.structure,
            side=side,
            entry_zone=analysis.structure.entry_zone,
            reasons=reasons,
        )

        if trend_ok:
            score += VALIDATION_TREND_SCORE

        if momentum_ok:
            score += VALIDATION_MOMENTUM_SCORE

        if structure_ok:
            score += VALIDATION_STRUCTURE_SCORE

        # Validation du ratio Risk/Reward
        rr_ok = risk.rr >= MIN_RR

        if rr_ok:
            reasons.append(
                f"Ratio R:R valide : {risk.rr:.2f} ≥ {MIN_RR:.2f}"
            )
        else:
            reasons.append(
                f"Ratio R:R insuffisant : {risk.rr:.2f} < {MIN_RR:.2f}"
            )

        # Validation générale du risque
        risk_ok = risk.valid

        if risk_ok:
            reasons.append("Gestion du risque valide")
        else:
            reasons.append("Gestion du risque non valide")

        # L'ATR ne fait pas encore partie de la validation
        atr_ok = False

        technical_ok = score >= VALIDATION_MIN_SCORE

        valid = technical_ok and rr_ok and risk_ok

        if valid:
            reasons.append("Trade techniquement et financièrement valide")
        elif not technical_ok:
            reasons.append("Validation technique insuffisante")
        else:
            reasons.append("Validation du risque insuffisante")

        return ValidationResult(
            score=score,
            trend_ok=trend_ok,
            momentum_ok=momentum_ok,
            structure_ok=structure_ok,
            rr_ok=rr_ok,
            risk_ok=risk_ok,
            atr_ok=atr_ok,
            valid=valid,
            reasons=reasons,
        )

    def _check_trend(
        self,
        trend: Trend,
        side: Side,
        reasons: list[str],
    ) -> bool:

        expected_trend = (
            Trend.BULLISH
            if side == Side.BUY
            else Trend.BEARISH
        )

        if trend == expected_trend:
            reasons.append("Tendance alignée avec le trade")
            return True

        reasons.append("Tendance non alignée avec le trade")
        return False

    def _check_momentum(
        self,
        momentum: Momentum,
        side: Side,
        reasons: list[str],
    ) -> bool:

        expected_momentum = (
            Momentum.BULLISH
            if side == Side.BUY
            else Momentum.BEARISH
        )

        if momentum == expected_momentum:
            reasons.append("Momentum aligné avec le trade")
            return True

        reasons.append("Momentum non aligné avec le trade")
        return False

    def _check_structure(
        self,
        structure: Structure,
        side: Side,
        entry_zone: bool,
        reasons: list[str],
    ) -> bool:

        expected_structure = (
            Structure.BULLISH
            if side == Side.BUY
            else Structure.BEARISH
        )

        if structure == expected_structure and entry_zone:
            reasons.append("Structure alignée et zone d'entrée valide")
            return True

        reasons.append("Structure ou zone d'entrée non valide")
        return False