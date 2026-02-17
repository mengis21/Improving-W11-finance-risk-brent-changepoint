# Presentation Outline - Finance Sector Capstone Walkthrough

Use this as a 10-12 slide structure for your final presentation.

## Slide 1 - Title
- Brent Oil Regime Shift Risk Analytics
- Week 12 Capstone Improvement
- Name, date, GitHub repo

## Slide 2 - Business Context
- Why regime shifts matter in finance
- Stakeholders: risk teams, portfolio managers, analysts
- Cost of delayed detection

## Slide 3 - Problem Statement
- Current pain point: manual and inconsistent shock interpretation
- Goal: transparent and reliable detection of structural breaks

## Slide 4 - Data and Inputs
- Brent daily price series
- Curated geopolitical/policy event dataset
- Data preparation and assumptions

## Slide 5 - Methodology
- Log-return transformation and stationarity rationale
- Bayesian single change point model
- Event alignment strategy (nearest-event mapping)

## Slide 6 - Key Findings
- Posterior median change point and HDI
- Nearest event and temporal gap
- Pre/post 90-day mean price change (-18.74%)

## Slide 7 - Engineering Improvements (Week 12)
- Refactor choices (import-light utility design)
- Test suite expansion (10 tests)
- CI workflow automation

## Slide 8 - Product Demonstration
- Dashboard overview
- Filtered view
- Event/changepoint interpretation panel

## Slide 9 - Reliability and Risk Controls
- Why tests + CI reduce delivery risk
- Reproducibility from clone to run
- Limits of causal claims and uncertainty communication

## Slide 10 - Business Impact
- Faster interpretation of market regimes
- Better support for scenario analysis and hedging reviews
- Improved trust through transparent evidence

## Slide 11 - Limitations and Next Steps
- Multi-change-point extension
- Robust distributions and stress testing
- API integration/performance tests

## Slide 12 - Closing
- Summary of value delivered
- Link to repo and report
- Q&A
