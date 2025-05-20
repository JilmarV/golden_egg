"""Test cases for Order endpoints."""

# pylint: disable=import-error, no-name-in-module, too-few-public-methods, redefined-outer-name

# Standard library
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Third-party
import pytest
from fastapi.testclient import TestClient

# Application
from app.main import app
from app.db.database import Base
from app.db.session import get_db

# In-memory database
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


def test_create_order(client):
    """Test creating an order."""
    client.post("/role/", json={"name": "CUSTOMER"})
    client.post("/user/", json={"name": "User", "phone_number": "3133333333", "email": "SomeEmail@Mail.com", "username":"user","password": "123","address": "Somewhere","enabled": True, "role_ids": [1]})
    response = client.post(
        "/order/",
        json={
            "totalPrice": 20100,
            "state": "pending",
            "user_id": 1,
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["totalPrice"] == 20100
    assert data["state"] == "pending"
    assert "id" in data
    assert data["user_id"] == 1


def test_get_orders(client):
    """Test retrieving all orders."""
    client.post("/role/", json={"name": "CUSTOMER"})
    client.post("/user/", json={"name": "User", "phone_number": "3133333333", "email": "SomeEmail@Mail.com", "username":"user","password": "123","address": "Somewhere","enabled": True, "role_ids": [1]})
    client.post(
        "/order/",
        json={
            "totalPrice": 40000,
            "state": "pending",
            "user_id": 1,
        },
    )
    response = client.get("/order/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_order(client):
    """Test retrieving a specific order."""
    client.post("/role/", json={"name": "CUSTOMER"})
    client.post("/user/", json={"name": "User", "phone_number": "3133333333", "email": "SomeEmail@Mail.com", "username":"user","password": "123","address": "Somewhere","enabled": True, "role_ids": [1]})
    response = client.post(
        "/order/",
        json={
            "totalPrice": 40000,
            "state": "pending",
            "user_id": 1
        },
    )
    created_order = response.json()
    response = client.get(f"/order/{created_order['id']}")
    print(response.json())
    assert response.status_code == 200
    data = response.json()
    assert data["totalPrice"] == 40000


def test_update_order(client):
    """Test updating an order."""
    client.post("/role/", json={"name": "CUSTOMER"})
    client.post("/user/", json={"name": "User", "phone_number": "3133333333", "email": "SomeEmail@Mail.com", "username":"user","password": "123","address": "Somewhere","enabled": True, "role_ids": [1]})
    response = client.post(
        "/order/",
        json={
            "totalPrice": 40000,
            "state": "pending",
            "user_id": 1,
        },
    )
    assert response.status_code == 201
    data = response.json()
    order_id = data["id"]
    response = client.put(
        f"/order/{order_id}",
        json={
            "totalPrice": 50000,
            "state": "shipped",
            "user_id": 1,
        },
    )
    
    print(response.json())
    assert response.status_code == 200
    data = response.json()
    assert data["totalPrice"] == 50000
    assert data["state"] == "shipped"
    assert data["user_id"] == 1


def test_delete_order(client):
    """Test deleting an order."""
    client.post("/role/", json={"name": "CUSTOMER"})
    client.post("/user/", json={"name": "User", "phone_number": "3133333333", "email": "SomeEmail@Mail.com", "username":"user","password": "123","address": "Somewhere","enabled": True, "role_ids": [1]})
    response = client.post(
        "/order/",
        json={
            "totalPrice": 40000,
            "state": "pending",
            "user_id": 1,
        },
    )
    created_order = response.json()
    response = client.delete(f"/order/{created_order['id']}")
    assert response.status_code == 200
    get_response = client.get(f"/order/{created_order['id']}")
    assert get_response.status_code == 404
    
def test_get_orders_year_month(client):
    """Test retrieving a specific order."""
    client.post("/role/", json={"name": "CUSTOMER"})
    client.post("/user/", json={"name": "User", "phone_number": "3133333333", "email": "SomeEmail@Mail.com", "username":"user","password": "123","address": "Somewhere","enabled": True, "role_ids": [1]})
    response = client.post(
        "/order/",
        json={
            "totalPrice": 40000,
            "state": "pending",
            "user_id": 1
        },
    )
    response = client.post(
        "/order/",
        json={
            "totalPrice": 30000,
            "state": "pending",
            "user_id": 1
        },
    )
    response = client.post(
        "/order/",
        json={
            "totalPrice": 20000,
            "state": "pending",
            "user_id": 1
        },
    )
    created_order = response.json()
    response = client.get("/order/search/totalOrdersMonth", params={"year": 2025, "month": 5})
    print(response.json())
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3