import MetaTrader5 as mt5
from tdi.graphical.market_bias_engine import MarketBiasEngine
from tdi.adapters.mt5_analysis_pipeline import MT5AnalysisPipeline
from tdi.adapters.mt5_market_data_adapter import MT5MarketDataAdapter
from tdi.adapters.mt5_multi_timeframe_pipeline import (
    MT5MultiTimeframePipeline,
)


def print_context(
    timeframe: str,
    context,
) -> None:
    print()
    print(f"=== {timeframe} ===")
    print(
        f"Direction : "
        f"{context.direction.value}"
    )
    print(
        f"Confiance direction : "
        f"{context.direction_confidence}%"
    )
    print(
        f"MA20 : {context.ma20}"
    )
    print(
        f"MA50 : {context.ma50}"
    )
    print(
        f"MA200 : {context.ma200}"
    )

    if context.ma_bullish:
        ma_direction = "Bullish"
    elif context.ma_bearish:
        ma_direction = "Bearish"
    else:
        ma_direction = "Neutral"

    print(
        f"Confirmation MA : "
        f"{ma_direction} "
        f"({context.ma_confirmation_score}%)"
    )
    bias = MarketBiasEngine().analyze(
        context
    )

    print(
        f"Market Bias : "
        f"{bias.bias.value}"
    )

    print(
        f"Preferred side : "
        f"{bias.preferred_side}"
    )

    print(
        f"Bias confidence : "
        f"{bias.confidence}%"
    )

    print(
        f"Bias reason : "
        f"{bias.reason}"
    )
    print(
        f"Localisation : "
        f"{context.location_type.value}"
    )
    print(
        f"Support : "
        f"{context.support}"
    )
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


def main():
    adapter = MT5MarketDataAdapter(mt5)

    try:
        adapter.initialize()

        analysis_pipeline = MT5AnalysisPipeline(
            adapter=adapter
        )

        multi_pipeline = (
            MT5MultiTimeframePipeline(
                pipeline=analysis_pipeline
            )
        )

        result = multi_pipeline.analyze(
            symbol="XAUUSD",
            count=250,
        )

        print()
        print("==============================")
        print(" TDI MULTI-TIMEFRAME MT5 TEST")
        print("==============================")

        print_context(
            "H4",
            result.h4,
        )

        print_context(
            "H1",
            result.h1,
        )

        print()
        print("=== ALIGNEMENT ===")

        if result.aligned:
            print(
                "H4 / H1 : OUI"
            )
        else:
            print(
                "H4 / H1 : NON"
            )

    finally:
        adapter.shutdown()


if __name__ == "__main__":
    main()
