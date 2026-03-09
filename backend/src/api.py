from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

from src.kpi_engine import KPIEngine

app = FastAPI(title="Intelligence Platform API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize engine, ensuring it resolves the right path from root
engine = KPIEngine(db_path=os.path.join(os.path.dirname(__file__), '..', 'data', 'warehouse.duckdb'))

@app.get("/")
def read_root():
    return {"status": "ok"}

@app.get("/api/kpis/executive-summary")
def get_executive_summary():
    try:
        return engine.get_executive_summary()
    except Exception as e:
        return {"error": str(e)}

@app.get("/api/kpis/finance-monthly")
def get_finance_monthly():
    try:
        return engine.get_financial_kpis_by_month()
    except Exception as e:
        return {"error": str(e)}

@app.get("/api/kpis/marketing-campaigns")
def get_marketing_campaigns():
    try:
        return engine.get_marketing_kpis_by_campaign()
    except Exception as e:
        return {"error": str(e)}
