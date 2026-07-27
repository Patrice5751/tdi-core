from tdi.analysis.structure_analysis import Structure, StructureAnalysis
from tdi.models.price_structure import PriceStructure
from tdi.models.trade import Side

from config.trading_rules import (
    STRUCTURE_ENTRY_THRESHOLD,
    STRUCTURE_NEAR_LEVEL_RATIO,
    STRUCTURE_RESISTANCE_SCORE,
    STRUCTURE_SUPPORT_SCORE,
    STRUCTURE_SWING_SCORE,
)


class StructureEngine:

    def analyze(
        self,
        structure: PriceStructure,
        side: Side,
    ) -> StructureAnalysis:

        if not self._is_valid_structure(structure):
            return StructureAnalysis(
                structure=Structure.NEUTRAL,
                confidence=0,
                entry_zone=False,
                reason=["Structure de prix invalide"],
            )

        score = 0
        reasons: list[str] = []

        score += self._check_support(structure, side, reasons)
        score += self._check_resistance(structure, side, reasons)
        score += self._check_swings(structure, side, reasons)

        entry_zone = score >= STRUCTURE_ENTRY_THRESHOLD

        if entry_zone:
            result = (
                Structure.BULLISH
                if side == Side.BUY
                else Structure.BEARISH
            )
        else:
            result = Structure.NEUTRAL

        if not reasons:
            reasons.append("Aucun critère structurel validé")

        return StructureAnalysis(
            structure=result,
            confidence=score,
            entry_zone=entry_zone,
            reason=reasons,
        )

    def _check_support(
        self,
        structure: PriceStructure,
        side: Side,
        reasons: list[str],
    ) -> int:

        price_range = structure.resistance - structure.support
        distance_to_support = (
            structure.current_price - structure.support
        ) / price_range

        if side == Side.BUY:
            if 0 <= distance_to_support <= STRUCTURE_NEAR_LEVEL_RATIO:
                reasons.append("Prix proche du support")
                return STRUCTURE_SUPPORT_SCORE

        if side == Side.SELL:
            if distance_to_support > STRUCTURE_NEAR_LEVEL_RATIO:
                reasons.append("Prix suffisamment éloigné du support")
                return STRUCTURE_SUPPORT_SCORE

        return 0

    def _check_resistance(
        self,
        structure: PriceStructure,
        side: Side,
        reasons: list[str],
    ) -> int:

        price_range = structure.resistance - structure.support
        distance_to_resistance = (
            structure.resistance - structure.current_price
        ) / price_range

        if side == Side.SELL:
            if 0 <= distance_to_resistance <= STRUCTURE_NEAR_LEVEL_RATIO:
                reasons.append("Prix proche de la résistance")
                return STRUCTURE_RESISTANCE_SCORE

        if side == Side.BUY:
            if distance_to_resistance > STRUCTURE_NEAR_LEVEL_RATIO:
                reasons.append("Résistance suffisamment éloignée")
                return STRUCTURE_RESISTANCE_SCORE

        return 0

    def _check_swings(
        self,
        structure: PriceStructure,
        side: Side,
        reasons: list[str],
    ) -> int:

        swing_range = structure.swing_high - structure.swing_low

        if swing_range <= 0:
            return 0

        if side == Side.BUY:
            distance_to_swing_low = (
                structure.current_price - structure.swing_low
            ) / swing_range

            if 0 <= distance_to_swing_low <= STRUCTURE_NEAR_LEVEL_RATIO:
                reasons.append("Prix proche du swing low")
                return STRUCTURE_SWING_SCORE

        if side == Side.SELL:
            distance_to_swing_high = (
                structure.swing_high - structure.current_price
            ) / swing_range

            if 0 <= distance_to_swing_high <= STRUCTURE_NEAR_LEVEL_RATIO:
                reasons.append("Prix proche du swing high")
                return STRUCTURE_SWING_SCORE

        return 0

    def _is_valid_structure(
        self,
        structure: PriceStructure,
    ) -> bool:

        return (
            structure.support < structure.resistance
            and structure.swing_low < structure.swing_high
        )