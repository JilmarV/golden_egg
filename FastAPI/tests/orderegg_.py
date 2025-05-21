"""Test cases for Order endpoints."""

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


def test_create_order_egg(_client):
    """Test creating an orderEgg."""
    response = _client.post(
        "/orderEgg/",
        json={
            "quantity": 30,
            "unit_price": 900,
            "sub_total": 180000,
            "egg_id": 1,
            "order_id": 1,
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["quantity"] == 30
    assert data["unit_price"] == 900
    assert data["sub_total"] == 90000
    assert "id" in data
    assert data["order_id"] == 1


def test_get_order_eggs(_client):
    """Test retrieving all orderEggs."""
    _client.post(
        "/orderEgg/",
        json={
            "quantity": 30,
            "unit_price": 900,
            "sub_total": 180000,
            "egg_id": 1,
            "order_id": 1,
        },
    )
    response = _client.get("/orderEgg/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_order_egg(_client):
    """Test retrieving a specific orderEgg."""
    response = _client.post(
        "/orderEgg/",
        json={
            "quantity": 33,
            "unit_price": 900,
            "sub_total": 180000,
            "egg_id": 1,
            "order_id": 1,
        },
    )
    created_order_egg = response.json()
    response = _client.get(f"/orderEgg/{created_order_egg['id']}")
    assert response.status_code == 200
    data = response.json()
    assert data["quantity"] == 33


def test_update_order_egg(_client):
    """Test updating an orderEgg."""
    response = _client.post(
        "/orderEgg/",
        json={
            "quantity": 33,
            "unit_price": 900,
            "sub_total": 180000,
            "egg_id": 1,
            "order_id": 1,
        },
    )
    created_order_egg = response.json()
    response = _client.put(
        f"/orderEgg/{created_order_egg['id']}",
        json={
            "quantity": 44,
            "unit_price": 180,
            "sub_total": 240000,
            "egg_id": 1,
            "order_id": 1,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["quantity"] == 44
    assert data["unit_price"] == 180
    assert data["sub_total"] == 240000


def test_delete_order_egg(_client):
    """Test deleting an orderEgg."""
    response = _client.post(
        "/orderEgg/",
        json={
            "quantity": 44,
            "unit_price": 180,
            "sub_total": 240000,
            "egg_id": 1,
            "order_id": 1,
        },
    )
    created_order_egg = response.json()
    response = _client.delete(f"/orderEgg/{created_order_egg['id']}")
    assert response.status_code == 200
    get_response = _client.get(f"/orderEgg/{created_order_egg['id']}")
    assert get_response.status_code == 404
