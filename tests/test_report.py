from tdi.reporting.report import Report


def test_report_as_text():
    report = Report(
        [
            "Hello",
            "World",
        ]
    )

    assert report.as_text() == (
        "Hello\n"
        "World"
    )