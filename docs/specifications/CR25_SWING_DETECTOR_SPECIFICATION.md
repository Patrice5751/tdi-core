# CR25 — SwingDetector Specification

Version: 0.11 Draft

---

# 1. Purpose

The SwingDetector identifies significant swing highs and swing lows from OHLC market data.

It does not determine market direction.

It does not classify pivots as HH, HL, LH or LL.

Its only responsibility is to detect meaningful price pivots.

---

# 2. Guiding Principle

Minor price fluctuations must not be interpreted as structural swings.

A detected swing must satisfy:

- a local pivot condition;
- a minimum amplitude condition;
- sufficient confirmation candles.

---

# 3. Input

The engine receives:

- an ordered list of OHLC candles;
- the ATR value associated with the analysed timeframe.

Candles must be ordered from oldest to newest.

Recommended analysis window:

- minimum: 50 candles;
- normal: 100 candles.

---

# 4. Candle Model

Each candle contains:

- index;
- timestamp;
- open;
- high;
- low;
- close.

The first implementation may use only:

- index;
- high;
- low.

---

# 5. Local Pivot Rule

## Swing High

A candle is a swing-high candidate when its high is strictly greater than the highs of:

- the two previous candles;
- the two following candles.

Formally:

Current high > highs of candles -2, -1, +1 and +2.

## Swing Low

A candle is a swing-low candidate when its low is strictly lower than the lows of:

- the two previous candles;
- the two following candles.

Formally:

Current low < lows of candles -2, -1, +1 and +2.

---

# 6. Confirmation Delay

A pivot requires two following candles.

Therefore, a swing cannot be confirmed immediately.

A pivot detected at index N becomes confirmed only after candle N+2 is available.

The last two candles of a dataset cannot be confirmed as swings.

---

# 7. Significant Amplitude

A local pivot is significant only if the associated movement has an amplitude of at least:

0.5 ATR

This filter removes minor fluctuations and market noise.

Initial rule:

- significant swing amplitude >= 0.5 ATR;
- insignificant candidate amplitude < 0.5 ATR.

The exact amplitude calculation will be defined and tested incrementally.

---

# 8. Price Reference

Swing highs are measured using candle highs.

Swing lows are measured using candle lows.

Wicks are therefore included.

Closing prices do not replace highs and lows for pivot detection.

---

# 9. Equal Highs and Equal Lows

The first version uses strict comparisons.

Therefore:

- equal neighbouring highs do not create a confirmed swing high;
- equal neighbouring lows do not create a confirmed swing low.

Equal-level handling may be added later as a plateau or zone rule.

---

# 10. Output

The engine returns a list of detected pivots.

Each pivot contains:

- candle index;
- price;
- pivot type;
- confirmation status;
- optional strength information.

Initial pivot types:

- HIGH;
- LOW.

HH, HL, LH and LL are not assigned by the SwingDetector.

---

# 11. Minimum Structural Sample

The detector may return any number of pivots.

However, another engine should not confirm a market direction without at least:

- 3 significant swing highs;
- 3 significant swing lows.

This requirement belongs to structural interpretation, not pivot detection.

---

# 12. Responsibilities

The SwingDetector does:

- detect local highs;
- detect local lows;
- apply confirmation delay;
- reject pivots below the amplitude threshold;
- return pivots in chronological order.

The SwingDetector does not:

- classify HH, HL, LH or LL;
- determine bullish or bearish direction;
- analyse moving averages;
- analyse H1/H4 coherence;
- detect channels;
- produce a trading decision.

---

# 13. Explainability

Each rejected or accepted pivot should eventually be explainable.

Examples:

- candidate accepted: local high and amplitude 0.72 ATR;
- candidate rejected: amplitude only 0.31 ATR;
- candidate unavailable: insufficient following candles.

The first implementation may omit detailed rejection records.

---

# 14. Initial Test Cases

The first test suite must cover:

1. Detect one clear swing high.
2. Detect one clear swing low.
3. Reject a non-pivot high.
4. Reject a non-pivot low.
5. Ignore the first two candles.
6. Ignore the final two candles.
7. Reject equal neighbouring highs.
8. Reject equal neighbouring lows.
9. Return pivots in chronological order.
10. Reject a pivot below 0.5 ATR.
11. Accept a pivot at exactly 0.5 ATR.
12. Handle an empty candle list.

---

# 15. Future Extensions

Future versions may include:

- configurable pivot width;
- dynamic ATR per candle;
- pivot strength;
- equal-high and equal-low zones;
- minimum time separation;
- adaptive sensitivity;
- volume confirmation;
- multi-timeframe pivot comparison.