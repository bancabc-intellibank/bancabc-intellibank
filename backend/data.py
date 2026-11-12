"""Dataset loading and validation helpers for approved customer-level CSV data."""
from pathlib import Path
import pandas as pd

REQUIRED_FOR_BASELINE = {"customer_id"}

def load_customer_csv(path: str | Path) -> pd.DataFrame:
    file_path = Path(path)
    if not file_path.exists():
        raise FileNotFoundError(f"Dataset not found: {file_path}")
    if file_path.suffix.lower() != ".csv":
        raise ValueError("The initial pipeline accepts CSV files only.")
    frame = pd.read_csv(file_path)
    missing = REQUIRED_FOR_BASELINE - set(frame.columns)
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(sorted(missing))}")
    if frame.empty:
        raise ValueError("Dataset contains no rows.")
    if frame["customer_id"].isna().any():
        raise ValueError("customer_id contains missing values.")
    return frame

def dataset_profile(frame: pd.DataFrame) -> dict:
    return {
        "rows": int(len(frame)),
        "columns": list(frame.columns),
        "missing_values": {str(k): int(v) for k, v in frame.isna().sum().items()},
        "duplicate_customer_ids": int(frame["customer_id"].duplicated().sum()),
    }
