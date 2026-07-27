
from tdi.analysis.trend_analysis import Trend, TrendAnalysis
from tdi.models.market_snapshot import MarketSnapshot
from config.trading_rules import RSI_SCORE
from config.trading_rules import MIN_CONFIDENCE

class TrendEngine:

    def analyze(self, snapshot: MarketSnapshot) -> TrendAnalysis:

        # Tendance haussière
        if snapshot.ema20 > snapshot.ema50 > snapshot.ema200:
            confidence = MIN_CONFIDENCE

            if snapshot.price > snapshot.ema20:
                confidence += 20

            return TrendAnalysis(
                trend=Trend.BULLISH,
                confidence=confidence,
                reason="EMA20 > EMA50 > EMA200",
            )

        # Tendance baissière
        if snapshot.ema20 < snapshot.ema50 < snapshot.ema200:
            confidence = MIN_CONFIDENCE

            if snapshot.price < snapshot.ema20:
                confidence += 20

            return TrendAnalysis(
                trend=Trend.BEARISH,
                confidence=confidence,
                reason="EMA20 < EMA50 < EMA200",
            )

        return TrendAnalysis(
            trend=Trend.NEUTRAL,
            confidence=40,
            reason="EMA non alignées",
        )
