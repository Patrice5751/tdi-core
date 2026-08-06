from types import SimpleNamespace

from tdi.engines.trade_advisor import TradeAdvisor
from tdi.models.trade import Side


def make_trade(
    *,
    side=Side.SELL,
    entry=4050.0,
    atr=30.0,
):
    return SimpleNamespace(
        side=side,
        entry=entry,
        atr=atr,
    )


def make_analysis(
    *,
    trend_confidence=90.0,
    momentum_confidence=90.0,
    support=3970.0,
    resistance=4050.0,
):
    return SimpleNamespace(
        trend=SimpleNamespace(
            confidence=trend_confidence,
        ),
        momentum=SimpleNamespace(
            confidence=momentum_confidence,
        ),
        structure=SimpleNamespace(
            support=support,
            resistance=resistance,
        ),
    )


def make_validation(
    *,
    trend_ok=True,
    momentum_ok=True,
    structure_ok=True,
    rr_ok=True,
    risk_ok=True,
    atr_ok=True,
):
    return SimpleNamespace(
        trend_ok=trend_ok,
        momentum_ok=momentum_ok,
        structure_ok=structure_ok,
        rr_ok=rr_ok,
        risk_ok=risk_ok,
        atr_ok=atr_ok,
    )


def make_decision(
    *,
    score=90,
    accepted=True,
):
    return SimpleNamespace(
        score=score,
        accepted=accepted,
    )


def make_risk(
    *,
    rr=3.0,
):
    return SimpleNamespace(
        rr=rr,
    )


def test_excellent_trade():
    advisor = TradeAdvisor()

    result = advisor.advise(
        trade=make_trade(),
        analysis=make_analysis(),
        validation=make_validation(),
        decision=make_decision(score=92),
        risk=make_risk(rr=3.2),
    )

    assert result.summary == "Le trade est valide selon les règles TDI."
    assert result.estimated_score == 92

    assert any(
        "résistance" in msg.lower()
        for msg in result.strengths
    )


def test_invalid_structure():
    advisor = TradeAdvisor()

    result = advisor.advise(
        trade=make_trade(entry=4000),
        analysis=make_analysis(
            support=3970,
            resistance=4050,
        ),
        validation=make_validation(structure_ok=False),
        decision=make_decision(
            score=70,
            accepted=False,
        ),
        risk=make_risk(),
    )

    assert result.recommendation == (
        "Attendre une meilleure zone d'entrée."
    )

    assert any(
        "pullback" in msg.lower()
        for msg in result.improvements
    )


def test_low_rr():
    advisor = TradeAdvisor()

    result = advisor.advise(
        trade=make_trade(),
        analysis=make_analysis(),
        validation=make_validation(rr_ok=False),
        decision=make_decision(
            score=65,
            accepted=False,
        ),
        risk=make_risk(rr=1.4),
    )

    assert any(
        "1.40" in msg
        for msg in result.improvements
    )


def test_estimated_score_never_exceeds_100():
    advisor = TradeAdvisor()

    result = advisor.advise(
        trade=make_trade(entry=4000),
        analysis=make_analysis(),
        validation=make_validation(
            trend_ok=False,
            momentum_ok=False,
            structure_ok=False,
            rr_ok=False,
            risk_ok=False,
            atr_ok=False,
        ),
        decision=make_decision(
            score=96,
            accepted=False,
        ),
        risk=make_risk(rr=1.0),
    )

    assert result.estimated_score == 100