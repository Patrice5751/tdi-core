import MetaTrader5 as mt5

from tdi.adapters.mt5_analysis_pipeline import MT5AnalysisPipeline
from tdi.adapters.mt5_market_data_adapter import MT5MarketDataAdapter
from tdi.adapters.mt5_momentum_pipeline import MT5MomentumPipeline
from tdi.adapters.mt5_multi_timeframe_pipeline import (
    MT5MultiTimeframePipeline,
)
from tdi.graphical.market_bias_engine import MarketBiasEngine
from tdi.graphical.multi_timeframe_decision_engine import (
    MultiTimeframeDecisionEngine,
)
from tdi.graphical.wait_action_plan_engine import (
    WaitActionPlanEngine,
)

from tdi.graphical.wait_priority_engine import (
    WaitPriorityEngine,
)

from tdi.graphical.bias_readiness_engine import (
    BiasReadinessEngine,
)

from tdi.graphical.scenario_state_engine import (
    ScenarioStateEngine,
)

from pathlib import Path

from tdi.graphical.json_scenario_state_repository import (
    JsonScenarioStateRepository,
)
from tdi.graphical.scenario_transition_engine import (
    ScenarioTransitionEngine,
)

from tdi.graphical.transition_alert_engine import (
    TransitionAlertEngine,
)

from pathlib import Path

from tdi.graphical.alert_deduplication_engine import (
    AlertDeduplicationEngine,
)
from tdi.graphical.alert_state import AlertState
from tdi.graphical.json_alert_state_repository import (
    JsonAlertStateRepository,
)

SCENARIO_STATE_PATH = (
    Path("data")
    / "scenario_states.json"
)

