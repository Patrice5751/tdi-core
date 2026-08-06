class RiskRecommendationRule:

    @staticmethod
    def build(result):
        if (
            result.rule == "Risk"
            and not result.passed
        ):
            return (
                "⚠ Reduce position size "
                "before entering."
            )

        return None