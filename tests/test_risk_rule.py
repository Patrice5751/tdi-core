from tdi.advisor.risk_rule import RiskRule


def test_valid_risk():
    result = RiskRule.evaluate(True)

    assert result.passed
    assert result.score == 15
    assert "conforme" in result.message.lower()


def test_invalid_risk():
    result = RiskRule.evaluate(False)

    assert not result.passed
    assert result.score == 0
    assert "réduire" in result.message.lower()