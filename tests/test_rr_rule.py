from tdi.advisor.rr_rule import RRRule


def test_rr_below_minimum():
    result = RRRule.evaluate(
        rr=1.4,
        minimum_rr=1.5,
    )

    assert result.score == 0
    assert not result.passed
    assert "insuffisant" in result.message.lower()


def test_rr_acceptable():
    result = RRRule.evaluate(1.8)

    assert result.score == 5
    assert result.passed
    assert "acceptable" in result.message.lower()


def test_rr_good():
    result = RRRule.evaluate(2.2)

    assert result.score == 10
    assert result.passed
    assert "bon ratio" in result.message.lower()


def test_rr_very_good():
    result = RRRule.evaluate(2.7)

    assert result.score == 13
    assert result.passed
    assert "très bon" in result.message.lower()


def test_rr_excellent():
    result = RRRule.evaluate(3.2)

    assert result.score == 15
    assert result.passed
    assert "excellent" in result.message.lower()


def test_rr_exactly_at_minimum():
    result = RRRule.evaluate(
        rr=1.5,
        minimum_rr=1.5,
    )

    assert result.score == 5
    assert result.passed


def test_rr_exactly_at_two():
    result = RRRule.evaluate(2.0)

    assert result.score == 10
    assert result.passed


def test_rr_exactly_at_three():
    result = RRRule.evaluate(3.0)

    assert result.score == 15
    assert result.passed