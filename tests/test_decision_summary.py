from tdi.reporting.decision_summary import DecisionSummary
from tdi.reporting.decision import Decision
from tdi.reporting.confidence import Confidence


def test_strong_buy():
    summary = DecisionSummary.from_score(95)

    assert summary.decision is Decision.STRONG_BUY
    assert summary.confidence is Confidence.HIGH


def test_buy():
    summary = DecisionSummary.from_score(80)

    assert summary.decision is Decision.BUY
    assert summary.confidence is Confidence.MEDIUM


def test_buy_with_caution():
    summary = DecisionSummary.from_score(65)

    assert summary.decision is Decision.BUY_WITH_CAUTION
    assert summary.confidence is Confidence.LOW


def test_no_trade():
    summary = DecisionSummary.from_score(40)

    assert summary.decision is Decision.NO_TRADE
    assert summary.confidence is Confidence.VERY_LOW