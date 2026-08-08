from types import SimpleNamespace

from tdi.analysis.recommendation import Recommendation
from tdi.engines.decision_engine import DecisionEngine
from tdi.graphical.graphical_decision import GraphicalDecision
from tdi.graphical.graphical_decision_analysis import (
    GraphicalDecisionAnalysis,
)


def make_analysis(
    trend_confidence: int = 80,
):
    return SimpleNamespace(
        trend=SimpleNamespace(
            confidence=trend_confidence,
        )
    )


def make_validation(
    score: int = 80,
    valid: bool = True,
):
    return SimpleNamespace(
        score=score,
        valid=valid,
        trend_ok=True,
        momentum_ok=True,
        structure_ok=True,
        rr_ok=True,
    )


def make_risk(
    rr: float = 2.0,
):
    return SimpleNamespace(
        rr=rr,
    )


def make_graphical_decision(
    decision: GraphicalDecision,
    reason: str = "Test graphique",
):
    return GraphicalDecisionAnalysis(
        decision=decision,
        confidence=90,
        reason=reason,
    )


def test_decision_without_graphical_context_keeps_legacy_behaviour():
    engine = DecisionEngine()

    result = engine.decide(
        analysis=make_analysis(),
        validation=make_validation(),
        risk=make_risk(),
    )

    assert result.accepted is True
    assert result.score == 80


def test_graphical_go_keeps_normal_decision():
    engine = DecisionEngine()

    legacy = engine.decide(
        analysis=make_analysis(),
        validation=make_validation(),
        risk=make_risk(),
    )

    graphical = engine.decide(
        analysis=make_analysis(),
        validation=make_validation(),
        risk=make_risk(),
        graphical_decision=make_graphical_decision(
            GraphicalDecision.GO,
        ),
    )

    assert graphical.score == legacy.score
    assert graphical.recommendation == legacy.recommendation
    assert graphical.accepted == legacy.accepted


def test_graphical_wait_forces_wait_and_blocks_entry():
    engine = DecisionEngine()

    result = engine.decide(
        analysis=make_analysis(),
        validation=make_validation(
            score=95,
            valid=True,
        ),
        risk=make_risk(rr=3.0),
        graphical_decision=make_graphical_decision(
            GraphicalDecision.WAIT,
            reason="Prix en extension",
        ),
    )

    assert result.recommendation == Recommendation.WAIT
    assert result.accepted is False
    assert any(
        "Prix en extension" in weakness
        for weakness in result.weaknesses
    )


def test_graphical_no_go_forces_reject_and_blocks_entry():
    engine = DecisionEngine()

    result = engine.decide(
        analysis=make_analysis(),
        validation=make_validation(
            score=95,
            valid=True,
        ),
        risk=make_risk(rr=3.0),
        graphical_decision=make_graphical_decision(
            GraphicalDecision.NO_GO,
            reason="Direction opposée",
        ),
    )

    assert result.recommendation == Recommendation.REJECT
    assert result.accepted is False
    assert any(
        "Direction opposée" in weakness
        for weakness in result.weaknesses
    )
    