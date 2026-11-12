"""Aggregate-only campaign feedback loop (in-memory prototype; no customer identifiers)."""
_records = []

def record_outcome(name, contacted, retained, campaign_cost, value_per_retained_customer, expected_retention_rate):
    if contacted <= 0 or retained < 0 or retained > contacted:
        raise ValueError("Retained customers must be between zero and contacted customers; contacts must be positive.")
    if campaign_cost < 0 or value_per_retained_customer < 0:
        raise ValueError("Campaign cost and retained-customer value must be non-negative.")
    if not 0 <= expected_retention_rate <= 100:
        raise ValueError("Expected retention rate must be between 0 and 100.")
    actual_rate = retained / contacted * 100
    actual_value = retained * value_per_retained_customer
    net_value = actual_value - campaign_cost
    record = {"campaign_name": name, "customers_contacted": contacted,
      "customers_retained": retained, "campaign_cost": round(campaign_cost, 2),
      "value_per_retained_customer": round(value_per_retained_customer, 2),
      "expected_retention_rate_percent": expected_retention_rate,
      "actual_retention_rate_percent": round(actual_rate, 2),
      "retention_rate_variance_percentage_points": round(actual_rate - expected_retention_rate, 2),
      "estimated_retained_value": round(actual_value, 2), "net_value_after_campaign_cost": round(net_value, 2)}
    _records.append(record)
    return record

def feedback_summary():
    contacts = sum(r["customers_contacted"] for r in _records)
    retained = sum(r["customers_retained"] for r in _records)
    return {"campaigns_recorded": len(_records), "customers_contacted": contacts,
      "customers_retained": retained,
      "actual_retention_rate_percent": round(retained / contacts * 100, 2) if contacts else None,
      "campaigns": list(_records),
      "note": "Aggregate feedback is held in process memory only and clears when the API restarts."}
