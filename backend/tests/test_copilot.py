import pytest

def test_copilot_sales_this_month(client):
    resp = client.post("/api/copilot/query", json={"query": "What were the total sales this month?"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["intent"] == "monthly_sales_inquiry"
    assert "Current Month Sales" in data["answer"]
    assert "metrics" in data
    assert data["confidence"] > 0.8

def test_copilot_top_selling_products(client):
    resp = client.post("/api/copilot/query", json={"query": "Which products are selling the most?"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["intent"] == "top_products_inquiry"
    assert "Top-Selling Products" in data["answer"]
    assert data["table_data"] is not None
    assert len(data["table_data"]) > 0

def test_copilot_overdue_payments(client):
    resp = client.post("/api/copilot/query", json={"query": "Which customers have overdue payments?"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["intent"] == "overdue_receivables_inquiry"
    assert "Overdue Receivables" in data["answer"]
    assert data["table_data"] is not None

def test_copilot_sales_trends(client):
    resp = client.post("/api/copilot/query", json={"query": "What are the major sales trends?"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["intent"] == "sales_trends_inquiry"
    assert "Sales Trends Analysis" in data["answer"]
    assert data["chart_data"] is not None

def test_copilot_business_summary(client):
    resp = client.post("/api/copilot/query", json={"query": "Summarize the current business situation."})
    assert resp.status_code == 200
    data = resp.json()
    assert data["intent"] == "executive_summary"
    assert "Executive Business Health Briefing" in data["answer"]
    assert data["metrics"] is not None

def test_copilot_inventory_query(client):
    resp = client.post("/api/copilot/query", json={"query": "Which products are low in stock?"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["intent"] == "inventory_inquiry"
    assert "Inventory & Stock Warning Report" in data["answer"]