ALERT_STATE_PATH = (
    Path("data")
    / "alert_states.json"
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
        f"Structure score : "
        f"{context.direction_confidence}/100"
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
        f"{ma_direction}"
    )

    print(
        f"MA score : "
        f"{context.ma_confirmation_score}/100"
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
        f"Bias strength : "
        f"{bias.confidence}/100"
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


def print_momentum(
    timeframe: str,
    momentum,
) -> None:
    print()
    print(
        f"=== MOMENTUM {timeframe} ==="
    )

    print(
        f"Momentum : "
        f"{momentum.momentum.value}"
    )

    print(
        f"Momentum score : "
        f"{momentum.confidence}/100"
    )

    if momentum.reason:
        print("Reasons :")

        for reason in momentum.reason:
            print(
                f"- {reason}"
            )
    else:
        print(
            "Reasons : aucune confirmation."
        )


def main():
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

        result = multi_pipeline.analyze(
            symbol="XAUUSD",
            count=250,
        )

        h4_momentum = momentum_pipeline.analyze(
            symbol="XAUUSD",
            timeframe="H4",
            count=250,
        )

        h1_momentum = momentum_pipeline.analyze(
            symbol="XAUUSD",
            timeframe="H1",
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

        print_momentum(
            "H4",
            h4_momentum,
        )

        print_context(
            "H1",
            result.h1,
        )

        print_momentum(
            "H1",
            h1_momentum,
        )

        print()
        print("=== ALIGNEMENT ===")

        if result.aligned:
            print(
                "Structure H4 / H1 : OUI"
            )
        else:
            print(
                "Structure H4 / H1 : NON"
            )

        decision = (
            MultiTimeframeDecisionEngine().decide(
                result=result,
                h4_momentum=h4_momentum,
                h1_momentum=h1_momentum,
            )
        )

        print()
        print(
            "=== TDI MULTI-TIMEFRAME DECISION ==="
        )

        print(
            f"Preferred side : "
            f"{decision.preferred_side}"
        )

        print(
            f"Bias aligned : "
            f"{decision.bias_aligned}"
        )

        print(
            f"Structure aligned : "
            f"{decision.structure_aligned}"
        )

        print(
            f"Momentum confirmed : "
            f"{decision.momentum_confirmed}"
        )

        print(
            f"Timing favorable : "
            f"{decision.timing_favorable}"
        )

        print(
            f"Directional bias strength : "
            f"{decision.confidence}/100"
        )

        print(
            f"Action : "
            f"{decision.decision.value}"
        )

        print(
            f"Reason : "
            f"{decision.reason}"
        )

        wait_plan = WaitActionPlanEngine().analyze(
            result=result,
            h4_momentum=h4_momentum,
            h1_momentum=h1_momentum,
        )

        print()
        print("=== TDI WAIT ACTION PLAN ===")

        print(
            f"Preferred side : "
            f"{wait_plan.preferred_side}"
        )

        print(
            f"Ready : "
            f"{wait_plan.ready}"
        )

        print(
            f"Reason : "
            f"{wait_plan.reason}"
        )

        if wait_plan.conditions:
            print("Waiting for:")

            for condition in wait_plan.conditions:
                print(
                    f"- {condition.value}"
                )
        else:
            print(
                "Waiting for: aucune condition restante."
            )

        priorities = WaitPriorityEngine().prioritize(
            plan=wait_plan,
            result=result,
            h4_momentum=h4_momentum,
            h1_momentum=h1_momentum,
        )

        print()
        print("=== TDI WAIT PRIORITIES ===")

        if priorities:
            for item in priorities:
                print(
                    f"{item.priority}. "
                    f"{item.condition.value}"
                )

                print(
                    f"   Importance : "
                    f"{item.importance_score}/100"
                )

                print(
                    f"   Proximity : "
                    f"{item.proximity_score}/100"
                )

                print(
                    f"   {item.reason}"
                )
        else:
            print(
                "Aucune condition d'attente restante."
            )

        bias_readiness = BiasReadinessEngine().analyze(
            result=result,
            h1_momentum=h1_momentum,
        )

        print()
        print("=== TDI BIAS READINESS ===")

        print(
            f"Target side : "
            f"{bias_readiness.target_side}"
        )

        print(
            f"Readiness : "
            f"{bias_readiness.readiness.value}"
        )

        print(
            f"Convergence : "
            f"{bias_readiness.convergence.value}"
        )

        print(
            f"Bias readiness score : "
            f"{bias_readiness.score}/100"
        )

        print(
            f"Reason : "
            f"{bias_readiness.reason}"
        )

        scenario = ScenarioStateEngine().analyze(
            decision=decision,
            wait_plan=wait_plan,
            bias_readiness=bias_readiness,
        )

        print()
        print("=== TDI SCENARIO STATE ===")

        print(
            f"Target side : "
            f"{scenario.target_side}"
        )

        print(
            f"Scenario state : "
            f"{scenario.state.value}"
        )

        print(
            f"Scenario maturity : "
            f"{scenario.score}/100"
        )

        print(
            f"Action : "
            f"{decision.decision.value}"
        )

        print(
            f"Reason : "
            f"{scenario.reason}"
        )

        previous = JsonScenarioStateRepository.load(
            symbol="XAUUSD",
            path=SCENARIO_STATE_PATH,
        )

        print()
        print("=== TDI SCENARIO TRANSITION ===")

        if previous is None:
            print("Previous state : None")

            print(
                f"Current state : "
                f"{scenario.state.value}"
            )

            print(
                "Transition : Initial"
            )

            print(
                "Reason : Premier état enregistré "
                "pour ce symbole."
            )

        else:
            previous_state, previous_side = previous

            transition = ScenarioTransitionEngine().analyze(
                previous_state=previous_state,
                current_state=scenario.state,
                previous_target_side=previous_side,
                current_target_side=scenario.target_side,
            )

            print(
                f"Previous state : "
                f"{previous_state.value}"
            )

            print(
                f"Previous target side : "
                f"{previous_side}"
            )

            print(
                f"Current state : "
                f"{scenario.state.value}"
            )

            print(
                f"Current target side : "
                f"{scenario.target_side}"
            )

            print(
                f"Transition : "
                f"{transition.transition.value}"
            )

            print(
                f"Reason : "
                f"{transition.reason}"
            )

            alert = TransitionAlertEngine().analyze(
                transition=transition,
                target_side=scenario.target_side,
            )

            previous_alert = JsonAlertStateRepository.load(
                symbol="XAUUSD",
                path=ALERT_STATE_PATH,
            )

            deduplication = AlertDeduplicationEngine().analyze(
                current_alert=alert,
                previous_alert=previous_alert,
            )

            print()
            print("=== TDI TRANSITION ALERT ===")

            print(
                f"Level : "
                f"{alert.level.value}"
            )

            print(
                f"Active : "
                f"{alert.active}"
            )

            print(
                f"Message : "
                f"{alert.message}"
            )

            print(
                f"New alert : "
                f"{deduplication.is_new}"
            )

            print(
                f"Deduplication reason : "
                f"{deduplication.reason}"
            )

            print(
                f"Action : "
                f"{alert.action}"
            )

            if alert.active:
                JsonAlertStateRepository.save(
                    symbol="XAUUSD",
                    alert=AlertState(
                        level=alert.level.value,
                        message=alert.message,
                    ),
                    path=ALERT_STATE_PATH,
                )

        JsonScenarioStateRepository.save(
            symbol="XAUUSD",
            state=scenario.state,
            target_side=scenario.target_side,
            path=SCENARIO_STATE_PATH,
        )


    finally:
        adapter.shutdown()

        

if __name__ == "__main__":
    main()
