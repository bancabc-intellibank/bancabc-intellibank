# BancABC IntelliBank
## Explainable Customer Intelligence for Retention, Value Discovery and Smarter Growth

**Competition:** BancABC Universities Hackathon 2026  
**Institution:** University of Zimbabwe  
**Team:** IntelliBank  
**Project category:** AI, data analytics and banking decision support

## 1. Executive summary

Banks generate valuable signals through everyday customer transactions. Changes in transaction frequency, value, recency, channel usage and product activity can indicate when a customer relationship is weakening, when a customer is becoming more valuable, and when an additional product may be relevant. However, raw transaction records do not automatically become timely, prioritised business decisions.

**BancABC IntelliBank** is a customer intelligence platform that converts approved banking data into clear, explainable insights. It combines three capabilities: identifying customers who may be at risk of churn, discovering high-value and emerging customer segments, and surfacing relevant cross-selling opportunities. An interactive dashboard presents trends, customer cohorts, risk indicators and suggested next actions.

The guiding principle is simple: **show the bank not only what happened, but who may need attention, why, and what action could be considered next.** IntelliBank is designed as decision support for authorised staff, not as an automated decision-maker about customers.

The current software prototype uses synthetic demonstration data. Final training, performance claims and bank-specific recommendations will use only the official hackathon dataset and its documented definitions.

## 2. Problem statement

Transaction data contains behavioural signals that can help a bank retain customers, recognise valuable relationships and identify relevant product opportunities. These signals can be difficult to interpret quickly when they are spread across raw records and separate reports.

The challenge creates four related business problems:

- **Customer attrition:** declining engagement may go unnoticed until a customer has already become inactive.
- **Missed customer value:** high-value and fast-growing relationships may not be consistently identified.
- **Untargeted cross-selling:** broad campaigns may fail to account for customer behaviour, existing products and eligibility.
- **Delayed insight:** teams may spend too much time preparing reports before they can identify priority customers and practical actions.

IntelliBank addresses the hackathon's central requirements by connecting churn-risk analysis, high-value customer discovery and actionable transaction insights in one workflow.

## 3. Proposed solution

IntelliBank will provide four connected capabilities.

### 3.1 Churn intelligence

The platform will analyse approved behavioural indicators to identify customers whose activity suggests elevated attrition risk. Depending on available fields, candidate indicators include transaction recency, changes in transaction frequency, transaction value trends, channel activity and product usage.

If the official dataset contains a defensible churn outcome label, the team will train and evaluate a supervised model. An interpretable baseline such as logistic regression will be established first; a tree-based model may be compared if data quality and time allow. Risk results will be accompanied by understandable contributing signals where technically valid.

The output will be a prioritised watchlist with risk bands, engagement trends and potential reasons for follow-up. A risk score is a prioritisation aid, not proof that a customer will leave.

### 3.2 Customer value and behavioural segmentation

Customers will be grouped into meaningful behavioural and value segments. The initial approach will assess recency, frequency and monetary value (RFM) where transaction fields permit. Additional features, such as product breadth or channel mix, may be included only if present, reliable and approved.

Potential segment labels include high-value, growing, regular, at-risk and dormant. Final definitions will be determined from the actual dataset and checked for business meaning rather than assumed in advance. This helps distinguish customers who may need retention attention from those who may benefit from relationship development.

### 3.3 Cross-selling opportunity intelligence

IntelliBank will identify potential product opportunities by combining customer behaviour with existing product holdings and approved product eligibility rules. Recommendations will include a reason, priority and evidence supporting the suggestion.

The system will not label a product as suitable when required eligibility or suitability information is missing. Where those fields are unavailable, it will show segment-level opportunities for human review rather than making unsupported individual recommendations.

### 3.4 Management dashboard

The dashboard will provide:
- An overview of customers analysed and key transaction trends.
- Churn-risk distribution and a prioritised customer watchlist.
- Segment sizes, characteristics and value indicators.
- Cross-selling opportunity cohorts and recommendation rationales.
- Concise summaries that help teams decide where to investigate or engage.

## 4. Objectives

1. Prepare and validate the official challenge dataset for reliable customer-level analysis.
2. Identify customers exhibiting behavioural patterns associated with churn, using a documented definition and prediction horizon.
3. Discover high-value and emerging customer groups using transparent behavioural and value measures.
4. Surface relevant cross-selling opportunities based on available product and eligibility information.
5. Present findings in an interactive dashboard that supports prioritisation and business decisions.
6. Evaluate analytical quality, explain limitations and demonstrate a reproducible workflow.

## 5. Methodology and technical approach

The solution follows a repeatable data-to-decision pipeline.

**Step 1 — Data understanding and quality checks.** Review the data dictionary, record grain (customer, account or transaction), date coverage and available fields. Check missing values, duplicates, invalid dates, inconsistent identifiers and outliers. Exclude direct identifiers from modelling features.

**Step 2 — Data preparation and feature engineering.** Where supported, aggregate transactions to customer-level features. Candidate features include recency (time since last activity), frequency (transaction count), monetary value, changes in activity between comparable periods, channel diversity and existing product holdings. Define all feature windows relative to an observation date and exclude information from after the prediction point.

