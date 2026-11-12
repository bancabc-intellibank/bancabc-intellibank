# BancABC IntelliBank

**AWS CAST TEAM | University of Zimbabwe | BancABC Universities Hackathon 2026**

BancABC IntelliBank is a customer-intelligence prototype that turns transaction records into explainable behavioural insights and decision-support scenarios. It is designed around four actions: **Retain, Recognise, Grow and Measure**.

## Current prototype capabilities

- Overview dashboard with customer, risk, value and segment summaries.
- CSV upload and data profiling (UTF-8, maximum 15 MB).
- Customer-level transaction frequency, value and recency analysis.
- Relative behavioural risk scoring with reason codes; this is not a calibrated churn probability.
- Customer segmentation using RFM-style behavioural indicators.
- Customer action prioritisation combining relative risk and customer value.
- Segment-level engagement and product-discovery prompts. These are not product eligibility or credit decisions.
- Retention campaign Impact Simulator using user-entered assumptions.
- Executive intelligence report download with summary, segment actions, priority watchlist and data-quality notes.
- Optional labelled churn-model evaluation endpoint reporting ROC-AUC, average precision (PR-AUC), precision, recall, F1 and confusion matrix.
- Synthetic demonstration data, clearly labelled.

## Run locally

### Backend

```bash
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# macOS/Linux:
# source .venv/bin/activate
pip install -r backend/requirements.txt
uvicorn backend.main:app --reload --port 8000
```

### Frontend

```bash
npm install
npm run dev
```

Open `http://localhost:3000`. The frontend defaults to `http://localhost:8000`; set `NEXT_PUBLIC_API_URL` if the API is hosted elsewhere.

Run backend tests:

```bash
python -m unittest discover -s backend -p "test_*.py"
```

## API endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/api/health` | Service health and current data mode |
| GET | `/api/analysis` | Current complete analysis |
| POST | `/api/analyse` | Upload transaction-level CSV |
| POST | `/api/simulate` | Calculate a retention campaign scenario |
| GET | `/api/report` | Generate executive intelligence report |
| POST | `/api/model/evaluate` | Evaluate an ephemeral labelled churn baseline |
| GET | `/api/overview` | Overview metrics |
| GET | `/api/segments` | Segment counts |
| GET | `/api/customers` | Customer watchlist |
| GET | `/api/recommendations` | Segment action prompts |

### Impact Simulator request

```json
{
  "budget": 500,
  "cost_per_contact": 5,
  "expected_retention_rate": 20,
  "value_per_retained_customer": 100
}
```

The simulator limits outreach to the high behavioural-risk customer count and calculates scenario spend, estimated retained customers, estimated retained value, net value and estimated ROI. Every output is assumption-based, not a forecast or guarantee. Amounts have no inferred currency.

### Churn model evaluation

POST a UTF-8 CSV to `/api/model/evaluate`. It must contain one row per customer and a binary `churned` target with exactly two classes. At least 20 records are required by the endpoint. The baseline is trained in memory for that request and is not saved or connected to the live watchlist. A random stratified split is only a baseline; a time-aware split and a business-approved churn definition/horizon are preferable.

See [CSV upload guide](docs/CSV_GUIDE.md) and [modelling guide](docs/MODELLING.md).

## Data, modelling and responsible use

- Synthetic fallback figures are not BancABC records.
- The uploaded-data score is a relative behavioural heuristic based on the uploaded sample, not a trained or calibrated churn probability.
- The reference date for recency is the latest valid transaction date in the uploaded dataset. The system does not assume the computer's current date is the customer's observation date.
- The action-priority score combines behavioural risk and relative transaction value. It is a ranking aid, not an estimate of customer lifetime value.
- Cross-sell prompts are segment-level suggestions only. Product eligibility, suitability, affordability, consent and bank policy must be checked by authorised staff.
- The Impact Simulator uses assumptions entered by the user. It does not establish actual revenue or campaign effectiveness.
- The churn evaluation endpoint requires approved historical labels. Do not fabricate labels or report metrics from synthetic labels as real bank performance.
- Uploaded data is kept in API process memory; restarting the backend clears it. This prototype is single-process and not multi-user isolated.
- Use only synthetic or organiser-authorised, appropriately minimised data. Do not upload identifiable customer records to a public demo.

## Security and production limitations

This is a hackathon prototype, not a production banking service. It does not yet provide user authentication, role-based permissions, persistent encrypted storage, multi-user tenant isolation, formal audit trails, data-retention workflows or a completed security assessment. Production deployment requires those controls, TLS, secret management, monitoring, threat modelling, bank security approval and compliance review.

## Technology

- Frontend: Next.js, React, TypeScript, Tailwind CSS, Recharts.
- Backend: Python, FastAPI, Pandas, NumPy and scikit-learn.
