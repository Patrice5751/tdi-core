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
        notification_filter=None,
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
        notification_filter=None,
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
        notification_filter=None,
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
        notification_filter=None,
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

def test_analyze_symbol_labels_scenario_score(
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
        convergence = type("Value", (), {"value": "Toward"})()
        readiness = type("Value", (), {"value": "Medium"})()
        score = 85

    class FakeScenario:
        state = type("Value", (), {"value": "Building"})()
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
        symbol="EURUSD",
        multi_pipeline=FakeMultiPipeline(),
        momentum_pipeline=FakeMomentumPipeline(),
    )

    output = capsys.readouterr().out

    assert "Scenario score    : 85/100" in output
    assert "Scenario maturity" not in output

def test_new_alert_triggers_notification(
    monkeypatch,
):
    notifications = []

    class FakeMultiPipeline:
        def analyze(self, symbol, count):
            return object()

    class FakeMomentumPipeline:
        def analyze(self, symbol, timeframe, count):
            return object()

    class FakeDecision:
        decision = type("Value", (), {"value": "Wait"})()
        preferred_side = "BUY"
        bias_aligned = True
        structure_aligned = False
        timing_favorable = False
        momentum_confirmed = False

    class FakeWaitPlan:
        conditions = []

    class FakeBiasReadiness:
        target_side = "BUY"
        convergence = type("Value", (), {"value": "Aligned"})()
        readiness = type("Value", (), {"value": "High"})()
        score = 100

    class FakeScenario:
        state = type("Value", (), {"value": "Building"})()
        target_side = "BUY"
        score = 90

    class FakeTransition:
        transition = type("Value", (), {"value": "Improving"})()

    class FakeAlert:
        active = True
        level = type("Value", (), {"value": "Info"})()
        message = "Scenario BUY improving"
        action = "Monitor confirmation"

    class FakeDeduplication:
        is_new = True

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
        lambda **kwargs: (FakeScenario.state, "BUY"),
    )
    monkeypatch.setattr(
        run_tdi_mt5.JsonScenarioStateRepository,
        "save",
        lambda **kwargs: None,
    )

    monkeypatch.setattr(
        run_tdi_mt5.ScenarioTransitionEngine,
        "analyze",
        lambda self, **kwargs: FakeTransition(),
    )
    monkeypatch.setattr(
        run_tdi_mt5.TransitionAlertEngine,
        "analyze",
        lambda self, **kwargs: FakeAlert(),
    )

    monkeypatch.setattr(
        run_tdi_mt5.JsonAlertStateRepository,
        "load",
        lambda **kwargs: None,
    )
    monkeypatch.setattr(
        run_tdi_mt5.JsonAlertStateRepository,
        "save",
        lambda **kwargs: None,
    )
    monkeypatch.setattr(
        run_tdi_mt5.JsonAlertStateRepository,
        "delete",
        lambda **kwargs: None,
    )

    monkeypatch.setattr(
        run_tdi_mt5.AlertDeduplicationEngine,
        "analyze",
        lambda self, **kwargs: FakeDeduplication(),
    )

    monkeypatch.setattr(
        run_tdi_mt5,
        "notify_new_alert",
        lambda symbol, level, message, action: notifications.append(
            (symbol, level, message, action)
        ),
        raising=False,
    )

    run_tdi_mt5.analyze_symbol(
        symbol="XAUUSD",
        multi_pipeline=FakeMultiPipeline(),
        momentum_pipeline=FakeMomentumPipeline(),
    )

    assert notifications == [
        (
            "XAUUSD",
            "Info",
            "Scenario BUY improving",
            "Monitor confirmation",
        )
    ]

def test_duplicate_alert_does_not_trigger_notification(
    monkeypatch,
):
    notifications = []

    class FakeMultiPipeline:
        def analyze(self, symbol, count):
            return object()

    class FakeMomentumPipeline:
        def analyze(self, symbol, timeframe, count):
            return object()

    class FakeDecision:
        decision = type("Value", (), {"value": "Wait"})()
        preferred_side = "BUY"
        bias_aligned = True
        structure_aligned = False
        timing_favorable = False
        momentum_confirmed = False

    class FakeWaitPlan:
        conditions = []

    class FakeBiasReadiness:
        target_side = "BUY"
        convergence = type("Value", (), {"value": "Aligned"})()
        readiness = type("Value", (), {"value": "High"})()
        score = 100

    class FakeScenario:
        state = type("Value", (), {"value": "Building"})()
        target_side = "BUY"
        score = 90

    class FakeTransition:
        transition = type("Value", (), {"value": "Unchanged"})()

    class FakeAlert:
        active = True
        level = type("Value", (), {"value": "Info"})()
        message = "Scenario BUY improving"
        action = "Monitor confirmation"

    class FakeDeduplication:
        is_new = False

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
        lambda **kwargs: (FakeScenario.state, "BUY"),
    )
    monkeypatch.setattr(
        run_tdi_mt5.JsonScenarioStateRepository,
        "save",
        lambda **kwargs: None,
    )
    monkeypatch.setattr(
        run_tdi_mt5.ScenarioTransitionEngine,
        "analyze",
        lambda self, **kwargs: FakeTransition(),
    )
    monkeypatch.setattr(
        run_tdi_mt5.TransitionAlertEngine,
        "analyze",
        lambda self, **kwargs: FakeAlert(),
    )
    monkeypatch.setattr(
        run_tdi_mt5.JsonAlertStateRepository,
        "load",
        lambda **kwargs: None,
    )
    monkeypatch.setattr(
        run_tdi_mt5.JsonAlertStateRepository,
        "save",
        lambda **kwargs: None,
    )
    monkeypatch.setattr(
        run_tdi_mt5.JsonAlertStateRepository,
        "delete",
        lambda **kwargs: None,
    )
    monkeypatch.setattr(
        run_tdi_mt5.AlertDeduplicationEngine,
        "analyze",
        lambda self, **kwargs: FakeDeduplication(),
    )
    monkeypatch.setattr(
        run_tdi_mt5,
        "notify_new_alert",
        lambda symbol, message, action: notifications.append(
            (symbol, message, action)
        ),
    )

    run_tdi_mt5.analyze_symbol(
        symbol="XAUUSD",
        multi_pipeline=FakeMultiPipeline(),
        momentum_pipeline=FakeMomentumPipeline(),
    )

    assert notifications == []

