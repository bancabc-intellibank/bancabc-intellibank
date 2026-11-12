import unittest
from backend.analytics import analyse_csv

SAMPLE = """customer_id,transaction_date,amount,transaction_type
A,2026-11-10,100,POS
A,2026-11-01,80,Transfer
B,2026-09-01,20,POS
C,2026-11-09,450,Transfer
C,2026-11-08,300,POS
D,2026-08-01,10,POS
"""

class AnalyticsTests(unittest.TestCase):
    def test_csv_produces_customer_intelligence(self):
        result = analyse_csv(SAMPLE)
        self.assertEqual(result["overview"]["customers_analysed"], 4)
        self.assertEqual(result["overview"]["transaction_rows"], 6)
        self.assertTrue(result["segments"])
        self.assertTrue(result["customers"])
        self.assertIn("risk_score", result["customers"][0])
        self.assertIn("reason", result["customers"][0])
        self.assertTrue(result["recommendations"])
        self.assertEqual(result["overview"]["data_mode"], "uploaded_csv")

    def test_missing_customer_identifier_is_rejected(self):
        with self.assertRaises(ValueError):
            analyse_csv("date,amount\n2026-01-01,10\n")

if __name__ == "__main__":
    unittest.main()
