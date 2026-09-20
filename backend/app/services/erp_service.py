import datetime
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func, desc, or_
from app.models import Customer, Product, SalesOrder, SalesOrderItem, Invoice

class ERPService:
    @staticmethod
    def get_dashboard_kpis(db: Session) -> Dict[str, Any]:
        today = datetime.date.today()
        first_day_this_month = today.replace(day=1)
        # Calculate first day of previous month
        prev_month_end = first_day_this_month - datetime.timedelta(days=1)
        first_day_prev_month = prev_month_end.replace(day=1)

        # Total revenue
        total_rev = db.query(func.sum(SalesOrder.total_amount)).scalar() or 0.0

        # This month revenue
        this_month_rev = db.query(func.sum(SalesOrder.total_amount))\
            .filter(SalesOrder.order_date >= first_day_this_month)\
            .scalar() or 0.0

        # Last month revenue
        prev_month_rev = db.query(func.sum(SalesOrder.total_amount))\
            .filter(SalesOrder.order_date >= first_day_prev_month, SalesOrder.order_date <= prev_month_end)\
            .scalar() or 0.0

        # Revenue growth percentage
        if prev_month_rev > 0:
            growth_pct = round(((this_month_rev - prev_month_rev) / prev_month_rev) * 100.0, 1)
        else:
            growth_pct = 0.0

        total_orders = db.query(func.count(SalesOrder.id)).scalar() or 0

        # Overdue invoices
        overdue_query = db.query(Invoice).filter(Invoice.status == "Overdue")
        overdue_invoices = overdue_query.all()
        overdue_count = len(overdue_invoices)
        overdue_amount = sum(inv.amount - inv.paid_amount for inv in overdue_invoices)

        # Low stock products
        low_stock_count = db.query(func.count(Product.id))\
            .filter(Product.stock_quantity <= Product.reorder_threshold)\
            .scalar() or 0

        # Active customers
        active_customers = db.query(func.count(Customer.id))\
            .filter(Customer.status == "Active")\
            .scalar() or 0

        return {
            "total_revenue": round(total_rev, 2),
            "monthly_revenue": round(this_month_rev, 2),
            "revenue_growth_pct": growth_pct,
            "total_orders_count": total_orders,
            "overdue_receivables": round(overdue_amount, 2),
            "overdue_invoices_count": overdue_count,
            "low_stock_products_count": low_stock_count,
            "active_customers_count": active_customers
        }

    @staticmethod
    def get_monthly_sales_trend(db: Session, months: int = 6) -> List[Dict[str, Any]]:
        today = datetime.date.today()
        # Find start date approx 6 months ago
        start_date = today.replace(day=1) - datetime.timedelta(days=30 * (months - 1))
        start_date = start_date.replace(day=1)

        orders = db.query(SalesOrder).filter(SalesOrder.order_date >= start_date).all()
        
        # Group by YYYY-MM
        monthly_data: Dict[str, Dict[str, Any]] = {}
        for order in orders:
            m_key = order.order_date.strftime("%b %Y")
            if m_key not in monthly_data:
                monthly_data[m_key] = {"month": m_key, "revenue": 0.0, "orders_count": 0, "sort_key": order.order_date.strftime("%Y-%m")}
            monthly_data[m_key]["revenue"] += order.total_amount
            monthly_data[m_key]["orders_count"] += 1

        # Sort chronologically
        sorted_trend = sorted(monthly_data.values(), key=lambda x: x["sort_key"])
        for item in sorted_trend:
            item["revenue"] = round(item["revenue"], 2)
            del item["sort_key"]

        return sorted_trend

    @staticmethod
    def get_top_selling_products(db: Session, limit: int = 5) -> List[Dict[str, Any]]:
        results = db.query(
            Product.name,
            Product.category,
            func.sum(SalesOrderItem.quantity).label("total_qty"),
            func.sum(SalesOrderItem.total_price).label("total_rev")
        ).join(SalesOrderItem, Product.id == SalesOrderItem.product_id)\
         .group_by(Product.id)\
         .order_by(desc("total_rev"))\
         .limit(limit)\
         .all()

        return [
            {
                "product_name": r[0],
                "category": r[1],
                "quantity_sold": int(r[2] or 0),
                "total_revenue": round(float(r[3] or 0.0), 2)
            }
            for r in results
        ]

    @staticmethod
    def get_overdue_invoices(db: Session) -> List[Dict[str, Any]]:
        today = datetime.date.today()
        invoices = db.query(Invoice).filter(Invoice.status == "Overdue").order_by(Invoice.due_date.asc()).all()
        
        result = []
        for inv in invoices:
            days_overdue = (today - inv.due_date).days if inv.due_date else 0
            unpaid_balance = round(inv.amount - inv.paid_amount, 2)
            result.append({
                "id": inv.id,
                "invoice_number": inv.invoice_number,
                "customer_name": inv.customer.name if inv.customer else "Unknown",
                "customer_email": inv.customer.email if inv.customer else "",
                "issue_date": inv.issue_date.isoformat(),
                "due_date": inv.due_date.isoformat(),
                "amount": inv.amount,
                "paid_amount": inv.paid_amount,
                "balance_due": unpaid_balance,
                "status": inv.status,
                "days_overdue": max(0, days_overdue)
            })
        return result

    @staticmethod
    def get_low_stock_products(db: Session) -> List[Dict[str, Any]]:
        products = db.query(Product)\
            .filter(Product.stock_quantity <= Product.reorder_threshold)\
            .order_by(Product.stock_quantity.asc())\
            .all()
        
        return [
            {
                "id": p.id,
                "sku": p.sku,
                "name": p.name,
                "category": p.category,
                "stock_quantity": p.stock_quantity,
                "reorder_threshold": p.reorder_threshold,
                "deficit": p.reorder_threshold - p.stock_quantity,
                "unit_cost": p.unit_cost
            }
            for p in products
        ]

    @staticmethod
    def get_customers(db: Session, search: Optional[str] = None) -> List[Dict[str, Any]]:
        query = db.query(Customer)
        if search:
            query = query.filter(or_(
                Customer.name.ilike(f"%{search}%"),
                Customer.email.ilike(f"%{search}%"),
                Customer.region.ilike(f"%{search}%")
            ))
        customers = query.order_by(Customer.name.asc()).all()
        return [
            {
                "id": c.id,
                "name": c.name,
                "email": c.email,
                "phone": c.phone,
                "region": c.region,
                "segment": c.segment,
                "credit_limit": c.credit_limit,
                "status": c.status
            }
            for c in customers
        ]

    @staticmethod
    def get_invoices(db: Session, status: Optional[str] = None, search: Optional[str] = None) -> List[Dict[str, Any]]:
        query = db.query(Invoice).join(Customer, Invoice.customer_id == Customer.id)
        if status:
            query = query.filter(Invoice.status == status)
        if search:
            query = query.filter(or_(
                Invoice.invoice_number.ilike(f"%{search}%"),
                Customer.name.ilike(f"%{search}%")
            ))
        invoices = query.order_by(Invoice.issue_date.desc()).limit(100).all()
        today = datetime.date.today()

        return [
            {
                "id": inv.id,
                "invoice_number": inv.invoice_number,
                "customer_name": inv.customer.name if inv.customer else "Unknown",
                "issue_date": inv.issue_date.isoformat(),
                "due_date": inv.due_date.isoformat(),
                "amount": inv.amount,
                "paid_amount": inv.paid_amount,
                "balance_due": round(inv.amount - inv.paid_amount, 2),
                "status": inv.status,
                "days_overdue": max(0, (today - inv.due_date).days) if inv.status == "Overdue" else 0
            }
            for inv in invoices
        ]

    @staticmethod
    def get_products(db: Session, category: Optional[str] = None, search: Optional[str] = None) -> List[Dict[str, Any]]:
        query = db.query(Product)
        if category:
            query = query.filter(Product.category == category)
        if search:
            query = query.filter(or_(
                Product.name.ilike(f"%{search}%"),
                Product.sku.ilike(f"%{search}%"),
                Product.category.ilike(f"%{search}%")
            ))
        products = query.order_by(Product.name.asc()).all()
        return [
            {
                "id": p.id,
                "sku": p.sku,
                "name": p.name,
                "category": p.category,
                "unit_price": p.unit_price,
                "unit_cost": p.unit_cost,
                "stock_quantity": p.stock_quantity,
                "reorder_threshold": p.reorder_threshold,
                "is_low_stock": p.stock_quantity <= p.reorder_threshold
            }
            for p in products
        ]