**Step 3 — Churn modelling and validation.** If a valid churn label is supplied or approved, train an interpretable supervised baseline. Evaluate beyond accuracy: report precision, recall, F1-score, ROC-AUC, PR-AUC and/or top-k lift as appropriate to the dataset. Prefer chronological validation when timestamps and prediction horizons allow it. Select thresholds with practical retention-team capacity in mind.

If no reliable churn label exists, the team will not fabricate one or claim supervised prediction. Instead, it will present a clearly named behavioural attrition-risk indicator based on documented inactivity and engagement rules, noting that it is a proxy requiring business validation.

**Step 4 — Segmentation and opportunity analysis.** Begin with interpretable RFM-style rules. Explore clustering only if it produces stable, understandable groups. Generate cross-sell opportunities using available product holdings, behavioural signals and approved eligibility rules.

**Step 5 — Visualisation and decision support.** Connect the analytics API to the dashboard. Distinguish observed facts, model estimates and rule-based suggestions so users can understand the evidence behind each insight.

**Step 6 — Testing and demonstration.** Test data validation, API responses, model evaluation and dashboard interactions. Use official data only where permitted; otherwise label synthetic data clearly.

## 6. Innovation and differentiating value

IntelliBank connects three business questions in one explainable workflow:

- **Retain:** Which customers may need attention, and what behavioural signals support that concern?
- **Recognise:** Which customers represent high or growing value, and what distinguishes their behaviour?
- **Grow responsibly:** Which product opportunities appear relevant based on evidence, existing holdings and eligibility?

The innovation is not simply the use of machine learning. It is the connection between analytical evidence and a prioritised action that a business team can understand, inspect and review. The platform moves beyond static reporting towards practical decision support without hiding its reasoning behind a black-box score.

## 7. Expected business value and success measures

The project is designed to support measurable business questions. It will not claim financial gains before evaluation.

| Business objective | Proposed measure |
|---|---|
| Improve churn identification | Precision, recall, PR-AUC and top-k lift where labels exist |
| Focus retention effort | Size and quality of a reviewable high-risk priority cohort |
| Understand customer value | Segment size, transaction contribution and segment stability |
| Improve cross-sell targeting | Eligible opportunity count, recommendation relevance and conversion if outcome data exists |
| Support decisions | Time from dataset to prioritised insight and dashboard usability feedback |

Results will be calculated from the supplied dataset. Any financial-impact estimate will state its assumptions and will not be presented as realised revenue or savings.

## 8. Feasibility and implementation

The prototype uses accessible, widely adopted technologies:

- **Frontend:** Next.js, React, TypeScript, Tailwind CSS and Recharts.
- **Backend:** Python and FastAPI.
- **Analytics and machine learning:** Pandas, NumPy and scikit-learn.
- **Data storage:** PostgreSQL can be added if persistence is required and permitted.

The software is modular: data preparation, modelling, recommendation logic and presentation are separated. This allows the official dataset to be integrated without rebuilding the application.

**Delivery milestones:** (1) confirm dataset definitions and permitted fields; (2) validate records and engineer customer features; (3) build churn baseline and segmentation; (4) implement cross-sell logic; (5) integrate and test the dashboard; (6) demonstrate findings, evidence and limitations.

## 9. Responsible AI, privacy and security

Banking analytics must protect customer trust. IntelliBank will use only authorised challenge data and follow organiser instructions. Raw customer data will not be committed to a public repository. Direct identifiers will be excluded from modelling features; access to any necessary mapping will be restricted. Credentials will be stored outside source code, and sensitive records will not appear in logs or screenshots.

The team will document definitions, feature windows, model limitations and recommendation rules; check for leakage and unstable segments; and keep human review in the decision loop. The prototype will not automatically deny services, set prices or make binding decisions about customers.

## 10. Risks and mitigation

| Risk | Mitigation |
|---|---|
| Missing or unclear churn labels | Confirm the definition; use a labelled behavioural risk indicator rather than inventing outcomes |
| Incomplete or inconsistent records | Apply documented validation and reconciliation |
| Class imbalance | Use precision-recall measures, appropriate class weighting and validation-based thresholds |
| Leakage or overfitting | Use time-aware splits where possible and exclude post-outcome information |
| Missing product eligibility data | Restrict individual recommendations and show segment-level opportunities for review |
| Sensitive data exposure | Keep raw data private, minimise identifiers and never commit it to Git |
| Limited hackathon time | Deliver an end-to-end baseline first, then add comparisons and refinements |

## 11. Expected deliverables

1. A working customer intelligence dashboard.
2. A documented data preparation and validation pipeline.
3. A churn-risk baseline and evaluation report, where valid labels exist.
4. Customer value and behavioural segment analysis.
5. Explainable cross-selling opportunity recommendations.
6. A concise technical and business report covering findings, assumptions and limitations.
7. A live demonstration using approved challenge data or clearly labelled synthetic data.

## 12. Conclusion

BancABC IntelliBank proposes a practical way to turn transaction data into better-informed customer decisions. By connecting churn intelligence, customer value segmentation and explainable cross-selling opportunities, it addresses the central needs of the BancABC Universities Hackathon in one coherent platform.

Its strength is the link between analytical evidence and an action that a business team can understand and review. The team will prioritise data quality, transparent modelling, measurable evaluation and responsible use of customer information.

**IntelliBank aims to help BancABC see risk earlier, recognise value more clearly and pursue growth more intelligently — one evidence-based customer insight at a time.**
