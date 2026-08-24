from scripts import run_tdi_mt5


def test_main_analyzes_all_requested_symbols(monkeypatch):
    analyzed_symbols = []

    class FakeAdapter:
        def __init__(self, mt5):
            pass

        def initialize(self):
            pass

        def shutdown(self):
            pass

    class FakeAnalysisPipeline:
        def __init__(self, adapter):
            pass

    class FakeMultiPipeline:
        def __init__(self, pipeline):
            pass

    class FakeMomentumPipeline:
        def __init__(self, analysis_pipeline):
            pass

    def fake_analyze_symbol(
        symbol,
        multi_pipeline,
        momentum_pipeline,
    ):
        analyzed_symbols.append(symbol)

    monkeypatch.setattr(
        run_tdi_mt5,
        "MT5MarketDataAdapter",
        FakeAdapter,
    )
    monkeypatch.setattr(
        run_tdi_mt5,
        "MT5AnalysisPipeline",
        FakeAnalysisPipeline,
    )
    monkeypatch.setattr(
        run_tdi_mt5,
        "MT5MultiTimeframePipeline",
        FakeMultiPipeline,
    )
    monkeypatch.setattr(
        run_tdi_mt5,
        "MT5MomentumPipeline",
        FakeMomentumPipeline,
    )
    monkeypatch.setattr(
        run_tdi_mt5,
        "analyze_symbol",
        fake_analyze_symbol,
    )
    monkeypatch.setattr(
        run_tdi_mt5,
        "parse_args",
        lambda: type(
            "Args",
            (),
            {
                "symbols": [
                    "XAUUSD",
                    "XAGUSD",
                    "NAS100",
                ]
            },
        )(),
    )

    run_tdi_mt5.main()

    assert analyzed_symbols == [
        "XAUUSD",
        "XAGUSD",
        "NAS100",
    ]