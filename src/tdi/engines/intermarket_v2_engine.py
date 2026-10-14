from tdi.analysis.intermarket_v2_analysis import (
    IntermarketV2Analysis,
    IntermarketV2State,
)
from tdi.analysis.trend_analysis import Trend


class IntermarketV2Engine:
    SILVER_WEIGHT = 60
    DOLLAR_WEIGHT = 40

    @staticmethod
    def _component_score(
        primary: Trend,
        confirmation: Trend | None,
        inverse: bool = False,
    ) -> int | None:
        if confirmation is None or primary == Trend.NEUTRAL:
            return None

        if confirmation == Trend.NEUTRAL:
            return 50

        aligned = primary == confirmation
        if inverse:
            aligned = not aligned

        return 100 if aligned else 0

    def analyze(
        self,
        primary: Trend,
        silver: Trend | None,
        dollar: Trend | None,
    ) -> IntermarketV2Analysis:
        coverage = (
            (self.SILVER_WEIGHT if silver is not None else 0)
            + (self.DOLLAR_WEIGHT if dollar is not None else 0)
        )

        silver_score = self._component_score(primary, silver)
        dollar_score = self._component_score(
            primary, dollar, inverse=True
        )

        if primary == Trend.NEUTRAL:
            score = None
            state = IntermarketV2State.UNAVAILABLE
            reason = "Primary trend neutral: no directional reference"
        elif coverage == 0:
            score = None
            state = IntermarketV2State.UNAVAILABLE
            reason = "No intermarket confirmation data available"
        else:
            weighted_sum = (
                (silver_score or 0) * self.SILVER_WEIGHT
                + (dollar_score or 0) * self.DOLLAR_WEIGHT
            )
            score = round(weighted_sum / coverage)

            available_scores = [
                value
                for value in (silver_score, dollar_score)
                if value is not None
            ]

            if all(value == 100 for value in available_scores):
                state = IntermarketV2State.CONFIRMED
            elif all(value == 0 for value in available_scores):
                state = IntermarketV2State.DIVERGENT
            else:
                state = IntermarketV2State.MIXED

            reason = (
                "Silver direct / dollar inverse confirmation; "
                f"coverage {coverage}%"
            )

        return IntermarketV2Analysis(
            state=state,
            score=score,
            primary_trend=primary,
            silver_trend=silver,
            dollar_trend=dollar,
            silver_score=silver_score,
            dollar_score=dollar_score,
            coverage=coverage,
            reason=reason,
        )