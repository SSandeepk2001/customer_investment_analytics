# Interview guide: Customer Acquisition, LTV & Investment Optimization Analytics

## 30-second explanation

I built a portfolio project to evaluate whether customer welcome offers justify their acquisition and incentive costs. I generated a reproducible synthetic prospect dataset, created Python scorecards for offer/market/channel performance, estimated assumption-based 36-month LTV, tested offer conversion-rate differences against a no-offer control, and forecast monthly conversions. A Streamlit dashboard presents the outputs. I also added Hive and BigQuery SQL templates and an optional PySpark aggregation example.

## Business questions answered

1. Which welcome offer has the best observed conversion rate?
2. Does a higher conversion rate also create better economics after incentive spend?
3. How do CPA, projected LTV, LTV:CAC, and projected ROI vary by market, channel, and offer?
4. Is the observed conversion-rate difference statistically significant after adjusting for multiple comparisons?
5. What does a 12-month monthly conversion forecast look like, and how was forecast error checked?

## Metric definitions

- **Conversion rate:** conversions / prospects.
- **Total investment:** marketing spend + incentive spend.
- **CPA:** total investment / conversions.
- **Projected LTV per acquisition:** summed projected 36-month LTV / conversions.
- **LTV:CAC:** projected LTV per acquisition / CPA.
- **Projected ROI:** (projected 36-month LTV − total investment) / total investment.
- **Incremental conversion:** treatment conversion rate minus no-offer conversion rate.
- **Incremental ROI:** (incremental projected LTV per prospect − incremental investment per prospect) / incremental investment per prospect.
- **Hypothesis test:** a two-proportion z-test compares conversion rates; Bonferroni-adjusted p-values account for the two offer comparisons.
- **Forecast error:** MAE, RMSE, and MAPE on the latest six held-out months.

## Illustrative readout from the seeded synthetic dataset

These are generated demo outputs, not real customer or market facts:

- Premium Welcome had the highest observed conversion rate in this simulation (about 14.6%); No Offer had the lowest acquisition cost and highest overall projected ROI.
- The Premium Welcome conversion-rate comparison did not meet the 5% significance threshold after Bonferroni adjustment in this run. Do not claim a statistically confirmed uplift.
- Standard Welcome's incremental estimated value did not cover the additional investment under the project's assumptions. Premium Welcome's incremental estimated value did cover the additional investment in this simulation, but the assumptions and non-significant test mean this is only a hypothesis for further testing—not a real-world recommendation.
- The six-month holdout provides one basic forecast check, not proof that SARIMAX is the best model. A real analysis should compare against seasonal-naive and other benchmarks.

## Questions you should be ready for

**Why use synthetic data?**  
To avoid private/customer data and to make a reproducible portfolio demonstration. Results must not be described as Amex data or business outcomes.

**What are the main limitations of the LTV model?**  
Annual contribution, retention, and discount rate are simulated assumptions. A production model would require validated customer-level contribution margins, attrition/retention curves, servicing and funding costs, cohort definitions, risk controls, and model validation.

**Why can an offer have a higher conversion rate but lower ROI?**  
The incentive increases cost for treated conversions. Incremental value matters: additional contribution from uplift must exceed the extra incentive/acquisition cost.

**What would you improve next?**  
Compare randomization balance, estimate confidence intervals for incremental value, test cohort/market heterogeneity, add sensitivity analysis around retention and discount rate, compare seasonal-naive/ETS/SARIMAX forecasts, monitor forecast drift, and validate on real approved data if permitted.

**What was your contribution?**  
Be ready to walk through your own code, rerun the pipeline, explain every formula, and demonstrate the dashboard live. Don't claim cloud execution, PySpark runtime, or a causal business impact unless you personally execute and verify it.
