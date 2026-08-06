from dataclasses import dataclass

from tdi.advisor.rule_category import RuleCategory


@dataclass(frozen=True)
class RuleResult:
    category: RuleCategory
    rule: str
    score: int
    max_score: int
    passed: bool
    message: str