"""Customer analytics engine with synthetic fallback and CSV-driven analysis.

All risk scores are behavioural heuristics unless an explicitly labelled churn
model is trained on an approved target. No probability of churn is claimed here.
"""
from __future__ import annotations
from io import StringIO
from typing import Any
import pandas as pd
import numpy as np

_DEMO = {
    "customers_analysed": 16170, "high_churn_risk": 1960,
    "high_value_customers": 2840, "cross_sell_leads": 3420,
    "data_mode": "synthetic_demo", "currency_note": "Amounts use the dataset's original units."
}
_current: dict[str, Any] | None = None

def _find(columns, hints):
    lower = {str(c).lower().replace(" ", "_"): c for c in columns}
    for hint in hints:
        for key, original in lower.items():
            if hint in key:
                return original
    return None

def analyse_csv(csv_text: str) -> dict[str, Any]:
    global _current
    if len(csv_text.encode("utf-8")) > 15 * 1024 * 1024:
        raise ValueError("CSV exceeds the 15 MB prototype upload limit.")
    frame = pd.read_csv(StringIO(csv_text))
    if frame.empty or len(frame.columns) < 2:
        raise ValueError("The CSV must contain records and at least two columns.")
    id_col = _find(frame.columns, ["customer_id", "customerid", "client_id", "account_id", "clientid"])
    date_col = _find(frame.columns, ["transaction_date", "txn_date", "date", "timestamp", "trans_date"])
    amount_col = _find(frame.columns, ["amount", "transaction_value", "txn_amount", "value", "credit"])
    type_col = _find(frame.columns, ["transaction_type", "txn_type", "product", "channel", "category"])
    if not id_col:
        raise ValueError("Could not identify a customer identifier. Include a column such as customer_id or account_id.")
    missing_customer_ids = int(frame[id_col].isna().sum())
    frame = frame.dropna(subset=[id_col]).copy()
    if frame.empty:
        raise ValueError("No rows have a usable customer identifier.")
    frame[id_col] = frame[id_col].astype(str)
    invalid_amounts = 0
    invalid_dates = 0
    if amount_col:
        parsed_amounts = pd.to_numeric(frame[amount_col], errors="coerce")
        invalid_amounts = int((frame[amount_col].notna() & parsed_amounts.isna()).sum())
        frame[amount_col] = parsed_amounts.fillna(0)
    if date_col:
        parsed_dates = pd.to_datetime(frame[date_col], errors="coerce", utc=True)
        invalid_dates = int((frame[date_col].notna() & parsed_dates.isna()).sum())
        frame[date_col] = parsed_dates
    today = frame[date_col].max() if date_col and frame[date_col].notna().any() else pd.Timestamp.now(tz="UTC")
    grouped = frame.groupby(id_col, dropna=True)
    rows = []
    for cid, g in grouped:
        valid_dates = g[date_col].dropna() if date_col else pd.Series(dtype="datetime64[ns, UTC]")
        recency = max(0, int((today - valid_dates.max()).days)) if len(valid_dates) else None
        frequency = int(len(g))
        spend = float(g[amount_col].clip(lower=0).sum()) if amount_col else 0.0
        avg = float(g[amount_col].mean()) if amount_col else 0.0
        rows.append({"id": str(cid), "transactions": frequency, "amount": spend,
                     "average_transaction": avg, "days_inactive": recency})
    customers = pd.DataFrame(rows)
    n = len(customers)
    # Percentile-based RFM-style segmentation, robust for small samples.
    rec = customers["days_inactive"].fillna(0) if date_col else pd.Series(0, index=customers.index)
    freq_rank = customers["transactions"].rank(pct=True)
    value_rank = customers["amount"].rank(pct=True) if amount_col else freq_rank
    rec_rank = 1 - rec.rank(pct=True) if date_col else pd.Series(.5, index=customers.index)
    value_score = (freq_rank * .35 + value_rank * .4 + rec_rank * .25)
    if date_col:
        risk_score = (rec.rank(pct=True) * 55 + (1-freq_rank) * 25 + (1-value_rank) * 20).round().astype(int)
        risk_score = risk_score.clip(0,100)
    else:
        risk_score = ((1-freq_rank) * 55 + (1-value_rank) * 45).round().astype(int).clip(0,100)
    customers["risk_score"] = risk_score
    customers["risk"] = np.where(risk_score >= 70, "High", np.where(risk_score >= 40, "Medium", "Low"))
    customers["segment"] = np.where((value_score >= .8), "High value",
        np.where((risk_score >= 70) & (rec >= 30 if date_col else True), "At risk",
        np.where(freq_rank >= .7, "Loyal", np.where(freq_rank <= .25, "Growing", "Regular"))))
    customers["engagement_score"] = (100-risk_score).astype(int)
    customers["priority_score"] = (risk_score * .65 + value_rank * 100 * .35).round().clip(0,100).astype(int)
    def reason(r):
        bits=[]
        if date_col and pd.notna(r["days_inactive"]) and r["days_inactive"] >= 21: bits.append(f'{int(r["days_inactive"])} days since last transaction')
        if r["transactions"] <= max(1, int(customers["transactions"].median())): bits.append("below/near-median transaction frequency")
        if amount_col and r["amount"] <= customers["amount"].median(): bits.append("below/near-median transaction value")
        return "; ".join(bits[:3]) or "relative behavioural indicators within this dataset"
    customers["reason"] = customers.apply(reason, axis=1)
    customers["action"] = np.where(customers["risk"]=="High", "Retention outreach and service check-in",
        np.where(customers["segment"]=="High value", "Relationship review and relevant premium services",
        "Engagement and relevant product education"))
    customers = customers.sort_values(["priority_score","risk_score","amount"], ascending=[False,False,False]).reset_index(drop=True)
    customers["priority_rank"] = np.arange(1, len(customers) + 1)
    segment_counts = customers["segment"].value_counts()
    risk_counts = customers["risk"].value_counts()
    recommendations = []
    for seg, count in segment_counts.items():
        subset=customers[customers.segment==seg]
        if seg=="At risk": offer="Retention outreach"; rationale="Prioritise customers with the highest behavioural risk scores."
        elif seg=="High value": offer="Relationship review"; rationale="Explore relevant premium services based on demonstrated activity and value."
        elif seg=="Growing": offer="Savings and engagement education"; rationale="Build engagement with customers showing developing activity."
        elif seg=="Loyal": offer="Relevant product discovery"; rationale="Explore additional services only where eligibility and customer needs fit."
        else: offer="Personalised engagement"; rationale="Use observed activity to guide a relevant service conversation."
        recommendations.append({"segment":seg,"customers":int(count),"opportunity":offer,"rationale":rationale,"priority":"High" if seg=="At risk" else "Medium"})
    _current = {
        "overview":{"customers_analysed":n,"high_churn_risk":int((customers.risk=="High").sum()),
            "high_value_customers":int((customers.segment=="High value").sum()),
            "cross_sell_leads":int(customers.segment.isin(["Growing","Loyal"]).sum()),
            "transaction_rows":int(len(frame)),"data_mode":"uploaded_csv",
            "currency_note":"Amounts are shown in the dataset's original units; currency is not inferred."},
        "segments":[{"name":str(k),"customers":int(v)} for k,v in segment_counts.items()],
        "customers":[{"id":r.id,"segment":r.segment,"days_since_activity":int(r.days_inactive) if pd.notna(r.days_inactive) else None,
            "churn_risk":r.risk,"risk_score":int(r.risk_score),"engagement_score":int(r.engagement_score),
            "priority_score":int(r.priority_score),"priority_rank":int(r.priority_rank),
            "transactions":int(r.transactions),"total_value":round(float(r.amount),2),
            "reason":r.reason,"action":r.action} for r in customers.head(500).itertuples()],
        "recommendations":recommendations,
        "profile":{"rows":int(len(frame)),"columns":[str(c) for c in frame.columns],
            "missing_values":{str(k):int(v) for k,v in frame.isna().sum().items()},
            "duplicate_customer_ids":int(frame[id_col].duplicated().sum()),
            "duplicate_transaction_rows":int(frame.duplicated().sum()),
            "missing_customer_ids":missing_customer_ids,
            "invalid_dates":invalid_dates,
            "invalid_amounts":invalid_amounts,
            "quality_warnings":([f"{int(frame.duplicated().sum())} exact duplicate transaction rows detected."] if frame.duplicated().sum() else []) + ([f"{missing_customer_ids} rows with missing customer IDs were excluded."] if missing_customer_ids else []) + ([f"{invalid_dates} invalid transaction dates were found."] if invalid_dates else []) + ([f"{invalid_amounts} invalid transaction amounts were treated as zero."] if invalid_amounts else []),
            "detected_fields":{"customer_id":str(id_col),"transaction_date":str(date_col) if date_col else None,
            "amount":str(amount_col) if amount_col else None,"type_or_channel":str(type_col) if type_col else None}},
        "trend":[{"period":"Uploaded dataset","transactions":int(len(frame)),"customers":n}],
        "insights":[
            f'{int((customers.risk=="High").sum())} customers have high relative behavioural risk in this dataset.',
            f'{int((customers.segment=="High value").sum())} customers fall in the high-value behavioural segment.',
            f'{int(customers.transactions.sum())} transaction records were analysed across {n} customers.',
            "Risk scores are heuristic rankings, not trained churn probabilities. Confirm churn labels and prediction horizon before model training."
        ],
        "mode_note":"CSV analysis uses behavioural heuristics. A supervised churn model requires an organiser-approved churn label and prediction window."
    }
    return _current

