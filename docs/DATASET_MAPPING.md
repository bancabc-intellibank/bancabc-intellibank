# Official dataset mapping checklist

The project currently runs on synthetic demonstration records only. Do not interpret demo metrics as BancABC findings.

When the organisers provide the approved dataset:

1. Record the data dictionary, grain (customer, account, transaction), date range and target definition.
2. Identify stable customer keys and transaction timestamps; document joins and duplicate handling.
3. Map candidate features such as transaction count/value, recency, frequency, channel mix, balance trends, product holdings and service interactions only where supplied and permitted.
4. Confirm whether a churn label exists. Define the prediction horizon with the organisers; do not invent labels from inactivity without documenting the business rule.
5. Separate training, validation and test periods chronologically to avoid leakage.
6. Remove direct identifiers from modelling data; protect raw data and never commit it to Git.
7. Document missing values, outliers, class imbalance, model metrics and limitations.
8. Validate cross-sell rules against actual product eligibility and suitability constraints.

## Required decisions

- What exactly counts as churn, and over what horizon?
- Is the dataset customer-level, account-level, transaction-level, or mixed?
- Which product codes and customer attributes are permitted for analysis?
- What evaluation metric will the judges expect (e.g. recall, precision, PR-AUC, lift, top-k capture)?
