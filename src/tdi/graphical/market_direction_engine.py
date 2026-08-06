from tdi.graphical.market_direction import MarketDirection
from tdi.graphical.market_direction_analysis import (
    MarketDirectionAnalysis,
)
from tdi.graphical.swing_point import SwingPoint
from tdi.graphical.swing_type import SwingType


class MarketDirectionEngine:
    MIN_SWINGS = 4

    def detect(
        self,
        swings: list[SwingPoint],
    ) -> MarketDirectionAnalysis:
        if not swings:
            return MarketDirectionAnalysis(
                direction=MarketDirection.RANGE,
                structure_confidence=0,
                ma_confirmation=0,
                timeframe_alignment=0,
                confidence=0,
                reason="Aucun swing disponible.",
            )

        if len(swings) < self.MIN_SWINGS:
            confidence = min(len(swings) * 20, 60)

            return MarketDirectionAnalysis(
                direction=MarketDirection.TRANSITION,
                structure_confidence=confidence,
                ma_confirmation=0,
                timeframe_alignment=0,
                confidence=confidence,
                reason=(
                    "Nombre de swings insuffisant pour confirmer "
                    "une direction structurelle."
                ),
            )

        bullish_types = {SwingType.HH, SwingType.HL}
        bearish_types = {SwingType.LH, SwingType.LL}

        bullish_count = sum(
            swing.swing_type in bullish_types
            for swing in swings
        )

        bearish_count = sum(
            swing.swing_type in bearish_types
            for swing in swings
        )

        total = len(swings)

        bullish_ratio = bullish_count / total
        bearish_ratio = bearish_count / total

        if bullish_ratio >= 0.75:
            direction = MarketDirection.BULLISH
            reason = (
                f"Structure majoritairement haussière : "
                f"{bullish_count}/{total} swings compatibles."
            )

        elif bearish_ratio >= 0.75:
            direction = MarketDirection.BEARISH
            reason = (
                f"Structure majoritairement baissière : "
                f"{bearish_count}/{total} swings compatibles."
            )

        elif all(
            swing.swing_type in {SwingType.HL, SwingType.LH}
            for swing in swings
        ):
            direction = MarketDirection.RANGE
            reason = "Absence de progression directionnelle claire."

        else:
            direction = MarketDirection.TRANSITION
            reason = (
                "Structure mixte sans majorité directionnelle suffisante."
            )

        structure_confidence = self._calculate_structure_confidence(
            swings=swings,
            direction=direction,
        )

        return MarketDirectionAnalysis(
            direction=direction,
            structure_confidence=structure_confidence,
            ma_confirmation=0,
            timeframe_alignment=0,
            confidence=structure_confidence,
            reason=reason,
        )

    def _calculate_structure_confidence(
        self,
        swings: list[SwingPoint],
        direction: MarketDirection,
    ) -> int:
        if not swings:
            return 0

        if direction == MarketDirection.BULLISH:
            compatible_types = {SwingType.HH, SwingType.HL}

        elif direction == MarketDirection.BEARISH:
            compatible_types = {SwingType.LH, SwingType.LL}

        elif direction == MarketDirection.RANGE:
            compatible_types = {SwingType.HL, SwingType.LH}

        else:
            return 50

        compatible_count = sum(
            swing.swing_type in compatible_types
            for swing in swings
        )

        return round(
            compatible_count / len(swings) * 100
        )