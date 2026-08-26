import argparse
from pathlib import Path
from time import sleep
import MetaTrader5 as mt5
import os
from tdi.adapters.mt5_analysis_pipeline import MT5AnalysisPipeline
from tdi.adapters.mt5_momentum_pipeline import MT5MomentumPipeline
from tdi.adapters.mt5_multi_timeframe_pipeline import (
    MT5MultiTimeframePipeline,
)
from tdi.graphical.alert_deduplication_engine import (
    AlertDeduplicationEngine,
)
from tdi.graphical.alert_state import AlertState
from tdi.graphical.bias_readiness_engine import (
    BiasReadinessEngine,
)
from tdi.graphical.json_alert_state_repository import (
    JsonAlertStateRepository,
)
from tdi.graphical.json_scenario_state_repository import (
    JsonScenarioStateRepository,
)
from tdi.graphical.multi_timeframe_decision_engine import (
    MultiTimeframeDecisionEngine,
)
from tdi.graphical.scenario_state_engine import (
    ScenarioStateEngine,
)
from tdi.graphical.scenario_transition_engine import (
    ScenarioTransitionEngine,
)
from tdi.graphical.transition_alert_engine import (
    TransitionAlertEngine,
)
from tdi.graphical.wait_action_plan_engine import (
    WaitActionPlanEngine,
)

from tdi.adapters.mt5_market_data_adapter import (
    MT5MarketDataAdapter,
)

from urllib.parse import urlencode
from urllib.request import Request, urlopen

from tdi.notifications.telegram_notifier import TelegramNotifier



SCENARIO_STATE_PATH = (
    Path("data")
    / "scenario_states.json"
)

ALERT_STATE_PATH = (
    Path("data")
    / "alert_states.json"
)

DEFAULT_COUNT = 250

def telegram_post(
    url: str,
    data: dict,
    timeout: int,
):
    encoded_data = urlencode(data).encode("utf-8")

    request = Request(
        url,
        data=encoded_data,
        method="POST",
    )

    return urlopen(
        request,
        timeout=timeout,
    )


def build_telegram_notifier() -> TelegramNotifier:
    return TelegramNotifier.from_environment(
        post=telegram_post,
    )

def notify_new_alert(
    symbol: str,
    message: str,
    action: str,
    level: str | None = None,
) -> None:
    bot_token = os.environ.get(
        "TDI_TELEGRAM_BOT_TOKEN"
    )
    chat_id = os.environ.get(
        "TDI_TELEGRAM_CHAT_ID"
    )

    if not bot_token or not chat_id:
        return

    notifier = build_telegram_notifier()

    notifier.send(
        symbol=symbol,
        message=message,
        action=action,
        level=level,
    )


