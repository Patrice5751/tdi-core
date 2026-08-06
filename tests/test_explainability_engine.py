from tdi.advisor.rule_category import RuleCategory
from tdi.advisor.rule_result import RuleResult
from tdi.reporting.explainability_engine import ExplainabilityEngine


def test_build_explanations():
    results = [
        RuleResult(
            category=RuleCategory.STRUCTURE,
            rule="Trend",
            score=20,
            max_score=20,
            passed=True,
            message="Strong trend.",
        )
    ]

    explanations = ExplainabilityEngine.build(results)

    assert len(explanations) == 1
    assert explanations[0].title == "Trend"
    assert explanations[0].value == 20
    assert explanations[0].message == "Strong trend."