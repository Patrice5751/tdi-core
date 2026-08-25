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
                ],
		"monitor": False,
            },
        )(),
    )

    run_tdi_mt5.main()

    assert analyzed_symbols == [
        "XAUUSD",
        "XAGUSD",
        "NAS100",
    ]

def test_main_continues_after_symbol_error(
    monkeypatch,
):
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

        if symbol == "XAGUSD":
            raise RuntimeError("Simulated failure")

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
                ],
		"monitor": False,
		"interval": 60,
            },
        )(),
    )

    run_tdi_mt5.main()

    assert analyzed_symbols == [
        "XAUUSD",
        "XAGUSD",
        "NAS100",
    ]

def test_main_always_shuts_down_adapter(
    monkeypatch,
):
    shutdown_called = []

    class FakeAdapter:
        def __init__(self, mt5):
            pass

        def initialize(self):
            pass



        def shutdown(self):
            shutdown_called.append(True)

    class FailingAnalysisPipeline:
        def __init__(self, adapter):
            raise RuntimeError("Simulated startup failure")

    monkeypatch.setattr(
        run_tdi_mt5,
        "MT5MarketDataAdapter",
        FakeAdapter,
    )
    monkeypatch.setattr(
        run_tdi_mt5,
        "MT5AnalysisPipeline",
        FailingAnalysisPipeline,
    )
    monkeypatch.setattr(
        run_tdi_mt5,
        "parse_args",
        lambda: type(
            "Args",
            (),
            {"symbols": ["XAUUSD"]},
        )(),
    )

    try:
        run_tdi_mt5.main()
    except RuntimeError:
        pass

    assert shutdown_called == [True]

def test_parse_args_supports_monitor_interval(
    monkeypatch,
):
    monkeypatch.setattr(
        "sys.argv",
        [
            "run_tdi_mt5",
            "XAUUSD",
            "--monitor",
            "--interval",
            "120",
        ],
    )

    args = run_tdi_mt5.parse_args()

    assert args.monitor is True
    assert args.interval == 120
def test_monitor_repeats_symbol_analysis(
    monkeypatch,
):
    analyzed_symbols = []
    sleep_calls = []

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

    def fake_sleep(seconds):
        sleep_calls.append(seconds)

        if len(sleep_calls) == 2:
            raise KeyboardInterrupt

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
        "sleep",
        fake_sleep,
        raising=False,
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
                ],
                "monitor": True,
		"interval": 60,
            },
        )(),
    )

    try:
        run_tdi_mt5.main()
    except KeyboardInterrupt:
        pass

    assert analyzed_symbols == [
        "XAUUSD",
        "XAGUSD",
        "XAUUSD",
        "XAGUSD",
    ]
    
    assert analyzed_symbols == [
        "XAUUSD",
        "XAGUSD",
        "XAUUSD",
        "XAGUSD",
    ]

def test_parse_args_supports_monitor_mode(
    monkeypatch,
):
    monkeypatch.setattr(
        "sys.argv",
        [
            "run_tdi_mt5",
            "XAUUSD",
            "XAGUSD",
            "--monitor",
        ],
    )

    args = run_tdi_mt5.parse_args()

    assert args.symbols == [
        "XAUUSD",
        "XAGUSD",
    ]
    assert args.monitor is True

def test_monitor_handles_keyboard_interrupt_and_shuts_down(
    monkeypatch,
):
    shutdown_called = []

    class FakeAdapter:
        def __init__(self, mt5):
            pass

        def initialize(self):
            pass

        def shutdown(self):
            shutdown_called.append(True)

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
        raise KeyboardInterrupt

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
                "symbols": ["XAUUSD"],
                "monitor": True,
                "interval": 60,
            },
        )(),
    )

    run_tdi_mt5.main()

    assert shutdown_called == [True]

def test_analyze_symbol_exposes_bias_readiness(
    monkeypatch,
    capsys,
):
    class FakeMultiPipeline:
        def analyze(self, symbol, count):
            return object()

    class FakeMomentumPipeline:
        def analyze(self, symbol, timeframe, count):
            return object()

    class FakeDecision:
        decision = type("Value", (), {"value": "Wait"})()
        preferred_side = None
        bias_aligned = False
        structure_aligned = False
        timing_favorable = False
        momentum_confirmed = False

    class FakeWaitPlan:
        conditions = []

    class FakeBiasReadiness:
        target_side = "BUY"
        convergence = type(
            "Value",
            (),
            {"value": "Toward"},
        )()
        readiness = type(
            "Value",
            (),
            {"value": "Medium"},
        )()
        score = 85

    class FakeScenario:
        state = type(
            "Value",
            (),
            {"value": "Building"},
        )()
        target_side = "BUY"
        score = 85

    monkeypatch.setattr(
        run_tdi_mt5.MultiTimeframeDecisionEngine,
        "decide",
        lambda self, **kwargs: FakeDecision(),
    )
    monkeypatch.setattr(
        run_tdi_mt5.WaitActionPlanEngine,
        "analyze",
        lambda self, **kwargs: FakeWaitPlan(),
    )
    monkeypatch.setattr(
        run_tdi_mt5.BiasReadinessEngine,
        "analyze",
        lambda self, **kwargs: FakeBiasReadiness(),
    )
    monkeypatch.setattr(
        run_tdi_mt5.ScenarioStateEngine,
        "analyze",
        lambda self, **kwargs: FakeScenario(),
    )
    monkeypatch.setattr(
        run_tdi_mt5.JsonScenarioStateRepository,
        "load",
        lambda **kwargs: None,
    )
    monkeypatch.setattr(
        run_tdi_mt5.JsonScenarioStateRepository,
        "save",
        lambda **kwargs: None,
    )

    run_tdi_mt5.analyze_symbol(
        symbol="XAUUSD",
        multi_pipeline=FakeMultiPipeline(),
        momentum_pipeline=FakeMomentumPipeline(),
    )

    output = capsys.readouterr().out

    assert "Target side       : BUY" in output
    assert "Bias convergence  : Toward" in output
    assert "Bias readiness    : Medium" in output
    assert "Bias score        : 85/100" in output
