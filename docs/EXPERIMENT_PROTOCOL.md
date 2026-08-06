# TDI Experimental Protocol

Version: 1.0  
Status: Active  
Baseline software version: 0.9.0

---

# 1. Purpose

The purpose of this protocol is to determine whether TDI improves the quality and performance of discretionary trading decisions.

TDI is a decision-support system.

It does not replace the trader.

The trader always makes the final decision.

Official motto:

> Better decisions before better profits.

Method:

> Measure. Explain. Improve.

---

# 2. Primary Research Question

Does the use of TDI improve trading performance through more objective, consistent and disciplined decisions?

The primary performance measure is:

- Expectancy in R per executed trade

Secondary measures are:

- Win Rate
- Profit Factor
- Average Winner in R
- Average Loser in R
- Maximum Drawdown in R
- Rule compliance
- Recommendation accuracy

---

# 3. Baseline

The first experimental baseline is:

- TDI version: 0.9.0
- H4/H1 alignment: recorded but not included in the score
- Decision rules: frozen during the baseline period
- Target sample: 30 analysed opportunities
- Minimum initial review: 10 opportunities
- First meaningful review: 30 opportunities
- Main validation target: 100 opportunities

The baseline must not be modified retrospectively.

---

# 4. Experimental Unit

One analysed trading opportunity equals one observation.

An opportunity must be recorded whether it is:

- executed;
- rejected by TDI;
- rejected by the trader;
- cancelled before execution;
- still unresolved.

A single trade cannot validate or invalidate a rule.

Conclusions must be based on a sufficiently large sample.

---

# 5. Data Recorded Before the Trade

The following information must be frozen before execution:

## Identity

- Trade ID
- Analysis date and time
- TDI version

## Market

- Symbol
- Primary timeframe
- Execution timeframe
- Direction
- H4 trend
- H1 trend
- H4/H1 alignment observed

## Setup

- Entry
- Stop Loss
- Take Profit
- ATR H4
- Planned Risk/Reward
- Capital
- Risk percentage
- Planned monetary risk

## TDI Analysis

- Rule results
- Raw score
- Normalized score
- Decision
- Confidence
- Setup Quality
- Trade Grade
- Assessment
- Strengths
- Weaknesses
- Recommendations
- Confluence observations
- Full report

## Trader Decision

- Executed: Yes / No
- Reason for execution or rejection

These fields must never be changed after the decision.

---

# 6. Data Recorded After the Trade

After the trade is closed, record:

- Execution price
- Exit price
- Exit date and time
- Winner: Yes / No
- Result in R
- Monetary profit or loss
- Exit reason
- Plan respected: Yes / No
- Execution error: Yes / No
- Notes

The outcome completes the record but never replaces the original analysis.

---

# 7. Treatment of Rejected Trades

Rejected opportunities must also be recorded.

When technically possible, their hypothetical outcome should be observed using the original Entry, Stop Loss and Take Profit.

They must remain clearly marked as:

- not executed;
- hypothetical outcome.

Hypothetical results must never be mixed with real executed-trade results when calculating account performance.

They may be used separately to assess the quality of TDI rejection decisions.

---

# 8. Version Control

Every TradeRecord must contain the exact TDI version used for the analysis.

Decision-impacting changes require a new experimental version.

Examples:

- adding a rule;
- changing a rule weight;
- changing score thresholds;
- changing validation logic;
- changing decision or confidence logic;
- integrating H4/H1 alignment into the score.

Non-decision changes may remain within the same version:

- display improvements;
- documentation;
- export formats;
- CLI ergonomics;
- persistence improvements that do not alter calculations.

Historical analyses must never be overwritten by a later version.

---

# 9. Development During the Experiment

Development may continue during the experiment.

The stable experimental version and the development version must remain separate.

Recommended branches:

- `main`: stable version used for real observations;
- `experimental`: development in progress.

A new version may replace the stable version only when:

1. all automated tests pass;
2. the change is documented;
3. the version number is updated;
4. the expected decision impact is defined;
5. a validation hypothesis is recorded.

