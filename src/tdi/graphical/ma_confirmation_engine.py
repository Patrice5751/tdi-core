from tdi.graphical.ma_confirmation_analysis import (
    MAConfirmationAnalysis,
)


class MAConfirmationEngine:
    def analyze(
        self,
        current_price: float,
        ma20: float | None,
        ma50: float | None,
        ma200: float | None,
    ) -> MAConfirmationAnalysis:
        if (
            ma20 is None
            or ma50 is None
            or ma200 is None
        ):
            return MAConfirmationAnalysis(
                score=0,
                bullish=False,
                bearish=False,
                reason="Moyennes mobiles insuffisantes.",
            )

        bullish_points = 0
        bearish_points = 0

        if current_price > ma20:
            bullish_points += 1
        elif current_price < ma20:
            bearish_points += 1

        if current_price > ma50:
            bullish_points += 1
        elif current_price < ma50:
            bearish_points += 1

        if current_price > ma200:
            bullish_points += 1
        elif current_price < ma200:
            bearish_points += 1

        if ma20 > ma50:
            bullish_points += 1
        elif ma20 < ma50:
            bearish_points += 1

        if ma50 > ma200:
            bullish_points += 1
        elif ma50 < ma200:
            bearish_points += 1

        total_points = 5

        bullish_score = round(
            bullish_points / total_points * 100
        )

        bearish_score = round(
            bearish_points / total_points * 100
        )

        if bullish_score >= 80:
            return MAConfirmationAnalysis(
                score=bullish_score,
                bullish=True,
                bearish=False,
                reason=(
                    "Prix au-dessus des moyennes mobiles "
                    "et ordre haussier des MA."
                ),
            )

        if bearish_score >= 80:
            return MAConfirmationAnalysis(
                score=bearish_score,
                bullish=False,
                bearish=True,
                reason=(
                    "Prix sous les moyennes mobiles "
                    "et ordre baissier des MA."
                ),
            )

        return MAConfirmationAnalysis(
            score=max(
                bullish_score,
                bearish_score,
            ),
            bullish=False,
            bearish=False,
            reason=(
                "Configuration des moyennes mobiles "
                "mixte ou insuffisamment directionnelle."
            ),
        )
    