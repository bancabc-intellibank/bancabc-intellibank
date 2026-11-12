"""Transparent retention campaign scenario calculator."""
def simulate_campaign(data, budget, cost_per_contact, retention_rate, value_per_customer):
    if budget < 0 or cost_per_contact <= 0 or value_per_customer < 0:
        raise ValueError("Budget/value must be non-negative and contact cost must be positive.")
    if not 0 <= retention_rate <= 100:
        raise ValueError("Retention rate must be between 0 and 100.")
    eligible = int(data.get("overview", {}).get("high_churn_risk", 0))
    capacity = int(budget // cost_per_contact)
    targeted = min(eligible, capacity)
    spend = round(targeted * cost_per_contact, 2)
    retained = round(targeted * retention_rate / 100, 2)
    value = round(retained * value_per_customer, 2)
    net = round(value - spend, 2)
    return {
        "eligible_high_risk_customers": eligible, "contact_capacity": capacity,
        "customers_targeted": targeted, "estimated_campaign_spend": spend,
        "estimated_retained_customers": retained, "estimated_retained_value": value,
        "estimated_net_value_after_campaign_cost": net,
        "estimated_roi_percent": round(net / spend * 100, 2) if spend else None,
        "assumptions": {"budget": budget, "cost_per_contact": cost_per_contact,
            "retention_rate_percent": retention_rate, "value_per_retained_customer": value_per_customer},
        "disclaimer": "Scenario only: estimates use user-entered assumptions and are not guaranteed outcomes."
    }
