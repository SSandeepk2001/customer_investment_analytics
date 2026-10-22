# Customer Acquisition, LTV & Investment Optimization Analytics

**Portfolio project tailored to the American Express Analyst – Data Science job description.** This is a learning/demo project built with fictional synthetic data. It is **not** American Express data, a representation of Amex processes, or a production-ready financial model.

## Business problem

Marketing teams need to assess whether welcome offers produce enough incremental customer value to justify incentive spend. This project measures acquisition KPIs and compares offer types across markets and channels, estimates assumption-based 36-month customer LTV, evaluates offer conversion differences, and forecasts monthly conversions.

## What it delivers

- **Customer LTV & profitability lens:** assumption-based 36-month projected LTV, acquisition investment, cost per acquisition (CPA), LTV:CAC, and projected ROI.
- **Offer/incentive optimization:** compares `No Offer`, `Standard Welcome`, and `Premium Welcome`; calculates incremental outcomes against the no-offer control.
- **Statistical testing:** two-proportion z-tests on conversion rates with a Bonferroni adjustment for two comparisons.
- **Forecasting:** 12-month monthly-conversion forecast using SARIMAX, a six-month holdout backtest, MAE/RMSE/MAPE metrics, and non-negative forecast intervals.
- **Business scorecards:** offer, international market, channel, and monthly KPI outputs.
- **Data engineering/SQL examples:** a PySpark aggregation script plus Hive SQL and BigQuery Standard SQL templates.
- **Interactive dashboard:** Streamlit + Plotly views for scorecards, conversion trends, forecast, and hypothesis-test results.

## Architecture

```text
src/generate_data.py
        |
        v
data/synthetic_prospects.csv
        |
        v
src/run_analysis.py --------------------> outputs/*.csv
        |                                      |
        +--> SARIMAX forecasting               +--> app.py (Streamlit dashboard)
        +--> hypothesis tests                  +--> SQL examples in sql/
        +--> offer and market scorecards       +--> optional PySpark example
```

## Dataset

The generator creates **24,000 fictional prospect records**, distributed across **36 monthly cohorts**, **5 markets**, **4 channels**, and **3 offer types**. It is deterministic (seed 42) so outputs can be reproduced. Offer assignments are balanced for portfolio experimentation but do not reproduce a real experiment or real customer population.

Main fields include:

| Field | Description |
|---|---|
| `prospect_id` | Synthetic unique prospect ID |
| `cohort_month` | Synthetic month assigned to the prospect |
| `market`, `channel`, `offer_type` | Synthetic analysis dimensions |
| `converted` | Synthetic binary acquisition outcome |
| `marketing_spend_usd` | Simulated marketing cost per prospect |
| `incentive_cost_usd` | Simulated offer cost when conversion occurs |
| `annual_contribution_usd` | Simulated annual contribution for converted customers |
| `retention_rate_assumption` | Synthetic retention assumption |
| `projected_ltv_36m_usd` | Discounted, assumptions-based contribution projection over three years |

All monetary amounts are illustrative USD values. The LTV model assumes the annual contribution proxy persists at a declining retention rate over three years and discounts future years at 10%. These inputs are generated for demonstration, not estimated from real customer records. Projected ROI is `(projected LTV − total acquisition/incentive investment) / total investment`; it should not be confused with realized profit or causal return.

## Run locally

Python 3.10+ is recommended.

```bash
# 1. Create and activate a virtual environment (optional but recommended)
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# macOS/Linux:
# source .venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Generate data and all analytical outputs
python run_project.py

# 4. Launch the dashboard
streamlit run app.py

# 5. Run checks
python -m pytest -q
```

If you only need the CSV outputs, steps 1–3 are sufficient. `pyspark` is an optional dependency for `src/pyspark_pipeline.py`; it is separate from the main pandas pipeline. To run that optional path, install `requirements-pyspark.txt` instead of `requirements.txt`.

## Outputs

- `outputs/offer_roi_scorecard.csv` — offer-level conversions, CPA, average LTV per acquisition, LTV:CAC, and projected ROI
- `outputs/offer_incrementality.csv` — offer vs no-offer estimates of incremental conversions, LTV, investment, and incremental cost
- `outputs/offer_hypothesis_tests.csv` — conversion-rate z-tests and adjusted p-values
- `outputs/market_kpi_scorecard.csv` and `outputs/channel_kpi_scorecard.csv` — segment scorecards
- `outputs/monthly_kpi_actuals.csv` — historical synthetic monthly acquisition KPIs
- `outputs/conversion_kpi_forecast_12m.csv` — 12-month forecast plus model intervals
- `outputs/forecast_backtest_metrics.csv` — latest six-month holdout error metrics
- `outputs/customer_ltv_detail.csv` — synthetic customer-level projected-LTV detail for converted records
- `outputs/run_summary.csv` — run-level dataset summary

## SQL and cloud practice

- `sql/hive_customer_investment.hql` contains a Hive aggregation example. Load the CSV into a Hive table before executing it.
- `sql/bigquery_customer_investment.sql` contains BigQuery Standard SQL. Replace `project.dataset.synthetic_prospects` with the table you upload into your own BigQuery project. Cloud execution/deployment is **not** included in this package.
- `src/pyspark_pipeline.py` contains an optional PySpark offer-scorecard aggregation, separate from the main pandas pipeline.

## Analytical caveats

1. The data and measured effects are simulated; results cannot support real investment decisions.
2. Conversion z-tests only test a difference in conversion proportions. They do not prove profit impact or causal outcomes in a real environment.
3. Forecasts are illustrative. For production work, compare SARIMAX against seasonal-naive and other baselines, check residuals and structural breaks, and validate forecast stability.
4. The synthetic LTV estimate is a simplified assumption-based proxy. A real LTV/profitability model would require validated contribution, cost, retention, discounting, and cohort definitions.
5. No Amex affiliation, confidential data, or proprietary methods are implied.

## Resume guidance

Only list tools and components you have personally run and can explain in an interview. In particular, run the main pipeline and dashboard, inspect the output CSVs, and only claim hands-on PySpark/BigQuery/Hive execution after running those components yourself.
