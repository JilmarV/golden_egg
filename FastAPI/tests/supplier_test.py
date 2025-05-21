"""Test cases for Supplier endpoints."""

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
def _test_db():
    """Creates a fresh database for each test."""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def _client(_test_db):
    """Overrides the dependency to use the test database."""

    def override_get_db():
        yield _test_db

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


def test_create_supplier(_client):
    """Test creating a supplier."""
    response = _client.post(
        "/supplier/", json={"name": "Supplier2", "address": "Somewhere"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Supplier2"


def test_get_supplier(_client):
    """Test getting a supplier."""
    # First, create a supplier
    response = _client.post(
        "/supplier/", json={"name": "Supplier", "address": "Someplace"}
    )
    assert response.status_code == 201
    supplier_id = response.json()["id"]

    # Now, get the supplier
    response = _client.get(f"/supplier/{supplier_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Supplier"


def test_get_all_suppliers(_client):
    """Test getting all suppliers."""
    # Create some suppliers
    _client.post("/supplier/", json={"name": "Supplier1", "address": "Someplace"})
    _client.post("/supplier/", json={"name": "Supplier2", "address": "Somewhere"})

    # Get all suppliers
    response = _client.get("/supplier/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2


def test_update_supplier(_client):
    """Test updating a supplier."""
    # First, create a supplier
    response = _client.post(
        "/supplier/", json={"name": "Supplier1", "address": "Someplace"}
    )
    assert response.status_code == 201
    supplier_id = response.json()["id"]
    # Now, update the supplier
    response = _client.put(
        f"/supplier/{supplier_id}", json={"name": "Supplier2", "address": "Somewhere"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Supplier2"


def test_delete_supplier(_client):
    """Test deleting a supplier."""
    # First, create a supplier
    response = _client.post(
        "/supplier/", json={"name": "Supplier2", "address": "Somewhere"}
    )
    assert response.status_code == 201
    supplier_id = response.json()["id"]
    # Now, delete the supplier
    response = _client.delete(f"/supplier/{supplier_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Supplier deleted successfully"
