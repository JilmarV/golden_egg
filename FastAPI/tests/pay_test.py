"""Test cases for Pay endpoints."""

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
    
def test_create_pay(client):
    """Test creating a pay."""
    client.post("/role/", json={"name": "CUSTOMER"})
    client.post("/user/", json={"name": "User", "phone_number": "3133333333", "email": "SomeEmail@Mail.com", "username":"user","password": "123","address": "Somewhere","enabled": True, "role_ids": [1]})
    client.post("/order/",json={"totalPrice": 20100,"state": "pending","user_id": 1,},)
    client.post("/bill/", json={"totalprice": 5000, "paid": False, "order_id": 1})
    response = client.post(
        "/pay/",json={"amount_paid": 20100,"payment_method": "cash", "user_id": 1,"bill_id": 1},
    )
    print(response.json())
    assert response.status_code == 201
    data = response.json()
    assert data["amount_paid"] == 20100
    assert data["payment_method"] == "cash"
    assert data["user_id"] == 1
    assert data["bill_id"] == 1
    assert "id" in data
    
    
def test_read_pays(client):
    """Test retrieving all pays."""
    client.post("/role/", json={"name": "CUSTOMER"})
    client.post("/user/", json={"name": "User", "phone_number": "3133333333", "email": "SomeEmail@Mail.com", "username":"user","password": "123","address": "Somewhere","enabled": True, "role_ids": [1]})
    client.post("/bill/", json={"totalprice": 45000, "paid": False, "order_id": 1})
    client.post(
        "/pay/",json={"amount_paid": 20100,"payment_method": "cash", "user_id": 1,"bill_id": 1},
    )
    client.post(
        "/pay/",json={"amount_paid": 2000,"payment_method": "cash", "user_id": 1,"bill_id": 1},
    )
    response = client.get("/pay/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    
def test_read_pay(client):
    """Test retrieving a specific pay."""
    client.post("/role/", json={"name": "CUSTOMER"})
    client.post("/user/", json={"name": "User", "phone_number": "3133333333", "email": "SomeEmail@Mail.com", "username":"user","password": "123","address": "Somewhere","enabled": True, "role_ids": [1]})
    client.post("/bill/", json={"totalprice": 5000, "paid": False, "order_id": 1})
    create_response = client.post(
        "/pay/",json={"amount_paid": 20100,"payment_method": "cash", "user_id": 1,"bill_id": 1},
    )
    created_pay = create_response.json()
    response = client.get(f"/pay/{created_pay['id']}")
    assert response.status_code == 200
    data = response.json()
    assert data["amount_paid"] == 20100
    assert data["payment_method"] == "cash"
    

def test_update_pay(client):
    """Test updating a pay."""
    client.post("/role/", json={"name": "CUSTOMER"})
    client.post("/user/", json={"name": "User", "phone_number": "3133333333", "email": "SomeEmail@Mail.com", "username":"user","password": "123","address": "Somewhere","enabled": True, "role_ids": [1]})
    client.post("/bill/", json={"totalprice": 5000, "paid": False, "order_id": 1})
    create_response = client.post(
        "/pay/",json={"amount_paid": 20100,"payment_method": "cash", "user_id": 1,"bill_id": 1},
    )
    created_pay = create_response.json()
    response = client.put(
        f"/pay/{created_pay['id']}",
        json={"amount_paid": 30000,"payment_method": "credit_card", "user_id": 1,"bill_id": 1},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["amount_paid"] == 30000
    assert data["payment_method"] == "credit_card"


def test_delete_pay(client):
    """Test deleting a pay."""
    client.post("/role/", json={"name": "CUSTOMER"})
    client.post("/user/", json={"name": "User", "phone_number": "3133333333", "email": "SomeEmail@Mail.com", "username":"user","password": "123","address": "Somewhere","enabled": True, "role_ids": [1]})
    client.post("/bill/", json={"totalprice": 5000, "paid": False, "order_id": 1})
    create_response = client.post(
        "/pay/",json={"amount_paid": 20100,"payment_method": "cash", "user_id": 1,"bill_id": 1},
    )
    created_pay = create_response.json()
    response = client.delete(f"/pay/{created_pay['id']}")
    assert response.status_code == 200
    get_response = client.get(f"/pay/{created_pay['id']}")
    assert get_response.status_code == 404

def test_total_earnings(client):
    """Test retrieving a specific pay."""
    client.post("/role/", json={"name": "CUSTOMER"})
    client.post("/user/", json={"name": "User", "phone_number": "3133333333", "email": "SomeEmail@Mail.com", "username":"user","password": "123","address": "Somewhere","enabled": True, "role_ids": [1]})
    client.post("/bill/", json={"totalprice": 5000, "paid": False, "order_id": 1})
    client.post("/pay/",json={"amount_paid": 20100,"payment_method": "cash", "user_id": 1,"bill_id": 1},)
    response = client.get(f"/pay/earnings/total_earnings/")
    print(response.json())
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    