def get_data():
    if _current is not None: return _current
    return {
      "overview":{**_DEMO},
      "segments":[{"name":"High value","customers":2840},{"name":"Growing","customers":4120},{"name":"Regular","customers":6380},{"name":"At risk","customers":1960},{"name":"Dormant","customers":870}],
      "customers":[
        {"id":"CUS-1048","segment":"High value","days_since_activity":0,"churn_risk":"Low","risk_score":8,"engagement_score":92,"priority_score":40,"priority_rank":1,"transactions":44,"total_value":8200,"reason":"Consistent recent activity and high relative value","action":"Relationship review"},
        {"id":"CUS-2081","segment":"Growing","days_since_activity":1,"churn_risk":"Low","risk_score":19,"engagement_score":81,"priority_score":35,"priority_rank":2,"transactions":25,"total_value":2300,"reason":"Recent activity and increasing engagement","action":"Engagement and product education"},
        {"id":"CUS-3194","segment":"At risk","days_since_activity":28,"churn_risk":"High","risk_score":87,"engagement_score":13,"priority_score":83,"priority_rank":3,"transactions":3,"total_value":160,"reason":"28 days inactive; low transaction frequency and value","action":"Retention outreach and service check-in"},
        {"id":"CUS-4270","segment":"Regular","days_since_activity":4,"churn_risk":"Medium","risk_score":52,"engagement_score":48,"priority_score":50,"priority_rank":4,"transactions":12,"total_value":900,"reason":"Moderate activity relative to this sample","action":"Personalised engagement"},
        {"id":"CUS-5112","segment":"At risk","days_since_activity":35,"churn_risk":"High","risk_score":94,"engagement_score":6,"priority_score":88,"priority_rank":5,"transactions":2,"total_value":80,"reason":"35 days inactive; low transaction frequency and value","action":"Retention outreach and service check-in"}],
      "recommendations":[{"segment":"At risk","customers":1960,"opportunity":"Retention outreach","rationale":"Illustrative demo rule: declining activity and long inactivity gaps.","priority":"High"},{"segment":"High value","customers":2840,"opportunity":"Relationship review","rationale":"Illustrative demo rule: strong relative transaction value.","priority":"Medium"}],
      "profile":None,"trend":[{"period":"Demo sample","transactions":31200,"customers":16170}],
      "insights":["Synthetic demonstration records are loaded.","Upload a CSV to calculate metrics from your own data.","No supervised churn model has been trained."],
      "mode_note":"Synthetic demonstration only. Upload CSV to calculate behavioural analytics."
    }

def get_overview(): return get_data()["overview"]
def get_segments(): return get_data()["segments"]
def get_watchlist(): return get_data()["customers"]
def get_recommendations(): return get_data()["recommendations"]
