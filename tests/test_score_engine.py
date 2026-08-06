from tdi.scoring.grade import Grade
from tdi.scoring.score_breakdown import ScoreBreakdown
from tdi.scoring.score_engine import ScoreEngine


def make_breakdown(score):

    return ScoreBreakdown(
        trend=score,
        structure=0,
        momentum=0,
        alignment=0,
        rr=0,
        atr=0,
        risk=0,
    )


def test_grade_A():

    result = ScoreEngine().compute(make_breakdown(95))

    assert result.grade == Grade.A


def test_grade_B():

    result = ScoreEngine().compute(make_breakdown(84))

    assert result.grade == Grade.B


def test_grade_C():

    result = ScoreEngine().compute(make_breakdown(75))

    assert result.grade == Grade.C


def test_grade_D():

    result = ScoreEngine().compute(make_breakdown(66))

    assert result.grade == Grade.D


def test_grade_E():

    result = ScoreEngine().compute(make_breakdown(45))

    assert result.grade == Grade.E