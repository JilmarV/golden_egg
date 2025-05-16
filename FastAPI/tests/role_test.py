"""Test cases for Role endpoints."""

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


def test_create_role(client):
    """Test creating a role."""
    response = client.post("/role/", json={"name": "Admin"})
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Admin"


def test_get_role(client):
    """Test getting a role."""
    # First, create a role
    response = client.post("/role/", json={"name": "User"})
    assert response.status_code == 201
    role_id = response.json()["id"]

    # Now, get the role
    response = client.get(f"/role/{role_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "User"


def test_get_all_roles(client):
    """Test getting all roles."""
    # Create some roles
    client.post("/role/", json={"name": "Admin"})
    client.post("/role/", json={"name": "User"})

    # Get all roles
    response = client.get("/role/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2


def test_update_role(client):
    """Test updating a role."""
    # First, create a role
    response = client.post("/role/", json={"name": "User"})
    assert response.status_code == 201
    role_id = response.json()["id"]
    # Now, update the role
    response = client.put(f"/role/{role_id}", json={"name": "SuperUser"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "SuperUser"


def test_delete_role(client):
    """Test deleting a role."""
    # First, create a role
    response = client.post("/role/", json={"name": "User"})
    assert response.status_code == 201
    role_id = response.json()["id"]
    # Now, delete the role
    response = client.delete(f"/role/{role_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Role deleted successfully"
