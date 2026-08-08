from tdi.graphical.candle import Candle
from tdi.indicators.indicator_result import IndicatorResult


class IndicatorEngine:
    ATR_PERIOD = 14
    RSI_PERIOD = 14

    MACD_FAST = 12
    MACD_SLOW = 26
    MACD_SIGNAL = 9

    def calculate(
        self,
        candles: list[Candle],
    ) -> IndicatorResult:
        closes = [
            candle.close
            for candle in candles
        ]

        macd_value, signal_value, histogram = (
            self._macd(closes)
        )

        return IndicatorResult(
            ma20=self._sma(candles, 20),
            ma50=self._sma(candles, 50),
            ma200=self._sma(candles, 200),
            atr=self._atr_wilder(
                candles,
                self.ATR_PERIOD,
            ),
            rsi=self._rsi_wilder(
                closes,
                self.RSI_PERIOD,
            ),
            macd=macd_value,
            macd_signal=signal_value,
            macd_histogram=histogram,
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
            abs(current.high - previous.close),
            abs(current.low - previous.close),
        )

    def _atr_wilder(
        self,
        candles: list[Candle],
        period: int,
    ) -> float | None:
        if len(candles) < period + 1:
            return None

        true_ranges: list[float] = []

        for index in range(1, len(candles)):
            true_ranges.append(
                self._true_range(
                    current=candles[index],
                    previous=candles[index - 1],
                )
            )

        atr = (
            sum(true_ranges[:period])
            / period
        )

        for true_range in true_ranges[period:]:
            atr = (
                (atr * (period - 1))
                + true_range
            ) / period

        return atr

    def _rsi_wilder(
        self,
        closes: list[float],
        period: int,
    ) -> float | None:
        if len(closes) < period + 1:
            return None

        gains: list[float] = []
        losses: list[float] = []

        for index in range(1, len(closes)):
            change = closes[index] - closes[index - 1]

            gains.append(
                max(change, 0.0)
            )
            losses.append(
                max(-change, 0.0)
            )

        avg_gain = (
            sum(gains[:period])
            / period
        )
        avg_loss = (
            sum(losses[:period])
            / period
        )

        for index in range(period, len(gains)):
            avg_gain = (
                (avg_gain * (period - 1))
                + gains[index]
            ) / period

            avg_loss = (
                (avg_loss * (period - 1))
                + losses[index]
            ) / period

        if avg_loss == 0:
            return 100.0

        if avg_gain == 0:
            return 0.0

        rs = avg_gain / avg_loss

        return 100.0 - (
            100.0 / (1.0 + rs)
        )

    def _ema_series(
        self,
        values: list[float],
        period: int,
    ) -> list[float]:
        if len(values) < period:
            return []

        multiplier = 2 / (period + 1)

        ema = (
            sum(values[:period])
            / period
        )

        result = [ema]

        for value in values[period:]:
            ema = (
                (value - ema)
                * multiplier
                + ema
            )
            result.append(ema)

        return result

    def _macd(
        self,
        closes: list[float],
    ) -> tuple[
        float | None,
        float | None,
        float | None,
    ]:
        if len(closes) < (
            self.MACD_SLOW
            + self.MACD_SIGNAL
            - 1
        ):
            return None, None, None

        fast_ema = self._ema_series(
            closes,
            self.MACD_FAST,
        )

        slow_ema = self._ema_series(
            closes,
            self.MACD_SLOW,
        )

        offset = (
            self.MACD_SLOW
            - self.MACD_FAST
        )

        aligned_fast = fast_ema[offset:]

        macd_series = [
            fast - slow
            for fast, slow in zip(
                aligned_fast,
                slow_ema,
            )
        ]

        signal_series = self._ema_series(
            macd_series,
            self.MACD_SIGNAL,
        )

        if not signal_series:
            return None, None, None

        macd_value = macd_series[-1]
        signal_value = signal_series[-1]

        return (
            macd_value,
            signal_value,
            macd_value - signal_value,
        )
    