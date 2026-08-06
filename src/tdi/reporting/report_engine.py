from tdi.advisor.score_aggregator import ScoreAggregator
from tdi.reporting.confluence_engine import ConfluenceEngine
from tdi.reporting.severity import Severity
from tdi.reporting.decision_summary import DecisionSummary
from tdi.reporting.verdict_engine import VerdictEngine
from tdi.reporting.report import Report
from tdi.advisor.rule_category import RuleCategory
from tdi.advisor.rule_result import RuleResult
from tdi.reporting.explainability_engine import ExplainabilityEngine

class ReportEngine:
    """Construit un rapport texte à partir des résultats des règles."""

    @staticmethod
    def build(rule_results):
        lines = []

        observations = ConfluenceEngine.build(rule_results)

        lines.extend(ReportEngine._header())
        lines.extend(ReportEngine._structure_section(rule_results))
        lines.extend(ReportEngine._risk_section(rule_results))
        lines.extend(ReportEngine._confluence_section(rule_results))
        lines.extend(
            ReportEngine._confluence_observations_section(
                observations
            )
        )

        lines.extend(ReportEngine._global_section(rule_results))
        lines.extend(ReportEngine._insights_section(rule_results))

        normalized_score = ScoreAggregator.normalized_score(
            rule_results
        )
        decision_summary = DecisionSummary.from_score(
            normalized_score
        )

        lines.append("")
        lines.extend(
            VerdictEngine.build(
            decision_summary,
            observations,
            normalized_score,
            )
        )

        explanations = ExplainabilityEngine.build(rule_results)

        return Report(lines)

    @staticmethod
    def _header():
        return [
            "=" * 50,
            "TDI TRADE ANALYSIS",
            "=" * 50,
            "",
        ]

    @staticmethod
    def _structure_section(rule_results):
        structure_results = [
            result
            for result in rule_results
            if result.category == RuleCategory.STRUCTURE
        ]

        if not structure_results:
            return []

        score = ScoreAggregator.compute(structure_results)
        maximum = ScoreAggregator.max_score(structure_results)

        lines = [
            "STRUCTURE",
            "-" * 50,
        ]

        for result in structure_results:
            lines.append(
                f"{ReportEngine._status_icon(result)} "
                f"{result.rule:<20} "
                f"{result.score}/{result.max_score}"
            )

        lines.extend(
            [
                "",
                f"TOTAL STRUCTURE: {score}/{maximum}",
                "",
            ]
        )

        return lines

    @staticmethod
    def _risk_section(rule_results):
        risk_results = [
            result
            for result in rule_results
            if result.category == RuleCategory.RISK
        ]

        if not risk_results:
            return []

        score = ScoreAggregator.compute(risk_results)
        maximum = ScoreAggregator.max_score(risk_results)

        lines = [
            "RISK",
            "-" * 50,
        ]

        for result in risk_results:
            lines.append(
                f"{ReportEngine._status_icon(result)} "
                f"{result.rule:<20} "
                f"{result.score}/{result.max_score}"
            )

        lines.extend(
            [
                "",
                f"TOTAL RISK: {score}/{maximum}",
                "",
            ]
        )

        return lines

    @staticmethod
    def _confluence_section(rule_results):
        confluence_results = [
            result
            for result in rule_results
            if result.category == RuleCategory.CONFLUENCE
        ]

        if not confluence_results:
            return []

        score = ScoreAggregator.compute(confluence_results)
        maximum = ScoreAggregator.max_score(confluence_results)

        lines = [
            "CONFLUENCE",
            "-" * 50,
        ]

        for result in confluence_results:
            lines.append(
                f"{ReportEngine._status_icon(result)} "
                f"{result.rule:<20} "
                f"{result.score}/{result.max_score}"
            )

        lines.extend(
            [
                "",
                f"TOTAL CONFLUENCE: {score}/{maximum}",
                "",
            ]
        )

        return lines

    @staticmethod
    def _confluence_observations_section(observations):
        lines = [
            "",
            "CONFLUENCE OBSERVATIONS",
            "-" * 50,
        ]

        if not observations:
            lines.append("No confluence observation.")
            return lines

        for observation in observations:
            icon = ReportEngine._severity_icon(
                observation.severity
            )

            lines.append(f"{icon} {observation.title}")
            lines.append(f"  {observation.message}")

        return lines

    @staticmethod
    def _global_section(rule_results):
        score = ScoreAggregator.compute(rule_results)
        maximum = ScoreAggregator.max_score(rule_results)
        normalized = ScoreAggregator.normalized_score(
            rule_results
        )

        return [
            f"Score: {score}/{maximum}",
            f"Normalized: {normalized}/100",
        ]

    @staticmethod
    def _insights_section(rule_results):
        strengths = ScoreAggregator.strengths(rule_results)
        weaknesses = ScoreAggregator.weaknesses(rule_results)

        lines = []

        if strengths:
            lines.extend(
                [
                    "",
                    "STRENGTHS",
                    "-" * 50,
                ]
            )

            for message in strengths:
                lines.append(f"• {message}")

        if weaknesses:
            lines.extend(
                [
                    "",
                    "WEAKNESSES",
                    "-" * 50,
                ]
            )

            for message in weaknesses:
                lines.append(f"• {message}")

        return lines

    @staticmethod
    def _status_icon(result):
        return "✔" if result.passed else "✘"

    @staticmethod
    def _severity_icon(severity):
        if severity is Severity.INFO:
            return "ℹ"

        if severity is Severity.WARNING:
            return "⚠"

        if severity is Severity.CRITICAL:
            return "✘"

        return "•"