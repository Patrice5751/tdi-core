from tdi.graphical.candle import Candle
from tdi.indicators.indicator_result import IndicatorResult


class IndicatorEngine:
    ATR_PERIOD = 14

    def calculate(
        self,
        candles: list[Candle],
    ) -> IndicatorResult:
        return IndicatorResult(
            ma20=self._sma(candles, 20),
            ma50=self._sma(candles, 50),
            ma200=self._sma(candles, 200),
            atr=self._atr_wilder(
                candles,
                self.ATR_PERIOD,
            ),
        )

    def _sma(
        self,
        candles: list[Candle],
        period: int,
    ) -> float | None:
        if len(candles) < period:
            return None

        closes = [
            candle.close
            for candle in candles[-period:]
        ]

        return sum(closes) / period

    def _true_range(
        self,
        current: Candle,
        previous: Candle,
    ) -> float:
        return max(
            current.high - current.low,
            abs(
                current.high
                - previous.close
            ),
            abs(
                current.low
                - previous.close
            ),
        )

    def _atr_wilder(
        self,
        candles: list[Candle],
        period: int,
    ) -> float | None:
        if len(candles) < period + 1:
            return None

        true_ranges: list[float] = []

        for index in range(
            1,
            len(candles),
        ):
            true_ranges.append(
                self._true_range(
                    current=candles[index],
                    previous=candles[index - 1],
                )
            )

        initial_atr = (
            sum(true_ranges[:period])
            / period
        )

        atr = initial_atr

        for true_range in true_ranges[period:]:
            atr = (
                (
                    atr * (period - 1)
                )
                + true_range
            ) / period

        return atr
    