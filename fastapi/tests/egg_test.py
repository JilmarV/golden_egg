"""Test cases for Egg endpoints."""

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


def test_create_egg(client):
    """Test creating an egg."""
    response = client.post(
        "/egg/",
        json={
            "type_egg": "Chicken",
            "color": "White",
            "expirationDate": "2025-01-01",
            "category": "Type 1",
            "supplier_id": 1,
            "inventory_id": 1
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["type_egg"] == "Chicken"
    assert data["color"] == "White"
    assert data["expirationDate"] == "2025-01-01"
    assert data["category"] == "Type 1"
    assert "id" in data


def test_read_eggs(client):
    """Test retrieving all eggs."""
    client.post(
        "/egg/",
        json={
            "type_egg": "Chicken",
            "color": "White",
            "expirationDate": "2025-02-01",
            "category": "Type 2",
            "supplier_id": 1,
            "inventory_id": 1
        }
    )
    response = client.get("/egg/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0


def test_read_egg(client):
    """Test retrieving a specific egg."""
    create_response = client.post(
        "/egg/",
        json={
            "type_egg": "Chicken",
            "color": "White",
            "expirationDate": "2025-03-01",
            "category": "Type 3",
            "supplier_id": 1,
            "inventory_id": 1
        }
    )
    created_egg = create_response.json()
    response = client.get(f"/egg/{created_egg['id']}")
    assert response.status_code == 200
    data = response.json()
    assert data["type_egg"] == "Chicken"
    assert data["color"] == "White"
    assert data["expirationDate"] == "2025-03-01"
    assert data["category"] == "Type 3"


def test_update_egg(client):
    """Test updating an egg."""
    create_response = client.post(
        "/egg/",
        json={
            "type_egg": "Chicken",
            "color": "White",
            "expirationDate": "2025-04-01",
            "category": "Type 4",
            "supplier_id": 1,
            "inventory_id": 1
        }
    )
    created_egg = create_response.json()
    response = client.put(
        f"/egg/{created_egg['id']}",
        json={
            "type_egg": "Chicken",
            "color": "White",
            "expirationDate": "2025-05-01",
            "category": "Type 5",
            "supplier_id": 1,
            "inventory_id": 1
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["type_egg"] == "Chicken"
    assert data["color"] == "White"
    assert data["expirationDate"] == "2025-05-01"
    assert data["category"] == "Type 5"


def test_delete_egg(client):
    """Test deleting an egg."""
    create_response = client.post(
        "/egg/",
        json={
            "type_egg": "Chicken",
            "color": "White",
            "expirationDate": "2025-06-01",
            "category": "Type 6",
            "supplier_id": 1,
            "inventory_id": 1
        }
    )
    created_egg = create_response.json()
    response = client.delete(f"/egg/{created_egg['id']}")
    assert response.status_code == 200
    get_response = client.get(f"/egg/{created_egg['id']}")
    assert get_response.status_code == 404
