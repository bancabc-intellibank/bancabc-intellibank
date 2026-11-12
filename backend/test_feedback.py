import unittest
from backend.feedback import record_outcome, feedback_summary

class FeedbackTests(unittest.TestCase):
    def test_records_aggregate_outcome_without_customer_identifiers(self):
        result = record_outcome("Pilot", 100, 25, 400, 80, 20)
        self.assertEqual(result["actual_retention_rate_percent"], 25)
        self.assertEqual(result["retention_rate_variance_percentage_points"], 5)
        self.assertNotIn("customer_id", result)

    def test_retained_cannot_exceed_contacted(self):
        with self.assertRaises(ValueError):
            record_outcome("Invalid", 10, 11, 20, 50, 10)

if __name__ == "__main__":
    unittest.main()
