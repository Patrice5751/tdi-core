from tdi.reporting.explanation import Explanation


class ExplainabilityEngine:
    """Construit les explications à partir des RuleResult."""

    @staticmethod
    def build(rule_results):
        explanations = []

        for result in rule_results:
            explanations.append(
                Explanation(
                    title=result.rule,
                    value=result.score,
                    message=result.message,
                )
            )

        return explanations