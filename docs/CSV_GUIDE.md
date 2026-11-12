# IntelliBank CSV upload guide

## Run the system

- Frontend: `npm install` then `npm run dev`
- Backend: create/activate a Python environment, run `pip install -r backend/requirements.txt`, then `uvicorn backend.main:app --reload --port 8000`
- Open the frontend at `http://localhost:3000`.

The frontend uses `NEXT_PUBLIC_API_URL` when configured; otherwise it calls `http://localhost:8000`.

## CSV format

The minimum required field is a customer identifier. The engine recognises common names such as `customer_id`, `client_id`, and `account_id`. To improve analysis, include:

| Field | Example | Purpose |
|---|---|---|
| customer_id | CUST-001 | Groups transactions by customer |
| transaction_date | 2026-11-08 | Calculates days since last activity |
| amount | 125.50 | Calculates transaction value |
| transaction_type | Transfer | Optional product/transaction context |
| channel | Mobile | Optional channel context |

Column names are detected using common keywords, so retain clear column names. CSV must be UTF-8 and no larger than 15 MB. The current prototype expects transaction-level rows, one row per transaction.

## What the analysis calculates

- Unique customers and transaction-row counts.
- Per-customer transaction frequency, total amount and average transaction amount when an amount column exists.
- Recency in days when a transaction date column exists.
- Relative behavioural risk score from recency, frequency and value ranks.
- RFM-style behavioural segments, a customer watchlist with reason codes, and next-action suggestions.
- Data profile: missing values, detected columns and duplicate customer identifiers.
- Downloadable customer-analysis CSV from the dashboard.

## Important limitations

1. Without an organiser-approved churn label and prediction horizon, the risk score is a transparent behavioural heuristic, **not** a trained churn probability.
2. The score is relative to the uploaded dataset and should not be interpreted as a calibrated probability or as evidence that a customer will leave.
3. Cross-sell suggestions are segment-level prompts, not eligibility decisions. Product suitability, affordability, consent and bank policy must be checked by authorised staff.
4. Currency is not inferred. Amounts remain in the source dataset's units.
5. Uploaded data is held in API process memory for the current run; restarting the API clears it. Do not upload real customer personal data to a public demo or repository. Use only data the organisers authorise.
6. This is a hackathon prototype, not a production banking system. Production deployment requires authentication, role-based access, encryption, secure storage, audit logging, retention controls and security review.

## Sample data

Use the dashboard's **Download sample CSV** control to obtain a small synthetic transaction file and test the complete upload-to-dashboard workflow. The sample contains no real BancABC customer information.
