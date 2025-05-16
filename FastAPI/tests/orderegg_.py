"""Test cases for Order endpoints."""

# pylint: disable=import-error, no-name-in-module, too-few-public-methods, redefined-outer-name

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

# In-memory database
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


def test_create_orderEgg(client):
    """Test creating an orderEgg."""
    response = client.post(
        "/orderEgg/",
        json={
            "quantity": 30,
            "unit_price": 900,
            "sub_total": 180000,
            "egg_id": 1,
            "order_id": 1
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["quantity"] == 30
    assert data["unit_price"] == 900
    assert data["sub_total"] == 90000
    assert "id" in data
    assert data["order_id"] == 1


def test_get_orderEggs(client):
    """Test retrieving all orderEggs."""
    client.post(
        "/orderEgg/",
        json={
            "quantity": 30,
            "unit_price": 900,
            "sub_total": 180000,
            "egg_id": 1,
            "order_id": 1
        },
    )
    response = client.get("/orderEgg/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_orderEgg(client):
    """Test retrieving a specific orderEgg."""
    response = client.post(
        "/orderEgg/",
        json={
            "quantity": 33,
            "unit_price": 900,
            "sub_total": 180000,
            "egg_id": 1,
            "order_id": 1
        },
    )
    created_orderEgg = response.json()
    response = client.get(f"/orderEgg/{created_orderEgg['id']}")
    assert response.status_code == 200
    data = response.json()
    assert data["quantity"] == 33


def test_update_orderEgg(client):
    """Test updating an orderEgg."""
    response = client.post(
        "/orderEgg/",
        json={
            "quantity": 33,
            "unit_price": 900,
            "sub_total": 180000,
            "egg_id": 1,
            "order_id": 1
        },
    )
    created_orderEgg = response.json()
    response = client.put(
        f"/orderEgg/{created_orderEgg['id']}",
        json={
            "quantity": 44,
            "unit_price": 180,
            "sub_total": 240000,
            "egg_id": 1,
            "order_id": 1
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["quantity"] == 44
    assert data["unit_price"] == 180
    assert data["sub_total"] == 240000


def test_delete_orderEgg(client):
    """Test deleting an orderEgg."""
    response = client.post(
        "/orderEgg/",
        json={
            "quantity": 44,
            "unit_price": 180,
            "sub_total": 240000,
            "egg_id": 1,
            "order_id": 1
        },
    )
    created_orderEgg = response.json()
    response = client.delete(f"/orderEgg/{created_orderEgg['id']}")
    assert response.status_code == 200
    get_response = client.get(f"/orderEgg/{created_orderEgg['id']}")
    assert get_response.status_code == 404
