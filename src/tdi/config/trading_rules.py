"""
Configuration globale des règles de trading de TDI.
Toutes les constantes métier sont définies ici.
"""

# ==========================
# TREND ENGINE
# ==========================

TREND_MAX_SCORE = 90
MIN_CONFIDENCE = 70
TREND_PRICE_BONUS = 20
TREND_NEUTRAL_CONFIDENCE = 40

# ==========================
# MOMENTUM ENGINE
# ==========================

RSI_BUY_THRESHOLD = 55
RSI_SELL_THRESHOLD = 45

RSI_SCORE = 30
MACD_SCORE = 35
HISTOGRAM_SCORE = 35

MOMENTUM_DECISION_THRESHOLD = 50
MOMENTUM_MAX_SCORE = 100


# ==========================
# STRUCTURE ENGINE
# ==========================

STRUCTURE_SUPPORT_SCORE = 30
STRUCTURE_SWING_SCORE = 40
STRUCTURE_RANGE_SCORE = 30

STRUCTURE_MIN_CONFIDENCE = 40

ENTRY_ZONE_SCORE = 60

STRUCTURE_RESISTANCE_SCORE = 30
STRUCTURE_ENTRY_THRESHOLD = 60
STRUCTURE_NEAR_LEVEL_RATIO = 0.20

STRUCTURE_BUY_ZONE = 0.30
STRUCTURE_SELL_ZONE = 0.70
STRUCTURE_MID_ZONE = 0.50

# ==========================
# RISK ENGINE
# ==========================

DEFAULT_RISK = 1.0          # %
MIN_RR = 2.0

# ==========================
# VALIDATION
# ==========================

MIN_CONFIDENCE = 70

# ==========================
# VALIDATION ENGINE
# ==========================

VALIDATION_TREND_SCORE = 30
VALIDATION_MOMENTUM_SCORE = 30
VALIDATION_STRUCTURE_SCORE = 40
VALIDATION_MIN_SCORE = 70

# ==========================
# DECISION ENGINE
# ==========================

DECISION_EXCELLENT = 90
DECISION_GOOD = 80
DECISION_ACCEPTABLE = 70
DECISION_WAIT = 60

DECISION_RR_BONUS = 5
DECISION_TREND_BONUS = 5
