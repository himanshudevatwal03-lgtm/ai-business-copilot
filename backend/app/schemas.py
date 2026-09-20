from pydantic import BaseModel, ConfigDict
from typing import List, Optional, Any, Dict
from datetime import date, datetime

class CustomerBase(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None
    region: str
    segment: str
    credit_limit: float
    status: str

class CustomerOut(CustomerBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime

class ProductBase(BaseModel):
    sku: str
    name: str
    category: str
    unit_price: float
    unit_cost: float
    stock_quantity: int
    reorder_threshold: int
    description: Optional[str] = None

class ProductOut(ProductBase):
    model_config = ConfigDict(from_attributes=True)
    id: int

class InvoiceOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    invoice_number: str
    customer_id: int
    customer_name: Optional[str] = None
    issue_date: date
    due_date: date
    amount: float
    paid_amount: float
    status: str
    days_overdue: Optional[int] = 0

class DashboardKPIs(BaseModel):
    total_revenue: float
    monthly_revenue: float
    revenue_growth_pct: float
    total_orders_count: int
    overdue_receivables: float
    overdue_invoices_count: int
    low_stock_products_count: int
    active_customers_count: int

class MonthlySalesPoint(BaseModel):
    month: str
    revenue: float
    orders_count: int

class TopProductPoint(BaseModel):
    product_name: str
    category: str
    quantity_sold: int
    total_revenue: float

class QueryRequest(BaseModel):
    query: str
    context: Optional[Dict[str, Any]] = None

class QueryResponse(BaseModel):
    query: str
    answer: str
    intent: str
    confidence: float
    metrics: Optional[Dict[str, Any]] = None
    table_data: Optional[List[Dict[str, Any]]] = None
    chart_data: Optional[Dict[str, Any]] = None
    suggestions: List[str] = []
    inference_provider: str = "local"
    timestamp: datetime = datetime.utcnow()
