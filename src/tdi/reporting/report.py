from dataclasses import dataclass

from tdi.reporting.markdown_formatter import MarkdownFormatter
from tdi.reporting.report_formatter import ReportFormatter


@dataclass(frozen=True)
class Report:
    lines: list[str]

    def as_text(self):
        return ReportFormatter.format(self.lines)

    def as_markdown(self):
        return MarkdownFormatter.format(self.lines)
