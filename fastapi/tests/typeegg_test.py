"""Test cases for TypeEgg endpoints."""

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

# In-memory database for testing
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


def test_create_type_egg(client):
    """Test creating a type egg."""
    response = client.post("/typeEgg/", json={"name": "SupremeEgg"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "SupremeEgg"
    assert "id" in data


def test_read_type_eggs(client):
    """Test retrieving all type eggs."""
    client.post("/typeEgg/", json={"name": "SupremeEgg"})
    response = client.get("/typeEgg/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0


def test_read_type_egg(client):
    """Test retrieving a specific type egg."""
    create_response = client.post("/typeEgg/", json={"name": "SupremeEgg"})
    created_type_egg = create_response.json()
    response = client.get(f"/typeEgg/{created_type_egg['id']}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "SupremeEgg"


def test_update_type_egg(client):
    """Test updating a type egg."""
    create_response = client.post("/typeEgg/", json={"name": "SupremeEgg"})
    created_type_egg = create_response.json()
    response = client.put(
        f"/typeEgg/{created_type_egg['id']}",
        json={"name": "GoldenEgg"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "GoldenEgg"


def test_delete_type_egg(client):
    """Test deleting a type egg."""
    create_response = client.post("/typeEgg/", json={"name": "SupremeEgg"})
    created_type_egg = create_response.json()
    response = client.delete(f"/typeEgg/{created_type_egg['id']}")
    assert response.status_code == 200
    get_response = client.get(f"/typeEgg/{created_type_egg['id']}")
    assert get_response.status_code == 404
