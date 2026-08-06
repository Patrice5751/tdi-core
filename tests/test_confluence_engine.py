from tdi.advisor.rule_category import RuleCategory
from tdi.advisor.rule_result import RuleResult
from tdi.reporting.confluence_engine import ConfluenceEngine
from tdi.reporting.confluence_observation import ConfluenceObservation
from tdi.reporting.severity import Severity

def test_high_conviction():

    results = [
        RuleResult(
            RuleCategory.STRUCTURE,
            "Trend",
            20,
            20,
            True,
            "",
        ),
        RuleResult(
            RuleCategory.CONFLUENCE,
            "Momentum",
            20,
            20,
            True,
            "",
        ),
        RuleResult(
            RuleCategory.STRUCTURE,
            "Structure",
            20,
            20,
            True,
            "",
        ),
        RuleResult(
            RuleCategory.RISK,
            "RiskReward",
            15,
            15,
            True,
            "",
        ),
    ]

    observations = ConfluenceEngine.build(results)

    assert observations == [
        ConfluenceObservation(
            severity=Severity.INFO,
            title="High Conviction",
            message="Trend, momentum, structure and risk/reward are aligned.",
        )
    ]

def test_missing_momentum_confirmation():
    results = [
        RuleResult(
            RuleCategory.STRUCTURE,
            "Trend",
            20,
            20,
            True,
            "",
        ),
        RuleResult(
            RuleCategory.CONFLUENCE,
            "Momentum",
            0,
            20,
            False,
            "",
        ),
        RuleResult(
            RuleCategory.STRUCTURE,
            "Structure",
            20,
            20,
            True,
            "",
        ),
    ]

    observations = ConfluenceEngine.build(results)

    assert observations == [
        ConfluenceObservation(
            severity=Severity.WARNING,
            title="Missing Momentum",
            message="Trend is valid but momentum confirmation is missing.",
        )
    ]

def test_technically_valid_but_poor_risk_reward():
    results = [
        RuleResult(
            RuleCategory.STRUCTURE,
            "Trend",
            20,
            20,
            True,
            "",
        ),
        RuleResult(
            RuleCategory.CONFLUENCE,
            "Momentum",
            20,
            20,
            True,
            "",
        ),
        RuleResult(
            RuleCategory.STRUCTURE,
            "Structure",
            20,
            20,
            True,
            "",
        ),
        RuleResult(
            RuleCategory.RISK,
            "RiskReward",
            0,
            15,
            False,
            "",
        ),
    ]

    observations = ConfluenceEngine.build(results)

    assert observations == [
        ConfluenceObservation(
            severity=Severity.CRITICAL,
            title="Poor Risk/Reward",
            message=(
                "Technically valid setup, but not tradable "
                "due to poor risk/reward."
            ),
        )
    ]


