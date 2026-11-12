# IntelliBank modelling and evaluation guide

## Behavioural risk scores

The uploaded transaction workflow calculates a relative behavioural risk score from available recency, frequency and transaction-value ranks. The score is designed to help sort a dataset for human review. It is **not** a probability of churn, and its High/Medium/Low bands are not validated customer outcomes.

Recency is measured relative to the latest valid transaction date in the uploaded file. If the file does not include a date column, the score uses frequency and value only. Results depend on the customers included in the uploaded sample.

## Customer action priority

The current prototype combines the relative behavioural risk score (65%) and relative transaction-value percentile (35%) into an action-priority score. This is a transparent ranking heuristic, not customer lifetime value, expected loss or a bank-approved treatment strategy. A bank should review the weighting and add business constraints before operational use.

## Supervised churn baseline

The API endpoint `POST /api/model/evaluate` accepts a UTF-8 CSV with one row per customer and a binary `churned` column. The label must be defined by BancABC or the hackathon organisers, including:
- an observation date,
- a prediction horizon,
- a precise definition of churn,
- features available at the observation date only.

The current baseline uses preprocessing for numeric and categorical features and class-weighted logistic regression. It reports ROC-AUC, average precision (PR-AUC), precision, recall, F1, confusion matrix and a classification report.

The baseline uses a random stratified split for demonstration. For realistic banking data, use chronological validation to avoid future-information leakage. Consider class imbalance, calibration, threshold selection, subgroup performance, drift and independent review. Metrics from a small or synthetic dataset should not be presented as evidence of real bank performance.

The model is trained in memory for the evaluation request only. It is not persisted and is not yet wired into the live behavioural watchlist.

## Cross-sell and campaign scenarios

Segment-level product discovery prompts are not product recommendations validated against bank eligibility rules. Staff must check customer needs, suitability, affordability, consent and applicable policies.

The Impact Simulator uses assumptions supplied by the user: campaign budget, cost per contact, expected retention rate and value per retained customer. The resulting retained-customer count, value and ROI are scenario calculations, not forecasts or guaranteed results.
