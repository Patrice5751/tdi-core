# TDI Score Specification

Version : 0.10 Draft

---

# Purpose

The TDI Score measures the technical quality of a trading setup.

It does NOT decide whether a trade should be taken.

Trade decisions are produced by the Decision Engine.

---

# Score Philosophy

A score represents the probability that a setup is technically sound according to the TDI methodology.

Higher scores indicate higher-quality setups.

The score is independent from money management.

---

# Evaluation Categories

The score is built from three categories.

## 1. Market Context

Question:

"Should I even look for a trade?"

Criteria:

- Trend
- Multi-timeframe alignment
- Market context

---

## 2. Setup Quality

Question:

"How good is this setup?"

Criteria:

- Market structure
- Momentum
- Entry quality
- Pullback quality
- Breakout quality

---

## 3. Execution Safety

Question:

"Can I execute this trade safely?"

Criteria:

- Risk / Reward
- ATR
- Risk management

---

# Score Distribution

| Criterion | Maximum |
|------------|--------:|
| Structure | 25 |
| Trend | 20 |
| Momentum | 15 |
| H4/H1 Alignment | 15 |
| Risk / Reward | 15 |
| ATR | 5 |
| Risk Management | 5 |

Total = 100

---

# Grade Scale

| Score | Grade | Interpretation |
|-------:|:-----:|----------------|
| 95-100 | A+ | Exceptional |
| 90-94 | A | Excellent |
| 80-89 | B | Good |
| 70-79 | C | Acceptable with caution |
| 60-69 | D | Weak |
| <60 | E | Reject |

---

# Blocking Rules

Some rules are mandatory.

A trade cannot be recommended if one of these fails.

Mandatory criteria:

- Trend alignment
- Market structure
- Minimum Risk/Reward

The Decision Engine is responsible for applying blocking rules.

The Score Engine only measures setup quality.

---

# Explainability

Every point of the score must be explainable.

Every lost point must have an explicit reason.

No black-box scoring is allowed.

---

# Future Evolution

Future versions may include:

- Channel quality
- Bias line quality
- Support / Resistance quality
- Economic context
- Statistical calibration

The architecture must remain backward compatible.

---

# Calibration

Initial weights are expert-based.

Future releases will calibrate these weights using the Baseline experimental dataset.

The objective is that the score reflects observed setup quality rather than subjective preference.