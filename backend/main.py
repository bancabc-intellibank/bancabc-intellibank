from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from io import StringIO
import pandas as pd
from backend.analytics import get_data, analyse_csv
from backend.simulation import simulate_campaign
from backend.reporting import build_executive_report
from backend.model import train_churn_baseline

app = FastAPI(title="BancABC IntelliBank API", version="0.3.0",
              description="Customer intelligence, scenario analysis and executive reporting prototype")
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:3000","http://127.0.0.1:3000"],
                   allow_credentials=False, allow_methods=["*"], allow_headers=["*"])

class SimulationRequest(BaseModel):
    budget: float = Field(ge=0, le=100000000)
    cost_per_contact: float = Field(gt=0, le=1000000)
    expected_retention_rate: float = Field(ge=0, le=100)
    value_per_retained_customer: float = Field(ge=0, le=100000000)

@app.get("/api/health")
def health():
    data=get_data()
    return {"status":"ok","service":"intellibank-api","version":"0.3.0","data_mode":data["overview"]["data_mode"]}

@app.get("/api/analysis")
def analysis():
    return get_data()

@app.post("/api/analyse")
async def upload_and_analyse(request: Request):
    try:
        raw=await request.body()
        if not raw: raise ValueError("The uploaded CSV is empty.")
        return analyse_csv(raw.decode("utf-8-sig"))
    except UnicodeDecodeError:
        raise HTTPException(status_code=400, detail="Please upload a UTF-8 encoded CSV file.")
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))

@app.post("/api/simulate")
def simulate(request: SimulationRequest):
    try:
        return simulate_campaign(get_data(), request.budget, request.cost_per_contact,
            request.expected_retention_rate, request.value_per_retained_customer)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

@app.get("/api/report")
def executive_report():
    return build_executive_report(get_data())

@app.post("/api/model/evaluate")
async def evaluate_churn_model(request: Request):
    """Train/evaluate an ephemeral baseline from one-row-per-customer CSV with approved churned labels."""
    try:
        raw=await request.body()
        if not raw: raise ValueError("Upload a labelled customer-level CSV.")
        frame=pd.read_csv(StringIO(raw.decode("utf-8-sig")))
        if len(frame)<20: raise ValueError("At least 20 labelled customer records are required for this prototype evaluation.")
        result=train_churn_baseline(frame, target="churned")
        return {"metrics":result.metrics,"feature_columns":result.feature_columns,
            "note":"Model is trained for this request only and is not saved. Use an approved churn definition and a time-aware validation design for serious evaluation."}
    except UnicodeDecodeError:
        raise HTTPException(status_code=400, detail="Please upload a UTF-8 encoded CSV file.")
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))

@app.get("/api/overview")
def overview(): return get_data()["overview"]
@app.get("/api/segments")
def segments(): return get_data()["segments"]
@app.get("/api/customers")
def customers(): return get_data()["customers"]
@app.get("/api/recommendations")
def recommendations(): return get_data()["recommendations"]
