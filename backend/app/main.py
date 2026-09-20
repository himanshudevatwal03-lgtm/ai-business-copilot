import os
from contextlib import asynccontextmanager
from typing import Optional
from fastapi import FastAPI, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.config import settings
from app.database import engine, Base, get_db, SessionLocal
from app.seed_data import seed_database
from app.services.erp_service import ERPService
from app.services.copilot_service import copilot_service
from app.schemas import QueryRequest, QueryResponse, DashboardKPIs

def init_db():
    """Ensure database schema exists and initial seed data is loaded."""
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_database(db, force=False)
    finally:
        db.close()

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    description="AI Business Copilot for ERP and Business Intelligence (Snapdragon AI Lab Challenge 2026)",
    lifespan=lifespan
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Endpoints
@app.get("/api/health", tags=["System"])
def health_check():
    return {
        "status": "online",
        "service": settings.PROJECT_NAME,
        "version": settings.PROJECT_VERSION,
        "environment": settings.ENVIRONMENT,
        "provider_info": copilot_service.get_provider_info(),
        "database": "SQLite (Local ERP Storage)"
    }

@app.get("/api/dashboard/kpis", tags=["Dashboard"], response_model=DashboardKPIs)
def get_dashboard_kpis(db: Session = Depends(get_db)):
    return ERPService.get_dashboard_kpis(db)

@app.get("/api/dashboard/trends", tags=["Dashboard"])
def get_sales_trends(months: int = 6, db: Session = Depends(get_db)):
    return ERPService.get_monthly_sales_trend(db, months=months)

@app.get("/api/dashboard/top-products", tags=["Dashboard"])
def get_top_products(limit: int = 5, db: Session = Depends(get_db)):
    return ERPService.get_top_selling_products(db, limit=limit)

@app.post("/api/copilot/query", tags=["Copilot"], response_model=QueryResponse)
async def query_copilot(req: QueryRequest, db: Session = Depends(get_db)):
    result = await copilot_service.answer_query(
        query=req.query,
        db=db,
        client_context=req.context
    )
    return result

@app.get("/api/erp/invoices", tags=["ERP Data"])
def get_invoices(status: Optional[str] = None, search: Optional[str] = None, db: Session = Depends(get_db)):
    return ERPService.get_invoices(db, status=status, search=search)

@app.get("/api/erp/customers", tags=["ERP Data"])
def get_customers(search: Optional[str] = None, db: Session = Depends(get_db)):
    return ERPService.get_customers(db, search=search)

@app.get("/api/erp/products", tags=["ERP Data"])
def get_products(category: Optional[str] = None, search: Optional[str] = None, db: Session = Depends(get_db)):
    return ERPService.get_products(db, category=category, search=search)

@app.get("/api/erp/overdue", tags=["ERP Data"])
def get_overdue_invoices(db: Session = Depends(get_db)):
    return ERPService.get_overdue_invoices(db)

@app.get("/api/erp/low-stock", tags=["ERP Data"])
def get_low_stock(db: Session = Depends(get_db)):
    return ERPService.get_low_stock_products(db)

@app.post("/api/erp/reseed", tags=["ERP Data"])
def reseed_data(db: Session = Depends(get_db)):
    seed_database(db, force=True)
    return {"message": "Database reseeded successfully with fresh ERP records."}

# Serve Frontend Static Assets in Production
frontend_dist = os.path.join(os.path.dirname(__file__), "..", "..", "frontend", "dist")
if os.path.isdir(frontend_dist):
    app.mount("/assets", StaticFiles(directory=os.path.join(frontend_dist, "assets")), name="assets")
    
    @app.get("/{full_path:path}", include_in_schema=False)
    def serve_frontend_spa(full_path: str):
        index_path = os.path.join(frontend_dist, "index.html")
        if os.path.exists(index_path):
            return FileResponse(index_path)
        return {"error": "Frontend build not found"}
