# Churn modelling plan

## Baseline implemented

`backend/model.py` provides a scikit-learn preprocessing and logistic-regression baseline. It:

- Requires an explicit binary `churned` target column.
- Excludes direct identifiers from features.
- Imputes missing numeric/categorical values and one-hot encodes categories.
- Uses class weighting and reports ROC-AUC plus a classification report.

## Before training on the competition data

- Confirm the organiser's churn definition, observation date and prediction horizon.
- Ensure all features are available before the prediction date; remove post-outcome leakage.
- Prefer chronological train/validation/test splits for time-based customer behaviour.
- Evaluate precision, recall, PR-AUC, lift and top-k capture in addition to ROC-AUC, especially if churn is rare.
- Review false positives/negatives with business stakeholders and calibrate thresholds to campaign capacity.
- Document feature meaning, limitations, fairness/privacy checks and reproducibility.

The model is a starting baseline, not a claim of production readiness or measured BancABC performance.
