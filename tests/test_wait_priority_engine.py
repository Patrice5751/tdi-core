from tdi.adapters.mt5_multi_timeframe_result import (
    MT5MultiTimeframeResult,
)
from tdi.analysis.momentum_analysis import (
    Momentum,
    MomentumAnalysis,
)
from tdi.graphical.graphical_context import GraphicalContext
from tdi.graphical.location_type import LocationType
from tdi.graphical.market_direction import MarketDirection
from tdi.graphical.wait_action_plan import WaitActionPlan
from tdi.graphical.wait_condition import WaitCondition
from tdi.graphical.wait_priority_engine import (
    WaitPriorityEngine,
)


def make_context(
    direction,
    confidence,
    location,
):
    return GraphicalContext(
        direction=direction,
        direction_confidence=confidence,
        location_type=location,
        support=None,
        resistance=None,
        support_touches=0,
        resistance_touches=0,
        ma_confirmation_score=100,
        ma_bullish=True,
        ma_bearish=False,
    )


def make_momentum(
    momentum,
    confidence,
):
    return MomentumAnalysis(
        momentum=momentum,
        confidence=confidence,
        reason=[],
    )


def make_result():
    return MT5MultiTimeframeResult(
        h4=make_context(
            MarketDirection.TRANSITION,
            50,
            LocationType.PULLBACK,
        ),
        h1=make_context(
            MarketDirection.TRANSITION,
            40,
            LocationType.MIDDLE,
        ),
        aligned=False,
    )


def test_priorities_are_returned_in_order():
    plan = WaitActionPlan(
        preferred_side="BUY",
        conditions=[
            WaitCondition.H4_STRUCTURE,
            WaitCondition.H1_STRUCTURE,
            WaitCondition.H1_SUPPORT,
            WaitCondition.MOMENTUM,
        ],
        ready=False,
        reason="Test",
    )

    priorities = WaitPriorityEngine().prioritize(
        plan=plan,
        result=make_result(),
        h4_momentum=make_momentum(
            Momentum.NEUTRAL,
            40,
        ),
        h1_momentum=make_momentum(
            Momentum.NEUTRAL,
            40,
        ),
    )

    assert priorities[0].priority == 1
    assert priorities[-1].priority == 4


def test_neutral_momentum_near_threshold_has_high_priority():
    plan = WaitActionPlan(
        preferred_side="BUY",
        conditions=[
            WaitCondition.MOMENTUM,
            WaitCondition.H4_STRUCTURE,
        ],
        ready=False,
        reason="Test",
    )

    priorities = WaitPriorityEngine().prioritize(
        plan=plan,
        result=make_result(),
        h4_momentum=make_momentum(
            Momentum.NEUTRAL,
            40,
        ),
        h1_momentum=make_momentum(
            Momentum.NEUTRAL,
            40,
        ),
    )

    assert priorities[0].condition == WaitCondition.MOMENTUM


def test_h1_timing_is_prioritized_over_h4_structure():
    plan = WaitActionPlan(
        preferred_side="BUY",
        conditions=[
            WaitCondition.H4_STRUCTURE,
            WaitCondition.H1_SUPPORT,
        ],
        ready=False,
        reason="Test",
    )

    priorities = WaitPriorityEngine().prioritize(
        plan=plan,
        result=make_result(),
    )

    assert priorities[0].condition == WaitCondition.H1_SUPPORT


def test_no_conditions_returns_empty_priorities():
    plan = WaitActionPlan(
        preferred_side="BUY",
        conditions=[],
        ready=True,
        reason="Ready",
    )

    priorities = WaitPriorityEngine().prioritize(
        plan=plan,
        result=make_result(),
    )

    assert priorities == []

def test_bias_alignment_is_highest_priority():
    plan = WaitActionPlan(
        preferred_side=None,
        conditions=[
            WaitCondition.BIAS_ALIGNMENT,
        ],
        ready=False,
        reason="Bias not aligned",
    )

    priorities = WaitPriorityEngine().prioritize(
        plan=plan,
        result=make_result(),
    )

    assert len(priorities) == 1
    assert (
        priorities[0].condition
        == WaitCondition.BIAS_ALIGNMENT
    )
    assert priorities[0].priority == 1
    assert priorities[0].proximity_score == 100
