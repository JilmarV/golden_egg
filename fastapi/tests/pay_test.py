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
from fastapi.app.main import app
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
    response = client.post(
        "/pay/",json={"amount_paid": 20000,"payment_method": "cash", "user_id": 1,"bill_id": 1},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["amount_paid"] == 20000
    assert data["payment_method"] == "cash"
    assert data["user_id"] == 1
    assert data["bill_id"] == 1
    assert "id" in data
    
    
def test_read_pays(client):
    """Test retrieving all pays."""
    client.post(
        "/pay/",json={"amount_paid": 20000,"payment_method": "cash", "user_id": 1,"bill_id": 1},
    )
    response = client.get("/pay/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["amount_paid"] == 20000
    assert data[0]["payment_method"] == "cash"
    
    
def test_read_pay(client):
    """Test retrieving a specific pay."""
    create_response = client.post(
        "/pay/",json={"amount_paid": 20000,"payment_method": "cash", "user_id": 1,"bill_id": 1},
    )
    created_pay = create_response.json()
    response = client.get(f"/pay/{created_pay['id']}")
    assert response.status_code == 200
    data = response.json()
    assert data["amount_paid"] == 20000
    assert data["payment_method"] == "cash"
    

def test_update_pay(client):
    """Test updating a pay."""
    create_response = client.post(
        "/pay/",json={"amount_paid": 20000,"payment_method": "cash", "user_id": 1,"bill_id": 1},
    )
    created_pay = create_response.json()
    response = client.put(
        f"/pay/{created_pay['id']}",
        json={"amount_paid": 30000,"payment_method": "credit_card", "user_id": 2,"bill_id": 2},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["amount_paid"] == 30000
    assert data["payment_method"] == "credit_card"


def test_delete_pay(client):
    """Test deleting a pay."""
    create_response = client.post(
        "/pay/",json={"amount_paid": 20000,"payment_method": "cash", "user_id": 1,"bill_id": 1},
    )
    created_pay = create_response.json()
    response = client.delete(f"/pay/{created_pay['id']}")
    assert response.status_code == 200
    get_response = client.get(f"/pay/{created_pay['id']}")
    assert get_response.status_code == 404