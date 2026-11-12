import unittest
from backend.simulation import simulate_campaign

class SimulationTests(unittest.TestCase):
    def test_budget_limits_outreach_and_calculates_scenario(self):
        data = {"overview": {"high_churn_risk": 100}}
        result = simulate_campaign(data, 500, 5, 20, 100)
        self.assertEqual(result["customers_targeted"], 100)
        self.assertEqual(result["estimated_campaign_spend"], 500)
        self.assertEqual(result["estimated_retained_customers"], 20)
        self.assertEqual(result["estimated_retained_value"], 2000)
        self.assertEqual(result["estimated_roi_percent"], 300)

    def test_invalid_retention_rate_is_rejected(self):
        with self.assertRaises(ValueError):
            simulate_campaign({"overview": {"high_churn_risk": 10}}, 100, 2, 120, 50)

if __name__ == "__main__":
    unittest.main()