def analyze_symbol(
    symbol: str,
    multi_pipeline: MT5MultiTimeframePipeline,
    momentum_pipeline: MT5MomentumPipeline,
) -> None:
    result = multi_pipeline.analyze(
        symbol=symbol,
        count=DEFAULT_COUNT,
    )

    h4_momentum = momentum_pipeline.analyze(
        symbol=symbol,
        timeframe="H4",
        count=DEFAULT_COUNT,
    )

    h1_momentum = momentum_pipeline.analyze(
        symbol=symbol,
        timeframe="H1",
        count=DEFAULT_COUNT,
    )

    decision = MultiTimeframeDecisionEngine().decide(
        result=result,
        h4_momentum=h4_momentum,
        h1_momentum=h1_momentum,
    )

    wait_plan = WaitActionPlanEngine().analyze(
        result=result,
        h4_momentum=h4_momentum,
        h1_momentum=h1_momentum,
    )

    bias_readiness = BiasReadinessEngine().analyze(
        result=result,
        h1_momentum=h1_momentum,
    )

    scenario = ScenarioStateEngine().analyze(
        decision=decision,
        wait_plan=wait_plan,
        bias_readiness=bias_readiness,
    )

    previous = JsonScenarioStateRepository.load(
        symbol=symbol,
        path=SCENARIO_STATE_PATH,
    )

    transition = None
    alert = None
    deduplication = None

    if previous is not None:
        previous_state, previous_side = previous

        transition = ScenarioTransitionEngine().analyze(
            previous_state=previous_state,
            current_state=scenario.state,
            previous_target_side=previous_side,
            current_target_side=scenario.target_side,
        )

        alert = TransitionAlertEngine().analyze(
            transition=transition,
            target_side=scenario.target_side,
        )

        previous_alert = JsonAlertStateRepository.load(
            symbol=symbol,
            path=ALERT_STATE_PATH,
        )

        deduplication = AlertDeduplicationEngine().analyze(
            current_alert=alert,
            previous_alert=previous_alert,
        )

        if alert.active:
            JsonAlertStateRepository.save(
                symbol=symbol,
                alert=AlertState(
                    level=alert.level.value,
                    message=alert.message,
                ),
                path=ALERT_STATE_PATH,
            )
        else:
            JsonAlertStateRepository.delete(
                symbol=symbol,
                path=ALERT_STATE_PATH,
            )

    JsonScenarioStateRepository.save(
        symbol=symbol,
        state=scenario.state,
        target_side=scenario.target_side,
        path=SCENARIO_STATE_PATH,
    )

    print()
    print("=" * 60)
    print(f"TDI LIVE — {symbol}")
    print("=" * 60)

    print(
        f"Decision          : "
        f"{decision.decision.value}"
    )

    print(
        f"Preferred side    : "
        f"{decision.preferred_side}"
    )

    print(
        f"Target side       : "
        f"{scenario.target_side}"
    )

    print(
        f"Bias convergence  : "
        f"{bias_readiness.convergence.value}"
    )

    print(
        f"Bias readiness    : "
        f"{bias_readiness.readiness.value}"
    )

    print(
        f"Bias score        : "
        f"{bias_readiness.score}/100"
    )


    print(
        f"Bias aligned      : "
        f"{decision.bias_aligned}"
    )

    print(
        f"Structure aligned : "
        f"{decision.structure_aligned}"
    )

    print(
        f"Timing favorable  : "
        f"{decision.timing_favorable}"
    )

    print(
        f"Momentum confirmed: "
        f"{decision.momentum_confirmed}"
    )

    print(
        f"Scenario          : "
        f"{scenario.state.value}"
    )

    print(
        f"Scenario score    : "
        f"{scenario.score}/100"
    )

    if wait_plan.conditions:
        print(
            "Waiting for       : "
            + ", ".join(
                condition.value
                for condition in wait_plan.conditions
            )
        )
    else:
        print("Waiting for       : None")

    if transition is None:
        print("Transition        : Initial")
        print("Alert             : None")
        return

    print(
        f"Transition        : "
        f"{transition.transition.value}"
    )

    print(
        f"Alert level       : "
        f"{alert.level.value}"
    )

    print(
        f"Alert active      : "
        f"{alert.active}"
    )

    print(
        f"New alert         : "
        f"{deduplication.is_new}"
    )

    if deduplication.is_new:
        print(
            f"ALERT             : "
            f"{alert.message}"
        )

        print(
            f"ACTION            : "
            f"{alert.action}"
        )

        notify_new_alert(
            symbol=symbol,
            level=alert.level.value,
            message=alert.message,
            action=alert.action,
        )


def parse_args():
    parser = argparse.ArgumentParser(
        description=(
            "TDI live MT5 analysis runner."
        )
    )

    parser.add_argument(
        "symbols",
        nargs="+",
        help=(
            "MT5 symbols to analyze, "
            "for example XAUUSD NAS100 EURUSD"
        ),
    )

    parser.add_argument(
        "--monitor",
        action="store_true",
        help=(
            "Continuously monitor the requested symbols."
        ),
    )

    parser.add_argument(
        "--interval",
        type=int,
        default=60,
        help=(
            "Monitoring interval in seconds "
            "(default: 60)."
        ),
    )

    return parser.parse_args()

def main():
    args = parse_args()

    adapter = MT5MarketDataAdapter(mt5)

    try:
        adapter.initialize()

        analysis_pipeline = MT5AnalysisPipeline(
            adapter=adapter
        )

        multi_pipeline = MT5MultiTimeframePipeline(
            pipeline=analysis_pipeline
        )

        momentum_pipeline = MT5MomentumPipeline(
            analysis_pipeline=analysis_pipeline
        )

        while True:
            for symbol in args.symbols:
                try:
                    analyze_symbol(
                        symbol=symbol,
                        multi_pipeline=multi_pipeline,
                        momentum_pipeline=momentum_pipeline,
                    )

                except Exception as exc:
                    print()
                    print("=" * 60)
                    print(f"TDI LIVE — {symbol}")
                    print("=" * 60)
                    print("Status            : ERROR")
                    print(
                        f"Error             : "
                        f"{type(exc).__name__}: {exc}"
                    )

            if not args.monitor:
                break

            sleep(args.interval)

    except KeyboardInterrupt:
        print()
        print("TDI monitoring stopped.")

    finally:
        adapter.shutdown()


if __name__ == "__main__":
    main()

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


