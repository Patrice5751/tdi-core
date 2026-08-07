from tdi.graphical.pivot import Pivot
from tdi.graphical.pivot_type import PivotType
from tdi.graphical.swing_point import SwingPoint
from tdi.graphical.swing_type import SwingType


class SwingClassifier:
    def classify(
        self,
        pivots: list[Pivot],
    ) -> list[SwingPoint]:
        if not pivots:
            return []

        swings: list[SwingPoint] = []

        previous_high: Pivot | None = None
        previous_low: Pivot | None = None

        for pivot in pivots:
            if pivot.pivot_type == PivotType.HIGH:
                if previous_high is not None:
                    swing_type = (
                        SwingType.HH
                        if pivot.price > previous_high.price
                        else SwingType.LH
                    )

                    swings.append(
                        SwingPoint(
                            index=pivot.index,
                            price=pivot.price,
                            swing_type=swing_type,
                        )
                    )

                previous_high = pivot

            elif pivot.pivot_type == PivotType.LOW:
                if previous_low is not None:
                    swing_type = (
                        SwingType.HL
                        if pivot.price > previous_low.price
                        else SwingType.LL
                    )

                    swings.append(
                        SwingPoint(
                            index=pivot.index,
                            price=pivot.price,
                            swing_type=swing_type,
                        )
                    )

                previous_low = pivot

        return swings
    