from tdi.advisor.trend_rule import TrendRule


def test_excellent_trend():
    result = TrendRule.evaluate(95)

    assert result.score == 20
    assert result.passed


def test_good_trend():
    result = TrendRule.evaluate(85)

    assert result.score == 16
    assert result.passed


def test_average_trend():
    result = TrendRule.evaluate(75)

    assert result.score == 12
    assert result.passed


def test_weak_trend():
    result = TrendRule.evaluate(65)

    assert result.score == 8
    assert result.passed


def test_bad_trend():
    result = TrendRule.evaluate(45)

    assert result.score == 0
    assert not result.passed