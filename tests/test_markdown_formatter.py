from tdi.reporting.report import Report


def test_report_as_markdown():
    report = Report(
        [
            "Line 1",
            "Line 2",
        ]
    )

    markdown = report.as_markdown()

    assert markdown == (
        "Line 1\n"
        "Line 2"
    )