from tdi.analysis.risk_result import RiskResult
from tdi.specifications.minimum_rr import MinimumRRSpecification


def test_rr_above_minimum():
    risk = RiskResult(
        stop_distance=100.0,
        target_distance=250.0,
        rr=2.5,
        risk_amount=200,
        position_size=0.10,
        valid=True,
        reasons=[],
    )

    assert MinimumRRSpecification().is_satisfied_by(risk)


def test_rr_below_minimum():
    risk = RiskResult(
        stop_distance=100.0,
        target_distance=120.0,
        rr=1.2,
        risk_amount=200,
        position_size=0.10,
        valid=True,
        reasons=[],
    )

    assert not MinimumRRSpecification().is_satisfied_by(risk)