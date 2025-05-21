"""Test cases for Role endpoints."""

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


def test_create_role(_client):
    """Test creating a role."""
    response = _client.post("/role/", json={"name": "Admin"})
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Admin"


def test_get_role(_client):
    """Test getting a role."""
    # First, create a role
    response = _client.post("/role/", json={"name": "User"})
    assert response.status_code == 201
    role_id = response.json()["id"]

    # Now, get the role
    response = _client.get(f"/role/{role_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "User"


def test_get_all_roles(_client):
    """Test getting all roles."""
    # Create some roles
    _client.post("/role/", json={"name": "Admin"})
    _client.post("/role/", json={"name": "User"})

    # Get all roles
    response = _client.get("/role/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2


def test_update_role(_client):
    """Test updating a role."""
    # First, create a role
    response = _client.post("/role/", json={"name": "User"})
    assert response.status_code == 201
    role_id = response.json()["id"]
    # Now, update the role
    response = _client.put(f"/role/{role_id}", json={"name": "SuperUser"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "SuperUser"


def test_delete_role(_client):
    """Test deleting a role."""
    # First, create a role
    response = _client.post("/role/", json={"name": "User"})
    assert response.status_code == 201
    role_id = response.json()["id"]
    # Now, delete the role
    response = _client.delete(f"/role/{role_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Role deleted successfully"
