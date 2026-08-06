from datetime import datetime

from tdi.engines.analysis_engine import AnalysisEngine
from tdi.engines.decision_engine import DecisionEngine
from tdi.engines.risk_engine import RiskEngine
from tdi.engines.trade_advisor import TradeAdvisor
from tdi.engines.validation_engine import ValidationEngine
from tdi.models.market_snapshot import MarketSnapshot
from tdi.models.price_structure import PriceStructure
from tdi.models.trade import Side, Trade
from tdi.reports.console_report import ConsoleReport


def main() -> None:
    trade = Trade(
        instrument="XAUUSD",
        side=Side.SELL,
        entry=4050.0,
        stop_loss=4090.0,
        take_profit=3970.0,
        capital=5000.0,
        risk_percent=1.0,
        timeframe="H4",
        atr=30.0,
        created_at=datetime.now(),
    )

    snapshot = MarketSnapshot(
        price=4002.0,
        ema20=4010.0,
        ema50=4030.0,
        ema200=4050.0,
        rsi=42.0,
        macd=-8.0,
        macd_signal=-5.0,
        macd_histogram=-3.0,
    )

    price_structure = PriceStructure(
        current_price=snapshot.price,
        support=3970.0,
        resistance=4050.0,
        swing_high=4060.0,
        swing_low=3980.0,
    )

    analysis_engine = AnalysisEngine()
    risk_engine = RiskEngine()
    validation_engine = ValidationEngine()
    decision_engine = DecisionEngine()
    trade_advisor = TradeAdvisor()

    analysis = analysis_engine.analyze(
        snapshot=snapshot,
        price_structure=price_structure,
        side=trade.side,
    )

    risk = risk_engine.analyze(trade)

    validation = validation_engine.validate(
        analysis=analysis,
        risk=risk,
        side=trade.side,
    )

    decision = decision_engine.decide(
        analysis=analysis,
        validation=validation,
        risk=risk,
    )

    advisor = trade_advisor.advise(
        trade=trade,
        analysis=analysis,
        validation=validation,
        decision=decision,
        risk=risk,
    )

    ConsoleReport.display(
        trade=trade,
        analysis=analysis,
        validation=validation,
        risk=risk,
        decision=decision,
        advisor=advisor,
    )


if __name__ == "__main__":
    main()