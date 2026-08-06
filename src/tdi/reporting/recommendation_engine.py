from tdi.advisor.rule_category import RuleCategory
from tdi.reporting.recommendation_rule_engine import RecommendationRuleEngine


class RecommendationEngine:

    @staticmethod
    def build(rule_results):
        recommendations = []

        for result in rule_results:
            recommendation = RecommendationRuleEngine.build(result)

            if recommendation is not None:
                recommendations.append(recommendation)

        # Recommandations classiques
        for result in rule_results:
            if result.passed:
                recommendations.append(f"✓ {result.message}")
            elif result.rule not in ("RiskReward", "Risk"):
                recommendations.append(f"⚠ {result.message}")

        return recommendations