"""Test cases for Supplier endpoints."""

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


def test_create_supplier(client):
    """Test creating a supplier."""
    response = client.post("/supplier/", json={"name": "Supplier2", "address": "Somewhere"})
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Supplier2"


def test_get_supplier(client):
    """Test getting a supplier."""
    # First, create a supplier
    response = client.post("/supplier/", json={"name": "Supplier", "address": "Someplace"})
    assert response.status_code == 201
    supplier_id = response.json()["id"]

    # Now, get the supplier
    response = client.get(f"/supplier/{supplier_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Supplier"


def test_get_all_suppliers(client):
    """Test getting all suppliers."""
    # Create some suppliers
    client.post("/supplier/", json={"name": "Supplier1", "address": "Someplace"})
    client.post("/supplier/", json={"name": "Supplier2", "address": "Somewhere"})

    # Get all suppliers
    response = client.get("/supplier/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2


def test_update_supplier(client):
    """Test updating a supplier."""
    # First, create a supplier
    response = client.post("/supplier/", json={"name": "Supplier1", "address": "Someplace"})
    assert response.status_code == 201
    supplier_id = response.json()["id"]
    # Now, update the supplier
    response = client.put(f"/supplier/{supplier_id}", json={"name": "Supplier2", "address": "Somewhere"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Supplier2"


def test_delete_supplier(client):
    """Test deleting a supplier."""
    # First, create a supplier
    response = client.post("/supplier/", json={"name": "Supplier2", "address": "Somewhere"})
    assert response.status_code == 201
    supplier_id = response.json()["id"]
    # Now, delete the supplier
    response = client.delete(f"/supplier/{supplier_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Supplier deleted successfully"