from tdi.analysis.momentum_analysis import Momentum, MomentumAnalysis
from tdi.models.market_snapshot import MarketSnapshot

from config.trading_rules import (
    HISTOGRAM_SCORE,
    MACD_SCORE,
    MOMENTUM_DECISION_THRESHOLD,
    RSI_BUY_THRESHOLD,
    RSI_SCORE,
    RSI_SELL_THRESHOLD,
)


class MomentumEngine:

    def analyze(self, snapshot: MarketSnapshot) -> MomentumAnalysis:

        score = 0
        reasons: list[str] = []

        # RSI
        if snapshot.rsi > RSI_BUY_THRESHOLD:
            score += RSI_SCORE
            reasons.append(f"RSI > {RSI_BUY_THRESHOLD}")

        elif snapshot.rsi < RSI_SELL_THRESHOLD:
            score -= RSI_SCORE
            reasons.append(f"RSI < {RSI_SELL_THRESHOLD}")

        # MACD
        if snapshot.macd > snapshot.macd_signal:
            score += MACD_SCORE
            reasons.append("MACD > Signal")

        elif snapshot.macd < snapshot.macd_signal:
            score -= MACD_SCORE
            reasons.append("MACD < Signal")

        # Histogramme
        if snapshot.macd_histogram > 0:
            score += HISTOGRAM_SCORE
            reasons.append("Histogramme positif")

        elif snapshot.macd_histogram < 0:
            score -= HISTOGRAM_SCORE
            reasons.append("Histogramme négatif")

        # Décision
        if score >= MOMENTUM_DECISION_THRESHOLD:
            return MomentumAnalysis(
                momentum=Momentum.BULLISH,
                confidence=score,
                reason=reasons,
            )

        if score <= -MOMENTUM_DECISION_THRESHOLD:
            return MomentumAnalysis(
                momentum=Momentum.BEARISH,
                confidence=abs(score),
                reason=reasons,
            )

        return MomentumAnalysis(
            momentum=Momentum.NEUTRAL,
            confidence=abs(score),
            reason=reasons,
        )