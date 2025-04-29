# sdm-cit-case-study: Case 1 & Case 2

## Overview
This repository contains the complete solution for Case 1 and Case 2:
- **Case 1**: Forecast the initial 15-week demand for the new Superman Plus product.
- **Case 2**: Strategically allocate constrained Material A across multiple programs with clear prioritization.

## Structure
- `/case1_forecast/`
  - `case1_forecast_script.py`
  - `case1_forecast_with_tech_sensitivity.csv`
  - `case1_forecast_without_tech_sensitivity.csv`
  - `case1_methodology_summary.md`
- `/case2_allocation/`
  - `case2_allocation_script.py`
  - `case2_allocation.csv`
  - `case2_methodology_summary.md`
- `/dashboard/`
  - `streamlit_app.py`

## Case 1: Demand Forecasting
- Predict the weekly demand for Superman Plus over the first 15 weeks post-launch.
- Consider seasonality, price elasticity, and linearity smoothing techniques.
- Applied light 3-week smoothing to preserve realistic demand fluctuations.
- Detailed methodology in `case1_methodology_summary.md`.

## Case 2: Material Allocation
- Prioritize PAC Reseller Partner fulfillment during Jan Wk4 promotion.
- Allocate remaining material proportionally to Superman and Superman Mini.
- Superman Plus (non-PAC channels) receives no allocation due to supply constraints.
- Detailed methodology in `case2_methodology_summary.md`.

## Methodologies
- Data-driven proportional and priority-based allocation.
- Demand forecasting incorporating elasticity and seasonality factors.
- Ceiling rounding to ensure no fractional units.

## Metrics Monitored
- PAC Reseller Fill Rate
- Program Coverage Ratios
- Risk Mitigation Planning
- Shortage Management Tactics

## How to Run
```bash
pip install -r requirements.txt
python case1_forecast/case1_forecast_script.py
python case2_allocation/case2_allocation_script.py
streamlit run dashboard/streamlit_app.py
