from tdi.graphical.candle import Candle
from tdi.graphical.pivot import Pivot
from tdi.graphical.pivot_type import PivotType


class PivotDetector:
    PIVOT_WIDTH = 2
    MIN_AMPLITUDE_ATR = 0.5

    def detect(
        self,
        candles: list[Candle],
        atr: float | None = None,
    ) -> list[Pivot]:
        if len(candles) < 5:
            return []

        pivots: list[Pivot] = []

        for i in range(
            self.PIVOT_WIDTH,
            len(candles) - self.PIVOT_WIDTH,
        ):
            current = candles[i]

            if (
                self._is_pivot_high(candles, i)
                and self._passes_atr_filter(
                    candles=candles,
                    index=i,
                    pivot_type=PivotType.HIGH,
                    atr=atr,
                )
            ):
                pivots.append(
                    Pivot(
                        index=current.index,
                        price=current.high,
                        pivot_type=PivotType.HIGH,
                    )
                )

            if (
                self._is_pivot_low(candles, i)
                and self._passes_atr_filter(
                    candles=candles,
                    index=i,
                    pivot_type=PivotType.LOW,
                    atr=atr,
                )
            ):
                pivots.append(
                    Pivot(
                        index=current.index,
                        price=current.low,
                        pivot_type=PivotType.LOW,
                    )
                )

        return pivots

    def _is_pivot_high(
        self,
        candles: list[Candle],
        index: int,
    ) -> bool:
        current_high = candles[index].high

        neighbours = self._neighbours(
            candles,
            index,
        )

        return all(
            current_high > candle.high
            for candle in neighbours
        )

    def _is_pivot_low(
        self,
        candles: list[Candle],
        index: int,
    ) -> bool:
        current_low = candles[index].low

        neighbours = self._neighbours(
            candles,
            index,
        )

        return all(
            current_low < candle.low
            for candle in neighbours
        )

    def _passes_atr_filter(
        self,
        candles: list[Candle],
        index: int,
        pivot_type: PivotType,
        atr: float | None,
    ) -> bool:
        if atr is None:
            return True

        if atr <= 0:
            return True

        neighbours = self._neighbours(
            candles,
            index,
        )

        if pivot_type == PivotType.HIGH:
            reference_price = max(
                candle.high
                for candle in neighbours
            )
            amplitude = (
                candles[index].high - reference_price
            )

        else:
            reference_price = min(
                candle.low
                for candle in neighbours
            )
            amplitude = (
                reference_price - candles[index].low
            )

        return amplitude >= (
            atr * self.MIN_AMPLITUDE_ATR
        )

    def _neighbours(
        self,
        candles: list[Candle],
        index: int,
    ) -> tuple[Candle, Candle, Candle, Candle]:
        return (
            candles[index - 2],
            candles[index - 1],
            candles[index + 1],
            candles[index + 2],
        )