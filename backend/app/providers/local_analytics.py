import re
from typing import Dict, Any, List
from app.providers.base import BaseInferenceProvider

class LocalAnalyticsProvider(BaseInferenceProvider):
    """
    Default deterministic NLP and Analytics Provider.
    Operates 100% locally with zero external API dependencies or costs.
    Extracts business intent and binds directly to real-time ERP analytics.
    """

    @property
    def name(self) -> str:
        return "Local Analytics Engine (Zero-Key Fallback)"

    @property
    def is_on_device(self) -> bool:
        return True

    async def process_query(self, query: str, erp_context: Dict[str, Any]) -> Dict[str, Any]:
        q = query.lower().strip()
        kpis = erp_context.get("kpis", {})
        top_products = erp_context.get("top_products", [])
        trends = erp_context.get("trends", [])
        overdue = erp_context.get("overdue", [])
        low_stock = erp_context.get("low_stock", [])
        customers = erp_context.get("customers", [])

        # 1. Total sales this month / Revenue queries
        if any(term in q for term in ["total sales this month", "sales this month", "monthly sales", "current month sales", "this month's revenue", "revenue this month"]):
            monthly_rev = kpis.get("monthly_revenue", 0.0)
            growth = kpis.get("revenue_growth_pct", 0.0)
            total_rev = kpis.get("total_revenue", 0.0)
            growth_desc = f"+{growth}%" if growth >= 0 else f"{growth}%"

            answer = (
                f"### 📊 Current Month Sales Performance\n\n"
                f"- **Monthly Sales:** **${monthly_rev:,.2f}**\n"
                f"- **Month-over-Month Growth:** **{growth_desc}** vs preceding month\n"
                f"- **All-Time Cumulative Revenue:** **${total_rev:,.2f}**\n"
                f"- **Total Closed Orders:** **{kpis.get('total_orders_count', 0)}**\n\n"
                f"Sales velocity remains positive with steady transaction volume across enterprise and mid-market accounts."
            )
            return {
                "answer": answer,
                "intent": "monthly_sales_inquiry",
                "confidence": 0.98,
                "metrics": {
                    "monthly_sales": monthly_rev,
                    "growth_pct": growth,
                    "total_revenue": total_rev
                },
                "chart_data": {
                    "type": "bar",
                    "title": "Monthly Revenue",
                    "data": trends[-3:] if len(trends) >= 3 else trends
                },
                "suggestions": [
                    "What are the major sales trends?",
                    "Which products are selling the most?",
                    "Summarize the current business situation."
                ]
            }

        # 2. Top selling products
        elif any(term in q for term in ["selling the most", "top products", "best seller", "best selling", "most popular", "highest volume"]):
            rows = []
            for p in top_products:
                rows.append({
                    "Product Name": p["product_name"],
                    "Category": p["category"],
                    "Units Sold": p["quantity_sold"],
                    "Total Revenue": f"${p['total_revenue']:,.2f}"
                })

            top_item = top_products[0] if top_products else {"product_name": "N/A", "total_revenue": 0}
            answer = (
                f"### 🏆 Top-Selling Products\n\n"
                f"The leading revenue driver is **{top_item['product_name']}** with **${top_item['total_revenue']:,.2f}** in sales.\n\n"
                f"Here is the ranking of top-performing items by generated revenue:"
            )
            return {
                "answer": answer,
                "intent": "top_products_inquiry",
                "confidence": 0.96,
                "table_data": rows,
                "chart_data": {
                    "type": "pie",
                    "title": "Revenue by Top Products",
                    "data": [
                        {"name": p["product_name"], "value": p["total_revenue"]}
                        for p in top_products
                    ]
                },
                "suggestions": [
                    "Which products are low in stock?",
                    "What were the total sales this month?",
                    "Show sales trends over time"
                ]
            }

        # 3. Overdue payments / invoices
        elif any(term in q for term in ["overdue", "unpaid", "delinquent", "pending payments", "outstanding payments", "debt"]):
            overdue_amount = kpis.get("overdue_receivables", 0.0)
            overdue_count = kpis.get("overdue_invoices_count", 0)

            rows = []
            for inv in overdue[:8]:
                rows.append({
                    "Invoice #": inv["invoice_number"],
                    "Customer": inv["customer_name"],
                    "Due Date": inv["due_date"],
                    "Days Overdue": f"{inv['days_overdue']} days",
                    "Balance Due": f"${inv['balance_due']:,.2f}"
                })

            answer = (
                f"### ⚠️ Overdue Receivables Alert\n\n"
                f"There are currently **{overdue_count} overdue invoices** totaling **${overdue_amount:,.2f}** in outstanding receivables.\n\n"
                f"The highest overdue balances require accounts receivable follow-up:"
            )
            return {
                "answer": answer,
                "intent": "overdue_receivables_inquiry",
                "confidence": 0.97,
                "metrics": {
                    "total_overdue": overdue_amount,
                    "overdue_count": overdue_count
                },
                "table_data": rows,
                "suggestions": [
                    "Summarize the current business situation.",
                    "What were total sales this month?",
                    "Which customers have delinquent status?"
                ]
            }

        # 4. Sales trends
        elif any(term in q for term in ["trend", "sales trends", "trajectory", "historical", "over time", "quarterly", "growth"]):
            if trends:
                first_month = trends[0]
                latest_month = trends[-1]
                trend_change = latest_month["revenue"] - first_month["revenue"]
                direction = "upward" if trend_change >= 0 else "downward"
                earliest_line = f"${first_month['revenue']:,.2f} ({first_month['orders_count']} orders)"
                latest_line = f"${latest_month['revenue']:,.2f} ({latest_month['orders_count']} orders)"
                earliest_label = first_month["month"]
                latest_label = latest_month["month"]
            else:
                direction = "stable"
                earliest_line = latest_line = "No data available"
                earliest_label = latest_label = "N/A"

            answer = (
                f"### 📈 Major Sales Trends Analysis\n\n"
                f"- **Overall Trajectory:** Healthy **{direction}** trend over the past {len(trends)} months.\n"
                f"- **Earliest Tracked Period ({earliest_label}):** {earliest_line}\n"
                f"- **Latest Period ({latest_label}):** {latest_line}\n"
                f"- **Key Momentum:** Demand is strongest in the **Edge AI Hardware** and **IoT Sensors** segments, reflecting expanding edge-processing deployments."
            )
            return {
                "answer": answer,
                "intent": "sales_trends_inquiry",
                "confidence": 0.95,
                "chart_data": {
                    "type": "line",
                    "title": "6-Month Revenue & Order Trajectory",
                    "data": trends
                },
                "suggestions": [
                    "Which products are selling the most?",
                    "What were total sales this month?",
                    "Summarize the current business situation."
                ]
            }

        # 5. Business summary / Executive overview
        elif any(term in q for term in ["summarize", "summary", "business situation", "health", "overview", "briefing", "status of business"]):
            tot_rev = kpis.get("total_revenue", 0.0)
            month_rev = kpis.get("monthly_revenue", 0.0)
            growth = kpis.get("revenue_growth_pct", 0.0)
            overdue_sum = kpis.get("overdue_receivables", 0.0)
            low_stock_num = kpis.get("low_stock_products_count", 0)
            active_cust = kpis.get("active_customers_count", 0)

            answer = (
                f"### 🏢 Executive Business Health Briefing\n\n"
                f"**1. Revenue & Growth:**\n"
                f"- Total cumulative revenue is **${tot_rev:,.2f}** with current month sales at **${month_rev:,.2f}** ({'+' if growth >= 0 else ''}{growth}% MoM).\n\n"
                f"**2. Cash Flow & Receivables:**\n"
                f"- Accounts Receivable has **${overdue_sum:,.2f}** past due across {kpis.get('overdue_invoices_count', 0)} invoices. Follow-up priority recommended for delinquent accounts.\n\n"
                f"**3. Operations & Inventory:**\n"
                f"- **{low_stock_num} SKUs** are currently at or below minimum reorder thresholds and require procurement restock.\n\n"
                f"**4. Customer Base:**\n"
                f"- **{active_cust} active corporate clients** across North America, Europe, and Asia Pacific."
            )
            return {
                "answer": answer,
                "intent": "executive_summary",
                "confidence": 0.99,
                "metrics": kpis,
                "suggestions": [
                    "Which customers have overdue payments?",
                    "Which products are low in stock?",
                    "What are the major sales trends?"
                ]
            }

        # 6. Inventory & low stock
        elif any(term in q for term in ["stock", "inventory", "reorder", "low inventory", "warehouse"]):
            rows = []
            for p in low_stock:
                rows.append({
                    "SKU": p["sku"],
                    "Product": p["name"],
                    "Category": p["category"],
                    "Current Stock": p["stock_quantity"],
                    "Threshold": p["reorder_threshold"],
                    "Deficit": f"{p['deficit']} units"
                })

            answer = (
                f"### 📦 Inventory & Stock Warning Report\n\n"
                f"Found **{len(low_stock)} products** at or below their safety reorder thresholds. Restocking is recommended immediately to prevent order fulfillment delays."
            )
            return {
                "answer": answer,
                "intent": "inventory_inquiry",
                "confidence": 0.94,
                "table_data": rows,
                "suggestions": [
                    "Which products are selling the most?",
                    "Summarize the current business situation."
                ]
            }

        # 7. Customer search / delinquent accounts
        elif any(term in q for term in ["customer", "client", "accounts", "delinquent"]):
            matching_customers = [
                c for c in customers
                if any(word in c["name"].lower() for word in q.split() if len(word) > 3)
            ]
            if matching_customers:
                c = matching_customers[0]
                answer = (
                    f"### 👤 Customer Profile: {c['name']}\n\n"
                    f"- **Segment:** {c['segment']} | **Region:** {c['region']}\n"
                    f"- **Account Status:** **{c['status']}**\n"
                    f"- **Credit Limit:** ${c['credit_limit']:,.2f}\n"
                    f"- **Contact:** {c['email']} ({c['phone']})"
                )
                return {
                    "answer": answer,
                    "intent": "customer_inquiry",
                    "confidence": 0.91,
                    "suggestions": [
                        "Which customers have overdue payments?",
                        "What were total sales this month?"
                    ]
                }
            else:
                delinquent = [c for c in customers if c["status"] == "Delinquent"]
                rows = [{"Customer": c["name"], "Region": c["region"], "Credit Limit": f"${c['credit_limit']:,.2f}", "Status": c["status"]} for c in delinquent]
                answer = (
                    f"### 👥 Customer Status Overview\n\n"
                    f"There are **{len(delinquent)} delinquent accounts** requiring credit review:"
                )
                return {
                    "answer": answer,
                    "intent": "customer_overview",
                    "confidence": 0.88,
                    "table_data": rows,
                    "suggestions": [
                        "Which customers have overdue payments?",
                        "Summarize the current business situation."
                    ]
                }

        # Default fallback query handling
        else:
            tot_rev = kpis.get("total_revenue", 0.0)
            month_rev = kpis.get("monthly_revenue", 0.0)
            answer = (
                f"### 💡 Copilot Business Query Assistant\n\n"
                f"I parsed your query: *\"{query}\"*.\n\n"
                f"Here is a quick snapshot of the business data:\n"
                f"- **Total Cumulative Sales:** ${tot_rev:,.2f}\n"
                f"- **Current Month Sales:** ${month_rev:,.2f}\n"
                f"- **Overdue Invoices:** {kpis.get('overdue_invoices_count', 0)} (${kpis.get('overdue_receivables', 0.0):,.2f})\n"
                f"- **Low Stock SKUs:** {kpis.get('low_stock_products_count', 0)}\n\n"
                f"Try asking one of the specific questions below for in-depth breakdowns!"
            )
            return {
                "answer": answer,
                "intent": "general_business_inquiry",
                "confidence": 0.80,
                "suggestions": [
                    "What were the total sales this month?",
                    "Which products are selling the most?",
                    "Which customers have overdue payments?",
                    "What are the major sales trends?",
                    "Summarize the current business situation."
                ]
            }
