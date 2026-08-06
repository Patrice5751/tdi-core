from tdi.analysis.advisor_result import AdvisorResult
from tdi.analysis.analysis_result import AnalysisResult
from tdi.analysis.risk_result import RiskResult
from tdi.analysis.validation_result import ValidationResult
from tdi.models.trade import Trade


class ConsoleReport:

    @staticmethod
    def display(
        trade: Trade,
        analysis: AnalysisResult,
        validation: ValidationResult,
        risk: RiskResult,
        decision,
        advisor: AdvisorResult,
    ) -> None:
        print("\n" + "=" * 60)
        print("             TDI ANALYSIS REPORT")
        print("=" * 60)

        ConsoleReport._trade(trade)
        ConsoleReport._trend(analysis)
        ConsoleReport._momentum(analysis)
        ConsoleReport._structure(analysis)
        ConsoleReport._risk(risk)
        ConsoleReport._validation(validation)
        ConsoleReport.print_decision(decision)
        ConsoleReport.print_advisor(advisor)

    @staticmethod
    def _trade(trade: Trade) -> None:
        print("\nTRADE")
        print("-" * 60)
        print(f"Instrument : {trade.instrument}")
        print(f"Direction  : {trade.side.name}")
        print(f"Entrée     : {trade.entry:.2f}")
        print(f"Stop Loss  : {trade.stop_loss:.2f}")
        print(f"Take Profit: {trade.take_profit:.2f}")
        print(f"Capital    : {trade.capital:.2f}")
        print(f"Risque     : {trade.risk_percent:.2f}%")
        print(f"Timeframe  : {trade.timeframe}")
        print(f"ATR        : {trade.atr:.2f}")

    @staticmethod
    def _trend(analysis: AnalysisResult) -> None:
        print("\nTREND")
        print("-" * 60)
        print(f"Direction  : {analysis.trend.trend.name}")
        print(f"Confidence : {analysis.trend.confidence}%")
        print(f"Reason     : {analysis.trend.reason}")

    @staticmethod
    def _momentum(analysis: AnalysisResult) -> None:
        print("\nMOMENTUM")
        print("-" * 60)
        print(f"Direction  : {analysis.momentum.momentum.name}")
        print(f"Confidence : {analysis.momentum.confidence}%")

        for reason in analysis.momentum.reason:
            print(f"✓ {reason}")

    @staticmethod
    def _structure(analysis: AnalysisResult) -> None:
        print("\nSTRUCTURE")
        print("-" * 60)
        print(f"Direction  : {analysis.structure.structure.name}")
        print(f"Confidence : {analysis.structure.confidence}%")
        print(f"Entry zone : {analysis.structure.entry_zone}")

        for reason in analysis.structure.reason:
            print(f"✓ {reason}")

    @staticmethod
    def _risk(risk: RiskResult) -> None:
        print("\nRISK MANAGEMENT")
        print("-" * 60)
        print(f"Montant risqué   : {risk.risk_amount:.2f}")
        print(f"Distance SL      : {risk.stop_distance:.2f}")
        print(f"Distance TP      : {risk.target_distance:.2f}")
        print(f"Ratio R:R        : {risk.rr:.2f}")
        print(f"Taille position  : {risk.position_size:.2f}")
        print(f"Risque valide    : {'✓' if risk.valid else '✗'}")

        for reason in risk.reasons:
            print(f"• {reason}")

    @staticmethod
    def _validation(validation: ValidationResult) -> None:
        print("\nVALIDATION")
        print("-" * 60)

        print(f"Score : {validation.score}/100")
        print(f"Trend      : {'✓' if validation.trend_ok else '✗'}")
        print(f"Momentum   : {'✓' if validation.momentum_ok else '✗'}")
        print(f"Structure  : {'✓' if validation.structure_ok else '✗'}")
        print(f"RR         : {'✓' if validation.rr_ok else '✗'}")
        print(f"Risk       : {'✓' if validation.risk_ok else '✗'}")
        print(f"ATR        : {'✓' if validation.atr_ok else '✗'}")

        print()

        if validation.valid:
            print("✅ TRADE VALIDÉ")
        else:
            print("❌ TRADE REFUSÉ")

        print("\nExplications :")

        if validation.reasons:
            for reason in validation.reasons:
                print(f"• {reason}")
        else:
            print("Aucune anomalie détectée.")

    @staticmethod
    def print_decision(decision) -> None:
        print()
        print("=" * 50)
        print("DECISION")
        print("=" * 50)

        print(f"\nScore final    : {decision.score}/100")
        print(f"Confiance      : {decision.confidence:.0f}%")
        print(
            f"Décision       : "
            f"{'TRADE ACCEPTÉ' if decision.accepted else 'TRADE REFUSÉ'}"
        )

        recommendation = getattr(
            decision.recommendation,
            "value",
            decision.recommendation,
        )
        print(f"Recommandation : {recommendation}")

        print("\nPoints forts")
        print("-" * 50)

        if decision.strengths:
            for strength in decision.strengths:
                print(f"✓ {strength}")
        else:
            print("Aucun point fort majeur détecté.")

        print("\nFaiblesses")
        print("-" * 50)

        if decision.weaknesses:
            for weakness in decision.weaknesses:
                print(f"• {weakness}")
        else:
            print("Aucune faiblesse majeure détectée.")

    @staticmethod
    def print_advisor(advisor: AdvisorResult) -> None:
        print()
        print("=" * 50)
        print("TRADE ADVISOR")
        print("=" * 50)

        print("\nRésumé")
        print("-" * 50)
        print(advisor.summary)

        print("\nRecommandation")
        print("-" * 50)
        print(advisor.recommendation)

        print("\nPoints forts")
        print("-" * 50)

        if advisor.strengths:
            for strength in advisor.strengths:
                print(f"✓ {strength}")
        else:
            print("Aucun point fort majeur détecté.")

        print("\nAméliorations proposées")
        print("-" * 50)

        if advisor.improvements:
            for improvement in advisor.improvements:
                print(f"• {improvement}")
        else:
            print("Aucune amélioration majeure détectée.")

        print()
        print(
            f"Score potentiel après optimisation : "
            f"{advisor.estimated_score}/100"
        )