from types import SimpleNamespace

from tdi.advisor.rule_engine import RuleEngine
from tdi.models.trade import Side


def make_trade():
    return SimpleNamespace(
        side=Side.BUY,
        entry=4000.0,
        atr=25.0,
    )


def make_analysis():
    return SimpleNamespace(
        trend=SimpleNamespace(confidence=90),
        momentum=SimpleNamespace(confidence=85),
        structure=SimpleNamespace(
            support=3975.0,
            resistance=4050.0,
        ),
    )


def make_validation():
    return SimpleNamespace(
        risk_ok=True,
        atr_ok=True,
    )


def make_risk():
    return SimpleNamespace(
        rr=2.5,
    )


def test_rule_engine_returns_all_rules():
    results = RuleEngine.evaluate(
        trade=make_trade(),
        analysis=make_analysis(),
        validation=make_validation(),
        risk=make_risk(),
    )

    assert len(results) == 6


def test_rule_engine_rule_names():
    results = RuleEngine.evaluate(
        trade=make_trade(),
        analysis=make_analysis(),
        validation=make_validation(),
        risk=make_risk(),
    )

    names = [r.rule for r in results]

    assert names == [
    "Trend",
    "Momentum",
    "Structure",
    "RiskReward",
    "Risk",
    "ATR",
]