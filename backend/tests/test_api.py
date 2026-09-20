import pytest

def test_health_endpoint(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "online"
    assert "provider_info" in data

def test_dashboard_kpis(client):
    response = client.get("/api/dashboard/kpis")
    assert response.status_code == 200
    data = response.json()
    assert "total_revenue" in data
    assert data["total_revenue"] > 0
    assert "monthly_revenue" in data
    assert "overdue_receivables" in data
    assert "low_stock_products_count" in data

def test_sales_trends(client):
    response = client.get("/api/dashboard/trends?months=6")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert "month" in data[0]
    assert "revenue" in data[0]

def test_top_products(client):
    response = client.get("/api/dashboard/top-products?limit=5")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) <= 5
    if len(data) > 0:
        assert "product_name" in data[0]
        assert "total_revenue" in data[0]

def test_erp_invoices(client):
    response = client.get("/api/erp/invoices")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert "invoice_number" in data[0]

def test_erp_customers(client):
    response = client.get("/api/erp/customers")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 10

def test_erp_low_stock(client):
    response = client.get("/api/erp/low-stock")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
