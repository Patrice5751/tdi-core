from tdi.reporting.explanation import Explanation


def test_create_explanation():
    explanation = Explanation(
        title="Trend",
        value=20,
        message="Strong trend detected.",
    )

    assert explanation.title == "Trend"
    assert explanation.value == 20
    assert explanation.message == "Strong trend detected."