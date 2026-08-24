from tdi.adapters.mt5_multi_timeframe_result import (
    MT5MultiTimeframeResult,
)
from tdi.analysis.momentum_analysis import (
    Momentum,
    MomentumAnalysis,
)
from tdi.graphical.location_type import LocationType
from tdi.graphical.market_bias_engine import (
    MarketBiasEngine,
)
from tdi.graphical.market_direction import MarketDirection
from tdi.graphical.wait_action_plan import WaitActionPlan
from tdi.graphical.wait_condition import WaitCondition


class WaitActionPlanEngine:
    def analyze(
        self,
        result: MT5MultiTimeframeResult,
        h4_momentum: MomentumAnalysis | None = None,
        h1_momentum: MomentumAnalysis | None = None,
    ) -> WaitActionPlan:
        h4_bias = MarketBiasEngine().analyze(
            result.h4
        )

        h1_bias = MarketBiasEngine().analyze(
            result.h1
        )

        preferred_side = (
            h4_bias.preferred_side
            if (
                h4_bias.preferred_side is not None
                and h4_bias.preferred_side
                == h1_bias.preferred_side
            )
            else None
        )

        conditions: list[WaitCondition] = []

        if preferred_side is None:
            return WaitActionPlan(
                preferred_side=None,
                conditions=[
                    WaitCondition.BIAS_ALIGNMENT
                ],
                ready=False,
                reason=(
                    "Les biais H4/H1 ne sont pas alignés. "
                    "Attendre un biais directionnel commun "
                    "avant de préparer une entrée."
                ),
            )

        self._add_structure_conditions(
            result=result,
            conditions=conditions,
        )

        self._add_location_conditions(
            result=result,
            preferred_side=preferred_side,
            conditions=conditions,
        )

        self._add_momentum_condition(
            preferred_side=preferred_side,
            h4_momentum=h4_momentum,
            h1_momentum=h1_momentum,
            conditions=conditions,
        )

        ready = len(conditions) == 0

        if ready:
            reason = (
                f"Les conditions {preferred_side} "
                "sont actuellement réunies."
            )
        else:
            reason = (
                f"Biais {preferred_side} identifié. "
                f"{len(conditions)} condition(s) "
                "reste(nt) à confirmer."
            )

        return WaitActionPlan(
            preferred_side=preferred_side,
            conditions=conditions,
            ready=ready,
            reason=reason,
        )

    def _add_structure_conditions(
        self,
        result: MT5MultiTimeframeResult,
        conditions: list[WaitCondition],
    ) -> None:
        if result.h4.direction in {
            MarketDirection.TRANSITION,
            MarketDirection.RANGE,
        }:
            conditions.append(
                WaitCondition.H4_STRUCTURE
            )

        if result.h1.direction in {
            MarketDirection.TRANSITION,
            MarketDirection.RANGE,
        }:
            conditions.append(
                WaitCondition.H1_STRUCTURE
            )

    def _add_location_conditions(
        self,
        result: MT5MultiTimeframeResult,
        preferred_side: str,
        conditions: list[WaitCondition],
    ) -> None:
        if result.h4.location_type == LocationType.EXTENSION:
            conditions.append(
                WaitCondition.H4_PULLBACK
            )

        if result.h1.location_type == LocationType.EXTENSION:
            conditions.append(
                WaitCondition.H1_PULLBACK
            )

        if (
            preferred_side == "BUY"
            and result.h1.location_type
            == LocationType.MIDDLE
        ):
            conditions.append(
                WaitCondition.H1_SUPPORT
            )

        if (
            preferred_side == "SELL"
            and result.h1.location_type
            == LocationType.MIDDLE
        ):
            conditions.append(
                WaitCondition.H1_RESISTANCE
            )

    def _add_momentum_condition(
        self,
        preferred_side: str,
        h4_momentum: MomentumAnalysis | None,
        h1_momentum: MomentumAnalysis | None,
        conditions: list[WaitCondition],
    ) -> None:
        if (
            h4_momentum is None
            or h1_momentum is None
        ):
            conditions.append(
                WaitCondition.MOMENTUM
            )
            return

        expected = (
            Momentum.BULLISH
            if preferred_side == "BUY"
            else Momentum.BEARISH
        )

        if (
            h4_momentum.momentum != expected
            or h1_momentum.momentum != expected
        ):
            conditions.append(
                WaitCondition.MOMENTUM
            )