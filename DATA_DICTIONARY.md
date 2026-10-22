# Data dictionary

The source CSV is generated from a deterministic synthetic data generator. All values and identifiers are fictional.

| Column | Type | Meaning |
|---|---|---|
| `prospect_id` | string | Unique synthetic prospect ID |
| `cohort_month` | YYYY-MM | Synthetic acquisition cohort month |
| `market` | string | Synthetic international market label |
| `channel` | string | Synthetic acquisition channel |
| `offer_type` | string | No Offer, Standard Welcome, or Premium Welcome |
| `converted` | 0/1 integer | Simulated acquisition outcome |
| `marketing_spend_usd` | float | Simulated marketing cost per prospect |
| `incentive_cost_usd` | float | Simulated incentive cost; zero for non-conversions and no-offer prospects |
| `annual_contribution_usd` | float | Simulated annual contribution proxy; zero for non-conversions |
| `retention_rate_assumption` | float | Simulated retention-rate assumption for converted prospects |
| `active_months_observed` | integer | Simulated observation duration field; zero for non-conversions |
| `projected_ltv_36m_usd` | float | Three-year discounted contribution estimate using assumed retention and a 10% discount rate; zero for non-conversions |

**Model note:** this is an educational proxy, not a validated financial LTV model. Interpret derived ROI and value metrics as examples of an analytics workflow only.
