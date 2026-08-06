from tdi.reporting.recommendation_rules.risk_reward_recommendation_rule import (
    RiskRewardRecommendationRule,
)
from tdi.reporting.recommendation_rules.risk_recommendation_rule import (
    RiskRecommendationRule,
)


class RecommendationRuleEngine:

    @staticmethod
    def build(result):
        for rule in (
            RiskRewardRecommendationRule,
            RiskRecommendationRule,
        ):
            recommendation = rule.build(result)

            if recommendation is not None:
                return recommendation

        return None