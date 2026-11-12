"""Synthetic demonstration analytics. Replace with validated official challenge data."""
from typing import Any

_DEMO = {
    "overview": {
        "customers_analysed": 16170,
        "high_churn_risk": 1960,
        "high_value_customers": 2840,
        "cross_sell_leads": 3420,
        "data_mode": "synthetic_demo",
    },
    "segments": [
        {"name": "High value", "customers": 2840},
        {"name": "Growing", "customers": 4120},
        {"name": "Regular", "customers": 6380},
        {"name": "At risk", "customers": 1960},
        {"name": "Dormant", "customers": 870},
    ],
    "customers": [
        {"id": "CUS-1048", "segment": "High value", "days_since_activity": 0, "churn_risk": "Low", "engagement_score": 92},
        {"id": "CUS-2081", "segment": "Growing", "days_since_activity": 1, "churn_risk": "Low", "engagement_score": 81},
        {"id": "CUS-3194", "segment": "At risk", "days_since_activity": 28, "churn_risk": "High", "engagement_score": 34},
        {"id": "CUS-4270", "segment": "Regular", "days_since_activity": 4, "churn_risk": "Medium", "engagement_score": 67},
        {"id": "CUS-5112", "segment": "At risk", "days_since_activity": 35, "churn_risk": "High", "engagement_score": 21},
    ],
    "recommendations": [
        {"segment": "High value", "opportunity": "Premium savings or investment products", "rationale": "Strong balances and sustained activity", "priority": "High"},
        {"segment": "Growing", "opportunity": "Personal lending pre-assessment", "rationale": "Increasing transaction frequency", "priority": "Medium"},
        {"segment": "At risk", "opportunity": "Retention outreach and service check-in", "rationale": "Declining activity and long inactivity gaps", "priority": "High"},
    ],
}

def get_overview() -> dict[str, Any]:
    return _DEMO["overview"].copy()

def get_segments() -> list[dict[str, Any]]:
    return list(_DEMO["segments"])

def get_watchlist() -> list[dict[str, Any]]:
    return list(_DEMO["customers"])

def get_recommendations() -> list[dict[str, Any]]:
    return list(_DEMO["recommendations"])
