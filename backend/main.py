from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from backend.analytics import get_data, analyse_csv

app = FastAPI(title="BancABC IntelliBank API", version="0.2.0",
              description="CSV-driven customer intelligence prototype")
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:3000","http://127.0.0.1:3000"],
                   allow_credentials=False, allow_methods=["*"], allow_headers=["*"])

@app.get("/api/health")
def health():
    data=get_data()
    return {"status":"ok","service":"intellibank-api","data_mode":data["overview"]["data_mode"]}

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

@app.get("/api/overview")
def overview(): return get_data()["overview"]
@app.get("/api/segments")
def segments(): return get_data()["segments"]
@app.get("/api/customers")
def customers(): return get_data()["customers"]
@app.get("/api/recommendations")
def recommendations(): return get_data()["recommendations"]
