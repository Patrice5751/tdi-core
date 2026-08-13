from tdi.adapters.mt5_multi_timeframe_result import (
    MT5MultiTimeframeResult,
)
from tdi.analysis.momentum_analysis import (
    Momentum,
    MomentumAnalysis,
)
from tdi.graphical.wait_action_plan import WaitActionPlan
from tdi.graphical.wait_condition import WaitCondition
from tdi.graphical.wait_priority import WaitPriority


class WaitPriorityEngine:
    MOMENTUM_THRESHOLD = 50

    def prioritize(
        self,
        plan: WaitActionPlan,
        result: MT5MultiTimeframeResult,
        h4_momentum: MomentumAnalysis | None = None,
        h1_momentum: MomentumAnalysis | None = None,
    ) -> list[WaitPriority]:
        candidates: list[
            tuple[WaitCondition, int, str]
        ] = []

        for condition in plan.conditions:
            score, reason = self._condition_score(
                condition=condition,
                result=result,
                preferred_side=plan.preferred_side,
                h4_momentum=h4_momentum,
                h1_momentum=h1_momentum,
            )

            candidates.append(
                (
                    condition,
                    score,
                    reason,
                )
            )

        candidates.sort(
            key=lambda item: item[1],
            reverse=True,
        )

        return [
            WaitPriority(
                condition=condition,
                priority=index + 1,
                proximity_score=score,
                reason=reason,
            )
            for index, (
                condition,
                score,
                reason,
            ) in enumerate(candidates)
        ]

    def _condition_score(
        self,
        condition: WaitCondition,
        result: MT5MultiTimeframeResult,
        preferred_side: str | None,
        h4_momentum: MomentumAnalysis | None,
        h1_momentum: MomentumAnalysis | None,
    ) -> tuple[int, str]:
        if condition == WaitCondition.MOMENTUM:
            return self._momentum_score(
                preferred_side=preferred_side,
                h4_momentum=h4_momentum,
                h1_momentum=h1_momentum,
            )

        if condition in {
            WaitCondition.H1_SUPPORT,
            WaitCondition.H1_RESISTANCE,
        }:
            return (
                80,
                "Condition de timing H1 à surveiller en priorité.",
            )

        if condition == WaitCondition.H1_PULLBACK:
            return (
                85,
                "Le timing H1 nécessite encore un pullback.",
            )

        if condition == WaitCondition.H4_PULLBACK:
            return (
                75,
                "Le prix H4 doit revenir vers une zone plus favorable.",
            )

        if condition == WaitCondition.H1_STRUCTURE:
            score = min(
                70,
                result.h1.direction_confidence,
            )

            return (
                score,
                "La structure H1 doit confirmer le biais.",
            )

        if condition == WaitCondition.H4_STRUCTURE:
            score = min(
                65,
                result.h4.direction_confidence,
            )

            return (
                score,
                "La structure H4 doit confirmer le biais de fond.",
            )

        if condition == WaitCondition.BREAKOUT:
            return (
                75,
                "Une confirmation de breakout est attendue.",
            )

        return (
            0,
            "Condition en attente.",
        )

    def _momentum_score(
        self,
        preferred_side: str | None,
        h4_momentum: MomentumAnalysis | None,
        h1_momentum: MomentumAnalysis | None,
    ) -> tuple[int, str]:
        if (
            preferred_side is None
            or h4_momentum is None
            or h1_momentum is None
        ):
            return (
                20,
                "Momentum insuffisamment renseigné.",
            )

        expected = (
            Momentum.BULLISH
            if preferred_side == "BUY"
            else Momentum.BEARISH
        )

        if (
            h4_momentum.momentum == expected
            and h1_momentum.momentum == expected
        ):
            return (
                100,
                "Momentum H4/H1 déjà confirmé.",
            )

        confidence = max(
            h4_momentum.confidence,
            h1_momentum.confidence,
        )

        if (
            h4_momentum.momentum == Momentum.NEUTRAL
            and h1_momentum.momentum == Momentum.NEUTRAL
        ):
            distance = max(
                self.MOMENTUM_THRESHOLD
                - confidence,
                0,
            )

            proximity = max(
                90 - distance,
                0,
            )

            return (
                proximity,
                (
                    "Momentum encore neutre mais proche "
                    "du seuil de confirmation."
                ),
            )

        return (
            60,
            "Le momentum doit se réaligner avec le biais.",
        )
    