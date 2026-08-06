from tdi.reporting.setup_quality import SetupQuality

def test_setup_quality_from_score():
    assert SetupQuality.from_score(95) is SetupQuality.A_PLUS
    assert SetupQuality.from_score(85) is SetupQuality.A
    assert SetupQuality.from_score(75) is SetupQuality.B
    assert SetupQuality.from_score(65) is SetupQuality.C
    assert SetupQuality.from_score(40) is SetupQuality.D