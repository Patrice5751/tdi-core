from tdi.advisor.atr_rule import ATRRule
from tdi.advisor.momentum_rule import MomentumRule
from tdi.advisor.risk_rule import RiskRule
from tdi.advisor.rr_rule import RRRule
from tdi.advisor.structure_rule import StructureRule
from tdi.advisor.trend_rule import TrendRule


RULES = [
    TrendRule,
    MomentumRule,
    StructureRule,
    RRRule,
    RiskRule,
    ATRRule,
]