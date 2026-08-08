import MetaTrader5 as mt5

from tdi.adapters.mt5_analysis_pipeline import MT5AnalysisPipeline
from tdi.adapters.mt5_market_data_adapter import MT5MarketDataAdapter
from tdi.graphical.graphical_decision_engine import (
    GraphicalDecisionEngine,
)
from tdi.models.trade import Side


def main():
    adapter = MT5MarketDataAdapter(mt5)

    try:
        adapter.initialize()

        pipeline = MT5AnalysisPipeline(
            adapter=adapter
        )

        context = pipeline.analyze(
            symbol="XAUUSD",
            timeframe="H4",
            count=250,
        )

        print("=== TDI MT5 TEST ===")
        print(f"Direction : {context.direction.value}")
        print(
            f"Confiance direction : "
            f"{context.direction_confidence}%"
        )
        print(
            f"Localisation : "
            f"{context.location_type.value}"
        )
        print(f"Support : {context.support}")
        print(
            f"Contacts support : "
            f"{context.support_touches}"
        )
        print(
            f"Resistance : "
            f"{context.resistance}"
        )
        print(
            f"Contacts resistance : "
            f"{context.resistance_touches}"
        )

        buy_decision = GraphicalDecisionEngine().decide(
            context=context,
            side=Side.BUY,
        )

        sell_decision = GraphicalDecisionEngine().decide(
            context=context,
            side=Side.SELL,
        )

        print()
        print("=== TDI DECISION ===")

        print(
            f"BUY  : {buy_decision.decision.value}"
        )
        print(
            f"       {buy_decision.reason}"
        )

        print(
            f"SELL : {sell_decision.decision.value}"
        )
        print(
            f"       {sell_decision.reason}"
        )

    finally:
        adapter.shutdown()


if __name__ == "__main__":
    main()
