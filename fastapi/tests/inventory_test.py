"""Test cases for Inventory endpoints."""

# pylint: disable=import-error, no-name-in-module, too-few-public-methods, redefined-outer-name

# Standard library
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Third-party
import pytest
from fastapi.testclient import TestClient

# Application
from fastapi.app.main import app
from app.db.database import Base
from app.db.session import get_db

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


def test_create_inventory(client):
    """Test creating an inventory item."""
    response = client.post(
        "/inventory/",
        json={
            "nameProduct": "Product",
            "availableQuantity": 10,
            "price": 100,
            "expirationDate": "2025-01-01"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["nameProduct"] == "Product"
    assert data["availableQuantity"] == 10
    assert data["price"] == 100
    assert data["expirationDate"] == "2025-01-01"
    assert "id" in data


def test_read_inventory_list(client):
    """Test retrieving all inventory items."""
    client.post(
        "/inventory/",
        json={
            "nameProduct": "Product",
            "availableQuantity": 10,
            "price": 100,
            "expirationDate": "2025-02-01"
        }
    )
    response = client.get("/inventory/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0


def test_read_inventory(client):
    """Test retrieving a specific inventory item."""
    create_response = client.post(
        "/inventory/",
        json={
            "nameProduct": "Product",
            "availableQuantity": 10,
            "price": 100,
            "expirationDate": "2025-03-01"
        }
    )
    created_item = create_response.json()
    response = client.get(f"/inventory/{created_item['id']}")
    assert response.status_code == 200
    data = response.json()
    assert data["nameProduct"] == "Product"


def test_update_inventory(client):
    """Test updating an inventory item."""
    create_response = client.post(
        "/inventory/",
        json={
            "nameProduct": "Product",
            "availableQuantity": 10,
            "price": 100,
            "expirationDate": "2025-04-01"
        }
    )
    created_item = create_response.json()
    response = client.put(
        f"/inventory/{created_item['id']}",
        json={
            "nameProduct": "Updated Product",
            "availableQuantity": 15,
            "price": 150,
            "expirationDate": "2025-05-01"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["nameProduct"] == "Updated Product"
    assert data["availableQuantity"] == 15
    assert data["price"] == 150


def test_delete_inventory(client):
    """Test deleting an inventory item."""
    create_response = client.post(
        "/inventory/",
        json={
            "nameProduct": "Product to Delete",
            "availableQuantity": 5,
            "price": 80,
            "expirationDate": "2025-06-01"
        }
    )
    created_item = create_response.json()
    response = client.delete(f"/inventory/{created_item['id']}")
    assert response.status_code == 200
    get_response = client.get(f"/inventory/{created_item['id']}")
    assert get_response.status_code == 404
