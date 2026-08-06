class RiskRewardRecommendationRule:

    @staticmethod
    def build(result):
        if (
            result.rule == "RiskReward"
            and not result.passed
        ):
            return (
                "⚠ Trade not recommended "
                "until risk/reward improves."
            )

        return None