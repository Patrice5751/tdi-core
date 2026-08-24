import argparse
from pathlib import Path

import MetaTrader5 as mt5

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



SCENARIO_STATE_PATH = (
    Path("data")
    / "scenario_states.json"
)

ALERT_STATE_PATH = (
    Path("data")
    / "alert_states.json"
)

DEFAULT_COUNT = 250


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
        f"Scenario maturity : "
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

    finally:
        adapter.shutdown()


if __name__ == "__main__":
    main()
