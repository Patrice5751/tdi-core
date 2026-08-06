from tdi.advisor.rule_category import RuleCategory
from tdi.advisor.rule_result import RuleResult
from tdi.reporting.recommendation_rule_engine import RecommendationRuleEngine


def test_risk_reward_rule():

    result = RuleResult(
        category=RuleCategory.RISK,
        rule="RiskReward",
        score=0,
        max_score=15,
        passed=False,
        message="Risk/Reward too low.",
    )

    recommendation = RecommendationRuleEngine.build(result)

    assert recommendation == (
        "⚠ Trade not recommended until risk/reward improves."
    )


def test_risk_rule():

    result = RuleResult(
        category=RuleCategory.RISK,
        rule="Risk",
        score=0,
        max_score=15,
        passed=False,
        message="Risk exceeds limit.",
    )

    recommendation = RecommendationRuleEngine.build(result)

    assert recommendation == (
        "⚠ Reduce position size before entering."
    )


def test_unknown_rule():

    result = RuleResult(
        category=RuleCategory.STRUCTURE,
        rule="Trend",
        score=20,
        max_score=20,
        passed=True,
        message="Strong trend.",
    )

    recommendation = RecommendationRuleEngine.build(result)

    assert recommendation is None