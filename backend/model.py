"""Baseline churn model training with explicit labelled targets."""
from dataclasses import dataclass
from typing import Any
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (classification_report, roc_auc_score,
    average_precision_score, precision_score, recall_score, f1_score, confusion_matrix)
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
        raise ValueError(f"Target column '{target}' is missing. Do not infer churn labels.")
    if frame[target].isna().any():
        raise ValueError("Target contains missing values.")
    labels = frame[target]
    if labels.nunique() != 2:
        raise ValueError("Churn target must contain exactly two classes.")
    if int(labels.value_counts().min()) < 2:
        raise ValueError("Each churn class needs at least two records for a stratified split.")
    excluded = {target, "customer_id", "account_id", "name", "email", "phone"}
    features = frame[[c for c in frame.columns if c not in excluded]].copy()
    if features.empty:
        raise ValueError("No usable feature columns remain after excluding identifiers and target.")
    numeric = features.select_dtypes(include=["number", "bool"]).columns.tolist()
    categorical = [c for c in features.columns if c not in numeric]
    transformers = []
    if numeric:
        transformers.append(("numeric", Pipeline([
            ("imputer", SimpleImputer(strategy="median")), ("scale", StandardScaler())
        ]), numeric))
    if categorical:
        transformers.append(("categorical", Pipeline([
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("encode", OneHotEncoder(handle_unknown="ignore"))
        ]), categorical))
    preprocessor = ColumnTransformer(transformers=transformers)
    model = Pipeline([("preprocess", preprocessor),
        ("classifier", LogisticRegression(max_iter=1000, class_weight="balanced"))])
    x_train, x_test, y_train, y_test = train_test_split(
        features, labels, test_size=0.2, random_state=42, stratify=labels)
    model.fit(x_train, y_train)
    predictions = model.predict(x_test)
    probabilities = model.predict_proba(x_test)[:, 1]
    positive_label = model.named_steps["classifier"].classes_[1]
    binary_test = (y_test == positive_label).astype(int)
    metrics = {
        "roc_auc": float(roc_auc_score(binary_test, probabilities)),
        "pr_auc_average_precision": float(average_precision_score(binary_test, probabilities)),
        "precision": float(precision_score(y_test, predictions, pos_label=positive_label, zero_division=0)),
        "recall": float(recall_score(y_test, predictions, pos_label=positive_label, zero_division=0)),
        "f1": float(f1_score(y_test, predictions, pos_label=positive_label, zero_division=0)),
        "positive_label": str(positive_label),
        "class_labels": [str(v) for v in model.named_steps["classifier"].classes_],
        "confusion_matrix": confusion_matrix(y_test, predictions, labels=model.named_steps["classifier"].classes_).tolist(),
        "classification_report": classification_report(y_test, predictions, output_dict=True, zero_division=0),
        "test_rows": int(len(x_test)), "train_rows": int(len(x_train)),
        "model": "LogisticRegression(class_weight=balanced)",
        "note": "Random stratified baseline only. Prefer chronological validation with an agreed observation date and prediction horizon."
    }
    return TrainingResult(model=model, metrics=metrics, feature_columns=features.columns.tolist())
