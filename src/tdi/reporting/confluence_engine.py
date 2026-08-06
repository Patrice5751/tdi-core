from tdi.reporting.confluence_rules.high_conviction_rule import (
    HighConvictionRule,
)
from tdi.reporting.confluence_rules.missing_momentum_rule import (
    MissingMomentumRule,
)

from tdi.reporting.confluence_rules.poor_risk_reward_rule import (
    PoorRiskRewardRule,
)

class ConfluenceEngine:

    @staticmethod
    def build(results):
        observations = []

        for rule in (
            HighConvictionRule,
            MissingMomentumRule,
        ):
            observation = rule.build(results)

            if observation is not None:
                observations.append(observation)

        return observations

class ConfluenceEngine:

    @staticmethod
    def build(results):
        observations = []

        for rule in (
            HighConvictionRule,
            MissingMomentumRule,
            PoorRiskRewardRule,
        ):
            observation = rule.build(results)

            if observation is not None:
                observations.append(observation)

        return observations