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
from app.main import app
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
    response = client.post("/supplier/", json={"name": "Supplier2", "address": "Somewhere"})
    print(response.json())
    response = client.post("/typeeggs/", json={"name": "SupremeEgg"})
    print(response.json())
    response = client.post(
        "/egg/",
        json={
            "avalibleQuantity": 30,
            "expirationDate": "2026-02-01",
            "entryDate": "2025-05-21",
            "sellPrice": 100,
            "entryPrice": 90,
            "color": "White",
            "type_egg_id": 1,
            "supplier_id": 1
        }
    )
    print(response.json())
    assert response.status_code == 201
    data = response.json()
    assert data["color"] == "White"
    assert data["expirationDate"] == "2026-02-01"
    assert "id" in data


def test_read_eggs(client):
    """Test retrieving all eggs."""
    response = client.post("/supplier/", json={"name": "Supplier2", "address": "Somewhere"})
    response = client.post("/typeeggs/", json={"name": "SupremeEgg"})
    client.post(
        "/egg/",
        json={
            "avalibleQuantity": 30,
            "expirationDate": "2026-02-01",
            "entryDate": "2025-05-21",
            "sellPrice": 100,
            "entryPrice": 90,
            "color": "White",
            "type_egg_id": 1,
            "supplier_id": 1
        }
    )
    response = client.get("/egg/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0


def test_read_egg(client):
    """Test retrieving a specific egg."""
    response = client.post("/supplier/", json={"name": "Supplier2", "address": "Somewhere"})
    response = client.post("/typeeggs/", json={"name": "SupremeEgg"})
    create_response = client.post(
        "/egg/",
        json={
            "avalibleQuantity": 30,
            "expirationDate": "2026-02-01",
            "entryDate": "2025-05-21",
            "sellPrice": 100,
            "entryPrice": 90,
            "color": "White",
            "type_egg_id": 1,
            "supplier_id": 1
        }
    )
    created_egg = create_response.json()
    response = client.get(f"/egg/{created_egg['id']}")
    assert response.status_code == 200
    data = response.json()
    assert data["color"] == "White"
    assert data["expirationDate"] == "2026-02-01"


def test_update_egg(client):
    """Test updating an egg."""
    response = client.post("/supplier/", json={"name": "Supplier2", "address": "Somewhere"})
    response = client.post("/typeeggs/", json={"name": "SupremeEgg"})
    create_response = client.post(
        "/egg/",
        json={
            "avalibleQuantity": 30,
            "expirationDate": "2026-02-01",
            "entryDate": "2025-05-21",
            "sellPrice": 100,
            "entryPrice": 90,
            "color": "White",
            "type_egg_id": 1,
            "supplier_id": 1
        }
    )
    created_egg = create_response.json()
    response = client.put(
        f"/egg/{created_egg['id']}",
        json={
            "avalibleQuantity": 90,
            "expirationDate": "2025-09-01",
            "entryDate": "2025-05-21",
            "sellPrice": 900,
            "entryPrice": 9000,
            "color": "Brown",
            "type_egg_id": 1,
            "supplier_id": 1
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["color"] == "Brown"
    assert data["expirationDate"] == "2025-09-01"


def test_delete_egg(client):
    """Test deleting an egg."""
    response = client.post("/supplier/", json={"name": "Supplier2", "address": "Somewhere"})
    print(response.json())
    response = client.post("/typeeggs/", json={"name": "SupremeEgg"})
    print(response.json())
    create_response = client.post(
        "/egg/",
        json={
            "avalibleQuantity": 30,
            "expirationDate": "2026-02-01",
            "entryDate": "2025-05-21",
            "sellPrice": 100,
            "entryPrice": 90,
            "color": "White",
            "type_egg_id": 1,
            "supplier_id": 1
        }
    )
    created_egg = create_response.json()
    response = client.delete(f"/egg/{created_egg['id']}")
    assert response.status_code == 200
    get_response = client.get(f"/egg/{created_egg['id']}")
    assert get_response.status_code == 404

def test_get_egg_stock(client):
    """Test retrieving all eggs."""
    client.post("/supplier/", json={"name": "Supplier2", "address": "Somewhere"})
    client.post("/typeeggs/", json={"name": "SupremeEgg"})
    client.post("/typeeggs/", json={"name": "AA"})
    response = client.post(
        "/egg/",
        json={
            "avalibleQuantity": 30,
            "expirationDate": "2026-02-01",
            "entryDate": "2025-05-21",
            "sellPrice": 100,
            "entryPrice": 90,
            "color": "White",
            "type_egg_id": 2,
            "supplier_id": 1
        }
    )
    assert response.status_code == 201
    response = client.post(
        "/egg/",
        json={
            "avalibleQuantity": 91,
            "expirationDate": "2026-02-01",
            "entryDate": "2025-05-21",
            "sellPrice": 100,
            "entryPrice": 90,
            "color": "White",
            "type_egg_id": 1,
            "supplier_id": 1
        }
    )
    assert response.status_code == 201
    response = client.get("/egg/search/stock/1")
    data = response.json()
    print(data)
    assert len(data) == 1

def test_get_month_egg(client):
    """Test retrieving all eggs."""
    client.post("/supplier/", json={"name": "Supplier2", "address": "Somewhere"})
    client.post("/typeeggs/", json={"name": "SupremeEgg"})
    response = client.post(
        "/egg/",
        json={
            "avalibleQuantity": 30,
            "expirationDate": "2026-02-01",
            "entryDate": "2025-05-21",
            "sellPrice": 100,
            "entryPrice": 90,
            "color": "White",
            "type_egg_id": 1,
            "supplier_id": 1
        }
    )
    assert response.status_code == 201
    response = client.post(
        "/egg/",
        json={
            "avalibleQuantity": 91,
            "expirationDate": "2026-02-01",
            "entryDate": "2025-05-21",
            "sellPrice": 100,
            "entryPrice": 90,
            "color": "White",
            "type_egg_id": 1,
            "supplier_id": 1
        }
    )
    assert response.status_code == 201
    response = client.get("/egg/search/count_this_month")
    data = response.json()
    print(data)
    assert data >= 2