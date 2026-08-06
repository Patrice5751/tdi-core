
from tdi.reporting.setup_quality import SetupQuality
from tdi.reporting.trade_grade import TradeGrade
from tdi.reporting.trade_assessment import TradeAssessment


class VerdictEngine:
    """Construit une synthèse textuelle de la décision."""

    @staticmethod
    def build(
        decision_summary,
        observations=None,
        normalized_score=None,
    ):
        if observations is None:
            observations = []

        lines = [
            "FINAL VERDICT",
            "-" * 50,
            f"Decision : {decision_summary.decision.name}",
            f"Confidence : {decision_summary.confidence.name}",
        ]

        if normalized_score is not None:
            setup_quality = SetupQuality.from_score(
                normalized_score
            )
            lines.append(
                f"Setup Quality : {setup_quality.value}"
            )

        if normalized_score is not None:
            setup_quality = SetupQuality.from_score(normalized_score)
            trade_grade = TradeGrade.from_score(normalized_score)

            lines.append(
                f"Setup Quality : {setup_quality.value}"
            )
            lines.append(
                f"Trade Grade : {trade_grade.value:.1f} / 10"
            )

        if normalized_score is not None:
            setup_quality = SetupQuality.from_score(normalized_score)
            trade_grade = TradeGrade.from_score(normalized_score)
            trade_assessment = TradeAssessment.from_grade(trade_grade)

            lines.append(
                f"Setup Quality : {setup_quality.value}"
            )
            lines.append(
                f"Trade Grade : {trade_grade.value:.1f} / 10"
            )
            lines.append(
                f"Assessment : {trade_assessment.value}"
            )    

        infos = [
            observation
            for observation in observations
            if observation.severity.name == "INFO"
        ]

        warnings = [
            observation
            for observation in observations
            if observation.severity.name != "INFO"
        ]

        if infos:
            lines.extend([
                "",
                "Reasons",
                "-" * 50,
            ])

            for observation in infos:
                lines.append(f"✔ {observation.message}")

        if warnings:
            lines.extend([
                "",
                "Warnings",
                "-" * 50,
            ])

            for observation in warnings:
                icon = (
                    "⚠"
                    if observation.severity.name == "WARNING"
                    else "✘"
                )
                lines.append(
                    f"{icon} {observation.message}"
                )

        return lines

    def test_build_verdict_with_trade_grade():
        summary = DecisionSummary(
            decision=Decision.BUY,
            confidence=Confidence.MEDIUM,
        )

        lines = VerdictEngine.build(
            summary,
            normalized_score=85,
        )

        report = "\n".join(lines)

        assert "Trade Grade : 8.5 / 10" in report