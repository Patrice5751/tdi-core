from tdi.scoring.score_breakdown import ScoreBreakdown


def test_total_score():

    breakdown = ScoreBreakdown(
        trend=20,
        structure=20,
        momentum=15,
        alignment=15,
        rr=15,
        atr=10,
        risk=5,
    )

    assert breakdown.total == 100