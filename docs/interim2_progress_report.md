# Interim 2 Progress Report (Week 12 Capstone Improvement)

**Student:** Kidus Gebremedhin  
**Project:** Improving-W11-finance-risk-brent-changepoint  
**Date:** 2026-02-16

## 1) Original Plan vs Actual Progress

### Original plan (Interim 1)
1. Refactor codebase for maintainability (type hints, modular design, constants).
2. Add unit/integration tests and validate reliability.
3. Configure CI/CD with automated checks and badge.
4. Improve professional documentation and business-impact narrative.
5. Prepare final delivery assets (report/blog + presentation-ready artifacts).

### Actual progress by Interim 2
- Bootstrapped a clean Week 12 capstone repository from Week 11 baseline.
- Added automated test suite with core function coverage.
- Introduced import-light refactor in change point utilities to reduce dependency friction during testing.
- Added GitHub Actions CI pipeline and upgraded README to a portfolio-grade format.
- Created branch-based proof-of-work workflow aligned with prior weeks.

## 2) What Was Completed

### Completed engineering work
- Baseline repository initialized and pushed.
- **Tests added:** 10 pytest tests for:
  - data loading/parsing/sorting (`load_brent_prices`, `load_events`)
  - transformation correctness (`compute_log_returns`)
  - change point utility behavior (`summary_to_dict`, `nearest_event`)
- **Refactor done:** `src/changepoint.py` updated for lazy imports of heavy Bayesian dependencies.
- **CI added:** `.github/workflows/ci.yml` runs pytest on push/pull request.
- **README improved:** clear business problem, solution overview, key results, quick start, project structure, and future improvements.

### Validation evidence
- Local test run output: `10 passed`.
- Branches with committed changes pushed to GitHub.

## 3) What Was Not Completed (Yet) and Why

- End-to-end API integration tests are not complete yet.
  - **Why:** prioritized core unit reliability and CI setup first to establish baseline quality gates.
- Dashboard KPI/latency instrumentation is still pending.
  - **Why:** time was redirected to test architecture and repository migration cleanup.
- Final report/blog and presentation assets are in progress.
  - **Why:** reserved for final submission window after engineering stabilization.

## 4) Revised Plan for Remaining Time

### Monday (2026-02-17)
- Add API integration tests for `/api/health`, `/api/events`, `/api/changepoint`.
- Validate CI passes on main after merges.
- Capture dashboard screenshots showing business impact context.

### Tuesday (2026-02-18) - Final submission prep
- Finalize technical report/blog (finance audience framing).
- Finalize presentation deck (problem, design, decisions, outcomes).
- Submit GitHub link + report/blog + screenshots + presentation.

## 5) GitHub Proof of Work

Repository:
- https://github.com/mengis21/Improving-W11-finance-risk-brent-changepoint

Branches containing Interim-2 work:
- https://github.com/mengis21/Improving-W11-finance-risk-brent-changepoint/tree/task-1-testing-refactor
- https://github.com/mengis21/Improving-W11-finance-risk-brent-changepoint/tree/task-2-ci-readme
- https://github.com/mengis21/Improving-W11-finance-risk-brent-changepoint/tree/task-3-interim2-report

## 6) Notes

- This report is authored in Markdown for version control traceability.
- Export to PDF before form submission.
