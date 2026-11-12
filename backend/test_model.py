import unittest
import pandas as pd
from backend.model import train_churn_baseline

class ChurnModelTests(unittest.TestCase):
    def test_labelled_baseline_returns_expected_metrics(self):
        frame = pd.DataFrame({
            "customer_id": [f"C{i:03d}" for i in range(60)],
            "monthly_transactions": [i % 9 for i in range(60)],
            "channel": ["mobile" if i % 2 else "branch" for i in range(60)],
            "churned": [1 if i % 3 == 0 else 0 for i in range(60)]
        })
        result = train_churn_baseline(frame)
        for key in ["roc_auc", "pr_auc_average_precision", "precision", "recall", "f1", "confusion_matrix"]:
            self.assertIn(key, result.metrics)
        self.assertEqual(result.metrics["test_rows"], 12)

    def test_missing_target_is_rejected(self):
        with self.assertRaises(ValueError):
            train_churn_baseline(pd.DataFrame({"customer_id": ["A", "B"], "amount": [2, 3]}))

if __name__ == "__main__":
    unittest.main()
