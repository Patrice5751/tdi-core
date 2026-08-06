from tdi.reporting.confidence import Confidence
from tdi.reporting.decision import Decision
from tdi.reporting.decision_summary import DecisionSummary
from tdi.reporting.verdict_engine import VerdictEngine
from tdi.reporting.confluence_observation import ConfluenceObservation
from tdi.reporting.severity import Severity


def test_build_verdict():
    summary = DecisionSummary(
        decision=Decision.BUY,
        confidence=Confidence.MEDIUM,
    )

    lines = VerdictEngine.build(summary)

    assert lines[0] == "FINAL VERDICT"
    assert "BUY" in lines[2]
    assert "MEDIUM" in lines[3]

    from tdi.reporting.confluence_observation import ConfluenceObservation
    from tdi.reporting.severity import Severity


def test_build_verdict_with_reasons():
    summary = DecisionSummary(
        decision=Decision.BUY,
        confidence=Confidence.MEDIUM,
    )

    observations = [
        ConfluenceObservation(
            severity=Severity.INFO,
            title="High Conviction",
            message="Trend and momentum are aligned.",
        ),
        ConfluenceObservation(
            severity=Severity.WARNING,
            title="Momentum",
            message="Momentum confirmation is missing.",
        ),
    ]

    lines = VerdictEngine.build(summary, observations)

    report = "\n".join(lines)

    assert "Reasons" in report
    assert "Trend and momentum are aligned." in report
    assert "Warnings" in report
    assert "Momentum confirmation is missing." in report

def test_build_verdict_with_setup_quality():
    summary = DecisionSummary(
        decision=Decision.BUY,
        confidence=Confidence.MEDIUM,
    )

    lines = VerdictEngine.build(
        summary,
        normalized_score=85,
    )

    report = "\n".join(lines)
    
    assert "Setup Quality : A" in report

def test_build_verdict_with_trade_assessment():
    summary = DecisionSummary(
        decision=Decision.BUY,
        confidence=Confidence.MEDIUM,
    )

    lines = VerdictEngine.build(
        summary,
        normalized_score=85,
    )

    report = "\n".join(lines)

    assert "Assessment : VERY GOOD" in report

    def test_build_verdict_with_trade_assessment():
        summary = DecisionSummary(
        decision=Decision.BUY,
        confidence=Confidence.MEDIUM,
    )

    lines = VerdictEngine.build(
        summary,
        normalized_score=85,
    )

    report = "\n".join(lines)

    assert "Assessment : VERY GOOD" in report