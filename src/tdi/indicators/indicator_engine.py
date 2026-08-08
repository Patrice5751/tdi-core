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
            atr=self._atr(
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

    def _atr(
        self,
        candles: list[Candle],
        period: int,
    ) -> float | None:
        if len(candles) < period + 1:
            return None

        true_ranges: list[float] = []

        recent_candles = candles[-(period + 1):]

        for index in range(
            1,
            len(recent_candles),
        ):
            current = recent_candles[index]
            previous = recent_candles[index - 1]

            true_range = max(
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

            true_ranges.append(true_range)

        return sum(true_ranges) / period
    