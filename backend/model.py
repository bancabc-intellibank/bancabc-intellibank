"""Leakage-conscious baseline churn model training utilities.

Expected input: one row per customer, approved behavioural features, and a binary
'churned' target defined by the hackathon dataset/business rules.
"""
from dataclasses import dataclass
from typing import Any
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

@dataclass
class TrainingResult:
    model: Pipeline
    metrics: dict[str, Any]
    feature_columns: list[str]

def train_churn_baseline(frame: pd.DataFrame, target: str = "churned") -> TrainingResult:
    if target not in frame.columns:
        raise ValueError(f"Target column '{target}' is missing. Do not infer churn labels without an approved definition.")
    if frame[target].isna().any():
        raise ValueError("Target contains missing values.")
    labels = frame[target]
    if labels.nunique() != 2:
        raise ValueError("Churn target must contain exactly two classes for this baseline.")
    excluded = {target, "customer_id", "account_id", "name", "email", "phone"}
    features = frame[[c for c in frame.columns if c not in excluded]].copy()
    if features.empty:
        raise ValueError("No usable feature columns remain after excluding identifiers and target.")
    numeric = features.select_dtypes(include=["number", "bool"]).columns.tolist()
    categorical = [c for c in features.columns if c not in numeric]
    transformers = []
    if numeric:
        transformers.append(("numeric", Pipeline([("imputer", SimpleImputer(strategy="median")), ("scale", StandardScaler())]), numeric))
    if categorical:
        transformers.append(("categorical", Pipeline([("imputer", SimpleImputer(strategy="most_frequent")), ("encode", OneHotEncoder(handle_unknown="ignore"))]), categorical))
    preprocessor = ColumnTransformer(transformers=transformers)
    model = Pipeline([("preprocess", preprocessor), ("classifier", LogisticRegression(max_iter=1000, class_weight="balanced"))])
    x_train, x_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, random_state=42, stratify=labels)
    model.fit(x_train, y_train)
    predictions = model.predict(x_test)
    probabilities = model.predict_proba(x_test)[:, 1]
    metrics = {
        "roc_auc": float(roc_auc_score(y_test, probabilities)),
        "classification_report": classification_report(y_test, predictions, output_dict=True, zero_division=0),
        "test_rows": int(len(x_test)),
        "train_rows": int(len(x_train)),
        "model": "LogisticRegression(class_weight=balanced)",
        "note": "Random stratified split baseline. Prefer a chronological split when event dates and prediction windows are available.",
    }
    return TrainingResult(model=model, metrics=metrics, feature_columns=features.columns.tolist())
