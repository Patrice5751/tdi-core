from tdi.reporting.report_formatter import ReportFormatter


def test_format_report():
    lines = [
        "Line 1",
        "Line 2",
        "Line 3",
    ]

    report = ReportFormatter.format(lines)

    assert report == (
        "Line 1\n"
        "Line 2\n"
        "Line 3"
    )