from tdi.advisor.momentum_rule import MomentumRule


def test_excellent_momentum():
    result = MomentumRule.evaluate(95)

    assert result.score == 20
    assert result.passed


def test_good_momentum():
    result = MomentumRule.evaluate(85)

    assert result.score == 16
    assert result.passed


def test_average_momentum():
    result = MomentumRule.evaluate(75)

    assert result.score == 12
    assert result.passed


def test_weak_momentum():
    result = MomentumRule.evaluate(65)

    assert result.score == 8
    assert result.passed


def test_bad_momentum():
    result = MomentumRule.evaluate(45)

    assert result.score == 0
    assert not result.passed