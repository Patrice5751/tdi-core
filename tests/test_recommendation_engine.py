from tdi.advisor.rule_category import RuleCategory
from tdi.advisor.rule_result import RuleResult
from tdi.reporting.recommendation_engine import RecommendationEngine


def test_build_recommendations():
    results = [
        RuleResult(
            category=RuleCategory.STRUCTURE,
            rule="Trend",
            score=20,
            max_score=20,
            passed=True,
            message="Strong trend.",
        ),
        RuleResult(
            category=RuleCategory.RISK,
            rule="RiskReward",
            score=0,
            max_score=15,
            passed=False,
            message="Risk/Reward is too low.",
        ),
    ]

    recommendations = RecommendationEngine.build(results)

    assert recommendations == [
    "⚠ Trade not recommended until risk/reward improves.",
    "✓ Strong trend.",
    ]

def test_risk_reward_priority():
    results = [
        RuleResult(
            category=RuleCategory.RISK,
            rule="RiskReward",
            score=0,
            max_score=15,
            passed=False,
            message="Risk/Reward is too low.",
        )
    ]

    recommendations = RecommendationEngine.build(results)

    assert recommendations == [
        "⚠ Trade not recommended until risk/reward improves."
    ]

def test_risk_priority():
    results = [
        RuleResult(
            category=RuleCategory.RISK,
            rule="Risk",
            score=0,
            max_score=15,
            passed=False,
            message="Risk exceeds limit.",
        )
    ]

    recommendations = RecommendationEngine.build(results)

    assert recommendations == [
        "⚠ Reduce position size before entering."
    ]