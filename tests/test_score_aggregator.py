
from tdi.advisor.rule_category import RuleCategory
from tdi.advisor.rule_result import RuleResult
from tdi.advisor.score_aggregator import ScoreAggregator


def test_compute_score():
    results = [
        RuleResult(
            category=RuleCategory.STRUCTURE,
            rule="Trend",
            score=20,
            max_score=20,
            passed=True,
            message="Trend",
        ),
        RuleResult(
            category=RuleCategory.STRUCTURE,
            rule="Structure",
            score=20,
            max_score=20,
            passed=True,
            message="Structure",
        ),
        RuleResult(
            category=RuleCategory.RISK,
            rule="RiskReward",
            score=15,
            max_score=15,
            passed=True,
            message="RR",
        ),
    ]

    assert ScoreAggregator.compute(results) == 55


def test_strengths():
    results = [
        RuleResult(
            category=RuleCategory.STRUCTURE,
            rule="Trend",
            score=20,
            max_score=20,
            passed=True,
            message="Trend OK",
        ),
        RuleResult(
            category=RuleCategory.RISK,
            rule="RiskReward",
            score=0,
            max_score=15,
            passed=False,
            message="RR faible",
        ),
    ]

    assert ScoreAggregator.strengths(results) == ["Trend OK"]


def test_weaknesses():
    results = [
        RuleResult(
            category=RuleCategory.STRUCTURE,
            rule="Trend",
            score=20,
            max_score=20,
            passed=True,
            message="Trend OK",
        ),
        RuleResult(
            category=RuleCategory.RISK,
            rule="RiskReward",
            score=0,
            max_score=15,
            passed=False,
            message="RR faible",
        ),
    ]

    assert ScoreAggregator.weaknesses(results) == ["RR faible"]

def test_max_score():
    results = [
        RuleResult(
            category=RuleCategory.STRUCTURE,
            rule="Trend",
            score=16,
            max_score=20,
            passed=True,
            message="Trend",
        ),
        RuleResult(
            category=RuleCategory.RISK,
            rule="ATR",
            score=10,
            max_score=10,
            passed=True,
            message="ATR",
        ),
    ]

    assert ScoreAggregator.max_score(results) == 30

def test_normalized_score():
    results = [
        RuleResult(
            category=RuleCategory.STRUCTURE,
            rule="Trend",
            score=16,
            max_score=20,
            passed=True,
            message="Trend",
        ),
        RuleResult(
            category=RuleCategory.RISK,
            rule="ATR",
            score=8,
            max_score=10,
            passed=True,
            message="ATR",
        ),
    ]

    assert ScoreAggregator.normalized_score(results) == 80

def test_normalized_score_with_empty_results():
    assert ScoreAggregator.normalized_score([]) == 0


def test_score_by_category():
    results = [
        RuleResult(
            category=RuleCategory.STRUCTURE,
            rule="Trend",
            score=16,
            max_score=20,
            passed=True,
            message="Trend",
        ),
        RuleResult(
            category=RuleCategory.STRUCTURE,
            rule="Structure",
            score=12,
            max_score=15,
            passed=True,
            message="Structure",
        ),
        RuleResult(
            category=RuleCategory.RISK,
            rule="ATR",
            score=10,
            max_score=10,
            passed=True,
            message="ATR",
        ),
    ]

    scores = ScoreAggregator.score_by_category(results)

    assert scores[RuleCategory.STRUCTURE] == {
        "score": 28,
        "max_score": 35,
    }

    assert scores[RuleCategory.RISK] == {
        "score": 10,
        "max_score": 10,
    }