---

# 10. Primary KPI

## Expectancy

Expectancy is measured in R per executed trade.

It represents the average result produced by one executed trade.

For a completed sample:

`Expectancy = Total R / Number of executed trades`

A positive expectancy does not guarantee the outcome of any individual trade.

It measures performance over a series of trades.

---

# 11. Secondary KPIs

## Win Rate

Percentage of executed trades that close as winners.

## Average Winner

Average positive result in R.

## Average Loser

Average negative result in R.

## Profit Factor

Gross positive R divided by absolute gross negative R.

## Maximum Drawdown

Largest peak-to-trough decline in cumulative R.

## Recommendation Accuracy

Measured separately for:

- accepted trades;
- rejected trades;
- executed trades;
- hypothetical rejected setups.

---

# 12. Experimental Reviews

## After 10 observations

Review only:

- workflow reliability;
- missing data;
- recording errors;
- usability problems.

Do not change business rules based on performance.

## After 30 observations

Produce the first baseline report.

Review:

- sample completeness;
- score distribution;
- decision distribution;
- early KPI values;
- recurring data-quality issues.

Any performance conclusion remains provisional.

## After 100 observations

Conduct the first formal evaluation.

Analyse:

- Expectancy by score range;
- performance by instrument;
- performance by direction;
- performance by setup type;
- performance with and without H4/H1 alignment;
- accuracy of TDI acceptance and rejection decisions.

## After 200 to 300 observations

Consider rule recalibration only if the evidence is consistent and economically meaningful.

---

# 13. Rule Validation

Each new rule is treated as a hypothesis.

Example:

> H4/H1 trend alignment improves Expectancy and reduces drawdown.

Each hypothesis must define:

- purpose;
- expected effect;
- affected KPI;
- software version;
- target sample;
- comparison method;
- acceptance criteria.

Possible states:

- Experimental
- Observed
- Validated
- Optimized
- Under Review
- Deprecated
- Rejected

No rule may be modified because of one isolated trade.

---

# 14. Bias Controls

The experiment must avoid:

- cherry-picking;
- deleting losing observations;
- changing the initial score after the outcome;
- changing Entry, SL or TP retrospectively;
- mixing real and hypothetical results;
- combining different TDI versions without identification;
- modifying several major rules simultaneously when their effects must be measured separately;
- drawing conclusions from a very small sample.

---

# 15. Risk Controls

The experimental phase does not justify increasing risk.

Risk per trade should remain stable during the baseline whenever possible.

Any change in risk policy must be documented because it affects monetary performance and drawdown.

TDI remains an aid to decision-making and does not guarantee profitability.

---

# 16. Baseline Completion Criteria

The initial baseline is complete when:

- at least 30 opportunities have been analysed;
- every opportunity has a complete pre-trade record;
- all closed trades have a TradeOutcome;
- executed and rejected opportunities are distinguished;
- the TDI version is recorded;
- KPI calculations are reproducible;
- no retrospective modification has occurred.

---

# 17. Final Decision

At the end of each experimental phase, the conclusion must be one of:

- Keep the current rule or version;
- Continue observation;
- Modify and retest;
- Deprecate;
- Reject.

The decision must be supported by documented evidence.

---

# 18. Golden Rule

> Never modify TDI because of one trade.

Modify TDI only when objective evidence justifies the change.

---

# 19. Experimental Workflow

1. Identify a trading opportunity on MT5.
2. Record the setup before execution.
3. Run TDI.
4. Freeze the analysis and report.
5. Record the trader's decision.
6. Execute manually on MT5 when approved.
7. Record the outcome after closure.
8. Update the journal.
9. Recalculate the experimental dashboard.
10. Review only at predefined milestones.

---

# 20. Current Baseline

- Version: TDI 0.9.0
- Status: Ready for initial field validation
- Target: 30 analysed opportunities
- H4/H1 alignment: observed, not scored
- Automatic MT5 integration: not active
- Execution: manual
- Final decision: trader
