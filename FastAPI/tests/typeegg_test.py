"""Test cases for TypeEgg endpoints."""

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

# In-memory database for testing
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


def test_create_type_egg(_client):
    """Test creating a type egg."""
    response = _client.post("/typeeggs/", json={"name": "SupremeEgg"})
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "SupremeEgg"
    assert "id" in data


def test_read_type_eggs(_client):
    """Test retrieving all type eggs."""
    _client.post("/typeeggs/", json={"name": "SupremeEgg"})
    response = _client.get("/typeeggs/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0


def test_read_type_egg(_client):
    """Test retrieving a specific type egg."""
    create_response = _client.post("/typeeggs/", json={"name": "SupremeEgg"})
    created_type_egg = create_response.json()
    response = _client.get(f"/typeeggs/{created_type_egg['id']}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "SupremeEgg"


def test_update_type_egg(_client):
    """Test updating a type egg."""
    create_response = _client.post("/typeeggs/", json={"name": "SupremeEgg"})
    created_type_egg = create_response.json()
    response = _client.put(
        f"/typeeggs/{created_type_egg['id']}", json={"name": "GoldenEgg"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "GoldenEgg"


def test_delete_type_egg(_client):
    """Test deleting a type egg."""
    create_response = _client.post("/typeeggs/", json={"name": "SupremeEgg"})
    created_type_egg = create_response.json()
    response = _client.delete(f"/typeeggs/{created_type_egg['id']}")
    assert response.status_code == 200
    get_response = _client.get(f"/typeeggs/{created_type_egg['id']}")
    assert get_response.status_code == 404
