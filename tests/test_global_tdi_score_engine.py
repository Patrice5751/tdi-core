from tdi.graphical.global_tdi_score_engine import GlobalTDIScoreEngine


def test_global_score_all_components_at_100():
    result = GlobalTDIScoreEngine().compute(
        bias_score=100,
        structure_score=100,
        momentum_score=100,
        location_score=100,
        bias_available=True,
        structure_aligned=True,
        timing_favorable=True,
        momentum_confirmed=True,
    )

    assert result.score == 100
    assert result.grade == "A"


def test_global_score_uses_expected_weights():
    result = GlobalTDIScoreEngine().compute(
        bias_score=80,
        structure_score=70,
        momentum_score=60,
        location_score=90,
        bias_available=True,
        structure_aligned=True,
        timing_favorable=True,
        momentum_confirmed=True,
    )

    # 80*0.25 + 70*0.30 + 60*0.20 + 90*0.25
    # = 20 + 21 + 12 + 22.5 = 75.5 -> 76
    assert result.score == 76
    assert result.grade == "C"


def test_global_score_is_capped_when_no_bias_is_available():
    result = GlobalTDIScoreEngine().compute(
        bias_score=100,
        structure_score=100,
        momentum_score=100,
        location_score=100,
        bias_available=False,
        structure_aligned=True,
        timing_favorable=True,
        momentum_confirmed=True,
    )

    assert result.score == 25
    assert result.grade == "E"


def test_global_score_is_capped_when_structure_is_not_aligned():
    result = GlobalTDIScoreEngine().compute(
        bias_score=100,
        structure_score=100,
        momentum_score=100,
        location_score=100,
        bias_available=True,
        structure_aligned=False,
        timing_favorable=True,
        momentum_confirmed=True,
    )

    assert result.score == 69
    assert result.grade == "D"


def test_global_score_is_capped_when_timing_is_not_favorable():
    result = GlobalTDIScoreEngine().compute(
        bias_score=100,
        structure_score=100,
        momentum_score=100,
        location_score=100,
        bias_available=True,
        structure_aligned=True,
        timing_favorable=False,
        momentum_confirmed=True,
    )

    assert result.score == 79
    assert result.grade == "C"


def test_global_score_is_capped_when_momentum_is_not_confirmed():
    result = GlobalTDIScoreEngine().compute(
        bias_score=100,
        structure_score=100,
        momentum_score=100,
        location_score=100,
        bias_available=True,
        structure_aligned=True,
        timing_favorable=True,
        momentum_confirmed=False,
    )

    assert result.score == 89
    assert result.grade == "B"
