# IntelliBank CSV upload guide

## Run the system

- Backend: activate a Python environment, run `pip install -r backend/requirements.txt`, then `uvicorn backend.main:app --reload --port 8000`.
- Frontend: run `npm install` then `npm run dev`.
- Open `http://localhost:3000`.

The frontend uses `NEXT_PUBLIC_API_URL` when configured; otherwise it calls `http://localhost:8000`.

## Transaction CSV format

The minimum required field is a customer identifier. Common names include `customer_id`, `client_id` and `account_id`. Recommended fields:

| Field | Example | Purpose |
|---|---|---|
| customer_id | CUST-001 | Groups transactions by customer |
| transaction_date | 2026-11-08 | Calculates days since latest activity in this file |
| amount | 125.50 | Calculates transaction value |
| transaction_type | Transfer | Optional transaction context |
| channel | Mobile | Optional channel context |

The transaction upload expects one row per transaction. CSV must be UTF-8 and no larger than 15 MB.

## What the transaction analysis calculates

- Unique customers and transaction-row counts.
- Transaction frequency, total value and average transaction amount when amount is available.
- Recency relative to the latest valid transaction date in the uploaded file.
- Relative behavioural risk ranking using available recency, frequency and value.
- RFM-style segments, reason codes and next-action prompts.
- Action-priority ranking combining behavioural risk (65%) and relative transaction-value rank (35%).
- Missing values, duplicate customer IDs and exact duplicate transaction rows.
- Downloadable customer-analysis CSV.

## Other prototype workflows

- **Impact Simulator:** uses a budget, contact cost, assumed retention rate and assumed value per retained customer to calculate a hypothetical campaign scenario.
- **Executive report:** downloads a JSON management summary containing dataset mode, overview, segments, recommendations, a priority watchlist and data-quality warnings.
- **Churn model evaluation:** `POST /api/model/evaluate` accepts a separate customer-level CSV with a binary `churned` target. It is not the same format as the transaction-level upload. The target must have an approved business definition and prediction horizon.

## Important limitations

1. Behavioural risk is not a trained churn probability.
2. Cross-sell prompts are segment-level ideas, not eligibility or lending decisions.
3. Campaign projections depend entirely on assumptions and are not forecasts.
4. Currency is not inferred; amounts remain in the source dataset's units.
5. Uploaded data is held in API process memory; restarting the API clears it. The prototype is not multi-user isolated.
6. Use only synthetic or organiser-authorised data. Do not upload identifiable customer data to a public demo or repository.
7. Production use requires authentication, role-based access, encryption, secure storage, audit logging, retention controls, monitoring and a security review.

## Sample data

Use the dashboard's **Download sample CSV** control to test the transaction upload workflow. The sample contains synthetic records and no real BancABC customer information.
