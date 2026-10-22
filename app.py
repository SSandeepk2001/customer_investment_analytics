"""Streamlit dashboard for synthetic customer investment analytics."""
from pathlib import Path
import pandas as pd
import plotly.express as px
import streamlit as st

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "outputs"

st.set_page_config(page_title="Customer Investment Analytics", layout="wide")
st.title("Customer Acquisition, LTV & Investment Optimization")
st.caption("Portfolio demo using fictional synthetic data only — not American Express data or production forecasts.")

required = ["offer_roi_scorecard.csv", "market_kpi_scorecard.csv", "monthly_kpi_actuals.csv",
            "conversion_kpi_forecast_12m.csv", "offer_hypothesis_tests.csv", "offer_incrementality.csv"]
if not all((OUT / f).exists() for f in required):
    st.warning("Run `python run_project.py` first to generate analysis outputs.")
    st.stop()

offers = pd.read_csv(OUT / "offer_roi_scorecard.csv")
markets = pd.read_csv(OUT / "market_kpi_scorecard.csv")
monthly = pd.read_csv(OUT / "monthly_kpi_actuals.csv")
forecast = pd.read_csv(OUT / "conversion_kpi_forecast_12m.csv")
tests = pd.read_csv(OUT / "offer_hypothesis_tests.csv")
incrementality = pd.read_csv(OUT / "offer_incrementality.csv")

market_options = ["All"] + sorted(markets["market"].astype(str).unique().tolist())
selected_market = st.sidebar.selectbox("Market filter", market_options)
if selected_market != "All":
    # Market filter is appropriate for the market card; offer chart is kept all-market for context.
    markets_view = markets[markets["market"] == selected_market]
    st.sidebar.info("Offer and monthly charts show all markets; use the market table for the selected market.")
else:
    markets_view = markets

total_prospects = int(monthly["prospects"].sum())
total_conversions = int(monthly["conversions"].sum())
conversion_rate = total_conversions / total_prospects if total_prospects else 0
investment = float(monthly["total_investment_usd"].sum())
ltv_value = float(monthly["projected_ltv_usd"].sum())
roi = (ltv_value - investment) / investment if investment else 0

c1, c2, c3, c4 = st.columns(4)
c1.metric("Prospects", f"{total_prospects:,}")
c2.metric("Conversions", f"{total_conversions:,}")
c3.metric("Conversion rate", f"{conversion_rate:.1%}")
c4.metric("Projected ROI", f"{roi:.1%}")
st.caption("ROI is calculated from assumptions-based projected 36-month LTV less acquisition/incentive investment; it is not realized financial performance.")

left, right = st.columns(2)
with left:
    st.subheader("Offer-level investment scorecard")
    st.dataframe(offers[["offer_type", "prospects", "conversions", "conversion_rate", "cost_per_acquisition_usd", "ltv_per_acquisition_usd", "ltv_to_cac_ratio", "projected_roi"]].style.format({
        "conversion_rate": "{:.1%}", "cost_per_acquisition_usd": "${:,.2f}", "ltv_per_acquisition_usd": "${:,.2f}",
        "ltv_to_cac_ratio": "{:.2f}x", "projected_roi": "{:.1%}"}), use_container_width=True)
    st.plotly_chart(px.bar(offers, x="offer_type", y="conversion_rate", title="Conversion rate by welcome offer",
                           labels={"offer_type": "Offer", "conversion_rate": "Conversion rate"}), use_container_width=True)
with right:
    st.subheader("Market KPI scorecard")
    st.dataframe(markets_view[["market", "prospects", "conversions", "conversion_rate", "cost_per_acquisition_usd", "projected_roi"]].style.format({
        "conversion_rate": "{:.1%}", "cost_per_acquisition_usd": "${:,.2f}", "projected_roi": "{:.1%}"}), use_container_width=True)
    st.plotly_chart(px.bar(markets, x="market", y="projected_roi", title="Projected ROI by market",
                           labels={"market": "Market", "projected_roi": "Projected ROI"}), use_container_width=True)

st.subheader("Monthly conversions: actuals and 12-month forecast")
hist = monthly[["month", "conversions"]].copy().rename(columns={"conversions": "conversions_or_forecast"})
hist["series"] = "Actual synthetic data"
fc = forecast[["month", "forecast_conversions"]].copy().rename(columns={"forecast_conversions": "conversions_or_forecast"})
fc["series"] = "Forecast"
plot_df = pd.concat([hist, fc], ignore_index=True)
st.plotly_chart(px.line(plot_df, x="month", y="conversions_or_forecast", color="series", markers=True,
                        title="Acquisition conversion forecast (illustrative)", labels={"month": "Month", "conversions_or_forecast": "Conversions"}),
                use_container_width=True)
st.dataframe(forecast, use_container_width=True)

st.subheader("Welcome-offer hypothesis tests")
st.caption("Two-proportion z-tests compare each offer with No Offer. Bonferroni-adjusted p-values account for two comparisons; results are synthetic.")
st.dataframe(tests[["treatment_group", "control_conversion_rate", "treatment_conversion_rate", "absolute_lift_pp", "relative_lift_pct", "p_value_bonferroni", "significant_at_5pct", "interpretation"]].style.format({
    "control_conversion_rate": "{:.2%}", "treatment_conversion_rate": "{:.2%}", "absolute_lift_pp": "{:.2f}",
    "relative_lift_pct": "{:.1f}%", "p_value_bonferroni": "{:.4f}"}), use_container_width=True)

st.download_button("Download offer scorecard CSV", data=(OUT / "offer_roi_scorecard.csv").read_bytes(), file_name="offer_roi_scorecard.csv", mime="text/csv")


st.subheader("Offer incrementality vs No Offer control")
st.caption("Incremental cost/value metrics are per-prospect comparisons scaled to the control group size. They are assumption-driven and synthetic.")
st.dataframe(incrementality[["treatment_offer", "incremental_conversions_at_control_volume", "incremental_ltv_per_prospect_usd", "incremental_investment_per_prospect_usd", "incremental_cost_per_incremental_conversion_usd", "incremental_roi"]].style.format({
    "incremental_conversions_at_control_volume": "{:.1f}", "incremental_ltv_per_prospect_usd": "${:,.2f}",
    "incremental_investment_per_prospect_usd": "${:,.2f}", "incremental_cost_per_incremental_conversion_usd": "${:,.2f}", "incremental_roi": "{:.1%}"}), use_container_width=True)
