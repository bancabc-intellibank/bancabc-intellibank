from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.analytics import get_overview, get_segments, get_watchlist, get_recommendations

app = FastAPI(title="BancABC IntelliBank API", version="0.1.0", description="Customer intelligence prototype API")
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:3000"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

@app.get("/api/health")
def health():
    return {"status": "ok", "service": "intellibank-api", "data_mode": "synthetic_demo"}

@app.get("/api/overview")
def overview():
    return get_overview()

@app.get("/api/segments")
def segments():
    return get_segments()

@app.get("/api/customers")
def customers():
    return get_watchlist()

@app.get("/api/recommendations")
def recommendations():
    return get_recommendations()
