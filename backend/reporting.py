"""Executive reporting helpers."""
from datetime import datetime, timezone

def build_executive_report(data):
    overview = data.get("overview", {})
    profile = data.get("profile") or {}
    customers = data.get("customers", [])
    ranked = sorted(customers, key=lambda c: c.get("priority_score", c.get("risk_score", 0)), reverse=True)[:10]
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "data_mode": overview.get("data_mode", "unknown"),
        "summary": {
            "customers_analysed": overview.get("customers_analysed", 0),
            "high_behavioural_risk": overview.get("high_churn_risk", 0),
            "high_value_customers": overview.get("high_value_customers", 0),
            "growth_opportunities": overview.get("cross_sell_leads", 0),
            "transaction_rows": overview.get("transaction_rows")
        },
        "segments": data.get("segments", []),
        "recommended_actions": data.get("recommendations", []),
        "priority_watchlist": [{
            "customer_id": c.get("id"), "segment": c.get("segment"),
            "risk_score": c.get("risk_score"),
            "priority_score": c.get("priority_score", c.get("risk_score")),
            "reason": c.get("reason"), "recommended_action": c.get("action")
        } for c in ranked],
        "data_quality": {
            "missing_values": profile.get("missing_values", {}),
            "duplicate_customer_ids": profile.get("duplicate_customer_ids", 0),
            "quality_warnings": profile.get("quality_warnings", [])
        },
        "interpretation": "Behavioural scores are relative indicators, not calibrated churn probabilities. Validate findings with authorised bank data and business owners."
    }
