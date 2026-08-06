from tdi.advisor.structure_rule import StructureRule
from tdi.models.trade import Side


def test_excellent_buy_structure():
    result = StructureRule.evaluate(
        side=Side.BUY,
        entry=100,
        support=95,
        resistance=120,
        atr=20,
    )

    assert result.passed is True
    assert result.score == 10


def test_good_buy_structure():
    result = StructureRule.evaluate(
        side=Side.BUY,
        entry=100,
        support=92,
        resistance=120,
        atr=20,
    )

    assert result.passed is True
    assert result.score == 5


def test_average_buy_structure():
    result = StructureRule.evaluate(
        side=Side.BUY,
        entry=100,
        support=84,
        resistance=120,
        atr=20,
    )

    assert result.passed is True
    assert result.score == 0


def test_bad_buy_structure():
    result = StructureRule.evaluate(
        side=Side.BUY,
        entry=100,
        support=70,
        resistance=120,
        atr=20,
    )

    assert result.passed is False
    assert result.score == -5