"""Test cases for Bill endpoints."""

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


def test_create_bill(client):
    """Test creating a bill."""
    response = client.post("/role/", json={"name": "EMPLOYEE"})
    response = client.post("/user/", json={"name": "User", "phone_number": "3133333333", "email": "SomeEmail@Mail.com", "username":"user","password": "123","address": "Somewhere","enabled": True, "role_ids": [1]})
    assert response.status_code == 201
    print(response.json())
    response = client.post("/order/",json={"totalPrice": 20100,"state": "pending","user_id": 1,},)
    assert response.status_code == 201
    response = client.post("/bill/", json={"totalprice": 5000, "paid": False, "order_id": 1})
    print(response.json())
    assert response.status_code == 201
    data = response.json()
    assert data["totalprice"] == 5000
    assert data["paid"] is False
    assert "id" in data


def test_read_bills(client):
    """Test retrieving all bills."""
    response = client.post("/role/", json={"name": "EMPLOYEE"})
    response = client.post("/user/", json={"name": "User", "phone_number": "3133333333", "email": "SomeEmail@Mail.com", "username":"user","password": "123","address": "Somewhere","enabled": True, "role_ids": [1]})
    assert response.status_code == 201
    response = client.post("/order/",json={"totalPrice": 20100,"state": "pending","user_id": 1,},)
    client.post("/bill/", json={"totalprice": 2010, "paid": False, "order_id": 1})
    response = client.get("/bill/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0


def test_read_bill(client):
    """Test retrieving a specific bill."""
    response = client.post("/role/", json={"name": "EMPLOYEE"})
    response = client.post("/user/", json={"name": "User", "phone_number": "3133333333", "email": "SomeEmail@Mail.com", "username":"user","password": "123","address": "Somewhere","enabled": True, "role_ids": [1]})
    response = client.post("/order/",json={"totalPrice": 20100,"state": "pending","user_id": 1,},)
    create_response = client.post("/bill/", json={"totalprice": 3000, "paid": False, "order_id": 1})
    created_bill = create_response.json()
    response = client.get(f"/bill/{created_bill['id']}")
    assert response.status_code == 200
    data = response.json()
    assert data["totalprice"] == 3000


def test_update_bill(client):
    """Test updating a bill."""
    response = client.post("/role/", json={"name": "EMPLOYEE"})
    response = client.post("/user/", json={"name": "User", "phone_number": "3133333333", "email": "SomeEmail@Mail.com", "username":"user","password": "123","address": "Somewhere","enabled": True, "role_ids": [1]})
    response = client.post("/order/",json={"totalPrice": 20100,"state": "pending","user_id": 1,},)
    create_response = client.post("/bill/", json={"totalprice": 1000, "paid": False, "order_id": 1})
    created_bill = create_response.json()
    response = client.put(
        f"/bill/{created_bill['id']}",
        json={"totalprice": 1500, "paid": True, "order_id": 1},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["totalprice"] == 1500
    assert data["paid"] is True


def test_delete_bill(client):
    """Test deleting a bill."""
    client.post("/role/", json={"name": "EMPLOYEE"})
    response = client.post("/user/", json={"name": "User", "phone_number": "3133333333", "email": "SomeEmail@Mail.com", "username":"user","password": "123","address": "Somewhere","enabled": True, "role_ids": [1]})
    response = client.post("/order/",json={"totalPrice": 20100,"state": "pending","user_id": 1,},)
    create_response = client.post("/bill/", json={"totalprice": 8000, "paid": False, "order_id": 1})
    created_bill = create_response.json()
    response = client.delete(f"/bill/{created_bill['id']}")
    assert response.status_code == 200
    get_response = client.get(f"/bill/{created_bill['id']}")
    assert get_response.status_code == 404

def test_count_this_month_bills(client):
    """Test counting bills for the current month."""
    client.post("/role/", json={"name": "CUSTOMER"})
    client.post("/user/", json={"name": "User", "phone_number": "3143333333", "email": "SomeEmail2@Mail.com", "username":"user2","password": "123","address": "Somewh2ere","enabled": True, "role_ids": [1]})
    client.post("/user/", json={"name": "User", "phone_number": "3133333333", "email": "SomeEmail@Mail.com", "username":"user","password": "123","address": "Somewhere","enabled": True, "role_ids": [1]})
    client.post("/order/",json={"totalPrice": 20100,"state": "pending","user_id": 1,},)
    client.post("/order/",json={"totalPrice": 20100,"state": "pending","user_id": 2,},)
    client.post("/bill/", json={"totalprice": 1000, "paid": False, "order_id": 1})
    client.post("/bill/", json={"totalprice": 2000, "paid": False, "order_id": 1})
    client.post("/bill/", json={"totalprice": 3000, "paid": False, "order_id": 1})
    client.post("/bill/", json={"totalprice": 4000, "paid": False, "order_id": 2})
    response = client.post("/bill/", json={"totalprice": 5000, "paid": False, "order_id": 2})
    print(response.json())
    response = client.get("/bill/count_this_month/")
    print(response.json())
    assert response.status_code == 200
    count = response.json()
    assert isinstance(count, int)
    assert count > 0

def test_best_client(client):
    """Test the customer with the most bills."""
    client.post("/role/", json={"name": "CUSTOMER"})
    client.post("/user/", json={"name": "User", "phone_number": "3143333333", "email": "SomeEmail2@Mail.com", "username":"user2","password": "123","address": "Somewh2ere","enabled": True, "role_ids": [1]})
    client.post("/user/", json={"name": "User", "phone_number": "3133333333", "email": "SomeEmail@Mail.com", "username":"user","password": "123","address": "Somewhere","enabled": True, "role_ids": [1]})
    client.post("/order/",json={"totalPrice": 20100,"state": "pending","user_id": 1,},)
    client.post("/order/",json={"totalPrice": 20100,"state": "pending","user_id": 2,},)
    client.post("/bill/", json={"totalprice": 1000, "paid": False, "order_id": 1})
    client.post("/bill/", json={"totalprice": 2000, "paid": False, "order_id": 1})
    client.post("/bill/", json={"totalprice": 3000, "paid": False, "order_id": 1})
    client.post("/bill/", json={"totalprice": 4000, "paid": False, "order_id": 2})
    response = client.post("/bill/", json={"totalprice": 5000, "paid": False, "order_id": 2})
    print(response.json())
    response = client.get("/bill/bestCustomer/")
    print(response.json())
    assert response.status_code == 200
    print(response.json())

def test_get_all_company(client):
    """Test the customer with the most bills."""
    client.post("/role/", json={"name": "EMPLOYEE"})
    client.post("/role/", json={"name": "ADMIN"})
    client.post("/user/", json={"name": "User", "phone_number": "3143333333", "email": "SomeEmail2@Mail.com", "username":"user2","password": "123","address": "Somewh2ere","enabled": True, "role_ids": [1]})
    client.post("/user/", json={"name": "User", "phone_number": "3133333333", "email": "SomeEmail@Mail.com", "username":"user","password": "123","address": "Somewhere","enabled": True, "role_ids": [2]})
    client.post("/order/",json={"totalPrice": 20100,"state": "pending","user_id": 1,},)
    client.post("/order/",json={"totalPrice": 20100,"state": "pending","user_id": 2,},)
    client.post("/bill/", json={"totalprice": 1000, "paid": False, "order_id": 1})
    client.post("/bill/", json={"totalprice": 2000, "paid": False, "order_id": 1})
    client.post("/bill/", json={"totalprice": 3000, "paid": False, "order_id": 1})
    client.post("/bill/", json={"totalprice": 4000, "paid": False, "order_id": 2})
    response = client.post("/bill/", json={"totalprice": 5000, "paid": False, "order_id": 2})
    response = client.get("/bill/getAllOfCompany/")
    print(response.json())
    assert response.status_code == 200
    print(response.json())

def test_get_all_from_customers(client):
    """Test the customer with the most bills."""
    client.post("/role/", json={"name": "EMPLOYEE"})
    client.post("/role/", json={"name": "CUSTOMER"})
    client.post("/user/", json={"name": "User", "phone_number": "3143333333", "email": "SomeEmail2@Mail.com", "username":"user2","password": "123","address": "Somewh2ere","enabled": True, "role_ids": [1]})
    client.post("/user/", json={"name": "User", "phone_number": "3133333333", "email": "SomeEmail@Mail.com", "username":"user","password": "123","address": "Somewhere","enabled": True, "role_ids": [2]})
    client.post("/order/",json={"totalPrice": 20100,"state": "pending","user_id": 1,},)
    client.post("/order/",json={"totalPrice": 20100,"state": "pending","user_id": 2,},)
    client.post("/bill/", json={"totalprice": 1000, "paid": False, "order_id": 1})
    client.post("/bill/", json={"totalprice": 2000, "paid": False, "order_id": 1})
    client.post("/bill/", json={"totalprice": 3000, "paid": False, "order_id": 1})
    client.post("/bill/", json={"totalprice": 4000, "paid": False, "order_id": 2})
    response = client.post("/bill/", json={"totalprice": 5000, "paid": False, "order_id": 2})
    response = client.get("/bill/getAllOfCustomers/")
    print(response.json())
    assert response.status_code == 200
    print(response.json())

def test_get_all_monthly_from_customer(client):
    """Test the customer with the most bills."""
    client.post("/role/", json={"name": "EMPLOYEE"})
    client.post("/role/", json={"name": "CUSTOMER"})
    client.post("/user/", json={"name": "User", "phone_number": "3133333333", "email": "SomeEmail@Mail.com", "username":"user","password": "123","address": "Somewhere","enabled": True, "role_ids": [1]})
    client.post("/user/", json={"name": "User", "phone_number": "3143333333", "email": "SomeEmail2@Mail.com", "username":"user2","password": "123","address": "Somewhere2","enabled": True, "role_ids": [2]})
    client.post("/order/",json={"totalPrice": 20100,"state": "pending","user_id": 1,},)
    client.post("/order/",json={"totalPrice": 20100,"state": "pending","user_id": 2,},)
    client.post("/bill/", json={"totalprice": 1000, "paid": False, "order_id": 1})
    client.post("/bill/", json={"totalprice": 2000, "paid": False, "order_id": 1})
    client.post("/bill/", json={"totalprice": 3000, "paid": False, "order_id": 1})
    client.post("/bill/", json={"totalprice": 4000, "paid": False, "order_id": 2})
    response = client.post("/bill/", json={"totalprice": 5000, "paid": False, "order_id": 2})
    response = client.get("/bill/monthlySalesTotal")
    print(response.json())
    assert response.status_code == 200
    print(response.json())