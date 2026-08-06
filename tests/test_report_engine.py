from unittest.mock import patch

from tdi.advisor.rule_category import RuleCategory
from tdi.advisor.rule_result import RuleResult
from tdi.reporting.report_engine import ReportEngine
from tdi.reporting.confluence_engine import ConfluenceEngine
from tdi.reporting.report import Report
from unittest.mock import patch


def test_build_global_report():
    results = [
        RuleResult(
            category=RuleCategory.STRUCTURE,
            rule="Trend",
            score=16,
            max_score=20,
            passed=True,
            message="Tendance forte.",
        ),
        RuleResult(
            category=RuleCategory.RISK,
            rule="ATR",
            score=10,
            max_score=10,
            passed=True,
            message="ATR conforme.",
        ),
    ]

    report = ReportEngine.build(results)
    text = report.as_text()

    assert "TDI TRADE ANALYSIS" in text
    assert "Score: 26/30" in text
    assert "Normalized: 87/100" in text

def test_build_structure_section():
    results = [
        RuleResult(
            category=RuleCategory.STRUCTURE,
            rule="Trend",
            score=16,
            max_score=20,
            passed=True,
            message="Tendance forte.",
        ),
        RuleResult(
            category=RuleCategory.STRUCTURE,
            rule="Momentum",
            score=12,
            max_score=20,
            passed=True,
            message="Momentum correct.",
        ),
        RuleResult(
            category=RuleCategory.RISK,
            rule="ATR",
            score=10,
            max_score=10,
            passed=True,
            message="ATR conforme.",
        ),
    ]

    report = ReportEngine.build(results)
    text = report.as_text()

    assert "STRUCTURE" in text
    assert "Trend" in text
    assert "16/20" in text
    assert "Momentum" in text
    assert "12/20" in text
    assert "✔ Trend" in text
    assert "TOTAL STRUCTURE: 28/40" in text

def test_build_risk_section():
    results = [
        RuleResult(
            category=RuleCategory.RISK,
            rule="RiskReward",
            score=10,
            max_score=15,
            passed=True,
            message="Ratio risque/rendement correct.",
        ),
        RuleResult(
            category=RuleCategory.RISK,
            rule="Risk",
            score=15,
            max_score=15,
            passed=True,
            message="Risque conforme.",
        ),
        RuleResult(
            category=RuleCategory.STRUCTURE,
            rule="Trend",
            score=16,
            max_score=20,
            passed=True,
            message="Tendance forte.",
        ),
    ]

    report = ReportEngine.build(results)
    text = report.as_text()
    
    assert "RISK" in text
    assert "RiskReward" in text
    assert "10/15" in text
    assert "Risk" in text
    assert "15/15" in text
    assert "✔ Risk" in text
    assert "TOTAL RISK: 25/30" in text

def test_build_confluence_section():
    results = [
        RuleResult(
            category=RuleCategory.CONFLUENCE,
            rule="MultiTimeframe",
            score=8,
            max_score=10,
            passed=True,
            message="Confluence multi-timeframe correcte.",
        ),
        RuleResult(
            category=RuleCategory.CONFLUENCE,
            rule="Confirmation",
            score=5,
            max_score=10,
            passed=True,
            message="Confirmation présente.",
        ),
        RuleResult(
            category=RuleCategory.RISK,
            rule="ATR",
            score=10,
            max_score=10,
            passed=True,
            message="ATR conforme.",
        ),
    ]

    report = ReportEngine.build(results)
    text = report.as_text()

    assert "CONFLUENCE" in text
    assert "MultiTimeframe" in text
    assert "8/10" in text
    assert "Confirmation" in text
    assert "5/10" in text
    assert "✔ MultiTimeframe" in text
    assert "TOTAL CONFLUENCE: 13/20" in text

def test_build_insights_section():
    results = [
        RuleResult(
            category=RuleCategory.STRUCTURE,
            rule="Trend",
            score=16,
            max_score=20,
            passed=True,
            message="Tendance forte.",
        ),
        RuleResult(
            category=RuleCategory.STRUCTURE,
            rule="Structure",
            score=5,
            max_score=15,
            passed=False,
            message="Structure de marché faible.",
        ),
    ]

    report = ReportEngine.build(results)
    text = report.as_text()

    assert "STRENGTHS" in text
    assert "• Tendance forte." in text
    assert "WEAKNESSES" in text
    assert "• Structure de marché faible." in text

def test_build_confluence_observations_section():
    results = [
        RuleResult(
            category=RuleCategory.STRUCTURE,
            rule="Trend",
            score=20,
            max_score=20,
            passed=True,
            message="Tendance forte.",
        ),
        RuleResult(
            category=RuleCategory.CONFLUENCE,
            rule="Momentum",
            score=20,
            max_score=20,
            passed=True,
            message="Momentum confirmé.",
        ),
        RuleResult(
            category=RuleCategory.STRUCTURE,
            rule="Structure",
            score=20,
            max_score=20,
            passed=True,
            message="Structure valide.",
        ),
        RuleResult(
            category=RuleCategory.RISK,
            rule="RiskReward",
            score=15,
            max_score=15,
            passed=True,
            message="Ratio conforme.",
        ),
    ]

    report = ReportEngine.build(results)
    text = report.as_text()

    assert "CONFLUENCE OBSERVATIONS" in text
    assert "ℹ High Conviction" in text
    assert (
        "Trend, momentum, structure and risk/reward are aligned."
        in text
    )

def test_confluence_engine_called_once():
    results = [
        RuleResult(
            category=RuleCategory.STRUCTURE,
            rule="Trend",
            score=20,
            max_score=20,
            passed=True,
            message="Tendance forte.",
        ),
        RuleResult(
            category=RuleCategory.CONFLUENCE,
            rule="Momentum",
            score=20,
            max_score=20,
            passed=True,
            message="Momentum confirmé.",
        ),
        RuleResult(
            category=RuleCategory.STRUCTURE,
            rule="Structure",
            score=20,
            max_score=20,
            passed=True,
            message="Structure valide.",
        ),
        RuleResult(
            category=RuleCategory.RISK,
            rule="RiskReward",
            score=15,
            max_score=15,
            passed=True,
            message="Ratio conforme.",
        ),
    ]

    with patch.object(
        ConfluenceEngine,
        "build",
        wraps=ConfluenceEngine.build,
    ) as mocked_build:
        ReportEngine.build(results)

    mocked_build.assert_called_once_with(results)

def test_build_final_verdict_section():
    results = [
        RuleResult(
            category=RuleCategory.STRUCTURE,
            rule="Trend",
            score=16,
            max_score=20,
            passed=True,
            message="Tendance forte.",
        ),
        RuleResult(
            category=RuleCategory.RISK,
            rule="Risk",
            score=10,
            max_score=10,
            passed=True,
            message="Risque conforme.",
        ),
    ]

    report = ReportEngine.build(results)
    text = report.as_text()

    assert "FINAL VERDICT" in text
    assert "Decision : BUY" in text
    assert "Confidence : MEDIUM" in text

    from tdi.reporting.report import Report


def test_build_returns_report():
    report = ReportEngine.build([])

    assert isinstance(report, Report)
    