def test_notify_new_alert_does_nothing_without_telegram_config(
    monkeypatch,
):
    monkeypatch.delenv(
        "TDI_TELEGRAM_BOT_TOKEN",
        raising=False,
    )
    monkeypatch.delenv(
        "TDI_TELEGRAM_CHAT_ID",
        raising=False,
    )

    run_tdi_mt5.notify_new_alert(
        symbol="XAUUSD",
        message="Scenario BUY ready",
        action="Review setup",
    )

def test_notify_new_alert_sends_telegram_when_configured(
    monkeypatch,
):
    sent = []

    monkeypatch.setenv(
        "TDI_TELEGRAM_BOT_TOKEN",
        "test-token",
    )
    monkeypatch.setenv(
        "TDI_TELEGRAM_CHAT_ID",
        "123456",
    )

    class FakeNotifier:
        def send(
            self,
            symbol,
            message,
            action,
            level=None,
        ):
            sent.append(
                (
                    symbol,
                    level,
                    message,
                    action,
                )
            )

    monkeypatch.setattr(
        run_tdi_mt5,
        "build_telegram_notifier",
        lambda: FakeNotifier(),
        raising=False,
    )

    run_tdi_mt5.notify_new_alert(
        symbol="XAUUSD",
        message="Scenario BUY ready",
        action="Review setup",
    )

    assert sent == [
    (
        "XAUUSD",
        None,
        "Scenario BUY ready",
        "Review setup",
    )
    ]

def test_build_telegram_notifier_uses_environment(
    monkeypatch,
):
    monkeypatch.setenv(
        "TDI_TELEGRAM_BOT_TOKEN",
        "test-token",
    )
    monkeypatch.setenv(
        "TDI_TELEGRAM_CHAT_ID",
        "123456",
    )

    notifier = run_tdi_mt5.build_telegram_notifier()

    assert notifier.bot_token == "test-token"
    assert notifier.chat_id == "123456"

def test_telegram_post_builds_encoded_post_request(
    monkeypatch,
):
    captured = {}

    def fake_urlopen(request, timeout):
        captured["request"] = request
        captured["timeout"] = timeout
        return object()

    monkeypatch.setattr(
        run_tdi_mt5,
        "urlopen",
        fake_urlopen,
    )

    run_tdi_mt5.telegram_post(
        url="https://example.test/sendMessage",
        data={
            "chat_id": "123456",
            "text": "TDI ALERT — XAUUSD",
        },
        timeout=10,
    )

    request = captured["request"]

    assert request.full_url == (
        "https://example.test/sendMessage"
    )
    assert request.get_method() == "POST"
    assert captured["timeout"] == 10

    body = request.data.decode("utf-8")

    assert "chat_id=123456" in body
    assert "text=TDI+ALERT+" in body

def test_notify_new_alert_forwards_high_level_to_telegram(
    monkeypatch,
):
    sent = []

    class FakeNotifier:
        def send(
            self,
            symbol,
            message,
            action,
            level=None,
        ):
            sent.append(
                (
                    symbol,
                    level,
                    message,
                    action,
                )
            )

    monkeypatch.setenv(
        "TDI_TELEGRAM_BOT_TOKEN",
        "test-token",
    )
    monkeypatch.setenv(
        "TDI_TELEGRAM_CHAT_ID",
        "123456",
    )

    monkeypatch.setattr(
        run_tdi_mt5,
        "build_telegram_notifier",
        lambda: FakeNotifier(),
    )

    run_tdi_mt5.notify_new_alert(
        symbol="XAUUSD",
        level="High",
        message="Scenario BUY ready",
        action="Review setup",
    )

    assert sent == [
        (
            "XAUUSD",
            "High",
            "Scenario BUY ready",
            "Review setup",
        )
    ]

def test_notify_new_alert_survives_telegram_failure(
    monkeypatch,
    capsys,
):
    monkeypatch.setenv(
        "TDI_TELEGRAM_BOT_TOKEN",
        "test-token",
    )
    monkeypatch.setenv(
        "TDI_TELEGRAM_CHAT_ID",
        "123456",
    )

    class FailingNotifier:
        def send(
            self,
            symbol,
            message,
            action,
            level=None,
        ):
            raise OSError("Telegram unavailable")

    monkeypatch.setattr(
        run_tdi_mt5,
        "build_telegram_notifier",
        lambda: FailingNotifier(),
    )

    run_tdi_mt5.notify_new_alert(
        symbol="XAUUSD",
        level="High",
        message="Scenario BUY ready",
        action="Review setup",
    )

    output = capsys.readouterr().out

    assert "Telegram" in output
    assert "unavailable" in output
