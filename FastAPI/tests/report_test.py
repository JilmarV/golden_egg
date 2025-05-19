"""Test cases for Report endpoints."""

# pylint: disable=import-error, no-name-in-module, too-few-public-methods, redefined-outer-name

# Standard library
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Third-party
import pytest

# Application
from fastapi.testclient import TestClient
from app.main import app
from app.db.database import Base
from app.db.session import get_db


# Use in-memory SQLite for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def test_db():
    """Creates a fresh database for each test."""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client(test_db):
    """Overrides the dependency to use the test database."""

    def override_get_db():
        yield test_db

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


def test_create_report(client):
    """Test creating a report."""
    response = client.post(
        "/report/",
        json={
            "type": "Monthly Report",
            "dateReport": "2025-10-21",
            "content": "This is the content of the report.",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["type"] == "Monthly Report"
    assert data["content"] == "This is the content of the report."


def test_get_report(client):
    """Test retrieving a report."""
    response = client.post(
        "/report/",
        json={
            "type": "Monthly Report",
            "dateReport": "2025-06-15",
            "content": "This is the content of the report.",
        },
    )
    assert response.status_code == 201
    data = response.json()
    report_id = data["id"]
    response = client.get(f"/report/{report_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["type"] == "Monthly Report"
    assert data["dateReport"] == "2025-06-15"
    assert data["content"] == "This is the content of the report."


def test_get_all_reports(client):
    """Test retrieving all reports."""
    response = client.post(
        "/report/",
        json={
            "type": "Monthly Report",
            "dateReport": "2025-11-12",
            "content": "This is the content of the report.",
        },
    )
    assert response.status_code == 201
    data = response.json()
    response = client.get("/report/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0


def test_update_report(client):
    """Test updating a report."""
    response = client.post(
        "/report/",
        json={
            "type": "Monthly Report",
            "dateReport": "2025-01-01",
            "content": "This is the content of the report.",
        },
    )
    assert response.status_code == 201
    data = response.json()
    report_id = data["id"]
    response = client.put(
        f"/report/{report_id}",
        json={
            "type": "Updated Report",
            "dateReport": "2025-02-02",
            "content": "Updated content.",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["type"] == "Updated Report"
    assert data["dateReport"] == "2025-02-02"
    assert data["content"] == "Updated content."


def test_delete_report(client):
    """Test deleting a report."""
    response = client.post(
        "/report/",
        json={
            "type": "Monthly Report",
            "dateReport": "2025-03-03",
            "content": "This is the content of the report.",
        },
    )
    assert response.status_code == 201
    data = response.json()
    report_id = data["id"]
    response = client.delete(f"/report/{report_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Report deleted successfully"

    # Verify that the report no longer exists
    response = client.get(f"/report/{report_id}")
    assert response.status_code == 404

def test_get_total_client_bills_route(client):
    """Test retrieving all reports."""
    client.post("/role/", json={"name": "CUSTOMER"})
    client.post("/user/", json={"name": "User", "phone_number": "3133333333", "email": "SomeEmail@Mail.com", "username":"user","password": "123","address": "Somewhere","enabled": True, "role_ids": [1]})
    client.post("/user/", json={"name": "User", "phone_number": "3133333333", "email": "SomeEmail@Mail.com", "username":"user","password": "123","address": "Somewhere","enabled": True, "role_ids": [1]})
    client.post("/order/",json={"totalPrice": 20100,"state": "pending","user_id": 1,},)
    client.post("/order/",json={"totalPrice": 20100,"state": "pending","user_id": 2,},)
    client.post("/bill/", json={"totalprice": 1000, "paid": False, "order_id": 1})
    client.post("/bill/", json={"totalprice": 2000, "paid": False, "order_id": 1})
    client.post("/bill/", json={"totalprice": 3000, "paid": False, "order_id": 1})
    client.post("/bill/", json={"totalprice": 4000, "paid": False, "order_id": 2})
    response = client.post(
        "/report/",
        json={
            "type": "Monthly Report",
            "dateReport": "2025-11-12",
            "content": "This is the content of the report.",
        },
    )
    assert response.status_code == 201
    data = response.json()
    response = client.get("/bills/clients/month-total")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0

def test_get_top_client_spender_this_month(client):
    """Test retrieving all reports."""
    client.post("/role/", json={"name": "CUSTOMER"})
    client.post("/user/", json={"name": "User", "phone_number": "3133333333", "email": "SomeEmail@Mail.com", "username":"user","password": "123","address": "Somewhere","enabled": True, "role_ids": [1]})
    client.post("/user/", json={"name": "User", "phone_number": "3133333333", "email": "SomeEmail@Mail.com", "username":"user","password": "123","address": "Somewhere","enabled": True, "role_ids": [1]})
    client.post("/order/",json={"totalPrice": 20100,"state": "pending","user_id": 1,},)
    client.post("/order/",json={"totalPrice": 20100,"state": "pending","user_id": 2,},)
    client.post("/bill/", json={"totalprice": 1000, "paid": False, "order_id": 1})
    client.post("/bill/", json={"totalprice": 2000, "paid": False, "order_id": 1})
    client.post("/bill/", json={"totalprice": 3000, "paid": False, "order_id": 1})
    client.post("/bill/", json={"totalprice": 4000, "paid": False, "order_id": 2})
    response = client.post(
        "/report/",
        json={
            "type": "Monthly Report",
            "dateReport": "2025-11-12",
            "content": "This is the content of the report.",
        },
    )
    assert response.status_code == 201
    data = response.json()
    response = client.get("/bills/monthlySalesTotal")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0