# BancABC IntelliBank

Explainable customer intelligence and decision-support prototype for the BancABC Universities Hackathon 2026.

## Implemented now

- Next.js dashboard with Overview, Customers, Churn Intelligence, Segments and Cross-sell workspaces.
- CSV upload to the FastAPI backend (UTF-8 CSV, maximum 15 MB).
- Automatic detection of common customer ID, transaction date, amount and transaction-type/channel columns.
- Customer-level recency, transaction frequency and value aggregation.
- Relative behavioural risk ranking with reason codes (not a trained churn probability).
- RFM-style behavioural segments and segment-based next-action recommendations.
- Data-quality profile, management insights and customer report CSV export.
- Downloadable synthetic sample transaction CSV for testing the full workflow.
- Unit tests for the CSV analytics engine in `backend/test_analytics.py`.

## Run locally

### Backend

```bash
python -m venv .venv
# Activate the environment, then:
pip install -r backend/requirements.txt
uvicorn backend.main:app --reload --port 8000
```

### Frontend

```bash
npm install
npm run dev
```

Open `http://localhost:3000`. The frontend defaults to `http://localhost:8000` for the API. Set `NEXT_PUBLIC_API_URL` if the API runs elsewhere.

Run backend tests with:

```bash
python -m unittest backend.test_analytics
```

See [CSV upload guide](docs/CSV_GUIDE.md) for supported columns and limitations.

## Important modelling and data notes

- Synthetic fallback figures are labelled and are not BancABC records.
- Uploaded CSV analysis calculates transparent behavioural heuristics from the available transactions. The risk score is relative to the uploaded sample; it is not a calibrated probability that a customer will churn.
- A supervised churn model requires an organiser-approved churn label, observation date and prediction horizon. Do not fabricate labels or claim model performance without a valid held-out evaluation.
- Product suggestions are prompts for authorised staff, not lending approvals or eligibility decisions.
- Currency is not inferred; monetary values remain in the source dataset's units.
- The prototype keeps the most recent analysis in API process memory. Restarting the backend clears it.

## Security

Do not commit real customer personal information, credentials, API keys or confidential data. Only process datasets that the organisers authorise. This prototype is not production-ready: production use requires authentication, role-based access, encryption, secure storage, audit logging, retention controls and a security review.

## Technology

- Frontend: Next.js, React, TypeScript, Tailwind CSS, Recharts.
- Backend: Python, FastAPI, Pandas, NumPy and scikit-learn.
