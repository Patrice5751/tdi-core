from tdi.graphical.pivot import Pivot
from tdi.graphical.pivot_type import PivotType
from tdi.graphical.support_resistance_analysis import (
    SupportResistanceAnalysis,
)


class SupportResistanceEngine:
    ZONE_TOLERANCE_ATR = 0.25

    def analyze(
        self,
        pivots: list[Pivot],
        current_price: float,
        atr: float | None = None,
    ) -> SupportResistanceAnalysis:
        supports = [
            pivot
            for pivot in pivots
            if (
                pivot.pivot_type == PivotType.LOW
                and pivot.price < current_price
            )
        ]

        resistances = [
            pivot
            for pivot in pivots
            if (
                pivot.pivot_type == PivotType.HIGH
                and pivot.price > current_price
            )
        ]

        support = (
            max(
                supports,
                key=lambda pivot: pivot.price,
            )
            if supports
            else None
        )

        resistance = (
            min(
                resistances,
                key=lambda pivot: pivot.price,
            )
            if resistances
            else None
        )

        return SupportResistanceAnalysis(
            support=(
                support.price
                if support is not None
                else None
            ),
            resistance=(
                resistance.price
                if resistance is not None
                else None
            ),
            support_touches=self._count_touches(
                pivots=pivots,
                reference=support,
                atr=atr,
            ),
            resistance_touches=self._count_touches(
                pivots=pivots,
                reference=resistance,
                atr=atr,
            ),
        )

    def _count_touches(
        self,
        pivots: list[Pivot],
        reference: Pivot | None,
        atr: float | None = None,
    ) -> int:
        if reference is None:
            return 0

        if atr is None or atr <= 0:
            return sum(
                pivot.pivot_type == reference.pivot_type
                and pivot.price == reference.price
                for pivot in pivots
            )

        tolerance = (
            atr * self.ZONE_TOLERANCE_ATR
        )

        return sum(
            pivot.pivot_type == reference.pivot_type
            and abs(
                pivot.price - reference.price
            ) <= tolerance
            for pivot in pivots
        )
    