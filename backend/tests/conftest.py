import pytest
from fastapi.testclient import TestClient
from app.main import app, init_db

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    init_db()

@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client
